"""The sandbox: the real dashboard and app on made-up data, with a stand-in Network, sealed off from the world.

    python3 sandbox/run.py --state busy            # then open http://127.0.0.1:8870
    python3 sandbox/run.py --state fleet,friends --port 8880

What runs: assistant.App from this checkout, on a fresh database in --dir (default /tmp/machine-sandbox-<port>) built
from sandbox/fixture.json; sandbox/stub_network.py as the Network when the state has a Fleet or friends; and a small proxy on
--port that signs every request in as the owner, so a browser (or Playwright) on this machine can click everything.

What doesn't: no collector, review, preparation, delivery, model or enrichment worker runs. An approved send (email,
Slack, WhatsApp, LinkedIn, X) goes to <dir>/sent.jsonl instead, and the phone and Telegram notifications too. guard.py
refuses any connection beyond 127.0.0.1 and any program start, whatever the code path."""
import argparse
import datetime as dt
import hashlib
import http.client
import http.server
import json
import os
import socket
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import guard  # noqa: E402
import load  # noqa: E402
import stub_network as network  # noqa: E402

for name in ('http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY'):
    os.environ.pop(name, None)


class Sent:
    """Where the sandbox's sends go: one JSON line each."""

    def __init__(self, path):
        self.path, self.lock, self.count = Path(path), threading.Lock(), 0

    def record(self, channel, value):
        with self.lock:
            self.count += 1
            with self.path.open('a') as handle:
                handle.write(json.dumps({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'channel': channel, 'value': value}, default=str) + '\n')
            return self.count


class FakeTransport:
    """Stands in for next_actions.ActionTransport: every approved send is recorded and reported sent."""

    def __init__(self, sent):
        self.sent = sent

    def pick(self, action):
        return self

    def preflight(self, action):
        return None

    def send(self, action, job):
        n = self.sent.record(action.get('kind', 'email'), action)
        return {'message_id': f'sandbox-{n}', 'thread_id': f'sandbox-thread-{n}'}

    def reconcile(self, action, job):
        return {'message_id': job.get('message_id') or 'sandbox-reconciled'}


def quiet_workers(app, sent):
    """Turns off everything that would read a real source, call a model or reach the owner, and fakes the sends."""
    import assistant
    for name in ('collector', 'delivery_worker', 'preparation_worker', 'review_worker', 'graph_worker', 'model_usage_worker',
                 'embedding_worker', 'enrichment_worker'):
        setattr(app, name, lambda *a, **k: None)
    transport = FakeTransport(sent)
    original = app.action_step
    app.action_step = lambda transport_=None: original(transport)
    import onboarding
    onboarding.missing = lambda config, account: ''  # the made-up accounts count as set up; there is nothing to sign in to
    assistant.push_send = lambda store, config, subscriptions, payload, label, sender=None: sent.record('push', payload)
    assistant.fleet_push = lambda store, config, rows, sender=None: sent.record('push', {'fleet_questions': len(rows)})
    assistant.fleet_notice_push = lambda store, config, view, sender=None: sent.record('push', view)
    assistant.fleet_telegram = lambda config, message, message_id=None, request=None: sent.record('telegram', message) and {}
    assistant.telegram = lambda config, row, action, message_id=None: sent.record('telegram', {'card': row.get('id') if hasattr(row, 'get') else None}) and {}


def seed_model(app):
    """Settings > Model: a made-up model on a signed-in plan, a limit half used and no resets left."""
    reset = int(time.time()) + 3 * 3600
    app.model_status = {'model': 'acme/lm-2.5-swift', 'provider': 'acme', 'chatgpt': True, 'plan': 'plus',
                        'windows': [{'label': '5h', 'used': 46, 'reset': reset}, {'label': 'Week', 'used': 12, 'reset': reset + 5 * 86400}],
                        'limit_reached': False, 'limit_resets_at': None, 'resets': {'available': 0, 'credits': []}, 'can_reset': False,
                        'usage_page': 'https://chatgpt.example/usage', 'checked_at': dt.datetime.now(dt.timezone.utc).isoformat()}
    # The models a chat can pick (chat_model.py), as the Gateway would list them for a made-up sign-in
    import chat_model
    models = [{'ref': 'acme/lm-2.5-swift', 'name': 'LM-2.5 Swift', 'levels': ['low', 'medium', 'high', 'xhigh', 'max'], 'default': 'low'},
              {'ref': 'acme/lm-2.5-mini', 'name': 'LM-2.5 Mini', 'levels': ['off', 'low', 'medium', 'high'], 'default': 'low'},
              {'ref': 'acme/lm-3-pro', 'name': 'LM-3 Pro', 'levels': ['low', 'medium', 'high', 'xhigh', 'max'], 'default': 'medium'}]
    app.chat_catalog = chat_model.Catalog(reader=lambda config: models)
    app.chat_catalog.refresh(app.config)
    # Settings > Signatures imports the mailbox's own: a made-up Gmail signature, no Google call.
    app.mail_read = lambda config, account, *a: {'signature': '<div><b>Alex Morgan</b></div><div style="color:#4e6b34">Lumen Labs</div><div><a href="https://lumenlabs.example">lumenlabs.example</a></div>'}


