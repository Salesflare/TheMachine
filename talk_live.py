"""Talk live: a spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice.

The owner's OpenAI sign-in stays in OpenClaw. The Gateway makes a short-lived, single-use session for each
conversation (talk-live-run.mjs). The service keeps that session's secret and hands the browser's WebRTC offer on, so
neither the key nor the secret reaches the browser. Audio then goes directly between the browser and OpenAI.

The dashboard gives the voice model its own tools (TOOLS): two that read (this to-do, and finding other to-dos),
`ask_chat`, which hands a request to the to-do's chat as if the owner had typed it, so it follows the chat's rules (it
can change the draft, snooze or mark done, never send), and two for approving a send by voice.

A spoken yes approves exactly one draft, and only when the owner has seen or heard it: the draft is on screen in this
to-do's chat (on a phone or with the screen off, the voice reads it out in full first), the voice has just asked a
confirm question naming who it goes to and how (`ask_to_send`), and the owner's next utterance clearly means yes. The
Machine judges that answer itself (judge_answer: a model turn with a strict schema; anything else counts as unclear),
from its own record of what was said, never from the voice's word. If the draft changed after the question, it asks
again. The yes goes the normal confirm_action way with source 'voice' and waits UNDO_SECONDS, so the chat can show
"Approved by voice" with Undo; pacing and the outbox's checks apply as for a tap. "Send without asking" is not touched.

What both sides say is kept as the to-do's chat (lines), so there is a record. A conversation ends after LIMIT_SECONDS.
"""
import hashlib
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
UNDO_SECONDS = 10            # a send approved by voice waits this long, with Undo in the chat
ASK_SECONDS = 180            # a confirm question older than this needs asking again
SEND_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'intercom', 'doc_reply')
CHANNELS = {'email': 'by email', 'linkedin': 'on LinkedIn', 'slack': 'on Slack', 'x': 'on X', 'whatsapp': 'on WhatsApp',
            'telegram': 'on Telegram', 'intercom': 'in Intercom', 'doc_reply': 'as a comment in the doc'}
