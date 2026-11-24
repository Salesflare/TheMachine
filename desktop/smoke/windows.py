"""Runs the app on a Windows desktop as a person would: real mouse and keys (SendInput), against a made-up Machine, with a
screenshot of each step. For CI's own throwaway computer (desktop.yml): it moves the mouse and changes the resolution.

  python smoke/windows.py <sandbox build> <build for people> <folder for the pictures> [<folder of certificate.sh>]

The last for the steps over https, where its root is trusted. The dashboard opens in its installed app or the browser here;
the app's own window is window.py's.
"""
import base64
import ctypes
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request
import uuid
import winreg
from ctypes import wintypes as w

from standin import LEAVES, SNOOZE, Machine, TODOS
from windows_tools import (
    BUBBLE, CERTIFICATE, DEBUG, ENTER, ESCAPE, MAIL, PORT, SM, SNIP, SOURCE, STATE, App, alt_f4, browsers_closed, click, drag, finish, fresh, in_corner,
    in_front, key, move, need, need_window, out, page, people, png, press, reasons, resolution, sandbox, saved, says, scale, scheme, step, to_front, tray,
    until, user, work_area, write)

fresh()
resolution(1920, 1080)
print('screen', SM(0), SM(1), 'of', SM(80), 'monitors', flush=True)


# WebView2's very first start on this computer takes more than the 5 s that count as a hang, whichever program starts it:
# once before anything is tried, and nothing of it is kept

at = time.time()
app = App(people, '--login', debug=False)
until(app.robot, 60)
print(f'the very first start: {time.time() - at:.1f} s', flush=True)
app.process.kill()
app.process.wait()
fresh()

# The build for people, as it first starts with Windows

app = App(people, '--login', debug=False)


@step('first start')
def _():
    need(until(app.robot, 60), 'the robot shows')
    time.sleep(3)
    ok, told = in_corner(app)
    need(ok, told)
    return told


@step('first start opens the sign-in')
def _():
    need(until(app.box, 10), 'the box opens by itself')


@step('click closes and opens')
def _():
    had = bool(app.box())
    for wanted in (not had, had, not had, True):
        if bool(app.box()) == wanted:
            continue
        click(*app.center())
        ok = until(lambda: bool(app.box()) == wanted, 8)
        need(app.answers(), 'its main thread answers')
        need(ok, f'the box is {"open" if wanted else "closed"}')


@step('quit from a second start')
def _():
    if not app.answers():
        print('(its main thread did not answer)')
    app.again('--quit')
    need(app.ended(), 'the process is gone')


if app.process.poll() is None:
    app.process.kill()
    app.process.wait()
fresh()


# The same with a made-up Machine

machine = Machine(PORT)
app = App(sandbox)


@step('sandbox first start')
def _():
    need(until(app.box, 30), 'the box opens by itself')
    need(until(lambda: says('#signin-go'), 10), 'it offers the sign-in')
    need(says('#state') == 'Not signed in', says('#state'))
    return says('#panel').replace('\n', ' | ')


@step('drag')
def _():
    a = app.center()
    b = (500, 300)
    drag(a, b)
    c = app.center()
    need(abs(c[0] - b[0]) < 6 and abs(c[1] - b[1]) < 6, f'from {a} to {b}, it is at {c}')
    need(app.answers(), 'its main thread answers')
    need(saved()['places'], 'its place is kept')
    return f'{a} to {c}'


@step('right click')
def _():
    click(*app.center(), right=True)
    need(until(app.box), 'the box opens')
    need(until(lambda: 'Quit' in says('#menu')), 'on its menu')
    told = says('#menu').replace('\n', ' | ')
    key(ESCAPE)
    need(until(lambda: not says('#menu')), 'Escape closes the menu')
    return told


@step('wrong address')
def _():
    press(app, '#signin-other')
    press(app, '#address')
    write('http://127.0.0.1:1')
    key(ENTER)
    need(until(lambda: says('#signin-error'), 25), 'it says why not')
    return says('#signin-error')


def listed():
    return page('box.html', '[...document.querySelectorAll("#todos li")].map(x => x.innerText)')


def greeted(name=', Sam'):
    part = lambda: 'morning' if 5 <= time.localtime().tm_hour < 12 else 'afternoon' if 12 <= time.localtime().tm_hour < 18 else 'evening'
    return says('#state') == f'Good {part()}{name}'


def one_line():
    return page('box.html', '(e => e.scrollWidth <= e.clientWidth && e.clientHeight < 20)(document.getElementById("state"))')


@step('sign in by address')
def _():
    press(app, '#address')
    key(0x11, False), key(0x41), key(0x11, True)
    write(f'http://127.0.0.1:{PORT}')
    key(ENTER)
    need(until(lambda: says('#compose')), 'signed in')
    need(until(greeted), says('#state'))
    need(until(lambda: len(listed()) == 4), 'three to-dos and more')
    need(listed() == [title for _, title in TODOS[:3]] + ['1 more'] and says('#ready-name') == 'For you 4', f"{says('#ready-name')}: {listed()}")
    return says('#panel').replace('\n', ' | ')


@step('the menu says where')
def _():
    press(app, '#more')
    need(until(lambda: f'Signed in to 127.0.0.1:{PORT}' in says('#menu')), says('#menu'))
    png('menu')
    key(ESCAPE)
    need(until(lambda: not says('#menu')), 'it closes')


@step('nothing for them')
def _():
    machine.todos = []
    reopen = lambda: (click(*app.center()), click(*app.center()))
    reopen()
    need(until(lambda: says('#state') == 'Nothing needs you right now, Sam.', 12), says('#state'))
    need(not says('#ready') and one_line(), 'one line, and no list')
    png('nothing-for-them')
    machine.name = ''
    reopen()
    need(until(lambda: says('#state') == 'Nothing needs you right now.', 12), says('#state'))
    machine.name, machine.todos = '<b>Sam</b> & ' + 'x' * 50, list(TODOS)
    reopen()
    need(until(lambda: greeted(''), 12) and one_line(), 'a name too long is left out')
    machine.name = '<i>S</i>'
    reopen()
    need(until(lambda: greeted(', <i>S</i>'), 12), f"only text: {says('#state')}")
    machine.name = 'Sam'
    reopen()
    need(until(greeted, 12), says('#state'))


@step('add a to-do')
def _():
    press(app, '#text')
    write('Call the printer about the flyers')
    key(ENTER)
    need(until(lambda: len(listed()) == 4 and listed()[0] == 'Call the printer about the flyers\nJust added · Needs you'), str(listed()))
    need(not page('box.html', 'document.getElementById("text").value') and not says('#said'), 'ready for the next one')
    need(machine.actions[-1][:2] == ('card_new', {'text': 'Call the printer about the flyers'}), str(machine.actions))
    png('just-added')
    need(until(lambda: says('#ready-name') == 'For you 5' and listed()[-1] == '2 more', 5), f"{says('#ready-name')}: {listed()}")
    first = listed()[0]
    machine.status[machine.todos[-1][0]] = {'status': 'accepted', 'preparation_status': 'working'}
    need(until(lambda: 'Working…' in says('#panel'), 12), says('#panel'))
    machine.status[machine.todos[-1][0]] = {'status': 'completed'}
    need(until(lambda: says('#added').endswith('Done'), 12), says('#added') + str(listed()))
    need(says('#ready-name') == 'For you 4', says('#ready-name'))
    png('just-added-but-not-for-you')
    machine.no = 'That to-do is too long.'
    write('Something else')
    key(ENTER)
    need(until(lambda: says('#said') == machine.no), says('#said'))
    need(page('box.html', 'document.getElementById("text").value') == 'Something else', 'the text is back')
    need(not any('Something' in x for x in listed()), str(listed()))
    machine.no = None
    key(0x11, False), key(0x41), key(0x11, True), key(8)
    machine.todos = list(TODOS)
    press(app, '#close')
    need(until(lambda: not app.box()), 'the box closes')
    click(*app.center())
    need(until(lambda: len(listed()) == 4 and not says('#added')), 'the next time it is a row like any other')
    return first.replace('\n', ' | ')


