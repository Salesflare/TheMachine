"""A graph build's publish (graph._build_in): the tables it makes, written as the changes from what is there.

A build used to empty graph_nodes, graph_links, graph_events, graph_unnamed and graph_same and write every row again,
under the write lock: seconds on a busy Machine, and every request that writes (Done, a sync, a merge) waited that long.
Most rows are the same from one build to the next, so only the rows that are new, changed or gone are written now;
what the tables hold afterwards is the same as before."""

# table: (how many lead columns are the key, its SELECT, DELETE and INSERT), written out: no SQL is put together
TABLES = {
    'graph_same': (2, 'SELECT a,b,why,score FROM graph_same',
                     'DELETE FROM graph_same WHERE a=? AND b=?',
                     'INSERT OR REPLACE INTO graph_same(a,b,why,score) VALUES(?,?,?,?)'),
    'graph_nodes': (1, 'SELECT id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info FROM graph_nodes',
                      'DELETE FROM graph_nodes WHERE id=?',
                      'INSERT OR REPLACE INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,?,?,?,?,?,?,?,?,?)'),
    'graph_links': (2, 'SELECT a,b,kind,strength,last_at FROM graph_links',
                      'DELETE FROM graph_links WHERE a=? AND b=?',
                      'INSERT OR REPLACE INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,?,?,?)'),
    'graph_events': (2, 'SELECT node_id,event_id,at,probable,direct FROM graph_events',
                       'DELETE FROM graph_events WHERE node_id=? AND event_id=?',
                       'INSERT OR REPLACE INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,?,?)'),
    'graph_unnamed': (1, 'SELECT key,event_ids,people,titles,size,last_at FROM graph_unnamed',
                        'DELETE FROM graph_unnamed WHERE key=?',
                        'INSERT OR REPLACE INTO graph_unnamed(key,event_ids,people,titles,size,last_at) VALUES(?,?,?,?,?,?)'),
}


# A row already there is changed in place: an UPDATE, which leaves its triggers the old row to compare with (an INSERT OR
# REPLACE is a new row to them). stamps.GRAPH_WHO counts a node only when who it is changed, not its strength or profile.
UPDATES = {
    'graph_nodes': 'UPDATE graph_nodes SET kind=?,name=?,strength=?,last_at=?,signals=?,gap_days=?,quiet=?,trend=?,info=? WHERE id=?',
}


def _events(rows):
    """graph_events rows as the old INSERT ... ON CONFLICT left them: the first row's time, a confirmed label over a
    probable one (min probable), direct when any row is (max direct)."""
    out = {}
    for row in rows:
        key = (row[0], int(row[1]))
        was = out.get(key)
        out[key] = (key[0], key[1], row[2], int(row[3]), int(row[4])) if was is None else \
            (*key, was[2], min(was[3], int(row[3])), max(was[4], int(row[4])))
    return out


def _same(value):
    """A value as SQLite gives it back: a bool is an integer there."""
    return int(value) if isinstance(value, bool) else value


def replace(db, table, rows):
    """Make `table` hold exactly `rows` (INSERT OR REPLACE order: a later row with the same key wins), writing only
    the difference. Returns how many rows were written or deleted."""
    keyed, select, delete, insert = TABLES[table]
    if table == 'graph_events':
        new = _events(rows)
    else:
        new = {}
        for row in rows:
            row = tuple(_same(v) for v in row)
            new[row[:keyed]] = row
    have = {tuple(r[:keyed]): tuple(r) for r in db.execute(select)}
    gone = [key for key in have if key not in new]
    db.executemany(delete, gone)
    changed = [row for key, row in new.items() if have.get(key) != row]
    update = UPDATES.get(table)
    if update:
        db.executemany(update, [(*row[keyed:], *row[:keyed]) for row in changed if row[:keyed] in have])
        db.executemany(insert, [row for row in changed if row[:keyed] not in have])
    else:
        db.executemany(insert, changed)
    return len(gone) + len(changed)


def publish(db, same_rows, nodes, links, event_rows, unnamed_rows):
    """The build's tables, as the changes from what they hold (in the build's write transaction)."""
    return sum(replace(db, table, rows) for table, rows in (('graph_same', same_rows), ('graph_nodes', nodes), ('graph_links', links),
                                                            ('graph_events', event_rows), ('graph_unnamed', unnamed_rows)))
