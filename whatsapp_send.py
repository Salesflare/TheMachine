"""Sending on WhatsApp: one owner-approved text, or one file with its caption, into an existing chat of the owner's own
linked WhatsApp, with wacli. next_actions.validate checks the draft; this sends it after the owner's Send now."""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from machine.owner_error import OwnerError


class WhatsAppTransport:
    """Sends one owner-approved WhatsApp text, or one file with its caption, into an existing chat with wacli. Only this send runs
    wacli without --read-only; every check before and after it stays read-only. When the sync keeps
    the store open, wacli hands the send to that running process. wacli has no idempotency token,
    so an unclear outcome is checked in the chat afterwards and never resent."""

    def __init__(self, config):
        self.config = config

    def account(self, action):
        return next(a for a in self.config['accounts'] if a['id'] == action['account_id'] and a.get('service') == 'whatsapp')

    def run(self, action, args, write=False, timeout=30):
        env = {k: v for k, v in os.environ.items() if k != 'WACLI_READONLY'}
        if not write:
            env['WACLI_READONLY'] = '1'
        command = [self.config.get('wacli') or 'wacli', '--store', self.account(action)['store'],
                   *([] if write else ['--read-only']), '--json', *args]
        return subprocess.run(command, env=env, capture_output=True, text=True, timeout=timeout)

    def read(self, action, args):
        try:
            result = self.run(action, ['--timeout', '15s', *args], timeout=25)
            data = {} if result.returncode else json.loads(result.stdout or '{}')
        except (subprocess.TimeoutExpired, ValueError):
            data = {}
        if not isinstance(data, dict) or data.get('success') is not True or not isinstance(data.get('data'), dict):
            raise OwnerError('I couldn’t reach WhatsApp on this computer. Nothing was sent; tap Send again.')
        return data['data']

    def preflight(self, action):
        if action['kind'] != 'whatsapp':
            raise OwnerError('Only an owner-approved WhatsApp message can use the WhatsApp transport')
        status = self.read(action, ['auth', 'status'])
        linked = status.get('linked_jid')
        if (status.get('authenticated') is not True or not isinstance(linked, str)
                or hashlib.sha256(linked.encode()).hexdigest() != self.account(action).get('identity_sha256')):
            raise OwnerError('WhatsApp is signed out, or linked to another number. Nothing was sent.')
        rows = self.read(action, ['messages', 'list', '--chat', action['chat_id'], '--limit', '50']).get('messages')
        if not rows:
            raise OwnerError('I couldn’t find that WhatsApp chat. Nothing was sent.')
        action['proof'] = {'whatsapp_before_ids': [r['MsgID'] for r in rows if r.get('MsgID')]}

    def send(self, action, job):
        quote = action.get('quote') or {}  # a reply to the to-do's own message in this chat quotes it
        reply = [*(['--reply-to', quote['message_id']] if quote else []),
                 *(['--reply-to-sender', quote['sender_id']] if quote.get('sender_id') else [])]
        folder = None
        try:
            if action.get('attachments'):
                # The approved bytes (checked against their checksum), in a private folder only for this send: the
                # store's copy may be sealed, and wacli (or the sync it hands the send to) reads a plain file.
                record = action['attachments'][0]
                from next_actions import attachment_bytes, attachment_store  # next_actions imports this module
                data = attachment_bytes(record, self.config)
                folder = Path(tempfile.mkdtemp(prefix='whatsapp-send-', dir=attachment_store(self.config)))
                path = folder / 'file'
                path.write_bytes(data)
                args = ['send', 'file', '--to', action['chat_id'], '--file', str(path), '--filename', record['name'],
                        '--mime', record['type'], *(['--caption', action['body']] if action['body'] else []), *reply]
            else:
                args = ['send', 'text', '--to', action['chat_id'], '--message', action['body'], *reply]
            result = self.run(action, ['--timeout', '90s', '--lock-wait', '30s', *args], write=True, timeout=150)
        except subprocess.TimeoutExpired:
            return {}
        finally:
            if folder:
                shutil.rmtree(folder, ignore_errors=True)
        try:
            out = json.loads(result.stdout or '{}')
        except ValueError:
            out = {}
        data = out.get('data') if isinstance(out.get('data'), dict) else {}
        if not result.returncode and out.get('success') is True and data.get('sent') is True and data.get('id'):
            return {'message_id': 'whatsapp:' + str(data['id'])}
        err = ((out.get('error') or '') if isinstance(out.get('error'), str) else '') + ' ' + result.stderr
        err = err.lower()
        if 'may still have gone through' in err or 'after dispatch' in err:
            return {}  # Unknown outcome: never resend; reconcile reads the chat.
        if 'lock' in err and 'store' in err:
            return {'not_sent': True}
        if 'not authenticated' in err or 'not logged in' in err or 'read-only' in err or 'invalid' in err:
            return {'rejected': 'refused'}
        return {}

    def reconcile(self, action, job):
        proof = action.get('proof') or {}
        stamp = proof.get('whatsapp_dispatched_at')
        if not stamp:
            return {}  # Legacy uncertain sends have no attributable dispatch boundary; never invent a receipt.
        try:
            since = datetime.datetime.fromisoformat(stamp)
            if since.tzinfo is None:
                return {}
            rows = self.read(action, ['messages', 'list', '--chat', action['chat_id'], '--from-me',
                                      '--after', since.isoformat(), '--limit', '50']).get('messages') or []
        except ValueError:
            return {}
        found = []
        for r in rows:
            try:
                occurred = datetime.datetime.fromisoformat(r.get('Timestamp', '').replace('Z', '+00:00'))
            except (ValueError, TypeError, AttributeError):
                continue
            if occurred.tzinfo is None:
                continue
            if action.get('attachments'):  # a file: its kind of row, its caption, and its name when WhatsApp keeps one
                name = action['attachments'][0]['name']
                same = (bool(r.get('MediaType')) and (r.get('MediaCaption') or '').strip() == action['body']
                        and (r.get('Filename') or name) == name)
            else:
                same = (r.get('Text') or '').strip() == action['body']
            if (r.get('FromMe') is True and same
                    and r.get('MsgID') not in proof.get('whatsapp_before_ids', []) and occurred >= since):
                found.append(r)
        return {'message_id': 'whatsapp:' + str(found[0]['MsgID'])} if len(found) == 1 and found[0].get('MsgID') else {}
