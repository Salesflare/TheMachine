"""WhatsApp as a source: the wacli client (WhatsApp), the photo askers, a message as an event (whatsapp_event), the
chats that are the owner's, where a reply goes (reply_spots), the first sync's history window and its sync
(sync_whatsapp). Moved out of assistant.py as is."""
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import time

import graph
from machine.sources.connectors import load_connector
from machine.sources.rows import Skips
from machine.text import encoded
from sources import SourceError
from timeutil import local_tz, now
import whatsapp_images


class WhatsApp:
    def __init__(self, config, account):
        self.config, self.account = config, account

    def read(self, command):
        if command[:2] not in (['auth', 'status'], ['messages', 'list'], ['chats', 'show'], ['chats', 'list'], ['profile', 'picture-info']):
            raise SourceError('unsupported_whatsapp_method')
        env = os.environ.copy()
        env['WACLI_READONLY'] = '1'
        args = [self.config.get('wacli', 'wacli'), '--store', self.account['store'],
                '--read-only', '--json', '--timeout', '15s', *command]
        try:
            result = subprocess.run(args, env=env, capture_output=True, text=True, timeout=20)
        except subprocess.TimeoutExpired:
            raise SourceError('whatsapp_read_timeout') from None
        except OSError:
            raise SourceError('whatsapp_source_unavailable') from None
        if result.returncode:
            raise SourceError('whatsapp_source_unavailable')
        try:
            data = json.loads(result.stdout)
        except ValueError:
            raise SourceError('whatsapp_invalid_json') from None
        if data.get('success') is not True or data.get('error') is not None or not isinstance(data.get('data'), list if command[:2] == ['chats', 'list'] else dict):
            raise SourceError('whatsapp_invalid_response')
        return data['data']

    def profile(self):
        data = self.read(['auth', 'status'])
        linked = data.get('linked_jid')
        if (data.get('authenticated') is not True or not isinstance(linked, str)
                or hashlib.sha256(linked.encode()).hexdigest() != self.account['identity_sha256']):
            raise SourceError('account_identity_mismatch')
        return data

    def picture(self, jid):
        """A person's profile picture, asked through the always-on mirror (`wacli sync --follow --profile-picture-budget`),
        which owns the session: {'id', 'url'}, or {} when they have none the owner can see. Read-only here: wacli only
        passes this one query on to the mirror, and refuses it when no mirror answers (SourceError)."""
        if not re.fullmatch(r'[0-9]{5,20}@(?:s\.whatsapp\.net|lid)', str(jid)):
            raise SourceError('whatsapp_invalid_person')
        data = self.read(['profile', 'picture-info', '--jid', jid])
        if data.get('none') is True or data.get('unchanged') is True:
            return {}
        url, picture = str(data.get('url') or ''), str(data.get('id') or '')
        return {'id': picture[:64], 'url': url} if url.startswith('https://') and picture else {}

    def download(self, chat, message_id, target):
        """One message's photo into `target` (a file in a private folder), read-only: wacli takes the media key and the
        checksums from its own store and the bytes from WhatsApp's media servers, checks them, and writes nothing else
        (`--read-only`: no session, no phone recovery). Returns wacli's answer ({'path', 'bytes', 'mime_type', ...})."""
        if not re.fullmatch(WHATSAPP_JID, str(chat)) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', str(message_id)):
            raise SourceError('whatsapp_invalid_message')
        env = os.environ.copy()
        env['WACLI_READONLY'] = '1'
        args = [self.config.get('wacli', 'wacli'), '--store', self.account['store'], '--read-only', '--json', '--timeout', '60s',
                'media', 'download', '--chat', chat, '--id', message_id, '--output', str(target)]
        try:
            result = subprocess.run(args, env=env, capture_output=True, text=True, timeout=75)
            data = json.loads(result.stdout) if result.returncode == 0 else None
        except subprocess.TimeoutExpired:
            raise SourceError('whatsapp_read_timeout') from None
        except (OSError, ValueError):
            raise SourceError('whatsapp_source_unavailable') from None
        if not isinstance(data, dict) or data.get('success') is not True or not isinstance(data.get('data'), dict):
            raise SourceError('whatsapp_media_unavailable')
        if str(data['data'].get('path') or '') != str(target):
            raise SourceError('whatsapp_invalid_response')
        return data['data']


