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
