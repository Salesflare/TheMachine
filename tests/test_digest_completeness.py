"""The morning digest against what waits, on one fixed fixture: every to-do that is due today, a reply someone waits
for, or one the owner added and that waits on them is named (up to the digest's own limits, the rest counted), nothing
is listed twice, and the named waiting to-dos plus the digest's counts ("N more can wait", "N more ready for your OK.")
add up to the dashboard's own count (waiting_count). The same rules score the nightly agent-users runs
(themachine-cloud tools/agent-users/delivery.py). Fake fixture data only; nothing is sent."""
import datetime as dt
import json
import re
import tempfile
import unittest
from pathlib import Path
from zoneinfo import ZoneInfo

import notify
from seams import patch_everywhere  # noqa: E402
import machine.app.recap as machine_app_recap
from machine.cards import NOT_FOR_OWNER_SQL
from machine.delivery.push import reply_waits, waiting_count
import machine.main as machine_main
from machine import todo_states
import security_levels
import timeutil

UTC = dt.timezone.utc
BXL = ZoneInfo('Europe/Brussels')
MORNING = dt.datetime(2026, 11, 16, 9, 5, tzinfo=BXL)  # a Monday
TODAY = MORNING.date().isoformat()
CARD_LINK = re.compile(r' · \[[^\]\n]+\]\([^)\s]*#card=([a-f0-9]{16})[^)\s]*\)')
ANY_LINK = re.compile(r' · \[[^\]\n]+\]\([^)\s]+\)')
COUNT_LINES = (re.compile(r'(\d+) more ready for your OK\.'), re.compile(r'(\d+) more due today\.'),
               re.compile(r'(\d+) others can wait'), re.compile(r'(\d+) more can wait'), re.compile(r'^(\d+) waiting\b'))
DUE_SHOWN, REPLIES_SHOWN, OWN_SHOWN = 3, 5, 5  # the fewest the digest names of each before it may count the rest


def read_brief(text):
    """The digest's text as {named: [(id or None, line)], counted: N}: its bullet lines (with the to-do's id from its
    Open link) and the sum of the numbers in its count lines. The headline (line one) is not a count line."""
    lines = text.splitlines()
    named, counted = [], 0
    for line in lines[1:]:
        if line.startswith('• '):
            found = CARD_LINK.search(line)
            named.append((found.group(1) if found else None, ANY_LINK.sub('', line[2:]).strip()))
        elif not line.startswith('Open The Machine'):
            counted += sum(int(m.group(1)) for pattern in COUNT_LINES for m in pattern.finditer(line))
    return {'named': named, 'counted': counted}


def check_brief(text, state, show_text=True):
    """What is wrong with a digest's text against the Machine's state, [] when nothing. state: {'count': the dashboard's
    waiting count, 'waiting': [{id, title, origin, reply}], 'due': [{id, title}] (open, due today, not snoozed)}."""
    brief = read_brief(text)
    by_title = {r['title']: r['id'] for r in state['waiting'] + state['due']}
    ids = [i or by_title.get(re.sub(r'^Due today: ', '', line)) for i, line in brief['named']]
    problems = [f'listed twice: {line}' for (i, line), n in zip(brief['named'], ids) if n and ids.count(n) > 1]
    named = set(ids) - {None}
    waiting = {r['id'] for r in state['waiting']}
    said = len(named & waiting) + brief['counted']
    if said != state['count']:
        problems.append(f"counts: the digest accounts for {said} waiting, the dashboard {state['count']}")
    if show_text:
        for what, rows, floor in (('due today', state['due'], DUE_SHOWN),
                                  ('reply waiting', [r for r in state['waiting'] if r['reply']], REPLIES_SHOWN),
                                  ('added by the owner', [r for r in state['waiting'] if r['origin'] == 'owner'], OWN_SHOWN)):
            shown = sum(1 for r in rows if r['id'] in named)
            if shown < min(len(rows), floor):
                problems += [f"not named, {what}: {r['title']}" for r in rows if r['id'] not in named]
    return sorted(set(problems))


