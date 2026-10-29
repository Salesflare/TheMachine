"""Telegram chats: the pinned libraries, the store's chat filter, the mirror's login, reads and sends with a stand-in
Telethon client, the collector, and the approve-before-send path. Nothing here talks to Telegram or PyPI."""
import asyncio
import datetime as dt
import hashlib
import importlib.util
import io
import json
import sys
import tarfile
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import next_actions as n  # noqa: E402
import telegram_mirror as tm  # noqa: E402
import telegram_release as tr  # noqa: E402
import telegram_store as ts  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_tg', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

NOW = dt.datetime.now(dt.timezone.utc)


def no_sleep(*_):
    async def done():
        return None
    return done()


# ---------------------------------------------------------------- the pinned libraries

class Libraries(unittest.TestCase):
    def test_the_requirements_file_lists_exactly_the_pin(self):
        lines = [line for line in tr.REQUIREMENTS.read_text().splitlines() if line and not line.startswith('#')]
        self.assertEqual(lines, tr.requirements(tr.pin()))
        for package in tr.pin()['packages']:
            self.assertTrue(package['url'].startswith('https://files.pythonhosted.org/'))
            self.assertRegex(package['sha256'], r'^[0-9a-f]{64}$')
        self.assertEqual(tr.version(), '1.45.0')

    def wheel(self, files):
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as archive:
            for name, text in files.items():
                archive.writestr(name, text)
        return out.getvalue()

    def sdist(self, files):
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode='w:gz') as archive:
            for name, text in files.items():
                data = text.encode()
                info = tarfile.TarInfo(name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        return out.getvalue()

    def test_install_checks_every_file_before_unpacking_anything_and_only_unpacks_package_folders(self):
        good = self.wheel({'lib/__init__.py': 'X = 1\n', 'lib-1.dist-info/METADATA': 'x', '../evil.py': 'bad', 'other/x.py': 'no'})
        source = self.sdist({'aes-1/aes/__init__.py': 'Y = 2\n', 'aes-1/setup.py': 'raise SystemExit', 'aes-1/../../up.py': 'bad'})
        data = {'packages': [
            {'name': 'lib', 'version': '1', 'license': 'MIT', 'packages': ['lib'], 'url': 'https://files.pythonhosted.org/lib.whl',
             'sha256': hashlib.sha256(good).hexdigest()},
            {'name': 'aes', 'version': '1', 'license': 'MIT', 'packages': ['aes'], 'url': 'https://files.pythonhosted.org/aes.tar.gz',
             'sha256': hashlib.sha256(source).hexdigest()}]}
        blobs = {'https://files.pythonhosted.org/lib.whl': good, 'https://files.pythonhosted.org/aes.tar.gz': source}
        with tempfile.TemporaryDirectory() as base:
            path = tr.install(base, data, fetch=blobs.__getitem__)
            self.assertEqual(sorted(p.relative_to(path).as_posix() for p in path.rglob('*') if p.is_file()),
                             ['.complete', 'NOTICE', 'aes/__init__.py', 'lib/__init__.py'])
            self.assertEqual(tr.installed(base, data), path)
            self.assertFalse((Path(base).parent / 'evil.py').exists())
            # A changed file: nothing is unpacked, and the earlier install stays
            tampered = json.loads(json.dumps(data))
            tampered['packages'][1]['sha256'] = '0' * 64
            with self.assertRaisesRegex(RuntimeError, 'did not match'):
                tr.install(base, tampered, fetch=blobs.__getitem__)
            self.assertIsNone(tr.installed(base, tampered))
            self.assertTrue(path.exists())

    def test_downloads_only_from_pypi(self):
        with self.assertRaises(RuntimeError):
            tr._fetch('https://example.com/telethon.whl')


# ---------------------------------------------------------------- the store

class Store(unittest.TestCase):
    def test_reads_private_chats_and_small_groups_only(self):
        read = lambda **chat: ts.readable({'id': '5', 'kind': 'dm', 'members': 2, 'muted': False, 'archived': False, **chat})
        self.assertEqual(read(), '')
        self.assertEqual(read(kind='group', members=50), '')
        self.assertEqual(read(kind='group', members=51), 'big_group')
        self.assertEqual(read(kind='channel'), 'channel')
        self.assertEqual(read(kind='bot'), 'bot')
        self.assertEqual(read(kind='self'), 'self')
        self.assertEqual(read(id='777000'), 'service')  # Telegram's login codes
        self.assertEqual(read(muted=True), 'muted')
        self.assertEqual(read(archived=True), 'archived')
        self.assertEqual(ts.readable({'id': '5', 'kind': 'group', 'members': 400, 'muted': True}, include=['5']), '')
        self.assertEqual(ts.readable({'id': '-100', 'kind': 'channel'}, include=['-100']), 'channel')  # never, even listed

    def test_session_is_sealed_private_and_needs_the_key(self):
        with tempfile.TemporaryDirectory() as store:
            seal = ts.sealer(store)
            ts.save_session(store, seal, 'SESSION-TEXT')
            raw = (Path(store) / ts.SESSION_NAME).read_bytes()
            self.assertNotIn(b'SESSION-TEXT', raw)
            self.assertEqual((Path(store) / ts.SESSION_NAME).stat().st_mode & 0o777, 0o600)
            self.assertEqual((Path(store) / ts.OWN_KEY).stat().st_mode & 0o777, 0o600)
            self.assertEqual(ts.load_session(store, ts.sealer(store)), 'SESSION-TEXT')
            other = tempfile.mkdtemp()
            with self.assertRaises(Exception):
                ts.load_session(store, ts.sealer(other))
            ts.forget_session(store)
            self.assertIsNone(ts.load_session(store, seal))

    def test_app_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'app.env'
            path.write_text('TELEGRAM_API_ID=12345\nTELEGRAM_API_HASH=' + 'a' * 32 + '\n')
            self.assertEqual(ts.read_app(path), (12345, 'a' * 32))
            path.write_text('TELEGRAM_API_ID=12345\nTELEGRAM_API_HASH=short\n')
            self.assertIsNone(ts.read_app(path))
            self.assertIsNone(ts.read_app(Path(folder) / 'missing'))


# ---------------------------------------------------------------- the mirror, with a stand-in Telethon

class SessionPasswordNeededError(Exception):
    pass


class PasswordHashInvalidError(Exception):
    pass


class PhoneCodeInvalidError(Exception):
    pass


class AuthKeyUnregisteredError(Exception):
    pass


class PhoneCodeExpiredError(Exception):
    pass


class PhoneCodeEmptyError(Exception):
    pass


class SentCodeTypeApp:
    pass


class SentCodeTypeSms:
    pass


class SentCodeTypeEmailCode:
    def __init__(self, pattern):
        self.email_pattern = pattern


class SentCodeTypeSetUpEmailRequired:
    pass


class FloodWaitError(Exception):
    def __init__(self, seconds):
        super().__init__('flood')
        self.seconds = seconds


def fake_telethon():
    errors = types.SimpleNamespace(SessionPasswordNeededError=SessionPasswordNeededError, PasswordHashInvalidError=PasswordHashInvalidError,
                                   PhoneCodeInvalidError=PhoneCodeInvalidError, PhoneCodeExpiredError=PhoneCodeExpiredError,
                                   PhoneCodeEmptyError=PhoneCodeEmptyError)
    account = types.ModuleType('telethon.tl.functions.account')
    account.GetPasswordRequest = lambda: 'get-password'
    account.UpdateStatusRequest = lambda offline: ('status', offline)
    auth = types.ModuleType('telethon.tl.functions.auth')
    auth.ResendCodeRequest = lambda phone, code_hash: ('resend', phone, code_hash)
    telethon = types.ModuleType('telethon')
    telethon.errors = errors
    return {'telethon': telethon, 'telethon.tl': types.ModuleType('telethon.tl'), 'telethon.tl.functions': types.ModuleType('telethon.tl.functions'),
            'telethon.tl.functions.account': account, 'telethon.tl.functions.auth': auth}


class QR:
    def __init__(self, outcomes):
        self.outcomes, self.url, self.renewed = list(outcomes), 'tg://login?token=one', 0
        self.expires = NOW + dt.timedelta(seconds=30)

    async def wait(self, timeout=None):
        outcome = self.outcomes.pop(0)
        if outcome:
            raise outcome

    async def recreate(self):
        self.renewed += 1
        self.url = 'tg://login?token=two'


class LoginClient:
    def __init__(self, qr=None, password='right', code='12345', sent=None, resent=None):
        self.qr, self.password, self.code, self.calls = qr, password, code, []
        self.sent, self.resent = sent or SentCodeTypeApp(), resent
        self.session = types.SimpleNamespace(save=lambda: 'SESSION')

    async def connect(self):
        self.calls.append('connect')

    async def disconnect(self):
        self.calls.append('disconnect')

    async def qr_login(self):
        return self.qr

    async def __call__(self, request):
        self.calls.append(request)
        if isinstance(request, tuple) and request[0] == 'resend':
            if isinstance(self.resent, Exception):
                raise self.resent
            return types.SimpleNamespace(phone_code_hash='hash2', type=self.resent or SentCodeTypeSms(), next_type=None, timeout=None)
        return types.SimpleNamespace(hint='pet')

    async def send_code_request(self, phone):
        self.calls.append(('code', phone))
        return types.SimpleNamespace(phone_code_hash='hash', type=self.sent, next_type=SentCodeTypeSms(), timeout=60)

    async def sign_in(self, phone=None, code=None, password=None, phone_code_hash=None):
        if password is not None:
            self.calls.append('password')
            if password != self.password:
                raise PasswordHashInvalidError()
            return
        self.calls.append(('sign_in', code))
        if code != self.code:
            raise PhoneCodeInvalidError()
        if self.password:
            raise SessionPasswordNeededError()

    async def get_me(self):
        return types.SimpleNamespace(id=4242, first_name='Alex', last_name='Morgan')


class Login(unittest.TestCase):
    def setUp(self):
        self.store = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.store, True)
        self.seal = ts.sealer(self.store)
        self.out = []
        modules = patch.dict(sys.modules, fake_telethon())
        modules.start()
        self.addCleanup(modules.stop)
        emit = patch.object(tm, 'emit', side_effect=lambda event, **data: self.out.append({'event': event, **data}))
        emit.start()
        self.addCleanup(emit.stop)
        matrix = patch.object(tm, 'qr_matrix', return_value=['101', '010', '101'])
        matrix.start()
        self.addCleanup(matrix.stop)

    def test_qr_login_with_a_renewed_code_and_a_cloud_password_that_is_never_kept(self):
        answers = iter(['wrong', 'right'])
        client = LoginClient(QR([asyncio.TimeoutError(), SessionPasswordNeededError()]))
        asyncio.run(tm.login(client, self.store, self.seal, ask=lambda field: next(answers)))
        events = [e['event'] for e in self.out]
        self.assertEqual(events, ['qr', 'qr', 'password', 'password_wrong', 'password', 'connected'])
        self.assertEqual(self.out[0]['matrix'], ['101', '010', '101'])
        self.assertEqual(client.qr.renewed, 1)
        self.assertEqual(self.out[-1]['identity'], ts.identity(4242))
        self.assertEqual(ts.load_session(self.store, self.seal), 'SESSION')
        with ts.connect(self.store) as db:
            self.assertEqual(ts.get_state(db)['identity'], ts.identity(4242))
        on_disk = b''.join(p.read_bytes() for p in Path(self.store).rglob('*') if p.is_file())
        self.assertNotIn(b'right', on_disk)
        self.assertNotIn('right', json.dumps(self.out))

    def test_code_by_phone(self):
        answers = iter(['00000', '12345', 'right'])
        client = LoginClient(password='right')
        asyncio.run(tm.login(client, self.store, self.seal, phone='+32470000000', ask=lambda field: next(answers)))
        self.assertEqual([e['event'] for e in self.out], ['code_sent', 'code_wrong', 'password', 'connected'])
        self.assertIn(('code', '+32470000000'), client.calls)
        self.assertEqual({k: self.out[0][k] for k in ('via', 'next', 'wait')}, {'via': 'app', 'next': 'sms', 'wait': 60})

    def test_the_owner_hears_where_the_code_went_and_can_have_it_sent_again(self):
        answers = iter([tm.RESEND, '12345', 'right'])
        client = LoginClient(password='right', sent=SentCodeTypeEmailCode('j***@example.com'))
        asyncio.run(tm.login(client, self.store, self.seal, phone='+32470000000', ask=lambda field: next(answers)))
        self.assertEqual([e['event'] for e in self.out], ['code_sent', 'code_sent', 'password', 'connected'])
        self.assertEqual((self.out[0]['via'], self.out[0]['to']), ('email', 'j***@example.com'))
        self.assertEqual((self.out[1]['via'], self.out[1]['again']), ('sms', True))
        self.assertIn(('resend', '+32470000000', 'hash'), client.calls)
        self.assertIn(('sign_in', '12345'), client.calls)
        self.assertNotIn('12345', json.dumps(self.out))

    def test_a_refused_resend_and_an_expired_code_keep_the_login_going(self):
        answers = iter([tm.RESEND, 'old', '12345', 'right'])
        client = LoginClient(password='right', resent=FloodWaitError(120))
        expired = iter([True])

        async def sign_in(phone=None, code=None, password=None, phone_code_hash=None, original=client.sign_in):
            if code == 'old' and next(expired, False):
                raise PhoneCodeExpiredError()
            return await original(phone=phone, code=code, password=password, phone_code_hash=phone_code_hash)
        client.sign_in = sign_in
        asyncio.run(tm.login(client, self.store, self.seal, phone='+32470000000', ask=lambda field: next(answers)))
        self.assertEqual([e['event'] for e in self.out], ['code_sent', 'code_resend_failed', 'code_expired', 'password', 'connected'])
        self.assertEqual(self.out[1], {'event': 'code_resend_failed', 'reason': 'FloodWaitError', 'wait': 120})

    def test_no_code_until_a_login_email_is_set_up_is_said_not_waited_for(self):
        client = LoginClient(sent=SentCodeTypeSetUpEmailRequired())
        with self.assertRaisesRegex(RuntimeError, 'email_setup_required'):
            asyncio.run(tm.login(client, self.store, self.seal, phone='+32470000000', ask=lambda field: self.fail('asked for a code')))
        self.assertEqual(self.out, [])

    def test_three_wrong_passwords_stop_without_a_session(self):
        client = LoginClient(QR([SessionPasswordNeededError()]))
        with self.assertRaisesRegex(RuntimeError, 'password_wrong'):
            asyncio.run(tm.login(client, self.store, self.seal, ask=lambda field: 'nope'))
        self.assertIsNone(ts.load_session(self.store, self.seal))

    def test_the_login_reads_answers_as_json_lines(self):
        self.assertEqual(tm.read_answer('code', io.StringIO('{"code": "123"}\n')), '123')
        self.assertEqual(tm.read_answer('code', io.StringIO('not json\n')), '')
        self.assertEqual(tm.read_answer('code', io.StringIO('{"resend": true}\n')), tm.RESEND)


