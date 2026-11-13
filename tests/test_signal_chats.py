"""Signal chats: the pinned signal-cli (signal-pin.json),the link as a device of the phone, what arrives becoming events, the outbox
that sends only what the owner approved, and the catalog. A stand-in for signal-cli: nothing here talks to Signal or
downloads anything."""
import argparse
import contextlib
import datetime as dt
import hashlib
import importlib.util
import io
import itertools
import json
import re
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import message_seal  # noqa: E402
import next_actions as n  # noqa: E402
import onboarding  # noqa: E402
import signal_mirror as sm  # noqa: E402
import signal_release as sr  # noqa: E402
import signal_send  # noqa: E402
import signal_store as ss  # noqa: E402
from machine.sources import groups  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_signal', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
spec = importlib.util.spec_from_file_location('signal_pin', ROOT / 'scripts/signal_pin.py')
signal_pin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signal_pin)

NUMBER = '+15555550100'  # a fictional number (555-01xx)
PAT = '11111111-1111-4111-8111-111111111111'
LEE = '22222222-2222-4222-8222-222222222222'
OWN = '33333333-3333-4333-8333-333333333333'
GROUP = 'Z3JvdXAtaWQtZm9yLXRlc3Rz'
NOW_MS = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)


class Cli:
    """A stand-in for signal-cli's JSON-RPC: answers per method, and every call kept."""

    def __init__(self, **answers):
        self.answers, self.calls = answers, []

    def __call__(self, method, params=None, wait=None):
        self.calls.append((method, params))
        answer = self.answers.get(method)
        if isinstance(answer, list) and answer and isinstance(answer[0], (Exception, dict)) and method in ('finishLink', 'send'):
            answer = answer.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer() if callable(answer) else answer

    call = __call__


def account(folder):
    return {'id': 'personal-signal', 'service': 'signal', 'transport': 'signal_mirror', 'store': str(folder),
            'identity_sha256': ss.identity(NUMBER), 'boundary': 'personal:signal'}


def mirror(folder, **answers):
    cli = Cli(listContacts=[{'uuid': PAT, 'name': 'Pat Example', 'number': NUMBER}, {'uuid': LEE, 'profile': {'givenName': 'Lee'}}],
              listGroups=[{'id': GROUP, 'name': 'Book club'}], **answers)
    m = sm.Mirror(cli, folder, ss.sealer(folder), NUMBER, sleep=lambda _: None, clock=lambda: 1000.0)
    ss.set_state(m.db, identity=ss.identity(NUMBER), account=NUMBER, uuid=OWN, linked_at=ss.now())
    m.refresh_names()
    return m, cli


def incoming(source, at, text=None, name='Pat Example', **data):
    return {'sourceUuid': source, 'sourceName': name, 'timestamp': at,
            'dataMessage': {'timestamp': at, **({'message': text} if text is not None else {}), **data}}


def rows(m):
    return {(r['chat_id'], r['author'], r['sent_at']): dict(r) for r in m.db.execute('SELECT * FROM signal_messages')}


# ---------------------------------------------------------------- the pinned signal-cli

