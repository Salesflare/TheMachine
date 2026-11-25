"""Calendar clashes, the App's part: the pass that turns a new clash into a to-do (calendar_clashes.py has the rules).
A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import time

import calendar_clashes
import graph
import i18n
import locale_prefs
from machine.config import LOG
from machine.sources.calendar import calendar_owned
from timeutil import local_tz, now

CLASH_CHECK_SECONDS = 900


def clash_text(group):
    """(title, body) of a clash to-do about its event, at the moment the overlap begins. Only that event is named: the
    other side is "your personal calendar" or "a work meeting", so nothing personal reaches a Work to-do
    (calendar_clashes.py)."""
    own, first = group['about'], min(group['pairs'], key=lambda c: c['start'])
    when = locale_prefs.clock_text(first['start'].astimezone(local_tz()))  # its day is on the to-do's source line
    title = i18n.t('Calendar clash: {}', ' '.join(own['title'].split())[:70])
    if group['side'] == 'work':
        body = i18n.t('Overlaps your personal calendar at {}. Move it or decline?', when)
    elif first['work']['others']:
        body = i18n.t('Overlaps a work meeting at {}. Move it or decline?', when)
    else:  # a block of their own
        body = i18n.t('Overlaps your work calendar at {}. Move it or decline?', when)
    return title[:90], body[:700]


class CalendarClashesApp:
    ACTIONS = {}

    def clash_step(self, every=CLASH_CHECK_SECONDS):
        """About every quarter hour: new clashes between a work and a personal calendar become to-dos (raise_clashes)."""
        if time.monotonic() - self.__dict__.get('clashes_swept', -every) < every:
            return
        self.clashes_swept = time.monotonic()
        self.raise_clashes()

    def raise_clashes(self, current=None):
        """Each clash not raised before becomes a to-do (one per event, calendar_clashes.plan), PER_DAY at most a day, or
        joins the one its event has. Off with "calendar_clashes": false in the config. Returns the ids of the to-dos it
        made."""
        if self.config.get('calendar_clashes') is False:
            return []
        sides = calendar_clashes.calendar_sides(self.config.get('accounts'), graph.account_side)
        if set(sides.values()) != set(calendar_clashes.SIDES):  # a clash needs a work and a personal calendar
            return []
        current = current or dt.datetime.fromisoformat(now())
        since = (current - dt.timedelta(days=1)).isoformat()
        made = []
        with self.store.connect() as db:
            plan = calendar_clashes.plan(db, calendar_clashes.pairs(db, sides, current, calendar_owned), lambda sid: self.store.clash_untouched(db, sid))
            room = calendar_clashes.PER_DAY - calendar_clashes.raised_today(db, since)
        if any(plan[step] for step in ('join', 'quiet', 'drop', 'gone')):
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                for clash, side, sid in plan['join']:
                    calendar_clashes.keep(db, clash, side, sid, now())
                for clash in plan['quiet']:
                    calendar_clashes.keep(db, clash, 'work', None, now())
                for clash in plan['drop']:
                    calendar_clashes.drop(db, clash)
                for sid, why in plan['gone']:
                    self.store.clash_gone(db, sid, why)
        for group in plan['raise'][:max(room, 0)]:
            side, about, key = group['side'], group['about'], next(c['key'] for c in group['pairs'] if not c.get('row'))
            title, body = clash_text(group)
            ahead = self.config.get('prepare_ahead', True) is not False and self.store.ahead_room(int(self.config.get('prepare_ahead_per_day', 10)), due=about['start'].isoformat())
            try:
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    saved = self.store.suggest(key, title, body, [about['id']], 'now', self.config.get('digest_at', '08:30'),
                                               work=side == 'work', personal=side == 'personal', ahead=ahead, _db=db,
                                               expires_at=about['start'].isoformat(), expires_what=title[:80])
                    for clash in group['pairs']:
                        calendar_clashes.keep(db, clash, side, saved['id'], now())
                    for sid in group['gone']:
                        self.store.clash_gone(db, sid, 'moved')
            except ValueError as error:  # not the owner's to act on (a calendar they only see), or its moment passed
                LOG.info('calendar clash skipped reason=%s', str(error)[:80])
                with self.store.connect() as db:
                    for clash in group['pairs']:
                        if not clash.get('row'):
                            calendar_clashes.keep(db, clash, side, None, now())
                continue
            if not saved.get('duplicate'):
                made.append(saved['id'])
        if made:
            LOG.info('calendar clashes raised=%s', len(made))
        return made
