"""Questions in a Family (docs/family.md, "Ask someone's Machine"): the owner asks one member's Machine something, as "any
news about the carpet?", and that member's Machine answers from its own owner's personal messages.

First comes a turn that sees only the question (family_question_check.py): an ordinary household matter, asked the
ordinary way? If not, or if it isn't sure, the question is set aside: nothing is searched or drafted, the to-do shows only
the question and the notice not even that (hushed).
- Ask me first (the default): this Machine drafts an answer in the background (family_question_sources.py: what it may
  read, the drafting turn and its checks; machine/app/family_questions.py runs it). The owner gets a to-do with the
  question quoted, the messages the draft comes from and the draft, to edit. Only their Send sends it.
- Never: not drafted, not shown to act on.
There is no Always: every answer is read by its owner, and from a notification or Telegram a question only opens.

What the asker's Machine hears is the same for every other outcome. It is told once that the question waits, and
nothing more when the owner declines, has it on Never, lets it expire, when no draft could be made, or when the asker
asks too much: so nothing says which one it was. Not answered in APPROVAL_DAYS days, it reads "No answer". A Machine
from before questions declines them itself: the asker sees that it needs an update first.

Safety: the question is untrusted text, kept as one plain line (parse) and only shown quoted, searched for and given to
the turns as data. It is taken in the Fleet's loop, which never runs a model: the draft is made by a worker of the
app, once. Each question and the exact answer that went are in the answering owner's Activity (activity)."""
from __future__ import annotations

import datetime as dt
import json
import sqlite3

import activity_log
import timeutil
from i18n import t
from machine.owner_error import OwnerError

KIND = 'question'
CHARS, ANSWER_CHARS = 300, 600
OPEN, A_DAY = 3, 10      # questions from one member: waiting at once, and taken in a day
RUNS = 6                 # questions a day that may use the model, over everyone in the Family
STALE = 300              # seconds a draft may take before its question waits without one
HOUSEHOLD, ASIDE = 'household', 'aside'  # what the turn on the question alone calls it (fleet_questions.asked)
RECENT, RECENT_DAYS = 40, 30             # the same member's earlier questions that turn sees
DRAFTING = 'drafting'    # fleet_in's status while a draft is made: nothing shows or acts on it yet
NOW = ('waiting', 'answered', 'expired', 'declined')
CONTEXT = 'family-question:'
SCHEMA = '''
CREATE TABLE IF NOT EXISTS fleet_questions(id TEXT PRIMARY KEY,state TEXT NOT NULL,draft TEXT,answer TEXT,day TEXT,at TEXT NOT NULL);
'''
# state: pending (no draft yet), running, then ready, empty, private, none (no safe draft), held (a usage limit or the
# day's drafts are used up) or failed. draft: {'text', 'sources': [{id, kind, title, from, at}]}. answer: what went,
# {'text', 'sources': [ids]}. day: the day its turns ran. asked: what the question is (family_question_check.py), none when
# that couldn't be judged.


def ensure(db):
    db.executescript(SCHEMA)
    if 'asked' not in {r[1] for r in db.execute('PRAGMA table_info(fleet_questions)')}:  # added 2026-11-23
        db.execute('ALTER TABLE fleet_questions ADD COLUMN asked TEXT')


def hushed(row):
    """Whether a notice leaves this question's words out: it isn't known to be an ordinary household matter."""
    import fleet
    return row['kind'] == KIND and (fleet._get(row, 'asked') != HOUSEHOLD or fleet._get(row, 'question_state') == 'private')


def parse(question):
    import fleet
    text = fleet.free_text(question.get('text'), CHARS) if isinstance(question, dict) else ''
    return {'text': text} if len(text) >= 3 else None


def clean_answer(answer):
    import fleet
    text = fleet.free_text(answer.get('text'), ANSWER_CHARS) if isinstance(answer, dict) else ''
    return {'text': text} if text else None


def question_text(question):
    return f"“{(question or {}).get('text', '')}”"


def answer_text(answer):
    return (answer or {}).get('text') or t('no answer')


def _load(value, default=None):
    try:
        found = json.loads(value) if value else default
    except ValueError:
        return default
    return found if isinstance(found, dict) else default


