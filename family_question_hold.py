"""An answer to a family member's question that goes by itself, and the hold before it does (family_question_always.py has
what may; docs/family.md, "Answers by itself").

Only where the owner chose Always for that one member, themselves, on the Sharing pane. The question is then an ordinary
waiting to-do with its draft and sources, and a notice says when it goes: "Answers Robin at 14:20". The owner can stop it,
edit it, send it now or decline. Done nothing by then, it goes, once, and Activity says so with a way back to Ask me first.

It waits for the owner like any other question instead, whenever something isn't as it was: the notice reached no phone and
no Telegram, the service restarted, the rule or the member's keys changed, they left, something on the matter is new or
changed, the day's answers are used up, a question of theirs was set aside meanwhile, or the time passed without this
Machine (asleep). At night nothing is told or sent: the notice comes in the morning, with a longer hold."""
from __future__ import annotations

import datetime as dt
import json
import logging
import secrets
import sqlite3

import timeutil
from i18n import t

LOG = logging.getLogger('personal-assistant')
KIND = 'question'
HOLD, MORE, MORNING = 10, 8, 30  # minutes: at least, up to this much more (so the time says nothing to the asker), after a night
LATE = 15                        # minutes after its time: no longer
EVENING = 21                     # the hour from which it waits for the morning
A_DAY = 3                        # answers by themselves to one member
ASIDE_DAYS = 3                   # after a question of theirs that was set aside, the next ones ask first


