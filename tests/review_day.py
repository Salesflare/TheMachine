"""A day of signals for a test persona, replayed through the real review worker (App.review_step) on a fake clock,
for tests/test_review_batch.py and `python3 tests/review_day.py` (prints before/after).

DAY is how many signals of each class came in per hour on a busy owner's Machine (a Saturday in 2026-11, its local
hours): counts only. Every signal made from it is invented: example.com senders, made-up subjects. The classes:
chat (WhatsApp from people), own (mail the owner sent), person (mail from someone they know), unknown (Primary mail
from someone new: every other one is a list mail, the rest a person writing for the first time), auto (no-reply and
category mail: notifications, receipts, every fourth a VAT receipt with a deadline), phone (phone notifications:
every fourth from WhatsApp, the rest other apps), system (payment events) and calendar (calendar changes).

A review claims everything waiting when it starts and takes RUN_MINUTES. Tokens per review are the fixed start plus
a share per signal, fitted on that Machine's 241 signal reviews of 2026-11-03..08 (fresh: uncached input)."""
import datetime as dt
import importlib.util
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seams import patch_everywhere  # noqa: E402

CLASSES = ('chat', 'own', 'person', 'unknown', 'auto', 'phone', 'system', 'calendar')
DAY = [  # local hour: signals per class, in CLASSES order
    (4, 0, 0, 1, 1, 2, 0, 0), (1, 0, 0, 1, 1, 1, 0, 0), (1, 0, 1, 0, 0, 3, 0, 0), (0, 0, 0, 1, 0, 1, 1, 0),
    (2, 0, 0, 0, 1, 1, 0, 0), (3, 0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 4, 0, 0), (0, 0, 0, 3, 5, 6, 0, 0),
    (0, 0, 1, 2, 2, 5, 0, 1), (17, 1, 1, 4, 0, 5, 0, 1), (4, 0, 0, 1, 2, 5, 0, 0), (47, 3, 28, 7, 13, 4, 0, 0),
    (8, 0, 5, 4, 3, 2, 0, 0), (5, 2, 1, 1, 1, 3, 0, 0), (7, 0, 5, 3, 1, 6, 0, 0), (4, 0, 0, 0, 1, 5, 0, 0),
    (4, 0, 0, 0, 1, 7, 0, 1), (4, 0, 0, 0, 0, 6, 0, 0), (0, 0, 2, 1, 1, 9, 0, 1), (0, 0, 0, 1, 0, 4, 0, 0),
    (4, 3, 1, 5, 0, 8, 0, 2), (18, 3, 0, 0, 2, 16, 0, 0), (6, 1, 3, 0, 0, 20, 0, 5), (0, 0, 0, 1, 1, 16, 2, 0)]
START = dt.datetime(2026, 11, 7, 0, 0, tzinfo=dt.timezone.utc)
RUN_MINUTES = 5
FIXED = {'fresh': 71829, 'all': 514136}  # tokens per review, its start
PER_SIGNAL = {'fresh': 2667, 'all': 17206}  # and per signal it reviews


def load():
    spec = importlib.util.spec_from_file_location('review_day_assistant', Path(__file__).resolve().parent.parent / 'assistant.py')
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    return a


def signal(cls, n, at):
    """One invented signal of a class: (account, event, person?). person: from a person, so its review must not wait."""
    sid = f'{cls}-{n}'
    base = {'source_id': sid, 'occurred_at': at.isoformat(), 'deleted': False}
    mail = lambda **m: ('mail', {**base, 'kind': 'gmail.message', 'body': 'Text', **m})
    if cls == 'chat':
        return ('chat', {**base, 'kind': 'whatsapp.message', 'title': 'Sam', 'body': 'Can you send it over?',
                         'metadata': {'chat_id': f'3247000{n % 9}@s.whatsapp.net', 'from': 'Sam', 'from_me': False}}), True
    if cls == 'own':
        return mail(title='Re: plan', metadata={'from': 'Owner <owner@example.com>', 'to': 'sam@example.org', 'labels': ['SENT'], 'thread_id': sid}), True
    if cls == 'person':
        return mail(title='Quick question', metadata={'from': f'Alex Doe <alex{n % 5}@example.org>', 'to': 'owner@example.com',
                                                      'labels': ['INBOX'], 'thread_id': sid}), True
    if cls == 'unknown' and n % 2:
        return mail(title='Hello from a new partner', metadata={'from': f'Robin Roe <robin{n}@example.net>', 'to': 'owner@example.com',
                                                                'labels': ['INBOX'], 'thread_id': sid}), True
    if cls == 'unknown':
        return mail(title='Weekly digest', metadata={'from': 'Digest <weekly@news.example.com>', 'to': 'owner@example.com', 'labels': ['INBOX'],
                                                     'list_unsubscribe': True, 'thread_id': sid}), False
    if cls == 'auto':
        vat = n % 4 == 0
        return mail(title='VAT receipt: pay within 14 days' if vat else 'Your order has shipped',
                    metadata={'from': 'Billing <billing@shop.example.com>' if vat else 'Shop <no-reply@shop.example.com>', 'to': 'owner@example.com',
                              'labels': ['INBOX', 'CATEGORY_UPDATES'], 'thread_id': sid}), False
    if cls == 'phone':
        app = 'com.whatsapp' if n % 4 == 0 else 'com.example.weather'
        return ('phone', {**base, 'kind': 'android.notification', 'title': 'Sam' if app == 'com.whatsapp' else 'Rain at 4 pm', 'body': '',
                          'metadata': {'package_name': app, 'notification_key_hash': sid}}), app == 'com.whatsapp'
    if cls == 'system':
        return ('pay', {**base, 'kind': 'stripe.event', 'title': 'Payment succeeded', 'body': '', 'metadata': {'type': 'charge.succeeded'}}), False
    return ('cal', {**base, 'kind': 'calendar.event', 'title': 'Call with Sam', 'body': '', 'metadata': {'organizer': {'email': 'sam@example.org'}}}), True