class Release(unittest.TestCase):
    def test_the_pin_names_a_release_and_checksums_for_each_build(self):
        data = sr.pin()
        self.assertEqual(data['repository'], 'AsamK/signal-cli')
        self.assertEqual(data['license'], 'GPL-3.0-only')
        for build in data['builds'].values():
            self.assertRegex(build['sha256'], r'^[0-9a-f]{64}$')
            self.assertTrue(sr.download_url(data, next(k for k, b in data['builds'].items() if b is build))
                            .startswith('https://github.com/AsamK/signal-cli/releases/download/' + data['tag'] + '/'))

    def test_install_checks_the_checksum_before_unpacking_and_keeps_one_version(self):
        blob = io.BytesIO()
        with tarfile.open(fileobj=blob, mode='w:gz') as archive:
            for name, body in (('signal-cli', b'#!/bin/sh\n'), ('../escape', b'no')):
                info = tarfile.TarInfo(name)
                info.size, info.mode = len(body), 0o755
                archive.addfile(info, io.BytesIO(body))
        blob = blob.getvalue()
        data = {'repository': 'AsamK/signal-cli', 'tag': 'v0.0.1', 'license': 'GPL-3.0-only',
                'builds': {'linux_amd64': {'archive': 'x.tar.gz', 'sha256': hashlib.sha256(blob).hexdigest(), 'binary': 'signal-cli'},
                           'java': {'archive': 'y.tar.gz', 'sha256': '0' * 64, 'binary': 'bin/signal-cli', 'java': 25}}}
        with tempfile.TemporaryDirectory() as base:
            (Path(base) / '0.0.0').mkdir()
            with self.assertRaisesRegex(RuntimeError, 'checksum'):
                sr.install(base, data, 'linux_amd64', fetch=lambda url: blob + b'x')
            self.assertIsNone(sr.installed(base, data, 'linux_amd64'))
            program = sr.install(base, data, 'linux_amd64', fetch=lambda url: blob)
            self.assertEqual(program, Path(base) / '0.0.1' / 'signal-cli')
            self.assertFalse((Path(base) / 'escape').exists())
            self.assertFalse((Path(base) / '0.0.0').exists())
            self.assertIn('GPL-3.0-only', (Path(base) / '0.0.1' / 'NOTICE').read_text())
            with self.assertRaisesRegex(RuntimeError, 'Java 25'):
                sr.install(base, data, 'java', fetch=lambda url: blob, java=lambda: 21)

    def test_downloads_only_from_its_own_releases(self):
        with self.assertRaises(RuntimeError):
            sr._fetch('https://example.com/signal-cli.tar.gz')

    def test_the_monthly_bump_pins_the_newest_release_with_its_checksums(self):
        data = {'repository': 'AsamK/signal-cli', 'tag': 'v0.1.2', 'license': 'GPL-3.0-only',
                'builds': {'linux_amd64': {'archive': 'signal-cli-0.1.2-Linux-native.tar.gz', 'sha256': '0' * 64, 'binary': 'signal-cli'},
                           'java': {'archive': 'signal-cli-0.1.2.tar.gz', 'sha256': '0' * 64, 'binary': 'signal-cli-0.1.2/bin/signal-cli', 'java': 25}}}
        release = {'tag_name': 'v0.1.3', 'assets': [{'name': 'signal-cli-0.1.3-Linux-native.tar.gz', 'digest': 'sha256:' + 'a' * 64},
                                                    {'name': 'signal-cli-0.1.3.tar.gz', 'digest': 'sha256:' + 'b' * 64},
                                                    {'name': 'signal-cli-0.1.3.tar.gz.asc', 'digest': None}]}
        tag, sums = signal_pin.newest('AsamK/signal-cli', lambda url, accept: json.dumps(release).encode())
        new = signal_pin.updated_pin(data, tag, sums)
        self.assertEqual(new['tag'], 'v0.1.3')
        self.assertEqual(new['builds']['linux_amd64'], {'archive': 'signal-cli-0.1.3-Linux-native.tar.gz', 'sha256': 'a' * 64, 'binary': 'signal-cli'})
        self.assertEqual(new['builds']['java']['binary'], 'signal-cli-0.1.3/bin/signal-cli')
        self.assertEqual(new['builds']['java']['sha256'], 'b' * 64)
        with self.assertRaises(SystemExit):
            signal_pin.updated_pin(data, tag, {'signal-cli-0.1.3.tar.gz': 'b' * 64})  # a build without its archive
        for odd in ('nightly', 'v0.1.3-rc1'):
            with self.assertRaises(SystemExit):
                signal_pin.newest('AsamK/signal-cli', lambda url, accept, odd=odd: json.dumps({'tag_name': odd}).encode())
        blob = b'archive'
        good = {**new, 'builds': {'java': {**new['builds']['java'], 'sha256': hashlib.sha256(blob).hexdigest()}}}
        with contextlib.redirect_stdout(io.StringIO()):
            signal_pin.verify(good, fetch=lambda url: blob)
            with self.assertRaises(SystemExit):
                signal_pin.verify(good, fetch=lambda url: blob + b'x')
        line = '| [signal-cli](https://github.com/AsamK/signal-cli) 0.1.2, downloaded from its GitHub releases'
        self.assertIn('signal-cli) 0.1.3, downloaded', signal_pin.notices(line, new))
        self.assertIn(f"signal-cli) {sr.version()},", (ROOT / 'THIRD_PARTY_NOTICES.md').read_text())