@step('ask')
def _():
    press(app, '#kind-ask')
    write('When is lunch with Nora?')
    key(ENTER)
    need(until(lambda: '12:30' in says('#answer')), says('#answer'))
    need(machine.actions[-1][0] == 'search_ask', str(machine.actions))
    need(says('#answer-to') == 'When is lunch with Nora?' and not page('box.html', 'document.getElementById("text").value'), says('#answer'))


def dot():
    return page('robot.html', '!document.getElementById("dot").hidden')


def label():
    return page('robot.html', 'document.getElementById("robot").getAttribute("aria-label")')


@step('close and the dot')
def _():
    press(app, '#close')
    need(until(lambda: not app.box()), 'the box closes')
    need(not dot(), 'nothing is new since the box was open')
    return label()


@step('the dot is what is new')
def _():
    since = time.time()
    machine.todos = list(TODOS) + [('aa05', 'Answer the caterer')]
    need(until(dot, 40), 'something new: the dot, with the box closed')
    took = time.time() - since
    png('the-dot')
    told = label()
    machine.todos = list(TODOS)[1:]
    need(until(lambda: not dot(), 40), 'it was handled elsewhere: no dot')
    machine.todos = list(TODOS)  # back again, so it is new
    need(until(dot, 40), 'one came back: the dot')
    click(*app.center())
    need(until(lambda: len(listed()) == 4, 5), 'opening the box asks at once')
    need(until(lambda: not dot()), 'and it is seen')
    press(app, '#close')
    need(until(lambda: not app.box()) and not dot(), 'it stays seen')
    print(told)
    return f'{took:.0f} s'


def hide():
    click(*app.center(), right=True)
    need(until(lambda: 'Hide' in says('#menu')), 'the menu opens')
    press(app, '#menu-hide')
    need(until(hidden), 'it only looks over the bottom edge')


def hidden():
    r = app.robot()
    return r and r[1].bottom - r[1].top == 40 and r[1].bottom == work_area().bottom


def back():
    r = app.robot()
    return r and (r[1].left, r[1].top, r[1].bottom - r[1].top) == stood


stood = None


@step('hide says where it is')
def _():
    global stood
    r = app.robot()[1]
    stood = r.left, r.top, r.bottom - r.top
    hide()
    need(until(lambda: 'bring it back' in says('#notice')), 'the box says how to bring it back')
    png('hidden-with-the-line')
    told = says('#notice').replace('\n', ' | ')
    press(app, '#notice-ok')
    need(until(lambda: not app.box()), 'the box closes')
    need(hidden(), 'it is still there')
    return told


@step('a click brings it back')
def _():
    click(*app.center())
    need(until(back), 'it is where it stood')
    need(not app.box(), 'and no box opens')


@step('hide, icon by the clock')
def _():
    hide()
    time.sleep(1)
    need(not app.box(), 'the line shows once')
    at = tray(app)
    png('hidden-icon-by-the-clock')
    click(*at)
    need(until(back), 'it is where it stood')
    need(not app.box(), 'and no box opens')


@step('hide and show in the icon menu')
def _():
    click(*tray(app), right=True)
    png('tray-menu-hide')
    key(0x28), key(ENTER)
    need(until(hidden), 'Hide')
    click(*tray(app), right=True)
    png('tray-menu-show')
    key(0x28), key(ENTER)
    need(until(back), 'Show robot')


@step('right click while hidden')
def _():
    hide()
    click(*app.center(), right=True)
    need(until(lambda: 'Show robot' in says('#menu')), 'the menu has Show robot')
    png('hidden-menu')
    press(app, '#menu-show')
    need(until(back), 'it is where it stood')


@step('hide and start again')
def _():
    hide()
    app.again()
    need(until(back), 'it is back')


def open_it():
    if not app.box():
        click(*app.center())
    need(until(app.box), 'the box opens')
    need(until(lambda: len(listed()) == 4), str(listed()))


def over(n, seconds=1.2):
    """The mouse over the nth row, with its tooltip."""
    at = page('box.html', f'(() => {{ const e = document.querySelectorAll("#todos li")[{n}].getBoundingClientRect(); return [e.x + 60, e.y + e.height / 2].map(v => v * devicePixelRatio) }})()')
    point = w.POINT(0, 0)
    user.ClientToScreen(need_window(app.box())[0], ctypes.byref(point))
    move(round(point.x + at[0]) - 4, round(point.y + at[1]))
    move(round(point.x + at[0]), round(point.y + at[1]))
    time.sleep(seconds)


def row(n):
    return page('box.html', f'(r => ({{names: [...r.querySelectorAll(".quick button")].map(b => b.title), shown: r.querySelector(".quick") ? getComputedStyle(r.querySelector(".quick")).opacity : "",'
                f' tip: r.querySelector(".name")?.title ?? null, text: r.innerText, labels: [...r.querySelectorAll(".quick button")].map(b => b.ariaLabel) }}))(document.querySelectorAll("#todos li")[{n}])')


def quick(n, act):
    over(n, 0.3)
    press(app, f'#todos li:nth-child({n + 1}) [data-act={act}]')


@step('quick buttons')
def _():
    open_it()
    need(until(lambda: row(0)['names'] == ['Do it', 'Snooze', 'Mark done']), str(row(0)))
    need(row(1)['names'] == ['Snooze', 'Mark done'] and row(0)['shown'] == '0', str(row(1)))
    over(0)
    r = row(0)
    need(r['shown'] == '1' and r['tip'] == '' and r['labels'][0] == 'Do it: ' + TODOS[0][1], str(r))
    png('quick-buttons')
    machine.todos = [('aa01', 'Reply to the caterer about the menu, the tables and who brings what'), *TODOS[1:]]
    press(app, '#close')
    open_it()
    need(until(lambda: 'caterer' in row(0)['text']), str(listed()))
    over(0)
    need(row(0)['tip'].startswith('Reply to the caterer'), str(row(0)))
    png('a-cut-off-title')
    machine.todos = list(TODOS)
    press(app, '#close')
    return r['labels']


def decided():
    return [a[1] for a in machine.actions if a[0] == 'decide'][-1]


def picks():
    return page('box.html', '[...document.querySelectorAll(".choices button")].map(b => b.innerText)')


@step('snooze and undo')
def _():
    open_it()
    need(until(lambda: row(0)['names']), 'its buttons')
    quick(0, 'snooze2h')
    choices = [text for _, text in SNOOZE] + ['Choose date']
    need(until(lambda: picks() == choices), str(picks()))
    focused = lambda: page('box.html', 'document.activeElement.innerText || document.activeElement.ariaLabel')
    need(until(lambda: focused() == '2 hours'), focused())
    png('snooze-choices')
    key(ESCAPE)
    need(until(lambda: not picks()) and app.box(), 'Escape closes the choices only')
    need(focused() == 'Snooze: ' + TODOS[0][1], focused())
    quick(0, 'snooze2h')
    need(until(picks), 'they open again')
    key(0x28)
    key(0x28)
    need(until(lambda: focused() == choices[2]), focused())
    key(ENTER)
    need(until(lambda: row(0)['text'].startswith('Snoozed it · ')), str(listed()))
    png('snoozed')
    told, d = row(0)['text'], decided()
    need(d['choice'] == 'snooze' and d['snooze_option'] == '3d' and d['decision_id'].startswith('notify-'), str(d))
    day = time.strftime('%A', time.localtime(time.time() + 3 * 86400))
    need(day in told, told)
    need(until(lambda: says('#ready-name') == 'For you 3'), says('#ready-name'))
    press(app, '#todos li:first-child .link')
    need(until(lambda: listed()[0] == TODOS[0][1]), str(listed()))
    d = decided()
    need(d['choice'] == 'accept' and not d['decision_id'].startswith('notify-'), str(d))
    return told


