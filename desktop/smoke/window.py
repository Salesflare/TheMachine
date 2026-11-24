"""The dashboard's own window, used as a person would: the other half of mac.py and windows.py, with the same arguments, for the
same throwaway computers only. What differs is in on_mac.py, on_windows.py and on_linux.py."""
import importlib
import json
import pathlib
import subprocess
import sys
import time

from standin import Machine

on = importlib.import_module({'darwin': 'on_mac', 'win32': 'on_windows', 'linux': 'on_linux'}[sys.platform])
App, SYSTEM, PORT, MAIL, DOWNLOADS, ENTER, ESCAPE = on.App, on.SYSTEM, on.PORT, on.MAIL, on.DOWNLOADS, on.ENTER, on.ESCAPE
clipboard, click, dark, drag, fresh, here, hit, key, need, no_browser = on.clipboard, on.click, on.dark, on.drag, on.fresh, on.here, on.hit, on.key, on.need, on.no_browser
other, ours, out, page, png, press, sandbox, saved, says, step, until, write = on.other, on.ours, on.out, on.page, on.png, on.press, on.sandbox, on.saved, on.says, on.step, on.until, on.write
HERE = f'http://127.0.0.1:{PORT}'
fresh()
(out / 'note.txt').write_text('made up')
(out / 'second.txt').write_text('made up too')
machine = Machine(PORT)
machine.window = machine.compact = True
elsewhere = Machine(PORT + 1)  # the account, at an address of its own
elsewhere.machine = machine
machine.account = elsewhere.at
print(on.VERSION, json.dumps(on.area()), flush=True)


def tap(selector, name='app'):
    click(*here(app, selector, name))


def told(selector='#told', name='app'):
    return says(selector, name)


def text(selector='#panel'):
    return told(selector).replace('\n', ' | ')


def dashboard():
    return until(lambda: 'Stand-in dashboard' in told('h1'), 20)


def gone_to(at, seconds=30):
    found = until(lambda: at in machine.left or at in elsewhere.left, seconds)
    no_browser()
    back_to_it()
    return found


def back_to_it():
    on.back_to_it(app)


def landed(name):
    found = until(lambda: (DOWNLOADS / name).exists(), 40)
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


def settings():
    app.settings() or on.settings_open(app)
    need(until(app.settings), 'its window')
    time.sleep(0.6)


def switch(name, on=None):
    tap('#' + name, 'settings')
    time.sleep(1)
    return page('settings', f'document.querySelector("#{name}").checked')


other()
start(account=elsewhere.at)


@step('first start')
def _():
    need(until(app.window, 60), f'the window shows {app.plain()}')
    time.sleep(2)
    need(ours(), on.in_front())
    on.like_any_app(app)
    need(not app.box() and not app.robot(), f'one thing at a time {app.raw()}')
    need('Sign in' in text(), text())
    r = app.window()
    need(SYSTEM == 'linux' or page('app', 'innerHeight') < r.height, f'its page is below the title bar {r} {page("app", "innerHeight")}')
    return f'{r} on {on.area()}; {text()}; {on.names(app)}'


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
    hit('all')
    clipboard(HERE)
    hit('paste')
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
    return on.names(app)


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
    x, y = here(app, '#frame')
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
    hit('back')
    need(until(lambda: page('app', 'location.hash') == '', 5), 'back: ' + str(page('app', 'location.hash')))


@step('the account in the browser')
def _():
    del elsewhere.hops[:]
    tap('#hop')
    need(until(lambda: elsewhere.hops, 30), 'its address is opened there')
    no_browser()
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
            wrong.append(f'{selector}: {app.plain()} {on.names(app)}')
    need(not wrong, wrong)
    need(machine.left == [] or 'chat-file' not in str(machine.left), f'none in the browser {machine.left}')
    need(on.marked(DOWNLOADS / 'a.txt'), 'marked as from the internet')
    need(dashboard(), 'the dashboard stays')


