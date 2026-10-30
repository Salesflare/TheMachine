"""Fast for to-do chats (chat_model.py): the person's own choice, off by default, kept in config.json. It goes only with
the turns they wait on in a to-do chat (a message, or a Do it they started there) and only on a model whose provider
has a fast option (OpenAI's API and Codex on a ChatGPT sign-in: service tier priority; Anthropic's API key on Opus:
speed fast). Preparations, work done ahead and a follow-up review's Change never run fast, also with Fast on; a session
that ran fast is set back to standard before its next turn."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import chat_model

spec = importlib.util.spec_from_file_location('chat_fast_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

LEVELS = [{'id': x} for x in ('low', 'medium', 'high')]
# A models.list reply ("configured" view) as OpenClaw 2026.10 gives it, with its fast-mode fields
REPLY = {'models': [
    # OpenAI with an API key (OpenClaw runtime): OpenClaw checks the route itself
    {'provider': 'openai', 'id': 'gpt-6.1-sol', 'name': 'GPT-6.1 Sol', 'available': True, 'thinkingLevels': LEVELS,
     'supportsFastMode': True, 'serviceTierObservation': {'requestedTier': 'priority', 'responseTier': 'default'}},
    # Codex on a ChatGPT sign-in: the account's catalog lists the tiers
    {'provider': 'openai', 'id': 'gpt-6.1-terra', 'name': 'GPT-6.1 Terra', 'available': True, 'thinkingLevels': LEVELS,
     'serviceTiers': ['priority']},
    # Anthropic with an API key: Opus has fast mode (speed fast), Sonnet 5.5 has none
    {'provider': 'anthropic', 'id': 'claude-opus-5-5', 'name': 'Claude Opus 5.5', 'available': True, 'thinkingLevels': LEVELS,
     'supportsFastMode': True},
    {'provider': 'anthropic', 'id': 'claude-sonnet-5-5', 'name': 'Claude Sonnet 5.5', 'available': True, 'thinkingLevels': LEVELS,
     'supportsFastMode': False},
    # A Claude plan through Claude Code: no fast option
    {'provider': 'claude-cli', 'id': 'claude-opus-5-5', 'name': 'Claude Opus 5.5 (Claude CLI)', 'available': True, 'thinkingLevels': LEVELS},
]}


class Catalog(unittest.TestCase):
    def test_which_models_have_a_fast_option(self):
        models = {m['ref']: m for m in chat_model.parse_catalog(REPLY)}
        self.assertEqual({ref: m['fast'] for ref, m in models.items()}, {
            'openai/gpt-6.1-sol': True, 'openai/gpt-6.1-terra': True, 'anthropic/claude-opus-5-5': True,
            'anthropic/claude-sonnet-5-5': False, 'claude-cli/claude-opus-5-5': False})
        # What the provider served when it wasn't what was asked
        self.assertEqual(models['openai/gpt-6.1-sol']['served'], 'default')
        self.assertNotIn('served', models['openai/gpt-6.1-terra'])

    def test_which_turns_are_interactive(self):
        self.assertTrue(chat_model.interactive_turn('chat-1'))
        self.assertTrue(chat_model.interactive_turn('chat-talk-1'))
        self.assertTrue(chat_model.interactive_turn('d1', do_it_source='dashboard'))  # Do it, started in the to-do
        for args in (('chat-1', True), ('chat-1', False, True), ('d1',), ('d1', False, False, 'auto_follow_up'), ('d1', False, False, 'telegram')):
            self.assertFalse(chat_model.interactive_turn(*args), args)


class AppTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.oc = root / 'openclaw.json'
        self.oc.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'openai/gpt-6.1-sol'}, 'thinkingDefault': 'low'}}}))
        self.config_path = root / 'config.json'
        self.config = {'accounts': [], 'database': str(root / 'events.sqlite'), 'openclaw_config': str(self.oc)}
        self.config_path.write_text(json.dumps(self.config))
        self.store = a.Store(root / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}], None)
        self.sid = self.store.suggest('task', 'Reply to the venue', 'I can draft this.', [1])['id']
        self.app = object.__new__(a.App)
        self.app.store, self.app.config, self.app.config_path = self.store, self.config, self.config_path
        self.app.chat_catalog = chat_model.Catalog(reader=lambda config: chat_model.parse_catalog(REPLY, config))

    def turn(self, finish=True):
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted', **({'fast': 'fast' if r['fast'] else 'standard'} if 'fast' in r else {})})
        starts = [c for c in calls if c.get('action') == 'start']
        self.assertEqual(len(starts), 1, calls)
        if finish:
            self.finish()
        return starts[0]

    def finish(self):
        with self.store.connect() as db:  # the run ended; the next message continues the same session
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=?", (a.now(),))
            db.execute("UPDATE preparations SET status='done' WHERE status IN ('starting','running')")

    def say(self, text):
        self.store.decide(self.sid, 'other', text, 'chat-' + a.uuid.uuid4().hex, 'dashboard')
        return self.turn()

    def fast(self, on):
        return self.app.action('chat_fast_set', {'fast': on}, owner_dashboard=True)

    def test_off_by_default_and_saved_per_person(self):
        self.assertFalse(self.app.chat_model_view()['fast'])
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.turn()
        self.assertNotIn('fast', self.say('Shorter please'))
        self.assertTrue(self.fast(True)['fast'])
        self.assertIs(json.loads(self.config_path.read_text())['chat_fast'], True)
        self.assertFalse(self.fast(False)['fast'])
        self.assertIsNone(json.loads(self.config_path.read_text())['chat_fast'])
        with self.assertRaises(ValueError):
            self.app.action('chat_fast_set', {'fast': True}, owner_dashboard=False)
        with self.assertRaises(ValueError):
            self.app.action('chat_fast_set', {'fast': 'yes'}, owner_dashboard=True)
        self.assertIn('chat_fast_set', a.OWNER_ACTIONS)

    def test_chat_turns_are_fast_on_openai_and_anthropic(self):
        self.fast(True)
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.assertNotIn('fast', self.turn())  # the preparation a Do it starts with: not fast
        with self.assertLogs(a.LOG, 'INFO') as logs:
            self.assertIs(self.say('Shorter please')['fast'], True)  # OpenAI, the main model
        self.assertTrue(any('fast=True model=openai/gpt-6.1-sol last_served=default' in x for x in logs.output), logs.output)
        self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'anthropic/claude-opus-5-5'}, owner_dashboard=True)
        start = self.say('And add the date')
        self.assertEqual((start['provider'], start['model'], start['fast']), ('anthropic', 'claude-opus-5-5', True))
        self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'openai/gpt-6.1-terra'}, owner_dashboard=True)
        self.assertIs(self.say('One more change')['fast'], True)  # Codex on a ChatGPT sign-in
        # A model without a fast option: standard, and the session that ran fast is set back first
        for ref in ('anthropic/claude-sonnet-5-5', 'claude-cli/claude-opus-5-5'):
            self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': ref}, owner_dashboard=True)
            start = self.say('Try it here')
            self.assertFalse(start.get('fast'), ref)
        self.assertNotIn('fast', start)  # already standard: no change sent

    def test_background_work_never_runs_fast_also_with_fast_on(self):
        self.fast(True)
        # Prepared ahead: nobody asked yet, so it runs in the background
        sid = self.app.action('suggest', {'dedupe_key': 'ahead', 'title': 'Reply to the caterer', 'body': 'I can draft the reply.',
                                          'event_ids': [1], 'when': 'now', 'prepare_ahead': True})['id']
        start = self.turn()
        self.assertTrue(start.get('background'))
        self.assertNotIn('fast', start)
        # The first preparation after Do it: not a chat turn either
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.assertNotIn('fast', self.turn())
        self.assertIs(self.say('Shorter please')['fast'], True)
        # A follow-up review's Change rewrites drafts in a batch: not a chat turn, and the session that just ran
        # fast is set back to standard before it starts
        self.app.follow_up_change_note = lambda job: '\n\nRewrite it.'
        self.assertIs(self.say('Shorter please')['fast'], False)
        self.assertNotIn('fast', self.say('Shorter still'))  # already standard: nothing to change
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM chat_fast_sessions').fetchone()[0], 0)
        self.assertNotEqual(sid, self.sid)

    def confirm(self, owner_dashboard):
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()['job_id']
        step = {'kind': 'finish', 'label': 'Book the room', 'url': 'https://venue.example.com/book',
                'instructions': 'On https://venue.example.com/book press Book.', 'preview': 'One room, Friday.'}
        self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'Ready to book.', 'next_actions': [step],
                                    'outcome': 'needs_you', 'needs': 'confirm the booking'})
        self.finish()
        with self.store.connect() as db:
            action = a.next_actions.actions(db.execute('SELECT next_action FROM suggestions WHERE id=?', (self.sid,)).fetchone()['next_action'])[0]
        approval = 'owner-tap' if owner_dashboard else 'telegram:tap'
        self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': approval}, owner_dashboard=owner_dashboard)
        return self.turn(finish=False)

    def test_a_do_it_started_in_the_chat_is_fast(self):
        self.fast(True)
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.assertNotIn('fast', self.turn(finish=False))
        self.assertIs(self.confirm(owner_dashboard=True)['fast'], True)  # Do it, tapped in the to-do
        # Confirmed from Telegram: not a turn in the chat; set back to standard after the fast one, never fast itself
        self.assertIs(self.confirm(owner_dashboard=False)['fast'], False)


if __name__ == '__main__':
    unittest.main()