TOOLS = [
    {'type': 'function', 'name': 'todo_details',
     'description': 'Read the to-do this conversation is about: its title, the messages in it and the current draft.',
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'find_todos',
     'description': "Find the owner's other open to-dos by words in their title.",
     'parameters': {'type': 'object', 'properties': {'words': {'type': 'string', 'description': 'A few words to look for.'}},
                    'required': ['words'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_chat',
     'description': ('Hand the owner’s request to this to-do’s chat, as if they had typed it: draft or change a reply, '
                     'snooze it, mark it done, look something up on the web. The chat follows its usual rules: it never sends. '
                     'Anything that goes to someone waits for the owner’s Approve on screen, and a spoken yes is not one.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The request, in the owner’s words and language.'}},
                    'required': ['request'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_to_send',
     'description': ('When the owner wants to send the draft that is on screen. Returns the confirm question for that one '
                     'draft. If read_aloud is true, read the draft out in full first. Then ask the question, in the owner’s '
                     'language, and stop to hear their answer.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'send_answer',
     'description': ('Call right after the owner answers your confirm question from ask_to_send. The Machine judges their '
                     'answer itself and says what happened; tell the owner that, and never say something was sent otherwise.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
]
# What the tools answer the voice (in English, for the model; the owner never sees these)
ASK_NOTE = ('The chat is on it. Say one short line, like "Looking that up", and go on with the conversation; don’t check '
            'on it or say you will. When the chat is done, its answer comes to you as a message. Nothing goes to anyone '
            'until the owner approves a draft they have seen: a tap on Approve, or a clear yes to your confirm question '
            '(ask_to_send).')
QUEUED_NOTE = 'The chat is still on the last request; this one joins it. Its answer comes to you as a message.'
# The chat's answer, pushed into the conversation when its turn ends (the dashboard sends it as a message)
DONE_NOTE = ('The chat finished what you asked. Its answer: "{answer}" Tell the owner now, in a sentence or two in '
             'their language, with where it came from if it says. Don’t read out links.')
STOPPED_NOTE = 'The chat stopped before it answered. Tell the owner, and offer to ask again.'
# A request Talk live hands to the chat: a decision id with this prefix (still a chat- turn), never shown as the
# owner's message (their own words are the talk lines), with this note in the chat's prompt
RELAY_PREFIX = 'chat-talk-'
RELAY_NOTE = ('This request came from the owner by voice, through Talk live, and the voice is waiting to tell them your '
              'answer. Do it now. When it needs facts from outside their messages (opening hours, an address, a price, '
              'a phone number), look them up on the web or in the browser instead of saying you can’t. Then reply in '
              'two or three plain sentences that read well aloud, and name where you found it (the site), without links '
              'or lists.')
SAY = {
    'ask': 'Ask exactly this, in the owner’s language, then stop and listen: ',
    'read': 'First read the draft below out in full, word for word. ',
    'queued': ('Approved. It goes out in %d seconds unless the owner taps Undo in the chat. Say it’s on its way.' % UNDO_SECONDS),
    'no': 'Not sent. Say so, and ask what they’d like instead.',
    'unclear': 'That wasn’t a clear yes, so nothing was sent. Call ask_to_send again and ask once more.',
    'changed': 'The draft changed after you asked, so nothing was sent. Call ask_to_send again to ask about the new draft.',
    'not_asked': 'No confirm question is open, so nothing was sent. Call ask_to_send first and ask its question.',
    'no_answer': 'No answer heard yet, so nothing was sent. Wait for the owner to answer.',
}
JUDGE = ('Someone was just asked aloud: "{question}"\n'
         'Their spoken answer, as transcribed: "{answer}"\n'
         'Does the answer clearly mean yes, send it now? Judge the meaning, in any language. A hesitant, conditional or '
         'partial answer, a question, a change request, or anything unrelated is "unclear". A refusal or "wait" is "no".\n'
         'Reply with only this JSON and nothing else: {{"approve": "yes"}} or {{"approve": "no"}} or {{"approve": "unclear"}}')
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
        'You can’t change or delete anything yourself, and nothing you say goes to anyone else.',
        'When the owner wants something done in this to-do (a reply drafted or changed, snoozed, marked done) or looked '
        'up (opening hours, an address, anything on the web), call ask_chat with their request. Say one short line, like '
        '"Looking that up", then keep talking about anything else; never poll or say you will check. The chat’s answer '
        'comes to you as a message when it is done: tell the owner then.',
        'To send: only when the owner asks to send the draft on screen, call ask_to_send and ask its question, reading the '
        'draft out first when it says so. After their answer, call send_answer and say what it returns. One draft per '
        'question; never send several at once, and never say something was sent unless send_answer says so.',
        'If something isn’t in the to-do, ask the chat to look it up rather than guess.',
        'It is now %s.' % now_text,
    ])


def digest(action):
    """What a confirm question was about: who, how and what. Any change after the question means asking again."""
    keep = {k: action.get(k) for k in ('kind', 'to', 'cc', 'bcc', 'from', 'subject', 'body', 'message', 'thread_id', 'channel')}
    return hashlib.sha256(json.dumps(keep, sort_keys=True, default=str).encode()).hexdigest()


def question(action, name):
    """The confirm question for one draft, naming who it goes to and how."""
    what = 'reply' if action.get('reply') or str(action.get('subject') or '').lower().startswith('re:') else 'message'
    if action.get('kind') == 'doc_reply':
        return 'Post this reply as a comment in the doc?'
    return 'Send this %s to %s %s?' % (what, name, CHANNELS.get(action.get('kind'), ''))


def judge_answer(answer, asked, run):
    """'yes', 'no' or 'unclear' for the owner's spoken answer to a confirm question: a model turn (run(prompt) -> text)
    that must answer with exactly one of three JSON objects. Anything else, or no answer, is 'unclear'."""
    try:
        out = str(run(JUDGE.format(question=asked.replace('"', "'"), answer=str(answer).replace('"', "'"))) or '')
        found = re.fullmatch(r'\s*(?:```(?:json)?\s*)?(\{[^{}]*\})\s*(?:```)?\s*', out)
        data = json.loads(found.group(1)) if found else None
    except Exception:  # the model could not be reached: not a yes
        return 'unclear'
    if isinstance(data, dict) and set(data) == {'approve'} and data['approve'] in ('yes', 'no', 'unclear'):
        return data['approve']
    return 'unclear'


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

    def start(self, suggestion_id, env, voice='cedar'):
        """A new conversation about this to-do: its ID for the dashboard, never the session's secret."""
        if not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        self.sweep()
        with self.lock:
            if any(t['suggestion_id'] == suggestion_id for t in self.open.values()):
                raise ValueError('A live conversation is already open for this to-do. End it first.')
            if len(self.open) >= 2:
                raise ValueError('Two live conversations are already open. End one first.')
        made = self.helper({'method': 'start', 'session_key': SESSION_PREFIX + suggestion_id, 'voice': voice}, env)
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

    def ask(self, talk_id, suggestion_id, revision, action, name, at):
        """The voice is about to ask to send this draft: the question, kept until the owner's next answer."""
        found = self.get(talk_id, suggestion_id)
        asked = question(action, name)
        with self.lock:
            found['confirm'] = {'revision': revision, 'digest': digest(action), 'at': at, 'question': asked, 'name': name.split(' and ')[0]}
        return asked

    def answer(self, db, talk_id, at, current, judge):
        """The owner's answer to the open confirm question, from what this conversation recorded (talk_lines): the
        voice's question, then the owner's next utterance. current(revision) is that draft as it is now, or None.
        Returns (status, confirm): 'yes' with the question it approves, or why not."""
        found = self.get(talk_id)
        with self.lock:
            c = found.get('confirm')
        if not c:
            return 'not_asked', None
        if at - c['at'] > ASK_SECONDS * 1000:
            found.pop('confirm', None)
            return 'unclear', None
        said = db.execute('SELECT role,text FROM talk_lines WHERE talk_id=? AND at>=? ORDER BY at,id', (talk_id, c['at'])).fetchall()
        spoke = next((n for n, r in enumerate(said) if r['role'] == 'assistant'), None)
        if spoke is None:
            return 'not_asked', None   # the voice hasn't asked yet: the question stays open
        first = next((n for n in range(spoke, len(said)) if said[n]['role'] == 'user'), None)
        voice = ' '.join(r['text'] for r in said[spoke:first] if r['role'] == 'assistant')
        if not voice:
            return 'not_asked', None   # the voice hasn't asked yet: the question stays open
        if first is None:
            return 'no_answer', None
        found.pop('confirm', None)     # one answer per question, whatever it was
        if c['name'] and '@' not in c['name'] and c['name'] != 'them' and c['name'].lower() not in voice.lower():
            return 'unclear', None     # the question it spoke didn't say who it goes to
        now = current(c['revision'])
        if not now or digest(now) != c['digest']:
            return 'changed', None
        return judge(said[first]['text'], c['question']), c

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
