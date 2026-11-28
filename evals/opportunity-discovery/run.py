"""Opportunity discovery: does the weekly pass across threads (opportunities.py) find work the existing checks don't?
Made-up Machines, a real model, a second model grades against each corpus's key. Nothing is sent; throwaway stores.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/opportunity-discovery/run.py --model <model> [--judge <model>] \
        [--set held-out] [--runs 2] [--cap 2000000] [--out results.json]

OPENAI_API_KEY is the whole Authorization value. Each Machine is replayed day by day into two stores with the review's
to-dos and promises as the corpus gives them. Once a week (4 weeks) the baseline store runs the stalled-project check
(project_stall: candidates, its real prompt, parse, Store.suggest) and the other store runs the pass as it ships
(App.opportunity_run), whose to-dos later weeks see. Then one grading turn per Machine labels every proposal and every
stalled-project step against the key. A held-out set is refused when its files don't match the FROZEN next to it."""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOW = dt.datetime(2026, 11, 9, 18, tzinfo=dt.timezone.utc)  # a Monday evening
WEEKS = (21, 14, 7, 0)  # the weekly runs, in days before NOW
DROPPED = {}  # {reason: count} of proposals the shipped parse dropped, over the whole run
LABELS = ('match', 'new_valuable', 'duplicate', 'restatement', 'stale', 'false', 'cross_area', 'trap')
JUDGE = '''You grade proposals of an assistant that reads its owner's mail. Each message was reviewed one by one already, and the
"existing to-dos" were made from that. A weekly pass then proposes work that only shows by putting separate threads together.
The key lists the planted opportunities (worth proposing) and traps (where nothing should be proposed, with why).
Label each proposal with exactly one of:
- "match": it is (mostly) the same work as a planted opportunity: give its id in "of";
- "new_valuable": not in the key, but genuinely useful, correct, supported by the messages it cites and not covered by an existing to-do;
- "duplicate": the same matter as an existing to-do (give its title in "of") or as an earlier proposal;
- "restatement": it restates one message or one per-message to-do, nothing combined;
- "stale": the matter was settled or over by the proposal's week;
- "false": not supported by the messages, or wrong;
- "cross_area": it joins personal and work matters;
- "trap": it falls into one of the key's traps (give its id in "of").
Also say "work_ok": true when its prepared work would be usable by the owner with at most light edits. It is false when the
work puts something at a time already over by the proposal's week, or writes one message to people of different organizations
(which shows each customer to the others) where one message each was needed.
Answer with one JSON object: {"P1": {"label": "...", "of": "...", "work_ok": true, "why": "a few words"}, ...}

'''


def ask(base, key, model, effort, prompt, spent, cap):
    """(text, input tokens, output tokens). Refuses past the token cap."""
    if spent[0] + spent[1] + len(prompt) // 3 > cap:
        raise SystemExit(f'token cap {cap} reached: {spent}')
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 8000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=240) as r:
                reply = json.load(r)
            used = reply.get('usage') or {}
            spent[0] += used.get('input_tokens', 0)
            spent[1] += used.get('output_tokens', 0)
            return (''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []),
                    used.get('input_tokens', 0), used.get('output_tokens', 0))
        except urllib.error.HTTPError as error:
            if error.code == 400:
                return '', 0, 0
            if attempt == 5:
                raise
            time.sleep(2 ** attempt)
        except (OSError, ValueError) as error:
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def frozen_ok(folder):
    """The held-out files match FROZEN (sha256 per file), written before the first run."""
    frozen = folder.parent / 'FROZEN'  # next to the set: this folder's, or an older set's kept elsewhere
    lines = frozen.read_text().split('\n') if frozen.exists() else []
    want = {k: v for k, v in (reversed(line.split('  ', 1)) for line in lines if '  ' in line) if k.startswith(folder.name + '/')}
    have = {f'{folder.name}/{p.name}': hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('*.json'))}
    return bool(have) and have == want


def at(day, hour=12):
    return (NOW - dt.timedelta(days=day)).replace(hour=hour, minute=0)


def person(pair):
    return f'{pair[0]} <{pair[1]}>'


def timeline(m):
    """[(moment, kind, item)] in order: messages, the review's to-dos and promises just after their message."""
    by_key = {x['key']: x for x in m['messages']}
    out = [(at(x['day'], x.get('hour', 12)), 0, 'message', x) for x in m['messages']]
    for t in m.get('todos', ()):  # the review makes it minutes after its last message comes in
        newest = max((at(by_key[k]['day'], by_key[k].get('hour', 12)) for k in t['evidence'] if k in by_key), default=at(t['day']))
        out.append((max(newest, at(t['day'], 7)) + dt.timedelta(minutes=10), 1, 'todo', t))
    for p in m.get('promises', ()):
        src = by_key[p['message']]
        out.append((at(src['day'], src.get('hour', 12)) + dt.timedelta(minutes=5), 1, 'promise', p))
    return [(w, kind, item) for w, _, kind, item in sorted(out, key=lambda x: (x[0], x[1]))]