def fake_help(config, prompt, model=None, thinking=None):
    """Help's stand-in model: the first lines of the help section that matched best, cited as [1]. No model runs."""
    import re
    found = re.search(r'^\[1\] Help: [^\n]*\n(.+?)(?:\n\n|$)', prompt, re.M | re.S)
    if not found:
        return 'The help pages don’t cover that. Try Report a bug, or write to support@themachine.computer.'
    text = re.sub(r'[*`]|\[([^\]]+)\]\([^)]+\)', lambda m: m[1] or '', found[1])
    return ' '.join(re.split(r'(?<=[.!?])\s+', ' '.join(text.split()))[:3]) + ' [1]'


def seed_ai(app):
    """Settings, AIs (ai_access.py): Claude connected for Work with Read & edit, and a key for a script that only
    reads, with a few calls each and one refused. Writes only through ai_access."""
    import ai_access
    now = dt.datetime.now(dt.timezone.utc)
    with app.store.connect() as db:
        if ai_access.connections(db):
            return
        client = ai_access.register(db, {'redirect_uris': ['https://claude.ai/api/mcp/auth_callback'], 'client_name': 'Claude'})
        req = {'client_id': client['client_id'], 'redirect_uri': 'https://claude.ai/api/mcp/auth_callback', 'name': 'Claude',
               'challenge': 'x' * 43, 'state': ''}
        ai_access.approve(db, req, 'draft', 'work', '30d', 'http://127.0.0.1')
        cid = next(c['id'] for c in ai_access.connections(db) if c['kind'] == 'oauth')
        key = ai_access.new_key(db, 'Morning script', 'read', 'both', '7d')['id']
        lines = [(cid, 25, 'list_todos', 'ok', '6 to-dos'), (cid, 24, 'search_graph', 'ok', '2 found'),
                 (cid, 20, 'get_todo', 'ok', '“Send the renewal quote”'),
                 (cid, 15, 'create_draft', 'ok', 'To buyer@example.com: “Renewal quote”'),
                 (key, 14, 'list_todos', 'ok', '9 to-dos'), (key, 13, 'create_todo', 'refused', 'Refused: this connection can only read')]
        for connection, hours, tool, outcome, detail in lines:
            ai_access.log(db, connection, tool, outcome, detail, at=now - dt.timedelta(hours=hours))
        ai_access.used(db, cid, at=now - dt.timedelta(minutes=12))
        ai_access.used(db, key, at=now - dt.timedelta(hours=13))
        claude = dict(db.execute('SELECT * FROM ai_connections WHERE id=?', (cid,)).fetchone())
        people = [r['node_id'] for r in db.execute('SELECT node_id FROM person_summaries ORDER BY node_id')]
    # Its Graph changes, each with Undo in Activity: through the same tools an AI calls, on a Work person it may see
    for node in people:
        try:
            changes = [app.ai_tool(claude, 'save_fact', {'id': node, 'text': 'Prefers a call over email for contract questions',
                                                         'kind': 'preference'}),
                       app.ai_tool(claude, 'add_summary_line', {'id': node, 'text': 'Asked for the renewal terms before the board meeting'})]
        except ValueError:
            continue
        with app.store.connect() as db:
            for (_, said, write), (tool, minutes) in zip(changes, (('save_fact', 9), ('add_summary_line', 8))):
                ai_access.log(db, cid, tool, 'ok', said, at=now - dt.timedelta(minutes=minutes), write=write)
        # Then Messages on: a read, logged by count and thread, and a change that waits for the owner's OK
        with app.store.connect() as db:
            ai_access.change(db, cid, messages=True, at=now - dt.timedelta(minutes=7))
            ai_access.log(db, cid, 'read_thread', 'ok', '3 messages read, from “Renewal quote”', at=now - dt.timedelta(minutes=6))
        try:
            _, said, write = app.ai_tool({**claude, 'messages': 1}, 'save_fact', {'id': node, 'text': 'Wants the renewal signed before March'})
        except ValueError:
            break
        with app.store.connect() as db:
            ai_access.log(db, cid, 'save_fact', 'ok', said, at=now - dt.timedelta(minutes=5), write=write)
        break


