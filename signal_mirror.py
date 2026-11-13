#!/usr/bin/env python3
"""The Signal mirror: the one process that runs signal-cli (signal_release.py) for the owner's Signal account, as a
linked device of their phone, like Signal Desktop. signal-cli keeps the device's keys in the store's `signal-keys/` folder on
this Machine; the mirror talks to it over JSON-RPC on stdin and stdout and keeps what arrives in signal_store.py.

    signal_mirror.py --store DIR [--cli PATH] [--base DIR] link      link this Machine (a QR code to scan on the phone)
    signal_mirror.py --store DIR [--cli PATH] [--base DIR] follow    keep the store in step (a user service)
    signal_mirror.py --store DIR [--cli PATH] [--base DIR] logout    forget this linked device's keys on this Machine
    signal_mirror.py [--cli PATH] [--base DIR] version               signal-cli's version, to check the install

`link` speaks JSON lines: {"event": "qr", "matrix", "expires"} (again each time Signal needs a new code) and
{"event": "connected", "identity"}, or {"event": "error", "code"}.

How it treats the account:
- One fixed device name ("The Machine"), so the phone shows one linked device that stays. Unlinked on the phone, it
  stops and says so (state `error`), and the owner links it again from Connections. It never links by itself again.
- Signal gives a newly linked device no older messages: it reads from the moment of linking, nothing before.
- People's chats and groups, as the phone shows them. Never stories, Note to Self, reactions, calls or typing.
- Attachments are never downloaded: a message says what was sent ("Sent a photo"), and view-once media says only that.
- Edits replace the text, a deleted-for-everyone message loses its text, and a disappearing message loses its text
  when its timer is up, as on the phone.
- Never sends read receipts or typing: the owner's own apps show what they read.
- Sends only what the outbox holds, which the app writes for a message the owner approved with Send; one at a time, at
  least SEND_GAP seconds apart. A send that may have gone out is never sent again (status `sending` stays)."""
import argparse
import datetime as dt
import json
import queue
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import portable  # noqa: E402
import qr  # noqa: E402
import signal_store as ss  # noqa: E402

SEND_GAP = 20            # seconds between two sends, at least
LINK_WAIT = 600          # seconds a link waits for the code to be scanned
CODE_LIFE = 90           # about how long Signal keeps one link code; a new one follows
REFRESH = 6 * 3600       # how often the names of people and groups are read again
RPC_WAIT = 60            # seconds one JSON-RPC call waits for signal-cli
TEMPORARY = 75           # exit code: try again later (the service restarts it)
# signal-cli's receive errors that end this linked device, or this signal-cli version, for good
UNLINKED = ('AuthorizationFailedException', 'NotRegisteredException', 'UnregisteredUserException', 'DeviceNotFoundException')
OUTDATED = ('DeprecatedVersionException',)
IGNORE = ('--ignore-attachments', '--ignore-stories', '--ignore-avatars', '--ignore-stickers')


def emit(event, **data):
    print(json.dumps({'event': event, **data}), flush=True)


class RpcError(Exception):
    def __init__(self, error):
        super().__init__(str((error or {}).get('message') or 'signal-cli error')[:200])
        self.code = (error or {}).get('code')


class Rpc:
    """signal-cli's JSON-RPC over the child's stdin and stdout: call() waits for its answer, notifications() yields what
    signal-cli sends by itself (received messages). The child's stderr is read and dropped (it may name numbers)."""

    def __init__(self, command):
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        self.answers, self.events, self.next_id, self.lock = {}, queue.Queue(), 0, threading.Lock()
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=lambda: [None for _ in self.process.stderr], daemon=True).start()

    def _read(self):
        for line in self.process.stdout:
            try:
                data = json.loads(line)
            except ValueError:
                continue
            if isinstance(data, dict) and 'id' in data and data['id'] in self.answers:
                self.answers[data['id']].put(data)
            elif isinstance(data, dict) and data.get('method'):
                self.events.put(data)
        self.events.put(None)

    def alive(self):
        return self.process.poll() is None

    def call(self, method, params=None, wait=RPC_WAIT):
        with self.lock:
            self.next_id += 1
            ident = self.next_id
            box = self.answers[ident] = queue.Queue()
            try:
                self.process.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': method, 'id': ident, **({'params': params} if params else {})}) + '\n')
                self.process.stdin.flush()
            except (OSError, ValueError):
                self.answers.pop(ident, None)
                raise RpcError({'message': 'signal-cli stopped'}) from None
        try:
            answer = box.get(timeout=wait)
        except queue.Empty:
            raise RpcError({'message': 'timeout', 'code': 'timeout'}) from None
        finally:
            self.answers.pop(ident, None)
        if 'error' in answer:
            raise RpcError(answer['error'])
        return answer.get('result')

    def notification(self, wait):
        try:
            return self.events.get(timeout=wait)
        except queue.Empty:
            return False

    def close(self):
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.terminate()
            self.process.wait(15)
        except (OSError, subprocess.TimeoutExpired):
            self.process.kill()


