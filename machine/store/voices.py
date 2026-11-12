"""The Store's voices (refactor PR 17): how the owner writes, per channel. Saving and seeding a voice, the voice study
that reads a sample of the owner's own messages, tuning a voice from their edits and what they sent elsewhere, and the
notes to learn from. The helpers above the mixin pick the owner's own messages and their channel. A mixin of Store
(assistant.py), like App's mixins. Moved out of assistant.py as is."""
import collections
import contextlib
import datetime as dt
import difflib
import email.utils
import hashlib
import json
from pathlib import Path
import re
import uuid

import authorship
import learning_loop
from machine.config import LOG
from machine.prompts.profile import VOICE_CHARS, VOICE_LINES
from machine.sources.slack import slack_ids_named
from machine.store import outcomes
from machine.text import clamp, encoded
import i18n
import memory_use
import next_actions
import team_learnings
from timeutil import now


def similar(a, b, cutoff=0.5):
    """Two openings mostly made of the same words in the same order (an outreach template). Words, not
    characters: ordinary sentences share most letters, so character matching is slow and says little."""
    a, b = a.split(), b.split()
    return len(set(a) & set(b)) > cutoff * max(len(a), len(b)) and difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() > cutoff


def sentences(value, chars):
    """One line of at most chars, ending at a whole sentence (or word) instead of mid-word."""
    text = ' '.join(str(value or '').split())
    if len(text) <= chars:
        return text
    cut = text[:chars]
    end = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    return cut[:end + 1] if end > chars // 3 else cut[:cut.rfind(' ')].rstrip(',;:') + '…'


# Not writing: media placeholders, reactions and automated mail say nothing about how someone writes.
PROFILE_SKIP = re.compile(r'^(?:Sent (?:an? )?(?:image|photo|video|sticker|audio|voice message|document|GIF|file)\b|Reacted \S{1,8} to |'
                          r'\[(?:image|photo|video|sticker|audio|voice|document|gif|file)[^\]]*\]$|!\[)', re.I)


OWN_KINDS = {'gmail.message': 'email', 'slack.message': 'Slack', 'teams.message': 'Teams', 'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram', 'linkedin.message': 'LinkedIn', 'x.dm': 'X DM'}


# How the owner writes, per channel. A voice is a short block (a few lines); All holds what goes for every channel.
VOICE_CHANNELS = ('All', 'Email', 'Slack', 'WhatsApp', 'Telegram', 'LinkedIn', 'X DM')


VOICE_KEEP = 0.6          # a learned update keeps most of the block: it works one note in, it doesn't start over


# A voice study reads a sample of the owner's own messages per channel and writes each channel's block (their own edits stay).
VOICE_STUDY = {'gmail.message': 50}  # messages per channel; email gets more (several languages and kinds of people)


VOICE_STUDY_EACH = 25


VOICE_STUDY_SCAN = 12     # read this many times as many recent messages and pick evenly across them, so one busy day doesn't decide


VOICE_STUDY_PER = 3       # messages per conversation partner or chat, so one long thread doesn't decide either


VOICE_STUDY_MIN = 5       # fewer says too little about a channel


VOICE_STUDY_DAYS = 30     # read again this often, so the blocks follow how the owner writes now


VOICE_MAX = 10


VOICE_EXAMPLES = 6        # the owner's own recent messages a draft gets to match, same conversation first


DRAFT_EVENT_KINDS = {'email': 'gmail.message', 'slack': 'slack.message', 'whatsapp': 'whatsapp.message', 'telegram': 'telegram.message', 'linkedin': 'linkedin.message', 'x': 'x.dm'}


EVENT_CHANNELS = {kind: 'Email' if name == 'email' else name for kind, name in OWN_KINDS.items()}


ELSEWHERE_DAYS = 3        # the owner's own message in the draft's conversation this soon after it was ready replaced the draft
# What shows a to-do the owner answered themselves (answered_elsewhere): its Looks done line, per channel
ANSWERED_ELSEWHERE = {'gmail.message': 'Answered in the email thread', 'slack.message': 'Answered in Slack',
                      'whatsapp.message': 'Answered on WhatsApp', 'telegram.message': 'Answered on Telegram',
                      'linkedin.message': 'Answered on LinkedIn', 'x.dm': 'Answered on X'}
CONVERSATION_KEYS = {'gmail.message': ('thread_id',), 'slack.message': ('channel_id',)}  # conversation_of; the chats: chat_id or conversation_id
CONVERSATION_KEYS.update({kind: ('chat_id', 'conversation_id') for kind in ('whatsapp.message', 'telegram.message', 'linkedin.message', 'x.dm')})


NOTE_KINDS = ('style', 'fact', 'continue', 'new_ask')


# A routine's draft (routines_app.routine_voice_lines): how the owner writes on the channel it may go out on.
VOICE_HEAD = ('How the owner writes, per channel. A draft follows the block for the channel it goes out on, plus All; these come '
              "from the owner's own messages and notes. Follow each line as written, no broader:")


def voice_channel(name):
    """A channel's name as voices keep it: the known ones in their usual spelling, any other as written."""
    name = ' '.join(str(name or '').split())
    known = {c.lower(): c for c in VOICE_CHANNELS} | {'x': 'X DM', 'mail': 'Email', 'e-mail': 'Email'}
    return known.get(name.lower(), name[:30])


