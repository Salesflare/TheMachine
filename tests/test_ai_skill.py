"""The skill that ships with the MCP connection (claude-plugin/: a Claude Code plugin with the MCP server and the
skill; the same SKILL.md goes to claude.ai, ClawHub and as rules elsewhere, ai-connections.md, The skill). It stays
true to the server: every tool it names exists, the address is the official one, and the frontmatter is what each
place reads."""
import json
from pathlib import Path
import re
import unittest

import ai_access

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / 'claude-plugin'
SKILL = PLUGIN / 'skills' / 'the-machine' / 'SKILL.md'
# The official address (test_ai_reach.py pins the server's to the same): importing or naming the module that has it
# would make every doc change run this test
SHARED_ADDRESS = 'https://mcp.themachine.computer/mcp'


class Skill(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding='utf-8')
        head, _, self.body = self.text.partition('\n---\n')
        self.head = dict(re.findall(r'^(name|description): (.+)$', head, re.M))

    def test_it_names_only_tools_the_server_has(self):
        named = set(re.findall(r'`([a-z]+(?:_[a-z]+)+)`', self.body))
        self.assertTrue(named)
        self.assertEqual(named - set(ai_access.TOOLS), set())
        for tool in ('get_brief', 'get_learnings', 'search_graph', 'save_learning', 'save_fact'):
            self.assertIn(tool, named)

    def test_each_step_works_without_the_learning_tools(self):
        # ChatGPT's app lists a new tool only once OpenAI approves it, and ai_learnings can be off: the list such a
        # connection gets (no LEARNING_TOOLS) must still give every step of the skill a tool to call
        listed = {tool['name'] for tool in ai_access.tool_list(learnings=False)}
        self.assertFalse(listed & set(ai_access.LEARNING_TOOLS))
        steps = re.split(r'^## ', self.body, flags=re.M)[1:]
        self.assertGreaterEqual(len(steps), 4)
        for step in steps:
            named = set(re.findall(r'`([a-z]+(?:_[a-z]+)+)`', step))
            if named:
                self.assertTrue(named & listed, step.splitlines()[0])
        drafts = next(s for s in steps if s.startswith('Before you draft'))
        for tool in ('get_graph_record', 'search_messages'):  # who it goes to, and how the owner writes to them
            self.assertIn(f'`{tool}`', drafts)

    def test_the_address_is_the_official_one(self):
        self.assertIn(SHARED_ADDRESS, self.body)
        servers = json.loads((PLUGIN / '.mcp.json').read_text(encoding='utf-8'))['mcpServers']
        self.assertEqual(servers, {'the-machine': {'type': 'http', 'url': SHARED_ADDRESS}})

    def test_frontmatter_each_place_reads(self):
        self.assertTrue(self.text.startswith('---\n'))
        self.assertEqual(self.head['name'], 'the-machine')  # the folder's name, lowercase and dashes (Claude, ClawHub)
        self.assertEqual(SKILL.parent.name, self.head['name'])
        self.assertLessEqual(len(self.head['description']), 1024)
        plugin = json.loads((PLUGIN / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(plugin['name'], 'the-machine')
        self.assertRegex(plugin['version'], r'^\d+\.\d+\.\d+$')

    def test_lean_and_never_claims_a_send(self):
        self.assertLess(len(self.body.split()), 450)  # it loads into every chat that uses it
        self.assertIn('Never say you sent', self.body)
        self.assertIn('<untrusted>', self.body)


class Published(unittest.TestCase):
    """Where it goes: the marketplace file Claude Code reads at the repository's root (the zips each desktop release
    carries: test_release.py, Skill)."""

    def test_the_marketplace_lists_the_plugin(self):
        market = json.loads((ROOT / '.claude-plugin' / 'marketplace.json').read_text(encoding='utf-8'))
        plugin = json.loads((PLUGIN / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
        [listed] = market['plugins']
        self.assertEqual((listed['name'], listed['source']), (plugin['name'], './claude-plugin'))
        self.assertEqual(listed['description'], plugin['description'])
        self.assertTrue(market['owner']['name'])