class Message:
    def __init__(self, mid, text, minutes=10, out=False, sender_id=7, first='Sam', media=None, action=None):
        self.id, self.message, self.out, self.sender_id, self.media, self.action = mid, text, out, sender_id, media, action
        self.date = NOW - dt.timedelta(minutes=minutes)
        self.sender = types.SimpleNamespace(first_name=first, last_name=None, username=None)
        self.edit_date, self.reply_to_msg_id, self.photo = None, None, media


def entity(kind, eid, **fields):
    return type(kind, (), {'id': eid, **fields})()


def dialog(ent, minutes=5, muted=False, archived=False):
    until = NOW + dt.timedelta(days=1) if muted else None
    return types.SimpleNamespace(entity=ent, id=None, date=NOW - dt.timedelta(minutes=minutes), archived=archived, folder_id=1 if archived else None,
                                 dialog=types.SimpleNamespace(notify_settings=types.SimpleNamespace(mute_until=until)))


class MirrorClient:
    def __init__(self, dialogs, history=None, fail=None):
        self.dialogs, self.history, self.fail, self.sent, self.logged_out = dialogs, history or {}, fail, [], False

    async def iter_dialogs(self, **_):
        for d in self.dialogs:
            yield d

    async def iter_messages(self, chat, limit=None):
        for message in self.history.get(chat, []):
            yield message

    async def send_message(self, chat, text, link_preview=True):
        if self.fail:
            raise self.fail
        self.sent.append((chat, text, link_preview))
        return Message(900 + len(self.sent), text, minutes=0, out=True)

    async def log_out(self):
        self.logged_out = True


