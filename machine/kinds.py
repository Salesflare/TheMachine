"""Every kind of event a source stores (`events.kind`, '<service>.<type>') and every kind of message a to-do can
send, with what the code knows about each. A leaf: data only, it imports nothing, so any module and the dashboard
(as JSON in the page, dashboard_parts) can read it. A new kind gets its row here; code asks this module instead of
spelling kinds out in a tuple of its own (tests/test_architecture.py counts the lists that still do).

An event kind's row:
- service: the service that reads it (machine/names.SERVICES), None for The Machine's own (a Fleet hand-off, a
  note the owner wrote, notes added to a meeting)
- name: what a to-do's source line calls it ("signal from Slack"), None for a kind it never names
  (machine/store/cards.source_label)
- via: the Graph's word for where someone was in touch ("last talked via LinkedIn"), None where it says the service's
  key: mostly its name, but a CRM's copy of an email is "email" and an X message "X" (graph.VIA)
- view: how the message viewer reads it: email, chat, notification or card (machine/store/message_view.py)
- family: what it is: mail, chat, meeting, notification or card
- timeline: its group on a person's Graph timeline: email, meetings, intercom, chats or other (graph.TIMELINE_SOURCES)
- send: the kind of message (SENDS) a reply to it goes out as, None when nothing replies to it
- mark: its one-color mark when the account it came in on says no more (dashboard/todos-logos.js sourceMark)
- markdown: its body renders as markdown (message_view.MARKDOWN_KINDS)
- media: a photo or file it sent without a caption shows as a chip (message_view.MEDIA_KINDS)
- messenger: a conversation that reads like its messenger app, bubbles with their times (events-message.js THREAD_IM)
"""

MAIL, CHAT, MEETING, NOTIFICATION, CARD = 'mail', 'chat', 'meeting', 'notification', 'card'
FAMILIES = (MAIL, CHAT, MEETING, NOTIFICATION, CARD)
VIEWS = ('email', 'chat', 'notification', 'card')
TIMELINE_GROUPS = ('email', 'meetings', 'intercom', 'chats', 'other')

_NO = {'via': None, 'send': None, 'timeline': 'other', 'markdown': False, 'media': False, 'messenger': False}

