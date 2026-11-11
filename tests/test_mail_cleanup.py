"""Routine templates and mail cleanup (routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, docs/help/routines.md
"Templates"): Newsletter cleanup and Spam cleanup are added with one tap, run without a turn when there is nothing to
read, make at most one quiet to-do with a choice per item, and change nothing until the owner confirms there. Each
item is done only with what the Machine may already do: never a new permission. Made-up mail only; nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('cleanup_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import mail_cleanup as mc  # noqa: E402
import mail_cleanup_app  # noqa: E402
import routine_templates  # noqa: E402
import routines  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402
from machine.cards import controls  # noqa: E402

T = dt.datetime
ACCOUNTS = [{'id': 'w', 'email': 'owner@acme.example', 'boundary': 'work:acme.example'}]
SESSION = 'agent:main:assistant-review-routine-'


def stamp(hours_ago):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat()


class Headers(unittest.TestCase):
    def test_the_ways_a_list_offers(self):
        both = mc.unsubscribe_ways('<mailto:leave@news.example?subject=stop>, <https://news.example/u/abc>', 'List-Unsubscribe=One-Click')
        self.assertEqual(both['one_click'], 'https://news.example/u/abc')
        self.assertEqual(both['mailto'], {'to': 'leave@news.example', 'subject': 'stop', 'body': 'unsubscribe'})
        self.assertEqual(mc.unsubscribe_ways('<https://news.example/u/abc>'), {'link': 'https://news.example/u/abc'})  # no one-click without its header
        for bad in ('<http://news.example/u>', '<javascript:alert(1)>', '<https://user:pw@news.example/u>', 'https://news.example/u',
                    '<mailto:not-an-address>'):
            self.assertEqual(mc.unsubscribe_ways(bad, 'List-Unsubscribe=One-Click'), {}, bad)

    def test_one_click_goes_only_to_a_public_address(self):
        for address in ('127.0.0.1', '10.0.0.5', '169.254.169.254', '::1'):
            with patch('socket.getaddrinfo', return_value=[(None, None, None, None, (address, 443))]), \
                    patch.object(mail_cleanup_app, '_Pinned') as pinned:
                self.assertFalse(mail_cleanup_app.one_click('https://news.example/u'))
                pinned.assert_not_called()
        self.assertFalse(mail_cleanup_app.one_click('http://news.example/u'))


# A Google Group (made-up names): it rewrites From to the group's address and puts its own List-Id and List-Unsubscribe
# on the mail. That unsubscribe takes the owner, or the team, off the group: it is never used.
GROUP = {'from': "\"'Pat Shop' via hello@team.example readers\" <hello@team.example>",
         'x-original-from': 'Pat Shop <orders@shop.example>', 'x-original-sender': 'orders@shop.example',
         'reply-to': 'Pat Shop <orders@shop.example>', 'list-id': '<hello.team.example>',
         'list-unsubscribe': '<mailto:hello+unsubscribe@groups.example>, <https://groups.example/g/hello/unsubscribe>',
         'list-unsubscribe-post': 'List-Unsubscribe=One-Click'}


class Relayed(unittest.TestCase):
    def test_a_relayed_mail_is_its_original_senders(self):
        m = {'from': GROUP['from'], 'reply-to': GROUP['reply-to'], 'list_id': GROUP['list-id']}
        self.assertEqual(mc.relay_of(m), 'hello@team.example')  # mail stored before X-Original-From was kept
        self.assertEqual(mc.original_sender(m), ('Pat Shop', 'orders@shop.example'))
        self.assertEqual(mc.original_sender({'from': GROUP['from'], 'original_from': 'Pat Shop <orders@shop.example>'}), ('Pat Shop', 'orders@shop.example'))
        self.assertEqual(mc.original_sender({'from': GROUP['from']}), ('Pat Shop', ''))  # no address kept: nothing to unsubscribe from
        # not relayed: a newsletter, an announcement list sending its own mail, a site's "via" in a name
        for plain in ({'from': 'Weekly Digest <digest@blog.example>', 'list_id': '<digest.blog.example>'},
                      {'from': 'Jo via Network <invites@network.example>'},
                      {'from': 'Shop <news@shop.example>', 'reply-to': 'help@shop.example', 'list_id': '<abc.list-id.mailer.example>'}):
            self.assertEqual(mc.relay_of(plain), '', plain)

    def test_a_groups_own_unsubscribe_is_never_chosen(self):
        self.assertEqual(mc.unsubscribe_ways_of(GROUP), {})
        # every way a relay shows itself, alone, with only the group's unsubscribe: still none
        shapes = [{'from': GROUP['from']},
                  {'from': 'Hello <hello@team.example>', 'x-original-from': 'Pat Shop <orders@shop.example>'},
                  {'from': 'Hello <hello@team.example>', 'x-original-sender': 'orders@shop.example'},
                  {'from': "'Pat Shop' via Hello <hello@team.example>", 'list-id': '<hello.team.example>', 'reply-to': 'orders@shop.example'}]
        for shape in shapes:
            ways = mc.unsubscribe_ways_of({**shape, 'list-unsubscribe': GROUP['list-unsubscribe'], 'list-unsubscribe-post': GROUP['list-unsubscribe-post']})
            self.assertEqual(ways, {}, shape)
        # an item that came through the group: its ways are filtered by it, whatever the headers read now say
        group_ways = mc.unsubscribe_ways(GROUP['list-unsubscribe'], GROUP['list-unsubscribe-post'])
        self.assertEqual(set(group_ways), {'one_click', 'link', 'mailto'})
        self.assertEqual(mc.relay_ways(group_ways, 'orders@shop.example', 'hello@team.example'), {})
        self.assertEqual(mc.unsubscribe_ways_of({'list-unsubscribe': GROUP['list-unsubscribe']}, via='hello@team.example'), {})
        # the original sender's own unsubscribe, when the relayed mail carries it, is kept
        own = mc.unsubscribe_ways_of({**GROUP, 'list-unsubscribe': '<https://mail.shop.example/u/1>, <mailto:hello+unsubscribe@groups.example>'})
        self.assertEqual(own, {'one_click': 'https://mail.shop.example/u/1', 'link': 'https://mail.shop.example/u/1'})
        # mail the group did not relay keeps its list's ways
        self.assertEqual(mc.unsubscribe_ways_of({'from': 'Weekly Digest <digest@blog.example>', 'list-id': '<digest.blog.example>',
                                                 'list-unsubscribe': '<mailto:leave@blog.example>'})['mailto']['to'], 'leave@blog.example')


class Cleanup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']
        self.app.cleanup_inline = True
        self.now = T(2026, 11, 9, 6, 0)
        self.ways, self.marks, self.clicked, self.moved = {}, False, [], []
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.gateway(request)),
                            ('routine_spawn', lambda s, target, run_id: target(run_id)),
                            ('cleanup_headers', lambda s, account, message: self.ways.get(message, {})),
                            ('cleanup_can_send', lambda s, account: False),
                            ('cleanup_can_mark', lambda s, account: self.marks)):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(mail_cleanup_app, 'one_click', lambda url: self.clicked.append(url) or True); p.start(); self.addCleanup(p.stop)
        self.sent, self.n = [], 0
        self.asked, self.reply = [], '{"spam": []}'
        self.app.cleanup_spam_model = lambda prompt: self.asked.append(prompt) or self.reply  # the spam pass's one model call

    def gateway(self, request):
        self.sent.append(request)
        return {'start': {'status': 'admitted'}}.get(request['action'], {'status': 'pending'})

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def mail(self, sender, title, hours_ago=3, body='', account='w', synced=None, version=1, **metadata):
        """A made-up mail; synced: hours ago it came in (else when it was sent), version: 2 for one that changed since."""
        self.n += 1
        meta = {'from': sender, 'labels': ['INBOX'], 'thread_id': f't{self.n}',
                'source_url': f'https://mail.google.com/mail/u/?authuser=owner@acme.example#all/m{self.n}', **metadata}
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at,version) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (account, f'm{self.n}', 'gmail.message', stamp(hours_ago), title, body, json.dumps(meta), 'h',
                        stamp(hours_ago if synced is None else synced), version))
        return f'm{self.n}'

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'routine-cleanup:%' ORDER BY created_at")]

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routine_runs ORDER BY started_at')]

    def view(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            return row, self.store.suggestion_result(row, db)

    def add(self, key):
        out = self.act('routine_template', key=key)
        self.app.routines_step()
        return out

    def test_only_the_owner_adds_a_template_and_confirms(self):
        with self.assertRaises(ValueError):
            self.act('routine_template', owner=False, key='newsletters')
        with self.assertRaises(ValueError):
            self.act('routine_cleanup', owner=False, suggestion_id='x', picks={'0': 'go'})
        self.assertTrue({'routine_template', 'routine_cleanup'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)

    def test_newsletters_without_a_turn_one_todo_and_nothing_changes_before_the_confirm(self):
        first = self.mail('Daily Deals <deals@shop.example>', 'Flash sale on lamps', list_unsubscribe=True)
        self.mail('Daily Deals <deals@shop.example>', 'Last call on lamps', hours_ago=2, list_unsubscribe=True)
        self.ways[first] = {}  # its older one: not read
        second = self.mail('Weekly Digest <digest@blog.example>', 'Ten links for the weekend', list_id='digest.blog.example',
                           list_unsubscribe=True)
        self.mail('Sam Rivera <sam@partner.example>', 'Lunch Thursday?')  # a person, not a list
        self.mail('Page Only <hello@pageonly.example>', 'Spring news', list_unsubscribe=True)
        self.mail('Owner <owner@acme.example>', 'My own note', from_me=True, list_unsubscribe=True)
        self.ways.update({'m2': {'one_click': 'https://shop.example/u/1', 'link': 'https://shop.example/u/1'},
                          second: {'mailto': {'to': 'leave@blog.example', 'subject': 'unsubscribe', 'body': 'unsubscribe'}},
                          'm5': {'link': 'https://pageonly.example/leave'}})
        out = self.add('newsletters')
        self.assertEqual([t['added'] for t in out['templates'] if t['key'] == 'newsletters'], [True])
        self.assertEqual([s for s in self.sent if s['action'] == 'start'], [])  # plain code: no model turn
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]['title'], '2 newsletters: keep or unsubscribe?')  # the mailto one needs sending: left out
        row, extra = self.view(todos[0]['id'])
        items = extra['cleanup']['items']
        self.assertEqual([(i['address'], i['count'], i['state']) for i in items],
                         [('deals@shop.example', 2, 'open'), ('hello@pageonly.example', 1, 'open')])  # newest first
        self.assertEqual(self.runs()[0]['state'], 'ready')
        self.assertEqual(self.clicked, [])  # nothing done yet
        # its buttons: no Do it; the picks and their confirm are on the to-do
        shown = json.dumps(controls({**row, **extra, 'next_action': None}))
        self.assertNotIn('Do it', shown)
        self.assertIn('Not needed', shown)
        with self.assertRaises(ValueError):
            self.act('decide', suggestion_id=row['id'], choice='accept', decision_id='d1')
        # quiet: no buzz and no push
        with self.store.connect() as db:
            self.assertTrue(mc.is_cleanup(db, row['id']))
        # the owner unsubscribes from the deals and keeps the page-only one
        self.act('routine_cleanup', suggestion_id=row['id'], picks={'0': 'go', '1': 'keep'})
        self.assertEqual(self.clicked, ['https://shop.example/u/1'])
        row, extra = self.view(row['id'])
        self.assertEqual([i['state'] for i in extra['cleanup']['items']], ['done', 'kept'])
        self.assertEqual(row['status'], 'completed')  # every item settled
        # a sender the owner decided on is never asked about again
        self.mail('Daily Deals <deals@shop.example>', 'Lamps are back', hours_ago=1, list_unsubscribe=True)
        self.mail('Page Only <hello@pageonly.example>', 'Summer news', hours_ago=1, list_unsubscribe=True)
        with self.store.connect() as db:
            self.assertEqual({i['address'] for i in mc.newsletters(db, ['w'], stamp(5))}, {'digest@blog.example'})  # never asked: still found


    def test_mail_through_a_group_is_its_original_senders_and_never_unsubscribes_the_group(self):
        group = "\"'Pat Shop' via hello@team.example readers\" <hello@team.example>"
        for n, title in enumerate(('Order summary 1', 'Order summary 2')):
            self.mail(group, title, hours_ago=3 - n, list_unsubscribe=True, list_id='<hello.team.example>', precedence='list',
                      **{'reply-to': 'Pat Shop <orders@shop.example>'})
        self.mail("\"'Lee Lamps' via hello@team.example readers\" <hello@team.example>", 'Lamp news', hours_ago=1, list_unsubscribe=True,
                  list_id='<hello.team.example>', original_from='Lee Lamps <news@lamps.example>')
        self.mail("\"'Someone' via hello@team.example readers\" <hello@team.example>", 'Hi all', hours_ago=1, list_unsubscribe=True,
                  list_id='<hello.team.example>')  # the group kept no address of theirs: nothing to unsubscribe but the group
        with self.store.connect() as db:
            found = mc.newsletters(db, ['w'], stamp(5))
        self.assertEqual([(i['from'], i['address'], i['count'], i['via']) for i in found],
                         [('Lee Lamps', 'news@lamps.example', 1, 'hello@team.example'), ('Pat Shop', 'orders@shop.example', 2, 'hello@team.example')])
        # the headers read now are the group's own: no way left, so no row offers Unsubscribe
        self.app.cleanup_headers = lambda account, message: mc.unsubscribe_ways_of(GROUP)
        sends = []
        with patch.object(a.App, 'cleanup_can_send', lambda s, account: True), \
                patch.object(a.App, 'cleanup_mailto', lambda s, account, mailto: sends.append(mailto['to']) or 'done'):
            self.assertEqual(self.app.cleanup_ways(found), [])
            # even if the group's ways got through the header read, an item that came through it never uses them
            self.app.cleanup_headers = lambda account, message: mc.unsubscribe_ways(GROUP['list-unsubscribe'], GROUP['list-unsubscribe-post'])
            self.assertEqual(self.app.cleanup_ways(found), [])
            self.assertEqual(self.app.cleanup_unsubscribe(ACCOUNTS[0], found[1]), ('failed', None, None))
        self.assertEqual((self.clicked, sends), ([], []))

    def test_a_todo_made_before_still_never_unsubscribes_the_group(self):
        # a row from before this fix: the group's address, the group's mailto planned; the confirm reads the headers again
        with patch.object(mail_cleanup_app.Gmail, 'get', lambda s, resource, params=None: {'payload': {'headers': [
                {'name': k.title(), 'value': v} for k, v in GROUP.items()]}}), \
                patch.object(a.App, 'cleanup_headers', mail_cleanup_app.MailCleanupApp.cleanup_headers), \
                patch.object(a.App, 'cleanup_can_send', lambda s, account: True), \
                patch.object(a.App, 'cleanup_mailto', lambda s, account, mailto: self.fail('the group was asked to unsubscribe')):
            old = {'account': 'w', 'message': 'm9', 'address': 'hello@team.example', 'from': "'Pat Shop' via hello@team.example readers"}
            self.assertEqual(self.app.cleanup_unsubscribe(ACCOUNTS[0], old), ('failed', None, None))
        self.assertEqual(self.clicked, [])

    def test_what_the_review_sorted_as_a_notification_is_no_newsletter(self):
        self.mail('Payments <noreply@pay.example>', 'Money received', list_unsubscribe=True)
        self.mail('Weekly Digest <digest@blog.example>', 'Ten links', list_unsubscribe=True)
        self.mail('Payments <noreply@pay.example>', 'Spring offers', hours_ago=4, list_unsubscribe=True)
        claim = self.store.begin_analysis(['w'], 40)
        with self.store.connect() as db:
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
        self.assertTrue(next(v for v in claim['events'] if v['id'] == ids['m1']).get('list'))  # the review sees it is list mail
        self.store.finish_analysis(claim['analysis_id'], 'ok', reviewed_ids=list(ids.values()), read={'notifications': [ids['m1']]})
        with self.store.connect() as db:
            found = mc.newsletters(db, ['w'], stamp(5))
        # the receipt is left out; the same sender's promotion still counts, as its own newest mail
        self.assertEqual([(i['address'], i['title'], i['count']) for i in found],
                         [('digest@blog.example', 'Ten links', 1), ('noreply@pay.example', 'Spring offers', 1)])
        self.assertIn('{"notifications": [event_ids]}', a.review_prompt('r1', ['w']))  # asked of every batch, in the finish it makes anyway

    def test_a_page_only_unsubscribe_is_left_for_the_owner(self):
        self.mail('Page Only <hello@pageonly.example>', 'Spring news', list_unsubscribe=True)
        self.ways['m1'] = {'link': 'https://pageonly.example/leave'}
        self.add('newsletters')
        sid = self.todos()[0]['id']
        self.act('routine_cleanup', suggestion_id=sid, picks={'0': 'go'})
        row, extra = self.view(sid)
        self.assertEqual((extra['cleanup']['items'][0]['state'], extra['cleanup']['items'][0]['link']), ('yours', 'https://pageonly.example/leave'))
        self.assertNotEqual(row['status'], 'completed')  # the owner opens the page, then marks it done

    def test_no_newsletters_no_todo(self):
        self.mail('Sam Rivera <sam@partner.example>', 'Lunch Thursday?')
        self.add('newsletters')
        self.assertEqual(self.todos(), [])
        self.assertEqual(self.runs()[0]['state'], 'nothing')

    def test_the_result_counts_what_the_todos_list(self):
        # a long list in one area and a short one in another: each to-do saves, and the result adds up what they list
        self.app.config['accounts'].append({'id': 'p', 'email': 'owner@home.example', 'boundary': 'personal'})
        for n in range(21):
            self.mail(f'Sender Number {n} <news{n}@list{n}.example>', f'A rather long subject line for issue {n} of this list', account='p',
                      list_unsubscribe=True)
        for n in range(2):
            self.mail(f'Work List {n} <w{n}@work{n}.example>', f'Work digest {n}', list_unsubscribe=True)
        self.ways.update({f'm{n}': {'one_click': f'https://list.example/u/{n}'} for n in range(1, 24)})
        self.add('newsletters')
        todos = self.todos()
        self.assertEqual(sorted(t['title'] for t in todos), ['2 newsletters: keep or unsubscribe?', '21 newsletters: keep or unsubscribe?'])
        self.assertTrue(all(len(t['body']) <= mail_cleanup_app.BODY_MAX for t in todos))
        with self.store.connect() as db:
            self.assertEqual(sum(len(mc.items_of(db, t['id'])) for t in todos), 23)
        run = self.runs()[0]
        self.assertEqual((run['state'], run['result']), ('ready', 'Made 2 to-dos with 23 newsletters.'))

    def test_a_todo_that_doesnt_save_is_said_and_read_again(self):
        self.mail('Daily Deals <deals@shop.example>', 'Flash sale on lamps', list_unsubscribe=True)
        self.ways['m1'] = {'one_click': 'https://shop.example/u/1'}
        real = a.Store.suggest
        with patch.object(a.Store, 'suggest', lambda s, *x, **k: (_ for _ in ()).throw(ValueError('no'))):
            self.add('newsletters')
        self.assertEqual(self.todos(), [])
        run = self.runs()[0]
        self.assertEqual((run['state'], run['why']), ('failed', 'Couldn’t make the to-do. The next run tries again.'))
        with self.store.connect() as db:  # never "since" for the next run: it reads the same mail again
            self.assertIsNone(routines.last_run(db, run['routine_id']))
        self.assertEqual(a.Store.suggest, real)
        self.assertEqual(mail_cleanup_app.MailCleanupApp.cleanup_said('newsletters', 4, 1, 7),
                         'Made a to-do with 4 newsletters. Couldn’t put 7 more on a to-do. The next run tries again.')

    def test_adding_twice_keeps_one(self):
        self.marks = True
        rid = self.act('routine_template', key='spam')['made']
        self.assertEqual(self.act('routine_template', key='spam')['made'], rid)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM routines WHERE origin='template:spam'").fetchone()[0], 1)
        view = self.app.routines_view()
        self.assertEqual([(r['template'], r['edited']) for r in view['routines']], [('spam', False)])
        self.assertEqual(view['routines'][0]['instructions'], routine_templates.TEMPLATES['spam']['words'])  # its words, not what it does
        with self.assertRaises(ValueError):
            self.act('routine_template', key='nope')

    def rid(self, key):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM routines WHERE origin=?', ('template:' + key,)).fetchone()[0]

    def again(self, key):
        with self.store.connect() as db:
            routines.run_now(db, self.rid(key), self.app.routines_stamp())
        self.app.routines_step()

    def turns(self):
        return [s for s in self.sent if s['action'] == 'start']

    def test_a_rename_or_its_own_words_keep_the_templates_own_run(self):
        self.mail('Daily Deals <deals@shop.example>', 'Flash sale on lamps', list_unsubscribe=True)
        self.ways['m1'] = {'one_click': 'https://shop.example/u/1'}
        self.add('newsletters')
        rid = self.rid('newsletters')
        shown = self.app.routines_view()['routines'][0]['instructions']
        with patch.object(routine_templates.i18n, 't', lambda text, *a: 'NL ' + text if text in shown else text):  # as shown in Dutch
            dutch = routine_templates.words('newsletters')
            self.app.action('routine_edit', {'id': rid, 'words': '  ' + dutch + ' ', 'name': 'My newsletters'}, owner_dashboard=True)
        r = self.app.routines_view()['routines'][0]
        self.assertEqual((r['name'], r['edited'], r['instructions']), ('My newsletters', False, shown))
        self.again('newsletters')
        self.assertEqual(self.turns(), [])  # still plain code, no model
        # Try it of its own words: its own code, dry, what it would list
        self.mail('Weekly Digest <digest@blog.example>', 'Ten links', hours_ago=-0.01, list_id='digest.blog.example', list_unsubscribe=True)
        self.ways['m2'] = {'one_click': 'https://blog.example/u/2'}
        self.act('routine_try', id=rid, words=shown)
        self.app.routines_step()
        self.assertEqual(self.turns(), [])
        test = self.app.routines_view()['routines'][0]['test']
        self.assertEqual((test['state'], test['result']), ('ready', 'Found 1 newsletter.'))
        self.assertEqual(len(self.todos()), 1)  # only the first run's

    def test_new_words_run_as_a_routine_keep_the_cleanup_todo_and_go_back(self):
        self.add('newsletters')  # no mail yet: nothing
        rid = self.rid('newsletters')
        words = 'Find the newsletters since the last run, but never the ones about lamps. One to-do, Keep or Unsubscribe each.'
        self.act('routine_edit', id=rid, words=words)
        r = self.app.routines_view()
        self.assertEqual((r['routines'][0]['edited'], r['routines'][0]['instructions']), (True, words))
        self.assertEqual([t['added'] for t in r['templates'] if t['key'] == 'newsletters'], [True])  # still from the template
        self.mail('Daily Deals <deals@shop.example>', 'Flash sale on lamps', hours_ago=-0.01, list_unsubscribe=True)
        self.mail('Weekly Digest <digest@blog.example>', 'Ten links', hours_ago=-0.01, list_id='digest.blog.example', list_unsubscribe=True)
        self.ways.update({'m1': {'one_click': 'https://shop.example/u/1'}, 'm2': {'one_click': 'https://blog.example/u/2'}})
        self.again('newsletters')
        turn = self.turns()
        self.assertEqual(len(turn), 1)  # a normal routine's turn now, on its words, with the mail it may pick from
        self.assertIn(words, turn[0]['message'])
        self.assertIn('never send, post, reply, change or buy anything', turn[0]['message'])
        self.assertIn('digest@blog.example', turn[0]['message'])
        self.assertIn('cleanup: [{event_id', turn[0]['message'])
        with self.store.connect() as db:
            digest = db.execute("SELECT id FROM events WHERE source_id='m2'").fetchone()[0]
        run = next(r for r in self.runs() if r['state'] == 'running')
        self.act('routine_result', owner=False, _routine_session=SESSION + run['id'], text='One newsletter, lamps left out.',
                 cleanup=[{'event_id': digest, 'why': 'Weekly links'}, {'event_id': 999999, 'why': 'made up'}])
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        row, extra = self.view(todos[0]['id'])
        self.assertEqual([(i['address'], i['state']) for i in extra['cleanup']['items']], [('digest@blog.example', 'open')])
        self.assertEqual(self.clicked, [])  # nothing done before the owner confirms
        self.assertEqual(self.runs()[-1]['result'], 'One newsletter, lamps left out.')
        # Back to the template: its words, no script steps, its own code again
        self.act('routine_edit', id=rid, words=words, steps={'check': {'command': 'true'}})
        self.act('routine_edit', id=rid, back=True)
        r = self.app.routines_view()['routines'][0]
        self.assertEqual((r['edited'], r['instructions'], r['steps']), (False, routine_templates.TEMPLATES['newsletters']['words'], {}))
        self.again('newsletters')
        self.assertEqual(len(self.turns()), 1)  # no new turn
        with self.assertRaisesRegex(ValueError, 'isn’t from a template'):
            self.act('routine_edit', id=self.act('routine_new', words='every day at 9, sum up my deals')['made'], back=True)

    def test_edited_spam_cleanup_picks_only_from_what_it_was_shown(self):
        self.marks = True
        self.add('spam')
        rid = self.rid('spam')
        self.act('routine_edit', id=rid, words='Find cold pitches about SEO only. One to-do, Spam or Not spam each.')
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=-0.01, body='We noticed your site...')
        self.mail('Sam Rivera <sam@partner.example>', 'Re: the contract', hours_ago=-0.01, **{'in-reply-to': '<x@partner.example>'})
        self.again('spam')
        turn = self.turns()
        self.assertEqual(len(turn), 1)
        self.assertIn('Find cold pitches about SEO only', turn[0]['message'])
        self.assertIn('seo@ranks.example', turn[0]['message'])
        self.assertNotIn('sam@partner.example', turn[0]['message'])
        with self.store.connect() as db:
            seo, sam = [db.execute('SELECT id FROM events WHERE source_id=?', (m,)).fetchone()[0] for m in ('m1', 'm2')]
        run = next(r for r in self.runs() if r['state'] == 'running')
        self.act('routine_result', owner=False, _routine_session=SESSION + run['id'], text='One SEO pitch.',
                 cleanup=[{'event_id': seo, 'why': 'Cold SEO pitch'}, {'event_id': sam, 'why': 'not shown'}])
        row, extra = self.view(self.todos()[0]['id'])
        self.assertEqual([(i['address'], i['plan']) for i in extra['cleanup']['items']], [('seo@ranks.example', 'spam')])

    def test_spam_cleanup_only_where_mail_can_move_to_spam(self):
        # hosted Gmail reads only: no Spam cleanup to add, and one added before reads nothing and makes no to-do
        self.assertEqual([x['key'] for x in self.app.routines_view()['templates']], ['newsletters', 'birthdays'])
        with self.assertRaises(ValueError):
            self.act('routine_template', key='spam')
        self.marks = True
        self.app._cleanup_marks = None
        self.assertEqual([x['key'] for x in self.app.routines_view()['templates']], ['newsletters', 'spam', 'birthdays'])
        self.add('spam')
        self.marks = False
        self.app._cleanup_marks = None
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=-0.01)
        with self.store.connect() as db:
            rid = db.execute("SELECT id FROM routines WHERE origin='template:spam'").fetchone()[0]
            routines.run_now(db, rid, self.app.routines_stamp())
        self.app.routines_step()
        self.assertEqual([s for s in self.sent if s['action'] == 'start'], [])
        self.assertEqual(self.asked, [])
        self.assertEqual([r['state'] for r in self.runs()], ['nothing', 'nothing'])
        self.assertEqual(self.todos(), [])

    def test_spam_reads_only_unknown_senders_and_takes_only_what_it_read(self):
        self.marks = True
        self.add('spam')  # nothing to read: no model at all
        self.assertEqual((self.turns(), self.asked), ([], []))
        self.assertEqual(self.runs()[0]['state'], 'nothing')
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=-0.01, body='We noticed your site...')
        self.mail('Sam Rivera <sam@partner.example>', 'Re: the contract', hours_ago=-0.01, **{'in-reply-to': '<x@partner.example>'})
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
        self.reply = 'Here you go:\n```json\n' + json.dumps({'spam': [{'event_id': event, 'why': 'Cold SEO pitch'}, {'event_id': 999999, 'why': 'made up'}]}) + '\n```'
        self.again('spam')
        self.assertEqual(self.turns(), [])  # one model call, never an agent turn
        self.assertEqual(len(self.asked), 1)
        self.assertIn('seo@ranks.example', self.asked[0])
        self.assertNotIn('sam@partner.example', self.asked[0])
        todos = self.todos()
        self.assertEqual(len(todos), 1)
        row, extra = self.view(todos[0]['id'])
        self.assertEqual([(i['address'], i['why'], i['plan']) for i in extra['cleanup']['items']], [('seo@ranks.example', 'Cold SEO pitch', 'spam')])
        # the right taken away since: Spam didn't work, and nothing is left for the owner to do elsewhere
        self.marks = False
        self.act('routine_cleanup', suggestion_id=row['id'], picks={'0': 'go'})
        row, extra = self.view(row['id'])
        self.assertEqual(extra['cleanup']['items'][0]['state'], 'failed')
        self.assertNotIn('url', extra['cleanup']['items'][0])

    def at(self, hour, minute=0):
        """The owner's clock moves on, and the routines take a step."""
        self.now = T(2026, 11, 9, hour, minute)
        self.app.routines_step()

    def test_spam_cleanup_runs_every_hour_and_asks_the_model_only_about_new_mail_by_unknown_senders(self):
        self.marks = True
        self.add('spam')  # its first run now, at 6:00
        with self.store.connect() as db:
            row = routines.get(db, self.rid('spam'))
        self.assertEqual((json.loads(row['rule']), row['at'], row['next_due']), (routines.HOURLY, '07:30', '2026-11-09T06:30:00'))
        self.assertEqual(self.app.routines_view()['routines'][0]['rule'], {'unit': 'hour', 'n': 1})
        self.at(6, 20)
        self.assertEqual(len(self.runs()), 1)  # not before :30
        self.at(6, 30)
        self.assertEqual([(r['period'], r['state']) for r in self.runs()[1:]], [('2026-11-09T06:30', 'nothing')])
        self.at(6, 59)
        self.assertEqual(len(self.runs()), 2)  # once per hour
        self.mail('Sam Rivera <sam@partner.example>', 'Lunch Thursday?', hours_ago=0, from_me=True)  # the owner's own
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=0)
        self.at(7, 31)
        self.assertEqual(len(self.asked), 1)  # one small call, with only the new mail by an unknown sender
        self.assertIn('seo@ranks.example', self.asked[0])
        self.assertNotIn('sam@partner.example', self.asked[0])
        self.assertIn('Answer with JSON only', self.asked[0])
        self.at(8, 30)  # nothing new since: no model call
        self.at(9, 45)  # missed slots don't stack: the newest one runs, once
        self.assertEqual(len(self.asked), 1)
        self.assertEqual([r['period'] for r in self.runs()[2:]], ['2026-11-09T07:30', '2026-11-09T08:30', '2026-11-09T09:30'])
        self.assertEqual(self.turns(), [])  # never an agent turn
        # paused: no runs; resumed: from the next slot on, never what was missed
        self.act('routine_state', id=self.rid('spam'), to='pause')
        self.at(10, 30)
        self.assertEqual(len(self.runs()), 5)
        self.act('routine_state', id=self.rid('spam'), to='resume')
        self.at(11, 0)
        self.assertEqual(len(self.runs()), 5)
        self.at(11, 30)
        self.assertEqual(self.runs()[-1]['period'], '2026-11-09T11:30')

    def test_mail_that_synced_after_a_run_is_read_once_and_a_changed_one_is_not_read_again(self):
        self.marks = True
        self.add('spam')
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=0.1, synced=0)  # sent before that run, synced after
        self.mail('Lead Lists <sales@leads.example>', '10,000 verified leads', hours_ago=0.1, synced=0, version=2)  # seen then, only its labels changed
        self.mail('Old Pitch <hi@old.example>', 'Still interested?', hours_ago=2, synced=0)  # older than the sync lag
        self.at(6, 30)
        self.assertEqual(len(self.asked), 1)
        self.assertIn('seo@ranks.example', self.asked[0])
        self.assertNotIn('sales@leads.example', self.asked[0])
        self.assertNotIn('hi@old.example', self.asked[0])
        self.at(7, 30)
        self.assertEqual(len(self.asked), 1)  # read once

    def test_a_reply_that_is_no_answer_fails_and_the_next_run_reads_that_mail_again(self):
        self.marks = True
        self.add('spam')
        self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=0)
        self.reply = 'I could not decide.'
        self.at(6, 30)
        self.assertEqual((self.runs()[-1]['state'], self.runs()[-1]['error']), ('failed', 'no_result'))
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
        self.reply = json.dumps({'spam': [{'event_id': event, 'why': 'Cold SEO pitch'}]})
        self.at(7, 30)
        self.assertEqual(len(self.asked), 2)
        self.assertIn('seo@ranks.example', self.asked[1])
        self.assertEqual(self.runs()[-1]['state'], 'ready')
        self.assertEqual(len(self.todos()), 1)
        # the usage budget holds the model call, never the plain-code check
        self.mail('Lead Lists <sales@leads.example>', '10,000 verified leads', hours_ago=0)
        with patch.object(a.App, 'background_pause', lambda s, **k: {'window': 'budget'}):
            self.at(8, 30)
            self.assertEqual(len(self.asked), 2)
            self.assertEqual(self.runs()[-1]['state'], 'running')
        self.at(8, 31)
        self.assertEqual(len(self.asked), 3)
        self.assertEqual(self.runs()[-1]['state'], 'nothing')

    def spam_reply(self, *sources):
        with self.store.connect() as db:
            self.reply = json.dumps({'spam': [db.execute('SELECT id FROM events WHERE source_id=?', (s,)).fetchone()[0] for s in sources]})

    def test_an_open_spam_todo_gets_the_next_runs_spam_and_a_settled_one_a_fresh_todo(self):
        self.marks = True
        self.add('spam')  # its first run at 6:00: nothing yet
        first = self.mail('Growth Team <seo@ranks.example>', 'Page one on Google in 30 days', hours_ago=0)
        self.spam_reply(first)
        self.at(6, 30)
        [todo] = self.todos()
        with self.store.connect() as db:
            sent = [dict(r) for r in db.execute('SELECT * FROM deliveries WHERE suggestion_id=?', (todo['id'],))]
        second = self.mail('Lead Lists <sales@leads.example>', '10,000 verified leads', hours_ago=0)
        self.spam_reply(second)
        self.at(7, 30)
        self.assertEqual(len(self.asked), 2)
        self.assertEqual([t['id'] for t in self.todos()], [todo['id']])  # one to-do, not one per hour
        row, extra = self.view(todo['id'])
        self.assertEqual([(i['n'], i['address'], i['state']) for i in extra['cleanup']['items']],
                         [(0, 'seo@ranks.example', 'open'), (1, 'sales@leads.example', 'open')])
        self.assertEqual(row['title'], '2 emails look like spam')
        self.assertIn('10,000 verified leads', row['body'])
        self.assertLessEqual(len(row['body']), mail_cleanup_app.BODY_MAX)
        self.assertEqual(self.runs()[-1]['result'], 'Added 1 email that looks like spam to the open to-do.')
        with self.store.connect() as db:  # no new notification or push for an add
            self.assertEqual([dict(r) for r in db.execute('SELECT * FROM deliveries WHERE suggestion_id=?', (todo['id'],))], sent)
        with patch.object(a.next_actions.ThreadSnooze, 'write', lambda s, account, method, params, body: {}):
            self.act('routine_cleanup', suggestion_id=todo['id'], picks={'0': 'go', '1': 'keep'})
        self.assertEqual(self.view(todo['id'])[0]['status'], 'completed')
        third = self.mail('Offshore Devs <hello@devs.example>', 'Your app built for half', hours_ago=0)
        self.spam_reply(third)
        self.at(8, 30)
        todos = self.todos()
        self.assertEqual(len(todos), 2)  # settled: the next spam makes a fresh one
        _, extra = self.view(todos[-1]['id'])
        self.assertEqual([i['address'] for i in extra['cleanup']['items']], ['hello@devs.example'])

    def test_a_daily_spam_cleanup_from_before_runs_hourly_unless_the_owner_changed_when(self):
        with self.store.connect() as db:
            old = routines.create(db, routine_templates.TEMPLATES['spam']['words'], 'daily', self.now.date(), '07:30', self.now,
                                  self.app.routines_stamp(), name='Spam cleanup', origin='template:spam')
            mine = routines.create(db, 'Sum up my deals', 'daily', self.now.date(), '08:00', self.now, self.app.routines_stamp())
        self.app._spam_hourly = False
        self.at(6, 0)
        with self.store.connect() as db:
            rules = {r['id']: json.loads(r['rule']) for r in db.execute('SELECT id,rule FROM routines')}
        self.assertEqual((rules[old], rules[mine]), (routines.HOURLY, {'unit': 'day', 'n': 1}))
        self.assertTrue(routine_templates.own('template:spam', routine_templates.TEMPLATES['spam']['was'][0]))  # one added before it had words
        with self.store.connect() as db:
            db.execute("UPDATE routines SET rule=?,at='06:15' WHERE id=?", ('{"unit": "day", "n": 1}', old))
        self.app._spam_hourly = False
        self.at(6, 5)
        with self.store.connect() as db:
            self.assertEqual(json.loads(db.execute('SELECT rule FROM routines WHERE id=?', (old,)).fetchone()[0]), {'unit': 'day', 'n': 1})

    def test_spam_is_marked_where_the_machine_may(self):
        self.marks = True
        self.mail('Invoices <billing@fake-invoice.example>', 'Overdue invoice 4471')
        writes = []
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
        self.reply = json.dumps({'spam': [event]})
        with patch.object(a.next_actions.ThreadSnooze, 'write', lambda s, account, method, params, body: writes.append((method, params, body)) or {}):
            self.add('spam')
            sid = self.todos()[0]['id']
            self.act('routine_cleanup', suggestion_id=sid, picks={'0': 'go'})
        self.assertEqual(writes, [('gmail.users.threads.modify', {'userId': 'me', 'id': 't1'}, {'addLabelIds': ['SPAM'], 'removeLabelIds': ['INBOX']})])
        row, extra = self.view(sid)
        self.assertEqual((extra['cleanup']['items'][0]['state'], row['status']), ('done', 'completed'))

    def test_an_unknown_send_is_never_sent_again(self):
        self.mail('Weekly Digest <digest@blog.example>', 'Ten links', list_unsubscribe=True)
        self.ways['m1'] = {'mailto': {'to': 'leave@blog.example', 'subject': 'unsubscribe', 'body': 'unsubscribe'}}
        sends = []
        with patch.object(a.App, 'cleanup_can_send', lambda s, account: True), \
                patch.object(a.App, 'cleanup_mailto', lambda s, account, mailto: sends.append(mailto['to']) or 'unknown'):
            self.add('newsletters')
            sid = self.todos()[0]['id']
            self.act('routine_cleanup', suggestion_id=sid, picks={'0': 'go'})
            with self.assertRaises(ValueError):  # a second tap: settled, the to-do is done
                self.act('routine_cleanup', suggestion_id=sid, picks={'0': 'go'})
        self.assertEqual(sends, ['leave@blog.example'])
        _, extra = self.view(sid)
        self.assertEqual(extra['cleanup']['items'][0]['state'], 'unknown')


class Catalog(unittest.TestCase):
    def test_every_template_has_its_words(self):
        for key, template in routine_templates.TEMPLATES.items():
            self.assertEqual(routine_templates.key_of('template:' + key), key)
            self.assertTrue(template['name'] and template['what'] and template['words'])
            self.assertTrue(routine_templates.is_own(key, template['what']))  # one added before it had words
        self.assertIsNone(routine_templates.key_of('openclaw:abc'))


if __name__ == '__main__':
    unittest.main()