@step('a PDF')
def _():
    tap('#pdf')
    need(until(lambda: len(app.plain()) == 2, 10), f'a window of its own {app.plain()}')
    time.sleep(2)
    png('a-pdf')
    was = on.names(app)
    hit('save')
    need(until(lambda: (DOWNLOADS / 'Plan B.pdf').exists(), 10), [p.name for p in DOWNLOADS.iterdir()])
    need((DOWNLOADS / 'Plan B.pdf').read_bytes().startswith(b'%PDF'), 'the file itself')
    hit('close')
    need(until(lambda: len(app.plain()) == 1, 8), 'it closes')
    need(ours() and dashboard(), 'the dashboard is there')
    return was


@step('alert, confirm and prompt')
def _():
    tap('#alert')
    need(until(lambda: on.dialog(app), 8), 'it asks')
    time.sleep(0.5)
    png('alert')
    key(ENTER)
    need(until(lambda: told() == 'alerted', 5), told())
    for how, said in ((ESCAPE, 'confirm false'), (ENTER, 'confirm true')):
        tap('#confirm')
        need(until(lambda: on.dialog(app), 8), 'it asks')
        time.sleep(0.5)
        png('confirm')
        key(how)
        need(until(lambda: told() == said, 5), told())
    tap('#prompt')
    need(until(lambda: on.dialog(app), 8), 'it asks')
    time.sleep(0.5)
    write('Alex')
    png('prompt')
    key(ENTER)
    need(until(lambda: told() == 'prompt Alex', 5), told())
    tap('#prompt')
    need(until(lambda: on.dialog(app), 8), 'it asks')
    time.sleep(0.5)
    key(ESCAPE)
    need(until(lambda: told() == 'prompt null', 5), told())


@step('choose a file')
def _():
    tap('#pick')
    time.sleep(2)
    png('choose-a-file')
    on.choose(out / 'note.txt')
    need(until(lambda: told('#picked') == 'note.txt', 8), told('#picked'))


@step('drop files')
def _():
    with on.drop_from(app, out / 'note.txt', out / 'second.txt') as at:
        drag(at, here(app, '#drop'))
        need(until(lambda: told() == 'dropped note.txt, second.txt', 6), told())
    need(dashboard(), 'and the page stays')


@step('copy and paste')
def _():
    tap('#field')
    hit('all')
    hit('copy')
    need(until(lambda: clipboard() == 'some words', 3), clipboard())
    clipboard('pasted')
    hit('paste')
    need(until(lambda: page('app', '$("#field").value') == 'pasted', 3), page('app', '$("#field").value'))
    hit('undo')
    need(until(lambda: page('app', '$("#field").value') == 'some words', 3), page('app', '$("#field").value'))


@step('find')
def _():
    if SYSTEM == 'windows':  # the browser's own
        hit('find')
        time.sleep(1)
        write('last needle')
        time.sleep(1)
        key(ENTER)
        need(until(lambda: page('app', 'scrollY') > 100, 5), f'it shows it {page("app", "scrollY")}')
        png('find')
        key(ESCAPE)
        time.sleep(0.5)
        page('app', 'scrollTo(0, 0)')
        return
    tall = page('app', 'innerHeight')
    hit('find')
    need(until(lambda: page('app', 'innerHeight') < tall, 5), f'the bar takes its room {tall} {page("app", "innerHeight")}')
    write('last needle')
    time.sleep(1)
    png('find')
    need(until(lambda: page('app', 'scrollY') > 100, 5), f'it shows it {page("app", "scrollY")}')
    hit('all')
    write('needle')
    found = lambda: page('app', '(r => r.startContainer.parentNode.textContent.slice(0, 3) + r.startOffset)(getSelection().getRangeAt(0))')
    time.sleep(1)
    places = [found()]
    for n in range(3):
        key(ENTER)
        time.sleep(0.6)
        places.append(found())
    need(len(set(places[:3])) == 3 and places[3] == places[0], f'one after the other {places}')
    hit('find back')
    time.sleep(0.6)
    need(found() == places[2], f'and back {found()} {places}')
    png('found')
    write('zzz')
    time.sleep(1)
    png('not-found')
    key(ESCAPE)
    need(until(lambda: page('app', 'innerHeight') == tall, 5), 'Escape ends it')
    page('app', 'scrollTo(0, 0)')
    hit('copy')


