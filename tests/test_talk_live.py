"""Talk live (talk_live.py): the session the Gateway makes, the offer handed on once, the limit, the transcript in the
to-do's chat, the read-only tools, and approving one draft by voice (a confirm question, then a clear yes). OpenAI and the Gateway never run here: talk-live-run.mjs is stubbed."""
import importlib.util
import datetime as dt
import json
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import dashboard_parts

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('talk_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
t = a.talk_live

SID = 'a' * 16
SECRET = 'ek_test_secret_never_shown'
OFFER = 'v=0\r\no=- 1 2 IN IP4 127.0.0.1\r\n'
ANSWER = 'v=0\r\no=- 3 4 IN IP4 127.0.0.1\r\n'


class Gateway:
    """Stands in for talk-live-run.mjs: what it was asked, and what it answers."""

    def __init__(self, ready=True, start=None, offer=None):
        self.calls, self.ready = [], ready
        self.answers = {'start': start or {'secret': SECRET, 'offer_url': 'https://api.openai.com/v1/realtime/calls',
                                           'offer_headers': {}, 'voice_session_id': 'vs1', 'model': 'gpt-realtime-2.1', 'via': 'key'},
                        'offer': offer or {'sdp': ANSWER}, 'end': {'ok': True}}

    def __call__(self, command, **kwargs):
        request = json.loads(kwargs['input'])
        self.calls.append(request)
        self.answers['status'] = {'ready': self.ready, 'model': 'gpt-realtime-2.1'}
        return subprocess.CompletedProcess(command, 0, json.dumps(self.answers[request['method']]), '')


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class Sessions(unittest.TestCase):
    def setUp(self):
        self.gateway, self.clock = Gateway(), Clock()
        self.talk = t.Talk({'_node': 'node'}, runner=self.gateway, clock=self.clock)

    def test_the_helper_is_asked_for_its_own_session_only(self):
        started = self.talk.start(SID, {})
        self.assertEqual(self.gateway.calls[-1], {'method': 'start', 'session_key': t.SESSION_PREFIX + SID, 'voice': 'cedar'})
        self.assertNotIn(SECRET, json.dumps(started))   # the browser gets an ID, never the secret
        self.assertEqual(started['via'], 'key')
        self.assertRegex(started['id'], '^[a-f0-9]{16}$')

    def test_status_is_kept_ten_minutes(self):
        self.assertIsNone(self.talk.status({}))
        self.assertEqual(self.talk.status({}, True, wait=True), {'ready': True, 'model': 'gpt-realtime-2.1'})
        self.gateway.ready = False
        self.assertTrue(self.talk.status({}, True, wait=True)['ready'])
        self.clock.now += 601
        self.assertFalse(self.talk.status({}, True, wait=True)['ready'])

    def test_status_never_waits_on_openclaw(self):
        slow, done = threading.Event(), threading.Event()

        def runner(command, **kwargs):
            slow.wait(5)
            done.set()
            return subprocess.CompletedProcess(command, 0, json.dumps({'ready': True}), '')
        talk = t.Talk({}, runner=runner, clock=self.clock)
        began = time.monotonic()
        self.assertIsNone(talk.status({}, True))   # not known yet: the answer comes in the background
        self.assertIsNone(talk.status({}, True))   # and only one question at a time
        self.assertLess(time.monotonic() - began, 0.5)
        slow.set()
        done.wait(5)
        for _ in range(50):
            if talk.status({}):
                break
            time.sleep(0.02)
        self.assertTrue(talk.status({})['ready'])

    def test_the_offer_goes_once_with_the_secret(self):
        talk_id = self.talk.start(SID, {})['id']
        self.assertEqual(self.talk.offer(talk_id, OFFER, {}), {'sdp': ANSWER})
        sent = self.gateway.calls[-1]
        self.assertEqual((sent['method'], sent['secret'], sent['sdp']), ('offer', SECRET, OFFER))
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, OFFER, {})   # a second offer would let anyone with the ID take the session over

    def test_a_bad_offer_or_answer_ends_it(self):
        talk_id = self.talk.start(SID, {})['id']
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, 'not sdp', {})
        self.gateway.answers['offer'] = {'error': 'unavailable', 'reason': 'auth'}
        with self.assertRaisesRegex(ValueError, 'couldn’t connect'):
            self.talk.offer(talk_id, OFFER, {})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.talk.get(talk_id)
        self.assertEqual(self.gateway.calls[-1]['method'], 'end')

    def test_one_per_to_do_and_two_in_all(self):
        first = self.talk.start(SID, {})['id']
        with self.assertRaisesRegex(ValueError, 'already open for this to-do'):
            self.talk.start(SID, {})
        self.talk.start('b' * 16, {})
        with self.assertRaisesRegex(ValueError, 'Two live conversations'):
            self.talk.start('c' * 16, {})
        self.talk.end(first, {})
        self.talk.start('c' * 16, {})
        with self.assertRaises(ValueError):
            self.talk.start('../../etc', {})

    def test_ten_minutes_and_then_it_is_gone(self):
        talk_id = self.talk.start(SID, {})['id']
        self.clock.now += t.LIMIT_SECONDS + t.GRACE_SECONDS - 1
        self.talk.get(talk_id)   # a last line just after the end still counts
        self.clock.now += 2
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.talk.get(talk_id)
        self.talk.sweep()
        self.assertEqual(self.talk.open, {})   # its secret with it
        self.assertEqual((t.LIMIT_SECONDS, t.WARN_SECONDS), (600, 540))

    def test_gateway_errors_say_what_to_do(self):
        self.gateway.answers['start'] = {'error': 'unavailable', 'reason': 'auth'}
        with self.assertRaisesRegex(ValueError, 'Check OpenAI in OpenClaw'):
            self.talk.start(SID, {})
        self.gateway.answers['start'] = {'error': 'unavailable', 'reason': 'timeout'}
        with self.assertRaisesRegex(ValueError, 'couldn’t start. Try again'):
            self.talk.start(SID, {})
        broken = t.Talk({}, runner=lambda *x, **y: (_ for _ in ()).throw(OSError()), clock=self.clock)
        with self.assertRaisesRegex(ValueError, 'couldn’t start'):
            broken.start(SID, {})


