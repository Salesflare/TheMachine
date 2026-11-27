"""Runs the made-up friends in cases.json through the real Stay in touch template (stay_in_touch.py, stay_in_touch_app.py)
day by day with a real model: a throwaway store, the routine run each morning, the messages, facts and page summaries
arriving on their own day, and a model judging each nudge against what really happened. No message is sent.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/stay-in-touch/run.py --model <model> [--set held-out] [--root <another checkout>]

The environment is that of evals/family-questions/run.py. --root: the code whose nudges are judged, so a branch and main
run on the same cases. README.md has what they test."""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
START = dt.datetime(2026, 11, 9, 7, 30, tzinfo=dt.timezone.utc)  # day 0, a Monday morning
ACCOUNTS = [{'id': 'wa', 'service': 'whatsapp', 'boundary': 'personal'},
            {'id': 'job', 'service': 'gmail', 'boundary': 'work:Larkspur', 'email': 'robin@larkspur.example'}]
SIDES = {'wa': 'personal', 'job': 'work'}
JUDGE = ('A personal assistant suggested its owner check in with a friend, for this reason:\n<<<{reason}>>>\nIt was suggested on {day}. '
         'What really happened: {truth}\nAnswer with one JSON object: {{"on_topic": true or false, "wrong": true or false}}. on_topic: the '
         'reason is about {expect}. wrong: the reason states or assumes something that is not so on that day (it asks how something went '
         'that has not happened yet or was called off, has an old date, or guesses at health or feelings the friend never shared).')


def ask(base, key, model, effort, prompt):
    """(text, input tokens, output tokens) of one turn."""
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 4000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=180) as r:
                reply = json.load(r)
            used = reply.get('usage') or {}
            return (''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []),
                    used.get('input_tokens', 0), used.get('output_tokens', 0))
        except urllib.error.HTTPError as error:
            if error.code == 400 or attempt == 5:
                raise
            time.sleep(2 ** attempt)
        except (OSError, ValueError) as error:
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def simulate(case, spec):
    """The case's days from 0 to its last: what happened that day goes in first, then the morning's run.
    {'nudges': [(day, reason)], 'calls': n, 'tokens': [in, out]}."""
    sys.path[:0] = [spec['root'], spec['root'] + '/tests']
    import graph
    import machine.main as main
    import person_summary
    import routine_templates
    from pinned import pinned
    folder = tempfile.TemporaryDirectory()
    store = main.Store(Path(folder.name) / 'e.sqlite')
    store.accounts = ACCOUNTS
    app = object.__new__(main.App)
    app.store, app.config = store, {'accounts': ACCOUNTS, 'timezone': 'Europe/Brussels', 'openclaw_state': folder.name + '/none.sqlite'}
    for name, value in (('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                        ('preparation_gateway', lambda s, request: {}), ('routine_spawn', lambda s, target, run_id: target(run_id))):
        mock.patch.object(main.App, name, value).start()
    used = {'calls': 0, 'in': 0, 'out': 0}

    def model(prompt):
        text, tin, tout = ask(spec['base'], spec['key'], spec['model'], spec['effort'], prompt)
        used['calls'] += 1
        used['in'] += tin
        used['out'] += tout
        return text
    app.touch_model = model
    person, number = case['person'], '15550100'
    node, ids, n = 'wa:' + number, [], [0]

    def chat(day, mine, text, account='wa'):
        """One message, stored the way its connector stores it; its id."""
        n[0] += 1
        at = (START + dt.timedelta(days=day, hours=-12)).isoformat()
        if account == 'wa':
            meta = {'chat_id': number + '@s.whatsapp.net', 'chat_name': person['name'], 'sender': 'me' if mine else number + '@s.whatsapp.net',
                    'sender_name': None if mine else person['name'], 'from_me': mine}
        else:
            meta = {'from': f"{person['name']} <{number}@larkspur.example>", 'to': 'robin@larkspur.example', 'labels': ['INBOX'], 'message-id': f'<{n[0]}@x.example>'}
        store.commit_page(account, {}, [{'account_id': account, 'source_id': f's{n[0]}', 'kind': 'whatsapp.message' if account == 'wa' else 'gmail.message',
                                         'occurred_at': at, 'title': person['name'], 'body': text, 'deleted': False, 'metadata': meta}])
        with store.connect() as db:
            return db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account, f's{n[0]}')).fetchone()['id']

    def build():
        with store.connect() as db:
            db.isolation_level = None
            graph.build(db, app.config, clock.at.isoformat())

    with pinned(START + dt.timedelta(days=person['first'])) as clock:
        with store.connect() as db:
            graph.ensure(db)
        for i, day in enumerate(range(person['first'], person['last'] + 1, person.get('every', 7))):
            clock.move(seconds=((START + dt.timedelta(days=day)) - clock.at).total_seconds())
            chat(day, i % 2 == 0, ('Hi! How are things?', 'All good here, busy week', 'Coffee soon?', 'Sure, let me know')[i % 4])
        chat(person['last'], True, 'Talk soon!')
        clock.move(seconds=((START + dt.timedelta(days=person['last'] + 1)) - clock.at).total_seconds())
        build()
        app.action('touch_people', {'add': node}, owner_dashboard=True)
        events = {}
        happens = sorted([(m['day'], 0, i, m) for i, m in enumerate(case.get('messages') or ())] +
                         [(f['day'], 1, i, f) for i, f in enumerate(case.get('facts') or ())] +
                         [(s['day'], 2, i, s) for i, s in enumerate(case.get('summaries') or ())], key=lambda x: x[:3])
        nudges, seen, first = [], set(), True
        for day in range(min([h[0] for h in happens] + [0]), case.get('days', 40) + 1):
            if clock.at < START + dt.timedelta(days=day):
                clock.move(seconds=((START + dt.timedelta(days=day)) - clock.at).total_seconds())
            today = [h for h in happens if h[0] == day]
            for _, what, i, item in today:
                if what == 0:
                    events[i] = chat(day, item['from'] == 'owner', item['text'], item.get('account', 'wa'))
                elif what == 1:
                    store.fact_add(node, item['text'])  # the owner adds it on their page
                else:
                    lines = [{'kind': line.get('kind', 'now'), 'text': line['text'],
                              'sources': ['ai'] if line.get('ai') else [f'E{events[c]}' for c in line['cites']]} for line in item['lines']]
                    with store.connect() as db:
                        person_summary.save(db, node, lines, clock.at.isoformat(), SIDES)
                if what == 0 and i == max(j for _, w, j, _ in today if w == 0):
                    build()  # the Graph takes in the day's messages
            if day < 0:
                continue
            with store.connect() as db:
                routine = routine_templates.live(db, 'touch')
            if first:
                app.action('routine_template', {'key': 'touch'}, owner_dashboard=True)
                first = False
            else:
                app.action('routine_run_now', {'id': routine['id']}, owner_dashboard=True)
            for _ in range(3):
                app.routines_step()
                with store.connect() as db:
                    if not db.execute("SELECT 1 FROM routine_runs WHERE state='running'").fetchone():
                        break
            with store.connect() as db:
                for row in db.execute("SELECT id,body FROM suggestions WHERE dedupe_key LIKE 'touch:%' ORDER BY created_at"):
                    if row['id'] not in seen:
                        seen.add(row['id'])
                        nudges.append((day, row['body'].split('\n')[0]))
    mock.patch.stopall()
    folder.cleanup()
    return {'nudges': nudges, 'calls': used['calls'], 'tokens': [used['in'], used['out']]}


