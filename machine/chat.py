"""A to-do's chat as the dashboard shows it: the owner's and the agent's turns (chat_items), their text, the names in
them, the hand-offs and drafts it mentions, and what a run's transcript says. Moved out of assistant.py as is."""
import datetime as dt
import json
from pathlib import Path
import re
import urllib.parse

import i18n
from machine.cards import CHAT_HANDLE, chat_plain_name
from machine.text import _address, clamp, split_quoted_history
import next_actions
from timeutil import local_tz, now


# A card's chat (dashboard #chat=<id>): the card's own preparation session, read with chat.history through
# chat-history-run.mjs, shown as a conversation. The owner's side comes from this app's decisions, never from the long
# service prompts in the transcript; the agent's side is its replies and its steps, in the owner's words.
CHAT_HISTORY_LIMIT = 200


CHAT_FILES_ONLY = ('Take a look at the attached file.', 'Take a look at the attached files.')


CHAT_OWNER_WORDS = {'accept': 'Do it', 'retry': 'Try again', 'complete': 'Marked done', 'reject': 'Not needed', 'not_done': 'Not done yet',
                    'snooze': 'Snoozed', 'reopen': 'Reopened', 'undo': 'Reopened', 'rename': 'Renamed',
                    'rename_reset': 'Back to the suggested title', 'merge': 'Merged into the other to-do', 'keep_both': 'Kept both to-dos'}


# A tap that the next one takes back within a minute (done then reopened, snoozed then unsnoozed), or that Undo took
# back, is left out, both.
CHAT_UNDONE = {('complete', 'reopen'), ('reject', 'reopen'), ('snooze', 'unsnooze')}


# A conversation event's parts, one per line: "<unix time> · <author> · <part kind>: <text>"
CHAT_PART = re.compile(r'^(\d{9,11}) · ([^·\n]{1,120}) · ([\w.-]{1,60}):[ \t]?(.*)$', re.M)


CHAT_AGENTS = {'claude': 'Claude Code', 'codex': 'Codex'}


CHAT_SENT = {'email': 'email', 'email_demo': 'email', 'linkedin': 'message', 'slack': 'message', 'x': 'post', 'whatsapp': 'message', 'telegram': 'message', 'intercom': 'reply', 'doc_reply': 'reply'}


