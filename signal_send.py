"""Sending on Signal, as on WhatsApp: one owner-approved text into an existing chat of the owner's own linked Signal.
check() validates a draft (next_actions.validate); SignalTransport hands an approved one to the Signal mirror's outbox
(signal_store.py), which alone runs signal-cli and sends it, paced, once. Never a new chat, never media."""
import contextlib
import time

FIELDS = {'kind', 'label', 'account_id', 'chat_id', 'to_name', 'body'}
MAX_LENGTH = 4000


def check(value, config, signal_chats, reply_spots=None):
    """A Signal draft as the card keeps it. The chat is one from this to-do's own Signal messages, or the person's
    existing chat in that account that the service looked up (owner_signal_chats). A reply quotes the message it answers
    where WhatsApp's would (next_actions.reply_spot)."""
    from next_actions import whatsapp_quote
    if set(value) - FIELDS:
        raise ValueError('Unsupported Signal fields; plain text only, no media')
    account = next((a for a in config['accounts'] if a['id'] == value.get('account_id') and a.get('service') == 'signal'), None)
    if not account or account.get('shared'):
        raise ValueError('Use one of the owner’s Signal accounts')
    result = {'kind': 'signal', 'account_id': account['id']}
    if value.get('label'):
        if value['label'] != 'Send' and not value['label'].startswith('Send '):
            raise ValueError('Signal button labels must say Send, such as Send reply')
        result['label'] = value['label']
    chat = (signal_chats or {}).get(str(value.get('chat_id') or ''))
    if not chat or chat.get('account_id') != account['id']:
        raise ValueError('Send only in an existing Signal chat: one from this task’s own messages (its metadata.chat_id), '
                         'or the person’s chat in this account (chat_id, or to_name to look it up)')
    result.update(chat_id=str(value['chat_id']), to_name=chat.get('name') or 'Signal chat', max_length=MAX_LENGTH)
    body = value.get('body')
    if not isinstance(body, str) or not body.strip() or len(body) > MAX_LENGTH or '\x00' in body:
        raise ValueError(f'Provide the concrete Signal message, at most {MAX_LENGTH} characters')
    result['body'] = body.strip()
    quote = whatsapp_quote(result, reply_spots)
    author, _, sent = str((quote or {}).get('message_id') or '').rpartition(':')
    if author and sent.isdigit():
        result['quote'] = {'author': author, 'sent_at': int(sent)}
    return result


class SignalTransport:
    """Sends one owner-approved Signal text into an existing chat. The app never holds the Signal keys: it puts the
    message in the mirror's outbox, keyed by the approved action job, and the mirror sends it and writes back what
    happened. A job is queued at most once, and a row the mirror started is never sent again."""
    WAIT = 120  # seconds a send waits for the mirror; it keeps at least 20 seconds between two sends

    def __init__(self, config, sleep=time.sleep, clock=time.monotonic):
        self.config, self.sleep, self.clock = config, sleep, clock

    def account(self, action):
        return next(a for a in self.config['accounts'] if a['id'] == action['account_id'] and a.get('service') == 'signal')

    def open(self, action, readonly=True):
        import signal_store
        try:
            return signal_store, signal_store.connect(self.account(action)['store'], readonly=readonly)
        except Exception:
            raise ValueError('I couldn’t reach Signal on this computer. Nothing was sent; tap Send again.') from None

    def preflight(self, action):
        if action['kind'] != 'signal':
            raise ValueError('Only an owner-approved Signal message can use the Signal transport')
        ss, db = self.open(action)
        with contextlib.closing(db):
            state = ss.get_state(db)
            if state.get('error') == 'outdated':
                raise ValueError('Signal no longer accepts this Machine’s Signal client. Nothing was sent.')
            if state.get('error') or state.get('identity') != self.account(action).get('identity_sha256'):
                raise ValueError('Signal is unlinked, or linked to another account. Nothing was sent.')
            if not ss.known_chat(db, action['chat_id']):
                raise ValueError('I couldn’t find that Signal chat. Nothing was sent.')

    def send(self, action, job):
        ss, db = self.open(action, readonly=False)
        seal = ss.sealer(self.account(action)['store'], self.config.get('database'), create=False)
        if seal is None:
            db.close()
            return {'rejected': 'no_key'}
        with contextlib.closing(db):
            ss.queue_send(db, seal, job['id'], action['chat_id'], action['body'], action.get('quote'))
        return self.outcome(action, job, wait=self.WAIT)

    def outcome(self, action, job, wait=0):
        ss, db = self.open(action)
        until = self.clock() + wait
        with contextlib.closing(db):
            while True:
                row = db.execute('SELECT status, sent_at, error FROM signal_outbox WHERE id=?', (job['id'],)).fetchone()
                if row and row['status'] == 'sent' and row['sent_at']:
                    return {'message_id': f"signal:{action['chat_id']}:{row['sent_at']}"}
                if row and row['status'] in ('failed', 'held'):
                    return {'rejected': str(row['error'] or 'refused')[:80]}
                if self.clock() >= until:
                    return {}
                self.sleep(2)

    def reconcile(self, action, job):
        try:
            result = self.outcome(action, job)
        except ValueError:
            return {}
        return result if result.get('message_id') else {}
