"""A request's timing, shared by the dashboard's request handler (which starts it and logs a slow request) and
Store.connect (which adds the time spent getting and holding a database connection). Moved out of assistant.py as is."""
import threading


# A dashboard or API request that takes longer than this is logged with its path, its total time and the time it spent
# getting a database connection (opening it, waiting on the lock) and holding one: never a query, a body or an answer.
SLOW_REQUEST_SECONDS = 5.0


_REQUEST_TIMING = threading.local()  # this thread's request, while one is answered (Store.connect adds to it)


def close_kept(timing):
    """Close the connections a request kept for its next store.connect (Store._connect): at the end of each request."""
    for kept in (timing or {}).pop('kept', {}).values():
        while kept:
            kept.pop().close()
