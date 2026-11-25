"""What a regular review claims while the Machine is behind (Store.begin_analysis): after a usage limit, a pause or a big
import, with more waiting than BEHIND_RUNS whole reviews take. Until then a claim shares itself out over the sources by
how much waits in each, oldest and newest by turns, whoever wrote: fine while one or two reviews take it all, but with
1,000 waiting most of a review went to what was 40 hours old and to the noisiest sources, and someone who wrote this
morning waited behind it.

Behind, two thirds of a review go to what likely needs the owner, recent first (`recent`): to-dos they wrote themselves,
what is on their calendar within SOON_HOURS (at most one in MEETINGS of the review), people writing to them directly
whom they haven't answered since, then other people's messages; never mailings, notifications, receipts or the owner's
own. Each step takes turns over the sources, so a noisy one never crowds out another. A conversation is claimed whole
(its waiting messages, the owner's own included, at most CONVERSATION of them), so a question and what came after it are
judged together, never the newer half first.

The other third goes to what came in first, whatever it is, so everything gets its turn: a signal with N waiting ones
that came in before it is claimed within about N / 40 new full reviews, however much keeps coming in (an unfinished
claim resumes first, and a message put off once waits behind the ones never put off, as in any claim). A review takes as much as before, so the backlog empties
as fast.

Plain code on what is already there, no model call: todo_likely, review_wait and need_rank, as in the first look."""
import datetime as dt

from machine import kinds
from machine.store import conversation, review_wait, todo_likely
from machine.store.events import RUN_SIGNAL_BUDGET, SET_ASIDE_AFTER

BEHIND_RUNS = 2         # behind: what waits fills more than this many whole reviews, so it needs a third one
OLDEST_SHARE = 3        # one in this many of a review goes to what came in first
MEETINGS = 10           # at most one in this many goes to what is on the calendar soon
SOON_HOURS = 48         # on the calendar soon
RECENT_HOURS = (24, 72)  # a day, three days: the newer step first
CONVERSATION = 20       # of one conversation's waiting messages per claim
SCAN = 3000             # waiting signals looked at, the newest of each source; what came in first has its own query
SLIM = 'id,account_id,kind,title,occurred_at,ingested_at,deferrals,deleted,metadata,version'  # no body: it can be long
LIGHTEST = 0.25         # what a signal takes of a review at least (review.BRIEF_WEIGHT)

# The order a review's recent part goes in: a person directly or another person's message, by how long ago (RECENT_HOURS)
OWN_TODO, SOON = 0, 1
STEPS = {('direct', 0): 2, ('direct', 1): 3, ('others', 0): 4, ('direct', 2): 5, ('others', 1): 6, ('others', 2): 7}