@step('zoom')
def _():
    wide = page('app', 'innerWidth')
    hit('zoom in')
    hit('zoom in')
    need(until(lambda: abs(page('app', 'innerWidth') - wide / 1.25) < 4, 5), f'{wide} {page("app", "innerWidth")}')
    png('zoomed')
    need(saved()['zoom'] == 1.25, saved())
    hit('reload')
    time.sleep(2)
    need(dashboard() and abs(page('app', 'innerWidth') - wide / 1.25) < 4, 'also after Reload')
    hit('zoom none')
    need(until(lambda: page('app', 'innerWidth') == wide, 5), 'and back')
    hit('zoom out')
    need(until(lambda: page('app', 'innerWidth') > wide, 5), 'and smaller')
    hit('zoom none')


@step('close and open again')
def _():
    me, at = page('app', 'me'), repr(app.window())
    hit('close')
    need(until(lambda: not app.window(), 5), 'closed')
    need(app.pids(), 'it keeps running')
    need(until(app.robot, 8), 'the robot is there')
    on.reopen(app)
    need(until(app.window, 8), 'opened again')
    need(page('app', 'me') == me and repr(app.window()) == at, 'where it was')
    need(len(app.pids()) == 1, app.pids())
    if SYSTEM == 'mac':
        on.menu('The Machine', 'Hide The Machine')
        need(until(lambda: not app.window(), 8), 'hidden')
        on.reopen(app)
        need(until(app.window, 8), 'and back')
    back_to_it()
    on.minimize(app)
    need(until(lambda: not app.window(), 8), 'minimized')
    on.reopen(app)
    need(until(app.window, 8), 'and back')


@step('full screen')
def _():
    was = app.window()
    hit('full')
    whole = on.whole()
    need(until(lambda: app.window() and app.window().width == whole[2] - whole[0] and app.window().height >= whole[3] - whole[1] - 60, 10), f'{app.window()} on {whole}')
    time.sleep(2)
    png('full-screen')
    need(not app.robot(), 'no robot over it')
    hit('close')
    need(until(lambda: not app.window(), 10), 'closed')
    time.sleep(2)
    png('closed-from-full-screen')
    on.reopen(app)
    need(until(app.window, 8), 'and back')
    need(until(lambda: repr(app.window()) == repr(was), 5), f'as it was: {app.window()}, {was}')


@step('its place is kept')
def _():
    on.place(app, 60, 70, 700, 560)
    time.sleep(1)
    at = repr(app.window())
    need('700x560' in at, at)
    png('small')
    stop(lambda: on.quit_it(app))
    start(account=elsewhere.at)
    need(until(app.window, 30), 'it opens')
    need(dashboard(), 'the dashboard, still signed in')
    need(repr(app.window()) == at, f'{app.window()}, {at}')
    return at


@step('settings')
def _():
    hit('settings')
    need(until(app.settings, 8), 'its key')
    time.sleep(1)
    png('settings-light')
    dark(True)
    time.sleep(2)
    png('settings-dark')
    dark(False)
    s = {x: page('settings', f'document.querySelector("#{x}").checked') for x in ('robot', 'login')}
    need(s == {'robot': True, 'login': False}, s)
    hit('close')
    need(until(lambda: not app.settings(), 5) and app.window(), 'only that closes')
    return f'{s}'


