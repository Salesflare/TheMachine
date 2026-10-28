"""Talk live: a spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice.

The owner's OpenAI sign-in stays in OpenClaw. The Gateway makes a short-lived, single-use session for each
conversation (talk-live-run.mjs). The service keeps that session's secret and hands the browser's WebRTC offer on, so
neither the key nor the secret reaches the browser. Audio then goes directly between the browser and OpenAI.

The dashboard gives the voice model its own tools (TOOLS): two that read (this to-do, and finding other to-dos), and
`propose`, which only shows a request on screen. Nothing is sent or changed from a conversation. A proposal goes to the
to-do's chat only when the owner taps it, and what the chat drafts then waits for the owner's Approve, as always. A
spoken "yes" is never an approval.

What both sides say is kept as the to-do's chat (lines), so there is a record. A conversation ends after LIMIT_SECONDS.
"""
import json
import re
import secrets
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMIT_SECONDS = 600          # one conversation at most; the dashboard warns a minute before
WARN_SECONDS = 540
GRACE_SECONDS = 30           # lines and tool calls that arrive just after the end still count
LINE_CHARS = 4000
ROLES = ('user', 'assistant')
SESSION_PREFIX = 'agent:main:assistant-talk-'
TOOLS = [
    {'type': 'function', 'name': 'todo_details',
     'description': 'Read the to-do this conversation is about: its title, the messages in it and the current draft.',
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'find_todos',
     'description': "Find the owner's other open to-dos by words in their title.",
     'parameters': {'type': 'object', 'properties': {'words': {'type': 'string', 'description': 'A few words to look for.'}},
                    'required': ['words'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'propose',
     'description': ('Show the owner a request for The Machine to work on in this to-do, such as drafting or changing a '
                     'reply. It only appears on screen. It goes to the chat only when the owner taps it, and anything '
                     'that sends or changes something then waits for their Approve. A spoken yes does nothing.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The request, in the owner’s words and language.'}},
                    'required': ['request'], 'additionalProperties': False}},
]
# What `propose` answers the voice (in English, for the model; the owner never sees it)
PROPOSE_NOTE = 'It is on the owner\'s screen now. Only their tap sends it to the chat. A spoken yes does nothing.'
LANGUAGE_NAMES = {'de': 'German', 'en': 'English', 'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'nl': 'Dutch', 'pt-BR': 'Brazilian Portuguese'}


def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS talk_lines(id INTEGER PRIMARY KEY, suggestion_id TEXT NOT NULL, talk_id TEXT NOT NULL, '
               'role TEXT NOT NULL, text TEXT NOT NULL, at INTEGER NOT NULL)')
    db.execute('CREATE INDEX IF NOT EXISTS talk_lines_card ON talk_lines(suggestion_id, at)')


def lines(db, suggestion_id):
    """A to-do's conversations for its chat: a "Talked live" line at the start of each, then what each side said."""
    out, seen = [], set()
    for r in db.execute('SELECT talk_id,role,text,at FROM talk_lines WHERE suggestion_id=? ORDER BY at,id', (suggestion_id,)):
        if r['talk_id'] not in seen:
            seen.add(r['talk_id'])
            out.append({'kind': 'event', 'text': 'Talked live', 'mine': True, 'at': max(0, r['at'] - 1)})
        out.append({'kind': 'you' if r['role'] == 'user' else 'reply', 'text': r['text'], 'via': 'live', 'at': r['at']})
    return out


def instructions(title, language, now_text):
    lang = LANGUAGE_NAMES.get(language, 'the owner’s language')
    return '\n'.join([
        'You are The Machine, a personal assistant, talking live with your owner about one of their to-dos: "%s".' % title,
        'Keep it short and spoken: a sentence or two at a time. Speak %s unless the owner speaks another language.' % lang,
        'Call todo_details before you answer anything about this to-do, and find_todos to look up others.',
        'You can’t send, change, approve or delete anything, and nothing you say goes to anyone else.',
        'When the owner wants something done (a reply drafted or changed, a meeting, a note), call propose with their request. '
        'Then tell them to tap it on screen if they want it. Never treat a spoken yes or okay as approval: only their tap counts, '
        'and what it drafts waits for their Approve.',
        'If something isn’t in the to-do, say you don’t know rather than guess.',
        'It is now %s.' % now_text,
    ])


class Talk:
    """The live conversations this service has open (in memory only), and the Gateway helper."""

    def __init__(self, config=None, runner=subprocess.run, clock=time.monotonic):
        self.config, self.run, self.clock = config or {}, runner, clock
        self.lock, self.asking = threading.Lock(), threading.Lock()
        self.open = {}      # talk ID -> {'suggestion_id', 'started', 'secret', 'offer_url', 'offer_headers', 'voice_session_id', 'via', 'offered'}
        self.ready = None   # (good until, {'ready', 'model'}) from the Gateway's catalog

    def helper(self, request, env, timeout=40):
        try:
            result = self.run([self.config.get('_node') or 'node', str(ROOT / 'talk-live-run.mjs')], env=env, input=json.dumps(request),
                              capture_output=True, text=True, timeout=timeout)
            found = json.loads(result.stdout or 'null')
        except (OSError, ValueError, subprocess.TimeoutExpired):
            return {'error': 'unavailable', 'reason': 'timeout'}
        return found if isinstance(found, dict) else {'error': 'unavailable', 'reason': 'other'}

    def status(self, env, check=False, wait=False):
        """Whether the Gateway can open a live session with OpenAI, kept 10 minutes; None until known. Asking takes OpenClaw
        seconds, so with check a stale answer is refreshed in the background and what is known comes back at once
        (Settings and a chat never wait on it); wait=True waits for the answer."""
        with self.lock:
            kept = self.ready
        if check and (not kept or kept[0] < self.clock()):
            if wait:
                self.refresh(env)
                with self.lock:
                    kept = self.ready
            elif self.asking.acquire(blocking=False):
                threading.Thread(target=self.refresh, args=(env, True), daemon=True, name='talk-status').start()
        return kept[1] if kept else None

    def refresh(self, env, release=False):
        try:
            found = self.helper({'method': 'status'}, env)
            seen = {'ready': bool(found.get('ready')), 'model': str(found.get('model') or '')[:80]} if not found.get('error') else {'ready': False, 'model': ''}
            with self.lock:
                self.ready = (self.clock() + 600, seen)
        finally:
            if release:
                self.asking.release()

    def start(self, suggestion_id, env):
        """A new conversation about this to-do: its ID for the dashboard, never the session's secret."""
        if not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        self.sweep()
        with self.lock:
            if any(t['suggestion_id'] == suggestion_id for t in self.open.values()):
                raise ValueError('A live conversation is already open for this to-do. End it first.')
            if len(self.open) >= 2:
                raise ValueError('Two live conversations are already open. End one first.')
        made = self.helper({'method': 'start', 'session_key': SESSION_PREFIX + suggestion_id}, env)
        if made.get('error') or not made.get('secret'):
            raise ValueError('Talk live couldn’t start. Check OpenAI in OpenClaw, then try again.'
                             if made.get('reason') == 'auth' else 'Talk live couldn’t start. Try again.')
        talk_id = secrets.token_hex(8)
        with self.lock:
            self.open[talk_id] = {'suggestion_id': suggestion_id, 'started': self.clock(), 'secret': made['secret'],
                                  'offer_url': made.get('offer_url'), 'offer_headers': made.get('offer_headers') or {},
                                  'voice_session_id': made.get('voice_session_id'), 'via': made.get('via'), 'offered': False}
        return {'id': talk_id, 'via': made.get('via'), 'model': str(made.get('model') or '')[:80]}

    def get(self, talk_id, suggestion_id=None):
        with self.lock:
            found = self.open.get(str(talk_id or ''))
        if not found or (suggestion_id is not None and found['suggestion_id'] != suggestion_id):
            raise ValueError('This live conversation has ended.')
        if self.clock() - found['started'] > LIMIT_SECONDS + GRACE_SECONDS:
            raise ValueError('This live conversation has ended.')
        return found

    def offer(self, talk_id, sdp, env):
        """The browser's WebRTC offer, handed on with the session's secret (once); the answer goes back."""
        found = self.get(talk_id)
        if not isinstance(sdp, str) or not sdp.startswith('v=0') or len(sdp) > 262144:
            raise ValueError('Talk live couldn’t connect. Try again.')
        with self.lock:
            if found['offered']:
                raise ValueError('Talk live couldn’t connect. Try again.')
            found['offered'] = True
        got = self.helper({'method': 'offer', 'session_key': SESSION_PREFIX + found['suggestion_id'], 'sdp': sdp, 'secret': found['secret'],
                           'offer_url': found['offer_url'], 'offer_headers': found['offer_headers']}, env)
        if got.get('error') or not str(got.get('sdp') or '').startswith('v=0'):
            self.end(talk_id, env)
            raise ValueError('Talk live couldn’t connect. Try again.')
        return {'sdp': got['sdp']}

    def line(self, db, talk_id, role, text, at):
        """What one side said, kept as the to-do's chat."""
        found = self.get(talk_id)
        text = ' '.join(str(text or '').split())[:LINE_CHARS]
        if role not in ROLES or not text:
            raise ValueError('Nothing to keep')
        db.execute('INSERT INTO talk_lines(suggestion_id,talk_id,role,text,at) VALUES(?,?,?,?,?)', (found['suggestion_id'], talk_id, role, text, at))
        return {'ok': True}

    def end(self, talk_id, env):
        with self.lock:
            found = self.open.pop(str(talk_id or ''), None)
        if found:
            self.helper({'method': 'end', 'session_key': SESSION_PREFIX + found['suggestion_id'],
                         'voice_session_id': found.get('voice_session_id')}, env, timeout=25)
        return {'ok': True}

    def sweep(self):
        """Conversations past their limit are forgotten (their secret with them)."""
        with self.lock:
            for talk_id in [k for k, v in self.open.items() if self.clock() - v['started'] > LIMIT_SECONDS + GRACE_SECONDS]:
                self.open.pop(talk_id, None)
