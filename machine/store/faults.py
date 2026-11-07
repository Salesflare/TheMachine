"""The Store's faults (refactor, Store leftovers): The Machine's own errors counted per day and version, the error
reports' signatures (error_feed.py), which faults are worth a signal, and closing a to-do about an error that stopped.
Moved out of assistant.Store as is. A mixin of assistant.Store."""
import datetime as dt
import json

import error_feed
from machine.faults import FAULT_STEPS
from timeutil import now


class FaultsStore:
    """Store methods for The Machine's own errors."""

    def record_fault(self, fingerprint, kind, frames, location, version, message=None, origin=None):
        stamp = now()
        with self.connect() as db:
            db.execute('INSERT INTO faults(fingerprint,day,kind,frames,location,version,first_at,last_at,count,message,origin) VALUES(?,?,?,?,?,?,?,?,1,?,?) '
                       'ON CONFLICT(fingerprint,day) DO UPDATE SET count=count+1,last_at=excluded.last_at,frames=excluded.frames,version=excluded.version,'
                       'message=coalesce(excluded.message,message),origin=excluded.origin',
                       (fingerprint, stamp[:10], kind, json.dumps(frames), location, version, stamp, stamp, message,
                        json.dumps(origin) if origin else None))
            if version:
                db.execute('INSERT INTO fault_versions VALUES(?,?,?,?,?,?,1) ON CONFLICT(fingerprint,version,day) '
                           'DO UPDATE SET last_at=excluded.last_at,count=count+1', (fingerprint,version,stamp[:10],kind,stamp,stamp))
            db.execute('DELETE FROM faults WHERE day<?', ((dt.datetime.fromisoformat(stamp) - dt.timedelta(days=30)).date().isoformat(),))
            db.execute('DELETE FROM fault_versions WHERE day<?', ((dt.datetime.fromisoformat(stamp) - dt.timedelta(days=30)).date().isoformat(),))

    def record_error(self, source, kind, message, file, function, line=None):
        """Count an error for the error reports (error_feed.py): a signature only. Never raises."""
        try:
            with self.connect() as db:
                return error_feed.record(db, source, kind, message, file, function, line, self.code_version)
        except Exception:
            return None  # recording an error must never cause one

    def unreported_faults(self):
        """Faults worth a (new) signal: the first one of a day, then again at 3, 10, 30, 100… occurrences."""
        with self.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM faults WHERE count>reported ORDER BY last_at')]
        return [r for r in rows if not r['reported'] or any(r['reported'] < step <= r['count'] for step in FAULT_STEPS)]

    def faults_reported(self, rows):
        with self.connect() as db:
            for row in rows:
                db.execute('UPDATE faults SET reported=? WHERE fingerprint=? AND day=?', (row['count'], row['fingerprint'], row['day']))

    def settle_faults(self, version, quiet=dt.timedelta(days=1)):
        """A card about The Machine's own error that nobody acted on closes itself once the error stopped: not
        seen for a day, and the code running now never recorded it (an update fixed it). Returns the closed ids."""
        if not version:
            return []
        stamp = now()
        cutoff = (dt.datetime.fromisoformat(stamp) - quiet).isoformat()
        closed = []
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for row in db.execute("SELECT s.id,s.event_ids FROM suggestions s WHERE s.status='pending' AND EXISTS(SELECT 1 FROM json_each(s.event_ids) i "
                                  "JOIN events e ON e.id=i.value WHERE e.kind='machine.fault')").fetchall():
                events = db.execute('SELECT e.kind,e.metadata FROM json_each(?) i JOIN events e ON e.id=i.value', (row['event_ids'],)).fetchall()
                prints = {json.loads(e['metadata']).get('fingerprint') if e['kind'] == 'machine.fault' else None for e in events}
                if not prints or None in prints:
                    continue  # it is about more than the error
                if any(db.execute('SELECT 1 FROM faults WHERE fingerprint=? AND last_at>=?', (fp, cutoff)).fetchone()
                       or db.execute('SELECT 1 FROM fault_versions WHERE fingerprint=? AND version=?', (fp, version)).fetchone() for fp in prints):
                    continue
                db.execute("UPDATE suggestions SET status='completed',completed_from='pending',early=0 WHERE id=?", (row['id'],))
                db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           ('fault-stopped:' + row['id'], row['id'], 'complete', 'The error stopped after an update: not seen for a day.', 'assistant', stamp))
                db.execute("UPDATE deliveries SET status='cancelled',reminder=0,updated_at=? WHERE suggestion_id=? AND message_id IS NULL", (stamp, row['id']))
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))
                closed.append(row['id'])
        return closed
