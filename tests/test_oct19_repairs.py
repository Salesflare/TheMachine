"""Disposable data only: concurrent edits, export boundaries and attributable WhatsApp receipts."""
import portable
import json
import sqlite3
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import graph
import next_actions as actions


class DurableEdits(unittest.TestCase):
    def test_concurrent_partial_org_edits_preserve_both_owners_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'db.sqlite'
            db=sqlite3.connect(path);db.row_factory=sqlite3.Row
            db.executescript("CREATE TABLE graph_nodes(id TEXT, kind TEXT, info TEXT);CREATE TABLE org_edits(domain TEXT PRIMARY KEY, fields TEXT, updated_at TEXT);")
            db.execute("INSERT INTO graph_nodes VALUES('org:example.test','org',?)",(json.dumps({'domain':'example.test'}),));db.commit()
            db.execute('BEGIN IMMEDIATE')
            graph.org_edit(db,'org:example.test',{'about':'Owner description'},'2026-10-19')
            errors=[];started=threading.Event()
            def edit():
                try:
                    with sqlite3.connect(path,timeout=5) as second:
                        second.row_factory=sqlite3.Row
                        started.set()
                        graph.org_edit(second,'org:example.test',{'industry':'Software'},'2026-10-19')
                except Exception as error:errors.append(error)
            other=threading.Thread(target=edit);other.start();started.wait(1);time.sleep(.05)
            db.commit();other.join(3)
            self.assertFalse(other.is_alive());self.assertFalse(errors)
            kept=json.loads(db.execute('SELECT fields FROM org_edits').fetchone()[0]);db.close()
            self.assertEqual(kept,{'about':'Owner description','industry':'Software'})


class AttributableWhatsApp(unittest.TestCase):
    def test_same_text_earlier_message_is_not_this_send(self):
        transport=actions.WhatsAppTransport({})
        draft={'kind':'whatsapp','chat_id':'test@s.whatsapp.net','body':'Yes',
               'proof':{'whatsapp_dispatched_at':'2026-10-19T10:00:00+00:00','whatsapp_before_ids':['old-id']}}
        rows=[{'MsgID':'old-id','FromMe':True,'Text':'Yes','Timestamp':'2026-10-19T10:00:00Z'},
              {'MsgID':'earlier','FromMe':True,'Text':'Yes','Timestamp':'2026-10-19T09:59:59Z'}]
        with patch.object(transport,'read',return_value={'messages':rows}):self.assertEqual(transport.reconcile(draft,{}),{})
        rows.append({'MsgID':'new-id','FromMe':True,'Text':'Yes','Timestamp':'2026-10-19T10:00:02Z'})
        with patch.object(transport,'read',return_value={'messages':rows}):self.assertEqual(transport.reconcile(draft,{}),{'message_id':'whatsapp:new-id'})
        rows.append({'MsgID':'also-new','FromMe':True,'Text':'Yes','Timestamp':'2026-10-19T10:00:03Z'})
        with patch.object(transport,'read',return_value={'messages':rows}):self.assertEqual(transport.reconcile(draft,{}),{})
        draft.pop('proof')
        with patch.object(transport,'read',side_effect=AssertionError('No fabricated legacy proof')):
            self.assertEqual(transport.reconcile(draft,{}),{})


try:
    import moving
except ImportError:
    moving=None  # private installation has no customer export/import feature


@unittest.skipUnless(moving,'public customer migration feature')
class ExportBoundaries(unittest.TestCase):
    def test_workspace_configured_key_is_omitted_without_passphrase(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(moving,'own_connectors',return_value=[]):
            root=Path(tmp);data=root/'data';space=root/'workspace';data.mkdir();space.mkdir()
            key=space/'unusual-credential.json';key.write_text('private-value')
            (space/'USER.md').write_text('Owner')
            config=data/'config.json';config.write_text(json.dumps({'credentials':{'slack':str(key)},'accounts':[]}))
            file,manifest=moving.export(config,root/'out',workspace=space,openclaw_home=root/'claw')
            import tarfile
            plain=root/'opened.tar.gz';moving._openssl(['-in',str(file),'-out',str(plain)],manifest['code'],decrypt=True)
            with tarfile.open(plain,'r:gz') as archive:
                self.assertNotIn('private-value',''.join(archive.extractfile(m).read().decode(errors='replace') for m in archive.getmembers() if m.isfile()))
            secrets=[i for i in moving.plan(config,space,root/'claw') if i[0]=='secret']
            self.assertEqual([name for _,_,name in secrets],['secrets/workspace/unusual-credential.json'])

    def test_import_refuses_live_lock_and_wal_without_modifying_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);config=root/'config.json';config.write_text('{}');wal=root/'events.sqlite-wal';wal.write_text('uncommitted bytes')
            with self.assertRaises(moving.MoveError):moving.import_(root/'missing.tar.gz',config,force=True)
            self.assertEqual(wal.read_text(),'uncommitted bytes');self.assertEqual(config.read_text(),'{}')
            wal.unlink()
            with (root/'service.lock').open('w') as lock:
                portable.lock(lock,blocking=False)
                with self.assertRaises(moving.MoveError):moving.import_(root/'missing.tar.gz',config,force=True)
            self.assertEqual(config.read_text(),'{}')
