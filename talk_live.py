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
import unicodedata
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
SEND_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'intercom', 'doc_reply', 'doc_write')
CHANNELS = {'email': 'by email', 'linkedin': 'on LinkedIn', 'slack': 'on Slack', 'x': 'on X', 'whatsapp': 'on WhatsApp',
            'telegram': 'on Telegram', 'intercom': 'in Intercom', 'doc_reply': 'as a comment in the doc', 'doc_write': 'in the doc'}
# An open to-do's state, in plain words, as the dashboard's lists show it (Ready, To decide, Preparing, Waiting on others,
# Later, Look done), in that order
STATES = ('ready', 'to decide', 'preparing', 'waiting on others', 'snoozed', 'looks done')
# A closed one's, as the Done / dismissed list shows it: marked done, or dismissed (Not needed)
CLOSED = ('done', 'dismissed')
# todo_action (the main conversation): a to-do's own buttons on the dashboard, by voice
TODO_ACTIONS = ('mark_done', 'dismiss', 'snooze', 'unsnooze', 'reopen', 'rename', 'try_again', 'not_done')
NONE = {'type': 'object', 'properties': {}, 'additionalProperties': False}
TOOLS = [
    {'type': 'function', 'name': 'todo_details',
     'description': ('Read the to-do this conversation is about: its title, the messages in it and whether a draft is ready '
                     '(who it goes to). To hear the draft itself, call read_draft; never read it out from here.'),
     'parameters': NONE},
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
     'description': ('Only for a real question or instruction about this to-do. Hand it to this to-do’s chat: draft or change '
                     'a reply, look something up on the web. Write it as a clean instruction for the chat (what to do, '
                     'with the details the owner gave), not their raw words. Never for moving between to-dos ("next one", '
                     '"move on", "go back", "stop", "leave it"): you do that yourself. The chat never sends: anything that '
                     'goes to someone waits for the owner’s OK.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The instruction, in the owner’s language.'}},
                    'required': ['request'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'create_todo',
     'description': ('Add a new to-do to the owner’s list, the same as New to-do on the dashboard, only when the owner clearly '
                     'asks for something new ("remind me to…", "add a to-do to…"). Never for "ask again", "report a bug" or '
                     'anything about the to-do in focus. Nothing is sent; The Machine fills in the rest. The to-do in focus '
                     'stays the same.'),
     'parameters': {'type': 'object', 'properties': {
         'title': {'type': 'string', 'description': 'What needs doing, short, in the owner’s words and language.'},
         'note': {'type': 'string', 'description': 'Any details the owner gave, like a day or who it is about.'}},
         'required': ['title'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'todo_action',
     'description': ('Do what this to-do’s own buttons do, when the owner clearly asks: mark it done ("mark this as done", '
                     '"mark it done", "it’s done", "I did it"), dismiss it (not needed), snooze it, or reopen it. Never '
                     'for a single odd word or a sound. It never sends anything.'),
     'parameters': {'type': 'object', 'properties': {
         'action': {'type': 'string', 'enum': ['mark_done', 'dismiss', 'snooze', 'reopen']},
         'snooze': {'type': 'string', 'enum': ['2h', 'tomorrow', '3d', '1w'], 'description': 'For snooze: how long.'},
         'snooze_until': {'type': 'string', 'description': 'For snooze, instead: a moment, ISO 8601 with its offset.'},
         'why': {'type': 'string', 'description': 'For dismiss: why it isn’t needed, if the owner said.'}},
         'required': ['action'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'undo_last_action',
     'description': ('The owner corrects what you just did ("no, not that", "I didn’t mean done"): undoes your last '
                     'todo_action on this to-do (reopens it, unsnoozes it).'),
     'parameters': NONE},
    {'type': 'function', 'name': 'read_draft',
     'description': ('When the owner wants to hear this to-do’s draft, or before sending one they haven’t seen or heard. '
                     'Returns the draft to read out word for word (who it goes to, the subject, the whole text) and its '
                     'confirm question. The Machine keeps that it was read, so it is never read twice.'),
     'parameters': {'type': 'object', 'properties': {
         'draft': {'type': 'integer', 'description': 'Which draft, by its number, only when it said there is more than one.'}},
         'additionalProperties': False}},
    {'type': 'function', 'name': 'ask_to_send',
     'description': ('When the owner wants to send this to-do’s draft. Returns its confirm question. When the owner has '
                     'already seen this exact draft (on screen) or heard it (read_draft), it says so: then only ask the '
                     'question. Otherwise it returns the draft to read out in full first. Ask in the owner’s language, then '
                     'stop to hear their answer.'),
     'parameters': {'type': 'object', 'properties': {
         'draft': {'type': 'integer', 'description': 'Which draft, by its number, only when ask_to_send said there is more than one.'}},
         'additionalProperties': False}},
    {'type': 'function', 'name': 'send_answer',
     'description': ('Call right after the owner answers your confirm question. The Machine checks their own words for a '
                     'clear yes and says what happened; tell the owner that, and never say something was sent otherwise.'),
     'parameters': NONE},
    {'type': 'function', 'name': 'undo_send',
     'description': ('While a send by voice still waits (Undo shows on screen), stop it: when the owner says "undo", "stop", '
                     '"wait", "don’t send" or the like. Cancels everything that is still waiting.'),
     'parameters': NONE},
    {'type': 'function', 'name': 'report_bug',
     'description': ('When the owner wants to report a bug or send feedback about The Machine ("report a bug", "file '
                     'feedback", "tell the team"). Files a real report the way Report a bug in Help does. Before calling, ask '
                     'once whether to add a support report (versions, checks and recent errors, no messages) and what was '
                     'just said in Talk.'),
     'parameters': {'type': 'object', 'properties': {
         'summary': {'type': 'string', 'description': 'What went wrong, in a few sentences, from what the owner said.'},
         'support_report': {'type': 'boolean', 'description': 'True only when the owner said yes to adding a support report.'},
         'context': {'type': 'boolean', 'description': 'True only when the owner said yes to adding the to-do in focus and the last lines of Talk.'}},
         'required': ['summary'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'end_talk',
     'description': ('End this conversation, the same as the owner pressing End. Only when the owner clearly says they are '
                     'done. Say one short goodbye first, then call this.'),
     'parameters': NONE},
]
TOOL = {t['name']: t for t in TOOLS}
# The main conversation's tools: the same reading, chat and send tools, about the to-do in focus, and two to move
# between to-dos. list_todos and open_todo are the dashboard's own (it knows what each list shows, and opens it).
MAIN_TOOLS = [
    {'type': 'function', 'name': 'list_todos',
     'description': ('All the owner’s open to-dos, in the order the dashboard shows them: ready (a draft is prepared) '
                     'and to decide first (these need the owner), then preparing (still being worked on, no draft yet), '
                     'waiting on others, snoozed and looks done. Each has an id, its state, its title and who it is '
                     'from; counts has how many there are in each state.'),
     'parameters': NONE},
    {'type': 'function', 'name': 'open_todo',
     'description': ('Open one to-do on screen and work on it: its title, messages and whether a draft is ready come back. '
                     'Everything after this (todo_details, ask_chat, read_draft, ask_to_send, send_answer) is about this '
                     'to-do until you open another. "Next one", "move on", "previous", "go back": open that one yourself.'),
     'parameters': {'type': 'object', 'properties': {'id': {'type': 'string', 'description': 'The id from list_todos or find_todos.'}},
                    'required': ['id'], 'additionalProperties': False}},
    {**TOOL['todo_details'], 'description': ('Read the to-do that is open now: its title, the messages in it and whether a '
                                             'draft is ready. To hear the draft itself, call read_draft.')},
    {**TOOL['find_todos'], 'description': TOOL['find_todos']['description'] + ' Each has an id for open_todo.'},
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
     'parameters': NONE},
    TOOL['ask_chat'], TOOL['create_todo'],
    # What a to-do's buttons on the dashboard do, through the same actions and rules; never a send
    {'type': 'function', 'name': 'do_it',
     'description': ('Press the to-do’s Do it button: The Machine starts working on it, browser work included (filling in a '
                     'form, booking, buying, anything on a website), and the owner can follow it on the to-do. For "do it", '
                     '"go ahead and do it", "handle it", "start it", "continue" or "let it continue". Not for "mark it '
                     'done", "it’s done" or "I did it": that is todo_action mark_done. Never sends a draft: sending is '
                     'ask_to_send.'),
     'parameters': {'type': 'object', 'properties': {'id': {'type': 'string', 'description': 'The to-do’s id. Leave out for the one in focus.'}},
                    'additionalProperties': False}},
    {'type': 'function', 'name': 'todo_action',
     'description': ('Do what a to-do’s other buttons on the dashboard do, for the to-do in focus or the one with this id: '
                     'mark it done ("mark it done", "it’s done", "I did it"; never for "do it"), dismiss it (not needed), '
                     'snooze it or bring it back, reopen a done or dismissed one, rename it, try again when preparing got '
                     'stuck, or say one that looks done isn’t. Only when the owner clearly asks. It never sends anything.'),
     'parameters': {'type': 'object', 'properties': {
         'action': {'type': 'string', 'enum': list(TODO_ACTIONS)},
         'id': {'type': 'string', 'description': 'The to-do’s id. Leave out for the one in focus.'},
         'snooze': {'type': 'string', 'enum': ['2h', 'tomorrow', '3d', '1w'], 'description': 'For snooze: how long.'},
         'snooze_until': {'type': 'string', 'description': 'For snooze, instead: a moment, ISO 8601 with its offset.'},
         'title': {'type': 'string', 'description': 'For rename: the new title.'},
         'why': {'type': 'string', 'description': 'For dismiss: why it isn’t needed, if the owner said.'}},
         'required': ['action'], 'additionalProperties': False}},
    {'type': 'function', 'name': 'undo_last_action',
     'description': ('The owner corrects what you just did ("no, not that", "I meant do it, not done"): undoes your last '
                     'todo_action or do_it on the to-do it touched (reopens it, unsnoozes it, renames it back) and opens that '
                     'to-do again, so you can then do what they meant on it.'),
     'parameters': NONE},
    {'type': 'function', 'name': 'ask_machine',
     'description': ('For anything else the owner wants done or answered that is not about the to-do in focus and no other '
                     'tool covers: hand it to The Machine’s chat, in a new to-do of its own, the way New to-do does. It can '
                     'look things up on the web, change the Graph, snooze or mark to-dos done, never send. Its answer comes '
                     'to you as a message.'),
     'parameters': {'type': 'object', 'properties': {'request': {'type': 'string', 'description': 'The request, in the owner’s words and language.'}},
                    'required': ['request'], 'additionalProperties': False}},
    TOOL['read_draft'], TOOL['ask_to_send'],
    {'type': 'function', 'name': 'ask_to_send_all',
     'description': ('When the owner wants several ready drafts sent at once ("send all the ready follow-ups", "send both"). '
                     'Give the to-dos’ ids (from list_todos). Returns one confirm question naming who each goes to; any '
                     'draft the owner hasn’t seen or heard comes with its text to read out first. One clear yes sends them '
                     'all, each with its own Undo.'),
     'parameters': {'type': 'object', 'properties': {
         'ids': {'type': 'array', 'items': {'type': 'string'}, 'description': 'The to-dos’ ids, at most 5.'}},
         'required': ['ids'], 'additionalProperties': False}},
    TOOL['send_answer'], TOOL['undo_send'], TOOL['report_bug'], TOOL['end_talk'],
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
DONE_NOTE = ('The chat of the to-do "{title}" finished what you asked. Its answer: "{answer}" Tell the owner now, in a '
             'sentence or two in their language, with where it came from if it says. If that to-do isn’t the one in focus '
             'any more, say first which one it is about. Don’t read out links. Say it once; if you already told them this, '
             'don’t repeat it.')
# A to-do that came in during the main conversation (the dashboard says it at a pause, never while either side talks)
NEW_NOTE = ('A new to-do needs the owner: "{title}" (from: {from}). At a natural pause, mention it in one short line, like "A new one '
            'just came in from Pieter. Want to hear it?", and only open it if they say so.')
# A to-do that was still preparing when the main conversation started (or since) and is ready now: told once, the same way
READY_NOTE = ('A to-do that was preparing is ready now: "{title}" (from: {from}). At a natural pause, mention it in one '
              'short line, like "The one for Pieter is ready now. Want to hear it?", and only open it if they say so.')
STOPPED_NOTE = ('The chat of the to-do "{title}" stopped before it answered "{request}". Tell the owner once, in a line, '
                'and offer to ask again. If they say "ask again", call ask_chat with that same request; never create_todo.')
# What the owner said didn't come through (a few words in a language they don't speak, or one odd word before an action)
AGAIN_NOTE = 'The owner’s last words didn’t come through clearly. Say only: "Sorry, say that again?" and do nothing else.'
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
              'or lists. Work only on this to-do: never look up, change or answer about the owner’s other to-dos.')
SAY = {
    'ask': 'Ask exactly this, in the owner’s language, then stop and listen: ',
    'read': 'First read the draft below out in full: who it goes to, the subject if there is one, and the whole text, word for word. ',
    'seen': 'The owner has already seen or heard this exact draft, so don’t read it again. ',
    'read_some': ('Read out in full, word for word, only the drafts below that have a text (the owner hasn’t seen those), '
                  'saying who each goes to. Don’t read the others again. '),
    'queued': ('Approved. It goes out in %d seconds. Say it’s on its way, and that they can say undo or tap Undo.' % UNDO_SECONDS),
    'queued_all': ('Approved. They go out in %d seconds. Say they’re on their way, and that they can say undo or tap Undo.' % UNDO_SECONDS),
    'no': 'Not sent. Say so, and ask what they’d like instead.',
    'unclear': ('That wasn’t a clear yes, so nothing was sent. Don’t read the draft again: ask the same question once more, '
                'short, like "Say yes to send it to {name}.", then call send_answer after their answer.'),
    'changed': 'The draft changed after you asked, so nothing was sent. Call ask_to_send again to ask about the new draft.',
    'not_read': ('The draft wasn’t read out in full, so nothing was sent. Call read_draft, read it out word for word, then ask '
                 'its question.'),
    'not_asked': 'No confirm question is open, so nothing was sent. Call ask_to_send first and ask its question.',
    'expired': 'The question was asked too long ago, so nothing was sent. Call ask_to_send again and ask once more.',
    'no_answer': 'No answer heard yet, so nothing was sent. Wait for the owner to answer.',
}
# A spoken yes, judged by the Machine itself from the owner's own words (never the voice's, never a model): every word of
# the answer is a plain yes or a small filler word in one of the owner's languages (English always), with at least one
# yes in it; no question, no "but", nothing else. A refusal or "wait" at the start is a no. Anything else asks again.
YES = {
    'en': ({'yes', 'yeah', 'yep', 'yup', 'ok', 'okay', 'sure', 'send', 'go', 'absolutely', 'correct', 'perfect', 'alright', 'fine', 'good'},
           {'it', 'them', 'all', 'both', 'please', 'ahead', 'now', 'just', 'do', 'that', 'thats', 'its', 'is', 'so', 'oh', 'um',
            'uh', 'and', 'then', 'sounds', 'right', 'the', 'one', 'ones', 'these', 'those', 'thanks', 'thank', 'you', 'great',
            'out', 'away', 'off', 'to'}),
    'nl': ({'ja', 'jawel', 'jep', 'oke', 'okee', 'ok', 'prima', 'goed', 'doe', 'verstuur', 'versturen', 'stuur', 'zeker', 'top', 'klopt', 'perfect'},
           {'maar', 'het', 'hem', 'ze', 'hoor', 'graag', 'mag', 'weg', 'door', 'is', 'dat', 'alles', 'allebei', 'beide', 'nu',
            'even', 'dan', 'die', 'ze', 'alle', 'drie', 'twee', 'ok', 'dank', 'je', 'u', 'nou', 'eh', 'uh'}),
    'de': ({'ja', 'jawohl', 'klar', 'okay', 'ok', 'gut', 'schick', 'senden', 'sende', 'genau', 'passt', 'los', 'sicher'},
           {'es', 'sie', 'ab', 'bitte', 'mach', 'ist', 'alle', 'beide', 'jetzt', 'doch', 'na', 'also', 'danke'}),
    'fr': ({'oui', 'ouais', 'daccord', 'ok', 'parfait', 'envoie', 'envoyez', 'vas', 'bien'},
           {'le', 'la', 'les', 'cest', 'bon', 'sil', 'te', 'vous', 'plait', 'tous', 'deux', 'merci', 'vas', 'y', 'oh'}),
    'es': ({'si', 'vale', 'claro', 'envialo', 'enviala', 'envialos', 'adelante', 'dale', 'perfecto', 'ok', 'bien'},
           {'por', 'favor', 'todos', 'ambos', 'gracias', 'ya', 'pues', 'esta'}),
    'it': ({'si', 'certo', 'ok', 'invia', 'inviala', 'invialo', 'vai', 'perfetto', 'bene'},
           {'va', 'pure', 'per', 'favore', 'tutti', 'grazie', 'ok'}),
    'pt': ({'sim', 'claro', 'pode', 'envia', 'enviar', 'manda', 'mandar', 'ok', 'perfeito', 'certo', 'beleza'},
           {'por', 'favor', 'isso', 'todos', 'obrigado', 'obrigada', 'ja', 'pode'}),
}
NO_START = {'no', 'nope', 'nah', 'nee', 'neen', 'niet', 'nein', 'non', 'nao', 'wait', 'wacht', 'warte', 'attends', 'espera',
            'aspetta', 'stop', 'cancel', 'dont', 'hold', 'undo', 'never', 'not'}


def answer_words(text):
    """An answer as plain lowercase words: accents and apostrophes gone ("Oké" is "oke", "it's" is "its")."""
    plain = unicodedata.normalize('NFKD', str(text or '').lower().replace('’', "'"))
    plain = ''.join(c for c in plain if not unicodedata.combining(c)).replace("'", '').replace('-', ' ')
    return re.findall(r'[a-z0-9]+', plain)


def clear_answer(text, languages=('en',), names=()):
    """'yes', 'no' or 'unclear' for the owner's spoken answer to a confirm question (see YES). names: the words of who it
    goes to, which may be in a yes ("Yes, send it to Dana")."""
    found = answer_words(text)
    if not found:
        return 'unclear'
    if found[0] in NO_START:
        return 'no'
    if '?' in str(text):
        return 'unclear'
    langs = ['en'] + [x for x in spoken(languages or []) if x != 'en']
    core = set().union(*(YES[x][0] for x in langs if x in YES))
    allowed = core | set().union(*(YES[x][1] for x in langs if x in YES)) | {w for n in names for w in answer_words(n)}
    if all(w in allowed for w in found) and any(w in core for w in found):
        return 'yes'
    return 'unclear'


# The voice's playback speed (session.update audio.output.speed, 0.25 to 1.5, 1.0 by default): a little quicker than
# OpenAI's default, natural and never rushed. How it phrases things (pacing, length) is in instructions().
SPEED = 1.1
# When the owner's turn ends (session.update audio.input.turn_detection): OpenAI's semantic VAD judges from the words
# whether they are done, instead of a fixed silence. "low" eagerness lets them take their time, so a short filler or a
# pause mid-thought doesn't start a reply. The Gateway's session starts with server_vad; the dashboard sets this.
TURN = {'type': 'semantic_vad', 'eagerness': 'low', 'create_response': True, 'interrupt_response': True}
# The microphone's audio is cleaned before turn detection and the model hear it (audio.input.noise_reduction), so a
# rustle, a cough or a room's hum starts fewer turns. far_field: a phone held in the hand or on the table, or a laptop
# (near_field is for a headset close to the mouth).
NOISE = {'type': 'far_field'}
# What the owner says is written down by this model (audio.input.transcription), in the languages they speak
# (transcription()) instead of guessing among every language, which turned short sounds into Korean or Thai.
TRANSCRIBE_MODEL = 'gpt-4o-transcribe'
# OpenAI's newest model for it, which takes the owner's languages as a list and says which one it heard. Asked for in a
# session.update of its own (transcription_next()): one a session refuses (it is new, and documented for WebSocket)
# changes nothing else, and TRANSCRIBE_MODEL stays.
NEXT_TRANSCRIBE_MODEL = 'gpt-transcribe'
# The languages the app speaks, as ISO 639-1 codes (what transcription takes); all of them write in Latin script
SPOKEN = ('de', 'en', 'es', 'fr', 'it', 'nl', 'pt')
LANGUAGE_NAMES = {'de': 'German', 'en': 'English', 'es': 'Spanish', 'fr': 'French', 'it': 'Italian', 'nl': 'Dutch', 'pt-BR': 'Brazilian Portuguese'}


def spoken(*wanted):
    """The owner's spoken languages, in order and at most three, as ISO 639-1 codes: from the UI language, the voice
    input language (Settings), the locale and the browser's languages ('nl-BE' -> 'nl'). English when none fits."""
    out = []
    for each in wanted:
        for tag in (each if isinstance(each, (list, tuple)) else [each]):
            code = str(tag or '').strip().lower()[:2]
            if code in SPOKEN and code not in out:
                out.append(code)
    return out[:3] or ['en']


def transcription(languages):
    """audio.input.transcription for the owner's languages. One language is pinned (`language`, which OpenAI says
    improves accuracy and latency); with several, pinning one would turn a sentence in another into a wrong
    transcript, so the prompt names them instead. Either way the model no longer picks among every language."""
    names = [LANGUAGE_NAMES.get(code) or {'pt': 'Portuguese'}.get(code, code) for code in languages]
    said = names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' or ' + names[-1]
    found = {'model': TRANSCRIBE_MODEL, 'prompt': 'One person talking with their assistant in %s.' % said}
    if len(languages) == 1:
        found['language'] = languages[0]
    return found


def transcription_next(languages):
    """The newer transcription for the owner's languages (NEXT_TRANSCRIBE_MODEL): a list, so several are pinned at once."""
    return {'model': NEXT_TRANSCRIBE_MODEL, 'languages': list(languages)}


def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS talk_lines(id INTEGER PRIMARY KEY, suggestion_id TEXT NOT NULL, talk_id TEXT NOT NULL, '
               'role TEXT NOT NULL, text TEXT NOT NULL, at INTEGER NOT NULL)')
    db.execute('CREATE INDEX IF NOT EXISTS talk_lines_card ON talk_lines(suggestion_id, at)')
    # A draft the owner has seen in full on the dashboard (its to-do, its chat or Talk's card): this exact text
    db.execute('CREATE TABLE IF NOT EXISTS draft_seen(suggestion_id TEXT NOT NULL, revision TEXT NOT NULL, digest TEXT NOT NULL, '
               'seen_at INTEGER NOT NULL, PRIMARY KEY(suggestion_id, revision, digest))')


def lines(db, suggestion_id):
    """A to-do's conversations for its chat: a "Talked live" line at the start of each, then what each side said."""
    out, seen = [], set()
    for r in db.execute('SELECT talk_id,role,text,at FROM talk_lines WHERE suggestion_id=? ORDER BY at,id', (suggestion_id,)):
        if r['talk_id'] not in seen:
            seen.add(r['talk_id'])
            out.append({'kind': 'event', 'text': 'Talked live', 'mine': True, 'at': max(0, r['at'] - 1)})
        out.append({'kind': 'you' if r['role'] == 'user' else 'reply', 'text': r['text'], 'via': 'live', 'at': r['at']})
    return out


def hearing(languages):
    """What the voice does with what it can't take as the owner talking: in the owner's languages, a noise or another
    language gets no answer (the dashboard also cancels a reply to a line it drops)."""
    names = [LANGUAGE_NAMES.get(code) or {'pt': 'Portuguese'}.get(code, code) for code in spoken(languages)]
    said = names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' or ' + names[-1]
    return ['- The owner speaks %s. A noise, a breath, a cough, a cut-off word or a few words in another language aren’t '
            'meant for you: don’t answer them, say nothing and wait.' % said]


def instructions(title, language, now_text, languages=None):
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
        *hearing(languages or [language]),
        '',
        '## Length',
        '- Keep it short and spoken: a sentence or two at a time, then let the owner talk.',
        '- One reply per turn, said once. Never follow it with a second reply that says the same thing again in other words.',
        '- No em dashes or en dashes: use a comma or a period, the way people pause when they talk.',
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
        '- The one exception: a draft read_draft or ask_to_send gives you to read. Read it in full, word for word.',
        '- If you didn’t hear or understand the owner, ask them briefly to say it again.',
        '',
        '# Tools and rules',
        '- Call todo_details before you answer anything about this to-do, and find_todos to look up others.',
        '- Nothing you say goes to anyone else.',
        '- When the owner clearly asks to mark this to-do done ("mark this as done", "it’s done"), dismiss it, snooze it '
        'or reopen it, call todo_action and say what it returns in a few words. Never hand that to the chat. A correction '
        'right after ("no, not done") is undo_last_action.',
        '- When the owner wants something done in this to-do (a reply drafted or changed) or looked '
        'up (opening hours, an address, anything on the web), call ask_chat with a clean instruction (what to do, with the details they gave). Say one short line, like '
        '"Looking that up", then keep talking about anything else; never poll or say you will check. The chat’s answer '
        'comes to you as a message when it is done: tell the owner then.',
        '- When the chat’s answer comes, say what is new in it once, in a sentence or two. If you already said it, or it '
        'says what you just told the owner, don’t say it again.',
        '- ask_chat is only for this to-do. Never hand it a request about something else. For anything new (a reminder, '
        'a new task) call create_todo; for another existing to-do, find it and open it first. "Ask again" means ask_chat '
        'again with the same request.',
        '- Creating: when they give something usable as a title, create it right away. Ask one short question at most, '
        'only when it is unclear what the to-do is. Then say it’s added in a few words, and stay on the to-do in focus.',
        '- To hear a draft: call read_draft and read out what it gives you, word for word. Never read or sum up a draft '
        'from anything else.',
        '- To send: only when the owner asks to send it, call ask_to_send. If it says the owner has seen or heard this '
        'draft, only ask its question; otherwise read the draft out in full first. It works without the screen. After '
        'their answer, call send_answer and say what it returns; never say something was sent unless send_answer says so. '
        'Never read the same draft twice.',
        '- Only a clear yes sends. If send_answer says it wasn’t clear, ask the question again in a few words, without '
        'reading the draft again.',
        '- While a send waits, Undo shows on screen. If the owner says "undo", "stop", "wait" or "don’t send", call '
        'undo_send at once.',
        '- Never say something happened (sent, filed, done, started, reported) unless a tool result says it did. Say only '
        'what the result says, nothing more.',
        '- To report a bug or send feedback, call report_bug, never create_todo. Ask once first whether to add a support '
        'report and what was just said. Then say only what it returns, like "Sent the bug report."',
        '- Before anything that changes something (create, dismiss, mark done, snooze, do it, send, report), be sure what '
        'the owner said. If it was unclear or a single odd word, say "Sorry, say that again?" and do nothing.',
        '- If something isn’t in the to-do, ask the chat to look it up rather than guess.',
        '- When the owner clearly says they are done (a goodbye, "that’s it for now", "let’s stop"), say one short goodbye '
        'and call end_talk. Don’t ask if there is anything else first. A single word, a sound or words in another '
        'language are never a goodbye or a wrap-up: ask what they meant.',
    ])


def main_instructions(language, now_text, languages=None):
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
        *hearing(languages or [language]),
        '',
        '## Length',
        '- Keep it short and spoken: one or two sentences, then let the owner talk.',
        '- One reply per turn, said once. Never follow it with a second reply that says the same thing again in other words.',
        '- No em dashes or en dashes: use a comma or a period, the way people pause when they talk.',
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
        '- The one exception: a draft read_draft or ask_to_send gives you to read. Read it in full, word for word.',
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
        'drafted. Offer to read the draft (read_draft); read it only if they want.',
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
        '- todo_action does what a to-do’s buttons do: mark done, dismiss, snooze, unsnooze, reopen, rename; do_it presses '
        'its Do it. Use them when they clearly ask, then say it in a few words. Nothing you do goes to anyone else.',
        '- When the owner wants something else done in this to-do (a reply drafted or changed) or looked '
        'up (opening hours, an address, anything on the web), call ask_chat with a clean instruction (what to do, with the details they gave). Say one short line, like '
        '"Looking that up", then keep talking about anything else; never poll or say you will check. The chat’s answer '
        'comes to you as a message when it is done: tell the owner then.',
        '- When the chat’s answer comes, say what is new in it once, in a sentence or two. If you already said it, or it '
        'says what you just told the owner, don’t say it again.',
        '- ask_chat is only for this to-do. Never hand it a request about something else. For anything new (a reminder, '
        'a new task) call create_todo; for another existing to-do, find it and open it first. "Ask again" means ask_chat '
        'again with the same request.',
        '- Creating: when they give something usable as a title, create it right away. Ask one short question at most, '
        'only when it is unclear what the to-do is. Then say it’s added in a few words, and stay on the to-do in focus.',
        '- To hear a draft: call read_draft and read out what it gives you, word for word. Never read or sum up a draft '
        'from anything else.',
        '- To send: only when the owner asks to send it, call ask_to_send. If it says the owner has seen or heard this '
        'draft, only ask its question; otherwise read the draft out in full first. It works without the screen. After '
        'their answer, call send_answer and say what it returns; never say something was sent unless send_answer says so. '
        'Never read the same draft twice.',
        '- Only a clear yes sends. If send_answer says it wasn’t clear, ask the question again in a few words, without '
        'reading the draft again.',
        '- While a send waits, Undo shows on screen. If the owner says "undo", "stop", "wait" or "don’t send", call '
        'undo_send at once.',
        '- Never say something happened (sent, filed, done, started, reported) unless a tool result says it did. Say only '
        'what the result says, nothing more.',
        '- To report a bug or send feedback, call report_bug, never create_todo. Ask once first whether to add a support '
        'report and what was just said. Then say only what it returns, like "Sent the bug report."',
        '- Before anything that changes something (create, dismiss, mark done, snooze, do it, send, report), be sure what '
        'the owner said. If it was unclear or a single odd word, say "Sorry, say that again?" and do nothing.',
        '- "Do it", "go ahead and do it", "handle it", "start it", "continue": call do_it. "Mark it done", "it’s done", '
        '"I did it": todo_action mark_done. Never mix them up.',
        '- Browser work on a to-do (a form, a booking, a purchase, anything on a website) goes through do_it: The Machine '
        'does it in its own browser and the owner can follow it on the to-do. Never say you can’t use the browser. Say the '
        'job started and they can follow it on the to-do.',
        '- If the owner corrects what you just did ("no, I meant…"), call undo_last_action: it undoes it on the to-do it '
        'touched and opens that one again. Say what you undid, then do what they meant there.',
        '- "Do this and move on": call the tool, wait for its result, and open the next to-do only when it says ok. If it '
        'didn’t work, say so and stay.',
        '- Moving between to-dos ("next one", "move on", "previous", "go back", "skip it") is yours to do with list_todos and '
        'open_todo, never ask_chat. "Stop" or "leave it" means do nothing more on it.',
        '- To send several ready drafts at once ("send all the ready ones", "send both"), call ask_to_send_all with their '
        'ids. Read out only the drafts it gives a text for, then ask its one question.',
        '- If something isn’t in the to-do, ask the chat to look it up rather than guess.',
        '- When the owner clearly says they are done (a goodbye, "that’s it for now", "let’s stop"), say one short goodbye '
        'and call end_talk. Don’t ask if there is anything else first. A single word, a sound or words in another '
        'language are never a goodbye or a wrap-up: ask what they meant.',
    ])



