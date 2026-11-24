"""A to-do whose draft or decision follows someone else's input in another message (a teammate's suggestion in a Slack
thread, another conversation) shows it on the to-do: "Based on Robin in #support · Wed", linking to that message. The
review (suggest) and the drafting step (prepare) name it with based_on; it joins the evidence after the main source."""
import json
import tempfile
import unittest
from pathlib import Path
import machine.app.preparation as machine_app_preparation
import machine.cards as machine_cards
import machine.main as machine_main
import machine.prompts.review as machine_prompts_review
import machine.store.cards as machine_store_cards
import machine.store.views as machine_store_views


def intercom():
    return {'account_id': 'ic', 'source_id': 'c1', 'kind': 'intercom.conversation', 'occurred_at': '2026-11-04T13:06:18+00:00',
            'title': 'Security report', 'body': 'I found a bug in the signup.', 'deleted': False,
            'metadata': {'from': 'reporter@example.com', 'from_name': 'Alex Reporter', 'conversation_id': 'c1'}}


def slack(ts, text, user, when, thread=None, channel='support', display=None):
    m = {'channel_id': 'C0SUPPORT1', 'channel_name': channel, 'conversation_type': 'channel', 'user_id': user,
         'message_ts': ts, 'source_url': f'https://acme.slack.com/archives/C0SUPPORT1/p{ts.replace(".", "")}'}
    if thread:
        m['thread_ts'] = thread
    if display:
        m['sender_display'] = display
    return {'account_id': 'sl', 'source_id': f'C0SUPPORT1:{ts}', 'kind': 'slack.message', 'occurred_at': when,
            'title': f'#{channel}: {text}', 'body': text, 'deleted': False, 'metadata': m}


