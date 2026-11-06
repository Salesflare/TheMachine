"""Rows an importer can't take: each one is skipped and counted by reason, never failing the whole page or poll.

One odd row (a WhatsApp Channel post, a Slack message without a timestamp, a feed item without a date) used to raise
out of the page it was on, so the source failed every poll and nothing after it came in. Now the row is set aside and
counted in the checkpoint and the sync log. Only a page where every one of many rows is refused still fails visibly:
that points at a changed source, not at a few unsupported rows.

Only for turning rows already read into events: a failed read (a network error, an HTTP status) is no odd row and
still raises, so it is retried as before."""
import collections

from sources import SourceError

ALL_REFUSED = 10  # a page of at least this many rows, every one refused: the source changed, so it fails visibly
SKIPPED = object()  # what Skips.take gives for a row it set aside
MALFORMED = (KeyError, TypeError, ValueError, AttributeError, IndexError)  # a field missing or of the wrong type


class Skips(collections.Counter):
    """The rows one page refused, by reason (a SourceError's category). `malformed`: the reason a row counts under when
    converting it fails on a missing field or a wrong type (KeyError, TypeError, ValueError...); None lets those raise."""

    SKIPPED = SKIPPED  # for connectors, which get this class as helpers.Skips

    def __init__(self, malformed=None):
        super().__init__()
        self.malformed, self.taken = malformed, 0

    def take(self, convert, *args):
        """convert(*args), or SKIPPED (counted) when it refuses the row."""
        try:
            result = convert(*args)
        except SourceError as error:
            if error.status or str(error.category).startswith('network:'):
                raise  # a failed read, not an odd row
            self[error.category] += 1
            return SKIPPED
        except MALFORMED:
            if not self.malformed:
                raise
            self[self.malformed] += 1
            return SKIPPED
        self.taken += 1
        return result

    def every(self, rows, convert, *args):
        """[(convert(*args, row), row)] for each row it took, the rest counted."""
        return [(e, row) for row in rows if (e := self.take(convert, *args, row)) is not SKIPPED]

    def check(self):
        """Fails visibly, with the most common reason, when every row of a page of ALL_REFUSED or more was refused."""
        if self and not self.taken and sum(self.values()) >= ALL_REFUSED:
            raise SourceError(self.most_common(1)[0][0])
        return self

    def note(self, state, key='skipped_rows'):
        """Adds this page's counts to the checkpoint's (state[key], by reason, kept across pages); returns the count."""
        if self:
            total = collections.Counter(state.get(key) or {})
            total.update(self)
            state[key] = dict(sorted(total.items()))
        return sum(self.values())