def whatsapp_photo_asker(config):
    """ask(account id, jid) for enrichment.whatsapp_photos_step: the owner's own WhatsApp accounts only (never one
    shared from a Fleet); None when the mirror can't answer."""
    accounts = {a['id']: a for a in config.get('accounts', []) if a.get('service') == 'whatsapp' and a.get('store') and not a.get('shared')}
    def ask(account_id, jid):
        try:
            return WhatsApp(config, accounts[account_id]).picture(jid)
        except (SourceError, KeyError):
            return None
    return list(accounts), ask


WHATSAPP_JID = r'(?:[0-9]+(?::[0-9]+)?@(?:s\.whatsapp\.net|lid)|[0-9]+(?:-[0-9]+)?@g\.us)'


def reply_spots(config, db, event_ids):
    """The Slack, WhatsApp and Signal messages a to-do came from, newest first, for a reply to go in their thread or quote
    them (next_actions.slack_thread, whatsapp_quote): the to-do's own messages, and a message a teammate's Machine carried
    (fleet.message) when this Machine has that same message itself (same moment and text). One carried that it
    doesn't have stays without a place ('service': None), so the draft says what it answers (next_actions.reply_context)."""
    accounts = {a['id']: a for a in config.get('accounts', [])}
    rows = db.execute("SELECT e.id,e.account_id,e.kind,e.body,e.metadata,e.occurred_at FROM events e JOIN json_each(?) ids ON ids.value=e.id "
                      "WHERE e.kind IN ('slack.message','whatsapp.message','signal.message','fleet.message') AND e.deleted=0 ORDER BY e.occurred_at DESC",
                      (event_ids or '[]',)).fetchall()
    spots = []
    for row in rows:
        if row['kind'] == 'fleet.message':
            own = [r for r in db.execute("SELECT id,account_id,kind,body,metadata,occurred_at FROM events WHERE occurred_at=? AND deleted=0 "
                                         "AND kind IN ('slack.message','whatsapp.message')", (row['occurred_at'],))
                   if ' '.join(str(r['body'] or '').split()) == ' '.join(str(row['body'] or '').split()) and str(row['body'] or '').strip()]
            if len(own) != 1:
                carried = json.loads(row['metadata'] or '{}')
                spots.append({'service': None, 'when': row['occurred_at'], 'carried_by': carried.get('carried_by'), 'from': carried.get('from')})
                continue
            row = own[0]
        account, m = accounts.get(row['account_id']) or {}, json.loads(row['metadata'] or '{}')
        if row['kind'] == 'slack.message' and account.get('service') == 'slack':
            channel, ts = str(m.get('channel_id') or ''), str(m.get('message_ts') or '')
            if not re.fullmatch(r'[CDG][A-Z0-9]{6,20}', channel) or not re.fullmatch(r'[0-9]{6,12}\.[0-9]{1,8}', ts):
                continue
            thread = str(m.get('thread_ts') or ts)
            dm = m.get('conversation_type') == 'dm' or channel.startswith('D')
            later = db.execute("SELECT 1 FROM events WHERE account_id=? AND kind='slack.message' AND deleted=0 AND json_extract(metadata,'$.channel_id')=? "
                               "AND occurred_at>? LIMIT 1", (row['account_id'], channel, row['occurred_at'])).fetchone() is not None
            members = sorted({r[0] for r in db.execute("SELECT DISTINCT json_extract(metadata,'$.user_id') FROM events WHERE account_id=? AND kind='slack.message' "
                                                        "AND json_extract(metadata,'$.channel_id')=?", (row['account_id'], channel))
                              if r[0] and r[0] != account.get('user_id')}) if dm else []
            spots.append({'service': 'slack', 'account_id': row['account_id'], 'channel_id': channel, 'ts': ts,
                          'thread_ts': thread if re.fullmatch(r'[0-9]{6,12}\.[0-9]{1,8}', thread) else ts, 'dm': dm,
                          'channel_name': str(m.get('channel_name') or ''), 'sender_id': m.get('user_id'),
                          'sender_name': str(m.get('sender_display') or ''), 'own': bool(account.get('user_id')) and m.get('user_id') == account.get('user_id'),
                          'members': members, 'later': later, 'when': row['occurred_at']})
        elif row['kind'] == 'whatsapp.message' and account.get('service') == 'whatsapp' and m.get('chat_id') and m.get('message_id'):
            later = db.execute("SELECT 1 FROM events WHERE account_id=? AND kind='whatsapp.message' AND deleted=0 AND json_extract(metadata,'$.chat_id')=? "
                               "AND occurred_at>? LIMIT 1", (row['account_id'], m['chat_id'], row['occurred_at'])).fetchone() is not None
            sender = m.get('sender_id') if isinstance(m.get('sender_id'), str) and re.fullmatch(WHATSAPP_JID, m['sender_id']) else None
            spots.append({'service': 'whatsapp', 'account_id': row['account_id'], 'chat_id': m['chat_id'], 'message_id': str(m['message_id']),
                          'sender_id': sender, 'group': str(m['chat_id']).endswith('@g.us'), 'later': later, 'when': row['occurred_at']})
        elif row['kind'] == 'signal.message' and account.get('service') == 'signal' and m.get('chat_id') and m.get('message_id'):
            later = db.execute("SELECT 1 FROM events WHERE account_id=? AND kind='signal.message' AND deleted=0 AND json_extract(metadata,'$.chat_id')=? "
                               "AND occurred_at>? LIMIT 1", (row['account_id'], m['chat_id'], row['occurred_at'])).fetchone() is not None
            spots.append({'service': 'signal', 'account_id': row['account_id'], 'chat_id': m['chat_id'], 'message_id': str(m['message_id']),
                          'group': m.get('chat_kind') == 'group', 'later': later, 'when': row['occurred_at']})
    return spots


