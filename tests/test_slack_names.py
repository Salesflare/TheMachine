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
        if params['user'] not in self.users:
            raise a.SourceError('slack_user_not_found:users.info')
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
        self.assertEqual(unknown, '#DM someone on Slack: Ask @someone on Slack about it')  # never blank, never the id
        self.assertFalse(graph.SLACK_MEMBER.search(unknown))
        self.assertEqual(a.slack_event(ACCOUNT, CHANNEL, raw('2.000100', 'hi <@U0ROBIN001|robin>'), {})['title'], '#general: hi @robin')
        self.assertEqual(graph.slack_title_shown('#DM U0ROBIN001: ping U0NOBODY01', names), '#DM Robin Example-Smith: ping someone on Slack')
        self.assertEqual(graph.slack_title_shown('#DM: hi', names), '#DM someone on Slack: hi')  # stored before, shown with words
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


    def test_apps_the_owner_and_former_members_are_named_too(self):
        """A DM with an app, the owner's own mentions and someone whose account is gone: a name to show for each, from
        Slack, never the id and never a blank "#DM: ..."."""
        bot_dm, gone_dm = {'id': 'D0BOT00001', 'name': 'DM U0BOT00001', 'type': 'dm'}, {'id': 'D0GONE0001', 'name': 'DM U0GONE0001', 'type': 'dm'}
        left_dm = {'id': 'D0LEFT0001', 'name': 'DM U0LEFT0001', 'type': 'dm'}
        events = [a.slack_event(ACCOUNT, bot_dm, raw('1.000100', 'Your report is ready for <@U0OWNER001>', 'U0BOT00001'), {}),
                  a.slack_event(ACCOUNT, gone_dm, raw('2.000100', 'See you around', 'U0GONE0001'), {}),
                  a.slack_event(ACCOUNT, left_dm, raw('3.000100', 'Bye all', 'U0LEFT0001'), {})]
        self.store.commit_page('slack', {}, events)
        self.assertTrue(all(t.startswith('#DM someone on Slack: ') for t, _ in self.titles().values()))
        source = FakeSlack({'U0BOT00001': {'id': 'U0BOT00001', 'is_bot': True, 'team_id': 'T0ACME0001', 'profile': {'real_name': 'Report Bot'}},
                            'U0OWNER001': {'id': 'U0OWNER001', 'team_id': 'T0ACME0001', 'profile': {'real_name': 'Sam Owner'}},
                            'U0LEFT0001': {'id': 'U0LEFT0001', 'deleted': True, 'team_id': 'T0ACME0001', 'profile': {}}})
        for _ in range(2):
            a.remember_slack_names(self.store, source, events, [bot_dm, gone_dm, left_dm])
        self.assertEqual(sorted(t for t, _ in self.titles().values()),
                         ['#DM Report Bot: Your report is ready for @Sam Owner', '#DM a former Slack user: Bye all', '#DM a former Slack user: See you around'])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM identity_names WHERE identifier IN ('slack:U0BOT00001','slack:U0OWNER001') AND name>''").fetchone()[0],
                             0)  # an app and the owner are no people in the graph
        calls = len(source.calls)
        a.remember_slack_names(self.store, source, events, [bot_dm, gone_dm, left_dm])
        self.assertEqual(len(source.calls), calls)  # each asked once, also the app and the one Slack no longer has

    def test_no_member_id_reaches_what_a_review_or_preparation_reads(self):
        """Event bodies, titles, earlier tool results and notes an agent reads: Slack members by name; ids it acts on stay."""
        with self.store.connect() as db:
            graph.ensure(db)
            db.execute("INSERT INTO identity_names(identifier,name,email,checked_at) VALUES('slack:U0ROBIN001','Robin Example-Smith',NULL,'2026-10-31')")
            graph.remember_slack_member(db, 'U0OWNER001', False, '2026-10-31', 'Sam Owner')
        msg = a.slack_event(ACCOUNT, DM, raw('1.000100', '<@U0OWNER001> can you ask <@U0KIM00001|kim> and <@U0NOBODY01>?'), {})
        self.store.commit_page('slack', {}, [msg])
        with self.store.connect() as db:
            rows = a.slack_named(db, [dict(r) for r in db.execute('SELECT * FROM events')])
            self.assertEqual(rows[0]['body'], '@Sam Owner can you ask @kim and @someone on Slack?')
            self.assertEqual(rows[0]['title'], '#DM Robin Example-Smith: @Sam Owner can you ask @kim and @someone on Slack?')
            out = a.slack_named_out(db, {'events': [{'id': 7, 'body': 'Ping <@U0ROBIN001>', 'metadata': json.dumps({'user_id': 'U0ROBIN001', 'channel_name': 'DM U0ROBIN001'})}],
                                         'note': 'yuri replied: #DM U0ROBIN001: done', 'evidence': [{'chat': 'DM U0ROBIN001', 'who': 'Slack teammate U0ROBIN001'}]})
        self.assertEqual(out['events'][0]['body'], 'Ping @Robin Example-Smith')
        self.assertEqual(json.loads(out['events'][0]['metadata']), {'user_id': 'U0ROBIN001', 'channel_name': 'DM Robin Example-Smith'})  # its id stays
        self.assertEqual(out['note'], 'yuri replied: #DM Robin Example-Smith: done')
        self.assertEqual(out['evidence'], [{'chat': 'DM Robin Example-Smith', 'who': 'Robin Example-Smith'}])
        shown = json.dumps({k: v for k, v in out.items() if k != 'events'}) + out['events'][0]['body']
        self.assertFalse(graph.SLACK_MEMBER.search(shown) or '<@' in shown, shown)


if __name__ == '__main__':
    unittest.main()
