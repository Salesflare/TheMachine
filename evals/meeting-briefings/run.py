"""Runs the made-up meetings in cases.json through the real briefing (meeting_prep.py: what it reads, its turn, its checks
and the to-do's text) with a real model, and has a model check each briefing against what it should and must not say.
Throwaway store, no to-do is made, nothing is sent.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/meeting-briefings/run.py --model <model> [--runs 2] [--set held-out] [--root <another checkout>]

The environment is that of evals/family-questions/run.py. --root: the code whose briefings are judged, so a branch and
main run on the same cases. README.md has what they test."""
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

HERE = Path(__file__).resolve().parent
NOW = dt.datetime(2026, 11, 9, 9, tzinfo=dt.timezone.utc)  # a Monday; the meetings are on Tuesday at 10:00
ACCOUNTS = [{'id': i, 'service': s, 'boundary': b, 'email': e} for i, s, b, e in (
    ('wcal', 'calendar', 'work:Larkspur', 'robin@larkspur.example'), ('wmail', 'gmail', 'work:Larkspur', 'robin@larkspur.example'),
    ('wmeet', 'zoom', 'work:Larkspur', 'robin@larkspur.example'), ('pcal', 'calendar', 'personal:home', 'robin@home.example'),
    ('pmail', 'gmail', 'personal:home', 'robin@home.example'))]
ME = {'email': 'robin@larkspur.example', 'displayName': 'Robin Hale', 'self': True, 'responseStatus': 'accepted'}
JUDGE = ('Below is a briefing a person gets before a meeting ("the owner" is Robin Hale; a step without a name is Robin\'s), and statements. For each '
         'statement, by its meaning, in any language, say whether the briefing says it: "yes" when it clearly says it (a date or number may be '
         'written otherwise), "partly" when it says only some of it, "no" when it does not. A statement "X (as current)" is said only when the briefing has X as what holds now, not as what '
         'it was before. "Y still has to be done" is said only when the briefing has Y as open. Answer with one JSON object: {"1": "yes", "2": "no", ...}.\n\n')
FAITH = ('Below are the only facts a briefing may use, and the briefing. List each statement in the briefing that these facts contradict, or that they do not '
         'support (made up, or shown as agreed when only planned or proposed, or shown as open when the facts show it done). A shortened or reworded fact, a suggestion what to raise, a label or a source is fine; who a step without a name belongs to is Robin. '
         'Answer with one JSON object: {"wrong": ["..."]}, an empty list when none.\n\n')