@step('it says how Do it goes')
def _():
    need(until(lambda: row(0)['names'][:1] == ['Do it']), str(row(0)))
    before = len(machine.actions)
    quick(0, 'prepare')
    need(until(lambda: row(0)['text'] == TODOS[0][1] + '\nPreparing…'), row(0)['text'])
    need(until(lambda: row(0)['names'] == ['Preparing…', 'Snooze', 'Mark done']), str(row(0)))
    for _ in range(3):
        press(app, '#todos li:first-child [data-act=prepare]')  # off: a press more does nothing
    need(app.box() and row(0)['text'].endswith('\nPreparing…') and not says('#said'), str(row(0)))
    png('being-prepared')
    need([a[1]['choice'] for a in machine.actions[before:] if a[0] == 'decide'] == ['accept'], str(machine.actions[before:]))
    for status, word in (({'preparation_status': 'working'}, 'Working…'), ({'preparation_status': 'blocked'}, 'Stuck'), ({'status': 'prepared', 'preparation_status': 'done'}, 'Prepared')):
        machine.status['aa01'] = {'status': 'accepted', **status}
        need(until(lambda: row(0)['text'].endswith('\n' + word), 40), f"{word}: {row(0)['text']}")
    need(until(lambda: row(0)['names'] == ['Snooze', 'Mark done']), str(row(0)))
    png('prepared')
    press(app, '#close')
    machine.status['aa01'] = {'status': 'accepted', 'preparation_status': 'working'}  # started on another device
    open_it()
    need(until(lambda: row(0)['text'].endswith('\nWorking…') and row(0)['names'][:1] == ['Working…']), str(row(0)))
    machine.status.clear()
    need(until(lambda: row(0)['text'].endswith('Needs you') and row(0)['names'][:1] == ['Do it'], 12), str(row(0)))
    press(app, '#close')


@step('mark done and it goes')
def _():
    open_it()
    need(until(lambda: row(1)['names']), 'its buttons')
    quick(1, 'done')
    need(until(lambda: row(1)['text'].startswith('Marked it done')), str(listed()))
    need(decided()['choice'] == 'complete', str(decided()))
    need(until(lambda: listed() == [TODOS[0][1], TODOS[2][1], TODOS[3][1]], 25), str(listed()))
    machine.todos = list(TODOS)


def again():
    global machine
    was, machine = machine, Machine(PORT)
    machine.cookies = was.cookies


@step('a decision that is refused')
def _():
    press(app, '#close')
    open_it()
    machine.no = 'Open the to-do to do this.'
    need(until(lambda: row(0)['names'][:1] == ['Do it']), 'its buttons')
    quick(0, 'prepare')
    need(until(lambda: says('#said') == machine.no), says('#said'))
    need(listed()[0] == TODOS[0][1], 'the row is back')
    png('refused')
    machine.no = None
    machine.stop()
    quick(0, 'prepare')
    need(until(lambda: 'reach' in says('#state'), 40), says('#state'))
    time.sleep(2)
    need(says('#panel').count('reach') == 1, 'once: ' + says('#panel'))
    png('cannot-reach')
    again()
    press(app, '#close')


CARD = 'compact=1'


def carded(todo):
    need(until(app.card, 20), f'the to-do shows {says("#panel")}')
    need(until(lambda: says('h1', CARD) == 'To-do ' + todo), says('h1', CARD))
    (_, b), (_, c) = app.box(), app.card()
    need(b.left < c.left < c.right < b.right and b.top < c.top < c.bottom < b.bottom, 'within the box')


def small(h=400):
    b = need_window(app.box())[1]
    return b.bottom - b.top < h