def voice_block(text):
    """A channel's voice as kept: up to VOICE_LINES short lines (a list's dashes or bullets dropped), spaces tidied."""
    lines = [' '.join(re.sub(r'^\s*(?:[-*•–]|\d+[.)])\s+', '', line).split()) for line in str(text or '').replace('\r', '').split('\n')]
    return '\n'.join(line for line in lines if line)


def voice_lines(text, indent='  '):
    """A voice block as lines under its channel in a prompt."""
    return ''.join(f'\n{indent}- {line}' for line in voice_block(text).split('\n') if line)


def conversation_of(kind, m):
    """The conversation a message belongs to: an email thread, a Slack channel or DM, a chat."""
    key = m.get('thread_id') if kind == 'gmail.message' else m.get('channel_id') if kind == 'slack.message' else m.get('chat_id') or m.get('conversation_id')
    return str(key) if key else None


def own_predicate(kind, owner_slack_ids=()):
    """SQL for "the owner wrote this" on one kind of message, with its parameters (same rule as own_message)."""
    if kind == 'gmail.message':
        return "EXISTS(SELECT 1 FROM json_each(json_extract(events.metadata,'$.labels')) WHERE value='SENT')", []
    if kind == 'slack.message':
        return f"json_extract(metadata,'$.user_id') IN ({','.join('?' for _ in owner_slack_ids)})", list(owner_slack_ids)
    return "json_extract(metadata,'$.from_me')=1", []


def own_text(body):
    """What the owner wrote in a message, without the quoted history below it."""
    return (body or '').split('[Quoted earlier messages', 1)[0].strip()


def tune_voice(channel, text, current):
    """A learning pass's voice block, checked like a learned update: short, and keeping most of the current one."""
    channel, text = voice_channel(channel), voice_block(text)
    if not 2 <= len(channel) <= 30 or not 5 <= len(text) <= VOICE_CHARS or text.count('\n') >= VOICE_LINES:
        raise ValueError('not a voice block')
    if current and len(text) < VOICE_KEEP * len(current['text']):
        raise ValueError('a learned update keeps most of the block')
    return channel, text


def card_channels(db, suggestion_id):
    """The channels a card's draft goes out on: its ready drafts first, then the messages it is about."""
    row = db.execute('SELECT event_ids,next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        return [], []
    drafts = [a for a in next_actions.actions(row['next_action']) if a.get('kind') in DRAFT_EVENT_KINDS] if row['next_action'] else []
    events = [dict(e) for e in db.execute('SELECT e.id,e.account_id,e.kind,e.metadata FROM json_each(?) i JOIN events e ON e.id=i.value '
                                          'WHERE e.deleted=0', (row['event_ids'],))]
    kinds = [DRAFT_EVENT_KINDS[a['kind']] for a in drafts] + [e['kind'] for e in events if e['kind'] in EVENT_CHANNELS]
    return list(dict.fromkeys(kinds)), events + [{'kind': DRAFT_EVENT_KINDS[a['kind']], 'account_id': a.get('account_id'),
                                                 'metadata': {k: a[k] for k in ('thread_id', 'chat_id', 'conversation_id', 'channel_id') if a.get(k)}}
                                                for a in drafts]


def tag_note(db, suggestion_id, kind, source='assistant'):
    """Record what the Change note behind this preparation was. Returns False when there's no untagged note."""
    job = db.execute("SELECT p.decision_id,d.choice FROM preparations p JOIN decisions d ON d.id=p.decision_id WHERE p.suggestion_id=?", (suggestion_id,)).fetchone()
    if not job or job['choice'] != 'other' or db.execute('SELECT 1 FROM note_kinds WHERE decision_id=?', (job['decision_id'],)).fetchone():
        return False
    if kind not in NOTE_KINDS:
        raise ValueError("Say what the owner's Change note was: note_kind " + ', '.join(NOTE_KINDS) +
                         ' (style: how it was written; fact: something you didn\'t know; continue: keep going or finish the job; new_ask: something else to do)')
    db.execute('INSERT INTO note_kinds VALUES(?,?,?,?,?)', (job['decision_id'], suggestion_id, kind, source, now()))
    return True


def rule_changes(db, since):
    return [dict(r) for r in db.execute('SELECT at,kind,text FROM rule_changes WHERE at>=? ORDER BY at', (since,))]


def note_rule_files(db, paths):
    """Log an edit to the rule files (AGENTS.md, PREPARATION.md) once, by content hash."""
    for path in paths:
        try:
            digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
        except OSError:
            continue
        name = Path(path).name
        last = db.execute("SELECT ref FROM rule_changes WHERE kind='file' AND text LIKE ? ORDER BY id DESC LIMIT 1", (name + ' %',)).fetchone()
        if not last or last['ref'] != digest:
            db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'file',?,?)", (now(), name + (' edited' if last else ' tracked'), digest))


