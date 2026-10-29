"""To-dos tied to a moment, and text that stays true on later days.

An agreed meeting in the calendar needs no confirmation to-do (the review's rule). A to-do whose whole point is a
moment (a confirmation or reminder before a meeting: the review's expires_at) closes by itself once it has passed, as
"No longer needed", with Undo. A title or summary never keeps "today" or "tomorrow": the day itself is saved, in the
words' own language (locale_prefs.undated)."""
import datetime as dt
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import locale_prefs

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('moment_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

WED = dt.datetime(2026, 10, 28, 9, 0)  # Wed Oct 28, the day the to-do was written


def at(text):
    return patch.object(a, 'now', lambda: text)


class RelativeDayWords(unittest.TestCase):
    def setUp(self):
        self.addCleanup(locale_prefs._current.update, dict(locale_prefs._current))
        locale_prefs._current.update(locale='en-US', language='en')

    def test_every_app_language_gets_the_day_itself(self):
        for text, want in (('Today at 13:30: Angular migration', 'Wed, Oct 28 at 13:30: Angular migration'),
                           ('Meet Sam tomorrow at 10', 'Meet Sam Thu, Oct 29 at 10'),
                           ('Sam replied yesterday', 'Sam replied Tue, Oct 27'),
                           ('Vandaag om 13:30: Angular migration met Kevin op kantoor', 'Wo 28 okt om 13:30: Angular migration met Kevin op kantoor'),
                           ('Morgen om 10 met Kim', 'Do 29 okt om 10 met Kim'),
                           ("Rendez-vous aujourd’hui à 15h", 'Rendez-vous mer. 28 oct. à 15h'),
                           ('Rappel demain', 'Rappel jeu. 29 oct.'),
                           ('Morgen um 10 mit Anna', 'Do. 29. Okt. um 10 mit Anna'),
                           ('Heute Termin mit Anna', 'Mi. 28. Okt. Termin mit Anna'),
                           ('Reunión hoy a las 10', 'Reunión mié 28 oct a las 10'),
                           ('Llamar mañana a las 9', 'Llamar jue 29 oct a las 9'),
                           ('Riunione domani alle 9', 'Riunione gio 29 ott alle 9'),
                           ('Ieri ha risposto', 'Mar 27 ott ha risposto'),
                           ('Reunião hoje às 10', 'Reunião qua. 28 de out. às 10'),
                           ('Ligar amanhã', 'Ligar qui. 29 de out.')):
            with self.subTest(text=text):
                self.assertEqual(locale_prefs.undated(text, WED)[0], want)

    def test_quotes_mornings_and_possessives_stay(self):
        for text in ('Kevin wrote "see you tomorrow"', 'Kevin schreef “tot morgen”', 'Llamó esta mañana', 'Am Morgen im Büro',
                     'Goede morgen allemaal', "Today's numbers", 'Here and hier'):
            with self.subTest(text=text):
                self.assertEqual(locale_prefs.undated(text, WED), (text, []))

    def test_morgen_reads_in_the_owners_language_when_the_words_cannot_tell(self):
        self.assertEqual(locale_prefs.undated('Morgen', WED, 'de')[0], 'Do. 29. Okt.')
        self.assertEqual(locale_prefs.undated('Morgen', WED, 'nl')[0], 'Do 29 okt')


class Store(unittest.TestCase):
    def setUp(self):
        self.addCleanup(locale_prefs._current.update, dict(locale_prefs._current))
        locale_prefs._current.update(locale='nl-BE', language='en')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('g', {}, [{'account_id': 'g', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-10-28T07:00:00+00:00',
                                          'title': 'Angular migration', 'body': 'Woensdag op kantoor?', 'deleted': False,
                                          'metadata': {'from': 'Kevin <kevin@example.com>', 'thread_id': 't1'}}])
        self.store.commit_page('c', {}, [{'account_id': 'c', 'source_id': 'ev1', 'kind': 'calendar.event', 'occurred_at': '2026-10-28T12:30:00+00:00',
                                          'title': 'Angular migration', 'body': 'Office', 'deleted': False,
                                          'metadata': {'start': {'dateTime': '2026-10-28T13:30:00+01:00'}, 'end': {'dateTime': '2026-10-28T15:00:00+01:00'},
                                                       'timezone': 'Europe/Brussels', 'status': 'confirmed'}}])
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'g'}, {'id': 'c'}], 'prepare_ahead': False}
        tz = patch.object(a, 'LOCAL_TZ', a.ZoneInfo('Europe/Brussels'))
        tz.start()
        self.addCleanup(tz.stop)

    def suggest(self, **args):
        with at('2026-10-28T07:05:00+00:00'):
            return self.app.action('suggest', {'dedupe_key': 'kevin', 'title': 'Vandaag om 13:30: Angular migration met Kevin',
                                               'body': 'De meeting met Kevin staat vandaag 13:30 tot 15:00 in je agenda.',
                                               'event_ids': [1], 'when': 'now', **args})

    def card(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def test_the_review_title_and_summary_are_saved_with_the_day(self):
        saved = self.suggest()
        card = self.card(saved['id'])
        self.assertEqual(card['title'], 'Wo 28 okt om 13:30: Angular migration met Kevin')
        self.assertEqual(card['body'], 'De meeting met Kevin staat wo 28 okt 13:30 tot 15:00 in je agenda.')
        self.assertIn('never today, tomorrow or yesterday', saved['dates'])

    def test_a_preparation_title_is_saved_with_the_day_too(self):
        sid = self.suggest()['id']
        self.store.decide(sid, 'accept', '', 'd1', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        with at('2026-10-28T08:00:00+00:00'):
            self.app.action('prepare', {'suggestion_id': sid, 'job_id': job, 'body': 'Kevin verwacht je morgen.', 'outcome': 'needs_you',
                                        'needs': 'check it', 'title': 'Morgen: Angular migration'})
        card = self.card(sid)
        self.assertEqual((card['title'], card['body']), ('Do 29 okt: Angular migration', 'Kevin verwacht je do 29 okt.'))

    def test_a_to_do_tied_to_a_moment_closes_by_itself_once_it_passed_with_undo(self):
        sid = self.suggest(expires_at='2026-10-28T13:30:00+01:00', expires_what='the meeting with Kevin')['id']
        self.assertEqual(self.card(sid)['expires_at'], '2026-10-28T12:30:00+00:00')
        with at('2026-10-28T12:29:00+00:00'):
            self.assertEqual(self.store.expire_passed(), [])
        self.assertEqual(self.card(sid)['status'], 'pending')
        with at('2026-10-29T08:00:00+00:00'):
            self.assertEqual(self.store.expire_passed(), [sid])
            self.assertEqual(self.store.expire_passed(), [])  # once
        card = self.card(sid)
        self.assertEqual((card['status'], card['expired_at']), ('completed', '2026-10-29T08:00:00+00:00'))
        self.assertGreater(card['undo_until'], '2026-10-29T20:00')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT source FROM decisions WHERE suggestion_id=? AND choice='complete'", (sid,)).fetchone()[0], 'expiry')
            self.assertEqual(db.execute("SELECT status FROM deliveries WHERE suggestion_id=?", (sid,)).fetchone()[0], 'cancelled')
        # Telegram keeps the line as written, so it names the day; never "Overdue" or a stored "today"
        self.assertEqual(a.expired_text(card), 'No longer needed: the meeting with Kevin was on Wed 28 Oct at 13:30.')
        self.assertIn('No longer needed: the meeting with Kevin', a.card(card))
        self.assertNotIn('Due', a.card({**card, 'due': '2026-10-28'}))
        # Undo brings it back and it stays: its moment no longer closes it
        with at('2026-10-29T08:01:00+00:00'):
            self.assertEqual(self.store.decide(sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
            self.assertEqual(self.store.expire_passed(), [])
        card = self.card(sid)
        self.assertEqual((card['status'], card['expires_at'], card['expired_at']), ('pending', None, None))

    def test_with_a_calendar_event_its_start_is_the_moment_whatever_the_review_wrote(self):
        # The review wrote 10:00; the meeting in the calendar starts at 13:30, and the Done line must say 13:30
        sid = self.suggest(event_ids=[1, 2], expires_at='2026-10-28T10:00:00+01:00', expires_what='the meeting with Kevin')['id']
        self.assertEqual(self.card(sid)['expires_at'], '2026-10-28T12:30:00+00:00')
        sid = self.suggest(dedupe_key='kevin-2', separate=True, event_ids=[2], expires_what='the meeting with Kevin')['id']
        self.assertEqual(self.card(sid)['expires_at'], '2026-10-28T12:30:00+00:00')
        with at('2026-10-29T08:00:00+00:00'):
            self.store.expire_passed()
        self.assertTrue(a.expired_text(self.card(sid)).endswith('at 13:30.'))

    def test_a_moment_without_what_it_is_or_already_past_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'expires_what'):
            self.suggest(expires_at='2026-10-28T13:30:00+01:00')
        with self.assertRaisesRegex(ValueError, 'passed already'):
            self.suggest(expires_at='2026-10-27T13:30:00+01:00', expires_what='the meeting')
        with self.assertRaisesRegex(ValueError, 'ISO time'):
            self.suggest(expires_at='Wednesday', expires_what='the meeting')

    def test_a_send_on_its_way_settles_before_the_moment_closes_it(self):
        sid = self.suggest(expires_at='2026-10-28T13:30:00+01:00', expires_what='the meeting')['id']
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) VALUES('j1',?,'r','{}','sending',?,?,'a1','dashboard','<m@x>')",
                       (sid, '2026-10-28T12:00:00+00:00', '2026-10-28T12:00:00+00:00'))
        with at('2026-10-29T08:00:00+00:00'):
            self.assertEqual(self.store.expire_passed(), [])


class ReviewRules(unittest.TestCase):
    def test_the_review_knows_the_three_rules(self):
        agents = (ROOT / 'AGENTS.md').read_text()
        prompt = a.review_prompt('r1', ['g'])
        for text in (agents, prompt):
            self.assertRegex(text, r'in the calendar needs no to-do to confirm it')
            self.assertIn('expires_at', text)
            self.assertIn('never today, tomorrow or yesterday', text)
            self.assertNotIn('—', re.sub(r'.*?(Moments|Agreed meetings)', '', text, count=1, flags=re.S)[:900])


if __name__ == '__main__':
    unittest.main()
