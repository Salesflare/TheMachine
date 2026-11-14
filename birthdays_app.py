"""The Birthdays template, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Its run (from routines_app.routine_template_run) is plain code, no model: whose birthday it is today among the
people the owner is close to (birthdays.py), from the calendars, Google's birthday events and its contacts' Birthdays
calendar (read here with calendar.readonly), Outlook's Birthdays calendar (read here with Calendars.Read: the scopes the
calendars already have, never a new one), Google contacts' birthdays and Birthday fields in the Graph. Each
of them gets one to-do on the channel the owner usually writes to them on, prepared ahead: the draft greeting is
written in that conversation, so in their language and the owner's voice, and nothing is sent until the owner says
so. A day without birthdays makes nothing."""
import datetime as dt
import logging

import birthdays
import crm_fixes
import i18n
import ms_graph
import routines
from sources import SourceError, credential, gog_read
from timeutil import local_tz
import timeutil

LOG = logging.getLogger('personal-assistant')
CALENDAR_READ = 'https://www.googleapis.com/auth/calendar.readonly'  # the scope the calendar already has


class BirthdaysApp:
    ACTIONS = {}  # its run starts from routines; the owner's tap on its to-do is any to-do's

    def birthdays_run(self, run):
        """A Birthdays run: today's to-dos (a test run only names them), then the run's result: who has one."""
        tz = local_tz()
        today = timeutil.clock(tz).date()
        outlook, code = self.birthdays_outlook(today, tz), self.birthdays_code()
        self.birthdays_save(self.birthdays_google(today, tz), code)
        with self.store.connect() as db:
            people = birthdays.today(db, today, tz, outlook, code)
        wished = [p['name'] for p in people if routines.is_test(run) or self.birthdays_todo(p, today)]
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if wished:
                routines.report(db, run['id'], text=i18n.t('Birthdays today: {}.', ', '.join(wished)), stamp=self.routines_stamp())
            else:
                routines.report(db, run['id'], nothing=True, why=self.birthdays_none(today, tz), stamp=self.routines_stamp())
        return True

    def birthdays_none(self, day, tz):
        """Why a run found nobody: no birthdays today, or no birthday info on this Machine at all, with what would add
        some given the calendars it reads (Google and Outlook show contacts' birthdays on them)."""
        with self.store.connect() as db:
            if birthdays.known(db):
                return i18n.t('No birthdays today')
        if self.birthdays_outlook(day, tz, days=366) or self.birthdays_google(day, tz, days=366):
            return i18n.t('No birthdays today')
        own = [a for a in self.config.get('accounts', []) if not a.get('shared') and a.get('calendar_id', 'primary') == 'primary']
        google = any(a.get('service') == 'calendar' for a in own)
        outlook = any(a.get('service') == 'outlook_calendar' for a in own)
        if google and outlook:
            return i18n.t('No birthday info yet. Add birthdays to your contacts.')
        if google:
            return i18n.t('No birthday info yet. Add birthdays to your Google contacts.')
        if outlook:
            return i18n.t('No birthday info yet. Add birthdays to your Outlook contacts.')
        return i18n.t('No birthday info yet. Connect your calendar, or add a Birthday field to people in the Graph.')

    def birthdays_outlook(self, day, tz, days=1):
        """The titles on the owner's Outlook Birthdays calendars today (or in the days from it). An account that can't
        be read is skipped."""
        start, end = birthdays.window(day, tz, days)
        titles = []
        for account in self.config.get('accounts', []):
            if account.get('service') != 'outlook_calendar' or account.get('shared') or account.get('calendar_id', 'primary') != 'primary':
                continue
            try:
                with ms_graph.budget(ms_graph.ROUND_SECONDS):  # a read Graph fails now and then is tried again
                    found = ms_graph.call(self.config, credential, account, 'calendars.list', {'$select': 'id,name', '$top': 50})
                    for calendar in found.get('value') or ():
                        if birthdays.fold(calendar.get('name')) not in birthdays.CALENDAR_NAMES or not calendar.get('id'):
                            continue
                        page = ms_graph.call(self.config, credential, account, 'calendars.view',
                                             {'id': calendar['id'], 'startDateTime': start, 'endDateTime': end, '$select': 'subject,isAllDay,isCancelled', '$top': 50})
                        titles += [str(e.get('subject') or '') for e in page.get('value') or () if not e.get('isCancelled')]
            except (ms_graph.GraphError, ValueError, RuntimeError, OSError) as error:
                LOG.info('birthdays outlook unread error=%s', type(error).__name__)
        return titles

    def birthdays_google(self, day, tz, days=1):
        """Today's birthdays (or in the days from it) on the owner's Google calendars, read now with calendar.readonly:
        Google's birthday events on the main calendar and the contacts' Birthdays calendar, also when it isn't
        connected or the sync leaves them out. Each Google account once; one that can't be read is skipped."""
        start, end = birthdays.window(day, tz, days)
        found, seen = [], set()
        for account in self.config.get('accounts', []):
            if (account.get('service') != 'calendar' or account.get('shared') or account.get('calendar_id', 'primary') != 'primary'
                    or account.get('transport') not in ('gog', 'broker') or str(account.get('email') or '').lower() in seen):
                continue
            seen.add(str(account.get('email') or '').lower())
            for calendar_id, only in (('primary', {'eventTypes': 'birthday'}), (birthdays.CONTACTS_CALENDAR, {})):
                params = {'calendarId': calendar_id, 'timeMin': start, 'timeMax': end, 'singleEvents': True, 'maxResults': 250, **only}
                try:
                    page = gog_read(self.config, account, 'calendar', 'v3', 'calendar.events.list', params, CALENDAR_READ)
                except (SourceError, ValueError, RuntimeError, OSError) as error:
                    LOG.info('birthdays google unread error=%s', type(error).__name__)
                    continue
                found += birthdays.google_birthdays(page.get('items'), day if days == 1 else None, calendar_id != 'primary')
        return found

    def birthdays_save(self, google, code):
        """Each Google birthday that is a close person's becomes their Birthday (source google_calendar), so their page
        shows it and the run reads it there: never over the owner's own (set or removed), and not again when the page
        already has that day (a year it knows stays)."""
        if not google:
            return 0
        import person_birthday
        saved, now = 0, timeutil.clock().isoformat()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for node, value in birthdays.google_people(db, birthdays.close_people(db), google, code).items():
                had = person_birthday.get(db, node, code)
                if had and (had['source'] == person_birthday.SOURCE or (f"--{had['month']:02d}-{had['day']:02d}" == value)):
                    continue
                saved += bool(person_birthday.offer(db, node, value, 'google_calendar', now))
        return saved

    def birthdays_todo(self, person, day):
        """One person's to-do (its id, also when it was made earlier today), on the channel the owner usually writes to
        them on, prepared ahead; None without such a channel."""
        with self.store.connect() as db:
            channel = birthdays.usual_channel(db, person['id'], timeutil.clock(), self.store.owner_user_ids)
            account = channel and db.execute('SELECT account_id FROM events WHERE id=?', (channel[1],)).fetchone()
        if not account:
            return None
        name = person['name']
        try:
            saved = self.store.suggest(f"birthday:{person['id']}:{day.isoformat()}", i18n.t('Wish {} a happy birthday', name)[:90],
                                       i18n.t('It’s {}’s birthday today.', name), [channel[1]], 'now', work=self.is_work([account[0]]),
                                       ahead=True, owner_step=False,
                                       expires_at=day.isoformat(), expires_what=i18n.t('{}’s birthday', name)[:80])
        except ValueError as error:
            LOG.info('birthday to-do not saved error=%s', type(error).__name__)
            return None
        return saved['id']

    def birthdays_code(self):
        """The owner's calling code (32), for a number in the Graph kept without its own; None when unknown."""
        region = crm_fixes.region_of({'country': self.config.get('country'), 'timezone': self.config.get('timezone') or getattr(local_tz(), 'key', '')})
        return crm_fixes.CALLING.get(region or '')
