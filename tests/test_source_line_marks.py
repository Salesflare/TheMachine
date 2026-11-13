"""A to-do's source line wears the icon of the message it names (views.source_marks, events-email.js cardViaIcon): a
"WhatsApp to Sam (+6 more)" with an email among the other messages once showed the email's mark. For every kind a
line can name, from every connector: the mark comes from that kind, never from another message on the to-do.
tests/test_source_line_marks_dashboard.mjs renders these to-dos and checks the icon each one shows."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant
from machine.sources.connectors import connector_services, load_connector
from machine.store.cards import SOURCE_KIND, line_head, source_lead, source_line
from machine.store.views import source_marks

AT, OLDER = '2026-11-12T09:00:00+00:00', '2026-11-05T09:00:00+00:00'
MAIL_URL = 'https://mail.google.com/mail/u/0/#all/abc123'


def named_kinds():
    """Every kind a source line can name: the built-in ones, every connector's, a routine's and a Fleet brief's."""
    kinds = set(SOURCE_KIND) | {'routine.cleanup', 'fleet.brief'}
    for service in connector_services():
        kinds |= set(getattr(load_connector(service), 'KINDS', None) or {})
    return sorted(kinds - {'owner.card', 'machine.parked_fix'})  # the owner's own words and an update's note: no line


def meta(kind):
    if kind == 'android.notification':
        return {'package_name': 'com.whatsapp', 'app_name': 'WhatsApp', 'sender_display': 'Robin Example'}
    if kind.startswith('routine.'):
        return {'sender_display': 'Spam cleanup'}
    return {'sender_display': 'Robin Example'}


def insert(db, account, kind, at, metadata):
    n = db.execute('SELECT count(*) FROM events').fetchone()[0]
    return db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,ingested_at) '
                      'VALUES(?,?,?,?,?,?,?,0,?,?)', (account, f'm{n}', kind, at, 'A message', 'Some text.',
                                                      json.dumps(metadata), f'h{n}', at)).lastrowid


def fixture(folder):
    """One to-do per named kind, its line naming that kind's message with an older Gmail email as "+1 more" (and a
    Gmail link among its originals), plus the reported case: the owner's own WhatsApp message with six others, one an
    email; and one whose evidence was reordered after its line was written. Returns (cards, connectors)."""
    store = assistant.Store(Path(folder) / 'events.sqlite')
    cards = []
    with store.connect() as db:
        for n, kind in enumerate(named_kinds()):
            lead = insert(db, f'a{n}', kind, AT, meta(kind))
            mail = insert(db, 'g1', 'gmail.message', OLDER, {'from': 'Sam Example <sam@example.com>', 'labels': ['INBOX']})
            rows = [dict(r) for r in db.execute('SELECT * FROM events WHERE id IN (?,?) ORDER BY id', (lead, mail))]
            cards.append({'id': f'k{n}', 'kind': kind, 'event_ids': json.dumps([lead, mail]), 'account_ids': [f'a{n}', 'g1'],
                          'original_urls': [MAIL_URL], 'source_line': source_line(rows, db)})
        # the owner's own WhatsApp message leads ("WhatsApp to Robin Example"), six more after it, one an email
        wa = insert(db, 'w1', 'whatsapp.message', AT, {'from_me': True, 'chat_name': 'Robin Example'})
        more = [insert(db, 'g1', 'gmail.message', OLDER, {'from': 'Robin Example <robin@example.com>', 'labels': ['INBOX']})]
        more += [insert(db, 'w1', 'whatsapp.message', f'2026-11-0{d}T09:00:00+00:00', {'chat_name': 'Robin Example'}) for d in range(1, 6)]
        ids = [wa, *more]
        rows = [dict(db.execute('SELECT * FROM events WHERE id=?', (i,)).fetchone()) for i in ids]
        cards.append({'id': 'owner-wa', 'kind': 'whatsapp.message', 'event_ids': json.dumps(ids), 'account_ids': ['g1', 'w1'],
                      'original_urls': [MAIL_URL], 'source_line': source_line(rows, db)})
        # its evidence reordered since (the email first now): the line still names the WhatsApp message
        cards.append({'id': 'reordered', 'kind': 'whatsapp.message', 'event_ids': json.dumps([more[0], wa, *more[1:]]),
                      'account_ids': ['g1', 'w1'], 'original_urls': [MAIL_URL], 'source_line': cards[-1]['source_line']})
        source_marks(db, cards)
    connectors = [{'id': 'g1', 'service': 'gmail'}, {'id': 'w1', 'service': 'whatsapp'}]
    return cards, connectors


def dump(folder):
    """{cards, connectors} for the dashboard test."""
    cards, connectors = fixture(folder)
    return json.dumps({'cards': cards, 'connectors': connectors})


class SourceLineMarks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cards, _ = fixture(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_every_named_kind_marks_the_message_its_line_names(self):
        for card in self.cards:
            with self.subTest(kind=card['kind'], card=card['id']):
                self.assertTrue(card['source_line'], 'every named kind writes a line')
                self.assertEqual(card['source_mark']['kind'], card['kind'], card['source_line'])

    def test_the_owners_whatsapp_message_with_an_email_among_the_rest(self):
        card = next(c for c in self.cards if c['id'] == 'owner-wa')
        self.assertRegex(card['source_line'], r'^Source: WhatsApp to Robin Example · .+ \(\+6 more\)$')
        self.assertEqual(card['source_mark'], {'kind': 'whatsapp.message', 'account_id': 'w1', 'app': None})
        self.assertEqual(next(c for c in self.cards if c['id'] == 'reordered')['source_mark']['kind'], 'whatsapp.message')

    def test_no_mark_when_no_message_fits_the_line(self):
        rows = [{'id': 1, 'kind': 'gmail.message', 'occurred_at': AT, 'metadata': '{}'}]
        self.assertIsNone(source_lead(rows, 'Source: WhatsApp to Robin · Thu 12 Nov'))
        # a whole word: a kind named "X" never fits a line about something else that starts with an X
        self.assertIsNone(source_lead([{'id': 1, 'kind': 'x.mention', 'occurred_at': AT, 'metadata': '{}'}], 'Source: Xero invoice · Thu 12 Nov'))
        self.assertEqual(line_head('x.dm'), 'X message')


if __name__ == '__main__':
    unittest.main()
