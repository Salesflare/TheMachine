"""The way back from the account's sign-in on Windows, next to what can be in its way: a second copy of the program, one that runs as
an administrator, a sign-in that is pressed again and again. For CI's own throwaway computer (desktop.yml), whose programs run
with an administrator's rights.

  python smoke/signin.py <sandbox build> - <folder for the pictures>
"""
import ctypes
import json
import os
import pathlib
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from ctypes import wintypes as w

import on_windows as on
from on_windows import ID, PORT, App, click, finish, fresh, here, need, page, png, saved, says, step, until
from standin import Machine
from windows_tools import scheme

program = str(pathlib.Path(on.sandbox).resolve())
copy = on.out / 'another folder' / os.path.basename(program)
copy.parent.mkdir(exist_ok=True)
shutil.copy(program, copy)
machine = Machine(PORT)
machine.window = machine.compact = True
account = Machine(PORT + 1)
account.machine = machine
machine.account = account.at
app = None
kernel, advapi = ctypes.WinDLL('kernel32', use_last_error=True), ctypes.WinDLL('advapi32', use_last_error=True)
kernel.OpenProcess.restype = kernel.GetCurrentProcess.restype = w.HANDLE


def start(signed_in=False, **kw):
    global app
    if app:
        app.kill()
        time.sleep(1)
    fresh()
    machine.window = True
    if signed_in:
        folder = pathlib.Path(os.environ['APPDATA'], ID)
        folder.mkdir(parents=True)
        (folder / 'app.json').write_text(json.dumps({'machine': machine.at + '/'}))
    app = App(program, account=account.at, **kw)
    need(until(lambda: app.answers('app'), 60), 'its page answers')
    need(until(app.window, 30), 'its window')
    time.sleep(1)


def tap(selector):
    click(*here(app, selector))


def text(selector='#panel'):
    return says(selector, 'app').replace('\n', ' | ')


def dashboard(seconds=20):
    return until(lambda: 'Stand-in dashboard' in says('h1', 'app'), seconds)


def sign_in(loopback):
    account.loopback = loopback
    del account.links[:], account.asked[:]
    if not on.ours():  # a browser of before may still come in front
        on.back_to_it(app)
    tap('#go')
    need(until(lambda: account.links, 60), 'the account opens in the browser')


def pids():
    lines = subprocess.run(['tasklist', '/fi', f'imagename eq {os.path.basename(program)}', '/fo', 'csv', '/nh'], capture_output=True, text=True).stdout.splitlines()
    return [int(line.split(',')[1].strip('"')) for line in lines if line.lower().startswith(f'"{os.path.basename(program).lower()}')]


def level(process):
    """8192 as the person, 12288 as an administrator."""
    token, size, told = w.HANDLE(), w.DWORD(), ctypes.create_string_buffer(64)
    advapi.OpenProcessToken(w.HANDLE(process), 8, ctypes.byref(token))
    advapi.GetTokenInformation(token, 25, told, 64, ctypes.byref(size))
    return int.from_bytes(told.raw[size.value - 4:size.value], 'little')


class Startup(ctypes.Structure):
    _fields_ = [('cb', w.DWORD), ('a', w.LPWSTR), ('desktop', w.LPWSTR), ('title', w.LPWSTR), *[(f'n{i}', w.DWORD) for i in range(8)], ('m', w.WORD), ('k', w.WORD), ('p', ctypes.c_void_p),
                *[(f'h{i}', w.HANDLE) for i in range(3)]]


class Process(ctypes.Structure):
    _fields_ = [('process', w.HANDLE), ('thread', w.HANDLE), ('pid', w.DWORD), ('tid', w.DWORD)]


class Label(ctypes.Structure):
    _fields_ = [('sid', ctypes.c_void_p), ('attributes', w.DWORD)]


def plainly(*command):
    """Started as Windows does it for the person, without an administrator's rights: how it ended, what it runs with."""
    safer, token, sid = w.HANDLE(), w.HANDLE(), ctypes.c_void_p()
    need(advapi.SaferCreateLevel(2, 0x20000, 1, ctypes.byref(safer), None), 'SaferCreateLevel')
    need(advapi.SaferComputeTokenFromLevel(safer, None, ctypes.byref(token), 0, None), 'SaferComputeTokenFromLevel')
    need(advapi.ConvertStringSidToSidW('S-1-16-8192', ctypes.byref(sid)), 'sid')
    label = Label(sid, 0x20)
    need(advapi.SetTokenInformation(token, 25, ctypes.byref(label), ctypes.sizeof(label)), 'its level')
    env = ctypes.create_unicode_buffer(''.join(f'{k}={v}\0' for k, v in sorted(app.env.items(), key=lambda x: x[0].upper()) if not k.startswith('=')) + '\0')
    startup, made = Startup(), Process()
    startup.cb = ctypes.sizeof(startup)
    line = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
    need(advapi.CreateProcessAsUserW(token, None, line, None, None, False, 0x400, env, None, ctypes.byref(startup), ctypes.byref(made)), f'CreateProcessAsUser {ctypes.get_last_error()}')
    at = level(made.process)
    need(at == 8192, f'it runs with {at}')
    kernel.WaitForSingleObject(w.HANDLE(made.process), 30_000)
    code = w.DWORD()
    kernel.GetExitCodeProcess(w.HANDLE(made.process), ctypes.byref(code))
    return code.value