CHAT_SECRETS = (
    (re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z0-9 ]*PRIVATE KEY-----'), '[redacted private key]'),
    (re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'), '[redacted token]'),
    (re.compile(r'\b(?:xox[abcdeoprs]|xapp)-[A-Za-z0-9-]{10,}|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|glpat-[A-Za-z0-9_-]{20,})'), '[redacted token]'),
    (re.compile(r'\bsk-(?:ant-|proj-|svcacct-)?[A-Za-z0-9_-]{20,}|\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}|\bya29\.[A-Za-z0-9_-]{20,}|\bAKIA[0-9A-Z]{16}\b'), '[redacted token]'),
    (re.compile(r'bot\d+:[A-Za-z0-9_-]{20,}|\b\d{8,10}:AA[A-Za-z0-9_-]{30,}'), '[redacted token]'),
    (re.compile(r'(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{16,}'), r'\1 [redacted]'),
    (re.compile(r'(?i)\b(password|passwd|passphrase|client[_-]?secret|api[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token)(["\']?\s*[:=]\s*["\']?)(?!\[redacted)[^\s"\'`,;&<>]{6,}'), r'\1\2[redacted]'),
)


CHAT_PATHS = re.compile(r'(?:~|/home|/tmp|/var|/Users|/root|/opt)/[^\s,;:)"\'”]+')


CHAT_IDS = re.compile(r'\b(?=[A-Za-z0-9_-]*\d)[A-Za-z0-9_-]{20,}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b')


def chat_text(text, step=False, chars=4000):
    """What the chat may show of the agent's words: no secrets and no local paths; a step line also without long IDs
    (the card's Technical details rule). Replies keep their links."""
    text = str(text or '')
    for shape, replacement in CHAT_SECRETS:
        text = shape.sub(replacement, text)
    text = CHAT_PATHS.sub('…', text)
    if step:
        text = CHAT_IDS.sub('…', ' '.join(text.split()))
    return text.strip()[:chars]


# The agent's own bookkeeping, never shown in the chat: a learned or saved skill or memory line ("💾 Learned: updated
# `some-skill` (…). Say "undo" to revert this skill change."). The chat only says it was noted.
CHAT_LEARNED = re.compile(r'^\W*(?:learned|learnt|remembered|saved to memory|memory updated|skill (?:updated|saved|created))\b|\bskill change\b', re.I)


CHAT_MARKER = re.compile(r'^[^\w\s"\'“‘(\[*_#>`~-]+\s*', re.M)  # an emoji or symbol a line starts with


def chat_reply(text):
    """(text, noted) of one reply: its learning lines left out (noted says there were some), no emoji markers at the
    start of lines and no code ticks around names."""
    kept, noted = [], False
    for part in re.split(r'\n\s*\n', str(text or '')):
        if CHAT_LEARNED.search(part.strip()):
            noted = True
            continue
        kept.append(CHAT_MARKER.sub('', part.replace('`', '')))
    return '\n\n'.join(p for p in kept if p.strip()).strip(), noted


# A link in a saved result to one of its files ("[Draft and sources](memory/assistant/x.md)"): the chat shows it as a
# chip that opens the file, never as a bare title.
CHAT_RESULT_LINK = re.compile(r'\[([^\]\n]{1,200})\]\((?:[^)\s]*/)?(memory/assistant/[^)\s]{1,300})\)')


def chat_result_files(body):
    """(body without its result-file links, [{'label', 'path'}]) of a saved result; a line left with only the link goes."""
    files, body = [], str(body or '')
    for m in CHAT_RESULT_LINK.finditer(body):
        path = m[2]
        if '..' in path.split('/') or not re.fullmatch(r'memory/assistant/[\w.\-/ ]{1,300}', path):
            continue
        if all(f['path'] != path for f in files):
            files.append({'label': clamp(m[1].strip() or path.rsplit('/', 1)[-1], 200), 'path': path})
    lines = []
    for line in body.split('\n'):
        kept = re.sub(r'(?<=\S)  +', ' ', CHAT_RESULT_LINK.sub('', line))
        if kept != line and re.fullmatch(r'[\s·•|,;:()\-–—]*', kept):
            continue
        lines.append(kept.rstrip())
    return '\n'.join(lines), files[:6]


# How a step without a draft went, after its label ("Merge fix: didn’t work"); done or sent says nothing more
CHAT_STEP_HOW = {'queued': '…', 'sending': '…', 'blocked': ': didn’t work', 'failed': ': didn’t work', 'cancelled': ': canceled',
                 'uncertain': ': not sure it went through', 'finish_uncertain': ': not sure it finished', 'undoing': ': undoing…', 'undone': ': undone'}


CHAT_STEP_FAILED = {'blocked', 'failed', 'uncertain', 'finish_uncertain'}


def handoff_machine(name):
    """"Pat’s Machine" for a teammate named Pat Lee; "a teammate’s Machine" without a name."""
    first = (str(name or '').split() or [''])[0]
    return f'{first}’s Machine' if first and name != 'A teammate' else 'a teammate’s Machine'


def card_chat_handoffs(db, suggestion_id):
    """A card's handoffs to a teammate's Machine, for its chat: when it went, and what came back (accepted, declined,
    done) once it did. A handoff that didn't go out says so, with Try again. A teammate's note is their words, as data.
    A silent acceptance ("Pat is on it") has its own line from the card's decisions."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='fleet_out'").fetchone():
        return []  # no Fleet on this Machine yet
    out = []
    meta = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='fleet_meta'").fetchone()
    for r in db.execute("SELECT id,name,status,answer,at,answered_at FROM fleet_out WHERE kind='handoff' AND context=? ORDER BY at",
                        ('handoff:' + str(suggestion_id),)):
        first = (str(r['name'] or '').split() or ['Your teammate'])[0]
        out.append({'kind': 'event', 'text': 'Handed off to ' + handoff_machine(r['name']), 'mine': True, 'handoff': True, 'at': chat_ms(r['at'])})
        taken = db.execute('SELECT value FROM fleet_meta WHERE key=?', ('handoff_withdrawn:' + str(r['id']),)).fetchone() if meta else None
        try:
            taken = json.loads(taken[0]) if taken else None
        except ValueError:
            taken = {}
        if taken is not None:  # handed to someone else instead: said once, when that one went
            out.append({'kind': 'event', 'text': 'Taken back from ' + first, 'mine': True, 'handoff': True,
                        'at': chat_ms((taken if isinstance(taken, dict) else {}).get('at') or r['at'])})
        try:
            answer = json.loads(r['answer'] or 'null') or {}
        except ValueError:
            answer = {}
        answer = answer if isinstance(answer, dict) else {}
        stage = answer.get('stage') or r['status']
        if answer.get('silent') or stage in ('asked', 'waiting'):
            continue
        note = clamp(' '.join(str(answer.get('note') or '').split()), 300)
        said = {'accepted': f'{first} accepted it', 'adjusted': f'{first} accepted it with a change',
                'done': f'{first} marked it done', 'declined': f'{first} declined it', 'expired': f'{first} didn’t answer in time'}.get(stage)
        if not said:
            continue
        said += f'. Their note: “{note}”' if note else ''
        out.append({'kind': 'event', 'text': said, 'handoff': True, 'at': chat_ms(r['answered_at'] or r['at'])})
    failed = db.execute("SELECT value FROM fleet_meta WHERE key=?", ('handoff_failed:' + str(suggestion_id),)).fetchone() if meta else None
    try:
        failed = json.loads(failed[0]) if failed else None
    except ValueError:
        failed = None
    if isinstance(failed, dict):
        out.append({'kind': 'event', 'text': 'Handoff didn’t go out to ' + handoff_machine(failed.get('name')), 'handoff': True,
                    'retry_handoff': str(suggestion_id), 'at': chat_ms(failed.get('at'))})
    return out


def chat_draft(action):
    """A draft in a saved result, for the chat: what goes out and to whom (no account or thread handles)."""
    if not isinstance(action, dict) or action.get('kind') not in CHAT_SENT or not isinstance(action.get('body'), str):
        return None
    to = action.get('to')
    to = [str(t) for t in to] if isinstance(to, list) else [str(to)] if to else []
    if not to and (action.get('to_name') or action.get('to_email')):  # a chat send names its person apart from the channel
        to = [str(action.get('to_name') or action.get('to_email'))]
    to = [chat_plain_name(t) for t in to if not CHAT_HANDLE.fullmatch(t.strip())]
    return {'kind': action['kind'], 'to': [clamp(t, 200) for t in to[:10]], 'subject': clamp(str(action.get('subject') or ''), 300),
            'body': chat_text(action['body'], chars=8000), 'reply': bool(action.get('in_reply_to') or action.get('thread_id'))}


def chat_excerpt(body, subject=''):
    """The new part of a message: its quoted history and signature left out, the first lines kept."""
    text = split_quoted_history(str(body or ''), subject)[0]
    lines = [line.rstrip() for line in text.replace('\r', '').split('\n') if not line.lstrip().startswith('>')]
    text = re.split(r'\n-- ?\n', '\n'.join(lines))[0]
    return chat_text(re.sub(r'\n{3,}', '\n\n', text).strip(), chars=1500)


def chat_person(name):
    """A display name as people say it: "Lee, Sam" is Sam Lee."""
    name = str(name or '').strip(' "\'')
    match = re.fullmatch(r'([^,@]{1,60}),\s*([^,@]{1,60})', name)
    return f'{match[2].strip()} {match[1].strip()}' if match else name


CHAT_ON = {'slack': ' on Slack', 'whatsapp': ' on WhatsApp', 'telegram': ' on Telegram', 'linkedin': ' on LinkedIn', 'x': ' on X', 'intercom': ' in Intercom', 'doc_reply': ' in the doc'}


def chat_name(address, names, fallback=''):
    """Who a draft goes to, by first name when a source message names them; a chat handle that is no email address
    (a WhatsApp or Slack ID) is the person the card is about (`fallback`)."""
    found = names.get(_address(address))
    if found:
        return found.split()[0]
    if CHAT_HANDLE.fullmatch(str(address).strip()):
        return (fallback.split() or ['them'])[0]
    if not _address(address) or '@' not in str(address):
        return chat_plain_name(str(address)).split()[0] if str(address).strip() else (fallback.split() or ['them'])[0]
    email = re.fullmatch(r'[^\s@<>]+@[\w.-]+\.[a-z]{2,}', _address(address) or '') and not re.search(r'@(s\.whatsapp\.net|g\.us|lid)$', _address(address))
    return _address(address) if email else (fallback.split() or [_address(address) or str(address)])[0]


# Who wrote a conversation part when it has no name: the person on the other side (Intercom's user, lead or visitor)
CHAT_ROLES = {'user', 'lead', 'contact', 'visitor', 'customer'}


CHAT_NOTES = {'note', 'note_and_reopen'}


def chat_conversation(body, parts, title, owner_name, metadata):
    """A conversation's source for the chat, as [(who, at ms, text, is_note)]: what the other side asked (the opening
    question, then their latest messages), followed by a later internal note of whom the card names. Empty when the
    conversation has no other side, and then the part the card is about stands alone."""
    first = lambda p: p[2].split()[0].lower()
    me = str(owner_name or '').strip().lower()
    named = {first(p) for p in parts if first(p) in str(title or '').lower() and p[2].strip().lower() not in CHAT_ROLES}
    def text_of(p):
        rest = body[p.end():]
        after = CHAT_PART.search(rest)
        return chat_excerpt(p[4] + rest[:after.start() if after else None], '')
    them = [p for p in parts if p[3] not in CHAT_NOTES and p[2].strip().lower() != me and first(p) not in named
            and (p[2].strip().lower() in CHAT_ROLES or not named)]
    if not them:
        pick = ([p for p in parts if first(p) in named] or [p for p in parts if p[2].strip().lower() != me] or parts)[-1]
        return [(chat_person(pick[2]), int(pick[1]) * 1000, text_of(pick), False)]
    who = them[-1][2]
    run = []  # their latest messages in a row; a one or two word "Great!" is left out when there is more
    for p in reversed(parts):
        if p[2] == who and p[3] not in CHAT_NOTES:
            run.insert(0, p)
        elif run and (p[2] != who and p[3] not in ('assignment', 'snoozed', 'open', 'close') or p[4].strip()):
            break
    said = [p for p in run if len(re.findall(r'\w+', p[4])) > 2] or run
    name = 'Contact' if who.strip().lower() in CHAT_ROLES else chat_person(who)
    out = []
    opening = chat_excerpt(body[:CHAT_PART.search(body).start()], '')
    if opening and (who.strip().lower() in CHAT_ROLES or not named):
        start = metadata.get('created_at') if isinstance(metadata.get('created_at'), int) else int(parts[0][1]) - 1
        out.append((name, start * 1000, opening, False))
    out.append((name, int(said[-1][1]) * 1000, chat_text('\n'.join(text_of(p) for p in said), chars=1500), False))
    note = [p for p in parts if first(p) in named and p[3] in CHAT_NOTES and int(p[1]) >= int(run[-1][1])]
    if note:
        out.append((chat_person(note[-1][2]), int(note[-1][1]) * 1000, text_of(note[-1]), True))
    return out


# A coding agent's housekeeping, which the chat leaves out: the files it saved (they show as chips) and what it did not send
CHAT_SAVED = re.compile(r'\b(?:wrote|written|saved|created|edited|updated|made|put|left|added)\b', re.I)


CHAT_NOT_SENT = re.compile(r'^(?:and\s+)?(?:nothing|no\s+\w+)(?:\s+else)?(?:\s+(?:was|has been|is))?\s+(?:\w+,?\s+){0,3}?(?:sent|posted|published|submitted|changed)\b[^.!?]*[.!?]?$', re.I)


def chat_agent_text(summary, files, full=False):
    """(text, nothing_sent) of a coding agent's result for the chat: what it found first, without the sentences (or
    clauses) about the files it saved (shown as chips) or about what it did not send (a quiet line says so). With
    `full`, also the whole answer when something was left out (the bubble's More shows it), else ''."""
    text = chat_reply(re.sub(r'\[([^\]\n]{1,200})\]\((?!https?:)[^)\s]{1,500}\)', r'\1', chat_text(summary, chars=4000)))[0]
    names = {Path(f).name.lower() for f in files} | {'this folder', 'the folder', 'your folder'}
    quiet, dropped, kept = False, False, []
    for line in text.split('\n'):
        pieces = re.split(r'((?<=[.!?])\s+|;\s+)', line)  # sentences and clauses, each with what came after it
        out = []
        for part, after in zip(pieces[::2], pieces[1::2] + ['']):
            bare = part.strip()
            if CHAT_NOT_SENT.match(bare):
                quiet = True
            elif not (CHAT_SAVED.search(bare) and any(n in bare.lower() for n in names) and len(bare) < 200):
                out.append((part, after))
                continue
            dropped = True
        if len(out) == len(pieces[::2]):
            kept.append(line)
        elif out:  # a clause left alone ends as a sentence
            kept.append(' '.join(p.strip() + ('.' if a.startswith(';') and not re.search(r'[.!?:]$', p.strip()) else '') for p, a in out))
    clean = re.sub(r'\n{3,}', '\n\n', '\n'.join(kept)).strip()
    if not full:
        return (clean or text), quiet
    return (clean or text), quiet, (text if dropped and clean and clean != text else '')


def chat_ms(value):
    try:
        return int(dt.datetime.fromisoformat(str(value)).timestamp() * 1000)
    except ValueError:
        return 0


def chat_text_phase(part):
    """'commentary' or 'final_answer' of a text block that says which (an OpenAI Responses run's textSignature), else ''."""
    signature = part.get('textSignature')
    if not isinstance(signature, str) or not signature.startswith('{'):
        return ''
    try:
        phase = json.loads(signature).get('phase')
    except (ValueError, AttributeError):
        return ''
    return phase if phase in ('commentary', 'final_answer') else ''


# A run's steps in its chat, said as done, in plain words, one line per kind with how many times ("Used the browser on
# example.com · 11"): the tool, the site a browser or web page step was on (its host name only, never the address,
# its path or its query) and what its lookups in The Machine looked up. Never a command, its arguments, search words
# or a file. Each line is a catalog sentence with its slot, so the dashboard says it in the owner's language. A step
# with nothing specific to say (a tool not named here) counts, but has no row.
CHAT_STEP_LINES = {'exec': 'Ran a command', 'browser': 'Used the browser', 'read': 'Read a file', 'write': 'Wrote notes',
                   'edit': 'Wrote notes', 'web_search': 'Searched the web', 'web_fetch': 'Read a web page',
                   'assistant_signals': 'Looked things up in The Machine', 'memory_search': 'Searched memory'}
CHAT_STEP_SITES = {'browser': 'Used the browser on {}', 'web_fetch': 'Read a page on {}'}
CHAT_STEP_ACTIONS = {'events': 'Searched messages', 'graph': 'Looked up people', 'status': 'Checked open to-dos',
                     'preparation_history': 'Read earlier work on this to-do', 'related': 'Looked for related to-dos',
                     'promise': 'Noted a promise', 'remember_fact': 'Remembered something about you',
                     'prepare': 'Saved its work on this to-do'}
CHAT_STEP_GROUPS = 20  # lines a run's steps fold into at most (the most frequent); its count still says them all


def chat_step_site(arguments):
    """The site a step opened, as its bare host name (www. left off), or '' when it has none worth showing: not a web
    address, a local or numeric host, or a host that is an ID."""
    found = arguments.get('url') or arguments.get('targetUrl')
    if not isinstance(found, str):
        return ''
    try:
        parts = urllib.parse.urlsplit(found.strip())
        host = (parts.hostname or '').lower()
    except ValueError:
        return ''
    if (parts.scheme not in ('http', 'https') or '.' not in host or not re.fullmatch(r'[a-z0-9.-]{1,60}', host)
            or re.fullmatch(r'[\d.]+', host) or host.endswith(('.local', '.internal', '.localhost')) or CHAT_IDS.search(host)):
        return ''
    return host.removeprefix('www.')


def chat_step(name, arguments, sites):
    """One step as the chat says it: the agent's own title for it (redacted), else its line ({'line': [sentence,
    slot]}), or None when there is nothing specific to say. A browser step without an address is on the site its tab (or the last tab) was last opened on (`sites`)."""
    title = arguments.get('title') if isinstance(arguments.get('title'), str) else ''
    title = chat_text(title, step=True, chars=120)
    if title:
        return {'text': title}
    site = chat_step_site(arguments) if name in CHAT_STEP_SITES else ''
    if name == 'browser':
        tab = arguments.get('targetId') or arguments.get('label')
        tab = tab if isinstance(tab, str) else ''
        if arguments.get('url') or arguments.get('targetUrl'):  # opened somewhere, shown or not: later steps are there
            sites[tab] = sites[''] = site
        else:
            site = sites.get(tab, '') if tab else sites.get('', '')
    if site:
        return {'line': [CHAT_STEP_SITES[name], site]}
    action = arguments.get('action') if name == 'assistant_signals' else None
    if isinstance(action, str) and action in CHAT_STEP_ACTIONS:
        return {'line': [CHAT_STEP_ACTIONS[action]]}
    return {'line': [CHAT_STEP_LINES[name]]} if name in CHAT_STEP_LINES else None


def chat_steps_item(run):
    """A run's steps item: each kind of step once, in the order it first came, with how many times (n), the most
    frequent CHAT_STEP_GROUPS of them, and how many steps it took in all (count)."""
    groups = run['steps']
    if len(groups) > CHAT_STEP_GROUPS:
        kept = set(map(id, sorted(groups, key=lambda g: -g['n'])[:CHAT_STEP_GROUPS]))
        groups = [g for g in groups if id(g) in kept]
    return {'kind': 'steps', 'count': run['step_count'], 'steps': [dict(g) for g in groups]}


def chat_run_keys(messages):
    """The run each message belongs to. A CLI agent's own turns (Claude Code), which OpenClaw imports into the session
    without a run ID, belong to the run whose record follows them, up to the prompt that started it."""
    keys, carry = [], ''
    for message in reversed(messages):
        meta = message.get('__openclaw') if isinstance(message.get('__openclaw'), dict) else {}
        if meta.get('runId'):
            carry = str(meta['runId'])
        elif message.get('role') == 'user':
            carry = ''
        keys.append(str(meta.get('runId') or (carry if meta.get('importedFrom') else '')))
    return keys[::-1]


def chat_cli_replies(run):
    """A CLI run's reply: its last turn's text, else OpenClaw's record of the run (all its text joined) without the
    working notes. Never the notes, and never both, which showed the reply twice."""
    found = run['finals']
    if not found:
        found = []
        for reply in run['texts']:
            text = reply['text']
            for note, _ in run['notes']:
                note = chat_reply(chat_text(note))[0]
                if note:
                    text = text.replace(note, '', 1)
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            if text:
                found.append({**reply, 'text': text})
        return found
    texts = []
    for raw, at in found:
        text, noted = chat_reply(chat_text(raw))
        run['noted'] = run['noted'] or noted
        if not text:
            continue
        if texts and texts[-1]['at'] >= at - 60000:
            texts[-1]['text'] = (texts[-1]['text'] + '\n\n' + text)[:8000]
        else:
            texts.append({'kind': 'reply', 'text': text, 'at': at})
    return texts


def asked_item(questions, at):
    """The line for what the to-do asked, just before the owner's answer to it: "Asked: Should I …?". Small, as the
    other event lines; the owner's own message then shows only their answer."""
    return {'kind': 'event', 'text': i18n.t('Asked: {}', clamp(' '.join(' '.join(str(q).split()) for q in questions), 400)),
            'asked': True, 'at': max(0, at - 1)}


def chat_unglued(text, questions):
    """An answer saved before the question was kept beside it (decision_asks): a quick pick wrote each answer line as
    the question, then the pick ("Should I …? October invoices now"). Only a line that starts with one of the run's
    own questions exactly, as that pick wrote it, comes apart: (the answer alone, [the questions]); else (text, [])."""
    heads = [q if q.endswith(('.', '?', '!', '…')) else q + '.' for q in (str(q).strip() for q in questions) if q]
    kept, asked = [], []
    for line in str(text or '').split('\n'):
        head = next((h for h in heads if line.startswith(h + ' ') and line[len(h) + 1:].strip()), None)
        if head and head not in asked:
            asked.append(head)
        kept.append(line[len(head) + 1:].strip() if head else line)
    return ('\n'.join(kept), asked) if asked else (text, [])


def chat_items(messages, owner, results=None):
    """The conversation, strictly by time: the owner's own notes and taps and the card's source messages (`owner`,
    from the service), each run's saved results (`results`, by job ID, from the service: what it said and the drafts
    it left) and, from the run's own session, the steps it took before them. A run's free text shows only when it
    saved no result. User rows in the transcript are the service's prompts and are never shown; tool results,
    thinking and nested tool rows neither; learning lines only as a "noted" mark on that run's reply. Progress notes
    (commentary, a CLI agent's text before a tool call, the Gateway's copies of them) never show; a CLI run's reply
    shows once (chat_cli_replies)."""
    results = results or {}
    items = [dict(o) for o in owner]
    runs, order = {}, []
    number = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
    messages = [m for m in messages if isinstance(m, dict)] if isinstance(messages, list) else []
    keys = chat_run_keys(messages)
    for message, key in zip(messages, keys):
        if message.get('role') != 'assistant' or not isinstance(message.get('content'), list):
            continue
        if isinstance(message.get('openclawStreamFallback'), dict):  # the Gateway's copy of a run's progress notes
            continue
        meta = message.get('__openclaw') if isinstance(message.get('__openclaw'), dict) else {}
        at = next((v for v in (message.get('timestamp'), meta.get('recordTimestampMs')) if number(v)), 0)
        if key not in runs:
            runs[key] = {'steps': [], 'step_keys': {}, 'step_count': 0, 'sites': {}, 'at': at, 'texts': [], 'noted': False,
                         'notes': [], 'finals': []}
            order.append(key)
        run = runs[key]
        imported = bool(meta.get('importedFrom'))
        for part in message['content']:
            if not isinstance(part, dict):
                continue
            if imported and part.get('type') == 'text':
                # A CLI agent's own turn (Claude Code): text before a tool call is a working note, never the reply; its
                # last turn's text is the reply, which OpenClaw's own record of the run repeats after all the notes.
                if str(part.get('text') or '').strip():
                    (run['notes'] if message.get('stopReason') == 'tool_use' else run['finals']).append((str(part['text']), at))
                continue
            if part.get('type') == 'text' and chat_text_phase(part) == 'commentary':
                continue
            if part.get('type') == 'toolCall':
                arguments = part.get('arguments') if isinstance(part.get('arguments'), dict) else {}
                step = chat_step(part.get('name'), arguments, run['sites'])
                run['step_count'] += 1
                if step is not None:
                    found = run['step_keys'].get(json.dumps(step))
                    if found is None:
                        found = run['step_keys'][json.dumps(step)] = {**step, 'n': 0}
                        run['steps'].append(found)
                    found['n'] += 1
                run['at'] = run['at'] or at
            elif part.get('type') == 'text' and str(part.get('text') or '').strip():
                text, noted = chat_reply(chat_text(part['text']))
                run['noted'] = run['noted'] or noted
                if text:
                    if run['texts'] and run['texts'][-1]['at'] >= at - 60000:
                        run['texts'][-1]['text'] = (run['texts'][-1]['text'] + '\n\n' + text)[:8000]
                    else:
                        run['texts'].append({'kind': 'reply', 'text': text, 'at': at})
    for key in order:
        run = runs[key]
        if run['notes'] or run['finals']:
            run['texts'] = chat_cli_replies(run)
        saved = [dict(r) for r in results.get(key, [])]
        replies = saved or run['texts']
        if run['steps']:
            first = min([run['at']] + [r['at'] for r in replies if r['at']]) if run['at'] or replies else 0
            items.append({**chat_steps_item(run), 'at': max(0, (first or 0) - 1)})
        if run['noted']:  # a learning turn of its own belongs to the reply before it
            target = replies[-1] if replies else next((i for i in reversed(items) if i['kind'] == 'reply'), None)
            if target is not None:
                target['noted'] = True
        items.extend(replies)
    for key, saved in results.items():  # a run whose session is gone: its results still show
        if key not in runs:
            items.extend(dict(r) for r in saved)
    rank = {'source': 0, 'you': 1, 'event': 1, 'steps': 2}
    items = sorted(items, key=lambda i: (i['at'], rank.get(i['kind'], 3)))
    # What a run learned shows under its reply (the run saves it before it answers), unless the owner wrote in between
    for learned in [i for i in items if i['kind'] in ('learned', 'fixed')][::-1]:
        n = items.index(learned)
        after = next((k for k in range(n + 1, len(items)) if items[k]['kind'] in ('reply', 'you')), None)
        if after is not None and items[after]['kind'] == 'reply' and items[after]['at'] - learned['at'] <= 1800000:
            items.insert(after, items.pop(n))
            learned['at'] = max(learned['at'], items[after - 1]['at'])
    return items


def unseen_draft(db, suggestion_id, revision, job_id=None):
    """Why the assistant may not send this draft revision for the owner now, or None when it may. It may only when the
    owner approved this exact draft: it was on the card (unchanged since) before the owner's own latest turn, the one
    that started this preparation (or, outside one, their latest note or Do it on the card). Whether that turn means
    "send it" is the model's judgment; that the draft was there to see first is checked here."""
    row = db.execute('SELECT next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or not any(a.get('revision') == revision for a in next_actions.actions(row['next_action'] or 'null')):
        return 'this draft is new or changed in this turn'
    saved = db.execute('SELECT saved_at FROM draft_saves WHERE suggestion_id=? AND revision=?', (suggestion_id, revision)).fetchone()
    job = db.execute('SELECT decision_id FROM preparations WHERE suggestion_id=? AND job_id=?', (suggestion_id, job_id)).fetchone() if job_id else None
    turn = (db.execute("SELECT created_at FROM decisions WHERE id=? AND suggestion_id=? AND source IN ('dashboard','telegram') AND choice IN ('other','accept')",
                       (job['decision_id'], suggestion_id)).fetchone() if job else None) if job_id else db.execute(
        "SELECT created_at FROM decisions WHERE suggestion_id=? AND source IN ('dashboard','telegram') AND choice IN ('other','accept') "
        'ORDER BY created_at DESC,rowid DESC LIMIT 1', (suggestion_id,)).fetchone()
    if not turn:
        return 'no message from the owner approves it'
    if not saved or saved['saved_at'] >= turn['created_at']:
        return 'the owner has not seen this draft before their latest message'
    return None


AGENT_WORK_NOTE = ('Work handed to Claude Code or Codex on this card, oldest first. It is part of the card\'s state, like a sent '
                   'message or the owner\'s taps: what it reports done is done, even where earlier turns of this session said it was still to do. '
                   'Build on it: never offer or describe work it already did as the next step; when it is still running, say so. '
                   'When the owner taps Do it, or asks you to apply, run, publish or deploy what it prepared, that is their approval: read its notes and '
                   'scripts in its folder and run them yourself, then check the result. If a step is refused, say what was refused and their '
                   'next step (for example: open the job in Codex and run it there).')

# A Do it tap on a to-do whose Claude Code or Codex result waits only on a step that job left for the owner (its brief's
# limits keep sends, publishing and deploys for them): the tap is the owner doing that step, so the run carries it out
# instead of offering it back as a Confirm (2026-11-07: a prepared blog update came back "Ready for you" twice).
AGENT_DO_IT_NOTE = ('The owner tapped Do it after this work. That tap is their approval for the step the latest job left for them '
                    'under its own limits: pushing, publishing or deploying what it prepared, or running the script it named for that '
                    '(such as ./publish.sh). Those limits held only for that job, not for you, and nobody else has to approve it. Read its '
                    'notes (HANDOFF.md) and scripts in its folder, check the step has not happened already and that nothing changed since, '
                    'then run it now and check the result. Never offer it back as a Confirm or Publish button, and never ask who approves it. '
                    'A message to someone that it prepared (a reply, an email) is not part of that step: save it as a draft on the to-do '
                    'for the owner to read and send, and never send it in this turn.')


def owner_time_line():
    """The owner's time zone and local time now, for a prompt: relative and local times are theirs, never UTC."""
    zone = getattr(local_tz(), 'key', None) or str(local_tz())
    local = dt.datetime.fromisoformat(now()).astimezone(local_tz()).strftime('%a %Y-%m-%d %H:%M')
    return (f"Their time zone is {zone}; it is now {local} there. Read every time they give (in an hour, at 9, tomorrow "
            f"morning) in that zone and write times back in it; never ask which time zone.")
