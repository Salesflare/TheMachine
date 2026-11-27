"""Catch-all projects eval (project_spread.py): replays each made-up case as a review that labels every message of the
day into the case's project, the way reviews built the catch-alls (by topic, whoever it is with). Before: the plain
label (graph.label). After: through project_spread.label, the path finish_analysis takes. No model, nothing sent.

    python3 evals/project-catchalls/run.py               # this checkout
    python3 evals/project-catchalls/run.py --root <dir>  # another checkout (its project_spread, when it has one)
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent


def replay(case, owner_email, after):
    import graph
    import machine.main as machine_main
    import project_spread
    base = dt.datetime(2026, 9, 1, 9, tzinfo=dt.timezone.utc)
    with tempfile.TemporaryDirectory() as folder:
        store = machine_main.Store(Path(folder) / 'events.sqlite', protect=True)
        store.accounts = [{'id': 'work', 'service': 'gmail', 'email': owner_email}]
        refused, spent = 0, 0.0
        with store.connect() as db:
            graph.ensure(db)
        for day in sorted({m['day'] for m in case['messages']}):
            page = []
            for i, m in enumerate(x for x in case['messages'] if x['day'] == day):
                meta = {'from': m['from'], 'to': ', '.join(m['to']), 'thread_id': m['thread'], 'labels': ['SENT'] if m.get('sent') else ['INBOX']}
                if m.get('cc'):
                    meta['cc'] = ', '.join(m['cc'])
                page.append({'account_id': 'work', 'source_id': f"{m['thread']}-{day}-{i}", 'kind': 'gmail.message', 'title': m['title'], 'body': '',
                             'occurred_at': (base + dt.timedelta(days=day, minutes=i)).isoformat(), 'deleted': False, 'metadata': meta})
            store.commit_page('work', {}, page)  # through the Store, sealed as a connector's (tests/test_message_seal.py)
            with store.connect() as db:
                owner = graph.Owner({'accounts': store.accounts}, db)
                ids = [db.execute("SELECT id FROM events WHERE account_id='work' AND source_id=?", (e['source_id'],)).fetchone()[0] for e in page]
                start = time.perf_counter()
                if after:
                    refused += project_spread.label(db, {case['project']: ids}, owner, (base + dt.timedelta(days=day)).isoformat()).get(case['project'], 0)
                else:
                    graph.label(db, ids, case['project'], 'review', (base + dt.timedelta(days=day)).isoformat())
                spent += time.perf_counter() - start
        with store.connect() as db:
            pid = db.execute('SELECT id FROM projects WHERE name=?', (case['project'],)).fetchone()[0]
            found, _ = project_spread.shape(db, pid, owner)
            # a thread is on the project when any of its messages is (graph.build spreads a label over its thread)
            on = {r[0] for r in db.execute("SELECT DISTINCT json_extract(e.metadata,'$.thread_id') FROM events e JOIN event_projects ep ON ep.event_id=e.id "
                                           'WHERE ep.project_id=?', (pid,))}
            answered = {m['thread'] for m in case['messages'] if not m.get('sent')}
            off = {m['thread'] for m in case['messages']} - on
            return {'groups': len(found.groups), 'one_way': found.one_way, 'flagged': found.catch_all(), 'refused': refused,
                    'answered_threads_off': len(off & answered), 'unanswered_threads_off': len(off - answered),
                    'labeled': db.execute('SELECT count(*) FROM event_projects WHERE project_id=?', (pid,)).fetchone()[0],
                    'ms': round(spent * 1000, 1)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(HERE.parent.parent))
    args = parser.parse_args()
    sys.path.insert(0, args.root)
    data = json.loads((HERE / 'cases.json').read_text())
    rows, totals = [], {'before': {}, 'after': {}}
    for case in data['cases']:
        for mode in ('before', 'after'):
            got = replay(case, data['owner'], mode == 'after')
            rows.append({'case': case['id'], 'kind': case['kind'], 'mode': mode, **got})
            t = totals[mode]
            if case['kind'] == 'catch-all':
                t['catch-alls formed'] = t.get('catch-alls formed', 0) + (got['groups'] >= project_spread_some(args.root))
                t['separate counterparts absorbed'] = t.get('separate counterparts absorbed', 0) + got['groups']
                t['flagged for a split'] = t.get('flagged for a split', 0) + got['flagged']
            else:
                wrong = got['answered_threads_off'] > 0 or got['flagged']
                t['genuine projects wrongly split'] = t.get('genuine projects wrongly split', 0) + wrong
                t['genuine conversations kept off'] = t.get('genuine conversations kept off', 0) + got['answered_threads_off']
                t['genuine unanswered messages kept off'] = t.get('genuine unanswered messages kept off', 0) + got['unanswered_threads_off']
            t['ms'] = round(t.get('ms', 0) + got['ms'], 1)
    for r in rows:
        print(json.dumps(r))
    print(json.dumps(totals, indent=1))


def project_spread_some(root):
    sys.path.insert(0, root)
    import project_spread
    return project_spread.SOME


if __name__ == '__main__':
    main()
