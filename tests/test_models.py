"""models.py: which model OpenClaw runs, whether it can run, and what background work uses."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import models


class Models(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'openclaw.json'
        self.config = {'openclaw_config': str(self.path)}
        models._model_ready.clear()
        self.addCleanup(models._model_ready.clear)

    def openclaw(self, model, allowed=None):
        defaults = {'model': model, **({'models': allowed} if allowed is not None else {})}
        self.path.write_text(json.dumps({'agents': {'defaults': defaults}}))

    def test_openclaw_model(self):
        self.assertIsNone(models.openclaw_model(self.config))  # no file
        self.openclaw({'primary': ' openai/gpt-6-astra '})
        self.assertEqual(models.openclaw_model(self.config), 'openai/gpt-6-astra')
        self.openclaw('  ')
        self.assertIsNone(models.openclaw_model(self.config))

    def test_claude_plan_route(self):
        self.assertFalse(models.claude_plan_route(self.config))
        self.openclaw('claude-cli/claude-opus-5-5')
        self.assertTrue(models.claude_plan_route(self.config))
        self.openclaw('anthropic/claude-opus-5-5', {'anthropic/*': {'agentRuntime': {'id': 'claude-cli'}}})
        self.assertTrue(models.claude_plan_route(self.config))
        self.openclaw('anthropic/claude-opus-5-5', {'anthropic/*': {'agentRuntime': {'id': 'default'}}})
        self.assertFalse(models.claude_plan_route(self.config))
        self.openclaw('openai/gpt-6-astra')
        self.assertFalse(models.claude_plan_route(self.config))

    def test_background_model_swaps_only_the_costly_one_the_allowlist_allows(self):
        self.openclaw('openai/gpt-6.1-sol')
        self.assertIsNone(models.background_model(self.config))
        self.openclaw('openai/gpt-6-astra')
        self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.1-sol'))
        self.openclaw('openai/gpt-6-astra', {'openai/gpt-6-astra': {}})
        self.assertIsNone(models.background_model(self.config))
        self.openclaw('openai/gpt-6-astra', {'openai/*': {}})
        self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.1-sol'))
        # GPT-6.2 Sol only where the allowlist names it (its OpenClaw entry is written with it); 6.1 where only it is named
        self.openclaw('openai/gpt-6-astra', {'openai/gpt-6-astra': {}, 'openai/gpt-6.2-sol': {}, 'openai/gpt-6.1-sol': {}})
        with patch.object(models, 'GPT_62_UNCACHED', False):
            self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.2-sol'))
            self.openclaw('openai/gpt-6.2-sol')
            self.assertIsNone(models.background_model(self.config))
        self.openclaw('openai/gpt-6-astra', {'openai/gpt-6-astra': {}, 'openai/gpt-6.1-sol': {}})
        self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.1-sol'))

    def test_background_model_skips_uncached_gpt_62_sol_on_the_chatgpt_sign_in(self):
        allowed = {'openai/gpt-6-astra': {}, 'openai/gpt-6.2-sol': {}, 'openai/gpt-6.1-sol': {}}
        for main in ('openai/gpt-6.2-sol', 'openai/gpt-6-astra', 'openai-codex/gpt-6.2-sol'):
            self.openclaw(main, {**allowed, 'openai-codex/*': {}})
            self.assertEqual(models.background_model(self.config)[1], 'gpt-6.1-sol', main)
        self.openclaw('openai/gpt-6.2-sol', {'openai/gpt-6.2-sol': {}})
        self.assertIsNone(models.background_model(self.config))  # the allowlist doesn't have 6.1: the main model
        for main in ('salesflare-openai/gpt-6.2-sol', 'openai/gpt-6.1-sol', 'claude-cli/claude-opus-5-5'):
            self.openclaw(main)
            self.assertIsNone(models.background_model(self.config), main)

    def test_gpt_62_sol_swap_follows_the_installed_openclaw_version(self):
        # The package as the installer leaves it: openclaw_package_dir in config.json, OpenClaw's own package.json there
        package = Path(self.tmp.name) / 'lib/node_modules/openclaw'
        package.mkdir(parents=True)
        self.config['openclaw_package_dir'] = str(package)
        allowed = {'openai/gpt-6-astra': {}, 'openai/gpt-6.2-sol': {}, 'openai/gpt-6.1-sol': {}}
        older, cached = (('openai', 'gpt-6.1-sol'), ('openai', 'gpt-6.1-sol')), (('openai', 'gpt-6.2-sol'), None)
        cases = (('2026.11.2', older), ('2026.11.9', older),  # hosted Machines today: as before
                 ('2026.11.10', cached), ('2026.12.1', cached), ('2027.1.0-beta.1', cached))
        for version, (from_astra, from_sol) in cases:
            (package / 'package.json').write_text(json.dumps({'name': 'openclaw', 'version': version}))
            self.openclaw('openai/gpt-6-astra', allowed)
            self.assertEqual(models.background_model(self.config), from_astra, version)
            self.openclaw('openai/gpt-6.2-sol', allowed)
            self.assertEqual(models.background_model(self.config), from_sol, version)  # None: the main model, 6.2
        with patch.object(models, 'GPT_62_UNCACHED', False):  # the switch still turns it off everywhere
            (package / 'package.json').write_text(json.dumps({'name': 'openclaw', 'version': '2026.11.2'}))
            self.assertIsNone(models.background_model(self.config))
        # Unknown version: today's swap. No folder, no package.json, another package, an unreadable version
        for body in (None, '{', json.dumps({'name': 'other', 'version': '2026.11.10'}), json.dumps({'name': 'openclaw', 'version': 'x'})):
            (package / 'package.json').unlink(missing_ok=True)
            if body:
                (package / 'package.json').write_text(body)
            self.assertIsNone(models.openclaw_version(self.config), body)
            self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.1-sol'), body)
        del self.config['openclaw_package_dir']
        self.assertEqual(models.background_model(self.config), ('openai', 'gpt-6.1-sol'))

    def test_main_model_reads_openclaw_settings(self):
        self.openclaw({'primary': 'openai/gpt-6-astra'})
        with patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(self.path)}):
            self.assertEqual(models.main_model(), 'openai/gpt-6-astra')
        with patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(self.path) + '.missing'}):
            self.assertEqual(models.main_model(), '')

    def test_model_ready_reads_models_status_once_a_while(self):
        calls = []

        def run(missing, fallbacks=()):
            out = json.dumps({'fallbacks': list(fallbacks), 'auth': {'missingProvidersInUse': missing}})
            return lambda args, **kw: calls.append(args) or type('R', (), {'stdout': out})()
        with patch.object(models, 'main_model', return_value='openai/gpt-6-astra'):
            self.assertFalse(models.model_ready({'openclaw': '/x/openclaw'}, run(['openai'])))
            self.assertFalse(models.model_ready({}, run([])))  # cached
            self.assertEqual(calls, [['/x/openclaw', 'models', 'status', '--json']])
            models._model_ready.clear()
            self.assertTrue(models.model_ready({}, run(['google'], ['google/gemini'])))  # only a fallback's
            models._model_ready.clear()
            self.assertIsNone(models.model_ready({}, lambda *a, **k: (_ for _ in ()).throw(OSError('no openclaw'))))
        with patch.object(models, 'main_model', return_value=''):
            self.assertFalse(models.model_ready({}, run([])))

    def test_has_model(self):
        with patch.object(models, 'main_model', return_value='openai/gpt-6-astra'):
            for ready, has in ((True, True), (None, True), (False, False)):
                with self.subTest(ready=ready), patch.object(models, 'model_ready', return_value=ready):
                    self.assertIs(models.has_model(), has)
        with patch.object(models, 'main_model', return_value=''):
            self.assertFalse(models.has_model())


if __name__ == '__main__':
    unittest.main()
