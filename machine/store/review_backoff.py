"""Review runs that came to nothing, for the review worker's gap (App.review_step): runs the runtime called ok that had
signals waiting but never claimed a batch with begin_analysis. A model that can't reach its tools ends each review
with "Done." and nothing else; counted as ok, it started again every minute after a quick first review or while the
first review dug on (about 100k tokens a run)."""


def empty_in_a_row(db, limit=6):
    """How many of the latest finished runs in a row ended ok without claiming anything while signals waited."""
    empty = 0
    for status, planned, claimed in db.execute(
            'SELECT r.status, r.planned, EXISTS(SELECT 1 FROM analyses a WHERE a.owner_run=r.run_id) FROM review_runs r '
            'WHERE r.finished_at IS NOT NULL ORDER BY r.finished_at DESC LIMIT ?', (limit,)):
        if status != 'ok' or claimed or not planned:
            break
        empty += 1
    return empty


def empty_gap(empty, gap, settings):
    """The gap before the next run after that many empty ones: 1, 2, 4… minutes up to 30, never sooner than gap."""
    if not empty:
        return gap
    return max(gap, min(settings.get('retry_seconds', 60) * 2 ** (empty - 1), settings.get('max_retry_seconds', 1800)))
