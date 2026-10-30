"""The model and thinking level for chats (chat_model.py): only what the sign-in offers, each model with its own levels;
the default saved in config.json and one to-do chat's own in the database; both go with the chat's turns, and without
any choice the turns go exactly as before. OpenClaw's own config is never written."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import chat_model

spec = importlib.util.spec_from_file_location('chat_model_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

# A models.list reply as the Gateway gives it ("configured" view), trimmed to what is read
REPLY = {'models': [
    {'id': 'lm-2', 'name': 'LM-2', 'provider': 'acme', 'available': True, 'recommended': True,
     'thinkingLevels': [{'id': x} for x in ('low', 'medium', 'high', 'xhigh', 'max', 'ultra')], 'thinkingDefault': 'low'},
    {'id': 'lm-2-mini', 'name': 'LM-2 Mini', 'provider': 'acme', 'available': True,
     'thinkingLevels': [{'id': 'off'}, {'id': 'low'}, {'id': 'medium'}], 'thinkingDefault': 'off'},
    {'id': 'sonnet', 'name': 'Sonnet', 'provider': 'other', 'available': None,  # no sign-in for this provider
     'thinkingLevels': [{'id': 'off'}, {'id': 'high'}]},
    {'id': 'gemma_4-q4/k', 'name': 'Gemma', 'provider': 'local-llm', 'available': True, 'thinkingLevels': [{'id': 'off'}]},
]}


class Catalog(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.oc = Path(self.temp.name) / 'openclaw.json'
        self.oc.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'acme/lm-2'}, 'thinkingDefault': 'medium'}}}))
        self.config = {'openclaw_config': str(self.oc)}

    def test_only_signed_in_and_allowed_models_with_their_own_levels(self):
        models = chat_model.parse_catalog(REPLY, self.config)
        self.assertEqual([m['ref'] for m in models], ['acme/lm-2', 'acme/lm-2-mini', 'local-llm/gemma_4-q4/k'])
        self.assertEqual(models[0]['levels'], ['low', 'medium', 'high', 'xhigh', 'max', 'ultra'])
        self.assertEqual(models[1]['default'], 'off')
        # An allowlist in OpenClaw's config narrows it the same way it narrows turns
        self.oc.write_text(json.dumps({'agents': {'defaults': {'model': 'acme/lm-2', 'models': {'acme/lm-2-mini': {}}}}}))
        self.assertEqual([m['ref'] for m in chat_model.parse_catalog(REPLY, self.config)], ['acme/lm-2-mini'])
        self.oc.write_text(json.dumps({'agents': {'defaults': {'modelPolicy': {'allow': ['acme/*']}}}}))
        self.assertEqual([m['ref'] for m in chat_model.parse_catalog(REPLY, self.config)], ['acme/lm-2', 'acme/lm-2-mini'])

    def test_the_list_comes_from_the_running_gateway_read_only(self):
        seen = []

        def run(args, **kw):
            seen.append(args)
            return subprocess.CompletedProcess(args, 0, json.dumps(REPLY), '')
        self.assertEqual(len(chat_model.read_catalog(self.config, run)), 3)
        self.assertEqual(seen[0][1:4], ['gateway', 'call', 'models.list'])
        self.assertEqual(json.loads(seen[0][seen[0].index('--params') + 1]), {'view': 'configured'})
        self.assertIsNone(chat_model.read_catalog(self.config, lambda args, **kw: subprocess.CompletedProcess(args, 1, '', 'down')))
        # A failed reading keeps the last good one
        replies = [chat_model.parse_catalog(REPLY, self.config), None]
        catalog = chat_model.Catalog(reader=lambda config: replies.pop(0))
        self.assertEqual(len(catalog.refresh(self.config)), 3)
        self.assertEqual(len(catalog.refresh(self.config, force=True)), 3)

    def test_the_main_models_levels_come_from_its_session_when_the_list_has_none(self):
        # A hosted Gateway listed the main model without its levels: the chat showed the model but no thinking picker
        bare = {'models': [{**REPLY['models'][0], 'thinkingLevels': [], 'thinkingDefault': None}, REPLY['models'][1]]}
        session = {'sessions': [{'modelProvider': 'acme', 'model': 'lm-2', 'thinkingDefault': 'high',
                                 'thinkingLevels': [{'id': x} for x in ('low', 'medium', 'high', 'ultra')]}]}
        seen = []

        def run(args, **kw):
            seen.append(args[3])
            return subprocess.CompletedProcess(args, 0, json.dumps(bare if args[3] == 'models.list' else session), '')
        models = chat_model.read_catalog(self.config, run)
        self.assertEqual(seen, ['models.list', 'sessions.list'])
        self.assertEqual(models[0], {'ref': 'acme/lm-2', 'name': 'LM-2', 'levels': ['low', 'medium', 'high', 'ultra'], 'default': 'high', 'fast': False})
        self.assertEqual(chat_model.resolve(self.config, models)['thinking'], 'medium')
        # Not listed at all (no "available" yet), though every turn runs on it: it is offered with its session's levels
        missing = {'models': [REPLY['models'][1]]}
        run2 = lambda args, **kw: subprocess.CompletedProcess(args, 0, json.dumps(missing if args[3] == 'models.list' else session), '')
        self.assertEqual([(m['ref'], len(m['levels'])) for m in chat_model.read_catalog(self.config, run2)], [('acme/lm-2', 4), ('acme/lm-2-mini', 3)])
        # A session on another model fills nothing in; levels the list has are never asked again
        other = {'sessions': [{**session['sessions'][0], 'model': 'lm-9'}]}
        run3 = lambda args, **kw: subprocess.CompletedProcess(args, 0, json.dumps(bare if args[3] == 'models.list' else other), '')
        self.assertEqual(chat_model.read_catalog(self.config, run3)[0]['levels'], [])
        seen.clear()
        chat_model.read_catalog(self.config, lambda args, **kw: (seen.append(args[3]), subprocess.CompletedProcess(args, 0, json.dumps(REPLY), ''))[1])
        self.assertEqual(seen, ['models.list'])

    def test_resolving_and_what_a_turn_gets(self):
        models = chat_model.parse_catalog(REPLY, self.config)
        # Nothing picked: the turn goes as before, with nothing added
        self.assertEqual(chat_model.turn_args(self.config, models), {})
        self.assertEqual(chat_model.resolve(self.config, models), {'model': 'acme/lm-2', 'thinking': 'medium'})
        # A chat's own model: OpenClaw's level, mapped to the nearest that model has
        self.assertEqual(chat_model.turn_args(self.config, models, {'model': 'acme/lm-2-mini'}),
                         {'provider': 'acme', 'model': 'lm-2-mini', 'thinking': 'medium'})
        self.assertEqual(chat_model.resolve(self.config, models, {'model': 'acme/lm-2-mini', 'thinking': 'max'})['thinking'], 'medium')
        self.assertEqual(chat_model.turn_args(self.config, models, {'model': 'local-llm/gemma_4-q4/k'}),
                         {'provider': 'local-llm', 'model': 'gemma_4-q4/k', 'thinking': 'off'})
        # The default for chats, and a chat's own choice over it
        config = {**self.config, 'chat_model': {'thinking': 'high'}}
        self.assertEqual(chat_model.turn_args(config, models), {'provider': 'acme', 'model': 'lm-2', 'thinking': 'high'})
        self.assertEqual(chat_model.resolve(config, models, {'thinking': 'low'}), {'model': 'acme/lm-2', 'thinking': 'low'})
        # A model the sign-in no longer offers falls back to OpenClaw's main model
        self.assertEqual(chat_model.resolve(self.config, models, {'model': 'other/sonnet'})['model'], 'acme/lm-2')

    def test_a_choice_is_checked_against_the_sign_in(self):
        models = chat_model.parse_catalog(REPLY, self.config)
        self.assertEqual(chat_model.check({'model': 'acme/lm-2-mini', 'thinking': 'off'}, models, self.config),
                         {'model': 'acme/lm-2-mini', 'thinking': 'off'})
        for bad in ({'model': 'other/sonnet'}, {'model': 'acme/nope'}, {'thinking': 'off'}, {'model': 'acme/lm-2-mini', 'thinking': 'max'}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                chat_model.check(bad, models, self.config)
        with self.assertRaises(ValueError):
            chat_model.check({'model': 'acme/lm-2'}, None, self.config)  # no list yet: nothing is taken on trust
        # Only what differs is kept
        self.assertEqual(chat_model.minimal(self.config, models, {'model': 'acme/lm-2', 'thinking': 'medium'}), {})
        self.assertEqual(chat_model.minimal(self.config, models, {'model': 'acme/lm-2', 'thinking': 'high'}), {'thinking': 'high'})


class AppTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.oc = root / 'openclaw.json'
        self.oc.write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'acme/lm-2'}, 'thinkingDefault': 'low'}}}))
        self.oc_text = self.oc.read_text()
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

    def turns(self):
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return [c for c in calls if c.get('action') == 'start']

    def test_dashboard_actions_are_the_owners(self):
        self.assertIn('chat_model_default', a.DASHBOARD_ACTIONS)
        self.assertIn('chat_model_set', a.OWNER_ACTIONS)
        with self.assertRaises(ValueError):
            self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'acme/lm-2-mini'}, owner_dashboard=False)

    def test_without_a_choice_a_turn_is_as_before(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        start = self.turns()[0]
        for key in ('provider', 'model', 'thinking'):
            self.assertNotIn(key, start)

    def test_a_chats_own_choice_goes_with_its_turns(self):
        out = self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'acme/lm-2-mini', 'thinking': 'medium'}, owner_dashboard=True)
        self.assertEqual(out['model'], {'model': 'acme/lm-2-mini', 'thinking': 'medium'})
        self.assertEqual(self.app.card_chat(self.sid)['model'], {'model': 'acme/lm-2-mini', 'thinking': 'medium'})
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        start = self.turns()[0]
        self.assertEqual((start['provider'], start['model'], start['thinking']), ('acme', 'lm-2-mini', 'medium'))
        # Back to what the default gives: nothing kept for this chat
        self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'acme/lm-2', 'thinking': 'low'}, owner_dashboard=True)
        self.assertEqual(self.app.card_chat(self.sid)['model'], {})
        with self.assertRaises(ValueError):
            self.app.action('chat_model_set', {'suggestion_id': self.sid, 'model': 'other/sonnet'}, owner_dashboard=True)
        with self.assertRaises(ValueError):
            self.app.action('chat_model_set', {'suggestion_id': '0' * 16, 'model': 'acme/lm-2'}, owner_dashboard=True)

    def test_the_default_is_saved_in_config_and_openclaw_is_left_alone(self):
        view = self.app.action('chat_model_default', {'model': 'acme/lm-2', 'thinking': 'high'}, owner_dashboard=True)
        self.assertEqual(view['default'], {'model': 'acme/lm-2', 'thinking': 'high'})
        self.assertEqual(json.loads(self.config_path.read_text())['chat_model'], {'thinking': 'high'})
        self.assertEqual(self.oc.read_text(), self.oc_text)
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        start = self.turns()[0]
        self.assertEqual((start['provider'], start['model'], start['thinking']), ('acme', 'lm-2', 'high'))
        self.app.action('chat_model_default', {'model': 'acme/lm-2', 'thinking': 'low'}, owner_dashboard=True)
        self.assertIsNone(json.loads(self.config_path.read_text())['chat_model'])
        # Settings names the model background work uses apart from the one chats use
        self.assertEqual(self.app.chat_model_view()['background'], 'acme/lm-2')

    def test_help_gets_the_pick(self):
        seen = []
        self.app.help_model = lambda config, prompt, model=None, thinking=None: seen.append((model, thinking)) or 'Answer.'
        self.app.owner_role = lambda: ''
        self.app.support_action('help_ask', {'question': 'How do I snooze a to-do?', 'model': 'acme/lm-2-mini', 'thinking': 'off'})
        self.assertEqual(seen[-1], ('acme/lm-2-mini', 'off'))
        self.app.support_action('help_ask', {'question': 'How do I snooze a to-do?'})
        self.assertEqual(seen[-1], (None, None))  # nothing picked: Help as before


if __name__ == '__main__':
    unittest.main()
