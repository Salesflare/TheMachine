"""A request's timing, shared by the dashboard's request handler (which starts it and logs a slow request) and
Store.connect (which adds the time spent getting and holding a database connection). Moved out of assistant.py as is."""
import queue
import threading
import time

from machine.config import LOG


# A dashboard or API request that takes longer than this is logged with its path, its total time and the time it spent
# getting a database connection (opening it, waiting on the lock) and holding one: never a query, a body or an answer.
SLOW_REQUEST_SECONDS = 5.0


_REQUEST_TIMING = threading.local()  # this thread's request, while one is answered (Store.connect adds to it)


def close_kept(timing):
    """Close the connections a request kept for its next store.connect (Store._connect): at the end of each request."""
    for kept in (timing or {}).pop('kept', {}).values():
        while kept:
            kept.pop().close()


# Small writes a dashboard read makes on the side (a visit counted, a first view marked). A read never waits for the
# write lock: while a first import takes in page after page, a write queues behind it for seconds, and the page that
# asked would stay blank that long. They go to one thread of their own, in order, and wait there instead.
_ASIDE, _ASIDE_LOCK, _ASIDE_WAITING = queue.SimpleQueue(), threading.Lock(), {}  # {what: how many wait}
_ASIDE_THREAD = None


def answering():
    """Is a dashboard or API request being answered on this thread?"""
    return getattr(_REQUEST_TIMING, 'value', None) is not None


def aside(write, what, once=True):
    """Run write() off the request: on the side thread when a request is being answered on this one, right away
    otherwise (a worker, a test). `what` names it for the log; with `once`, one of a kind waits at a time (the status
    poll asks for the same marks every few seconds). An error is logged there, as the caller can no longer hear it."""
    global _ASIDE_THREAD
    if not answering():
        return write()
    with _ASIDE_LOCK:
        if once and what in _ASIDE_WAITING:
            return None
        _ASIDE_WAITING[what] = _ASIDE_WAITING.get(what, 0) + 1
        if _ASIDE_THREAD is None or not _ASIDE_THREAD.is_alive():
            _ASIDE_THREAD = threading.Thread(target=_aside_run, name='aside-writes', daemon=True)
            _ASIDE_THREAD.start()
    _ASIDE.put((write, what))
    return None


def _aside_run():
    while True:
        write, what = _ASIDE.get()
        try:
            write()
        except Exception as error:  # noqa: BLE001 - a count or a mark: the next ask makes it again
            LOG.warning('write on the side failed what=%s error=%s', what, type(error).__name__)
        finally:
            with _ASIDE_LOCK:
                _ASIDE_WAITING[what] -= 1
                if not _ASIDE_WAITING[what]:
                    del _ASIDE_WAITING[what]


def aside_settled(timeout=10.0):
    """Wait until the writes handed aside so far are made (tests; nothing in the service waits on them)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not _ASIDE_WAITING:
            return True
        time.sleep(0.01)
    return False