KINDS = {
    # mail
    'gmail.message': {**_NO, 'via': 'email', 'service': 'gmail', 'name': 'email', 'view': 'email', 'family': MAIL, 'timeline': 'email', 'send': 'email', 'mark': 'mail'},
    'outlook.message': {**_NO, 'service': 'outlook', 'name': None, 'view': 'email', 'family': MAIL, 'send': 'email', 'mark': 'outlook'},
    'ms_graph.message': {**_NO, 'service': 'outlook', 'name': None, 'view': 'email', 'family': MAIL, 'send': 'email', 'mark': 'source'},
    'imap.message': {**_NO, 'service': 'imap', 'name': None, 'view': 'email', 'family': MAIL, 'mark': 'imap'},
    'salesflare.email': {**_NO, 'via': 'email', 'service': 'salesflare', 'name': 'CRM email', 'view': 'email', 'family': MAIL, 'timeline': 'email', 'send': 'email', 'mark': 'salesflare'},
    'fleet.email': {**_NO, 'service': None, 'name': 'email', 'view': 'email', 'family': MAIL, 'mark': 'mail'},
    # chat
    'slack.message': {**_NO, 'via': 'Slack', 'service': 'slack', 'name': 'Slack', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'slack', 'mark': 'slack', 'markdown': True},
    'teams.message': {**_NO, 'via': 'Teams', 'service': 'teams', 'name': 'Teams', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'mark': 'teams', 'markdown': True, 'messenger': True},
    'whatsapp.message': {**_NO, 'via': 'WhatsApp', 'service': 'whatsapp', 'name': 'WhatsApp', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'whatsapp', 'mark': 'whatsapp', 'markdown': True, 'media': True, 'messenger': True},
    'telegram.message': {**_NO, 'via': 'Telegram', 'service': 'telegram', 'name': 'Telegram', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'telegram', 'mark': 'telegram', 'markdown': True, 'media': True, 'messenger': True},
    'signal.message': {**_NO, 'via': 'Signal', 'service': 'signal', 'name': 'Signal', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'signal', 'mark': 'signal', 'media': True, 'messenger': True},
    'linkedin.message': {**_NO, 'via': 'LinkedIn', 'service': 'linkedin', 'name': 'LinkedIn', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'linkedin', 'mark': 'linkedin', 'messenger': True},
    'x.dm': {**_NO, 'via': 'X', 'service': 'x', 'name': 'X message', 'view': 'chat', 'family': CHAT, 'timeline': 'chats', 'send': 'x', 'mark': 'x', 'messenger': True},
    'x.mention': {**_NO, 'via': 'X', 'service': 'x', 'name': 'X', 'view': 'card', 'family': CARD, 'timeline': 'chats', 'send': 'x', 'mark': 'x'},
    'intercom.conversation': {**_NO, 'via': 'Intercom', 'service': 'intercom', 'name': 'Intercom', 'view': 'chat', 'family': CHAT, 'timeline': 'intercom', 'send': 'intercom', 'mark': 'intercom'},
    'fleet.message': {**_NO, 'service': None, 'name': 'message', 'view': 'chat', 'family': CHAT, 'mark': 'chat', 'markdown': True},
    'fleet.intercom': {**_NO, 'service': None, 'name': 'Intercom', 'view': 'chat', 'family': CHAT, 'mark': 'intercom'},
    # meetings
    'calendar.event': {**_NO, 'via': 'calendar', 'service': 'calendar', 'name': 'calendar', 'view': 'card', 'family': MEETING, 'timeline': 'meetings', 'mark': 'cal'},
    'outlook.event': {**_NO, 'service': 'outlook', 'name': None, 'view': 'card', 'family': MEETING, 'mark': 'outlook'},
    'ms_graph.event': {**_NO, 'service': 'outlook', 'name': None, 'view': 'card', 'family': MEETING, 'mark': 'source'},
    'salesflare.meeting': {**_NO, 'service': 'salesflare', 'name': 'CRM meeting', 'view': 'card', 'family': MEETING, 'timeline': 'meetings', 'mark': 'salesflare'},
    'meeting.notes': {**_NO, 'service': None, 'name': 'meeting notes', 'view': 'card', 'family': MEETING, 'timeline': 'meetings', 'mark': 'cal', 'markdown': True},
    'meeting.transcript': {**_NO, 'service': None, 'name': 'transcript', 'view': 'card', 'family': MEETING, 'timeline': 'meetings', 'mark': 'cal'},
    'zoom.summary': {**_NO, 'service': 'zoom', 'name': 'Zoom notes', 'view': 'card', 'family': MEETING, 'timeline': 'meetings', 'mark': 'zoom', 'markdown': True},
    'zoom.transcript': {**_NO, 'service': 'zoom', 'name': 'Zoom transcript', 'view': 'card', 'family': MEETING, 'mark': 'zoom'},
    'google_meet.notes': {**_NO, 'service': 'google_meet', 'name': 'Meet notes', 'view': 'card', 'family': MEETING, 'mark': 'google_meet', 'markdown': True},
    'google_meet.transcript': {**_NO, 'service': 'google_meet', 'name': 'Meet transcript', 'view': 'card', 'family': MEETING, 'mark': 'google_meet'},
    'teams.notes': {**_NO, 'service': 'teams', 'name': 'Teams notes', 'view': 'card', 'family': MEETING, 'mark': 'teams', 'markdown': True},
    'teams.transcript': {**_NO, 'service': 'teams', 'name': 'Teams transcript', 'view': 'card', 'family': MEETING, 'mark': 'teams'},
    # notifications
    'android.notification': {**_NO, 'service': 'android', 'name': 'phone', 'view': 'notification', 'family': NOTIFICATION, 'mark': 'android'},
    'gateway.alert': {**_NO, 'service': 'gateway', 'name': 'The Machine', 'view': 'notification', 'family': NOTIFICATION, 'mark': 'gateway'},
    'machine.system_log': {**_NO, 'service': None, 'name': 'The Machine', 'view': 'notification', 'family': NOTIFICATION, 'mark': 'gateway'},
    # cards: an item with a state
    'docs.comment': {**_NO, 'service': 'docs', 'name': 'Doc comment', 'view': 'card', 'family': CARD, 'send': 'doc_reply', 'mark': 'docs', 'markdown': True},
    'docs.mention': {**_NO, 'service': 'docs', 'name': 'Doc mention', 'view': 'card', 'family': CARD, 'send': 'doc_reply', 'mark': 'docs', 'markdown': True},
    'docs.suggestion': {**_NO, 'service': 'docs', 'name': 'Suggested edit', 'view': 'card', 'family': CARD, 'send': 'doc_reply', 'mark': 'docs', 'markdown': True},
    'docs.shared': {**_NO, 'service': 'docs', 'name': 'Shared doc', 'view': 'card', 'family': CARD, 'mark': 'docs'},
    'github.notification': {**_NO, 'via': 'GitHub', 'service': 'github', 'name': 'GitHub', 'view': 'card', 'family': CARD, 'mark': 'github', 'markdown': True},
    'github.ci': {**_NO, 'service': 'github', 'name': 'GitHub CI', 'view': 'card', 'family': CARD, 'mark': 'github', 'markdown': True},
    'shortcut.move': {**_NO, 'service': 'shortcut', 'name': 'Shortcut', 'view': 'card', 'family': CARD, 'mark': 'shortcut', 'markdown': True},
    'trello.action': {**_NO, 'service': 'trello', 'name': 'Trello', 'view': 'card', 'family': CARD, 'mark': 'trello', 'markdown': True},
    'stripe.event': {**_NO, 'service': 'stripe', 'name': 'Stripe', 'view': 'card', 'family': CARD, 'mark': 'stripe'},
    'salesforce.opportunity': {**_NO, 'service': 'salesforce', 'name': 'CRM deal', 'view': 'card', 'family': CARD, 'mark': 'salesforce'},
    'salesforce.task': {**_NO, 'service': 'salesforce', 'name': 'CRM task', 'view': 'card', 'family': CARD, 'mark': 'salesforce'},
    'salesforce.activity': {**_NO, 'service': 'salesforce', 'name': 'CRM activity', 'view': 'card', 'family': CARD, 'mark': 'salesforce'},
    'rss.item': {**_NO, 'service': 'rss', 'name': 'feed', 'view': 'card', 'family': CARD, 'mark': 'rss'},
    'owner.card': {**_NO, 'service': None, 'name': 'note', 'view': 'card', 'family': CARD, 'mark': 'note'},
    'fleet.request': {**_NO, 'service': None, 'name': 'Fleet', 'view': 'card', 'family': CARD, 'mark': 'gateway'},
    'fleet.brief': {**_NO, 'service': None, 'name': None, 'view': 'card', 'family': CARD, 'mark': 'gateway'},
    'machine.fault': {**_NO, 'service': None, 'name': 'The Machine', 'view': 'card', 'family': CARD, 'mark': 'gateway'},
    'machine.parked_fix': {**_NO, 'service': None, 'name': None, 'view': 'card', 'family': CARD, 'mark': 'gateway'},
    'machine.moved': {**_NO, 'service': None, 'name': None, 'view': 'card', 'family': CARD, 'mark': 'gateway'},
}