def saw(db, sid, revision, digest_, at):
    """The dashboard showed this exact draft in full, long enough to read (Assistant.draft_seen checked the text)."""
    db.execute('INSERT OR IGNORE INTO draft_seen(suggestion_id,revision,digest,seen_at) VALUES(?,?,?,?)', (sid, revision, digest_, at))


def seen(db, sid, revision, digest_):
    """Whether the dashboard showed this exact draft (this revision, this text) in full."""
    return bool(db.execute('SELECT 1 FROM draft_seen WHERE suggestion_id=? AND revision=? AND digest=?',
                           (sid, revision, digest_)).fetchone())


def digest(action):
    """What a confirm question was about: who, how and what. Any change after the question means asking again."""
    keep = {k: action.get(k) for k in ('kind', 'to', 'cc', 'bcc', 'from', 'subject', 'body', 'message', 'thread_id', 'channel',
                                       'op', 'title', 'file_id', 'version', 'changes')}
    return hashlib.sha256(json.dumps(keep, sort_keys=True, default=str).encode()).hexdigest()


def question(action, name):
    """The confirm question for one draft, naming who it goes to and how."""
    what = 'reply' if action.get('reply') or str(action.get('subject') or '').lower().startswith('re:') else 'message'
    if action.get('kind') == 'doc_reply':
        return 'Post this reply as a comment in the doc?'
    if action.get('kind') == 'doc_write':  # a new doc or an edit, read aloud in full first (doc_writes.spoken)
        return ('Create this doc?' if action.get('op') == 'create'
                else 'Save these changes to “%s”?' % action.get('doc_title', 'the doc'))
    return 'Send this %s to %s %s?' % (what, name, CHANNELS.get(action.get('kind'), ''))


