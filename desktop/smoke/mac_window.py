"""The dashboard's own window on a Mac, used as a person would: mac.py's other half, with the same arguments, for the same
throwaway computer only."""
import json
import os
import pathlib
import subprocess
import sys
import threading
import time

from mac_tools import (
    A, C, CMD, CTRL, ENTER, ESCAPE, F, ID, LIBRARY, MAIL, NAME, PORT, Q, V, VERSION, W, all_windows, App, click, drag,
    finish, fresh, in_front, key, need, need_window, other, out, page, png, press, run, sandbox, saved, says, screens,
    step, until, work_area, write,
)
from standin import Machine

HERE = f'http://127.0.0.1:{PORT}'
DOWNLOADS = pathlib.Path.home() / 'Downloads'
R, G, ZERO, PLUS, MINUS, COMMA, S, LEFT, M, FOUR, ONE = 15, 5, 29, 24, 27, 43, 1, 33, 46, 21, 18
SHIFT = 1 << 17
fresh()
(out / 'note.txt').write_text('made up')
(out / 'second.txt').write_text('made up too')
machine = Machine(PORT)
machine.window = machine.compact = True
elsewhere = Machine(PORT + 1)  # the account, at an address of its own
elsewhere.machine = machine
machine.account = elsewhere.at
print('macOS', VERSION, json.dumps(screens()), flush=True)


def ask(what):
    return run('osascript', '-e', f'tell application "System Events" to tell process "{NAME}" to {what}')


def titles():
    return ask('get name of every window').stdout.strip()


def menu(of, name):
    made = ask(f'click menu item "{name}" of menu 1 of menu bar item "{of}" of menu bar 1')
    need(made.returncode == 0, made.stderr)
    time.sleep(0.5)


def sheet():
    told = ask('get value of static texts of sheet 1 of window 1')
    return told.stdout.strip() if told.returncode == 0 else ''


