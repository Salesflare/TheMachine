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


def clash_text(clash, side):
    """(title, body) of a clash to-do about its `side` event. Only that event is named: the other side is "something
    in your personal calendar" or "a work meeting", so nothing personal reaches a Work to-do (calendar_clashes.py)."""
    own = clash[side]
    when = locale_prefs.clock_text(own['start'].astimezone(local_tz()))  # its day is on the to-do's source line
    title = i18n.t('Calendar clash: {}', ' '.join(own['title'].split())[:70])
    if side == 'work':
        body = i18n.t('Overlaps your personal calendar at {}. Move it or decline?', when)
    else:
        body = i18n.t('Overlaps a work meeting at {}. Move it or decline?', when)
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
        """Each clash not raised before becomes one to-do, PER_DAY at most a day. Off with "calendar_clashes": false in
        the config. Returns the ids of the to-dos it made."""
        if self.config.get('calendar_clashes') is False:
            return []
        sides = calendar_clashes.calendar_sides(self.config.get('accounts'), graph.account_side)
        if set(sides.values()) != set(calendar_clashes.SIDES):  # a clash needs a work and a personal calendar
            return []
        current = current or dt.datetime.fromisoformat(now())
        since = (current - dt.timedelta(days=1)).isoformat()
        made = []
        with self.store.connect() as db:
            found = calendar_clashes.find(db, sides, current, calendar_owned)
            done = calendar_clashes.raised(db, [c['key'] for c in found])
            room = calendar_clashes.PER_DAY - calendar_clashes.raised_today(db, since)
        for clash in [c for c in found if c['key'] not in done][:max(room, 0)]:
            side = calendar_clashes.newer_side(clash)
            title, body = clash_text(clash, side)
            ahead = self.config.get('prepare_ahead', True) is not False and self.store.ahead_room(int(self.config.get('prepare_ahead_per_day', 10)))
            try:
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    saved = self.store.suggest(clash['key'], title, body, [clash[side]['id']], 'now', self.config.get('digest_at', '08:30'),
                                               work=side == 'work', personal=side == 'personal', ahead=ahead, _db=db,
                                               expires_at=clash[side]['start'].isoformat(), expires_what=title[:80])
                    calendar_clashes.keep(db, clash, side, saved['id'], now())
            except ValueError as error:  # not the owner's to act on (a calendar they only see), or its moment passed
                LOG.info('calendar clash skipped reason=%s', str(error)[:80])
                with self.store.connect() as db:
                    calendar_clashes.keep(db, clash, side, None, now())
                continue
            if not saved.get('duplicate'):
                made.append(saved['id'])
        if made:
            LOG.info('calendar clashes raised=%s', len(made))
        return made
