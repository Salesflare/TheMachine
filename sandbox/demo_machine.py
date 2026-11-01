"""A demo Machine: the sandbox's made-up day (fixture.json, the busy state) loaded into a real, freshly installed
Machine, for the app directories' review account (the control plane's cloud/reviewer.py). Run on that Machine as its
owner, with the installed app on the path:

    python3 sandbox/demo_machine.py --config ~/.config/the-machine/config.json [--app /path/to/installed/app]

What it loads: the fixture's signals, to-dos, promises, boards, reviews and the Graph built from them, into the
Machine's own database through the app's Store, so message contents are sealed as on any Machine.

What it never adds: the fixture's mail, chat and calendar accounts. The config is not touched: nothing syncs, and no
account exists to send from. Signals keep their made-up account ids only as labels. No saved logins, no Fleet, no
friends. It refuses a database that already has signals, so it never mixes with real data."""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import load  # noqa: E402

STATES = {'busy'}


def fill(config, fixture, base=None):
    """Loads the fixture into config['database']; returns how many signals, to-dos and promises it added."""
    import assistant
    import graph

    if config.get('accounts'):
        raise SystemExit('This Machine has accounts connected: a demo Machine starts with none.')
    store = assistant.Store(config['database'])
    base = base or dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    with store.connect() as db:
        if db.execute('SELECT 1 FROM events LIMIT 1').fetchone():
            raise SystemExit('This Machine already has signals: a demo Machine starts empty.')
        ids = {}
        for e in fixture['events']:
            meta = load.calendar_meta(e['metadata'], base) if e['kind'] == 'calendar.event' else e['metadata']
            at = meta['start']['dateTime'] if e['kind'] == 'calendar.event' else load.stamp(e['minutes_ago'], base)
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                       'VALUES(?,?,?,?,?,?,?,0,?,1,1,?)',
                       (e['account_id'], 'sandbox:' + e['key'], e['kind'], at, e['title'], e['body'], json.dumps(meta),
                        hashlib.sha256((e['title'] + e['body']).encode()).hexdigest(), load.stamp(max(e['minutes_ago'], 0) - 1, base)))
            ids[e['key']] = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        load.load_cards(db, fixture, ids, base)
        load.load_reviews(db, ids, base, assistant)
        load.load_boards(db, fixture, ids, base)
    with store.connect() as db:
        load.load_job(db, fixture, base)
        db.commit()  # graph.build opens its own transaction
        # The Graph is built as if the made-up accounts were there (which side each person is on); they are not saved
        graph.build(db, {**config, 'accounts': fixture['accounts']}, base.isoformat())
        load.load_roles(db, base)
        load.load_fields(db, base)
        load.load_skills(db, STATES, fixture, base)
        counts = [db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ('events', 'suggestions', 'promises')]
    return dict(zip(('signals', 'todos', 'promises'), counts))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--config', required=True)
    parser.add_argument('--app', default=str(HERE.parent), help='the installed app (default: this checkout)')
    parser.add_argument('--fixture', default=str(HERE / 'fixture.json'))
    args = parser.parse_args(argv)
    sys.path.insert(0, args.app)
    config = json.loads(Path(args.config).expanduser().read_text())
    print(json.dumps(fill(config, json.loads(Path(args.fixture).read_text()))))


if __name__ == '__main__':
    main()
