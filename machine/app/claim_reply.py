"""What a review's claim (begin_analysis) carries next to its signals, kept small enough that the whole reply stays
under the cut: the boards with only the projects this claim touches, and a plain note on anything left out.

A board used to come with every project on it (150 a board), in every claim, whatever the batch was about. That was
most of a small claim and pushed a full one past OpenClaw's cut, which took the signals at the end of the reply. The
rest of a board is one lookup away: graph {"board": name}."""
import json

import graph
from machine.store.review import REVIEW_PAGE_CHARS
from machine.text import encoded

BOARD_PROJECTS = 1000  # read per board, so a project this claim is about is found however long the board is
BOARD_LOOKUP = 300  # one whole board on request, most recently moved first
THREAD_SIGNALS = 30  # of a signal's mail thread, the latest ones
SIGNAL_PEOPLE = 6  # of a signal's people, its sender first
PERSON_PROJECTS = 8  # of the board projects a person or their organization is on, the closest ones
BOARDS_NOTE = 'Each board lists only the projects this claim touches; others counts the rest. See a whole board with graph {"board": "<name>"}.'
# What goes when a reply is still too long, in this order: the signals are what the review came for and stay
LEFT_OUT = (('projects', 'the project names to reuse (find one with graph query)'),
            ('board projects', 'the projects on each board (see a board with graph {"board": "<name>"})'),
            ('share_groups', 'the share groups unsure threads already have'),
            ('boards', 'the boards (list them with graph {"boards": true})'))


def claim_ids(db, analysis_id):
    """Every signal of the claim, on all its pages."""
    row = db.execute('SELECT items FROM analyses WHERE id=?', (analysis_id,)).fetchone()
    return [int(i['id']) for i in json.loads(row['items'] or '[]') if not i.get('excluded')] if row else []


def in_projects(db, event_ids):
    """Names of the projects these signals are in: labeled into, or linked (surely or probably) by the graph."""
    names = set()
    for start in range(0, len(event_ids), 400):
        ids = event_ids[start:start + 400]
        marks = ','.join('?' * len(ids))
        names.update(r[0] for r in db.execute(
            f"SELECT p.name FROM graph_events g JOIN projects p ON g.node_id='project:'||p.id WHERE g.event_id IN ({marks}) "
            f'UNION SELECT p.name FROM event_projects e JOIN projects p ON p.id=e.project_id WHERE e.event_id IN ({marks})', (*ids, *ids)))
    return names


def claimed_projects(db, event_ids, config):
    """Names of the projects a claim is about. A signal that just came in is in no project yet (the graph links it at
    its next build, up to ten minutes later), so it also counts what its mail thread is in and the board projects of
    the people in it and of their organization: a partner's reply shows their listing before the graph has seen it."""
    names = in_projects(db, event_ids)
    owner, threads, people = graph.Owner(config, db), set(), set()
    for start in range(0, len(event_ids), 400):
        ids = event_ids[start:start + 400]
        for r in db.execute(f"SELECT account_id,kind,metadata FROM events WHERE id IN ({','.join('?' * len(ids))})", ids):
            metadata = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
            if metadata.get('thread_id'):
                threads.add((r['account_id'], str(metadata['thread_id'])))
            sender, others = graph.event_parties(r['kind'], metadata, owner)
            people.update([i for i in [sender, *sorted(others)] if i and not owner.has(i)][:SIGNAL_PEOPLE])
    earlier = [r[0] for account, thread in sorted(threads) for r in db.execute(
        "SELECT id FROM events WHERE json_extract(metadata,'$.thread_id')=? AND account_id=? AND deleted=0 ORDER BY id DESC LIMIT ?", (thread, account, THREAD_SIGNALS))]
    names |= in_projects(db, earlier)
    on_board = 'p.board_id IS NOT NULL AND p.closed_at IS NULL'
    for person in sorted(people):
        node = graph.resolve(db, person)
        if node and node['kind'] == 'person':
            names.update(r[0] for r in db.execute(f"SELECT p.name FROM graph_links l JOIN projects p ON l.b='project:'||p.id WHERE l.a=? AND l.kind='project' AND {on_board} "
                                                  'ORDER BY l.strength DESC LIMIT ?', (node['id'], PERSON_PROJECTS)))
    domains = {i.rpartition('@')[2].lower() for i in people if i.startswith('email:') and '@' in i}
    for domain in sorted(domains | {d.split('.', 1)[1] for d in domains if d.count('.') > 1}):  # mail.acme.example is acme.example's too
        names.update(r[0] for r in db.execute(f'SELECT p.name FROM projects p WHERE lower(p.org)=? AND {on_board} ORDER BY coalesce(p.stage_at,p.created_at) DESC LIMIT ?',
                                              (domain, PERSON_PROJECTS)))
    return names