class Mirroring(unittest.TestCase):
    def setUp(self):
        self.store = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.store, True)
        self.seal = ts.sealer(self.store)
        sam = entity('User', 7, first_name='Sam', last_name='Whitlock', bot=False, is_self=False)
        family = entity('Chat', 20, title='Family', participants_count=5)
        big = entity('Channel', 30, title='Neighborhood', megagroup=True, participants_count=900)
        news = entity('Channel', 40, title='News', megagroup=False, participants_count=10)
        quiet = entity('User', 8, first_name='Muted', bot=False, is_self=False)
        bot = entity('User', 9, first_name='Bot', bot=True, is_self=False)
        old = entity('User', 10, first_name='Old', bot=False, is_self=False)
        self.client = MirrorClient(
            [dialog(sam), dialog(family), dialog(big), dialog(news), dialog(quiet, muted=True), dialog(bot), dialog(old, minutes=60 * 24 * 30)],
            {7: [Message(3, 'Still on for Saturday?', 5), Message(2, 'Hi', 60 * 24 * 3), Message(1, 'Long ago', 60 * 24 * 9)],
             -20: [Message(5, 'Dinner at 7', 30, sender_id=11, first='Robin')]})
        self.mirror = tm.Mirror(self.client, self.store, self.seal, sleep=no_sleep)

    def rows(self, sql, *args):
        return [dict(r) for r in self.mirror.db.execute(sql, args)]

    def test_reads_the_last_week_of_the_chats_it_reads_and_skips_the_rest(self):
        seen = asyncio.run(self.mirror.refresh_chats())
        asyncio.run(self.mirror.backfill(seen))
        skipped = {r['id']: r['skipped'] for r in self.rows('SELECT id, skipped FROM chats')}
        self.assertEqual(skipped, {'7': '', '-20': '', str(-(10 ** 12) - 30): 'big_group', str(-(10 ** 12) - 40): 'channel',
                                   '8': 'muted', '9': 'bot', '10': ''})
        kept = [(r['chat_id'], r['msg_id']) for r in self.rows('SELECT chat_id, msg_id FROM messages ORDER BY chat_id, msg_id')]
        self.assertEqual(kept, [('-20', 5), ('7', 2), ('7', 3)])  # not the 9-day-old one, nothing from skipped chats
        raw = (Path(self.store) / ts.DB_NAME).read_bytes()
        self.assertNotIn(b'Saturday', raw)  # sealed
        self.assertTrue(ts.get_state(self.mirror.db)['backfilled_at'])

    def test_live_messages_edits_and_deletions(self):
        asyncio.run(self.mirror.refresh_chats())
        self.assertTrue(asyncio.run(self.mirror.on_message(7, Message(4, 'See you'))))
        self.assertFalse(asyncio.run(self.mirror.on_message(8, Message(6, 'muted chat'))))
        self.assertFalse(asyncio.run(self.mirror.on_message(7, Message(7, '', action='joined'))))
        edited = Message(4, 'See you at 10')
        edited.edit_date = NOW
        asyncio.run(self.mirror.on_message(7, edited))
        self.mirror.on_deleted(None, [4])
        row = self.rows('SELECT * FROM messages WHERE msg_id=4')[0]
        self.assertEqual((row['edited'], row['deleted'], row['text']), (1, 1, None))

    def queue(self, key, chat='7', approval='job', op='send', text='Yes, I am in'):
        self.mirror.db.execute('INSERT INTO outbox(id, op, chat_id, text, approval, created_at) VALUES (?,?,?,?,?,?)',
                               (key, op, chat, self.seal.seal(text), approval, ts.now()))
        self.mirror.db.commit()

    def status(self, key):
        return self.rows('SELECT status, msg_id, error FROM outbox WHERE id=?', key)[0]

    def test_sends_only_approved_rows_into_chats_it_reads_paced(self):
        asyncio.run(self.mirror.refresh_chats())
        waits = []

        async def sleep(seconds):
            waits.append(seconds)
        self.mirror.sleep = sleep
        self.queue('no-approval', approval=None)
        self.queue('channel', chat=str(-(10 ** 12) - 40))
        self.queue('one')
        self.queue('two', text='Second')
        for _ in range(4):
            asyncio.run(self.mirror.outbox())
        self.assertEqual(self.status('no-approval')['error'], 'not_approved')
        self.assertEqual(self.status('channel')['error'], 'chat_not_read')
        self.assertEqual(self.status('one')['status'], 'sent')
        self.assertEqual(self.client.sent, [(7, 'Yes, I am in', False), (7, 'Second', False)])
        self.assertGreaterEqual(max(waits), tm.SEND_GAP - 1)  # the second send waited for the gap
        self.assertIsNone(asyncio.run(self.mirror.outbox()))

    def test_a_refused_send_is_said_and_never_retried_and_a_lost_session_stops_the_mirror(self):
        asyncio.run(self.mirror.refresh_chats())
        self.client.fail = FloodWaitError(300)
        self.queue('one')
        self.assertEqual(asyncio.run(self.mirror.outbox()), 'failed')
        self.assertEqual(self.status('one')['error'], 'flood_wait:300')
        self.client.fail = AuthKeyUnregisteredError()
        self.queue('two')
        with self.assertRaises(AuthKeyUnregisteredError):
            asyncio.run(self.mirror.outbox())
        self.assertEqual(self.status('two')['status'], 'sending')  # an unclear outcome stays as it is: never sent again
        self.assertIsNone(asyncio.run(self.mirror.outbox()))

    def test_a_logout_row_logs_out_at_telegram_and_forgets_the_session(self):
        ts.save_session(self.store, self.seal, 'SESSION')
        self.queue('bye', op='logout', chat=None, approval=None)
        self.assertEqual(asyncio.run(self.mirror.outbox()), 'logout')
        self.assertTrue(self.client.logged_out)
        self.assertIsNone(ts.load_session(self.store, self.seal))
        self.assertEqual(ts.get_state(self.mirror.db)['error'], 'logged_out')

    def test_a_stopped_mirror_never_reconnects_by_itself(self):
        ts.save_session(self.store, self.seal, 'SESSION')
        ts.set_state(self.mirror.db, error='app_blocked')
        app = Path(self.store) / 'app.env'
        app.write_text('TELEGRAM_API_ID=1\nTELEGRAM_API_HASH=' + 'b' * 32 + '\n')
        args = types.SimpleNamespace(command='follow', store=self.store, app=str(app), database=None, include='', phone=None)
        with patch.object(tm, 'client_for', side_effect=AssertionError('connected')):
            self.assertEqual(tm.run(args), 0)