class Tools(unittest.TestCase):
    def test_it_ends_itself_after_a_goodbye_and_lets_an_okay_be(self):
        # Like a person on the phone: an "all right" needs no paragraph back, a filler before a tool once at most, and
        # a clear goodbye ends the call (end_talk, which the page handles like End)
        end = [x for x in t.TOOLS if x['name'] == 'end_talk'][0]
        self.assertIn('the same as the owner pressing End', end['description'])
        self.assertIn('end_talk', [x['name'] for x in t.MAIN_TOOLS])
        for text in (t.instructions('Reply to Lotte', 'en', 'Thursday'), t.main_instructions('en', 'Thursday')):
            self.assertIn('only acknowledges or fills a pause', text)
            self.assertIn('Say one word at most, or nothing, and wait for them.', text)
            self.assertIn('Before a tool call, say one short line at most', text)
            self.assertIn('say one short goodbye and call end_talk', text)

    def test_reading_tools_the_chat_and_a_confirmed_send(self):
        names = [tool['name'] for tool in t.TOOLS]
        self.assertEqual(names, ['todo_details', 'find_todos', 'ask_chat', 'create_todo', 'todo_action', 'undo_last_action', 'read_draft', 'ask_to_send', 'send_answer',
                                 'send_status', 'undo_send', 'report_bug', 'end_talk'])
        self.assertIn('never sends', [tool for tool in t.TOOLS if tool['name'] == 'ask_chat'][0]['description'])
        self.assertIn('a clear yes to your confirm question', t.ASK_NOTE)

    def test_a_todos_own_talk_marks_it_done_itself(self):
        # Jeroen, by voice in the payroll to-do's chat: "mark this as done" went to the chat, which only offered Mark done
        # buttons. Its own Talk marks it done (the owner's own decision), and a sound is never a wrap-up.
        action = t.TOOL['todo_action']
        self.assertEqual(action['parameters']['properties']['action']['enum'], ['mark_done', 'dismiss', 'snooze', 'reopen'])
        self.assertNotIn('id', action['parameters']['properties'])
        self.assertIn('"mark this as done"', action['description'])
        text = t.instructions('Check the payroll', 'en', 'Thursday', ['en', 'nl'])
        self.assertIn('call todo_action and say what it returns', text)
        self.assertIn('Never hand that to the chat.', text)
        self.assertIn('never a goodbye or a wrap-up: ask what they meant', text)
        self.assertNotIn('marked done) or looked', text)
        self.assertNotIn('—', text)

    def test_talk_sees_every_open_todo_and_starts_with_what_needs_the_owner(self):
        # Jeroen, live: "let's go through the to-dos" said nothing needs him while one was still Preparing. Talk sees
        # them all, starts with ready and to decide, says how many are preparing, and keeps it short.
        text = t.main_instructions('en', 'Thursday')
        for words in ('It has every open to-do and its state', 'how many are still preparing', 'you’ll tell them when one is ready',
                      'There is no draft to send yet.', 'Never say there is nothing before you’ve checked list_todos',
                      'one or two sentences', 'Don’t list options'):
            self.assertIn(words, text)
        listing = [x for x in t.MAIN_TOOLS if x['name'] == 'list_todos'][0]['description']
        for words in ('All the owner’s open to-dos', 'preparing', 'waiting on others', 'snoozed', 'its state'):
            self.assertIn(words, listing)
        find = [x for x in t.MAIN_TOOLS if x['name'] == 'find_todos'][0]['parameters']
        self.assertEqual(find['properties']['state']['enum'], list(t.STATES) + ['done', 'dismissed'])
        self.assertNotIn('required', find)   # by state only: "anything preparing?"

    def test_new_things_become_a_new_todo_not_the_focused_chat(self):
        # Jeroen, live: "create a new to-do: plan a trip to Antwerp" went into another to-do's chat
        create = [x for x in t.MAIN_TOOLS if x['name'] == 'create_todo'][0]
        self.assertEqual(create['parameters']['required'], ['title'])
        self.assertIn('Nothing is sent', create['description'])
        self.assertIn('Only for a real question or instruction about this to-do.', [x for x in t.MAIN_TOOLS if x['name'] == 'ask_chat'][0]['description'])
        for text in (t.instructions('Reply to Lotte', 'en', 'Thursday'), t.main_instructions('en', 'Thursday')):
            self.assertIn('ask_chat is only for this to-do. Never hand it a request about something else.', text)
            self.assertIn('create it right away. Ask one short question at most', text)

    def test_asking_the_chat_says_one_line_and_never_polls(self):
        text = t.instructions('Pick up the paint', 'en', 'Thursday 29 October 2026, 12:39')
        self.assertIn('never poll', text)
        self.assertIn('comes to you as a message', text)
        self.assertNotIn('call todo_details a little later', text)
        self.assertIn('Looking that up', t.ASK_NOTE)
        self.assertIn('{answer}', t.DONE_NOTE)
        self.assertTrue(t.RELAY_PREFIX.startswith('chat-'))   # still a chat turn (the short follow-up prompt)
        for words in ('web', 'browser', 'where you found it'):
            self.assertIn(words, t.RELAY_NOTE)

    def test_the_instructions_send_only_after_a_question(self):
        text = t.instructions('Reply to Dana', 'nl', 'Tuesday 28 October 2026, 10:00')
        self.assertIn('"Reply to Dana"', text)
        self.assertIn('Speak Dutch', text)
        self.assertIn('call ask_to_send. If it says the owner has seen or heard this draft, only ask its question; otherwise '
                      'read the draft out in full first.', text)
        self.assertIn('call send_answer right away, without saying anything first', text)
        self.assertIn('never say something was sent unless a tool says so', text)
        self.assertIn('Never read the same draft twice.', text)
        self.assertIn('call read_draft and read out what it gives you, word for word', text)
        self.assertIn('ask the question again in a few words, without reading the draft again', text)

    def test_talk_never_claims_what_no_tool_did_and_routes_its_own_commands(self):
        # Jeroen, live: "report a bug" became a to-do with "it's filed and being looked into"; "do it" marked a to-do
        # done; "move on to the next one" went to a to-do's chat; "azk" became a new to-do
        for text in (t.instructions('Reply to Dana', 'en', 'Thursday'), t.main_instructions('en', 'Thursday')):
            for words in ('Never say something happened (sent, filed, done, started, reported) unless a tool result says it did.',
                          'call report_bug, never create_todo', 'If it was unclear or a single odd word, say "Sorry, say that again?" and do nothing.',
                          'call undo_send at once', '"Ask again" means ask_chat again with the same request.'):
                self.assertIn(words, text)
        main = t.main_instructions('en', 'Thursday')
        for words in ('"Do it", "go ahead and do it", "handle it", "start it", "continue": call do_it.',
                      '"I did it": todo_action mark_done.', 'Never say you can’t use the browser.', 'call undo_last_action',
                      'open the next to-do only when it says ok', 'never ask_chat. "Stop" or "leave it" means do nothing more on it.',
                      'call ask_to_send_all'):
            self.assertIn(words, main)
        tools = {x['name']: x for x in t.MAIN_TOOLS}
        self.assertNotIn('do_it', t.TODO_ACTIONS)
        self.assertIn('"go ahead and do it", "handle it", "start it", "continue"', tools['do_it']['description'])
        self.assertIn('Not for "mark it done", "it’s done" or "I did it"', tools['do_it']['description'])
        self.assertIn('browser work included', tools['do_it']['description'])
        self.assertIn('never for "do it"', tools['todo_action']['description'])
        self.assertIn('Never for "ask again", "report a bug"', tools['create_todo']['description'])
        self.assertIn('Never for moving between to-dos', tools['ask_chat']['description'])
        self.assertIn('ask once whether to add a support report', tools['report_bug']['description'])
        self.assertEqual(tools['report_bug']['parameters']['required'], ['summary'])
        self.assertIn('never read it out from here', t.TOOL['todo_details']['description'])
        self.assertIn('Work only on this to-do', t.RELAY_NOTE)
        for note in (t.DONE_NOTE, t.STOPPED_NOTE):
            self.assertIn('{title}', note)
        self.assertIn('{request}', t.STOPPED_NOTE)
        self.assertIn('never create_todo', t.STOPPED_NOTE)

    def test_the_instructions_sound_like_a_conversation(self):
        text = t.instructions('Reply to Dana', 'en', 'Tuesday 28 October 2026, 10:00')
        for section in ('# Personality and tone', '## Length', '## Pacing', '## Variety', '# Tools and rules'):
            self.assertIn(section, text)   # labeled sections, as OpenAI's Realtime prompting guide suggests
        for words in ('contractions', 'Don’t repeat the same sentence', 'Don’t read its title out word for word',
                      'Don’t read out lists', 'Never rushed', 'say it again'):
            self.assertIn(words, text)
        self.assertIn('Read it in full, word for word', text)   # a draft asked about is still read out whole
        self.assertNotIn('—', text)

    def test_the_voice_plays_a_little_quicker_never_rushed(self):
        self.assertTrue(1.05 <= t.SPEED <= 1.15)

    def test_the_instructions_keep_replies_single_and_without_dashes(self):
        for text in (t.instructions('Reply to Dana', 'en', 'now', ['en', 'nl']), t.main_instructions('en', 'now', ['en', 'nl'])):
            self.assertIn('One reply per turn, said once', text)
            self.assertIn('No em dashes or en dashes', text)
            self.assertIn('If you already said it', text)              # the chat's answer isn't restated
            self.assertIn('The owner speaks English or Dutch', text)   # noise and other languages get no answer
            self.assertNotIn('—', text)
        self.assertIn('don’t repeat it', t.DONE_NOTE)

    def test_the_owner_is_heard_in_their_own_languages(self):
        self.assertEqual(t.spoken('en', '', 'en-BE', ['en-US', 'nl-BE', 'nl', 'ko']), ['en', 'nl'])
        self.assertEqual(t.spoken('pt-BR', None, None, []), ['pt'])
        self.assertEqual(t.spoken(None, '', None, ['ko-KR', 'th']), ['en'])   # nothing the app speaks: English
        self.assertEqual(len(t.spoken('en', 'nl', 'fr-BE', ['de', 'es'])), 3)
        one = t.transcription(['nl'])
        self.assertEqual((one['model'], one['language']), ('gpt-4o-transcribe', 'nl'))   # one language: pinned
        two = t.transcription(['en', 'nl'])
        self.assertNotIn('language', two)                     # pinning one would garble a sentence in the other
        self.assertIn('English or Dutch', two['prompt'])
        self.assertEqual(t.transcription_next(['en', 'nl']), {'model': 'gpt-transcribe', 'languages': ['en', 'nl']})
        self.assertIn(t.NOISE['type'], ('near_field', 'far_field'))
        self.assertEqual((t.TURN['type'], t.TURN['eagerness']), ('semantic_vad', 'low'))

    def test_the_question_names_who_and_how(self):
        self.assertEqual(t.question({'kind': 'email', 'subject': 'Re: Offsite'}, 'Dana'), 'Send this reply to Dana by email?')
        self.assertEqual(t.question({'kind': 'slack'}, 'Robin'), 'Send this message to Robin on Slack?')
        self.assertEqual(t.question({'kind': 'whatsapp', 'reply': True}, 'Sam'), 'Send this reply to Sam on WhatsApp?')

    def test_only_a_clear_yes_in_the_owners_languages_counts(self):
        # Jeroen, live: "Jasne." and "Ja, ist gut, das endet." (noise, transcribed as Polish and German) sent a draft.
        # The Machine judges the owner's own words itself: plain yes words and fillers only, in their languages.
        yes = lambda text, langs=('en', 'nl'): t.clear_answer(text, langs, ['Dana'])
        for text in ('Yes, send it.', 'yes, send it', 'Ok, send it.', 'Ja, verstuur maar.', 'Ja.', 'Go ahead.', 'Yep',
                     'Yes, send it to Dana.', 'Oké, doe maar.', 'Yes please', 'Sure, send them all.'):
            self.assertEqual(yes(text), 'yes', text)
        for text in ('Jasne.', 'Ja, ist gut, das endet.', 'Ja ist gut das endet', 'yes but change X', 'Yes, but change the date.',
                     'Hmm, maybe, what did it say again?', 'Yes?', '', 'Send it to Kim instead.', 'Oui, envoie-le'):
            self.assertEqual(yes(text), 'unclear', text)
        for text in ('no', 'No.', 'Nee, wacht even.', 'Wait.', 'Don’t send it.', 'Stop'):
            self.assertEqual(yes(text), 'no', text)
        self.assertEqual(yes('Oui, envoie-le', ['en', 'fr']), 'yes')       # their language, when they speak it
        self.assertEqual(yes('Ja, ist gut.', ['de']), 'yes')



