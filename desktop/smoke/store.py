"""The Mac App Store's build (mac/bundle.sh, STORE=1), in its App Sandbox, on CI's own throwaway computer (desktop.yml,
mac-store). Signed ad hoc, with the sandbox's entitlements.

  python3 smoke/store.py probe <build> <folder for the pictures>       sandboxed, its container, the robot and the box
  python3 smoke/store.py run <smoke script> <its arguments>...          mac.py, window.py or hangs.py, with the app's
                                                                        folders where the sandbox puts them, and what
                                                                        the store's build does otherwise (STORE)
  python3 smoke/store.py denials <log show output>                      what the sandbox denied, counted

In the sandbox the app's Library is in ~/Library/Containers/<id>/Data, and it reads and writes nowhere else: the test's
mail file and the made-up certificate go there too.
"""
import collections
import ctypes
import os
import pathlib
import plistlib
import re
import runpy
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
NAME = 'the-machine-desktop'
sys.path.insert(0, str(HERE))
os.environ['MACHINE_STORE'] = '1'


def own_id(build):
    """Its ID, which may be another than the direct download's (desktop.yml, MAS_BUNDLE_ID)."""
    return plistlib.loads((pathlib.Path(build) / 'Contents/Info.plist').read_bytes())['CFBundleIdentifier']


ID = own_id(sys.argv[2] if sys.argv[1] == 'probe' else sys.argv[3]) if sys.argv[1] in ('probe', 'run') else ''
DATA = pathlib.Path.home() / 'Library/Containers' / ID / 'Data'


def sandboxed(pid):
    system = ctypes.CDLL('/usr/lib/libSystem.B.dylib')
    system.sandbox_check.restype, system.sandbox_check.argtypes = ctypes.c_int, [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    return system.sandbox_check(pid, None, 0) == 1  # SANDBOX_FILTER_NONE: whether it has one at all


def contained(tools):
    tools.ID = ID
    tools.LIBRARY = DATA / 'Library'
    tools.MAIL = DATA / 'mail.txt'
    if tools.CERTIFICATE:
        copy = DATA / 'certificate'
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(tools.CERTIFICATE, copy)
        tools.CERTIFICATE = copy
    return tools


def probe(build, folder):
    sys.argv = [sys.argv[0], build, build, folder]
    import mac_tools as t
    contained(t)
    t.fresh()
    entitled = subprocess.run(['codesign', '-d', '--entitlements', ':-', build], capture_output=True, text=True).stdout
    t.other()
    app = t.App(build, debug=False)

    @t.step('signed with the sandbox')
    def _():
        t.need('com.apple.security.app-sandbox' in entitled, entitled)
        return ' '.join(re.findall(r'com\.apple\.security\.[\w.-]+', entitled))

    @t.step('it runs in the App Sandbox')
    def _():
        t.need(sandboxed(app.pid), f'process {app.pid} has no sandbox')
        t.need(t.until(lambda: (DATA / 'Library').is_dir(), 20), f'no container at {DATA}')
        children = subprocess.run(['pgrep', '-P', str(app.pid)], capture_output=True, text=True).stdout.split()
        return f'pid {app.pid} sandboxed; container {DATA}; children {children}'

    @t.step('the robot floats above other windows')
    def _():
        t.need(t.until(app.robot, 60), 'the robot shows')
        levels = [(x['kCGWindowLayer'], t.Rect(x['kCGWindowBounds'])) for x in app.raw()]
        t.need(all(level > 0 for level, _ in levels), str(levels))
        ok, told = t.in_corner(app)
        t.need(ok, told)
        return f'{told}; levels {levels}; in front {t.in_front()}'

    @t.step('the sign-in box opens by itself')
    def _():
        t.need(t.until(app.box, 15), 'the box opens')

    @t.step('one of it, and no socket in /tmp')
    def _():
        t.need((DATA / '.one').is_socket(), f'its socket in {DATA}')
        t.need(not list(pathlib.Path('/tmp').glob(f'{ID}*')) and not list(pathlib.Path('/private/tmp').glob(f'{ID.replace(".", "_")}*')), 'none in /tmp')
        t.need(app.again('--toggle') == 0, 'a second start ends')
        t.need(t.until(lambda: not app.box(), 10), 'and the robot toggles the box')
        t.need(len(app.pids()) == 1, app.pids())
        return f'{len(app.pids())} process'

    @t.step('no updater')
    def _():
        program = pathlib.Path(build, 'Contents/MacOS', NAME).read_bytes()
        t.need(b'tauri-plugin-updater' not in program and b'plugin:updater' not in program, 'nothing of the updater')
        return 'the store updates it'

    @t.step('quit from a second start')
    def _():
        app.again('--quit')
        t.need(app.ended(), 'the process is gone')

    app.kill()
    t.finish()


def unasked():
    """What macOS still asks from a step before (the microphone, which window.py leaves unanswered): Don't Allow, so that
    it is no longer in front of the next."""
    for owner in ('UserNotificationCenter', 'universalAccessAuthWarn', 'CoreServicesUIAgent', 'the-machine-desktop'):
        subprocess.run(['osascript', '-e', f'tell application "System Events" to tell process "{owner}" to repeat with w in windows\n'
                        'repeat with b in buttons of w\nif name of b starts with "Don" then click b\nend repeat\nend repeat'],
                       capture_output=True, timeout=20, check=False)


def run(script, *args):
    sys.argv = [script, *args]
    if not DATA.is_dir():
        sys.exit(f'no container at {DATA}: run probe first')
    unasked()
    import mac_tools
    contained(mac_tools)
    mac_tools.STORE = True
    runpy.run_path(script, run_name='__main__')


LINE = re.compile(r'Sandbox: (\S+?)\((\d+)\) deny\(\d+\) (\S+)(?: (.*))?')


def denials(file):
    counted = collections.Counter()
    for line in pathlib.Path(file).read_text(errors='replace').splitlines():
        found = LINE.search(line)
        if found:
            process, _, operation, target = found.groups()
            target = re.sub(r'\b\d{3,}\b', 'N', (target or '').strip())
            counted[(process, operation, target[:160])] += 1
    lines = [f'{n:5}  {p}  {o}  {t}' for (p, o, t), n in counted.most_common()]
    summary = pathlib.Path(file).with_name('sandbox-denials-counted.txt')
    summary.write_text('\n'.join(lines) + '\n')
    print(f'{sum(counted.values())} denials, {len(counted)} kinds')
    print('\n'.join(lines[:150]))


if __name__ == '__main__':
    {'probe': probe, 'run': run, 'denials': denials}[sys.argv[1]](*sys.argv[2:])
