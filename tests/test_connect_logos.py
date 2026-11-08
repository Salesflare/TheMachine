"""Connections, + Add: the services' logos are small static SVG files in dashboard/logos, loaded only when shown, never
inlined in the page. Every logo the dashboard names has its file and a NOTICE.md entry (source and terms), each file is
plain artwork (no script, no outside reference) and small, and the Machine serves them as images."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS = ROOT / 'dashboard' / 'logos'


class ConnectLogos(unittest.TestCase):
    def named(self):
        js = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')
        return set(re.search(r'const LOGOS=/\^\(([a-z_|]+)\)\$/', js).group(1).split('|'))

    def test_every_named_logo_has_its_file_and_notice(self):
        notice = (LOGOS / 'NOTICE.md').read_text(encoding='utf-8')
        for name in self.named():
            with self.subTest(name=name):
                self.assertTrue((LOGOS / f'{name}.svg').is_file())
                self.assertIn(f'`{name}.svg`', notice)
        self.assertEqual({p.stem for p in LOGOS.glob('*.svg')}, self.named(), 'no file the dashboard never shows')

    def test_each_file_is_small_plain_artwork(self):
        for path in LOGOS.glob('*.svg'):
            svg = path.read_text(encoding='utf-8')
            with self.subTest(logo=path.name):
                self.assertLess(len(svg.encode()), 8 * 1024)
                self.assertTrue(svg.lstrip().startswith('<svg'))
                self.assertNotRegex(svg, r'(?i)<script|<foreignObject|\son\w+\s*=|javascript:|<image|(?:xlink:)?href\s*=\s*["\'](?!#)')

    def test_the_machine_serves_them_as_images_and_the_page_never_inlines_them(self):
        from machine.config import BRAND_ASSETS
        for path in LOGOS.glob('*.svg'):
            self.assertEqual(BRAND_ASSETS[f'/brand/logos/{path.name}'], path)
        handler = (ROOT / 'machine' / 'web' / 'handler.py').read_text(encoding='utf-8')
        self.assertIn("'.svg': 'image/svg+xml'", handler)
        import dashboard_parts
        page = dashboard_parts.assemble(ROOT)
        self.assertIn('loading="lazy"', page)
        stripe = re.search(r' d="([^"]{40})', (LOGOS / 'stripe.svg').read_text()).group(1)
        self.assertNotIn(stripe, page, 'a logo is a file of its own, not part of the page')


if __name__ == '__main__':
    unittest.main()
