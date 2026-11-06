"""Meeting writes in the service (meeting_writer.py writes them): the queue a meeting note or a calendar change waits in,
its worker and one run with the model (meeting_write_run), resumed after a restart. Moved out of assistant.App as is. A
mixin of assistant.App (APP_MIXINS)."""
import logging
import sqlite3
import threading
import time

import i18n
import locale_prefs
import meeting_notes
import meeting_writer
from models import background_model, has_model
from sources import CALENDAR_SERVICES
from timeutil import now

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