def media_kind(message):
    """What a message without text sent, in a word or two: never the file itself."""
    if message.get('viewOnce'):
        return 'view-once media'
    if message.get('sticker'):
        return 'sticker'
    if message.get('contacts'):
        return 'contact'
    for item in message.get('attachments') or ():
        kind = str((item or {}).get('contentType') or '')
        if item.get('voiceNote'):
            return 'voice message'
        return 'photo' if kind.startswith('image/') else 'video' if kind.startswith('video/') else 'audio' if kind.startswith('audio/') else 'file'
    return ''


def display_name(contact):
    """A contact's name as the phone shows it, never their number."""
    profile = contact.get('profile') or {}
    for name in (contact.get('name'), contact.get('nickName'),
                 ' '.join(p for p in (profile.get('givenName'), profile.get('familyName')) if p),
                 ' '.join(p for p in (contact.get('givenName'), contact.get('familyName')) if p), contact.get('username')):
        if isinstance(name, str) and name.strip():
            return name.strip()[:200]
    return ''


class Mirror:
    """What arrives and what goes out, apart from signal-cli so it is tested with a stand-in `call`."""

    def __init__(self, call, store, seal, account, sleep=time.sleep, clock=time.monotonic):
        self.call, self.store, self.seal, self.account = call, Path(store), seal, account
        self.db = ss.connect(store)
        self.sleep, self.clock = sleep, clock
        self.last_send = -SEND_GAP
        self.names = {}

    def save_chat(self, chat_id, kind, name):
        if name:
            self.names[chat_id] = name
        ss.save_chat(self.db, self.seal, chat_id, kind, name)

    def refresh_names(self):
        """The names of people and groups, from signal-cli's contact and group lists (the phone syncs them). The
        account's own entry gives the name its Connections card goes by ("Sam’s Signal"), never its number."""
        own = ss.get_state(self.db)
        contacts = list(self.call('listContacts') or ())
        try:  # the account itself is no contact, so the plain list leaves it out: asked for by its number
            mine = list(self.call('listContacts', {'recipient': [self.account], 'allRecipients': True}) or ())
        except RpcError:
            mine = []
        # by its number: the ID getUserStatus gives for it can be its phone number identity, not the one listed here
        named = (display_name(c) for c in mine + contacts
                 if c.get('number') == self.account or (own.get('uuid') and c.get('uuid') == own.get('uuid')))
        name = next((n for n in named if n and n != self.account), '')
        if name and name[:100] != own.get('name'):
            ss.set_state(self.db, name=name[:100])
        for contact in contacts:
            uuid = str(contact.get('uuid') or '')
            if ss.re_person(uuid) and not contact.get('isBlocked'):
                self.save_chat(uuid, 'dm', display_name(contact))
        for group in self.call('listGroups') or ():
            gid = 'g:' + str(group.get('id') or '')
            if ss.re_chat(gid) and not group.get('isBlocked'):
                self.save_chat(gid, 'group', str(group.get('name') or '').strip()[:200] or 'Signal group')
        self.db.commit()
        ss.set_state(self.db, names_at=ss.now())

    def keep(self, chat_id, author, sent_at, from_me, sender, message, edited=False):
        text = message.get('message') if isinstance(message.get('message'), str) else ''
        media = media_kind(message)
        if message.get('viewOnce'):
            text = ''
        if not text and not media:
            return False
        seconds = message.get('expiresInSeconds') or 0
        expires = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=int(seconds))).isoformat(timespec='seconds') if seconds else None
        quote = message.get('quote') or {}
        if not sent_at:
            return False
        ss.keep_message(self.db, self.seal, {'chat_id': chat_id, 'author': author, 'sent_at': sent_at, 'from_me': from_me, 'sender': sender,
                                             'text': text, 'media': media, 'edited': edited, 'expires_at': expires,
                                             'quote_author': str(quote.get('authorUuid') or quote.get('author') or '') or None,
                                             'quote_sent_at': quote.get('id') if isinstance(quote.get('id'), int) else None})
        return True

    def removed(self, author, sent_at):
        """Deleted for everyone: the row stays, its text goes."""
        ss.remove_message(self.db, author, sent_at)

    def chat_of(self, message, peer):
        group = message.get('groupInfo') or {}
        if group.get('groupId'):
            gid = 'g:' + str(group['groupId'])
            if not ss.re_chat(gid):
                return None, None
            if gid not in self.names and not ss.known_chat(self.db, gid):
                self.save_chat(gid, 'group', str(group.get('groupName') or '') or 'Signal group')
            return gid, 'group'
        return (peer, 'dm') if ss.re_person(peer) else (None, None)

    def on_envelope(self, envelope):
        """One envelope from signal-cli: a message, an edit or a delete, from someone or from the owner's own phone."""
        source = str(envelope.get('sourceUuid') or '')
        name = str(envelope.get('sourceName') or '').strip()[:200]
        data, edit = envelope.get('dataMessage'), envelope.get('editMessage')
        sent = ((envelope.get('syncMessage') or {}).get('sentMessage'))
        if isinstance(sent, dict):
            peer = str(sent.get('destinationUuid') or '')
            if (peer and peer == self.own_uuid()) or (sent.get('destinationNumber') and sent.get('destinationNumber') == self.account):
                return False  # Note to Self
            inner = sent.get('editMessage') if isinstance(sent.get('editMessage'), dict) else None
            message = inner.get('dataMessage') if inner else sent
            chat, kind = self.chat_of(message or {}, peer)
            if not chat or not isinstance(message, dict):
                return False
            if message.get('remoteDelete'):
                self.removed('me', message['remoteDelete'].get('timestamp') or 0)
                return True
            if message.get('reaction') or message.get('isExpirationUpdate'):
                return False
            if kind == 'dm':
                self.save_chat(peer, 'dm', '')  # known as a chat, its name from the contact list
            target = inner.get('targetSentTimestamp') if inner else (sent.get('timestamp') or envelope.get('timestamp'))
            return self.keep(chat, 'me', target, True, 'You', message, edited=bool(inner))
        if isinstance(edit, dict) and isinstance(edit.get('dataMessage'), dict):
            message = edit['dataMessage']
            chat, kind = self.chat_of(message, source)
            if not chat:
                return False
            return self.keep(chat, source, edit.get('targetSentTimestamp') or 0, False, name or 'Unknown sender', message, edited=True)
        if not isinstance(data, dict) or not ss.re_person(source):
            return False
        if data.get('remoteDelete'):
            self.removed(source, data['remoteDelete'].get('timestamp') or 0)
            return True
        if data.get('reaction') or data.get('isExpirationUpdate') or ((data.get('groupInfo') or {}).get('type') == 'UPDATE' and not data.get('message')):
            return False
        chat, kind = self.chat_of(data, source)
        if not chat:
            return False
        if kind == 'dm':
            self.save_chat(source, 'dm', name)
        return self.keep(chat, source, data.get('timestamp') or envelope.get('timestamp') or 0, False, name or 'Unknown sender', data)

    def own_uuid(self):
        return ss.get_state(self.db).get('uuid')

    def on_notification(self, note):
        """A JSON-RPC notification. Returns a stop reason ('unlinked', 'outdated') when signal-cli says this device ended."""
        params = note.get('params') or {}
        if note.get('method') != 'receive':
            return None
        error = params.get('exception') or params.get('error')
        if isinstance(error, dict):
            kind = str(error.get('type') or '')
            return 'unlinked' if kind.endswith(UNLINKED) else 'outdated' if kind.endswith(OUTDATED) else None
        envelope = params.get('envelope') or (params.get('result') or {}).get('envelope')
        if isinstance(envelope, dict):
            self.on_envelope(envelope)
        return None

    def outbox(self):
        """The next queued send the owner approved: sent once, paced. Returns 'sent', 'failed' or None."""
        row = ss.next_outbox(self.db)
        if not row:
            return None
        done = lambda status, **values: ss.mark_outbox(self.db, row['id'], status, **values)
        if row['op'] != 'send' or not row['approval'] or not row['chat_id'] or not ss.re_chat(row['chat_id']):
            done('failed', error='not_approved')
            return 'failed'
        if not ss.known_chat(self.db, row['chat_id']):
            done('failed', error='chat_not_read')  # never a new chat
            return 'failed'
        wait = SEND_GAP - (self.clock() - self.last_send)
        if wait > 0:
            self.sleep(wait)
        self.sleep(random.uniform(1.0, 3.0))
        done('sending')
        text = self.seal.open(row['text'])
        params = {'message': text}
        if row['chat_id'].startswith('g:'):
            params['groupId'] = row['chat_id'][2:]
        else:
            params['recipient'] = [row['chat_id']]
        if row['quote_sent_at'] and row['quote_author']:
            params.update(quoteTimestamp=int(row['quote_sent_at']), quoteAuthor=self.account if row['quote_author'] == 'me' else row['quote_author'])
        self.last_send = self.clock()
        try:
            result = self.call('send', params) or {}
        except RpcError as error:
            done('failed', error=('rpc:' + str(error.code)) if error.code else 'refused')
            return 'failed'
        results = [r for r in result.get('results') or () if isinstance(r, dict)]
        if not isinstance(result.get('timestamp'), int) or (results and not any(r.get('type') == 'SUCCESS' for r in results)):
            done('failed', error=next((str(r.get('type'))[:60] for r in results if r.get('type') != 'SUCCESS'), 'refused'))
            return 'failed'
        self.keep(row['chat_id'], 'me', result['timestamp'], True, 'You', {'message': text})
        done('sent', sent_at=result['timestamp'])
        return 'sent'