# ---------------------------------------------------------------- the collector

ACCOUNT = {'id': 'home-telegram', 'service': 'telegram', 'transport': 'telegram_mirror', 'identity_sha256': ts.identity(4242),
           'boundary': 'personal:telegram'}


def mirror_store(folder, error=None):
    """A store as the mirror leaves it: Sam's private chat with two messages and a muted chat."""
    seal = ts.sealer(folder)
    db = ts.connect(folder)
    ts.set_state(db, identity=ts.identity(4242), error=error)
    for cid, kind, name, skipped in (('7', 'dm', 'Sam Whitlock', ''), ('8', 'dm', 'Muted', 'muted')):
        db.execute('INSERT INTO chats(id, kind, name, skipped, updated_at) VALUES (?,?,?,?,?)', (cid, kind, seal.seal(name), skipped, ts.now()))
    for cid, mid, mine, text in (('7', 1, 0, 'Still on for climbing Saturday?'), ('7', 2, 1, 'Probably'), ('8', 3, 0, 'quiet'),
                                 ('7', 4, 0, 'Your login code: 12345')):
        db.execute('INSERT INTO messages(chat_id, msg_id, from_me, sender_id, sender_name, text, occurred_at) VALUES (?,?,?,?,?,?,?)',
                   (cid, mid, mine, None if mine else '7', seal.seal('You' if mine else 'Sam Whitlock'), seal.seal(text), ts.now()))
    db.commit()
    db.close()
    return {**ACCOUNT, 'store': folder}


