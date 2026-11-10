"""The Birthdays template, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Its run (from mail_cleanup_app.routine_template_run) is plain code, no model: whose birthday it is today among the
people the owner is close to (birthdays.py), from the calendars, Outlook's Birthdays calendar (read here with
Calendars.Read, the scope the calendar already has), Google contacts' birthdays and Birthday fields in the Graph. Each
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
from sources import credential
from timeutil import local_tz

LOG = logging.getLogger('personal-assistant')


class BirthdaysApp:
    ACTIONS = {}  # its run starts from routines; the owner's tap on its to-do is any to-do's

    def birthdays_run(self, run):
        """A Birthdays run: today's to-dos (a test run only names them), then the run's result: who has one."""
        tz = local_tz()
        today = dt.datetime.now(tz).date()
        outlook = self.birthdays_outlook(today, tz)
        with self.store.connect() as db:
            people = birthdays.today(db, today, tz, outlook, self.birthdays_code())
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
        if self.birthdays_outlook(day, tz, days=366):
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

    def birthdays_todo(self, person, day):
        """One person's to-do (its id, also when it was made earlier today), on the channel the owner usually writes to
        them on, prepared ahead; None without such a channel."""
        with self.store.connect() as db:
            channel = birthdays.usual_channel(db, person['id'], dt.datetime.now(dt.timezone.utc), self.store.owner_user_ids)
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
