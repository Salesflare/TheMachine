"""The owner's own name (machine/owner_name.py): the hello, the digests and the status use one accessor. The config wins,
then USER.md's Name line, then the owner's own work mailbox; a company or a mailbox's name never greets anyone. A Machine
set up without owner_name greeted nobody though it knew the name. Made-up names."""
import datetime as dt
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from machine import owner_name
from machine.app import preparation
from machine.export import knowledge
import machine.main as machine_main
import notify
import own_addresses
import subscriptions
from subscriptions_app import SubscriptionsTemplate

NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
WORK = {'id': 'work', 'email': 'sam.rivera@acme.example', 'service': 'gmail', 'boundary': 'work:Acme'}


class OwnerNameTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'USER.md'
        self.config = {'accounts': [dict(WORK)], 'openclaw_workspace': self.temp.name}
        self.fresh()

    def user_md(self, text):
        self.path.write_text(text, encoding='utf-8')

    def fresh(self):
        for kept in (owner_name._mail, owner_name._kept):  # what a restart forgets
            kept.clear()

    def greets(self, line):
        self.user_md(f'# About me\n\n- Name: {line}\n')
        return owner_name.for_greeting(self.config)

    def app(self):
        app = object.__new__(machine_main.App)
        app.store, app.config_path, app.config = machine_main.Store(Path(self.temp.name) / 'events.sqlite'), None, self.config
        return app

    def mailbox(self, app, name, email='sam.rivera@acme.example'):
        self.config['accounts'] = [dict(WORK, email=email)]
        with app.store.connect() as db:
            own_addresses.save_fetched(db, 'work', [{'address': email, 'primary': True, 'alias': True, 'verified': True, 'name': name}], NOW.isoformat())
        self.fresh()
        return app.owner_full_name()

    def sent(self, app, *senders, labels=('SENT',), at=1):
        app.store.commit_page('work', {}, [{
            'account_id': 'work', 'source_id': f'{sender}{n}{at}{labels}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=n + at)).isoformat(),
            'title': 'Hello', 'body': 'Text', 'deleted': False, 'metadata': {'from': sender, 'to': 'kim@globex.example', 'labels': list(labels)}}
            for n, sender in enumerate(senders)])

    def test_the_title_of_a_long_lived_user_md_gives_the_name(self):
        for text, name in (('# USER.md - About Sam\n\nSam Rivera (born 1 January 1980), baker in Ghent.\n', 'Sam Rivera'),
                           ('# USER.md - About Sam\n**Sam Rivera**, baker.\n', 'Sam Rivera'),
                           ('# USER.md - About Sam\n\n- Sam Rivera Vale is a baker.\n', 'Sam Rivera Vale'),
                           ('# USER.md – About Sam\n\nSam lives in Ghent.\n', 'Sam'),
                           ('# USER.md - About Sam\n\nSam Rivera CEO of a bakery\n', 'Sam Rivera'),
                           ('# USER.md - About Sam\n\nKim Rivera is a baker.\n', 'Sam'),
                           ('# USER.md - About Sam\n\nSamuel Rivera is a baker.\n', 'Sam'),
                           ('# USER.md - About Sam\n\nSam Rivera Vale Lane Baker\n', 'Sam'),
                           ('# USER.md - About Sam\n\n## Work\n\nSam Rivera\n', 'Sam'),
                           ('# USER.md - About Sam\n', 'Sam'),
                           ('# About Sam Rivera\n\nBaker.\n', 'Sam Rivera'),
                           ('# USER.md - About Sam (owner)\n', 'Sam'),
                           ('# USER.md - User Model\n\n- Prefer ...\n\n# About Sam\n', 'Sam'),
                           ('# About Sam\n\n- Name: Robin Vale\n', 'Robin Vale'),  # its Name line goes first
                           ('# About Sam\n\n- Name: info\n', 'Sam')):
            self.user_md(text); self.fresh()
            self.assertEqual(owner_name.full_name(self.config), name, text)
            self.assertEqual(owner_name.for_greeting(self.config), name.split()[0])

    def test_a_title_about_anything_else_gives_none(self):
        for title in ('# About me', '# USER.md - About Me', '# USER.md - About you', '# About the team', '# About Our Family', '# About this file', '# About Acme',
                      '# USER.md - About Acme Support', '# About Vale BV', "# About Sam's Machine", '# About Sam and Kim', '# About CEO', '# USER.md - User Model',
                      '## About Sam', '# Notes\n\n# About Kim', '# About me\n\n- Name:\n\n# About Kim', '<!-- # About Sam -->'):
            self.user_md(title + '\n\nSome words.\n'); self.fresh()
            self.assertEqual(owner_name.for_greeting(self.config), '', title)

    def test_the_shapes_a_machine_has(self):
        import onboarding
        config = {**self.config, 'owner_name': 'Sam Rivera'}
        template = '# USER.md - User Model\n\n## Directives\n\n- Prefer ...\n\n'
        for text in (onboarding.starter_user_md(config), template + onboarding.starter_user_md(config),
                     '# USER.md - About Your Human\n\n- **Name:** Sam Rivera\n- **What to call them:**\n', '# USER.md - About Sam\n\nSam Rivera (born 1980), baker.\n'):
            self.user_md(text); self.fresh()
            self.assertEqual(owner_name.full_name(self.config), 'Sam Rivera', text)
        for text in (onboarding.starter_user_md(self.config), template, '# USER.md - About Your Human\n\n- **Name:**\n- **What to call them:**\n'):
            self.user_md(text); self.fresh()
            self.assertEqual(owner_name.full_name(self.config), '', text)

    def test_sent_mail_gives_the_name_gmails_list_leaves_out(self):
        app = self.app()
        self.sent(app, 'Sam Rivera <sam.rivera@acme.example>', '"Sam Rivera | Acme" <Sam.Rivera@acme.example>', 'Other Name <sam.rivera@acme.example>',
                  *['Kim Vale <kim@acme.example>'] * 4)
        self.assertEqual(self.mailbox(app, ''), 'Sam Rivera')
        with patch.object(owner_name, 'sent_name', side_effect=AssertionError('read again')):  # kept once found
            self.assertEqual(app.owner_full_name(), 'Sam Rivera')
        self.assertNotIn('The owner is', preparation.owner_details(self.config))  # greets, never signs

    def test_sent_mail_under_another_name_gives_none(self):
        app = self.app()
        self.sent(app, 'Sam Rivera <sam.rivera@acme.example>', labels=('INBOX',))  # a message to them, as anyone can write it
        self.assertEqual(self.mailbox(app, ''), '')
        self.sent(app, 'Acme Support <sam.rivera@acme.example>', 'Acme Support <sam.rivera@acme.example>', 'sam.rivera@acme.example', 'Sam <sam.rivera@acme.example>')
        self.assertEqual(self.mailbox(app, ''), '')
        self.sent(app, 'Sam Rivera <sam.rivera@gmail.com>', 'Sam Rivera <sam.rivera@gmail.com>', at=9)
        self.assertEqual(self.mailbox(app, '', 'sam.rivera@gmail.com'), '')

    def test_a_mailbox_without_a_name_is_not_read_on_every_status_poll(self):
        app = self.app()
        self.assertEqual(self.mailbox(app, ''), '')
        with patch.object(owner_name, 'sent_name', side_effect=lambda *a: '') as look:
            for _ in range(3):
                self.assertEqual(app.owner_full_name(), '')
            self.assertEqual(look.call_count, 0)
            with patch.object(owner_name.time, 'monotonic', return_value=owner_name.time.monotonic() + owner_name.LOOK_AGAIN + 1):
                app.owner_full_name(); app.owner_full_name()
            self.assertEqual(look.call_count, 1)

    def test_the_config_wins(self):
        self.config['owner_name'] = 'Robin  Vale'
        self.user_md('# About me\n\n- Name: Sam Rivera\n')
        self.assertEqual(owner_name.full_name(self.config), 'Robin Vale')
        self.assertEqual(owner_name.for_greeting(self.config), 'Robin')

    def test_without_it_user_md_gives_the_name(self):
        self.assertEqual(self.greets('Sam Rivera'), 'Sam')
        for text in ('# USER.md - User Model\n\n- **Name:** Sam Rivera\n', '# USER.md\n- **Name**: Sam Rivera\n* Role: baker',
                     '- Name: Sam Rivera', '# USER.md\n\n## About me\n- Name:  Sam   Rivera \n'):
            self.user_md(text)
            self.assertEqual(owner_name.full_name(self.config), 'Sam Rivera', text)

    def test_no_name_is_no_name(self):
        self.assertEqual(owner_name.full_name(self.config), '')  # no USER.md
        for text in ('', '# About me\n\n- Name: \n- Time zone: Europe/Brussels\n', '# About me\n\n- Name:\n- Role: Baker\n', '- Named: Sam Rivera\n',
                     '<!--\n- Name: Sam Rivera\n-->\n', '# About me\n\n## My sister\n\n- Name: Kim Rivera\n'):
            self.user_md(text)
            self.assertEqual(owner_name.full_name(self.config), '', text)
        self.path.write_bytes(b'\xff\xfe- Name: Sam')
        self.assertEqual(owner_name.full_name(self.config), '')

    def test_odd_names_never_greet(self):
        for line in ('info', 'Support', 'Sales Team', 'sam@acme.example', '(your name)', 'your name', '_unknown_', '12 Sam', 'Vale BV', 'Vale Bakery Ltd.',
                     'Acme', 'ACME', 'Acme Support', 'Ac-me'):
            self.assertEqual(self.greets(line), '', line)
        for line, first in (('Zoë', 'Zoë'), ('Łukasz Nowak', 'Łukasz'), ("D'Arcy Vale", "D'Arcy"), ('Jean-Luc Vale', 'Jean-Luc'), ('Dev Vale', 'Dev')):
            self.assertEqual(self.greets(line), first)
        self.assertEqual([notify.first_name(x) for x in ('info', 'Acme BV', 'Robin de Vries', None)], ['', '', 'Robin', ''])

    def test_a_company_is_told_from_someone_with_their_own_domain(self):
        self.config['accounts'] = [{'id': 'w', 'email': 'sam@samrivera.example'}, {'id': 'b', 'email': 'info@valebakery.example'}]
        self.assertEqual(self.greets('Sam Rivera'), 'Sam')
        self.assertEqual(self.greets('Vale Bakery'), '')
        self.config['accounts'] = [{'id': 'x', 'service': 'x', 'email': '@samrivera', 'boundary': 'work:Acme'}]  # their own handle
        self.assertEqual(self.greets('Sam Rivera'), 'Sam')
        self.config['accounts'] = [{'id': 'h', 'email': 'sam@gmail.com'}]  # a mail provider is nobody's company
        self.assertEqual(self.greets('Gmail'), 'Gmail')

    def test_an_owner_name_that_is_no_persons_gives_way_to_one_that_is(self):
        self.config['owner_name'] = 'info'
        self.assertEqual(owner_name.full_name(self.config), 'info')  # nothing better: as it was set
        self.assertEqual(owner_name.for_greeting(self.config), '')
        self.assertEqual(self.greets('Sam Rivera'), 'Sam')

    def test_it_is_read_again_only_when_the_file_changed(self):
        self.assertEqual(self.greets('Sam Rivera'), 'Sam')
        with patch.object(owner_name, 'open', side_effect=AssertionError('read again'), create=True):
            for _ in range(3):
                self.assertEqual(owner_name.for_greeting(self.config), 'Sam')
        stat = self.path.stat()
        self.user_md('# About me\n\n- Name: Kim Rivera\n')  # as long as before: the time alone tells
        os.utime(self.path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
        self.assertEqual(owner_name.for_greeting(self.config), 'Kim')
        self.path.unlink()
        self.assertEqual(owner_name.for_greeting(self.config), '')

    def test_the_work_mailboxs_own_name_comes_last_and_only_when_it_is_a_persons(self):
        app = self.app()
        self.assertEqual(self.mailbox(app, 'Sam Rivera'), 'Sam Rivera')
        self.assertEqual(self.mailbox(app, 'Sam Rivera', 'srivera@acme.example'), 'Sam Rivera')
        for name, email in (('Acme Support', 'support@acme.example'), ('Acme Bakery', 'acme@acmebakery.example'), ('Acme', 'acme@acme.example'),
                            ('', 'sam@acme.example'), ('Sam', 'sam@acme.example'), ('Vale Orders', 'sam@acme.example'), ('Blue Harbor', 'desk@acme.example'),
                            ('Vale Bakery', 'valebakery@gmail.com'), ('Sam Rivera', 'sam.rivera@gmail.com'), ('Info Desk', 'info@acme.example')):
            self.assertEqual(self.mailbox(app, name, email), '', (name, email))
        self.mailbox(app, 'Sam Rivera')
        self.config['accounts'][0]['shared'] = {'fleet': 'f'}  # a colleague's mailbox shared with them
        self.assertEqual(app.owner_full_name(), '')
        del self.config['accounts'][0]['shared']
        self.user_md('# About me\n\n- Name: Robin Rivera\n')
        self.assertEqual(app.owner_full_name(), 'Robin Rivera')

    def test_the_status_the_hello_and_the_digests_use_it(self):
        app = self.app()
        self.user_md('# About me\n\n- Name: Sam Rivera\n')
        before = self.path.read_bytes()
        names = []
        with patch.object(app.store, 'greeting', side_effect=lambda name: names.append(name)):
            self.assertEqual(app.action('status', {'full': True, 'done': 5})['first_name'], 'Sam')
        self.assertEqual(names, ['Sam Rivera'])
        for compose, digest in (('compose', app.digest), ('evening_compose', app.evening_digest)):
            with patch.object(notify, compose, return_value=None) as made:
                digest()
            self.assertEqual(made.call_args.kwargs['name'], 'Sam')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotIn('owner_name', self.config)

    def test_the_hello_never_says_a_mailboxs_name(self):
        app = self.app()
        with app.store.connect() as db:
            app.store.greeting('')
        self.assertEqual((app.store.greeting('Sam Rivera') or {}).get('name'), 'Sam')
        self.assertFalse((app.store.greeting('info') or {}).get('name'))

    def test_signing_uses_the_same_name_but_never_a_mailboxs(self):
        self.assertNotIn('The owner is', preparation.owner_details(self.config))
        self.user_md('# About me\n\n- Name: Sam Rivera\n- Role: Baker\n')
        self.assertIn('- The owner is Sam Rivera; sign emails with their first name.', preparation.owner_details(self.config))
        self.user_md('# About me\n\n- Name: Acme\n')
        self.assertNotIn('The owner is', preparation.owner_details(self.config))
        self.mailbox(self.app(), 'Sam Rivera')
        self.assertNotIn('The owner is', preparation.owner_details(self.config))
        self.config['owner_name'] = 'Dr. Robin Vale'  # as the config says it, also when no greeting would
        self.assertIn('- The owner is Dr. Robin Vale;', preparation.owner_details(self.config))
        self.assertEqual(knowledge.StoreReader(None, self.config).owner()['name'], 'Dr. Robin Vale')

    def test_the_cancel_draft_is_signed_with_it(self):
        row = {'name': 'Streamly', 'reply': 'help@streamly.example', 'link': ''}
        app = self.app()
        ask = lambda: app.action('subs_pick', {'suggestion_id': 's', 'item': 1, 'choice': 'cancel'}, owner_dashboard=True)['draft']['body']
        with patch.object(subscriptions, 'pick', return_value=row), patch.object(SubscriptionsTemplate, 'subs_rows', return_value=[]):
            self.assertTrue(ask().endswith('Thank you'))
            self.mailbox(app, 'Sam Rivera')  # a mailbox's name never signs
            self.assertTrue(ask().endswith('Thank you'))
            self.user_md('# About me\n\n- Name: Sam Rivera\n')
            self.assertTrue(ask().endswith('Thank you\nSam Rivera'))
            self.user_md('# About me\n\n- Name: Acme\n')
            self.assertTrue(ask().endswith('Thank you'))
            self.config['owner_name'] = 'Robin Vale'
            self.assertTrue(ask().endswith('Thank you\nRobin Vale'))


if __name__ == '__main__':
    unittest.main()