def handler():
    import winreg
    try:
        return winreg.QueryValue(winreg.HKEY_CURRENT_USER, r'Software\Classes\computer.themachine.app\shell\open\command')
    except FileNotFoundError:
        return None


@step('the browser comes back to the app')
def _():
    start()
    rules = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all', 'verbose'], capture_output=True).stdout.lower()
    sign_in(True)
    need(dashboard(), text())
    png('back-in-the-app')
    need(machine.cookies and saved()['cookie'] in machine.cookies, 'with its session')
    need(until(lambda: not scheme(), 5), 'its links are taken back')
    q = account.asked[-1]
    need(q['on'] == 'desktop' and len(q['c']) == 43 and q['p'].isdigit(), q)
    on.browsers_closed()
    after = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all', 'verbose'], capture_output=True).stdout.lower()
    need(b'the-machine-desktop' not in after and len(after) >= len(rules), "Windows' firewall has nothing to ask about it")
    return q


@step('nothing comes back, and then it does')
def _():
    start()
    sign_in(False)
    need('Continue in your browser' in text(), text())
    need(until(lambda: 'Nothing came back' in text(), 30), text())
    need('Try again' in text('#go'), text('#go'))
    png('nothing-came-back')
    first = account.asked[-1]
    port = int(first['p'])
    for path in ('/', '/' + 'A' * 43 + '?u=x', f'/{first["c"]}', f'/{first["c"]}?u=nothing', '/favicon.ico'):
        try:
            told = urllib.request.urlopen(f'http://127.0.0.1:{port}{path}', timeout=10).status
        except urllib.error.HTTPError as e:
            told = e.code
        need(told == 404, f'{path} {told}')
    on.back_to_it(app)
    sign_in(True)  # pressed again
    need(dashboard(), text())
    need(account.asked[-1] == first, f'the same one, for each of its tabs: {first} {account.asked}')
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=5)
        need(False, 'its port goes with it')
    except urllib.error.URLError as e:
        need(not isinstance(e, urllib.error.HTTPError), e)
    on.browsers_closed()


@step('a second copy, from another folder')
def _():
    start(signed_in=True)
    need(dashboard(), text())
    # Its place is kept as another comes in front, and what was seen as the dashboard shows the list: that is its own, not the copy's
    kept = lambda: {k: v for k, v in saved().items() if k not in ('window', 'seen')}
    was = kept()
    on.other()
    ended = subprocess.run([str(copy)], env=app.env, timeout=20).returncode
    need(until(on.ours, 8), 'the one that runs comes forward')
    need(ended == 0 and pids() == app.pids() and kept() == was, f'{ended} {pids()} {app.pids()} {kept()}, was {was}')
    start()
    sign_in(False)
    its = handler()
    ended = subprocess.run([str(copy)], env=app.env, timeout=20).returncode
    need(its and program.lower() in its.lower() and handler() == its, f'the sign-in that goes on is the same: {its} {handler()}')
    ended = subprocess.run([str(copy), account.links[-1]], env=app.env, timeout=20).returncode
    need(dashboard(), f'a link that gets to it is the one\'s that runs {text()}')
    on.browsers_closed()
    return ended


@step('a start as the person, while an administrator\'s runs')
def _():
    start(signed_in=True)
    need(dashboard(), text())
    at, was = level(kernel.OpenProcess(0x1000, False, app.process.pid)), saved()
    need(at == 12288, f'this computer runs it with {at}')
    on.other()
    ended = plainly(program)
    forward = until(on.ours, 8)
    found = pids()
    png('started-as-the-person')
    wrong = [f'two of them: {found}'] if found != app.pids() else []
    wrong += [] if forward else ['the one that runs does not come forward']
    wrong += [] if saved() == was else [f'what is kept is now {saved()}']
    start()
    sign_in(False)
    its = handler()
    plainly(program, account.links[-1])
    wrong += [] if dashboard() else [f'the browser\'s link does not get to it: {text()}']
    start()
    sign_in(False)
    plainly(program)
    wrong += [] if its and handler() == its else [f'the sign-in\'s links are taken back: {its}, now {handler()}']
    on.browsers_closed()
    need(not wrong, f'ended {ended}; ' + '; '.join(wrong))
    return f'ended {ended}'


@step('an administrator\'s start, while the person\'s runs')
def _():
    global app
    app.kill()
    time.sleep(1)
    fresh()
    folder = pathlib.Path(os.environ['APPDATA'], ID)
    folder.mkdir(parents=True)
    (folder / 'app.json').write_text(json.dumps({'machine': machine.at + '/'}))
    kernel.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
    wait, kernel.WaitForSingleObject = kernel.WaitForSingleObject, lambda *_: 0
    try:
        plainly(program)
    finally:
        kernel.WaitForSingleObject = wait
    first = until(pids, 10)
    time.sleep(8)
    need(pids() == first and len(first) == 1, f'it runs: {pids()}')
    ended = subprocess.run([program], env=app.env, timeout=30).returncode
    time.sleep(3)
    need(pids() == first and ended == 0, f'the one that runs stays the one: {first} {pids()} {ended}')
    png('an-administrators-start')
    subprocess.run([program, '--quit'], env=app.env, timeout=20)
    need(until(lambda: not pids(), 20), 'and it quits it')
    return f'ended {ended}'


@step('back as it was')
def _():
    for pid in pids():
        os.kill(pid, 9)
    on.browsers_closed()
    fresh()


finish()