# ---------------------------------------------------------------- linking

class Linking(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name) / 'signal'

    def link(self, cli, clock):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                sm.link(cli, self.store, ss.sealer(self.store), wait=600, clock=clock)
            except RuntimeError as error:
                return [json.loads(line) for line in out.getvalue().splitlines()], str(error)
        return [json.loads(line) for line in out.getvalue().splitlines()], None

    def test_a_new_code_follows_until_it_is_scanned_and_only_a_hash_of_the_number_is_said(self):
        uri = 'sgnl://linkdevice?uuid=abc&pub_key=def'
        cli = Cli(startLink={'deviceLinkUri': uri}, finishLink=[sm.RpcError({'message': 'timeout'}), {'number': NUMBER}])
        events, error = self.link(cli, itertools.count(0, 100).__next__)
        self.assertIsNone(error)
        self.assertEqual([e['event'] for e in events], ['qr', 'qr', 'connected'])
        self.assertTrue(all(re.fullmatch('[01]+', row) for row in events[0]['matrix']))
        self.assertEqual(events[-1]['identity'], ss.identity(NUMBER))
        self.assertNotIn(NUMBER, json.dumps(events))
        self.assertIn(('finishLink', {'deviceLinkUri': uri, 'deviceName': 'The Machine'}), cli.calls)
        with ss.connect(self.store) as db:
            state = ss.get_state(db)
        self.assertEqual((state['identity'], state.get('error')), (ss.identity(NUMBER), None))

    def test_an_unscanned_code_stops_after_the_wait(self):
        def unscanned():
            raise sm.RpcError({'message': 'timeout'})
        cli = Cli(startLink={'deviceLinkUri': 'sgnl://linkdevice?uuid=a&pub_key=b'}, finishLink=unscanned)
        events, error = self.link(cli, itertools.count(0, 100).__next__)
        self.assertEqual(error, 'qr_expired')
        self.assertEqual({e['event'] for e in events}, {'qr'})  # a fresh code each round, never a link
    def test_unlinked_on_the_phone_stops_for_good_and_never_links_again_by_itself(self):
        m, _ = mirror(self.store)
        note = {'method': 'receive', 'params': {'exception': {'type': 'org.signal.AuthorizationFailedException'}}}
        self.assertEqual(m.on_notification(note), 'unlinked')
        self.assertEqual(m.on_notification({'method': 'receive', 'params': {'exception': {'type': 'x.DeprecatedVersionException'}}}), 'outdated')
        ss.set_state(m.db, error='unlinked')
        args = argparse.Namespace(cli='/nonexistent/signal-cli', base=None, store=str(self.store), database=None, command='follow')
        self.assertEqual(sm.run(args), 0)  # nothing started: the owner links it again from Connections
        with self.assertRaisesRegex(a.SourceError, 'signal_unlinked'):
            a.Signal({}, account(self.store)).profile()
        ss.set_state(m.db, error='outdated')
        with self.assertRaisesRegex(a.SourceError, 'signal_outdated'):
            a.Signal({}, account(self.store)).profile()
        with self.assertRaisesRegex(a.SourceError, 'account_identity_mismatch'):
            ss.set_state(m.db, error=None)
            a.Signal({}, {**account(self.store), 'identity_sha256': 'other'}).profile()


