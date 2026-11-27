"""The Machine's browser out through the app (src/exit.rs), on Windows: a real browser's page through the made-up Machine's
SOCKS5 listener reaches a made-up site from the address the app goes out from, and what isn't a public site on 80 or 443 is
refused. For CI's own throwaway computer (desktop.yml).

  python smoke/exit.py <sandbox build> - <folder for the pictures>
"""
import http.server
import json
import os
import pathlib
import subprocess
import threading
import time

import exit_side
import on_windows as on
from on_windows import ID, PORT, App, finish, fresh, need, saved, step, until
from standin import Machine

program = str(pathlib.Path(on.sandbox).resolve())
machine = Machine(PORT)
machine.tunnel = exit_side.Tunnel()
seen = []
app = None


class Site(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        seen.append(self.client_address[0])
        body = f'<title>Made-up site</title><p id="seen">{self.client_address[0]}</p>'.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Site)
threading.Thread(target=site.serve_forever, daemon=True).start()
target = f'http://127.0.0.1:{site.server_address[1]}/'


def start(away_from=None, **kept):
    global app
    if app:
        app.kill()
        need(until(lambda: not machine.tunnel.up.is_set(), 30), 'its way out ends with it')
    fresh()
    os.environ.pop('MACHINE_SANDBOX_EXIT_FROM', None)
    if away_from:
        os.environ['MACHINE_SANDBOX_EXIT_FROM'] = away_from
    folder = pathlib.Path(os.environ['APPDATA'], ID)
    folder.mkdir(parents=True)
    (folder / 'app.json').write_text(json.dumps({'machine': machine.at + '/', **kept}))
    app = App(program)
    need(until(lambda: app.answers('app'), 60), 'its page answers')


def browser():
    for path in (r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                 r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'):
        if os.path.exists(path):
            return path
    raise AssertionError('no Chrome or Edge')


def browse(url):
    """A headless browser's page through the Machine's way out, as its own browser would go."""
    profile = on.out / 'browser'
    got = subprocess.run([browser(), '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={profile}',
                          f'--proxy-server=socks5://127.0.0.1:{machine.tunnel.port}', '--proxy-bypass-list=<-loopback>', '--dump-dom', url],
                         capture_output=True, text=True, timeout=60)
    return got.stdout


@step('it connects')
def _():
    start('127.0.0.2')
    need(machine.tunnel.up.wait(60), 'the app takes the way out')
    need(until(lambda: machine.tunnel.hellos, 10), 'and says hello')
    hello = machine.tunnel.hellos[-1]
    need(hello.get('v') == 1 and hello.get('os') == 'windows', f'its hello: {hello}')
    need(until(lambda: saved().get('exit_at') == machine.at + '/', 10), f'it keeps that this Machine has it: {saved().get("exit_at")}')
    return hello


@step('a browser goes out through it')
def _():
    page = browse(target)
    need(seen and seen[-1] == '127.0.0.2', f'the site saw {seen}')
    need('127.0.0.2' in page, f'the page: {page[:200]}')
    return f'seen as {seen[-1]}'


@step('only public sites on 80 and 443')
def _():
    del machine.tunnel.refused[:]
    browse('http://10.1.2.3/')
    browse('http://1.1.1.1:8080/')
    browse('http://169.254.169.254/')
    refused = {(host, port): why for host, port, why in machine.tunnel.refused}
    need(refused.get(('10.1.2.3', 80)) == 'blocked', f'a private address: {refused}')
    need(refused.get(('1.1.1.1', 8080)) == 'port', f'another port: {refused}')
    need(refused.get(('169.254.169.254', 80)) == 'blocked', f'a cloud metadata address: {refused}')
    return refused


@step('this computer itself, without the sandbox address')
def _():
    start()
    need(machine.tunnel.up.wait(60), 'the app takes the way out')
    del machine.tunnel.refused[:], seen[:]
    browse(target)
    need(not seen, f'the site saw {seen}')
    need(any(why == 'blocked' for *_, why in machine.tunnel.refused), f'refused: {machine.tunnel.refused}')
    return machine.tunnel.refused


@step('off in Settings')
def _():
    del machine.tunnel.hellos[:]
    start('127.0.0.2', no_exit=True)
    time.sleep(15)
    need(not machine.tunnel.hellos, f'it stays away: {machine.tunnel.hellos}')


@step('back as it was')
def _():
    if app:
        app.kill()
    time.sleep(1)
    fresh()


finish()
