"""Connections, + Add: the services' logos are small static SVG files in dashboard/logos, loaded only when shown, never
inlined in the page (Zoom's is a PNG: its owner publishes no SVG of it). Every logo the dashboard names has its file and a NOTICE.md entry (source and terms), each file is
plain artwork (no script, no outside reference) and small, and the Machine serves them as images."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS = ROOT / 'dashboard' / 'logos'
PNG = {'zoom'}


def files():
    return [p for p in LOGOS.iterdir() if p.suffix in ('.svg', '.png')]


class ConnectLogos(unittest.TestCase):
    def named(self):
        js = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')
        return set(re.search(r'const LOGOS=/\^\(([a-z_|]+)\)\$/', js).group(1).split('|'))

    def test_every_named_logo_has_its_file_and_notice(self):
        notice = (LOGOS / 'NOTICE.md').read_text(encoding='utf-8')
        for name in self.named():
            with self.subTest(name=name):
                file = f'{name}.png' if name in PNG else f'{name}.svg'
                self.assertTrue((LOGOS / file).is_file())
                self.assertIn(f'`{file}`', notice)
        self.assertEqual({p.stem for p in files()}, self.named(), 'no file the dashboard never shows')
        js = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')
        self.assertIn("(n==='zoom'?'.png':'.svg')", js)

    def test_each_file_is_small_plain_artwork(self):
        for path in LOGOS.glob('*.svg'):
            svg = path.read_text(encoding='utf-8')
            with self.subTest(logo=path.name):
                self.assertLess(len(svg.encode()), 8 * 1024)
                self.assertTrue(svg.lstrip().startswith('<svg'))
                self.assertNotRegex(svg, r'(?i)<script|<foreignObject|\son\w+\s*=|javascript:|<image|(?:xlink:)?href\s*=\s*["\'](?!#)')
        for name in PNG:
            png = (LOGOS / f'{name}.png').read_bytes()
            self.assertTrue(png.startswith(b'\x89PNG\r\n\x1a\n'))
            self.assertLess(len(png), 8 * 1024)

    def test_multicolor_brands_keep_their_colors(self):
        """Cards and + Add show each brand's own colored logo: a multicolor mark never collapses to one fill (Gmail once
        showed as a flat red M). Gmail is Google's four-color M; one-color logos are only the brands that are one color."""
        def colors(name):
            svg = (LOGOS / f'{name}.svg').read_text(encoding='utf-8')
            return {c.upper() for c in re.findall(r'(?:fill|stop-color)="(#[0-9A-Fa-f]{3,6})"', svg)} | set(re.findall(r'url\(#[^)]+\)', svg))
        gmail = colors('gmail')
        for brand in ('#4285F4', '#34A853', '#FBBC04', '#EA4335'):  # blue, green, yellow, red
            self.assertIn(brand, gmail, f'Gmail logo misses {brand}')
        self.assertGreaterEqual(len(colors('calendar') & {'#4285F4', '#34A853', '#FBBC04', '#EA4335'}), 4)
        self.assertGreaterEqual(len(colors('google_meet')), 5)
        one_color = {'codex', 'crm', 'github', 'google_docs', 'icloud_calendar', 'intercom', 'linkedin', 'rss',
                     'shortcut', 'signal', 'stripe', 'telegram', 'trello', 'whatsapp', 'x'}
        for path in LOGOS.glob('*.svg'):
            if path.stem not in one_color:
                with self.subTest(logo=path.name):
                    self.assertGreaterEqual(len(colors(path.stem)), 2, 'a multicolor brand logo flattened to one color')

    def test_the_machine_serves_them_as_images_and_the_page_never_inlines_them(self):
        from machine.config import BRAND_ASSETS
        for path in files():
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
