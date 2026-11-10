"""store.connect for the Fleet tests, but a connection goes back for the next call instead of being closed."""
import contextlib
import sqlite3

import message_seal


def kept_connections(store, cleanup):
    """store.connect for the Fleet, but a connection goes back for the next call instead of being closed. Opening one
    reads the whole schema (some 150 tables), and a Graph round asks for hundreds, which was most of this file's time.
    Each call still has a connection of its own, in a transaction of its own, as with store.connect."""
    free = []

    def close():
        while free:
            free.pop().close()
    cleanup(close)

    @contextlib.contextmanager
    def connect():
        db = free.pop() if free else None
        if db is None:
            db = sqlite3.connect(store.path, timeout=20, factory=message_seal.Connection)
            db.row_factory = sqlite3.Row
            if store.sealer:  # a Machine with message protection on: its rows open themselves, as with store.connect
                message_seal.attach(db, store.sealer)
            db.kept_rows = db.row_factory
        db.row_factory, db.isolation_level, db.protected = db.kept_rows, '', store.protected
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