class Holds:
    """Mixed into family_questions.Questions. Set by the app: notify_hold(row, hold) tells the owner and returns whether it
    reached a phone or Telegram (the Telegram message's id, or True); hold_moved(ask_id, mark) whether something on the
    matter is new or changed since it was marked."""
    notify_hold = hold_moved = None
    _question_boot = None

    def question_boot(self):
        if not self._question_boot:
            self._question_boot = secrets.token_hex(8)
        return self._question_boot

    def question_always(self, db, ref, member_id):
        """When the owner chose Always for this one member, while it holds and their Machine is still the one it was chosen
        for; else None."""
        own = db.execute('SELECT rule,updated_at FROM fleet_rules WHERE fleet=? AND member_id=? AND kind=?', (ref, member_id, KIND)).fetchone()
        if not own or own['rule'] != 'always' or self.rule(db, ref, member_id, KIND)[0] != 'always' or not self.member(ref, member_id) or self.kind_of(ref) != 'family':
            return None
        try:
            pin = db.execute('SELECT changed_at FROM network_pins WHERE member_id=?', (member_id,)).fetchone()
        except sqlite3.OperationalError:
            return None
        return own['updated_at'] if pin and not (pin['changed_at'] and pin['changed_at'] >= own['updated_at']) else None

    def question_may(self, db, ref, member_id):
        """Whether one more answer may go to this member by itself today: the day's limit, and no question of theirs set
        aside lately."""
        mine = 'SELECT COUNT(*) FROM fleet_questions q JOIN fleet_in i ON i.id=q.id WHERE i.fleet=? AND i.member_id=? AND i.kind=? '
        count = lambda more, *args: db.execute(mine + more, (ref, member_id, KIND, *args)).fetchone()[0]
        return (count("AND i.choice='always' AND i.status='answered' AND i.decided_at>=?", self.question_since(days=1)) < A_DAY
                and not count("AND q.asked='aside' AND i.at>=?", self.question_since(days=ASIDE_DAYS)))

    def question_hold(self, db, ask_id, mark):
        """Holds a drafted answer, from its notice on. mark: what is on its matter now."""
        row = db.execute("SELECT fleet,member_id FROM fleet_in WHERE id=? AND status='waiting'", (str(ask_id),)).fetchone()
        chosen = row and self.question_always(db, row['fleet'], row['member_id'])
        if not chosen or not self.question_may(db, row['fleet'], row['member_id']):
            return False
        self.keep_hold(db, ask_id, {'boot': self.question_boot(), 'rule': chosen, 'mark': mark, 'since': timeutil.stamp()})
        return True

    def question_held(self, db):
        out = []
        for r in db.execute("SELECT i.*,q.hold,q.draft drafted,q.asked,q.state question_state FROM fleet_in i JOIN fleet_questions q ON q.id=i.id WHERE q.hold IS NOT NULL").fetchall():
            try:
                out.append((dict(r), json.loads(r['hold'])))
            except ValueError:
                out.append((dict(r), {}))
        return out

    def hold_end(self, ask_id, again=False):
        """Back to Ask me first. again: the owner was told it would go, so they hear of it once more."""
        with self.connect() as db:
            ended = bool(db.execute('SELECT 1 FROM fleet_questions WHERE id=? AND hold IS NOT NULL', (str(ask_id),)).fetchone())
            self.keep_hold(db, ask_id, None)
            row = db.execute("SELECT telegram_message_id FROM fleet_in WHERE id=? AND status='waiting'", (str(ask_id),)).fetchone()
            if ended and again and row:
                self.told_in(db, ask_id, None)
        if ended and row and row['telegram_message_id'] and self.retell:
            self.retell(row['telegram_message_id'])
        return ended

    def hold_local(self, stamp=None):
        local = self.hours.get('local_now')
        return (stamp or local()) if local else None

    def hold_night(self, local):
        """Whether the owner isn't to be told anything now: the evening, the night, until their morning."""
        hour, minute = timeutil.hour_minute(self.hours['morning']())
        return local.hour >= EVENING or (local.hour, local.minute) < (hour, minute)

    def hold_round(self):
        """Every held answer, each round of the Fleet's loop: told, sent when its time has come, or back to Ask me first."""
        with self.connect() as db:
            held = self.question_held(db)
        for row, hold in held:
            try:
                self.hold_step(row, hold)
            except Exception as error:  # noqa: BLE001 - whatever goes wrong, it waits for the owner
                LOG.warning('family question hold error=%s', type(error).__name__)
                self.hold_end(row['id'], again=True)

    def hold_step(self, row, hold):
        with self.connect() as db:
            chosen = self.question_always(db, row['fleet'], row['member_id'])
        if row['status'] != 'waiting':
            return self.hold_end(row['id'])
        if hold.get('boot') != self.question_boot() or not chosen or chosen != hold.get('rule'):
            return self.hold_end(row['id'], again=True)
        if not hold.get('goes_at'):
            return self.hold_tell(row, hold)
        now, at = timeutil.clock(), dt.datetime.fromisoformat(hold['goes_at'])
        if now < at:
            return None
        if now > at + dt.timedelta(minutes=LATE) or self.hold_night(self.hold_local()) or not self.hold_moved or self.hold_moved(row['id'], hold['mark']):
            return self.hold_end(row['id'], again=True)
        return self.hold_send(row, hold)

    def hold_tell(self, row, hold):
        """The notice, from which the hold counts. Not reaching the owner: an ordinary question."""
        local = self.hold_local()
        if local is None or not self.notify_hold or not self.hold_moved:
            return self.hold_end(row['id'])
        minutes = (MORNING if hold.get('night') else HOLD) + secrets.randbelow(MORE + 1)
        if self.hold_night(local) or self.hold_night(local + dt.timedelta(minutes=HOLD + MORE)):  # told in the morning
            if not hold.get('night'):
                self.hold_set(row['id'], hold, {**hold, 'night': True})
            return None
        if self.hold_moved(row['id'], hold['mark']):
            return self.hold_end(row['id'])
        told = {**hold, 'goes_at': (timeutil.clock() + dt.timedelta(minutes=minutes)).isoformat(timespec='seconds')}
        if not self.hold_set(row['id'], hold, told):
            return None
        with self.connect() as db:
            self.told_in(db, row['id'], timeutil.stamp())
        reached = self.notify_hold({**row, 'hold': json.dumps(told)}, told)
        if not reached:
            return self.hold_end(row['id'], again=True)
        if reached is not True:
            with self.connect() as db:
                self.telegram_in(db, row['id'], reached)
        return True

    def hold_set(self, ask_id, was, hold):
        with self.connect() as db:
            return self.keep_hold(db, ask_id, hold, was)

    def hold_send(self, row, hold):
        """Its time has come and nothing changed: sent, once. The last look is inside the transaction that marks it sent."""
        import fleet
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            draft = self.question_draft(db, row['id'])
            if (self.question_always(db, row['fleet'], row['member_id']) != hold['rule'] or not self.question_may(db, row['fleet'], row['member_id'])
                    or draft.get('state') != 'ready' or not draft.get('text')):
                ready = False
            else:
                ready = bool(self.keep_hold(db, row['id'], None, was=hold)
                             and self.move_in(db, row['id'], 'waiting', 'answered', 'always', fleet.now()))
                if ready:
                    self.keep_answer(db, row['id'], {'text': draft['text'], 'sources': [s['id'] for s in draft['sources']]})
        if not ready:
            return self.hold_end(row['id'], again=True)
        try:
            self.send_question(row['id'], {'text': draft['text'], 'auto': True})  # the asker sees that nobody read it first
        except Exception as error:  # noqa: BLE001 - refused or away: it waits for the owner with its draft (send_question)
            LOG.warning('family question not sent by itself error=%s', type(error).__name__)
            with self.connect() as db:
                self.told_in(db, row['id'], None)
        if row['telegram_message_id'] and self.retell:
            self.retell(row['telegram_message_id'])
        return True

    def question_ask_first(self, ask_id):
        """Activity's way back, from a line of an answer that went by itself: Ask me first for that member again."""
        with self.connect() as db:
            row = db.execute('SELECT fleet,member_id FROM fleet_in WHERE id=? AND kind=?', (str(ask_id), KIND)).fetchone()
        if row:
            self.set_rule(row['fleet'], row['member_id'], KIND, 'ask')
        return {'rule': 'ask'}


def local_time(value):
    return dt.datetime.fromisoformat(value).astimezone(timeutil.local_tz()).strftime('%H:%M')


def hold_line(row, hold):
    return t('Answers {} at {}', row['name'], local_time(hold['goes_at']))


def hold_text(row):
    """The answer, as a notice quotes it."""
    import family_questions
    return f"“{(family_questions._load(row['drafted']) or {}).get('text', '')}”"