@step('a to-do in the box')
def _():
    open_it()
    machine.compact = True
    since = time.time()
    press(app, '#todos li:nth-child(2) .name')
    carded('aa02')
    took = time.time() - since
    need(says('#ipc', CARD) == 'refused', 'nothing of the app for it: ' + says('#ipc', CARD))
    r = app.box()[1]
    need(r.top >= 0 and small(), 'a short one: the box is not tall for it')
    png('a-to-do-in-the-box')
    short = r.bottom - r.top
    press(app, '#long', CARD)
    need(until(lambda: not small(short + 60)), 'a longer one: the box grows with it')
    r = app.box()[1]
    need(r.top >= 0, 'within the screen')
    grown = r.bottom - r.top
    press(app, '#long', CARD)
    time.sleep(1.5)
    r = app.box()[1]
    need(r.bottom - r.top == grown, 'and stays so')
    press(app, '#more', CARD)
    need(until(lambda: says('dialog', CARD)), 'a dialog of its own')
    key(ESCAPE)
    need(until(lambda: not says('dialog', CARD)) and app.card(), 'Escape closes that')
    time.sleep(1)
    need(app.card(), 'only that')
    press(app, 'a[href="/elsewhere"]', CARD)
    time.sleep(1)
    need(says('h1', CARD) == 'To-do aa02', 'it stays on its page')
    b = app.box()[1]
    click((b.left + b.right) // 2, b.top + 30)
    time.sleep(0.5)
    need(app.card(), 'above the box, also after a click on that')
    press(app, 'h1', CARD)
    key(ESCAPE)
    need(until(lambda: not app.card() and app.box() and small()), 'Escape: back to the list')
    need(until(lambda: len(listed()) == 4), str(listed()))
    return f'{took:.1f} s'


@step('the next one, done there')
def _():
    since = time.time()
    press(app, '#todos li:nth-child(1) .name')
    carded('aa01')
    took = time.time() - since
    press(app, '#done', CARD)
    time.sleep(3)
    need(app.card(), 'it stays a moment, for its Undo')
    need(until(lambda: not app.card(), 12), 'back by itself')
    press(app, '#close')
    return f'{took:.1f} s'


@step('a date, and close')
def _():
    open_it()
    quick(0, 'snooze2h')
    need(until(picks), 'its choices')
    press(app, '.choices [data-until=date]')
    carded('aa01')
    press(app, '#card-close')
    need(until(lambda: not app.wide()), 'both go')
    need(not any(CARD in p['url'] for p in json.load(urllib.request.urlopen(f'http://127.0.0.1:{DEBUG}/json', timeout=5))), 'its page goes')
    open_it()
    need(not app.card() and small(), 'the next time it is the list')
    press(app, '#close')
    machine.compact = False


@step('what leaves a to-do')
def _():
    machine.compact = True
    wrong = []
    for selector, kind, at in LEAVES:
        if not app.card():
            open_it()
            press(app, '#todos li:nth-child(3) .name')
            carded('aa03')
            need(until(lambda: says('#leave', CARD)), 'its links')
            time.sleep(1)
        del machine.left[:], machine.seen[:]
        MAIL.unlink(missing_ok=True)
        press(app, selector, CARD)
        if kind == 'nowhere':
            time.sleep(4)
            went = True
        else:
            went = until(lambda: {'browser': lambda: machine.left, 'mail': MAIL.exists, 'dashboard': lambda: any(s.get('at') == at for s in machine.seen)}[kind](), 40)
        time.sleep(1)
        found = machine.left + [s.get('at') for s in machine.seen] + ([MAIL.read_text()] if MAIL.exists() else [])
        stays = bool(app.card()) and says('h1', CARD) == 'To-do aa03'
        if not went or stays != (kind != 'dashboard') or (found != ([at] if at else []) and kind != 'dashboard'):
            wrong.append(f'{selector}: {found}, {"stays" if stays else "goes"}')
            png('left-' + selector[1:])
        if kind == 'dashboard':
            browsers_closed()
    if app.card():
        press(app, '#card-close')
        need(until(lambda: not app.wide()), 'both go')
    machine.compact = False
    browsers_closed()
    need(not wrong, str(wrong))
    return f'{len(LEAVES)} kinds'


def plus():
    if page('box.html', 'document.querySelector("#plus").hidden'):  # it was asking
        press(app, '#kind-todo')
    until(lambda: not page('box.html', 'document.querySelector("#plus").hidden'))
    press(app, '#plus')


def shot():
    plus()
    need(until(lambda: says('#add-shot')), 'the menu')
    press(app, '#add-shot')
    need(until(lambda: not app.windows(), 8), 'the robot and its box are away')


@step('a screenshot')
def _():
    open_it()
    SNIP.write_text('@powershell -sta -noprofile -command "Add-Type -A System.Windows.Forms,System.Drawing; Start-Sleep 1; $b = New-Object Drawing.Bitmap 320,200; '
                    '$g = [Drawing.Graphics]::FromImage($b); $g.Clear([Drawing.Color]::Teal); [Windows.Forms.Clipboard]::SetImage($b)"')
    plus()
    need(until(lambda: 'Take a screenshot' in says('#adds')), says('#adds'))
    png('the-plus-menu')
    key(ESCAPE)
    need(until(lambda: not says('#adds')) and app.box(), 'Escape closes the menu only')
    shot()
    need(until(app.box, 30), 'the box is back')
    need(until(lambda: 'Screenshot.png' in says('#files')), says('#files') + ' | ' + says('#said'))
    size = page('box.html', '(i => [i.naturalWidth, i.naturalHeight])(document.querySelector("#files img"))')
    need(size == [320, 200], str(size))
    need(until(lambda: machine.actions[-1][0] == 'chat_upload'), str(machine.actions[-1][0]))
    need(base64.b64decode(machine.actions[-1][1]['data'])[:4] == b'\x89PNG', 'a PNG')
    need(user.CountClipboardFormats() == 0, 'nothing is left on the clipboard')
    png('a-screenshot')
    press(app, '#files button')
    need(until(lambda: machine.actions[-1][0] == 'chat_file_remove'), str(machine.actions[-1]))
    need(not says('#files'), 'it is gone')


@step('a screenshot that does not come')
def _():
    open_it()
    SNIP.write_text('@exit')
    shot()
    need(until(app.box, 30), 'the box is back')
    need(until(lambda: 'screenshot' in says('#said')), says('#said'))
    return says('#said')


@step('a screenshot with Windows own snip')
def _():
    SNIP.unlink(missing_ok=True)
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'ms-screenclip').Close()
    except FileNotFoundError:
        return 'NOT TESTED: this Windows has none'
    open_it()
    shot()
    time.sleep(4)
    png('windows-own-snip')
    drag((300, 300), (520, 420))
    if not until(app.box, 25) or not until(lambda: 'Screenshot' in says('#files'), 5):
        until(app.box, 180)
        return 'NOT TESTED: ' + says('#said')
    size = page('box.html', '(i => [i.naturalWidth, i.naturalHeight])(document.querySelector("#files img"))')
    png('from-windows-own-snip')
    press(app, '#files button')
    shot()
    time.sleep(4)
    key(ESCAPE)
    need(until(app.box, 20), 'Escape: the box is back')
    time.sleep(1)
    need(not says('#files') and not says('#said'), 'with nothing: ' + says('#said'))
    return f'{size}'


@step('toggle from a second start')
def _():
    if app.box():
        press(app, '#close')
        need(until(lambda: not app.box()), 'it was open')
    app.again('--toggle')
    need(until(app.box), 'the box opens')
    need(app.answers(), 'its main thread answers')
    app.again('--toggle')
    need(until(lambda: not app.box()), 'the box closes')


@step('not reachable')
def _():
    machine.stop()
    click(*app.center())
    need(until(app.box), 'the box opens')
    need(until(lambda: 'reach' in says('#state'), 25), says('#state'))
    return says('#state')


@step('reachable again')
def _():
    global machine
    machine = Machine(PORT)
    click(*app.center())
    click(*app.center())
    need(until(greeted, 25), says('#state'))


@step('signed out elsewhere')
def _():
    machine.refuse = True
    click(*app.center())
    click(*app.center())
    need(until(lambda: says('#signin') and says('#state'), 25), 'it offers the sign-in')
    told = says('#panel').replace('\n', ' | ')
    machine.refuse = False
    click(*app.center())
    click(*app.center())
    need(until(lambda: says('#compose'), 25), 'and is back')
    return told


@step('sign out')
def _():
    press(app, '#more')
    press(app, '#menu-signout')
    time.sleep(1)
    if not app.box():
        click(*app.center())
    need(until(lambda: says('#state') == 'Not signed in'), says('#state'))


@step('account sign-in')
def _():
    if says('#signin-other') != 'Self-hosted?':
        press(app, '#signin-other')
    press(app, '#signin-go')
    need(until(lambda: machine.links, 60), 'the browser opens the account')
    need(scheme(), 'its links are registered')
    png('account-in-the-browser')
    os.startfile(machine.links[-1])  # as the browser does: by the registered scheme
    need(until(lambda: says('#compose'), 25), 'signed in')
    need(not says('#answer') and not page('box.html', 'document.getElementById("text").value'), 'nothing from before')
    need(machine.cookies and saved()['cookie'] in machine.cookies, 'with its session')
    need(until(lambda: not scheme()), 'its links are taken back')
    subprocess.run(['taskkill', '/f', '/im', 'msedge.exe'], capture_output=True)
    return says('#state') + ' | ' + says('#said')


# What it opens on the dashboard: in the installed app, or else in the browser

OTHER = Machine(PORT + 1)  # another Machine, with an app of its own
HERE, THERE = f'http://127.0.0.1:{PORT}/', f'http://127.0.0.1:{PORT + 1}/'


def facts():
    """What the taskbar knows of the window in front: the id it is grouped by, how it is started again."""
    class Guid(ctypes.Structure):
        _fields_ = [('a', w.DWORD), ('b', w.WORD), ('c', w.WORD), ('d', ctypes.c_ubyte * 8)]

    class PropertyKey(ctypes.Structure):
        _fields_ = [('of', Guid), ('pid', w.DWORD)]
    guid = lambda text: Guid.from_buffer_copy(uuid.UUID(text).bytes_le)
    ctypes.windll.ole32.CoInitialize(None)
    store = ctypes.c_void_p()
    call = ctypes.windll.shell32.SHGetPropertyStoreForWindow
    call.argtypes = [w.HWND, ctypes.c_void_p, ctypes.c_void_p]
    if call(user.GetForegroundWindow(), ctypes.byref(guid('886d8eeb-8cf2-4446-8d02-cdba1dbdcf99')), ctypes.byref(store)):
        return in_front()
    table = ctypes.cast(ctypes.cast(store, ctypes.POINTER(ctypes.c_void_p))[0], ctypes.POINTER(ctypes.c_void_p))
    get = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(table[5])
    found = []
    for pid in (5, 2):
        value, text = ctypes.create_string_buffer(24), ctypes.c_wchar_p()
        get(store, ctypes.byref(PropertyKey(guid('9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3'), pid)), value)
        ctypes.windll.propsys.PropVariantToStringAlloc(value, ctypes.byref(text))
        found.append(text.value)
    return (*in_front(), *found)