def activity(db, limit):
    """The Activity lines of the questions asked here: who, what, and exactly what was sent (activity_log.register)."""
    try:
        rows = db.execute("SELECT i.id,i.name,i.question,i.status,i.choice,i.at,i.decided_at,q.answer FROM fleet_in i LEFT JOIN fleet_questions q "
                          'ON q.id=i.id WHERE i.kind=? ORDER BY coalesce(i.decided_at,i.at) DESC LIMIT ?', (KIND, limit)).fetchall()
    except sqlite3.OperationalError:
        return  # no Fleet tables here yet
    for r in rows:
        answer = _load(r['answer'])
        what = t('{} asked: {}', r['name'], question_text(_load(r['question'])))
        if answer and r['status'] == 'answered':
            outcome, status = 'done', t('Answered')
        elif r['status'] in ('waiting', DRAFTING):
            outcome, status = 'pending', t('Waiting for you')
        else:
            outcome, status = 'refused', {'expired': t('Not answered in time')}.get(r['status']) or (
                t('Not answered (the rule is Never)') if r['choice'] in ('rule', 'never') else
                t('Not answered (too many questions)') if r['choice'] == 'limit' else t('Declined'))
        yield {'id': 'question:' + r['id'], 'kind': 'fleet', 'at': r['decided_at'] or r['at'], 'what': what, 'where': t('Family'), 'outcome': outcome,
               'status': status, 'by': None, 'todo': None, 'detail': t('Sent: {}', question_text(answer)) if outcome == 'done' else None}


activity_log.register('fleet', activity)


