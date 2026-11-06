"""A to-do whose draft or decision follows someone else's input in another message (a teammate's suggestion in a Slack
thread, another conversation) shows it on the to-do: "Based on Robin in #support · Wed", linking to that message. The
review (suggest) and the drafting step (prepare) name it with based_on; it joins the evidence after the main source."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('based_on_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


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
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'U0OWNER001'}
        self.app = object.__new__(a.App)
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
            a.based_on_views(db, cards)
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

    def test_the_review_and_the_drafting_step_are_told(self):
        self.assertIn('based_on', a.review_prompt('r1', ['sl']))
        self.assertIn('based_on', a.preparation_prompt({'job_id': 'j', 'suggestion_id': 's'}))
        self.assertIn('based_on', (a.ROOT / 'AGENTS.md').read_text())


if __name__ == '__main__':
    unittest.main()
