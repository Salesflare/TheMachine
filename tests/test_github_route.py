"""A to-do's final step on GitHub (filing an issue): it runs with the signed-in gh tool or a GitHub MCP server when
there is one, the browser only when nothing GitHub is connected, the to-do says which, and nothing is filed before the
owner's Confirm. Button names in the model's text follow the owner's dashboard language. Made-up data; gh is a fake
here and nothing reaches GitHub."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_chat_finish as cf

a = cf.a
github_route, i18n = a.github_route, a.i18n

ISSUE = {'kind': 'finish', 'label': 'Submit GitHub issue', 'url': 'https://github.com/example-org/example-app/issues/new',
         'instructions': 'In example-org/example-app file one issue with the title and text below, label BUG.',
         'preview': 'Repository: example-org/example-app\nLabel: BUG\n\nExport button does nothing on mobile'}
GITHUB = {'id': 'github', 'service': 'github', 'transport': 'gh', 'boundary': 'work', 'login': 'sam-example'}


class FakeGh:
    """gh as a recorder: `auth status` answers with `code`; any other call fails the test."""
    def __init__(self, code=0):
        self.code, self.calls = code, []

    def __call__(self, args, **kwargs):
        self.calls.append(args[1:])
        if args[1:3] != ['auth', 'status']:
            raise AssertionError('only gh auth status may run here: ' + ' '.join(args))
        return subprocess.CompletedProcess(args, self.code, '', '')


class Route(unittest.TestCase):
    def setUp(self):
        github_route._cache.clear()
        self.addCleanup(github_route._cache.clear)
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.openclaw = Path(self.temp.name) / 'openclaw.json'
        self.openclaw.write_text('{}')

    def config(self, *accounts, servers=None):
        if servers is not None:
            self.openclaw.write_text(json.dumps({'mcp': {'servers': servers}}))
        return {'accounts': list(accounts), 'openclaw_config': str(self.openclaw)}

    def test_signed_in_gh_runs_it_and_says_as_whom(self):
        gh = FakeGh(0)
        with patch.object(github_route.shutil, 'which', return_value='/usr/bin/gh'):
            step = github_route.route(ISSUE, self.config(GITHUB), run=gh)
        self.assertEqual((step['via'], step['via_login']), ('gh', 'sam-example'))
        self.assertEqual(gh.calls, [['auth', 'status', '--hostname', 'github.com']])  # a check, never a write
        rule = github_route.finish_rule(step)
        self.assertIn('gh tool, signed in as sam-example, not in the browser', rule)
        self.assertIn("don't switch to the browser", rule)
        self.assertNotIn('image uploads', rule)
        self.assertIn('image uploads', github_route.finish_rule({**step, 'attachments': [{'name': 'shot.png'}]}))

    def test_signed_out_gh_or_no_connection_falls_back_to_the_browser(self):
        with patch.object(github_route.shutil, 'which', return_value='/usr/bin/gh'):
            self.assertEqual(github_route.route(ISSUE, self.config(GITHUB), run=FakeGh(1))['via'], 'browser')
            github_route._cache.clear()
            gh = FakeGh(0)
            self.assertEqual(github_route.route(ISSUE, self.config(), run=gh)['via'], 'browser')
            self.assertEqual(gh.calls, [])  # without The Machine's GitHub connection gh isn't asked at all
        self.assertIn('runs in the browser', github_route.finish_rule({**ISSUE, 'via': 'browser'}))
        self.assertEqual(github_route.prompt(self.config(), run=gh), '')

    def test_a_github_mcp_server_counts_when_gh_is_not_there(self):
        config = self.config(servers={'gh-tools': {'command': 'npx', 'args': ['@example/github-mcp']}, 'notes': {'command': 'notes-mcp'}})
        with patch.object(github_route.shutil, 'which', return_value=None):
            step = github_route.route(ISSUE, config, run=FakeGh())
            self.assertIn('GitHub MCP server gh-tools', github_route.prompt(config, run=FakeGh()))
        self.assertEqual(step['via'], 'mcp');self.assertNotIn('via_login', step)
        self.assertIn('MCP server', github_route.finish_rule(step))

    def test_other_pages_and_model_supplied_ways_are_left_to_the_service(self):
        shop = {**ISSUE, 'url': 'https://shop.example.com/checkout', 'via': 'gh'}
        self.assertNotIn('via', github_route.route(shop, self.config(), run=FakeGh()))
        self.assertEqual(github_route.finish_rule(shop), '')
        with patch.object(github_route, 'access', return_value={'gh': None, 'mcp': None}):
            step = a.next_actions.validate({**ISSUE, 'via': 'gh', 'via_login': 'someone-else'}, {'accounts': []}, [])
        self.assertEqual(step['via'], 'browser');self.assertNotIn('via_login', step)
        self.assertEqual(step['kind'], 'finish');self.assertIn('finish', a.next_actions.FINISH_KINDS)


class Flow(unittest.TestCase):
    """The real prepare and Confirm path, with gh faked as signed in."""
    job, accept, ended = cf.ChatFinish.job, cf.ChatFinish.accept, cf.ChatFinish.ended
    ready_step, action_now = cf.ChatFinish.ready_step, cf.ChatFinish.action_now

    def setUp(self):
        cf.ChatFinish.setUp(self)
        github_route._cache.clear()
        self.addCleanup(github_route._cache.clear)
        found = patch.object(github_route, 'access', return_value={'gh': 'sam-example', 'mcp': None})
        found.start();self.addCleanup(found.stop)

    def test_ready_step_says_gh_and_waits_for_confirm(self):
        action = self.ready_step(ISSUE)
        self.assertEqual((action['via'], action['via_login']), ('gh', 'sam-example'))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions').fetchone()[0], 'prepared')
            self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0], 0)  # nothing runs before Confirm
        calls = []
        self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'go'}, owner_dashboard=True)
        self.app.preparation_step(lambda req: calls.append(req) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        self.assertIn("Run this step with GitHub's gh tool, signed in as sam-example, not in the browser", message)

    def test_an_edit_keeps_the_way(self):
        action = self.ready_step(ISSUE)
        self.app.action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': 'Export button does nothing on phones'}, owner_dashboard=True)
        self.assertEqual(self.action_now()['via'], 'gh')


class ButtonNames(unittest.TestCase):
    def test_prompts_name_buttons_in_the_dashboard_language(self):
        rule = i18n.prompt_rule('nl')
        self.assertIn('Continue is "Doorgaan"', rule);self.assertIn('Try again is "Opnieuw proberen"', rule)
        self.assertNotIn('Name the dashboard', i18n.prompt_rule('en'))

    def test_a_blocker_in_the_owners_language_resumes_with_continue(self):
        self.assertEqual(a.retry_label('Vul je code in op de open pagina in de browser van je Machine, en tik daarna op Doorgaan.'), 'Continue')
        self.assertEqual(a.retry_label('Gib den Code im offenen Tab ein und tippe dann auf Weiter.'), 'Continue')
        self.assertEqual(a.retry_label('De site was niet bereikbaar. Tik op Opnieuw proberen.'), 'Try again')
        self.assertEqual(a.retry_label('The site was down.'), 'Try again')


if __name__ == '__main__':
    unittest.main()
