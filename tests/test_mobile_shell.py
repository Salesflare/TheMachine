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
        files = sorted(str(f.relative_to(MOBILE)) for f in (MOBILE / 'tests').glob('*.test.js'))
        self.assertTrue(files)
        # Explicit files: node 24 (CI) takes a directory argument as a module to run, not a folder of tests
        run = subprocess.run(['node', '--test', *files], cwd=MOBILE, capture_output=True, text=True, timeout=120)
        self.assertEqual(run.returncode, 0, run.stdout[-3000:] + run.stderr[-2000:])

    def test_exact_pins(self):
        pkg = json.loads((MOBILE / 'package.json').read_text())
        for name, version in {**pkg['dependencies'], **pkg.get('devDependencies', {})}.items():
            self.assertRegex(version, r'^\d+\.\d+\.\d+$', name)
        self.assertEqual(pkg['license'], 'AGPL-3.0-only')
        self.assertRegex(pkg['scripts']['cap'], r'@capacitor/cli@\d+\.\d+\.\d+$')
        # The lockfile holds only the app's own packages, with licenses that fit AGPL (the CLI runs through npx)
        lock = json.loads((MOBILE / 'package-lock.json').read_text())['packages']
        for name, entry in lock.items():
            if name:
                self.assertIn(entry.get('license'), {'MIT', 'ISC', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', '0BSD'}, name)

    def test_webview_only_opens_machines(self):
        config = json.loads((MOBILE / 'capacitor.config.json').read_text())
        self.assertEqual(config['appId'], 'computer.themachine.app')
        self.assertEqual(sorted(config['server']['allowNavigation']), ['*.app.themachine.computer', '*.ts.net'])
        self.assertNotIn('url', config['server'])  # the start page is the app's own; the Machine is opened from it
        self.assertFalse(config['android']['allowMixedContent'])
        self.assertFalse(config['android']['webContentsDebuggingEnabled'])

    def test_release_build_needs_push_config(self):
        gradle = (MOBILE / 'android/app/build.gradle').read_text()
        guard = gradle[gradle.index("tasks.matching { it.name == 'preReleaseBuild' }"):]
        self.assertIn("if (!file('google-services.json').exists())", guard)
        self.assertIn('throw new GradleException', guard)
        self.assertIn('android/app/google-services.json', (MOBILE / '.gitignore').read_text())

    def test_ios_build_only_by_hand(self):
        flow = (ROOT / '.github/workflows/ios.yml').read_text()
        on = re.search(r'^on:\n((?:  .*\n|\n)*)', flow, re.M).group(1)
        triggers = [l.strip() for l in on.splitlines() if re.match(r'  \S', l) and not l.strip().startswith('#')]
        self.assertEqual(triggers, ['workflow_dispatch:'])
        # Signing secrets only on the upload step, only in this repository, and the key file never outlives the run
        upload = flow[flow.index('- name: Archive and upload to TestFlight'):]
        self.assertIn("github.repository == 'Salesflare/TheMachine'", upload)
        self.assertIn("trap 'rm -f \"$key\"' EXIT", upload)
        self.assertEqual(flow.count('secrets.'), upload.count('secrets.'))
        # Nothing uploads unless the archive holds the app and both extensions, each with the app group
        check = upload[upload.index(' archive |'):upload.index('-exportArchive')]
        for bundle in ('App.app', 'ShareExtension.appex', 'NotificationService.appex', 'group.computer.themachine.app'):
            self.assertIn(bundle, check)
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
                     'ShareExtension.appex in Embed App Extensions', 'CODE_SIGN_ENTITLEMENTS = App/App.entitlements',
                     'NotificationService.swift in Sources', 'NotificationService.appex in Embed App Extensions',
                     'PRODUCT_BUNDLE_IDENTIFIER = computer.themachine.app.notifications;'):
            self.assertIn(name, project)
        self.assertEqual(project.count('MachineNotice.swift in Sources */ = {isa = PBXBuildFile'), 2)  # the app and the extension
        manifest = (MOBILE / 'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertIn('android:networkSecurityConfig="@xml/network_security_config"', manifest)
        self.assertIn('cleartextTrafficPermitted="false"', (MOBILE / 'android/app/src/main/res/xml/network_security_config.xml').read_text())
        self.assertNotIn('armv7', (MOBILE / 'ios/App/App/Info.plist').read_text())
        # FCM's status bar icon: a monochrome one in every density, not the launcher icon (a plain circle)
        self.assertIn('android:resource="@drawable/ic_stat_notify"', manifest)
        for density in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi'):
            self.assertTrue((MOBILE / f'android/app/src/main/res/drawable-{density}/ic_stat_notify.png').exists(), density)

    def test_native_sides_take_only_443_and_8443(self):
        # The JavaScript side is tested in mobile/tests; the native checks must allow the same two ports, no others.
        java = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MachineShellPlugin.java').read_text()
        swift = (MOBILE / 'ios/App/App/MachineShellPlugin.swift').read_text()
        self.assertIn('static final int OWN_PORT = 8443;', java)
        self.assertIn('(port != 443 && port != OWN_PORT)) return null;', java)
        self.assertIn('static let ownPort = 8443', swift)
        self.assertIn('port == 443 || port == ownPort else { return nil }', swift)
        for side in (java, swift):
            self.assertNotIn('8080', side)

    def test_native_sides_take_a_dashboards_own_domain_and_check_it_first(self):
        # A self-hosted Machine on its own https domain, not only .ts.net: the same rule on both sides as in
        # www/machine-url.js (ownHost), its JVM test (android/app/src/test), and a manifest check before it is saved
        # that follows no redirects (www/app.js check, machine-url.js isMachine).
        java = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MachineShellPlugin.java').read_text()
        swift = (MOBILE / 'ios/App/App/MachineShellPlugin.swift').read_text()
        js = (MOBILE / 'www/machine-url.js').read_text()
        self.assertIn('if (!ownHost(host) || (port != 443 && port != OWN_PORT)) return null;', java)
        self.assertIn('guard ownHost(host), port == 443 || port == ownPort else { return nil }', swift)
        for side in (java, swift, js):
            self.assertIn('[a-z]{2,63}', side)  # a top level of letters: never an IP address
            self.assertIn('.ts.net', side)
        self.assertIn('c.setInstanceFollowRedirects(false);', java)
        # Only the start page may ask (a Machine's page could otherwise read other sites through it)
        self.assertRegex(java, r'public void check\(PluginCall call\) \{\s+bridge\.executeOnMainThread\(\(\) -> \{[^\n]*\n\s+if \(!onStartPage\(\)\)')
        self.assertRegex(swift, r'@objc func check\(_ call: CAPPluginCall\) \{\s+DispatchQueue\.main\.async \{[^\n]*\n\s+guard self\.onStartPage')
        self.assertIn('"manifest.webmanifest"', java)
        self.assertIn('completionHandler(nil)', swift)
        self.assertIn('"manifest.webmanifest"', swift)
        self.assertIn('.ephemeral', swift)
        self.assertIn("'Use the owner-authenticated Tailscale dashboard'", js)
        test = (MOBILE / 'android/app/src/test/java/computer/themachine/app/MachineAddressTest.java').read_text()
        self.assertIn('https://my.themachine.computer/', test)
        # The dashboard's own words that check: the manifest's name and its refusal for someone not its owner
        self.assertEqual(json.loads((ROOT / 'manifest.webmanifest').read_text())['name'], 'The Machine')
        self.assertIn("'Use the owner-authenticated Tailscale dashboard'", (ROOT / 'assistant.py').read_text())


    def test_web_features_only_for_the_machine(self):
        # What a browser gives the dashboard (the microphone, downloads, Back) the app gives it too, only on the Machine's
        # own address: Capacitor's own web listener list drops one a plugin adds while it loads, so MainActivity attaches
        java = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MachineShellPlugin.java').read_text()
        main = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MainActivity.java').read_text()
        swift = (MOBILE / 'ios/App/App/MachineShellPlugin.swift').read_text()
        manifest = (MOBILE / 'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertLess(main.index('super.onCreate'), main.index('.attach();'))
        self.assertRegex(main, r'if \(webView\.canGoBack\(\)\) webView\.goBack\(\);\s+else moveTaskToBack\(true\);')
        for perm in ('RECORD_AUDIO', 'MODIFY_AUDIO_SETTINGS'):
            self.assertIn(f'android.permission.{perm}', manifest)
        self.assertNotIn('android.permission.CAMERA', manifest)
        self.assertIn('<uses-feature android:name="android.hardware.microphone" android:required="false" />', manifest)
        # The microphone only, only for the Machine; nothing else a page asks for
        self.assertIn('if (!audioOnly || !shell.isMachine(request.getOrigin())) {\n                request.deny();\n                return;', java)
        # The phone's questions and its settings page: asked by the Machine's own page only
        self.assertIn('"MachinePhone", Collections.singleton(origin)', java)
        self.assertEqual(java.count('if (!mainFrame || !isMachine(source) || message.getData() == null) return;'), 2)
        self.assertIn('addScriptMessageHandler(PhoneHandler(plugin: self), contentWorld: .page, name: "machinePhone")', swift)
        self.assertIn('guard message.frameInfo.isMainFrame, let plugin = plugin, plugin.isMachine(message.frameInfo.securityOrigin)', swift)
        self.assertIn('Settings.ACTION_APPLICATION_DETAILS_SETTINGS', java)
        self.assertIn('UIApplication.openSettingsURLString', swift)
        self.assertIn('"MachineFiles", Collections.singleton(origin)', java)  # the files bridge exists only on that address
        self.assertIn('if (!mainFrame || !isMachine(source) ||', java)
        self.assertIn('type == .microphone && frame.isMainFrame && plugin?.isMachine(origin) == true ? .grant : .deny', swift)
        self.assertIn('guard message.frameInfo.isMainFrame, plugin?.isMachine(message.frameInfo.securityOrigin) == true', swift)
        self.assertIn('NSMicrophoneUsageDescription', (MOBILE / 'ios/App/App/Info.plist').read_text())
        self.assertNotIn('NSCameraUsageDescription', (MOBILE / 'ios/App/App/Info.plist').read_text())

if __name__ == '__main__':
    unittest.main()


class IOSNotifications(unittest.TestCase):
    """The Notification Service extension and the notification buttons (Shared/MachineNotice.swift)."""
    IOS = MOBILE / 'ios/App'

    def test_the_extension_is_a_notification_service_in_the_app_group(self):
        info = (self.IOS / 'NotificationService/Info.plist').read_text()
        self.assertIn('<string>com.apple.usernotifications.service</string>', info)
        self.assertIn('$(PRODUCT_MODULE_NAME).NotificationService', info)
        for entitlements in ('App/App.entitlements', 'NotificationService/NotificationService.entitlements'):
            self.assertIn('<string>group.computer.themachine.app</string>', (self.IOS / entitlements).read_text())
        # no new entitlement: only the app group, in the extension as in the Share extension
        self.assertEqual((self.IOS / 'NotificationService/NotificationService.entitlements').read_text(),
                         (self.IOS / 'ShareExtension/ShareExtension.entitlements').read_text())
        self.assertIn('<string>remote-notification</string>', (self.IOS / 'App/Info.plist').read_text())  # the clear push

    def test_buttons_unlock_first_and_never_send(self):
        shared = (self.IOS / 'Shared/MachineNotice.swift').read_text()
        self.assertIn('["prepare": "accept", "snooze": "snooze", "done": "complete"]', shared)
        self.assertIn('options: [.authenticationRequired]', shared)
        self.assertNotIn('.foreground', shared)
        self.assertNotIn('"send"', shared)
        self.assertIn('kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly', shared)
        self.assertIn('completionHandler(nil)', shared)  # never follows a redirect
        app = (self.IOS / 'App/AppDelegate.swift').read_text()
        self.assertIn('MachineActions.shared.install()', app)
        self.assertIn('"clear"', app)
        plugin = (self.IOS / 'App/MachineShellPlugin.swift').read_text()
        for call in ('MachineActions.shared.install()', 'MachineNotice.sweep()', 'MachineNotice.forget()', 'keepSignIn(saved)', '"fetch": true'):
            self.assertIn(call, plugin)

    def test_android_buttons_are_the_same_decisions(self):
        java = (MOBILE / 'android/app/src/main/java/computer/themachine/app/PushText.java').read_text()
        for action, choice in (('prepare', 'accept'), ('snooze', 'snooze'), ('done', 'complete')):
            self.assertIn(f'if ("{action}".equals(action)) return "{choice}";', java)
        service = (MOBILE / 'android/app/src/main/java/computer/themachine/app/MachinePushService.java').read_text()
        self.assertIn('.setAuthenticationRequired(true)', service)
        self.assertIn('"clear".equals(kind)', service)
        manifest = (MOBILE / 'android/app/src/main/AndroidManifest.xml').read_text()
        self.assertRegex(manifest, r'android:name="\.NotificationActions"\s+android:exported="false"')
