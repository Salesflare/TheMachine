"""The dashboard's own address (machine/dashboard_link.py): links in messages, pushes and pages are built in one place,
never by hand from dashboard_host and dashboard_path (tests/test_architecture.py checks that)."""
import unittest

from machine.dashboard_link import dashboard_address, dashboard_link


class DashboardLink(unittest.TestCase):
    def test_a_link_is_the_host_and_path_as_the_config_spells_them(self):
        self.assertEqual(dashboard_link({'dashboard_host': 'm.example:8443', 'dashboard_path': '/assistant/'}, '#card=1'),
                         'https://m.example:8443/assistant/#card=1')
        self.assertEqual(dashboard_link({'dashboard_host': 'm.example'}), 'https://m.example/')
        self.assertEqual(dashboard_link({'dashboard_host': 'm.example', 'dashboard_path': ''}, '#x'), 'https://m.example/#x')
        self.assertEqual(dashboard_link({'dashboard_host': 'm.example', 'dashboard_path': None}), 'https://m.example/')
        self.assertEqual(dashboard_link({'dashboard_path': '/'}, '#card=1'), '')
        self.assertEqual(dashboard_link(None), '')

    def test_the_address_is_tidied_up(self):
        self.assertEqual(dashboard_address({'dashboard_host': ' M.Example ', 'dashboard_path': 'assistant'}), 'https://m.example/assistant/')
        self.assertEqual(dashboard_address({'dashboard_host': 'm.example', 'dashboard_path': '/'}), 'https://m.example/')
        self.assertIsNone(dashboard_address({'dashboard_path': '/'}))


if __name__ == '__main__':
    unittest.main()