class Collector(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = str(Path(self.tmp.name) / 'tg')
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')

    def test_reads_the_store_without_talking_to_telegram(self):
        account = mirror_store(self.folder)
        result = a.sync_telegram(self.store, {}, account)
        self.assertEqual(result['events'], 3)
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute("SELECT * FROM events WHERE kind='telegram.message' ORDER BY occurred_at")]
        bodies = sorted(a.json.loads(r['metadata'])['message_id'] for r in rows)
        self.assertEqual(bodies, [1, 2, 4])
        event = a.telegram_event(account, {'chat_id': '7', 'msg_id': 4, 'from_me': 0, 'text': 'Your login code: 12345', 'occurred_at': ts.now(),
                                           'chat_name': 'Sam Whitlock', 'chat_kind': 'dm', 'sender_name': 'Sam Whitlock'})
        self.assertEqual(event['body'], '[One-time security code omitted]')
        mine = a.telegram_event(account, {'chat_id': '7', 'msg_id': 2, 'from_me': 1, 'text': 'Probably', 'occurred_at': ts.now(), 'chat_name': 'Sam Whitlock'})
        self.assertEqual((mine['metadata']['from'], mine['metadata']['sender_id']), ('You', None))

    def test_a_stop_is_said_never_a_silent_gap(self):
        for error, label in (('app_blocked', 'telegram_app_blocked'), ('signed_out', 'telegram_logged_out'), ('logged_out', 'telegram_logged_out')):
            folder = tempfile.mkdtemp(dir=self.tmp.name)
            with self.assertRaisesRegex(a.SourceError, label):
                a.Telegram({}, mirror_store(folder, error)).profile()
        with self.assertRaisesRegex(a.SourceError, 'account_identity_mismatch'):
            a.Telegram({}, {**mirror_store(tempfile.mkdtemp(dir=self.tmp.name)), 'identity_sha256': 'other'}).profile()
        with self.assertRaisesRegex(a.SourceError, 'telegram_source_unavailable'):
            a.Telegram({}, {**ACCOUNT, 'store': str(Path(self.tmp.name) / 'none')}).profile()