class BasedOn(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'U0OWNER001'}
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'ic', 'service': 'intercom', 'boundary': 'work:Acme'},
                                        {'id': 'sl', 'service': 'slack', 'boundary': 'work:Acme'}], 'prepare_ahead': False}
        self.store.commit_page('ic', {}, [intercom()])
        self.store.commit_page('sl', {}, [
            slack('1793790256.828209', 'Report in, should we pay a bounty?', 'U0KIM00001', '2026-11-04T11:04:16+00:00', display='Kim Doe'),
            # the reply only carries the member id: the to-do names them, never "U0ROBIN001"
            slack('1793792264.759699', 'Lowest bounty is fine', 'U0ROBIN001', '2026-11-04T11:37:44+00:00', thread='1793790256.828209'),
            slack('1793792300.000100', 'Agreed', 'U0OWNER001', '2026-11-04T11:40:00+00:00', thread='1793790256.828209'),
        ])
        with self.store.connect() as db:
            db.execute("INSERT INTO identity_names(identifier,name,checked_at) VALUES('slack:U0ROBIN001','Robin Example','2026-11-04')")
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
        self.ticket, self.parent = self.ids['c1'], self.ids['C0SUPPORT1:1793790256.828209']
        self.reply, self.mine = self.ids['C0SUPPORT1:1793792264.759699'], self.ids['C0SUPPORT1:1793792300.000100']

    def suggest(self, **args):
        return self.app.action('suggest', {'dedupe_key': 'bounty', 'title': 'Offer the bounty', 'body': 'Offer the lowest bounty.',
                                           'when': 'now', 'event_ids': [self.ticket, self.parent], 'newer_checked': list(range(1, 50)), **args})

    def card(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def shown(self, sid):
        with self.store.connect() as db:
            cards = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())]
            machine_store_views.based_on_views(db, cards)
        return cards[0]

    def test_the_review_names_the_teammate_input_and_the_to_do_shows_it_by_name_with_its_link(self):
        sid = self.suggest(based_on=self.reply)['id']
        card = self.card(sid)
        self.assertEqual(card['based_on'], self.reply)
        self.assertEqual(json.loads(card['event_ids']), [self.ticket, self.parent, self.reply])  # Read message has it too
        self.assertTrue(card['source_line'].startswith('Source: Intercom from Alex Reporter'))  # the main source still leads
        view = self.shown(sid)['based_on']
        self.assertEqual(view['who'], 'Robin')
        self.assertEqual(view['where'], '#support')
        self.assertEqual(view['url'], 'https://acme.slack.com/archives/C0SUPPORT1/p1793792264759699')
        self.assertEqual(view['at'], '2026-11-04T11:37:44+00:00')
        self.assertNotIn('U0ROBIN001', json.dumps(view))

    def test_the_drafting_step_names_it_too(self):
        sid = self.suggest()['id']
        self.assertIsNone(self.shown(sid)['based_on'])
        self.store.decide(sid, 'accept', '', 'n1', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        self.app.action('prepare', {'suggestion_id': sid, 'job_id': job, 'body': 'Drafted the bounty offer.', 'outcome': 'needs_you',
                                    'needs': 'check the reply', 'based_on': self.reply})
        self.assertEqual(self.shown(sid)['based_on']['who'], 'Robin')
        self.assertEqual(json.loads(self.card(sid)['event_ids']).count(self.reply), 1)

    def later(self, text='Any news on the bounty?', ts='1793800000.000100', user='U0KIM00001'):
        self.store.commit_page('sl', {}, [slack(ts, text, user, '2026-11-04T15:00:00+00:00', thread='1793790256.828209', display='Kim Doe')])
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (f'C0SUPPORT1:{ts}',)).fetchone()[0]

    def drafted(self):
        """A to-do whose draft follows Robin's reply, as its run said."""
        sid = self.suggest()['id']
        self.store.decide(sid, 'accept', '', 'n1', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        self.app.action('prepare', {'suggestion_id': sid, 'job_id': job, 'body': 'Drafted the bounty offer.', 'outcome': 'needs_you',
                                    'needs': 'check the reply', 'based_on': self.reply})
        self.assertEqual(self.shown(sid)['based_on']['who'], 'Robin')
        return sid

    def test_a_new_message_that_replaces_the_result_takes_the_line_with_it(self):
        sid = self.drafted()
        news = self.later()
        self.suggest(card_id=sid, event_ids=[news], title='Answer Kim on the bounty', body='Kim asks for news on the bounty.')
        self.assertEqual(self.card(sid)['body'], 'Kim asks for news on the bounty.')
        self.assertIsNone(self.card(sid)['based_on'])  # "Based on Robin" was said about the draft that is gone
        self.assertIsNone(self.shown(sid)['based_on'])
        self.assertIn(self.reply, json.loads(self.card(sid)['event_ids']))  # still evidence, with Read message

    def test_an_update_that_names_its_own_input_shows_that_one(self):
        sid = self.drafted()
        news = self.later()
        self.suggest(card_id=sid, event_ids=[news], body='Kim asks for news: Robin says the lowest is fine.', based_on=self.reply)
        self.assertEqual(self.shown(sid)['based_on']['who'], 'Robin')

    def test_an_update_with_the_same_text_keeps_the_line(self):
        sid = self.drafted()
        news = self.later()
        self.suggest(card_id=sid, event_ids=[news], body='Drafted the bounty offer.')
        self.assertEqual(self.shown(sid)['based_on']['who'], 'Robin')

    def test_waiting_on_someone_after_it_drops_the_line(self):
        sid = self.drafted()
        news = self.later()
        self.suggest(card_id=sid, event_ids=[news], body='You asked Kim which bounty they want.', waiting_on='Kim to say which bounty')
        self.assertEqual(json.loads(self.card(sid)['outcome'])['state'], 'waiting')
        self.assertIsNone(self.card(sid)['based_on'])

    def test_what_settles_or_reads_the_result_keeps_the_line(self):
        sid = self.drafted()
        self.store.review_body(sid, 'Drafted the bounty offer.')
        self.store.decide(sid, 'complete', '', 'n2', 'dashboard')
        self.assertEqual(self.card(sid)['based_on'], self.reply)
        # A message kept on the done to-do is evidence only: the result it stood on is the same
        self.suggest(card_id=sid, event_ids=[self.later('Thanks!')], body='Kim said thanks.')
        self.assertEqual(self.card(sid)['based_on'], self.reply)

    def test_the_owners_own_to_do_keeps_the_line_of_a_draft_that_stays_ready(self):
        sid = self.drafted()
        for text, action, kept in (('Another text.', '{"kind":"email"}', True), ('A third text.', None, False)):
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET next_action=? WHERE id=?', (action, sid))
                card = db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone()
                evidence = [dict(db.execute('SELECT * FROM events WHERE id=?', (self.ticket,)).fetchone())]
                self.store.fill_owner_card(db, card, 'Offer the bounty', text, [self.ticket], ['ic'], evidence, None, False, None, [self.ticket])
            self.assertEqual((self.card(sid)['body'], self.card(sid)['based_on']), (text, self.reply if kept else None))

    def test_only_a_live_message_from_someone_else(self):
        for wrong in (self.mine, 999999, 'x', True):
            with self.assertRaises(ValueError):
                self.suggest(based_on=wrong)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)  # refused before saving

    def test_a_message_gone_since_is_left_out_and_an_unknown_member_is_never_an_id(self):
        sid = self.suggest(based_on=self.reply)['id']
        with self.store.connect() as db:
            db.execute("DELETE FROM identity_names")
        view = self.shown(sid)['based_on']
        self.assertIsNone(view['who'])  # "Based on a message in #support"
        self.assertNotIn('U0ROBIN001', json.dumps(view))
        with self.store.connect() as db:
            db.execute('UPDATE events SET deleted=1 WHERE id=?', (self.reply,))
        self.assertIsNone(self.shown(sid)['based_on'])

    def test_the_main_source_is_never_shown_twice(self):
        # The review named the to-do's own source: its source line already names that message, so no Based on line
        sid = self.suggest(event_ids=[self.reply], based_on=self.reply)['id']
        self.assertTrue(self.card(sid)['source_line'].startswith('Source: Slack from'))
        self.assertIsNone(self.shown(sid)['based_on'])
        # Another message in the evidence ("+1 more") still gets its line
        other = self.suggest(dedupe_key='other', event_ids=[self.parent, self.reply], based_on=self.reply)['id']
        self.assertEqual(self.shown(other)['based_on']['who'], 'Robin')

    def test_a_google_group_sender_reads_as_people_say_it(self):
        row = {'kind': 'gmail.message', 'occurred_at': '2026-11-06T09:00:00+00:00',
               'metadata': {'from': '"\'Zapier Alerts\' via info@acme.example readers" <info@acme.example>'}}
        self.assertEqual(machine_store_cards.source_text(row).split(' · ')[0], 'email from Zapier Alerts via info@acme.example')
        self.assertEqual(machine_cards.source_line_shown("Source: email from 'Zapier Alerts' via info@acme.example readers · Fri 6 Nov (+1 more)"),
                         'Source: email from Zapier Alerts via info@acme.example · Fri 6 Nov (+1 more)')  # stored before
        self.assertEqual(machine_cards.group_sender("'Sam Lee' via Sales"), 'Sam Lee via Sales')
        self.assertEqual(machine_store_views.sender_first_name(row['metadata']), 'Zapier')

    def test_the_review_and_the_drafting_step_are_told(self):
        self.assertIn('based_on', machine_prompts_review.review_prompt('r1', ['sl']))
        self.assertIn('based_on', machine_app_preparation.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'}))


if __name__ == '__main__':
    unittest.main()
