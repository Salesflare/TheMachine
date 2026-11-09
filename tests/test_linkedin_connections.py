"""LinkedIn connections onto the Graph's people (linkedin_connections.py): titles and companies from the Connections
list, matched by profile link or by name and company, a line when someone moves on, and a slow pace. Made-up people,
no live calls."""
import datetime as dt
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_ux as ux
import crm
import enrichment
import graph
import linkedin_connections as lc

a = ux.a
ACCOUNT = {'id': 'li', 'service': 'linkedin', 'transport': 'linkedin-inbox', 'boundary': 'work'}
NOW = '2026-11-09T10:00:00+00:00'  # 11:00 in Amsterdam: waking hours


def conn(name, headline, slug=None, member=None):
    return {'name': name, 'headline': headline, 'slug': slug or '', 'member': member or '', 'connected_at': 1790000000000}


class Reader:
    """Pages of made-up connections; `fail` raises that SourceError code instead."""
    def __init__(self, pages, fail=None):
        self.pages, self.fail, self.calls = pages, fail, []

    def __call__(self, start, count):
        self.calls.append(start)
        if self.fail:
            raise a.SourceError(self.fail)
        page = self.pages[start // count] if start // count < len(self.pages) else []
        return {'connections': page, 'more': start // count + 1 < len(self.pages)}


class LinkedInConnections(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'a.sqlite')
        a.set_timezone('Europe/Amsterdam')
        with self.store.connect() as db:
            graph.ensure(db)
            crm.ensure(db)
            db.execute("INSERT INTO milestones(name,at) VALUES('first_import:li',?)", (NOW,))
            db.execute("INSERT INTO checkpoints(account_id,state,last_success) VALUES('li','{}',?)", (NOW,))
            self.org(db, 'org:globex.example', 'Globex')
            self.person(db, 'email:ada@globex.example', 'Ada Quill', org='org:globex.example')
            self.person(db, 'email:bo@acme.example', 'Bo Tamsin', profile={'linkedin_url': 'https://www.linkedin.com/in/bo-tamsin/'})
            self.person(db, 'li:urn:li:msg_conversation:(urn:li:fsd_profile:ME,2-X==)', 'Cy Marlowe',
                        profile={'linkedin_url': 'https://www.linkedin.com/in/ACoAAcy123'})
            self.person(db, 'email:dee@one.example', 'Dee Varga', profile={'company': 'Initech'})
            self.person(db, 'email:dee@two.example', 'Dee Varga', profile={'company': 'Initech'})

    def org(self, db, node, name):
        db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'org',?,1,1,'{}')", (node, name))

    def person(self, db, node, name, org=None, profile=None):
        info = {'identifiers': [node], 'org': org, 'profile': profile or {}}
        db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,1,?)", (node, name, json.dumps(info)))

    def facts(self, node):
        with self.store.connect() as db:
            return {f: v[0] for f, v in (enrichment.people_facts(db, None, [node]).get(node) or {}).items()}

    def changes(self, node):
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM graph_nodes WHERE id=?', (node,)).fetchone()
            return crm.changes(db, row)

    def step(self, read, at=NOW, account=ACCOUNT):
        return lc.step(self.store.connect, {}, account, read, at)

    def later(self, minutes, at=NOW):
        return (dt.datetime.fromisoformat(at) + dt.timedelta(minutes=minutes)).isoformat()

    def test_a_headline_gives_a_title_and_company_only_when_it_says_so(self):
        self.assertEqual(lc.job('Head of Sales at Acme | Helping teams grow'), ('Head of Sales', 'Acme'))
        self.assertEqual(lc.job('CTO @ Globex'), ('CTO', 'Globex'))
        self.assertEqual(lc.job('Accountmanager bij Initech'), ('Accountmanager', 'Initech'))
        self.assertEqual(lc.job('Engineer at Acme, ex-Globex'), ('Engineer', 'Acme'))
        for vague in ('Founder, Acme', 'Helping SaaS teams grow', '', None, 'at Acme'):
            self.assertEqual(lc.job(vague), (None, None), vague)

    def test_matches_by_profile_link_then_name_and_company_and_never_makes_people(self):
        read = Reader([[conn('Bo Tamsin', 'VP Sales at Acme', slug='bo-tamsin'),
                        conn('Cy M.', 'Designer at Hooli', slug='cy-marlowe', member='ACoAAcy123'),
                        conn('Ada Quill', 'Product Lead at Globex', slug='ada-q'),
                        conn('Dee Varga', 'Analyst at Initech', slug='dee-v'),  # two Dee Vargas at Initech: neither
                        conn('Eli Stranger', 'CEO at Nowhere', slug='eli-s')]])
        with self.store.connect() as db:
            nodes = db.execute('SELECT count(*) FROM graph_nodes').fetchone()[0]
        found = self.step(read)
        self.assertEqual((found['seen'], found['matched'], found['done']), (5, 3, True))
        self.assertEqual(self.facts('email:bo@acme.example')['title'], 'VP Sales')
        self.assertEqual(self.facts('email:bo@acme.example')['company'], 'Acme')
        cy = self.facts('li:urn:li:msg_conversation:(urn:li:fsd_profile:ME,2-X==)')  # by member id, as messages link it
        self.assertEqual((cy['title'], cy['linkedin_url']), ('Designer', 'https://www.linkedin.com/in/cy-marlowe/'))
        self.assertEqual(self.facts('email:ada@globex.example')['title'], 'Product Lead')  # name and company
        self.assertEqual(self.facts('email:dee@one.example'), {})
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM graph_nodes').fetchone()[0], nodes)
            kept = {r[0] for r in db.execute('SELECT DISTINCT identifier FROM person_facts')}
            seen = {r[0] for r in db.execute("SELECT DISTINCT source FROM person_facts")}
            at = {r[0] for r in db.execute('SELECT DISTINCT seen_at FROM person_facts')}
        self.assertFalse(any('eli' in i or 'dee' in i for i in kept))
        self.assertEqual((seen, at), ({'linkedin'}, {NOW}))  # where it came from and when LinkedIn last showed it

    def test_a_name_alone_is_not_enough(self):
        self.step(Reader([[conn('Ada Quill', 'Helping teams grow', slug='ada-q'), conn('Ada Quill', 'Engineer at Hooli', slug='ada-q2')]]))
        self.assertEqual(self.facts('email:ada@globex.example'), {})

    def test_a_new_title_is_a_dated_line_on_their_page_once(self):
        bo = 'email:bo@acme.example'
        self.step(Reader([[conn('Bo Tamsin', 'Sales Lead at Acme', slug='bo-tamsin')]]))
        self.assertEqual(self.changes(bo), [])  # first seen, nothing known before: no change
        week = self.later(8 * 24 * 60)
        self.step(Reader([[conn('Bo Tamsin', 'Head of Sales at Acme', slug='bo-tamsin')]]), at=week)
        lines = self.changes(bo)
        self.assertEqual(len(lines), 1)
        self.assertEqual((lines[0]['field'], lines[0]['at']), ('job', week))
        self.assertEqual(lines[0]['old'], {'title': 'Sales Lead', 'company': 'Acme'})
        self.assertEqual(lines[0]['new'], {'title': 'Head of Sales', 'company': 'Acme', 'via': 'LinkedIn'})
        self.assertEqual(self.facts(bo)['title'], 'Head of Sales')
        self.step(Reader([[conn('Bo Tamsin', 'Head of Sales at Acme', slug='bo-tamsin')]]), at=self.later(16 * 24 * 60))
        self.assertEqual(len(self.changes(bo)), 1)  # the same again: no new line

    def test_first_seen_notes_another_company_but_not_another_wording(self):
        with self.store.connect() as db:
            enrichment.offer_facts(db, [(['email:ada@globex.example'], {'title': 'PM'}, enrichment.RECORD)], 'google', NOW)
        self.step(Reader([[conn('Ada Quill', 'Product Manager at Globex', slug='ada-q')]]))
        self.assertEqual(self.changes('email:ada@globex.example'), [])  # same company, other words: no line
        with self.store.connect() as db:
            db.execute("DELETE FROM person_facts WHERE source='linkedin'")
            enrichment.offer_facts(db, [(['email:ada@globex.example'], {'title': 'PM'}, enrichment.RECORD)], 'google', NOW)
            db.execute("UPDATE graph_nodes SET info=json_set(info,'$.profile.linkedin_url','https://www.linkedin.com/in/ada-q/') WHERE id='email:ada@globex.example'")
        self.step(Reader([[conn('Ada Quill', 'Product Manager at Hooli', slug='ada-q')]]), at=self.later(8 * 24 * 60))
        line, = self.changes('email:ada@globex.example')
        self.assertEqual((line['old'], line['new']['company']), ({'title': 'PM', 'company': 'Globex'}, 'Hooli'))

    def test_pages_through_slowly_and_starts_again_after_a_week(self):
        pages = [[conn('Bo Tamsin', 'VP at Acme', slug='bo-tamsin')]] * 3
        read = Reader(pages)
        self.assertEqual(self.step(read)['done'], False)
        self.assertEqual(self.step(read, at=self.later(5)), {'wait': 'pause'})  # 8 to 20 minutes apart
        self.assertEqual(self.step(read, at=self.later(21))['done'], False)
        self.assertTrue(self.step(read, at=self.later(42))['done'])
        self.assertEqual(read.calls, [0, 40, 80])
        self.assertEqual(self.step(read, at=self.later(70)), {'wait': 'rest'})
        self.assertEqual(self.step(read, at=self.later(6 * 24 * 60)), {'wait': 'rest'})
        self.step(read, at=self.later(7 * 24 * 60 + 60))
        self.assertEqual(read.calls[-1], 0)
        with self.store.connect() as db:
            state = lc.get_state(db, 'li')
        least, most = (dt.datetime.fromisoformat(self.later(7 * 24 * 60 + 60 + m)) for m in (8, 20))
        self.assertTrue(least <= dt.datetime.fromisoformat(state['next_at']) <= most)

    def test_waking_hours_and_a_daily_cap(self):
        read = Reader([[conn('Bo Tamsin', 'VP at Acme', slug='bo-tamsin')]] * 100)
        self.assertEqual(self.step(read, at='2026-11-09T06:30:00+00:00'), {'wait': 'hours'})  # 7:30 local
        self.assertEqual(self.step(read, at='2026-11-09T20:30:00+00:00'), {'wait': 'hours'})  # 21:30 local
        narrow = {**ACCOUNT, 'active_hours': [12, 18]}
        self.assertEqual(self.step(read, account=narrow), {'wait': 'hours'})
        at = '2026-11-09T08:00:00+00:00'
        for _ in range(lc.PACE['steps_per_day']):
            self.assertIn('seen', self.step(read, at=at))
            at = self.later(21, at)
        self.assertEqual(self.step(read, at=at), {'wait': 'cap'})
        self.assertEqual(len(read.calls), 24)

    def test_any_failure_stops_for_the_day_and_never_retries(self):
        for code in ('linkedin_query_failed:HTTP_429', 'linkedin_security_check', 'linkedin_invalid_page'):
            with self.subTest(code), self.store.connect() as db:
                db.execute('DELETE FROM enrich_prefs')
            read = Reader([], fail=code)
            self.assertEqual(self.step(read), {'error': code})
            for minutes in (25, 60, 6 * 60, 23 * 60):
                self.assertIn(self.step(read, at=self.later(minutes))['wait'], ('stopped', 'hours'))
            self.assertEqual(len(read.calls), 1)
        busy = Reader([], fail='linkedin_browser_busy')  # only another job in the browser: just the pause
        with self.store.connect() as db:
            db.execute('DELETE FROM enrich_prefs')
        self.step(busy)
        self.step(busy, at=self.later(21))
        self.assertEqual(len(busy.calls), 2)

    def test_an_empty_page_that_says_more_is_odd(self):
        read = Reader([[], []])
        self.assertEqual(self.step(read), {'error': 'linkedin_odd_page'})
        self.assertEqual(self.step(read, at=self.later(30)), {'wait': 'stopped'})

    def test_waits_for_a_failing_sync_and_the_first_import(self):
        read = Reader([[conn('Bo Tamsin', 'VP at Acme', slug='bo-tamsin')]])
        with self.store.connect() as db:
            db.execute("UPDATE checkpoints SET error='linkedin_signed_out' WHERE account_id='li'")
        self.assertEqual(self.step(read), {'wait': 'live_error'})
        with self.store.connect() as db:
            db.execute("DELETE FROM milestones WHERE name='first_import:li'")
            db.execute("DELETE FROM checkpoints")
        self.assertEqual(self.step(read), {'wait': 'first_import'})
        self.assertEqual(read.calls, [])

    def test_which_accounts_read_connections(self):
        config = {'accounts': [ACCOUNT, {**ACCOUNT, 'id': 'off', 'connections': False}, {**ACCOUNT, 'id': 'shared', 'shared': True},
                               {**ACCOUNT, 'id': 'quiet', 'signals': False}, {'id': 'x', 'service': 'x'}]}
        self.assertEqual([x['id'] for x in lc.accounts(config)], ['li'])

    def test_the_connector_reads_a_page_and_names_a_security_check(self):
        li = a.load_connector('linkedin')
        source = li.Source({}, ACCOUNT, a.CONNECTOR_HELPERS)
        page = {'connections': [conn('Bo Tamsin', 'VP at Acme', slug='bo-tamsin')], 'more': False}
        with patch.object(li.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(page), '')) as run:
            self.assertEqual(source.connections(40), page)
        self.assertEqual(run.call_args[0][0][1:], ['connections', '--start', '40', '--count', '40'])
        failed = subprocess.CompletedProcess([], 2, '', 'linkedin-inbox: LinkedIn asked for a security check; finish it in the OpenClaw browser')
        with patch.object(li.subprocess, 'run', return_value=failed), self.assertRaises(a.SourceError) as caught:
            source.connections(0)
        self.assertEqual(caught.exception.category, 'linkedin_security_check')
        with patch.object(li.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '{"connections": "no"}', '')), \
                self.assertRaises(a.SourceError):
            source.connections(0)


if __name__ == '__main__':
    unittest.main()
