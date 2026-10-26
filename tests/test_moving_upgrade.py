"""Migration regressions with disposable archives, keys and unrelated files only."""
import json
import unittest
from pathlib import Path
import moving
import network
import network_crypto as nc
from test_moving import Moving, HAS_OPENSSL

class NetworkImport(Moving):
    def external_keys(self):
        outside = self.tmp / 'external'
        outside.mkdir()
        key = outside / 'shared.json'
        key.write_text(json.dumps(nc.new_keys()))
        config = json.loads(self.config.read_text())
        config['network_keys'] = str(key)
        self.config.write_text(json.dumps(config))
        return key

    @unittest.skipUnless(HAS_OPENSSL, 'openssl not installed')
    def test_network_restore_cannot_overwrite_same_named_credential(self):
        key = self.external_keys()
        expected = key.read_bytes()
        credential = self.tmp / 'credential' / key.name
        credential.parent.mkdir()
        credential.write_text('unrelated-credential-fixture')
        config = json.loads(self.config.read_text())
        config['credentials']['custom'] = str(credential)
        self.config.write_text(json.dumps(config))
        archive, _ = self.export('a long example passphrase')
        credential.unlink(); key.unlink()
        target, space, claw = self.target()
        moving.import_(archive, target, passphrase='a long example passphrase', workspace=space, openclaw_home=claw)
        restored = json.loads(target.read_text())
        self.assertEqual(Path(restored['credentials']['custom']).read_text(), 'unrelated-credential-fixture')
        self.assertEqual(network.keys_path(restored).read_bytes(), expected)
        self.assertNotEqual(network.keys_path(restored), Path(restored['credentials']['custom']))

    @unittest.skipUnless(HAS_OPENSSL, 'openssl not installed')
    def test_external_keys_are_copied_even_when_original_path_is_still_here(self):
        key = self.external_keys()
        expected = key.read_bytes()
        archive, _ = self.export('a long example passphrase')
        target, space, claw = self.target()
        moving.import_(archive, target, passphrase='a long example passphrase', workspace=space, openclaw_home=claw)
        restored = network.keys_path(json.loads(target.read_text()))
        self.assertEqual(restored.parent, target.parent)
        key.unlink()
        self.assertEqual(restored.read_bytes(), expected)

    def test_plain_import_does_not_reuse_exporters_external_identity(self):
        key = self.external_keys()
        archive, _ = self.export()
        target, space, claw = self.target()
        moving.import_(archive, target, passphrase=self.code, workspace=space, openclaw_home=claw)
        restored = json.loads(target.read_text())
        self.assertNotEqual(network.keys_path(restored), key)
        self.assertNotIn('network_keys', restored)

    @unittest.skipUnless(HAS_OPENSSL, 'openssl not installed')
    def test_external_identity_cannot_replace_imported_data_with_same_filename(self):
        key = self.external_keys()
        renamed = key.with_name('notes.txt')
        key.rename(renamed)
        config = json.loads(self.config.read_text())
        config['network_keys'] = str(renamed)
        self.config.write_text(json.dumps(config))
        expected = renamed.read_bytes()
        archive, _ = self.export('a long example passphrase')
        target, space, claw = self.target()
        moving.import_(archive, target, passphrase='a long example passphrase', workspace=space, openclaw_home=claw)
        self.assertEqual((target.parent / 'notes.txt').read_text(), 'kept as data')
        self.assertEqual(network.keys_path(json.loads(target.read_text())).read_bytes(), expected)

    def test_import_does_not_follow_predictable_temporary_symlink(self):
        archive, _ = self.export()
        target, space, claw = self.target()
        target.parent.mkdir(parents=True)
        unrelated = self.tmp / 'unrelated.txt'
        unrelated.write_text('keep this file')
        (target.parent / 'notes.txt.import-new').symlink_to(unrelated)
        moving.import_(archive, target, passphrase=self.code, workspace=space, openclaw_home=claw)
        self.assertEqual(unrelated.read_text(), 'keep this file')
        self.assertEqual((target.parent / 'notes.txt').read_text(), 'kept as data')
