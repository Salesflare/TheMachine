"""Ask from search (search_ask.py, machine/app/search_ask.py): a question typed into Search gets a short answer from the
owner's own messages in the area in view, with its sources; a name or keywords get nothing; no model, nothing; a failed
turn says so. It never sends or makes a to-do. All names and messages here are made up."""
import json
import unittest
from unittest import mock

import test_graph as tg

a, graph = tg.a, tg.graph
import help_chat  # noqa: E402
import search_ask  # noqa: E402
import shared_graph  # noqa: E402
from machine.app import search_ask as app_ask  # noqa: E402

CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'scope': 'work'},
                       {'id': 'chat', 'service': 'whatsapp', 'email': 'Personal WhatsApp', 'scope': 'personal'}]}


def work_mail(days_ago, sender, title, body, thread=None):
    e = tg.mail(days_ago, sender, 'sam@acme.example', title=title, thread=thread)
    e['body'] = body
    return e


def home_chat(days_ago, name, body):
    e = tg.chat(days_ago, '3255501', name)
    e['body'] = body
    return e


class SearchAsk(unittest.TestCase):
    add = tg.Graph.add

    def setUp(self):
        tg.Graph.setUp(self)
        self.app.config = CONFIG
        self.prompts, self.plans = [], []
        self.reply = 'Kim said the pilot moves to March [1].'
        self.plan = {'question': True, 'person': None, 'said_by': 'both', 'from': None, 'to': None, 'about': ''}
        search_ask._asked.clear()

        def model(config, text):
            if 'reply with one JSON object' in text:  # the first turn: what the question means
                self.plans.append(text)
                return json.dumps(self.plan)
            self.prompts.append(text)
            if isinstance(self.reply, Exception):
                raise self.reply
            return self.reply
        self.app.ask_model = model
        self.add(work_mail(2, 'Kim Vale <kim@initech.example>', 'Pilot timing', 'The pilot moves to March, budget unchanged.'),
                 work_mail(5, 'Lee Park <lee@initech.example>', 'Lunch', 'Lunch on Friday?'),
                 home_chat(1, 'Robin Hart', 'The pilot of the plane said we land at noon.'))

    def ask(self, question, area=None):
        return self.app.action('search_ask', {'query': question, 'area': area}, owner_dashboard=True)

    def test_a_question_is_answered_from_its_messages_with_links(self):
        found = self.ask('what did kim say about the pilot?', 'work')
        self.assertEqual(found['answer'], 'Kim said the pilot moves to March.')  # the numbers become links
        self.assertEqual([s['title'] for s in found['sources']], ['Pilot timing'])
        self.assertEqual(found['sources'][0]['from'], 'Kim Vale')
        self.assertEqual(set(found['sources'][0]), {'id', 'kind', 'title', 'from', 'at'})  # no message text goes back
        prompt = self.prompts[0]
        self.assertIn('<<<The pilot moves to March, budget unchanged.>>>', prompt)  # other people's words marked as data
        self.assertIn('Question: <<<what did kim say about the pilot?>>>', prompt)
        self.assertIn('reply with exactly NONE', prompt)  # whether it's a question: the model's call, from meaning
        self.assertIn('Reply in the language of the question', prompt)

    def test_only_the_area_in_view(self):
        self.ask('what did they say about the pilot', 'work')
        self.assertNotIn('land at noon', self.prompts[-1])
        self.ask('what did they say about the pilot', 'personal')
        self.assertIn('land at noon', self.prompts[-1])
        self.assertNotIn('moves to March', self.prompts[-1])
        self.ask('what did they say about the pilot', 'all')
        self.assertIn('land at noon', self.prompts[-1])
        self.assertIn('moves to March', self.prompts[-1])
        with self.assertRaises(ValueError):
            self.ask('what about the pilot', 'fleet')

    def test_work_leaves_out_a_thread_about_the_owners_own_life(self):
        self.add(work_mail(1, 'Dr. Ash <ash@clinic.example>', 'Pilot appointment', 'Your pilot appointment is on Monday.', thread='tpriv'))
        with self.store.connect() as db:
            shared_graph.ensure(db)
            row = db.execute("SELECT id,kind,metadata FROM events WHERE title='Pilot appointment'").fetchone()
            db.execute('INSERT INTO share_threads(thread,verdict,at) VALUES(?,?,?)',
                       (shared_graph.thread_of(row['kind'], json.loads(row['metadata']), row['id']), 'personal', tg.NOW.isoformat()))
        self.ask('what is going on with the pilot', 'work')
        self.assertNotIn('appointment', self.prompts[-1])
        self.ask('what is going on with the pilot', None)
        self.assertIn('appointment', self.prompts[-1])  # All shows it, as Search does

    def test_keywords_or_a_name_get_nothing(self):
        self.reply = 'NONE'
        self.assertEqual(self.ask('kim pilot march'), {'none': True})
        self.assertEqual(self.ask('kim'), {'none': True})  # one word: not even asked
        self.assertEqual(len(self.prompts), 1)
        self.assertEqual(self.ask('what did zephyr quoxx say'), {'none': True})  # nothing found: no turn
        self.assertEqual(len(self.prompts), 1)

    def test_no_model_shows_nothing_and_a_failed_turn_says_so(self):
        del self.app.ask_model
        with mock.patch.object(app_ask, 'has_model', return_value=False):
            self.assertEqual(self.ask('what did kim say about the pilot?'), {'off': True})
        self.app.ask_model = lambda config, text: (_ for _ in ()).throw(help_chat.Unavailable('slow'))
        self.assertEqual(self.ask('what did kim say about the pilot?'), {'error': True})

    def test_it_never_sends_or_makes_a_to_do_and_waits_for_nothing(self):
        with self.store.connect() as db:
            before = [db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ('suggestions', 'decisions', 'action_jobs')]
        # Not background work: it never asks the background pause or spacing (the first look and a check keep theirs)
        self.app.background_pause = self.app.background_started = mock.Mock(side_effect=AssertionError('background'))
        self.reply = 'Send Kim a reply now [1]. I made a to-do for it.'
        self.ask('what did kim say about the pilot?')
        with self.store.connect() as db:
            after = [db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ('suggestions', 'decisions', 'action_jobs')]
        self.assertEqual(before, after)
        self.assertIn('search_ask', a.DASHBOARD_ACTIONS)
        self.assertIn('search_ask', a.OWNER_ACTIONS)  # never from the CLI the agent runs
        with self.assertRaises(ValueError):
            self.app.action('search_ask', {'query': 'what about the pilot?'}, owner_dashboard=False)

    def test_the_prompt_and_the_answer_are_capped(self):
        rows = [{'id': i, 'kind': 'gmail.message', 'title': f'Note {i}', 'occurred_at': '2026-10-01T09:00:00+00:00',
                 'metadata': {'from': f'P{i} <p{i}@x.example>'}, 'body': 'word ' * 2000} for i in range(30)]
        found = search_ask.sources(rows)
        self.assertEqual(len(found), search_ask.SOURCES)
        self.assertTrue(all(len(s['text']) <= search_ask.SOURCE_CHARS for s in found))
        text = search_ask.prompt('what changed? ' * 100, found, 'nl')
        self.assertLessEqual(len(text), search_ask.PROMPT_CHARS + search_ask.QUESTION_CHARS + 40)
        self.assertIn('reply in Dutch', text)
        long = search_ask.parse('Yes. ' * 600 + '[2]', found)
        self.assertLessEqual(len(long['answer']), search_ask.ANSWER_CHARS + 1)
        self.assertEqual([s['id'] for s in long['sources']], [1])
        self.assertIsNone(search_ask.parse(' NONE. ', found))
        self.assertEqual(search_ask.parse('Nothing in these messages says so.', found)['sources'], [])  # none cited: no sources
        with mock.patch.object(search_ask, 'PER_HOUR', 1):
            search_ask._asked.clear()
            search_ask.ask('what changed here?', rows, lambda p: 'A [1].')
            with self.assertRaises(search_ask.Unavailable):
                search_ask.ask('what changed here?', rows, lambda p: 'A [1].')

    def test_the_lighter_model_at_a_low_thinking_level(self):
        self.app.chat_models = lambda read=True: [{'ref': 'p/light', 'levels': ['off', 'minimal', 'low', 'high']}]
        with mock.patch.object(app_ask, 'background_model', return_value=('p', 'light')):
            self.assertEqual(self.app.search_ask_model(), ('p/light', 'low'))
        self.app.chat_models = lambda read=True: None  # the model list not read yet: OpenClaw's own level
        with mock.patch.object(app_ask, 'background_model', return_value=None):
            self.assertEqual(self.app.search_ask_model()[1], None)