def read_out(text, said):
    """Whether what the voice said holds the draft: at least 70% of its words (three letters or more) are in it."""
    want = {w for w in answer_words(text) if len(w) >= 3}
    if not want:
        return True
    got = set(answer_words(said))
    return len(want & got) >= 0.7 * len(want)


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

    def start(self, suggestion_id, env, voice='cedar', languages=('en',)):
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
                                  'limit': MAIN_LIMIT_SECONDS if main else LIMIT_SECONDS, 'languages': list(languages or ['en']),
                                  'read': {}, **({'main': True, 'focus': None} if main else {})}
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

    def ask(self, talk_id, items, asked, name, at, suggestion_id=None):
        """The voice is about to ask to send these drafts (one, or several at once): the question, kept until the owner's
        next answer. items: {'sid', 'revision', 'digest', 'read'} each; read is the text the voice must read out first
        (a draft the owner hasn't seen or heard), else None."""
        found = self.get(talk_id, suggestion_id)
        with self.lock:
            found['confirm'] = {'items': items, 'at': at, 'question': asked, 'name': name.split(' and ')[0], 'named': False}
        return asked

    def heard(self, db, talk_id, sid, revision, digest_, at=None):
        """Whether the owner heard this exact draft read out in this conversation: the voice's own lines since it was
        handed over hold (nearly) all its words."""
        found = self.get(talk_id)
        kept = found['read'].get((sid, revision))
        if not kept or kept['digest'] != digest_:
            return False
        if kept.get('done'):
            return True
        said = ' '.join(r['text'] for r in db.execute("SELECT text FROM talk_lines WHERE talk_id=? AND role='assistant' AND at>=? "
                                                      'ORDER BY at,id', (talk_id, kept['at'])))
        if read_out(kept['text'], said):
            kept['done'] = True
        return bool(kept.get('done'))

    def reading(self, talk_id, sid, revision, digest_, text, at):
        """The voice was handed this draft to read out (heard() checks it was)."""
        found = self.get(talk_id)
        with self.lock:
            found['read'][(sid, revision)] = {'digest': digest_, 'text': text, 'at': at}

    def answer(self, db, talk_id, at, current):
        """The owner's answer to the open confirm question, from what this conversation recorded (talk_lines): the
        voice's question, then what the owner said after it (their latest line). current(sid, revision) is that draft
        as it is now, or None. Returns (status, confirm): 'yes' with the question it approves, or why not. An unclear
        answer keeps the question open: the voice asks it again, short, without reading the draft again."""
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
        if spoke is None:              # the voice hasn't asked (again) yet: the question stays open
            return ('no_answer' if c.get('again') else 'not_asked'), None
        owner = [r['text'] for r in said[spoke:] if r['role'] == 'user']
        first = next(n for n in range(spoke, len(said) + 1) if n == len(said) or said[n]['role'] == 'user')
        voice = ' '.join(r['text'] for r in said[spoke:first] if r['role'] == 'assistant')
        if not owner:
            return 'no_answer', None
        if not c['named'] and c['name'] and '@' not in c['name'] and c['name'] != 'them' and c['name'].lower() not in voice.lower():
            found.pop('confirm', None)
            return 'unclear', None     # the question it spoke didn't say who it goes to: asked again from the start
        c['named'] = True
        for item in c['items']:
            now = current(item['sid'], item['revision'])
            if not now or digest(now) != item['digest']:
                found.pop('confirm', None)
                return 'changed', None
            if item.get('read') and not self.heard(db, talk_id, item['sid'], item['revision'], item['digest']):
                found.pop('confirm', None)
                return 'not_read', None
        judged = clear_answer(owner[-1], found.get('languages'), [c['name']] if c['name'] != 'them' else [])
        if judged == 'unclear':
            c['at'], c['again'] = at, True   # asked again: the next answer comes after that
            return 'unclear', c
        found.pop('confirm', None)     # one answer per question
        return judged, c

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