def owner_whatsapp_chats(config, db, raw, task_chats, source=None):
    """The chats a prepare's WhatsApp messages go to that are not from the task's own messages: the person's
    existing chat in the owner's own WhatsApp account, for a card that switches to WhatsApp because that is
    where the owner talks to them. A chat_id is checked against the account's synced messages, else its chat
    list (read-only); a to_name alone is looked up there and must match one chat. Never a new number, never a
    chat the owner excluded. Returns {chat_id: {account_id, name, switched}} and fills in the chat_id it found."""
    found = {}
    for item in raw if isinstance(raw, list) else [raw]:
        if not isinstance(item, dict) or item.get('kind') != 'whatsapp' or str(item.get('chat_id') or '') in task_chats:
            continue
        account = next((a for a in config['accounts'] if a['id'] == item.get('account_id') and a.get('service') == 'whatsapp'), None)
        if not account:
            continue
        excluded = {c for r in account.get('exclude') or [] if set(r) == {'chats'} for c in r['chats']}
        reader = source(config, account) if source else WhatsApp(config, account)
        chat_id, name = str(item.get('chat_id') or ''), None
        if chat_id:
            if not re.fullmatch(WHATSAPP_JID, chat_id) or chat_id in excluded:
                continue
            row = db.execute("SELECT metadata FROM events WHERE kind='whatsapp.message' AND account_id=? AND json_extract(metadata,'$.chat_id')=? "
                             'ORDER BY occurred_at DESC LIMIT 1', (account['id'], chat_id)).fetchone()
            if row:
                name = json.loads(row['metadata']).get('chat_name')
            else:
                try:
                    chat = reader.read(['chats', 'show', '--jid', chat_id])
                except SourceError:
                    continue
                if chat.get('jid') != chat_id:
                    continue
                name = chat.get('name')
        elif isinstance(item.get('to_name'), str) and 2 <= len(item['to_name'].strip()) <= 100:
            try:
                chats = reader.read(['chats', 'list', '--query', item['to_name'].strip(), '--limit', '10'])
            except SourceError:
                raise ValueError('WhatsApp can’t be read right now, so I can’t find the chat. Put the message in the body and say '
                                 'in one line that they can send it on WhatsApp themselves.') from None
            chats = [c for c in chats if isinstance(c, dict) and isinstance(c.get('jid'), str) and re.fullmatch(WHATSAPP_JID, c['jid'])
                     and c['jid'] not in excluded] if isinstance(chats, list) else []
            people = [c for c in chats if c.get('kind') == 'dm'] or chats
            if len(people) != 1:
                raise ValueError(('More than one WhatsApp chat matches: ' + '; '.join(f"{c.get('name') or 'chat'} (chat_id {c['jid']})" for c in people[:5])
                                  + '. Give the right chat_id.') if people else
                                 'No WhatsApp chat with ' + item['to_name'].strip() + ' in this account. Never start a new one: put the message '
                                 'in the body and say in one line that they can send it on WhatsApp themselves.')
            chat_id, name = people[0]['jid'], people[0].get('name')
            item['chat_id'] = chat_id
        else:
            continue
        found[chat_id] = {'account_id': account['id'], 'name': name or 'WhatsApp chat', 'switched': True}
    return found