def here(selector, name='app'):
    """Where something in the window is on the screen: its page may be zoomed, under the title bar."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [e.x + e.width / 2, e.y + e.height / 2, innerWidth, innerHeight] }})()')
    r = need_window(app.window() if name == 'app' else app.settings())
    by = r.width / at[2]
    return round(r.left + at[0] * by), round(r.bottom - (at[3] - at[1]) * by)


def tap(selector, name='app'):
    click(*here(selector, name))


def told(selector='#told', name='app'):
    return says(selector, name)


def text(selector='#panel'):
    return told(selector).replace('\n', ' | ')


def dashboard():
    return until(lambda: 'Stand-in dashboard' in told('h1'), 20)


def gone_to(at, seconds=30):
    found = until(lambda: at in machine.left or at in elsewhere.left, seconds)
    run('osascript', '-e', 'tell application "Safari" to quit')
    until(lambda: 'Safari' not in in_front(), 8)
    back_to_it()
    return found


def back_to_it():
    if ID not in in_front():
        run('open', sandbox)
    need(until(lambda: ID in in_front(), 10), 'in front: ' + in_front())
    time.sleep(0.5)


def landed(name):
    found = until(lambda: (DOWNLOADS / name).exists(), 15)
    need(found, f'{name} in {[p.name for p in DOWNLOADS.iterdir()]}')
    need(until(lambda: told() == json.dumps({'saved': name}, separators=(',', ':')), 10), f'the page is told: {told()}')


def start(window=True, **kw):
    global app
    app = App(sandbox, window=window, **kw)
    need(until(lambda: app.answers('app'), 60), 'its page answers')
    return app


def stop(how=None):
    (how or (lambda: app.again('--quit')))()
    need(app.ended(), 'the process is gone')


def kind():
    return run('lsappinfo', 'info', '-only', 'ApplicationType', ID).stdout.strip()


def settings():
    menu('The Machine', 'Settings…') if not app.settings() else None
    need(until(app.settings), 'its window')
    time.sleep(0.6)


def switch(name, on=None):
    tap('#' + name, 'settings')
    time.sleep(1)
    return page('settings', f'document.querySelector("#{name}").checked')


def no_network():
    """Python, not the app, may be asked about: it is said no to, as it needs nothing there."""
    while True:
        of = 'tell application "System Events" to tell process "UserNotificationCenter"'
        if 'Python' in run('osascript', '-e', f'{of} to get value of static texts of window 1').stdout:
            run('osascript', '-e', f'{of} to click button "Don’t Allow" of window 1')
        time.sleep(3)


threading.Thread(target=no_network, daemon=True).start()
dark = lambda on: run('osascript', '-e', f'tell application "System Events" to tell appearance preferences to set dark mode to {str(on).lower()}')  # noqa: E731
ours = other()
start(account=elsewhere.at)


@step('first start')
def _():
    need(until(app.window, 60), f'the window shows {app.plain()}')
    time.sleep(2)
    need(ID in in_front(), in_front())
    need('Foreground' in kind(), kind())
    print([(x.get('kCGWindowOwnerName'), x.get('kCGWindowName'), x['kCGWindowLayer']) for x in all_windows()], flush=True)
    need(not app.box() and not app.robot(), f'one thing at a time {app.raw()}')
    need('Sign in' in text(), text())
    r = app.window()
    need(page('app', 'innerHeight') < r.height, f'its page is below the title bar {r} {page("app", "innerHeight")}')
    return f'{r} on {work_area()}; {text()}; {titles()}'


@step('sign in by address')
def _():
    tap('#other')
    need(until(lambda: told('#address') is not None and page('app', 'document.activeElement.id') == 'address', 5), 'the field has the keys')
    png('self-hosted')
    write('nowhere.invalid')
    key(ENTER)
    need(until(lambda: told('#error'), 30), 'a wrong one is told')
    png('wrong-address')
    tap('#address')
    key(A, CMD)
    run('pbcopy', input=HERE)
    key(V, CMD)
    key(ENTER)
    need(dashboard(), 'the dashboard')
    seen = machine.seen[-1]
    need(seen.get('desktop') == '1', f'it knows where it is: {seen}')
    need(until(lambda: told('#ipc') == 'refused', 8), 'it gets none of the app: ' + told('#ipc'))
    need(not told(), told())
    return seen


@step('the robot is away while it is in front')
def _():
    time.sleep(3)
    need(not app.robot(), 'away')
    other()
    need(until(app.robot, 8), 'another program in front: there')
    back_to_it()
    need(until(lambda: not app.robot(), 8), 'and away again')
    return titles()


@step('links')
def _():
    wrong = []
    for selector, at in (('#web', '/out?web'), ('#opens', '/out?opens'), ('#here', '/out?here'), ('#goes', '/out?goes'), ('#blank', '/out?blank')):
        del machine.left[:]
        tap(selector)
        if not gone_to(at):
            wrong.append(f'{selector}: {machine.left}')
        if not dashboard():
            wrong.append(f'{selector}: not the dashboard any more')
            png('left-' + selector[1:])
    need(not wrong, wrong)


@step('a link in a frame')
def _():
    del machine.left[:]
    x, y = here('#frame')
    at = page('app', '(() => { const f = document.querySelector("#frame"), r = f.getBoundingClientRect(), a = f.contentDocument.querySelector("#framed").getBoundingClientRect(); return [a.x + a.width / 2 - r.width / 2, a.y + a.height / 2 - r.height / 2] })()')
    click(round(x + at[0]), round(y + at[1]))
    need(gone_to('/out?framed'), machine.left)


@step('mail links')
def _():
    for selector, to in (('#mail', 'mailto:a@b.example?subject=new'), ('#mailnew', 'mailto:a@b.example?subject=newer')):
        MAIL.unlink(missing_ok=True)
        tap(selector)
        need(until(MAIL.exists, 8) and MAIL.read_text() == to, f'{selector}: {MAIL.read_text() if MAIL.exists() else ""}')
        need(dashboard(), 'it stays')


@step('its own place in a new window')
def _():
    del machine.seen[:]
    me = page('app', 'me')
    tap('#own')
    need(until(lambda: any(s.get('at') == '#person=7' for s in machine.seen), 8), machine.seen)
    need(len(app.plain()) == 1 and page('app', 'me') == me, 'the same page, in the same window')
    key(LEFT, CMD)
    need(until(lambda: page('app', 'location.hash') == '', 5), 'Command-[ is back: ' + str(page('app', 'location.hash')))


@step('the account in the browser')
def _():
    del elsewhere.hops[:]
    tap('#hop')
    need(until(lambda: elsewhere.hops, 30), 'its address is opened there')
    run('osascript', '-e', 'tell application "Safari" to quit')
    back_to_it()
    need(dashboard(), 'and the dashboard stays')
    return elsewhere.hops


@step('downloads')
def _():
    for old in [*DOWNLOADS.glob('[abc].txt'), *DOWNLOADS.glob('a (*.txt'), *DOWNLOADS.glob('sent*')]:
        old.unlink()
    wrong = []
    for selector, name in (('#file', 'a.txt'), ('#save', 'b.txt'), ('#blob', 'c.txt'), ('#sent', 'sent 4.bin'), ('#sentnew', 'sent 5.bin'), ('#file', 'a (1).txt')):
        try:
            tap(selector)
            landed(name)
        except AssertionError as e:
            wrong.append(f'{selector}: {e}')
            png('download-' + selector[1:])
        if len(app.plain()) != 1:
            wrong.append(f'{selector}: {app.plain()} {titles()}')
    need(not wrong, wrong)
    need(machine.left == [] or 'chat-file' not in str(machine.left), f'none in the browser {machine.left}')
    need('com.apple.quarantine' in run('xattr', str(DOWNLOADS / 'a.txt')).stdout, 'marked as from the internet')
    need(dashboard(), 'the dashboard stays')


@step('a PDF')
def _():
    tap('#pdf')
    need(until(lambda: len(app.plain()) == 2, 10), f'a window of its own {app.plain()}')
    time.sleep(2)
    png('a-pdf')
    was = titles()
    key(S, CMD)
    need(until(lambda: (DOWNLOADS / 'Plan B.pdf').exists(), 10), [p.name for p in DOWNLOADS.iterdir()])
    need((DOWNLOADS / 'Plan B.pdf').read_bytes().startswith(b'%PDF'), 'the file itself')
    key(W, CMD)
    need(until(lambda: len(app.plain()) == 1, 8), 'Command-W closes it')
    need(ID in in_front() and dashboard(), 'the dashboard is there')
    return was


@step('alert, confirm and prompt')
def _():
    tap('#alert')
    need(until(sheet, 5), 'it asks')
    time.sleep(0.5)
    png('alert')
    key(ENTER)
    need(until(lambda: told() == 'alerted', 5), told())
    for how, said in ((ESCAPE, 'confirm false'), (ENTER, 'confirm true')):
        tap('#confirm')
        need(until(sheet, 5), 'it asks')
        time.sleep(0.5)
        png('confirm')
        key(how)
        need(until(lambda: told() == said, 5), told())
    tap('#prompt')
    need(until(sheet, 5), 'it asks')
    time.sleep(0.5)
    write('Alex')
    png('prompt')
    key(ENTER)
    need(until(lambda: told() == 'prompt Alex', 5), told())
    tap('#prompt')
    need(until(sheet, 5), 'it asks')
    time.sleep(0.5)
    key(ESCAPE)
    need(until(lambda: told() == 'prompt null', 5), told())


@step('choose a file')
def _():
    tap('#pick')
    time.sleep(2)
    png('choose-a-file')
    key(G, CMD | SHIFT)
    time.sleep(1)
    write(str(out / 'note.txt'))
    time.sleep(0.5)
    key(ENTER)
    time.sleep(1)
    key(ENTER)
    need(until(lambda: told('#picked') == 'note.txt', 8), told('#picked'))


@step('drop files')
def _():
    source = out.parent / 'source'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-o', str(source), str(pathlib.Path(__file__).with_name('source.m')))
    need(made.returncode == 0, made.stderr)
    r = need_window(app.window())
    grab = subprocess.Popen([str(source), str(out / 'note.txt'), str(out / 'second.txt')])
    try:
        time.sleep(1.5)
        x, y = here('#drop')
        need(not (40 <= x <= 440 and 100 <= y <= 200), f'the drop is beside it: {x},{y} in {r}')
        drag((100, 150), (x, y))
        need(until(lambda: told() == 'dropped note.txt, second.txt', 6), told())
    finally:
        grab.terminate()
    need(dashboard(), 'and the page stays')


@step('copy and paste')
def _():
    tap('#field')
    key(A, CMD)
    key(C, CMD)
    need(until(lambda: run('pbpaste').stdout == 'some words', 3), run('pbpaste').stdout)
    run('pbcopy', input='pasted')
    key(V, CMD)
    need(until(lambda: page('app', '$("#field").value') == 'pasted', 3), page('app', '$("#field").value'))
    key(6, CMD)  # Z
    need(until(lambda: page('app', '$("#field").value') == 'some words', 3), page('app', '$("#field").value'))


@step('find')
def _():
    tall = page('app', 'innerHeight')
    key(F, CMD)
    need(until(lambda: page('app', 'innerHeight') < tall, 5), f'the bar takes its room {tall} {page("app", "innerHeight")}')
    write('last needle')
    time.sleep(1)
    png('find')
    need(until(lambda: page('app', 'scrollY') > 100, 5), f'it shows it {page("app", "scrollY")}')
    key(A, CMD)
    write('needle')
    found = lambda: page('app', '(r => r.startContainer.parentNode.textContent.slice(0, 3) + r.startOffset)(getSelection().getRangeAt(0))')
    time.sleep(1)
    places = [found()]
    for n in range(3):
        key(ENTER)
        time.sleep(0.6)
        places.append(found())
    need(len(set(places[:3])) == 3 and places[3] == places[0], f'one after the other {places}')
    key(G, CMD | SHIFT)
    time.sleep(0.6)
    need(found() == places[2], f'and back {found()} {places}')
    png('found')
    write('zzz')
    time.sleep(1)
    png('not-found')
    key(ESCAPE)
    need(until(lambda: page('app', 'innerHeight') == tall, 5), 'Escape ends it')
    page('app', 'scrollTo(0, 0)')
    key(C, CMD)


@step('zoom')
def _():
    wide = page('app', 'innerWidth')
    key(PLUS, CMD)
    key(PLUS, CMD)
    need(until(lambda: abs(page('app', 'innerWidth') - wide / 1.25) < 4, 5), f'{wide} {page("app", "innerWidth")}')
    png('zoomed')
    need(saved()['zoom'] == 1.25, saved())
    key(R, CMD)
    time.sleep(2)
    need(dashboard() and abs(page('app', 'innerWidth') - wide / 1.25) < 4, 'also after Reload')
    key(ZERO, CMD)
    need(until(lambda: page('app', 'innerWidth') == wide, 5), 'Command-0')
    key(MINUS, CMD)
    need(until(lambda: page('app', 'innerWidth') > wide, 5), 'and smaller')
    key(ZERO, CMD)


@step('close and open again')
def _():
    me, at = page('app', 'me'), repr(app.window())
    key(W, CMD)
    need(until(lambda: not app.window(), 5), 'closed')
    need(app.pids(), 'it keeps running')
    need(until(app.robot, 8), 'the robot is there')
    run('open', sandbox)
    need(until(app.window, 8), 'the Dock icon opens it')
    need(page('app', 'me') == me and repr(app.window()) == at, 'where it was')
    need(len(app.pids()) == 1, app.pids())
    menu('The Machine', 'Hide The Machine')
    need(until(lambda: not app.window(), 8), 'hidden')
    run('open', sandbox)
    need(until(app.window, 8), 'and back')
    key(M, CMD)
    need(until(lambda: not app.window(), 8), 'in the Dock')
    run('open', sandbox)
    need(until(app.window, 8), 'and back')


@step('full screen')
def _():
    was = app.window()
    key(F, CMD | CTRL)
    whole = screens()[0]['whole']
    need(until(lambda: app.window() and app.window().width == whole[2] - whole[0] and app.window().height >= whole[3] - whole[1] - 60, 10), f'{app.window()} on {whole}')
    time.sleep(2)
    png('full-screen')
    need(not app.robot(), 'no robot over it')
    key(W, CMD)
    need(until(lambda: not app.window(), 10), 'closed')
    time.sleep(2)
    png('closed-from-full-screen')
    run('open', sandbox)
    need(until(app.window, 8), 'and back')
    need(until(lambda: repr(app.window()) == repr(was), 5), f'as it was: {app.window()}, {was}')


@step('its place is kept')
def _():
    ask('set position of (first window whose subrole is "AXStandardWindow") to {60, 70}')
    ask('set size of (first window whose subrole is "AXStandardWindow") to {700, 560}')
    time.sleep(1)
    at = repr(app.window())
    need('700x560' in at, at)
    png('small')
    stop(lambda: key(Q, CMD))
    start(account=elsewhere.at)
    need(until(app.window, 30), 'it opens')
    need(dashboard(), 'the dashboard, still signed in')
    need(repr(app.window()) == at, f'{app.window()}, {at}')
    return at


@step('settings')
def _():
    key(COMMA, CMD)
    need(until(app.settings, 8), 'Command-,')
    time.sleep(1)
    png('settings-light')
    dark(True)
    time.sleep(2)
    png('settings-dark')
    dark(False)
    s = {x: page('settings', f'document.querySelector("#{x}").checked') for x in ('robot', 'login')}
    need(s == {'robot': True, 'login': False}, s)
    key(W, CMD)
    need(until(lambda: not app.settings(), 5) and app.window(), 'Command-W closes only that')
    return f'{s}'


@step('without the robot')
def _():
    settings()
    need(switch('robot') is False, 'off')
    time.sleep(1)
    png('settings-without-robot')
    key(W, CMD)
    key(W, CMD)
    need(until(lambda: not app.window(), 5), 'the window closed')
    other()
    time.sleep(3)
    need(not app.robot() and not app.box(), f'no robot {app.raw()}')
    need(ask('get name of menu bar item 1 of menu bar 2').returncode != 0, 'no icon in the menu bar')
    run('open', sandbox)
    need(until(app.window, 8), 'the Dock opens it')
    stop()
    start(account=elsewhere.at)
    need(until(app.window, 30) and dashboard(), 'so after a start')
    other()
    time.sleep(3)
    need(not app.robot() and not app.box(), f'no robot {app.raw()}')


@step('notifications')
def _():
    back_to_it()
    settings()
    need(page('settings', 'document.querySelector("#notify-row").hidden') is False, 'offered without the robot')
    need(saved()['notify'] is True, f'on with the robot off {saved()["notify"]}')
    hint = told('#notify-hint', 'settings')
    png('notifications')
    if 'Not allowed' in hint:
        need(page('settings', 'document.querySelector("#notify").checked') is False, 'off while macOS refuses them')
    else:
        need(switch('notify') is False and saved()['notify'] is False, 'off')
        need(switch('robot') is True and switch('robot') is False and saved()['notify'] is False, 'and the robot leaves that so')
        need(switch('notify') is True, 'and on')
    return f'{hint}; the banner itself is NOT TESTED'


@step('the robot again')
def _():
    key(W, CMD) if app.settings() else None
    settings()
    if page('settings', 'document.querySelector("#robot").checked') is False:
        need(switch('robot') is True, 'on')
    key(W, CMD)
    other()
    need(until(app.robot, 8), 'the robot is there')
    need(ask('get name of menu bar item 1 of menu bar 2').returncode == 0, 'and its icon')


@step('closing quits, when the person wants that')
def _():
    back_to_it()
    settings()
    page('settings', '(() => { const s = document.querySelector("#quits"); s.value = "1"; s.dispatchEvent(new Event("change")) })()')
    need(until(lambda: saved().get('quits'), 5), saved())
    key(W, CMD)
    key(W, CMD)
    need(app.ended(), 'the process is gone')
    start(account=elsewhere.at)
    need(until(app.window, 30) and dashboard(), 'the window')
    settings()
    page('settings', '(() => { const s = document.querySelector("#quits"); s.value = ""; s.dispatchEvent(new Event("change")) })()')
    need(until(lambda: not saved().get('quits'), 5), saved())
    key(W, CMD)


@step('start at login')
def _():
    settings()
    on = switch('login')
    png('at-login')
    said = told('#error', 'settings')
    if on:
        need(switch('login') is False, 'and off again')
    key(W, CMD) if app.settings() else None
    return f'{"works" if on else "NOT TESTED: macOS refuses it for this build"} {said}'


@step('from the robot')
def _():
    key(W, CMD)
    need(until(lambda: not app.window(), 5), 'the window closed')
    other()
    need(until(app.robot, 8), 'the robot')
    del machine.seen[:]
    click(*app.center())
    need(until(app.box, 8) and until(lambda: says('#todos'), 10), 'its box')
    press(app, '#more')
    time.sleep(1)
    png('robot-menu')
    press(app, '#menu-dashboard')
    need(until(app.window, 8), 'Open dashboard is this window')
    need(until(lambda: ID in in_front(), 5), 'in front: ' + in_front())
    need(until(lambda: not app.box(), 5), 'the box closes')


@step('the box and the window together')
def _():
    ask('set size of (first window whose subrole is "AXStandardWindow") to {640, 560}')
    app.again('--toggle')
    need(until(app.box, 8), 'the box over it')
    need(until(lambda: says('#todos'), 10), 'its list')
    press(app, '#todos li:nth-child(1) .name')
    need(until(app.card, 10), 'a to-do in the box')
    time.sleep(2)
    png('box-and-window')
    need(dashboard() and told('h1', 'card').startswith('To-do'), 'both are signed in')
    me = page('app', 'me')
    page('app', 'location.hash = "card=aa02"')
    time.sleep(1)
    need('aa02' in page('app', 'location.hash') and 'aa01' in told('h1', 'card'), 'each its own')
    key(ESCAPE)
    key(ESCAPE)
    need(until(lambda: not app.box(), 5), 'the box closes')
    need(page('app', 'me') == me, 'the window is as it was')
    return in_front()


@step('a page that ends')
def _():
    back_to_it()
    me = page('app', 'me')
    pids = [int(x) for x in run('pgrep', '-f', 'com.apple.WebKit.WebContent').stdout.split()]
    need(pids, 'its process')
    for pid in pids:
        os.kill(pid, 9)
    need(until(lambda: app.answers('app') and page('app', 'typeof me === "string" ? me : ""') not in ('', me), 20), 'a fresh page')
    need(dashboard(), 'the dashboard')


@step('signed out')
def _():
    machine.away = elsewhere.at + '/open?to=' + 'app'
    key(R, CMD)
    need(until(lambda: 'Signed out' in text(), 10), text())
    png('signed-out')
    del elsewhere.links[:]
    tap('#go')
    need(until(lambda: elsewhere.links, 40), 'the account opens in the browser')
    png('waiting-for-the-browser')
    machine.away = None
    need(run('open', '-a', sandbox, elsewhere.links[-1]).returncode == 0, 'the link it goes to')
    time.sleep(2)
    run('osascript', '-e', 'tell application "Safari" to quit')
    found = text() if not dashboard() else 'back in the dashboard'
    if 'dashboard' not in found:
        need(until(lambda: told('#error'), 1), 'or it says why: ' + found)
        return 'the sign-in itself is over https only, see mac.py: ' + found
    return found


@step('unreachable')
def _():
    stop()
    machine.stop()
    start(account=elsewhere.at)
    need(until(lambda: 'reach' in text(), 40), text())
    png('offline-light')
    dark(True)
    time.sleep(2)
    png('offline-dark')
    dark(False)
    tap('#go')
    time.sleep(6)
    need('reach' in text(), text())
    return text()


@step('reachable again')
def _():
    global machine
    machine = Machine(PORT)
    machine.window = machine.compact = True
    machine.account, elsewhere.machine = elsewhere.at, machine
    tap('#go')
    need(dashboard(), text())


@step('light and dark, small and large')
def _():
    area = work_area()
    for name, w, h in (('1024', 1024, 640), ('large', area[2] - area[0], area[3] - area[1])):
        ask(f'set position of (first window whose subrole is "AXStandardWindow") to {{{area[0]}, {area[1]}}}')
        ask(f'set size of (first window whose subrole is "AXStandardWindow") to {{{w}, {h}}}')
        for on in (False, True):
            dark(on)
            time.sleep(2)
            png(f'{name}-{"dark" if on else "light"}')
    dark(False)
    return app.window()


def second(look):
    """At two pixels a point, on a screen that isn't there."""
    maker = out.parent / 'screen'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-framework', 'CoreGraphics', '-Wl,-U,_OBJC_CLASS_$_CGVirtualDisplay', '-o', str(maker), str(pathlib.Path(__file__).with_name('screen.m')))
    need(made.returncode == 0, made.stderr)
    runs = subprocess.Popen([str(maker)], stdout=subprocess.PIPE, text=True)
    try:
        if not until(lambda: len(screens()) == 2, 10):
            return print('no second screen here', flush=True)
        time.sleep(2)
        area = work_area(1)
        ask(f'set position of (first window whose subrole is "AXStandardWindow") to {{{area[0] + 20}, {area[1] + 20}}}')
        ask('set size of (first window whose subrole is "AXStandardWindow") to {1200, 700}')
        time.sleep(3)
        look()
    finally:
        runs.terminate()
        runs.wait()
        time.sleep(2)


