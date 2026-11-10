"""Milestones on done to-dos: a small celebration on To-dos when the Done count passes a round number (LEVELS), with
an image to share (dashboard/todos-milestone.js, drawn on the device). The count is the Done list's own (done_counts
'all'), so the number celebrated is the one the owner sees there.

Only the latest level passed shows, once: a Machine already past several gets that one, not a backlog. Closing it
(or sharing) marks it seen on the Machine (the `done_milestone` milestone), so it never shows again on another device,
and a lower level never shows after a higher one was seen."""
import json

from timeutil import now

# Round numbers that feel worth a moment: often at first (a new owner's first 10 and 50 come within days), then further
# apart as the habit sets in (a busy owner passes 100s every few weeks), so it stays a treat and never a chore.
LEVELS = (10, 50, 100, 250, 500, 1000, 2500, 5000, 10000)

MARK = 'done_milestone'  # milestones: at = when the latest one was closed, detail = {"seen": level}


def reached(count):
    """The highest level count has passed, or 0."""
    return max((level for level in LEVELS if level <= int(count or 0)), default=0)


def seen(db):
    """The highest level closed so far, or 0."""
    row = db.execute('SELECT detail FROM milestones WHERE name=?', (MARK,)).fetchone()
    try:
        return int(json.loads(row[0] or '{}').get('seen') or 0) if row else 0
    except (ValueError, TypeError, AttributeError):
        return 0


def view(db, count):
    """{'count': level} for the dashboard's status while the latest level passed is not seen yet, else None."""
    level = reached(count)
    return {'count': level} if level and level > seen(db) else None


def mark_seen(db, level, count):
    """The celebration for level was closed: it and every lower level count as seen. Only a level that was reached."""
    try:
        level = int(level)
    except (TypeError, ValueError):
        return False
    if level not in LEVELS or level > reached(count) or level <= seen(db):
        return False
    db.execute('INSERT OR REPLACE INTO milestones(name,at,detail) VALUES(?,?,?)', (MARK, now(), json.dumps({'seen': level})))
    return True


class DoneMilestonesStore:
    """Store methods for the milestone celebration on To-dos."""

    def done_milestone(self, count):
        with self.connect() as db:
            return view(db, count)

    def done_milestone_seen(self, level):
        with self.connect() as db:
            count = self.done_counts(db)['all']
            mark_seen(db, level, count)
            return {'done_milestone': view(db, count)}
