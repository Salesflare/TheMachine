"""Recent Network/Family/Skills/export regressions, with disposable files and fake peers."""
import concurrent.futures
import json
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import network
import moving
import network_crypto as nc
import test_network as tn
import test_family as tf
import test_skills as ts
import test_moving as tm

class Crypto(unittest.TestCase):
    def test_concurrent_first_use_keeps_one_complete_keypair(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)/'keys.json'
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                rows = list(pool.map(lambda _: nc.load_or_make(target), range(24)))
            self.assertTrue(all(k == rows[0] for k in rows))
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            target.write_text('{broken')
            with self.assertRaises(nc.SealError): nc.load_or_make(target)
            self.assertEqual(target.read_text(),'{broken')

    def test_missing_envelope_field_is_a_seal_error_not_batch_crash(self):
        me, peer = nc.new_keys(), nc.new_keys()
        envelope = nc.seal({'test':True},me,nc.public_keys(peer),{})
        for field in ('eph','n','mac','sig'):
            damaged = {k:v for k,v in envelope.items() if k != field}
            with self.assertRaises(nc.SealError):nc.open_sealed(damaged,peer,nc.public_keys(me),{})

    def test_small_order_signature_cannot_forge_an_identity(self):
        identity = b'\x01'+bytes(31)
        for fast in (nc._ced,None):
            with patch.object(nc,'_ced',fast):
                self.assertFalse(nc.ed25519_verify(identity,b'anything',identity+bytes(32)))

    def test_schema_preserves_old_table_and_does_not_commit_callers_transaction(self):
        db=sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.execute('CREATE TABLE network_taken(legacy TEXT)')
        db.execute('CREATE TABLE network_taken_old(legacy TEXT)')
        db.commit()
        db.execute('BEGIN')
        network.ensure(db)
        self.assertTrue(db.in_transaction)
        self.assertTrue(db.execute("SELECT 1 FROM sqlite_master WHERE name='network_taken_old_2'").fetchone())
        db.rollback()
        self.assertEqual([r[1] for r in db.execute('PRAGMA table_info(network_taken)')],['legacy'])

class Replies(tn.Machines):
    def test_outbox_is_committed_before_delivery_and_stale_flush_keeps_newer_intent(self):
        relay=self.pat.relay
        original=relay.inner.call
        def interrupted(method,path,body=None,timeout=40):
            with self.pat.connect() as db:
                self.assertTrue(db.execute('SELECT 1 FROM network_outbox WHERE key=?',('regression',)).fetchone())
            raise RuntimeError('process stopped before receipt')
        with patch.object(relay.inner,'call',interrupted):
            with self.assertRaises(RuntimeError):relay.send_or_keep('POST','/test',{'value':1},'regression')
        with self.pat.connect() as db: db.execute("UPDATE network_outbox SET next_at='2000-01-01'")
        def newer(method,path,body=None,timeout=40):
            with self.pat.connect() as db: db.execute('UPDATE network_outbox SET body=? WHERE key=?',(json.dumps({'value':2},sort_keys=True),'regression'))
            return {'ok':True}
        with patch.object(relay.inner,'call',newer):relay.flush()
        with self.pat.connect() as db:
            self.assertEqual(json.loads(db.execute('SELECT body FROM network_outbox WHERE key=?',('regression',)).fetchone()[0]),{'value':2})

class Family(tf.Family):
    def test_retry_keeps_request_id_and_context_then_new_request_gets_a_new_id(self):
        calls=[]
        def reply(method,path,body=None,timeout=40):
            if path=='/ask':
                calls.append(dict(body))
                if len(calls)==1: raise tf.fleet.Unavailable('response lost')
                return {'ids':{'fm_robin':'retry'+str(len(calls))}}
            return self.relay.call(method,path,body,timeout)
        with patch.object(self.fleet.relay,'call',reply):
            with self.assertRaises(tf.fleet.Unavailable):self.fleet.propose_todo('fm_robin','Get groceries',self.day)
            self.fleet.propose_todo('fm_robin','Get groceries',self.day)
            self.fleet.propose_todo('fm_robin','Get groceries',self.day)
        self.assertEqual(calls[0]['request_id'],calls[1]['request_id'])
        self.assertNotEqual(calls[1]['request_id'],calls[2]['request_id'])
        with self.fleet.connect() as db:
            self.assertFalse(db.execute("SELECT 1 FROM fleet_meta WHERE key LIKE 'pending_context:%'").fetchone())

    def test_event_end_compares_instants_and_rejects_invalid_end(self):
        self.assertIsNotNone(tf.family.parse('event',{'title':'Dinner','start':'2026-10-24T18:00+02:00','end':'2026-10-24T17:30+01:00'}))
        self.assertIsNone(tf.family.parse('event',{'title':'Dinner','start':'2026-10-24T18:00+02:00','end':'2026-10-24T18:30+03:00'}))
        self.assertIsNone(tf.family.parse('event',{'title':'Dinner','start':self.day,'end':'not-a-date'}))

