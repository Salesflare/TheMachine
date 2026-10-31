"""A Slack member id ("U02AB3CD4") never reaches what people see or what the sharing decides on: a message's title names
the people in it ("#DM Robin Example-Smith: ..."), one whose name isn't known yet is left out and named once it is, the
title is written again in place without the message looking new or edited, and whether someone is outside the company's
own Slack (another company's member or a guest) comes from Slack itself, not from the id."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('slack_names_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
ACCOUNT = {'id': 'slack', 'service': 'slack', 'email': 'sam@acme.example', 'team_id': 'T0ACME0001', 'user_id': 'U0OWNER001',
           'slack_host': 'acme.slack.com'}
DM = {'id': 'D0ROBIN001', 'name': 'DM U0ROBIN001', 'type': 'dm'}
CHANNEL = {'id': 'C0GENERAL1', 'name': 'general', 'type': 'channel'}


def raw(ts, text, user='U0ROBIN001'):
    return {'ts': ts, 'text': text, 'user': user}


class FakeSlack:
    def __init__(self, users):
        self.account, self.users, self.calls = ACCOUNT, users, []

    def get(self, method, params):
        self.calls.append((method, params))
        assert method == 'users.info'
        return {'user': self.users[params['user']]}


class SlackNames(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def titles(self):
        with self.store.connect() as db:
            return {r['source_id']: (r['title'], r['version']) for r in db.execute("SELECT source_id,title,version FROM events")}

    def test_titles_name_people_and_never_show_a_member_id(self):
        names = {'U0ROBIN001': 'Robin Example-Smith', 'U0KIM00001': 'Kim Doe'}
        self.assertEqual(a.slack_event(ACCOUNT, DM, raw('1.000100', 'Ask <@U0KIM00001> about it'), names)['title'],
                         '#DM Robin Example-Smith: Ask @Kim Doe about it')
        unknown = a.slack_event(ACCOUNT, DM, raw('1.000100', 'Ask <@U0KIM00001> about it'), {})['title']
        self.assertEqual(unknown, '#DM: Ask @… about it')
        self.assertFalse(graph.SLACK_MEMBER.search(unknown))
        self.assertEqual(a.slack_event(ACCOUNT, CHANNEL, raw('2.000100', 'hi <@U0ROBIN001|robin>'), {})['title'], '#general: hi @robin')
        self.assertEqual(graph.slack_title_shown('#DM U0ROBIN001: ping U0NOBODY01', names), '#DM Robin Example-Smith: ping …')
        external = a.slack_event(ACCOUNT, {**DM, 'external': True}, raw('3.000100', 'hello'), names)
        self.assertIs(external['metadata']['slack_connect'], True)  # Slack Connect: kept on the message for the sharing
        self.assertNotIn('slack_connect', a.slack_event(ACCOUNT, DM, raw('3.000100', 'hello'), names)['metadata'])

    def test_a_name_learned_later_is_written_in_and_the_message_does_not_look_edited(self):
        old = a.slack_event(ACCOUNT, DM, raw('1.000100', 'Can you send it?'), {})
        old['title'] = '#DM U0ROBIN001: Can you send it?'  # as titles were stored before members were named
        self.store.commit_page('slack', {}, [old])
        source = FakeSlack({'U0ROBIN001': {'id': 'U0ROBIN001', 'team_id': 'T0ACME0001', 'profile': {'real_name': 'Robin Example-Smith',
                                                                                                    'email': 'robin@acme.example'}}})
        a.remember_slack_names(self.store, source, [old], [DM])
        self.assertEqual(self.titles(), {'D0ROBIN001:1.000100': ('#DM Robin Example-Smith: Can you send it?', 1)})
        again = a.slack_event(ACCOUNT, DM, raw('1.000100', 'Can you send it?'), {'U0ROBIN001': 'Robin Example-Smith'})
        self.store.commit_page('slack', {}, [again])  # read again (Slack's daily replay): the same message, no new version
        self.assertEqual(self.titles()['D0ROBIN001:1.000100'], ('#DM Robin Example-Smith: Can you send it?', 1))
        unnamed = a.slack_event(ACCOUNT, DM, raw('2.000100', 'And the other one'), {})
        self.store.commit_page('slack', {}, [unnamed])
        self.assertEqual(a.name_slack_titles(self.store, 'slack'), 1)
        self.assertEqual(self.titles()['D0ROBIN001:2.000100'], ('#DM Robin Example-Smith: And the other one', 1))

    def test_who_is_outside_the_company_slack_comes_from_slack(self):
        source = FakeSlack({'U0ROBIN001': {'id': 'U0ROBIN001', 'team_id': 'T0ACME0001', 'profile': {'real_name': 'Robin'}},
                            'U0GUEST001': {'id': 'U0GUEST001', 'team_id': 'T0ACME0001', 'is_restricted': True, 'profile': {'real_name': 'Gil'}},
                            'U0OTHER001': {'id': 'U0OTHER001', 'team_id': 'T0OTHER001', 'profile': {'real_name': 'Ola'}}})
        events = [a.slack_event(ACCOUNT, CHANNEL, raw(f'{n}.000100', 'hi', user)) for n, user in enumerate(source.users, 1)]
        a.remember_slack_names(self.store, source, events, [])
        with self.store.connect() as db:
            outside = dict(db.execute('SELECT user_id,outside FROM slack_members').fetchall())
        self.assertEqual(outside, {'U0ROBIN001': 0, 'U0GUEST001': 1, 'U0OTHER001': 1})
        a.remember_slack_names(self.store, source, events, [])
        self.assertEqual(len(source.calls), 3)  # once a month, like the names


if __name__ == '__main__':
    unittest.main()
