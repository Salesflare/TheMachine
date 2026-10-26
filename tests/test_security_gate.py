"""Release scans fail closed: a failed or unavailable scan cannot permit shipping."""
import contextlib
import io
import subprocess
import unittest
from unittest import mock

from scripts import security_gate


class SecurityGate(unittest.TestCase):
    def call(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return security_gate.require_release_scan('repo', 'a' * 40)

    def test_only_a_successful_receipt_permits_shipping(self):
        with mock.patch.object(security_gate.shutil, 'which', return_value='/official/client'), \
             mock.patch.object(security_gate.subprocess, 'run') as run:
            for code, receipt in [(0, '{"gate_passed":false}'), (10, '{"gate_passed":true}'),
                                  (0, '{}'), (0, '{"gate_passed":1}'), (0, '[]'),
                                  (0, 'null'), (0, 'not JSON')]:
                with self.subTest(code=code, receipt=receipt):
                    run.return_value = subprocess.CompletedProcess([], code, stdout=receipt)
                    with self.assertRaises(RuntimeError):
                        self.call()
            run.return_value = subprocess.CompletedProcess([], 0, stdout='{"gate_passed":true}')
            self.assertIs(self.call()['gate_passed'], True)
            command = run.call_args.args[0]
            self.assertIn('--fail-on-sast-scan', command)
            self.assertIn('--fail-on-secrets-scan', command)
            self.assertIn('--fail-on-iac-scan', command)
            self.assertNotIn('--no-fail-on-dependency-scan', command)
            self.assertEqual(command[command.index('--minimum-severity-level') + 1], 'HIGH')

    def test_missing_client_never_starts_a_scan(self):
        with mock.patch.object(security_gate.shutil, 'which', return_value=None), \
             mock.patch.object(security_gate.subprocess, 'run') as run:
            with self.assertRaises(RuntimeError):
                self.call()
            run.assert_not_called()

    def test_timeout_and_execution_failure_block_shipping(self):
        with mock.patch.object(security_gate.shutil, 'which', return_value='/official/client'), \
             mock.patch.object(security_gate.subprocess, 'run') as run:
            for error in [subprocess.TimeoutExpired('scan', 1800), OSError('unavailable')]:
                with self.subTest(error=error):
                    run.side_effect = error
                    with self.assertRaises(RuntimeError):
                        self.call()


if __name__ == '__main__':
    unittest.main()
