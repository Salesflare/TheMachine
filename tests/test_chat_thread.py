"""A to-do's chat sources read as one clean thread (dashboard/events-email.js chatThreadHTML): event_views names each
chat message's conversation once (chat, and dm for a Slack direct message) and splits an Intercom conversation into its
turns. Email and other sources carry no chat fields and read as before. The dashboard test
(test_chat_thread_dashboard.mjs) reads its originals from fixture() here. All names and messages are made up."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('chat_thread_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

DAY = '2026-11-05T'
# An Intercom conversation as the connector stores it: the opening message, then "<unix time> · <author> · <type>: <text>"
INTERCOM_BODY = ('Hi! Our invoices show the old company address since the update.\n'
                 '1793876100 · Kit Navarro · comment: Thanks for flagging, checking it now.\n'
                 '1793876160 · Kit Navarro · assignment: \n'
                 '1793876520 · Kit Navarro · note: Billing team changed the template on Monday.\n'
                 '1793876880 · Juno Park · comment: Thanks. Can you resend the October one?\nWe need it for the books :pray:')


def fixture(folder):
    """Six to-dos: a Slack DM (the to-do's message first of five, with one from the owner), a WhatsApp group, one in
    that group from its links, a photo and a file (wamedia), a WhatsApp 1:1 (wa1on1), an
    Intercom conversation, and an email. Returns the app and each to-do's id."""
    store = a.Store(Path(folder) / 'events.sqlite')

    def slack(i, at, text, me=False):
        return {'account_id': 'work-slack', 'source_id': f'sl{i}', 'kind': 'slack.message', 'occurred_at': DAY + at + ':00+00:00',
                'title': '#DM Rowan Vale: ' + text.split('\n')[0], 'body': text, 'deleted': False,
                'metadata': {'channel_name': 'DM Rowan Vale', 'conversation_type': 'dm', 'channel_id': 'D0ROWAN', 'from_me': me,
                             'sender_display': '' if me else 'Rowan Vale', 'source_url': f'https://acme.slack.example/archives/D0ROWAN/p{i}'}}

    def whatsapp(i, at, who, text, media='', chat='Climbing crew'):
        return {'account_id': 'home-wa', 'source_id': f'wa{i}', 'kind': 'whatsapp.message', 'occurred_at': DAY + at + ':00+00:00',
                'title': chat, 'body': text, 'deleted': False,
                'metadata': {'chat_name': chat, 'chat_id': '1203@g.us' if chat == 'Climbing crew' else '3247@s.whatsapp.net', 'from_me': who == 'You', 'sender_display': who,
                             'from': who, 'media_type': media}}
    store.commit_page('work-slack', {}, [
        slack(1, '17:56', 'I just noticed we pay for the mail warmup tool with my personal credit card :upside_down_face:'),
        slack(2, '18:15', 'Could we move it to the company card asap?'),
        slack(3, '18:15', 'Also worth checking what it costs per month'),
        slack(4, '18:31', 'And whether we still need it :+1::skin-tone-3:'),
        slack(5, '18:40', 'Will look at it tomorrow morning.', me=True)], None)
    store.commit_page('home-wa', {}, [
        whatsapp(1, '08:02', 'Sasha Brook', 'Who is in for Saturday?'),
        whatsapp(2, '08:05', 'Milo Grant', 'Me! 10:00 at the usual wall?'),
        whatsapp(3, '08:06', 'Milo Grant', 'I can drive'),
        whatsapp(4, '08:30', 'You', 'Count me in'),
        whatsapp(5, '08:40', 'Milo Grant', 'Sent image', 'image'),
        whatsapp(6, '08:41', 'Milo Grant', 'The gear list', 'document'),
        whatsapp(7, '08:42', 'Sasha Brook', 'Chalk and tape from here:\nhttps://shop.example/nl/p/climbing-chalk-bag-large/9300001/\n'
                                            'https://www.shop.example/nl/p/finger-tape-roll-white/9300002/\nhttps://wall.example/routes/north'),
        whatsapp(8, '09:10', 'Robin Hale', 'Can you order this one?', chat='Robin Hale'),
        whatsapp(9, '09:11', 'Robin Hale', 'https://shop.example/p/oak-desk-lamp-with-dimmer/77/', chat='Robin Hale'),
        whatsapp(10, '09:20', 'You', 'Will do', chat='Robin Hale')], None)
    store.commit_page('work-intercom', {}, [{
        'account_id': 'work-intercom', 'source_id': '9101', 'kind': 'intercom.conversation', 'occurred_at': DAY + '11:08:00+00:00',
        'title': 'Hi! Our invoices show the old company address since the update.', 'body': INTERCOM_BODY, 'deleted': False,
        'metadata': {'conversation_id': '9101', 'from': 'juno@harbor.example', 'from_name': 'Juno Park', 'contact_name': 'Juno Park',
                     'created_at': 1793875800, 'source_url': 'https://app.intercom.example/a/inbox/w1/inbox/shared/all/conversation/9101'}}], None)
    store.commit_page('work', {}, [{
        'account_id': 'work', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': DAY + '09:10:00+00:00', 'title': 'Quote for the booth',
        'body': 'Hi,\n\nHere is the quote for the fair booth.\n\nBest,\nAvery', 'deleted': False,
        'metadata': {'from': 'Avery Stone <avery@booths.example>', 'to': 'owner@example.com'}}], None)
    with store.connect() as db:
        ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
    cards = {'slack': store.suggest('slack-card', 'Move the warmup tool billing to the company card', 'Rowan asked.',
                                    [ids['sl1'], ids['sl2'], ids['sl3'], ids['sl4'], ids['sl5']])['id'],
             'whatsapp': store.suggest('wa-card', 'Tell the climbing crew if you drive on Saturday', 'Milo offered.',
                                       [ids['wa2'], ids['wa1'], ids['wa3'], ids['wa4']])['id'],
             'wamedia': store.suggest('wa-media-card', 'Get the chalk and tape for Saturday', 'Sasha sent links.',
                                      [ids['wa7'], ids['wa5'], ids['wa6'], ids['wa4']])['id'],
             'wa1on1': store.suggest('wa-duo-card', 'Order the lamp Robin sent', 'Robin asked.', [ids['wa8'], ids['wa9'], ids['wa10']])['id'],
             'intercom': store.suggest('ic-card', 'Resend the October invoice to Harbor', 'Juno asked.', [ids['9101']])['id'],
             'email': store.suggest('mail-card', 'Reply to Avery about the booth quote', 'Avery sent a quote.', [ids['m1']])['id']}
    app = object.__new__(a.App)
    app.store = store
    app.config = {'accounts': [], 'database': str(Path(folder) / 'events.sqlite')}
    return app, cards


def dump(folder):
    """The originals per to-do, as JSON, for the dashboard test."""
    app, cards = fixture(folder)
    return json.dumps({k: {'id': sid, 'originals': app.originals(sid)} for k, sid in cards.items()})


class ChatThread(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.app, self.cards = fixture(temp.name)

    def test_a_slack_dm_names_its_conversation_once_per_message_by_the_other_person(self):
        items = self.app.originals(self.cards['slack'])
        self.assertEqual({(i['chat'], i['dm']) for i in items}, {('Rowan Vale', True)})
        self.assertEqual([i['from'] for i in items], ['Rowan Vale'] * 4 + ['You'])
        self.assertTrue(all('turns' not in i for i in items))

    def test_a_slack_channel_is_its_hash_name(self):
        self.assertEqual(a.chat_view('slack.message', {'channel_name': 'support', 'conversation_type': 'channel'}, 'x', DAY),
                         {'chat': '#support', 'dm': False})

    def test_whatsapp_names_its_chat(self):
        items = self.app.originals(self.cards['whatsapp'])
        self.assertEqual({i['chat'] for i in items}, {'Climbing crew'})
        self.assertNotIn('dm', items[0])

    def test_a_photo_or_file_says_what_it_is_and_its_placeholder_words_never_read_as_a_message(self):
        items = {i['body']: i for i in self.app.originals(self.cards['wamedia'])}
        self.assertEqual((items['Sent image']['media'], items['Sent image']['media_only']), ('photo', True))
        self.assertEqual(items['The gear list']['media'], 'file')
        self.assertNotIn('media_only', items['The gear list'])  # a caption reads under the chip
        self.assertNotIn('media', items['Count me in'])

    def test_media_by_source(self):
        from machine.store.message_view import media_shown as shown
        self.assertEqual(shown('telegram.message', {'media_type': 'photo'}, 'Sent a photo'), {'media': 'photo', 'media_only': True})
        self.assertEqual(shown('signal.message', {'media_type': 'audio'}, 'Sent audio'), {'media': 'audio', 'media_only': True})
        self.assertEqual(shown('whatsapp.message', {'media_type': 'video_note'}, 'Sent video note'), {'media': 'video', 'media_only': True})
        self.assertEqual(shown('whatsapp.message', {'media_type': 'ptt'}, 'Sent ptt'), {'media': 'voice', 'media_only': True})
        self.assertEqual(shown('slack.message', {'media_type': 'image'}, 'Sent image'), {})
        self.assertEqual(shown('whatsapp.message', {}, 'Sent image'), {})

    def test_an_intercom_conversation_is_its_turns_with_notes_marked_and_events_left_out(self):
        [item] = self.app.originals(self.cards['intercom'])
        self.assertEqual(item['chat'], 'Juno Park')
        self.assertEqual([(t['from'], t['body'], t.get('note', False)) for t in item['turns']], [
            ('Juno Park', 'Hi! Our invoices show the old company address since the update.', False),
            ('Kit Navarro', 'Thanks for flagging, checking it now.', False),
            ('Kit Navarro', 'Billing team changed the template on Monday.', True),
            ('Juno Park', 'Thanks. Can you resend the October one?\nWe need it for the books :pray:', False)])
        self.assertEqual(item['turns'][0]['occurred_at'], '2026-11-05T10:50:00+00:00')
        self.assertEqual(item['turns'][1]['occurred_at'], '2026-11-05T10:55:00+00:00')

    def test_an_intercom_message_without_history_is_one_message(self):
        self.assertEqual(a.chat_view('intercom.conversation', {'from_name': 'Juno Park'}, 'Just one question', DAY),
                         {'chat': 'Juno Park', 'turns': [{'from': 'Juno Park', 'role': 'customer', 'body': 'Just one question', 'occurred_at': DAY}]})

    def test_email_and_other_sources_carry_no_chat_fields(self):
        [item] = self.app.originals(self.cards['email'])
        self.assertNotIn('chat', item)
        self.assertEqual(a.chat_view('stripe.event', {}, 'x', DAY), {})


if __name__ == '__main__':
    unittest.main()

