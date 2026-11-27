"""Learning scope eval: where does a rule a learning pass writes hold? Made-up batches (cases.json, frozen before the
first run; cases-fresh.json, written apart and frozen too), each with the scopes a rule from it may rightly take. The
turn is the app's own (learning_loop.prompt, with the page as profile_evidence gives it); each change it answers is
placed the way apply places it (learning_loop.scope_of). --main FILE also places the same answers with another
learning_loop.py (main's), so both are judged on one set of turns. Nothing is sent anywhere but the model.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/learning-scope/run.py --model <model> --runs 3 [--main old.py]

Counted per change kept: right, wrongly global (global where the cases want narrower), too broad (an area or channel
where they want one person or organization), too narrow, off (another area, channel or record), and lost (a change
not kept although the case has something to learn). On a case with nothing to learn, every kept change is unwanted."""
import argparse
import concurrent.futures
import importlib.util
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

import learning_loop  # noqa: E402
from machine.store.voices import voice_channel  # noqa: E402

CHANNEL = lambda name: voice_channel(name.capitalize())  # a channel's name as voices and contexts keep it


def ask(base, key, model, effort, prompt):
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 4000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=180) as r:
                reply = json.load(r)
            usage = reply.get('usage') or {}
            return ''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []), usage.get('input_tokens', 0), usage.get('output_tokens', 0)
        except (OSError, ValueError) as error:
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def evidence(case):
    """The batch as profile_evidence stores it: signals with n and context, refs to records (here, their names)."""
    refs, by_name, signals = {}, {}, []

    def ref(name):
        if name not in by_name:
            by_name[name] = f'r{len(by_name) + 1}'
            refs[by_name[name]] = name
        return by_name[name]
    for i, s in enumerate(case['signals']):
        if s['kind'] == 'edit':
            out = {'what': 'edited a draft', 'at': '2026-11-2%dT09:00:00Z' % (i % 7), 'channel': s['channel'], 'to_do': s['to_do'],
                   'draft': s['draft'], 'theirs': s['theirs']}
        elif s['kind'] == 'miss':
            out = {'what': 'said a message the review left without a to-do needed one', 'at': '2026-11-2%dT09:00:00Z' % (i % 7),
                   'channel': CHANNEL(s['channel']), 'message': s['message'], 'review_said': s['review_said']}
        else:
            out = {'what': s['what'], 'at': '2026-11-2%dT09:00:00Z' % (i % 7), 'to_do': s['to_do'], **({'note': s['note']} if s.get('note') else {})}
        found = []
        for w in s.get('with') or ():
            name, _, org = w.partition('@')
            kind = 'person' if org or ' ' in name else 'organization'
            found.append({'ref': ref(name), 'name': name, 'kind': kind, **({'at': org} if org else {})})
            if org:
                found.append({'ref': ref(org), 'name': org, 'kind': 'organization'})
        context = {'area': s['area'], 'channel': CHANNEL(s['channel']), **({'with': found[:learning_loop.WITH_MAX]} if found else {})}
        signals.append({'n': i + 1, **out, 'context': context})
    return {'tune': True, 'scoped': True, 'signals': signals, 'refs': refs, 'voices': [], 'rules': [], 'facts': []}


def parsed(reply):
    start, end = reply.find('{'), reply.rfind('}')
    try:
        found = json.loads(reply[start:end + 1])
    except ValueError:
        return None
    if isinstance(found, dict) and 'profile' in found:
        found = found['profile']
    return found.get('changes') if isinstance(found, dict) and isinstance(found.get('changes'), list) else None


def placed(scope_of, change, given):
    out = scope_of(change, given)
    if out is None:
        return None
    scope, side, node = out
    return 'area:' + side if scope == 'area' else scope


RANK = lambda s: 2 if s == 'global' else 0 if s.startswith('with:') else 1


def verdict(want, got):
    if want == ['none']:
        return 'unwanted' if got else 'dropped-ok'
    if got is None:
        return 'lost'
    if got in want:
        return 'right'
    if got == 'global':
        return 'wrongly global'
    if RANK(got) > max(map(RANK, want)):
        return 'too broad'
    if RANK(got) < min(map(RANK, want)):
        return 'too narrow'
    return 'off'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--cases', default='cases.json')
    p.add_argument('--main', help="another learning_loop.py whose scope_of places the same answers")
    p.add_argument('--out')
    a = p.parse_args()
    gates = {'change': learning_loop.scope_of}
    if a.main:
        spec = importlib.util.spec_from_file_location('main_learning_loop', a.main)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        gates['main'] = old.scope_of
    cases = json.loads((HERE / a.cases).read_text(encoding='utf-8'))['cases']
    base, key = os.environ['OPENAI_BASE_URL'].rstrip('/'), os.environ['OPENAI_API_KEY']

    def one(job):
        case, run = job
        given = evidence(case)
        prompt = (learning_loop.prompt('eval', given) + '\n\nWhat assistant_signals profile_evidence page 1 returned:\n'
                  + json.dumps(learning_loop.page(given), ensure_ascii=False)
                  + '\n\nThere are no tools here: instead of calling save_profile, reply with only its args.profile as JSON.')
        text, tin, tout = ask(base, key, a.model, a.effort, prompt)
        changes = [{**c, 'scope': None if c.get('scope') is None else ' '.join(str(c['scope']).split())[:120],  # as save_draft keeps it
                    'from': [int(n) for n in c['from'][:learning_loop.MAX_SIGNALS] if str(n).isdigit()] if isinstance(c.get('from'), list) else None}
                   for c in (parsed(text) or []) if isinstance(c, dict) and c.get('kind') in ('draft', 'fact')]
        rows = [{'text': c.get('text'), 'said': c.get('scope'), 'from': c.get('from'),
                 **{g: placed(f, c, given) for g, f in gates.items()}} for c in changes]
        return {'id': case['id'], 'run': run, 'want': case['want'], 'changes': rows, 'tokens': [tin, tout], 'raw': text if parsed(text) is None else None}

    jobs = [(c, r) for r in range(a.runs) for c in cases]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = list(pool.map(one, jobs))
    for g in gates:
        counts, cases_right = {}, 0
        for r in results:
            seen = [verdict(r['want'], c[g]) for c in r['changes']] or (['dropped-ok'] if r['want'] == ['none'] else ['nothing said'])
            for v in seen:
                counts[v] = counts.get(v, 0) + 1
            cases_right += ('right' in seen) if r['want'] != ['none'] else ('unwanted' not in seen)
        print(f'{g}: {cases_right}/{len(results)} turns right;', ', '.join(f'{k} {v}' for k, v in sorted(counts.items())))
    tin = sum(r['tokens'][0] for r in results) / len(results)
    tout = sum(r['tokens'][1] for r in results) / len(results)
    print(f'tokens per turn in/out: {tin:.0f}/{tout:.0f}; unparsed: {sum(1 for r in results if r["raw"])}')
    if a.out:
        Path(a.out).write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
