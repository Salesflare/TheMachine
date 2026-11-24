"""Asks the help chat the questions in cases.json and says how often it found the right help section and answered right:
the real search and the real prompt (help_chat.py), with a real model. Nothing is read but the public docs and code.

    python3 evals/help-questions/run.py --set dev                      (the search only, no model)
    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/help-questions/run.py --set held --model <model> --judge <model>

OPENAI_API_KEY is the whole Authorization value ("Bearer ..." where the provider wants that) and OPENAI_BASE_URL the
address of any Responses API. README.md says what the sets are for."""
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
sys.path.insert(0, str(HERE.parent.parent))

import help_chat

JUDGE = ("You grade one answer of an app's help chat. Reference is what is true and what a right answer says; the answer may "
         "be in another language, name buttons in that language, and leave out side details. Reply with one word first:\n"
         "right: it gives the main point of the reference (for a No: it says plainly it isn't possible) and nothing that "
         "contradicts it. More steps and details than the reference has are fine: they come from the help pages\n"
         "partly: useful, but misses the main point or is hedged where the reference is clear\n"
         "wrong: it contradicts the reference, or answers something else\n"
         "none: it says it doesn't know or the help doesn't cover it\n"
         "Then one short line why.\n\nQuestion: {q}\nReference: {fact}\nAnswer: {answer}")


def ask(text, model, effort, used, limit=3000):
    body = {'model': model, 'input': text, 'reasoning': {'effort': effort}, 'max_output_tokens': limit}
    for attempt in range(6):
        try:
            request = urllib.request.Request(os.environ['OPENAI_BASE_URL'].rstrip('/') + '/responses', json.dumps(body).encode(),
                                             {'Authorization': os.environ['OPENAI_API_KEY'], 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=90) as r:
                reply = json.load(r)
            usage = reply.get('usage') or {}
            used.append((usage.get('input_tokens', 0), usage.get('output_tokens', 0)))
            return ''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or [])
        except (OSError, ValueError):  # a busy model is asked again
            if attempt == 5:
                raise
            time.sleep(2 ** attempt)


def place(section):
    return section['slug'] + ('#' + section['anchor'] if section['anchor'] else '')


def one(case, args):
    sections, snippets = help_chat.retrieve(case['q'], lang=case['lang'])
    found = [place(s) for s in sections]
    got = {**case, 'found': found, 'code': len(snippets), 'hit': any(w in found for w in case['want']),
           'article': any(w.split('#')[0] in {f.split('#')[0] for f in found} for w in case['want']), 'turns': [], 'judging': []}
    text = help_chat.prompt(case['q'], (), sections, snippets, lang=case['lang'])
    got['chars'] = len(text)
    if args.model:
        got['answer'] = ask(text, args.model, args.effort, got['turns'])
        look = help_chat.search_again(got['answer'])
        if look:  # as help_chat.ask does
            sections, snippets = help_chat.retrieve(case['q'], lang=case['lang'], look=look)
            got['look'], got['second'] = look, [place(s) for s in sections]
            got['answer'] = ask(help_chat.prompt(case['q'], (), sections, snippets, lang=case['lang'], again=True), args.model, args.effort, got['turns'])
        shown = re.split(help_chat.TOPIC_LINE, got['answer'])[0]
        why = ask(JUDGE.format(q=case['q'], fact=case['fact'], answer=shown), args.judge, 'low', got['judging'])
        got['grade'], got['why'] = (re.findall(r'right|partly|wrong|none', why.lower()) or ['?'])[0], why
    return got


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--set', choices=('dev', 'held'), required=True)
    p.add_argument('--model')
    p.add_argument('--judge')
    p.add_argument('--effort', default='low')
    p.add_argument('--jobs', type=int, default=6)
    p.add_argument('--out')
    p.add_argument('--quiet', action='store_true', help='only the totals')
    args = p.parse_args()
    cases = [c for c in json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))['cases'] if c['set'] == args.set]
    with concurrent.futures.ThreadPoolExecutor(args.jobs if args.model else 1) as pool:
        got = list(pool.map(lambda c: one(c, args), cases))
    if not args.quiet:
        for g in got:
            if not g['hit'] or g.get('grade', 'right') != 'right':
                print(g['id'], g['lang'], 'hit ' if g['hit'] else 'MISS', g.get('grade', ''), '|', g['q'], '->', ' '.join(g['found']), '=>', g.get('look', ''), ' '.join(g.get('second', [])))
    n = len(got)
    print(f"section {sum(g['hit'] for g in got)}/{n}, article {sum(g['article'] for g in got)}/{n}, prompt {sum(g['chars'] for g in got) // n} characters")
    if args.model:
        grades = {}
        for g in got:
            grades[g['grade']] = grades.get(g['grade'], 0) + 1
        turns = [t for g in got for t in g['turns']]
        judging = [t for g in got for t in g['judging']]
        print(f"looked again {sum('look' in g for g in got)}, found then {sum(not g['hit'] and any(w in g.get('second', ()) for w in g['want']) for g in got)}")
        print(f"right {grades.get('right', 0)}/{n} {grades}, tokens in per answer {sum(t[0] for t in turns) // n}, out {sum(t[1] for t in turns) // n}, "
              f"all {sum(t[0] for t in turns)}+{sum(t[1] for t in turns)}, judge {sum(t[0] for t in judging)}+{sum(t[1] for t in judging)}")
    if args.out:
        Path(args.out).write_text(json.dumps(got, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
