"""The missed-work audit (missed_work.py) as a command, next to the knowledge eval (knowledge_eval.py): read-only against a
copy of a real install's database, or the evaluator alone on the made-up signals.

    python3 tests/missed_work_eval.py --calibrate                      the evaluator on every made-up signal (CASES):
                                                                       its precision and recall (weekly, with --llm of
                                                                       knowledge_eval.py; needs the Gateway's model)
    python3 tests/missed_work_eval.py --db X --config Y [--days 7]     one audit over a database, opened read-only:
                                      [--sample 40] [--key-from Z]     counts, rates and patterns, never a message

Nothing is written to the database and nothing is sent anywhere but the model turn. --out keeps the verdicts (event
ids, kinds of work, short reasons) in a local file for the owner to check."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--db', help='the database to audit, opened read-only')
    parser.add_argument('--key-from', help='a database path whose message-content.key opens it (default: next to --db)')
    parser.add_argument('--config', help="that install's config.json (its accounts and areas)")
    parser.add_argument('--days', type=int)
    parser.add_argument('--sample', type=int)
    parser.add_argument('--model', help="provider/model for the evaluator (default: the Gateway's)")
    parser.add_argument('--seed')
    parser.add_argument('--calibrate', action='store_true', help="only the made-up signals: the evaluator's precision and recall")
    parser.add_argument('--out', help='write the verdicts to this local JSON file')
    args = parser.parse_args(argv)
    sys.path.insert(0, str(ROOT))
    import missed_work as mw
    config = json.loads(Path(args.config).read_text()) if args.config else {}
    ask = lambda prompt: mw.model_run(config, prompt, args.model)
    if args.calibrate:
        prompt, ids = mw.page({}, mw.CASES, args.seed or 'calibrate')
        verdicts = mw.parse(ask(prompt), ids)
        pairs = [(mw.CASES_BY_ID[ref][7], verdicts[sid]['work']) for sid, (_, ref) in ids.items() if sid in verdicts]
        result = mw.accuracy(pairs)
        print(f"Made-up signals judged: {result['n']} of {len(mw.CASES)}; precision {result['precision']}, recall {result['recall']}")
        wrong = [ref for sid, (_, ref) in ids.items() if sid in verdicts and verdicts[sid]['work'] != mw.CASES_BY_ID[ref][7]]
        print('Wrong on: ' + (', '.join(sorted(wrong)) or 'none'))
        return 0
    if not args.db:
        parser.error('--db or --calibrate')
    spec = importlib.util.spec_from_file_location('missed_eval_assistant', ROOT / 'assistant.py')
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    import own_addresses
    db = mw.open_readonly(args.db, args.key_from)
    try:
        own = frozenset(own_addresses.yours(db, config)) | {str(x.get('email') or '').lower() for x in config.get('accounts') or () if '@' in str(x.get('email') or '')}
    except Exception:  # noqa: BLE001 - the addresses help, they are not needed
        own = frozenset()
    found = mw.run(db, config.get('accounts') or [], ask, args.days or mw.DAYS, args.sample or mw.SAMPLE, args.seed, own,
                   cases=len(mw.CASES), owned=a.calendar_owned, bulk=a.bulk_kind)
    print('\n'.join(mw.report(found, mw.calibration_of(found))))
    if args.out and not found.get('error'):
        Path(args.out).write_text(json.dumps({'sampled': found['sampled'], 'calibration': found['calibration'],
                                              'strata': {f'{k[0]}|{k[1]}': v for k, v in found['strata'].items()}}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
