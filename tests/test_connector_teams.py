"""Microsoft Teams (connectors/teams.py), faked at the Graph boundary: no live Microsoft calls. Every call still goes
through ms_graph.url_for, so only allowlisted GET methods with their right parameters pass. It reads chats with Chat.Read
alone, leaves out bots and Teams' own notices, keeps a cursor per chat, falls back from Copilot's notes to the
transcript to the meeting chat, says what's missing and why, and refuses a personal Microsoft account."""
import copy
import datetime as dt
import types
import unittest
from unittest import mock

import graph
import ms_graph
from connectors import teams
from machine.sources.connectors import CONNECTOR_HELPERS

OWNER = 'owner@acme.example'
ME, SAM, ROBIN = 'u-owner', 'u-sam', 'u-robin'
NOW = '2026-11-05T12:00:00+00:00'
CHAT_1 = '19:a1b2c3_d4e5@unq.gbl.spaces'
MEETING_CHAT = '19:meeting_abc123@thread.v2'
JOIN = 'https://teams.microsoft.com/l/meetup-join/19%3ameeting_abc123%40thread.v2/0'
ACCOUNT = {**teams.SETUP['account'], 'email': OWNER, 'boundary': 'work:Acme'}
OUTLOOK = {'id': 'acme-outlook', 'service': 'outlook', 'email': OWNER, 'transport': 'broker', 'boundary': 'work:Acme'}
CHAT_SCOPES = {'User.Read', 'Chat.Read'}
ALL_SCOPES = CHAT_SCOPES | set(teams.ADMIN_SCOPES)


def user(uid, name):
    return {'user': {'id': uid, 'displayName': name, 'userIdentityType': 'aadUser'}, 'application': None, 'device': None}


def message(mid, at, who=None, text='hi', kind='message', **more):
    return {'id': mid, 'messageType': kind, 'createdDateTime': at, 'lastModifiedDateTime': at, 'deletedDateTime': None,
            'from': who, 'body': {'contentType': 'html', 'content': text}, 'webUrl': f'https://teams.microsoft.com/l/message/{mid}', **more}