def lock(store):
    handle = open(Path(ss.private_dir(store)) / ss.LOCK_NAME, 'a')
    try:
        portable.lock(handle, blocking=False)
    except BlockingIOError:
        handle.close()
        return None
    return handle


def program(args):
    """signal-cli: --cli, else this pin's build under --base (unpacked once; a new pin unpacks the new one)."""
    if args.cli:
        return args.cli
    import signal_release
    base = Path(args.base).expanduser()
    return str(signal_release.installed(base) or signal_release.install(base))


def link(rpc, store, seal, wait=LINK_WAIT, clock=time.monotonic):
    """Links this Machine as a device of the owner's Signal: a QR code to scan in Signal on the phone, Settings, Linked
    devices, Link new device. Signal's code lasts a minute or two; a new one follows until LINK_WAIT."""
    db = ss.connect(store)
    until = clock() + wait
    while True:
        uri = str((rpc.call('startLink') or {}).get('deviceLinkUri') or '')
        if not uri.startswith('sgnl://linkdevice?'):
            raise RuntimeError('no_code')
        emit('qr', matrix=qr.encode(uri), expires=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=CODE_LIFE)).isoformat(timespec='seconds'))
        try:
            result = rpc.call('finishLink', {'deviceLinkUri': uri, 'deviceName': ss.DEVICE}, wait=max(5, min(until - clock(), 300))) or {}
            break
        except RpcError:
            if clock() >= until:
                raise RuntimeError('qr_expired') from None
    number = str(result.get('number') or '')
    if not number:
        accounts = rpc.call('listAccounts') or []
        number = str((accounts[0] or {}).get('number') or '') if len(accounts) == 1 else ''
    if not number:
        raise RuntimeError('no_account')
    ss.set_state(db, identity=ss.identity(number), account=number, linked_at=ss.now(), error=None)
    emit('connected', identity=ss.identity(number))