class VoicesStore:
    """Store methods for how the owner writes, per channel."""

    def style_notes_to_learn(self, run_id=None, days=30, limit=6, chars=300):
        """The owner's style notes (how a draft should have been written) that no fact, rule or voice came from yet, each offered once."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        with self.connect() as db:
            rows = db.execute("SELECT d.id,d.feedback,s.title FROM note_kinds k JOIN decisions d ON d.id=k.decision_id JOIN suggestions s ON s.id=d.suggestion_id "
                              "WHERE k.kind='style' AND d.feedback!='' AND d.created_at>=? AND d.id NOT IN (SELECT decision_id FROM facts) "
                              "AND d.id NOT IN (SELECT decision_id FROM decision_annotations) "
                              "AND 'decision:'||d.id NOT IN (SELECT ref FROM rule_changes WHERE kind='voice' AND ref IS NOT NULL) "
                              "AND 'note:'||d.id NOT IN (SELECT edit_id FROM edits_offered) ORDER BY d.created_at DESC LIMIT ?", (since, limit)).fetchall()
            if run_id:
                db.executemany('INSERT OR IGNORE INTO edits_offered(edit_id,run_id,offered_at) VALUES(?,?,?)', [('note:' + str(r['id']), run_id, now()) for r in rows])
            return '\n'.join(f"- \"{r['title']}\". They wrote: \"{slack_ids_named(db, r['feedback'])[:chars]}\" (decision_id {r['id']})" for r in rows)

    # How the owner writes, per channel: a short block each, learned from their own messages, style notes and edits.
    def voices(self, db=None):
        with contextlib.nullcontext(db) if db else self.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT channel,text,source,updated_at FROM voices')]
        order = {c: i for i, c in enumerate(VOICE_CHANNELS)}
        return sorted(rows, key=lambda v: (order.get(v['channel'], len(order)), v['channel'].lower()))

    def save_voice(self, channel, text, source, decision_id=None, edit_id=None, replaces=None):
        """Set one channel's voice block. The assistant rewrites the whole block from one of the owner's own notes or
        edits (never from a message someone else wrote); the owner edits it in Settings, and an empty block removes it."""
        channel = voice_channel(channel)
        text = voice_block(text)
        if not 2 <= len(channel) <= 30:
            raise ValueError('channel is where the owner writes this way: ' + ', '.join(VOICE_CHANNELS) + ', or another channel\'s name')
        if len(text) > VOICE_CHARS or text.count('\n') >= VOICE_LINES or (text and len(text) < 5) or (not text and source != 'owner'):
            raise ValueError(f'A voice is a short block (up to {VOICE_LINES} lines, 5-{VOICE_CHARS} characters): the whole block for that channel')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            ref = None
            originals = self.replaced_facts(db, replaces) if source != 'owner' else []
            if originals and not (decision_id or edit_id):  # condensing style facts into this voice
                decision_id = originals[-1]['decision_id']
            if source != 'owner':
                if decision_id:
                    if not db.execute("SELECT 1 FROM decisions WHERE id=? AND source IN ('telegram','dashboard') AND feedback!='' "
                                      "AND id NOT IN (SELECT decision_id FROM decision_annotations)", (decision_id,)).fetchone():
                        raise ValueError('A voice is learned from one of the owner’s own written notes (decision_id) or their edit of a draft (edit_id)')
                    ref = 'decision:' + str(decision_id)
                elif edit_id and db.execute('SELECT 1 FROM draft_edits WHERE id=?', (edit_id,)).fetchone():
                    ref = 'edit:' + str(edit_id)
                else:
                    raise ValueError('A voice is learned from one of the owner’s own written notes (decision_id) or their edit of a draft (edit_id)')
            current = db.execute('SELECT * FROM voices WHERE channel=?', (channel,)).fetchone()
            if source == 'assistant' and current and len(text) < VOICE_KEEP * len(current['text']):
                raise ValueError(f'Keep the whole {channel} block: rewrite it with the note worked in and only what it contradicts dropped. '
                                 f'The current block is:\n{current["text"]}')
            if not text:
                if current:
                    db.execute('DELETE FROM voices WHERE channel=?', (channel,))
                    db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'voice',?,?)", (now(), f'Removed {channel} voice', None))
                return {'channel': channel, 'removed': bool(current)}
            if originals:
                # A later owner edit starts a new undo baseline; consecutive learned merges share the first one.
                prior = db.execute('SELECT merged_text,merged_ref FROM voice_merges WHERE channel=?', (channel,)).fetchone()
                if prior and (not current or current['text'] != prior['merged_text'] or current['ref'] != prior['merged_ref']):
                    db.execute('DELETE FROM voice_merges WHERE channel=?', (channel,))
                db.execute('INSERT INTO voice_merges(channel,previous,merged_text,merged_ref) VALUES(?,?,?,?) '
                           'ON CONFLICT(channel) DO UPDATE SET merged_text=excluded.merged_text,merged_ref=excluded.merged_ref',
                           (channel, json.dumps(dict(current)) if current else None, text, ref))
                self.merge_originals(db, originals, 'voice:' + channel, f'{channel} voice')
            if current and current['text'] == text and (not originals or current['ref'] == ref):
                return {'channel': channel, 'text': text, 'unchanged': True, **({'merged': len(originals)} if originals else {})}
            if not current and db.execute('SELECT count(*) FROM voices').fetchone()[0] >= VOICE_MAX:
                raise ValueError(f'At most {VOICE_MAX} voices: work this into an existing channel or All')
            db.execute('INSERT INTO voices(channel,text,source,ref,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(channel) DO UPDATE SET '
                       'text=excluded.text,source=excluded.source,ref=excluded.ref,updated_at=excluded.updated_at', (channel, text, source, ref, now()))
            db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'voice',?,?)", (now(), f'{channel} voice: {text}', ref))
        return {'channel': channel, 'text': text, **({'merged': len(originals)} if originals else {})}

    def seed_voices(self):
        """A profile run read the owner's own messages and described each channel: those lines become the voices of
        channels that have none yet, once per run (a voice the owner removed stays removed until a new profile)."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT run_id,draft FROM profile_runs WHERE kind='profile' AND status='ok' AND draft LIKE '%\"voices\"%' "
                             'ORDER BY started_at DESC LIMIT 1').fetchone()
            if not run or db.execute("SELECT 1 FROM rule_changes WHERE kind='voice' AND ref=?", ('profile:' + run['run_id'],)).fetchone():
                return 0
            try:
                voices = json.loads(run['draft']).get('voices') or {}
            except (ValueError, AttributeError):
                voices = {}
            added = 0
            for channel, text in list(voices.items())[:VOICE_MAX] if isinstance(voices, dict) else ():
                channel, text = voice_channel(channel), voice_block(sentences(text, VOICE_CHARS))
                if 2 <= len(channel) <= 30 and len(text) >= 5 and db.execute('SELECT count(*) FROM voices').fetchone()[0] < VOICE_MAX:
                    added += db.execute("INSERT OR IGNORE INTO voices(channel,text,source,ref,updated_at) VALUES(?,?,'profile',?,?)",
                                        (channel, text, 'profile:' + run['run_id'], now())).rowcount
            db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'voice',?,?)",
                       (now(), f'Voices from your own messages: {added} channel' + ('' if added == 1 else 's'), 'profile:' + run['run_id']))
        return added

    def voice_sample(self):
        """For a voice study: the owner's own recent messages per channel (email gets more: several languages and kinds of
        people), spread over time and over the people they wrote to, outreach templates and media left out, each with who
        it went to and what they are to the owner when known."""
        ids, items = sorted(self.owner_user_ids), []
        own = {str(a.get('email', '')).lower() for a in self.accounts}
        with self.connect() as db:
            db.execute('BEGIN')
            sent = authorship.MachineSent.load(db)  # only what the owner wrote themselves (authorship.py)
            for kind, channel in EVENT_CHANNELS.items():
                limit, picked, copies, per = VOICE_STUDY.get(kind, VOICE_STUDY_EACH), [], [], collections.Counter()
                predicate, params = own_predicate(kind, ids)
                for row in db.execute(f'SELECT id,source_id,occurred_at,title,body,metadata FROM events WHERE deleted=0 AND kind=? AND ({predicate}) '
                                      'ORDER BY occurred_at DESC,id DESC LIMIT ?', (kind, *params, limit * VOICE_STUDY_SCAN)):
                    text = own_text(row['body'])
                    if len(text.split()) < 2 or PROFILE_SKIP.match(text) or sent.wrote(row, text):
                        continue
                    gist = ' '.join(re.sub(r'^\W*(?:hey|hi|hello|dear|hoi|dag)\b[^,\n!]{0,40}[,\n!]', '', text[:400], flags=re.I).split()).lower()[:120]
                    if sum(gist == other or (len(gist) > 60 and len(other) > 60 and similar(gist, other)) for other in copies) >= 1:
                        continue  # one copy of a template says all it can
                    m = json.loads(row['metadata'] or '{}')
                    partner = (','.join(sorted(a.lower() for _, a in email.utils.getaddresses([str(m.get('to') or '')]) if a)) if kind == 'gmail.message'
                               else conversation_of(kind, m)) or ''
                    if per[partner] >= VOICE_STUDY_PER:
                        continue
                    per[partner] += 1
                    copies.append(gist)
                    roles = [r[0] for r in db.execute("SELECT DISTINCT json_extract(n.info,'$.role') FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id "
                                                      "WHERE g.event_id=? AND g.direct=1 AND n.kind='person' AND json_extract(n.info,'$.role') IS NOT NULL LIMIT 3",
                                                      (row['id'],))]
                    item = {'channel': channel, 'date': row['occurred_at'][:10],
                            'text': clamp(slack_ids_named(db, text) if kind == 'slack.message' else text, 700 if kind == 'gmail.message' else 250)}
                    if kind == 'gmail.message':
                        to = [(n, a) for n, a in email.utils.getaddresses([str(m.get(f) or '') for f in ('to', 'cc')]) if a and a.lower() not in own]
                        item['to'] = clamp(', '.join(n or a.split('@')[0] for n, a in to[:3]), 120)
                        item['same_domain'] = bool(to) and all(a.lower().rsplit('@', 1)[-1] in {o.rsplit('@', 1)[-1] for o in own} for _, a in to)
                    elif m.get('chat_name') or m.get('channel_name'):
                        item['chat'] = clamp(slack_ids_named(db, str(m.get('chat_name') or m.get('channel_name'))), 60)  # "DM Sam Lee", never the id
                    if roles:
                        item['they_are'] = ', '.join(clamp(str(r), 60) for r in roles)
                    picked.append(item)
                if len(picked) > limit:  # evenly across the period read, newest first
                    picked = [picked[i * len(picked) // limit] for i in range(limit)]
                if len(picked) >= VOICE_STUDY_MIN:
                    items += picked
            notes = [{'decision_id': r['id'], 'date': r['created_at'][:10], 'note': clamp(slack_ids_named(db, r['feedback']), 300), 'card': clamp(r['title'], 100)}
                     for r in db.execute("SELECT d.id,d.feedback,d.created_at,s.title FROM note_kinds k JOIN decisions d ON d.id=k.decision_id "
                                         "JOIN suggestions s ON s.id=d.suggestion_id WHERE k.kind='style' AND d.feedback!='' "
                                         "AND d.source IN ('telegram','dashboard') AND d.id NOT IN (SELECT decision_id FROM decision_annotations) "
                                         "ORDER BY d.created_at DESC LIMIT 40")]
            voices = [{'channel': v['channel'], 'text': v['text'], 'written_by_owner': v['source'] == 'owner'} for v in self.voices(db)]
        return {'messages': items, 'notes': notes, 'voices': voices}

    def voice_study_start(self, again=False, auto=False):
        """One turn that reads a sample of the owner's own messages per channel and writes each channel's voice block
        (greetings and sign-offs per language, length and structure, tone per kind of person, habits), with their style
        notes worked in. Blocks the owner wrote themselves stay as they are."""
        with self.connect() as db:
            run = db.execute("SELECT run_id,started_at FROM profile_runs WHERE kind='voices' AND (status IN ('starting','running') OR "
                             "(status='ok' AND finished_at>? AND NOT ?)) ORDER BY started_at DESC LIMIT 1",
                             ((dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=30)).isoformat(), int(bool(again)))).fetchone()
        if run:
            return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}
        evidence = self.voice_sample()
        if not evidence['messages']:
            return {'messages': 0}
        run_id, started = uuid.uuid4().hex, now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT 1 FROM profile_runs WHERE kind='voices' AND status IN ('starting','running')").fetchone():
                return {'attached': True}
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'voices',?)",
                       (run_id, started, started, json.dumps(evidence), int(bool(auto))))
        return {'run_id': run_id, 'started_at': started, 'counts': dict(collections.Counter(m['channel'] for m in evidence['messages']))}

    def voice_study_due(self):
        """A voice study when there never was one, and again every VOICE_STUDY_DAYS (a failed one after a day)."""
        stamp = dt.datetime.fromisoformat(now())
        with self.connect() as db:
            last = db.execute("SELECT status,finished_at,started_at FROM profile_runs WHERE kind='voices' ORDER BY started_at DESC LIMIT 1").fetchone()
        if last and (last['status'] in ('starting', 'running') or (last['finished_at'] or last['started_at']) >
                     (stamp - dt.timedelta(days=VOICE_STUDY_DAYS if last['status'] == 'ok' else 1)).isoformat()):
            return None
        return self.voice_study_start(auto=True)

    def learnings_due(self, current=None):
        """At most once a day, with new material, when the owner wants to be offered: one cheap turn distils what was
        learned since the last one into a few general learnings for The Machine team (team_learnings.py). Nothing is
        sent here: it goes by itself with Send automatically on (team_learnings.auto_send, the default), else the owner is
        asked first; learnings from Personal to-dos always ask."""
        current = current or dt.datetime.fromisoformat(now())
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone() or not team_learnings.due(db, current):
                return None
            evidence = team_learnings.evidence(db, lambda: self.quality(team_learnings.SINCE_DAYS), current, getattr(self, 'accounts', None))
            run_id, started = uuid.uuid4().hex, now()
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'learnings',1)",
                       (run_id, started, started, json.dumps(evidence)))
        return run_id

    def tune_due(self, current=None):
        """About twice a day, with a few signals waiting (edits, dismissals, snoozes, chat corrections): one small turn
        reads the next batch and brings voices, rules and facts up to date (learning_loop.py). It waits for the usage
        budget like every background turn. Each signal stays pending until a pass's changes are applied."""
        current = current or dt.datetime.fromisoformat(now())
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for finished in learning_loop.unapplied(db):  # stopped between a pass's end and applying it
                LOG.info('learning pass recovered changes=%s', learning_loop.apply(db, finished, self.tune_voice, self.link_named))
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone():
                return None
            skipped = learning_loop.settle(db)  # a failed pass's signals wait for a retry, given up after MAX_TRIES
            if skipped:
                LOG.warning('learning pass gave up signals=%s', skipped)
            if not learning_loop.due(db, current):
                return None
            evidence = learning_loop.evidence(db, self.voices(db), current)
            run_id, started = uuid.uuid4().hex, now()
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'tune',1)",
                       (run_id, started, started, json.dumps(evidence)))
            learning_loop.claim(db, run_id, evidence['keys'])
        return run_id

    def tune_voice(self, channel, text, current):
        return tune_voice(channel, text, current)

    def apply_tune(self, run_id):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            return learning_loop.apply(db, run_id, self.tune_voice, self.link_named)

    def undo_learning(self, change_id):
        try:
            change_id = int(change_id)
        except (TypeError, ValueError):
            raise ValueError('id is the change to undo') from None
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            return learning_loop.undo(db, change_id, self.unlink_named)

    def apply_voice_study(self, run_id):
        """A finished study's blocks become the voices, except blocks the owner wrote themselves."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT draft FROM profile_runs WHERE run_id=? AND kind='voices' AND status='ok'", (run_id,)).fetchone()
            ref = 'study:' + run_id
            if not row or not row['draft'] or db.execute("SELECT 1 FROM rule_changes WHERE kind='voice' AND ref=?", (ref,)).fetchone():
                return 0
            written = 0
            for channel, text in (json.loads(row['draft']).get('voices') or {}).items():
                current = db.execute('SELECT source FROM voices WHERE channel=?', (channel,)).fetchone()
                if (current and current['source'] == 'owner') or (not current and db.execute('SELECT count(*) FROM voices').fetchone()[0] >= VOICE_MAX):
                    continue
                db.execute("INSERT INTO voices(channel,text,source,ref,updated_at) VALUES(?,?,'study',?,?) ON CONFLICT(channel) DO UPDATE SET "
                           'text=excluded.text,source=excluded.source,ref=excluded.ref,updated_at=excluded.updated_at', (channel, text, ref, now()))
                written += 1
            db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'voice',?,?)",
                       (now(), f'How you write, read again from your own messages: {written} channel' + ('' if written == 1 else 's'), ref))
        return written


    def card_channels(self, suggestion_id, db):
        return card_channels(db, suggestion_id)

    def own_examples(self, suggestion_id, limit=VOICE_EXAMPLES, scan=200):
        """The owner's own recent messages on the card's channel: in the same conversation first, then to the same
        people, then on the same account. Real examples of how they write there, for the draft to match."""
        ids = sorted(self.owner_user_ids)
        with self.connect() as db:
            db.execute('BEGIN')
            kinds, events = self.card_channels(suggestion_id, db)
            if not kinds:
                return []
            kind = kinds[0]
            mine = [e for e in events if e['kind'] == kind]
            meta = lambda e: e['metadata'] if isinstance(e['metadata'], dict) else json.loads(e['metadata'] or '{}')
            conversations = {c for c in (conversation_of(kind, meta(e)) for e in mine) if c}
            people = {a.lower() for e in mine for _, a in email.utils.getaddresses([str(meta(e).get(f) or '') for f in ('from', 'to', 'cc')]) if a}
            people -= {str(a.get('email', '')).lower() for a in self.accounts}
            accounts = {e.get('account_id') for e in mine}
            if not accounts:
                return []
            predicate, params = own_predicate(kind, ids)
            rows = db.execute(f'SELECT id,account_id,source_id,occurred_at,title,body,metadata FROM events WHERE deleted=0 AND kind=? AND ({predicate}) '
                              f'AND account_id IN ({",".join("?" for _ in accounts)}) '
                              'ORDER BY occurred_at DESC,id DESC LIMIT ?', (kind, *params, *sorted(accounts), scan)).fetchall()
            sent = authorship.MachineSent.load(db)
        picked = []
        for row in rows:
            text = own_text(row['body'])
            if len(text.split()) < 2 or PROFILE_SKIP.match(text) or sent.wrote(row, text):
                continue
            m = json.loads(row['metadata'] or '{}')
            to = {a.lower() for _, a in email.utils.getaddresses([str(m.get(f) or '') for f in ('to', 'cc')]) if a}
            rank = 0 if conversation_of(kind, m) in conversations else 1 if to & people else 2 if row['account_id'] in accounts else 3
            names = [n or a.split('@')[0] for n, a in email.utils.getaddresses([str(m.get('to') or '')]) if a][:2]
            picked.append((rank, len(picked), {'channel': EVENT_CHANNELS[kind], 'where': ('this conversation' if rank == 0 else
                           'to ' + ', '.join(names) if names else str(m.get('chat_name') or m.get('channel_name') or '')[:60]),
                           'text': clamp(text, 500 if kind == 'gmail.message' else 300)}))
        picked.sort(key=lambda p: (p[0], p[1]))
        return [p[2] for p in picked[:limit]]

    def style_text(self, suggestion_id, chars=4000):
        """What a draft for this card gets about how the owner writes: every channel's voice (this card's marked),
        the owner's own recent messages there, and how they changed earlier drafts on that channel."""
        with self.connect() as db:
            kinds, events = self.card_channels(suggestion_id, db)
            voices = self.voices(db)
        here = [EVENT_CHANNELS[k] for k in kinds]
        parts = []
        if voices:
            parts.append('How the owner writes, per channel. A draft follows the block for the channel it goes out on, plus All; these '
                         'come from the owner\'s own messages and notes and win over general tone notes elsewhere. Follow each line as written, '
                         'no broader: a habit about how sentences start leaves names, places, brands and I capitalized unless the line '
                         'says those are lowercase too, and one channel\'s habits stay on that channel:\n' +
                         '\n'.join(f"- {v['channel']}{' (this card)' if v['channel'] in here else ''}:{voice_lines(v['text'])}" for v in voices))
        examples = self.own_examples(suggestion_id)
        if examples:
            parts.append(f"The owner's own recent {examples[0]['channel']} messages, newest first. Match how these read (length, greeting, sign-off, "
                         'language, capitals, punctuation, emoji, formality), not what they say:\n' +
                         '\n'.join(f"- ({e['where']}) {e['text']}" if e['where'] else f"- {e['text']}" for e in examples))
        edits = self.draft_edits_text(kinds=[k for k, v in DRAFT_EVENT_KINDS.items() if v in kinds], accounts={e['account_id'] for e in events})
        if edits:
            parts.append(f"Earlier {here[0] + ' ' if here else ''}drafts the owner changed before sending, or answered themselves instead. Write the next drafts "
                         'the way they ended up writing these (length, tone, what they cut or added):\n' + edits)
        text = '\n\n'.join(parts)
        return text if len(text) <= chars else text[:chars] + '\n…'

    def learn_sent_elsewhere(self, days=ELSEWHERE_DAYS):
        """A ready draft the owner didn't send from the card, because they wrote their own reply in that conversation
        (in Gmail, WhatsApp, Telegram, Slack…): what they wrote instead teaches the next drafts like an edit does."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        ids, learned = sorted(self.owner_user_ids), 0
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT s.id,s.next_action,p.updated_at ready FROM suggestions s JOIN preparations p ON p.suggestion_id=s.id "
                              "WHERE p.updated_at>=? AND s.next_action IS NOT NULL AND s.status IN ('prepared','completed') "
                              "AND NOT EXISTS(SELECT 1 FROM action_jobs j WHERE j.suggestion_id=s.id AND j.status NOT IN ('cancelled','blocked')) "
                              "AND NOT EXISTS(SELECT 1 FROM draft_edits d WHERE d.suggestion_id=s.id AND d.source='elsewhere')", (since,)).fetchall()
            sent = authorship.MachineSent.load(db) if rows else None  # another to-do's send in that conversation isn't theirs
            for row in rows:
                draft = next((a for a in next_actions.actions(row['next_action']) if a.get('kind') in DRAFT_EVENT_KINDS), None)
                if not draft or not (next_actions.draft_text(draft) or '').strip():
                    continue
                kind = DRAFT_EVENT_KINDS[draft['kind']]
                _, events = self.card_channels(row['id'], db)
                conversations = {(e.get('account_id'), c) for e in events if e['kind'] == kind
                                 if (c := conversation_of(kind, e['metadata'] if isinstance(e['metadata'], dict) else json.loads(e['metadata'] or '{}')))}
                if not conversations:
                    continue
                until = (dt.datetime.fromisoformat(row['ready']) + dt.timedelta(days=days)).isoformat()
                predicate, params = own_predicate(kind, ids)
                found = next((e for e in db.execute(f'SELECT id,account_id,source_id,title,body,metadata FROM events WHERE deleted=0 AND kind=? AND ({predicate}) '
                                                    'AND occurred_at>? AND occurred_at<=? ORDER BY occurred_at,id LIMIT 50', (kind, *params, row['ready'], until))
                              if (e['account_id'], conversation_of(kind, json.loads(e['metadata'] or '{}'))) in conversations
                              and not sent.wrote(e, own_text(e['body']))), None)
                if not found:
                    continue
                text, before = own_text(found['body']), next_actions.draft_text(draft).strip()
                if len(text.split()) < 2 or PROFILE_SKIP.match(text) or ' '.join(text.split()) == ' '.join(before.split()):
                    continue
                db.execute('INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_subject,before_body,after_subject,after_body,source,created_at) '
                           "VALUES(?,?,?,?,?,?,?,?,?,'elsewhere',?)", (uuid.uuid4().hex, row['id'], draft.get('revision') or '', f"elsewhere:{found['id']}", draft['kind'],
                                                                       draft.get('subject'), before, found['title'] if kind == 'gmail.message' else None, text, now()))
                learned += 1
        return learned

    def answered_elsewhere(self):
        """An open to-do with a reply draft the owner answered themselves in that conversation (from Gmail, Slack,
        WhatsApp..., not from the card) is done: their reply was its step. It closes by itself (Done, "Closed by itself:
        Answered in the email thread", with Undo for a day), once for that message, and Done shows that line under its
        title. One with a done when (outcomes.py) isn't done by their reply, as by a send from the card
        (settle_sent): it waits for that result under Waiting on others, and a review reading the answer closes it.
        Their message counts when it came after what the to-do is about and after the to-do was made (or reached the
        Machine after that, so the review that made it never saw it). The Machine's own sends, reactions and media
        don't count, and a Not done, Undo or Reopen after that message stands. Returns the ids closed or set waiting."""
        ids, marked = sorted(self.owner_user_ids), []
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT s.* FROM suggestions s WHERE s.status IN ('pending','prepared') "
                              'AND s.handled_hint IS NULL AND s.next_action IS NOT NULL '
                              "AND NOT EXISTS(SELECT 1 FROM action_jobs j WHERE j.suggestion_id=s.id AND j.status NOT IN ('cancelled','blocked'))").fetchall()
            sent = None
            for row in rows:
                draft = next((a for a in next_actions.actions(row['next_action']) if a.get('kind') in DRAFT_EVENT_KINDS
                              and (next_actions.draft_text(a) or '').strip()), None)
                if not draft:
                    continue
                kind = DRAFT_EVENT_KINDS[draft['kind']]
                _, events = self.card_channels(row['id'], db)
                conversations = {(e.get('account_id'), c) for e in events if e['kind'] == kind
                                 if (c := conversation_of(kind, e['metadata'] if isinstance(e['metadata'], dict) else json.loads(e['metadata'] or '{}')))}
                if not conversations:
                    continue
                # Slack: a channel holds many matters, so only the to-do's own thread counts there (a DM is one conversation)
                threads = {str(m['thread_ts']) for e in events if e['kind'] == 'slack.message'
                           if (m := e['metadata'] if isinstance(e['metadata'], dict) else json.loads(e['metadata'] or '{}')).get('thread_ts')}
                threads |= {str(draft['thread_ts'])} if draft.get('thread_ts') else set()
                newest = db.execute('SELECT max(e.occurred_at) FROM json_each(?) i JOIN events e ON e.id=i.value', (row['event_ids'],)).fetchone()[0]
                sent = sent or authorship.MachineSent.load(db)  # another to-do's send in that conversation isn't theirs
                predicate, params = own_predicate(kind, ids)
                # Only in its conversations (the keys are kept in the clear), and after a Not done only what came in since
                where = ' OR '.join(f"json_extract(metadata,'$.{key}') IN ({','.join('?' * len(conversations))})" for key in CONVERSATION_KEYS[kind])
                keys = [c for _, c in conversations] * len(CONVERSATION_KEYS[kind])
                said = db.execute("SELECT max(created_at) FROM decisions WHERE suggestion_id=? AND choice IN ('not_done','undo','reopen')",
                                  (row['id'],)).fetchone()[0]
                found = next((e for e in db.execute(f'SELECT id,account_id,source_id,body,metadata FROM events WHERE deleted=0 AND kind=? AND ({predicate}) AND ({where}) '
                                                    'AND occurred_at>? AND (occurred_at>? OR ingested_at>?) AND ingested_at>? ORDER BY occurred_at,id LIMIT 50',
                                                    (kind, *params, *keys, newest or row['created_at'], row['created_at'], row['created_at'], said or ''))
                              if (e['account_id'], conversation_of(kind, m := json.loads(e['metadata'] or '{}'))) in conversations
                              and (kind != 'slack.message' or str(m.get('channel_id') or '').startswith('D') or str(m.get('thread_ts') or '') in threads)
                              and (text := own_text(e['body'])) and not PROFILE_SKIP.match(text) and not sent.wrote(e, text)), None)
                if not found:
                    continue
                if row['done_when']:  # their part went out, the result it is for hasn't come yet
                    outcomes.wait_for_result(db, row, '', now())
                    marked.append(row['id'])
                    continue
                # Their own reply is the to-do's step done: it closes by itself (once for this message, Undo for a day)
                decision_id = 'handled:' + hashlib.sha256(f"{row['id']}:{[int(found['id'])]}".encode()).hexdigest()[:32]
                if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                    continue  # closed for this message before and the owner took it back
                reason, stamp = i18n.t(ANSWERED_ELSEWHERE[kind]), now()
                db.execute('UPDATE suggestions SET handled_hint=? WHERE id=?',  # Done shows what closed it under the title
                           (encoded({'reason': reason, 'event_ids': [found['id']], 'at': stamp}), row['id']))
                outcomes.close_handled(db, row, decision_id, reason, stamp)
                marked.append(row['id'])
        return marked

    def edits_to_learn(self, run_id=None, limit=3, days=14, chars=350):
        """Edits not offered to a review yet, each offered once, for it to fold lasting habits into that channel's voice."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        clip = lambda v: (v or '') if len(v or '') <= chars else v[:chars] + '…'
        with self.connect() as db:
            rows = db.execute('SELECT e.id,e.kind,e.source,e.before_body,e.after_body,s.title FROM draft_edits e JOIN suggestions s ON s.id=e.suggestion_id '
                              "WHERE e.id NOT IN (SELECT edit_id FROM edits_offered) AND e.created_at>=? AND e.source!='agent' "  # an agent's rewrite is not the owner's
                              'ORDER BY e.created_at DESC LIMIT ?', (since, limit)).fetchall()
            if run_id:  # offered to this review: it's in the prompt
                db.executemany('INSERT OR IGNORE INTO edits_offered(edit_id,run_id,offered_at) VALUES(?,?,?)', [(r['id'], run_id, now()) for r in rows])
        return '\n'.join(f"- {EVENT_CHANNELS.get(DRAFT_EVENT_KINDS.get(r['kind']), r['kind'])}, \"{r['title']}\" (edit_id {r['id']})\n  Draft: {clip(r['before_body'])}\n  "
                         + ('They wrote themselves instead: ' if r['source'] == 'elsewhere' else 'They changed it to: ') + clip(r['after_body']) for r in rows)

    def voice_text(self, channels, chars):
        """The owner's voice for a draft that goes out on one of these channels (voice_channel names, most likely first):
        All, then each channel's block, as many whole ones as fit chars; noted for the use log (memory_use kind voice,
        its channel as row id). '' when none of them has a voice."""
        have = {v['channel']: v for v in self.voices()}
        out, size = [], len(VOICE_HEAD) + 1
        for channel in dict.fromkeys(['All', *(voice_channel(c) for c in channels)]):
            v = have.get(channel)
            line = v and f"- {channel}:{voice_lines(v['text'])}"
            if not line or size + len(line) + 1 > chars:
                continue
            out.append(line)
            size += len(line) + 1
            memory_use.note('voice', channel, line, 'always' if channel == 'All' else 'match', source='owner' if v['source'] == 'owner' else 'review',
                            at=v['updated_at'])
        return VOICE_HEAD + '\n' + '\n'.join(out) if out else ''

    def voices_text(self):
        return '\n'.join(f"- {v['channel']}:{voice_lines(v['text'])}" for v in self.voices())

    def tag_note(self, suggestion_id, kind, db, source='assistant'):
        return tag_note(db, suggestion_id, kind, source)

    def note_kind_counts(self, days=30):
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        with self.connect() as db:
            rows = db.execute("SELECT coalesce(k.kind,'unsorted') kind,count(*) n FROM decisions d LEFT JOIN note_kinds k ON k.decision_id=d.id "
                              "WHERE d.choice='other' AND d.source IN ('telegram','dashboard') AND d.created_at>=? GROUP BY 1", (since,)).fetchall()
        counts = {k: 0 for k in NOTE_KINDS + ('unsorted',)}
        counts.update({r['kind']: r['n'] for r in rows})
        return counts

    def rule_changes(self, since):
        with self.connect() as db:
            return rule_changes(db, since)

    def note_rule_files(self, paths):
        with self.connect() as db:
            note_rule_files(db, paths)