def seed_transcript(app):
    """Generate notes in the Calendar: the latest past meeting with guests has a long made-up transcript (2h 15m) and no
    notes yet."""
    import assistant
    now = dt.datetime.now(dt.timezone.utc)
    with app.store.connect() as db:
        rows = db.execute("SELECT id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND occurred_at<? "
                          "ORDER BY occurred_at DESC LIMIT 40", (now.isoformat(),)).fetchall()
    for r in rows:
        m = json.loads(r['metadata'] or '{}')
        guests = [g for g in m.get('attendees') or [] if isinstance(g, dict) and not g.get('self')]
        if len(guests) >= 1 and not m.get('all_day'):
            break
    else:
        return
    names = ['Alex Morgan'] + [str(g.get('displayName') or g.get('email', '').split('@')[0].replace('.', ' ').title()) for g in guests[:2]]
    topics = ['the pilot timeline', 'reminders on shared inboxes', 'the rollout to the second team', 'pricing for the larger plan',
              'the security questions from IT', 'who owns the onboarding checklist', 'the go-live date']
    lines = []
    for minute in range(135):
        for second in range(0, 60, 6):
            who = names[(minute + second // 6) % len(names)]
            topic = topics[minute // 20]
            lines.append(f'[{minute // 60}:{minute % 60:02d}:{second:02d}] {who}: On {topic}, we went through what is open and what comes next.')
    lines.append(f'[2:14:30] {names[0]}: So we go live on the 15th, and I send the rollout plan by Friday.')
    app.meeting_notes({'event_id': r['id'], 'field': 'transcript', 'text': '\n'.join(lines)}, True)
    print(f"sandbox: a 2h 15m transcript on \"{r['title']}\" ({r['occurred_at'][:16]})", flush=True)


def fake_notes(config, prompt):
    """Generate notes' stand-in model: a few seconds per turn (so the dialog shows Writing notes…), then made-up notes in
    the shape the prompt asks for. No model runs."""
    import re
    time.sleep(4)
    if 'This is part' in prompt:
        part = re.search(r'This is part (\d+) of (\d+)', prompt)
        return f'- Part {part[1]}: went through what is open and what comes next.'
    title = re.search(r'^Meeting: (.+?), \d{4}-', prompt, re.M)
    return (f"## Summary\n\n{title[1] if title else 'The meeting'}: the team went through the pilot, the rollout and pricing, and agreed on a go-live date.\n\n"
            '## Decisions\n\n- Go live on the 15th\n- Start the rollout with the second team\n\n'
            '## Action items\n\n- **Alex Morgan**: send the rollout plan by Friday\n- **Unassigned**: answer the security questions from IT')


def fake_summary(config, prompt):
    """Person summaries' stand-in model (person_summary.py): lines about substance, never what the page shows already
    (role, organization, how often you talk), each citing the evidence it was given. Organizations by their display name
    from the fixture. No model runs."""
    people = json.loads(prompt.split('\nPeople:\n', 1)[1])
    names = {c['domain']: c['name'] for c in json.loads((HERE / 'fixture.json').read_text())['companies']}
    out = []
    for p in people:
        signals, promises, facts = p.get('signals') or [], p.get('open_promises') or [], p.get('facts') or []
        org = names.get(p['node_id'].rpartition('@')[2]) or p.get('organization')
        title = lambda m: (m.get('title') or 'a message').strip().rstrip('.')[:100]
        lines = []
        if signals:
            first, latest = signals[-1], signals[0]
            lines.append({'kind': 'who', 'text': f"You first worked together on {title(first)}.", 'sources': [first['id']] + [f['id'] for f in facts[:1]]})
            lines.append({'kind': 'now', 'text': f"Latest with {org}: {title(latest)}." if org else f"Latest: {title(latest)}.", 'sources': [latest['id']]})
        for promise in promises[:2]:
            who = 'You promised' if promise['who_promised'] == 'the owner' else 'They promised'
            lines.append({'kind': 'open', 'text': f"{who}: {promise['what'][:140]}", 'sources': [promise['id']]})
        out.append({'node_id': p['node_id'], 'lines': lines})
    return json.dumps({'people': out})


def seed_summaries(app):
    """The person summaries on top of their pages, written once by the stand-in for everyone with real activity."""
    import person_summary
    with app.store.connect() as db:
        people = person_summary.due(db, limit=40)
    if people:
        written = app.summary_run(people)
        print(f'sandbox: {written} person summaries', flush=True)


def proxy(public_port, app_port, config):
    """Signs each request in as the owner on the dashboard's own host (what Tailscale Serve does for real)."""
    host, owner = config['dashboard_host'], config['tailscale_owner']

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'

        def log_message(self, *_):
            pass

        def forward(self):
            length = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(length) if length else None
            headers = {k: v for k, v in self.headers.items() if k.lower() not in ('host', 'origin', 'tailscale-user-login', 'x-tailnet-client',
                                                                                    'x-forwarded-for', 'authorization', 'connection')}
            headers.update({'Host': host, 'Tailscale-User-Login': owner})
            if self.command == 'POST':
                headers['Origin'] = 'https://' + host
            connection = http.client.HTTPConnection('127.0.0.1', app_port, timeout=120)
            try:
                connection.request(self.command, self.path, body=body, headers=headers)
                response = connection.getresponse()
                data = response.read()
            except OSError:
                data, response = b'{"error":"The sandbox app is not answering"}', None
            self.send_response(response.status if response else 502)
            for k, v in (response.getheaders() if response else [('Content-Type', 'application/json')]):
                if k.lower() not in ('content-length', 'connection', 'transfer-encoding'):
                    self.send_header(k, v)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            connection.close()

        do_GET = do_POST = do_HEAD = forward

    server = http.server.ThreadingHTTPServer(('127.0.0.1', public_port), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def seed_network(app, net, fixture):
    """What the Network had waiting: teammates' questions and requests, a seat request, and an answered question of the owner's."""
    groups_ids = {'work': fixture['network']['work']['id'], 'family': fixture['network']['family']['id']}
    names = {m['member_id']: m['name'] for g in ('work', 'family') for m in fixture['network'][g]['team']}
    asks = [{'id': a['id'], 'kind': a['kind'], 'fleet_id': groups_ids[a['fleet']], 'from': a['from'], 'name': names.get(a['from'], ''),
             'question': a['question']} for a in fixture['network']['asks'] if a['fleet'] in ('work', 'family') and
            {'work': 'work', 'family': 'family'}[a['fleet']] in net.groups]
    notices = [n for n in net.notices.values() if n['fleet'] in net.groups]
    net.queue(asks, notices)
    if 'work' in net.groups:
        for asked in fixture['network']['asked']:
            def ask(asked=asked):
                for _ in range(20):
                    try:
                        app.fleet.directory(refresh=True)
                        return app.fleet.ask(asked['kind'], asked['question'])
                    except Exception:  # the Fleet still starting up
                        time.sleep(0.5)
            threading.Thread(target=ask, daemon=True).start()
        for handed in fixture['network'].get('handed', []):
            def hand(handed=handed):
                card = hashlib.sha256(handed['card'].encode()).hexdigest()[:16]  # as load.py names the card
                for _ in range(20):
                    try:
                        app.fleet.directory(refresh=True)
                        return app.fleet.hand_off(card, app.fleet.ref('work'), handed['to'], handed['title'], handed['summary'], sources=False)
                    except Exception:  # the Fleet still starting up
                        time.sleep(0.5)
            threading.Thread(target=hand, daemon=True).start()
        threading.Thread(target=seed_brief, args=(app, fixture), daemon=True).start()
        threading.Thread(target=seed_graph, args=(app,), daemon=True).start()


def seed_graph(app):
    """The Shared Graph (shared_graph.py): this Machine, the Fleet's owner, confirms Priya's and Tomasz's Machines as it
    would on its owner's OK, so their Machines get its graph key and share theirs. Its own sharing starts in a day."""
    for _ in range(40):
        try:
            app.fleet.directory(refresh=True)
            app.fleet.shared_round()
            app.fleet.directory(refresh=True)
            app.fleet.graph_round(force=True)
            prompts = [p for p in app.fleet._prompts() if p['kind'] == 'member']
            if prompts:
                for p in prompts:
                    app.fleet.share_ok(p['id'], 'yes')
                app.fleet.directory(refresh=True)
                app.fleet.graph_round(force=True)
                app.fleet.graph_fetch()
                return
        except Exception as error:  # noqa: BLE001 - the Fleet still starting up
            print('sandbox graph seed waiting:', type(error).__name__, error, file=sys.stderr, flush=True)
        time.sleep(0.5)


def seed_brief(app, fixture):
    """This morning's team brief: this Machine's own facts from the sandbox mail, and two teammates' answers made of the
    fixture's companies (a customer waiting on one of them, one you both write to, a shared meeting, one gone quiet)."""
    import fleet
    for _ in range(20):
        try:
            app.fleet.directory(refresh=True)
            refs = app.fleet.work_fleets()
            break
        except Exception:  # the Fleet still starting up
            time.sleep(0.5)
    else:
        return
    today = dt.date.today()
    ago = lambda days: (today - dt.timedelta(days=days)).isoformat()
    company = lambda n: {'org': fixture['companies'][n]['name'], 'domain': fixture['companies'][n]['domain']}
    team = [m['name'] for m in fixture['network']['work']['team'] if m['machine']]
    for ref in refs:
        since = ago(1)
        with app.fleet.connect() as db:
            own = app.fleet.compute(db, 'brief', {'since': since}, False, ref)
        touched = own['touched'][:1] or [{**company(0), 'count': 3, 'last': ago(1)}]
        first = {'touched': [{**t, 'count': 2, 'last': ago(2)} for t in touched] + [{**company(2), 'count': 4, 'last': ago(1)}],
                 'quiet': [], 'replied': [], 'meetings': [{**company(6), 'day': (today + dt.timedelta(days=1)).isoformat(), 'key': 'b' * 64}],
                 'unanswered': [{**company(3), 'key': 'c' * 64, 'at': ago(3)}, {**company(3), 'key': 'd' * 64, 'at': ago(2)}]}
        second = {'touched': [{**company(2), 'count': 1, 'last': ago(4)}], 'replied': [],
                  'quiet': [{**company(7), 'last': ago(40)}], 'unanswered': [{**company(5), 'key': 'e' * 64, 'at': ago(4)}],
                  'meetings': [{**company(6), 'day': (today + dt.timedelta(days=1)).isoformat(), 'key': 'f' * 64}]}
        view = fleet.assemble_brief(own, [(team[0], fleet.clean_brief(first)), (team[1], fleet.clean_brief(second))])
        view.update(period=today.isoformat(), every='day', since=since, fleet=ref, fleet_name=fixture['network']['work']['name'], asked=2, missing=[], declined=[])
        with app.fleet.connect() as db:
            db.execute('INSERT OR REPLACE INTO fleet_briefs(fleet,period,every,view,answers,built_at) VALUES(?,?,?,?,?,?)',
                       (ref, today.isoformat(), 'day', json.dumps(view), 2, dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--state', default='busy', help='one or more of ' + ', '.join(load.STATES) + ' (comma separated)')
    parser.add_argument('--port', type=int, default=8870, help='the dashboard port; the Network uses port+1 and the app port+2')
    parser.add_argument('--dir', help='where the sandbox install goes (emptied first)')
    args = parser.parse_args()
    states = load.parse_states(args.state)
    for port in (args.port, args.port + 1, args.port + 2):
        with socket.socket() as probe:
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                raise SystemExit(f'port {port} is in use (another sandbox?); pick another with --port')
    directory = Path(args.dir or f'/tmp/machine-sandbox-{args.port}')
    config, config_path = load.load(directory, states, port=args.port + 2, network_port=args.port + 1)
    os.environ['OPENCLAW_WORKSPACE'] = str(directory / 'workspace')
    guard.install()  # from here on: nothing but 127.0.0.1, no programs
    import assistant
    sent = Sent(directory / 'sent.jsonl')
    app = assistant.App(config, config_path)
    quiet_workers(app, sent)
    seed_model(app)
    app.help_model = fake_help
    app.notes_model = fake_notes
    app.summary_model = fake_summary
    seed_transcript(app)
    seed_summaries(app)
    seed_ai(app)
    fixture = json.loads((HERE / 'fixture.json').read_text())
    net = None
    if load.groups(states):
        net = network.Network(fixture, load.groups(states), load_secret(config, 'fleet'))
        network.serve(net, args.port + 1)
    proxy(args.port, args.port + 2, config)
    if net and app.fleet:
        seed_network(app, net, fixture)
    print(f"sandbox ({','.join(sorted(states))}) on http://127.0.0.1:{args.port}  data: {directory}  sends: {directory / 'sent.jsonl'}", flush=True)
    app.serve()


def load_secret(config, name):
    return Path(config['credentials'][name]).read_text().strip()


if __name__ == '__main__':
    main()