def follow(rpc, mirror, refresh=REFRESH, clock=time.monotonic):
    """Keeps the store in step until Signal ends this linked device, or signal-cli stops (then the service restarts it)."""
    db = mirror.db
    try:  # the owner's own account ID, so Note to Self stays out
        own = [s for s in rpc.call('getUserStatus', {'recipient': [mirror.account]}) or () if isinstance(s, dict)]
        if own and ss.re_person(own[0].get('uuid')):
            ss.set_state(db, uuid=own[0]['uuid'])
    except RpcError:
        pass
    try:
        mirror.refresh_names()
    except RpcError:
        pass
    ss.set_state(db, error=None, last_ok=ss.now())
    refreshed = beat = tick = clock()
    while rpc.alive():
        note = rpc.notification(1)
        if note is None:
            break
        if note:
            reason = mirror.on_notification(note)
            if reason:
                ss.set_state(db, error=reason)
                return 0
        if clock() - tick < 2:
            continue
        tick = clock()
        mirror.outbox()
        ss.purge_expired(db)
        if clock() - refreshed > refresh:
            try:
                mirror.refresh_names()
            except RpcError:
                pass
            refreshed = clock()
        if clock() - beat > 60:
            ss.set_state(db, last_ok=ss.now())
            beat = clock()
    return TEMPORARY


