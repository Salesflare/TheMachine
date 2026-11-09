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
            people = birthdays.today(db, today, tz, outlook)
        wished = [p['name'] for p in people if routines.is_test(run) or self.birthdays_todo(p, today)]
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if wished:
                routines.report(db, run['id'], text=i18n.t('Birthdays today: {}.', ', '.join(wished)), stamp=self.routines_stamp())
            else:
                routines.report(db, run['id'], nothing=True, why=i18n.t('No birthdays today'), stamp=self.routines_stamp())
        return True

    def birthdays_outlook(self, day, tz):
        """The titles on the owner's Outlook Birthdays calendars today. An account that can't be read is skipped."""
        start, end = birthdays.window(day, tz)
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