class Replay:
    """One store fed a Machine's timeline up to a moment."""

    def __init__(self, m, path, main, timeutil):
        self.m, self.main, self.timeutil = m, main, timeutil
        self.accounts = [{'id': a['id'], 'service': 'gmail', 'boundary': a['boundary'], 'email': a['email']} for a in m['accounts']]
        self.store = main.Store(path)
        self.store.accounts = self.accounts
        self.app = object.__new__(main.App)
        self.app.store, self.app.config = self.store, {'accounts': self.accounts, 'review_worker': {'enabled': True}, 'owner_name': m['owner']['name']}
        self.app.fleet = None
        self.items, self.done, self.ids, self.cards = timeline(m), 0, {}, {}

    def until(self, moment):
        import graph
        while self.done < len(self.items) and self.items[self.done][0] <= moment:
            when, kind, x = self.items[self.done]
            self.done += 1
            self.timeutil.pin(when)
            if kind == 'message':
                meta = {'from': person(x['from']), 'to': ', '.join(person(t) for t in x['to']), 'thread_id': x['thread'],
                        'labels': ['SENT'] if x['from'][1].lower() == self.email(x['account']) else ['INBOX']}
                if x.get('bulk'):
                    meta['list_unsubscribe'] = '<mailto:unsubscribe@list.example>'
                self.store.commit_page(x['account'], {}, [{'account_id': x['account'], 'source_id': x['key'], 'kind': 'gmail.message', 'occurred_at': when.isoformat(),
                                                          'title': x['subject'], 'body': x['body'], 'metadata': meta, 'deleted': False}])
                with self.store.connect() as db:
                    self.ids[x['key']] = db.execute('SELECT id FROM events WHERE source_id=?', (x['key'],)).fetchone()[0]
                    if x.get('project'):
                        graph.label(db, [self.ids[x['key']]], x['project'], 'review', when.isoformat())
                    db.commit()
            elif kind == 'todo':
                ids = [self.ids[k] for k in x['evidence'] if k in self.ids]
                if not ids:
                    continue
                card = self.store.suggest('review:' + x['key'], x['title'], x['title'], ids)
                self.cards[x['key']] = card['id']
                if x['state'] in ('dismissed', 'done'):
                    self.store.decide(card['id'], 'reject' if x['state'] == 'dismissed' else 'complete', '', 'd-' + x['key'], 'dashboard')
            elif kind == 'promise' and x['message'] in self.ids:
                try:
                    made = self.store.promise({'direction': x['direction'], 'who': x['who'], 'what': x['what'][:80], 'event_id': self.ids[x['message']]})
                    if x.get('status', 'open') != 'open':
                        self.store.update_promise({'id': made['id'], 'status': x['status']}, source='dashboard')
                except ValueError:
                    pass
        self.timeutil.pin(moment)
        with self.store.connect() as db:
            graph.build(db, self.app.config, moment.isoformat())
            db.commit()

    def email(self, account):
        return next(a['email'].lower() for a in self.accounts if a['id'] == account)

    def key_of(self, event_id):
        return next((k for k, v in self.ids.items() if v == event_id), f'E{event_id}')


def stall_week(replay, turn):
    """The stalled-project check, as App.stall_run does it, on this week's state: [{'title', 'why', 'sources'}]."""
    import project_stall
    with replay.store.connect() as db:
        run_id = project_stall.begin(db)
        items = project_stall.candidates(db)
        db.commit()
    if not items:
        return [], 0, 0, 0
    used = [0, 0]

    def model(config, text):
        reply, i, o = turn(text)
        used[0] += i
        used[1] += o
        return reply
    replay.app.stall_model = model
    with replay.store.connect() as db:
        before = {r[0] for r in db.execute('SELECT id FROM suggestions')}
    replay.app.stall_run(run_id, items)
    with replay.store.connect() as db:
        rows = [dict(r) for r in db.execute('SELECT id,title,body,event_ids FROM suggestions')]
    made = [{'title': r['title'], 'why': r['body'], 'sources': [replay.key_of(e) for e in json.loads(r['event_ids'])]} for r in rows if r['id'] not in before]
    return made, len(items), used[0], used[1]


