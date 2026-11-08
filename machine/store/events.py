"""The Store's events (refactor PR 14): the messages and signals each source commits (commit_page, keep_found), the
Android feed, tombstones, reading events back (events, meeting, calendar and its links) and each source's sync
checkpoints. A mixin of Store (assistant.py), like App's mixins; StoreCore (core.py) opens the database and seals
what is written here. Moved out of assistant.py as is."""
import collections
import datetime as dt
import hashlib
import html
import json
import os
import re
import sqlite3
import urllib.request
import uuid

import error_feed
import graph
from machine.sources.android import ANDROID_APP_NAMES, android_app_name
from machine.sources.calendar import (
    all_day_span,
    calendar_edit_times,
    calendar_guests,
    calendar_keys,
    calendar_owned,
    calendar_owner_name,
    calendar_room,
    calendar_rooms,
    room_name,
)
from machine.sources.exclusions import excluded_by_rules, routine_rules
from machine.sources.slack import slack_named, slack_raw_title
from machine.store import history as history_store
from machine.text import encoded
import meeting_notes
import message_seal
from sources import transient
from timeutil import local_tz, now


# Failures in a row before a transient sync failure (a rate limit, the service's own 5xx, the network) goes into the
# error reports: each waits its Retry-After or the poll interval, so this is an hour or more of not reading.
TRANSIENT_REPORT_AFTER = 20


# A signal deferred this many times at the same version is set aside: still pending
# and searchable, but no longer offered in review batches until new content arrives.
SET_ASIDE_AFTER = 2


# One heartbeat may claim this many signals, in a single begin_analysis call if it likes.
RUN_SIGNAL_BUDGET = 120


