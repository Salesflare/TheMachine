"""A backlog of some 1,000 made-up signals worked off by the real claim (Store.begin_analysis) on a fake clock, for
tests/test_review_catch_up.py and by hand: `python3 tests/review_backlog.py dev` (`held` for the set that was frozen
before the order was worked out; `--app <checkout>` runs another version's code, such as main's).

The case: reviews paused for 43 hours (a usage limit), new signals keep coming in, and every 5-hour usage window takes
only so much: a run that meets its end is interrupted, its claim handed to the first run of the next window, as
App.review_step does. Nothing here is real data: example domains, made-up people, plain subjects."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import random
import statistics
import sys
import tempfile

ME = 'owner@example.com'
OWNER_SLACK = 'U0OWNER'
START = dt.datetime(2026, 11, 23, 5, 0, tzinfo=dt.timezone.utc)
RUN_MINUTES, GAP_MINUTES, WINDOW_HOURS = 12, 10, 5
ASKS = ('Can you send the numbers?', 'Could you approve this before Friday?', 'Are we still on for next week?', 'What do you think of the draft?')
SAYS = ('The new office is open now.', 'Here are the notes of today.', 'The parcel came in this morning.', 'Moving along nicely here.')
DAY = (.2, .1, .1, .1, .1, .2, .5, 1, 1.6, 2, 2, 1.8, 1.5, 1.7, 1.9, 1.8, 1.6, 1.3, 1, .9, .9, .8, .5, .4)  # people by hour of the day

# Signals per hour of each class, how much one 5-hour usage window reads (in signals of the run's budget), and seeds.
# DEV is what the order was worked out on. HELD was written and hashed (HELD_SHA) before that and is what is reported.
SPECS = {
    'dev': {'rates': {'newsletter': 4.5, 'auto': 2.5, 'stripe': .6, 'phone': 1.5, 'mail_ask': .7, 'mail_say': .9, 'mail_thanks': .4, 'mail_cc': 1.4,
                      'mail_thread': .5, 'sent': .8, 'calendar': .3, 'slack_channel': 3.0, 'slack_bot': 1.0, 'slack_dm': .9, 'chat_dm': .9, 'chat_group': 1.5,
                      'linkedin': .4, 'teams_dm': .3, 'github': .4},
            'window': 260, 'import': 60, 'seeds': (1, 2, 3)},
    'held': {'rates': {'newsletter': 2.5, 'auto': 4.5, 'stripe': .2, 'phone': 1.0, 'mail_ask': .5, 'mail_say': .5, 'mail_thanks': .3, 'mail_cc': 2.2,
                       'mail_thread': .7, 'sent': .6, 'calendar': .8, 'slack_channel': 2.0, 'slack_bot': 2.5, 'slack_dm': .6, 'chat_dm': 1.4, 'chat_group': 4.0,
                       'linkedin': .7, 'teams_dm': .6, 'github': 1.2},
             'window': 260, 'import': 120, 'seeds': (11, 12, 13, 14, 15)},
}
HELD_SHA = '9f54377be7caabc101ba2387ce3248c5108b62c9c6e1e24eaa76a3df997c07b3'
PEOPLE = {'mail_ask', 'mail_say', 'mail_thanks', 'mail_cc', 'mail_thread', 'sent', 'slack_channel', 'slack_dm', 'chat_dm', 'chat_group', 'linkedin', 'teams_dm', 'github'}
PAUSE_HOURS, AFTER_HOURS = 43, 150


def signals(spec, seed):
    """[(came in, account, event, direct, ask)] in order. direct: a person wrote to the owner, who hasn't answered; ask:
    and asked something."""
    rng, out, n = random.Random(seed), [], 0

    def add(at, account, kind, title, body, meta, direct=False, ask=False, occurred=None):
        nonlocal n
        n += 1
        out.append((at, account, {'account_id': account, 'source_id': f's{n}', 'kind': kind, 'occurred_at': (occurred or at).isoformat(), 'title': title,
                                  'body': body, 'metadata': meta, 'deleted': False}, direct, ask))

    def mail(at, box, sender, title, body, direct=False, ask=False, to=ME, labels=('INBOX',), thread=None, occurred=None, **meta):
        add(at, box, 'gmail.message', title, body, {'from': sender, 'to': to, 'labels': list(labels), 'thread_id': thread or f'th{n}', **meta}, direct, ask, occurred)

    def one(cls, at):
        box, who = rng.choice(('work-mail', 'work-mail', 'home-mail')), rng.randrange(40)
        person = f'Person {who} <p{who}@people{who % 7}.example>'
        asks = rng.random() < .5
        words = rng.choice(ASKS if asks else SAYS)
        if cls == 'newsletter':
            mail(at, box, f'Shop {who % 9} <news@shop{who % 9}.example>', f'Deals {n}', 'Save this week.', labels=('CATEGORY_PROMOTIONS',), list_unsubscribe='<mailto:u@shop.example>')
        elif cls == 'auto':
            mail(at, box, f'Service <no-reply@service{who % 5}.example>', f'Update {n}', 'Your status changed.', labels=('INBOX', 'CATEGORY_UPDATES'))
        elif cls == 'stripe':
            add(at, 'payments', 'stripe.event', 'Payment succeeded', '', {'type': 'charge.succeeded'})
        elif cls == 'phone':
            add(at, 'phone', 'android.notification', 'Rain at 4', '', {'package_name': 'com.example.weather', 'notification_key_hash': f'k{n}'})
        elif cls == 'mail_ask':
            mail(at, box, person, f'Question {n}', rng.choice(ASKS), True, True)
        elif cls == 'mail_say':
            mail(at, box, person, f'News {n}', rng.choice(SAYS), True)
        elif cls == 'mail_thanks':
            mail(at, box, person, 'Thanks!', 'Thanks, have a good day.', True)
        elif cls == 'mail_cc':
            mail(at, box, person, f'Team update {n}', words, to=f'a@x.example, b@x.example, c@x.example, {ME}')
        elif cls == 'mail_thread':  # a question, the owner's answer, sometimes their next question
            thread, gap = f'conv{n}', dt.timedelta(minutes=rng.randrange(20, 600))
            again = rng.random() < .5
            mail(at, box, person, f'Matter {n}', rng.choice(ASKS), thread=thread)
            mail(at + gap, box, f'Owner <{ME}>', f'Re: Matter {n}', 'Here it is.', to=f'p{who}@people{who % 7}.example', labels=('SENT',), thread=thread, **{'in-reply-to': '<q>'})
            if again:
                mail(at + gap * 2, box, person, f'Re: Matter {n}', 'Thanks. Can you also send the second one?', True, True, thread=thread, **{'in-reply-to': '<a>'})
        elif cls == 'sent':
            mail(at, box, f'Owner <{ME}>', f'Note {n}', 'As discussed.', to=f'p{who}@people{who % 7}.example', labels=('SENT',))
        elif cls == 'calendar':
            add(at, 'calendar', 'calendar.event', f'Meeting {n}', 'Agenda', {'attendees': [{'email': f'p{who}@people.example'}]},
                occurred=at + dt.timedelta(hours=rng.choice((6, 20, 40, 90, 300))))
        elif cls == 'slack_channel':
            add(at, 'slack', 'slack.message', '#team', words, {'conversation_type': 'channel', 'channel_id': f'C{who % 4}', 'user_id': f'U{who}', 'message_ts': f'{n}.1', 'thread_ts': f'{n}.1'})
        elif cls == 'slack_bot':
            add(at, 'slack', 'slack.message', '#builds', 'Build passed', {'conversation_type': 'channel', 'channel_id': 'C9', 'bot_id': 'B1', 'message_ts': f'{n}.1', 'thread_ts': f'{n}.1'})
        elif cls == 'slack_dm':
            add(at, 'slack', 'slack.message', f'DM {who}', words, {'conversation_type': 'dm', 'channel_id': f'D{who}', 'user_id': f'U{who}', 'message_ts': f'{n}.1', 'thread_ts': f'{n}.1'}, True, asks)
        elif cls == 'chat_dm':  # a chat message comes in one to three pieces
            for i in range(rng.randrange(1, 4)):
                add(at + dt.timedelta(minutes=i), 'whatsapp', 'whatsapp.message', f'Person {who}', words if i == 0 else 'And one more thing.',
                    {'chat_id': f'32{who}@s.whatsapp.net', 'from': f'Person {who}', 'from_me': False}, True, asks and i == 0)
        elif cls == 'chat_group':
            add(at, 'whatsapp', 'whatsapp.message', 'Group', words, {'chat_id': f'g{who % 3}@g.us', 'from': f'Person {who}', 'from_me': False})
        elif cls == 'linkedin':
            add(at, 'linkedin', 'linkedin.message', f'Person {who}', words, {'conversation_id': f'li{who}', 'from': f'Person {who}', 'from_me': False, 'group': False}, True, asks)
        elif cls == 'teams_dm':
            add(at, 'teams', 'teams.message', f'Person {who}', words, {'chat_id': f'te{who}', 'chat_kind': 'oneOnOne', 'from_me': False, 'user_id': f'x{who}'}, True, asks)
        elif cls == 'github':
            add(at, 'github', 'github.issue', f'Issue {n}', words, {'url': f'https://github.example/{n}'})

    for hour in range(PAUSE_HOURS + AFTER_HOURS):
        for cls, rate in spec['rates'].items():
            rate *= DAY[(START + dt.timedelta(hours=hour)).hour] if cls in PEOPLE else 1
            for _ in range(int(rate) + (rng.random() < rate % 1)):
                one(cls, START + dt.timedelta(hours=hour, minutes=rng.uniform(0, 59)))
    for _ in range(spec['import']):  # a mailbox connected again late in the pause: a week of mail at once
        at, occurred = START + dt.timedelta(hours=PAUSE_HOURS - 4), START - dt.timedelta(hours=rng.uniform(1, 120))
        who = rng.randrange(40)
        mail(at, 'home-mail', f'Person {who} <p{who}@people.example>' if rng.random() < .3 else f'Shop <news@shop{who}.example>', f'Old mail {n}', 'From before.', occurred=occurred,
             labels=('INBOX',) if who % 2 else ('CATEGORY_PROMOTIONS',))
    return sorted(out, key=lambda s: (s[0], s[2]['source_id']))


def digest(name):
    """A hash of a set's signals and windows: shows the held-out set is the one frozen before the order was worked out."""
    spec = SPECS[name]
    found = [[(at.isoformat(), account, event, direct, ask) for at, account, event, direct, ask in signals(spec, seed)] for seed in spec['seeds']]
    return hashlib.sha256(json.dumps([spec['window'], found], sort_keys=True).encode()).hexdigest()


