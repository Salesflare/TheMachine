"""Done checks, the read (machine/store/done_checks.py has the rows): a waiting to-do whose result a public page will show
has that page read when its time to chase comes, before it comes back to the owner. A mixin of assistant.App
(APP_MIXINS), stepped by the preparation worker.

One page per step, at most every EVERY seconds: claimed in one short write, read outside any transaction (one plain
GET as a polite reader, connectors/web_page.read), kept in another short write that holds only for that claim. A read
never sends, drafts or writes anywhere outside the Machine, and needs no model."""
import time

from connectors import web_page
from machine.config import LOG
from machine.store import done_checks
from sources import SourceError
from timeutil import now

EVERY = 30  # seconds between steps


def read_page(url):
    """The page's text lines now: robots.txt asked, public addresses only, MAX_BYTES and TIMEOUT. SourceError when it
    can't be read."""
    status, _, lines = web_page.read(url, {}, SourceError)
    if status != 200 or not lines:
        raise SourceError('web_page_empty')
    return lines


class DoneChecksApp:
    ACTIONS = {}

    def done_check_step(self, read=None):
        if time.monotonic() - self.__dict__.get('done_checked', -EVERY) < EVERY:
            return None
        self.done_checked = time.monotonic()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            jobs = done_checks.claim(db, now())
        if not jobs:
            return None
        job, why, fingerprint = jobs[0], None, None
        try:
            result, fingerprint = done_checks.judge((read or read_page)(job['url']), job['expect'])
        except SourceError as error:
            result, why = 'unknown', error.category
        except Exception as error:  # noqa: BLE001 - any other failure to read is unknown too, never a close
            result, why = 'unknown', type(error).__name__
            LOG.warning('done check read error=%s', why)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            kept = done_checks.settle(db, job, result, now(), why, fingerprint)
        LOG.info('done check result=%s kept=%s', result, kept)
        return kept