TOKEN = 'test-token'


class Api(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = self.store, TOKEN, threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'database': str(Path(temp.name) / 'events.sqlite'),
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        self.gateway = Gateway()
        self.app._talk = t.Talk({}, runner=self.gateway)
        self.app._talk.status({}, True, wait=True)
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       (SID, 'Reply to Dana about the offsite', 'Reply to Dana about the offsite', 'pending', '2026-10-28T09:00:00Z'))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       ('b' * 16, 'Book the offsite venue', 'Book the offsite venue', 'pending', '2026-10-28T09:00:00Z'))
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       ('c' * 16, 'Old offsite invoice', 'Old offsite invoice', 'completed', '2026-10-01T09:00:00Z'))

    def act(self, name, args):
        return self.app.action(name, args, owner_dashboard=True)

    DRAFT = {'kind': 'email', 'label': 'Reply to Dana', 'to': ['dana@example.com'], 'to_name': 'Dana Reyes', 'from': 'me@example.com',
             'subject': 'Re: Offsite', 'body': 'Hi Dana, Thursday works. See you then.', 'account_id': 'mail', 'revision': 'r1'}

    def ready_draft(self, **change):
        draft = {**self.DRAFT, **change}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), SID))
        return draft

    READ = 'To Dana, re Offsite: Hi Dana, Thursday works. See you then. '

    def asked(self, answer=None, spoken=READ + 'Send this reply to Dana by email?'):
        """A conversation where the voice read out the draft, asked to send it, and the owner answered."""
        self.ready_draft()
        talk_id = self.act('talk_start', {'suggestion_id': SID, 'languages': ['en-US', 'nl-BE']})['id']   # English and Dutch
        asked = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})
        if spoken:
            self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': spoken})
        if answer:
            self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': answer})
        return talk_id, asked

    def jobs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT status,source,approval_id,retry_at,revision FROM action_jobs')]

    def test_yes_after_the_question_sends_that_one_draft(self):
        talk_id, asked = self.asked('Ja, verstuur maar.')
        self.assertEqual(asked['question'], 'Send this reply to Dana by email?')
        self.assertEqual(asked['draft']['to'], ['Dana'])
        self.assertEqual(asked['revision'], 'r1')
        self.assertTrue(asked['say'].endswith('Send this reply to Dana by email?'))
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'queued')
        jobs = self.jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual((jobs[0]['status'], jobs[0]['source'], jobs[0]['revision'], jobs[0]['approval_id']), ('queued', 'voice', 'r1', sent['approval_id']))
        self.assertGreater(jobs[0]['retry_at'], a.now())       # held for Undo: the outbox doesn't take it yet
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT choice,source FROM decisions").fetchall()[0][:], ('send', 'voice'))
        # One yes, one draft: the question is used up
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')
        self.assertEqual(len(self.jobs()), 1)

    def test_the_chat_shows_approved_by_voice_with_undo(self):
        talk_id, _ = self.asked('Yes, send it.')
        approval = self.act('talk_send', {'id': talk_id})['approval_id']
        line = [i for i in self.app.card_chat(SID)['items'] if i.get('text') == 'Approved by voice']
        self.assertEqual(len(line), 1)
        self.assertEqual(line[0]['undo_voice'], approval)
        self.assertTrue(line[0]['mine'])
        self.assertEqual(self.act('talk_undo', {'suggestion_id': SID, 'approval_id': approval}), {'status': 'cancelled'})
        self.assertEqual(self.jobs()[0]['status'], 'cancelled')
        with self.assertRaisesRegex(ValueError, 'Nothing to undo'):
            self.act('talk_undo', {'suggestion_id': SID, 'approval_id': 'voice:other'})
        # A new yes for the same draft after Undo waits again
        self.act('talk_end', {'id': talk_id})
        talk_id, _ = self.asked('Yes, now send it.')
        again = self.act('talk_send', {'id': talk_id})
        self.assertEqual(again['status'], 'queued')
        job = self.jobs()[0]
        self.assertEqual((job['status'], job['approval_id']), ('queued', again['approval_id']))
        self.assertGreater(job['retry_at'], a.now())

    # Talk (the main conversation): not tied to one to-do; it works on the one on screen (talk_focus)

    def test_talk_goes_through_the_todos_with_its_own_tools_and_limit(self):
        started = self.act('talk_start', {'main': True})
        self.assertTrue(started['main'])
        self.assertEqual(self.gateway.calls[-1]['session_key'], t.SESSION_PREFIX + 'main')
        self.assertEqual((started['limit'], started['warn']), (1800, 1740))   # OpenAI allows 60 minutes
        self.assertEqual([x['name'] for x in started['tools']],
                         ['list_todos', 'open_todo', 'todo_details', 'find_todos', 'search', 'open_record', 'calendar', 'machine_status',
                          'ask_chat', 'create_todo', 'do_it', 'todo_action', 'undo_last_action', 'ask_machine', 'read_draft',
                          'ask_to_send', 'ask_to_send_all', 'send_answer', 'send_status', 'undo_send', 'report_bug', 'end_talk'])
        action = [x for x in started['tools'] if x['name'] == 'todo_action'][0]['parameters']['properties']['action']['enum']
        self.assertFalse([x for x in action if 'send' in x or 'approve' in x])   # a to-do's buttons, never a send
        for words in ('Start with list_todos', 'One to-do at a time', 'never say something was sent unless a tool says so',
                      'call ask_to_send. If it says the owner has seen or heard this draft', 'never poll', 'contractions'):
            self.assertIn(words, started['instructions'])
        self.assertIn('{title}', started['notes']['new'])
        self.assertIn('was preparing is ready now', started['notes']['ready'])   # told once when a preparing one is ready
        self.assertIn('Sorry, say that again?', started['notes']['again'])
        # words that keep not coming through: said once, plainly, what's wrong (never a loop of "say that again")
        self.assertIn('check their microphone or type in the chat', started['notes']['unheard'])
        self.assertIn('don’t say it again', started['notes']['unheard'])
        self.assertNotIn('\u2014', started['notes']['unheard'])
        self.assertNotIn(SECRET, json.dumps(started))
        with self.assertRaisesRegex(ValueError, 'Talk is already open'):
            self.act('talk_start', {'main': True})
        # A to-do's own conversation can still open next to it
        self.assertTrue(self.act('talk_start', {'suggestion_id': SID})['id'])

    def test_the_page_status_says_whether_talk_can_show(self):
        self.assertIs(self.app.talk_ready(), True)   # known (setUp asked): the sidebar's Talk shows
        self.app._talk = t.Talk({}, runner=Gateway(ready=False))
        self.app._talk.status({}, True, wait=True)
        self.assertIs(self.app.talk_ready(), False)

    def test_talk_reads_only_the_todo_it_opened(self):
        talk_id = self.act('talk_start', {'main': True})['id']
        self.assertIn('error', self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output'])
        found = self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': {'words': 'offsite'}})['output']['todos']
        self.assertEqual({x['id'] for x in found}, {SID, 'b' * 16})   # ids, so it can open one
        with self.assertRaisesRegex(ValueError, 'Unknown suggestion'):
            self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'f' * 16})
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'b' * 16})
        self.assertEqual(self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output']['title'], 'Book the offsite venue')
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'}))   # nothing to send there

    def test_finding_todos_by_state_says_each_ones_state(self):
        with self.store.connect() as db:
            for sid, title, status, extra in (('d' * 16, 'Plan the Antwerp trip', 'accepted', ''), ('e' * 16, 'Send the quote to Kim', 'prepared', ''),
                                              ('f' * 16, 'Review the deck', 'prepared', '{"state":"waiting"}'), ('0' * 16, 'Call the bank', 'snoozed', '')):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,outcome) VALUES(?,?,?,'','[]','[]',?,?,?)",
                           (sid, title, title, status, '2026-10-28T10:00:00Z', extra or None))
        talk_id = self.act('talk_start', {'main': True})['id']
        find = lambda **args: self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': args})['output']
        self.assertEqual([(x['title'], x['state']) for x in find(state='preparing')['todos']], [('Plan the Antwerp trip', 'preparing')])
        self.assertEqual(find(state='preparing')['todos'][0]['id'], 'd' * 16)
        # "do you see something that's preparing?": no title has the word, so the state it names
        self.assertEqual([x['title'] for x in find(words='preparing')['todos']], ['Plan the Antwerp trip'])
        self.assertEqual([x['state'] for x in find(state='waiting on others')['todos']], ['waiting on others'])
        self.assertEqual([x['title'] for x in find(state='snoozed')['todos']], ['Call the bank'])
        everything = [x['state'] for x in find(words='the')['todos']]   # what needs the owner first, the dashboard's order
        self.assertEqual(everything, sorted(everything, key=t.STATES.index))
        self.assertEqual(find(state='nonsense'), {'todos': []})
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'd' * 16})
        self.assertEqual(self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output']['state'], 'preparing')

    def graph_people(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES('email:dana@client.example','person','Dana Reyes',3,"
                       "'2026-10-27T15:00:00Z',4,?)", (json.dumps({'role': 'Head of Events', 'org': 'org:client.example'}),))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:client.example','org','Client Example',2,3,?)",
                       (json.dumps({'domain': 'client.example'}),))
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:sam@other.example','person','Sam Lane',1,1,'{}')")
            db.execute("INSERT INTO graph_links(a,b,kind,strength) VALUES('email:dana@client.example','org:client.example','works_at',1)")

    def test_talk_looks_up_people_organizations_and_projects_in_the_graph(self):
        self.graph_people()
        talk_id = self.act('talk_start', {'main': True})['id']
        tool = lambda name, **args: self.act('talk_tool', {'id': talk_id, 'name': name, 'args': args})['output']
        found = tool('search', words='dana')['found']
        self.assertEqual([(x['id'], x['kind'], x['name']) for x in found], [('email:dana@client.example', 'person', 'Dana Reyes')])
        self.assertEqual([x['kind'] for x in tool('search', words='client', kind='organization')['found']], ['organization'])
        self.assertEqual(tool('search', words='dana', kind='project')['found'], [])
        self.assertIn('error', tool('search', words=' '))
        record = tool('open_record', id='email:dana@client.example')
        self.assertEqual((record['kind'], record['name']), ('person', 'Dana Reyes'))
        self.assertEqual(record['card'], {'kind': 'person', 'title': 'Dana Reyes', 'line': record.get('about') or record.get('headline') or '',
                                          'node': 'email:dana@client.example'})   # what Talk's transcript shows
        self.assertNotIn('info', record)
        for wrong in ('', 'team:x', 'email:nobody@example.com', 'promise:x'):
            self.assertIn('error', tool('open_record', id=wrong), wrong)
        # The focused to-do stays the same, and a to-do's own conversation doesn't have these
        self.assertIn('error', self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output'])
        own = self.act('talk_start', {'suggestion_id': SID})['id']
        with self.assertRaisesRegex(ValueError, 'Unknown tool'):
            self.act('talk_tool', {'id': own, 'name': 'search', 'args': {'words': 'dana'}})

    def test_talk_reads_the_calendar_and_opens_a_meeting(self):
        cal = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
        self.app.config['accounts'] = [cal]
        today = dt.datetime.now(a.local_tz()).replace(hour=14, minute=30, second=0, microsecond=0)
        raw = {'id': 'pilot', 'summary': 'Pilot review with Dana', 'status': 'confirmed', 'location': 'Zoom', 'description': 'Agenda: the offsite',
               'start': {'dateTime': today.isoformat()}, 'end': {'dateTime': (today + dt.timedelta(minutes=45)).isoformat()},
               'attendees': [{'email': 'owner@example.com', 'self': True, 'responseStatus': 'accepted'}, {'email': 'dana@client.example'}]}
        self.store.commit_page('cal', {}, [a.calendar_event(cal, raw, str(a.local_tz()))])
        talk_id = self.act('talk_start', {'main': True})['id']
        tool = lambda name, **args: self.act('talk_tool', {'id': talk_id, 'name': name, 'args': args})['output']
        day = tool('calendar')
        self.assertEqual((day['count'], day['days']), (1, 1))
        meeting = day['meetings'][0]
        self.assertEqual((meeting['title'], meeting['where']), ('Pilot review with Dana', 'Zoom'))
        self.assertTrue(meeting['when'].endswith('14:30') and meeting['until'] == '15:15', meeting)
        self.assertEqual(tool('calendar', day=(today + dt.timedelta(days=1)).date().isoformat())['meetings'], [])
        self.assertEqual(tool('calendar', day=(today - dt.timedelta(days=1)).date().isoformat(), days=3)['count'], 1)
        self.assertIn('error', tool('calendar', day='tomorrow'))
        record = tool('open_record', id=meeting['id'])
        self.assertEqual((record['kind'], record['title'], record['with']), ('meeting', 'Pilot review with Dana', ['dana@client.example']))
        self.assertNotIn('Agenda', json.dumps(record))   # what the Calendar shows, not the invite's private notes
        self.assertEqual(record['card']['event'], int(meeting['id'].split(':')[1]))
        self.assertIn('error', tool('open_record', id='event:999999'))
        found = tool('search', words='pilot review', kind='meeting')['found']
        self.assertEqual([(x['id'], x['kind'], x['title']) for x in found], [(meeting['id'], 'meeting', 'Pilot review with Dana')])
        self.assertEqual(tool('search', words='pilot review', kind='message')['found'], [])

    def test_ask_machine_hands_off_to_a_new_todos_chat_that_never_sends(self):
        self.assertEqual(t.ASK_PREFIX, 'chat-voice-')
        self.assertTrue(t.ASK_PREFIX.startswith('chat-') and not t.ASK_PREFIX.startswith(t.RELAY_PREFIX))
        self.assertIn('never send', t.ASK_MACHINE_NOTE)
        source = (ROOT / 'assistant.py').read_text()
        self.assertIn("startswith(talk_live.ASK_PREFIX):request['message']+='\\n\\n'+talk_live.RELAY_NOTE+'\\n'+talk_live.ASK_MACHINE_NOTE", source)
        with self.store.connect() as db:   # the owner's request shows in that to-do's chat as theirs
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('chat-voice-1',?,'other',"
                       "'Who is Dana again?','dashboard','2026-10-29T12:39:00Z')", (SID,))
        said = [i['text'] for i in self.act('card_chat', {'suggestion_id': SID})['items'] if i['kind'] == 'you']
        self.assertEqual(said, ['Who is Dana again?'])
        text = t.main_instructions('en', 'Thursday 29 October 2026, 10:00')
        for words in ('# The rest of the Machine', 'ask_machine, never ask_chat', 'Never guess about someone', 'calendar for meetings'):
            self.assertIn(words, text)
        self.assertNotIn('—', text)
        tools = {x['name']: x for x in t.MAIN_TOOLS}
        self.assertIn('never send', tools['ask_machine']['description'])
        self.assertEqual(set(t.MACHINE_TOOLS) & {x['name'] for x in t.TOOLS}, set())   # only the main conversation has them

    def test_talk_reaches_done_and_dismissed_todos(self):
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='rejected' WHERE id=?", ('b' * 16,))
            for rid, sid, choice, at in (('d1', 'c' * 16, 'complete', '2026-10-02T09:00:00Z'), ('d2', 'b' * 16, 'reject', '2026-10-28T11:00:00Z')):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,'','dashboard',?)", (rid, sid, choice, at))
        talk_id = self.act('talk_start', {'main': True})['id']
        find = lambda **args: self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': args})['output']
        self.assertEqual([(x['title'], x['state']) for x in find(state='done')['todos']], [('Old offsite invoice', 'done')])
        self.assertEqual([(x['title'], x['state']) for x in find(state='dismissed')['todos']], [('Book the offsite venue', 'dismissed')])
        self.assertEqual([x['title'] for x in find(words='anything dismissed')['todos']], ['Book the offsite venue'])
        # Open ones first: a closed one only when no open one matches, latest closed first
        self.assertEqual([x['state'] for x in find(words='offsite')['todos']], ['to decide'])
        self.assertEqual([(x['title'], x['state']) for x in find(words='venue')['todos']], [('Book the offsite venue', 'dismissed')])
        self.assertEqual([x['id'] for x in find(words='invoice')['todos']], ['c' * 16])
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'c' * 16})   # it can open one for its details
        self.assertEqual(self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output']['state'], 'done')

    def test_talk_keeps_what_was_said_in_each_todos_chat(self):
        talk_id = self.act('talk_start', {'main': True})['id']
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'You have two that need you.'})
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': SID})
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Dana asks if Thursday works.'})
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'b' * 16})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Snooze the venue one.'})
        with self.store.connect() as db:
            dana, venue = t.lines(db, SID), t.lines(db, 'b' * 16)
        self.assertEqual([(i['kind'], i['text']) for i in dana], [('event', 'Talked live'), ('reply', 'Dana asks if Thursday works.')])
        self.assertEqual([(i['kind'], i['text']) for i in venue], [('event', 'Talked live'), ('you', 'Snooze the venue one.')])

    def test_talk_sends_one_draft_by_voice_under_the_same_rules(self):
        self.ready_draft()
        talk_id = self.act('talk_start', {'main': True})['id']
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')   # nothing open, nothing asked
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': SID})
        asked = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})
        self.assertEqual(asked['question'], 'Send this reply to Dana by email?')
        self.assertTrue(asked['say'].startswith(t.SAY['read']))
        # The owner opens another to-do before answering: the question is dropped, nothing goes
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': 'b' * 16})
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Send this reply to Dana by email?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')
        self.assertEqual(self.jobs(), [])
        # Back on Dana's: asked, a clear yes, that one draft waits with Undo, and the chat says so
        self.act('talk_focus', {'id': talk_id, 'suggestion_id': SID})
        self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': self.READ + 'Send this reply to Dana by email?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes, send it.'})
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'queued')
        self.assertEqual([(j['source'], j['revision']) for j in self.jobs()], [('voice', 'r1')])
        self.assertTrue([i for i in self.app.card_chat(SID)['items'] if i.get('text') == 'Approved by voice'])
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')   # one yes, one draft

    def test_talk_ends_after_its_own_limit(self):
        talk = t.Talk({}, runner=Gateway(), clock=Clock())
        main = talk.start(None, {})['id']
        own = talk.start(SID, {})['id']
        talk.clock.now += t.LIMIT_SECONDS + t.GRACE_SECONDS + 1
        talk.get(main)
        with self.assertRaisesRegex(ValueError, 'ended'):
            talk.get(own)
        talk.clock.now += t.MAIN_LIMIT_SECONDS
        with self.assertRaisesRegex(ValueError, 'ended'):
            talk.get(main)

    def test_the_voice_and_the_undo_bar_count_the_same_seconds(self):
        # Jeroen, live: the voice said "in ten seconds" while the bar counted "in 5 s". Both come from the outbox's own
        # hold now (the job's retry_at): the seconds left when the yes went through, in the say and for the bar.
        talk_id, _ = self.asked('Yes.')
        sent = self.act('talk_send', {'id': talk_id})
        with self.store.connect() as db:
            held = db.execute('SELECT retry_at FROM action_jobs').fetchone()[0]
        left = (dt.datetime.fromisoformat(held) - dt.datetime.fromisoformat(a.now())).total_seconds()
        self.assertLessEqual(abs(sent['undo_ms'] / 1000 - left), 1.5)
        self.assertLessEqual(sent['undo_ms'], t.UNDO_SECONDS * 1000)
        self.assertIn('Say only: "Sending in %d seconds. Say undo to stop it."' % sent['undo_seconds'], sent['say'])
        self.assertIn('not sent yet', sent['say'])

    def test_is_it_sent_comes_from_the_outbox_never_a_guess(self):
        # Jeroen, live: "Is it sent?" got "I can't confirm it's sent yet", then "Probably, yes... I can't say for sure
        # from here". send_status reads the outbox row: waiting with the seconds left, going out, sent at a time, or not.
        talk_id, _ = self.asked('Yes.')
        tool = lambda **args: self.act('talk_tool', {'id': talk_id, 'name': 'send_status', 'args': args})['output']
        self.assertEqual(tool()['state'], 'none')    # asked, not yet answered: nothing sent from this to-do
        approval = self.act('talk_send', {'id': talk_id})['approval_id']
        waiting = tool()
        self.assertEqual(waiting['state'], 'waiting')
        self.assertTrue(0 < waiting['seconds_left'] <= t.UNDO_SECONDS)
        self.assertIn('Not sent yet: it goes out to Dana in %d seconds' % waiting['seconds_left'], waiting['say'])
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET retry_at='2000-01-01T00:00:00+00:00'")
        self.assertEqual(tool()['state'], 'sending')
        self.assertIn('hasn’t confirmed it yet', tool()['say'])
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='sent',updated_at='2026-10-31T11:42:00+00:00'")
        with patch.object(a, 'local_tz', return_value=dt.timezone(dt.timedelta(hours=1))):
            sent = tool(approval_id=approval)
        self.assertEqual((sent['state'], sent['time'], sent['to']), ('sent', '12:42', 'Dana'))
        self.assertEqual(sent['say'], 'Sent to Dana at 12:42. Say exactly that.')
        self.assertEqual(tool(approval_id='voice:other')['state'], 'none')
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='failed',error='The mailbox refused it.'")
        failed = tool()
        self.assertEqual((failed['state'], failed['why']), ('failed', 'The mailbox refused it.'))
        self.assertIn('It didn’t go out to Dana: The mailbox refused it.', failed['say'])
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='uncertain'")
        self.assertIn('without guessing', tool()['say'])
        # The voice is told to use it, and the page's notes say "Sent." once the outbox confirms it
        for text in (t.instructions('Reply to Dana', 'en', 'Thursday'), t.main_instructions('en', 'Thursday')):
            self.assertIn('call send_status and say what it returns', text)
            self.assertIn('Never guess ("probably", "I can’t say from here")', text)
        notes = self.act('talk_start', {'main': True})['notes']
        self.assertTrue(notes['sent'].endswith('Say only: "Sent."'))
        self.assertIn('{why}', notes['not_sent'])

    def test_talk_says_results_plainly_without_narration(self):
        # Jeroen, live: "Got it, thanks for confirming. Let me finish that step now." before the send went through
        for text in (t.instructions('Reply to Dana', 'en', 'Thursday'), t.main_instructions('en', 'Thursday')):
            self.assertIn('never "thanks for confirming", "let me finish that step"', text)

    def test_undo_is_too_late_once_the_wait_is_over(self):
        talk_id, _ = self.asked('Yes.')
        approval = self.act('talk_send', {'id': talk_id})['approval_id']
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET retry_at='2000-01-01T00:00:00+00:00'")
        with self.assertRaisesRegex(ValueError, 'already on its way'):
            self.act('talk_undo', {'suggestion_id': SID, 'approval_id': approval})
        self.assertNotIn('undo_voice', [i for i in self.app.card_chat(SID)['items'] if i.get('text') == 'Approved by voice'][0])

    # Read once, seen counts: the owner approves what they saw or heard, and never hears the same draft twice

    def test_read_then_yes_sends_without_a_second_reading(self):
        # Jeroen, live: Talk read the draft, then ask_to_send read it again and wanted another yes
        self.ready_draft()
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        read = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1', 'read': True})
        self.assertEqual(read['draft']['text'], 'Hi Dana, Thursday works. See you then.')
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': self.READ + 'Send this reply to Dana by email?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'No, hold on.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'no')
        asked = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})    # "ok, send it now": heard, so only the question
        self.assertTrue(asked['seen'])
        self.assertNotIn('text', asked['draft'])
        self.assertTrue(asked['say'].startswith(t.SAY['seen']))
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Send it to Dana?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued')

    def test_read_then_the_draft_changed_reads_it_again(self):
        self.ready_draft()
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1', 'read': True})
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': self.READ})
        self.ready_draft(body='Hi Dana, Friday works instead. See you then.')       # same revision, other words
        asked = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})
        self.assertNotIn('seen', asked)
        self.assertEqual(asked['draft']['text'], 'Hi Dana, Friday works instead. See you then.')
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Send this reply to Dana by email?'})   # not read out
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_read')
        self.assertEqual(self.jobs(), [])

    def test_a_draft_seen_on_screen_sends_without_reading(self):
        self.ready_draft()
        shown = {'suggestion_id': SID, 'revision': 'r1', 'to': ['dana@example.com'], 'subject': 'Re: Offsite', 'body': self.DRAFT['body']}
        self.assertEqual(self.act('draft_seen', {**shown, 'body': 'Something else'}), {'ok': False})   # not what is there
        self.assertEqual(self.act('draft_seen', shown), {'ok': True})
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        asked = self.act('talk_ask_send', {'id': talk_id})
        self.assertTrue(asked['seen'])
        self.assertNotIn('text', asked['draft'])
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Send this reply to Dana by email?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Ok, send it.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued')

    def test_a_draft_changed_after_it_was_seen_is_read_out(self):
        self.ready_draft()
        self.act('draft_seen', {'suggestion_id': SID, 'revision': 'r1', 'to': ['dana@example.com'], 'subject': 'Re: Offsite', 'body': self.DRAFT['body']})
        self.ready_draft(body='Hi Dana, Friday it is.')
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        asked = self.act('talk_ask_send', {'id': talk_id})
        self.assertEqual(asked['draft']['text'], 'Hi Dana, Friday it is.')
        self.assertTrue(asked['say'].startswith(t.SAY['read']))

    def batch(self):
        """Three ready to-dos, one draft each: Dana's and Kim's seen on screen, Robin's not."""
        drafts = {SID: {**self.DRAFT}, 'b' * 16: {**self.DRAFT, 'to': ['kim@example.com'], 'to_name': 'Kim Lee', 'body': 'Hi Kim, booked.', 'revision': 'r2'},
                  'd' * 16: {**self.DRAFT, 'kind': 'slack', 'to': ['U1'], 'to_name': 'Robin', 'subject': '', 'body': 'Robin, the deck is in the folder now.', 'revision': 'r3'}}
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'','[]','[]',?,?)",
                       ('d' * 16, 'Deck for Robin', 'Deck for Robin', 'pending', '2026-10-28T09:00:00Z'))
            for sid, d in drafts.items():
                db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(d), sid))
        for sid in (SID, 'b' * 16):
            d = drafts[sid]
            self.assertEqual(self.act('draft_seen', {'suggestion_id': sid, 'revision': d['revision'], 'to': d['to'], 'subject': d['subject'], 'body': d['body']}), {'ok': True})
        return list(drafts)

    def test_send_all_reads_only_the_unseen_one_and_one_yes_sends_each(self):
        ids = self.batch()
        talk_id = self.act('talk_start', {'main': True})['id']
        asked = self.act('talk_ask_send', {'id': talk_id, 'ids': ids})
        self.assertEqual(asked['question'], 'Send all 3, to Dana, Kim and Robin?')
        self.assertEqual([('text' in d) for d in asked['drafts']], [False, False, True])
        self.assertTrue(asked['say'].startswith(t.SAY['read_some']))
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'To Robin on Slack: Robin, the deck is in the folder now. Send all 3, to Dana, Kim and Robin?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes, send them all.'})
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'queued')
        self.assertEqual([x['suggestion_id'] for x in sent['sent']], ids)
        self.assertEqual([x['to'] for x in sent['sent']], ['Dana', 'Kim', 'Robin'])   # Talk's Undo bar says who
        self.assertEqual(sent['sent'][2]['kind'], 'slack')
        jobs = self.jobs()
        self.assertEqual(sorted(j['revision'] for j in jobs), ['r1', 'r2', 'r3'])
        self.assertTrue(all(j['status'] == 'queued' and j['source'] == 'voice' and j['retry_at'] > a.now() for j in jobs))
        self.assertEqual(len({j['approval_id'] for j in jobs}), 3)        # each its own approval and Undo
        # Undo (spoken or tapped) cancels the batch: each one still waiting
        for x in sent['sent']:
            self.assertEqual(self.act('talk_undo', x), {'status': 'cancelled'})
        self.assertEqual({j['status'] for j in self.jobs()}, {'cancelled'})

    def test_send_all_waits_for_the_unseen_one_to_be_read(self):
        ids = self.batch()
        talk_id = self.act('talk_start', {'main': True})['id']
        self.act('talk_ask_send', {'id': talk_id, 'ids': ids})
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Send all 3, to Dana, Kim and Robin?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_read')
        self.assertEqual(self.jobs(), [])
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'ids': ids + ['e' * 16, 'f' * 16, '0' * 16]}))   # at most 5

    def test_yes_without_a_question_sends_nothing(self):
        self.ready_draft()
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Thursday after two works for Dana.'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes, send it.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')
        self.assertEqual(self.jobs(), [])

    def test_a_question_not_yet_spoken_or_answered_waits(self):
        talk_id, _ = self.asked(spoken=None)
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes'})   # before the question was even asked
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'not_asked')
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': self.READ + 'Send this reply to Dana by email?'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'no_answer')
        self.assertEqual(self.jobs(), [])
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Go ahead.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued')

    def test_a_draft_changed_after_the_question_asks_again(self):
        talk_id, _ = self.asked('Yes, send it.')
        self.ready_draft(body='Hi Dana, Friday works instead.', revision='r2')
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'changed')
        self.assertIn('ask_to_send again', sent['say'])
        self.assertEqual(self.jobs(), [])
        # The same revision with other words or recipients is a change too
        self.act('talk_end', {'id': talk_id})
        talk_id2, _ = self.asked('Yes.')
        self.ready_draft(to=['someone@example.com'])
        self.assertEqual(self.act('talk_send', {'id': talk_id2})['status'], 'changed')
        self.assertEqual(self.jobs(), [])

    def test_an_unclear_answer_asks_again_without_reading_again(self):
        talk_id, _ = self.asked('Ja, ist gut, das endet.')
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'unclear')
        self.assertIn('Don’t read the draft again', sent['say'])
        self.assertIn('Say yes to send it to Dana.', sent['say'])
        self.assertEqual(self.jobs(), [])
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'no_answer')   # the question waits for a new answer
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': 'Say yes to send it to Dana.'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued')

    def test_garbled_or_partial_answers_never_send(self):
        for answer in ('Jasne.', 'Ja ist gut das endet', 'yes but change X'):
            talk_id, _ = self.asked(answer)
            self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'unclear', answer)
            self.act('talk_end', {'id': talk_id})
        talk_id, _ = self.asked('no')
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'no')
        self.assertEqual(self.jobs(), [])
        for answer in ('yes, send it', 'ja, verstuur maar', 'Ok, send it.'):
            self.act('talk_end', {'id': talk_id})
            talk_id, _ = self.asked(answer)
            self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued', answer)
            with self.store.connect() as db:
                db.execute('DELETE FROM action_jobs')
                db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (SID,))

    def test_no_sends_nothing(self):
        talk_id, _ = self.asked('Nee, wacht even.')
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'no')
        self.assertEqual(self.jobs(), [])

    def test_a_question_without_who_it_goes_to_is_not_one(self):
        talk_id, _ = self.asked('Yes', spoken='Shall I send it?')
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'unclear')
        self.assertEqual(self.jobs(), [])

    def test_only_a_ready_draft_to_named_people(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'}))      # nothing prepared
        self.ready_draft(to_options=['a@example.com', 'b@example.com'])
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'}))      # who gets it is picked on screen
        self.ready_draft(kind='merge')
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'}))
        self.ready_draft()
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'revision': 'old'}))     # not the draft on screen
        read = self.act('talk_ask_send', {'id': talk_id, 'revision': 'r1'})
        self.assertTrue(read['say'].startswith('First read the draft below out in full: who it goes to, the subject'))
        self.assertEqual(read['draft'], {'to': ['Dana'], 'how': 'by email', 'subject': 'Re: Offsite', 'text': 'Hi Dana, Thursday works. See you then.'})

    def test_without_the_screen_the_machine_picks_the_draft_and_pins_it(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id}))      # nothing prepared
        self.ready_draft(to=['dana@example.com', 'kim@example.com'], to_name='')
        asked = self.act('talk_ask_send', {'id': talk_id})   # no card on screen: its only draft, read out whole
        self.assertEqual(asked['revision'], 'r1')
        self.assertEqual(asked['draft']['to'], ['dana@example.com', 'kim@example.com'])   # every recipient, read out
        self.assertIn('Hi Dana, Thursday works.', asked['draft']['text'])
        self.act('talk_line', {'id': talk_id, 'role': 'assistant', 'text': self.READ + 'Send this reply to dana@example.com and 1 more by email?'})
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Yes.'})
        self.assertEqual(self.act('talk_send', {'id': talk_id})['status'], 'queued')
        self.assertEqual(self.jobs()[0]['revision'], 'r1')   # the revision it pinned, nothing else

    def test_more_than_one_draft_is_asked_by_its_number(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        two = {'kind': 'menu', 'actions': [self.DRAFT, {**self.DRAFT, 'label': 'Reply to Kim', 'to': ['kim@example.com'], 'to_name': 'Kim', 'revision': 'r9'}]}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(two), SID))
        which = self.act('talk_ask_send', {'id': talk_id})
        self.assertIn('more than one draft', which['error'])
        self.assertEqual(which['drafts'], [{'draft': 1, 'label': 'Reply to Dana'}, {'draft': 2, 'label': 'Reply to Kim'}])
        self.assertEqual(self.act('talk_ask_send', {'id': talk_id, 'draft': 2})['revision'], 'r9')
        self.assertIn('error', self.act('talk_ask_send', {'id': talk_id, 'draft': 5}))

    def test_an_old_question_expires(self):
        talk_id, _ = self.asked('Yes, send it.')
        self.app._talk.open[talk_id]['confirm']['at'] -= (t.ASK_SECONDS + 1) * 1000
        sent = self.act('talk_send', {'id': talk_id})
        self.assertEqual(sent['status'], 'expired')
        self.assertIn('Call ask_to_send again and ask once more', sent['say'])
        self.assertEqual(self.jobs(), [])

    def test_the_voice_cannot_approve_through_the_normal_controls(self):
        self.ready_draft()
        with self.assertRaisesRegex(ValueError, 'owner’s controls'):
            self.act('confirm_action', {'suggestion_id': SID, 'revision': 'r1', 'approval_id': 'voice:x y'})

    def test_only_the_owner_on_the_dashboard(self):
        for name in sorted(a.TALK_ACTIONS):
            with self.assertRaisesRegex(ValueError, 'Only the owner'):
                self.app.action(name, {})
        self.assertLessEqual(a.TALK_ACTIONS, a.DASHBOARD_ACTIONS)
        self.assertLessEqual(a.TALK_ACTIONS, a.OWNER_ACTIONS)

    def test_a_conversation_from_start_to_end(self):
        self.assertEqual(self.act('talk_status', {}), {'ready': True, 'limit': 600, 'warn': 540})
        started = self.act('talk_start', {'suggestion_id': SID})
        self.assertNotIn(SECRET, json.dumps(started))
        self.assertEqual((started['limit'], started['warn'], started['per_use']), (600, 540, True))
        self.assertEqual([tool['name'] for tool in started['tools']], [x['name'] for x in t.TOOLS])
        self.assertIn('Reply to Dana about the offsite', started['instructions'])
        self.assertEqual(self.act('talk_offer', {'id': started['id'], 'sdp': OFFER}), {'sdp': ANSWER})
        self.act('talk_line', {'id': started['id'], 'role': 'user', 'text': 'What does Dana want?'})
        self.act('talk_line', {'id': started['id'], 'role': 'assistant', 'text': 'She asks if  Thursday works.'})
        self.assertEqual(self.act('talk_end', {'id': started['id']}), {'ok': True})
        self.assertEqual(self.gateway.calls[-1], {'method': 'end', 'session_key': t.SESSION_PREFIX + SID, 'voice_session_id': 'vs1'})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.act('talk_line', {'id': started['id'], 'role': 'user', 'text': 'Too late'})
        with self.store.connect() as db:
            said = t.lines(db, SID)
        self.assertEqual([(i['kind'], i['text']) for i in said],
                         [('event', 'Talked live'), ('you', 'What does Dana want?'), ('reply', 'She asks if Thursday works.')])
        self.assertTrue(all(i['at'] for i in said))

    def test_the_voice_is_cedar_unless_the_owner_picks_another(self):
        started = self.act('talk_start', {'suggestion_id': SID})
        self.assertEqual((started['voice'], self.gateway.calls[-1]['voice']), ('cedar', 'cedar'))
        self.assertEqual(started['speed'], t.SPEED)            # the page sets it in session.update
        self.assertEqual(started['turn'], {'type': 'semantic_vad', 'eagerness': 'low', 'create_response': True, 'interrupt_response': True})
        self.assertNotIn('speed', self.gateway.calls[-1])      # talk.client.create takes no speed
        self.assertEqual(started['noise'], {'type': 'far_field'})
        self.assertEqual(started['transcription']['model'], 'gpt-4o-transcribe')
        self.assertEqual(started['transcription_next'], {'model': 'gpt-transcribe', 'languages': started['languages']})
        self.assertEqual(started['languages'][0], 'en')
        self.act('talk_end', {'id': started['id']})
        started = self.act('talk_start', {'suggestion_id': SID, 'languages': ['en-US', 'nl-BE', 7, 'x' * 99]})
        self.assertEqual(started['languages'], ['en', 'nl'])   # the browser's languages, checked
        self.assertIn('English or Dutch', started['instructions'])
        self.assertNotIn('language', started['transcription'])
        self.act('talk_end', {'id': started['id']})
        saved = self.act('voice_prefs', {'talk_voice': 'marin'})
        self.assertEqual(saved['talk_voice'], 'marin')
        self.assertIn('ready', saved['talk'])   # Settings keeps its Talk live and Voice rows after a change
        with self.assertRaisesRegex(ValueError, 'Pick one of the voices'):
            self.act('voice_prefs', {'talk_voice': 'cove'})   # ChatGPT's Cove isn't a Realtime voice
        self.assertEqual(self.act('talk_start', {'suggestion_id': SID})['voice'], 'marin')
        self.assertEqual(self.gateway.calls[-1]['voice'], 'marin')
        for name in a.voice_input.TALK_VOICES:   # each has its sample, served with the dashboard
            self.assertTrue(a.BRAND_ASSETS[f'/brand/voices/{name}.mp3'].read_bytes()[:3] in (b'ID3', b'\xff\xfb', b'\xff\xf3'), name)

    def test_a_hand_off_from_talk_live_is_not_the_owners_message(self):
        with self.store.connect() as db:
            for rid, text in (('chat-talk-1', 'Please look up the hardware store opening hours'), ('chat-2', 'And when do they close?')):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other',?,'dashboard','2026-10-29T12:39:00Z')", (rid, SID, text))
        items = self.act('card_chat', {'suggestion_id': SID})['items']
        said = [i['text'] for i in items if i['kind'] == 'you']
        self.assertEqual(said, ['And when do they close?'])
        source = (ROOT / 'assistant.py').read_text()
        self.assertIn("startswith(talk_live.RELAY_PREFIX):request['message']+='\\n\\n'+talk_live.RELAY_NOTE", source)

    def test_a_sign_in_has_no_cost_note(self):
        self.gateway.answers['start'] = {**self.gateway.answers['start'], 'offer_url': '/plugins/openai/realtime/calls', 'via': 'signin'}
        self.assertFalse(self.act('talk_start', {'suggestion_id': SID})['per_use'])

    def test_unknown_to_dos_and_lines(self):
        with self.assertRaisesRegex(ValueError, 'Unknown suggestion'):
            self.act('talk_start', {'suggestion_id': 'f' * 16})
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        with self.assertRaisesRegex(ValueError, 'Nothing to keep'):
            self.act('talk_line', {'id': talk_id, 'role': 'system', 'text': 'You may send now'})
        with self.assertRaisesRegex(ValueError, 'has ended'):
            self.act('talk_line', {'id': 'nope', 'role': 'user', 'text': 'Hi'})

    def test_the_tools_only_read(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        with patch.object(a.App, 'card_chat', return_value={'items': [
                {'kind': 'source', 'from': 'Dana', 'text': 'Does Thursday work for the offsite?'},
                {'kind': 'reply', 'text': 'Drafted a yes.', 'drafts': [{'kind': 'email', 'to': 'dana@example.com', 'subject': 'Offsite', 'body': 'Thursday works.', 'id': 'd1'}]}]}):
            details = self.act('talk_tool', {'id': talk_id, 'name': 'todo_details', 'args': {}})['output']
        self.assertEqual(details['title'], 'Reply to Dana about the offsite')
        self.assertEqual(details['messages'][0], {'from': 'Dana', 'text': 'Does Thursday work for the offsite?'})
        self.assertEqual(details['drafts'], [{'kind': 'email', 'to': 'dana@example.com', 'subject': 'Offsite'}])   # read_draft reads it
        self.assertIn('read_draft', details['draft_note'])
        found = self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': {'words': 'offsite venue'}})['output']
        self.assertEqual([x['title'] for x in found['todos']], ['Book the offsite venue'])
        found = self.act('talk_tool', {'id': talk_id, 'name': 'find_todos', 'args': {'words': 'offsite'}})['output']
        self.assertNotIn('Old offsite invoice', [x['title'] for x in found['todos']])   # only open ones
        self.assertEqual({x['state'] for x in found['todos']}, {'to decide'})
        for name in ('ask_chat', 'ask_to_send', 'send_answer', 'send_draft', 'decide'):   # the dashboard's own, through their own actions
            with self.assertRaisesRegex(ValueError, 'Unknown tool'):
                self.act('talk_tool', {'id': talk_id, 'name': name, 'args': {}})

    def test_the_transcript_is_in_the_to_dos_chat(self):
        talk_id = self.act('talk_start', {'suggestion_id': SID})['id']
        self.act('talk_line', {'id': talk_id, 'role': 'user', 'text': 'Draft a yes for Thursday'})
        with self.store.connect() as db:
            items = t.lines(db, SID)
        self.assertEqual(items[0]['text'], 'Talked live')
        self.assertTrue(items[0]['mine'])
        self.assertEqual(items[1]['via'], 'live')
        with self.store.connect() as db:   # nothing in the decisions: talking never decides
            self.assertEqual(db.execute('SELECT count(*) FROM decisions').fetchone()[0], 0)


class Sealed(unittest.TestCase):
    def test_what_was_said_is_sealed_at_rest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'events.sqlite'
            store = a.Store(path, protect=True)
            talk = t.Talk({}, runner=Gateway())
            talk_id = talk.start(SID, {})['id']
            with store.connect() as db:
                talk.line(db, talk_id, 'user', 'Tell Quinzel the zebra code', 1)
            raw = b''.join(f.read_bytes() for f in Path(temp).iterdir() if f.is_file())
            self.assertNotIn(b'zebra code', raw)
            with store.connect() as db:
                self.assertEqual(t.lines(db, SID)[1]['text'], 'Tell Quinzel the zebra code')


class Dashboard(unittest.TestCase):
    def test_asking_the_chat_never_sends(self):
        html = dashboard_parts.assemble(ROOT)
        self.assertIn('${micBtn()}${talkBtn()}', html)
        # What the voice asks goes to the chat the way a typed message does: a decision 'other', never a send or Approve
        start, end = html.index('async function talkAsk('), html.index("document.addEventListener('click',async e=>{const b=e.target.closest('[data-voice-undo]')")
        body = html[start:end]
        self.assertIn("choice:'other'", body)
        for word in ('approve', 'send_draft', "'accept'", 'deliver', 'confirm_action'):
            self.assertNotIn(word, body)
        # The page only passes a voice yes on to the Machine (talk_send), which judges it; never confirm_action itself
        start = html.index('async function talkAskSend(')
        voice = html[start:html.index('// What the voice asks the chat', start)]
        self.assertIn("'talk_send'", voice)
        self.assertNotIn('confirm_action', voice)

    def test_the_helper_never_asks_to_write(self):
        helper = (ROOT / 'talk-live-run.mjs').read_text()
        self.assertIn("scopes: ['operator.read', 'operator.talk']", helper)
        self.assertNotIn('operator.write', helper.replace('never operator.write', ''))
        self.assertNotIn('operator.admin', helper)


if __name__ == '__main__':
    unittest.main()
