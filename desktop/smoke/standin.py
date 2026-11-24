"""A made-up Machine and account sign-in on 127.0.0.1 for windows.py and the Mac's: just the routes the app calls, as a sandbox build
takes them. It keeps what it was asked. Over https with the certificate of certificate.sh (its folder)."""
import base64
import datetime
import hashlib
import http.server
import json
import pathlib
import secrets
import socketserver
import ssl
import threading
import time
import urllib.parse

TODOS = [('aa01', 'Answer Nora about the lunch'), ('aa02', 'Send Ravi the floor plan'), ('aa03', 'Book the van for Friday'), ('aa04', 'Pay the florist')]

ICON = (pathlib.Path(__file__).parents[2] / 'brand' / 'app-icon-192.png').read_bytes()
MANIFEST = {'id': '.', 'name': 'The Machine', 'start_url': '.', 'scope': '.', 'display': 'standalone',
            'launch_handler': {'client_mode': ['focus-existing', 'auto']}, 'icons': [{'src': 'icon.png', 'sizes': '192x192', 'type': 'image/png'}]}
# Says which window it is, whether it is an app's, and where it points, also when its app is started again
DASHBOARD = b'''<!doctype html><link rel="manifest" href="manifest.webmanifest"><title>Stand-in</title><h1>Stand-in dashboard</h1><script>
const me = Math.random().toString(36).slice(2);
const tell = () => { document.title = 'Stand-in ' + location.hash; document.querySelector('h1').textContent = 'Stand-in dashboard ' + location.hash;
  fetch('seen?' + new URLSearchParams({me, at: location.hash, app: matchMedia('(display-mode: standalone)').matches ? 'yes' : ''})) };
onhashchange = tell;
if (window.launchQueue) launchQueue.setConsumer(p => { const u = p.targetURL && new URL(p.targetURL);
  if (u && u.hash && u.hash !== location.hash) location.hash = u.hash });
onfocus = tell;
tell();
</script>'''
# The dashboard in the app's own window: what it does with a browser around it (mac_window.py)
WINDOW = b'''<!doctype html><link rel="manifest" href="manifest.webmanifest"><title>Stand-in</title><style>body{margin:0;padding:16px;background:light-dark(#f8f7f3,#1b1c1f);color:light-dark(#222,#eee);color-scheme:light dark;font:15px sans-serif}
#drop{border:1px dashed;padding:20px;width:260px}iframe{width:300px;height:60px;border:1px solid}p{margin:8px 0}</style>
<h1>Stand-in dashboard</h1><p id="told"></p><p id="ipc"></p><p><input id="field" value="some words"> <input id="pick" type="file" multiple> <span id="picked"></span></p>
<p><a id="web" target="_blank" rel="noopener" href="OUT?web">Web</a> <a id="here" href="OUT?here">Here</a> <a id="mail" href="mailto:a@b.example?subject=new">Mail</a> <a id="mailnew" target="_blank" href="mailto:a@b.example?subject=newer">Mail too</a>
<a id="own" target="_blank" href="/#person=7">Own</a> <button id="opens">window.open</button> <button id="goes">location</button> <button id="blank">a window, then location</button> <button id="hop">Account</button></p>
<p><a id="file" target="_blank" rel="noopener" download="a.txt" href="api/chat-file?id=1">File</a> <a id="save" download="b.txt" href="api/chat-file?id=3">Save</a> <button id="blob">blob</button> <a id="sent" href="api/attachment?id=4&sent=1">Sent as a file</a>
<a id="sentnew" target="_blank" href="api/attachment?id=5&sent=1">Sent, in a window</a> <a id="pdf" target="_blank" href="api/attachment?id=6&pdf=1">PDF</a></p>
<p><button id="alert">alert</button> <button id="confirm">confirm</button> <button id="prompt">prompt</button> <button id="mic">microphone</button></p>
<div id="drop">Drop here</div><p><iframe id="frame" srcdoc="<body style='font:15px sans-serif'><p id=words>In a frame</p><a id=framed target=_blank href='OUT?framed'>Framed</a></body>"></iframe></p>
<p>The needle is here. And a second needle there.</p><div style="height:1600px"></div><p>The last needle.</p><script>
const me = Math.random().toString(36).slice(2), $ = s => document.querySelector(s), says = x => { $('#told').textContent = x };
const tell = () => { document.title = 'Stand-in ' + location.hash; $('h1').textContent = 'Stand-in dashboard ' + location.hash;
  fetch('seen?' + new URLSearchParams({me, at: location.hash, desktop: window.machineDesktop ? machineDesktop.version : ''})) };
addEventListener('hashchange', tell);
tell();
const on = (s, run) => { $(s).onclick = run };
on('#opens', () => window.open('OUT?opens', '_blank', 'noopener'));
on('#goes', () => { location.href = 'OUT?goes' });
on('#blank', () => { const w = window.open('about:blank'); if (w) w.location = 'OUT?blank'; else location.assign('OUT?blank') });
on('#hop', () => { const f = Object.assign(document.createElement('form'), {method: 'post', action: '/_machine/account-hop'}); document.body.append(f); f.submit() });
on('#blob', () => Object.assign(document.createElement('a'), {href: URL.createObjectURL(new Blob(['x'])), download: 'c.txt'}).click());
on('#alert', () => { alert('Something\\nto know'); says('alerted') });
on('#confirm', () => says('confirm ' + confirm('Delete this?')));
on('#prompt', () => says('prompt ' + prompt('What name?', 'Sam')));
if (window.webkitSpeechRecognition) says('speech');
on('#mic', () => { says('asking'); navigator.mediaDevices.getUserMedia({audio: true}).then(s => says('microphone ' + s.getAudioTracks().length), e => says('microphone ' + e.name)) });
$('#pick').onchange = e => { $('#picked').textContent = [...e.target.files].map(f => f.name).join(', ') };
$('#drop').ondragover = e => e.preventDefault();
$('#drop').ondrop = e => { e.preventDefault(); says('dropped ' + [...e.dataTransfer.files].map(f => f.name).join(', ')) };
addEventListener('machinedesktop', e => says(JSON.stringify(e.detail)));
const i = window.__TAURI_INTERNALS__;
(i ? Promise.all(['app_state', 'settings_state', 'box_state'].map(c => i.invoke(c).then(() => 'ALLOWED', () => 'refused'))).then(x => [...new Set(x)].join()) : Promise.resolve('none')).then(x => { $('#ipc').textContent = x });
</script>'''
PDF = b'''%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 400 300]/Contents 4 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>>>>endobj
4 0 obj<</Length 44>>stream
BT /F1 24 Tf 60 150 Td (A made-up PDF) Tj ET
endstream endobj
trailer<</Root 1 0 R>>
%%EOF'''
# The dashboard's page of one to-do (?compact=1#card=<id>): its state in its title, a dialog of its own, links out
COMPACT = b'''<!doctype html><title>The Machine</title><style>body{margin:0;padding:12px;background:#fff;font:14px sans-serif}</style>
<h1></h1><p id="ipc"></p><button id="done">Done here</button> <button id="more">More</button> <a target="_blank" href="/#person=7">A person</a> <a href="/elsewhere">Away</a>
<button id="long">Long</button><div id="longer"></div><p id="leave" style="white-space:nowrap" hidden><a id="own" target="_blank" href="/#person=7">Own</a> <a id="web" target="_blank" rel="noopener" href="OUT?web">Web</a>
<a id="mail" target="_blank" href="mailto:a@b.example?subject=new">Mail</a><br><a id="file" target="_blank" rel="noopener" download="a.txt" href="/api/chat-file?id=1">File</a> <a id="view" target="_blank" href="/api/attachment?id=2">View</a> <a id="save" download="b.txt" href="/api/chat-file?id=3">Save</a><br><a id="here" href="OUT?here">Here</a> <a id="mailhere" href="mailto:a@b.example?subject=here">Mail here</a><br>
<button id="opens">window.open</button> <button id="opensown">of its own</button> <br><button id="goes">location</button> <button id="goesmail">mail</button> <button id="blob">blob</button></p><dialog>Something open <button>Close</button></dialog><script>
let id, done = false;
const draw = () => { id = (location.hash.match(/card=(\\w+)/) || [])[1]; document.querySelector('h1').textContent = 'To-do ' + id;
  document.querySelector('#leave').hidden = id !== 'aa03';
  document.title = (done ? 'done' : /^gone/.test(id) ? 'gone' : 'open') + ': To-do ' + id;
  };
onhashchange = draw;
const on = (name, run) => document.querySelector(name).onclick = run;
on('#opens', () => window.open('OUT?opens', '_blank', 'noopener'));
on('#opensown', () => window.open('/#person=8'));
on('#goes', () => { location.href = 'OUT?goes' });
on('#goesmail', () => { location.href = 'mailto:a@b.example?subject=goes' });
on('#blob', () => Object.assign(document.createElement('a'), {href: URL.createObjectURL(new Blob(['x'])), download: 'c.txt'}).click());
document.querySelector('#done').onclick = () => { done = true; draw() };
document.querySelector('#long').onclick = () => { const s = document.querySelector('#longer').style; s.height = s.height ? '' : '300px' };
document.querySelector('#more').onclick = () => document.querySelector('dialog').showModal();
const i = window.__TAURI_INTERNALS__;
(i ? i.invoke('box_state').then(() => 'ALLOWED', () => 'refused') : Promise.resolve('none')).then(x => document.querySelector('#ipc').textContent = x);
setTimeout(draw, 300);
</script>'''
# What leaves it (on aa03), and where to: a place in the dashboard, a page in the browser, a mail, or nowhere
LEAVES = [('#web', 'browser', '/out?web'), ('#opens', 'browser', '/out?opens'), ('#file', 'browser', '/api/chat-file?id=1'), ('#view', 'browser', '/api/attachment?id=2'),
          ('#save', 'browser', '/api/chat-file?id=3'), ('#mail', 'mail', 'mailto:a@b.example?subject=new'), ('#mailhere', 'mail', 'mailto:a@b.example?subject=here'),
          ('#goesmail', 'mail', 'mailto:a@b.example?subject=goes'), ('#here', 'nowhere', ''), ('#goes', 'nowhere', ''), ('#blob', 'nowhere', ''),
          ('#own', 'dashboard', '#person=7'), ('#opensown', 'dashboard', '#person=8')]