class DigestCompleteness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'boundary': 'personal:me'}], 'owner_name': 'Sam Example',
                           'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        timeutil.set_work_hours({'start': '08:00', 'end': '18:00'}); self.addCleanup(timeutil.set_work_hours, None)
        self.seq = 0

    def at(self, hours_ago):
        return (MORNING - dt.timedelta(hours=hours_ago)).astimezone(UTC).isoformat()

    def card(self, title, hours_ago=30, **columns):
        self.seq += 1
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': f'm-{self.seq}', 'kind': 'gmail.message', 'occurred_at': self.at(hours_ago),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        with self.store.connect() as db:
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
        sid = self.store.suggest(f'k-{self.seq}', title, 'Body', [event])['id']
        self.set(sid, deliver_after=None, created_at=self.at(hours_ago), **columns)
        return sid

    def own(self, title, hours_ago=20):
        sid = self.store.owner_card(title, 'home')['id']
        self.set(sid, created_at=self.at(hours_ago))
        return sid

    def set(self, sid, **columns):
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET ' + ','.join(f'{k}=?' for k in columns) + ' WHERE id=?', (*columns.values(), sid))

    def fixture(self, ready=True, older=4):
        """One morning of every kind: replies and other drafts ready for the owner's OK, due today (waiting, and one
        The Machine is still preparing), a snoozed one back later today, the owner's own, overnight, older, and two
        that don't wait on the owner (waiting on someone else, done)."""
        if ready:
            reply = json.dumps({'kind': 'email', 'to': ['client@example.com'], 'subject': 'Re: Quote', 'body': 'Here it is.', 'thread_id': 't-1', 'label': 'Send'})
            self.card('Send the quote to the client', 40, status='prepared', next_action=reply)
            self.card('Approve the new supplier terms', 38, status='prepared')
        self.card('Pay the venue deposit', 50, due=TODAY)
        self.card('Send the board pack', 45, due=TODAY, status='accepted')
        self.card('Call back the landlord', 60, status='snoozed', due=(MORNING.date() - dt.timedelta(days=1)).isoformat(),
                  snoozed_until=(MORNING + dt.timedelta(hours=2)).astimezone(UTC).isoformat())
        self.own('Lower the kitchen step')
        self.own('Get new bike pedals', 30)
        self.card('Reply to the new lead', 5)  # overnight
        for n in range(older):
            self.card(f'Older to-do {n + 1}', 70 + n)
        self.card('Wait for the signed contract', 26, status='prepared', outcome=json.dumps({'state': 'waiting'}))
        self.card('Already handled', 27, status='completed')

    def state(self):
        current = MORNING.astimezone(UTC).isoformat()
        with patch_everywhere(timeutil, 'now', return_value=current), patch_everywhere(timeutil, 'local_tz', return_value=BXL), self.store.connect() as db:
            waiting = [dict(r) for r in db.execute(
                f"SELECT * FROM suggestions WHERE status IN {todo_states.sql(todo_states.WAITING_ON_OWNER)} AND NOT {NOT_FOR_OWNER_SQL} "
                "AND (deliver_after IS NULL OR deliver_after<=?)", (current,))]
            due = [dict(r) for r in db.execute(
                f"SELECT id,title FROM suggestions WHERE status IN {todo_states.sql(todo_states.OPEN_NOT_SNOOZED)} AND due=? AND NOT {NOT_FOR_OWNER_SQL}", (TODAY,))]
            count = waiting_count(db)
        return {'count': count, 'due': due,
                'waiting': [{'id': r['id'], 'title': r['title'], 'origin': r.get('origin'), 'reply': reply_waits(r)} for r in waiting]}

    def digest(self, show_text=True):
        current = MORNING.astimezone(UTC)
        with patch_everywhere(timeutil, 'local_tz', return_value=BXL), patch_everywhere(timeutil, 'now', return_value=current.isoformat()), \
                patch_everywhere(machine_app_recap, 'recap_meetings', return_value=[]), \
                patch_everywhere(security_levels, 'notify_text', return_value=show_text):
            return self.app.digest(current)

    def assertComplete(self, show_text=True):
        digest, state = self.digest(show_text), self.state()
        self.assertTrue(digest)
        self.assertEqual(check_brief(digest['text'], state, show_text), [], digest['text'])
        return digest, state

    def test_ready_headline_names_what_is_due_and_the_owners_own(self):
        self.fixture()
        digest, state = self.assertComplete()
        self.assertTrue(any(r['reply'] for r in state['waiting']))  # the fixture has a reply waiting
        self.assertIn('• Lower the kitchen step', digest['text'])

    def test_due_headline(self):
        self.fixture(ready=False)
        digest, _ = self.assertComplete()
        self.assertIn('due today', digest['subject'])

    def test_a_pile(self):
        self.fixture(ready=False, older=notify.PILE + 2)
        self.assertComplete()

    def test_counts_only_without_titles(self):
        self.fixture()
        digest, _ = self.digest(False), None
        self.assertEqual(check_brief(digest['text'], self.state(), show_text=False), [], digest['text'])

    def test_the_check_catches_the_regressions(self):
        """The rules fail the two digests that went out before the fix: the owner's own to-dos folded into "N more can
        wait", and a snoozed due line taken off that count."""
        state = {'count': 3, 'due': [], 'waiting': [{'id': 'a' * 16, 'title': 'Send the quote', 'origin': None, 'reply': False},
                                                    {'id': 'b' * 16, 'title': 'Lower the kitchen step', 'origin': 'owner', 'reply': False},
                                                    {'id': 'c' * 16, 'title': 'Book the venue', 'origin': None, 'reply': False}]}
        link = lambda i: f' · [Open](https://the-machine.example/assistant/#card={i}&or=chat)'
        folded = f"Good morning, ready for your OK: Send the quote\n\n• Send the quote{link('a' * 16)}\n• Due today: Call back the landlord{link('d' * 16)}\n\n1 more can wait.\n"
        problems = check_brief(folded, state)
        self.assertIn('not named, added by the owner: Lower the kitchen step', problems)
        self.assertIn('counts: the digest accounts for 2 waiting, the dashboard 3', problems)
        twice = f"Good morning\n\n• Send the quote{link('a' * 16)}\n• Send the quote{link('a' * 16)}\n• Lower the kitchen step{link('b' * 16)}\n\n1 more can wait.\n"
        self.assertIn('listed twice: Send the quote', check_brief(twice, state))


if __name__ == '__main__':
    unittest.main()