def scan(db, counts, current):
    """The waiting signals looked at, without their text: the newest of each source, up to what is on soon."""
    waiting = [a for a, n in counts.items() if n]
    until = (current + dt.timedelta(hours=SOON_HOURS)).isoformat()
    found = []
    for account in waiting:
        found += [dict(r) for r in db.execute(f'SELECT {SLIM} FROM events WHERE account_id=? AND analyzed_version<version AND deferrals<? '
                                              'AND occurred_at<=? ORDER BY occurred_at DESC LIMIT ?',
                                              (account, SET_ASIDE_AFTER, until, max(200, SCAN // len(waiting))))]
    return found


def behind(counts, rows, weigh):
    """Whether what waits fills more than BEHIND_RUNS reviews: each by what it takes of one (a newsletter's title line a
    quarter of a message), the ones not looked at by the least one can take."""
    return sum(map(weigh, rows)) + (sum(counts.values()) - len(rows)) * LIGHTEST > BEHIND_RUNS * RUN_SIGNAL_BUDGET


def conversation_of(row, m):
    """The conversation a message is in (a mail thread, a chat, a Slack thread), or itself."""
    value = m.get(conversation.CONTEXT_KEYS.get(row['kind']) or '')
    if value and row['kind'] == 'slack.message' and not conversation.one_to_one(row['kind'], m):
        value = f"{value}:{m.get('thread_ts') or m.get('message_ts') or row['id']}"
    return (row['account_id'], row['kind'], str(value)) if value else (row['account_id'], 'signal', row['id'])


def own(row, m, slack_ids):
    return bool(m.get('from_me') or {'SENT', 'DRAFT'} & set(m.get('labels') or ()) or (row['kind'] == 'slack.message' and m.get('user_id') in slack_ids))


def who(store, row, m, rank, people):
    """'direct' (a person to the owner alone), 'others' (another person's message) or None (automated, the owner's own)."""
    if row['deleted'] or own(row, m, store.owner_user_ids) or review_wait.can_wait(row, people):
        return None
    chat = kinds.KINDS.get(row['kind'], {}).get('family') == kinds.CHAT
    if chat and m.get('mentions_me') or (rank == 0 and (not chat or row['kind'] == 'slack.message' or conversation.one_to_one(row['kind'], m))):
        return 'direct'
    return 'direct' if row['kind'] == 'teams.message' and m.get('chat_kind') == 'oneOnOne' else 'others'


def steps(store, rows, addresses, people, current):
    """({conversation: its step, the row that leads it and its rank}, {conversation: its waiting rows, newest first})."""
    soon, stamp = (current + dt.timedelta(hours=SOON_HOURS)).isoformat(), current.isoformat()
    talks, meta = {}, {}
    for row in sorted(rows, key=lambda r: (r['occurred_at'], r['id']), reverse=True):
        meta[row['id']] = todo_likely.metadata(row)
        talks.setdefault(conversation_of(row, meta[row['id']]), []).append(row)
    ages = [(current - dt.timedelta(hours=h)).isoformat() for h in RECENT_HOURS]
    found = {}
    for key, talk in talks.items():
        for row in talk:  # newest first: the newest of its first step leads
            m = meta[row['id']]
            if row['kind'] == 'owner.card' and not row['deleted']:
                found[key] = (OWN_TODO, row, 0)
                break
            if row['kind'] == 'calendar.event':
                if stamp <= row['occurred_at'] <= soon and not row['deleted']:
                    found[key] = (SOON, row, 1)
                break
            if own(row, m, store.owner_user_ids):
                if row['kind'] == 'gmail.message':
                    continue  # mail: Store.answered decides (a forward answers nobody)
                break  # the owner wrote since: what came before it is answered
            rank = store.need_rank(row, addresses)
            kind = who(store, row, m, rank, people)
            step = kind and STEPS[kind, sum(row['occurred_at'] < a for a in ages)]
            if step and (key not in found or step < found[key][0]):  # a mention under newer talk in a group leads
                found[key] = (step, row, 0 if kind == 'direct' else 2)
    return found, talks


def full(db, ids):
    ids, found = list(ids), {}
    for i in range(0, len(ids), 400):
        part = ids[i:i + 400]
        found.update((r['id'], dict(r)) for r in db.execute('SELECT * FROM events WHERE id IN (' + ','.join('?' * len(part)) + ')', part))
    return found


def recent(store, db, rows, room, weigh, taken, current):
    """What likely needs the owner, recent first, up to `room` of the review: rows without their text. taken: the ids
    already in the claim, which it adds its own to."""
    addresses, people = store.review_own_addresses(db), review_wait.People(db)
    found, talks = steps(store, rows, addresses, people, current)
    # Each source's likeliest for this review, with their text: a question, an ask or a date at the top of it
    by_account = {}
    for key, (step, row, rank) in found.items():
        if row['id'] not in taken:
            by_account.setdefault(row['account_id'], []).append((step, row['deferrals'], key, row, rank))
    short = []
    for queue in by_account.values():
        queue.sort(key=lambda u: u[3]['occurred_at'], reverse=True)
        queue.sort(key=lambda u: u[:2])
        short += queue[:int(room)]
    texts, checked, queues = full(db, [u[3]['id'] for u in short]), 0, {}
    for step, deferrals, key, row, rank in sorted(short, key=lambda u: u[0]):
        row, live = texts[row['id']], False
        if rank == 0 and row['kind'] == 'gmail.message' and checked < todo_likely.THREAD_CHECKS:
            checked += 1
            if store.answered(db, row):
                continue
            live = store.owner_wrote_in(db, row['account_id'], todo_likely.metadata(row))
        score = -dt.datetime.fromisoformat(row['occurred_at']).timestamp() if step == SOON else todo_likely.score(row, rank, current, people, False, live)
        queues.setdefault(step, {}).setdefault(row['account_id'], []).append((deferrals, -score, row['id'], key))
    picked, spent, left = [], dict.fromkeys(by_account, 0), room
    for step in sorted(queues):
        turns = {a: sorted(q) for a, q in queues[step].items()}
        most = min(left, max(room // MEETINGS, 1)) if step == SOON else left
        while turns and most > 0:
            account = min(turns, key=lambda a: (spent[a], turns[a][0]))  # the source with the least of this review so far
            _, _, _, key = turns[account].pop(0)
            if not turns[account]:
                del turns[account]
            for row in talks[key][:CONVERSATION]:
                if row['id'] in taken or most <= 0:
                    continue
                taken.add(row['id'])
                picked.append(row['id'])
                weight = weigh(row)
                spent[account] += weight
                left -= weight
                most -= weight
    return picked, left


def oldest(db, counts, room, weigh, taken):
    """What came in first, whatever it is, up to `room` of the review (a message put off once behind the rest)."""
    wide = int(room / LIGHTEST) + len(taken) + 1
    first = []
    for account in [a for a, n in counts.items() if n]:
        first += db.execute('SELECT deferrals,ingested_at,id FROM events WHERE account_id=? AND analyzed_version<version AND deferrals<? '
                            'ORDER BY deferrals,ingested_at,id LIMIT ?', (account, SET_ASIDE_AFTER, wide)).fetchall()
    ids = [r['id'] for r in sorted(first, key=tuple) if r['id'] not in taken][:int(room / LIGHTEST) + 1]
    rows, picked = full(db, ids), []
    for i in ids:
        if room <= 0:
            break
        taken.add(i)
        picked.append(rows[i])
        room -= weigh(rows[i])
    return picked


def claim(store, db, counts, limit, weigh, interrupted, current):
    """(rows, the claim the first of them was recovered from) for this review while behind, else None. interrupted: the
    unfinished claims' signals, which go first as in any review."""
    if sum(counts.values()) <= BEHIND_RUNS * RUN_SIGNAL_BUDGET:
        return None  # at most that many reviews, whatever each takes: nothing more is read
    rows = scan(db, counts, current)
    if not behind(counts, rows, weigh):
        return None
    taken, first, recovered, room = set(), [], None, limit
    for row in interrupted:
        if room <= 0:
            break
        if row['account_id'] in counts and row['id'] not in taken:
            event = dict(row)
            recovered = recovered or event.pop('review_id')
            event.pop('review_id', None)
            taken.add(event['id'])
            first.append(event)
            room -= 1
    share = -(-room // OLDEST_SHARE)  # rounded up: the oldest always get a turn
    ids, left = recent(store, db, rows, room - share, weigh, taken, current) if room > share else ([], room - share)
    texts = full(db, ids)
    return first + [texts[i] for i in ids] + oldest(db, counts, share + left, weigh, taken), recovered
