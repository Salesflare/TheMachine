"""The build for people, as a download starts it: its window opens to sign in, and a start at login has only the robot, in
its corner and on top. On X11 (linux.sh) or on Wayland (wayland.sh); with Wayland's layer-shell the robot is a layer surface,
never a window. No Machine, no sign-in. For CI's throwaway computers only (desktop.yml).

  python3 smoke/started.py <folder for the pictures> <program> [its first arguments, as for an AppImage: env ... file]
"""
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
import threading
import time
import traceback

if not (pathlib.Path.home() / '.made-up-home').exists():
    sys.exit('only by linux.sh or wayland.sh')
out = pathlib.Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
program = sys.argv[2:]
WAYLAND = bool(os.environ.get('WAYLAND_DISPLAY'))
results = []


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, timeout=30)


def until(what, seconds):
    end = time.time() + seconds
    while True:
        found = what()
        if found or time.time() > end:
            return found
        time.sleep(0.5)


def need(ok, text):
    if not ok:
        raise AssertionError(text)


def png(name):
    time.sleep(1)
    file = str(out / f'{name}.png')
    run(*(('grim', file) if WAYLAND else ('import', '-window', 'root', file)))


class Started:
    """The program, in a session of its own; on Wayland with what it says to the compositor about its surfaces."""

    def __init__(self, name, *args):
        env = dict(os.environ, WAYLAND_DEBUG='client') if WAYLAND else dict(os.environ)
        self.told = (out / f'{name}.txt').open('w')
        self.said = []
        self.process = subprocess.Popen([*program, *args], env=env, stdin=subprocess.DEVNULL, stdout=self.told, stderr=subprocess.PIPE,
                                        text=True, errors='replace', start_new_session=True)
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()

    def read(self):
        for line in self.process.stderr:
            if re.match(r'\s*\[\s*\d+\.\d+\]', line):  # WAYLAND_DEBUG: only what makes and shows its surfaces
                if not re.search(r'layer|xdg_toplevel', line):
                    continue
                self.said.append(line.strip())
            self.told.write(line)
            self.told.flush()

    def running(self):
        return self.process.poll() is None

    def stop(self):
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
            self.process.wait(10)
        except ProcessLookupError:
            pass
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait()
        self.reader.join(5)


def x11_windows():
    """Each visible window: its name, size, and whether it stays on top."""
    found = []
    for window in run('xdotool', 'search', '--onlyvisible', '--name', '').stdout.split():
        geometry = dict(line.split('=') for line in run('xdotool', 'getwindowgeometry', '--shell', window).stdout.split() if '=' in line)
        state = run('xprop', '-id', window, '_NET_WM_STATE').stdout
        if 'WIDTH' in geometry and int(geometry['WIDTH']) > 40:
            found.append({'name': run('xdotool', 'getwindowname', window).stdout.strip(), 'width': int(geometry['WIDTH']), 'height': int(geometry['HEIGHT']),
                          'above': '_NET_WM_STATE_ABOVE' in state or '_NET_WM_STATE_SKIP_TASKBAR' in state})
    return found


def wayland_windows():
    """Each window the compositor has (layer surfaces are none of them)."""
    found = []

    def walk(node):
        if node.get('type') in ('con', 'floating_con') and (node.get('app_id') or node.get('window')) and node.get('visible'):
            found.append({'name': node.get('name') or '', 'width': node['rect']['width'], 'height': node['rect']['height'], 'above': False})
        for child in node.get('nodes', []) + node.get('floating_nodes', []):
            walk(child)
    walk(json.loads(run('swaymsg', '-t', 'get_tree', '-r').stdout or '{}'))
    return found


def windows():
    return wayland_windows() if WAYLAND else x11_windows()


def signin():
    return next((w for w in windows() if w['name'].startswith('The Machine') and not w['above']), None)


def robot_layer(app):
    """The robot's layer surface (namespace the-machine-robot), and that the compositor configured it to be shown."""
    made = [re.search(r'new id zwlr_layer_surface_v1[@#](\d+)', line) for line in app.said if 'get_layer_surface' in line and '"the-machine-robot"' in line]
    ids = {m.group(1) for m in made if m}
    return next((i for i in ids if any(re.search(rf'zwlr_layer_surface_v1[@#]{i}\.configure\(', line) for line in app.said)), None)


def robot(app):
    if WAYLAND:
        return robot_layer(app)
    return next((w for w in windows() if w['above'] and 40 <= w['width'] < 250), None)


def step(name):
    def do(f):
        try:
            results.append((name, True, f() or ''))
        except Exception as e:  # noqa: BLE001 (the next step still tells something)
            results.append((name, False, f'{type(e).__name__}: {e}'))
            traceback.print_exc()
        png(name.replace(' ', '-'))
        print(f"{'ok  ' if results[-1][1] else 'FAIL'} {name}  {results[-1][2]}", flush=True)
    return do


app = Started('first')


@step('its window opens to sign in')
def _():
    window = until(signin, 90)
    need(window, f'the window {windows()}; running: {app.running()}')
    time.sleep(3)
    need(app.running(), f'and it keeps running {app.process.returncode}')
    return f'{window}, on {"Wayland" if WAYLAND else "X11"}'


@step('it quits')
def _():
    subprocess.run([*program, '--quit'], timeout=30, capture_output=True)
    need(until(lambda: not app.running(), 15), 'it ended')
    return f'exit {app.process.returncode}'


app.stop()
app = Started('login', '--login')


@step('at login only the robot')
def _():
    found = until(lambda: robot(app), 60)
    need(found, f'the robot {windows()}; running: {app.running()}; {app.said[-10:]}')
    time.sleep(3)
    need(app.running(), f'and it keeps running {app.process.returncode}')
    if WAYLAND:  # a layer surface, not a window the compositor places
        need(not windows(), f'no window: {windows()}')
        return f'layer surface zwlr_layer_surface_v1 {found}'
    return f'{found}, on top'


app.stop()
lines = [f"{'ok  ' if ok else 'FAIL'} {name}  {told}" for name, ok, told in results]
(out / 'results.txt').write_text('\n'.join(lines) + '\n')
sys.exit(not all(ok for _, ok, _ in results))