def open_box():
    if not app.box():
        click(*app.center()) if app.robot() else app.again('--toggle')
    need(until(app.box), 'the box opens')


def changes(seconds):
    """How often the robot shows or goes meanwhile."""
    end, seen = time.time() + seconds, [bool(app.robot())]
    while time.time() < end:
        if bool(app.robot()) != seen[-1]:
            seen.append(not seen[-1])
        time.sleep(0.03)
    return len(seen) - 1


def opens(press_it, at, app_window, program=None):
    """Clicks something in the box; what the page that opened says."""
    open_box()
    need(until(lambda: says('#todos')), 'the box opens, with the to-dos')
    del machine.seen[:], OTHER.seen[:]
    since = time.time()
    press_it()
    seen = until(lambda: next((s for s in machine.seen if s.get('at', '') == at and bool(s.get('app')) == app_window), None), 40)
    took = time.time() - since
    need(seen, f'opened {machine.seen}, in front {in_front()}')
    need(all(bool(s.get('app')) == app_window for s in machine.seen), f'only there: {machine.seen}')
    need(not OTHER.seen, 'and not in the other one')
    need(until(lambda: not app.box()), 'the box closes')
    need(until(lambda: in_front()[1] == program if program else in_front()[1] in ('msedge.exe', 'chrome.exe'), 10), f'in front: {in_front()}')
    if app_window:
        need(until(lambda: not app.robot(), 5), f'the robot goes: {facts()}')
    else:
        need(app.robot(), 'the robot stays')
    return seen['me'], f'{took:.1f} s, in front: {in_front()}'


def todo(n):
    return lambda: press(app, f'#todos li:nth-child({n}) button')


