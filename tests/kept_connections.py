"""store.connect for the Fleet tests, but a connection goes back for the next call instead of being closed."""
import contextlib
import sqlite3

import message_seal


def kept_connections(store, cleanup):
    """store.connect for the Fleet, but a connection goes back for the next call instead of being closed. Opening one
    reads the whole schema (some 150 tables), and a Graph round asks for hundreds, which was most of this file's time.
    Each call still has a connection of its own, in a transaction of its own, as with store.connect."""
    assert store.sealer is None  # store.connect attaches the sealer; these Machines have none
    free = []

    def close():
        while free:
            free.pop().close()
    cleanup(close)

    @contextlib.contextmanager
    def connect():
        db = free.pop() if free else sqlite3.connect(store.path, timeout=20, factory=message_seal.Connection)
        db.row_factory, db.isolation_level, db.protected = sqlite3.Row, '', store.protected
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            if db.in_transaction:
                db.rollback()
            free.append(db)
    connect.close = close
    return connect