SNOOZE = [['2h', '2 hours'], ['tomorrow', 'Tomorrow \u00b7 9:00'], ['3d', '3 days \u00b7 9:00'], ['1w', '1 week \u00b7 9:00']]
HOURS = {'2h': 2, 'tomorrow': 24, '3d': 72, '1w': 168}


class Machine(http.server.ThreadingHTTPServer):
    daemon_threads = True
    server_bind = socketserver.TCPServer.server_bind  # HTTPServer's looks for the computer's name, on the local network too

    def __init__(self, port, certificate=None):
        super().__init__(('127.0.0.1', port), Page)
        self.at = f'http{"s" if certificate else ""}://127.0.0.1:{port}'
        if certificate:
            tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            tls.load_cert_chain(certificate / 'cert.pem', certificate / 'key.pem')
            self.socket = tls.wrap_socket(self.socket, server_side=True, do_handshake_on_connect=False)  # on each one's own thread
        self.port, self.actions, self.cookies, self.links, self.challenges = port, [], set(), [], {}
        self.seen, self.cards, self.left, self.opened, self.hops = [], [], [], [], []
        self.account = self.machine = None  # its account's address; whose account this is
        self.window, self.away = False, None  # the dashboard is the app's window's; where a signed-out one is sent
        self.desks, self.notices, self.meeting = [], [], None  # what the robot says of itself with each look; what waits for it to say
        self.todos, self.name = list(TODOS), 'Sam'
        self.refuse = False
        self.compact = False  # its dashboard has the page of one to-do
        self.no = None  # why it doesn't take a decision
        self.gone, self.status = {}, {}  # a to-do's own state
        threading.Thread(target=self.serve_forever, daemon=True).start()

    def stop(self):
        self.shutdown()
        self.server_close()