def whatsapp_event(account, raw):
    jid, mid, timestamp = raw.get('ChatJID'), raw.get('MsgID'), raw.get('Timestamp')
    if (not isinstance(jid, str) or not re.fullmatch(r'(?:[0-9]+(?::[0-9]+)?@(?:s\.whatsapp\.net|lid)|[0-9]+(?:-[0-9]+)?@g\.us)', jid)
            or not isinstance(mid, str) or not mid or mid.startswith('imported_')
            or any(c.isspace() or ord(c) < 32 for c in mid) or type(raw.get('FromMe')) is not bool
            or not isinstance(timestamp, str)):
        raise SourceError('whatsapp_invalid_message')
    try:
        stamp = dt.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        raise SourceError('whatsapp_invalid_timestamp') from None
    if stamp.tzinfo is None:
        raise SourceError('whatsapp_missing_timezone')
    for key in ('Text','DisplayText','MediaCaption'):
        if key in raw and not isinstance(raw[key], str):
            raise SourceError('whatsapp_invalid_content')
    # wacli stores a row for every message it sees, also those with nothing to read: WhatsApp's own notices from a
    # history sync (the encryption notice, a member who joined, a changed number), a message still on its way, a type
    # it doesn't parse. Their DisplayText is a placeholder, "(message)", or a quoted reply above one. Such a row is
    # kept deleted (so one taken in before goes too); a later copy with content replaces it.
    display = raw.get('DisplayText') or ''
    if re.fullmatch(r'(?s)(?:> .*\n)?\(message\)\s*', display):
        display = ''
    body = raw.get('Text') or display or raw.get('MediaCaption') or ''
    caption = raw.get('MediaCaption') or ''
    if caption and caption not in body:
        body += '\n' + caption
    empty = not body.strip()
    if empty and raw.get('MediaType'):  # a photo or file without a caption: say what it is
        body, empty = 'Sent ' + str(raw['MediaType']).replace('_', ' '), False
    sensitive = bool(re.search(r'(?i)verification code|security code|one.time (?:code|password)|\bOTP\b|verificatiecode', body))
    if sensitive:
        body = '[One-time security code omitted]'
    identity = hashlib.sha256(encoded([jid, mid, raw['FromMe']]).encode()).hexdigest()
    sender = raw.get('SenderJID') or ''
    sender_known = bool(re.fullmatch(r'[0-9]+(?::[0-9]+)?@(?:s\.whatsapp\.net|lid)', sender))
    revoked = raw.get('Revoked') is True or raw.get('DeletedForMe') is True
    metadata = {'chat_name': raw.get('ChatName') or 'WhatsApp chat', 'chat_id': jid,
                'message_id': mid, 'from_me': raw['FromMe'], 'sender_id': None if raw['FromMe'] else sender,
                'sender_identity': 'authenticated_account_owner' if raw['FromMe'] else ('source_label_unverified' if sender_known else 'unknown'),
                'from': 'You' if raw['FromMe'] else (raw.get('SenderName') or ('Unknown sender' if jid.endswith('@g.us') else raw.get('ChatName') or 'Unknown sender')),
                'sender_display': 'You' if raw['FromMe'] else (raw.get('SenderName') or ('Unknown sender' if jid.endswith('@g.us') else raw.get('ChatName') or 'Unknown sender')),
                'sender_display_source': 'authenticated_account_owner' if raw['FromMe'] else 'source_label_unverified',
                'edited': raw.get('Edited') is True, 'revoked': revoked, 'no_content': empty,
                'forwarded': raw.get('IsForwarded') is True,
                'media_type': raw.get('MediaType') or '', 'media_collected': False,
                'security_code_omitted': sensitive, 'truncated': len(body) > 40000,
                'transport': 'existing_wacli_local_store',
                'coverage': 'Available synced messages, not proof of complete or live account sync.'}
    return {'account_id':account['id'], 'source_id':identity, 'kind':'whatsapp.message',
            'occurred_at':stamp.astimezone(dt.timezone.utc).isoformat(),
            'title':metadata['chat_name'][:1000], 'body':body[:40000], 'metadata':metadata, 'deleted':revoked or empty}


