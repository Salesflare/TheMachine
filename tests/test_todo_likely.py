"""The review order by how likely a signal brings a to-do (machine/store/todo_likely.py): the quick first look reads the
likeliest first, a regular review reads its claimed batch in that order, and nothing is left out. A fake week of mail
(fixture_week) measures how many signals the first look reads up to the first one that needs a to-do (`measure`; run it
on main and on a change to compare). Fake data only; no Gateway, no model."""
import datetime as dt, importlib.util, random, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('todo_likely_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.store import todo_likely  # noqa: E402

ME = 'me@example.com'


class Runner:
    def __init__(self, *results): self.results = list(results)
    def __call__(self, request): return {'status': self.results.pop(0)}


def fixture_week(seed=0):
    """[(event, needs a to-do)]: a fake owner's week. Most of it newsletters, notifications, their own sent mail and
    mail they were copied on; some people thanking them or passing something on; a few asking something of them, some by
    a date, one in a thread they were in. With `seed`, every signal's time is drawn at random within the week."""
    rng = random.Random(seed)
    out, n = [], 0

    def add(sender, title, body, todo=False, to=ME, labels=(), hours=None, thread=None, reply=False, kind='gmail.message', meta=None):
        nonlocal n
        n += 1
        hours = rng.uniform(1, 160) if seed or hours is None else hours
        when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).isoformat()
        metadata = {'from': sender, 'to': to, 'labels': list(labels), 'thread_id': thread or f't{n}', **(meta or {})}
        if reply:
            metadata['in-reply-to'] = f'<m{n}@example.org>'
        out.append(({'account_id': 'work', 'source_id': f's{n}', 'kind': kind, 'occurred_at': when, 'title': title, 'body': body,
                     'metadata': metadata, 'deleted': False}, todo))

    for i in range(60):
        add(f'Shop {i % 6} <news@shop{i % 6}.example>', f'Weekly deals {i}', 'Save on everything this week.', labels=['CATEGORY_PROMOTIONS'],
            hours=1 + i, meta={'list_unsubscribe': '<mailto:u@shop.example>'})
    for i in range(20):
        add('noreply@service.example', f'Your receipt {i}', 'Thanks for your payment.', labels=['CATEGORY_UPDATES'], hours=2 + i * 3)
    for i in range(15):
        add(f'Me <{ME}>', f'Re: notes {i}', 'Sounds good.', to=f'p{i}@example.org', labels=['SENT'], hours=3 + i * 4)
    for i in range(12):
        add(f'Team {i} <t{i}@example.org>', f'Project update {i}', 'Status as of today, all on track.',
            to=f'a@x.example, b@x.example, c@x.example, {ME}', hours=4 + i * 5)
    add('Lee <lee@example.org>', 'Budget sign-off', 'Hi all, we still need the owner to approve the budget by Friday.',
        todo=True, to=f'a@x.example, b@x.example, c@x.example, {ME}', hours=50)
    for i in range(9):  # people thanking them or passing something on: most of them recent, a few from early in the week
        title = ('Thanks!', 'FYI: slides from today', 'Got it', 'Thank you so much', 'FYI', 'Great, thanks', 'Noted', 'Thanks again', 'Perfect')[i]
        add(f'Friend {i} <f{i}@example.net>', title, 'Thanks, have a good day.', hours=0.5 + i * 0.7 if i < 6 else 120 + i * 5)
    for i in range(4):  # mail that informs and asks nothing
        add(f'Partner {i} <p{i}@example.net>', f'Our new office {i}', 'Just letting you know we moved.', hours=6 + i * 3)
    for i in range(5):  # threads the owner already answered
        add(f'Client {i} <c{i}@example.net>', f'Question {i}', 'Can you send the file?', hours=40 + i * 2, thread=f'answered{i}')
        add(f'Me <{ME}>', f'Re: Question {i}', 'Here it is.', to=f'c{i}@example.net', labels=['SENT'], hours=39 + i * 2, thread=f'answered{i}')
    add('Sam <sam@example.org>', 'Contract', 'Could you review the attached contract and let me know?', todo=True, hours=20)
    add('Kim <kim@example.org>', 'Quick question', 'Are we still on for the demo next week?', todo=True, hours=26)
    add('Ana <ana@example.org>', 'Invoice 2041', 'Please pay the invoice before the 20th.', todo=True, hours=70)
    add('Bo <bo@example.org>', 'Re: Proposal', 'Thanks for the call. Can you send the revised proposal by tomorrow?',
        todo=True, hours=12, thread='bo', reply=True)
    add(f'Me <{ME}>', 'Proposal', 'As discussed, here is the proposal.', to='bo@example.org', labels=['SENT'], hours=30, thread='bo')
    for i in range(6):
        when = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=10 + i * 20)).isoformat()
        out.append(({'account_id': 'work', 'source_id': f'event{i}', 'kind': 'calendar.event', 'occurred_at': when, 'title': f'Sync {i}',
                     'body': 'Weekly sync', 'metadata': {}, 'deleted': False}, False))
    return out