def run(args):
    cli = program(args)
    if args.command == 'version':
        out = subprocess.run([cli, '--version'], capture_output=True, text=True, timeout=120)
        print(json.dumps({'signal-cli': out.stdout.strip().split()[-1] if out.stdout.strip() else ''}))
        return 0
    store = Path(args.store).expanduser()
    held = lock(store)
    if held is None:
        emit('error', code='busy')
        return TEMPORARY if args.command == 'follow' else 3
    db = ss.connect(store)
    try:
        seal = ss.sealer(store, args.database)
    except Exception:  # noqa: BLE001 - another Machine's key
        ss.set_state(db, error='store_unreadable')
        return 0
    config = str(ss.cli_dir(store))
    if args.command == 'logout':
        ss.forget_link(store)
        ss.set_state(db, error='logged_out')
        emit('logged_out')
        return 0
    if args.command == 'link':
        ss.forget_link(store)  # a new link starts clean: never two devices in one folder
        rpc = Rpc([cli, '--config', str(ss.cli_dir(store)), '-o', 'json', 'jsonRpc'])
        try:
            link(rpc, store, seal)
        except (RuntimeError, RpcError) as error:
            emit('error', code=str(error)[:60])
            return 1
        finally:
            rpc.close()
        return 0
    state = ss.get_state(db)
    if not state.get('account') or state.get('error') in (*ss.ERRORS, 'logged_out', 'outdated'):
        return 0  # nothing to follow, or stopped for a reason only the owner can fix: never retried by itself
    rpc = Rpc([cli, '--config', config, '-a', state['account'], '-o', 'json', 'jsonRpc', *IGNORE, '--receive-mode', 'on-start'])
    mirror = Mirror(rpc.call, store, seal, state['account'])
    try:
        result = follow(rpc, mirror)
    finally:
        rpc.close()
    if ss.get_state(db).get('error') == 'unlinked':
        ss.forget_link(store)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='The Signal mirror of The Machine')
    parser.add_argument('--store')
    parser.add_argument('--cli', help='signal-cli to run (else the pinned build under --base)')
    parser.add_argument('--base', default='~/.local/share/personal-assistant/signal-cli', help='where the pinned signal-cli is unpacked')
    parser.add_argument('--database', help="The Machine's database, whose message key seals the store")
    parser.add_argument('command', choices=('link', 'follow', 'logout', 'version'))
    args = parser.parse_args(argv)
    if args.command != 'version' and not args.store:
        parser.error('--store is needed')
    try:
        return run(args)
    except (OSError, RuntimeError) as error:
        emit('error', code='signal_cli', message=str(error)[:200])
        return TEMPORARY


if __name__ == '__main__':
    sys.exit(main())
