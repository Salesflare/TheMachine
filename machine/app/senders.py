"""Who wrote a review's batch: the `sender` block of the review's memory (machine/app/recall.py).

A review judges new mail and messages. Without this it knew the owner's facts, decisions and open promises, but
nothing about who sent each signal unless it opened the Graph once per person. lines() gives it one short line per
sender the Graph knows something specific about: who they are to the owner (role, organization), how close, and the
gist of their summary. It reads what is already stored (graph_nodes, person_summaries): no model call, no new table.

Quality or nothing: a sender the Graph knows nothing specific about gets no line, and neither does the owner
themself. Someone the owner really dealt with before (wrote to on PAST_DAYS days or more, or met) is specific, also
when that closeness has faded: their line says so in a few words, so a review tells a personal check-in from someone
they know (it expects a reply) from the same words from a stranger (an opener), on every channel (the review prompt's Personal check-ins). A summary's line goes in only when its areas (Work, Personal) are those of the signals that person sent in
this batch (person_summary.prep_lines), so one side's memory never reaches a signal of the other side.

The block is short on purpose (SENDER_CHARS, about 400 tokens): the closest senders first, and a line that no longer
fits stays out. Each line is noted for the use log (memory_use.note, kind record)."""
import json
import sqlite3

import graph
import memory_use
import person_summary

SENDER_CHARS = 1600  # the whole block, its first line included: about 400 tokens a review
GIST_CHARS = 160     # of a summary's first line
SIGNALS_SHOWN = 4    # signal ids on a line, so the review knows which messages are theirs
PAST_DAYS = 2        # days the owner wrote to someone before it counts as a past exchange (one reply to a pitch doesn't)
# OpenClaw cuts a tool result at 64,000 characters (machine/store/review.py). The claim's reply also lists the
# projects and boards, so the block goes in only while the whole reply stays under the cut: past it the block
# would be cut off unread, and logged as read.
REPLY_CUT = 64000
REPLY_RESERVE = 2000
HEADER = ('Who wrote these, from the Graph (who they are to the owner, how close, past exchanges, what is known; signals by id). '
          'Senders not listed: nothing specific known, no real exchange with the owner yet. It is context for judging; what the message says still decides.')


def clip(text, limit):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + '…'


def batch(db, analysis_id):
    """The signals of a review's claim: [events row], without the ones it set aside."""
    row = db.execute('SELECT items FROM analyses WHERE id=?', (analysis_id,)).fetchone()
    ids = [int(i['id']) for i in json.loads(row['items'] or '[]') if not i.get('excluded')] if row else []
    if not ids:
        return []
    return db.execute(f"SELECT id,account_id,kind,metadata FROM events WHERE id IN ({','.join('?' * len(ids))}) ORDER BY id", ids).fetchall()


def wrote(db, rows, owner, area):
    """{node id: {'row', 'signals': [event id], 'sides': {side or None}}} for the people who wrote these signals. The
    owner's own messages, meetings and anyone the Graph has no person for are left out (graph.event_parties)."""
    found = {}
    for r in rows:
        metadata = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        sender, _ = graph.event_parties(r['kind'], metadata, owner)
        if not sender or owner.has(sender):
            continue
        node = graph.resolve(db, sender)
        if not node or node['kind'] != 'person':
            continue
        entry = found.setdefault(node['id'], {'row': node, 'signals': [], 'sides': set()})
        entry['signals'].append(r['id'])
        entry['sides'].add(area.get(r['account_id']))
    return found


def gist(db, node_id, sides):
    """The first line of their summary that every one of their signals in this batch may see: a line stays out when
    its areas are not those of a signal's account (an account in no area sees only lines without one)."""
    try:
        allowed = [person_summary.prep_lines(db, node_id, {side} if side else set()) for side in sides]
    except (sqlite3.Error, ValueError, KeyError, TypeError):
        return ''
    if not allowed:
        return ''
    return next((clip(line, GIST_CHARS) for line in allowed[0] if all(line in other for other in allowed[1:])), '')


def past(view):
    """A few words on the owner's own exchanges with them ('the owner wrote on 9 days, met on 2'), '' when they never
    wrote to or met them: what tells a relationship from a stranger, also once closeness has faded."""
    wrote, met = view.get('wrote_days') or 0, view.get('met_days') or 0
    bits = ([f'the owner wrote on {wrote} day' + ('s' if wrote != 1 else '')] if wrote else []) \
        + ([f'met on {met} day' + ('s' if met != 1 else '')] if met else [])
    return ', '.join(bits)


def line(db, entry):
    """One sender's line, or '' when the Graph knows nothing specific about them: no role, no summary line this batch
    may see, less than a regular contact and no past exchange with the owner (PAST_DAYS)."""
    view = graph.node_view(entry['row'])
    summary = gist(db, view['id'], entry['sides'])
    known = (view.get('wrote_days') or 0) >= PAST_DAYS or (view.get('met_days') or 0) > 0
    if not view['role'] and not summary and view['closeness'] not in ('close', 'regular') and not known:
        return ''
    history = past(view)
    org = db.execute('SELECT name,info FROM graph_nodes WHERE id=?', (view['org'],)).fetchone() if view['org'] else None
    org_role = json.loads(org['info'] or '{}').get('role') if org else None
    bits = ([clip(view['role'], 80)] if view['role'] else []) \
        + ([f"at {clip(org['name'], 60)}" + (f' ({clip(org_role, 60)})' if org_role else '')] if org else []) \
        + [f"{view['closeness']} contact" + (', gone quiet' if view['quiet'] else '') + (f' ({history})' if history else '')] \
        + ([f'summary: {summary}'] if summary else [])
    shown, more = entry['signals'][:SIGNALS_SHOWN], len(entry['signals']) - SIGNALS_SHOWN
    signals = ', '.join(str(i) for i in shown) + (f' and {more} more' if more > 0 else '')
    return f"- {clip(view['name'], 60)} (signal{'s' if len(entry['signals']) > 1 else ''} {signals}): " + '; '.join(bits)


def lines(app, analysis_id, limit=SENDER_CHARS):
    """The block's text for a review's claim, '' when no sender has a line. The closest senders first; a line that no
    longer fits in `limit` characters stays out."""
    if not analysis_id:
        return ''
    area = {a.get('id'): graph.account_side(a) for a in app.config.get('accounts', []) if a.get('id')}
    with app.store.connect() as db:
        found = wrote(db, batch(db, analysis_id), graph.Owner(app.config, db), area)
        text, kept = HEADER, []
        for entry in sorted(found.values(), key=lambda e: (-e['row']['strength'], e['signals'][0])):
            if len(text) + GIST_CHARS > limit and kept:  # full: don't read the rest's summaries for nothing
                break
            one = line(db, entry)
            if one and len(text) + len(one) + 1 <= limit:
                text += '\n' + one
                kept.append((entry['row']['id'], one))
    for node, one in kept:
        memory_use.note('record', node, one, 'about', about=(node,), source='signal')
    return text if kept else ''