def ask(base, key, model, effort, prompt):
    """(text, input tokens, output tokens) of one turn."""
    body = {'model': model, 'input': prompt, 'reasoning': {'effort': effort}, 'max_output_tokens': 6000}
    for attempt in range(6):
        try:
            request = urllib.request.Request(base + '/responses', json.dumps(body).encode(), {'Authorization': key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=180) as r:
                reply = json.load(r)
            used = reply.get('usage') or {}
            return (''.join(c.get('text', '') for o in reply.get('output', []) for c in o.get('content') or []),
                    used.get('input_tokens', 0), used.get('output_tokens', 0))
        except urllib.error.HTTPError as error:
            if error.code == 400:  # the provider's own filter refuses it: nothing is written, as in the app
                return '', 0, 0
            if attempt == 5:
                raise
            time.sleep(2 ** attempt)
        except (OSError, ValueError) as error:  # a busy model is asked again
            if attempt == 5:
                raise ValueError(type(error).__name__) from None
            time.sleep(2 ** attempt)


def meeting(source, start, title, body, guests, team=0, account='wcal', me='accepted', **meta):
    end = (start + dt.timedelta(hours=1)).isoformat()
    people = [{**ME, 'responseStatus': me}, *({'email': e, 'displayName': n, 'responseStatus': 'accepted'} for e, n in guests),
              *({'email': f'team{i}@larkspur.example', 'responseStatus': 'accepted'} for i in range(team))]
    return {'account_id': account, 'source_id': source, 'kind': 'calendar.event', 'occurred_at': start.isoformat(), 'title': title, 'body': body, 'deleted': False,
            'metadata': {'start': {'dateTime': start.isoformat()}, 'end': {'dateTime': end}, 'end_at': end, 'all_day': False, 'timezone': 'UTC', 'status': 'confirmed',
                         'ical_uid': source + '@larkspur.example', 'attendees': people, **meta}}


def prepare(case, text, folder, history=False):
    """The app with this case's signals, and the upcoming meeting's events id. {name} in a text is its filler. history: what
    came before is history, but for a case with a promise or to-do (history makes neither)."""
    import graph
    import machine.main as main
    store = main.Store(Path(folder) / (case['id'] + '.sqlite'))
    store.accounts = ACCOUNTS
    app = object.__new__(main.App)
    app.store, app.config = store, {'accounts': ACCOUNTS, 'review_worker': {'enabled': True}, 'meeting_prep_research': False, 'owner_name': 'Robin Hale', 'openclaw_workspace': str(folder)}
    page = lambda e: store.commit_page(e['account_id'], {}, [e])
    web = case.get('web')
    if web:  # what the web has of them: a page of their own site, and each search's results
        app.config['meeting_prep_research'] = True
        app.meeting_prep_site_text = lambda domain: web['site'].get(domain)
        app.meeting_prep_web_search = lambda query: web['search'] if query.startswith(f'"{case["guests"][0][1]}"') else []
    if history and not case['promises'] and not case['done']:
        page = lambda e: store.commit_page(e['account_id'], None, [e], record_sync=False, history=True)
    ago = lambda days, hour=13: (NOW - dt.timedelta(days=days)).replace(hour=hour)
    def full(body):
        for name, filler in text.items():
            body = body.replace('{%s}' % name, filler * 2)
        return body
    record = {}
    for n, m in enumerate(case['meetings']):
        start, key, account = ago(m['days']), f"m{n}", 'pcal' if m.get('account') == 'p' else 'wcal'
        meta = {'recurring_event_id': m['series']} if m.get('series') else {}
        said = full(m['text'])
        if m['kind'] == 'description':
            meta['updated'] = (start + dt.timedelta(minutes=10)).isoformat()
        page(meeting(key, start, m['title'], said if m['kind'] == 'description' else '', m['guests'], m.get('team', 0), account, **meta))
        with store.connect() as db:
            event = db.execute('SELECT id FROM events WHERE source_id=?', (key,)).fetchone()[0]
        end = (start + dt.timedelta(hours=1)).isoformat()
        if m['kind'] == 'mail':
            page({'account_id': 'wmail', 'source_id': key + 'r', 'kind': 'gmail.message', 'occurred_at': (start + dt.timedelta(minutes=65)).isoformat(), 'title': 'Meeting assets for ' + m['title'] + ' are ready',
                  'body': said, 'metadata': {'from': 'Zoom <no-reply@zoom.us>', 'labels': ['INBOX']}, 'deleted': False})
        elif m['kind'] != 'description':
            own = m['kind'].startswith('meeting.')
            page({'account_id': account if own else 'wmeet', 'source_id': f'notes:{event}' if own else key + 'r', 'kind': m['kind'], 'occurred_at': start.isoformat(), 'title': m['title'],
                  'body': said, 'metadata': {'start_at': start.isoformat(), 'end_at': end}, 'deleted': False})
        with store.connect() as db:
            row = db.execute('SELECT id FROM events WHERE source_id IN (?,?)', (key + 'r', f'notes:{event}')).fetchone()
        record[n] = row[0] if row else event
    for n, m in enumerate(case['mails']):
        own = m['from'] == 'own'
        who = case['guests'][0] if own else m['from']
        sender, to = (['robin@larkspur.example', 'Robin Hale'], who) if own else (who, ['robin@larkspur.example', 'Robin Hale'])
        page({'account_id': 'wmail', 'source_id': f'mail{n}', 'kind': 'gmail.message', 'occurred_at': ago(m['days'], 15).isoformat(), 'title': m['subject'], 'body': m['text'],
              'metadata': {'from': f'{sender[1]} <{sender[0]}>', 'to': f'{to[1]} <{to[0]}>', 'labels': ['SENT'] if own else ['INBOX'], 'thread_id': f'{case["id"]}{n}'}, 'deleted': False})
    page = lambda e: store.commit_page(e['account_id'], {}, [e])
    page(meeting('next', NOW.replace(day=10, hour=10), case['title'], case['about'], case['guests'], me=case.get('me', 'accepted'),
                 **({'recurring_event_id': case['series'], 'original_start': {'dateTime': '2026-11-10T10:00:00+00:00'}} if case.get('series') else {})))
    with store.connect() as db:
        for a, b in case['merges']:
            graph.merge(db, 'email:' + a, 'email:' + b, True, NOW.isoformat(), source='owner')
        db.commit()
        sent = dict(db.execute('SELECT source_id,id FROM events').fetchall())
    for p in case['promises']:
        made = store.promise({'direction': p['direction'], 'who': p['who'], 'what': p['what'], 'event_id': sent[f"mail{p['mail']}"]})
        if p['status'] != 'open':
            store.update_promise({'id': made['id'], 'status': p['status']}, source='dashboard')
    for n, d in enumerate(case['done']):
        card = store.suggest(f'done{n}', d['title'], d['title'], [record[d['of']]])
        store.decide(card['id'], 'complete', '', f'd{n}', 'dashboard')
    if history:
        from machine.store import graph_history
        with store.connect() as db:
            graph_history.advance(db, (NOW - dt.timedelta(days=graph.HORIZON_DAYS)).isoformat(), NOW.isoformat())
    if case.get('own'):  # what the owner's own organization does, as it was looked up
        import enrichment
        with store.connect() as db:
            enrichment.save(db, 'larkspur.example', 'found', case['own'], NOW.isoformat())
    if case.get('before'):  # the briefing before an earlier occurrence
        import meeting_prep
        with store.connect() as db:
            row = db.execute("SELECT * FROM events WHERE kind='calendar.event' AND source_id='m0'").fetchone()
        card = store.suggest(meeting_prep.KEY_PREFIX + 'before', 'Prepare for ' + case['title'], case['before'], [row['id']])
        store.decide(card['id'], 'complete', '', 'before', 'dashboard')
        with store.connect() as db:
            meeting_prep.keep(db, {'key': meeting_prep.KEY_PREFIX + 'before', 'id': row['id'], 'start': dt.datetime.fromisoformat(row['occurred_at'])}, 'made', card['id'],
                              (NOW - dt.timedelta(days=7)).isoformat(), case['before'])
    with store.connect() as db:
        graph.build(db, app.config, NOW.isoformat(), **({'history': True} if history else {}))
    return app


def case_quiet(case):
    return bool(case.get('quiet'))


def facts(case, text):
    """What the judge of made-up claims reads: the notes and mail of the meeting's own people and area, in full."""
    day = lambda n: (NOW - dt.timedelta(days=n)).date().isoformat()
    emails = {e for e, _ in case['guests']} | {b for _, b in case['merges']}
    out = [f"Upcoming meeting: {case['title']}; {case['about']}. Guests: " + ', '.join(f'{n} of {e.partition("@")[2]}' for e, n in case['guests']) + '. Today is 2026-11-09.']
    for m in case['meetings']:
        if m.get('account') != 'p' and emails & {e for e, _ in m['guests']}:
            kind = 'agenda written beforehand, nothing decided yet' if m['kind'] == 'description' else 'notes'
            out.append(f"{m['title']}, {day(m['days'])} ({kind}): " + ''.join(m['text'].replace('{%s}' % n, '') for n in ['talk'])[:3000])
    if any('team' in m for m in case['meetings']):
        out.append('Lars and Petra are colleagues of Robin.')
    out += [f"Mail on {day(m['days'])} from {'Robin' if m['from'] == 'own' else m['from'][1]}, {m['subject']}: {m['text']}" for m in case['mails']]
    out += [f"Promise by Robin, {p['status']} since {day(6)}: {p['what']}" for p in case['promises']] + [f"Done on {day(6)}: {d['title']}" for d in case['done']]
    web = case.get('web') or {}
    out += [f"{domain}'s own website: {p['title']}: {p['description']}" for domain, p in (web.get('site') or {}).items()]
    out += [f"Web page {r['title']}: {r['description']}" for r in web.get('search') or ()]
    out += [f"What Robin's own organization does: {json.dumps(case['own'])}"] if case.get('own') else []
    out += ['The last briefing said: ' + case['before']] if case.get('before') else []
    return '\n'.join(out)


def briefing(case, text, folder, turn, history=False):
    """The briefing's text ('' for none), and its turn's (input, output) tokens."""
    import meeting_prep
    import i18n
    import inspect
    app, used = prepare(case, text, folder, history), [0, 0]

    def model(config, prompt):
        reply, i, o = turn(prompt)
        used[0] += i
        used[1] += o
        return reply
    app.meeting_prep_model = model
    found = app.meeting_prep_next(NOW)
    if not found:
        return '', used
    from machine import model_reply
    try:
        made = app.meeting_prep_brief(found)
    except model_reply.Unreadable:
        return '(no readable answer)', used
    if not made or made['area'] == 'personal':
        return '', used
    more = (app.meeting_prep_cites(found),) if len(inspect.signature(meeting_prep.body_text).parameters) > 3 else ()
    return meeting_prep.body_text(made['fields'], i18n.t, made.get('links'), *more), used


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--judge', default='')
    p.add_argument('--effort', default='low')
    p.add_argument('--runs', type=int, default=1)
    p.add_argument('--jobs', type=int, default=3)
    p.add_argument('--set', default='')
    p.add_argument('--only', default='')
    p.add_argument('--root', default=str(HERE.parent.parent))
    p.add_argument('--chars', type=int, default=0, help='another limit for the notes in a turn')
    p.add_argument('--history', action='store_true', help='earlier meetings, notes and mail are history')
    p.add_argument('--show', action='store_true', help='print the turns, ask nothing')
    p.add_argument('--texts', action='store_true', help='print the briefings too')
    a = p.parse_args()
    sys.path.insert(0, a.root)
    import locale_prefs
    import machine.main  # noqa: F401  every module it sets the clock of is loaded
    clock = sys.modules['timeutil']
    clock.LOCAL_TZ = dt.timezone.utc
    real, settled = clock.now, (NOW - dt.timedelta(days=6)).isoformat()  # when a promise was kept or a to-do done
    for module in list(sys.modules.values()):
        if getattr(module, 'now', None) is real:
            module.now = lambda: settled
    if a.chars:
        import earlier_notes
        earlier_notes.FIRST, earlier_notes.REST = a.chars * earlier_notes.FIRST // earlier_notes.CHARS, a.chars * earlier_notes.REST // earlier_notes.CHARS
        earlier_notes.CHARS = a.chars
    locale_prefs._current.update(locale='en-US', language='en')
    spec = json.loads((HERE / 'cases.json').read_text())
    cases = [c for c in spec['cases'] if (not a.set or c['set'] == a.set) and (not a.only or c['id'] in a.only.split(','))]
    spent = [0, 0]
    with tempfile.TemporaryDirectory() as folder:
        if a.show:
            for c in cases:
                briefing(c, spec['text'], folder, lambda t: (print(t, '\n\n=====\n\n'), ('{"useful": false}', 0, 0))[1], a.history)
            return
        base, key = os.environ['OPENAI_BASE_URL'].rstrip('/'), os.environ['OPENAI_API_KEY']
        turn = lambda t: ask(base, key, a.model, a.effort, t)

        def judged(prompt):
            reply, i, o = ask(base, key, a.judge or a.model, 'low', prompt)
            return (json.loads(reply[reply.find('{'):reply.rfind('}') + 1]) if '{' in reply else {'wrong': ['(the check was refused)']}), i, o

        def one(c, run):
            sub = Path(folder) / f'r{run}'
            sub.mkdir(exist_ok=True)
            body, used = briefing(c, spec['text'], sub, turn, a.history)
            says = [*c['want'], *c['never']]
            said, wrong, extra = {}, [], [0, 0]
            if body:
                said, i, o = judged(JUDGE + 'Briefing:\n' + body + '\n\nStatements:\n' + '\n'.join(f'{n}. {s}' for n, s in enumerate(says, 1)))
                checked, i2, o2 = judged(FAITH + 'Facts:\n' + facts(c, spec['text']) + '\n\nBriefing:\n' + body)
                wrong, extra = [w for w in checked.get('wrong') or () if w], [i + i2, o + o2]
            return c, body, used, extra, [s for n, s in enumerate(says, 1) if str(said.get(str(n))).lower() == 'yes'], wrong
        with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
            got = list(pool.map(lambda x: one(*x), [(c, r) for r in range(a.runs) for c in cases]))
    tally = {}
    for c, body, used, extra, said, wrong in got:
        t = tally.setdefault(c['set'], {'want': 0, 'of': 0, 'bad': 0, 'badof': 0, 'wrong': 0, 'made': 0, 'n': 0, 'quiet': 0, 'quietof': 0, 'in': [], 'out': [], 'chars': []})
        missed, bad = [w for w in c['want'] if w not in said], [x for x in c['never'] if x in said]
        for k, v in (('want', len(c['want']) - len(missed)), ('of', len(c['want'])), ('bad', len(bad)), ('badof', len(c['never'])), ('wrong', len(wrong)), ('made', bool(body)), ('n', 1),
                     ('quiet', bool(case_quiet(c) and body)), ('quietof', case_quiet(c))):
            t[k] += v
        if used[0]:
            t['in'].append(used[0])
            t['out'].append(used[1])
            t['chars'].append(len(body))
        spent[0] += used[0] + extra[0]
        spent[1] += used[1] + extra[1]
        if a.texts:
            print('---', c['id'], used, '\n' + body)
        if missed or bad or wrong or case_quiet(c) and body:
            print(c['id'], *(['BRIEFING WITH NOTHING TO SAY'] if case_quiet(c) and body else []), *([f'missed: {missed}'] if missed else []), *([f'BAD: {bad}'] if bad else []), *([f'unsupported: {wrong}'] if wrong else []), sep='\n   ')
    for name, t in tally.items():
        avg = lambda v: sum(v) // max(1, len(v))
        print(f"{name}: facts recalled {t['want']} of {t['of']}; wrong or stale {t['bad']} of {t['badof']}; unsupported statements {t['wrong']}; briefings {t['made']} of {t['n']} (with nothing to say {t['quiet']} of {t['quietof']}); "
              f"turn tokens in {avg(t['in'])} (max {max(t['in'] or [0])}) out {avg(t['out'])}; briefing chars {avg(t['chars'])} (max {max(t['chars'] or [0])})")
    print('tokens used in all', spent)


if __name__ == '__main__':
    main()