class Page(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def answer(self, body, status=200, kind='application/json', **headers):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        for k, v in {'Content-Type': kind, 'Content-Length': str(len(data)), **headers}.items():
            self.send_header(k.replace('_', '-'), v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        m, u = self.server, urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        if u.path == '/open':  # the account: the browser shows this, and windows.py opens the link it would go to
            t = secrets.token_urlsafe(32)
            own = m.machine or m
            if 'c' not in q:
                return self.answer(b'<title>Stand-in account</title>', kind='text/html')
            own.challenges[t] = q['c']
            back = urllib.parse.quote(f'{own.at}/_machine/auth?t={t}&to=app', safe='')
            m.links.append('computer.themachine.app://signed-in?u=' + back)
            return self.answer(b'<title>Stand-in account</title>Signed in', kind='text/html')
        if u.path == '/_machine/auth':
            made = base64.urlsafe_b64encode(hashlib.sha256(q.get('v', '').encode()).digest()).rstrip(b'=').decode()
            if m.challenges.pop(q.get('t'), None) != made:
                return self.answer({}, 403)
            cookie = '__Host-machine=' + secrets.token_urlsafe(24)
            m.cookies.add(cookie)
            return self.answer(b'', 302, Location='/', Set_Cookie=cookie + '; Path=/; Secure; HttpOnly')
        if u.path == '/manifest.webmanifest':
            return self.answer(MANIFEST, kind='application/manifest+json')
        if u.path == '/icon.png':
            return self.answer(ICON, kind='image/png')
        if u.path == '/api/attachment' and 'pdf' in q:
            return self.answer(PDF, kind='application/pdf', Content_Disposition="inline; filename*=UTF-8''Plan%20B.pdf")
        if u.path == '/api/attachment' and 'sent' in q:
            return self.answer(b'made up', kind='application/octet-stream', Content_Disposition=f"attachment; filename*=UTF-8''sent%20{q['id']}.bin")
        if u.path == '/hop':
            m.hops.append(q)
            return self.answer(b'<title>Stand-in account</title>The account', kind='text/html')
        if u.path in ('/out', '/api/chat-file', '/api/attachment'):
            if not self.headers.get('Referer'):  # the browser's, not the page's own
                m.left.append(self.path)
            return self.answer(b'<title>Stand-in</title>What left the to-do', kind='text/html')
        if u.path == '/seen':
            m.seen.append(q)
            return self.answer({})
        if m.refuse:
            return self.answer({'error': 'Sign in'}, 403)
        if u.path == '/api/session':
            return self.answer({'csrf': 'made-up', **({'compact': 1} if m.compact else {})})
        if u.path == '/api/status':
            waits = []
            if 'desk' in q:
                m.desks.append((q['desk'], q.get('up')))
                if q.get('up') == '1':
                    m.notices = [n for n in m.notices if n['key'] not in q.get('got', '').split(',')]
                    waits = m.notices
            return self.answer({**({'notices': waits, **({'meeting': m.meeting} if m.meeting and q.get('up') == '1' else {})} if 'desk' in q else {}), 'first_name': m.name, 'suggestions': [{'id': i, 'title': t, 'status': 'prepared' if i != 'aa01' else 'pending', 'due': '2000-01-01' if i == 'aa01' else None,
                                                                             'created_at': '2026-01-01T00:00:00Z', 'snooze_choices': SNOOZE, **m.status.get(i, {})} for i, t in m.todos]})
        if u.path == '/api/notice':
            own = m.status.get(q['tag'], {}).get('status', 'pending' if q['tag'] == 'aa01' else 'prepared')
            first = {'pending': ['prepare'], 'accepted': []}.get(own, ['draft'])
            named = dict(TODOS).get(q['tag'])
            return self.answer({'title': named, 'body': 'Made up, for the stand-in.', 'actions': [*first, 'snooze2h', 'done', 'send'],
                                'labels': {'open': 'Open', 'prepare': 'Do it', 'draft': 'See draft', 'snooze2h': 'Snooze', 'done': 'Mark done', 'send': 'Send'},
                                'events': {'prepare': 'Preparing it', 'snooze2h': 'Snoozed it', 'done': 'Marked it done', 'send': 'Sent'}})
        if q.get('compact') == '1':
            m.cards.append(self.headers.get('Cookie') in m.cookies)
            return self.answer(COMPACT.replace(b'OUT', f'http://localhost:{m.port}/out'.encode()), kind='text/html')
        if m.away:
            return self.answer(b'', 302, Location=m.away)
        if u.path == '/':  # a browser asks for an icon too
            m.opened.append(self.headers.get('Cookie') in m.cookies)
        self.answer(WINDOW.replace(b'OUT', f'http://localhost:{m.port}/out'.encode()) if m.window else DASHBOARD, kind='text/html')

    def do_POST(self):
        m = self.server
        if self.path == '/_machine/account-hop' and m.account:
            return self.answer(b'', 302, Location=m.account + '/hop?t=made-up')
        asked = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        own = self.headers.get('Origin') == m.at and self.headers.get('X-CSRF-Token') == 'made-up'
        if self.path != '/api/action' or not own:
            return self.answer({'error': 'Not from the dashboard'}, 403)
        if asked['action'] in ('decide', 'card_new') and m.no:
            return self.answer({'error': m.no}, 409)
        m.actions.append((asked['action'], asked['args'], self.headers.get('Cookie') in m.cookies))
        if asked['action'] == 'search_ask':
            return self.answer({'answer': 'Nora wrote on Monday: lunch is at 12:30, at the corner place.'})
        if asked['action'] == 'decide':
            todo, choice = asked['args']['suggestion_id'], asked['args']['choice']
            if choice in ('snooze', 'complete'):
                m.gone[todo] = m.todos
                m.todos = [x for x in m.todos if x[0] != todo]
            elif todo in m.gone:
                m.todos = m.gone.pop(todo)
            if choice == 'accept' and asked['args']['decision_id'].startswith('notify-'):  # Do it: the run is on
                m.status[todo] = {'status': 'accepted', 'preparation_status': 'queued'}
            until = datetime.datetime.fromtimestamp(time.time() + 3600 * HOURS[asked['args'].get('snooze_option', '2h')], datetime.timezone.utc)
            return self.answer({'status': 'ok', **({'snoozed_until': until.isoformat()} if choice == 'snooze' else {})})
        if asked['action'] == 'card_new':
            made = 'bb0' + str(len(m.actions))
            m.todos, m.status[made] = [*m.todos, (made, asked['args']['text'])], {'status': 'pending'}
            return self.answer({'id': made, 'title': asked['args']['text'], 'status': 'pending'})
        self.answer({'id': 'bb0' + str(len(m.actions))})