class EventsStore:
    """Store methods for the events table and the sync checkpoints."""

    def coalesce_android_history(self, account):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            originals = db.execute("SELECT * FROM events WHERE account_id=? AND source_id LIKE 'forwarded:%' ORDER BY occurred_at,id",
                                   (account['id'],)).fetchall()
            if not originals:
                return {'observations_before':0, 'signals_after':0, 'removed':0}
            original_ids = {row['id'] for row in originals}
            if any(original_ids & set(json.loads(row['event_ids'])) for row in db.execute('SELECT event_ids FROM suggestions')):
                raise ValueError('Notification history has suggestion references; reconcile those before merging')
            queued = []
            for row in originals:
                meta = json.loads(row['metadata'])
                queued.append({'id':row['source_id'].removeprefix('forwarded:'), 'received_at':row['occurred_at'],
                    'payload':encoded({'id':row['source_id'].removeprefix('forwarded:'),
                        'at_ms':int(dt.datetime.fromisoformat(row['occurred_at']).timestamp()*1000),
                        'change':meta['change'], 'package_name':meta['package_name'],
                        'notification_key_hash':meta['notification_key_hash'], 'text':row['body'],
                        'security_code_omitted':meta.get('security_code_omitted',False)})})
            events, _ = self.android_feed_batch(account, queued, read_existing=False, settle=False)
            self.exclude_sources(db, account['id'], [r['source_id'] for r in originals], reason='notification_update_merged')
            for event in events:
                # The first observation of each episode supplies a stable source
                # identity. Keep only latest text; pending analysis must re-read it.
                digest_event = {**event, 'metadata':{k:v for k,v in event['metadata'].items()
                    if k not in ('is_active','last_notification_event_ms','last_notification_event_id','updates_merged','snapshot_content_hash','snapshot_checked_at')}}
                values = (event['account_id'],event['source_id'],event['kind'],event['occurred_at'],
                          event['title'],event['body'],encoded(event['metadata']),0,
                          hashlib.sha256(encoded(digest_event).encode()).hexdigest(),now())
                db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,ingested_at) VALUES(?,?,?,?,?,?,?,?,?,?)',values)
            return {'observations_before':len(originals), 'signals_after':len(events), 'removed':len(originals)-len(events)}

    def android_feed_batch(self, account, rows, read_existing=True, settle=True):
        groups = {}
        for row in rows:
            raw = json.loads(row['payload'])
            if 'text' in raw:  # sealed by the Gateway's plugin
                raw['text'] = message_seal.open_inbox(self.sealer, raw['text'])
            groups.setdefault(raw['notification_key_hash'], []).append((row, raw))
        events, consumed = {}, []
        current = dt.datetime.fromisoformat(now())
        with self.connect() as db:
            for key, entries in groups.items():
                # Short quiet period absorbs progress updates; a five-minute cap
                # keeps continuously updating notifications from starving review.
                newest = max(dt.datetime.fromisoformat(row['received_at']) for row, _ in entries)
                oldest = min(dt.datetime.fromisoformat(row['received_at']) for row, _ in entries)
                if (settle and entries[-1][1]['change'] != 'removed' and
                        (current-newest).total_seconds() < 60 and (current-oldest).total_seconds() < 300):
                    continue
                old = db.execute("SELECT * FROM events WHERE account_id=? AND json_extract(metadata,'$.notification_key_hash')=? ORDER BY occurred_at DESC,id DESC LIMIT 1",
                                 (account['id'],key)).fetchone() if read_existing else None
                event = None
                if old:
                    event = {k: old[k] for k in ('account_id','source_id','kind','occurred_at','title','body','deleted')}
                    event['deleted'] = bool(event['deleted'])
                    event['metadata'] = json.loads(old['metadata'])
                for row, raw in entries:
                    consumed.append(row['id'])
                    if event and (raw['at_ms'] < event['metadata'].get('last_notification_event_ms', -1) or
                                  raw['id'] == event['metadata'].get('last_notification_event_id')):
                        continue
                    if raw['change'] == 'removed':
                        if event:
                            event['metadata'].update(is_active=False, last_notification_event_ms=raw['at_ms'],
                                                     last_notification_event_id=raw['id'])
                            events[event['source_id']] = json.loads(encoded(event))
                        continue
                    if event and event['metadata'].get('transport') != 'existing_openclaw_feed':
                        # Adopt an exactly keyed recovery snapshot. Retain its
                        # stable identity; subsequent feed updates then coalesce.
                        event['metadata']['transport'] = 'existing_openclaw_feed'
                    if not event or not event['metadata'].get('is_active', True):
                        package = raw['package_name']
                        event = {'account_id': account['id'], 'source_id': 'notification:' + key + ':' + raw['id'],
                                 'kind': 'android.notification',
                                 'occurred_at': dt.datetime.fromtimestamp(raw['at_ms']/1000,dt.timezone.utc).isoformat(),
                                 'title':'', 'body':'', 'deleted':False,
                                 'metadata':{'package_name':package, 'app_name':android_app_name(package),
                                     'app_name_source':'known_package_label' if package in ANDROID_APP_NAMES else 'package_id_fallback',
                                     'notification_key_hash':key, 'source_account':'unknown', 'transport':'existing_openclaw_feed',
                                     'truncated':True, 'coverage':'Latest forwarded preview per notification; queue/phone gaps possible.',
                                     'updates_merged':0}}
                    event['title'] = (raw.get('text') or event['metadata']['package_name'])[:1000]
                    event['body'] = raw.get('text','')[:40000]
                    event['metadata'].update(is_active=True, change='posted',
                        security_code_omitted=raw.get('security_code_omitted',False),
                        last_notification_event_ms=raw['at_ms'], last_notification_event_id=raw['id'],
                        updates_merged=event['metadata'].get('updates_merged',0)+1)
                    events[event['source_id']] = json.loads(encoded(event))
        return list(events.values()), consumed

    def commit_page(self, account, state, events, record_sync=True, excluded_source_ids=(), android_inbox_ids=(), history=False):
        # The page AND its next cursor commit together. A killed fetch replays the page. history: new rows only (machine/store/history.py).
        rules = self.exclusions.get(account)
        routine = set()
        if rules:
            dropping, keeping = routine_rules(rules)
            dropped = [e['source_id'] for e in events if excluded_by_rules(dropping, e)]
            if dropped:
                events = [e for e in events if e['source_id'] not in set(dropped)]
                excluded_source_ids = [*excluded_source_ids, *dropped]
            routine = {e['source_id'] for e in events if excluded_by_rules(keeping, e)}
        with self.connect() as db:
            if events and graph.anyone_forgotten(db):  # someone the owner deleted permanently: what they send is not kept or learned from
                gone, owner = graph.forgotten(db), graph.Owner({})
                dropped = [e['source_id'] for e in events if isinstance(e.get('metadata'), dict) and graph.from_forgotten(e['kind'], e['metadata'], owner, gone)]
                if dropped:
                    events = [e for e in events if e['source_id'] not in set(dropped)]
                    excluded_source_ids = [*excluded_source_ids, *dropped]
            self.exclude_sources(db, account, excluded_source_ids)
            changed, line = set(), history_store.moved_line(db)  # after an import: what happened before it is never new
            for event in events:
                settled = history_store.from_before(event.get('occurred_at'), line)
                if event['account_id'] != account:
                    raise ValueError('Event account does not match the checkpoint boundary')
                if os.environ.get('MESSAGE_SEAL_AUDIT') and (leaks := message_seal.plain_leaks(event, state)):
                    raise AssertionError(f"{event['kind']} keeps message text in the clear in {', '.join(leaks)}")
                digest_event = event
                if event['kind'] == 'android.notification' and event['metadata'].get('transport') == 'existing_openclaw_feed':
                    digest_event = {**event, 'metadata':{k:v for k,v in event['metadata'].items()
                        if k not in ('is_active','last_notification_event_ms','last_notification_event_id','updates_merged','snapshot_content_hash','snapshot_checked_at')}}
                slack = event['kind'] == 'slack.message' and isinstance(event.get('metadata'), dict)
                if slack:  # its title names people as they become known: the same message, not an edit (slack_raw_title)
                    digest_event = {**event, 'title': slack_raw_title(event)}
                digest = hashlib.sha256(encoded(digest_event).encode()).hexdigest()
                old = db.execute('SELECT id,content_hash' + (',title' if slack else '') + ' FROM events WHERE account_id=? AND source_id=?',
                                 (account, event['source_id'])).fetchone()
                if old and (history or old['content_hash'] == digest):
                    if history:
                        continue
                    if slack:
                        if old['title'] != event['title']:
                            db.execute('UPDATE events SET title=? WHERE id=?', ((self.sealer.seal if self.protected else str)(event['title']), old['id']))
                    elif digest_event is not event:
                        db.execute('UPDATE events SET metadata=? WHERE id=?', (encoded(event['metadata']),old['id']))
                    continue
                changed.add(event['source_id'])
                seal = self.sealer.seal if self.protected else (lambda value: value)
                metadata = self.sealer.seal_json(encoded(event['metadata'])) if self.protected else encoded(event['metadata'])
                values = (event['kind'], event['occurred_at'], seal(event['title']), seal(event['body']),
                          metadata, int(event['deleted']), digest, now())
                if old:
                    db.execute('UPDATE events SET kind=?,occurred_at=?,title=?,body=?,metadata=?,deleted=?,content_hash=?,ingested_at=?,version=version+1,deferrals=0,'
                               'analyzed_version=CASE WHEN history=1 THEN version+1 ELSE analyzed_version END WHERE id=?', (*values, old['id']))
                else:
                    db.execute('INSERT INTO events(kind,occurred_at,title,body,metadata,deleted,content_hash,ingested_at,account_id,source_id,history,analyzed_version) '
                               'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (*values, account, event['source_id'], int(history or settled), int(history or settled)))
                if event['source_id'] in routine or (old and settled):  # on the Calendar, or edited after a move: never a review or a to-do
                    db.execute('UPDATE events SET analyzed_version=version WHERE account_id=? AND source_id=?', (account, event['source_id']))
            if state is None:
                pass  # found by a search (keep_found): no cursor moves
            elif record_sync:
                self.record_sync_activity(db, account, 'success', signals=len(changed))
                self.note_first_import(db, account, state)
                db.execute('INSERT INTO checkpoints(account_id,state,last_success,last_sync_signals) VALUES(?,?,?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state,last_success=excluded.last_success,last_sync_signals=excluded.last_sync_signals,error=NULL,failures=0,retry_at=NULL',
                           (account, encoded(state), now(), len(changed)))
            else:
                # Internal cursor/retry transitions are not successful source reads.
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state',
                           (account, encoded(state)))
            db.executemany('DELETE FROM android_inbox WHERE id=?', [(value,) for value in android_inbox_ids])
            db.executemany('INSERT OR IGNORE INTO android_receipts VALUES(?,?,?)',[(value,account,now()) for value in android_inbox_ids])
            db.execute('DELETE FROM android_receipts WHERE processed_at<?',((dt.datetime.fromisoformat(now())-dt.timedelta(days=30)).isoformat(),))
        return len(changed)

    def keep_found(self, account, events):
        """Messages a mailbox search found (App.mailbox_lookup), kept as collected signals so a to-do can hold them: the
        same exclusions, forgetting and sealing as a sync page (commit_page), but no cursor or sync receipt, and marked
        reviewed (old mail a run looked up is context, never news for the review). One already collected stays as it
        is. Returns their event ids, in the order found."""
        with self.connect() as db:
            have = {r['source_id']: r['id'] for r in db.execute(
                'SELECT id,source_id FROM events WHERE account_id=? AND source_id IN (' + ','.join('?' * len(events)) + ')',
                (account, *[e['source_id'] for e in events]))} if events else {}
        fresh = [e for e in events if e['source_id'] not in have]
        if fresh:
            self.commit_page(account, None, fresh, record_sync=False)
        with self.connect() as db:
            rows = {r['source_id']: r['id'] for r in db.execute(
                'SELECT id,source_id FROM events WHERE account_id=? AND deleted=0 AND source_id IN (' + ','.join('?' * len(events)) + ')',
                (account, *[e['source_id'] for e in events]))} if events else {}
            db.executemany('UPDATE events SET analyzed_version=version WHERE id=?', [(rows[e['source_id']],) for e in fresh if e['source_id'] in rows])
        return [rows[e['source_id']] for e in events if e['source_id'] in rows]

    def record_sync_activity(self, db, account, status, signals=None, error=None, retry_at=None):
        # Source-page receipts share their content/checkpoint transaction. Keep
        # a small redacted history, independent of a transient current error.
        stamp = now()
        db.execute('INSERT INTO sync_activity VALUES(?,?,?,?,?,?,?)',
                   (uuid.uuid4().hex,account,stamp,status,signals,error,retry_at))

    def failed(self, account, error):
        with self.connect() as db:
            retry_at = (dt.datetime.fromisoformat(now()) + dt.timedelta(seconds=error.retry_after)).isoformat() if error.retry_after else None
            self.record_sync_activity(db, account, 'failed', error=str(error), retry_at=retry_at)
            try:  # the error reports: the source's service and the error type, never the account (error_feed.py)
                service_name = str(account).split(':')[0]
                # A rate limit, the service's own 503 or a dropped connection is the service or the network saying
                # "later": the sync waits and reads on. Only one that keeps a source from reading for a long run of
                # tries is worth a report; a sign-in or permission error (401, 403) is reported at once.
                row = db.execute('SELECT failures FROM checkpoints WHERE account_id=?', (account,)).fetchone()
                streak = (row[0] if row and row[0] else 0) + 1
                if transient(error) and streak < TRANSIENT_REPORT_AFTER:
                    pass
                elif re.fullmatch(r'[a-z0-9_-]{1,24}', service_name):
                    error_feed.record(db, 'sync', type(error).__name__, str(error), 'sync', service_name, None, self.code_version)
            except Exception:
                pass
            db.execute('INSERT INTO checkpoints(account_id,state,error,error_at,failures,retry_at) VALUES(?,?,?,?,1,?) ON CONFLICT(account_id) DO UPDATE SET error=excluded.error,error_at=excluded.error_at,failures=failures+1,retry_at=excluded.retry_at',
                       (account, '{}', str(error), now(), retry_at))

    def signed_in_again(self, account_ids):
        """A reconnect that worked: these accounts' sign-in errors end now, and their sync reads at once (no wait for
        the retry). Without it the setup page kept "Sign in to Google again" until the next sync round."""
        with self.connect() as db:
            for account in account_ids:
                db.execute('UPDATE checkpoints SET error=NULL,error_at=NULL,failures=0,retry_at=NULL WHERE account_id=? AND error IS NOT NULL', (account,))

    def tombstone(self, account, source_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM events WHERE account_id=? AND source_id=?', (account, source_id)).fetchone()
            if not row:
                return None
            return {'account_id': account, 'source_id': source_id, 'kind': row['kind'],
                    'occurred_at': row['occurred_at'], 'title': row['title'], 'body': '',
                    'metadata': json.loads(row['metadata']), 'deleted': True}

    def events(self, account_ids, query='', limit=40, pending=False, event_ids=None, reviewable=False, since='', kinds=None):
        if not account_ids:
            raise ValueError('Explicit account_ids are required')
        limit = max(len(set(event_ids)), 1) if event_ids is not None else min(max(int(limit), 1), RUN_SIGNAL_BUDGET)
        sql = 'SELECT e.* FROM events e WHERE e.account_id IN (' + ','.join('?' for _ in account_ids) + ')'
        args = list(account_ids)
        if pending:
            sql += ' AND e.analyzed_version<e.version'
            if reviewable:
                sql += ' AND e.deferrals<?'
                args.append(SET_ASIDE_AFTER)
        else:
            sql += ' AND e.deleted=0'
        if since:
            sql += ' AND e.occurred_at>=?'
            args.append(since)
        if kinds:  # only these kinds (New to-do's Email pill: emails)
            sql += ' AND e.kind IN (' + ','.join('?' for _ in kinds) + ')'
            args.extend(kinds)
        if query:
            sql += ' AND e.id IN (SELECT rowid FROM event_search WHERE event_search MATCH ?)'
            # Treat search input as words, not arbitrary FTS operators.
            args.append(message_seal.match(self, query.split(), ' AND '))
        if event_ids is not None:
            if not event_ids:
                return []
            sql += ' AND e.id IN (' + ','.join('?' for _ in event_ids) + ')'
            args.extend(event_ids)
        # Upcoming appointments nearest first; email and historical signals newest first.
        sql += " ORDER BY CASE WHEN e.kind='calendar.event' AND e.occurred_at>=? THEN 0 ELSE 1 END, "
        sql += "CASE WHEN e.kind='calendar.event' AND e.occurred_at>=? THEN e.occurred_at END ASC, e.occurred_at DESC,e.id DESC LIMIT ?"
        args.extend([now(), now()])
        with self.connect() as db:
            rows = [dict(r) for r in db.execute(sql, (*args, limit))]
            for row in rows:
                row['metadata'] = json.loads(row['metadata'])
            rows = slack_named(db, rows)
        for row in rows:
            if row.get('kind') == 'android.notification':
                row['metadata']['app_name'] = android_app_name(row['metadata'].get('package_name', 'Unknown app'))
        return rows

    def move_meeting_transcripts(self, db):
        """Make what meeting_notes.transcript_moves says, in the caller's transaction, first keeping each row's old kind
        and source_id in meeting_moves (to put it back by hand). [moved event ids]"""
        db.execute(meeting_notes.MOVES)
        moved = []
        for event_id, old_source, new_source, metadata in meeting_notes.transcript_moves(db):
            db.execute('INSERT OR REPLACE INTO meeting_moves VALUES(?,?,?,?,?,?)',
                       (event_id, meeting_notes.NOTES, old_source, meeting_notes.TRANSCRIPT, new_source, now()))
            db.execute('UPDATE events SET kind=?,source_id=?,metadata=? WHERE id=? AND kind=?',
                       (meeting_notes.TRANSCRIPT, new_source, metadata, event_id, meeting_notes.NOTES))
            moved.append(event_id)
        return moved

    def save_meeting_notes(self, db, write):
        """Make what meeting_notes.plan says, in the caller's transaction: notes on a meeting are a signal like any other."""
        if write[0] == 'remove':
            db.execute('UPDATE events SET deleted=1,version=version+1,ingested_at=? WHERE id=?', (now(), write[1]))
            return {}
        r = write[-1]
        if write[0] == 'update':
            db.execute('UPDATE events SET kind=?,occurred_at=?,title=?,body=?,metadata=?,deleted=0,content_hash=?,ingested_at=?,version=version+1,deferrals=0 WHERE id=?',
                       (r['kind'], r['occurred_at'], r['title'], r['body'], r['metadata'], r['content_hash'], r['ingested_at'], write[1]))
            return {'notes_id': write[1]}
        return {'notes_id': db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,ingested_at) '
                                       'VALUES(?,?,?,?,?,?,?,0,?,?)', (r['account_id'], r['source_id'], r['kind'], r['occurred_at'], r['title'], r['body'],
                                                                       r['metadata'], r['content_hash'], r['ingested_at'])).lastrowid}

    def meeting(self, account_ids, event_id, owner=(), writable=(), names=None):
        """One meeting as the Calendar shows it, for its details wherever it is opened (a timeline, Events, a to-do's
        source): the copy the Calendar keeps when it is on several calendars, so its notes and transcript are the same
        ones. One the owner declined still opens. None when the event is no meeting (or not on these accounts)."""
        if not account_ids:
            return None
        with self.connect() as db:
            r = db.execute("SELECT id,title,occurred_at,metadata FROM events WHERE id=? AND kind='calendar.event' AND deleted=0 "
                           'AND account_id IN (' + ','.join('?' for _ in account_ids) + ')', (int(event_id), *account_ids)).fetchone()
        if not r:
            return None
        m = json.loads(r['metadata'])
        at = dt.datetime.fromisoformat(str(r['occurred_at']).replace('Z', '+00:00'))
        at = at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)
        keys = calendar_keys(m, r['title'], r['occurred_at'], m.get('end_at'))
        second = dt.timedelta(seconds=1)
        rows = self._calendar(account_ids, (at - second).isoformat(), (at + second).isoformat(), owner, writable, names, declined=True)
        return next((row for k, row in rows if row['id'] == r['id']), None) or next((row for k, row in rows if k & keys), None)

    def calendar(self, account_ids, start, end, owner=(), writable=(), names=None):
        """Meetings that overlap [start, end), for the dashboard's Calendar: slim rows, soonest first."""
        return [row for _, row in self._calendar(account_ids, start, end, owner, writable, names)]

    def _calendar(self, account_ids, start, end, owner=(), writable=(), names=None, declined=False):
        """[(keys, row)] of the meetings that overlap [start, end), soonest first (calendar); declined keeps the ones the
        owner said no to.
        One that is on someone else's calendar shared with the owner, and that they aren't on, carries that
        person's first name (shared); one on both calendars shows once, as the owner's. One on a calendar the owner
        can change (`writable` account ids) without other people on it carries `edit`: its times for the form."""
        start, end = (dt.datetime.fromisoformat(str(v).replace('Z', '+00:00')) for v in (start, end))
        if start.tzinfo is None or end.tzinfo is None or not dt.timedelta(0) < end - start <= dt.timedelta(days=15):
            raise ValueError('Use a window of at most 15 days, with time zones')
        start, end = start.astimezone(dt.timezone.utc).isoformat(), end.astimezone(dt.timezone.utc).isoformat()
        if not account_ids:
            return []
        with self.connect() as db:
            # by the meetings' own index (events_kind_calendar_event), not each account's events: +account_id keeps SQLite
            # off events_account_time, which walked every message of every account up to the week's end (some 80 ms)
            rows = db.execute("SELECT id,account_id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                              'AND +account_id IN (' + ','.join('?' for _ in account_ids) + ') AND occurred_at<? '
                              "AND coalesce(json_extract(metadata,'$.end_at'),occurred_at)>? ORDER BY occurred_at,id LIMIT 300",
                              (*account_ids, end, start)).fetchall()
        owner = {str(e).lower() for e in owner if e}
        rooms, kept, room_names = calendar_rooms(self.connect)
        found = []
        for r in rows:
            m = json.loads(r['metadata'])
            guests = [a for a in m.get('attendees') or [] if isinstance(a, dict)]
            booked = [a for a in guests if a.get('resource') or calendar_room(a, rooms, kept)]
            attendees = [a for a in guests if not any(a is b for b in booked)]  # a booked room isn't a guest: it shows under Where
            where = [n for n in dict.fromkeys(room_name(a, room_names) for a in booked if a.get('responseStatus') != 'declined') if n]
            shared = m.get('access') == 'shared_read_only'
            mine = owner | {str(m.get('credential_account') or '').lower()}
            me = next((a for a in attendees if (str(a.get('email') or '').lower() in mine if shared else a.get('self'))), {})
            if me.get('responseStatus') == 'declined' and not declined:
                continue  # a meeting the owner said no to isn't on their day
            theirs = not calendar_owned(m, owner)
            url = m.get('source_url')
            people = [str(a.get('displayName') or a.get('email') or '')[:80] for a in attendees if a is not me and (a.get('displayName') or a.get('email'))]
            met = [{'name': str(a.get('displayName') or '')[:80], 'email': str(a.get('email') or '')[:120],
                    **({'declined': True} if a.get('responseStatus') == 'declined' else {})}
                   for a in attendees if a is not me and (a.get('displayName') or a.get('email'))]
            organizer = m.get('organizer') or {}
            if (organizer.get('displayName') and str(organizer.get('email') or '').lower() not in mine and not (organizer.get('self') and not shared)
                    and str(organizer.get('email') or '').lower() not in {w['email'].lower() for w in met if w['email']}):  # on the guest list too: once
                people.append(str(organizer['displayName'])[:80])
                met.append({'name': str(organizer['displayName'])[:80], 'email': str(organizer.get('email') or '')[:120]})
            begins, ends, span = r['occurred_at'], m.get('end_at') or r['occurred_at'], all_day_span(m)
            if span:  # all day: midnight to midnight on its own dates in the owner's zone (day, until: the dates themselves)
                begins, ends = (dt.datetime.combine(dt.date.fromisoformat(d), dt.time(), local_tz()).astimezone(dt.timezone.utc).isoformat() for d in span)
            found.append((theirs, shared, calendar_keys(m, r['title'], r['occurred_at'], m.get('end_at')), {
                'id': r['id'], 'account_id': r['account_id'], 'title': str(r['title'])[:300], 'start': begins,
                'end': ends, 'all_day': bool(m.get('all_day')), **({'day': span[0], 'until': span[1]} if span else {}),
                'location': str(m.get('location') or '')[:200], 'guests': sum(1 for a in attendees if a is not me),
                **({'rooms': [n[:120] for n in where if n.casefold() not in str(m.get('location') or '').casefold()][:4]} if where else {}),
                'people': list(dict.fromkeys(people))[:20], 'with': met, 'shared': ((names or {}).get(r['account_id']) or calendar_owner_name(m)) if theirs else None,
                'url': url if isinstance(url, str) and urllib.parse.urlsplit(url).scheme == 'https' else None,
                **({'edit': dict(zip(('start', 'end', 'all_day'), calendar_edit_times(m)))}
                   if r['account_id'] in writable and not calendar_guests(m, owner) else {})}))
        # Who it's with, by name: the invite's name, else the Graph's for that address, else the address
        unnamed = {w['email'].lower() for f in found for w in f[3]['with'] if not w['name'] and w['email']}
        known = {}
        if unnamed:
            try:
                with self.connect() as db:
                    known = {r[0][6:]: r[1] for r in db.execute("SELECT id,name FROM graph_nodes WHERE kind='person' AND id IN (SELECT 'email:' || value FROM json_each(?))",
                                                                (json.dumps(sorted(unnamed)),)) if r[1] and '@' not in r[1]}
            except sqlite3.OperationalError:
                known = {}
        for f in found:
            row, keys, out = f[3], set(), []
            for w in row['with']:
                key = w['email'].lower() or w['name']
                if key not in keys:
                    keys.add(key)
                    out.append({**w, 'name': w['name'] or known.get(w['email'].lower(), '')})
            row['with'] = out[:20]
            row['people'] = list(dict.fromkeys(w['name'] or w['email'] for w in out))[:20]
        self._calendar_links([f[3] for f in found])
        try:  # a meeting with notes or a transcript added to it says so (by whom, when): its details show them
            with self.connect() as db:
                noted = meeting_notes.added_for(db, [f[3]['id'] for f in found])
        except sqlite3.OperationalError:
            noted = {}
        for f in found:
            f[3].update(noted.get(f[3]['id'], {}))
        for f in found:
            for w in f[3]['with']:
                w.pop('declined', None)
        # The owner's own copy first, so a meeting on their calendar and a shared one shows once, as theirs
        seen, result = set(), []
        for theirs, shared, keys, row in sorted(found, key=lambda f: (f[0], f[1])):
            if keys & seen:
                continue
            seen |= keys
            result.append((keys, row))
        return sorted(result, key=lambda x: (x[1]['start'], x[1]['id']))

    def _calendar_links(self, rows):
        """The Graph behind each meeting, for links in its details: each guest the Graph knows gets their node
        (`node_id` on `with`), and the meeting carries its organizations and open projects (`orgs`, `projects`:
        [{node_id, name}]): the ones it is on, and those of its people. Guesses (probable) are left out. Only what
        the Graph already shows the owner."""
        ids = [r['id'] for r in rows]
        if not ids:
            return
        try:
            with self.connect() as db:
                found = db.execute(
                    'SELECT g.event_id,n.id,n.kind,n.name,n.info,o.id org_id,o.name org_name FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id '
                    "LEFT JOIN graph_nodes o ON n.kind='person' AND o.kind='org' AND o.id=json_extract(n.info,'$.org') "
                    "WHERE g.probable=0 AND (n.kind IN ('person','org') OR n.kind='project' AND json_extract(n.info,'$.closed_at') IS NULL) AND g.event_id IN (SELECT value FROM json_each(?)) "
                    'ORDER BY n.strength DESC', (json.dumps(ids),)).fetchall()
                people = sorted({r['id'] for r in found if r['kind'] == 'person'})
                # The open projects its people are on, and the ones its own signal was filed under
                on_people = db.execute("SELECT l.a,'project:'||p.id,p.name FROM graph_links l JOIN projects p ON 'project:'||p.id=l.b "
                                       "WHERE l.kind='project' AND p.closed_at IS NULL AND l.a IN (SELECT value FROM json_each(?)) ORDER BY p.id",
                                       (json.dumps(people),)).fetchall() if people else []
                filed = db.execute("SELECT e.event_id,'project:'||p.id,p.name FROM event_projects e JOIN projects p ON p.id=e.project_id "
                                   'WHERE p.closed_at IS NULL AND e.event_id IN (SELECT value FROM json_each(?))', (json.dumps(ids),)).fetchall()
                rooms = graph.resources(db)
        except sqlite3.OperationalError:
            return  # no Graph yet
        per, projects_of = collections.defaultdict(list), collections.defaultdict(list)
        for r in found:
            per[r['event_id']].append(r)
        for who, node, name in on_people:
            projects_of[who].append((node, name))
        for row in rows:
            emails, orgs, projects, theirs, outside = {}, {}, {}, {}, 0
            for event_id, node, name in filed:
                if event_id == row['id']:
                    projects.setdefault(node, name)
            for r in per.get(row['id'], ()):
                if r['kind'] == 'person' and r['id'] in rooms:
                    continue
                if r['kind'] == 'person':
                    info = json.loads(r['info'] or '{}')
                    for i in (info.get('identifiers') or [r['id']]):
                        if str(i).startswith('email:'):
                            emails.setdefault(str(i)[6:].lower(), r['id'])
                    if r['org_id'] and r['org_name']:
                        orgs.setdefault(r['org_id'], r['org_name'])
                    outside += not info.get('colleague')
                    for node, name in projects_of.get(r['id'], ()):
                        theirs.setdefault(node, [name, 0, False])
                        theirs[node][1] += 1
                        theirs[node][2] = theirs[node][2] or not info.get('colleague')
                elif r['kind'] == 'org':
                    orgs.setdefault(r['id'], r['name'])
                else:
                    projects.setdefault(r['id'], r['name'])
            # A project of its people is what the meeting is about when several of them are on it together, or when it is
            # one outside guest's and they are the only one: a teammate on every project doesn't make each one this meeting's.
            for node, (name, many, outsider) in sorted(theirs.items(), key=lambda kv: -kv[1][1]):
                if many >= 2 or (outsider and outside == 1):
                    projects.setdefault(node, name)
            out, nodes = [], {}
            for w in row['with']:
                if 'email:' + w['email'].lower() in rooms:
                    continue  # a meeting room the Graph knows is one: not someone it's with
                if emails.get(w['email'].lower()):
                    w['node_id'] = emails[w['email'].lower()]
                    if w['node_id'] in nodes:  # one person with two addresses on the invite: once, by the one that's coming
                        kept = nodes[w['node_id']]
                        if kept.get('declined') and not w.get('declined'):
                            kept, w = w, kept
                            out[out.index(w)] = nodes[kept['node_id']] = kept
                        kept['name'] = kept.get('name') or w.get('name') or ''  # and by the name either address gave
                        continue
                    nodes[w['node_id']] = w
                out.append(w)
            if len(out) != len(row['with']):
                gone = {w['email'].lower() for w in row['with']} - {w['email'].lower() for w in out}
                row['guests'] = max(0, row['guests'] - len(gone))
                row['with'] = out
                row['people'] = list(dict.fromkeys(w['name'] or w['email'] for w in out))[:20]
            if orgs:
                row['orgs'] = [{'node_id': k, 'name': str(v)[:80]} for k, v in orgs.items()][:6]
            if projects:
                row['projects'] = [{'node_id': k, 'name': str(v)[:80]} for k, v in projects.items()][:6]

    def name_slack_titles(self, account_id, ids=None):
        """Writes stored Slack titles again with people's names in place of member ids ("#DM U02AB3CD4: hi" becomes
        "#DM Sam Lee: hi"): all of them, or those of the messages with these members (a name just learned). The content
        hash stays (slack_raw_title): no message looks new or edited for it."""
        changed = 0
        with self.connect() as db:
            rows = db.execute("SELECT id,title,body,metadata FROM events WHERE kind='slack.message' AND account_id=? AND deleted=0", (account_id,)).fetchall()
            found = []
            for r in rows:
                m = json.loads(r['metadata'] or '{}')
                on = set(graph.slack_members_on(m)) | {x[0] for x in graph.SLACK_MENTION.findall(str(r['body'] or ''))}
                if ids is not None and not on & set(ids):
                    continue
                if not graph.slack_title_unnamed(r['title']):
                    continue
                found.append((r, m, on))
            names = graph.slack_names(db, {u for _, _, on in found for u in on})
            seal = self.sealer.seal if self.protected else (lambda value: value)
            for r, m, _ in found:
                title = graph.slack_title(m.get('channel_name'), html.unescape(str(r['body'] or '')), names)
                if title != r['title']:
                    db.execute('UPDATE events SET title=? WHERE id=?', (seal(title), r['id']))
                    changed += 1
        return changed
