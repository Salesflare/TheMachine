"""Talk live: a spoken conversation with The Machine in a to-do's chat, with OpenAI's Realtime voice.

The owner's OpenAI sign-in stays in OpenClaw. The Gateway makes a short-lived, single-use session for each
conversation (talk-live-run.mjs). The service keeps that session's secret and hands the browser's WebRTC offer on, so
neither the key nor the secret reaches the browser. Audio then goes directly between the browser and OpenAI.

The dashboard gives the voice model its own tools (TOOLS): two that read (this to-do, and finding other to-dos),
`ask_chat`, which hands a request to the to-do's chat as if the owner had typed it, so it follows the chat's rules (it
can change the draft, snooze or mark done, never send), and two for approving a send by voice.

A spoken yes approves exactly one draft, and only when the owner has heard it: the voice reads it out in full (who it
goes to, the subject, the whole text), so it works with the phone in a pocket or on another page; the draft shows on
screen too when it can. The Machine pins the revision it handed the voice (`ask_to_send`), the voice asks a confirm
question naming who it goes to and how, and the owner's next utterance clearly means yes. A question expires after
ASK_SECONDS and is dropped when the focus moves to another to-do. The
Machine judges that answer itself (judge_answer: a model turn with a strict schema; anything else counts as unclear),
from its own record of what was said, never from the voice's word. If the draft changed after the question, it asks
again. The yes goes the normal confirm_action way with source 'voice' and waits UNDO_SECONDS, so the chat can show
"Approved by voice" with Undo; pacing and the outbox's checks apply as for a tap. "Send without asking" is not touched.

What both sides say is kept as the to-do's chat (lines), so there is a record. A conversation ends after LIMIT_SECONDS.

The main conversation (Talk in the sidebar) isn't tied to one to-do: the voice goes through what needs the owner one by
one (MAIN_TOOLS). It works on one to-do at a time, the one on screen (`focus`): the dashboard opens it when the voice
does (open_todo), and when the owner opens another one, that becomes the focus. Every rule above holds for the to-do in
focus, and what is said about it is kept in that to-do's chat. It ends after MAIN_LIMIT_SECONDS (OpenAI allows a
Realtime session up to 60 minutes).
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
MAIN_LIMIT_SECONDS = 1800    # the main conversation goes through several to-dos: longer, well under OpenAI's 60 minutes
MAIN_WARN_SECONDS = 1740
ROLES = ('user', 'assistant')
SESSION_PREFIX = 'agent:main:assistant-talk-'
UNDO_SECONDS = 10            # a send approved by voice waits this long, with Undo in the chat
ASK_SECONDS = 180            # a confirm question older than this needs asking again
SEND_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'intercom', 'doc_reply')
CHANNELS = {'email': 'by email', 'linkedin': 'on LinkedIn', 'slack': 'on Slack', 'x': 'on X', 'whatsapp': 'on WhatsApp',
            'telegram': 'on Telegram', 'intercom': 'in Intercom', 'doc_reply': 'as a comment in the doc'}
# An open to-do's state, in plain words, as the dashboard's lists show it (Ready, To decide, Preparing, Waiting on others,
# Later, Look done), in that order
STATES = ('ready', 'to decide', 'preparing', 'waiting on others', 'snoozed', 'looks done')
# A closed one's, as the Done / dismissed list shows it: marked done, or dismissed (Not needed)
CLOSED = ('done', 'dismissed')
# todo_action (the main conversation): a to-do's own buttons on the dashboard, by voice
TODO_ACTIONS = ('mark_done', 'dismiss', 'snooze', 'unsnooze', 'reopen', 'rename', 'do_it', 'try_again', 'not_done')
TOOLS = [
    {'type': 'function', 'name': 'todo_details',
     'description': 'Read the to-do this conversation is about: its title, the messages in it and the current draft.',
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'find_todos',
     'description': ("Find the owner's other to-dos by words in their title, by state, or both. Each comes with its "
                     'state: ready, to decide, preparing (still being worked on, no draft yet), waiting on others, '
                     'snoozed or looks done; or done or dismissed (closed ones, latest first, only when asked for or when no '
                     'open one matches).'),
     'parameters': {'type': 'object', 'properties': {
         'words': {'type': 'string', 'description': 'A few words to look for in the title. Leave out to find by state only.'},
         'state': {'type': 'string', 'enum': list(STATES + CLOSED), 'description': 'Only to-dos in this state.'}},
         'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_chat',
     'description': ('Only for a request about this to-do. Hand it to this to-do’s chat, as if the owner had typed it: draft or change a reply, '
                     'snooze it, mark it done, look something up on the web. The chat follows its usual rules: it never sends. '
                     'Anything that goes to someone waits for the owner’s Approve on screen, and a spoken yes is not one.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The request, in the owner’s words and language.'}},
                    'required': ['request'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'create_todo',
     'description': ('Add a new to-do to the owner’s list, the same as New to-do on the dashboard: for anything new, or '
                     'about something other than the to-do in focus. Nothing is sent; The Machine fills in the rest. '
                     'The to-do in focus stays the same.'),
     'parameters': {'type': 'object', 'properties': {
         'title': {'type': 'string', 'description': 'What needs doing, short, in the owner’s words and language.'},
         'note': {'type': 'string', 'description': 'Any details the owner gave, like a day or who it is about.'}},
         'required': ['title'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_to_send',
     'description': ('When the owner wants to send this to-do’s draft. Returns that one draft and its confirm question. '
                     'Read the draft out in full first: who it goes to, the subject if there is one, and the whole text, word '
                     'for word. Then ask the question, in the owner’s language, and stop to hear their answer.'),
     'parameters': {'type': 'object', 'properties': {
         'draft': {'type': 'integer', 'description': 'Which draft, by its number, only when ask_to_send said there is more than one.'}},
         'additionalProperties': False}},
    {'type': 'function', 'name': 'send_answer',
     'description': ('Call right after the owner answers your confirm question from ask_to_send. The Machine judges their '
                     'answer itself and says what happened; tell the owner that, and never say something was sent otherwise.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'end_talk',
     'description': ('End this conversation, the same as the owner pressing End. Only when the owner clearly says they are '
                     'done. Say one short goodbye first, then call this.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
]
# The main conversation's tools: the same reading, chat and send tools, about the to-do in focus, and two to move
# between to-dos. list_todos and open_todo are the dashboard's own (it knows what each list shows, and opens it).
MAIN_TOOLS = [
    {'type': 'function', 'name': 'list_todos',
     'description': ('All the owner’s open to-dos, in the order the dashboard shows them: ready (a draft is prepared) '
                     'and to decide first (these need the owner), then preparing (still being worked on, no draft yet), '
                     'waiting on others, snoozed and looks done. Each has an id, its state, its title and who it is '
                     'from; counts has how many there are in each state.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    {'type': 'function', 'name': 'open_todo',
     'description': ('Open one to-do on screen and work on it: its title, messages and current draft come back. Everything '
                     'after this (todo_details, ask_chat, ask_to_send, send_answer) is about this to-do until you open another.'),
     'parameters': {'type': 'object', 'properties': {'id': {'type': 'string', 'description': 'The id from list_todos or find_todos.'}},
                    'required': ['id'], 'additionalProperties': False}},
    {**TOOLS[0], 'description': 'Read the to-do that is open now: its title, the messages in it and the current draft.'},
    {**TOOLS[1], 'description': TOOLS[1]['description'] + ' Each has an id for open_todo.'},
    # The rest of the Machine, read only and quick: what the dashboard's Graph, Events, Calendar, Promises and
    # Connections show. The to-do in focus stays the same.
    {'type': 'function', 'name': 'search',
     'description': ('Look something up in the owner’s Machine: people, organizations and projects (their Graph), messages '
                     'and meetings (Events), or promises. Each result has an id for open_record.'),
     'parameters': {'type': 'object', 'properties': {
         'words': {'type': 'string', 'description': 'A name or a few words to look for.'},
         'kind': {'type': 'string', 'enum': ['anything', 'person', 'organization', 'project', 'message', 'meeting', 'promise'],
                  'description': 'What to look for. anything searches people, organizations and projects.'}},
         'required': ['words'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'open_record',
     'description': ('Read one person, organization, project, meeting, message or promise by its id from search or '
                     'calendar: who they are, when you last talked, what is open with them, what was said. Talk shows it on '
                     'screen. It doesn’t change the to-do in focus.'),
     'parameters': {'type': 'object', 'properties': {'id': {'type': 'string', 'description': 'The id from search or calendar.'}},
                    'required': ['id'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'calendar',
     'description': 'The owner’s meetings: today, or from a day for a few days. Each has an id for open_record.',
     'parameters': {'type': 'object', 'properties': {
         'day': {'type': 'string', 'description': 'The first day, YYYY-MM-DD. Leave out for today.'},
         'days': {'type': 'integer', 'description': 'How many days, 1 to 14. 1 by default.'}},
         'additionalProperties': False}},
    {'type': 'function', 'name': 'machine_status',
     'description': ('How the Machine itself is doing, as Connections shows it: each connected source and whether it '
                     'needs the owner, the reviews, and anything else that needs them.'),
     'parameters': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
    *TOOLS[2:4],
    # What a to-do's buttons on the dashboard do, through the same actions and rules; never a send
    {'type': 'function', 'name': 'todo_action',
     'description': ('Do what a to-do’s buttons on the dashboard do, for the to-do in focus or the one with this id: mark it '
                     'done, dismiss it (not needed), snooze it or bring it back, reopen a done or dismissed one, rename it, '
                     'start one that waits for a decision (do it), try again when preparing got stuck, or say one that looks '
                     'done isn’t. Only when the owner clearly asks. It never sends anything.'),
     'parameters': {'type': 'object', 'properties': {
         'action': {'type': 'string', 'enum': list(TODO_ACTIONS)},
         'id': {'type': 'string', 'description': 'The to-do’s id. Leave out for the one in focus.'},
         'snooze': {'type': 'string', 'enum': ['2h', 'tomorrow', '3d', '1w'], 'description': 'For snooze: how long.'},
         'snooze_until': {'type': 'string', 'description': 'For snooze, instead: a moment, ISO 8601 with its offset.'},
         'title': {'type': 'string', 'description': 'For rename: the new title.'},
         'why': {'type': 'string', 'description': 'For dismiss: why it isn’t needed, if the owner said.'}},
         'required': ['action'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_machine',
     'description': ('For anything else the owner wants done or answered that is not about the to-do in focus and no other '
                     'tool covers: hand it to The Machine’s chat, in a new to-do of its own, the way New to-do does. It can '
                     'look things up on the web, change the Graph, snooze or mark to-dos done, never send. Its answer comes '
                     'to you as a message.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The request, in the owner’s words and language.'}},
                    'required': ['request'], 'additionalProperties': False}},
    *TOOLS[4:],
]
# Talk's read tools the Machine answers itself (talk_tool, main conversation only); machine_status and ask_machine are
# the dashboard's own
MACHINE_TOOLS = ('search', 'open_record', 'calendar')
# What the tools answer the voice (in English, for the model; the owner never sees these)
ASK_NOTE = ('The chat is on it. Say one short line, like "Looking that up", and go on with the conversation; don’t check '
            'on it or say you will. When the chat is done, its answer comes to you as a message. Nothing goes to anyone '
            'until the owner approves a draft they have seen: a tap on Approve, or a clear yes to your confirm question '
            '(ask_to_send).')
QUEUED_NOTE = 'The chat is still on the last request; this one joins it. Its answer comes to you as a message.'
# The chat's answer, pushed into the conversation when its turn ends (the dashboard sends it as a message)
DONE_NOTE = ('The chat finished what you asked. Its answer: "{answer}" Tell the owner now, in a sentence or two in '
             'their language, with where it came from if it says. Don’t read out links.')
# A to-do that came in during the main conversation (the dashboard says it at a pause, never while either side talks)
NEW_NOTE = ('A new to-do needs the owner: "{title}" (from: {from}). At a natural pause, mention it in one short line, like "A new one '
            'just came in from Pieter. Want to hear it?", and only open it if they say so.')
# A to-do that was still preparing when the main conversation started (or since) and is ready now: told once, the same way
READY_NOTE = ('A to-do that was preparing is ready now: "{title}" (from: {from}). At a natural pause, mention it in one '
              'short line, like "The one for Pieter is ready now. Want to hear it?", and only open it if they say so.')
STOPPED_NOTE = 'The chat stopped before it answered. Tell the owner, and offer to ask again.'
# A request Talk live hands to the chat: a decision id with this prefix (still a chat- turn), never shown as the
# owner's message (their own words are the talk lines), with this note in the chat's prompt
RELAY_PREFIX = 'chat-talk-'
# What ask_machine hands on: a decision id with this prefix in the new to-do it made (a chat- turn, shown as the owner's
# message, since what was said is kept with the to-do in focus), with RELAY_NOTE and this note in the chat's prompt
ASK_PREFIX = 'chat-voice-'
ASK_MACHINE_NOTE = ('This to-do was made by voice, in Talk, for this one request. Do it now, as you would in any chat: you may '
                    'look things up, change the Graph, snooze or mark to-dos done, never send. When it is done and nothing is '
                    'left for the owner here, mark this to-do done.')
RELAY_NOTE = ('This request came from the owner by voice, through Talk live, and the voice is waiting to tell them your '
              'answer. Do it now. When it needs facts from outside their messages (opening hours, an address, a price, '
              'a phone number), look them up on the web or in the browser instead of saying you can’t. Then reply in '
              'two or three plain sentences that read well aloud, and name where you found it (the site), without links '
              'or lists.')
SAY = {
    'ask': 'Ask exactly this, in the owner’s language, then stop and listen: ',
    'read': 'First read the draft below out in full: who it goes to, the subject if there is one, and the whole text, word for word. ',
    'queued': ('Approved. It goes out in %d seconds unless the owner taps Undo in the chat. Say it’s on its way.' % UNDO_SECONDS),
    'no': 'Not sent. Say so, and ask what they’d like instead.',
    'unclear': 'That wasn’t a clear yes, so nothing was sent. Call ask_to_send again and ask once more.',
    'changed': 'The draft changed after you asked, so nothing was sent. Call ask_to_send again to ask about the new draft.',
    'not_asked': 'No confirm question is open, so nothing was sent. Call ask_to_send first and ask its question.',
    'expired': 'The question was asked too long ago, so nothing was sent. Call ask_to_send again, read the draft out and ask once more.',
    'no_answer': 'No answer heard yet, so nothing was sent. Wait for the owner to answer.',
}
JUDGE = ('Someone was just asked aloud: "{question}"\n'
         'Their spoken answer, as transcribed: "{answer}"\n'
         'Does the answer clearly mean yes, send it now? Judge the meaning, in any language. A hesitant, conditional or '
         'partial answer, a question, a change request, or anything unrelated is "unclear". A refusal or "wait" is "no".\n'
         'Reply with only this JSON and nothing else: {{"approve": "yes"}} or {{"approve": "no"}} or {{"approve": "unclear"}}')
# The voice's playback speed (session.update audio.output.speed, 0.25 to 1.5, 1.0 by default): a touch slower than
# OpenAI's default, never slow. How it phrases things (pacing, length) is in instructions().
SPEED = 0.95
# When the owner's turn ends (session.update audio.input.turn_detection): OpenAI's semantic VAD judges from the words
# whether they are done, instead of a fixed silence. "low" eagerness lets them take their time, so a short filler or a
# pause mid-thought doesn't start a reply. The Gateway's session starts with server_vad; the dashboard sets this.
TURN = {'type': 'semantic_vad', 'eagerness': 'low', 'create_response': True, 'interrupt_response': True}
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
    """The voice's instructions, laid out the way OpenAI's Realtime prompting guide suggests (short labeled sections of
    bullets, a Variety rule, pacing in words): how it sounds first, then the rules, which stay word for word."""
    lang = LANGUAGE_NAMES.get(language, 'the owner’s language')
    return '\n'.join([
        '# Role',
        '- You are The Machine, a personal assistant, talking live with your owner about one of their to-dos: "%s".' % title,
        '- It is now %s.' % now_text,
        '',
        '# Personality and tone',
        '- Warm, relaxed and natural, like a capable friend on the phone. Confident, never fawning or formal.',
        '- Talk the way people talk: contractions, plain everyday words, no stock assistant phrases.',
        '- Speak %s unless the owner speaks another language.' % lang,
        '',
        '## Length',
        '- Keep it short and spoken: a sentence or two at a time, then let the owner talk.',
        '- Answer the question first. Leave out what they didn’t ask for.',
        '- When the owner only acknowledges or fills a pause ("okay", "all right", "cool", "mm-hm"), don’t answer with a '
        'sentence. Say one word at most, or nothing, and wait for them.',
        '- Before a tool call, say one short line at most ("One sec"), once. Don’t announce what you will do next, and '
        'don’t add another line while it runs.',
        '',
        '## Pacing',
        '- A natural, easy conversational pace: unhurried, with small pauses between ideas. Never rushed.',
        '',
        '## Variety',
        '- Don’t repeat the same sentence or opener twice. Vary how you acknowledge and how you start.',
        '- A brief "Sure", "Okay" or "Got it" is fine now and then, not every turn.',
        '- Say what a to-do is about in your own words (who, what for). Don’t read its title out word for word each time.',
        '',
        '## Speaking, not reading',
        '- Don’t read out lists, bullets, headings, links or email addresses. Pick what matters and say it in a sentence.',
        '- Say dates and times the way people say them ("Thursday at half past two", not "2026-10-29 14:30").',
        '- The one exception: the draft ask_to_send gives you. Read it in full, word for word.',
        '- If you didn’t hear or understand the owner, ask them briefly to say it again.',
        '',
        '# Tools and rules',
        '- Call todo_details before you answer anything about this to-do, and find_todos to look up others.',
        '- You can’t change or delete anything yourself, and nothing you say goes to anyone else.',
        '- When the owner wants something done in this to-do (a reply drafted or changed, snoozed, marked done) or looked '
        'up (opening hours, an address, anything on the web), call ask_chat with their request. Say one short line, like '
        '"Looking that up", then keep talking about anything else; never poll or say you will check. The chat’s answer '
        'comes to you as a message when it is done: tell the owner then.',
        '- ask_chat is only for this to-do. Never hand it a request about something else. For anything new (a reminder, '
        'a new task) call create_todo; for another existing to-do, find it and open it first.',
        '- Creating: when they give something usable as a title, create it right away. Ask one short question at most, '
        'only when it is unclear what the to-do is. Then say it’s added in a few words, and stay on the to-do in focus.',
        '- To send: only when the owner asks to send the draft, call ask_to_send, read the draft out in full (who it goes '
        'to, the subject, the whole text), then ask its question. It works without the screen. After their answer, call '
        'send_answer and say what it returns. One draft per question; never send several at once, and never say something '
        'was sent unless send_answer says so.',
        '- If something isn’t in the to-do, ask the chat to look it up rather than guess.',
        '- When the owner clearly says they are done (a goodbye, "that’s it for now", "let’s stop"), say one short goodbye '
        'and call end_talk. Don’t ask if there is anything else first.',
    ])


def main_instructions(language, now_text):
    """The main conversation: the same voice and rules, going through the to-dos that need the owner one by one."""
    lang = LANGUAGE_NAMES.get(language, 'the owner’s language')
    return '\n'.join([
        '# Role',
        '- You are The Machine, a personal assistant, talking live with your owner to go through their to-dos together.',
        '- It is now %s.' % now_text,
        '',
        '# Personality and tone',
        '- Warm, relaxed and natural, like a capable friend on the phone. Confident, never fawning or formal.',
        '- Talk the way people talk: contractions, plain everyday words, no stock assistant phrases.',
        '- Speak %s unless the owner speaks another language.' % lang,
        '',
        '## Length',
        '- Keep it short and spoken: one or two sentences, then let the owner talk.',
        '- Answer the question first. Leave out what they didn’t ask for.',
        '- Don’t list options or what you could do next. Ask one short question at most.',
        '- When the owner only acknowledges or fills a pause ("okay", "all right", "cool", "mm-hm"), don’t answer with a '
        'sentence. Say one word at most, or nothing, and wait for them.',
        '- Before a tool call, say one short line at most ("One sec"), once. Don’t announce what you will do next, and '
        'don’t add another line while it runs.',
        '',
        '## Pacing',
        '- A natural, easy conversational pace: unhurried, with small pauses between ideas. Never rushed.',
        '',
        '## Variety',
        '- Don’t repeat the same sentence or opener twice. Vary how you acknowledge and how you start.',
        '- A brief "Sure", "Okay" or "Got it" is fine now and then, not every turn.',
        '- Say what a to-do is about in your own words (who, what for). Don’t read its title out word for word.',
        '',
        '## Speaking, not reading',
        '- Don’t read out lists, bullets, headings, links or email addresses. Pick what matters and say it in a sentence.',
        '- Say dates and times the way people say them ("Thursday at half past two", not "2026-10-29 14:30").',
        '- The one exception: the draft ask_to_send gives you. Read it in full, word for word.',
        '- If you didn’t hear or understand the owner, ask them briefly to say it again.',
        '',
        '# Going through the to-dos',
        '- Start with list_todos. It has every open to-do and its state. Begin with the ones that need the owner (ready, '
        'to decide): say how many, in one line, then take the first one.',
        '- Mention in a few words how many are still preparing, and that you’ll tell them when one is ready. Don’t go '
        'through the preparing, waiting or snoozed ones unless they ask.',
        '- If they ask about one that is preparing, open it and say in a sentence what it’s working on. There is no draft '
        'to send yet.',
        '- One to-do at a time: open_todo, say in a sentence who it is from and what they want, and whether a reply is '
        'drafted. Offer to read the draft; read it only if they want.',
        '- Then follow their lead: change the draft (ask_chat), snooze it, mark it done or not needed (todo_action), send '
        'it, or skip to the next one. When one is handled, move on to the next without being asked.',
        '- If they ask about another to-do, find it (list_todos, or find_todos by words or by state) and open it. Never '
        'say there is nothing before you’ve checked list_todos.',
        '- Done and dismissed ones: find_todos with state done or dismissed. To bring one back, todo_action reopen.',
        '',
        '# The rest of the Machine',
        '- You can see everything the dashboard shows. Pick the direct tool when one fits: search and open_record for '
        'people, organizations, projects, messages, meetings and promises; calendar for meetings on a day; machine_status '
        'for connections and reviews. They don’t change the to-do in focus.',
        '- Never guess about someone or something: look it up first. Say what matters in a sentence or two.',
        '- Anything else they want done or answered that isn’t about the to-do in focus: ask_machine, never ask_chat. Say '
        'one short line, like "On it", and go on; its answer comes to you as a message.',
        '- When nothing that needs them is left, say so in a line and ask if there is anything else.',
        '',
        '# Tools and rules',
        '- Everything below is about the to-do that is open (open_todo). Open the right one first.',
        '- Call todo_details before you answer anything about this to-do.',
        '- todo_action does what a to-do’s buttons do: mark done, dismiss, snooze, unsnooze, reopen, rename. Use it when '
        'they clearly ask, then say it in a few words. Nothing you do goes to anyone else.',
        '- When the owner wants something else done in this to-do (a reply drafted or changed) or looked '
        'up (opening hours, an address, anything on the web), call ask_chat with their request. Say one short line, like '
        '"Looking that up", then keep talking about anything else; never poll or say you will check. The chat’s answer '
        'comes to you as a message when it is done: tell the owner then.',
        '- ask_chat is only for this to-do. Never hand it a request about something else. For anything new (a reminder, '
        'a new task) call create_todo; for another existing to-do, find it and open it first.',
        '- Creating: when they give something usable as a title, create it right away. Ask one short question at most, '
        'only when it is unclear what the to-do is. Then say it’s added in a few words, and stay on the to-do in focus.',
        '- To send: only when the owner asks to send the draft, call ask_to_send, read the draft out in full (who it goes '
        'to, the subject, the whole text), then ask its question. It works without the screen. After their answer, call '
        'send_answer and say what it returns. One draft per question; never send several at once, and never say something '
        'was sent unless send_answer says so.',
        '- If something isn’t in the to-do, ask the chat to look it up rather than guess.',
        '- When the owner clearly says they are done (a goodbye, "that’s it for now", "let’s stop"), say one short goodbye '
        'and call end_talk. Don’t ask if there is anything else first.',
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


def subject(found):
    """The to-do a conversation is about now: its own, or in the main conversation the one in focus (None before one is open)."""
    return found.get('focus') if found.get('main') else found['suggestion_id']


class Talk:
    """The live conversations this service has open (in memory only), and the Gateway helper."""

    def __init__(self, config=None, runner=subprocess.run, clock=time.monotonic):
        self.config, self.run, self.clock = config or {}, runner, clock
        self.lock, self.asking = threading.Lock(), threading.Lock()
        self.open = {}      # talk ID -> {'suggestion_id', 'started', 'secret', 'offer_url', 'offer_headers', 'voice_session_id', 'via', 'offered'}
                            # (+ 'main' and 'focus' for the main conversation, whose suggestion_id is '')
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
        """A new conversation about this to-do, or the main one (suggestion_id None): its ID for the dashboard, never
        the session's secret."""
        main = suggestion_id is None
        if not main and not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        suggestion_id = '' if main else suggestion_id
        self.sweep()
        with self.lock:
            if main and any(t.get('main') for t in self.open.values()):
                raise ValueError('Talk is already open. End it first.')
            if not main and any(t['suggestion_id'] == suggestion_id for t in self.open.values()):
                raise ValueError('A live conversation is already open for this to-do. End it first.')
            if len(self.open) >= 2:
                raise ValueError('Two live conversations are already open. End one first.')
        made = self.helper({'method': 'start', 'session_key': SESSION_PREFIX + (suggestion_id or 'main'), 'voice': voice}, env)
        if made.get('error') or not made.get('secret'):
            raise ValueError('Talk live couldn’t start. Check OpenAI in OpenClaw, then try again.'
                             if made.get('reason') == 'auth' else 'Talk live couldn’t start. Try again.')
        talk_id = secrets.token_hex(8)
        with self.lock:
            self.open[talk_id] = {'suggestion_id': suggestion_id, 'started': self.clock(), 'secret': made['secret'],
                                  'offer_url': made.get('offer_url'), 'offer_headers': made.get('offer_headers') or {},
                                  'voice_session_id': made.get('voice_session_id'), 'via': made.get('via'), 'offered': False,
                                  'limit': MAIN_LIMIT_SECONDS if main else LIMIT_SECONDS, **({'main': True, 'focus': None} if main else {})}
        return {'id': talk_id, 'via': made.get('via'), 'model': str(made.get('model') or '')[:80]}

    def get(self, talk_id, suggestion_id=None):
        with self.lock:
            found = self.open.get(str(talk_id or ''))
        if not found or (suggestion_id is not None and subject(found) != suggestion_id):
            raise ValueError('This live conversation has ended.')
        if self.clock() - found['started'] > found.get('limit', LIMIT_SECONDS) + GRACE_SECONDS:
            raise ValueError('This live conversation has ended.')
        return found

    def focus(self, talk_id, suggestion_id):
        """The main conversation moves to this to-do (the one on screen). A confirm question about another one is dropped."""
        found = self.get(talk_id)
        if not found.get('main') or not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        with self.lock:
            if found['focus'] != suggestion_id:
                found.pop('confirm', None)
            found['focus'] = suggestion_id
        return {'ok': True}

    def offer(self, talk_id, sdp, env):
        """The browser's WebRTC offer, handed on with the session's secret (once); the answer goes back."""
        found = self.get(talk_id)
        if not isinstance(sdp, str) or not sdp.startswith('v=0') or len(sdp) > 262144:
            raise ValueError('Talk live couldn’t connect. Try again.')
        with self.lock:
            if found['offered']:
                raise ValueError('Talk live couldn’t connect. Try again.')
            found['offered'] = True
        got = self.helper({'method': 'offer', 'session_key': SESSION_PREFIX + (found['suggestion_id'] or 'main'), 'sdp': sdp, 'secret': found['secret'],
                           'offer_url': found['offer_url'], 'offer_headers': found['offer_headers']}, env)
        if got.get('error') or not str(got.get('sdp') or '').startswith('v=0'):
            self.end(talk_id, env)
            raise ValueError('Talk live couldn’t connect. Try again.')
        return {'sdp': got['sdp']}

    def line(self, db, talk_id, role, text, at):
        """What one side said, kept as the to-do's chat (in the main conversation: the to-do in focus; before one is
        open, kept for the record only)."""
        found = self.get(talk_id)
        text = ' '.join(str(text or '').split())[:LINE_CHARS]
        if role not in ROLES or not text:
            raise ValueError('Nothing to keep')
        db.execute('INSERT INTO talk_lines(suggestion_id,talk_id,role,text,at) VALUES(?,?,?,?,?)', (subject(found) or '', talk_id, role, text, at))
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
            return 'expired', None
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
            self.helper({'method': 'end', 'session_key': SESSION_PREFIX + (found['suggestion_id'] or 'main'),
                         'voice_session_id': found.get('voice_session_id')}, env, timeout=25)
        return {'ok': True}

    def sweep(self):
        """Conversations past their limit are forgotten (their secret with them)."""
        with self.lock:
            for talk_id in [k for k, v in self.open.items() if self.clock() - v['started'] > v.get('limit', LIMIT_SECONDS) + GRACE_SECONDS]:
                self.open.pop(talk_id, None)