# ---------------------------------------------------------------- approve before send

class Sending(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.account = mirror_store(str(Path(self.tmp.name) / 'tg'))
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        a.sync_telegram(self.store, {}, self.account)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM events WHERE kind='telegram.message'")]
        self.sid = self.store.suggest('tg-task', 'Answer Sam', 'Sam asks about Saturday.', ids)['id']
        self.config = {'accounts': [self.account, {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog'}]}

    def app(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        return app

    def row(self):
        return self.store.snapshot([])['suggestions'][0]

    def save(self, **draft):
        action = {k: v for k, v in {'kind': 'telegram', 'label': 'Send reply', 'account_id': self.account['id'], 'chat_id': '7',
                                    'body': 'Yes, I am in for 10.', **draft}.items() if v is not None}
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})

    def ready(self, **draft):
        self.store.decide(self.sid, 'accept', '', 'accept', 'dashboard')
        self.save(**draft)
        return self.row()['next_action']

    def confirm(self, key='owner-approval'):
        action = self.row()['next_action']
        return self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': key},
                                 owner_dashboard=True)

    def jobs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM action_jobs')]

    def outbox(self):
        with ts.connect(self.account['store']) as db:
            return [dict(r) for r in db.execute('SELECT * FROM outbox')]

    def test_a_reply_only_into_a_chat_the_mirror_reads(self):
        action = self.ready()
        self.assertEqual((action['chat_id'], action['to_name'], action['max_length']), ('7', 'Sam Whitlock', 4096))
        self.assertEqual(n.preview(action), 'Telegram message to Sam Whitlock\n\nYes, I am in for 10.')
        for bad in ({'chat_id': '8'}, {'chat_id': '999'}, {'account_id': 'work'}, {'label': 'Post it'}, {'body': 'a' * 4097},
                    {'body': ' '}, {'media': ['a.png']}):
            with self.assertRaises(ValueError, msg=bad):
                self.save(**bad)

    def test_nothing_reaches_the_outbox_without_the_owners_approval(self):
        self.ready()
        transport = n.TelegramTransport(self.config, sleep=lambda _: None)
        self.assertIsNone(self.app().action_step(transport))  # no approved job: nothing to do
        self.assertEqual(self.jobs(), [])
        self.assertEqual(self.outbox(), [])
        with self.assertRaises(ValueError):  # the agent can't send by itself
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'send_now': True,
                                          'next_action': {'kind': 'telegram', 'account_id': self.account['id'], 'chat_id': '7', 'body': 'Yes'}})
        self.assertEqual(self.outbox(), [])

    def test_an_approved_reply_goes_to_the_outbox_once_and_the_mirrors_answer_returns(self):
        self.ready()
        self.confirm()
        self.confirm('second-click')
        clock = iter(range(0, 1000, 5))
        transport = n.TelegramTransport(self.config, sleep=lambda _: self.mirror_sends(), clock=lambda: next(clock))
        self.assertEqual(self.app().action_step(transport), 'sent')
        rows = self.outbox()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['approval'], self.jobs()[0]['id'])
        self.assertEqual(ts.sealer(self.account['store']).open(rows[0]['text']), 'Yes, I am in for 10.')
        self.assertIsNone(self.app().action_step(transport))
        self.assertEqual(len(self.outbox()), 1)
        self.assertIn('Telegram message sent', str(a.card(self.row())))

    def mirror_sends(self):
        with ts.connect(self.account['store']) as db:
            db.execute("UPDATE outbox SET status='sent', msg_id=99 WHERE status='queued'")

    def test_an_unclear_outcome_is_checked_never_resent(self):
        self.ready()
        self.confirm()
        clock = iter(range(0, 10000, 60))
        transport = n.TelegramTransport(self.config, sleep=lambda _: None, clock=lambda: next(clock))
        self.app().action_step(transport)
        self.assertEqual(self.jobs()[0]['status'], 'uncertain')
        self.mirror_sends()
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET retry_at=NULL')
        self.app().action_step(transport)
        self.assertEqual(self.jobs()[0]['status'], 'sent')
        self.assertEqual(len(self.outbox()), 1)

    def test_a_stopped_mirror_blocks_the_send(self):
        self.ready()
        self.confirm()
        with ts.connect(self.account['store']) as db:
            ts.set_state(db, error='app_blocked')
        transport = n.TelegramTransport(self.config, sleep=lambda _: None)
        self.assertEqual(self.app().action_step(transport), 'blocked')
        self.assertEqual(self.outbox(), [])
        self.assertIn('app ID', self.jobs()[0]['error'])


