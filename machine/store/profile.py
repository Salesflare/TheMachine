"""The Store's profile (refactor PR 18): who the owner is and how they work. The evidence a profile, roles or
organizations turn reads, saving what it found, and the quality and behavior numbers. A mixin of Store (assistant.py),
like App's mixins. Moved out of assistant.py as is."""
import collections
import datetime as dt
import email.utils
import json
import re
import sqlite3
import uuid

import authorship
import crm_import
import enrichment
import fleet_learnings
import graph
import learning_loop
import locale_prefs
from machine.store.graph_history import live
from machine.prompts.profile import VOICE_CHARS, VOICE_LINES
from machine.sources.connectors import load_connector
from machine.store.voices import OWN_KINDS, PROFILE_SKIP, sentences, similar, voice_block, voice_channel, VOICE_MAX
from machine.text import clamp, encoded
import shared_graph
import team_learnings
from timeutil import local_tz, now


def evidence_pages(items, budget=None, first=0):
    """Items split into pages of at most `budget` characters (`first`: what page 1 carries besides), at least one item
    a page, in order. The same evidence always gives the same pages."""
    budget, pages, size = budget or EVIDENCE_PAGE_CHARS, [[]], first
    for item in items:
        length = len(encoded(item)) + 2
        if pages[-1] and size + length > budget:
            pages.append([])
            size = 0
        pages[-1].append(item)
        size += length
    return pages


# `assistant profile`: one read-only turn of the owner's agent drafts USER.md lines (how they write,
# their role, who and what matters) from their own recent messages; the owner sees it before anything is saved.
PROFILE_SESSION_PREFIX = 'agent:main:assistant-review-profile-'


PROFILE_MESSAGES = 120  # the owner's own messages one draft reads, newest first, mixed across sources


PROFILE_MIN = 5         # fewer says too little about how someone writes


PROFILE_LISTS = {'languages': 4, 'examples': 4, 'matters': 8, 'leave_alone': 6}


PROFILE_TEXT = ('role', 'tone', 'greeting', 'sign_off', 'habits')


PROFILE_VOICES = 6      # one voice per channel: email reads nothing like WhatsApp or Telegram


PROFILE_TEMPLATE_COPIES = 2  # near-identical sends (outreach templates) kept per template


ROLES_PEOPLE = 15       # closest people without a role one roles turn names


ORGS_PEOPLE = 60        # people without an organization one organizations turn reads


# A profile, voices, roles or organizations turn reads its evidence in pages of about this many characters, well below
# OpenClaw's 64,000-character tool result: each page is a model step that resends the whole context, so fewer, fuller
# pages cost less for the same evidence (2026-10-26: 15 messages, 3 or 6 people a page took 5 to 10 steps).
EVIDENCE_PAGE_CHARS = 40000
SHARE_HISTORY_BATCH, SHARE_HISTORY_PAGE = 120, 20  # the Shared Graph's history pass: threads per turn, and per page


PROFILE_WEIGHTS = {'gmail.message': 2}  # drafts are mostly email, so email gets two turns per round


# Where a to-do came from, by meaning, as Feedback's rows name it ("How the to-dos are doing"): every kind of email is
# Email, problems The Machine found in itself are one row, a to-do the owner made is "Added by you". A connector's kinds
# go under its own name (its SETUP label); what is left (no signal, or one nothing names) is Other.
TODO_SOURCE = {'gmail.message': 'Email', 'ms_graph.message': 'Email', 'outlook.message': 'Email', 'fleet.email': 'Email',
               'calendar.event': 'Calendar', 'outlook.event': 'Calendar', 'ms_graph.event': 'Calendar', 'outlook_calendar.event': 'Calendar',
               'meeting.notes': 'Meeting notes', 'meeting.transcript': 'Meeting notes',
               'salesflare.email': 'CRM email', 'salesflare.meeting': 'CRM meeting',
               'slack.message': 'Slack', 'teams.message': 'Teams', 'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram', 'fleet.intercom': 'Intercom',
               'android.notification': 'Phone notifications', 'owner.card': 'Added by you',
               'fleet.request': 'Fleet', 'fleet.message': 'Fleet',
               'gateway.alert': 'The Machine itself', 'machine.fault': 'The Machine itself', 'machine.parked_fix': 'The Machine itself',
               'machine.system_log': 'The Machine itself'}


TODO_SOURCE_OTHER = 'Other'


def todo_source(kind):
    """Feedback's name for where a to-do with this first signal kind came from (TODO_SOURCE)."""
    if kind in TODO_SOURCE:
        return TODO_SOURCE[kind]
    plugin = load_connector(kind.split('.')[0]) if isinstance(kind, str) and '.' in kind else None
    label = (getattr(plugin, 'SETUP', None) or {}).get('label')
    return label if isinstance(label, str) and label else TODO_SOURCE_OTHER


def recap_day(value, with_time=False):
    """Fri, Oct 23 (and 09:30, or 9:30 AM) in the owner's time zone and format (locale_prefs), from a date or a time."""
    if len(str(value)) <= 10:
        return locale_prefs.day_text(dt.date.fromisoformat(str(value)[:10]))
    t = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone(local_tz())
    return locale_prefs.day_text(t) + (' ' + locale_prefs.clock_text(t) if with_time else '')