# ---------------------------------------------------------------- what arrives

class Arriving(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name) / 'signal'
        self.m, _ = mirror(self.store)

    def test_messages_groups_attachments_edits_and_deletes(self):
        m, t = self.m, NOW_MS
        self.assertTrue(m.on_envelope(incoming(PAT, t, 'Lunch on Friday?')))
        self.assertTrue(m.on_envelope(incoming(LEE, t + 1, 'Chapter 3 tonight', name='Lee', groupInfo={'groupId': GROUP, 'type': 'DELIVER'})))
        self.assertTrue(m.on_envelope(incoming(PAT, t + 2, attachments=[{'contentType': 'image/jpeg', 'id': 'x'}])))
        self.assertTrue(m.on_envelope(incoming(PAT, t + 3, 'secret', viewOnce=True, attachments=[{'contentType': 'image/jpeg'}])))
        self.assertTrue(m.on_envelope({'sourceUuid': PAT, 'sourceName': 'Pat Example', 'timestamp': t + 9,
                                       'editMessage': {'targetSentTimestamp': t, 'dataMessage': {'message': 'Lunch on Saturday?'}}}))
        self.assertTrue(m.on_envelope({'sourceUuid': OWN, 'timestamp': t + 4, 'syncMessage': {'sentMessage': {
            'destinationUuid': PAT, 'timestamp': t + 4, 'message': 'Sure'}}}))
        self.assertTrue(m.on_envelope(incoming(PAT, t + 5, 'oops')))
        self.assertTrue(m.on_envelope(incoming(PAT, t + 6, remoteDelete={'timestamp': t + 5})))
        # skipped: Note to Self, reactions, a group change without text, someone without an account ID
        self.assertFalse(m.on_envelope({'sourceUuid': OWN, 'syncMessage': {'sentMessage': {'destinationUuid': OWN, 'timestamp': t + 7, 'message': 'note'}}}))
        self.assertFalse(m.on_envelope(incoming(PAT, t + 8, reaction={'emoji': '+1'})))
        self.assertFalse(m.on_envelope(incoming(LEE, t + 8, groupInfo={'groupId': GROUP, 'type': 'UPDATE'})))
        self.assertFalse(m.on_envelope(incoming('not-an-id', t + 8, 'hi')))

        kept = rows(m)
        self.assertEqual(len(kept), 6)
        seal = ss.sealer(self.store)
        first = kept[(PAT, PAT, t)]
        self.assertEqual((seal.open(first['text']), first['edited']), ('Lunch on Saturday?', 1))
        self.assertEqual(kept[(PAT, PAT, t + 2)]['media_type'], 'photo')
        self.assertEqual((seal.open(kept[(PAT, PAT, t + 3)]['text']), kept[(PAT, PAT, t + 3)]['media_type']), ('', 'view-once media'))
        self.assertEqual((kept[(PAT, PAT, t + 5)]['deleted'], kept[(PAT, PAT, t + 5)]['text']), (1, None))
        self.assertEqual(seal.open(kept[(PAT, 'me', t + 4)]['text']), 'Sure')
        self.assertIn(('g:' + GROUP, LEE, t + 1), kept)
        raw = (self.store / ss.DB_NAME).read_bytes()
        for plain in (b'Lunch', b'Chapter 3', b'Pat Example', b'Book club', b'secret'):
            self.assertNotIn(plain, raw)  # sealed, names too

    def test_disappearing_messages_lose_their_text_when_their_timer_is_up(self):
        self.m.on_envelope(incoming(PAT, NOW_MS, 'gone soon', expiresInSeconds=60))
        later = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=2)).isoformat()
        self.assertEqual(ss.purge_expired(self.m.db, later), 1)
        row = rows(self.m)[(PAT, PAT, NOW_MS)]
        self.assertEqual((row['deleted'], row['text']), (1, None))

    def test_the_collector_reads_the_store_as_events_like_whatsapp(self):
        m, t = self.m, NOW_MS
        m.on_envelope(incoming(PAT, t, 'Lunch on Friday?'))
        m.on_envelope(incoming(LEE, t + 1, 'Chapter 3 tonight', name='Lee', groupInfo={'groupId': GROUP}))
        m.on_envelope(incoming(PAT, t + 2, attachments=[{'contentType': 'audio/aac', 'voiceNote': True}]))
        m.on_envelope(incoming(PAT, t + 3, 'Your verification code is 123456'))
        store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        result = a.sync_signal(store, {}, account(self.store))
        self.assertEqual(result['events'], 4)
        with store.connect() as db:
            events = {json.loads(r['metadata'])['message_id']: dict(r) for r in db.execute("SELECT * FROM events WHERE kind='signal.message'")}
        dm = events[f'{PAT}:{t}']
        meta = json.loads(dm['metadata'])
        self.assertEqual((dm['title'], meta['chat_kind'], meta['from'], meta['chat_id']), ('Pat Example', 'dm', 'Pat Example', PAT))
        self.assertIn('no older messages', meta['coverage'])
        group = json.loads(events[f'{LEE}:{t + 1}']['metadata'])
        self.assertEqual((group['chat_name'], group['chat_kind'], group['sender_id']), ('Book club', 'group', LEE))
        self.assertEqual(events[f'{PAT}:{t + 2}']['body'], 'Sent a voice message')
        self.assertEqual(events[f'{PAT}:{t + 3}']['body'], '[One-time security code omitted]')
        self.assertFalse({'chat_name', 'sender_display', 'media_type'} & message_seal.PLAIN_METADATA)

    def test_the_linked_accounts_own_name_names_its_card_never_its_number(self):
        self.assertNotIn('name', ss.get_state(self.m.db))  # its own entry wasn't in the list
        self.m.call.answers['listContacts'] = [{'uuid': OWN, 'number': NUMBER, 'profile': {'givenName': 'Sam', 'familyName': 'Example'}}]
        self.m.refresh_names()
        self.assertEqual(ss.get_state(self.m.db)['name'], 'Sam Example')
        store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        a.sync_signal(store, {}, account(self.store))
        self.assertEqual(store.checkpoint('personal-signal')['account_name'], 'Sam Example')
        from machine import names
        card = names.account_card(account(self.store), [], store.checkpoint('personal-signal'))
        self.assertEqual(card, {'card_title': 'Sam’s Signal', 'card_subtitle': 'Personal'})
        self.m.call.answers['listContacts'] = [{'uuid': OWN, 'number': NUMBER}]  # no name: never the number instead
        self.m.refresh_names()
        self.assertEqual(ss.get_state(self.m.db)['name'], 'Sam Example')

    def test_work_or_personal_and_the_graph_like_whatsapp(self):
        event = a.signal_event(account(self.store), {'chat_id': PAT, 'author': PAT, 'sent_at': NOW_MS, 'from_me': 0, 'text': 'Hi',
                                                     'occurred_at': ss.now(), 'chat_name': 'Pat Example', 'sender_name': 'Pat Example'})
        self.assertEqual(event['kind'], 'signal.message')
        import graph
        self.assertEqual(graph.touches('signal.message', event['metadata'], None, None)[0][0], 'sig:' + PAT)
        group = {**event['metadata'], 'chat_id': 'g:' + GROUP, 'chat_kind': 'group', 'sender_id': LEE}
        self.assertEqual(graph.touches('signal.message', group, None, None), [('sig:' + LEE, 'Pat Example', 0.1, 'seen')])
        self.assertEqual(graph.thread_key('signal.message', event['metadata'])[0], 'sig:' + PAT)


