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
from machine.app import ask_memory, search_ask as app_ask  # noqa: E402

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


def notes(days_ago, title, body, account='work', people=()):
    n = next(tg.counter)
    return {'account_id': account, 'source_id': f'n{n}', 'kind': 'meeting.notes', 'occurred_at': tg.at(days_ago), 'title': title, 'body': body,
            'deleted': False, 'metadata': {'attendees': list(people)}}


class AskMemory(unittest.TestCase):
    """What Ask reads besides messages (machine/app/ask_memory.py): promises, facts, a summary and meeting notes that
    match the question, each cited as what it is, fitted to the prompt, logged, and only of the area in view."""
    add, build, setUp, ask = tg.Graph.add, tg.Graph.build, SearchAsk.setUp, SearchAsk.ask
    KIM = 'email:kim@initech.example'

    def event(self, title):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE title=?', (title,)).fetchone()[0]

    def log(self):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute("SELECT kind,row_id,how,chars,score FROM memory_use WHERE purpose='ask' ORDER BY id")]

    def memory(self, prompt=None):
        """The part of the prompt that is not messages: '' when nothing matched."""
        prompt = self.prompts[-1] if prompt is None else prompt
        return prompt.split(ask_memory.INTRO, 1)[1].rsplit('\nQuestion: <<<', 1)[0] if ask_memory.INTRO in prompt else ''

    def fact(self, text, **more):
        """A fact from a note the owner wrote on a to-do."""
        if not getattr(self, 'noted', None):
            self.noted = self.store.suggest('other', 'Pay the vendor', 'Body', [self.event('Lunch')])['id']
            self.store.decide(self.noted, 'reject', 'we stopped using them', 'owner-note', 'dashboard')
        return self.store.remember_fact(text, 'owner-note', **more)

    def about_kim(self, **more):
        self.plan = {'question': True, 'person': 'Kim Vale', 'said_by': 'both', 'from': None, 'to': None, 'about': '', **more}

    def test_nothing_matches_and_the_prompt_is_the_one_it_was(self):
        self.fact('The owner flies on Tuesdays.')  # no embeddings here: no fact by meaning
        self.store.promise({'direction': 'theirs', 'event_id': self.event('Lunch'), 'who': 'Lee Park', 'what': 'book the table'})
        found = self.ask('what did kim say about the pilot?', 'work')
        self.assertNotIn('memory', found)
        self.assertEqual(self.memory(), '')
        with mock.patch.object(app_ask.ask_memory, 'read', return_value=('', {})):
            self.ask('what did kim say about the pilot?', 'work')
        self.assertEqual(self.prompts[0], self.prompts[1])  # the same text as without the blocks
        self.assertEqual({'signal'}, {r[0] for r in self.log()})
        self.assertEqual(self.ask('what did zephyr quoxx say'), {'none': True})  # nothing found at all: still no turn
        self.assertEqual(len(self.prompts), 2)

    def test_a_promise_in_a_found_message_is_cited_as_a_promise(self):
        made = self.store.promise({'direction': 'theirs', 'event_id': self.event('Pilot timing'), 'who': 'Kim Vale', 'what': 'send the new pilot plan',
                                   'due': '2026-10-20'})
        self.reply = 'Kim promised the new pilot plan by October 20 [P1], after moving the pilot to March [1].'
        found = self.ask('what did kim say about the pilot?', 'work')
        self.assertEqual(found['answer'], 'Kim promised the new pilot plan by October 20, after moving the pilot to March.')
        self.assertEqual([s['title'] for s in found['sources']], ['Pilot timing'])  # the message stays a message
        self.assertEqual([(m['type'], m['id'], m['title'], m['from'], m['state']) for m in found['memory']],
                         [('promise', made['id'], 'send the new pilot plan', 'Kim Vale', 'open')])
        self.assertIn('[P1] Promise by Kim Vale to the owner, open, due 2026-10-20, said 2026-10-14: <<<send the new pilot plan>>>', self.memory())
        self.assertLess(self.prompts[-1].index('[1] gmail from Kim Vale'), self.prompts[-1].index(ask_memory.INTRO))
        row = next(r for r in self.log() if r[0] == 'promise')
        self.assertEqual(row[:3], ('promise', str(made['id']), 'search'))
        self.assertEqual(row[3], len(self.memory().strip()))  # the characters of its line, never its text
        self.reply = 'It is in [P4] and [F1].'  # a tag its prompt never had is no source
        self.assertNotIn('memory', self.ask('what did kim say about the pilot?', 'work'))

    def test_a_question_about_a_person_gets_their_promises_and_summary(self):
        self.add(work_mail(40, 'Kim Vale <kim@initech.example>', 'Old contract', 'I will send the signed contract.'),
                 work_mail(50, 'Kim Vale <kim@initech.example>', 'Older still', 'I will send the logo.'),
                 work_mail(1, 'Sam <sam@acme.example>', 'Re: Pilot timing', 'I will confirm the March dates.', thread='tsent'))
        self.build()
        open_one = self.store.promise({'direction': 'theirs', 'event_id': self.event('Old contract'), 'who': 'Kim Vale', 'what': 'send the signed contract'})
        gone = self.store.promise({'direction': 'theirs', 'event_id': self.event('Older still'), 'who': 'Kim Vale', 'what': 'send the logo'})
        self.store.promise({'id': gone['id'], 'status': 'kept', 'reason': 'The logo came in', 'event_ids': [self.event('Older still')]})
        self.store.promise({'direction': 'theirs', 'event_id': self.event('Lunch'), 'who': 'Lee Park', 'what': 'book the table'})  # someone else's
        with self.store.connect() as db:
            a.person_summary.save(db, self.KIM, [{'kind': 'now', 'text': 'Moving the pilot to March with the budget unchanged.',
                                                 'sources': [f"E{self.event('Pilot timing')}"]}], tg.NOW.isoformat(), {'work': 'work', 'chat': 'personal'})
        self.about_kim()
        self.reply = 'Kim still owes the signed contract [P1] and is moving the pilot to March [S1].'
        found = self.ask('what is open with kim vale?', 'work')
        text = self.memory()
        self.assertIn('<<<send the signed contract>>>', text)
        self.assertIn(', kept, no date, said', text)  # closed in the last 30 days: still told, as kept
        self.assertNotIn('book the table', text)
        self.assertIn('Summary of Kim Vale', text)
        self.assertIn('<<<Moving the pilot to March with the budget unchanged.>>>', text)
        self.assertEqual([(m['type'], m['id']) for m in found['memory']], [('promise', open_one['id']), ('person', self.KIM)])
        self.assertEqual(found['memory'][1]['title'], 'Kim Vale')
        log = self.log()
        self.assertEqual({('promise', str(open_one['id']), 'about'), ('promise', str(gone['id']), 'about'), ('record', self.KIM, 'about')},
                         {r[:3] for r in log if r[0] != 'signal'})
        with self.store.connect() as db:  # closed longer ago than CLOSED_DAYS: no longer brought up
            db.execute('UPDATE promises SET updated_at=? WHERE id=?', (tg.at(ask_memory.CLOSED_DAYS + 1), gone['id']))
        self.ask('what is open with kim vale?', 'work')
        self.assertNotIn('send the logo', self.memory())
        self.about_kim(**{'from': '2026-10-01', 'to': '2026-10-16'})  # a question about some days: the ones said in them
        self.ask('what did kim vale promise this month?', 'work')
        self.assertNotIn('send the signed contract', self.memory())

    def test_facts_on_a_named_organization_and_by_meaning(self):
        self.build()
        tied = self.fact('Initech renews for eight seats in January.', about=['org:initech.example'])
        self.fact('The owner flies on Tuesdays.')
        self.fact('Kim Vale takes calls after ten.', about=[self.KIM])  # on one of its people: read too, after its own
        self.reply = 'Initech renews for eight seats in January [F1].'
        found = self.ask('how many seats does initech renew for?', 'work')
        self.assertEqual([(m['type'], m['id'], m['title']) for m in found['memory']], [('fact', tied['id'], 'Initech renews for eight seats in January.')])
        self.assertEqual(found['sources'], [])
        self.assertIn('[F1] Learned 2026-10-16: <<<Initech renews for eight seats in January.>>>', self.memory())
        self.assertIn('[F2] Learned 2026-10-16: <<<Kim Vale takes calls after ten.>>>', self.memory())
        self.assertNotIn('Tuesdays', self.memory())
        self.assertIn(('fact', str(tied['id']), 'about'), [r[:3] for r in self.log()])
        with self.store.connect() as db:
            self.assertEqual(2, db.execute('SELECT count(*) FROM facts WHERE used_at IS NOT NULL').fetchone()[0])  # read for a question: used
        # By meaning: the question's vector against each fact's, one local embedding request, no model turn
        self.app.config = {**CONFIG, 'embeddings': {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}}
        close = self.fact('Flights are booked through the travel desk.')
        vector = lambda t: [1.0, 0.0] if 'travel desk' in t or 'book a flight' in t else [0.3, 0.954] if 'Tuesdays' in t else [0.0, 1.0]
        with mock.patch.object(a.embeddings, 'embed', side_effect=lambda settings, texts, timeout=120: [vector(t) for t in texts]) as embed, \
                mock.patch.object(a.embeddings, 'related', side_effect=a.embeddings.EmbeddingError('down')):
            self.ask('how do i book a flight here?', 'work')
            self.assertEqual(embed.call_count, 1)
        self.assertIn('travel desk', self.memory())
        self.assertNotIn('Initech renews', self.memory())  # far from the question, and it names no Initech
        self.assertNotIn('Tuesdays', self.memory())  # 0.3: under FACT_FLOOR... a fact has to be about the question
        row = [r for r in self.log() if r[0] == 'fact'][-1]
        self.assertEqual((row[1], row[2], row[4]), (str(close['id']), 'closeness', 1.0))

    def test_a_project_and_an_organization_named_in_the_question(self):
        pilot = self.event('Pilot timing')
        with self.store.connect() as db:
            graph.save_board(db, {'name': 'Rollouts', 'stages': ['Planned', 'Agreed', 'Live']}, tg.NOW.isoformat())
            node = graph.set_stage(db, 'Northwind rollout', 'Agreed', 'review', tg.NOW.isoformat(), board='Rollouts', reason='Kim agreed to March',
                                   event_id=pilot, next_step='Send the rollout plan')['node_id']
            graph.label(db, [pilot], 'Northwind rollout', 'review', tg.NOW.isoformat())
        self.build()
        with self.store.connect() as db:
            graph.set_role(db, 'org:initech.example', 'customer', 'owner', tg.NOW.isoformat())
        self.reply = 'It is agreed, and the next step is to send the rollout plan [S1].'
        found = self.ask('where does the northwind rollout stand?', 'work')
        self.assertEqual([(m['type'], m['id'], m['title']) for m in found['memory']], [('project', node, 'Northwind rollout')])
        self.assertIn('[S1] Project Northwind rollout: <<<stage Agreed (Kim agreed to March); next step: Send the rollout plan; ', self.memory())
        self.assertIn(('record', node, 'match'), [r[:3] for r in self.log()])
        self.ask('what is new at northwind and initech?', 'work')  # a name's first word, when no other record has it
        self.assertIn('Project Northwind rollout', self.memory())
        self.assertIn('Organization Initech: <<<customer>>>', self.memory())
        self.ask('what is new at northwind and initech?', 'personal')  # known only from Work: not a record of this area
        self.assertEqual(self.memory(), '')
        self.ask('what did they say about the rollout plan?', 'work')  # a word of the name is not the name
        self.assertNotIn('Project Northwind', self.memory())

    def test_meeting_notes_the_search_found(self):
        self.add(notes(3, 'Pilot kickoff', 'Agreed in the room: the pilot starts with twelve seats and Kim owns the rollout plan.'),
                 notes(4, 'Pilot at home', 'The pilot light of the boiler is fixed on Saturday.', account='chat'))
        self.reply = 'The pilot starts with twelve seats [M1].'
        found = self.ask('how many seats does the pilot start with?', 'work')
        self.assertEqual([(m['type'], m['id'], m['title'], m['kind']) for m in found['memory']],
                         [('meeting', self.event('Pilot kickoff'), 'Pilot kickoff', 'meeting.notes')])
        self.assertIn('[M1] Meeting notes, 2026-10-13: Pilot kickoff\n<<<Agreed in the room: the pilot starts with twelve seats', self.memory())
        self.assertNotIn('boiler', self.prompts[-1])  # the other area's notes
        self.assertNotIn('Pilot kickoff', self.prompts[-1].split(ask_memory.INTRO)[0])  # notes are no message
        self.assertIn(('signal', str(self.event('Pilot kickoff')), 'search'), [r[:3] for r in self.log()])
        self.ask('how many seats does the pilot start with?', 'personal')
        self.assertIn('boiler', self.memory())
        self.assertNotIn('twelve seats', self.prompts[-1])

    def test_the_other_areas_memory_never_goes_in(self):
        self.build()
        robin = self.event('Robin Hart')
        self.store.promise({'direction': 'theirs', 'event_id': robin, 'who': 'Robin Hart', 'what': 'bring the pilot photos'})
        self.store.remember_fact('Kim Vale is training for a marathon.', 'ai:1', about=[self.KIM], source='ai:Notes', side='personal')
        self.add(work_mail(1, 'Dr. Ash <ash@clinic.example>', 'Pilot appointment', 'Your pilot appointment is on Monday.', thread='tpriv'))
        with self.store.connect() as db:
            shared_graph.ensure(db)
            row = db.execute("SELECT id,kind,metadata FROM events WHERE title='Pilot appointment'").fetchone()
            db.execute('INSERT INTO share_threads(thread,verdict,at) VALUES(?,?,?)',
                       (shared_graph.thread_of(row['kind'], json.loads(row['metadata']), row['id']), 'personal', tg.NOW.isoformat()))
            a.person_summary.save(db, self.KIM, [{'kind': 'who', 'text': 'Plays in the same tennis club.', 'sources': [f'E{robin}']},
                                                 {'kind': 'now', 'text': 'Moving the pilot to March.', 'sources': [f"E{self.event('Pilot timing')}"]}],
                                  tg.NOW.isoformat(), {'work': 'work', 'chat': 'personal'})
        self.store.promise({'direction': 'theirs', 'event_id': row['id'], 'who': 'Dr. Ash', 'what': 'send the pilot results'})
        self.about_kim(about='pilot')
        self.ask('what about kim vale and the pilot?', 'work')
        for private in ('pilot photos', 'marathon', 'tennis club', 'pilot results'):
            self.assertNotIn(private, self.prompts[-1])
        self.assertIn('Moving the pilot to March.', self.memory())
        self.ask('what about kim vale and the pilot?', None)  # All: the owner's own view of everything
        self.assertIn('marathon', self.memory())
        self.assertIn('tennis club', self.memory())
        self.plan = {'question': True, 'person': None, 'said_by': 'both', 'from': None, 'to': None, 'about': ''}
        self.ask('what is going on with the pilot', 'personal')
        self.assertIn('pilot photos', self.memory())
        self.assertNotIn('Moving the pilot', self.prompts[-1])
        self.ask('what is going on with the pilot', 'work')
        self.assertNotIn('pilot results', self.prompts[-1])  # with Work, never a thread about the owner's own life

    def test_a_promise_goes_with_the_best_messages_only(self):
        self.add(*(work_mail(3 + n, 'Lee Park <lee@initech.example>', f'Pilot part {n}', 'pilot notes') for n in range(6)))
        self.build()
        made = [self.store.promise({'direction': 'theirs', 'event_id': self.event(f'Pilot part {n}'), 'who': 'Lee Park', 'what': f'send pilot part {n}'})['id'] for n in range(6)]
        self.ask('where are the pilot notes?', 'work')
        told = [int(r[1]) for r in self.log() if r[0] == 'promise']
        self.assertTrue(0 < len(told) <= ask_memory.PROMISE_HITS, told)  # not one for each of the messages found
        self.assertTrue(set(told) <= set(made))

    def test_it_fits_the_prompt_and_its_own_share(self):
        self.add(*(work_mail(3 + n, 'Kim Vale <kim@initech.example>', f'Pilot part {n}', 'pilot ' + 'word ' * 400) for n in range(8)))
        self.build()
        for n in range(8):
            self.store.promise({'direction': 'theirs', 'event_id': self.event(f'Pilot part {n}'), 'who': 'Kim Vale', 'what': f'send pilot part {n} ' + 'x' * 60})
            self.fact(f'Initech pilot fact {n}: ' + 'y' * 200, about=['org:initech.example'])
        self.add(notes(1, 'Pilot review', 'pilot ' + 'notes ' * 600), notes(2, 'Pilot retro', 'pilot ' + 'retro ' * 600))
        self.ask('what is the state of the initech pilot?', 'work')
        prompt, text = self.prompts[-1], self.memory()
        self.assertLessEqual(len(prompt), search_ask.PROMPT_CHARS)
        self.assertLessEqual(len(ask_memory.INTRO) + len(text), ask_memory.MEMORY_CHARS)
        self.assertEqual(text.count('[P'), ask_memory.PROMISES)
        self.assertTrue(text.rstrip().endswith('>>>'))  # whole lines only: none cut in the middle
        self.assertIn('[1] gmail from Kim Vale', prompt)  # the messages are still there
        logged = sum(r[3] for r in self.log() if r[0] != 'signal' or r[2] != 'search') + len(ask_memory.INTRO)
        self.assertLessEqual(logged, ask_memory.MEMORY_CHARS)
        with mock.patch.object(app_ask.ask_memory, 'MEMORY_CHARS', 300):  # no room for a block: it stays out whole, and unlogged
            before = len(self.log())
            self.ask('what is the state of the initech pilot?', 'work')
        self.assertLessEqual(len(ask_memory.INTRO) + len(self.memory()), 300)
        self.assertEqual({'signal'}, {r[0] for r in self.log()[before:] if r[2] == 'search'} | {'signal'})


if __name__ == '__main__':
    unittest.main()