# Today is Friday 2026-10-16 (tg.NOW): last week is Monday 5 to Sunday 11 October, 5 to 11 days ago.
LAST_WEEK = {'from': '2026-10-05', 'to': '2026-10-11'}


class PersonAndDays(unittest.TestCase):
    """A question about someone and some days ("what did Andrea say last week?") reads that person's messages from those
    days, found through the Graph, never any text with the name in it or messages from another time."""
    add, ask = tg.Graph.add, SearchAsk.ask

    def setUp(self):
        SearchAsk.setUp(self)
        self.add(work_mail(7, 'Andrea Vale <andrea@initech.example>', 'Rollout', 'The rollout slips to Thursday.'),
                 work_mail(20, 'Andrea Vale <andrea@initech.example>', 'Invoices', 'Old note about invoices.'),
                 work_mail(6, 'Andreas Berg <andreas@globex.example>', 'Pilot', 'Andreas here about the pilot.'),
                 work_mail(6, 'Kim Vale <kim@initech.example>', 'Hello', 'Andrea said hi to everyone.'))
        self.graph()

    def graph(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, CONFIG, tg.NOW.isoformat())

    def person(self, address):
        with self.store.connect() as db:
            return db.execute("SELECT id FROM graph_nodes WHERE kind='person' AND id=?", ('email:' + address,)).fetchone()[0]

    def test_only_their_messages_from_those_days(self):
        self.plan = {'question': True, 'person': 'Andrea', 'said_by': 'person', **LAST_WEEK, 'about': ''}
        self.reply = 'On Fri 9 Oct Andrea said the rollout slips to Thursday [1].'
        found = self.ask('what did Andrea say last week?')
        prompt = self.prompts[-1]
        self.assertIn('The rollout slips to Thursday.', prompt)
        self.assertNotIn('Old note about invoices', prompt)  # her message from another week
        self.assertNotIn('Andreas here', prompt)  # Andreas is another name
        self.assertNotIn('Andrea said hi', prompt)  # someone else's message with her name in it
        self.assertIn('Andrea Vale', prompt)
        self.assertIn('2026-10-05 to', prompt)
        self.assertEqual([s['title'] for s in found['sources']], ['Rollout'])
        self.assertEqual(found['messages'], [])  # nothing else it read

    def test_the_days_are_the_owners_own(self):
        tz = tg.dt.timezone(tg.dt.timedelta(hours=2))
        start, until = search_ask.bounds(tg.dt.date(2026, 10, 5), tg.dt.date(2026, 10, 11), tz)
        self.assertEqual((start, until), ('2026-10-04T22:00:00+00:00', '2026-10-11T22:00:00+00:00'))  # midnight to midnight there
        self.assertEqual(search_ask.last_week(tg.dt.date(2026, 11, 8)), (tg.dt.date(2026, 10, 26), tg.dt.date(2026, 11, 1)))
        self.assertEqual(search_ask.last_week(tg.dt.date(2026, 11, 9)), (tg.dt.date(2026, 11, 2), tg.dt.date(2026, 11, 8)))
        got = search_ask.parse_plan('Sure: {"question": true, "person": "Andrea", "said_by": "person", "from": "2026-10-11", "to": "2026-10-05", "about": ""}')
        self.assertEqual((got['person'], got['start'], got['end']), ('Andrea', tg.dt.date(2026, 10, 5), tg.dt.date(2026, 10, 11)))
        self.assertIsNone(search_ask.parse_plan('no idea'))
        self.assertFalse(search_ask.parse_plan('{"question": false}')['question'])

    def test_a_time_without_a_person_keeps_only_those_days(self):
        self.add(work_mail(1, 'Lee Park <lee@initech.example>', 'Pilot again', 'The pilot is on track.'))
        self.plan = {'question': True, 'person': None, 'said_by': 'both', 'from': '2026-10-12', 'to': '2026-10-16', 'about': 'pilot'}
        self.ask('what changed about the pilot this week?')
        self.assertIn('The pilot is on track.', self.prompts[-1])
        self.assertNotIn('Andreas here about the pilot', self.prompts[-1])  # 6 days ago: last week
        self.assertIn('moves to March', self.prompts[-1])  # Kim's, 2 days ago: this week too

    def test_nothing_in_those_days_says_so_and_gives_their_latest(self):
        self.plan = {'question': True, 'person': 'Andrea', 'said_by': 'person', 'from': '2026-10-12', 'to': '2026-10-16', 'about': ''}
        self.reply = 'Andrea Vale sent nothing this week. Her latest, on Fri 9 Oct, said the rollout slips to Thursday [1].'
        found = self.ask('what did Andrea say this week?')
        prompt = self.prompts[-1]
        self.assertIn('There are no messages from Andrea Vale', prompt)
        self.assertIn('Say that plainly first', prompt)
        self.assertIn('The rollout slips to Thursday.', prompt)  # her latest, with its date
        self.assertIn('Fri 2026-10-09', prompt)
        self.assertNotIn('Old note about invoices', prompt)
        self.assertEqual([s['title'] for s in found['sources']], ['Rollout'])

    def test_several_with_the_name_are_named(self):
        self.add(work_mail(8, 'Andrea Moss <andrea@moss.example>', 'Venue', 'The venue is booked.'))
        self.graph()
        self.plan = {'question': True, 'person': 'Andrea', 'said_by': 'person', **LAST_WEEK, 'about': ''}
        self.ask('what did Andrea say last week?')
        prompt = self.prompts[-1]
        self.assertIn('Other people with that name: ', prompt)
        self.assertIn('Andrea Moss', prompt)
        self.assertIn('Andrea Vale', prompt)
        self.assertNotIn('Andreas Berg', prompt)

    def test_a_suggested_question_comes_with_its_person_and_days(self):
        self.add(work_mail(2, 'Noor Lind <noor@initech.example>', 'Lunch again', 'Lunch next week?'))
        self.graph()
        andrea, noor = self.person('andrea@initech.example'), self.person('noor@initech.example')
        got = self.app.action('search_ask_examples', {'people': [noor, andrea, 'email:nobody@x.example']}, owner_dashboard=True)
        self.assertEqual([(p['name'], p['from'], p['to']) for p in got['people']], [('Andrea Vale', *LAST_WEEK.values())])  # Noor wrote this week only
        found = self.app.action('search_ask', {'query': 'what did Andrea say last week?', 'plan': {'person': andrea, **LAST_WEEK}}, owner_dashboard=True)
        self.assertEqual(self.plans, [])  # no first turn: it knows who and when
        self.assertIn('The rollout slips to Thursday.', self.prompts[-1])
        self.assertTrue(found['answer'])
        self.assertIn('search_ask_examples', a.DASHBOARD_ACTIONS)
        self.assertIn('search_ask_examples', a.OWNER_ACTIONS)

    def test_not_a_question_takes_one_small_turn(self):
        self.plan = {'question': False, 'person': 'Andrea', 'said_by': 'both', 'from': None, 'to': None, 'about': ''}
        self.assertEqual(self.ask('andrea vale invoices'), {'none': True})
        self.assertEqual((len(self.plans), self.prompts), (1, []))


if __name__ == '__main__':
    unittest.main()
