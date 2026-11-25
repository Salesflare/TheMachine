"""Asks the questions in cases*.json in Ask from search (search_ask.py, machine/app/search_ask.py) on a made-up Machine, with
a real model, and has a second model grade each answer. Throwaway store, nothing is sent.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/ask-questions/run.py --model <model> --judge <model> [--runs 2] [--root <another checkout>]

The environment is that of evals/family-questions/run.py. --root: the code that answers, so a branch and main run on the
same questions. A question passes when its answer is right, reads like one to a person, and no message of another
connection was read for it (`only`; `beyond`: a subject nothing there matches may be looked for elsewhere), and, where a
service or address is only mentioned (`whole`), it was not narrowed to one. README.md has what they test."""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOW = dt.datetime(2026, 11, 9, 16, tzinfo=dt.timezone.utc)  # a Monday
JUDGE = ('You grade one answer of the search box of an assistant, which answers its owner from their own mail and chats. Today is Monday November 9, 2026. '
         'Reference is what a right answer says and what it must not; the answer may be in another language and shorter than the reference ("and/or" '
         'and "for example": one of them is enough). NO ANSWER means the box showed nothing.\nReply with one JSON object: {"right": true or false, "plain": true or false, "why": "a few words"}\n'
         '- right: it gives the main point of the reference, and nothing the reference says it must not. NO ANSWER is right only when the reference allows it.\n'
         '- plain: it speaks to its owner like a person, in the language of the question. false when it speaks of itself or its instructions like a program: "these messages", '
         '"the messages below", "the messages do not establish", "the search results", "the data provided", codes. The page Connections (Koppelingen, Connexions) and its words are names the owner knows.\n\nQuestion: {q}\nReference: {fact}\nAnswer: {answer}')


def ask(prompt, args, model, effort, used):
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 3000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(os.environ['OPENAI_BASE_URL'].rstrip('/') + '/responses', json.dumps(body).encode(),
                                             {'Authorization': os.environ['OPENAI_API_KEY'], 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=120) as r:
                reply = json.load(r)
            usage = reply.get('usage') or {}
            used.append((len(prompt), usage.get('input_tokens', 0), usage.get('output_tokens', 0)))
            return ''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or [])
        except (OSError, ValueError) as error:  # a busy model is asked again
            if attempt == 5 or isinstance(error, urllib.error.HTTPError) and error.code == 400:
                raise
            time.sleep(2 ** attempt)


def message(world, n, row):
    from machine import services
    account, days, sender, title, body, *to = row
    at, mine = (NOW - dt.timedelta(days=days)).isoformat(), sender.startswith(world['owner'])
    address, service = next((a['email'], a['service']) for a in world['accounts'] if a['id'] == account)
    if service not in services.of(group=services.MAIL):
        chat = str(sum(map(ord, title))) + ('@s.whatsapp.net' if service == 'whatsapp' else '')
        return {'account_id': account, 'source_id': f'c{n}', 'kind': f'{service}.message', 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
                'metadata': {'chat_id': chat, 'chat_name': title, 'chat_kind': 'dm', 'from_me': mine, 'from': sender, 'sender_display': sender, 'sender_id': None if mine else chat}}
    return {'account_id': account, 'source_id': f'm{n}', 'kind': 'outlook.message' if service == 'outlook' else 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': to[0] if to else address, 'labels': ['SENT'] if mine else ['INBOX'],
                                           'message-id': f'<{n}@x.example>', 'thread_id': f't{n}'}}


def machine(world, folder, lang):
    """The app of a Machine with these connections and messages, its Graph built."""
    import graph
    import machine.main as main
    from sources import SourceError
    clock = sys.modules['timeutil']
    clock.pin(NOW)
    store = main.Store(Path(folder) / f'{lang}.sqlite')
    store.accounts = world['accounts']
    app = object.__new__(main.App)
    app.store, app.config = store, {'accounts': world['accounts'], 'owner_emails': world['owner_emails'], 'language': lang, 'timezone': 'UTC'}
    if not (Path(folder) / f'{lang}.ready').exists():
        for n, row in enumerate(world['messages']):
            clock.pin(NOW - dt.timedelta(days=world['read'].get(row[0], 0)))  # when it was last read
            store.commit_page(row[0], {}, [message(world, n, row)])
        clock.pin(NOW)
        for account, failing in world['failing'].items():
            store.failed(account, SourceError(failing))
        with store.connect() as db:
            db.isolation_level = None
            graph.build(db, app.config, NOW.isoformat())
        for n, (account, minutes, *rest) in enumerate(world.get('after', ()), len(world['messages'])):  # came in after the Graph was built
            clock.pin(NOW - dt.timedelta(minutes=world.get('read_after', 3)))
            store.commit_page(account, world.get('state', {}).get(account, {}), [message(world, n, [account, minutes / 1440, *rest])])
        clock.pin(NOW)
        (Path(folder) / f'{lang}.ready').touch()
    return app