class FakeGraph:
    """Answers the Teams calls the connector makes, after url_for checked each one."""

    def __init__(self, granted=CHAT_SCOPES):
        self.granted, self.calls = set(granted), []
        self.chats = {
            CHAT_1: {'id': CHAT_1, 'chatType': 'oneOnOne', 'topic': None, 'webUrl': 'https://teams.microsoft.com/l/chat/' + CHAT_1,
                     'lastMessagePreview': {'createdDateTime': '2026-11-05T10:00:00Z'}},
            MEETING_CHAT: {'id': MEETING_CHAT, 'chatType': 'meeting', 'topic': 'Acme sync', 'webUrl': 'https://teams.microsoft.com/l/chat/m',
                           'onlineMeetingInfo': {'joinWebUrl': JOIN, 'organizer': {'id': ME}},
                           'lastMessagePreview': {'createdDateTime': '2026-11-05T09:30:00Z'}}}
        self.members = {CHAT_1: [(ME, 'Owner', OWNER), (SAM, 'Sam Sender', 'sam@partner.example')],
                        MEETING_CHAT: [(ME, 'Owner', OWNER), (SAM, 'Sam Sender', 'sam@partner.example'), (ROBIN, 'Robin Reviewer', 'robin@acme.example')]}
        self.messages = {
            CHAT_1: [message('m3', '2026-11-05T10:00:00Z', user(SAM, 'Sam Sender'), '<p>Can you send the <b>quote</b> today?</p>'),
                     message('m2', '2026-11-05T09:00:00Z', {'application': {'id': 'bot', 'displayName': 'Polly'}, 'user': None}, 'Vote now'),
                     message('m1', '2026-11-04T08:00:00Z', user(ME, 'Owner'), 'Morning Sam')],
            MEETING_CHAT: [message('e1', '2026-11-05T09:30:00Z', None, '<systemEventMessage/>', kind='systemEventMessage',
                                   eventDetail={'@odata.type': '#microsoft.graph.callEndedEventMessageDetail'}),
                           message('k1', '2026-11-05T09:10:00Z', user(ROBIN, 'Robin Reviewer'), 'Notes in the deck')]}
        self.fail = {}  # method -> status
        self.vtt = b'WEBVTT\n\n00:00:01.000 --> 00:00:04.000\n<v Robin Reviewer>We ship Friday.</v>\n\n00:00:05.000 --> 00:00:07.000\n<v Robin Reviewer>Sam sends the quote.</v>\n'
        self.insights = []
        self.joined, self.channels, self.channel_pages = [], {}, {}

    def scopes(self, config, credential, signin):
        return sorted(self.granted)

    def call(self, config, credential, signin, method, params=None, body=None, write=False, raw=False, **kw):
        assert not write and body is None
        verb, scope, url = ms_graph.url_for(method, params)  # the real allowlist: a wrong method or parameter fails here
        assert verb == 'GET', method
        self.calls.append((method, dict(params or {})))
        if method in self.fail:
            raise ms_graph.GraphError('graph_http', self.fail[method])
        if scope and scope not in self.granted and scope != 'User.Read':
            raise ms_graph.GraphError('microsoft_scope_not_granted', 403)
        p = params or {}
        if method == 'me':
            return {'id': ME, 'mail': OWNER, 'userPrincipalName': OWNER}
        if method == 'teams.chats':
            return {'value': [copy.deepcopy(c) for c in sorted(self.chats.values(), key=lambda c: c['lastMessagePreview']['createdDateTime'], reverse=True)]}
        if method == 'teams.chat':
            return copy.deepcopy(self.chats[p['chat']])
        if method == 'teams.chat.members':
            return {'value': [{'userId': u, 'displayName': n, 'email': e} for u, n, e in self.members[p['chat']]]}
        if method == 'teams.chat.messages':
            rows = self.messages.get(p['chat'], [])
            flt = p.get('$filter', '')
            if flt.startswith('lastModifiedDateTime gt '):
                since = flt.split(' gt ')[1]
                rows = [r for r in rows if r['lastModifiedDateTime'] > since.replace('.000Z', 'Z')]
            if flt.startswith('createdDateTime lt '):
                upper = flt.split(' lt ')[1]
                rows = [r for r in rows if r['createdDateTime'] < upper.replace('.000Z', 'Z')]
            return {'value': copy.deepcopy(rows)}
        if method == 'teams.meetings':
            assert p['$filter'] == f"JoinWebUrl eq '{JOIN}'"
            return {'value': [{'id': 'MSo-meeting-1', 'subject': 'Acme sync', 'startDateTime': '2026-11-05T09:00:00Z',
                               'endDateTime': '2026-11-05T09:30:00Z', 'participants': {'organizer': {'upn': OWNER, 'identity': {'user': {'id': ME}}}}}]}
        if method == 'teams.insights':
            assert p['user'] == ME
            return {'value': [{'id': i['id']} for i in self.insights]}
        if method == 'teams.insight':
            return copy.deepcopy(next(i for i in self.insights if i['id'] == p['insight']))
        if method == 'teams.transcripts':
            return {'value': [{'id': 't-1'}]}
        if method == 'teams.transcript.content':
            assert raw and p['$format'] == 'text/vtt'
            return self.vtt
        if method == 'teams.joined':
            return {'value': copy.deepcopy(self.joined)}
        if method == 'teams.channels':
            return {'value': copy.deepcopy(self.channels.get(p['team'], []))}
        if method == 'teams.channel.messages':
            pages = self.channel_pages.get(p['channel'], [])
            n = int(p['$link'].rsplit('=', 1)[1]) if p.get('$link') else 0
            out = {'value': copy.deepcopy(pages[n]) if n < len(pages) else []}
            if n + 1 < len(pages):
                out['@odata.nextLink'] = f"https://graph.microsoft.com/v1.0/teams/{p['team']}/channels/{p['channel']}/messages?$skiptoken={n + 1}"
            return out
        raise AssertionError('unexpected ' + method)