@step('without the robot')
def _():
    settings()
    need(switch('robot') is False, 'off')
    time.sleep(1)
    png('settings-without-robot')
    hit('close')
    hit('close')
    need(until(lambda: not app.window(), 5), 'the window closed')
    other()
    time.sleep(3)
    need(not app.robot() and not app.box(), f'no robot {app.raw()}')
    need(on.icon_there() == (SYSTEM == 'windows'), 'its icon')
    on.reopen(app)
    need(until(app.window, 8), 'it opens')
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
    need(until(lambda: page('settings', 'document.querySelector("#notify-row").hidden') is False, 5), 'offered without the robot')
    need(saved()['notify'] is True, f'on with the robot off {saved()["notify"]}')
    hint = told('#notify-hint', 'settings')
    png('notifications')
    if 'Not allowed' in hint:
        need(page('settings', 'document.querySelector("#notify").checked') is False, 'off while macOS refuses them')
    else:
        need(switch('notify') is False and saved()['notify'] is False, 'off')
        need(switch('robot') is True and switch('robot') is False and saved()['notify'] is False, 'and the robot leaves that so')
        need(switch('notify') is True, 'and on')
    if SYSTEM == 'mac':
        return f'{hint}; the banner itself is NOT TESTED'
    need('Not allowed' not in hint, hint)


@step('a notification')
def _():
    """The system shows it, and its click opens the to-do."""
    if SYSTEM == 'mac':
        return 'NOT TESTED: macOS asks the person first'
    hit('close') if app.settings() else None
    key_, todo = f'{time.time_ns():x}', 'aa02'
    machine.notices = [{'key': key_, 'id': todo, 'kind': 'todo', 'snooze': [['2h', '2 hours']]}]
    time.sleep(6)
    need(machine.notices and not on.kept(), f'not with the dashboard in front {on.kept()}')
    other()
    need(until(on.kept, 45), f'the system has it {machine.desks[-2:]}')
    need(until(lambda: not machine.notices, 5), 'and it is got')
    need(on.known_there() == 'The Machine', f'by its name: {on.known_there()}')
    at = until(lambda: on.on_screen('Send Ravi the floor plan'), 8)
    png('notification')
    need(at, f'on the screen; {on.kept()}')
    click(*at)
    need(until(ours, 8), f'it comes to the front: {on.in_front()}')
    need(until(lambda: todo in (page('app', 'location.hash') or ''), 8), page('app', 'location.hash'))
    need(until(lambda: not on.kept(), 8), f'and it is gone: {on.kept()}')
    page('app', 'location.hash = ""')
    return on.in_front()


@step('several notifications')
def _():
    if SYSTEM == 'mac':
        return 'NOT TESTED: macOS asks the person first'
    other()
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': t, 'kind': 'todo', 'snooze': []} for t in ('aa01', 'aa03')]
    need(until(lambda: len(on.kept()) == 2, 60), f'each of them: {on.kept()}')
    png('notifications-kept')
    machine.todos = [x for x in machine.todos if x[0] != 'aa03']
    gone = until(lambda: len(on.kept()) == 1, 45)
    back_to_it()
    need(gone, f'a done one goes: {on.kept()}')  # the other: as the app quits, see the end


@step('a browser here may notify too')
def _():
    hit('close') if app.settings() else None
    settings()
    if page('settings', 'document.querySelector("#robot").checked') is False:
        need(switch('robot') is True, 'on')
    asks = lambda: page('settings', '!document.querySelector("#browser-row").hidden') is True
    need(not asks(), 'nothing is asked')
    machine.browser = 7
    other()  # nothing is said with the dashboard in front
    before = len(machine.desks)
    need(until(lambda: '1' in [d[1] for d in machine.desks[before:]], 45), str(machine.desks[-3:]))
    time.sleep(1)
    back_to_it()
    settings()
    need(until(asks, 45), 'it asks')
    png('browser-asked')
    tap('#browser-yes', 'settings')
    need(until(lambda: machine.paired == [saved()['desk']], 30), f'the browser opens it and says so {machine.paired}')
    no_browser()
    back_to_it()
    settings()
    tap('#browser-no', 'settings')
    need(until(lambda: not asks(), 5) and saved()['none'] == 7, f'answered {saved()["none"]}')
    other()
    need(until(lambda: machine.says[-1] == (SYSTEM, '7'), 45), str(machine.says[-3:]))
    back_to_it()
    settings()
    need(not asks(), 'not asked again')
    machine.browser = 0


