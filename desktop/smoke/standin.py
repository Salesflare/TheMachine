"""A made-up Machine and account sign-in on 127.0.0.1 for windows.py: just the routes the app calls, as a sandbox build
takes them. It keeps what it was asked."""
import base64
import datetime
import hashlib
import http.server
import json
import pathlib
import secrets
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
# The dashboard's page of one to-do (?compact=1#card=<id>): its state in its title, a dialog of its own, links out
COMPACT = b'''<!doctype html><title>The Machine</title><style>body{margin:0;padding:12px;background:#fff;font:14px sans-serif}</style>
<h1></h1><p id="ipc"></p><button id="done">Done here</button> <button id="more">More</button> <a target="_blank" href="/#person=7">A person</a> <a href="/elsewhere">Away</a>
<button id="long">Long</button><div id="longer"></div><dialog>Something open <button>Close</button></dialog><script>
let id, done = false;
const draw = () => { id = (location.hash.match(/card=(\\w+)/) || [])[1]; document.querySelector('h1').textContent = 'To-do ' + id;
  document.title = (done ? 'done' : /^gone/.test(id) ? 'gone' : 'open') + ': To-do ' + id;
  };
onhashchange = draw;
document.querySelector('#done').onclick = () => { done = true; draw() };
document.querySelector('#long').onclick = () => { const s = document.querySelector('#longer').style; s.height = s.height ? '' : '300px' };
document.querySelector('#more').onclick = () => document.querySelector('dialog').showModal();
const i = window.__TAURI_INTERNALS__;
(i ? i.invoke('box_state').then(() => 'ALLOWED', () => 'refused') : Promise.resolve('none')).then(x => document.querySelector('#ipc').textContent = x);
setTimeout(draw, 300);
</script>'''
SNOOZE = [['2h', '2 hours'], ['tomorrow', 'Tomorrow \u00b7 9:00'], ['3d', '3 days \u00b7 9:00'], ['1w', '1 week \u00b7 9:00']]
HOURS = {'2h': 2, 'tomorrow': 24, '3d': 72, '1w': 168}


class Machine(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, port):
        super().__init__(('127.0.0.1', port), Page)
        self.port, self.actions, self.cookies, self.links, self.challenges = port, [], set(), [], {}
        self.seen, self.cards = [], []
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
            m.challenges[t] = q['c']
            back = urllib.parse.quote(f'http://127.0.0.1:{m.port}/_machine/auth?t={t}&to=app', safe='')
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
            return self.answer(COMPACT, kind='text/html')
        self.answer(DASHBOARD, kind='text/html')

    def do_POST(self):
        m = self.server
        asked = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        own = self.headers.get('Origin') == f'http://127.0.0.1:{m.port}' and self.headers.get('X-CSRF-Token') == 'made-up'
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
