"""Runs the made-up cases in cases.json through the real pages of the checks that close to-dos and promises by themselves
(handled_check_text, promise_check_text) with a real model. Throwaway store, nothing is closed or sent.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/closing-checks/run.py --model <model> [--runs 3] [--root <another checkout>]

The environment is that of evals/family-questions/run.py. --root: the code whose pages are judged, so a branch and main
run on the same cases. README.md has the sets."""
import argparse
import concurrent.futures
import json
import os
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PER_TURN = 3  # to-dos or promises on one page


def ask(base, key, model, effort, prompt):
    """(text, input tokens) of one turn."""
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 6000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=120) as r:
                reply = json.load(r)
            return ''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []), (reply.get('usage') or {}).get('input_tokens', 0)
        except (OSError, ValueError) as error:  # a busy model is asked again
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def event(case, n, message, text):
    """A case's message as its source stores it."""
    channel = message.get('channel', 'gmail')
    body = message['body']
    for name, filler in text.items():
        body = body.replace('{%s}' % name, filler)
    who = 'Robin Hale' if message.get('own') else message['who']
    meta = {'from': f'{who} <{who.split()[0].lower()}@larkspur.example>', 'labels': ['SENT'] if message.get('own') else ['INBOX'], 'thread_id': case['id']}
    title = message.get('title') or who
    if channel == 'gmail':
        if 'files' in message:  # else a message kept before its files were
            meta['attachments'] = [{'name': f, 'type': 'application/octet-stream'} for f in message['files']]
    elif channel == 'slack':
        meta = {'channel_id': 'D0' + case['id'].upper(), 'channel_name': 'DM', 'user_id': None}
        title = '#DM ' + who + ': ' + body.split('\n')[0][:900]
    else:
        meta = {'chat_id': case['id'], 'from': who, 'from_me': bool(message.get('own'))}
        if channel == 'whatsapp':
            meta['media_type'] = message.get('media', '')
    return {'account_id': 'a', 'source_id': f"{case['id']}-{n}", 'kind': channel + '.message', 'occurred_at': f'2026-03-0{3 + n}T09:00:00+00:00',
            'title': title, 'body': body, 'metadata': meta, 'deleted': False}


def pages(cases, text, folder):
    """[(prompt, its cases)]: the real pages, PER_TURN cases each, to-dos and promises apart."""
    import machine.main as main
    store = main.Store(Path(folder) / 'events.sqlite')
    app = object.__new__(main.App)
    app.store, app.config = store, {'accounts': []}
    out = []
    for kind in ('todo', 'promise'):
        mine = [c for c in cases if c['kind'] == kind]
        for i in range(0, len(mine), PER_TURN):
            group, page = mine[i:i + PER_TURN], []
            for case in group:
                found = []
                for n, message in enumerate(case['since']):
                    store.commit_page('a', {}, [event(case, n, message, text)])
                    with store.connect() as db:
                        row = db.execute('SELECT id,occurred_at FROM events WHERE source_id=?', (f"{case['id']}-{n}",)).fetchone()
                    found.append({'id': row['id'], 'at': row['occurred_at'], 'channel': message.get('channel', 'gmail'), 'where': 'same conversation',
                                  'who': 'the owner' if message.get('own') else message['who']})
                if kind == 'todo':
                    step = case.get('step')
                    page.append(({'id': case['id'], 'title': case['title'], 'next_action': json.dumps(step) if step else None}, found))
                else:
                    page.append(({'id': len(page) + 1, 'who': case['who'], 'what': case['what'], 'direction': case['direction'], 'together': 0,
                                  'made_at': '2026-03-02T09:00:00+00:00', 'due': None, 'alike': []}, found))
            with store.connect() as db:
                out.append((app.handled_check_text(db, page) if kind == 'todo' else app.promise_check_text(db, page), group))
    return out


def answers(reply, group):
    """{case id: done or open}; a case without a readable answer stays open, as in the app."""
    start, end = reply.find('['), reply.rfind(']')
    said = {str(x.get('todo' if group[0]['kind'] == 'todo' else 'promise')): x for x in json.loads(reply[start:end + 1]) if isinstance(x, dict)}
    out = {}
    for n, case in enumerate(group, 1):
        x = said.get(case['id'] if case['kind'] == 'todo' else str(n)) or {}
        out[case['id']] = 'done' if x.get('state') in ('done', 'kept') else 'open'
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--jobs', type=int, default=3)
    p.add_argument('--root', default=str(HERE.parent.parent))
    p.add_argument('--show', action='store_true', help='print the pages, ask nothing')
    a = p.parse_args()
    sys.path.insert(0, a.root)
    spec = json.loads((HERE / 'cases.json').read_text())
    cases = {c['id']: c for c in spec['cases']}
    with tempfile.TemporaryDirectory() as folder:
        turns = pages(spec['cases'], spec['text'], folder)
    if a.show:
        print('\n\n=====\n\n'.join(t for t, _ in turns))
        return
    base, key = os.environ['OPENAI_BASE_URL'].rstrip('/'), os.environ['OPENAI_API_KEY']
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        jobs = [(run, group, pool.submit(ask, base, key, a.model, a.effort, prompt)) for run in range(a.runs) for prompt, group in turns]
        got = [(run, group, *j.result()) for run, group, j in jobs]
    tally, wrong, tokens = {}, {}, 0
    for run, group, reply, used in got:
        tokens += used
        for cid, state in answers(reply, group).items():
            case = cases[cid]
            right, total = tally.get(case['set'], (0, 0))
            tally[case['set']] = (right + (state == case['want']), total + 1)
            if state != case['want']:
                wrong.setdefault(cid, []).append(state)
    for name, (right, total) in tally.items():
        print(f'{name:14} {right} of {total}')
    closed = sum(len(v) for c, v in wrong.items() if cases[c]['want'] == 'open')
    missed = sum(len(v) for c, v in wrong.items() if cases[c]['want'] == 'done')
    print(f'right {sum(r for r, _ in tally.values())} of {sum(t for _, t in tally.values())}; closed wrongly {closed}; left open though done {missed}; '
          f'input tokens per turn {tokens // max(1, len(got))}')
    print('wrong:', ', '.join(f'{c} x{len(v)}' for c, v in sorted(wrong.items())) or 'none')


if __name__ == '__main__':
    main()
