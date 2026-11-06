"""After an import: nothing goes out by itself, and nothing old comes back as new (docs/moving.md).

An import copies the databases as they were at the export, sends that were waiting included. Before the service starts
on the new computer, hold() makes each of them wait for the owner:
- a send that was queued (an email, a message, a calendar change, a doc edit) is blocked with a line that says why, so its to-do
  shows Send again; one that was going out at that moment is uncertain and never resent;
- the Telegram chats' own outbox stops the same way;
- an agent job that ran or waited on the old computer ends with its work kept in its folder (Try again carries on);
- automated follow-ups are paused on every board that has them, until the owner resumes them;
- phone notifications still waiting are dropped (they were for the old Machine), and so are AI connector tokens and
  phone sign-ups when the keys stayed behind.

And the history line: moved_in records the export's moment. A source read again after the move (a new Google sign-in,
WhatsApp linked again) brings in what happened before that moment as history (machine/store/history.py), never as a
signal, so no review, first look or to-do picks up an old message again."""
import sqlite3

from machine.store import history

MOVED_SEND = 'Not sent: The Machine moved to this computer. Check it and send it again.'
MOVED_UNSURE = 'The Machine moved while this was going out. I won’t resend it.'
MOVED_JOB = 'Stopped by the move to this computer. Its work is still in its folder: try again to carry on.'


def _has(db, table):
    return bool(db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone())


def hold(db, at, since, keys=False, source=None):
    """Hold the pending work of an imported main database. `at`: now; `since`: the export's moment. Returns
    {what: count} of what it held. Run once, with the service stopped, before it starts on the imported data."""
    import activity_log, agent_jobs, ai_access, follow_ups, notify  # noqa: E401  (their own tables, written by them)
    db.row_factory = db.row_factory or sqlite3.Row  # follow_ups reads rows by name
    held = {}
    history.record_move(db, at, since, source)
    if _has(db, 'action_jobs'):
        # action_jobs, deliveries and push_subscriptions belong to assistant.py's Store, which is at its line budget and
        # isn't open while an import runs with the service stopped: tests/test_architecture.py OTHER_WRITERS
        queued = [r[0] for r in db.execute("SELECT id FROM action_jobs WHERE status IN ('queued','local_preparation')")]
        for job in queued:
            db.execute("UPDATE action_jobs SET status='blocked',error=?,retry_at=NULL,updated_at=? WHERE id=?", (MOVED_SEND, at, job))
            activity_log.note_block(db, job, MOVED_SEND, at)
        held['sends'] = len(queued)
        held['sends_unsure'] = db.execute("UPDATE action_jobs SET status='uncertain',error=?,retry_at=NULL,updated_at=? "
                                          "WHERE status IN ('sending','undoing')", (MOVED_UNSURE, at)).rowcount
        if queued and _has(db, 'deliveries'):
            db.executemany('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id IN (SELECT suggestion_id FROM action_jobs WHERE id=?)',
                           [(job,) for job in queued])
    if _has(db, 'agent_jobs'):
        held['agent_jobs'] = agent_jobs.stop_for_move(db, MOVED_JOB, at)
    if _has(db, 'follow_up_rules') and _has(db, 'follow_up_pauses') and _has(db, 'boards'):
        boards = 0
        for (ref,) in db.execute("SELECT ref FROM follow_up_rules WHERE scope='board'").fetchall():
            try:
                if not follow_ups.current_pause(db, 'board', ref, at):
                    follow_ups.pause(db, 'board', ref, None, at)
                    boards += 1
            except ValueError:  # off there, or the board is gone
                pass
        held['follow_up_boards'] = boards
    if _has(db, 'notify_queue'):
        held['notifications'] = notify.drop_all(db)
    if not keys:
        held['ai_tokens'] = ai_access.forget_all(db)
        if _has(db, 'push_subscriptions'):
            held['push_subscriptions'] = db.execute('DELETE FROM push_subscriptions').rowcount
    return {k: v for k, v in held.items() if v}


def hold_telegram(db, at):
    """The Telegram chats store's outbox (telegram_store.py): what waited to go out stops, with the same line."""
    import telegram_store
    return telegram_store.hold_outbox(db, MOVED_SEND, at) if _has(db, 'outbox') else 0