def work(args):
    case, spec = args
    try:
        return case, simulate(case, spec)
    except Exception as error:
        return case, {'error': f'{type(error).__name__}: {error}'[:300]}


def judge(case, day, reason, spec):
    on = (START + dt.timedelta(days=day)).date().isoformat()
    text, _, _ = ask(spec['base'], spec['key'], spec['judge'], 'low', JUDGE.format(reason=reason, day=on, truth=case['truth'], expect=case.get('expect') or 'nothing in particular'))
    start, end = text.find('{'), text.rfind('}')
    found = json.loads(text[start:end + 1])
    return bool(found.get('on_topic')), bool(found.get('wrong'))


def verdict(case, got, spec):
    """useful | early | late | missed (a nudge case) or quiet | extra (a quiet case); with whether a nudge was wrong."""
    if 'error' in got:
        return 'error', False
    wrong = False
    marks = []
    for day, reason in got['nudges']:
        on_topic, bad = judge(case, day, reason, spec)
        wrong = wrong or bad
        marks.append((day, on_topic, bad))
    got['marks'] = marks
    if case['label'] == 'quiet':
        return ('extra' if marks else 'quiet'), wrong
    if not marks:
        return 'missed', wrong
    day, on_topic, bad = marks[0]
    lo, hi = case['window']
    if day < lo:
        return 'early', wrong
    if day > hi or not on_topic or bad:
        return 'late' if day > hi else 'off', wrong
    return 'useful', wrong


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--judge')
    parser.add_argument('--effort', default='low')
    parser.add_argument('--set', default='development')
    parser.add_argument('--root', default=str(HERE.parent.parent))
    parser.add_argument('--only')
    parser.add_argument('--out')
    args = parser.parse_args()
    spec = {'base': os.environ['OPENAI_BASE_URL'].rstrip('/'), 'key': os.environ['OPENAI_API_KEY'], 'model': args.model,
            'judge': args.judge or args.model, 'effort': args.effort, 'root': str(Path(args.root).resolve())}
    cases = [c for c in json.loads((HERE / 'cases.json').read_text()) if c['set'] == args.set and (not args.only or c['id'] == args.only)]
    with concurrent.futures.ProcessPoolExecutor(4) as pool:
        done = list(pool.map(work, [(c, spec) for c in cases]))
    tally, rows = {}, []
    for case, got in done:
        kind, wrong = verdict(case, got, spec)
        tally[kind] = tally.get(kind, 0) + 1
        tally['wrong'] = tally.get('wrong', 0) + wrong
        for key in ('calls',):
            tally[key] = tally.get(key, 0) + got.get(key, 0)
        tally['tokens_in'] = tally.get('tokens_in', 0) + (got.get('tokens') or [0])[0]
        tally['tokens_out'] = tally.get('tokens_out', 0) + (got.get('tokens') or [0, 0])[1]
        rows.append({'id': case['id'], 'label': case['label'], 'verdict': kind, 'wrong': wrong, **got})
        print(f"{case['id']:28} {case['label']:6} {kind:8} {'WRONG ' if wrong else ''}{got.get('nudges') or got.get('error') or ''} calls={got.get('calls')}", flush=True)
    print(json.dumps(tally, sort_keys=True))
    if args.out:
        Path(args.out).write_text(json.dumps({'tally': tally, 'rows': rows}, indent=1))


if __name__ == '__main__':
    main()