# ---------------------------------------------------------------- what goes out

class Outbox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name) / 'signal'

    def test_sends_only_approved_rows_into_chats_it_has_once_and_paced(self):
        sent = {'timestamp': NOW_MS + 50, 'results': [{'type': 'SUCCESS'}]}
        m, cli = mirror(self.store, send=[sent])
        m.on_envelope(incoming(PAT, NOW_MS, 'Lunch?'))
        seal = ss.sealer(self.store)
        ss.queue_send(m.db, seal, 'job-1', PAT, 'Yes, Saturday works.', {'author': PAT, 'sent_at': NOW_MS})
        ss.queue_send(m.db, seal, 'job-1', PAT, 'twice', None)  # one row per approved job
        m.db.execute("INSERT INTO signal_outbox(id, op, chat_id, text, approval, created_at) VALUES ('x', 'send', ?, ?, NULL, ?)",
                     (PAT, seal.seal('unapproved'), ss.now()))
        ss.queue_send(m.db, seal, 'job-2', LEE[:-1] + '9', 'new chat', None)
        self.assertEqual([m.outbox(), m.outbox(), m.outbox(), m.outbox()], ['sent', 'failed', 'failed', None])
        sends = [p for method, p in cli.calls if method == 'send']
        self.assertEqual(sends, [{'message': 'Yes, Saturday works.', 'recipient': [PAT], 'quoteTimestamp': NOW_MS, 'quoteAuthor': PAT}])
        status = {r['id']: (r['status'], r['error']) for r in m.db.execute('SELECT * FROM signal_outbox')}
        self.assertEqual(status, {'job-1': ('sent', None), 'x': ('failed', 'not_approved'), 'job-2': ('failed', 'chat_not_read')})
        self.assertIn((PAT, 'me', NOW_MS + 50), rows(m))

    def test_a_refused_send_is_said_and_never_retried(self):
        m, cli = mirror(self.store, send=[sm.RpcError({'message': 'rate limited', 'code': -5})])
        ss.queue_send(m.db, ss.sealer(self.store), 'job-1', 'g:' + GROUP, 'Running late', None)
        self.assertEqual(m.outbox(), 'failed')
        self.assertIsNone(m.outbox())
        self.assertEqual([p['groupId'] for method, p in cli.calls if method == 'send'], [GROUP])


