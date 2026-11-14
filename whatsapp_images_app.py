"""Photos in WhatsApp chats, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The Read photos switch on a WhatsApp connection (whatsapp_photos), and the worker that fetches each noted photo
read-only through wacli, keeps it and has the Machine's model read it, then joins what it read to its message
(whatsapp_images.py). App gives it the WhatsApp source (whatsapp_source), the message's update (whatsapp_photo_event)
and the usage check every background turn makes (background_pause)."""
import datetime as dt
import logging
import subprocess

import message_seal
import models
import whatsapp_images
from machine.faults import loop_failed
from sources import SourceError
from timeutil import now
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
STEP_SECONDS = 20


class WhatsAppImagesApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'whatsapp_photos': 'whatsapp_photos_action',
    }

    def whatsapp_photo_accounts(self):
        """{id: account} of this Machine's own WhatsApp connections (never one shared from a Fleet)."""
        return {a['id']: a for a in self.config.get('accounts', []) if a.get('service') == 'whatsapp' and a.get('store') and not a.get('shared')}

    def whatsapp_photos_action(self, name, args, owner_dashboard):
        """Read photos on one WhatsApp connection: read (work chats), personal (personal chats too)."""
        if not owner_dashboard:
            raise OwnerError('Only the owner turns Read photos on or off, on Connections')
        account = self.whatsapp_photo_accounts().get(args.get('account'))
        if not account:
            raise OwnerError('That WhatsApp is not connected here')
        with self.store.connect() as db:
            chosen = whatsapp_images.set_prefs(db, account['id'], args.get('read') is True, args.get('personal') is True, now())
            LOG.info('whatsapp photos read=%s personal=%s', chosen['read'], chosen['personal'])
            return whatsapp_images.view(db, account)

    def whatsapp_photo_worker(self):
        while not self.stop.wait(STEP_SECONDS):
            try:
                self.whatsapp_photo_step()
            except Exception as error:  # noqa: BLE001 - tried again at the next step
                loop_failed(LOG, 'whatsapp photos', error)

    def whatsapp_photo_step(self, run=subprocess.run):
        """Fetch and read a few noted photos. Returns how many it finished (read, or set aside)."""
        accounts = self.whatsapp_photo_accounts()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            connected = [a['id'] for a in self.config.get('accounts', []) if a.get('service') == 'whatsapp']  # removed ones' photos go
            whatsapp_images.sweep(db, self.config, connected, (dt.datetime.fromisoformat(now()) - dt.timedelta(hours=1)).isoformat())
            rows = whatsapp_images.waiting(db, accounts)
        if not rows:
            return 0
        paused = bool(self.background_pause(job='whatsapp_photos', signals=True))  # reads wait for the model's room; downloads don't
        done = 0
        for row in rows:
            account = accounts[row['account_id']]
            if row['status'] == 'waiting':
                row = self.whatsapp_photo_fetch(account, row)
            if row and row['status'] == 'kept' and not paused:
                row = self.whatsapp_photo_read(row, run)
            if row and row['status'] in ('read', 'unread', 'kept'):
                self.whatsapp_photo_event(row['account_id'], row['source_id'])
                done += row['status'] != 'kept'
        return done

    def whatsapp_photo_fetch(self, account, row):
        """Download one photo read-only and keep it when it is one: the row as it is now, or None when it gave up."""
        folder = whatsapp_images.private_dir(self.config)
        try:
            target = folder / 'photo'
            try:
                said = self.whatsapp_source(account).download(row['chat_id'], row['message_id'], target)
                data = target.read_bytes() if target.is_file() and target.stat().st_size <= whatsapp_images.IMAGE_BYTES else b''
            except (SourceError, OSError):
                said, data = None, None
        finally:
            whatsapp_images.drop(folder)
        with self.store.connect() as db:
            if data is None:
                whatsapp_images.failed(db, row, now())
                return None
            mime = whatsapp_images.check(data, said.get('bytes') if isinstance(said, dict) and isinstance(said.get('bytes'), int) else None)
            if not mime:
                whatsapp_images.failed(db, row, now(), gone=True)
                return None
            whatsapp_images.keep(db, self.config, row, data, mime, now())
            return {**row, 'status': 'kept', 'mime': mime, 'size': len(data), 'tries': 0}

    def whatsapp_photo_read(self, row, run=subprocess.run):
        """Have the Machine's model read one kept photo: its own image routing first, then the main model."""
        try:
            with self.store.connect() as db:
                data, mime = whatsapp_images.data_of(db, self.config, row['id'])
        except (ValueError, OSError, message_seal.SealError):
            return None
        folder = whatsapp_images.private_dir(self.config)
        try:
            path = folder / ('photo.' + mime.split('/')[1].replace('jpeg', 'jpg'))
            path.write_bytes(data)
            path.chmod(0o600)
            swap = models.background_model(self.config)
            fallback = '/'.join(swap) if swap else models.openclaw_model(self.config)
            said = whatsapp_images.describe(self.config, path, None, run) or (
                whatsapp_images.describe(self.config, path, fallback, run) if fallback else None)
        finally:
            whatsapp_images.drop(folder)
        with self.store.connect() as db:
            if not said or not any(said):
                return {**row, 'status': whatsapp_images.failed(db, row, now())}
            whatsapp_images.read_done(db, row, said[0], said[1], now())
        return {**row, 'status': 'read', 'description': said[0], 'text': said[1]}