def boards(db, analysis_id, config):
    """The boards for a claim: each one's stages and about (to place a new project), and where the projects in this
    claim (its signals, their mail threads and their people) stand, with their done_when. The other projects are
    counted, not listed."""
    mine = claimed_projects(db, claim_ids(db, analysis_id), config)
    out = []
    for b in graph.boards_brief(db, BOARD_PROJECTS):
        here = {name: stage for name, stage in b['projects'].items() if name in mine}
        done = {name: text for name, text in (b.get('done_when') or {}).items() if name in here}
        out.append({'board': b['board'], 'stages': b['stages'], **({'about': b['about']} if b.get('about') else {}),
                    **({'projects': here} if here else {}), **({'done_when': done} if done else {}),
                    **({'others': len(b['projects']) - len(here)} if len(b['projects']) > len(here) else {})})
    return out


def lookup(db, name=None):
    """graph {"board": name}: one whole board, each project with its stage (and done_when). graph {"boards": true}:
    the boards themselves, with how many projects each holds; a name no board has gets that list too, under no_board."""
    found = graph.boards_brief(db, BOARD_PROJECTS)
    wanted = str(name or '').strip().casefold()
    board = next((b for b in found if b['board'].casefold() == wanted), None)
    if not board:
        return {**({'no_board': str(name)} if name is not None else {}),
                'boards': [{k: v for k, v in b.items() if k not in ('projects', 'done_when')} | {'projects': len(b['projects'])} for b in found]}
    shown = dict(list(board['projects'].items())[:BOARD_LOOKUP])
    done = {n: t for n, t in (board.get('done_when') or {}).items() if n in shown}
    return {**{k: v for k, v in board.items() if k not in ('projects', 'done_when')}, 'projects': shown, **({'done_when': done} if done else {}),
            **({'more': len(board['projects']) - len(shown)} if len(board['projects']) > len(shown) else {})}


def fit(result, limit=REVIEW_PAGE_CHARS):
    """Keep a claim reply under the page size. The signals stay; what goes is named in left_out with how to get it."""
    if any(b.get('others') for b in result.get('boards') or []):
        result['boards_note'] = BOARDS_NOTE
    left = []
    for part, how in LEFT_OUT:
        if len(encoded(result)) <= limit:
            return result
        if part == 'board projects':
            trimmed = False
            for b in result.get('boards') or []:
                gone = b.pop('projects', None)
                b.pop('done_when', None)
                if gone:
                    b['others'] = b.get('others', 0) + len(gone)
                    trimmed = True
            if not trimmed:
                continue
            result['boards_note'] = BOARDS_NOTE
        elif result.pop(part, None) in (None, [], {}):
            continue
        elif part == 'boards':
            result.pop('boards_note', None)
        left.append(how)
        result['left_out'] = 'Left out to keep this reply whole: ' + '; '.join(left) + '.'
    views, moved = result.get('events') or [], []
    while len(views) > 1 and len(encoded(result)) > limit:  # only when a page itself is too long: the last signals wait
        moved.insert(0, views.pop()['id'])
        result['left_out'] = ('Left out to keep this reply whole: ' + '; '.join([*left, f'signals {moved} of this page (read them with events, their '
                                                                                           'account and event_ids, before finishing)']) + '.')
    return result
