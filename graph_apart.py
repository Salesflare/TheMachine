"""The graph worker's rebuild (graph.build), in a process of its own. A build takes ten to thirty seconds on a big
mailbox, every half hour and after edits, and ran in the server's own process: all that time each page request
waited its turn for Python, and an api/status that takes a tenth of a second took several. Here a child process opens
the same database (its own connection, the same message key), runs the same build, and hands its summary back; the
server only waits on the pipe, which leaves Python to the requests.

Nothing changes in what is built: the same code reads and writes the same rows, in the same transactions, and a build
that meets an edit is Outdated here as there. Where a child can't run (the sandbox refuses programs, an install
without its interpreter, a child that fails), the caller builds in-process as before.

Both ways across the pipe are pickles of plain values only (shared_graph_apart._Plain refuses any class)."""
from __future__ import annotations

import logging
import os
import pickle
import sqlite3
import subprocess
import sys

from shared_graph_apart import _dumps, _loads, _set_state, _state

LOG = logging.getLogger('personal-assistant')
TIMEOUT = 1800  # seconds: a child that takes longer is stopped (its transaction ends with it), and this build runs in-process


def run(store, config, now, team, kin, history, lock_last):
    """graph.build's summary from a child process; raises graph.Outdated where the build would; None when no child
    could build (the caller builds in-process instead)."""
    import graph
    path, key = getattr(store, 'path', None), getattr(store, '_seal_key', None)
    if path is None or (getattr(store, 'sealer', None) and not key):
        return None
    try:
        request = _dumps({'path': str(path), 'key': key, 'protected': bool(getattr(store, 'protected', False)), 'config': config,
                          'now': now, 'team': set(team or ()), 'kin': kin, 'history': history, 'lock_last': lock_last, 'state': _state()})
    except (pickle.PicklingError, TypeError, RuntimeError, AttributeError) as error:  # a setting changing meanwhile
        LOG.info('graph build in-process reason=%s', type(error).__name__)
        return None
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        child = subprocess.Popen([sys.executable, os.path.join(here, 'graph_apart.py')], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=here)
    except (OSError, ValueError, RuntimeError, PermissionError) as error:  # the sandbox's guard, or no interpreter
        LOG.info('graph build in-process reason=%s', type(error).__name__)
        return None
    try:
        out, err = child.communicate(request, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        child.kill()
        child.communicate()
        LOG.warning('graph build in-process reason=timeout')
        return None
    if child.returncode != 0:
        # the error's type only (the last line's start): never anything it read
        LOG.warning('graph build in-process reason=child_exit code=%s error=%s', child.returncode,
                    (err or b'').decode('utf-8', 'replace').strip().rsplit('\n', 1)[-1].split(':', 1)[0][:80])
        return None
    try:
        found = _loads(out)
    except (pickle.UnpicklingError, EOFError, ValueError, TypeError) as error:
        LOG.warning('graph build in-process reason=%s', type(error).__name__)
        return None
    if found.get('outdated'):
        raise graph.Outdated()
    return found.get('built')


def _connect(path, key, protected):
    """A connection as Store.connect makes one (machine/store/core.py), for writing."""
    import message_seal
    db = sqlite3.connect(path, timeout=20, factory=message_seal.Connection)
    db.row_factory = sqlite3.Row
    db.protected = protected
    if key:
        message_seal.attach(db, message_seal.Sealer(key))
        db.execute('PRAGMA secure_delete=ON')
    db.execute('PRAGMA foreign_keys=ON')
    db.isolation_level = None  # graph.build runs its own transaction
    return db


def build(db, request):
    """The child's work: the same build the graph worker runs. {'built': summary} or {'outdated': True}."""
    import graph
    try:
        return {'built': graph.build(db, request['config'], request['now'], request['team'], request['kin'],
                                     history=request['history'], lock_last=request['lock_last'])}
    except graph.Outdated:
        return {'outdated': True}


def main():
    request = _loads(sys.stdin.buffer.read())
    _set_state(request['state'])
    db = _connect(request['path'], request['key'], request['protected'])
    try:
        found = build(db, request)
    finally:
        db.close()
    sys.stdout.buffer.write(_dumps(found))
    sys.stdout.buffer.flush()


if __name__ == '__main__':
    main()