def day_signals():
    """[(at, account, event, person)] of the whole day, spread evenly over each hour, in order."""
    found = []
    for hour, counts in enumerate(DAY):
        for cls, count in zip(CLASSES, counts):
            for i in range(count):
                at = START + dt.timedelta(hours=hour, minutes=(i + 0.5) * 60 / count, seconds=CLASSES.index(cls))
                (account, event), person = signal(cls, len(found), at)
                found.append((at, account, event, person))
    return sorted(found, key=lambda s: s[0])


def replay(a, batch_wait_minutes=None, step_minutes=1):
    """The day through App.review_step. {'reviews', 'signals', 'waits': {source_id: (person, minutes)}, 'tokens': {...}}."""
    temp = tempfile.TemporaryDirectory()
    try:
        store = a.Store(Path(temp.name) / 'events.sqlite')
        app = object.__new__(a.App)
        app.store = store
        app.quick_first_review = lambda db: 0
        settings = {'enabled': True, 'min_signals': 40, 'max_wait_minutes': 15, 'gap_seconds': 600, 'timeout_seconds': 1500}
        if batch_wait_minutes is not None:
            settings['batch_wait_minutes'] = batch_wait_minutes
        app.config = {'accounts': [{'id': x} for x in ('chat', 'mail', 'phone', 'pay', 'cal')], 'review_worker': settings}
        signals, ingested, waits, runs = day_signals(), {}, {}, []
        clock = {'at': START}

        def runner(request):
            at = clock['at']
            if request['action'] == 'start':
                job = request['job_id']
                session = a.REVIEW_SESSION_PREFIX + job
                claim = store.begin_analysis([x['id'] for x in app.config['accounts']], 120, session, job)
                with store.connect() as db:
                    row = db.execute('SELECT items FROM analyses WHERE id=?', (claim.get('analysis_id'),)).fetchone()
                    items = [i['id'] for i in a.json.loads(row['items'])] if row else []
                    ids = dict(db.execute('SELECT id,source_id FROM events WHERE id IN (%s)' % ','.join('?' * len(items)), items).fetchall()) if items else {}
                for event_id in items:
                    sid = ids[event_id]
                    waits[sid] = (ingested[sid][1], (at - ingested[sid][0]).total_seconds() / 60)
                if claim.get('analysis_id'):
                    store.finish_analysis(claim['analysis_id'], 'Reviewed', session, job)
                runs.append({'job': job, 'at': at, 'signals': len(items)})
                return {'status': 'admitted'}
            started = next(r['at'] for r in runs if r['job'] == request['job_id'])
            return {'status': 'ok' if at - started >= dt.timedelta(minutes=RUN_MINUTES) else 'pending'}

        end, i = START + dt.timedelta(hours=24), 0
        while clock['at'] < end + dt.timedelta(hours=2):
            with patch_everywhere(a, 'now', return_value=clock['at'].isoformat()):
                while i < len(signals) and signals[i][0] <= clock['at']:
                    at, account, event, person = signals[i]
                    store.commit_page(account, {}, [{**event, 'account_id': account}])
                    ingested[event['source_id']] = (clock['at'], person)
                    i += 1
                app.review_step(runner)
            clock['at'] += dt.timedelta(minutes=step_minutes)
        day = [r for r in runs if r['at'] < end]
        tokens = {k: sum(FIXED[k] + PER_SIGNAL[k] * r['signals'] for r in day) for k in FIXED}
        return {'reviews': len(day), 'signals': len(signals), 'waits': waits, 'tokens': tokens, 'runs': runs}
    finally:
        temp.cleanup()


def summary(result):
    person = sorted(m for p, m in result['waits'].values() if p)
    batch = sorted(m for p, m in result['waits'].values() if not p)
    pct = lambda xs, q: round(xs[min(len(xs) - 1, int(q * len(xs)))], 1) if xs else None
    return {'reviews': result['reviews'], 'signals per review': round(result['signals'] / max(result['reviews'], 1), 1),
            'fresh tokens': result['tokens']['fresh'], 'all tokens': result['tokens']['all'],
            'person wait p50/p95/max min': (pct(person, .5), pct(person, .95), pct(person, 1)),
            'batch wait p50/p95/max min': (pct(batch, .5), pct(batch, .95), pct(batch, 1)), 'unreviewed': result['signals'] - len(result['waits'])}


if __name__ == '__main__':
    a = load()
    before, after = replay(a, batch_wait_minutes=0), replay(a)
    for name, r in (('before', before), ('after', after)):
        print(name, summary(r))
    later = [(sid, b[1], after['waits'][sid][1]) for sid, b in before['waits'].items() if b[0] and after['waits'][sid][1] > b[1] + 0.01]
    print('person signals reviewed later than before:', len(later), 'of', sum(1 for p, _ in before['waits'].values() if p),
          '; most later by', round(max((x[2] - x[1] for x in later), default=0), 1), 'min, longest wait', round(max((x[2] for x in later), default=0), 1), 'min')