class Week:
    """A fresh install with the fixture week in it, its first look claimed."""

    def __init__(self, seed=0):
        self.temp = tempfile.TemporaryDirectory()
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'gateway', 'service': 'gateway'}, {'id': 'work', 'service': 'gmail'}],
                           'review_worker': {'enabled': False}, 'delivery_enabled': False}
        week = fixture_week(seed)
        self.todo = {e['source_id'] for e, todo in week if todo}
        self.store.commit_page('work', {}, [e for e, _ in week])

    def first_look_order(self):
        """The source ids the whole first look reads, in order: the quick look's batch, then each next batch."""
        with patch_everywhere(a, 'has_model', return_value=True), patch.object(a.Store, 'accounts', [{'id': 'work', 'service': 'gmail', 'email': ME}]):
            self.app.review_step(Runner('admitted'))
            with self.store.connect() as db:
                run = db.execute('SELECT run_id FROM review_runs').fetchone()[0]
                names = {i: s for i, s in db.execute('SELECT id,source_id FROM events')}
            order = []
            while True:
                claim = self.store.begin_analysis(['work'], a.QUICK_LOOK_SIGNALS if not order else 40, a.REVIEW_SESSION_PREFIX + run, run)
                if not claim.get('analysis_id'):
                    return [names[i] for i in order]
                ids = [e['id'] for e in claim['events']]
                order += ids
                with self.store.connect() as db:
                    db.execute('UPDATE events SET analyzed_version=version WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)
                    db.execute("UPDATE analyses SET status='complete',finished_at=? WHERE id=?", (a.now(), claim['analysis_id']))
                    db.execute("UPDATE review_runs SET budget=100000 WHERE run_id=?", (run,))

    def close(self):
        self.temp.cleanup()


def measure(seed=0):
    """(signals read up to and with the first that needs a to-do, to-dos in the quick look, all read, to-dos, distinct read)."""
    week = Week(seed)
    try:
        order = week.first_look_order()
        first = next(i for i, s in enumerate(order, 1) if s in week.todo)
        in_quick = sum(s in week.todo for s in order[:a.QUICK_LOOK_SIGNALS])
        return first, in_quick, len(order), len(week.todo), len(set(order))
    finally:
        week.close()


class TodoLikely(unittest.TestCase):
    def test_the_first_look_reads_who_asks_something_first_and_still_reads_everything(self):
        # Before, the newest "Thanks!" and FYI mails and the longest-waiting thank-you came first (2026-11-13: the first
        # to-do's signal 10th on this week)
        first, in_quick, read, todos, distinct = measure(0)
        self.assertEqual(first, 1)  # the first signal it reads needs a to-do
        self.assertEqual(in_quick, todos)  # every one that needs a to-do is in the quick look
        self.assertEqual((read, distinct), (len(fixture_week(0)), read))  # all of it, each once

    def test_at_random_times_the_first_to_do_comes_from_the_top(self):
        for seed in (1, 2, 3):
            first, in_quick, read, todos, distinct = measure(seed)
            self.assertLessEqual(first, 3)
            self.assertGreaterEqual(in_quick, todos - 1)
            self.assertEqual(read, distinct)

    def test_words_read_the_top_of_a_reply_not_what_it_quotes(self):
        quoted = {'title': 'Re: lunch', 'body': 'Sounds good.\n\nOn Mon, Sam wrote:\n> Can you send it by Friday?'}
        self.assertEqual(todo_likely.words(quoted), {'question': False, 'ask': False, 'dated': False, 'courtesy': False})
        asked = {'title': 'Contract', 'body': 'Could you sign it before Friday?'}
        self.assertEqual(todo_likely.words(asked), {'question': True, 'ask': True, 'dated': True, 'courtesy': False})
        self.assertTrue(todo_likely.words({'title': 'Thanks!', 'body': 'Thank you'})['courtesy'])

    def test_a_regular_review_reads_its_batch_likeliest_first_and_claims_the_same_signals(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        store = a.Store(Path(temp.name) / 'events.sqlite')
        when = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)).isoformat()
        mail = lambda sid, sender, title, body, labels=(): {'account_id': 'work', 'source_id': sid, 'kind': 'gmail.message', 'occurred_at': when,
                                                            'title': title, 'body': body, 'deleted': False,
                                                            'metadata': {'from': sender, 'to': ME, 'labels': list(labels), 'thread_id': sid}}
        store.commit_page('work', {}, [mail('news', 'Shop <news@shop.example>', 'Deals', 'Sale', ['CATEGORY_PROMOTIONS']),
                                       mail('thanks', 'Ann <ann@example.org>', 'Thanks!', 'Thank you'),
                                       mail('ask', 'Sam <sam@example.org>', 'Contract', 'Could you sign it by Friday?')])
        with patch.object(a.Store, 'accounts', [{'id': 'work', 'service': 'gmail', 'email': ME}]):
            claim = store.begin_analysis(['work'], 40)
        with store.connect() as db:
            names = {i: s for i, s in db.execute('SELECT id,source_id FROM events')}
        self.assertEqual([names[e['id']] for e in claim['events']], ['ask', 'thanks', 'news'])


if __name__ == '__main__':
    unittest.main()
