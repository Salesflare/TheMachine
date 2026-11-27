"""Done checks eval: does the review write a page check (done_check) only when the messages give the page, and would the
check close the to-do only once the page really shows the result? Made-up cases (cases.json, frozen before the first
run; cases-fresh.json, a second held-out slice kept for an improvement round). Nothing is read from the web: each case
carries the page's text before and after the result, and the real rules decide (machine/store/done_checks.py).

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/done-checks/run.py --model <model> --runs 3
    ... --root <another checkout>      # that code's review prompt (its "Done when:" part), the same rules to score it
    ... --cases cases-fresh.json

The prompt is the review prompt's own "Done when:" paragraph with the case's messages, asking for suggest's arguments:
the part of the review that writes a done when and its check, not a whole review. README.md has what is counted."""
import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def ask(base, key, model, effort, prompt):
    """(text, input tokens, output tokens) of one turn."""
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 4000}
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


def instructions(root):
    """The "Done when:" paragraph of that checkout's review prompt."""
    text = (Path(root) / 'machine/prompts/review.py').read_text(encoding='utf-8')
    line = next(x for x in text.splitlines() if x.startswith("Done when: when a to-do's point"))
    return line.replace('{{', '{').replace('}}', '}')


def prompt(owner, paragraph, case):
    lines = [f"[event {n}] From: {m['from']}{' (sent by the owner)' if m.get('own') else ''}\n{m['body']}" for n, m in enumerate(case['messages'], 1)]
    return (f"{owner}\n\nThis is a signal review. These messages are about one matter the owner already did their part on; "
            'it now waits for someone else. Write the to-do for it with suggest, following this part of your instructions:\n\n'
            f"{paragraph}\n\nMessages, oldest first:\n\n" + '\n\n'.join(lines)
            + '\n\nAnswer with only the JSON arguments you pass to suggest for this to-do: title, body, done_when, and any other '
              'argument the instructions above call for. No other text.')


def parsed(reply):
    start, end = reply.find('{'), reply.rfind('}')
    try:
        found = json.loads(reply[start:end + 1])
    except ValueError:
        return {}
    return found if isinstance(found, dict) else {}


def score(case, args, done_checks):
    """What the check this reply asks for would do: {'plan', 'fabricated', 'kept', 'inert', 'closes', 'wrong', 'miss'}.
    The baseline read is the page before the result (case before): a page that already shows the words leaves the check
    inert. wrong: a close of a case that wants none, or one the page showed before (no baseline to stop it)."""
    plan = args.get('done_check') if isinstance(args.get('done_check'), dict) else None
    out = {'plan': bool(plan and plan.get('url')), 'fabricated': False, 'kept': False, 'inert': False, 'closes': False, 'wrong': False, 'miss': False}
    if not out['plan']:
        return out
    texts = [m['body'] for m in case['messages']]
    try:
        clean = done_checks.clean(plan)
    except ValueError:
        clean = None
    url = done_checks._address(plan.get('url'))
    out['fabricated'] = not (url and done_checks.in_evidence(url, texts))
    if not clean or out['fabricated'] or not args.get('done_when'):
        return out  # the app keeps no check: the to-do comes back as before
    out['kept'] = True
    before = bool(case['before']) and done_checks.shows(case['before'], clean['expect'])
    live = bool(case['live']) and done_checks.shows(case['live'], clean['expect'])
    out['inert'] = before or not case['before']  # baseline shows the words, or no page to read: never checked
    out['closes'] = live and not out['inert']
    out['wrong'] = out['closes'] and case['want'] == 'none'
    out['miss'] = case['want'] == 'check' and not live  # the page shows it, in other words
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--root', default=str(ROOT))
    p.add_argument('--cases', default='cases.json')
    p.add_argument('--out', help='write every reply and score here (JSON)')
    a = p.parse_args()
    sys.path.insert(0, str(ROOT))  # the rules that score it are always this checkout's
    from machine.store import done_checks
    spec = json.loads((HERE / a.cases).read_text())
    paragraph = instructions(a.root)
    base, key = os.environ['OPENAI_BASE_URL'].rstrip('/'), os.environ['OPENAI_API_KEY']
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        jobs = [(run, case, pool.submit(ask, base, key, a.model, a.effort, prompt(spec['owner'], paragraph, case)))
                for run in range(a.runs) for case in spec['cases']]
        got = [(run, case, *j.result()) for run, case, j in jobs]
    sets, rows, tokens = {}, [], [0, 0]
    for run, case, reply, used_in, used_out in got:
        tokens[0], tokens[1] = tokens[0] + used_in, tokens[1] + used_out
        s = score(case, parsed(reply), done_checks)
        rows.append({'run': run, 'id': case['id'], 'set': case['set'], 'reply': reply, **s})
        t = sets.setdefault(case['set'], {'n': 0, 'plan': 0, 'kept': 0, 'fabricated': 0, 'inert': 0, 'closes': 0, 'wrong': 0, 'miss': 0})
        t['n'] += 1
        for k in ('plan', 'kept', 'fabricated', 'inert', 'closes', 'wrong', 'miss'):
            t[k] += s[k]
    print(f"{'set':10} {'turns':>5} {'plan':>5} {'kept':>5} {'made-up url':>11} {'inert':>5} {'closes':>6} {'wrong close':>11} {'literal miss':>12}")
    for name, t in sets.items():
        print(f"{name:10} {t['n']:5} {t['plan']:5} {t['kept']:5} {t['fabricated']:11} {t['inert']:5} {t['closes']:6} {t['wrong']:11} {t['miss']:12}")
    total = {k: sum(t[k] for t in sets.values()) for k in ('n', 'plan', 'kept', 'fabricated', 'inert', 'closes', 'wrong', 'miss')}
    print(f"{'all':10} {total['n']:5} {total['plan']:5} {total['kept']:5} {total['fabricated']:11} {total['inert']:5} {total['closes']:6} {total['wrong']:11} {total['miss']:12}")
    print(f'tokens per turn: {tokens[0] // max(1, len(got))} in, {tokens[1] // max(1, len(got))} out')
    if a.out:
        Path(a.out).write_text(json.dumps(rows, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
