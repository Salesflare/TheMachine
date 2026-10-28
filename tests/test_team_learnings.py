"""Learnings for The Machine team (team_learnings.py): at most once a day one turn distils what the Machine learned into a
few general learnings, the service strips anything personal, and the owner is asked. Nothing goes without their Send
on exactly what they saw; an error log only when ticked; sealed for the team's key and signed by a key for learnings
only, never the Machine's Network identity. The Network is a stand-in here: nothing is sent anywhere."""
import datetime as dt
import importlib.util
import json
import re
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import network_crypto as nc
import team_learnings as tl

PINNED = tl.TEAM_KEY_FINGERPRINT  # as shipped: empty until the team key is made, then its fingerprint

spec = importlib.util.spec_from_file_location('learnings_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

CASE = {'given': 'a first reply to a customer who has not heard of the owner yet', 'when': 'the owner opens the draft',
        'then': 'the draft says who the owner is before the ask'}
PERSONAL = ('Sam Lee', 'Globex', 'sam@globex.example', 'Office move', 'https://globex.example/deal', '+32 470 12 34 56')


class Network:
    """The Network's learnings route, as the control plane answers it: the team's public key, and what was sent."""
    def __init__(self, team=None):
        self.team = team or nc.new_keys()
        self.sent, self.fail = [], False

    def call(self, method, path, body=None, timeout=40):
        assert (method, path) == ('POST', '/learnings'), (method, path)
        if body['action'] == 'key':
            return {'keys': nc.public_keys(self.team)}
        if body['action'] == 'candidates':
            return {'candidates': getattr(self, 'candidates', [])}
        if self.fail:
            raise OSError('connection reset')
        self.sent.append(json.loads(json.dumps(body)))
        return {'ok': True}

    def opened(self, n=-1):
        body = self.sent[n]
        me = nc.check_keys(body['from'])['fingerprint']
        team = nc.check_keys(nc.public_keys(self.team))['fingerprint']
        return nc.open_sealed(body['sealed'], self.team, body['from'], {**tl.CONTEXT, 'f': me, 't': team, 'r': body['id']})


class TeamLearnings(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        database = Path(self.temp.name) / 'events.sqlite'
        self.store = a.Store(database)
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@globex.example', 'display_name': 'Owner Work'}]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'database': str(database), 'review_worker': {'enabled': True}}
        self.network = Network()
        pin = patch.object(tl, 'TEAM_KEY_FINGERPRINT', nc.check_keys(nc.public_keys(self.network.team))['fingerprint'])
        pin.start()
        self.addCleanup(pin.stop)
        self.app.fleet = types.SimpleNamespace(relay=types.SimpleNamespace(call=self.network.call))
        with self.store.connect() as db:
            for node, kind, name in (('email:sam@globex.example', 'person', 'Sam Lee'), ('org:globex.example', 'org', 'Globex'),
                                     ('project:1', 'project', 'Office move'), ('org:whatsapp.com', 'org', 'WhatsApp')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,1,'{}')", (node, kind, name))
            for i, note in enumerate(('Introduce yourself first, Sam Lee has never heard of us', 'Send it on WhatsApp instead',
                                      'Say who we are before the ask, they don’t know the context')):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) "
                           "VALUES(?,?,'Reply','','[]','[\"work\"]','done',?)", (f's{i}', f's{i}', a.now()))
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)",
                           (f'd{i}', f's{i}', 'other', note, 'dashboard', a.now()))
            db.execute("INSERT INTO faults(fingerprint,day,kind,frames,location,version,first_at,last_at,count,message) "
                       "VALUES('fp1',?,'KeyError','x','graph.py:120 build','abc',?,?,7,'missing key \"…\"')", (a.now()[:10], a.now(), a.now()))
            db.execute("INSERT INTO milestones(name,at) VALUES('first_card_shown',?)", (a.now(),))  # past the first look (background turns wait for it)

    fresh = True

    def distil(self, learnings):
        """One learnings run, as the turn does it: started by the service, read, saved, finished. A learning without
        use_cases gets the generic CASE, as the turn is asked to write one or more."""
        learnings = [{**item, 'use_cases': [CASE]} if isinstance(item, dict) and 'use_cases' not in item else item for item in learnings]
        run_id = self.store.learnings_due()
        self.assertTrue(run_id)
        session = a.PROFILE_SESSION_PREFIX + run_id
        page = self.store.profile_evidence(1, session)
        if self.fresh:
            self.assertEqual([f['fingerprint'] for f in page['faults']], ['fp1'])
        if self.fresh:  # the owner's own notes reach their own agent only; a later run reads only what is new
            self.assertIn('Send it on WhatsApp instead', json.dumps(page['rows']))
        def runner(request):
            if request['action'] == 'start':
                self.assertIn('Nothing personal', request['message'])
                self.assertIn('Judge by what the notes mean', request['message'])
                self.assertIn('use_cases: 1 to 3', request['message'])
                self.store.save_profile({'learnings': learnings}, session)
                return {'status': 'admitted'}
            return {'status': 'ok'}
        self.app.background_at = 0  # a week's learnings run: not spaced behind an earlier background turn here
        self.app.profile_step(runner)
        self.app.profile_step(runner)
        return self.app.learnings_view()['ask']

    def test_strip_takes_out_names_addresses_and_numbers_and_keeps_product_names(self):
        with self.store.connect() as db:
            names = tl.known_names(db, {'accounts': self.store.accounts})
        text, taken = tl.strip('Sam Lee at Globex wants the Office move update on WhatsApp: sam@globex.example, '
                               'https://globex.example/deal, +32 470 12 34 56, €1,200 by 2026-10-30. Sam said so.', names)
        for bit in PERSONAL + ('1,200', '2026-10-30', 'Sam'):
            self.assertNotIn(bit, text)
        self.assertIn('WhatsApp', text)  # what The Machine works with is the product, not a person
        self.assertEqual(text[:8], 'Someone ')
        self.assertEqual(tl.taken_line(taken), 'Took out an address, a link, a date, an amount, a number and 4 names.')
        # A single name only with its capital: "will" stays, "Will" the person doesn't
        self.assertEqual(tl.strip('It will help Will.', [('Will', 'person')])[0], 'It will help someone.')
        self.assertEqual(tl.strip('Drafts should introduce the context first.', names), ('Drafts should introduce the context first.', []))

    def test_a_week_of_notes_becomes_learnings_the_owner_reads_edits_and_sends_sealed(self):
        ask = self.distil([
            {'text': 'Drafts for people who don’t know Sam Lee or Globex yet should introduce the context first.',
             'example': 'A first email to a new supplier opens with who we are.', 'area': 'drafts'},
            {'text': 'People often switch a card’s channel to WhatsApp in chat; a button would save a step.', 'area': 'chat'},
            {'text': 'Graph updates fail now and then.', 'area': 'nonsense', 'fault': 'fp1'},
            {'text': 'short'}])  # too short to say anything: dropped
        self.assertEqual([i['n'] for i in ask['items']], [1, 2, 3])
        first, second, third = ask['items']
        self.assertNotIn('Sam', first['text'])
        self.assertNotIn('Globex', first['text'])
        self.assertEqual(first['taken'], 'Took out 2 names.')
        self.assertEqual((second['taken'], third['area']), ('', 'other'))
        self.assertIsNone(first['log'])
        self.assertIn('KeyError', third['log'])
        self.assertIn('graph.py:120', third['log'])
        self.assertEqual(self.network.sent, [])  # asked, never sent by itself
        self.assertIn('**For The Machine team**', a.weekly_recap_message(self.store, {'accounts': []})['text'])

        # An edit that puts a name back in is refused, so what goes is always what the owner saw
        with self.assertRaisesRegex(ValueError, 'take out a name first'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1, 'text': 'Sam Lee should be introduced.'}]}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 2}]})
        self.assertEqual(self.network.sent, [])

        # The owner keeps two (one edited), ticks the log on the third, and leaves the first out
        done = self.app.action('learnings_share', {'id': ask['id'], 'items': [
            {'n': 2, 'text': 'People often switch a card’s channel to WhatsApp in chat.', 'log': True},
            {'n': 3, 'log': True}]}, owner_dashboard=True)
        self.assertEqual((done['status'], done['count']), ('sent', 2))
        self.assertIsNone(done['team_learnings']['ask'])
        body = self.network.sent[0]
        wire = json.dumps(body)
        for bit in PERSONAL + ('WhatsApp in chat', 'KeyError', 'owner@'):
            self.assertNotIn(bit, wire)  # sealed: the Network sees none of it
        self.assertFalse(body['named'])
        opened = self.network.opened()
        self.assertEqual([i['text'] for i in opened['items']],
                         ['People often switch a card’s channel to WhatsApp in chat.', 'Graph updates fail now and then.'])
        self.assertNotIn('log', opened['items'][0])  # it had none: a tick can't make one up
        self.assertIn('KeyError', opened['items'][1]['log'])
        # Signed with a key for learnings only, not the Machine's Network identity
        self.assertTrue((Path(self.temp.name) / 'learnings-keys.json').exists())
        self.assertFalse((Path(self.temp.name) / 'network-keys.json').exists())
        with self.assertRaisesRegex(ValueError, 'no longer waiting'):  # once
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 2}]}, owner_dashboard=True)
        self.assertEqual(self.app.learnings_view()['last_shared']['count'], 2)

    def test_logs_stay_home_unless_ticked_and_a_failed_send_keeps_the_batch(self):
        ask = self.distil([{'text': 'Graph updates fail now and then on a busy day.', 'fault': 'fp1'}])
        self.network.fail = True
        with self.assertRaisesRegex(ValueError, 'not confirmed'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}]}, owner_dashboard=True)
        again = self.app.learnings_view()['ask']
        self.assertEqual((again['id'], again['error']), (ask['id'], 'delivery_unknown'))
        self.network.fail = False
        self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}]}, owner_dashboard=True)
        self.assertNotIn('log', self.network.opened()['items'][0])
        self.assertFalse(self.network.sent[0]['named'])  # retry the same choice, not a new disclosure

    def test_another_team_key_than_the_pinned_one_sends_nothing(self):
        ask = self.distil([{'text': 'Cards about invoices should show the due date first.'}])
        self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}]}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute("UPDATE profile_runs SET started_at='2000-01-01' WHERE kind='learnings'")
            db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('a','d0',?),('b','d1',?),('c','d2',?)", (a.now(),) * 3)
        self.network.team = nc.new_keys()  # the Network hands out another key than the one pinned in the code
        ask = self.distil([{'text': 'Cards about invoices should show the amount first.'}])
        with self.assertRaisesRegex(ValueError, 'isn’t the team’s key'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}]}, owner_dashboard=True)
        self.assertEqual(len(self.network.sent), 1)

    def test_until_the_team_key_is_pinned_no_one_is_asked(self):
        with patch.object(tl, 'TEAM_KEY_FINGERPRINT', ''):
            self.assertIsNone(self.store.learnings_due())
            self.assertFalse(self.app.learnings_view()['network'])  # no card, no Settings switch
        self.assertRegex(tl.TEAM_KEY_FINGERPRINT, r'^([0-9a-f]{4} ){5}[0-9a-f]{4}$')  # the test's pin, in the form keygen prints
        self.assertTrue(PINNED == '' or re.fullmatch(r'([0-9a-f]{4} ){5}[0-9a-f]{4}', PINNED), PINNED)

    def test_not_now_never_ask_and_the_settings_switch(self):
        ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}])
        self.assertEqual(self.app.action('learnings_later', {'id': ask['id']}, owner_dashboard=True)['team_learnings']['ask'], None)
        self.assertIsNone(self.store.learnings_due())  # not again within the week
        with patch.object(a, 'now', return_value=(a.dt.datetime.fromisoformat(a.now()) + a.dt.timedelta(days=8)).isoformat()):
            with self.store.connect() as db:
                db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('a','d0',?),('b','d1',?),('c','d2',?)", (a.now(),) * 3)
            self.fresh = False  # the error was more than a week ago
            ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first, again.'}])
            self.assertEqual(self.store.learnings_due(), None)  # one waits for the owner: no second one meanwhile
            view = self.app.action('learnings_never', {'id': ask['id']}, owner_dashboard=True)['team_learnings']
            self.assertEqual((view['offer'], view['ask']), (False, None))
        with patch.object(a, 'now', return_value=(a.dt.datetime.fromisoformat(a.now()) + a.dt.timedelta(days=30)).isoformat()):
            self.assertIsNone(self.store.learnings_due())  # Never ask: no run at all
            with self.store.connect() as db:
                db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('d','d0',?),('e','d1',?),('f','d2',?)", (a.now(),) * 3)
            self.assertIsNone(self.store.learnings_due())
            self.assertTrue(self.app.action('set_learnings_offer', {'on': True}, owner_dashboard=True)['team_learnings']['offer'])
            self.assertTrue(self.store.learnings_due())
        self.assertEqual(self.network.sent, [])
        self.assertTrue(a.LEARNING_ACTIONS <= a.OWNER_ACTIONS)

    def test_no_network_no_offer(self):
        self.app.fleet = None
        self.assertEqual(self.app.learnings_view()['network'], False)
        with self.assertRaisesRegex(ValueError, 'needs The Machine Network'):
            self.app.action('learnings_share', {'id': 'x', 'items': [{'n': 1}]}, owner_dashboard=True)
        with patch.object(self.store, 'learnings_due') as due:
            self.app.style_step()
        due.assert_not_called()

    def test_uncertain_send_retries_the_saved_proposal_not_new_edits(self):
        ask = self.distil([{'text': 'Drafts should introduce the context first.'}])
        chosen = [{'n': 1, 'text': 'Drafts should introduce the context first.'}]
        original = self.network.call
        failed = False
        def accepted_then_disconnected(method, path, body=None, timeout=40):
            nonlocal failed
            if body['action'] == 'send':
                if self.network.sent:
                    return {'ok': True}  # the real relay takes a batch id only once
                reply = original(method, path, body, timeout)
                if not failed:
                    failed = True
                    raise OSError('response lost after commit')
                return reply
            return original(method, path, body, timeout)
        self.app.fleet.relay.call = accepted_then_disconnected
        with self.assertRaises(ValueError):
            self.app.action('learnings_share', {'id': ask['id'], 'items': chosen, 'named': True}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'same items'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1, 'text': 'A different suggestion instead.'}], 'named': True}, owner_dashboard=True)
        pending = self.app.learnings_view()['ask']
        self.assertEqual(pending['pending']['items'], chosen)
        self.assertTrue(pending['pending']['named'])
        result = self.app.action('learnings_share', {'id': ask['id'], 'items': chosen, 'named': True}, owner_dashboard=True)
        self.assertEqual(result['count'], 1)
        with self.store.connect() as db:
            record = json.loads(db.execute('SELECT sent FROM team_learnings WHERE id=?', (ask['id'],)).fetchone()[0])
        self.assertEqual(record['request'], self.network.sent[0])
        self.assertEqual(record['items'], self.network.opened()['items'])


    def later(self, **delta):
        return patch.object(a, 'now', return_value=(a.dt.datetime.fromisoformat(a.now()) + a.dt.timedelta(**delta)).isoformat())

    def material(self, *texts):
        with self.store.connect() as db:
            for text in texts:
                db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES(?,'d0',?)", (text, a.now()))

    def sends(self):
        return [b for b in self.network.sent if b['action'] == 'send']

    def test_daily_it_reads_only_what_is_new_and_never_offers_the_same_learning_twice(self):
        self.assertEqual((tl.DAYS, tl.MIN_MATERIAL), (1, 3))
        ask = self.distil([{'text': 'Drafts for people who don’t know the context yet should introduce it first.'},
                           {'text': 'Invoice reminders should wait until the due date has passed.'}])
        self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}]}, owner_dashboard=True)  # the second one removed
        self.assertIsNone(self.store.learnings_due())  # not twice a day
        with self.later(hours=25):
            self.assertIsNone(self.store.learnings_due())  # a day later, but nothing new to learn from
            self.material('Prefers short replies', 'Calls before noon', 'Writes in English to suppliers')
            self.fresh = False
            run_id = self.store.learnings_due()
            self.assertTrue(run_id)
            page = self.store.profile_evidence(1, a.PROFILE_SESSION_PREFIX + run_id)
            self.assertEqual(sorted(r['text'] for r in page['rows']), ['Calls before noon', 'Prefers short replies', 'Writes in English to suppliers'])
            self.assertEqual(page['shared_before'], ['Drafts for people who don’t know the context yet should introduce it first.'])
            self.assertEqual(page['removed_before'], ['Invoice reminders should wait until the due date has passed.'])
            self.assertIn('Never repeat what was shared, removed or withdrawn before', tl.prompt(run_id, page))
            with self.store.connect() as db:  # this run is the one the helper finishes below
                db.execute("DELETE FROM profile_runs WHERE run_id=?", (run_id,))
            ask = self.distil([{'text': 'Drafts for people who don’t know the context yet should introduce it first!'},  # sent before
                               {'text': 'Invoice reminders should wait until the due date has passed, always.'},  # removed before
                               {'text': 'Suggested call times should avoid the afternoon for this kind of owner.'}])
        self.assertEqual([i['text'] for i in ask['items']], ['Suggested call times should avoid the afternoon for this kind of owner.'])
        self.assertEqual([i['n'] for i in ask['items']], [1])

    def test_not_now_holds_a_daily_offer_for_a_week(self):
        ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}])
        self.app.action('learnings_later', {'id': ask['id']}, owner_dashboard=True)
        self.material('a', 'b', 'c')
        with self.later(days=3):
            self.assertIsNone(self.store.learnings_due())
        with self.later(days=8):
            self.assertTrue(self.store.learnings_due())

    def test_asking_each_time_is_the_default(self):
        view = self.app.learnings_view()
        self.assertEqual((view['offer'], view['auto']), (True, False))
        ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}])
        self.assertTrue(ask)
        self.app.learnings_auto_send()
        self.assertEqual(self.sends(), [])  # nothing goes by itself

    def test_send_automatically_sends_new_learnings_lists_them_and_withdraws_one(self):
        view = self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)['team_learnings']
        self.assertTrue(view['auto'])
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('set_learnings_auto', {'on': True})
        ask = self.distil([{'text': 'Drafts for people who don’t know Sam Lee yet should introduce the context first.'},
                           {'text': 'Graph updates fail now and then on a busy day.', 'fault': 'fp1'}])
        self.assertIsNone(ask)  # not asked: it went
        [body] = self.sends()
        self.assertFalse(body['named'])  # never the email by itself
        opened = self.network.opened()
        self.assertEqual([i['text'] for i in opened['items']], ['Drafts for people who don’t know someone yet should introduce the context first.',
                                                                'Graph updates fail now and then on a busy day.'])
        self.assertNotIn('log', opened['items'][1])  # never the error excerpt by itself
        self.assertNotIn('Sam', json.dumps(opened))  # the strip ran as always
        with self.store.connect() as db:
            self.assertEqual(tl.waiting(db), 0)
        shared = self.app.learnings_view()['shared']
        self.assertEqual([(s['n'], s['text'], s['auto'], s['withdrawn_at']) for s in shared],
                         [(1, opened['items'][0]['text'], True, None), (2, opened['items'][1]['text'], True, None)])
        self.assertEqual(shared[0]['use_cases'], [CASE])

        # Withdraw: signed with the same learnings key, so the team knows it is the sender without knowing who
        view = self.app.action('learnings_withdraw', {'id': shared[1]['id'], 'n': 2}, owner_dashboard=True)['team_learnings']
        req = self.network.sent[-1]
        self.assertEqual((req['action'], req['id'], req['n']), ('withdraw', shared[1]['id'], 2))
        self.assertEqual(req['from'], body['from'])
        me, team = nc.check_keys(req['from'])['fingerprint'], nc.check_keys(nc.public_keys(self.network.team))['fingerprint']
        said = nc.open_sealed(req['sealed'], self.network.team, req['from'], {**tl.CONTEXT, 'f': me, 't': team, 'r': f'withdraw:{req["id"]}:2'})
        self.assertEqual((said['id'], said['n'], said['withdraw']), (req['id'], 2, True))
        self.assertTrue(view['shared'][1]['withdrawn_at'])
        self.assertIsNone(view['shared'][0]['withdrawn_at'])
        count = len(self.network.sent)
        self.app.action('learnings_withdraw', {'id': shared[1]['id'], 'n': 2}, owner_dashboard=True)
        self.assertEqual(len(self.network.sent), count)  # once
        with self.assertRaisesRegex(ValueError, 'Unknown learning'):
            self.app.action('learnings_withdraw', {'id': shared[1]['id'], 'n': 3}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('learnings_withdraw', {'id': shared[1]['id'], 'n': 1})

        # A withdrawn learning counts as removed: it isn't made again
        self.material('a', 'b', 'c')
        with self.later(hours=25):
            self.fresh = False
            self.assertIsNone(self.distil([{'text': 'Graph updates fail now and then on a busy day!'}]))
        self.assertEqual(len(self.sends()), 1)

    def test_the_offers_tick_turns_it_on_and_the_email_is_never_automatic(self):
        ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}])
        done = self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}], 'named': True, 'auto': True}, owner_dashboard=True)
        self.assertTrue(done['team_learnings']['auto'])
        self.assertTrue(self.sends()[0]['named'])  # ticked this once, by the owner
        self.assertFalse(self.app.learnings_view()['shared'][0]['auto'])
        self.material('a', 'b', 'c')
        with self.later(hours=25):
            self.fresh = False
            self.assertIsNone(self.distil([{'text': 'Calendar invites should say the time zone of the other side.'}]))
        self.assertFalse(self.sends()[1]['named'])
        with self.store.connect() as db:
            batch = db.execute("SELECT id FROM team_learnings ORDER BY created_at DESC LIMIT 1").fetchone()[0]
        with self.assertRaisesRegex(ValueError, 'never added automatically'):
            tl.share(self.store.connect, self.app.config, batch, [{'n': 1}], True, self.network.call, auto=True)

    def test_an_uncertain_automatic_send_retries_quietly_and_a_refused_one_asks(self):
        self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        self.network.fail = True
        self.assertIsNone(self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}]))  # not asked meanwhile
        self.network.fail = False
        self.app.learnings_auto_send()  # the next step
        self.assertEqual(len(self.sends()), 1)
        self.assertEqual(self.app.learnings_view()['shared'][0]['auto'], True)
        # A stored learning the check would change now (a name learned since) is not sent: the owner sees it
        self.material('a', 'b', 'c')
        with self.later(hours=25):
            self.fresh = False
            with patch.object(tl, 'final_items', side_effect=ValueError('Learning 1: take out a name first')):
                ask = self.distil([{'text': 'Calendar invites should say the time zone of the other side.'}])
        self.assertEqual(ask['items'][0]['text'], 'Calendar invites should say the time zone of the other side.')
        self.assertEqual(len(self.sends()), 1)

    def test_careful_off_and_a_careful_fleet_stop_sending_automatically(self):
        import security_levels
        self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        with self.store.connect() as db:
            security_levels.apply(db, 'careful')
            self.assertEqual((tl.offer_on(db), tl.auto_chosen(db)), (False, False))
        self.assertIsNone(self.store.learnings_due())  # Careful: no run, nothing sent
        with self.store.connect() as db:
            security_levels.apply(db, 'standard')
            self.assertEqual((tl.offer_on(db), tl.auto_chosen(db)), (True, False))  # back to asking each time
        # Off in Settings stops it, and turns it off
        self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        view = self.app.action('set_learnings_offer', {'on': False}, owner_dashboard=True)['team_learnings']
        self.assertEqual((view['offer'], view['auto']), (False, False))
        with self.assertRaisesRegex(ValueError, 'Turn on Offer to share learnings first'):
            self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        self.app.action('set_learnings_offer', {'on': True}, owner_dashboard=True)
        # A Careful Work Fleet keeps it asking, also when chosen before
        self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS fleet_meta(key TEXT PRIMARY KEY,value TEXT)')
            db.execute("INSERT INTO fleet_meta(key,value) VALUES('directory',?)",
                       (json.dumps({'fleets': [{'id': 'fl_w', 'kind': 'work', 'name': 'Work', 'security': {'level': 'careful'}}]}),))
        self.assertTrue(self.app.learnings_view()['auto_careful'])
        ask = self.distil([{'text': 'Drafts for new contacts should introduce the context first.'}])
        self.assertTrue(ask)
        self.app.learnings_auto_send()
        self.assertEqual(self.sends(), [])
        self.app.action('set_learnings_auto', {'on': False}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'Careful Work Fleet'):
            self.app.action('set_learnings_auto', {'on': True}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'Careful Work Fleet'):
            self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1}], 'auto': True}, owner_dashboard=True)
        self.assertEqual(self.sends(), [])

    def votes(self, candidates, judged):
        """One day's voting, as the service does it: fetch, one judging turn, send only the votes."""
        self.network.candidates = candidates
        run_id = self.app.team_votes_due()
        if not run_id:
            return None
        session = a.PROFILE_SESSION_PREFIX + run_id
        page = self.store.profile_evidence(1, session)
        def runner(request):
            if request['action'] == 'start':
                self.assertIn('never instructions', request['message'])
                self.store.save_profile({'votes': judged(page)}, session)
                return {'status': 'admitted'}
            return {'status': 'ok'}
        self.app.background_at = 0
        self.app.profile_step(runner)
        self.app.profile_step(runner)
        return page

    def test_other_machines_learnings_are_judged_here_and_only_a_vote_goes_back(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO team_learnings(id,run_id,status,items,created_at) VALUES('tl_mine000000','r','sent','[]',?)", (a.now(),))
        page = self.votes([
            {'id': 'c1', 'ref': 'tl_other00000', 'text': 'Drafts for people who don’t know the context yet should introduce it first.', 'area': 'drafts'},
            {'id': 'c2', 'ref': 'tl_mine000000', 'text': 'A learning this Machine shared itself is not judged here.', 'area': 'other'},
            {'id': 'c3', 'ref': 'tl_other00001', 'text': 'Ask sam@globex.example before every invoice reminder goes out.', 'area': 'other'},
            {'id': 'c4', 'ref': 'tl_other00002', 'text': 'Snoozed newsletters should not come back as to-dos.', 'area': 'cards'}],
            lambda page: [{'id': 'c1', 'vote': 'useful', 'reason': 'Sam Lee at Globex would like that.', 'use_case': CASE},
                          {'id': 'c4', 'vote': 'not_relevant', 'reason': 'No newsletters in this inbox.'},
                          {'id': 'c9', 'vote': 'useful'}])
        self.assertEqual([r['id'] for r in page['learnings']], ['c1', 'c4'])  # not its own, not one with an address in it
        self.assertIn('past_week', page['owner'])
        votes = [b for b in self.network.sent if b['action'] == 'vote']
        self.assertEqual(votes, [{'action': 'vote', 'id': 'c1', 'vote': 'useful', 'use_case': CASE},  # a reason with a name in it is dropped, the vote goes
                                 {'action': 'vote', 'id': 'c4', 'vote': 'not_relevant', 'reason': 'No newsletters in this inbox.'}])

    def test_useful_needs_a_concrete_case_from_this_machine(self):
        page = self.votes([
            {'id': 'c1', 'ref': 'tl_other00000', 'text': 'Drafts for people who don’t know the context yet should introduce it first.', 'area': 'drafts'},
            {'id': 'c2', 'ref': 'tl_other00001', 'text': 'Snoozed newsletters should not come back as to-dos.', 'area': 'cards'},
            {'id': 'c3', 'ref': 'tl_other00002', 'text': 'Invoice reminders should wait until the due date has passed.', 'area': 'cards'}],
            lambda page: [{'id': 'c1', 'vote': 'useful', 'reason': 'Good idea.'},  # agrees, no case: not relevant here
                          {'id': 'c2', 'vote': 'useful', 'use_case': {**CASE, 'when': 'Sam Lee opens the draft'}},  # a case with a name: dropped
                          {'id': 'c3', 'vote': 'useful', 'use_case': CASE}])
        self.assertIn('Introduce yourself first, Sam Lee has never heard of us', json.dumps(page['owner']['past_week']))  # private, its own turn only
        self.assertIn('would this have changed something on this Machine in the past week?', tl.vote_prompt('r', page))
        votes = {b['id']: b for b in self.network.sent if b['action'] == 'vote'}
        self.assertEqual({k: v['vote'] for k, v in votes.items()}, {'c1': 'not_relevant', 'c2': 'not_relevant', 'c3': 'useful'})
        self.assertNotIn('use_case', votes['c2'])
        self.assertNotIn('Sam', json.dumps(list(votes.values())))
        self.assertEqual(votes['c3']['use_case'], CASE)
        self.assertIsNone(self.app.team_votes_due())  # fetched today: nothing more until tomorrow, and nothing waits

    def test_voting_off_in_settings_fetches_and_sends_nothing(self):
        self.assertTrue(self.app.learnings_view()['vote'])
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('set_learnings_vote', {'on': False})
        self.assertFalse(self.app.action('set_learnings_vote', {'on': False}, owner_dashboard=True)['team_learnings']['vote'])
        self.assertIsNone(self.votes([{'id': 'c1', 'ref': 'tl_x00000000', 'text': 'Drafts should introduce the context first.'}], lambda p: []))
        self.assertEqual(self.network.sent, [])

    def test_ask_first_holds_each_vote_for_the_owner_in_one_place(self):
        with self.store.connect() as db:
            cards = db.execute('SELECT count(*) FROM suggestions').fetchone()[0]
        view = self.app.action('set_learnings_vote', {'mode': 'ask'}, owner_dashboard=True)['team_learnings']
        self.assertEqual((view['vote_mode'], view['vote']), ('ask', True))
        self.votes([{'id': 'c1', 'ref': 'tl_other00000', 'text': 'Drafts for people who don’t know the context yet should introduce it first.', 'area': 'drafts'},
                    {'id': 'c2', 'ref': 'tl_other00001', 'text': 'Snoozed newsletters should not come back as to-dos.', 'area': 'cards'}],
                   lambda page: [{'id': 'c1', 'vote': 'useful', 'reason': 'Works for short chat replies too.', 'use_case': CASE}, {'id': 'c2', 'vote': 'not_relevant'}])
        self.assertEqual([b for b in self.network.sent if b['action'] == 'vote'], [], 'judged, but nothing goes before the owner says so')
        waiting = self.app.learnings_view()['votes_waiting']
        self.assertEqual(sorted((v['id'], v['vote']) for v in waiting), [('c1', 'useful'), ('c2', 'not_relevant')])
        with self.store.connect() as db:  # a vote never becomes a to-do of its own
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], cards)
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('learnings_votes_decide', {'ids': ['c1'], 'send': True})
        self.app.action('learnings_votes_decide', {'ids': ['c1'], 'send': True}, owner_dashboard=True)
        self.app.action('learnings_votes_decide', {'ids': ['c2'], 'send': False}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'no longer waiting'):
            self.app.action('learnings_votes_decide', {'ids': ['c2'], 'send': True}, owner_dashboard=True)
        self.assertEqual(self.app.learnings_view()['votes_waiting'], [])
        self.app.team_votes_due()  # the next send, ten minutes on at most
        self.assertEqual([b for b in self.network.sent if b['action'] == 'vote'],
                         [{'action': 'vote', 'id': 'c1', 'vote': 'useful', 'reason': 'Works for short chat replies too.', 'use_case': CASE}])

    def test_a_vote_left_waiting_goes_unsent_and_off_drops_what_waits(self):
        with self.store.connect() as db:
            tl.ensure(db)
            tl.set_vote(db, 'ask')
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=tl.ASK_DAYS + 1)).isoformat(timespec='seconds')
            for cid, at in (('c1', old), ('c2', a.now())):
                db.execute("INSERT INTO team_learning_votes(candidate_id,text,status,vote,fetched_at) VALUES(?,'A general tip for drafts.','judged','useful',?)", (cid, at))
        self.assertEqual(tl.send_votes(self.store.connect, self.network.call), 0)
        self.assertEqual([v['id'] for v in self.app.learnings_view()['votes_waiting']], ['c2'])
        self.app.action('set_learnings_vote', {'mode': 'off'}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM team_learning_votes WHERE status!='skipped'").fetchone()[0], 0)
        with self.assertRaisesRegex(ValueError, 'on, ask or off'):
            self.app.action('set_learnings_vote', {'mode': 'sometimes'}, owner_dashboard=True)

    def test_the_old_on_and_off_carry_over(self):
        with self.store.connect() as db:
            tl.ensure(db)
            for stored, mode in (('on', 'on'), ('off', 'off'), ('ask', 'ask'), ('garbled', 'on')):
                tl.set_pref(db, 'vote', stored)
                self.assertEqual(tl.vote_mode(db), mode)
        self.assertEqual(self.app.action('set_learnings_vote', {'on': True}, owner_dashboard=True)['team_learnings']['vote_mode'], 'on')  # an older dashboard
        self.assertEqual(self.app.action('set_learnings_vote', {'on': False}, owner_dashboard=True)['team_learnings']['vote_mode'], 'off')

    # ------------------------------------------------------------ use cases

    def test_use_cases_are_stripped_and_checked_before_they_leave(self):
        with self.store.connect() as db:
            names = tl.known_names(db, {'accounts': self.store.accounts})
        self.assertEqual(tl.check_case(CASE, names), (CASE, []))
        # Product and screen names may stay capitalized mid-sentence; a sentence may start with a capital
        fine = {'given': 'A customer writes on WhatsApp on a Friday', 'when': 'the owner taps Snooze in Settings of The Machine',
                'then': 'the to-do comes back on Monday. Nothing else changes'}
        self.assertEqual(tl.check_case(fine, names)[1], [])
        for field, bad, problem in (('given', 'a reply to Sam Lee about the deal', 'name'),
                                    ('given', 'a reply to Initech about the deal', 'name'),  # a company the graph doesn't know yet
                                    ('when', 'the owner writes "see you at the office then"', 'quote'),
                                    ('when', 'the owner mails sam@globex.example', 'address'),
                                    ('then', 'the invoice of €1,200 goes out', 'amount'),
                                    ('then', 'it is sent on 2026-10-30', 'date'),
                                    ('then', 'the owner checks https://globex.example/deal', 'link')):
            case, problems = tl.check_case({**CASE, field: bad}, names)
            self.assertIn(problem, problems, bad)
        # What the turn wrote: names are stripped; one that still isn't generic is left out, and the owner is told
        cases, taken = tl.clean_cases([{**CASE, 'given': 'a first reply to Sam Lee at Globex'},
                                       {**CASE, 'when': 'the owner writes “hi there, long time”'},
                                       {**CASE, 'given': 'a reply in Initech’s thread'}, CASE, CASE,
                                       {'given': 'x', 'when': 'y', 'then': 'z'}], names)
        self.assertEqual([c['given'] for c in cases], ['a first reply to someone at a company', CASE['given']])
        self.assertEqual(tl.taken_line(taken), 'Took out 2 names and 2 use cases.')
        for bit in PERSONAL + ('Initech', 'long time'):
            self.assertNotIn(bit, json.dumps(cases))

    def test_a_learning_carries_its_use_cases_to_the_team_as_the_owner_kept_them(self):
        other = {'given': 'a colleague asks for a status update in chat', 'when': 'the owner opens the to-do',
                 'then': 'the draft starts with the status, not a greeting'}
        ask = self.distil([
            {'text': 'Drafts for people who don’t know the context yet should introduce it first.', 'area': 'drafts',
             'use_cases': [CASE, {**other, 'then': 'the owner says “ok” and moves on'}, other]},
            {'text': 'A learning without any use case says too little to build from.', 'use_cases': []}])
        self.assertEqual(len(ask['items']), 1)  # the one without a use case is dropped
        item = ask['items'][0]
        self.assertEqual(item['use_cases'], [CASE, other])  # the quoted one is left out
        self.assertEqual(item['taken'], 'Took out a use case.')
        share = lambda cases: self.app.action('learnings_share', {'id': ask['id'], 'items': [{'n': 1, 'use_cases': cases}]}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'use case 1: write it generically'):
            share([{**CASE, 'given': 'a first reply to Initech'}])
        with self.assertRaisesRegex(ValueError, 'use case 2: take out an address first'):
            share([CASE, {**other, 'when': 'the owner mails owner@globex.example'}])
        with self.assertRaisesRegex(ValueError, 'keep at least one use case'):
            share([])
        with self.assertRaisesRegex(ValueError, 'fill in all three parts'):
            share([{**CASE, 'then': ''}])
        self.assertEqual(self.network.sent, [])
        edited = {**other, 'then': 'the draft opens with the status'}
        share([edited])  # the owner kept one, edited
        self.assertEqual(self.network.opened()['items'][0]['use_cases'], [edited])
        self.assertNotIn('status', json.dumps(self.network.sent[0]))  # sealed like the learning itself

    def test_a_vote_carries_its_own_use_case_and_counts_without_one(self):
        their = {'given': 'a supplier sends a second reminder', 'when': 'the owner opens the to-do', 'then': 'the draft mentions the first reminder'}
        page = self.votes([
            {'id': 'c1', 'ref': 'tl_other00000', 'text': 'Drafts for people who don’t know the context yet should introduce it first.', 'area': 'drafts',
             'use_cases': [CASE, {**CASE, 'given': 'a reply to Initech'}]},
            {'id': 'c2', 'ref': 'tl_other00001', 'text': 'Reminders should say how many came before.', 'area': 'drafts', 'use_cases': [their]},
            {'id': 'c3', 'ref': 'tl_other00002', 'text': 'Snoozed newsletters should not come back as to-dos.', 'area': 'cards'}],
            lambda page: [{'id': 'c1', 'vote': 'useful', 'use_case': {'given': 'a first mail to a new partner', 'when': 'the owner opens the draft',
                                                                    'then': 'it introduces the owner first'}},
                          {'id': 'c2', 'vote': 'not_useful', 'use_case': {**their, 'given': 'Sam Lee sends a second reminder'}},
                          {'id': 'c3', 'vote': 'not_relevant'}])
        self.assertEqual([r['use_cases'] for r in page['learnings']], [[CASE], [their], []])  # one that isn't generic never reaches the turn
        self.assertIn('"use_case"', tl.vote_prompt('r', page))
        votes = {b['id']: b for b in self.network.sent if b['action'] == 'vote'}
        self.assertEqual(votes['c1']['use_case']['then'], 'it introduces the owner first')
        self.assertNotIn('use_case', votes['c2'])  # a name in it: dropped, the vote still goes
        self.assertEqual(votes['c2']['vote'], 'not_useful')
        self.assertNotIn('use_case', votes['c3'])

    def test_an_older_votes_table_gets_the_use_case_columns(self):
        import sqlite3
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE team_learning_votes(candidate_id TEXT PRIMARY KEY,ref TEXT,text TEXT NOT NULL,example TEXT,area TEXT,'
                   'status TEXT NOT NULL,vote TEXT,reason TEXT,fetched_at TEXT NOT NULL,sent_at TEXT,error TEXT)')
        tl.ensure(db)
        tl.ensure(db)  # twice is fine
        columns = {r[1] for r in db.execute('PRAGMA table_info(team_learning_votes)')}
        self.assertTrue({'use_cases', 'use_case'} <= columns)


if __name__ == '__main__':
    unittest.main()
