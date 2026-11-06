"""Owners read the names of services they know (Gmail, WhatsApp, Google Calendar, Codex), never the tools The Machine
runs underneath (gog, gogcli, wacli, himalaya, msgraph-cli, codex-cli). Settings, Activity once read "Gog ·
sam@…": an account's transport shown as its channel. machine/names.py is the one place a key from data becomes a
name; this guards it and the owner-facing text (catalogs, help docs), as test_i18n's OpenClaw check does for OpenClaw."""
import json
import re
import unittest
from pathlib import Path

from machine import names

ROOT = Path(__file__).resolve().parents[1]
TOOLS = re.compile(r'(?i)\b(?:gog|gogcli|wacli|himalaya|msgraph-cli|codex-cli)\b')
# Terminal text only: a command to type names the tool it runs, and so does an install step on one's own computer
COMMANDS = re.compile(r'`[^`]*`|\bgog auth\b|\bwacli --store\b|https://github\.com/Salesflare/wacli')


class OwnerNamesTest(unittest.TestCase):
    def test_keys_from_data_read_as_the_service_never_the_tool(self):
        for key in ('gog', 'Gog', 'gogcli', 'wacli', 'wacli-local', 'existing_wacli_local_store', 'himalaya', 'msgraph-cli',
                    'openclaw-feed', 'existing_openclaw_feed', 'codex-cli', 'journald', 'broker', 'maton', 'api', 'x-inbox'):
            for name in (names.service_name(key), names.agent_name(key), names.place(key), names.place(f'{key} · sam@acme.example')):
                self.assertFalse(name and TOOLS.search(name), f'{key} -> {name}')
        self.assertEqual(names.service_name('gog'), 'Gmail')
        self.assertEqual(names.service_name(names.account_service({'transport': 'gog'})), 'Gmail')
        self.assertEqual(names.service_name(names.account_service({'transport': 'wacli-local'})), 'WhatsApp')
        self.assertEqual(names.agent_name('codex-cli'), 'Codex')
        self.assertEqual(names.place('Gog · gh@acme.example'), 'Gmail · gh@acme.example')  # an address is never a tool
        self.assertEqual(names.service_name('google_drive'), 'Google drive')  # a key nobody named still reads in words

    def test_the_dashboard_hides_the_same_tool_names(self):
        # The dashboard's service() hides a tool name from data with the same list (todos-cards.js INTERNAL_NAME)
        js = (ROOT / 'dashboard' / 'todos-cards.js').read_text(encoding='utf-8')
        found = re.search(r'const INTERNAL_NAME=/(.+)/i;', js)
        self.assertIsNotNone(found)
        self.assertEqual(found.group(1).replace('\\\\', '\\'), names.INTERNAL.pattern.removeprefix('(?i)'))
        self.assertIn("const service=v=>SERVICE_NAMES[v]||(INTERNAL_NAME.test(", js)

    def test_owner_facing_text_names_no_tool_underneath(self):
        catalog = json.loads((ROOT / 'i18n' / 'en.json').read_text(encoding='utf-8'))
        lines = [f'i18n: {key}' for key in catalog if TOOLS.search(COMMANDS.sub('', key))]
        for doc in sorted((ROOT / 'docs' / 'help').rglob('*.md')):
            for n, line in enumerate(doc.read_text(encoding='utf-8').splitlines(), 1):
                if TOOLS.search(COMMANDS.sub('', line)):
                    lines.append(f'{doc.relative_to(ROOT)}:{n}: {line[:120]}')
        self.assertEqual(lines, [], 'name the service the owner knows (Gmail, WhatsApp), or drop it:\n' + '\n'.join(lines[:30]))


if __name__ == '__main__':
    unittest.main()
