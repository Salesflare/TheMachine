"""Times what setup, Connected and reviews read, before and after a year of history (synthetic rows, a temp DB).

Run: python3 tests/history_measure.py . 50000. The reads of signals should stay flat; only search grows."""
import importlib.util, sys, tempfile, time, json, datetime as dt
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'tests'))
spec = importlib.util.spec_from_file_location('a', ROOT / 'assistant.py'); a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import graph
N = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
acct = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}
def ev(i, at, hist):
    return {'account_id': 'work', 'source_id': f'{"h" if hist else "s"}{i}', 'kind': 'gmail.message', 'occurred_at': at,
            'title': f'Subject {i}', 'body': 'Some body text about numbers and plans ' * 20,
            'metadata': {'from': f'p{i % 500}@example.org', 'to': 'owner@example.com', 'thread_id': f't{i}', 'labels': ['INBOX'], 'in-reply-to': 'x'}, 'deleted': False}
def timed(label, f, n=5):
    t = time.perf_counter()
    for _ in range(n): f()
    print(f'{label}: {(time.perf_counter() - t) / n * 1000:.1f} ms')
with tempfile.TemporaryDirectory() as d:
    s = a.Store(Path(d) / 'events.sqlite')
    now = dt.datetime.now(dt.timezone.utc)
    s.commit_page('work', {}, [ev(i, (now - dt.timedelta(hours=i)).isoformat(), False) for i in range(1500)])
    def measure(tag):
        print('--', tag)
        timed('Connected snapshot', lambda: s.snapshot([acct]))
        timed('pending (review batch)', lambda: s.events(['work'], pending=True, limit=120))
        with s.connect() as db:
            timed('graph signals', lambda: graph._signals(db, (now - dt.timedelta(days=400)).isoformat()))
            timed('owner_wrote_in', lambda: a.Store.owner_wrote_in(db, 'work', {'in-reply-to': 'x', 'thread_id': 't5'}), 20)
        timed('search', lambda: s.events(['work'], query='numbers plans', limit=40))
    measure('signals only (1,500)')
    t = time.perf_counter()
    for start in range(0, N, 500):
        s.commit_page('work', None, [ev(i, (now - dt.timedelta(days=8, minutes=10 * i)).isoformat(), True) for i in range(start, min(N, start + 500))], record_sync=False, history=True)
    print(f'kept {N} history rows in {time.perf_counter() - t:.1f} s; db {(Path(d) / "events.sqlite").stat().st_size / 1e6:.0f} MB')
    measure(f'with {N:,} history rows')