def sync_whatsapp(store, config, account, source=None):
    source = source or WhatsApp(config, account)
    linked = source.profile()
    if isinstance(linked, dict) and linked.get('linked_jid'):
        with store.connect() as db:  # the owner's own number: theirs in the graph, findable on the Network (hashed)
            graph.keep_linked_number(db, linked['linked_jid'], now())
    stamp = dt.datetime.fromisoformat(now())
    after = (stamp - dt.timedelta(days=config.get('bootstrap_days', 7))).isoformat()
    before = stamp.isoformat()
    def read_window(start, end):
        page = source.read(['messages','list','--after',start.isoformat(),'--before',end.isoformat(),'--limit','1000'])
        rows = page.get('messages')
        if not isinstance(rows, list):
            raise SourceError('whatsapp_invalid_page')
        if len(rows) < 1000:
            return rows
        # CLI has no opaque page cursor; split a saturated window rather than
        # failing every poll during a busy week. A saturated hour still fails
        # visibly: it must not claim to be complete.
        if end - start <= dt.timedelta(hours=1):
            raise SourceError('whatsapp_window_limit')
        middle = start + (end - start) / 2
        return read_window(start, middle) + read_window(middle, end)
    rows = read_window(dt.datetime.fromisoformat(after), stamp)
    # A row this importer can't take (a WhatsApp Channel post from an ...@newsletter chat, a status update, an imported
    # row, an odd timestamp) is skipped and counted by reason, never failing the whole account (machine/sources/rows.py).
    skipped = Skips()
    pairs = skipped.every(rows, lambda raw: whatsapp_event(account, raw if isinstance(raw, dict) else {}))
    skipped.check()
    events = list({e['source_id']: e for e, _ in pairs}.values())
    with store.connect() as db:  # photos the owner has read (whatsapp_images.py): noted, and joined to their message once read
        events = whatsapp_images.note(db, account, events, {e['source_id']: raw for e, raw in pairs}, now())
    state = store.checkpoint(account['id']) or {}
    state.update(mode='incremental', after=after, before=before, retained_days=config.get('bootstrap_days', 7),
                 available_messages=len(rows), skipped_messages=dict(sorted(skipped.items())), source_latest_message=max((e['occurred_at'] for e in events), default=None),
                 upstream_live_sync='Not established by a successful local read',
                 coverage='Seven-day reread of existing synced store. No network sync, backfill or media download by this collector.')
    store.commit_page(account['id'], state, events)
    return {'mode':'incremental','events':len(events),'filtered':sum(skipped.values())}