# The kinds of message a to-do can send (a prepared action's `kind`), in the order the code lists them. A send kind's row:
# - name: the app it goes out in, as Settings, Activity names it (activity_log.MESSAGE_KINDS)
# - text_only: a message without a subject (next_actions.TEXT_KINDS)
# - to_person: it reaches a person: their conversations are read before it shows (handled_check), the owner is nudged
#   to send it (push), an agent job edits its draft (agent_jobs); a reply in a doc's comments is none of these
# - send_now: a connected AI may send its draft when the owner says so in a later message (card_actions send_now)
SENDS = {
    'email': {'name': 'Email', 'text_only': False, 'to_person': True, 'send_now': True},
    'linkedin': {'name': 'LinkedIn', 'text_only': True, 'to_person': True, 'send_now': True},
    'slack': {'name': 'Slack', 'text_only': True, 'to_person': True, 'send_now': True},
    'x': {'name': 'X', 'text_only': True, 'to_person': True, 'send_now': True},
    'whatsapp': {'name': 'WhatsApp', 'text_only': True, 'to_person': True, 'send_now': False},
    'telegram': {'name': 'Telegram', 'text_only': True, 'to_person': True, 'send_now': False},
    'signal': {'name': 'Signal', 'text_only': True, 'to_person': True, 'send_now': False},
    'intercom': {'name': 'Intercom', 'text_only': True, 'to_person': True, 'send_now': False},
    'doc_reply': {'name': 'Docs', 'text_only': True, 'to_person': False, 'send_now': False},
}
SEND = tuple(SENDS)  # every send kind: a draft the owner approves before it goes out
TEXT_ONLY = tuple(k for k, s in SENDS.items() if s['text_only'])  # a message without a subject
TO_PERSON = tuple(k for k, s in SENDS.items() if s['to_person'])  # it reaches a person, not a doc's comments
SEND_NOW = tuple(k for k, s in SENDS.items() if s['send_now'])  # a connected AI may send it at the owner's word


def of(*, family=None, view=None, timeline=None, service=None, send=None, flag=None):
    """The event kinds whose row matches every field given, in this module's order: of(family=MAIL),
    of(flag='markdown'). A tuple, so callers can use it where a hand-written one was."""
    want = {'family': family, 'view': view, 'timeline': timeline, 'service': service, 'send': send}
    return tuple(kind for kind, row in KINDS.items()
                 if all(value is None or row[key] == value for key, value in want.items()) and (flag is None or row[flag]))
