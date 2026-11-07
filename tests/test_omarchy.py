"""machine/omarchy.py: the current Omarchy theme's colors for the dashboard's Omarchy theme setting, or None without
Omarchy. Only #rrggbb values pass, since they end up in the page's style."""
from pathlib import Path
import tempfile
import unittest

from machine import omarchy

TOKYO = '''mode = "dark"
accent = "#7aa2f7"
background = "#1a1b26"
dark_background = "#16161E"
foreground = "#a9b1d6"
red = "#f7768e"
hyprland_inactive_border = "rgba(58516e66)"
'''


def place(home, folder, colors, name=None):
    theme = Path(home) / folder / 'theme'
    theme.mkdir(parents=True)
    (theme / 'colors.toml').write_text(colors)
    if name is not None:
        (theme.parent / 'theme.name').write_text(name + '\n')


class OmarchyThemeTest(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()

    def test_no_omarchy(self):
        self.assertIsNone(omarchy.theme(self.home))

    def test_omarchy_4(self):
        place(self.home, '.local/state/omarchy/current', TOKYO, 'tokyo-night')
        got = omarchy.theme(self.home)
        self.assertEqual(got['name'], 'tokyo-night')
        self.assertEqual(got['mode'], 'dark')
        self.assertEqual(got['colors'], {'accent': '#7aa2f7', 'background': '#1a1b26', 'dark_background': '#16161e',
                                         'foreground': '#a9b1d6', 'red': '#f7768e'})

    def test_omarchy_3_and_light(self):
        place(self.home, '.config/omarchy/current', 'mode = "light"\n' + TOKYO.split('\n', 1)[1])
        got = omarchy.theme(self.home)
        self.assertEqual((got['mode'], got['name']), ('light', ''))

    def test_only_plain_colors(self):
        place(self.home, '.local/state/omarchy/current',
              TOKYO.replace('"#f7768e"', '"red;background:url(x)"').replace('mode = "dark"', 'mode = "x"'),
              'evil</style><script>')
        got = omarchy.theme(self.home)
        self.assertNotIn('red', got['colors'])
        self.assertEqual(got['mode'], 'dark')
        self.assertEqual(got['name'], 'evilstylescript')

    def test_incomplete_or_broken_is_none(self):
        place(self.home, '.local/state/omarchy/current', 'accent = "#7aa2f7"\n')
        self.assertIsNone(omarchy.theme(self.home))
        (Path(self.home) / '.local/state/omarchy/current/theme/colors.toml').write_text('not = [toml')
        self.assertIsNone(omarchy.theme(self.home))


if __name__ == '__main__':
    unittest.main()
