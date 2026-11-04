"""A matter of the owner's own life on a work mailbox is Personal (todo_areas.py): family asking about the kids' party
in the owner's work inbox came out Work (2026-11-04). The review's personal (or family_with), or evidence whose people
are all from the owner's own life, puts the to-do in Personal from the start: with a Personal area it gets that area's
accounts, as a move does; with only work accounts it keeps its mailbox and is pinned Personal. Either way its label,
connected AIs, team learnings, handoffs and reviews follow, so it is never offered to a Work Fleet. A move to Work takes
the pin off, and Undo puts it back. Offline: nothing is sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('personal_work_mailbox_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import fleet_requests  # noqa: E402
import knowledge  # noqa: E402
import todo_areas  # noqa: E402

WORK_ONLY = [{'id': 'work-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
             {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'}]
WITH_HOME = WORK_ONLY + [{'id': 'home-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@home.example', 'boundary': 'personal:me'}]


def mail(source_id, sender, subject, thread):
    return {'account_id': 'work-mail', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': '2026-11-02T09:00:00+00:00',
            'title': subject, 'body': 'The venue has no room on December 13. Can you find another one?',
            'metadata': {'from': sender, 'to': 'robin@acme.example', 'thread_id': thread}, 'deleted': False}


class PersonalOnWorkMailbox(unittest.TestCase):
    def open(self, accounts):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = accounts
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': accounts, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        self.store.commit_page('work-mail', {}, [mail('f1', 'Jo <jo@mail.example>', 'Birthday party venue', 't1'),
                                                  mail('c1', 'Sam <sam@client.example>', 'Renewal quote', 't2')])

    def suggest(self, event=1, **extra):
        return self.app.action('suggest', {'dedupe_key': f'mail:{event}', 'title': 'Find another venue for the December 13 birthday party',
                                           'body': 'The venue has no room on December 13.', 'event_ids': [event], **extra})['id']

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def card(self, sid):
        row = self.row(sid)
        with self.store.connect() as db:
            self.store.card_views(db, [row])
        return row

    def test_only_work_accounts_the_family_matter_is_pinned_personal_and_stays_on_its_mailbox(self):
        self.open(WORK_ONLY)
        sid = self.suggest(personal=True)
        row, card = self.row(sid), self.card(sid)
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['work-mail'], 'personal'))
        self.assertEqual((card['scope'], card['area']), ('personal', 'personal'))
        self.assertEqual(a.suggestion_scope(row['account_ids'], WORK_ONLY, row['area']), 'personal')
        self.assertEqual(knowledge.card_area(self.app.config, row['account_ids'], row['area']), 'personal')
        # Never a Work Fleet's: no handoff, no team learnings, a review only from the Family
        stub = type('S', (), {'connect': self.store.connect})()
        with self.assertRaisesRegex(ValueError, 'personal to-do goes only to your Family'):
            fleet_requests.Requests.handoff_draft(stub, sid)
        self.assertEqual(self.app.review_subject(sid)['scope'], 'personal')
        import fleet
        with self.store.connect() as db:
            self.assertEqual(fleet.Fleet.learning_fleet(stub, db, sid)[0], None)
        # A work matter on the same mailbox stays Work
        work = self.suggest(event=2)
        self.assertEqual((self.card(work)['scope'], self.row(work)['area']), ('work', None))
        # The owner moves it to Work: the pin goes; Undo brings it back
        moved = self.app.action('card_move', {'suggestion_id': sid, 'area': 'work:Acme', 'decision_id': 'd-move'}, owner_dashboard=True)
        self.assertEqual(moved['area'], 'work:Acme')
        self.assertEqual((self.card(sid)['scope'], self.row(sid)['area']), ('work', 'work:Acme'))
        self.app.action('card_move', {'suggestion_id': sid, 'undo': 'd-move', 'decision_id': 'd-undo'}, owner_dashboard=True)
        self.assertEqual((self.card(sid)['scope'], self.row(sid)['area']), ('personal', 'personal'))

    def test_family_with_counts_as_personal_and_a_personal_area_gets_its_accounts(self):
        self.open(WITH_HOME)
        sid = self.suggest(family_with='email:jo@mail.example')
        row = self.row(sid)
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['home-mail'], 'personal'))
        self.assertEqual(self.card(sid)['scope'], 'personal')
        self.assertEqual(todo_areas.current(row['account_ids'], WITH_HOME, row['area']), 'personal')

    def test_people_all_from_the_owners_own_life_make_it_personal_without_the_reviews_word(self):
        self.open(WORK_ONLY)
        with self.store.connect() as db:
            for node, info in (('email:jo@mail.example', {'side': 'personal', 'side_why': 'network'}),
                               ('email:sam@client.example', {'side': 'work'})):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,'person',?,1,NULL,1,NULL,0,NULL,?)",
                           (node, node, json.dumps(info)))
            db.executemany('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)',
                           [('email:jo@mail.example', 1, '2026-11-02'), ('email:sam@client.example', 2, '2026-11-02')])
        self.assertEqual(self.card(self.suggest(event=1))['scope'], 'personal')  # Jo is in the owner's Family
        self.assertEqual(self.card(self.suggest(event=2))['scope'], 'work')

    def test_the_review_is_told_when_a_to_do_is_personal(self):
        self.open(WORK_ONLY)
        self.assertIn('gets personal:true on suggest, also when it came in on a work mailbox', a.review_prompt('r1', ['work-mail']))
        self.assertIn('`personal:true`', (ROOT / 'AGENTS.md').read_text())


if __name__ == '__main__':
    unittest.main()
