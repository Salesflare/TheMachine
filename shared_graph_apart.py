"""The Shared Graph's reads for a publish (shared_graph.collect), in a process of their own. Collecting reads every
shared thread, about half a gigabyte on a big mailbox, and ran in the server's own process: for its ten seconds and
more every round, each page request waited its turn for Python and took two to ten times as long. Here a child process
reads the same database (its own read-only connection, the same message key), runs the same collect, and hands the
result back; the server only waits on the pipe, which leaves Python to the requests.

Nothing changes in what is published: the same code reads the same rows. Where a child can't run (the sandbox refuses
programs, an install without its interpreter, a child that fails), collect runs in this process as before.

The request and the answer cross the pipe as pickles of plain values only (dicts, lists, tuples, sets, text, numbers):
_Plain refuses any class, so a pickle can't make an object or run code."""
from __future__ import annotations

import io
import logging
import os
import pickle
import sqlite3
import subprocess
import sys

LOG = logging.getLogger('personal-assistant')
TIMEOUT = 900  # seconds: a child that takes longer is stopped, and this round collects in-process as before


class _Plain(pickle.Unpickler):
    def find_class(self, module, name):
        raise pickle.UnpicklingError(f'not a plain value: {module}.{name}')


def _loads(data):
    return _Plain(io.BytesIO(data)).load()


def _dumps(value):
    return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)


def _state():
    """What collect reads besides the database and its arguments: the clock (a pinned one too), the time zone and
    the owner's language and locale."""
    import locale_prefs
    import timeutil
    return {'pinned': timeutil.PINNED.isoformat() if timeutil.PINNED else None, 'tz': timeutil.LOCAL_TZ.key,
            'locale': dict(locale_prefs._current)}


def _set_state(state):
    import locale_prefs
    import timeutil
    timeutil.pin(state['pinned'])
    timeutil.set_timezone(state['tz'])
    locale_prefs._current.update(state['locale'])


def run(store, scope_args, keys, secret, kept, grants):
    """[(records, threads, stats, files, held)] for the Fleet's scope and then each grant's (scope.granted(*grant)),
    collected in a child process; None when that can't be done (the caller collects in-process instead).
    store: the Store whose database it reads; scope_args: Scope's after db (accounts, internal, mine, personal)."""
    path, key = getattr(store, 'path', None), getattr(store, '_seal_key', None)
    if path is None or (getattr(store, 'sealer', None) and not key):
        return None
    request = _dumps({'path': str(path), 'key': key, 'protected': bool(getattr(store, 'protected', False)),
                      'scope': [sorted(a) if isinstance(a, (set, frozenset)) else a for a in scope_args], 'keys': list(keys),
                      'secret': secret, 'kept': set(kept), 'grants': [list(map(sorted, g)) for g in grants], 'state': _state()})
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        child = subprocess.Popen([sys.executable, os.path.join(here, 'shared_graph_apart.py')], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=here)
    except (OSError, ValueError, RuntimeError, PermissionError) as error:  # the sandbox's guard, or no interpreter
        LOG.info('shared graph collect in-process reason=%s', type(error).__name__)
        return None
    try:
        out, err = child.communicate(request, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        child.kill()
        child.communicate()
        LOG.warning('shared graph collect in-process reason=timeout')
        return None
    if child.returncode != 0:
        # the error's type only (the last line's start): never anything it read
        LOG.warning('shared graph collect in-process reason=child_exit code=%s error=%s', child.returncode,
                    (err or b'').decode('utf-8', 'replace').strip().rsplit('\n', 1)[-1].split(':', 1)[0][:80])
        return None
    try:
        return _loads(out)
    except (pickle.UnpicklingError, EOFError, ValueError, TypeError) as error:
        LOG.warning('shared graph collect in-process reason=%s', type(error).__name__)
        return None


def _connect(path, key, protected):
    import message_seal
    db = sqlite3.connect(path, timeout=20, factory=message_seal.Connection)
    db.row_factory = sqlite3.Row
    db.protected = protected
    if key:
        message_seal.attach(db, message_seal.Sealer(key))
    db.execute('PRAGMA query_only=ON')  # this process only reads
    return db


def collect(db, request):
    """The child's work: the same collect calls graph_publish makes, in one read transaction."""
    import shared_graph
    scope = shared_graph.Scope(db, *request['scope'])
    out = []
    for grant in [None, *request['grants']]:
        held = set()
        records, threads, stats, files = shared_graph.collect(db, scope if grant is None else scope.granted(*grant), request['keys'],
                                                              request['secret'], held=held if grant is None else None,
                                                              kept=request['kept'])
        out.append((records, threads, stats, files, held))
    return out


def main():
    request = _loads(sys.stdin.buffer.read())
    _set_state(request['state'])
    db = _connect(request['path'], request['key'], request['protected'])
    try:
        with db:
            db.execute('BEGIN')  # one snapshot for all of it, as the server's one connection had
            found = collect(db, request)
    finally:
        db.close()
    sys.stdout.buffer.write(_dumps(found))
    sys.stdout.buffer.flush()


if __name__ == '__main__':
    main()
