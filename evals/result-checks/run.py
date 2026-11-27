"""Result checks eval: when a waiting to-do's result seems to have come (its page shows the words, a message shows it),
does the check close it only when it is what was agreed? Made-up cases (cases.json, frozen before the first run) plus
the done-checks sets' live pages (--old). Nothing is read from the web: each case carries what came and the thread.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/result-checks/run.py --model <model> --runs 3
    ... --old                           # also the done-checks listing and status cases, which should still close
    ... --main                          # main's rule: the words found close it, no turn

The turn is the app's own (machine/prompts/result_check.py) and the verdict is kept the way result_checks.settle keeps
it: a close only on "matches" with nothing owed in return (the case's open promises first). README.md has what is
counted."""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))


def ask(base, key, model, effort, prompt):
    """(text, input tokens, output tokens) of one turn."""
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 2000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=120) as r:
                reply = json.load(r)
            usage = reply.get('usage') or {}
            return ''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []), usage.get('input_tokens', 0), usage.get('output_tokens', 0)
        except (OSError, ValueError) as error:  # a busy model is asked again
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def old_cases():
    """The done-checks sets' cases whose page goes live: the words are there and nothing else was agreed. Want: close."""
    out = []
    for name in ('cases.json', 'cases-fresh.json'):
        for c in json.loads((ROOT / 'evals/done-checks' / name).read_text(encoding='utf-8'))['cases']:
            if c['set'] not in ('listing', 'status'):
                continue
            url = re.search(r'(?:https?://)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.example(?:/[^\s,)]*)?', ' '.join(m['body'] for m in c['messages'])).group(0).rstrip('.')
            out.append({'id': 'old-' + c['id'], 'set': 'old-' + c['set'], 'want': 'close', 'done_when': 'It is live at ' + url,
                        'source': 'page', 'url': url, 'promises': [], 'came': ' '.join(c['live']),
                        'thread': [('The owner sent: ' if m.get('own') else f"From {m['from'].split('<')[0].strip()}: ") + m['body'] for m in c['messages']]})
    return out


def parsed(reply):
    start, end = reply.find('{'), reply.rfind('}')
    try:
        found = json.loads(reply[start:end + 1])
    except ValueError:
        return None
    return found if isinstance(found, dict) else None


def outcome(case, found):
    """What the to-do does, as result_checks.settle decides: close, owed, differs, early or unsure."""
    owed = case['promises'][0] if case['promises'] else found['owed']
    if found['state'] == 'matches' and not owed:
        return 'close'
    if found['state'] in ('differs', 'early'):
        return found['state']
    return 'owed' if owed else 'unsure'


def real(case, difference):
    """The named difference is one the case has: every token of one of its token sets is in it."""
    text = difference.lower()
    return any(all(t in text for t in tokens) for tokens in case.get('difference') or [])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--cases', default='cases.json')
    p.add_argument('--old', action='store_true')
    p.add_argument('--main', action='store_true', help="main's rule: the words found close it")
    p.add_argument('--out', help='write every reply and score here (JSON)')
    a = p.parse_args()
    from machine.prompts.result_check import result_check_prompt, verdict
    cases = json.loads((HERE / a.cases).read_text(encoding='utf-8')) + (old_cases() if a.old else [])
    base, key = os.environ.get('OPENAI_BASE_URL', ''), os.environ.get('OPENAI_API_KEY', '')

    def one(case):
        if a.main:
            return {'id': case['id'], 'did': 'close', 'tokens': (0, 0), 'found': None}
        text, tin, tout = ask(base, key, a.model, a.effort, result_check_prompt(case))
        answer = parsed(text)
        found = verdict(answer) if answer is not None else {'state': 'unsure', 'checked': '', 'difference': '', 'owed': ''}
        return {'id': case['id'], 'did': outcome(case, found), 'tokens': (tin, tout), 'found': found, 'reply': text}
    jobs = [c for _ in range(a.runs if not a.main else 1) for c in cases]
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(one, jobs))
    by_id = {c['id']: c for c in cases}
    rows = {}
    for r in results:
        c = by_id[r['id']]
        row = rows.setdefault(c['set'], {'turns': 0, 'closed': 0, 'wrong': 0, 'owed_close': 0, 'differs': 0, 'real': 0, 'did': {}})
        row['turns'] += 1
        row['did'][r['did']] = row['did'].get(r['did'], 0) + 1
        row['closed'] += r['did'] == 'close'
        row['wrong'] += r['did'] == 'close' and c['want'] != 'close'
        row['owed_close'] += r['did'] == 'close' and c['want'] == 'owed'
        if r['found'] and r['found']['state'] == 'differs':
            row['differs'] += 1
            row['real'] += real(c, r['found']['difference'])
    tin = sum(r['tokens'][0] for r in results) / max(len(results), 1)
    tout = sum(r['tokens'][1] for r in results) / max(len(results), 1)
    want_close = sum(rows[s]['turns'] for s in rows if by_id[next(c['id'] for c in cases if c['set'] == s)]['want'] == 'close')
    closed_ok = sum(rows[s]['closed'] for s in rows if by_id[next(c['id'] for c in cases if c['set'] == s)]['want'] == 'close')
    print(json.dumps(rows, indent=1))
    print(f"turns {len(results)} | matching closed {closed_ok}/{want_close} | wrong closes {sum(r['wrong'] for r in rows.values())} | "
          f"closes while owed {sum(r['owed_close'] for r in rows.values())} | differs {sum(r['differs'] for r in rows.values())} "
          f"(real {sum(r['real'] for r in rows.values())}) | tokens in {tin:.0f} out {tout:.0f}")
    if a.out:
        Path(a.out).write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