class Store:
    def __init__(self):
        self.state, self.events = {}, []

    def checkpoint(self, account_id):
        return copy.deepcopy(self.state)

    def commit_page(self, account_id, state, events, **kw):
        if state is not None:
            self.state = copy.deepcopy(state)
        self.events += events
        return len(events)


class TeamsTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeGraph()
        api = types.SimpleNamespace(READ=ms_graph.READ, GraphError=ms_graph.GraphError, personal=ms_graph.personal,
                                    identity=ms_graph.identity, call=self.fake.call, scopes=self.fake.scopes)
        self.patch = mock.patch.dict('sys.modules', {'ms_graph': api})
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.helpers = types.SimpleNamespace(**{**vars(CONNECTOR_HELPERS), 'now': lambda: self.now, 'credential': lambda config, name: 'x'})
        self.now = NOW
        self.config = {'accounts': [OUTLOOK, ACCOUNT], 'bootstrap_days': 7}
        self.store = Store()

    def sync(self):
        return teams.sync(self.store, self.config, ACCOUNT, self.helpers)

    def test_allowlisted_reads_only(self):
        for method, (verb, template, scope) in ms_graph.READ.items():
            if method.startswith('teams.'):
                self.assertEqual(verb, 'GET')
                self.assertNotIn(method, ms_graph.WRITE)
        # Graph writes a chat id unquoted in its next links; this module quotes it: both are the same path
        link = f'https://graph.microsoft.com/v1.0/chats/{CHAT_1}/messages?$skiptoken=abc'
        self.assertEqual(ms_graph.url_for('teams.chat.messages', {'chat': CHAT_1, '$link': link})[2], link)
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('teams.chat.messages', {'chat': CHAT_1, '$link': 'https://graph.microsoft.com/v1.0/chats/other/messages?x=1'})
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('teams.chat.messages', {'chat': CHAT_1, '$link': 'https://evil.example/v1.0/chats/' + CHAT_1 + '/messages'})

    def test_first_sync_reads_people_only(self):
        result = self.sync()
        texts = sorted(e['body'] for e in self.store.events)
        self.assertEqual(texts, ['Can you send the quote today?', 'Morning Sam', 'Notes in the deck'])  # no bot, no system notice
        sam = next(e for e in self.store.events if e['body'].startswith('Can you'))
        m = sam['metadata']
        self.assertEqual((sam['kind'], m['chat_id'], m['chat_kind'], m['from_email'], m['from_me']),
                         ('teams.message', CHAT_1, 'oneOnOne', 'sam@partner.example', False))
        self.assertEqual(m['to'], ['sam@partner.example'])
        self.assertTrue(m['source_url'].startswith('https://teams.microsoft.com/'))
        self.assertFalse(result['more'])
        self.assertEqual(self.store.state['missing'], {'channels': 'admin', 'transcripts': 'admin', 'notes': 'admin'})
        self.assertNotIn('queue', self.store.state)
        self.assertEqual(self.store.state['since'], NOW)
        # nothing outside Chat.Read was asked for
        self.assertFalse({c[0] for c in self.fake.calls} & {'teams.meetings', 'teams.joined', 'teams.transcripts', 'teams.insights'})

    def test_next_sync_reads_only_changes(self):
        self.sync()
        first = len(self.store.events)
        self.fake.messages[CHAT_1].insert(0, message('m4', '2026-11-05T12:30:00Z', user(SAM, 'Sam Sender'), 'Any news?'))
        self.fake.chats[CHAT_1]['lastMessagePreview']['createdDateTime'] = '2026-11-05T12:30:00Z'
        self.now = '2026-11-05T12:35:00+00:00'
        self.fake.calls.clear()
        self.sync()
        filters = [p['$filter'] for m, p in self.fake.calls if m == 'teams.chat.messages']
        self.assertEqual(filters, ['lastModifiedDateTime gt 2026-11-05T10:00:00.000Z'])  # the last pass less the overlap
        new = {e['body'] for e in self.store.events[first:]}
        self.assertIn('Any news?', new)
        self.assertNotIn('Morning Sam', new)

    def test_meeting_transcript_without_copilot_license(self):
        self.fake.granted = set(ALL_SCOPES)
        self.fake.fail['teams.insights'] = 403  # no Copilot license
        self.sync()
        transcript = [e for e in self.store.events if e['kind'] == 'teams.transcript']
        self.assertEqual(len(transcript), 1)
        self.assertEqual(transcript[0]['body'], 'Robin Reviewer: We ship Friday. Sam sends the quote.')
        self.assertEqual(transcript[0]['metadata']['host_email'], OWNER)
        self.assertEqual(transcript[0]['metadata']['start_at'], '2026-11-05T09:00:00+00:00')
        self.assertEqual(self.store.state['missing'], {'notes': 'license'})
        self.assertEqual(self.store.state['meetings'], [])  # done with it

    def test_copilot_notes_then_transcript_blocked(self):
        self.fake.granted = set(ALL_SCOPES)
        self.fake.insights = [{'id': 'ai-1', 'meetingNotes': [{'title': 'Pricing', 'text': 'Agreed on the annual plan.',
                                                               'subpoints': [{'title': 'Discount', 'text': 'None this year.'}]}],
                               'actionItems': [{'title': 'Send the quote', 'ownerDisplayName': 'Sam Sender'}]}]
        self.fake.fail['teams.transcripts'] = 403  # the organization turned transcript access off
        self.sync()
        notes = next(e for e in self.store.events if e['kind'] == 'teams.notes')
        self.assertIn('Agreed on the annual plan.', notes['body'])
        self.assertIn('Action items\n- Send the quote (Sam Sender)', notes['body'])
        self.assertEqual(notes['metadata']['next_steps'], ['Send the quote'])
        self.assertEqual(self.store.state['missing'], {'transcripts': 'blocked'})

    def test_meeting_waits_for_its_record_then_gives_up(self):
        self.fake.granted = CHAT_SCOPES | {'OnlineMeetings.Read', 'OnlineMeetingAiInsight.Read.All'}
        self.sync()  # Copilot hasn't made them yet
        self.assertEqual(len(self.store.state['meetings']), 1)
        self.now = '2026-11-08T12:00:00+00:00'  # past MEETING_DAYS: the meeting chat is what there is
        self.sync()
        self.assertEqual(self.store.state['meetings'], [])

    def test_personal_account_refused(self):
        account = {**ACCOUNT, 'email': 'someone@outlook.com'}
        self.config['accounts'] = [{**OUTLOOK, 'email': 'someone@outlook.com'}, account]
        with self.assertRaises(CONNECTOR_HELPERS.SourceError) as caught:
            teams.sync(self.store, self.config, account, self.helpers)
        self.assertEqual(caught.exception.category, 'teams_work_only')

    def test_without_chat_read_not_connected(self):
        self.fake.granted = {'User.Read', 'Mail.Read'}
        with self.assertRaises(CONNECTOR_HELPERS.SourceError) as caught:
            self.sync()
        self.assertEqual(caught.exception.category, 'teams_not_connected')

    def test_history_pages_back(self):
        state = {}
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, '2026-11-05T09:30:00+00:00', '2026-10-01T00:00:00+00:00')
        self.assertEqual((events, done), ([], False))
        self.assertEqual(state['chats'], [CHAT_1, MEETING_CHAT])
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, '2026-11-05T09:30:00+00:00', '2026-10-01T00:00:00+00:00')
        self.assertEqual([e['body'] for e in events], ['Morning Sam'])  # older than upper, no bot
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, '2026-11-05T09:30:00+00:00', '2026-10-01T00:00:00+00:00')
        self.assertEqual([e['body'] for e in events], ['Notes in the deck'])
        self.assertFalse(done)
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, '2026-11-05T09:30:00+00:00', '2026-10-01T00:00:00+00:00')
        self.assertEqual((events, done, state['channels']), ([], True, []))  # no admin OK: no channels, as the live sync
        self.assertNotIn('teams.joined', [m for m, _ in self.fake.calls])

    def test_history_reads_channel_threads_with_the_admins_ok_and_rests_on_throttling(self):
        self.fake.granted = set(ALL_SCOPES)
        self.fake.joined = [{'id': 'team-1', 'displayName': 'Acme'}]
        self.fake.channels = {'team-1': [{'id': 'chan-1', 'displayName': 'Sales', 'membershipType': 'standard'}]}
        reply = message('r1', '2026-09-02T10:00:00Z', user(ME, 'Owner'), 'On it')
        self.fake.channel_pages = {'chan-1': [
            [message('t1', '2026-11-05T08:00:00Z', user(SAM, 'Sam Sender'), 'Live week, not history'),
             {**message('t2', '2026-09-01T10:00:00Z', user(ROBIN, 'Robin Reviewer'), 'Q3 plan'), 'replies': [reply]}],
            [message('t3', '2026-08-01T10:00:00Z', user(SAM, 'Sam Sender'), 'Summer numbers')],
            [message('t4', '2025-01-01T10:00:00Z', user(SAM, 'Sam Sender'), 'Too old')]]}
        upper, target = '2026-10-29T09:00:00+00:00', '2025-11-05T09:00:00+00:00'
        state = {'chats': []}  # the chats are in (a Machine from before channel history goes on from here)
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, upper, target)
        self.assertEqual((events, done, state['channels']), ([], False, [['team-1', 'chan-1', 'Acme / Sales']]))
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, upper, target)
        self.assertEqual(([e['body'] for e in events], done), (['Q3 plan', 'On it'], False))
        self.assertEqual(events[0]['metadata']['chat_kind'], 'channel')
        self.fake.fail['teams.channel.messages'] = 429  # Graph throttles: the step raises, history rests, the link stays
        with self.assertRaises(CONNECTOR_HELPERS.SourceError) as caught:
            teams.history_page(self.config, ACCOUNT, self.helpers, state, upper, target)
        self.assertEqual(caught.exception.status, 429)
        self.assertTrue(state['link'].endswith('skiptoken=1'))
        del self.fake.fail['teams.channel.messages']
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, upper, target)
        self.assertEqual(([e['body'] for e in events], done), (['Summer numbers'], False))
        events, done = teams.history_page(self.config, ACCOUNT, self.helpers, state, upper, target)
        self.assertEqual((events, done), ([], True))  # a thread older than the target ends the channel

    def test_text(self):
        self.assertEqual(teams.html_text({'contentType': 'html', 'content': '<p>One&nbsp;two</p><p>three</p>'}), 'One two\n\nthree')
        self.assertIsNone(teams.teams_link('https://evil.example/l/chat/1'))

    def test_people_in_the_graph(self):
        owner = types.SimpleNamespace(mine=lambda a: a == OWNER, emails={OWNER})
        one = {'chat_kind': 'oneOnOne', 'from_email': 'sam@partner.example', 'from_me': False, 'to': ['sam@partner.example'], 'sender_display': 'Sam Sender'}
        self.assertEqual(graph._touches('teams.message', one, owner, set())[0][:2], ('email:sam@partner.example', 'Sam Sender'))
        mine = {**one, 'from_me': True, 'from_email': OWNER}
        self.assertEqual(graph._touches('teams.message', mine, owner, set())[0][0], 'email:sam@partner.example')
        channel = {'chat_kind': 'channel', 'from_email': 'robin@acme.example', 'from_me': False}
        self.assertEqual(graph._touches('teams.message', channel, owner, set())[0][2:], (0.05, 'seen'))


if __name__ == '__main__':
    unittest.main()