def replay(spec, seed):
    """The catch-up. {'runs': [...], 'seen': {source_id: (came in, reviewed at, run number, direct, ask)}, 'backlog': n, 'left': n}"""
    import timeutil
    from machine.main import Store
    from machine.store import review as review_store
    found, kept = signals(spec, seed), timeutil.PINNED
    with tempfile.TemporaryDirectory() as folder:
        try:
            timeutil.pin(START)
            store = Store(Path(folder) / 'events.sqlite')
            boxes = sorted({s[1] for s in found})
            store.accounts = [{'id': b, 'service': 'gmail', 'email': ME} if b.endswith('-mail') else {'id': b, 'service': b} for b in boxes]
            store.owner_user_ids = {OWNER_SLACK}
            at, i, runs, seen, ids, empty_at = START + dt.timedelta(hours=PAUSE_HOURS), 0, [], {}, {}, None

            def arrive(until):
                nonlocal i
                while i < len(found) and found[i][0] <= until:
                    page, stamp = {}, found[i][0]
                    while i < len(found) and found[i][0] <= until and found[i][0] - stamp < dt.timedelta(minutes=5):
                        page.setdefault(found[i][1], []).append(found[i][2]); i += 1
                    timeutil.pin(stamp)
                    for account, events in page.items():
                        store.commit_page(account, {}, events)
                timeutil.pin(until)

            def waiting():
                with store.connect() as db:
                    return db.execute('SELECT count(*),min(ingested_at) FROM events WHERE analyzed_version<version').fetchone()
            truth = {s[2]['source_id']: s for s in found}
            arrive(at)
            backlog, end, window_ends, used = waiting()[0], START + dt.timedelta(hours=PAUSE_HOURS + AFTER_HOURS), at + dt.timedelta(hours=WINDOW_HOURS), 0.0
            while at < end and empty_at is None:
                arrive(at)
                job = f'run{len(runs)}'
                with store.connect() as db:
                    db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,planned,promising) VALUES(?,'running',?,?,0,0)", (job, at.isoformat(), at.isoformat()))
                session = review_store.REVIEW_SESSION_PREFIX + job
                claim = store.begin_analysis(boxes, 120, session, job)
                if not claim.get('analysis_id'):
                    empty_at = at
                    break
                with store.connect() as db:
                    items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0])
                    ids.update(dict(db.execute('SELECT id,source_id FROM events').fetchall()))
                cost = review_store.claim_weight(items)
                run = {'at': at, 'claimed': len(items), 'cost': cost, 'resumed': bool(claim.get('resumed')),
                       'ages': [(at - truth[ids[x['id']]][0]).total_seconds() / 3600 for x in items],
                       'direct': sum(truth[ids[x['id']]][3] for x in items)}
                if used + cost > spec['window']:  # the window's end: the run stops, its claim goes to the next window's first run
                    run['interrupted'] = True
                    at, used = window_ends, 0.0
                    window_ends = at + dt.timedelta(hours=WINDOW_HOURS)
                    timeutil.pin(at - dt.timedelta(hours=1))
                    with store.connect() as db:
                        db.execute("UPDATE analyses SET status='retryable',last_error='run_interrupted',error_at=? WHERE id=?", (timeutil.now(), claim['analysis_id']))
                        db.execute("UPDATE review_runs SET status='error',finished_at=? WHERE run_id=?", (timeutil.now(), job))
                else:
                    used += cost
                    done = at + dt.timedelta(minutes=RUN_MINUTES)
                    timeutil.pin(done)
                    store.finish_analysis(claim['analysis_id'], 'Reviewed', session, job)
                    with store.connect() as db:
                        db.execute("UPDATE review_runs SET status='ok',finished_at=? WHERE run_id=?", (done.isoformat(), job))
                    for x in items:
                        sid = ids[x['id']]
                        seen.setdefault(sid, (truth[sid][0], done, len(runs) + 1, truth[sid][3], truth[sid][4]))
                    at = done + dt.timedelta(minutes=GAP_MINUTES)
                    if at >= window_ends:
                        window_ends, used = at + dt.timedelta(hours=WINDOW_HOURS), 0.0
                run['left'], oldest = waiting()
                run['oldest_hours'] = (done - dt.datetime.fromisoformat(oldest)).total_seconds() / 3600 if oldest and not run.get('interrupted') else None
                runs.append(run)
                if run['left'] <= 40 and not run.get('interrupted'):  # caught up: what is left is what came in since
                    empty_at = at
            return {'runs': runs, 'seen': seen, 'backlog': backlog, 'empty_at': empty_at, 'found': found, 'left': waiting()[0]}
        finally:
            timeutil.PINNED = kept


