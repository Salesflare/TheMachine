"""Work ready on arrival: a new owner who finishes setup finds a to-do already prepared, the reply to whoever has waited
longest on them, and a hello by first name with one line from their own Machine ("Ria has been waiting on your reply
since Thursday"), or just "Hi Alex" while nothing is ready. The quick first look leads with that person's signal and its
to-do's draft is the first one prepared; the hello shows on the first views only and only on the owner's own dashboard.
Made-up people, no Gateway, nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('ready_on_arrival_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class Runner:
    def __init__(self): self.requests = []
    def __call__(self, request): self.requests.append(request); return {'status': 'admitted'}


def ago(hours):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).isoformat()


def mail(source_id, sender, hours_ago, labels=(), thread=None, to='me@example.com'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': ago(hours_ago), 'title': 'Hello',
            'body': 'Text', 'metadata': {'from': sender, 'to': to, 'labels': list(labels), 'thread_id': thread or source_id}, 'deleted': False}


class ReadyOnArrival(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail', 'email': 'me@example.com'}],
                           'review_worker': {'enabled': True}, 'delivery_enabled': True, 'owner_name': 'Alex Example'}
        a.Store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'me@example.com'}]
        self.addCleanup(setattr, a.Store, 'accounts', [])
        for name, value in (('has_model', True), ('openclaw_model', 'claude-cli/claude-opus-5-5')):
            p = patch.object(a, name, return_value=value); p.start(); self.addCleanup(p.stop)
        self.app.model_usage = None
        self.store.commit_page('work', {}, [
            *[mail(f'news{n}', 'Shop <news@shop.example>', 1, labels=['CATEGORY_PROMOTIONS']) for n in range(10)],
            mail('sam', 'Sam Lee <sam@example.org>', 3),               # waiting, newest
            mail('kim', 'Kim Park <kim@example.org>', 24 * 2),          # waiting
            mail('ria', 'Ria Example <ria@example.org>', 24 * 4),       # waiting longest
            mail('lou', 'Lou Grant <lou@example.org>', 24 * 5),         # older, but the owner answered it
            mail('lou-re', 'Me <me@example.com>', 24 * 5 - 1, labels=['SENT'], thread='lou', to='lou@example.org'),
        ])
        with self.store.connect() as db:
            self.ids = {s: i for i, s in db.execute('SELECT id,source_id FROM events')}

    def claim(self):
        self.assertEqual(self.app.review_step(Runner()), 'admitted')
        with self.store.connect() as db:
            run = dict(db.execute('SELECT * FROM review_runs ORDER BY started_at DESC').fetchone())
        return self.store.begin_analysis(['work'], 120, a.REVIEW_SESSION_PREFIX + run['run_id'], run['run_id'])

    def ahead(self, key, source_id):
        return self.app.action('suggest', {'dedupe_key': key, 'title': f'Reply to {key}', 'body': 'I can draft it.',
                                           'event_ids': [self.ids[source_id]], 'when': 'now', 'prepare_ahead': True})['id']

    def test_the_quick_first_look_leads_with_who_has_waited_longest(self):
        claim = self.claim()
        names = {i: s for s, i in self.ids.items()}
        order = [names[e['id']] for e in claim['events']]
        self.assertEqual(order[:3], ['ria', 'sam', 'kim'])  # the longest wait first, then newest first as before
        self.assertEqual(claim['waiting_longest'], self.ids['ria'])
        self.assertIn('prepare_ahead:true', claim['first_look'])
        self.assertIn('nothing is sent', claim['first_look'])

    def test_once_a_first_draft_started_the_hint_is_not_given_again(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_ahead_started',?)", (a.now(),))
        claim = self.claim()
        self.assertNotIn('waiting_longest', claim)
        self.assertNotIn('first_look', claim)

    def test_the_most_waiting_to_do_is_prepared_first_and_nothing_is_sent(self):
        newest = self.ahead('sam', 'sam')  # saved first, but Ria has waited longer
        longest = self.ahead('ria', 'ria')
        runner = Runner()
        self.app.preparation_step(runner)
        self.assertEqual([r['action'] for r in runner.requests], ['start'])  # one draft ahead at a time
        with self.store.connect() as db:
            started = db.execute("SELECT suggestion_id FROM preparations WHERE status IN ('starting','running')").fetchall()
            self.assertEqual([r[0] for r in started], [longest])
            self.assertEqual(db.execute("SELECT status FROM preparations WHERE suggestion_id=?", (newest,)).fetchone()[0], 'queued')
            # A draft only: nothing went out or is waiting to go out
            self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0], 0)
            self.assertFalse(db.execute("SELECT 1 FROM deliveries WHERE status='sent'").fetchone())

    def test_the_hello_names_who_has_waited_longest_on_a_ready_to_do(self):
        self.ahead('sam', 'sam')
        longest = self.ahead('ria', 'ria')
        hello = self.store.greeting('Alex Example')
        self.assertEqual(hello['name'], 'Alex')
        self.assertEqual((hello['line']['person'], hello['line']['card']), ('Ria', longest))
        with self.store.connect() as db:
            self.assertEqual(hello['line']['since'], db.execute('SELECT occurred_at FROM events WHERE id=?', (self.ids['ria'],)).fetchone()[0])

    def test_a_ready_to_do_leads_over_an_older_wait_still_to_decide(self):
        # The hello and the top of the list name the same to-do: the dashboard leads with line.card. A ready draft (Sam,
        # waiting since this morning) beats Ria's older message whose to-do still waits for a decision.
        older = self.app.action('suggest', {'dedupe_key': 'ria', 'title': 'Answer Ria', 'body': 'Asked.', 'event_ids': [self.ids['ria']], 'when': 'now'})['id']
        ready = self.ahead('sam', 'sam')
        self.assertEqual(self.store.greeting('Alex')['line']['card'], older)  # nothing ready yet: the longest wait
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (ready,))
        self.assertEqual(self.store.greeting('Alex')['line'], {'person': 'Sam', 'card': ready, 'since': self.since('sam')})

    def since(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT occurred_at FROM events WHERE id=?', (self.ids[source_id],)).fetchone()[0]

    def test_decisions_from_before_the_hello_began_do_not_end_it(self):
        # The sample Machine of the site demo: its history is older than the owner's first view (sandbox/load.py)
        sid = self.ahead('ria', 'ria')
        self.store.decide(sid, 'reject', '', 'click', 'dashboard')
        later = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)).isoformat()
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('greeting',?,'on')", (later,))
        with patch.object(a, 'now', return_value=later):
            self.assertEqual(self.store.greeting('Alex')['name'], 'Alex')

    def test_with_nothing_ready_it_is_a_plain_hello(self):
        self.assertEqual(self.store.greeting('Alex Example'), {'name': 'Alex'})
        # A to-do nobody waits on (a newsletter) gives no line either
        self.app.action('suggest', {'dedupe_key': 'n', 'title': 'Sale', 'body': 'Maybe.', 'event_ids': [self.ids['news0']], 'when': 'now'})
        self.assertEqual(self.store.greeting('Alex Example'), {'name': 'Alex'})

    def test_only_on_the_first_views(self):
        self.assertEqual(self.store.greeting('Alex'), {'name': 'Alex'})
        later = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=a.GREETING_HOURS + 1)).isoformat()
        with patch.object(a, 'now', return_value=later):
            self.assertIsNone(self.store.greeting('Alex'))  # a day on, it is gone
        sid = self.ahead('ria', 'ria')
        self.store.decide(sid, 'reject', '', 'click', 'dashboard')
        self.assertIsNone(self.store.greeting('Alex'))  # their first decided to-do ends it

    def test_an_owner_who_decided_to_dos_before_never_gets_it(self):
        sid = self.ahead('ria', 'ria')
        self.store.decide(sid, 'reject', '', 'click', 'dashboard')
        with self.store.connect() as db:
            db.execute("DELETE FROM milestones WHERE name='greeting'")
        self.assertIsNone(self.store.greeting('Alex'))

    def test_the_hello_never_leaves_the_machine(self):
        self.ahead('ria', 'ria')
        self.assertEqual(self.store.greeting('Alex')['line']['person'], 'Ria')
        with self.store.connect() as db:
            reports = json.dumps([a.first_cards_report(db, self.app.config['accounts']), a.activity_report(db)])
        for word in ('Ria', 'Alex', 'ria@example.org', 'greeting'):
            self.assertNotIn(word, reports)  # the health reports stay counts and timestamps

    def test_a_sender_without_a_name_gives_no_line(self):
        self.store.commit_page('work', {}, [mail('bare', 'pat@example.org', 24 * 6)])
        with self.store.connect() as db:
            bare = db.execute("SELECT id FROM events WHERE source_id='bare'").fetchone()[0]
        self.app.action('suggest', {'dedupe_key': 'bare', 'title': 'Reply', 'body': 'Asked.', 'event_ids': [bare], 'when': 'now'})
        self.assertEqual(self.store.greeting('Alex'), {'name': 'Alex'})  # never an address in its place
        self.assertEqual(a.sender_first_name({'from': '"Lee, Sam" <sam@example.org>'}), 'Sam')
        self.assertEqual(a.sender_first_name({'from': 'U02AB3CD4'}), '')

    def test_the_line_names_the_to_dos_own_message_not_another_it_carries(self):
        # A to-do about a mailbox's thread (first evidence) that also carries an older message from someone else in
        # another thread: the hello names the to-do's own sender, never the other one, and links to that to-do
        self.store.commit_page('work', {}, [mail('hall', 'Pat Hall <pat@town.example>', 24 * 1),
                                            mail('other', 'Kai Other <kai@other.example>', 24 * 3)])
        with self.store.connect() as db:
            ids = dict(db.execute("SELECT source_id,id FROM events WHERE source_id IN ('hall','other')").fetchall())
        card = self.app.action('suggest', {'dedupe_key': 'hall', 'title': 'Book the hall', 'body': 'Draft ready.',
                                           'event_ids': [ids['hall'], ids['other']], 'when': 'now'})['id']
        line = self.store.greeting('Alex')['line']
        self.assertEqual((line['person'], line['card']), ('Pat', card))
        with self.store.connect() as db:
            self.assertEqual(line['since'], db.execute('SELECT occurred_at FROM events WHERE id=?', (ids['hall'],)).fetchone()[0])

    def test_a_mailbox_name_is_not_a_name(self):
        # "frontdesk <frontdesk@…>": the mail tool shows the mailbox as the name. No line from it, nor a made-up name.
        self.assertEqual(a.sender_first_name({'from': 'frontdesk <frontdesk@mail.example>'}), '')
        self.assertEqual(a.sender_first_name({'from': '"info.desk" <info-desk@mail.example>'}), '')
        self.assertEqual(a.sender_first_name({'from': 'Jan <jan@mail.example>'}), 'Jan')  # a real first name stays
        self.assertEqual(a.sender_first_name({'from': 'jan peeters <jan.peeters@mail.example>'}), 'jan')
        self.store.commit_page('work', {}, [mail('box', 'frontdesk <frontdesk@mail.example>', 24 * 6)])
        with self.store.connect() as db:
            box = db.execute("SELECT id FROM events WHERE source_id='box'").fetchone()[0]
        self.app.action('suggest', {'dedupe_key': 'box', 'title': 'Reply', 'body': 'Asked.', 'event_ids': [box], 'when': 'now'})
        self.assertEqual(self.store.greeting('Alex'), {'name': 'Alex'})
        # Someone else waiting on a to-do of their own is named instead, linked to theirs
        kim = self.ahead('kim', 'kim')
        self.assertEqual({k: v for k, v in self.store.greeting('Alex')['line'].items() if k != 'since'}, {'person': 'Kim', 'card': kim})

    def test_a_mailbox_is_named_by_its_organization_from_the_graph(self):
        self.store.commit_page('work', {}, [mail('rent', 'rentals <rentals@town.example>', 24 * 2)])
        with self.store.connect() as db:
            rent = db.execute("SELECT id FROM events WHERE source_id='rent'").fetchone()[0]
            db.execute("INSERT INTO graph_nodes(id,kind,name,info,strength,signals) VALUES('org:town.example','org','Town Hall','{}',1,1)")
            db.execute("INSERT INTO graph_nodes(id,kind,name,info,strength,signals) VALUES('email:rentals@town.example','person','rentals',?,1,1)",
                       (json.dumps({'org': 'org:town.example'}),))
            db.execute("INSERT INTO graph_events(node_id,event_id,at,direct) VALUES('email:rentals@town.example',?,?,1)", (rent, a.now()))
        card = self.app.action('suggest', {'dedupe_key': 'rent', 'title': 'Book the hall', 'body': 'Asked.', 'event_ids': [rent], 'when': 'now'})['id']
        self.assertEqual({k: v for k, v in self.store.greeting('Alex')['line'].items() if k != 'since'}, {'person': 'Town Hall', 'card': card})


if __name__ == '__main__':
    unittest.main()
