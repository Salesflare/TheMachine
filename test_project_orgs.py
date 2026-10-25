"""A project's organization: set from its people where that is clear (never personal mail, never the owner's own
company, never when unsure), picked by the owner (which stays), a one-time backfill that can be taken back, an
organization's page listing its projects, merges moving them along, and a shared board never sending more for it."""
import json
import unittest

import crm
import shared_graph as sg
import test_graph as tg
from test_graph import NOW, graph, mail

T = NOW.isoformat()


class ProjectOrgs(unittest.TestCase):
    setUp, add, build = tg.Boards.setUp, tg.Boards.add, tg.Boards.build
    STAGES = tg.Boards.STAGES

    def project(self, name, *mails):
        self.add(*mails)
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id DESC LIMIT ?', (len(mails),))]
            graph.label(db, ids, name, 'review', T)
            return db.execute('SELECT id FROM projects WHERE name=?', (name,)).fetchone()[0]

    def row(self, pid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT org,org_by FROM projects WHERE id=?', (pid,)).fetchone())

    def test_the_first_build_backfills_from_the_people_and_records_it_and_later_ones_are_auto(self):
        umicore = self.project('Umicore rollout', mail(4, 'Ann <ann@umicore.example>', 'sam@acme.com', thread='u'),
                               mail(3, 'Sam <sam@acme.com>', 'ann@umicore.example, Bo <bo@umicore.example>', ('SENT',), thread='u'))
        self.build()
        self.assertEqual(self.row(umicore), {'org': 'umicore.example', 'org_by': 'backfill'})
        with self.store.connect() as db:
            done = db.execute('SELECT done_at,filled FROM project_org_backfill').fetchone()
            self.assertEqual((done['done_at'], done['filled']), (T, 1))
            self.assertEqual(db.execute('SELECT org,source FROM project_org_fills WHERE project_id=?', (umicore,)).fetchone()[:], ('umicore.example', 'backfill'))
        later = self.project('Inkwell pilot', mail(2, 'Kim <kim@inkwell.example>', 'sam@acme.com', thread='i'))
        self.build()
        self.assertEqual(self.row(later), {'org': 'inkwell.example', 'org_by': 'auto'})
        self.assertEqual(self.row(umicore)['org_by'], 'backfill')  # once set, it stays

    def test_the_backfill_is_reversible_and_keeps_what_someone_changed_since(self):
        a = self.project('Alpha', mail(4, 'Ann <ann@alpha.example>', 'sam@acme.com', thread='a'))
        b = self.project('Beta', mail(4, 'Bo <bo@beta.example>', 'sam@acme.com', thread='b'))
        self.build()
        with self.store.connect() as db:
            graph.save_project(db, {'node_id': f'project:{b}', 'org': 'org:alpha.example'}, T)
            self.assertEqual(graph.undo_org_fills(db), 1)
        self.assertEqual(self.row(a), {'org': None, 'org_by': None})
        self.assertEqual(self.row(b), {'org': 'alpha.example', 'org_by': 'owner'})

    def test_personal_mail_colleagues_and_unsure_projects_get_no_organization(self):
        webmail = self.project('Garden', mail(4, 'Bob <bob@gmail.com>', 'sam@acme.com', thread='g'),
                               mail(3, 'Bob <bob@yahoo.co.uk>', 'sam@acme.com', thread='g2'))
        mostly_personal = self.project('Kitchen', mail(4, 'Bob <bob@gmail.com>', 'sam@acme.com', thread='k'),
                                       mail(3, 'Bob <bob@gmail.com>', 'sam@acme.com', thread='k2'),
                                       mail(2, 'Lia <lia@tiles.example>', 'sam@acme.com', thread='k3'))
        split = self.project('Joint venture', mail(4, 'Ann <ann@one.example>', 'sam@acme.com', thread='j'),
                             mail(3, 'Kim <kim@two.example>', 'sam@acme.com', thread='j2'))
        with_colleague = self.project('Client deal', mail(4, 'Pat <pat@acme.com>', 'sam@acme.com, Ann <ann@client.example>', thread='c'))
        self.build()
        self.assertEqual(self.row(webmail), {'org': None, 'org_by': None})
        self.assertEqual(self.row(mostly_personal), {'org': None, 'org_by': None})
        self.assertEqual(self.row(split), {'org': None, 'org_by': None})
        self.assertEqual(self.row(with_colleague)['org'], 'client.example')

    def test_a_mail_provider_not_on_any_list_looks_like_one_by_its_people(self):
        self.add(*[mail(3, f'P{i} <p{i}@isp.example>', 'sam@acme.com', thread=f'isp{i}') for i in range(7)],
                 *[mail(3, f'C{i} <c{i}@company.example>', 'sam@acme.com, ' + ', '.join(f'c{j}@company.example' for j in range(7) if j != i), thread='co')
                   for i in range(7)])
        self.build()
        with self.store.connect() as db:
            self.assertTrue(graph.personal_mail(db, 'gmail.com'))
            self.assertTrue(graph.personal_mail(db, 'isp.example'))  # seven people who never write together
            self.assertFalse(graph.personal_mail(db, 'company.example'))  # seven people in the same threads
            self.assertFalse(graph.personal_mail(db, 'named:acme'))

    def test_the_owner_picks_one_from_the_graph_or_a_new_one_and_their_pick_stays(self):
        pid = self.project('Umicore rollout', mail(4, 'Ann <ann@umicore.example>', 'sam@acme.com', thread='u'))
        with self.store.connect() as db:
            with self.assertRaisesRegex(ValueError, 'personal email'):
                graph.save_project(db, {'node_id': f'project:{pid}', 'org': 'gmail.com'}, T)
            with self.assertRaisesRegex(ValueError, 'personal email'):
                graph.create_record(db, 'org', {'name': 'Gmail', 'website': 'gmail.com'}, T)
            db.execute('COMMIT')
            made = graph.create_record(db, 'org', {'name': 'Umicore Battery'}, T)
            db.execute('COMMIT')
            graph.save_project(db, {'node_id': f'project:{pid}', 'org': made['node_id']}, T)
        self.assertEqual(self.row(pid), {'org': 'named:umicore-battery', 'org_by': 'owner'})
        self.build()
        with self.store.connect() as db:
            card = graph.project_card(db, f'project:{pid}')
            self.assertEqual((card['org_node']['id'], card['org_node']['name'], card['org_node']['by']), ('org:named:umicore-battery', 'Umicore Battery', 'owner'))
            graph.save_project(db, {'node_id': f'project:{pid}', 'org': ''}, T)  # none, and it stays none
        self.build()
        self.assertEqual(self.row(pid), {'org': None, 'org_by': 'owner'})
        with self.store.connect() as db:  # a review's domain doesn't change the owner's word either
            graph.set_stage(db, f'project:{pid}', 'Contacted', 'review', T, board='Listings', reason='asked',
                            event_id=db.execute('SELECT max(id) FROM events').fetchone()[0], org='umicore.example')
        self.assertEqual(self.row(pid), {'org': None, 'org_by': 'owner'})

    def test_a_review_never_sets_personal_mail(self):
        self.add(mail(3, 'Bob <bob@gmail.com>', 'sam@acme.com', thread='b'))
        with self.store.connect() as db:
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
            node = graph.set_stage(db, 'Bob deal', 'Contacted', 'review', T, board='Listings', reason='asked', event_id=event, org='gmail.com')['node_id']
            self.assertEqual(db.execute('SELECT org,org_by FROM projects WHERE id=?', (node[8:],)).fetchone()[:], (None, None))

    def test_the_organization_lists_its_projects_open_first_its_timeline_has_their_moves_and_merges_move_them(self):
        old = self.project('Umicore 2025 pilot', mail(30, 'Ann <ann@umicore.example>', 'sam@acme.com', thread='o'))
        new = self.project('Umicore rollout', mail(3, 'Ann <ann@umicore.example>', 'sam@acme.com', thread='n'))
        with self.store.connect() as db:
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
        other = self.project('Umicore Asia', mail(2, 'Li <li@umicore-asia.example>', 'sam@acme.com', thread='a'))
        with self.store.connect() as db:
            graph.set_stage(db, f'project:{new}', 'Agreed', 'review', T, board='Listings', reason='Ann agreed', event_id=event)
            db.execute("UPDATE projects SET outcome='won' WHERE id=?", (old,))  # won before boards: no stage
        self.build()
        with self.store.connect() as db:
            view = graph.detail(db, 'org:umicore.example')
            self.assertEqual([(p['name'], p['stage'], p['open']) for p in view['projects']],
                             [('Umicore rollout', 'Agreed', True), ('Umicore 2025 pilot', None, False)])
            moves = [i for i in graph.timeline(db, 'org:umicore.example', now=T)['items'] if i['type'] == 'move']
            self.assertEqual([(m['project'], m['stage']) for m in moves], [('Umicore rollout', 'Agreed')])
            crm.merge_orgs(db, 'org:umicore-asia.example', into='org:umicore.example', now=T)
            self.assertEqual(db.execute('SELECT org FROM projects WHERE id=?', (other,)).fetchone()[0], 'umicore.example')
            self.assertIn('Umicore Asia', [p['name'] for p in graph.detail(db, 'org:umicore.example')['projects']])
            crm.split_org(db, 'org:umicore-asia.example', now=T)
            self.assertEqual(db.execute('SELECT org FROM projects WHERE id=?', (other,)).fetchone()[0], 'umicore-asia.example')

    def test_named_organizations_carry_their_projects_into_a_merge(self):
        with self.store.connect() as db:
            named = graph.create_record(db, 'org', {'name': 'Globex'}, T)
            db.execute('COMMIT')
            graph.create_record(db, 'org', {'name': 'Globex Corp', 'website': 'globex.example'}, T)
            db.execute('COMMIT')
        self.build()
        with self.store.connect() as db:
            pid = graph.save_project(db, {'name': 'Globex deal', 'org': named['node_id']}, T)['node_id']
            crm.merge_orgs(db, named['node_id'], into='org:globex.example', now=T)
            self.assertEqual(db.execute('SELECT org FROM projects WHERE id=?', (pid[8:],)).fetchone()[0], 'globex.example')
            crm.split_org(db, named['node_id'], now=T)
            self.assertEqual(db.execute('SELECT org FROM projects WHERE id=?', (pid[8:],)).fetchone()[0], 'named:globex')

    def test_boards_and_lists_show_the_organization_to_link_to(self):
        pid = self.project('Umicore rollout', mail(3, 'Ann <ann@umicore.example>', 'sam@acme.com', thread='u'))
        with self.store.connect() as db:
            graph.set_stage(db, f'project:{pid}', 'Contacted', 'review', T, board='Listings', reason='asked',
                            event_id=db.execute('SELECT max(id) FROM events').fetchone()[0])
        self.build()
        with self.store.connect() as db:
            tile, = graph.boards(db, T)[0]['projects']
            self.assertEqual((tile['org']['node_id'], tile['org']['name']), ('org:umicore.example', 'Umicore'))
            row, = graph.page(db, 'projects')['items']
            self.assertEqual(row['org_node'], {'id': 'org:umicore.example', 'name': 'Umicore'})

    def test_a_shared_board_sends_the_organization_only_when_it_could_go_itself(self):
        pid = self.project('Paperkite', mail(3, 'Ann <ann@partner.example>', 'sam@acme.com', thread='p'))
        with self.store.connect() as db:
            sg.ensure(db)
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
            graph.set_stage(db, f'project:{pid}', 'Agreed', 'review', T, board='Listings', reason='Ann agreed', event_id=event)
        self.build()

        def shared(org):
            with self.store.connect() as db:
                db.execute('UPDATE projects SET org=? WHERE id=?', (org, pid))
                sg.judge(db, [{'event_id': event, 'share': 'client', 'line': 'Ann agreed'}])
                scope = sg.Scope(db, ['work'], ['acme.com'], ['sam@acme.com'])
                records, _, _, _ = sg.collect(db, scope, b'k' * 32, b's' * 32, today=NOW)
                project = next(r for r in records.values() if r['t'] == 'project')
                return project['org'], project['people'], project['timeline']
        org, people, story = shared('partner.example')
        self.assertEqual(org['name'], 'Partner')
        for kept_out in ('gmail.com', 'acme.com', 'named:partner'):
            got, same_people, same_story = shared(kept_out)
            self.assertIsNone(got, kept_out)
            self.assertEqual((same_people, same_story), (people, story))  # linking one never adds people or threads


if __name__ == '__main__':
    unittest.main()