def measure(result):
    """The numbers of one catch-up."""
    t0 = START + dt.timedelta(hours=PAUSE_HOURS)
    stop = result['empty_at'] or max(r['at'] for r in result['runs'])
    seen, missing = result['seen'], (dt.datetime.max.replace(tzinfo=dt.timezone.utc), 10**6)

    def worst(rows):
        """(run number, hours since the catch-up began) when the last of these was reviewed"""
        ends = [(seen[s[2]['source_id']][2], (seen[s[2]['source_id']][1] - t0).total_seconds() / 3600) if s[2]['source_id'] in seen else missing[::-1] for s in rows]
        return (max(e[0] for e in ends), max(e[1] for e in ends)) if ends and all(e[0] < 10**6 for e in ends) else None
    waiting = [s for s in result['found'] if s[0] <= t0]
    day = dt.timedelta(hours=24)
    occurred = lambda s: dt.datetime.fromisoformat(s[2]['occurred_at'])
    recent = [s for s in waiting if s[3] and t0 - occurred(s) <= day]
    newer = [s for s in result['found'] if s[3] and t0 < s[0] <= stop - dt.timedelta(hours=WINDOW_HOURS)]
    waits = sorted((seen[s[2]['source_id']][1] - s[0]).total_seconds() / 3600 for s in newer if s[2]['source_id'] in seen)
    others = sorted((v[1] - v[0]).total_seconds() / 3600 for v in seen.values())
    done = [r for r in result['runs'] if not r.get('interrupted')]
    talks, late = {}, 0  # messages reviewed in a later run than a newer one of their own thread or one-to-one chat
    for s in result['found']:
        m, sid = s[2]['metadata'], s[2]['source_id']
        talk = m.get('thread_id') or (m.get('chat_id') if not str(m.get('chat_id')).endswith('@g.us') else None) or m.get('conversation_id') or (
            m.get('channel_id') if m.get('conversation_type') == 'dm' else None)
        if talk and sid in seen:
            talks.setdefault((s[1], talk), []).append((s[2]['occurred_at'], seen[sid][2]))
    for runs in talks.values():
        runs.sort()
        late += sum(1 for i, (_, run) in enumerate(runs) if any(later < run for _, later in runs[i + 1:]))
    pct = lambda xs, q: round(xs[min(len(xs) - 1, int(q * len(xs)))], 1) if xs else None
    return {'waiting': result['backlog'], 'recent direct': len(recent), 'all direct': sum(1 for s in waiting if s[3]),
            'recent asks, run and hours': worst([s for s in recent if s[4]]), 'recent direct, run and hours': worst(recent),
            'all direct, run and hours': worst([s for s in waiting if s[3]]),
            'new direct wait p50/p95/max h': (pct(waits, .5), pct(waits, .95), pct(waits, 1)),
            'direct in runs 1-3': [r['direct'] for r in done[:3]], 'median age claimed h, runs 1-3': [round(statistics.median(r['ages']), 1) for r in done[:3]],
            'oldest left h, runs 1/3/6': [round(done[k]['oldest_hours'], 1) if len(done) > k and done[k]['oldest_hours'] is not None else None for k in (0, 2, 5)],
            'longest wait of any h': round(others[-1], 1), 'empty after h': round((result['empty_at'] - t0).total_seconds() / 3600, 1) if result['empty_at'] else None,
            'reviewed after a newer one of their thread': late, 'runs': len(result['runs']), 'reviewed twice': sum(r['claimed'] for r in done) - len(seen), 'left': result['left']}


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('name', choices=sorted(SPECS))
    args.add_argument('--app', default=str(Path(__file__).resolve().parent.parent))
    args.add_argument('--seed', type=int)
    args.add_argument('--digest', action='store_true')
    args = args.parse_args()
    if args.digest:
        print(digest(args.name))
        raise SystemExit
    sys.path.insert(0, args.app)
    for seed in [args.seed] if args.seed is not None else SPECS[args.name]['seeds']:
        print('seed', seed)
        for key, value in measure(replay(SPECS[args.name], seed)).items():
            print(f'  {key}: {value}')