def entries():
    """What Windows lists as installed by a browser."""
    found, top = [], r'Software\Microsoft\Windows\CurrentVersion\Uninstall'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, top) as k:
            for i in range(winreg.QueryInfoKey(k)[0]):
                try:
                    with winreg.OpenKey(k, winreg.EnumKey(k, i)) as one:
                        found.append(winreg.QueryValueEx(one, 'UninstallString')[0])
                except OSError:
                    pass
    except OSError:
        pass
    menu = pathlib.Path(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    return found + [str(x) for x in menu.rglob('*.lnk') if 'Machine' in x.name]


FORCED = {}


def data(browser):
    return str(out.resolve().parent / ('data-' + pathlib.Path(browser).stem))


def web_app(browser, what, address):
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Uninstall').Close()  # as any used Windows has
    before = entries()
    if not FORCED.get(browser):
        done = subprocess.run(['node', str(pathlib.Path(__file__).with_name('webapp.mjs')), browser, data(browser), what, address], capture_output=True, text=True, timeout=90)
        print(done.stdout, done.stderr, *entries(), sep='\n', flush=True)
        if entries() != before:
            need(done.returncode == 0, done.stdout)
            return done.stdout.strip()
    # The browser wrote nothing for it: as an administrator installs one for people
    FORCED[browser] = [*(a for a in FORCED.get(browser, []) if a != address), *([address] if what == 'install' else [])]
    with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Microsoft\Edge' if 'msedge' in browser else r'SOFTWARE\Policies\Google\Chrome') as k:
        winreg.SetValueEx(k, 'WebAppInstallForceList', 0, winreg.REG_SZ, json.dumps([{'url': a, 'default_launch_container': 'window'} for a in FORCED[browser]]))
    subprocess.Popen([browser, '--no-first-run', '--no-default-browser-check', 'about:blank'])
    changed = until(lambda: entries() != before, 45)
    time.sleep(4)
    browsers_closed()
    print('by policy', *entries(), sep='\n', flush=True)
    return 'by policy' if changed else None


def program(*parts):
    return next((str(p) for base in ('PROGRAMFILES', 'PROGRAMFILES(X86)') if (p := pathlib.Path(os.environ[base], *parts)).exists()), None)


@step('to-do without an app')
def _():
    told = opens(todo(1), '#card=aa01', False)[1]
    browsers_closed()
    return told


def with_app(name, exe):
    if not exe:
        return
    running, window, missing = pathlib.Path(exe).name.lower(), None, 'NOT TESTED: here this browser tells Windows nothing of an app it installs'

    @step(f'{name}, another Machine has an app')
    def _():
        nonlocal missing
        version = web_app(exe, 'install', THERE)
        if not version:
            return missing
        missing = ''
        told = opens(todo(1), '#card=aa01', False)[1]
        browsers_closed()
        return f'{version}: {told}'

    @step(f'{name}, to-do in the app')
    def _():
        nonlocal window
        if missing:
            return missing
        web_app(exe, 'install', HERE)
        window, told = opens(todo(2), '#card=aa02', True, running)
        return told

    @step(f'{name}, next to-do in the open app')
    def _():
        if missing:
            return missing
        me, told = opens(todo(1), '#card=aa01', True, running)
        need(me == window, 'the same window')
        return told

    @step(f'{name}, more and the dashboard in the open app')
    def _():
        if missing:
            return missing
        me, told = opens(lambda: press(app, '#todos .more'), '#card=aa01', True, running)
        need(me == window, 'the same window')
        return told

    @step(f'{name}, the robot and the app in front')
    def _():
        if missing:
            return missing
        its = user.GetForegroundWindow()
        told = facts()
        need(not app.robot(), f'the app is in front, so no robot: {told}')
        pad = subprocess.Popen(['notepad.exe'])
        try:
            other = until(lambda: user.FindWindowW('Notepad', None), 10)
            since = time.time()
            need(to_front(other), 'another window in front')
            need(until(app.robot, 5, 0.05), 'the robot is back')
            took = time.time() - since
            need(in_front()[1] == 'notepad.exe', f'and takes no focus: {in_front()}')
            # A click on the robot and its box, with the app behind them
            click(*app.center())
            need(until(app.box), 'the box opens')
            press(app, '#text')
            write('Half a to-do')
            need(changes(2) == 0, 'no flicker')
            # The app again: the box closes, what is written stays
            need(to_front(its), 'the app in front')
            need(until(lambda: not app.box() and not app.robot(), 5), 'the robot and its box go')
            app.again('--toggle')
            need(until(app.box), 'a key still opens the box')
            need(page('box.html', 'document.getElementById("text").value') == 'Half a to-do', 'with what was written')
            need(changes(2) == 0 and app.robot(), 'it stays while the box is open')
            app.again('--toggle')
            need(until(lambda: not app.box()), 'the box closes')
            # Minimized, back, full screen
            need(to_front(its) and until(lambda: not app.robot(), 5), 'no robot')
            user.ShowWindow(w.HWND(its), 6)
            need(until(app.robot, 5), 'minimized: the robot is back')
            need(to_front(its) and until(lambda: not app.robot(), 5), 'no robot')
            key(0x7A)
            time.sleep(4)
            need(not app.robot(), 'full screen: no robot')
            key(0x7A)
            time.sleep(1)
            # The person's own Hide stays
            need(to_front(other) and until(app.robot, 5), 'the robot is back')
            hide()
            need(to_front(its) and until(lambda: not app.robot(), 5), 'no robot')
            click(*tray(app), right=True)
            key(ESCAPE), key(ESCAPE)
            need(to_front(other) and until(hidden, 5), 'it still only looks over the edge')
            need(changes(1) == 0, 'no flicker')
            need(to_front(its) and until(lambda: not app.robot(), 5), 'no robot')
            user.PostMessageW(w.HWND(its), 0x10, 0, 0)
            need(until(app.robot, 8), 'closed: the robot is back')
            click(*app.center())
            need(until(back), 'it is where it stood')
        finally:
            subprocess.run(['taskkill', '/f', '/im', 'notepad.exe'], capture_output=True)
        return f'{took:.1f} s after another window came to the front; {told}'

    @step(f'{name}, its app is uninstalled')
    def _():
        if missing:
            return missing
        browsers_closed()
        web_app(exe, 'uninstall', HERE)
        told = opens(todo(3), '#card=aa03', False)[1]
        browsers_closed()
        web_app(exe, 'uninstall', THERE)
        return told


with_app('Chrome', program('Google', 'Chrome', 'Application', 'chrome.exe'))
with_app('Edge', program('Microsoft', 'Edge', 'Application', 'msedge.exe'))
browsers_closed()


@step('another resolution')
def _():
    drag(app.center(), (SM(0) - 100, SM(1) - 200))
    before = app.robot()[1]
    gap = work_area().right - before.right, work_area().bottom - before.bottom
    if not resolution(1280, 720):
        return 'not offered here'
    fits = lambda: (r := app.robot()[1]) and (work_area().right - r.right, work_area().bottom - r.bottom) == gap
    ok = until(fits, 12)
    r = app.robot()[1]
    need(ok, f'{gap} from the corner, now {work_area().right - r.right, work_area().bottom - r.bottom}')
    return f'stays {gap} from the corner'


resolution(1920, 1080)
time.sleep(4)


@step('scale 150%')
def _():
    r = app.robot()[1]
    corner = work_area().right - r.right, work_area().bottom - r.bottom
    if not scale(150):
        return 'not offered here'
    until(lambda: app.robot()[1].right - app.robot()[1].left == 132, 8)
    r = app.robot()[1]
    need(r.right - r.left == 132 and r.bottom - r.top == 132, f'{r.right - r.left}x{r.bottom - r.top}')
    gap = (work_area().right - r.right) / 1.5, (work_area().bottom - r.bottom) / 1.5
    need(all(abs(a - b) < 2 for a, b in zip(gap, corner)), f'{gap} from the corner, it was {corner}')
    click(*app.center())
    need(until(app.box), 'the box opens')
    png('scale-150-box')
    click(*app.center())
    b = (700, 400)
    drag(app.center(), b)
    c = app.center()
    need(abs(c[0] - b[0]) < 6 and abs(c[1] - b[1]) < 6, f'to {b}, it is at {c}')
    return f'132 pixels, dragged to {c}'


@step('scale back')
def _():
    if not scale(100):
        return 'not offered here'
    need(until(lambda: app.robot()[1].right - app.robot()[1].left == 88, 8), 'it is 88 pixels again')


@step('tray icon')
def _():
    if app.box():
        click(*app.center())
    click(*tray(app))
    need(until(app.box, 5), 'a click on it opens the box')


@step('Alt F4 closes the box')
def _():
    if not app.box():
        click(*app.center())
    press(app, '#panel h1')
    alt_f4()
    need(until(lambda: not app.box()), 'the box closes')
    need(app.process.poll() is None and app.robot(), 'the robot stays')


@step('Alt alone')
def _():
    click(*app.center())
    need(until(app.box), 'the box opens')
    press(app, '#text')
    write('Al')
    key(0x12)
    time.sleep(1)
    write('so')
    said = page('box.html', 'document.getElementById("text").value')
    need(said.endswith('Also'), f'it goes on: {said!r}')
    key(0x11, False), key(0x41), key(0x11, True), key(0x08)
    click(*app.center())


@step('Alt F4 quits from the robot')
def _():
    click(*app.center())
    click(*app.center())  # clicked last, so it has the keys
    need(until(lambda: not app.box()), 'the box is closed')
    alt_f4()
    need(app.ended(), 'the process is gone')


app = App(sandbox)


@step('next start')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(4)
    need(not app.box(), 'signed in: the box waits for a click')
    need(not dot(), 'what was seen before stays seen')
    machine.todos = [*TODOS, ('aa07', 'Answer the florist')]
    need(until(dot, 40), 'the dot shows')
    machine.todos = list(TODOS)


@step('started twice')
def _():
    need(app.again() == 0 and app.process.poll() is None, 'the second one ends')


def comes(todo, soon=False):
    """The Machine has something for it to say. Soon: asked as the box closes (what its rows show isn't said after it)."""
    if app.box():
        press(app, '#close')
    need(until(lambda: not app.wide(), 20), 'nothing is there')
    asked = len(machine.named)
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': todo, 'kind': 'todo', 'snooze': SNOOZE}]
    since = time.time()
    if soon:
        app.again('--toggle')
        need(until(app.box), 'the box opens')
        need(until(lambda: todo in machine.named[asked:]), 'it is asked')
        time.sleep(1)
        need(not app.bubble(), 'not while the box is open')
        need(machine.notices, 'and not taken: if the box stays open the browser gets it')
        app.again('--toggle')
    need(until(app.bubble, 45, 0.05), f'the bubble shows {machine.desks[-2:]}')
    need(until(lambda: not machine.notices, 5), 'and is got')
    need(until(lambda: says('#title', BUBBLE)), 'with its words')
    return time.time() - since


def away():
    click(work_area().left + 60, work_area().top + 400)


def goes(seconds=20):
    """Once somebody is there."""
    user.mouse_event(1, 1, 1, 0, 0)
    need(until(lambda: not app.bubble(), seconds, 0.05), 'it goes')


def said():
    return page(BUBBLE, '[...document.querySelectorAll("#buttons button")].filter(b => b.getClientRects().length).map(b => b.innerText)')


@step('it speaks up')
def _():
    machine.todos = list(TODOS)
    away()
    before = user.GetForegroundWindow()
    took = comes('aa02')
    came = time.time()
    png('it-speaks-up')
    need(user.GetForegroundWindow() == before, 'the keys stay where they were')
    need(says('#title', BUBBLE) == TODOS[1][1] and says('#line', BUBBLE) == 'Made up, for the stand-in.', says('#panel', BUBBLE))
    need(said() == ['See draft', 'Snooze', 'Mark done'], str(said()))  # never Send
    (_, b), (_, r), area = app.bubble(), app.robot(), work_area()
    need(area.left <= b.left and b.right <= area.right + 20 and area.top <= b.top and b.bottom <= r.top + 20, f'above the robot, on the screen: {b.left} {b.top} {b.right} {b.bottom}')
    time.sleep(18)
    need(app.bubble(), 'it stays: nobody touched the mouse or the keys')
    came = time.time()
    goes()
    stayed = time.time() - came
    need(10.5 < stayed < 15, f'about 12 s after that: {stayed:.1f}')
    need(len(saved()['desk']) == 32 and machine.desks[-1][0] == saved()['desk'], str(machine.desks[-1]))
    return f'{took:.0f} s after the Machine had it, for {stayed:.1f} s'


@step('a bubble stays under the pointer, and goes when it is done elsewhere')
def _():
    comes('aa03')
    (_, b) = app.bubble()
    user.SetCursorPos((b.left + b.right) // 2, (b.top + b.bottom) // 2)
    time.sleep(0.3)
    user.mouse_event(1, 1, 1, 0, 0)
    time.sleep(14)
    need(app.bubble(), 'it stays')
    machine.todos = [x for x in TODOS if x[0] != 'aa03']
    need(until(lambda: not app.bubble(), 40), 'it goes with it')
    machine.todos = list(TODOS)
    away()


@step('snooze and undo in a bubble')
def _():
    comes('aa04', soon=True)
    before = len(machine.actions)
    press(app, '#buttons [data-act^=snooze]', BUBBLE)
    shown = lambda: page(BUBBLE, '[...document.querySelectorAll("#choices button")].filter(b => b.getClientRects().length).map(b => b.innerText)')
    need(until(lambda: shown() == [text for _, text in SNOOZE] + ['Choose date']), str(shown()))
    time.sleep(0.5)
    png('it-speaks-up-snooze')
    press(app, '#choices [data-until="3d"]', BUBBLE)
    need(until(lambda: says('#said', BUBBLE).startswith('Snoozed it · ')), says('#panel', BUBBLE))
    png('it-speaks-up-snoozed')
    told = says('#said', BUBBLE).replace('\n', ' ')
    need(machine.actions[before][1]['snooze_option'] == '3d' and machine.actions[before][1]['decision_id'].startswith('notify-'), str(machine.actions[before:]))
    press(app, '#said .link', BUBBLE)
    need(until(lambda: any(x[0] == 'aa04' for x in machine.todos)), 'it is back')
    away()
    goes(15)
    return told


@step('Do it in a bubble')
def _():
    comes('aa01')
    before = len(machine.actions)
    need(said() == ['Open', 'Do it', 'Snooze', 'Mark done'], str(said()))
    press(app, '#buttons [data-act=prepare]', BUBBLE)
    need(until(lambda: says('#said', BUBBLE) == 'Preparing…'), says('#panel', BUBBLE))
    away()
    need(until(lambda: not app.bubble(), 10), 'it goes')
    need([a[1]['choice'] for a in machine.actions[before:]] == ['accept'], str(machine.actions[before:]))
    machine.status.clear()


@step('a bubble opens it in the box')
def _():
    machine.compact = True
    comes('aa04', soon=True)
    press(app, '#open', BUBBLE)
    need(until(app.box), 'the box opens')
    carded('aa04')
    need(not app.bubble(), 'the bubble goes')
    press(app, '#card-close')
    machine.compact = False


def windows_says(to='read'):
    """Windows' own word of notifications: its state, and its mode (Do Not Disturb)."""
    done = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(pathlib.Path(__file__).with_name('dnd.ps1')), to], capture_output=True, text=True, timeout=120)
    return (done.stdout.strip().splitlines() or [done.stderr.strip()[-300:]])[-1]


