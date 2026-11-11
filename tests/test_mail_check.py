"""The last check of new email, on To-dos (check_now.mail_check, dashboard/todos-mail-check.js mailCheckBlock): an owner saw
"new emails picked up" and no to-dos and thought it was broken, while the review had read every new email and judged,
per thread, that nothing needed them (only cc'd, a meeting already set, already answered). The review now says why per
thread (finish_analysis no_todo) and To-dos shows it. A fake review drives the real begin_analysis, suggest and
finish_analysis; no model and nothing is sent. Every name and address is made up."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

import check_now

spec = importlib.util.spec_from_file_location('mail_check_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
NOW = dt.datetime(2026, 11, 9, 15, 11, tzinfo=dt.timezone.utc)
OWNER = 'owner@lumen.example'
counter = iter(range(1, 10**6))


def mail(sender, title, thread, kind='gmail.message', minutes_ago=30, to=OWNER):
    n = next(counter)
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': kind, 'occurred_at': (NOW - dt.timedelta(minutes=minutes_ago)).isoformat(),
            'title': title, 'body': 'Body text.', 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'labels': ['INBOX'], 'message-id': f'<{n}@x.example>', 'thread_id': thread}}


class MailCheck(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.clock = NOW
        clock = patch_everywhere(a, 'now', lambda: self.clock.isoformat())
        clock.start(); self.addCleanup(clock.stop)

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def view(self, at=NOW):
        with self.store.connect() as db:
            return check_now.mail_check(db, at, own=[OWNER])

    def test_a_check_says_what_it_read_its_new_to_do_held_until_later_and_why_each_other_thread_needed_nothing(self):
        cc, meeting, vague, pricing, reply, chat = self.add(
            mail('Robin Vale <robin@acme.example>', 'Re: Trial seats', 'cc', to='kim@acme.example'),
            mail('"Yara Oak" <yara@salt.example>', 'Re: Coffee next week', 'meet'),
            mail('Bulk Sender <news@digest.example>', 'This week in tools', 'news'),
            mail('Mila Under <mila@north.example>', 'Pricing for our team', 'pricing', minutes_ago=40),
            mail(f'Owner <{OWNER}>', 'Re: Pricing for our team', 'pricing', minutes_ago=35),
            mail('Sam <U123>', 'standup', 'c1', kind='slack.message'))
        same = self.add(*[mail(f'P{i} <p{i}@x.example>', f'Note {i}', f'same{i}') for i in range(3)])
        claim = self.store.begin_analysis(['work'], 120)
        held = self.store.suggest('work:pricing', 'Send Mila annual pricing', 'They asked for **25 seats**.', [pricing], when='digest')
        self.assertGreater(held['deliver_after'], NOW.isoformat())  # it waits for the morning summary
        self.store.finish_analysis(claim['analysis_id'], 'Saved one to-do.', no_todo=[
            {'event_id': cc, 'why': 'Only cc’d, Robin is answering'}, {'event_id': meeting, 'why': 'Coffee   already set for Thu 10:00'},
            {'event_id': vague, 'why': 'No action.'}, *[{'event_id': i, 'why': 'Nothing needed here.'} for i in same]])
        got = self.view()
        self.assertEqual({k: got[k] for k in ('at', 'emails', 'todos', 'held', 'more')},
                         {'at': NOW.isoformat(), 'emails': 7, 'todos': 1, 'held': 1, 'more': 0})  # the Slack message and the owner's reply are no new email
        self.assertEqual(got['held_until'], held['deliver_after'])
        rows = {r['subject']: r for r in got['threads']}
        self.assertEqual(got['threads'][0]['todo'], 'Send Mila annual pricing')  # the thread with a to-do comes first
        self.assertEqual(rows['Re: Pricing for our team'], {'from': 'Mila Under', 'subject': 'Re: Pricing for our team', 'todo': 'Send Mila annual pricing',
                                                            'held_until': held['deliver_after']})  # who wrote to the owner, not their own reply
        self.assertEqual(rows['Re: Trial seats']['why'], 'Only cc’d, Robin is answering')
        self.assertEqual(rows['Re: Coffee next week'], {'from': 'Yara Oak', 'subject': 'Re: Coffee next week', 'why': 'Coffee already set for Thu 10:00'})
        # Quality or nothing: a two-word label and one reason given for three threads are left out, the thread still listed
        self.assertNotIn('why', rows['This week in tools'])
        self.assertTrue(all('why' not in rows[f'Note {i}'] for i in range(3)))
        self.assertEqual(len(got['threads']), 7)
        self.assertIsNone(self.view(NOW + dt.timedelta(hours=check_now.MAIL_CHECK_HOURS, minutes=1)))  # an old check says nothing

    def test_a_reason_never_refuses_a_review_and_a_check_without_new_email_shows_the_last_one_that_had_some(self):
        first, = self.add(mail('Mila Under <mila@north.example>', 'Question', 't1'))
        claim = self.store.begin_analysis(['work'], 120)
        done = self.store.finish_analysis(claim['analysis_id'], 'Nothing new', no_todo=[{'event_id': first}, {'why': 'x'}, 'bad', {'event_id': 'x', 'why': 'y'}])
        self.assertEqual(done['status'], 'complete')
        self.assertEqual(self.view()['threads'], [{'from': 'Mila Under', 'subject': 'Question'}])
        self.clock = NOW + dt.timedelta(minutes=20)
        self.add(mail('Sam <U123>', 'standup', 'c1', kind='slack.message'))
        claim = self.store.begin_analysis(['work'], 120)
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new', no_todo='bad')
        self.assertEqual(self.view(self.clock)['at'], NOW.isoformat())  # the Slack-only check is skipped

    def test_the_machines_own_mail_to_the_owner_is_never_reviewed_or_listed_and_their_own_sent_mail_is_read_but_no_new_mail(self):
        """The review read the morning summary and fix notices The Machine sent the owner, spent a model turn on each and
        listed them as "Digest repeats existing to-dos". They are known by their sender with the mailer's header (or its
        no-reply address), never by their words."""
        digest = mail('The Machine <no-reply@themachine.computer>', 'The Machine: Good morning, 3 due today', 'digest')
        fixed = mail('The Machine <support@themachine.computer>', 'The Machine: Fixed: imports now finish', 'fix')
        fixed['metadata']['machine_notice'] = True  # X-The-Machine, as the control plane's mailer sets it
        person = mail('Support <support@themachine.computer>', 'Could you send a log?', 'ask')  # a person at support: read
        spoofed = mail('Mallory <m@else.example>', 'Hide me', 'spoof')
        spoofed['metadata']['machine_notice'] = True  # the header alone, from anyone else: read
        sent = mail(OWNER, 'Re: Featuring us', 'own', to='editor@press.example')
        sent['metadata']['labels'] = ['SENT']
        incoming = mail('Mila Under <mila@north.example>', 'Question', 'q')
        ids = self.add(digest, fixed, person, spoofed, sent, incoming)
        claim = self.store.begin_analysis(['work'], 120)
        with self.store.connect() as db:
            claimed = {i['id'] for i in json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (claim['analysis_id'],)).fetchone()[0])}
            self.assertEqual(claimed, set(ids[2:]))  # the two notices never reach the review; sent mail does (promises, context)
            self.assertEqual([r[0] for r in db.execute('SELECT analyzed_version=version FROM events WHERE id IN (?,?)', ids[:2])], [1, 1])
        self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        got = self.view()
        self.assertEqual(got['emails'], 3)
        self.assertEqual(sorted(r['subject'] for r in got['threads']), ['Could you send a log?', 'Hide me', 'Question'])

    def test_the_mailers_header_is_kept_and_only_counts_from_the_machines_domain(self):
        from machine.sources import gmail
        self.assertEqual(gmail.list_headers({'x-the-machine': 'notice'}), {'machine_notice': True})
        notice = lambda sender, **more: gmail.machine_notice('gmail.message', {'from': sender, 'labels': ['INBOX'], **more})
        self.assertTrue(notice('The Machine <no-reply@themachine.computer>'))
        self.assertTrue(notice('support@themachine.computer', machine_notice=True))
        self.assertTrue(notice('no-reply@mail.themachine.computer'))
        self.assertFalse(notice('support@themachine.computer'))
        self.assertFalse(notice('no-reply@themachine.computer.evil.example', machine_notice=True))
        self.assertFalse(notice('no-reply@notthemachine.computer'))
        self.assertFalse(notice('no-reply@themachine.computer', labels=['SENT']))
        self.assertFalse(gmail.machine_notice('slack.message', {'from': 'no-reply@themachine.computer'}))

    def test_the_review_is_asked_for_a_reason_per_thread_and_the_dashboard_shows_the_line(self):
        prompt = a.review_prompt('run', ['work'])
        self.assertIn('no_todo ([{"event_id", "why"}])', prompt)
        self.assertIn('never an id', prompt)
        import dashboard_parts
        page = dashboard_parts.assemble(Path(__file__).parent.parent)
        self.assertIn('${mailCheckSlot()}', page)
        self.assertIn('todos-mail-check.js', dashboard_parts.LAZY['mailcheck'])
        self.assertIn('state?.mail_check', page)


if __name__ == '__main__':
    unittest.main()