def discover_week(replay, turn, moment):
    """The weekly pass as it ships (App.opportunity_run, opportunities.py), its turns through `turn`: (rows, threads read,
    longest prompt, input tokens, output tokens)."""
    import opportunities
    used = [0, 0, 0]

    def model(config, text):
        answer, i, o = turn(text)
        used[0], used[1], used[2] = max(used[0], len(text)), used[1] + i, used[2] + o
        return answer
    replay.app.opportunity_model = model
    replay.app.opportunity_dropped = DROPPED  # the shipped checks' drop reasons, kept over the whole run
    with replay.store.connect() as db:
        run_id = opportunities.begin(db, moment.isoformat(timespec='seconds'))
        before = {r['suggestion_id'] for r in db.execute('SELECT suggestion_id FROM opportunity_items')}
    replay.app.opportunity_run(run_id, moment)
    out = []
    with replay.store.connect() as db:
        read = db.execute('SELECT threads FROM opportunity_runs WHERE id=?', (run_id,)).fetchone()['threads'] or 0
        for item in db.execute('SELECT suggestion_id,threads FROM opportunity_items WHERE run_id=?', (run_id,)).fetchall():
            if item['suggestion_id'] in before:
                continue
            card = db.execute('SELECT title,body,event_ids FROM suggestions WHERE id=?', (item['suggestion_id'],)).fetchone()
            why, _, work = card['body'].partition('\n\n')  # opportunities.body: why, a blank line, the prepared work
            out.append({'title': card['title'], 'why': why, 'work': work, 'sources': [replay.key_of(e) for e in json.loads(card['event_ids'] or '[]')],
                        'threads': len(json.loads(item['threads']))})
    return out, read, used[0], used[1], used[2]


def grade(m, rows, judge):
    """{label id: verdict} for every proposal and stall step in rows."""
    if not rows:
        return {}
    by_key = {x['key']: x for x in m['messages']}
    area = {a['id']: a['boundary'].split(':')[0] for a in m['accounts']}
    cite = lambda k: (f"{k} [{area.get(by_key[k]['account'])}, day -{by_key[k]['day']}, thread {by_key[k]['thread']}, from {by_key[k]['from'][0]}] {by_key[k]['subject']}"
                      if k in by_key else k)
    key = json.dumps(m['key'], ensure_ascii=False, indent=1)
    todos = '\n'.join(f"- [{t['state']}, day -{t['day']}] {t['title']}" for t in m.get('todos', ()))
    props = '\n\n'.join(f"P{n} (week ending day -{r['week']}): {r['title']}\nWhy: {r['why']}\nWork: {r.get('work', '')}\nCites:\n" +
                        '\n'.join('  ' + cite(k) for k in r['sources']) for n, r in enumerate(rows, 1))
    messages = '\n'.join(f"{x['key']} | {area.get(x['account'])} | day -{x['day']} | {x['thread']} | {x['from'][0]} | {x['subject']} | {' '.join(x['body'].split())[:160]}"
                         for x in m['messages'] if not x.get('bulk'))
    reply = judge(JUDGE + f'Key:\n{key}\n\nExisting to-dos:\n{todos}\n\nMessages (shortened):\n{messages}\n\nProposals:\n{props}')
    try:
        return json.loads(reply[reply.find('{'):reply.rfind('}') + 1])
    except ValueError:
        return {}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--judge', default='')
    p.add_argument('--effort', default='low')
    p.add_argument('--set', default='development')
    p.add_argument('--only', default='')
    p.add_argument('--runs', type=int, default=1)
    p.add_argument('--cap', type=int, default=2_000_000)
    p.add_argument('--out', default='')
    p.add_argument('--root', default=str(HERE.parent.parent))
    p.add_argument('--show', action='store_true', help='print the turns, ask nothing')
    a = p.parse_args()
    folder = Path(a.set) if '/' in a.set else HERE / a.set
    if a.set.startswith('held-out') and not frozen_ok(folder):
        raise SystemExit('held-out files differ from FROZEN')
    sys.path.insert(0, a.root)
    sys.path.insert(0, str(HERE))
    import locale_prefs
    import machine.main as main_module
    timeutil = sys.modules['timeutil']  # the checkout's, loaded by machine.main (as evals/ask-questions/run.py)
    local = timeutil.clock(timeutil.local_tz())
    if 1.5 <= local.hour + local.minute / 60 < 3.5:  # the nightly setup runs then
        raise SystemExit('not between 01:30 and 03:30')
    timeutil.LOCAL_TZ = dt.timezone.utc
    locale_prefs._current.update(locale='en-US', language='en')
    spent = [0, 0]
    if a.show:
        turn = lambda t: (print(t[:6000], '\n=====\n'), ('{"proposals": [], "steps": []}', 0, 0))[1]
        judge = lambda t: '{}'
    else:
        base, key = os.environ['OPENAI_BASE_URL'].rstrip('/'), os.environ['OPENAI_API_KEY']
        turn = lambda t: ask(base, key, a.model, a.effort, t, spent, a.cap)
        judge = lambda t: ask(base, key, a.judge or a.model, 'low', t, spent, a.cap)[0]
    machines = [json.loads(f.read_text()) for f in sorted(folder.glob('*.json')) if not a.only or f.stem in a.only.split(',')]
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for run in range(a.runs):
            for m in machines:
                base_r = Replay(m, Path(tmp) / f'{m["id"]}-{run}-base.sqlite', main_module, timeutil)
                exp_r = Replay(m, Path(tmp) / f'{m["id"]}-{run}-exp.sqlite', main_module, timeutil)
                rows, cost = [], {'discover_in': 0, 'discover_out': 0, 'stall_in': 0, 'stall_out': 0, 'turns': 0, 'groups': 0, 'chars': 0}
                for week in WEEKS:
                    moment = NOW - dt.timedelta(days=week)
                    for r in (base_r, exp_r):
                        r.until(moment)
                    steps, candidates, si, so = stall_week(base_r, turn)
                    rows += [dict(s, arm='stall', week=week) for s in steps]
                    found, groups, chars, di, do = discover_week(exp_r, turn, moment)
                    rows += [dict(f, arm='discover', week=week) for f in found]
                    cost['stall_in'] += si
                    cost['stall_out'] += so
                    cost['discover_in'] += di
                    cost['discover_out'] += do
                    cost['pass_in'] = max(cost.get('pass_in', 0), di)
                    cost['turns'] += bool(groups) + bool(candidates)
                    cost['groups'] += groups
                    cost['chars'] = max(cost['chars'], chars)
                verdicts = grade(m, rows, judge) if not a.show else {}
                for n, r in enumerate(rows, 1):
                    r['verdict'] = verdicts.get(f'P{n}') or {}
                results.append({'machine': m['id'], 'run': run, 'rows': rows, 'cost': cost, 'opportunities': [o['id'] for o in m['key']['opportunities']]})
                print(m['id'], run, json.dumps(cost), flush=True)
    summary = summarize(results)
    summary['dropped'] = DROPPED
    print(json.dumps(summary, indent=1))
    print('tokens', spent)
    if a.out:
        Path(a.out).write_text(json.dumps({'summary': summary, 'tokens': spent, 'results': results}, ensure_ascii=False, indent=1))