class Sending(unittest.TestCase):
    """The approve-before-send path, as for WhatsApp: a draft is checked, waits on the to-do, and only the owner's Send
    puts it in the outbox."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        folder = Path(self.tmp.name) / 'signal'
        m, _ = mirror(folder)
        m.on_envelope(incoming(PAT, NOW_MS, 'Are you in for Saturday?'))
        self.account = account(folder)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        a.sync_signal(self.store, {}, self.account)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM events WHERE kind='signal.message'")]
        self.sid = self.store.suggest('signal-task', 'Answer Pat', 'Pat asks about Saturday.', ids)['id']
        self.config = {'accounts': [self.account, {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog'}]}

    def app(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        return app

    def row(self):
        return self.store.snapshot([])['suggestions'][0]

    def save(self, **draft):
        action = {k: v for k, v in {'kind': 'signal', 'label': 'Send reply', 'account_id': self.account['id'], 'chat_id': PAT,
                                    'body': 'Yes, I am in.', **draft}.items() if v is not None}
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})

    def ready(self, **draft):
        self.store.decide(self.sid, 'accept', '', 'accept', 'dashboard')
        self.save(**draft)
        return self.row()['next_action']

    def outbox(self):
        with ss.connect(self.account['store']) as db:
            return [dict(r) for r in db.execute('SELECT * FROM signal_outbox')]

    def test_a_reply_only_into_an_existing_chat(self):
        action = self.ready()
        self.assertEqual((action['chat_id'], action['to_name'], action['max_length']), (PAT, 'Pat Example', 4000))
        self.assertTrue(n.preview(action).startswith('Signal message to Pat Example'))
        for bad in ({'chat_id': LEE[:-1] + '9'}, {'chat_id': 'g:' + GROUP + 'x'},{'account_id': 'work'}, {'label': 'Post it'}, {'body': 'a' * 4001}, {'body': ' '}, {'media': ['a.png']}):
            with self.assertRaises(ValueError, msg=bad):
                self.save(**bad)

    def test_nothing_reaches_the_outbox_without_the_owners_send(self):
        self.ready()
        transport = signal_send.SignalTransport(self.config, sleep=lambda _: None)
        self.assertIsNone(self.app().action_step(transport))
        self.assertEqual(self.outbox(), [])
        with self.assertRaises(ValueError):
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'send_now': True,
                                          'next_action': {'kind': 'signal', 'account_id': self.account['id'], 'chat_id': PAT, 'body': 'Yes'}})
        self.assertEqual(self.outbox(), [])

    def test_an_approved_reply_goes_to_the_outbox_once(self):
        self.ready()
        action = self.row()['next_action']
        self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'owner-approval'},
                          owner_dashboard=True)
        clock = iter(range(0, 1000, 5))
        transport = signal_send.SignalTransport(self.config, sleep=lambda _: self.mirror_sends(), clock=lambda: next(clock))
        self.assertEqual(self.app().action_step(transport), 'sent')
        self.assertIsNone(self.app().action_step(transport))
        rows_ = self.outbox()
        self.assertEqual(len(rows_), 1)
        self.assertEqual(ss.sealer(self.account['store']).open(rows_[0]['text']), 'Yes, I am in.')
        self.assertIn('Signal message sent', str(a.card(self.row())))

    def mirror_sends(self):
        with ss.connect(self.account['store']) as db:
            db.execute("UPDATE signal_outbox SET status='sent', sent_at=? WHERE status='queued'", (NOW_MS + 100,))

    def test_a_reply_in_a_group_quotes_the_message_it_answers(self):
        spots = [{'service': 'signal', 'account_id': self.account['id'], 'chat_id': 'g:' + GROUP, 'message_id': f'{LEE}:{NOW_MS}', 'group': True}]
        action = signal_send.check({'kind': 'signal', 'account_id': self.account['id'], 'chat_id': 'g:' + GROUP, 'body': 'Yes'}, self.config,
                                   {'g:' + GROUP: {'account_id': self.account['id'], 'name': 'Book club'}}, spots)
        self.assertEqual(action['quote'], {'author': LEE, 'sent_at': NOW_MS})
        self.assertIn('as a reply', n.preview(action))


# ---------------------------------------------------------------- the catalog

class Catalog(unittest.TestCase):
    def test_signal_sits_with_the_chats_with_its_logo_and_one_color_mark(self):
        self.assertEqual(groups.GROUP_OF['signal'], 'chat')
        self.assertEqual(onboarding.label('signal'), 'Signal chats')
        self.assertIn('signal', onboarding.STEPS)
        logo = (ROOT / 'dashboard/logos/signal.svg').read_text()
        self.assertIn('fill="#3B45FD"', logo)  # the brand color on its card and in + Add, like WhatsApp's and Telegram's
        self.assertIn('`signal.svg` | Signal | signal', (ROOT / 'dashboard/logos/NOTICE.md').read_text())
        self.assertNotIn("|signal)$/.test(n)?' mono'", (ROOT / 'dashboard/connections-cards.js').read_text())
        self.assertRegex((ROOT / 'dashboard/todos-logos.js').read_text(), r"const MONO=\[[^\]]*'signal'")  # the thin one-color mark in rows
        self.assertTrue((ROOT / 'dashboard/logos/mono/signal.svg').is_file())
        self.assertRegex((ROOT / 'dashboard/connections-cards.js').read_text(), r'const LOGOS=/\^\([a-z_|]*\|signal\|')

    def test_the_message_key_never_lets_content_or_identities_through(self):
        self.assertFalse({'text', 'body', 'sender_name', 'chat_name', 'sender_display', 'identity'} & message_seal.PLAIN_METADATA)


if __name__ == '__main__':
    unittest.main()