class Skills(ts.Skills):
    def test_sync_never_follows_an_owned_skill_folder_symlink(self):
        row=self.mine()
        target=self.root/'weekly-report'
        for f in target.iterdir():f.unlink()
        target.rmdir()
        outside=Path(self.temp.name)/'outside';outside.mkdir()
        target.symlink_to(outside,target_is_directory=True)
        self.keeper.sync()
        self.assertEqual(list(outside.iterdir()),[])

    def test_replayed_share_keeps_the_original_pending_owner_choice(self):
        ask={'id':'replayed','question':ts.shared()}
        mate={'member_id':'fm_pat'}
        self.keeper.take_share(ask,mate,self.ref,'Pat')
        first=self.keeper.view()['skills'][0]['id']
        self.keeper.take_share(ask,mate,self.ref,'Pat')
        self.assertEqual(self.keeper.view()['skills'][0]['id'],first)

class Moving(tm.Moving):
    def test_plain_export_omits_default_and_custom_network_private_keys(self):
        default=self.data/'network-keys.json';default.write_text(json.dumps(nc.new_keys()))
        custom=self.data/'peer-identity.json';custom.write_text(json.dumps(nc.new_keys()))
        config=json.loads(self.config.read_text());config['network_keys']=str(custom);self.config.write_text(json.dumps(config))
        archive,_=self.export()
        self.assertFalse(any('network-keys.json' in n or 'peer-identity.json' in n for n in self.files(archive)))

    def network_keys(self, where=None):
        keys = nc.new_keys()
        path = where or self.data / 'network-keys.json'
        path.write_text(json.dumps(keys))
        if where:
            config = json.loads(self.config.read_text()); config['network_keys'] = str(where); self.config.write_text(json.dumps(config))
        return nc.public_keys(keys)

    def moved(self, passphrase):
        archive, manifest = self.export(passphrase=passphrase)
        shutil.rmtree(self.tmp / 'elsewhere', ignore_errors=True)  # another computer: the folder outside isn't there
        config_path, space, claw = self.target()
        with patch.dict('os.environ', {moving.PASSPHRASE_ENV: passphrase} if passphrase else {}):
            moving.import_(archive, config_path, passphrase=passphrase or manifest['code'], workspace=space, openclaw_home=claw)
        config = json.loads(config_path.read_text())
        found = network.keys_path(config)
        return manifest, config_path, (nc.public_keys(json.loads(found.read_text())) if found and found.is_file() else None)

    def test_an_export_with_keys_keeps_the_network_identity(self):
        public = self.network_keys()
        manifest, config_path, moved = self.moved('a long passphrase')
        self.assertEqual(moved, public)  # same Machine on the Network: no key-change notice for teammates
        self.assertEqual(manifest['network_identity'], 'kept')
        self.assertEqual(network.keys_path(json.loads(config_path.read_text())), config_path.parent / 'network-keys.json')
        self.assertEqual((config_path.parent / 'network-keys.json').stat().st_mode & 0o777, 0o600)

    def test_network_keys_kept_outside_the_data_folder_come_along_too(self):
        public = self.network_keys(Path(self.temp_outside()) / 'peer-identity.json')
        manifest, config_path, moved = self.moved('a long passphrase')
        self.assertEqual(moved, public)
        self.assertIn('secrets/network/peer-identity.json', manifest['files'])
        self.assertEqual(json.loads(config_path.read_text())['network_keys'], str(config_path.parent / 'peer-identity.json'))

    def test_an_export_without_keys_says_a_new_network_identity_will_be_made(self):
        self.network_keys(Path(self.temp_outside()) / 'peer-identity.json')
        manifest, config_path, moved = self.moved(None)
        self.assertEqual(manifest['network_identity'], 'new')
        self.assertTrue(any('a new Network identity will be made' in line for line in manifest['reconnect']))
        self.assertIsNone(moved)
        self.assertNotIn('network_keys', json.loads(config_path.read_text()))  # the old folder isn't here: new keys go next to the database

    def test_no_network_line_for_a_machine_that_never_joined(self):
        _, manifest = self.export()
        self.assertIsNone(manifest['network_identity'])
        self.assertFalse(any('Network' in line for line in manifest['reconnect']))

    def temp_outside(self):
        folder = self.tmp / 'elsewhere'
        folder.mkdir(exist_ok=True)
        return folder