def summarize(results):
    out = {}
    for arm in ('discover', 'stall'):
        labels, found, total, ok, weekly = {}, set(), set(), 0, []
        for res in results:
            total |= {(res['machine'], res['run'], o) for o in res['opportunities']}
            per_week = {}
            for r in res['rows']:
                if r['arm'] != arm:
                    continue
                v = r['verdict']
                label = v.get('label') or 'ungraded'
                labels[label] = labels.get(label, 0) + 1
                ok += bool(v.get('work_ok'))
                per_week[r['week']] = per_week.get(r['week'], 0) + 1
                if label == 'match' and v.get('of') in res['opportunities']:
                    found.add((res['machine'], res['run'], v['of']))
            weekly.append(max(per_week.values(), default=0))
        n = sum(labels.values())
        good = labels.get('match', 0) + labels.get('new_valuable', 0)
        quiet = sum(1 for res in results if not res['opportunities'] for r in res['rows'] if r['arm'] == arm)
        out[arm] = {'proposals': n, 'labels': labels, 'opportunities_found': len(found), 'opportunities': len(total),
                    'precision': round(good / n, 2) if n else None, 'work_ok': ok, 'most_in_a_week': max(weekly, default=0),
                    'on_quiet_machines': quiet, 'most_input_per_pass': max((res['cost'].get('pass_in', 0) for res in results), default=0)}
        bad = labels.get('trap', 0) + labels.get('false', 0)
        out[arm]['bar'] = {  # README.md: Bar
            'quiet': quiet == 0, 'trap_or_false': bad == 0, 'right': bool(n) and good / n >= 0.85,
            'found': bool(total) and len(found) / len(total) >= 0.5, 'duplicates': labels.get('duplicate', 0) <= 0.1 * n,
            'work_and_personal': labels.get('cross_area', 0) == 0, 'light_edits': n - ok <= 0.1 * n,
            'tokens': out[arm]['most_input_per_pass'] <= 20_000, 'most_two_a_week': out[arm]['most_in_a_week'] <= 2}
        out[arm]['passes'] = all(out[arm]['bar'].values())
    return out


if __name__ == '__main__':
    main()