class Questions:
    """Mixed into fleet.Fleet. Set by the app: draft_answer(ask_id) starts the draft in the background."""
    draft_answer = None

    # -- the owner asks
    def question_fleet(self):
        """The owner's Family, where the Network carries questions (the directory's asks), else None."""
        ref = self.family_ref()
        return ref if ref and KIND in (self.fleets()[ref].get('asks') or ()) and self.teammates(ref) else None

    def ask_question(self, member_id, text):
        ref = self._family()
        if not self.question_fleet():
            raise OwnerError(t('Questions come with the Network’s next update.'))
        member = self.member(ref, member_id)
        if not member:
            raise OwnerError('Not in your Family')
        question = parse({'text': text})
        if not question:
            raise OwnerError(t('Ask a question of at least a few words.'))
        import fleet
        name = fleet.clean(fleet.label(member), 80)
        with self.connect() as db:
            rows = db.execute('SELECT status,at FROM fleet_out WHERE fleet=? AND member_id=? AND kind=? AND at>=?',
                              (ref, member_id, KIND, self.question_since(days=fleet.APPROVAL_DAYS))).fetchall()
        if sum(r['status'] in ('asked', 'waiting') for r in rows) >= OPEN:
            raise OwnerError(t('{} of your questions already wait for {}.', OPEN, name))
        if sum(r['at'] >= self.question_since(days=1) for r in rows) >= A_DAY:
            raise OwnerError(t('That’s enough questions for {} today.', name))
        return self.ask_context(KIND, question, CONTEXT, ref, to=[member_id])[0]

    @staticmethod
    def question_since(**delta):
        return (timeutil.clock() - dt.timedelta(**delta)).isoformat(timespec='seconds')

    def questions_view(self, groups):
        """The owner's own questions, newest first, as they stand: waiting, answered, no answer, or a Machine that needs
        an update. groups: family_view's, of the kind question."""
        import fleet
        out, late = [], self.question_since(days=fleet.APPROVAL_DAYS)
        for g in groups:
            a = g['answers'][0]
            answer = a['answer'] if a['status'] == 'answered' else None
            state = ('answered' if answer else 'old' if a['status'] == 'declined' else
                     'none' if a['status'] == 'expired' or g['at'] < late else 'waiting')
            out.append({'id': g['id'], 'at': g['at'], 'name': a['name'], 'question': g['question'].get('text', ''), 'state': state,
                        **({'answer': answer['text']} if answer else {})})
        return out[:10]

    def question_answered(self, row, answer):
        """An answer came: the owner is told, once (their own phone and Telegram)."""
        if answer and self.tell and row['status'] != 'answered':
            first = row['name'].split()[0] if row['name'].split() else row['name']
            said = question_text(answer)
            self.tell(t('{} answered: {}', first, said), row['id'])

    # -- a member asks
    def take_question(self, ask, teammate, ref, question, name):
        """Kept, and its draft started; or nothing more, by the owner's rule or the limits. Their Machine hears the same
        of either. Never a model, and never an answer, here."""
        import fleet
        if not teammate or not question or self.kind_of(ref) != 'family':
            with self.connect() as db:
                self.log(db, 'in', ref, ask.get('from'), name, KIND if ref in self.fleets() else 'other', 'a question this Machine does not answer', 'declined')
            self.relay.call('POST', '/answer', {'id': ask['id'], 'status': 'declined'})
            return 'declined'
        member = teammate['member_id']
        with self.connect() as db:
            row = db.execute('SELECT status FROM fleet_in WHERE id=?', (ask['id'],)).fetchone()
            status = row['status'] if row else None
            if status is None:
                rule = self.rule(db, ref, member, KIND)[0]
                asked = db.execute('SELECT status,at,choice FROM fleet_in WHERE fleet=? AND member_id=? AND kind=? AND at>=?',
                                   (ref, member, KIND, self.question_since(days=fleet.APPROVAL_DAYS))).fetchall()
                today = [r for r in asked if r['at'] >= self.question_since(days=1)]
                over = sum(r['status'] in ('waiting', DRAFTING) for r in asked) >= OPEN or len(today) >= A_DAY
                status, choice = ('declined', 'rule') if rule == 'never' else ('declined', 'limit') if over else (DRAFTING, None)
                if len(today) < A_DAY * 3:  # more than the Network carries: not kept, so nobody fills the disk
                    self.keep_in(db, ask['id'], ref, member, name, KIND, question, status, choice)
                if status == DRAFTING:
                    db.execute("INSERT OR IGNORE INTO fleet_questions(id,state,at) VALUES(?,'pending',?)", (ask['id'], fleet.now()))
        if status != 'answered':
            self.relay.call('POST', '/answer', {'id': ask['id'], 'status': 'waiting'})
        if status == DRAFTING:
            self.draft_answer(ask['id']) if self.draft_answer else self.question_drafted(ask['id'], {'state': 'none'})
        return 'waiting'

    def question_earlier(self, ask):
        """The questions this member asked before this one lately, newest first: their own words, however each ended."""
        with self.connect() as db:
            rows = db.execute('SELECT question FROM fleet_in WHERE fleet=? AND member_id=? AND kind=? AND id<>? AND at>=? ORDER BY at DESC,id LIMIT ?',
                              (ask['fleet'], ask['member_id'], KIND, ask['id'], self.question_since(days=RECENT_DAYS), RECENT)).fetchall()
        return [text for r in rows if (text := (_load(r['question']) or {}).get('text'))]

    def question_claim(self, ask_id):
        """The question to draft for, once: {'id', 'fleet', 'member_id', 'name', 'question'}; None when it was taken before
        (a draft cut off by a restart is never run again)."""
        with self.connect() as db:
            taken = db.execute("UPDATE fleet_questions SET state='running' WHERE id=? AND state='pending'", (str(ask_id),)).rowcount
            row = db.execute('SELECT id,fleet,member_id,name,question FROM fleet_in WHERE id=? AND status=?', (str(ask_id), DRAFTING)).fetchone()
        if not taken or not row:
            return None
        return {**{k: row[k] for k in ('id', 'fleet', 'member_id', 'name')}, 'question': (_load(row['question']) or {}).get('text', '')}

    def question_run(self, ask_id):
        """Whether its model turns may run: for RUNS questions a day, over everyone. Counted before they run."""
        day = timeutil.today().isoformat()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT COUNT(*) FROM fleet_questions WHERE day=?', (day,)).fetchone()[0] >= RUNS:
                return False
            return bool(db.execute("UPDATE fleet_questions SET day=? WHERE id=? AND state='running'", (day, str(ask_id))).rowcount)

    def question_drafted(self, ask_id, result):
        """The draft, or why there is none: from now on the question waits for the owner. Only the first outcome counts: a
        draft that comes after its question already waits without one changes nothing."""
        import fleet
        kept = {k: result[k] for k in ('text', 'sources') if result.get(k)}
        with self.connect() as db:
            if not self.move_in(db, ask_id, DRAFTING, 'waiting'):
                return
            db.execute('UPDATE fleet_questions SET state=?,draft=?,asked=? WHERE id=?',
                       (result['state'], json.dumps(kept) if kept else None, result.get('asked'), str(ask_id)))
            row = db.execute('SELECT status,fleet,member_id FROM fleet_in WHERE id=?', (str(ask_id),)).fetchone()
            if row and row['status'] == 'waiting' and self.rule(db, row['fleet'], row['member_id'], KIND)[0] == 'never':
                self.move_in(db, ask_id, 'waiting', 'declined', 'rule', fleet.now())  # Never was chosen meanwhile

    def question_round(self):
        """A draft that takes too long, or was cut off by a restart: its question waits without one (only the first outcome
        counts, should its draft still come)."""
        with self.connect() as db:
            rows = [r['id'] for r in db.execute('SELECT id FROM fleet_in WHERE kind=? AND status=? AND at<?', (KIND, DRAFTING, self.question_since(seconds=STALE)))]
        for ask_id in rows:
            self.question_drafted(ask_id, {'state': 'failed'})

    def question_draft(self, db, ask_id):
        """What the owner's to-do shows: the draft and its messages, or why there is none. Nothing of it for a question that
        was set aside or whose answer may be private: neither that something was found nor that nothing was."""
        row = db.execute('SELECT state,draft,asked FROM fleet_questions WHERE id=?', (str(ask_id),)).fetchone()
        if not row:
            return {'state': 'none'}
        if row['asked'] == ASIDE or row['state'] == 'private':
            return {'state': 'aside'}
        return {'state': row['state'], **(_load(row['draft']) or {})}

    def is_question(self, ask_id):
        with self.connect() as db:
            row = db.execute('SELECT kind FROM fleet_in WHERE id=?', (str(ask_id),)).fetchone()
        return bool(row) and row['kind'] == KIND

    def decide_question(self, ask_id, choice, text=None, retell=True):
        """The owner on a question, from their dashboard: Send with the answer as they see it, Decline, or Never from
        this member. Only Send sends anything."""
        import fleet
        if choice == 'always':
            raise OwnerError(t('Questions are answered one at a time: send this answer, or decline'))
        if choice not in ('once', 'decline', 'never'):
            raise OwnerError('Choose once, decline or never')
        answer = None
        if choice == 'once':
            said = fleet.free_text(text, ANSWER_CHARS)
            if not said:  # also a Send without the answer in it, as a notification's would be: the owner reads it first
                raise OwnerError('Write an answer first, or decline')
            answer = {'text': said}
        with self.connect() as db:
            row = db.execute("SELECT * FROM fleet_in WHERE id=? AND status='waiting'", (str(ask_id),)).fetchone()
            if not row or not self.move_in(db, ask_id, 'waiting', 'answered' if answer else 'declined', choice, fleet.now()):
                raise OwnerError('That question was answered or has expired')
            if answer:
                draft = self.question_draft(db, ask_id)
                self.keep_answer(db, ask_id, {**answer, 'sources': [s['id'] for s in draft.get('sources') or []]})
            if choice == 'never':
                self.set_member_rule(db, row['fleet'], row['member_id'], KIND, 'never')
        if answer:
            self.send_question(row['id'], answer)
        if retell and row['telegram_message_id'] and self.retell:
            self.retell(row['telegram_message_id'])
        if choice == 'never':
            self.settle_waiting(row['fleet'], row['member_id'], KIND, retell=retell)
        return {'status': 'answered' if answer else 'declined', 'answer': answer_text(answer) if answer else None}

    def keep_answer(self, db, ask_id, answer):
        db.execute('INSERT INTO fleet_questions(id,state,answer,at) VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET answer=excluded.answer',
                   (str(ask_id), 'none', json.dumps(answer), timeutil.stamp()))

    def send_question(self, ask_id, answer):
        """Sends the kept answer; refused by the Network, the question waits again and nothing is kept as sent."""
        try:
            self.relay.call('POST', '/answer', {'id': ask_id, 'status': 'answered', 'answer': answer})
        except Exception:
            with self.connect() as db:
                self.move_in(db, ask_id, 'answered', 'waiting')
                db.execute('UPDATE fleet_questions SET answer=NULL WHERE id=?', (str(ask_id),))
            raise

    def settle_question(self, row):
        """A waiting question under the owner's rules now: Never takes it off their list. Nothing is sent; nothing else
        settles it."""
        import fleet
        with self.connect() as db:
            if self.rule(db, row['fleet'], row['member_id'], KIND)[0] != 'never':
                return False
            return bool(self.move_in(db, row['id'], 'waiting', 'declined', 'rule', fleet.now()))