@step('the real dashboard')
def _():
    """The sandbox's: the real pages, on made-up data (sandbox/run.py), when it runs here."""
    root = pathlib.Path(__file__).resolve().parents[2]
    log = out / 'sandbox.txt'
    if not (root / 'sandbox' / 'run.py').exists():
        return 'NOT TESTED: no sandbox here'
    with log.open('w') as told_to:
        runs = subprocess.Popen([sys.executable, str(root / 'sandbox/run.py'), '--state', 'busy', '--port', '8970', '--dir', str(out.parent / 'sandbox-dir')], stdout=told_to, stderr=told_to)
    try:
        if not until(lambda: 'sandbox (' in log.read_text() or runs.poll() is not None, 60) or runs.poll() is not None:
            return 'NOT TESTED: ' + log.read_text()[-300:]
        stop()
        fresh()
        start(account=elsewhere.at)
        need(until(app.window, 30), 'the window')
        need(until(lambda: text(), 10), 'asks to sign in')
        tap('#other')
        time.sleep(0.5)
        write('http://127.0.0.1:8970')
        key(ENTER)
        need(until(lambda: page('app', 'location.port') == '8970', 20), page('app', 'location.href'))
        time.sleep(6)
        area = work_area()
        for name, w, h in (('1024', 1024, 640), ('large', area[2] - area[0], area[3] - area[1])):
            ask(f'set position of (first window whose subrole is "AXStandardWindow") to {{{area[0]}, {area[1]}}}')
            ask(f'set size of (first window whose subrole is "AXStandardWindow") to {{{w}, {h}}}')
            for on in (False, True):
                dark(on)
                time.sleep(3)
                png(f'dashboard-{name}-{"dark" if on else "light"}')
        dark(False)
        settings()
        png('dashboard-settings')
        key(W, CMD)
        key(W, CMD)
        other()
        need(until(app.robot, 8), 'the robot')
        click(*app.center())
        need(until(app.box, 8), 'its box')
        time.sleep(4)
        png('dashboard-box')
        key(ESCAPE)
        back_to_it()
        second(lambda: png('dashboard-on-two-screens'))
        return f"{page('app', 'document.title')} {page('app', 'innerWidth')}"
    finally:
        runs.terminate()


@step('the microphone')
def _():
    stop()
    machine.window = True
    fresh()
    start(account=elsewhere.at)
    need(until(app.window, 30) and until(lambda: text(), 10), 'the window')
    tap('#other')
    time.sleep(0.5)
    write(HERE)
    key(ENTER)
    need(dashboard(), text())
    tap('#mic')
    time.sleep(4)
    png('microphone-asked')
    found = told()
    if found == 'asking':
        return 'macOS asks the person, which stays unanswered here'
    return found


@step('quit')
def _():
    stop() if app.pids() else None
    need(not app.pids(), 'no process')
    sent = {a for a, _, _ in machine.actions}
    need(not sent, f'nothing done by itself: {sent}')
    crashes = [p.name for p in (LIBRARY / 'Logs/DiagnosticReports').glob(NAME + '*')]
    need(not crashes, f'no crash reports: {crashes}')


app.kill()
dark(False)
finish()
(out / 'second.txt').unlink()