# ---------------------------------------------------------------- setup and disconnect

class Setup(unittest.TestCase):
    def test_disconnect_logs_out_at_telegram_and_deletes_the_store(self):
        import onboarding
        with tempfile.TemporaryDirectory() as home:
            store = Path(home) / 'tg'
            mirror_store(str(store))
            config = {'database': str(Path(home) / 'events.sqlite'), 'accounts': [{**ACCOUNT, 'store': str(store)}]}
            path = Path(home) / 'config.json'
            path.write_text(json.dumps(config))
            ran = []
            with patch.object(onboarding, 'run', side_effect=lambda args, **kw: ran.append(args) or types.SimpleNamespace(returncode=0, stdout='')), \
                 patch.object(onboarding, 'home', return_value=Path(home)), patch.object(onboarding.service, 'available', return_value=False):
                onboarding.disconnect(path, ACCOUNT['id'])
            self.assertTrue(any(args[-1] == 'logout' and 'telegram_mirror.py' in args[1] for args in ran))
            self.assertFalse(store.exists())
            self.assertEqual(json.loads(path.read_text())['accounts'], [])

    def test_the_form_asks_for_an_own_app_id_only_without_one(self):
        import onboarding
        with tempfile.TemporaryDirectory() as home:
            config = {'database': str(Path(home) / 'events.sqlite'), 'accounts': []}
            form = onboarding.web_form(config, 'telegram')
            self.assertEqual(form['secret'], onboarding.TELEGRAM_SECRET)
            self.assertTrue(form['personal'])
            (Path(home) / 'telegram-app.env').write_text('TELEGRAM_API_ID=1\nTELEGRAM_API_HASH=' + 'c' * 32 + '\n')
            form = onboarding.web_form(config, 'telegram')
            self.assertIsNone(form['secret'])
            self.assertEqual(form['ask'], [])
            self.assertEqual(onboarding.label('telegram'), 'Telegram chats')

    def test_the_phone_login_says_where_the_code_went_and_can_send_it_again(self):
        import onboarding
        script = [{'event': 'code_sent', 'via': 'email', 'to': 'j***@example.com'}, {'event': 'code_sent', 'via': 'sms', 'again': True},
                  {'event': 'connected', 'name': 'Owner'}]
        written = []

        class Process:
            def __init__(self, *a, **kw):
                self.stdout = io.StringIO(''.join(json.dumps(e) + '\n' for e in script))
                self.stdin = types.SimpleNamespace(write=written.append, flush=lambda: None)

            def poll(self):
                return 0

            def wait(self, *a):
                return 0

        class UI:
            web, said, asked, extras = True, [], [], []

            def choose(self, prompt, options):
                self.extras.append(dict(self.extra))
                return 'phone'

            def ask(self, prompt):
                self.asked.append(prompt)
                self.extras.append(dict(getattr(self, 'extra', {}) or {}))
                return '+32 470 00 00 00' if 'phone number' in prompt else ('again' if len(self.asked) == 2 else '12345')

            def say(self, line):
                self.said.append(line)

            def show_code(self, code):
                pass
        ui = UI()
        with tempfile.TemporaryDirectory() as home, patch.object(onboarding.subprocess, 'Popen', Process), \
                patch.object(onboarding.service, 'available', return_value=False):
            onboarding.telegram_login({}, {**ACCOUNT, 'store': str(Path(home) / 'tg')}, ui)
        self.assertEqual(ui.extras[0], {'phone_first': 1})
        self.assertTrue(ui.extras[2].get('resend'))
        self.assertIn('Code sent to your login email j***@example.com.', ui.said)
        self.assertIn('Sent again. Code sent by SMS.', ui.said)
        self.assertEqual([json.loads(w) for w in written], [{'resend': True}, {'code': '12345'}])

    def test_a_terminal_qr_code(self):
        import onboarding
        self.assertEqual(onboarding.telegram_qr_text(['10', '01', '11']), '▀▄\n▀▀')


if __name__ == '__main__':
    unittest.main()
