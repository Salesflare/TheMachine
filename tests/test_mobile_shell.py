"""The phone app (mobile/, mobile/README.md): its JavaScript tests (mobile/tests), and the rules around it that are easy to
break by accident: exact dependency pins, which sites the app's WebView may open, the iOS build only ever started by
hand (macOS minutes cost 10x), and no sign-up or buying anywhere in the app's own pages."""
import json
import pathlib
import re
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOBILE = ROOT / 'mobile'


class MobileShellTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'needs node')
    def test_javascript(self):
        run = subprocess.run(['node', '--test', 'tests/'], cwd=MOBILE, capture_output=True, text=True, timeout=120)
        self.assertEqual(run.returncode, 0, run.stdout[-3000:] + run.stderr[-2000:])

    def test_exact_pins(self):
        pkg = json.loads((MOBILE / 'package.json').read_text())
        for name, version in {**pkg['dependencies'], **pkg['devDependencies']}.items():
            self.assertRegex(version, r'^\d+\.\d+\.\d+$', name)
        self.assertEqual(pkg['license'], 'AGPL-3.0-only')

    def test_webview_only_opens_machines(self):
        config = json.loads((MOBILE / 'capacitor.config.json').read_text())
        self.assertEqual(config['appId'], 'computer.themachine.app')
        self.assertEqual(sorted(config['server']['allowNavigation']), ['*.app.themachine.computer', '*.ts.net'])
        self.assertNotIn('url', config['server'])  # the start page is the app's own; the Machine is opened from it
        self.assertFalse(config['android']['allowMixedContent'])
        self.assertFalse(config['android']['webContentsDebuggingEnabled'])

    def test_ios_build_only_by_hand(self):
        flow = (ROOT / '.github/workflows/ios.yml').read_text()
        on = re.search(r'^on:\n((?:  .*\n|\n)*)', flow, re.M).group(1)
        self.assertEqual([l.strip() for l in on.splitlines() if l.strip() and not l.strip().startswith('#')], ['workflow_dispatch:'])
        for uses in re.findall(r'uses: (\S+)', flow):
            self.assertRegex(uses, r'@[0-9a-f]{40}$')

    def test_native_sides_agree(self):
        java = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MachineShellPlugin.java').read_text()
        swift = (MOBILE / 'ios/App/App/MachineShellPlugin.swift').read_text()
        js = (MOBILE / 'www/app.js').read_text()
        for method in sorted(set(re.findall(r'shell\.(\w+)\(', js))):
            self.assertIn(f'public void {method}(PluginCall', java, method)
            self.assertIn(f'name: "{method}"', swift, method)
        for side in (java, swift):
            self.assertIn('app.themachine.computer', side)
            self.assertIn('computer.themachine.app', side)
        project = (MOBILE / 'ios/App/App.xcodeproj/project.pbxproj').read_text()
        for name in ('MachineShellPlugin.swift in Sources', 'ShareViewController.swift in Sources',
                     'ShareExtension.appex in Embed App Extensions', 'CODE_SIGN_ENTITLEMENTS = App/App.entitlements'):
            self.assertIn(name, project)
        manifest = (MOBILE / 'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertIn('android:networkSecurityConfig="@xml/network_security_config"', manifest)
        self.assertIn('cleartextTrafficPermitted="false"', (MOBILE / 'android/app/src/main/res/xml/network_security_config.xml').read_text())
        self.assertNotIn('armv7', (MOBILE / 'ios/App/App/Info.plist').read_text())


if __name__ == '__main__':
    unittest.main()
