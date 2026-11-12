"""Every source's one-color mark (dashboard/todos-logos.js MONO, files in dashboard/logos/mono): the small icons in rows
that say where something came from. Every connector has one, so a new connector can't ship with a generic glyph; each
file is listed in its NOTICE.md (source and terms), is plain one-color artwork and small, and the Machine serves it."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MONO_DIR = ROOT / 'dashboard' / 'logos' / 'mono'
JS = (ROOT / 'dashboard' / 'todos-logos.js').read_text(encoding='utf-8')
# The line icons in todos-chat.css (--i-<name>) an alias may point at
LINE_ICONS = {'mail', 'chat', 'cal', 'note', 'file', 'browser', 'link'}
# Phone apps with no brand mark here: they show the phone
NO_MARK_APPS = {'android', 'com.google.android.apps.wellbeing', 'com.kbc.mobile.android.phone.kbc', 'com.google.android.dialer'}


def registry():
    mono = re.findall(r"'([a-z0-9_]+)'", re.search(r'const MONO=\[([^\]]*)\];', JS).group(1))
    alias = dict(re.findall(r"(\w+):'(\w+)'", re.search(r'const MONO_ALIAS=\{([^}]*)\}', JS).group(1)))
    apps = dict(re.findall(r"'([\w.]+)':'(\w+)'", re.search(r'const MONO_APPS=\{([^}]*)\}', JS, re.S).group(1)))
    return mono, alias, apps


def connectors():
    """Every source the owner can connect or that shows as a connection: + Add's catalog, the services the dashboard
    names, and every connector module."""
    import onboarding
    from machine import names
    found = {onboarding.SERVICES.get(n, n) for n in onboarding.sources()} | set(onboarding.SERVICES.values()) | set(names.SERVICES)
    found |= {p.stem for p in (ROOT / 'connectors').glob('*.py') if not p.stem.startswith('_')}
    return found


class SourceIcons(unittest.TestCase):
    def test_every_connector_has_a_mark(self):
        mono, alias, _ = registry()
        for name in sorted(connectors()):
            with self.subTest(connector=name):
                key = name if name in mono else alias.get(name)
                self.assertTrue(key in mono or key in LINE_ICONS,
                                f'{name}: add its one-color mark to dashboard/logos/mono/ and MONO in dashboard/todos-logos.js '
                                '(docs/adding-a-source.md)')
        for name, key in alias.items():
            with self.subTest(alias=name):
                self.assertTrue(key in mono or key in LINE_ICONS, key)
        self.assertIn('source', mono, 'a neutral mark for a source with none')

    def test_the_machines_own_kinds_have_a_mark(self):
        # a routine's draft, a Fleet hand-off and what it carried: never the neutral mark
        mono, _, _ = registry()
        kinds = dict(re.findall(r"'([\w.]+)':'(\w+)'", re.search(r'const KIND_MARK=\{([^}]*)\}', JS, re.S).group(1)))
        for kind, key in kinds.items():
            with self.subTest(kind=kind):
                self.assertTrue(key in mono or key in LINE_ICONS, key)
        self.assertEqual({k: kinds[k] for k in ('fleet.email', 'fleet.intercom', 'fleet.message')},
                         {'fleet.email': 'mail', 'fleet.intercom': 'intercom', 'fleet.message': 'chat'})
        self.assertIn("['machine','routine','fleet'].includes(head)?'gateway'", JS)

    def test_known_phone_apps_show_their_brand(self):
        mono, _, apps = registry()
        from machine.sources.android import ANDROID_APP_NAMES
        for package in ANDROID_APP_NAMES:
            if package not in NO_MARK_APPS:
                with self.subTest(package=package):
                    self.assertIn(package, apps)
        for package, key in apps.items():
            with self.subTest(app=package):
                self.assertIn(key, mono)
        self.assertEqual(apps['com.medium.reader'], 'medium')

    def test_each_mark_is_a_listed_small_one_color_file(self):
        mono, _, _ = registry()
        self.assertEqual(sorted(mono), sorted(set(mono)))
        self.assertEqual({p.stem for p in MONO_DIR.glob('*.svg')}, set(mono), 'a file for every mark, none unused')
        notice = (MONO_DIR / 'NOTICE.md').read_text(encoding='utf-8')
        for key in mono:
            svg = (MONO_DIR / f'{key}.svg').read_text(encoding='utf-8')
            with self.subTest(mark=key):
                self.assertIn(f'`{key}.svg`', notice)
                self.assertTrue(svg.lstrip().startswith('<svg'))
                self.assertLess(len(svg.encode()), 4 * 1024)
                self.assertNotRegex(svg, r'(?i)<script|<foreignObject|\son\w+\s*=|javascript:|<image|<style|href\s*=')
                # one color: a mask uses only its shape, so no colors of its own beyond black
                self.assertEqual(set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]+|[a-z]+)"', svg)) - {'#000', 'none'}, set())

    def test_the_machine_serves_them_and_the_page_never_inlines_them(self):
        from machine.config import BRAND_ASSETS
        for path in MONO_DIR.glob('*.svg'):
            self.assertEqual(BRAND_ASSETS[f'/brand/logos/mono/{path.name}'], path)
        import dashboard_parts
        page = dashboard_parts.assemble(ROOT)
        slack = re.search(r' d="([^"]{40})', (MONO_DIR / 'slack.svg').read_text()).group(1)
        self.assertNotIn(slack, page, 'a mark is a file of its own, loaded when shown')
        self.assertIn('brand/logos/mono/', page)

    def test_small_icon_spots_use_the_marks(self):
        # the rows that list messages and sources draw marks, not the old line glyphs
        for part, needle in [('todos-mail-check.js', 'markIco(sourceMark(r.kind,r.account,r.app))'),
                             ('events-list.js', 'markIco(sourceMark(e.kind,e.account_id,e.metadata.package_name))'),
                             ('graph-record.js', 'markIco(sourceMark(k))'),
                             ('learning-missed.js', 'markIco(VOICE_ICON')]:
            with self.subTest(part=part):
                self.assertIn(needle, (ROOT / 'dashboard' / part).read_text(encoding='utf-8'))
        self.assertNotIn('icon(kindService(', ''.join(p.read_text(encoding='utf-8') for p in (ROOT / 'dashboard').glob('*.js')))


if __name__ == '__main__':
    unittest.main()