def look():
    """It asks now, as its box opens: not only in its half a minute. Somebody is there, too."""
    away()
    before = len(machine.desks)
    app.again('--toggle')
    need(until(lambda: len(machine.desks) > before), 'it asks')
    app.again('--toggle')
    need(until(lambda: not app.box()), 'the box goes')


@step('a meeting that starts soon')
def _():
    at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 600))
    meets = {'id': 'aa02', 'event': 7, 'at': at, 'who': 'Dana', 'others': 2, 'join': None}
    # a Machine that says no title yet, then one that does: with a guest, and without
    for join, line, more, name in (('https://zoom.us.example.com/j/1', 'Meeting', {}, 'Meeting with Dana and 2 others'),
                                   ('https://zoom.us/j/1', 'Call', {'title': 'Kickoff'}, 'Call with Dana and 2 others'),
                                   (None, 'Kickoff alone', {'who': '', 'others': 0, 'title': 'Kickoff'}, 'Kickoff')):
        machine.meeting = {**meets, 'event': len(line), 'join': join, **more}
        look()
        need(until(app.bubble, 45, 0.05), 'the bubble shows')
        need(until(lambda: says('#title', BUBBLE) in [f'{name} in {m} min' for m in (9, 10)]), says('#panel', BUBBLE))
        need(said() == ['Open brief', *(['Join'] if line == 'Call' else [])], str(said()))
        png(f'a-meeting-{line.split()[0].lower()}')
        goes()
    look()
    time.sleep(3)
    need(not app.bubble(), 'once each')
    machine.meeting = None


def speaks(yes):
    for _ in range(3):
        look()
        if machine.desks[-1][1] == '01'[yes]:
            return
    raise AssertionError(str(machine.desks[-1]))


def quiet(todo='aa03'):
    """What comes isn't said, and left to the browser."""
    speaks(False)
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': todo, 'kind': 'todo'}]
    look()
    time.sleep(3)
    need(not app.bubble() and machine.notices, 'it says nothing, and leaves it to the browser')
    machine.notices = []


def speak_up(when):
    if not app.box():
        open_it()
    press(app, '#more')
    need(until(lambda: says('#menu-speak')), 'the menu')
    press(app, f'#speak-{when}')
    chosen = 'document.querySelector("#menu-speak [aria-checked=true]").id'
    need(until(lambda: page('box.html', chosen) == f'speak-{when}'), 'it is the one')
    png(f'speak-up-{when}')
    press(app, '#close')
    need(until(lambda: saved()['speak'] == when), str(saved().get('speak')))


@step('what is not shown is not taken')
def _():
    away()
    asked = lambda n: until(lambda: len(machine.named) > n, 45)
    n, machine.odd = len(machine.named), 500
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': 'aa04', 'kind': 'todo'}]
    need(asked(n), 'it is asked')
    time.sleep(1)
    need(machine.notices and not app.bubble(), 'no answer: not taken')
    machine.odd = None
    need(until(app.bubble, 45, 0.05), 'asked again, and said')
    goes()
    app.again('--toggle')
    need(until(app.box), 'the box opens')
    n = len(machine.named)
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': 'aa04', 'kind': 'todo'}]
    need(asked(n), 'it is asked')
    time.sleep(1)
    need(machine.notices, 'the box is open: not taken')
    machine.notices = []  # 90 seconds later: the browser's
    time.sleep(1)
    app.again('--toggle')
    need(until(lambda: not app.box()), 'the box goes')
    need(not until(app.bubble, 6, 0.05), 'the browser had it: not said too')
    log = reasons()
    for reason in ('showed a bubble', "the Machine didn't say what one is", 'one waits: the box is open', 'no longer offers it here'):
        need(reason in log, f'{reason}: {log[-800:]}')
    need(not any(title in log for _, title in TODOS), 'no titles')
    return log.strip().splitlines()[-1]


@step('never while presenting, locked or on a doubled screen')
def _():
    away()
    for state in ('4', '1', '2 1', '3', '5 0 1'):
        STATE.write_text(state)
        speaks(False)
        STATE.write_text('5')
        speaks(True)
    STATE.write_text('4')
    quiet()
    STATE.write_text('5')
    speaks(True)
    need('may not speak: locked, presented, mirrored or idle' in reasons(), 'it says why')


@step('a bubble makes way for a presentation, and waits behind a lock')
def _():
    STATE.write_text('5')
    speaks(True)
    comes('aa03')
    STATE.write_text('4')
    need(until(lambda: not app.bubble(), 8), 'it makes way')
    need('a bubble went: something is full screen or presented' in reasons(), 'and says why')
    STATE.write_text('5')
    speaks(True)
    comes('aa03')
    STATE.write_text('1')
    time.sleep(2.5)
    for _ in range(3):  # the one who unlocks it hasn't seen it
        user.mouse_event(1, 1, 1, 0, 0)
        time.sleep(1)
    time.sleep(14)
    need(app.bubble(), 'it is there')
    STATE.write_text('5')
    time.sleep(16)
    need(app.bubble(), 'and still is when it is unlocked')
    goes()


@step('Do Not Disturb, by choice')
def _():
    need(saved().get('speak', 'always') == 'always', 'Always, to start with')
    STATE.write_text('5 1')
    comes('aa03')
    away()
    goes()
    speak_up('calm')
    quiet()
    STATE.write_text('5 0')
    speaks(True)
    STATE.write_text('6')
    speaks(False)
    STATE.write_text('5')
    speaks(True)
    speak_up('never')
    quiet('aa04')
    speak_up('always')
    speaks(True)


