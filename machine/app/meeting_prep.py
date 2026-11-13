"""Meeting prep, the App's part: the pass that turns an upcoming meeting with people from outside into one briefing
to-do (meeting_prep.py has the rules). A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import sqlite3
import threading
import time

import graph
import i18n
import locale_prefs
import meeting_prep
import person_summary
from machine.config import LOG
from machine.sources.calendar import calendar_owned
from machine.store.review import CARD_OPEN
from models import background_model
from timeutil import local_tz, now

MEETING_PREP_SECONDS = 600  # how often the calendar is looked at
MEETING_PREP_TURN_SECONDS = 180


class MeetingPrepApp:
    ACTIONS = {}

    def meeting_prep_step(self, every=MEETING_PREP_SECONDS):
        """About every ten minutes: a moved or canceled meeting's briefing follows it, and the next meeting due a
        briefing gets its one turn, in a thread of its own, within the usage budget like every background turn."""
        if self.config.get('meeting_prep') is False or not (self.config.get('review_worker') or {}).get('enabled'):
            return None
        if time.monotonic() - self.__dict__.get('meeting_prep_at', -every) < every:
            return None
        self.meeting_prep_at = time.monotonic()
        self.meeting_prep_follow()
        thread = getattr(self, '_meeting_prep_thread', None)
        if thread and thread.is_alive():
            return None
        if not self.background_spaced() or self.background_pause(job='meeting-prep'):
            return None
        meeting = self.meeting_prep_next()
        if not meeting:
            return None
        self.background_started()
        self._meeting_prep_thread = threading.Thread(target=self.meeting_prep_run, args=(meeting,), name='meeting-prep', daemon=True)
        self._meeting_prep_thread.start()
        return meeting['id']

    def meeting_prep_owner(self, db):
        owner = graph.Owner({'accounts': self.config.get('accounts', [])}, db)
        return owner.emails, owner.domains | set(owner.team or ())

    def meeting_prep_next(self, current=None):
        """The soonest meeting due a briefing and not judged yet, with what it reads; None when there is none or the
        day's turns are used. One with no evidence is passed over (it may have some on a later pass), never asked."""
        current = current or dt.datetime.fromisoformat(now())
        sides = {a['id']: graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')}
        with self.store.connect() as db:
            if meeting_prep.judged_today(db, (current - dt.timedelta(days=1)).isoformat()) >= meeting_prep.PER_DAY:
                return None
            emails, domains = self.meeting_prep_owner(db)
            found = meeting_prep.upcoming(db, current, calendar_owned, emails, domains, local_tz())
            done = meeting_prep.judged(db, [m['key'] for m in found])
            for meeting in found:
                if meeting['key'] in done:
                    continue
                if meeting_prep.taken(db, meeting['id'], CARD_OPEN):  # the review already made a to-do for it
                    meeting_prep.keep(db, meeting, 'taken', None, now())
                    continue
                side = sides.get(meeting['account_id'])
                evidence = meeting_prep.evidence(db, meeting, side, sides, emails, current, CARD_OPEN, graph.resolve,
                                                 person_summary.prep_lines, graph.excerpt)
                if not meeting_prep.worth_asking(evidence):
                    continue  # quality or nothing: no turn, no to-do
                if all(p.get('role') and graph.personal_relation(p['role']) for p in evidence['people']):
                    meeting_prep.keep(db, meeting, 'family', None, now())  # family and friends only: their own life, no turn
                    continue
                return {**meeting, 'side': side, 'evidence': evidence}
        return None

    def meeting_prep_model_turn(self, text):
        stand_in = getattr(self, 'meeting_prep_model', None)  # tests and the sandbox: (config, prompt)
        if stand_in:
            return stand_in(self.config, text)
        import help_chat
        swap = background_model(self.config)  # never the costliest model for background work
        return help_chat.openclaw_model_run(self.config, text, '/'.join(swap) if swap else None, timeout=MEETING_PREP_TURN_SECONDS)

    def meeting_prep_run(self, meeting):
        """The meeting's one turn, then its to-do, or nothing when the turn found nothing useful. Returns the to-do's id."""
        import help_chat
        tz = local_tz()
        text = meeting_prep.prompt(meeting, meeting['evidence'], tz, i18n.prompt_rule(locale_prefs.language_of(self.config)))
        try:
            reply = self.meeting_prep_model_turn(text)
        except help_chat.Unavailable:
            LOG.info('meeting prep: no model now')
            return None  # not judged: the next pass asks again
        except (OSError, ValueError, TypeError) as failure:  # the turn may have run: never a second one for this meeting
            LOG.warning('meeting prep error=%s', type(failure).__name__)
            with self.store.connect() as db:
                meeting_prep.keep(db, meeting, 'failed', None, now())
            return None
        found = meeting_prep.parse(reply, meeting['evidence'])
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if meeting_prep.judged(db, [meeting['key']]):
                return None
            if not found or found['area'] == 'personal':
                meeting_prep.keep(db, meeting, 'personal' if found else 'nothing', None, now())
                LOG.info('meeting prep verdict=%s', 'personal' if found else 'nothing')
                return None
            title = found['title'] if found['title'] else i18n.t('Prepare for {}', meeting['title'][:70])
            body = meeting_prep.body_text(found['fields'], i18n.t)
            try:
                saved = self.store.suggest(meeting['key'], title[:90], body, [meeting['id'], *found['sources']], 'now', self.config.get('digest_at', '08:30'),
                                           work=True, _db=db, expires_at=meeting['start'].isoformat(), expires_what=title[:80])
            except ValueError as error:  # not the owner's to act on, or its moment passed
                LOG.info('meeting prep skipped reason=%s', str(error)[:80])
                meeting_prep.keep(db, meeting, 'nothing', None, now())
                return None
            meeting_prep.keep(db, meeting, 'made', saved['id'], now())
        LOG.info('meeting prep made=1')
        return saved['id']

    def meeting_prep_follow(self, current=None):
        """A briefing follows its meeting: a new time moves when it closes by itself; a canceled meeting's closes now."""
        current = current or dt.datetime.fromisoformat(now())
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                for sid, start, key in meeting_prep.moved(db, CARD_OPEN, current):
                    at = (start or current).astimezone(dt.timezone.utc).isoformat(timespec='seconds')
                    self.store.move_moment(db, sid, at)
                    meeting_prep.moved_to(db, key, start or current)
        except sqlite3.OperationalError as error:
            LOG.warning('meeting prep follow error=%s', type(error).__name__)
        self.store.expire_passed()
