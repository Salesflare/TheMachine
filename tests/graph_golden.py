"""The Graph built from the sandbox at a fixed moment, as rows: what tests/test_graph_golden.py compares with
tests/graph_golden.json, so a change to how the Graph is built (graph.py) shows every row it changes.

    python3 tests/graph_golden.py OUT        write the rows of every graph_* table to OUT
    python3 tests/graph_golden.py --write    store them as the snapshot, after a change meant to change the Graph

The scenario: the sandbox's all state (sandbox/load.py), loaded at BASE; its signals older than HISTORY_DAYS turned
into history and all of it taken in (machine/store/graph_history.py); a rebuild with the owner's Fleets (team, kin),
as the Graph worker runs it. Nothing in it reads the clock: the same rows on every run, machine and time zone."""
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / 'tests' / 'graph_golden.json'
BASE = dt.datetime(2026, 3, 10, 9, 30, tzinfo=dt.timezone.utc)
HISTORY_DAYS = 21
CLOCK = {'graph_state': ('took_ms',)}  # columns that measure the run itself: left out


def rows(db):
    """{table: sorted rows} of every graph_* table."""
    out = {}
    for table in [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'graph%' ORDER BY name")]:
        columns = [r[1] for r in db.execute(f'PRAGMA table_info({table})') if r[1] not in CLOCK.get(table, ())]
        found = [list(r) for r in db.execute(f"SELECT {','.join(columns)} FROM {table}")]
        out[table] = {'columns': columns, 'rows': sorted(found, key=lambda r: json.dumps(r))}
    return out


def text(tables):
    """One line a row, so a diff names the rows that changed."""
    parts = []
    for table, t in tables.items():
        lines = ',\n'.join('    ' + json.dumps(r, ensure_ascii=False) for r in t['rows'])
        parts.append(f'  {json.dumps(table)}: {{"columns": {json.dumps(t["columns"])}, "rows": [\n{lines}\n  ]}}')
    return '{\n' + ',\n'.join(parts) + '\n}\n'


def build():
    sys.path.insert(0, str(ROOT / 'sandbox'))
    import load
    with tempfile.TemporaryDirectory() as folder:
        config, _ = load.load(folder, load.parse_states('all'), base=BASE)  # imports assistant with HOME in the folder
        import assistant
        import graph
        from machine.store import graph_history
        fixture = json.loads((ROOT / 'sandbox' / 'fixture.json').read_text())
        network = fixture['network']
        kin = {}
        for group in ('work', 'family'):
            for member in network[group]['team']:
                kin.setdefault(member['email'], set()).add(group)
        now = BASE.isoformat()
        horizon = (BASE - dt.timedelta(days=graph.HORIZON_DAYS)).isoformat()
        with assistant.Store(config['database']).connect() as db:
            db.execute('UPDATE events SET history=1 WHERE occurred_at<?', ((BASE - dt.timedelta(days=HISTORY_DAYS)).isoformat(),))
            while graph_history.advance(db, horizon, now):
                pass
        with assistant.Store(config['database']).connect() as db:
            db.commit()  # graph.build opens its own transaction
            graph.build(db, config, now, set(kin), kin, history=True)
            return rows(db)


if __name__ == '__main__':
    built = text(build())
    if sys.argv[1:] == ['--write']:
        SNAPSHOT.write_text(built)
    elif len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(built)
    else:
        raise SystemExit(__doc__)