class ProfileStore:
    """Store methods for the owner's profile, roles and organizations."""

    def own_messages(self, limit=PROFILE_MESSAGES):
        """The owner's own recent messages (sent email, their chat messages), newest first and taken
        round-robin across sources so one busy chat can't drown out email. Quoted history is cut."""
        ids = sorted(self.owner_user_ids)
        queues = collections.OrderedDict()
        with self.connect() as db:
            db.execute('BEGIN')  # one read snapshot across replenishment and all source queues
            sent = authorship.MachineSent.load(db)  # drafts sent from a to-do are no example of how the owner writes
            for kind in OWN_KINDS:
                predicate = ("instr(metadata,'\"SENT\"')>0" if kind == 'gmail.message' else
                             f"json_extract(metadata,'$.user_id') IN ({','.join('?' for _ in ids)})" if kind == 'slack.message' else
                             "json_extract(metadata,'$.from_me')=1")
                params = ids if kind == 'slack.message' else []
                queue, copies = [], []
                # Per-source candidates, replenished after template/media filtering.
                # At most 40 * limit rows per source keeps even huge template archives bounded.
                for offset in range(0, limit * 40, limit * 4):
                    rows = db.execute("SELECT id,account_id,source_id,kind,occurred_at,title,body,metadata FROM events "
                                      f"WHERE deleted=0 AND kind=? AND ({predicate}) "
                                      "ORDER BY occurred_at DESC,id DESC LIMIT ? OFFSET ?",
                                      (kind, *params, limit * 4, offset)).fetchall()
                    for row in rows:
                        text = (row['body'] or '').split('[Quoted earlier messages', 1)[0].strip()
                        if len(text.split()) < 2 or PROFILE_SKIP.match(text) or sent.wrote(row, text):
                            continue
                        gist = ' '.join(re.sub(r'^\W*(?:hey|hi|hello|dear|hoi|dag)\b[^,\n!]{0,40}[,\n!]', '', text[:400], flags=re.I).split()).lower()[:120]
                        if sum(gist == other or (len(gist) > 60 and len(other) > 60 and similar(gist, other))
                               for other in copies) >= PROFILE_TEMPLATE_COPIES:
                            continue
                        copies.append(gist)
                        queue.append((row, text))
                        if len(queue) >= limit:
                            break
                    if len(queue) >= limit or len(rows) < limit * 4:
                        break
                if queue:
                    queues[kind] = queue
        picked = []
        while len(picked) < limit and any(queues.values()):
            for kind, queue in queues.items():
                for _ in range(PROFILE_WEIGHTS.get(kind, 1)):
                    if queue and len(picked) < limit:
                        picked.append(queue.pop(0))
        items = []
        for row, text in sorted(picked, key=lambda p: p[0]['occurred_at'], reverse=True):
            m = json.loads(row['metadata'])
            item = {'id': row['id'], 'source': OWN_KINDS[row['kind']], 'account': row['account_id'],
                    'date': recap_day(row['occurred_at'], True),
                    'text': clamp(text, 900 if row['kind'] == 'gmail.message' else 300)}
            if row['kind'] == 'gmail.message':
                item.update(to=clamp(str(m.get('to') or ''), 160), subject=clamp(row['title'] or '', 120))
            elif m.get('chat_name') or m.get('channel_name'):
                item['chat'] = clamp(str(m.get('chat_name') or m.get('channel_name')), 80)
            items.append(item)
        return items

    def frequent_unanswered(self, days=30, limit=10):
        """Email senders who write most often and whom the owner never wrote to: candidates for "leave alone"."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        written, counts = set(), collections.Counter()
        with self.connect() as db:
            for (metadata,) in db.execute("SELECT metadata FROM events WHERE kind='gmail.message' AND deleted=0 AND history=0 AND occurred_at>=?", (since,)):
                m = json.loads(metadata)
                if 'SENT' in m.get('labels', []):
                    written |= {a.lower() for _, a in email.utils.getaddresses([str(m.get(f) or '') for f in ('to', 'cc')]) if a}
                else:
                    counts.update({a.lower() for _, a in email.utils.getaddresses([str(m.get('from') or '')]) if a})
        own = {str(a.get('email', '')).lower() for a in self.accounts}
        return [{'sender': a, 'emails': n} for a, n in counts.most_common() if a not in written and a not in own][:limit]

    def profile_evidence(self, page=1, session=None):
        run_id = str(session or '').removeprefix(PROFILE_SESSION_PREFIX)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = (db.execute('SELECT run_id,evidence FROM profile_runs WHERE run_id=?', (run_id,)).fetchone() if session else
                   db.execute("SELECT run_id,evidence FROM profile_runs WHERE kind='profile' AND status IN ('starting','running') ORDER BY started_at DESC LIMIT 1").fetchone())
            if session and (not str(session).startswith(PROFILE_SESSION_PREFIX) or not run):
                raise ValueError('Unknown profile run')
            if run and run['evidence']:
                evidence = json.loads(run['evidence'])
            else:
                evidence = {'messages': self.own_messages(), 'frequent_unanswered_senders': self.frequent_unanswered()}
                if run:  # legacy active requests get one snapshot, never changing pages afterward
                    db.execute('UPDATE profile_runs SET evidence=? WHERE run_id=?', (json.dumps(evidence), run['run_id']))
        if 'token' in evidence:
            raise ValueError('A Find my skills run has no profile evidence')
        if 'import' in evidence:  # a CSV import's columns and unclear cells (crm_import.ai_evidence), one page
            return {'page': 1, 'pages': 1, **evidence['import']}
        if 'threads' in evidence:  # the Shared Graph's history pass
            threads, size = evidence['threads'], int(evidence.get('page_size') or SHARE_HISTORY_PAGE)
            pages = max(1, -(-len(threads) // size))
            page = min(max(int(page or 1), 1), pages)
            return {'page': page, 'pages': pages, 'threads': threads[(page - 1) * size:page * size]}
        if evidence.get('team_votes'):  # judging other Machines' learnings (team_learnings.py)
            return team_learnings.vote_page(evidence)
        if evidence.get('learnings'):  # a learnings run (team_learnings.py)
            return team_learnings.evidence_page(evidence, page)
        if evidence.get('fleet_learn'):  # team learnings from team conversations (fleet_learnings.py): one short page
            return fleet_learnings.page(evidence)
        if evidence.get('tune'):  # a learning pass (learning_loop.py): one short page
            return learning_loop.page(evidence)
        if 'people' in evidence:  # a roles or organizations run
            extra = {k: evidence[k] for k in ('organisations', 'corrections') if evidence.get(k)}
            split = evidence_pages(evidence['people'], first=len(encoded(extra)))
            page = min(max(int(page or 1), 1), len(split))
            result = {'page': page, 'pages': len(split), 'people': split[page - 1]}
            if page == 1:  # the organizations, and how the owner corrected earlier roles
                result.update(extra)
            return result
        items = evidence['messages']
        extra = {k: evidence.get(k) for k in ('notes', 'voices', 'frequent_unanswered_senders')}
        split = evidence_pages(items, first=len(encoded(extra)) + 200)
        page = min(max(int(page or 1), 1), len(split))
        result = {'page': page, 'pages': len(split), 'messages': split[page - 1]}
        if page == 1 and 'notes' in evidence:  # a voice study: the owner's style notes and the current blocks
            result.update(counts=dict(collections.Counter(i['channel'] for i in items)), style_notes=evidence['notes'], current_voices=evidence['voices'])
        elif page == 1:
            result['counts'] = dict(collections.Counter(i['source'] for i in items))
            result['frequent_unanswered_senders'] = evidence['frequent_unanswered_senders']
        return result

    def profile_start(self, again=False, room=None, auto=False):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='profile' AND (status IN ('starting','running') OR "
                             "(status='ok' AND finished_at>? AND NOT ?)) ORDER BY started_at DESC LIMIT 1",
                             ((dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=30)).isoformat(), int(bool(again)))).fetchone()
            if run:  # follow the running draft, or show the one just made
                return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
        evidence = {'messages': self.own_messages(), 'frequent_unanswered_senders': self.frequent_unanswered()}
        counts = collections.Counter(i['source'] for i in evidence['messages'])
        if sum(counts.values()) < PROFILE_MIN:
            raise ValueError(f'Only {sum(counts.values())} of your own messages are collected so far; that says too little about how you write. '
                             'Try again in a few days: assistant profile')
        run_id, started = uuid.uuid4().hex, now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='profile' AND (status IN ('starting','running') OR "
                             "(status='ok' AND finished_at>? AND NOT ?)) ORDER BY started_at DESC LIMIT 1",
                             ((dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=30)).isoformat(), int(bool(again)))).fetchone()
            if run:
                return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,room,evidence,auto) VALUES(?,'starting',?,?,?,?,?)",
                       (run_id, started, started, None if room is None else min(max(int(room), 400), 4000), json.dumps(evidence), int(bool(auto))))
        roles = self.roles_start(again=again, auto=auto)  # onboarding names the closest people too, right after the draft
        return {'run_id': run_id, 'started_at': started, 'counts': dict(counts), 'roles_run_id': roles.get('run_id')}

    def no_role_yet(self, event_ids):
        """The people a card or job is directly about who have no role yet."""
        ids = [int(i) for i in event_ids or () if str(i).lstrip('-').isdigit()]
        if not ids:
            return []
        try:
            with self.connect() as db:
                return [{'node_id': r['id'], 'name': r['name']} for r in db.execute(
                    "SELECT DISTINCT n.id,n.name,n.strength FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id WHERE g.direct=1 AND n.kind='person' "
                    "AND json_extract(n.info,'$.role') IS NULL AND coalesce(json_extract(n.info,'$.role_by'),'')!='owner' AND g.event_id IN (" + ','.join('?' for _ in ids) + ') ORDER BY n.strength DESC LIMIT 4', ids)]
        except sqlite3.Error:
            return []

    def role_evidence(self, limit=ROLES_PEOPLE):
        """The closest people with no role yet, each with what the graph knows and their first and latest
        messages with the owner, plus the main organizations with no role, for one roles turn."""
        people = []
        with self.connect() as db:
            owner = graph.Owner({'accounts': self.accounts}, db)
            owner.slack |= set(self.owner_user_ids)
            rows = db.execute(f"SELECT * FROM graph_nodes WHERE kind='person' AND {live()}>=0.5 AND json_extract(info,'$.role') IS NULL AND coalesce(json_extract(info,'$.role_by'),'')!='owner' "
                              f'ORDER BY {live()} DESC LIMIT ?', (limit,)).fetchall()
            for r in rows:
                view = graph.node_view(r)
                org = db.execute('SELECT name,info FROM graph_nodes WHERE id=?', (view['org'],)).fetchone() if view['org'] else None
                people.append({'node_id': r['id'], 'name': r['name'], 'ids': view['ids'][:4], 'closeness': view['closeness'],
                               'days_in_touch': {'owner_wrote': view['wrote_days'], 'they_wrote': view['heard_days'], 'met': view['met_days']},
                               'usual_gap_days': view['usual_gap_days'], 'hints': view['hints'],
                               'linkedin_headline': graph.headline(db, r['id']) if json.loads(r['info'] or '{}').get('has_headline') else None,
                               'organisation': {'node_id': view['org'], 'name': org['name'], 'role': json.loads(org['info']).get('role'),
                                                'profile': enrichment.summary(json.loads(org['info']).get('profile')),
                                                'others': [{'name': n['name'], 'role': n['role']} for n in graph.detail(db, view['org'], 0)['people_roles']
                                                           if n['id'] != r['id']][:5]} if org else None,
                               'projects': [n['name'] for n in graph.neighbours(db, r['id']) if n['kind'] == 'project'][:3],
                               'messages': graph.person_evidence(db, r['id'], owner)})
            orgs = [{'node_id': r['id'], 'name': r['name'], 'domain': json.loads(r['info']).get('domain'),
                     'about': (json.loads(r['info']).get('profile') or {}).get('about'), 'profile': enrichment.summary(json.loads(r['info']).get('profile')),
                     'people': [{'name': n['name'], 'role': n['role']} for n in graph.detail(db, r['id'], 0)['people_roles']][:6],
                     'messages': [m for n in graph.detail(db, r['id'], 0)['people_roles'][:2] for m in graph.person_evidence(db, n['id'], owner, 4)]}
                    for r in db.execute(f"SELECT * FROM graph_nodes WHERE kind='org' AND {live()}>=1 AND json_extract(info,'$.role') IS NULL AND coalesce(json_extract(info,'$.role_by'),'')!='owner' "
                                        f'ORDER BY {live()} DESC LIMIT 6')]
        return people, orgs

    def roles_start(self, again=False, auto=False):
        """One turn that says what the closest people are to the owner (also part of onboarding's profile)."""
        recent = (dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=30)).isoformat()
        with self.connect() as db:
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='roles' AND (status IN ('starting','running') OR "
                             "(status='ok' AND finished_at>? AND NOT ?)) ORDER BY started_at DESC LIMIT 1", (recent, int(bool(again)))).fetchone()
        if run:
            return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
        people, orgs = self.role_evidence()
        if not people and not orgs:
            return {'people': 0}
        run_id, started = uuid.uuid4().hex, now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='roles' AND (status IN ('starting','running') OR "
                             "(status='ok' AND finished_at>? AND NOT ?)) ORDER BY started_at DESC LIMIT 1", (recent, int(bool(again)))).fetchone()
            if run:
                return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'roles',?)",
                       (run_id, started, started, json.dumps({'people': people, 'organisations': orgs, 'corrections': graph.corrections(db)}), int(bool(auto))))
        return {'run_id': run_id, 'started_at': started, 'people': len(people), 'organisations': len(orgs)}

    def org_evidence(self, limit=ORGS_PEOPLE):
        """People with no organization yet whose sources may state one: their LinkedIn headline and their own latest
        messages (a signature, them saying where they work). Those with a headline first, then the closest."""
        people = []
        with self.connect() as db:
            owner = graph.Owner({'accounts': self.accounts}, db)
            owner.slack |= set(self.owner_user_ids)
            rows = db.execute("SELECT * FROM graph_nodes WHERE kind='person' AND json_extract(info,'$.org') IS NULL AND id NOT IN (SELECT identifier FROM person_orgs) "
                              f"AND (json_extract(info,'$.has_headline') OR ({live()}>=0.3 AND json_extract(info,'$.heard')>0)) "
                              f"ORDER BY NOT json_extract(info,'$.has_headline'),{live()} DESC LIMIT ?", (limit,)).fetchall()
            for r in rows:
                said = graph.headline(db, r['id']) if json.loads(r['info'] or '{}').get('has_headline') else None
                theirs = [m for m in graph.person_evidence(db, r['id'], owner) if m.get('from') not in (None, 'the owner')][-3:]
                if said or theirs:
                    people.append({'node_id': r['id'], 'name': r['name'], 'linkedin_headline': said, 'messages': theirs})
        return people

    def orgs_start(self, auto=False):
        """One turn that records where people work, from what their sources state (also the one-time backfill)."""
        with self.connect() as db:
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='orgs' AND status IN ('starting','running') ORDER BY started_at DESC LIMIT 1").fetchone()
        if run:
            return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
        people = self.org_evidence()
        if not people:
            return {'people': 0}
        run_id, started = uuid.uuid4().hex, now()
        with self.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'orgs',?)",
                       (run_id, started, started, json.dumps({'people': people}), int(bool(auto))))
        return {'run_id': run_id, 'started_at': started, 'people': len(people)}

    def save_profile(self, profile, session):
        """The draft from the running profile turn only; it waits for the owner to look at it."""
        run_id = str(session or '').removeprefix(PROFILE_SESSION_PREFIX)
        if not str(session or '').startswith(PROFILE_SESSION_PREFIX):
            raise ValueError('save_profile belongs to the profile turn that assistant profile starts')
        if not isinstance(profile, dict):
            raise ValueError('profile must be an object')
        with self.connect() as db:
            kind = db.execute('SELECT kind FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()
        if kind and kind['kind'] == 'voices':
            return self.save_voice_study(profile, run_id)
        if kind and kind['kind'] == 'share':
            return self.save_share_history(profile, run_id)
        if kind and kind['kind'] == 'learnings':
            with self.connect() as db:
                return team_learnings.save_draft(db, run_id, profile, {'accounts': self.accounts})
        if kind and kind['kind'] == 'tune':
            with self.connect() as db:
                return learning_loop.save_draft(db, run_id, profile)
        if kind and kind['kind'] == 'fleet_learn':
            with self.connect() as db:
                return fleet_learnings.save_draft(db, run_id, profile)
        if kind and kind['kind'] == 'team_votes':
            with self.connect() as db:
                return team_learnings.save_votes(db, run_id, profile, {'accounts': self.accounts})
        if kind and kind['kind'] == 'import':
            return self.save_import_check(profile, run_id)
        if kind and kind['kind'] != 'profile':
            raise ValueError('This roles run has no draft: set roles with graph node_id and role')
        counts = collections.Counter({('Email' if k == 'email' else k): v
                                      for k, v in self.profile_evidence(1, session)['counts'].items()})
        clean = {k: sentences(profile.get(k), 300) for k in PROFILE_TEXT if sentences(profile.get(k), 300)}
        for key, most in PROFILE_LISTS.items():
            values = profile.get(key) or []
            values = values if isinstance(values, list) else [values]
            items = []
            for v in values[:most]:
                v = sentences(': '.join(str(x) for x in v.values() if x) if isinstance(v, dict) else v, 200).rstrip(' .;')
                if v:
                    items.append(v)
            if items:
                clean[key] = items
        voices = profile.get('voices') or {}
        if isinstance(voices, list):  # [{"channel": "Email", "voice": "…"}] works too
            voices = {str(v.get('channel') or ''): v.get('voice') or v.get('text') for v in voices if isinstance(v, dict)}
        if isinstance(voices, dict):
            known = {k.lower(): k for k in counts | {'Email': 0}} | {'mail': 'Email', 'x': 'X DM'}
            voices = {known.get(' '.join(str(k).split()).lower(), clamp(' '.join(str(k).split()), 30)): sentences(v, 250).rstrip(';')
                      for k, v in list(voices.items())[:PROFILE_VOICES] if ' '.join(str(k).split()) and sentences(v, 250)}
            if voices:  # most used channel first
                clean['voices'] = dict(sorted(voices.items(), key=lambda v: (-counts[v[0]], v[0])))
        if not clean:
            raise ValueError('The profile is empty')
        # What it read, counted here rather than taken from the model.
        clean['based_on'] = ', '.join(f'{counts[k]} {"email" if k == "Email" else k}' for k in sorted(counts, key=lambda k: (-counts[k], k)))
        with self.connect() as db:
            if not db.execute("UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=? AND kind='profile' AND status IN ('starting','running')",
                              (json.dumps(clean), now(), run_id)).rowcount:
                raise ValueError('This profile run is no longer active')
        return {'saved': True, 'fields': sorted(clean)}

    def save_import_check(self, profile, run_id):
        """The model's mapping and fixes for a CSV import, kept where they fit the columns and cells it was given."""
        with self.connect() as db:
            run = db.execute("SELECT evidence FROM profile_runs WHERE run_id=? AND kind='import' AND status IN ('starting','running')", (run_id,)).fetchone()
            if not run:
                raise ValueError('This import check is no longer active')
            evidence = json.loads(run['evidence'])
            draft = crm_import.ai_draft(evidence['kind'], evidence['import'], profile)
            db.execute('UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=?', (json.dumps(draft), now(), run_id))
        return {'saved': True, 'columns': len(draft['mapping']), 'fixes': len(draft['fixes'])}

    def save_share_history(self, profile, run_id):
        """The history pass's calls (shared_graph.judge), only for threads this run was given."""
        team = profile.get('team')
        if not isinstance(team, list) or not team or not all(isinstance(t, dict) and str(t.get('event_id') or '').isdigit() for t in team):
            raise ValueError('args.profile.team is [{"event_id", "share", "line"}]')
        with self.connect() as db:
            run = db.execute("SELECT evidence FROM profile_runs WHERE run_id=? AND kind='share' AND status IN ('starting','running')", (run_id,)).fetchone()
            if not run:
                raise ValueError('This history pass is no longer active')
            given = {t['event_id'] for t in json.loads(run['evidence']).get('threads', [])}
            if not {int(t['event_id']) for t in team} <= given:
                raise ValueError('An event_id must be one of this pass\'s threads')
            shared_graph.ensure(db)
            kept = shared_graph.judge(db, team)
            draft = json.loads(db.execute('SELECT draft FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()[0] or '{}')
            db.execute('UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=?', (json.dumps({'judged': int(draft.get('judged') or 0) + kept}), now(), run_id))
        return {'saved': True, 'judged': kept}

    def save_voice_study(self, profile, run_id):
        voices = profile.get('voices')
        if isinstance(voices, list):
            voices = {str(v.get('channel') or ''): v.get('voice') or v.get('text') for v in voices if isinstance(v, dict)}
        if not isinstance(voices, dict) or not voices:
            raise ValueError('args.profile.voices is {"Email": "<block>", "Slack": "<block>", …}')
        clean, problems = {}, []
        for channel, text in list(voices.items())[:VOICE_MAX]:
            channel, text = voice_channel(channel), voice_block('\n'.join(text) if isinstance(text, list) else text)
            if not 2 <= len(channel) <= 30 or len(text) < 5:
                continue
            if len(text) > VOICE_CHARS or text.count('\n') >= VOICE_LINES:
                problems.append(f'{channel} is {len(text)} characters in {text.count(chr(10)) + 1} lines')
            clean[channel] = text
        if problems:
            raise ValueError(f'Each block is at most {VOICE_LINES} lines and {VOICE_CHARS} characters: ' + '; '.join(problems) + '. Make them shorter and save again.')
        if not clean:
            raise ValueError('No channel block to save')
        with self.connect() as db:
            if not db.execute("UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=? AND kind='voices' AND status IN ('starting','running')",
                              (json.dumps({'voices': clean}), now(), run_id)).rowcount:
                raise ValueError('This voice study is no longer active')
        return {'saved': True, 'channels': sorted(clean)}

    def profile_status(self, run_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM profile_runs WHERE run_id=?', (run_id,)).fetchone()
        if not row:
            raise ValueError('Unknown profile run')
        row = dict(row)
        row.pop('evidence', None)  # only paged profile_evidence returns the saved private sample
        if row['kind'] == 'orgs':
            with self.connect() as db:
                row['orgs'] = [dict(r) for r in db.execute("SELECT n.name,o.org,o.via FROM person_orgs o JOIN graph_nodes n ON n.id=o.identifier "
                                                           "WHERE o.source!='owner' AND o.created_at>=? ORDER BY n.strength DESC", (row['started_at'],))]
        if row['kind'] == 'roles':
            with self.connect() as db:  # roles read from the owner's messages since this run started
                row['roles'] = [dict(r) for r in db.execute("SELECT n.name,r.role FROM person_roles r JOIN graph_nodes n ON n.id=r.identifier "
                                                            "WHERE r.source!='owner' AND r.created_at>=? ORDER BY n.strength DESC", (row['started_at'],))]
        row['draft'] = json.loads(row['draft']) if row['draft'] else None
        return row

    def preference_summary(self, days=30, limit=3500):
        """What the owner did with recent suggestions, so reviews learn what's worth the owner's time."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        with self.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT id,title,status,snoozed_until,early FROM suggestions WHERE created_at>=? ORDER BY created_at DESC', (since,))]
            for r in rows:
                if r['early'] and r['status'] in ('accepted', 'prepared'):
                    r['status'] = 'ahead'
            notes = {}
            for d in db.execute("SELECT suggestion_id,feedback FROM decisions WHERE feedback!='' AND source IN ('telegram','dashboard') "
                                "AND id NOT IN (SELECT decision_id FROM decision_annotations) AND created_at>=? ORDER BY created_at", (since,)):
                notes.setdefault(d['suggestion_id'], []).append(d['feedback'][:200])
        groups = {'Dismissed': ['rejected'], 'Done': ['completed'], 'Accepted or prepared': ['accepted', 'prepared', 'instructions'],
                  'Snoozed (already in the owner\'s list)': ['snoozed'], 'Waiting for the owner\'s decision': ['pending'],
                  'Prepared ahead, waiting for the owner\'s approval': ['ahead']}
        lines = []
        for heading, statuses in groups.items():
            items = [r for r in rows if r['status'] in statuses]
            if items:
                lines.append(f'{heading}:')
                lines += ['- ' + r['title'] + ''.join(f' (owner wrote: "{n}")' for n in notes.get(r['id'], [])) for r in items]
        behaviour = self.behaviour_text(days)
        if behaviour:
            lines += ['', 'How the owner acted on cards:', behaviour]
        rates = self.quality_text(days)
        if rates:
            # First, so the length limit never cuts it.
            lines = [rates, ''] + lines
        text = '\n'.join(lines)
        return text if len(text) <= limit else text[:limit] + '\n…'

    def behaviour(self, days=30, accounts=None):
        """What the owner did, not only what they wrote: drafts they edited before sending, cards
        they snoozed again and again, and cards they dismissed within minutes without a note."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        with self.connect() as db:
            edits = {}
            scope = ' AND EXISTS(SELECT 1 FROM json_each(s.account_ids) WHERE value IN (' + ','.join('?' for _ in accounts) + '))' if accounts is not None else ''
            # A draft Claude Code or Codex rewrote (source 'agent') is not the owner's own edit: it teaches nothing.
            for r in db.execute("SELECT e.*,s.title FROM draft_edits e JOIN suggestions s ON s.id=e.suggestion_id WHERE e.created_at>=? AND e.source!='agent'" + scope + ' ORDER BY e.created_at', (since, *(sorted(accounts) if accounts is not None else []))):
                first = edits.setdefault(r['suggestion_id'], {'title': r['title'], 'before': r['before_body'], 'before_subject': r['before_subject'], 'at': r['created_at']})
                first.update(after=r['after_body'], after_subject=r['after_subject'], at=r['created_at'], kind=r['kind'], source=r['source'])
            edited_revisions = {r[0] for r in db.execute('SELECT new_revision FROM draft_edits')}
            # As is: no edit in the dashboard and no Change or Try again before the send.
            # A note that only said keep going or asked for something else didn't change the draft.
            # The drafting rules last changed: a saved draft rule, or an edit to PREPARATION.md.
            rules_at = db.execute("SELECT max(at) FROM rule_changes WHERE kind IN ('draft_rule','voice') OR (kind='file' AND text='PREPARATION.md edited')").fetchone()[0]
            sends = [(r['updated_at'], bool(r['revision'] in edited_revisions or r['changed'])) for r in db.execute(
                "SELECT j.revision,j.updated_at,EXISTS(SELECT 1 FROM decisions d LEFT JOIN note_kinds k ON k.decision_id=d.id WHERE d.suggestion_id=j.suggestion_id AND d.choice='other' "
                "AND coalesce(k.kind,'') NOT IN ('continue','new_ask') AND d.source IN ('telegram','dashboard') AND d.created_at<j.created_at) changed "
                "FROM action_jobs j WHERE j.status='sent' AND j.updated_at>=?", (since,))]
            sent = [changed for _, changed in sends]
            after = [changed for at, changed in sends if rules_at and at > rules_at]
            snoozed = db.execute("SELECT s.title,count(*) n FROM decisions d JOIN suggestions s ON s.id=d.suggestion_id WHERE d.choice='snooze' "
                                 "AND d.source IN ('telegram','dashboard') AND d.created_at>=? GROUP BY d.suggestion_id HAVING n>=2 ORDER BY n DESC", (since,)).fetchall()
            quick = [r[0] for r in db.execute("SELECT s.title FROM decisions d JOIN suggestions s ON s.id=d.suggestion_id WHERE d.choice='reject' AND d.feedback='' "
                                              "AND d.source IN ('telegram','dashboard') AND d.created_at>=? AND "
                                              "(julianday(d.created_at)-julianday(coalesce(s.deliver_after,s.created_at)))*1440 BETWEEN 0 AND 10", (since,))]
        return {'edits': sorted(edits.values(), key=lambda e: e['at'], reverse=True), 'sent_as_written': sent.count(False),
                'sent_edited': sent.count(True),
                # Only meaningful when some of these sends came before the latest rule change.
                'since_rules': {'at': rules_at, 'as_written': after.count(False), 'edited': after.count(True)} if rules_at and len(after) < len(sent) else None,
                'snoozed_again': [(r[0], r[1]) for r in snoozed], 'quick_dismissed': quick}

    def quality(self, days=30, until=None, since=None):
        """How good the cards were, so changes to the rules can be judged by results.

        Worth it: the owner tapped Do it or Send, or marked it done. Not needed: dismissed. Do it right
        first time: no Change and no Try again after the first Do it. Cards that closed themselves (a
        follow-up that arrived) don't count."""
        end = until or now()
        since = since or (dt.datetime.fromisoformat(end) - dt.timedelta(days=days)).isoformat()
        return self._quality_of(self._quality_rows(since, end), days, since, end)

    def _quality_rows(self, since, end):
        """The to-dos made from since until end, and the owner's decisions from since on (quality reads both): one read
        for every period inside, as quality_trend counts 22 of them."""
        with self.connect() as db:
            cards = [dict(r) for r in db.execute(
                "SELECT s.id,s.status,s.created_at,(SELECT e.kind FROM events e WHERE e.id=json_extract(s.event_ids,'$[0]')) kind FROM suggestions s "
                "WHERE s.created_at>=? AND s.created_at<? AND s.id NOT IN (SELECT suggestion_id FROM decisions WHERE id LIKE 'followed-up:%' OR id LIKE 'expired:%')", (since, end))]
            decisions = [dict(d) for d in db.execute(
                "SELECT d.suggestion_id,d.choice,k.kind,d.created_at FROM decisions d LEFT JOIN note_kinds k ON k.decision_id=d.id "
                "WHERE d.source IN ('telegram','dashboard') AND d.created_at>=? ORDER BY d.created_at", (since,))]
        return cards, decisions

    def _quality_of(self, rows, days, since, end):
        """quality() from _quality_rows read for this period or a longer one around it."""
        cards = [c for c in rows[0] if since <= c['created_at'] < end and c['kind'] != 'assistant.test']
        choices = collections.defaultdict(list)
        for d in rows[1]:
            if d['created_at'] >= since:
                # A Change counts as what it was: other:style, other:continue, … (other: when not sorted).
                choices[d['suggestion_id']].append(d['choice'] + (':' + (d['kind'] or '') if d['choice'] == 'other' else ''))
        def outcome(c):
            made = choices.get(c['id'], [])
            if c['status'] == 'rejected':
                return 'dismissed'
            if {'accept', 'send'} & set(made) or c['status'] == 'completed':
                return 'worth_it'
            return 'open'
        result = {'days': days, 'cards': len(cards), 'worth_it': 0, 'dismissed': 0, 'open': 0, 'do_it': 0, 'first_time': 0, 'finished': 0, 'by_source': {}}
        for c in cards:
            o = outcome(c)
            result[o] += 1
            source = result['by_source'].setdefault(todo_source(c['kind']), {'worth_it': 0, 'dismissed': 0, 'open': 0})
            source[o] += 1
            made = choices.get(c['id'], [])
            if 'accept' in made:
                result['do_it'] += 1
                after = set(made[made.index('accept') + 1:])
                # First try: no correction (style, a missing fact, or a Change not sorted yet).
                result['first_time'] += not ({'other:', 'other:style', 'other:fact'} & after)
                # Finished: no keep-going nudge and no Try again.
                result['finished'] += not ({'other:continue', 'retry'} & after)
        decided = result['worth_it'] + result['dismissed']
        result['hit_rate'] = round(100 * result['worth_it'] / decided) if decided else None
        result['first_time_rate'] = round(100 * result['first_time'] / result['do_it']) if result['do_it'] else None
        result['finished_rate'] = round(100 * result['finished'] / result['do_it']) if result['do_it'] else None
        return result

    def quality_report(self, days=30):
        """This period and the one before, for the dashboard and recap."""
        current = self.quality(days)
        before = self.quality(days, (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat())
        b = self.behaviour(days)
        return {**current, 'previous': {k: before[k] for k in ('hit_rate', 'first_time_rate', 'finished_rate', 'cards')},
                'sent_as_written': b['sent_as_written'], 'sent_edited': b['sent_edited'], 'trend': self.quality_trend(),
                'notes': self.note_kind_counts(days)}

    def quality_trend(self, days=14, weeks=8):
        """Hit rate per local day and per week (from Monday), oldest first, so progress shows.
        A card counts in the day it was made, with how it was decided since. `first` is the local day of the first
        decided to-do (None before any), so the chart starts there and never with empty weeks from before the Machine.
        Rule changes are not marked: drafting rules and PREPARATION.md change nearly every day, so a mark said nothing."""
        zone = local_tz()
        today = dt.datetime.fromisoformat(now()).astimezone(zone).date()
        utc = lambda d: dt.datetime.combine(d, dt.time(), zone).astimezone(dt.timezone.utc).isoformat()
        monday = today - dt.timedelta(days=today.weekday())
        # every period read at once: the earliest start (a day or a week back) to the latest end (tomorrow)
        rows = self._quality_rows(utc(min(today - dt.timedelta(days=days - 1), monday - dt.timedelta(weeks=weeks - 1))),
                                  utc(max(today + dt.timedelta(days=1), monday + dt.timedelta(weeks=1))))
        def bucket(start, end):
            q = self._quality_of(rows, 30, utc(start), utc(end))
            return {'start': start.isoformat(), **{k: q[k] for k in ('worth_it', 'dismissed', 'open', 'hit_rate', 'do_it', 'first_time_rate', 'finished_rate')}}
        with self.connect() as db:  # decided as quality() counts it: dismissed, done, or Do it or Send by the owner
            first = db.execute(
                "SELECT min(s.created_at) FROM suggestions s WHERE (s.status IN ('rejected','completed') OR EXISTS(SELECT 1 FROM decisions d "
                "WHERE d.suggestion_id=s.id AND d.choice IN ('accept','send') AND d.source IN ('telegram','dashboard'))) "
                "AND s.id NOT IN (SELECT suggestion_id FROM decisions WHERE id LIKE 'followed-up:%' OR id LIKE 'expired:%') "
                "AND coalesce((SELECT e.kind FROM events e WHERE e.id=json_extract(s.event_ids,'$[0]')),'')!='assistant.test'").fetchone()[0]
        return {'first': dt.datetime.fromisoformat(first).astimezone(zone).date().isoformat() if first else None,
                'daily': [bucket(today - dt.timedelta(days=i), today - dt.timedelta(days=i - 1)) for i in range(days - 1, -1, -1)],
                'weekly': [bucket(monday - dt.timedelta(weeks=i), monday - dt.timedelta(weeks=i - 1)) for i in range(weeks - 1, -1, -1)]}

    def quality_text(self, days=30):
        """Which sources' cards were worth it, for reviews. Only sources with enough decided cards."""
        q = self.quality(days)
        lines = [f"- {source}: {n['worth_it']} of {n['worth_it'] + n['dismissed']} worth it" for source, n in
                 sorted(q['by_source'].items(), key=lambda x: -(x[1]['worth_it'] + x[1]['dismissed'])) if n['worth_it'] + n['dismissed'] >= 3]
        if not lines:
            return ''
        return f"Cards in the last {days} days by source (worth it = Do it, Send or done; the rest dismissed):\n" + '\n'.join(lines)

    def behaviour_text(self, days=30):
        b = self.behaviour(days)
        lines = []
        if b['sent_as_written'] or b['sent_edited']:
            lines.append(f"Drafts: {b['sent_as_written']} sent as written, {b['sent_edited']} changed by the owner first (Change, Try again or an edit).")
        if b['snoozed_again']:
            lines += ['Snoozed two or more times (wrong moment, or less important than it looked):'] + [f'- {t} ({n}x)' for t, n in b['snoozed_again'][:8]]
        if b['quick_dismissed']:
            lines += ['Dismissed within minutes, without a note (not worth their time):'] + [f'- {t}' for t in b['quick_dismissed'][:10]]
        return '\n'.join(lines)

    def draft_edits_text(self, limit=4, chars=500, kinds=None, accounts=None):
        """Recent drafts the owner rewrote before sending (or answered themselves instead), for the next drafts:
        only those on the given channels (draft kinds) when given, since email edits say little about a chat."""
        clip = lambda v: v if len(v) <= chars else v[:chars] + '…'
        out = []
        for e in [e for e in self.behaviour(accounts=accounts)['edits'] if kinds is None or e['kind'] in kinds][:limit]:
            subject = f"\n  Subject: {e['before_subject']} → {e['after_subject']}" if e['before_subject'] != e['after_subject'] and e['after_subject'] else ''
            changed = 'They wrote this themselves instead' if e['source'] == 'elsewhere' else 'The owner changed it to'
            out.append(f"- {e['title']}{subject}\n  Your draft: {clip(e['before'])}\n  {changed}: {clip(e['after'])}")
        return '\n'.join(out)
