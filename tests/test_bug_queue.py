"""Report a bug never loses a report: when the control plane can't take it now (its limit with Retry-After, 5xx,
offline), the Machine keeps it and sends it by itself later (bug_queue.py). No network: the control plane is a stand-in."""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import bug_queue  # noqa: E402
import fleet  # noqa: E402

spec = importlib.util.spec_from_file_location('bug_queue_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class Clock:
    def __init__(self):
        self.now = 1_800_000_000

    def __call__(self):
        return self.now


class ControlPlane:
    """bug_report as fleet.Fleet has it: each call takes the next answer (an error to raise, or a result)."""
    def __init__(self, *answers):
        self.answers, self.sent = list(answers), []

    def bug_report(self, body):
        answer = self.answers.pop(0) if self.answers else {'id': 's_1'}
        if isinstance(answer, Exception):
            raise answer
        self.sent.append(body)
        return answer


def limited(seconds):
    error = fleet.Limited('You sent a few reports just now; we have them.')
    error.retry_after = seconds
    return error


class BugQueue(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.config = {'database': str(Path(temp.name) / 'events.sqlite')}
        self.app.config_path = ''
        self.clock = Clock()
        patcher = patch.object(bug_queue.time, 'time', self.clock)
        patcher.start()
        self.addCleanup(patcher.stop)

    def send(self, cp, what='The Calendar shows yesterday'):
        self.app.fleet = cp
        return self.app.support_action('bug_send', {'description': what})

    def flush(self, cp):
        return bug_queue.flush(self.app.config, cp.bug_report, clock=self.clock)

    def test_with_the_support_report_it_is_kept_at_once_and_the_worker_adds_the_report(self):
        cp = ControlPlane()
        self.app.fleet = cp
        built = []

        def report(path, doctor=None, budget=None):
            built.append(budget)
            return {'parts': {'service-log': ['ERROR token=sk-abcdefghijklmnopqrstuvwxyz0123']}, 'settings': {'model': 'm'}}
        with patch.object(__import__('support'), 'report', side_effect=report) as made:
            out = self.app.support_action('bug_send', {'description': 'Slow checks', 'diagnostics': True})
            self.assertEqual(out['sent'], True)
            self.assertEqual(made.call_count, 0, 'the dashboard never waits for the support report')
            self.assertEqual(cp.sent, [])
            self.assertEqual([i['what'] for i in bug_queue.view(self.app.config)], ['Slow checks'], 'kept before anything goes')
            self.assertEqual(bug_queue.flush(self.app.config, self.app.bug_with_report, clock=self.clock), 1, 'due now')
        self.assertEqual(built, [a.App.REPORT_BUDGET], 'built within the time budget')
        self.assertEqual(cp.sent[0]['description'], 'Slow checks')
        self.assertNotIn('diagnostics', cp.sent[0])
        self.assertEqual(cp.sent[0]['report']['settings'], {'model': 'm'})
        self.assertNotIn('sk-abcdef', json.dumps(cp.sent))
        self.assertEqual(bug_queue.view(self.app.config), [])

    def test_a_support_report_that_fails_never_loses_the_bug_report(self):
        cp = ControlPlane()
        self.app.fleet = cp
        with patch.object(__import__('support'), 'report', side_effect=RuntimeError('stuck')):
            self.app.support_action('bug_send', {'description': 'Broken', 'diagnostics': True})
            self.assertEqual(bug_queue.flush(self.app.config, self.app.bug_with_report, clock=self.clock), 1)
        self.assertEqual(cp.sent[0]['description'], 'Broken')
        self.assertEqual(cp.sent[0]['report'], {'parts': {'report': ['not built: RuntimeError']}})

    def test_unticked_it_goes_at_once_without_a_report(self):
        cp = ControlPlane()
        self.app.fleet = cp
        with patch.object(__import__('support'), 'report') as made:
            self.assertEqual(self.app.support_action('bug_send', {'description': 'Plain', 'diagnostics': False}), {'sent': True, 'id': 's_1'})
        made.assert_not_called()
        self.assertEqual(cp.sent, [{'description': 'Plain', 'screenshot': None, 'report': None}])

    def test_a_429_with_retry_after_is_kept_and_sent_then(self):
        cp = ControlPlane(limited(900))
        out = self.send(cp)
        self.assertEqual(out, {'sent': False, 'queued': True, 'at': self.clock.now + 900})
        self.assertEqual(self.app.support_action('bug_queued', {})['queued'],
                         [{'id': bug_queue.load(self.app.config)[0]['id'], 'what': 'The Calendar shows yesterday', 'next_at': self.clock.now + 900}])
        self.clock.now += 899
        self.assertEqual((self.flush(cp), cp.sent), (0, []))  # not before the control plane said
        self.clock.now += 1
        self.assertEqual(self.flush(cp), 1)
        self.assertEqual(cp.sent[0]['description'], 'The Calendar shows yesterday')
        self.assertEqual(self.app.support_action('bug_queued', {})['queued'], [])

    def test_offline_it_waits_backs_off_and_goes_once_back(self):
        cp = ControlPlane(urllib.error.URLError(OSError('no route')))
        self.assertEqual(self.send(cp)['at'], self.clock.now + bug_queue.FIRST)
        self.assertTrue(self.send(ControlPlane(fleet.NetworkUnavailable('away')), 'Second one')['queued'])
        cp.answers = [OSError('still offline')]
        self.clock.now += bug_queue.FIRST
        self.assertEqual(self.flush(cp), 0)
        waiting = bug_queue.load(self.app.config)
        self.assertEqual(waiting[0]['next_at'], self.clock.now + 2 * bug_queue.FIRST)  # backs off
        self.assertTrue(all(i['next_at'] >= waiting[0]['next_at'] for i in waiting))  # the others wait as long
        self.clock.now += 2 * bug_queue.FIRST
        self.assertEqual(self.flush(cp), 2)  # back online: both go, oldest first
        self.assertEqual([b['description'] for b in cp.sent], ['The Calendar shows yesterday', 'Second one'])
        self.assertEqual(bug_queue.load(self.app.config), [])
        self.assertEqual(bug_queue.wait(20), bug_queue.LONGEST)

    def test_a_429_again_respects_the_new_retry_after(self):
        cp = ControlPlane(limited(60), limited(3000))
        self.send(cp)
        self.clock.now += 60
        self.flush(cp)
        self.assertEqual(bug_queue.load(self.app.config)[0]['next_at'], self.clock.now + 3000)

    def test_a_refusal_retrying_cant_fix_is_said_at_once(self):
        cp = ControlPlane(ValueError('That image can’t be sent. Try a smaller PNG or JPEG.'), ValueError('unknown machine'))
        with self.assertRaisesRegex(ValueError, 'smaller PNG'):
            self.send(cp)
        with self.assertRaisesRegex(ValueError, 'support@themachine.computer'):
            self.send(cp)
        self.assertEqual(bug_queue.load(self.app.config), [])

    def test_a_hosted_dashboards_refused_report_is_kept_with_its_retry_after(self):
        self.app.fleet = ControlPlane()
        out = self.app.support_action('bug_later', {'description': 'Buttons overlap', 'retry_after': 1200})
        self.assertEqual(out, {'sent': False, 'queued': True, 'at': self.clock.now + 1200})
        self.assertEqual(self.app.fleet.sent, [])  # not now: the control plane just said no

    def test_the_kept_file_is_the_owners_only_and_has_a_cap(self):
        cp = ControlPlane(*[OSError('offline')] * (bug_queue.MOST + 1))
        for i in range(bug_queue.MOST):
            self.send(cp, f'Bug {i}')
        self.assertEqual(bug_queue.path(self.app.config).stat().st_mode & 0o777, 0o600)
        with self.assertRaisesRegex(ValueError, 'support@themachine.computer'):
            self.send(cp, 'One too many')

    def test_the_network_client_reads_429_and_its_retry_after(self):
        client = object.__new__(fleet.NetworkClient)
        client.token = lambda: 'fd_test'
        body = json.dumps({'error': 'You sent a few reports just now.', 'retry_after': 600}).encode()
        refusal = urllib.error.HTTPError('https://network.example/api/fleet/bug', 429, 'Too Many Requests', {'Retry-After': '1500'}, io.BytesIO(body))
        with patch.object(fleet.urllib.request, 'urlopen', side_effect=refusal):
            with self.assertRaises(fleet.Limited) as caught:
                client._call('https://network.example/api/fleet', 'POST', '/bug', {'description': 'x'}, 5)
        self.assertEqual(caught.exception.retry_after, 1500)
        self.assertTrue(bug_queue.retryable(caught.exception))
        self.assertFalse(bug_queue.retryable(ValueError('That report can’t be sent.')))


if __name__ == '__main__':
    unittest.main()