@step('the robot again')
def _():
    hit('close') if app.settings() else None
    settings()
    if page('settings', 'document.querySelector("#robot").checked') is False:
        need(switch('robot') is True, 'on')
    hit('close')
    other()
    need(until(app.robot, 8), 'the robot is there')
    need(SYSTEM == 'linux' or on.icon_there(), 'and its icon')


@step('closing quits, when the person wants that')
def _():
    back_to_it()
    settings()
    page('settings', '(() => { const s = document.querySelector("#quits"); s.value = "1"; s.dispatchEvent(new Event("change")) })()')
    need(until(lambda: saved().get('quits'), 5), saved())
    hit('close')
    hit('close')
    need(app.ended(), 'the process is gone')
    start(account=elsewhere.at)
    need(until(app.window, 30) and dashboard(), 'the window')
    settings()
    page('settings', '(() => { const s = document.querySelector("#quits"); s.value = ""; s.dispatchEvent(new Event("change")) })()')
    need(until(lambda: not saved().get('quits'), 5), saved())
    hit('close')


@step('start at login')
def _():
    settings()
    works = switch('login')
    png('at-login')
    said = told('#error', 'settings')
    if works:
        need(switch('login') is False, 'and off again')
    hit('close') if app.settings() else None
    return f'{"works" if works else "NOT TESTED: macOS refuses it for this build"} {said}'


@step('from the robot')
def _():
    hit('close')
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
    need(until(lambda: ours(), 5), f'in front: {on.in_front()}')
    need(until(lambda: not app.box(), 5), 'the box closes')


@step('the box and the window together')
def _():
    r = app.window()
    on.place(app, r.left, r.top, 640, 560)
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
    return on.in_front()


@step('a page that ends')
def _():
    back_to_it()
    me = page('app', 'me')
    on.pages_killed()
    need(until(lambda: app.answers('app') and page('app', 'typeof me === "string" ? me : ""') not in ('', me), 20), 'a fresh page')
    need(dashboard(), 'the dashboard')


@step('signed out')
def _():
    machine.away = elsewhere.at + '/open?to=' + 'app'
    hit('reload')
    need(until(lambda: 'Signed out' in text(), 10), text())
    png('signed-out')
    del elsewhere.links[:]
    tap('#go')
    need(until(lambda: elsewhere.links, 40), 'the account opens in the browser')
    png('waiting-for-the-browser')
    machine.away = None
    on.link(app, elsewhere.links[-1])
    time.sleep(2)
    no_browser()
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
    area = on.area()
    for name, w, h in (('1024', 1024, 640), ('large', area[2] - area[0], area[3] - area[1])):
        on.place(app, area[0], area[1], w, h)
        for night in (False, True):
            dark(night)
            time.sleep(2)
            png(f'{name}-{"dark" if night else "light"}')
    dark(False)
    return app.window()


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
        area = on.area()
        for name, w, h in (('1024', 1024, 640), ('large', area[2] - area[0], area[3] - area[1])):
            on.place(app, area[0], area[1], w, h)
            for night in (False, True):
                dark(night)
                time.sleep(3)
                png(f'dashboard-{name}-{"dark" if night else "light"}')
        dark(False)
        settings()
        png('dashboard-settings')
        hit('close')
        hit('close')
        other()
        need(until(app.robot, 8), 'the robot')
        click(*app.center())
        need(until(app.box, 8), 'its box')
        time.sleep(4)
        png('dashboard-box')
        key(ESCAPE)
        back_to_it()
        on.second(app, lambda: png('dashboard-on-two-screens'))
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
        return 'it asks the person, which stays unanswered here'
    return found


@step('quit')
def _():
    stop() if app.pids() else None
    need(not app.pids(), 'no process')
    sent = {a for a, _, _ in machine.actions}
    need(not sent, f'nothing done by itself: {sent}')
    need(not on.crashes(), f'no crash reports: {on.crashes()}')
    on.nothing_left()


app.kill()
dark(False)
(out / 'second.txt').unlink()
on.finish()