def one(case, world, folder, args):
    import search_ask
    app = machine(world, folder, case['lang'])
    prompts, used, judging, scopes, scoped = [], [], [], [], app.search_ask_scoped

    def seen(*args, **kw):
        found = scoped(*args, **kw)
        scopes.append(found[1] or {})
        return found
    app.search_ask_scoped = seen

    def model(config, text):
        prompts.append(text)
        return ask(text, args, args.model, args.effort, used)
    app.ask_model = model
    search_ask.limited = lambda now=None: False  # the eval asks more than an owner may in an hour
    started = time.monotonic()
    found = app.action('search_ask', {'query': case['q'], 'area': case.get('area', 'all'), 'before': case.get('before')}, owner_dashboard=True)
    took = time.monotonic() - started
    answer = found.get('answer') or ('FAILED' if found.get('error') else 'NO ANSWER')
    read = prompts[1].split('\nQuestion: <<<')[0] if len(prompts) > 1 else ''
    outside = sorted({m[0] for m in [*world['messages'], *world.get('after', ())] if f'<<<{m[4]}>>>' in read and m[0] not in case['only']}) if 'only' in case and not case.get('beyond') else []
    missing = [x for x in case.get('needs', ()) if f"<<<{x.split(':', 1)[1]}" not in read]
    narrowed = bool(case.get('whole') and any(s.get('connections') for s in scopes))
    try:
        graded = json.loads(re.search(r'\{.*\}', ask(JUDGE.replace('{q}', case['q']).replace('{fact}', case['fact']).replace('{answer}', answer),
                                                     args, args.judge, 'low', judging), re.S)[0])
    except (TypeError, ValueError):
        graded = {'right': False, 'plain': False, 'why': 'not graded'}
    return {'id': case['id'], 'ordinary': bool(case.get('ordinary')), 'lang': case['lang'], 'q': case['q'], 'answer': answer, 'outside': outside, 'missing': missing, 'narrowed': narrowed, **graded,
            'pass': bool(graded.get('right') and graded.get('plain') and not (outside or missing or narrowed)), 'used': used, 'seconds': round(took, 1), 'prompts': prompts}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--judge', required=True)
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=1)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--root', default=str(HERE.parent.parent))
    p.add_argument('--cases', nargs='*', help='the files of questions: every cases*.json here')
    p.add_argument('--only')
    p.add_argument('--out')
    args = p.parse_args()
    sys.path.insert(0, args.root)
    os.environ['TZ'] = 'UTC'
    time.tzset()
    got = []
    for file in args.cases or sorted(HERE.glob('cases*.json')):
        world = json.loads(Path(file).read_text(encoding='utf-8'))
        cases = [c for c in world['cases'] if not args.only or re.search(args.only, c['id'])]
        with tempfile.TemporaryDirectory() as folder:
            for lang in sorted({c['lang'] for c in cases}):
                machine(world, folder, lang)
            with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
                got += pool.map(lambda c: one(c, world, folder, args), cases * args.runs)
    for g in got:
        why = [str(g.get('why')), *['not right'] * (not g.get('right')), *['not plain'] * (not g.get('plain')), *['narrowed'] * g['narrowed'],
               *['read ' + a for a in g['outside']], *['not read ' + m for m in g['missing']]]
        print('ok  ' if g['pass'] else 'MISS', g['id'], '|', g['answer'], '' if g['pass'] else '=> ' + '; '.join(why))
    for name, part in (('own connections', [g for g in got if not g['ordinary']]), ('ordinary', [g for g in got if g['ordinary']])):
        if part:
            print(f"{name}: passed {sum(g['pass'] for g in part)}/{len(part)}, right {sum(bool(g.get('right')) for g in part)}, plain {sum(bool(g.get('plain')) for g in part)}, "
                  f"read other connections {sum(bool(g['outside']) for g in part)}, narrowed {sum(g['narrowed'] for g in part)}")
    plans, answers = [g['used'][0] for g in got if g['used']], [g['used'][1] for g in got if len(g['used']) > 1]
    for name, turns in (('first turn', plans), ('answer turn', answers)):
        if turns:
            print(f"{name}: {len(turns)}, characters {sum(t[0] for t in turns) // len(turns)} (largest {max(t[0] for t in turns)}), tokens in {sum(t[1] for t in turns) // len(turns)}, "
                  f"out {sum(t[2] for t in turns) // len(turns)}")
    print(f"seconds {sum(g['seconds'] for g in got) / len(got):.1f}")
    if args.out:
        Path(args.out).write_text(json.dumps(got, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