@step('what Windows itself says: notifications off, Do Not Disturb')
def _():
    path = r'Software\Microsoft\Windows\CurrentVersion\PushNotifications'
    told = [f'as it is {windows_says()}']
    plain = windows_says('off')  # a runner may start with it on
    told.append(f'Do Not Disturb off {plain}')
    if plain.split()[0].isdigit():
        on = windows_says('on')
        told.append(f'on {on}')
        need(on.split()[0] == plain.split()[0], f'in the mode and nowhere else: {told}')
        told.append('and it speaks' if on.split()[1] != plain.split()[1] else 'NOT TESTED with it on: the switch did not take')
        comes('aa02')
        png('always-in-do-not-disturb')
        away()
        goes()
        windows_says('off')
    plain = windows_says()
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, path) as key:
        winreg.SetValueEx(key, 'ToastEnabled', 0, winreg.REG_DWORD, 0)
    try:
        time.sleep(2)
        off = windows_says()
        told.append(f'notifications on {plain}, off {off}')
        need(off == plain, f'the same: {told}')
        comes('aa02')
        away()
        goes()
    finally:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, path) as key:
            winreg.SetValueEx(key, 'ToastEnabled', 0, winreg.REG_DWORD, 1)
    return ', '.join(told)


@step('drop anything on it')
def _():
    if app.box():
        press(app, '#close')
    need(until(lambda: not app.wide()), 'nothing is there')
    script, where, one, two = (out.resolve() / n for n in ('source.ps1', 'source.txt', 'notes.txt', 'plan & b.txt'))
    script.write_text(SOURCE, encoding='utf-8')
    for f in (one, two):
        f.write_text('made up')
    source = subprocess.Popen(['powershell', '-sta', '-noprofile', '-executionpolicy', 'bypass', '-file', str(script), f'{one}|{two}', str(where)])
    try:
        need(until(lambda: where.exists() and where.read_text().strip(), 30), 'a window to drag from')
        x, y = map(int, where.read_text().split())
        from_ = lambda n: (x + 130 * n + 60, y + 60)
        before = len(machine.actions)
        drag(from_(1), app.center())
        need(until(app.box), 'the box opens')
        value = lambda: page('box.html', 'document.getElementById("text").value')
        need(until(lambda: value() == 'Ask Dana <b>about</b> the pilot'), str(value()))
        need(page('box.html', 'document.activeElement.id') == 'text', 'ready to go on')
        png('dropped-text')
        drag(from_(2), app.center())
        need(until(lambda: 'https://example.com/pilot?x=1' in value().split('\n')), str(value()))
        need(len(machine.actions) == before, f'nothing is sent: {machine.actions[before:]}')
        drag(from_(0), app.center())
        need(until(lambda: 'notes.txt' in says('#files') and 'plan & b.txt' in says('#files')), says('#files'))
        need(until(lambda: len(machine.actions) == before + 2), str(machine.actions[before:]))
        need({n for n, *_ in machine.actions[before:]} == {'chat_upload'}, 'the files are attached, as with +')
        png('dropped-files')
        press(app, '#kind-ask')
        need(value().startswith('Ask Dana'), 'it can be asked too')
        press(app, '#kind-todo')
        for _ in range(2):
            press(app, '#files button')
        press(app, '#text')
        key(0x11, False), key(0x41), key(0x11, True), key(8)
        press(app, '#close')
        hide()
        drag(from_(1), app.center())
        need(until(app.box), 'a hidden one comes back with it')
        press(app, '#text')
        key(0x11, False), key(0x41), key(0x11, True), key(8)
        press(app, '#close')
    finally:
        source.kill()


@step('quit from the menu')
def _():
    click(*app.center(), right=True)
    need(until(lambda: 'Quit' in says('#menu')), 'the menu opens')
    press(app, '#menu-quit')
    need(app.ended(), 'the process is gone')


app = App(sandbox)


@step('quit from the tray')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(2)
    click(*tray(app), right=True)
    png('tray-menu')
    key(0x26)  # up, to the last one
    key(ENTER)
    need(app.ended(), 'the process is gone')


app = App(sandbox)


@step('quit from a second start while it is stuck')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(2)
    app.again('--hang')
    time.sleep(1)
    need(not app.answers(), 'its main thread is stuck')
    since = time.time()
    app.again('--quit')
    need(app.ended(), 'the process is gone')
    return f'gone after {time.time() - since:.1f} s'


if app.process.poll() is None:
    app.process.kill()
    app.process.wait()


# As a hosted Machine is: over https, with an account's session, which a browser sends only there

fresh()
hosted = Machine(PORT + 2, CERTIFICATE) if CERTIFICATE else None
app = App(sandbox, over=hosted) if hosted else app


@step('account sign-in over https')
def _():
    if not hosted:
        return 'NOT TESTED: no certificate'
    need(until(app.box, 30) and until(lambda: says('#signin-go')), 'it offers the sign-in')
    need(not says('#signin-error'), says('#panel'))
    press(app, '#signin-go')
    need(until(lambda: hosted.links, 60), 'the browser opens the account')
    os.startfile(hosted.links[-1])
    need(until(lambda: says('#compose'), 25), f'signed in {says("#panel")}')
    need(saved()['machine'] == hosted.at + '/' and saved()['cookie'] in hosted.cookies, 'with its session')
    browsers_closed()
    return hosted.at


@step('a to-do in the box, with an account')
def _():
    if not hosted:
        return 'NOT TESTED: a browser sends the session only to https, here it is http'
    hosted.compact = True
    open_it()
    press(app, '#todos li:nth-child(2) .name')
    carded('aa02')
    need(hosted.cards[-1] and all(hosted.cards), f'its page has the session {hosted.cards}')
    need(page(CARD, 'location.origin') == hosted.at and page(CARD, 'document.cookie') == '', 'which no script can read')
    png('signed-in-to-do')
    need(until(lambda: says('#done', CARD)), 'it is drawn')
    press(app, 'a[target]', CARD)
    need(until(lambda: any(s.get('at') == '#person=7' for s in hosted.seen), 40), f'the link opens {hosted.seen}')
    need(until(lambda: not app.wide()), 'the box goes')
    browsers_closed()
    return 'signed in'


@step('a to-do in the box, after the next start')
def _():
    global app
    if not hosted:
        return 'NOT TESTED: no certificate'
    app.again('--quit')
    need(app.ended(), 'the process is gone')
    app = App(sandbox, over=hosted)
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(4)
    del hosted.cards[:]
    open_it()
    press(app, '#todos li:nth-child(1) .name')
    carded('aa01')
    need(hosted.cards and all(hosted.cards), f'its page has the session {hosted.cards}')


@step('signed out over https')
def _():
    if not hosted:
        return 'NOT TESTED: no certificate'
    if app.card():
        key(ESCAPE)
        need(until(lambda: not app.card() and app.box() and small()), 'Escape: back to the list')
    need(until(app.box), 'the box is there')
    press(app, '#more')
    need(until(lambda: says('#menu-signout')), 'its menu opens')
    press(app, '#menu-signout')
    time.sleep(1)
    if not app.box():
        click(*app.center())
    need(until(lambda: says('#state') == 'Not signed in'), says('#state'))
    need(not saved()['cookie'], 'its session is gone')
    app.again('--quit')
    need(app.ended(), 'the process is gone')


if app.process.poll() is None:
    app.process.kill()


@step('nothing is left')
def _():
    name = os.path.basename(sandbox)
    need(until(lambda: name not in subprocess.run(['tasklist'], capture_output=True, text=True).stdout, 5), 'no process')
    need(not scheme(), 'no links')
    need(not hosted or not hosted.actions, 'nothing done there')
    sent = {a for a, _, _ in machine.actions}
    need(sent <= {'card_new', 'search_ask', 'decide', 'chat_upload', 'chat_file_remove'}, str(sent))
    need({a['choice'] for n, a, _ in machine.actions if n == 'decide'} <= {'accept', 'snooze', 'complete', 'undo'}, 'only what the buttons do')


finish()
