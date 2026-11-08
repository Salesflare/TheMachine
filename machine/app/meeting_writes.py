"""Meeting writes in the service (meeting_writer.py writes them): the queue a meeting note or a calendar change waits in,
its worker and one run with the model (meeting_write_run), resumed after a restart; and the meeting_notes tool that reads
and adds a meeting's Notes and Transcript. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import hashlib
import logging
import re
import sqlite3
import threading
import time

import calendar_writes
import i18n
import locale_prefs
from machine.sources.calendar import calendar_write_events
from machine.text import encoded
import meeting_notes
import meeting_writer
from models import background_model, has_model
from sources import CALENDAR_SERVICES, credential, gog_read
from timeutil import local_tz, now

LOG = logging.getLogger('personal-assistant')


class MeetingWritesApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    # ------------------------------------------------------------------ Generate notes (meeting_writer.py)
    MEETING_WRITE_SECONDS = 600  # one model turn on a part of a long transcript

    def meeting_write(self, args):
        """The owner's Generate notes on a meeting in the Calendar: queue The Machine writing its Notes from its
        Transcript on the service, so it goes on when the dialog or the dashboard closes. Only when it has a transcript
        and no notes. The job's view."""
        calendars = [a['id'] for a in self.config['accounts'] if a.get('service') in CALENDAR_SERVICES]
        if not getattr(self, 'notes_model', None) and not has_model(self.config):
            raise ValueError(i18n.t('Writing notes needs a model. Set one up in Settings, Model.'))
        with self.store.connect() as db:
            event = meeting_notes.meeting(db, args.get('event_id'))
            if not event or event['account_id'] not in calendars:
                raise ValueError('That meeting is not there anymore')
            meeting_writer.source(db, event['id'])  # raises when it has notes or no transcript
            db.execute('BEGIN IMMEDIATE')
            found = meeting_writer.start(db, event['id'], now())
        self.meeting_write_kick()
        return {'event_id': event['id'], 'writing': found}

    def meeting_write_kick(self):
        """Make sure the writer runs: one thread, started when there is work and gone when there is none."""
        if not hasattr(self, '_meeting_write_lock'):
            self._meeting_write_lock, self._meeting_write_thread = threading.Lock(), None
        with self._meeting_write_lock:
            wake = getattr(self, 'meeting_write_wake', None)
            if wake:
                wake.set()
            if self._meeting_write_thread is None:
                self.meeting_write_wake = threading.Event()
                self._meeting_write_thread = threading.Thread(target=self.meeting_write_worker, name='meeting-notes', daemon=True)
                self._meeting_write_thread.start()

    def meeting_write_worker(self):
        while not (getattr(self, 'stop', None) and self.stop.is_set()):
            with self._meeting_write_lock:
                with self.store.connect() as db:
                    job = meeting_writer.next_job(db, time.time())
                if job is None:
                    self._meeting_write_thread = None
                    return
                self.meeting_write_wake.clear()
            event_id, wait = job
            if wait > 0:
                self.meeting_write_wake.wait(min(wait, 600))
                with self.store.connect() as db:
                    db.execute("UPDATE meeting_writes SET status='queued' WHERE event_id=? AND status='waiting' AND COALESCE(until,0)<=?", (event_id, time.time()))
                continue
            try:
                self.meeting_write_run(event_id)
            except Exception as error:  # noqa: BLE001 - one meeting's failure never stops the others
                LOG.warning('meeting notes not written error=%s', type(error).__name__)
                with self.store.connect() as db:
                    meeting_writer.mark(db, event_id, now(), status='failed', error='failed')

    def meeting_write_model(self, prompt):
        """One turn on the owner's model for notes: the cheaper background model when there is one."""
        swap = background_model(self.config)
        import help_chat
        try:
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(swap) if swap else None, timeout=self.MEETING_WRITE_SECONDS)
        except help_chat.Unavailable:
            raise OSError from None

    def meeting_write_run(self, event_id):
        """Write one meeting's notes: its transcript in parts when it is long, then the notes, saved by The Machine
        unless notes came in meanwhile. Waits (status waiting, until) while a usage limit holds."""
        stand_in = getattr(self, 'notes_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        run = (lambda prompt: stand_in(self.config, prompt)) if stand_in else self.meeting_write_model
        parts_done = getattr(self, '_meeting_write_parts', None)
        if parts_done is None:
            parts_done = self._meeting_write_parts = {}
        with self.store.connect() as db:
            try:
                meeting, text, minutes = meeting_writer.source(db, event_id)
            except ValueError:  # notes came in, or the transcript or the meeting went: nothing to write
                meeting_writer.finish(db, event_id)
                parts_done.pop(event_id, None)
                return
            pieces = meeting_writer.chunks(text)
            total = len(pieces) + 1 if len(pieces) > 1 else 1
            meeting_writer.mark(db, event_id, now(), status='running', total=total, until=None, error=None)
        lang = locale_prefs.language_of(self.config)
        notes_of = parts_done.setdefault(event_id, [])

        def turn(prompt):
            paused = self.background_pause(owner=True)
            if paused:
                with self.store.connect() as db:
                    meeting_writer.mark(db, event_id, now(), status='waiting', until=float(paused.get('until') or time.time() + 900))
                return None
            try:
                return run(prompt)
            except OSError:
                paused = self.background_pause(owner=True)  # the limit came on during this turn: wait for it
                with self.store.connect() as db:
                    if paused:
                        meeting_writer.mark(db, event_id, now(), status='waiting', until=float(paused.get('until') or time.time() + 900))
                    else:
                        meeting_writer.mark(db, event_id, now(), status='failed', error='model')
                return None

        if len(pieces) > 1:
            for index, piece in enumerate(pieces, 1):
                if index <= len(notes_of):
                    continue
                answer = turn(meeting_writer.part_prompt(meeting, minutes, piece, index, len(pieces), lang))
                if answer is None:
                    return
                notes_of.append(meeting_writer.clean_notes(answer)[:meeting_writer.PART_CHARS * 2])
                with self.store.connect() as db:
                    meeting_writer.mark(db, event_id, now(), done=len(notes_of))
            prompt = meeting_writer.notes_prompt(meeting, minutes, '\n\n'.join(f'### Part {i}\n{n}' for i, n in enumerate(notes_of, 1)), lang, True)
        else:
            prompt = meeting_writer.notes_prompt(meeting, minutes, text, lang)
        answer = turn(prompt)
        if answer is None:
            return
        notes = meeting_writer.clean_notes(answer)
        with self.store.connect() as db:
            if not notes:
                meeting_writer.mark(db, event_id, now(), status='failed', error='empty')
                return
            db.execute('BEGIN IMMEDIATE')
            parts_done.pop(event_id, None)
            if meeting_writer.has_notes(meeting_notes.read(db, event_id, 0, 1)):  # never over notes that came in meanwhile
                meeting_writer.finish(db, event_id)
                LOG.info('meeting notes written but notes came in meanwhile; dropped')
                return
            _, write = meeting_notes.plan(db, event_id, notes, 'machine', now(), field='notes', written_from='transcript')
            if write:
                self.store.save_meeting_notes(db, write)
            meeting_writer.finish(db, event_id)
        LOG.info('meeting notes written parts=%d', len(pieces))
        if getattr(self, 'graph_dirty', None):
            self.graph_dirty.set()

    def meeting_write_resume(self):
        """At the start: notes that were being written go on (from the start of the transcript)."""
        try:
            with self.store.connect() as db:
                left = meeting_writer.resume(db, now())
        except sqlite3.Error as error:
            LOG.warning('meeting notes resume error=%s', type(error).__name__)
            return
        if left:
            self.meeting_write_kick()

    def meeting_notes(self, args, owner_dashboard=False, limit=meeting_notes.READ_CHARS):
        """A meeting's Notes and Transcript (meeting_notes.py). Without event_id: the meetings of a day (day, YYYY-MM-DD,
        today when left out; query narrows them by title), to find the one. With event_id: both, added ones and Zoom's
        (field reads only one, offset reads on). With text: add to field (notes when left out; append:true below what it
        has), or remove:true. Saving never moves text to the other field. The owner adds them on the meeting in the
        Calendar, a Do it run or the owner's chat with its tool; a signal review only reads them, since what it reads
        can't tell it what to write."""
        writes = 'text' in args or args.get('remove') is True
        session = str(args.get('_notes_session') or '')
        if writes and not owner_dashboard and re.match(r'agent:main:assistant-review-(?!preparation-)', session):
            raise ValueError('Reviews read meeting notes; the owner or a Do it run adds them')
        calendars = [a['id'] for a in self.config['accounts'] if a.get('service') in CALENDAR_SERVICES]
        with self.store.connect() as db:
            if args.get('event_id') in (None, ''):
                day = str(args.get('day') or dt.datetime.now(local_tz()).date().isoformat())
                try:
                    dt.date.fromisoformat(day)
                except ValueError:
                    raise ValueError('day is YYYY-MM-DD') from None
                return {'day': day, 'meetings': meeting_notes.meetings_on(db, calendars, day, local_tz(), str(args.get('query') or '')[:200])}
            event = meeting_notes.meeting(db, args.get('event_id'))
            if not event or event['account_id'] not in calendars:
                raise ValueError('No meeting with that event_id. Find it with day (and query) first')
            if not writes:
                try:
                    offset = max(0, int(args.get('offset') or 0))
                except (TypeError, ValueError):
                    raise ValueError('offset is a number') from None
                found = meeting_notes.read(db, event['id'], offset, limit, args.get('field') or None)
                if owner_dashboard and not args.get('field'):  # the Calendar: Generate notes, while it writes (meeting_writer.py)
                    found['writing'] = meeting_writer.view(db, event['id'])
                return found
            field = args.get('field') or 'notes'
            meeting_notes.field_kind(field)
            text = '' if args.get('remove') is True else args.get('text')
            if not isinstance(text, str) or (not text.strip() and args.get('remove') is not True):
                raise ValueError('text is the notes or transcript, as Markdown; remove:true takes them off')
            db.execute('BEGIN IMMEDIATE')
            saved, write = meeting_notes.plan(db, event['id'], text, 'owner' if owner_dashboard else 'machine', now(), args.get('append') is True, field)
            if write:
                saved.update(self.store.save_meeting_notes(db, write))
        if getattr(self, 'graph_dirty', None):
            self.graph_dirty.set()  # the notes show on the timelines of the people in the meeting
        return saved

    def calendar_write(self, args, transport=None):
        """The Calendar form's Add, Save or Delete: the owner filled it in and tapped it, so this one change runs now.
        request_id is the tap: the same id again is that same write (a create keeps its Google event id), never a second.
        guests: who the owner invited; the form listed them above a button that said how many (invite), so a list that
        doesn't match that count is refused, and nobody gets an invite without that tap."""
        request_id = str(args.get('request_id') or '')
        if not re.fullmatch(r'[a-f0-9-]{16,64}', request_id):
            raise ValueError('Invalid request')
        change = {k: v for k, v in args.items() if k in calendar_writes.KEYS - {'kind', 'label'}}
        if args.get('guests'):
            if not isinstance(args['guests'], list) or args.get('invite') != len(args['guests']):
                raise ValueError('Check who gets an invite and tap again. Nothing was sent.')
            change['guests'] = args['guests']
        with self.store.connect() as db:
            done = db.execute('SELECT status,result FROM calendar_writes WHERE id=?', (request_id,)).fetchone()
            if done and done['status'] == 'done':
                return {'status': 'done', 'duplicate': True}
            if done and done['status'] == 'sending':
                raise ValueError('That change is still going through.')
            events = calendar_write_events(db, [change.get('event')], self.owner_emails())
        action = calendar_writes.validate({'kind': 'calendar', **change}, self.config, events, invite=True)
        transport = transport or calendar_writes.CalendarTransport(self.config, credential, gog_read)
        transport.preflight(action)
        stamp = now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT 1 FROM calendar_writes WHERE id=? AND status IN ('sending','done')", (request_id,)).fetchone():
                raise ValueError('That change is still going through.')
            db.execute('INSERT INTO calendar_writes(id,account_id,op,payload,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?) '
                       "ON CONFLICT(id) DO UPDATE SET status='sending',payload=excluded.payload,error=NULL,updated_at=excluded.updated_at",
                       (request_id, action['account_id'], action['op'], hashlib.sha256(encoded(action).encode()).hexdigest(), 'sending', stamp, stamp))
        job = {'id': request_id}
        try:
            result = transport.send(action, job)
        except Exception:  # noqa: BLE001 - unknown outcome: read it back below
            result = {}
        if not result.get('message_id') and not result.get('rejected'):
            try:
                result = transport.reconcile(action, job) or result
            except Exception:  # noqa: BLE001
                pass
        status = 'done' if result.get('message_id') else 'failed' if result.get('rejected') else 'uncertain'
        error = {'done': None, 'failed': f"Google Calendar refused it (error {result.get('rejected')}). Nothing was changed.",
                 'uncertain': 'I couldn’t confirm the change. Check the calendar before you try again.'}[status]
        with self.store.connect() as db:
            db.execute('UPDATE calendar_writes SET status=?,result=?,error=?,updated_at=? WHERE id=?',
                       (status, result.get('message_id'), error, now(), request_id))
        if status == 'done':
            self.sync_soon(action['account_id'])
        return {'status': status, 'error': error, 'op': action['op'], 'calendar': action['calendar_name'], 'invited': len(action.get('guests') or ())}
