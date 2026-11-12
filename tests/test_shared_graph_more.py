"""The Shared Graph, continued (shared_graph.py, docs/shared-graph.md): removal, new devices and pause, what goes per
thread, a live Fleet's cases, sharing by name, whose it is, and team learnings. The made-up Fleet, its fake Network and the
helpers are tests/test_shared_graph.py's; these tests are a file of their own so the two halves run side by side."""
import json
import sqlite3
import time
import unittest
import unittest.mock
from unittest.mock import patch

import fleet_trust as ft
import network_crypto as nc
import shared_graph as sg
import test_shared_graph as base  # by module: its test classes run in its own file, not again here
from test_shared_graph import BODY, DEAL, FLEET, HEALTH, PERSONAL, a, ago, fleet, graph, mail


class SharedGraphMore(base.SharedGraph):
    # -- seamless, and still safe: removal, new devices, pause
    def test_someone_taken_out_gets_nothing_new_even_if_the_network_keeps_them_in(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        self.adm.graph_remove(FLEET, 'mem3')
        self.assertTrue(any(i['s']['t'] == 'remove' and i['s']['member'] == 'mem3' for i in self.net.trust))
        self.rounds(1)
        self.assertNotIn(BODY, self.received(self.mem))  # what the team shared with them left their Machine
        self.assertEqual(self.from_others(self.mem), {})
        self.net.trust = [i for i in self.net.trust if i['s']['t'] != 'remove']  # a Network that hides the remove later
        self.new_thread(20, 'Second order', 'Forty more seats, please.')
        self.rounds()
        self.assertNotIn('Forty more seats', self.received(self.mem))
        self.assertEqual(self.from_others(self.mem), {})
        self.assertFalse([p for p in self.adm._prompts() if p['kind'] == 'member' and p['member'] == 'mem3'])  # no new OK asked
        self.assertEqual({p['name']: p['state'] for p in self.adm.sharing()[0]['people']}['Mo'], 'removed')
        # let back in: what the team shares now, each thread and record once
        self.adm.graph_remove(FLEET, 'mem3', back=True)
        self.rounds(6)
        self.assertIn('Forty more seats', self.received(self.mem))
        self.assertIn(BODY, self.received(self.mem))
        theirs = lambda box, table, key: sorted((r['member'], r[key]) for r in self.team(box, table) if r['member'] == 'own1')
        self.assertEqual(theirs(self.mem, 'team_mail', 'tag'), theirs(self.adm, 'team_mail', 'tag'))  # as a teammate who was never out
        self.assertEqual(theirs(self.mem, 'team_records', 'rid'), theirs(self.adm, 'team_records', 'rid'))
        with self.mem.store.connect() as db:
            self.assertEqual([p['name'] for p in self.mem.team_overview(db, {})['people']].count('Lee Park'), 1)

    def test_someone_taken_out_loses_what_the_team_shared_with_them_and_only_that(self):
        self.olive_mail()
        board = self.deal_board()
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])  # a board shared with Mo by name
        # Ada knows someone only she knows; Mo knows Lee too, from Mo's own mail, and shares that
        self.add(self.adm, mail('work', 60, 'Kim Vale <kim@other.example>', 'adm2@acme.example', 'Pilot', 'Kim asks about a pilot.', 2, 't-kim'))
        self.judge(self.adm, ('work-60', 'client', 'Kim asked about a pilot'))
        self.add(self.mem, mail('work', 70, 'Lee Park <lee@client.example>', 'mem3@acme.example', 'Seats', 'Mo, can you check the seats?', 2, 't-seats'),
                 mail('home', 71, 'Sam Friend <sam@friends.example>', 'mem3@home.example', 'Sunday', 'Lunch on Sunday?', 1, 't-lunch'))
        self.judge(self.mem, ('work-70', 'client', 'Lee asked Mo about seats'))
        self.rounds(3)
        self.assertIn(BODY, self.received(self.mem))
        self.assertIn(DEAL, self.received(self.mem))
        self.assertIn('Kim asks about a pilot', self.received(self.mem))
        with self.mem.store.connect() as db:
            self.assertEqual({p['name'] for p in self.mem.team_overview(db, {})['people']} & {'Lee Park', 'Kim Vale'}, {'Lee Park', 'Kim Vale'})

        def own_data(box):
            with box.store.connect() as db:
                sg.ensure(db)
                return {name: [tuple(r) for r in db.execute(sql)] for name, sql in (
                    ('events', 'SELECT id,source_id,title,body,metadata FROM events ORDER BY id'),
                    ('nodes', 'SELECT id,kind,name,info FROM graph_nodes ORDER BY id'),
                    ('links', 'SELECT node_id,event_id FROM graph_events ORDER BY 1,2'),
                    ('calls', 'SELECT thread,verdict,hand FROM share_threads ORDER BY 1'),
                    ('sent', 'SELECT fleet,kind,key,hash FROM share_out ORDER BY 1,2,3'),
                    ('blobs', "SELECT id FROM team_blobs WHERE member='mem3' ORDER BY 1"),
                    ('to-dos', 'SELECT id,title FROM suggestions ORDER BY 1'))}
        before, had = own_data(self.mem), {box.member_id: self.received(box) for box in (self.own, self.adm)}
        self.assertTrue(before['sent'] and before['blobs'])
        self.assertTrue(any(n[0] == 'email:lee@client.example' for n in before['nodes']))
        self.adm.graph_remove(FLEET, 'mem3')
        self.rounds(1)
        self.assertEqual(self.from_others(self.mem), {})  # records, threads, the board shared by name, the copies to pass on
        for text in (BODY, DEAL, 'Kim asks about a pilot'):
            self.assertNotIn(text, self.received(self.mem) + json.dumps(self.team(self.mem)))
        self.assertNotIn('Sale: Buyer', self.projects_of(self.mem))
        self.assertEqual(own_data(self.mem), before)  # Mo's own mail, people, to-dos and what Mo shared: as they were
        with self.mem.store.connect() as db:
            names = {p['name'] for p in self.mem.team_overview(db, {})['people']}
            self.assertNotIn('Kim Vale', names)  # known only through the team: gone
            lee = db.execute("SELECT name FROM graph_nodes WHERE id='email:lee@client.example'").fetchone()
            self.assertEqual(lee['name'], 'Lee Park')  # known to Mo too: Mo's own record of Lee stays
            self.assertFalse([e for e in self.mem.team_graph(db) if any(x['member'] != 'mem3' for x in e['sources'])])
        self.assertTrue(any(line['outcome'].startswith('removed from this Machine') for line in self.mem.view()['log']))
        # the team keeps what Mo shared, and each other's
        self.assertIn('Mo, can you check the seats?', self.received(self.own))
        self.assertEqual({box.member_id: self.received(box) for box in (self.own, self.adm)}, had)
        self.rounds()
        self.assertEqual(self.from_others(self.mem), {})
        self.assertEqual(own_data(self.mem), before)

    def test_someone_taken_out_while_their_machine_is_away_loses_it_when_it_is_back(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        everyone, self.boxes = self.boxes, [self.own, self.adm]  # Mo's Machine is off
        self.new_thread(22, 'While away', 'Sent while Mo was away.')
        self.rounds()  # on the Network for Mo's Machine, from before the removal
        self.adm.graph_remove(FLEET, 'mem3')
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))  # still off: nothing reached it
        self.boxes = everyone  # back on, any time later
        self.rounds(1)
        self.assertEqual(self.from_others(self.mem), {})
        self.assertNotIn('Sent while Mo was away', self.received(self.mem))  # nor what was still on its way
        self.rounds()
        self.assertEqual(self.from_others(self.mem), {})
        with self.mem.store.connect() as db:
            self.assertFalse(db.execute('SELECT count(*) FROM team_pending').fetchone()[0])

    def test_someone_taken_out_loses_it_as_soon_as_the_network_rings_their_machine(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        everyone, self.boxes = self.boxes, [self.own, self.adm]  # no round of Mo's Machine from here on
        # a ring without a signed remove does nothing: Mo keeps what the team shared
        self.adm.graph_nudge(self.adm.directory()['fleets'][0], {'member_id': 'adm2'}, 'mem3')
        self.mem.graph_fetch()
        self.assertIn(BODY, self.received(self.mem))
        self.assertTrue(self.from_others(self.mem))
        # the remove: the admin's Machine rings Mo's, which looks at the Fleet when its inbox says so (fleet.step)
        before = len(self.net.calls)
        self.adm.graph_remove(FLEET, 'mem3')
        rings = [c[3]['blob'] for c in self.net.calls[before:] if c[0] == 'adm2' and c[2] == '/graph' and c[3] and c[3].get('op') == 'put'
                 and c[3]['blob']['header']['to'] == ['mem3']]
        self.assertEqual([b['header']['kind'] for b in rings], ['want'])  # one, empty: nothing of the team's is in it
        self.mem.graph_fetch()
        self.assertEqual(self.from_others(self.mem), {})
        self.assertNotIn(BODY, self.received(self.mem))
        self.boxes = everyone

    def test_a_round_reads_the_directory_again_so_a_remove_is_seen_within_one(self):
        self.rounds()
        asked = lambda: len([c for c in self.net.calls if c[0] == 'mem3' and c[2] == '/directory'])
        before = asked()
        self.mem.last['graph'] = -1e9
        self.mem.graph_round()  # as every five minutes, not forced
        self.assertEqual(asked(), before + 1)

    def test_someone_who_left_is_signed_out_so_the_network_cant_bring_them_back(self):
        self.rounds()
        person = self.net.people.pop('mem3')  # they left the Fleet
        self.rounds()
        self.assertTrue(any(i['s']['t'] == 'remove' and i['s']['member'] == 'mem3' for i in self.net.trust))
        self.net.people['mem3'] = person  # a Network that puts them back, with the same keys
        self.new_thread(21, 'After they left', 'Nothing of this goes to them.')
        self.rounds()
        self.assertNotIn('Nothing of this', self.received(self.mem))

    def test_a_new_machine_of_someone_admitted_needs_no_ok_but_waits_for_the_hold(self):
        self.olive_mail()
        self.rounds()
        phone = self.machine('mem3', '-new')  # Mo's new Machine: new keys, same person
        phone.set_meta('graph_start:' + FLEET, {'shown': a.now(), 'started': a.now()})
        self.boxes = [self.own, self.adm, phone]
        self.rounds()
        self.assertFalse([p for p in self.adm._prompts() if p['kind'] == 'member'])  # no tap for a known person
        devices = self.adm.sharing()[0]['new_devices']
        self.assertEqual([d['name'] for d in devices], ['Mo'])
        self.assertEqual([d['name'] for d in self.own.sharing()[0]['new_devices']], ['Mo'])  # every admin sees it
        self.assertEqual(phone.sharing()[0]['new_devices'], [])
        self.assertNotIn(BODY, self.received(phone))  # not during the hold
        for box in (self.own, self.adm):
            rekey = box.meta('graph_rekey:' + FLEET) or {}
            for r in rekey.values():
                r['since'] = ago(2)
            box.set_meta('graph_rekey:' + FLEET, rekey)
        self.rounds(3)
        self.assertTrue(any(i['s']['t'] == 'member' and i['s'].get('device') and i['s']['member'] == 'mem3' for i in self.net.trust))
        self.assertIn(BODY, self.received(phone))

    def test_not_theirs_keeps_a_new_key_out(self):
        self.rounds()
        stranger = self.machine('mem3', '-forged')  # keys the Network made up for Mo
        self.boxes = [self.own, self.adm, stranger]
        self.rounds()
        for box in (self.own, self.adm):
            box.graph_rekey_no(FLEET, 'mem3')
            rekey = box.meta('graph_rekey:' + FLEET) or {}
            self.assertNotIn('mem3', rekey)
        self.olive_mail()
        self.rounds(3)
        self.assertFalse(any(i['s']['t'] == 'member' and i['s'].get('device') for i in self.net.trust))
        self.assertEqual(self.received(stranger), '[]')

    def test_an_admin_pauses_sharing_for_everyone(self):
        self.olive_mail()
        self.adm.graph_pause(FLEET, True)
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))
        self.assertEqual(self.own.sharing()[0]['paused']['by'], 'Ada')
        with self.assertRaisesRegex(ValueError, 'confirmed admin'):
            self.mem.graph_pause(FLEET, False)
        self.adm.graph_pause(FLEET, False)
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))

    def test_sharing_off_with_remove_deletes_it_everywhere_also_on_a_machine_that_was_away(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        self.boxes.remove(self.mem)  # away
        self.new_thread(40, 'Late order', 'One more order, sent while Mo was away.')
        self.rounds()  # waits in the mailbox for Mo's Machine
        time.sleep(1.1)  # statements and blobs carry whole seconds: the removal comes after the late blob
        with self.assertRaisesRegex(ValueError, 'confirmed admin'):
            self.mem.graph_pause(FLEET, True, remove=True)
        self.adm.graph_pause(FLEET, True, remove=True)
        self.rounds()
        self.assertTrue(self.own.sharing()[0]['paused']['removed'])
        for box in (self.own, self.adm):
            self.assertEqual(self.team(box, 'team_mail') + self.team(box) + self.team(box, 'team_blobs'), [])
        self.assertFalse(self.own.sharing()[0]['started'])  # each owner looks it over again
        self.adm.graph_pause(FLEET, False)  # back on before Mo's Machine is: the removal still reaches it
        self.rounds()
        self.boxes.append(self.mem)
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail') + self.team(self.mem) + self.team(self.mem, 'team_blobs'), [])
        self.assertNotIn('One more order', json.dumps(self.team(self.mem, 'team_mail')))  # the late blob from before is dropped
        self.own.graph_start(FLEET)
        self.rounds(3)
        self.assertIn(BODY, self.received(self.mem))  # Olive started again: it goes again, from the start
        self.assertIn('One more order', self.received(self.mem))

    def test_taking_a_thread_back_goes_first_and_never_waits_behind_new_shares(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        spent = [[int(time.time() // 60), sg.PER_HOUR]]
        self.own.set_meta('graph_puts', spent)  # new shares spent this hour's budget
        self.assertEqual(self.own._budget(), 0)
        self.assertEqual(self.own._budget(gone=True), sg.GONE_HOUR)
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-1'), 'private')
        self.own.set_meta('graph_gone_puts', [[int(time.time() // 60), sg.GONE_HOUR]])  # and taking back spent its own
        self.own.graph_round(force=True)
        self.assertEqual([h for h in self.mail_puts(self.own) if not self.net.blobs[h['id']]['ct']], [])
        self.own.set_meta('graph_gone_puts', [])  # an hour later; new shares still out of budget
        self.own.graph_round(force=True)
        gone = [h for h in self.mail_puts(self.own) if not self.net.blobs[h['id']]['ct']]
        self.assertEqual(len(gone), 1)
        self.assertEqual(self.own._budget(gone=True), sg.GONE_HOUR - 1)  # counted on its own
        self.assertEqual(self.own.meta('graph_puts'), spent)
        for box in (self.adm, self.mem):
            box.graph_round(force=True)
        self.assertNotIn(BODY, self.received(self.mem))
        self.assertLess(sg.PER_HOUR, 1200)  # under the Network's own limits (the cloud's fleet_graph.py)
        self.assertLess(sg.GONE_HOUR, 1200)
        self.assertLess(sg.PER_DAY, 20000)
        self.assertLess(sg.GONE_DAY, 20000)

    def test_put_counts_from_before_still_count(self):
        stamp = time.time()
        self.own.set_meta('graph_puts', [stamp - 10, stamp - 7200, stamp - 90000])  # times, as a Machine from before kept them
        self.assertEqual(self.own._budget(), sg.PER_HOUR - 1)
        self.own._spent()
        self.assertEqual(self.own._budget(), sg.PER_HOUR - 2)
        self.assertEqual(sum(n for _, n in self.own.meta('graph_puts')), 3)  # the day-old one dropped

    def test_an_unshared_thread_is_never_passed_on_from_an_old_copy(self):
        self.olive_mail()
        self.rounds()
        with self.adm.store.connect() as db:
            sg.ensure(db)
            old = dict(db.execute("SELECT * FROM team_blobs WHERE member='own1' AND kind='mail'").fetchone())
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-1'), 'private')
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))
        self.assertNotIn(BODY, self.received(self.adm))
        header = json.loads(old['header'])  # a teammate's Machine that kept an old copy passes it on anyway
        wrap = nc.seal({'dk': old['dk'], 'h': old['sha'], 'from_key': self.net.keys['own1']['sign']}, self.adm._private(), self.net.keys['mem3'],
                       sg.wrap_context(header, 'adm2', 'mem3'))
        with self.assertRaisesRegex(ValueError, 'no longer shared|older'):  # its tombstone or the newer list stops it
            self.mem.graph_take({'header': header, 'ct': old['ct'], 'sig': old['sig'], 'wrap': wrap, 'by': 'adm2'})
        with self.mem.store.connect() as db:  # a Machine that never got the tombstone: the newer thread list still stops it
            db.execute("DELETE FROM team_blobs WHERE member='own1' AND kind='mail'")
        with self.assertRaisesRegex(ValueError, 'no longer shared'):
            self.mem.graph_take({'header': header, 'ct': old['ct'], 'sig': old['sig'], 'wrap': wrap, 'by': 'adm2'})
        self.assertNotIn(BODY, self.received(self.mem))

    def test_sharing_is_off_until_an_admin_requires_something_which_turns_it_on_and_off_still_wins(self):
        self.olive_mail()
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['paused'], {'default': True})
        self.adm.graph_set_policy(FLEET, ['mail'])  # requiring the Work email is the admin's turn-on: no second switch
        self.rounds()
        self.assertIsNone(self.own.sharing()[0]['paused'])
        self.assertIn(BODY, self.received(self.mem))
        self.adm.graph_pause(FLEET, True)  # an admin's Off still wins over what is required
        self.rounds()
        self.assertTrue(self.own.sharing()[0]['paused'])

    def test_sharing_is_off_until_an_admin_turns_it_on(self):
        self.olive_mail()
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        self.assertEqual(self.own.sharing()[0]['paused'], {'default': True})
        with self.assertRaisesRegex(ValueError, 'confirmed admin'):
            self.mem.graph_pause(FLEET, False)
        self.adm.graph_pause(FLEET, False)
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        self.assertIsNone(self.own.sharing()[0]['paused'])

    def test_each_connection_is_shared_or_not_work_on_and_personal_never(self):
        self.olive_mail()
        self.add(self.own, mail('home', 20, 'Kim Wu <kim@globex.example>', 'own1@home.example', 'Pilot from home', 'Pilot price, from my own address.', 1, 't-home-pilot'))
        self.judge(self.own, ('home-20', 'client', 'Kim asked about the pilot'), ('home-5', 'personal', 'Sam wrote'))
        conns = {c['id']: c for c in self.own.sharing()[0]['connections']}
        self.assertEqual((conns['work']['on'], conns['home']['on'], conns['home']['personal']), (True, False, True))
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        with self.assertRaisesRegex(ValueError, 'Personal connections are never shared'):
            self.own.graph_connection(FLEET, 'home', True)
        self.own.set_meta('graph_conn:' + FLEET, {'home': True})  # an old choice from before can't turn a personal one on
        self.rounds()
        self.assertNotIn('Pilot price', self.received(self.mem))
        self.assertNotIn(PERSONAL, self.received(self.mem))
        self.own.graph_connection(FLEET, 'work', False)  # off: what it shared is taken back
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))

    def test_a_connection_replaced_by_a_new_one_to_the_same_place_is_listed_once(self):
        # Intercom reconnected: the old account stays in the config, retired into the new one; What's shared lists one
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'old-intercom', 'service': 'intercom', 'email': 'olive@acme.example', 'boundary': 'work:Acme',
                                         'retired': {'into': 'new-intercom', 'at': '2026-10-24T03:38:08+00:00'}},
                                        {'id': 'new-intercom', 'service': 'intercom', 'email': 'olive@acme.example', 'boundary': 'work:Acme'}]
        ids = [c['id'] for c in self.own.sharing()[0]['connections'] if c['service'] == 'intercom']
        self.assertEqual(ids, ['new-intercom'])
        self.assertNotIn('old-intercom', self.own.graph_accounts(FLEET))

    def test_an_x_account_named_for_the_company_is_its_work_even_with_a_handle_for_an_address(self):
        # an X account's address is its handle (@acme): no email domain, so it's the company's when it's named for the
        # Fleet, and another company's only when it's named for another one
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'acme-x', 'service': 'x', 'email': '@acme', 'boundary': 'work:Acme'},
                                        {'id': 'side-x', 'service': 'x', 'email': '@SideProject', 'boundary': 'work:Side Project'}]
        conns = {c['id']: c for c in self.own.sharing()[0]['connections']}
        self.assertEqual((conns['acme-x']['company'], conns['acme-x']['on']), (True, True))
        self.assertEqual((conns['side-x']['company'], conns['side-x']['on']), (False, False))

    def test_another_persons_calendar_read_through_the_owners_sign_in_is_named_for_that_calendar(self):
        # a partner's calendar read through the work sign-in is its own personal connection, not a second copy of the
        # work calendar: named for the calendar it reads, and the work calendar keeps its own label and switch
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'work-cal', 'service': 'calendar', 'email': 'olive@acme.example', 'boundary': 'work:Acme'},
                                        {'id': 'partner-cal', 'service': 'calendar', 'email': 'olive@acme.example', 'calendar_id': 'robin@home.example',
                                         'display_name': 'Robin’s calendar', 'boundary': 'personal:Robin'},
                                        {'id': 'bare-cal', 'service': 'calendar', 'email': 'olive@acme.example', 'calendar_id': 'sam@home.example', 'boundary': 'personal:Sam'}]
        self.adm.graph_set_policy(FLEET, ['calendar'])
        self.rounds()
        conns = {c['id']: c for c in self.own.sharing()[0]['connections']}
        self.assertEqual((conns['work-cal']['name'], conns['work-cal']['required'], conns['work-cal']['on']), ('', True, True))
        self.assertEqual((conns['partner-cal']['name'], conns['partner-cal']['personal'], conns['partner-cal']['on']), ('Robin’s calendar', True, False))
        self.assertEqual(conns['bare-cal']['name'], 'sam@home.example')
        self.assertEqual(conns['work']['name'], '')

    def test_an_admin_can_require_work_email_and_threads_kept_private_still_stay(self):
        self.olive_mail()
        with self.assertRaisesRegex(ValueError, 'confirmed admin'):
            self.mem.graph_set_policy(FLEET, ['mail'])
        self.adm.graph_set_policy(FLEET, ['mail', 'calendar', 'everything'])
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['require'], ['mail', 'calendar'])
        work = next(c for c in self.own.sharing()[0]['connections'] if c['id'] == 'work')
        self.assertEqual((work['required'], work['on']), (True, True))
        self.assertFalse(next(c for c in self.own.sharing()[0]['connections'] if c['id'] == 'home')['required'])  # personal: never required
        with self.assertRaisesRegex(ValueError, 'Required'):
            self.own.graph_connection(FLEET, 'work', False)
        self.own.set_meta('graph_conn:' + FLEET, {'work': False})  # an old choice can't beat what the Fleet requires
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-1'), 'private')  # Keep private on one thread still holds
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))
        forged = ft.sign(self.mem._private(), {'t': 'policy', 'fleet': FLEET, 'member': 'mem3', 'key': self.net.keys['mem3']['sign'], 'by': 'mem3',
                                               'require': [], 'at': '2099-01-01T00:00:00+00:00'})
        self.net.trust.append(forged)  # a Network that makes one up, or a member who isn't an admin: ignored
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['require'], ['mail', 'calendar'])

    def test_an_only_you_board_shares_nothing_and_switching_to_it_takes_back_what_went(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        with self.own.store.connect() as db:  # this project is Only you
            db.execute("INSERT INTO projects(id,name,created_at,visibility) VALUES(77,'Quiet deal',?,'only_you')", (a.now(),))
            db.execute("INSERT INTO event_projects(event_id,project_id,source,created_at) VALUES(?,77,'test',?)", (self.event_id(self.own, 'work-2'), a.now()))
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))  # the whole thread, also its other messages
        self.assertNotIn('Quiet deal', json.dumps(self.team(self.mem)))

    # -- what goes, judged per thread: when unsure, not
    def test_a_new_client_thread_waits_an_hour_first(self):
        sg.HOLD = 3600
        self.olive_mail()
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))
        with self.own.store.connect() as db:
            db.execute('UPDATE share_threads SET sorted_at=?', (ago(0, 2),))
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))

    def test_unsure_waits_in_share_these_and_other_never_goes(self):
        self.add(self.own, mail('work', 30, 'Pat Peer <pat@peer.example>', 'own1@acme.example', 'Swap listings?', 'Shall we list each other?', 1, 't-peer'),
                 mail('work', 31, 'Ads Team <team@ads.example>', 'own1@acme.example', 'Grow your reach', 'Our new ad formats are here.', 1, 't-ads'))
        self.judge(self.own, ('work-30', 'unsure', 'Pat asked about listings'), ('work-31', 'other', ''))
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        view = self.own.graph_overview(FLEET)
        self.assertEqual([x['title'] for x in view['unsure']], ['Swap listings?'])
        self.assertEqual(view['sorted']['other'], 1)
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        app.graph_share_action('graph_share_many', {'event_ids': [self.event_id(self.own, 'work-30')], 'share': 'team'})
        self.rounds()
        self.assertIn('Shall we list each other?', self.received(self.mem))
        self.assertNotIn('ad formats', self.received(self.mem))

    def test_share_these_asks_once_per_group_with_the_review_s_suggestion(self):
        self.peers()
        view = self.own.graph_overview(FLEET)
        self.assertEqual(view['groups'], [{'name': 'Partner and listing exchanges', 'suggest': 'team', 'count': 2},
                                          {'name': 'Investors and buyers', 'suggest': 'people', 'count': 1},
                                          {'name': '', 'suggest': None, 'count': 1}])  # no group (or a made-up choice): last, nothing suggested
        self.assertEqual({x['title']: x['group'] for x in view['unsure']}, {'Listy x Acme': 'Partner and listing exchanges', 'Rankr x Acme': 'Partner and listing exchanges',
                                                                           'Quick catch-up': 'Investors and buyers', 'Hello': ''})
        self.assertEqual(view['teammates'], [{'fleet': FLEET, 'member': 'adm2', 'name': 'Ada'}, {'fleet': FLEET, 'member': 'mem3', 'name': 'Mo'}])
        with self.own.store.connect() as db:
            self.assertEqual(sg.groups(db), ['Partner and listing exchanges', 'Investors and buyers'])  # for the next review to reuse
        self.assertEqual(sg.unsure_groups([{'group': 'G', 'suggest': 'team'}, {'group': 'G', 'suggest': 'private'}]),
                         [{'name': 'G', 'suggest': 'private', 'count': 2}])  # a tie: the cautious choice

    def test_share_with_chosen_teammates_from_share_these_reaches_only_them(self):
        self.peers()
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        fund = self.event_id(self.own, 'work-42')
        with self.assertRaisesRegex(ValueError, 'Choose who'):
            app.graph_share_action('graph_share_many', {'event_ids': [fund], 'share': 'people', 'people': []})
        with self.assertRaises(ValueError):  # only confirmed teammates of a Work Fleet
            app.graph_share_action('graph_share_many', {'event_ids': [fund], 'share': 'people', 'people': [{'fleet': FLEET, 'member': 'stranger'}]})
        out = app.graph_share_action('graph_share_many', {'event_ids': [fund], 'share': 'people',
                                                          'people': [{'fleet': FLEET, 'member': 'adm2'}]})
        self.assertEqual((out['done'], out['shared_with']), (1, ['Ada']))
        self.rounds()
        self.assertIn('selling a stake', self.received(self.adm))
        self.assertNotIn('selling a stake', self.received(self.mem))  # plain Share is the whole team; Share with… is not
        view = self.own.graph_overview(FLEET)
        self.assertNotIn('Quick catch-up', [x['title'] for x in view['unsure']])
        kept = next(x for x in view['by_hand'] if x['title'] == 'Quick catch-up')
        self.assertEqual((kept['shared_with'], 'thread' in kept), (['Ada'], False))
        self.assertEqual([g['name'] for g in view['groups']], ['Partner and listing exchanges', ''])

    def test_share_with_skips_personal_and_colleague_only_threads(self):
        self.olive_mail()
        self.add(self.own, mail('work', 23, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Our kids', 'Family weekend plans.', 2, 't-kids'))
        self.judge(self.own, ('work-23', 'personal', 'Family'))
        out = self.own.graph_threads_share([self.event_id(self.own, s) for s in ('work-23', 'work-4', 'home-5')], [{'fleet': FLEET, 'member': 'adm2'}])
        self.assertEqual((out['done'], out['skipped']), (0, 3))
        self.rounds()
        self.assertNotIn('Family weekend plans', self.received(self.adm))
        self.assertNotIn(PERSONAL, self.received(self.adm))

    def test_an_unsure_thread_from_before_groups_is_judged_again_and_still_waits_for_the_owner(self):
        self.peers()
        with self.own.store.connect() as db:
            db.execute('UPDATE share_threads SET grp=NULL,suggest=NULL')  # judged before the review grouped them
        given = {x['subject'] for x in self.own.graph_unjudged()}
        self.assertTrue({'Listy x Acme', 'Rankr x Acme', 'Quick catch-up', 'Hello'} <= given)
        with self.own.store.connect() as db:
            sg.judge(db, [{'event_id': self.event_id(self.own, 'work-40'), 'share': 'client', 'line': 'Pat proposed a listing swap', 'group': 'Partner and listing exchanges'},
                          {'event_id': self.event_id(self.own, 'work-41'), 'share': 'client', 'line': 'Kim proposed a backlink swap'},
                          {'event_id': self.event_id(self.own, 'work-42'), 'share': 'sensitive', 'line': ''},
                          {'event_id': self.event_id(self.own, 'work-43'), 'share': 'unsure', 'line': ''}])
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])  # "They stay with you until you choose": client now only suggests Share
        view = self.own.graph_overview(FLEET)
        self.assertEqual({x['title']: (x['group'], x['suggest']) for x in view['unsure']},
                         {'Listy x Acme': ('Partner and listing exchanges', 'team'), 'Rankr x Acme': ('Client and partner work', 'team'), 'Hello': ('', None)})
        self.assertEqual(view['held'], 1)  # the fund's question: sensitive, out of the list, nothing goes
        self.assertFalse({'Listy x Acme', 'Rankr x Acme', 'Quick catch-up', 'Hello'} & {x['subject'] for x in self.own.graph_unjudged()})  # once
        self.add(self.own, mail('work', 44, 'Sol <sol@new.example>', 'own1@acme.example', 'Sol x Acme', 'A listing swap?', 0, 't-sol'))
        with self.own.store.connect() as db:  # a new one the review is sure of: client, as before
            sg.judge(db, [{'event_id': self.event_id(self.own, 'work-44'), 'share': 'client', 'line': 'Sol proposed a listing swap'}])
        self.rounds()
        self.assertIn('A listing swap?', self.received(self.mem))

    def test_sensitive_sticks_whatever_a_later_review_says(self):
        self.olive_mail()
        for later in ('client', 'unsure', 'other'):
            self.judge(self.own, ('work-3', later, 'Lee wrote'))
            with self.own.store.connect() as db:
                self.assertEqual(db.execute('SELECT verdict FROM share_threads WHERE event_id=?', (self.event_id(self.own, 'work-3'),)).fetchone()[0], 'sensitive')
        self.rounds()
        self.assertNotIn(HEALTH, self.received(self.mem))

    def test_a_shared_thread_a_later_review_calls_sensitive_is_taken_back(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, self.received(self.mem))
        self.judge(self.own, ('work-1', 'sensitive', 'Lee wrote about the deal'))
        self.rounds()
        self.assertNotIn(BODY, self.received(self.mem))
        self.assertNotIn(BODY, self.received(self.adm))

    def test_automated_senders_are_never_a_client(self):
        self.add(self.own, mail('work', 40, 'Site Audit <no-reply@audit.example>', 'own1@acme.example', 'Weekly audit', '12 broken links found.', 1, 't-audit'))
        self.judge(self.own, ('work-40', 'client', 'An audit'))
        self.rounds()
        self.assertNotIn('broken links', self.received(self.mem))

    def test_choosing_twice_for_one_company_asks_once_to_make_it_a_rule(self):
        self.add(self.own, *[mail('work', 50 + i, 'Lee Park <lee@client.example>', 'own1@acme.example', f'Note {i}', f'Note body {i}', 1, f't-note-{i}') for i in range(3)])
        self.judge(self.own, *[(f'work-{50 + i}', 'client', 'Lee wrote') for i in range(3)])
        app = object.__new__(a.App); app.store, app.fleet, app.config = self.own.store, self.own, self.own.config
        first = app.graph_share_action('graph_share', {'event_id': self.event_id(self.own, 'work-50'), 'share': 'only_you'})
        self.assertIsNone(first['suggest'])
        second = app.graph_share_action('graph_share', {'event_id': self.event_id(self.own, 'work-51'), 'share': 'only_you'})
        self.assertEqual(second['suggest'], {'key': '@client.example', 'name': 'Client', 'choice': 'private'})
        again = app.graph_share_action('graph_share', {'event_id': self.event_id(self.own, 'work-52'), 'share': 'only_you'})
        self.assertIsNone(again['suggest'])  # asked once
        app.graph_share_action('graph_rule', {'key': '@client.example', 'choice': 'private', 'name': 'Client'})
        self.add(self.own, mail('work', 60, 'Kai <kai@client.example>', 'own1@acme.example', 'Later', 'A later note.', 0, 't-later'))
        self.judge(self.own, ('work-60', 'client', 'Kai wrote'))
        self.rounds()
        self.assertNotIn('A later note.', self.received(self.mem))

    def test_the_review_sorts_every_thread_again_once_hand_choices_stay(self):
        self.olive_mail()
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'work-4'), 'private')
            db.execute("DELETE FROM share_meta WHERE key='sorter'")
            sg.ensure(db)
            calls = dict(db.execute('SELECT event_id,coalesce(verdict,hand) FROM share_threads').fetchall())
        self.assertEqual(calls, {self.event_id(self.own, 'work-1'): None, self.event_id(self.own, 'work-3'): None, self.event_id(self.own, 'work-4'): 'internal'})  # a thread with a hand choice keeps its call
        with self.own.store.connect() as db:
            pending = sg.unjudged(db, self.own.scopes(db)[FLEET], 10)
        thread = next(x for x in pending if x['subject'] == 'Re: Renewal quote')
        self.assertEqual([x['text'] for x in thread['earlier']], [BODY])  # what an earlier message says counts too

    # -- what went wrong in a live Fleet: these are its cases, with made-up names
    def test_automated_billing_security_and_recruiting_mail_never_goes(self):
        def categorised(m, *labels):
            m['metadata']['labels'] = list(labels)
            return m
        self.add(self.own,
                 mail('work', 70, 'Tool Co <invoice+statements@pay.example>', 'own1@acme.example', 'Your receipt from Tool Co', 'Receipt 2543, paid by card.', 1, 't-receipt'),
                 mail('work', 71, 'Cloud <payments-noreply@cloud.example>', 'own1@acme.example', 'Invoices due soon', 'Two invoices are due.', 1, 't-due'),
                 categorised(mail('work', 72, 'AI Lab <team@mail.ailab.example>', 'own1@acme.example', 'Out of usage credits', 'Your organization is out of credits.', 1, 't-credits'), 'CATEGORY_UPDATES', 'INBOX'),
                 categorised(mail('work', 73, 'Ann Fox <ann@agency.example>', 'own1@acme.example', 'The part they leave out', 'A newsletter about success.', 1, 't-news'), 'CATEGORY_PROMOTIONS'),
                 mail('work', 74, 'Code Host <noreply@codehost.example>', 'own1@acme.example', 'A token was added', 'A new access token was added to your account.', 1, 't-token'),
                 mail('work', 75, 'Jo Hart <jo@recruit.example>', 'own1@acme.example', 'Interview opportunity', 'A role I think fits you, Olive.', 1, 't-recruit'),
                 categorised(mail('work', 76, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Billing question', 'Can we move to yearly billing?', 2, 't-bill'), 'CATEGORY_UPDATES'),
                 mail('work', 77, 'Olive <own1@acme.example>', 'lee@client.example', 'Re: Billing question', 'Yes, from next month.', 1, 't-bill'))
        # the review got some wrong; the rules hold anyway, and its own calls for security and recruiting say sensitive
        self.judge(self.own, ('work-70', 'client', 'A receipt'), ('work-71', 'client', 'Invoices'), ('work-72', 'client', 'Credits'),
                   ('work-73', 'client', 'A newsletter'), ('work-74', 'sensitive', 'A security alert'), ('work-75', 'sensitive', 'A recruiter wrote'),
                   ('work-76', 'client', 'Lee asked about yearly billing'))
        self.rounds()
        received = json.dumps(self.team(self.mem) + self.team(self.mem, 'team_mail'))
        for text in ('Receipt 2543', 'Two invoices', 'out of credits', 'newsletter about success', 'access token', 'A token was added',
                     'A security alert', 'role I think fits', 'Interview', 'A recruiter wrote', 'Jo'):
            self.assertNotIn(text, received)
        self.assertIn('yearly billing', received)  # a customer asking about their bill, and Olive answered: a client thread
        with self.own.store.connect() as db:
            scope = self.own.scopes(db)[FLEET]
            views = {s: sg.visibility(db, scope, dict(db.execute('SELECT * FROM events WHERE source_id=?', (s,)).fetchone()))
                     for s in ('work-70', 'work-71', 'work-72', 'work-73', 'work-74', 'work-76')}
            self.assertEqual(views, {'work-70': 'other', 'work-71': 'other', 'work-72': 'other', 'work-73': 'other', 'work-74': 'other', 'work-76': 'team'})
            self.assertEqual([x['subject'] for x in sg.unjudged(db, scope, 50) if x['subject'] in ('Your receipt from Tool Co', 'Out of usage credits')], [])
        self.assertGreaterEqual(self.own.graph_overview(FLEET)['sorted']['other'], 4)

    def test_the_review_is_told_billing_security_and_recruiting_are_never_client(self):
        for words in ('own bills', 'support tickets with the tools and suppliers', 'security', 'recruiting', 'never choose client'):
            self.assertIn(words, a.SHARE_VERDICTS)

    def test_the_review_calls_deals_sensitive_and_partner_listings_client_and_groups_the_rest(self):
        for words in ('possible buyer, acquirer or investor', 'board matters and investor updates', 'fundraising',  # sensitive, not unsure
                      'partner company, also one in the same market', 'listing or link exchange',  # business as usual: client
                      'group:', 'suggest:', '"people"', 'share_groups'):
            self.assertIn(words, a.SHARE_VERDICTS)
        prompt = a.share_history_prompt('r1', 2, ['Partner and listing exchanges'])
        self.assertIn('"group", "suggest"', prompt)
        self.assertIn('["Partner and listing exchanges"]', prompt)
        self.assertNotIn('share_groups (', a.share_history_prompt('r1', 2))

    def test_a_second_companys_mailbox_starts_off_and_its_owner_decides(self):
        self.olive_mail()
        self.side_company()
        # the domain decides, not the name: a mailbox named for this Fleet at another company's domain is another company's
        self.own.config['accounts'].append({'id': 'named', 'email': 'olive@othercorp.example', 'boundary': 'work:Acme', 'service': 'gmail'})
        self.own.config['accounts'].append({'id': 'code', 'email': 'olive-codes', 'boundary': 'work:Acme', 'service': 'github'})
        conns = {c['id']: c for c in self.own.sharing()[0]['connections']}
        self.assertEqual((conns['side']['work'], conns['side']['company'], conns['side']['on'], conns['side']['personal']), (False, False, False, False))  # never in the Fleet's briefs either
        self.assertEqual((conns['named']['company'], conns['named']['on']), (False, False))
        self.assertEqual((conns['code']['company'], conns['code']['on']), (True, True))  # no address: named for the Fleet
        self.assertEqual((conns['work']['company'], conns['work']['on']), (True, True))
        self.adm.graph_set_policy(FLEET, ['mail'])  # what the Fleet requires is its own company's mail, never another's
        self.rounds()
        conns = {c['id']: c for c in self.own.sharing()[0]['connections']}
        self.assertEqual((conns['side']['required'], conns['side']['on'], conns['side']['kind']), (False, False, 'mail'))
        self.assertEqual((conns['named']['required'], conns['named']['on']), (False, False))
        self.assertEqual(self.own.fleet_domains(FLEET), {'acme.example'})  # Olive's other addresses aren't the Fleet's
        self.assertIn(BODY, self.received(self.mem))
        self.assertNotIn('Sidecorp pilot', self.received(self.mem))
        self.own.graph_connection(FLEET, 'side', True)
        self.rounds()
        self.assertIn('Sidecorp pilot', self.received(self.mem))
        self.own.graph_connection(FLEET, 'side', False)  # taken back from the teammates' Machines
        self.rounds()
        self.assertNotIn('Sidecorp pilot', self.received(self.mem))
        self.assertIn(BODY, self.received(self.mem))

    def test_the_dashboards_read_writes_nothing_and_a_busy_database_is_no_error(self):
        """GET /api/fleet (shared_view -> sharing) while another writer holds the database (a graph build after a
        restart): what it keeps on the way is unchanged, so nothing is written and nothing waits on the lock."""
        self.adm.graph_set_policy(FLEET, ['mail'])
        self.rounds()
        before = self.own.sharing()
        def locked(key, value):
            raise sqlite3.OperationalError('database is locked')
        with patch.object(self.own, 'set_meta', side_effect=locked) as write:
            self.assertEqual(self.own.sharing(), before)
        self.assertEqual(write.call_count, 0)

    def test_a_gmail_account_without_a_service_is_work_email_the_fleet_can_require(self):
        for acc in self.own.config['accounts']:
            acc.pop('service', None)
        self.adm.graph_set_policy(FLEET, ['mail'])
        self.rounds()
        work = next(c for c in self.own.sharing()[0]['connections'] if c['id'] == 'work')
        self.assertEqual((work['kind'], work['service'], work['required'], work['on']), ('mail', 'gmail', True, True))

    def test_an_update_keeps_a_fleet_that_was_sharing_on_and_sorts_everything_again(self):
        """The version before shared without a Fleet switch, without per-connection choices and with an older sorting: a
        receipt, a second company's mailbox and a deal went as client. After the update the Fleet stays on, those are
        taken back at once or once sorted again, and a real client thread stays with the team throughout."""
        self.olive_mail()
        self.side_company()
        receipt = mail('work', 80, 'Tool Co <hello@toolco.example>', 'own1@acme.example', 'Your receipt', 'Receipt 99, paid.', 1, 't-r')
        receipt['metadata']['labels'] = ['CATEGORY_UPDATES', 'INBOX']  # an ordinary sender address, filed as an update by the mailbox
        self.add(self.own, receipt,
                 mail('work', 81, 'Max Rue <max@buyer.example>', 'own1@acme.example', 'Acquisition', 'Our offer to buy your company.', 1, 't-deal'))
        self.judge(self.own, ('work-80', 'client', 'A receipt'), ('work-81', 'client', 'Max wrote'))
        self.own.set_meta('graph_conn:' + FLEET, {'side': True})
        with patch.object(sg.Scope, 'automated', new_callable=unittest.mock.PropertyMock, return_value=set()):  # the old sorting
            self.rounds()
        for text in (BODY, 'Receipt 99', 'Sidecorp pilot', 'offer to buy'):
            self.assertIn(text, self.received(self.mem))
        # the update: no switch statement yet (the version before had none), no connection choices, every call sorted again
        self.net.trust = [t for t in self.net.trust if t['s'].get('t') != 'pause']
        for box in self.boxes:
            box.set_meta('graph_pause:' + FLEET, None)
        self.own.set_meta('graph_conn:' + FLEET, None)
        with self.own.store.connect() as db:
            db.execute("DELETE FROM share_meta WHERE key='sorter'")
            sg.ensure(db)
        group = self.mem.directory()['fleets'][0]
        self.assertIsNone(self.mem.graph_paused(group))  # a member's Machine that shared before: still on, before any admin says so
        self.rounds()
        self.assertIsNone(self.own.sharing()[0]['paused'])  # stays on, for everyone
        said = [t['s'] for t in self.net.trust if t['s'].get('t') == 'pause']
        self.assertEqual([(s['by'], s['on']) for s in said], [('own1', False)])  # signed once by an admin's Machine that was sharing
        received = self.received(self.mem)
        self.assertNotIn('Receipt 99', received)  # a rule says no: taken back at once
        self.assertNotIn('Sidecorp pilot', received)  # another company's mailbox: off unless its owner turns it on
        self.assertIn(BODY, received)  # waits to be sorted again: stays with the team meanwhile
        self.assertIn('offer to buy', received)
        waiting = self.own.graph_unjudged(1)
        self.assertEqual(len(waiting), 1)
        self.assertIn(waiting[0]['subject'], ('Re: Renewal quote', 'Acquisition'))  # what went before is sorted first
        tombstones = len([b for b in self.net.blobs.values() if b['header']['kind'] == 'mail'])
        self.judge(self.own, ('work-1', 'client', 'Lee asked for the renewal quote'), ('work-81', 'sensitive', 'Max wrote'))
        self.rounds()
        received = self.received(self.mem)
        self.assertIn(BODY, received)
        self.assertNotIn('offer to buy', received)  # sorted again as sensitive: taken back
        self.assertNotIn('Max wrote', json.dumps(self.team(self.mem)))
        self.assertTrue(self.own.sharing()[0]['started'])  # it shared before: no new hour to look it over
        self.assertLessEqual(len([b for b in self.net.blobs.values() if b['header']['kind'] == 'mail']) - tombstones, 1)  # no take back and send again

    def test_a_fleet_that_never_shared_stays_off_after_the_update(self):
        self.olive_mail()
        self.net.trust = [t for t in self.net.trust if t['s'].get('t') != 'pause']
        for box in self.boxes:
            box.set_meta('graph_pause:' + FLEET, None)
        self.rounds()
        self.assertEqual(self.own.sharing()[0]['paused'], {'default': True})
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        self.assertEqual([t for t in self.net.trust if t['s'].get('t') == 'pause'], [])

    # -- a board or a thread shared with chosen teammates, by name
    def test_a_board_shared_by_name_goes_only_to_them_sensitive_too_and_never_personal_automated_or_another_company(self):
        board = self.deal_board()
        self.rounds()
        self.assertNotIn(DEAL, self.received(self.mem))
        with self.assertRaises(ValueError):
            self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'someone'}])  # only confirmed teammates
        out = self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.assertEqual((out['visibility'], out['shared_with']), ('people', ['Mo']))
        self.rounds()
        self.assertIn(DEAL, self.received(self.mem))  # sensitive, and shared with Mo by name: it goes to Mo
        self.assertEqual(self.projects_of(self.mem)['Sale: Buyer']['board'], 'Acquisition conversations')
        self.assertIn(BODY, self.received(self.mem))  # and the rest of the team's Graph as before
        for text in ('Invoice 88', 'Family weekend', 'Sidecorp pilot', HEALTH, PERSONAL):
            self.assertNotIn(text, self.received(self.mem) + json.dumps(self.team(self.mem)))
        self.assertNotIn(DEAL, self.received(self.adm))  # Ada isn't on it
        self.assertNotIn('Sale: Buyer', self.projects_of(self.adm))
        self.assertIn(BODY, self.received(self.adm))
        blobs = self.only_blobs()
        self.assertTrue(blobs)
        self.assertEqual({tuple(b['header']['to']) for b in blobs}, {('mem3',)})  # sealed to Mo alone
        self.assertEqual({k for b in blobs for k in b.get('wraps') or {}}, {'mem3'})
        self.assertNotIn(DEAL, json.dumps(self.net.calls) + json.dumps(self.net.blobs))
        with self.own.store.connect() as db:
            self.assertEqual(graph.hidden_project_ids(db), {1})  # never the whole team's
        # Back to Only you: taken back from Mo's Machine, signed by Olive's
        self.own.graph_board_share(board, [])
        self.rounds()
        self.assertNotIn(DEAL, self.received(self.mem))
        self.assertNotIn('Sale: Buyer', self.projects_of(self.mem))
        self.assertIn(BODY, self.received(self.mem))
        with self.own.store.connect() as db:
            self.assertEqual(db.execute('SELECT visibility FROM boards WHERE id=?', (board,)).fetchone()[0], 'only_you')

    def test_threads_of_a_board_shared_by_name_are_sorted_first_and_then_go_only_to_them(self):
        board = self.deal_board()
        self.add(self.own,
                 mail('work', 24, 'Bo Hale <bo@buyer.example>', 'own1@acme.example', 'Closing date', 'We aim to close on June 3.', 1, 't-close'),
                 mail('work', 25, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Support question', 'How do I export a report?', 0, 't-support'))
        with self.own.store.connect() as db:
            graph.label(db, [self.event_id(self.own, 'work-24')], 'Sale: Buyer', 'review', a.now())
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        waiting = self.own.graph_unjudged(1)
        self.assertEqual([w['subject'] for w in waiting], ['Closing date'])  # the owner waits on it: before the rest
        self.assertIn('Support question', [w['subject'] for w in self.own.graph_unjudged()])
        self.judge(self.own, ('work-24', 'sensitive', 'Bo set a closing date'))
        self.assertNotIn('Closing date', [w['subject'] for w in self.own.graph_unjudged()])
        self.rounds()
        self.assertIn('close on June 3', self.received(self.mem))  # sorted: it goes to Mo
        self.assertNotIn('close on June 3', self.received(self.adm) + json.dumps(self.team(self.adm)))

    def test_another_company_or_a_personal_account_on_a_board_shared_by_name_stays_out(self):
        board = self.deal_board()
        self.add(self.own,
                 mail('side', 3, 'Pat Moss <pat@buyer.example>', 'olive@sidecorp.example', 'Side deal', 'Sidecorp side letter.', 1, 't-side-deal'),
                 mail('home', 24, 'Bo Hale <bo@buyer.example>', 'own1@home.example', 'From home', 'Home note on the sale.', 1, 't-home-deal'))
        with self.own.store.connect() as db:
            graph.label(db, [self.event_id(self.own, 'side-3'), self.event_id(self.own, 'home-24')], 'Sale: Buyer', 'review', a.now())
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        subjects = [w['subject'] for w in self.own.graph_unjudged()]
        self.assertNotIn('Side deal', subjects)  # never even queued to be sorted
        self.assertNotIn('From home', subjects)
        self.judge(self.own, ('side-3', 'client', 'Pat sent a side letter'), ('home-24', 'client', 'Bo wrote from home'))
        self.rounds()
        self.assertIn(DEAL, self.received(self.mem))
        for text in ('Sidecorp side letter', 'Home note on the sale', 'Sidecorp pilot'):
            for box in (self.mem, self.adm):
                self.assertNotIn(text, self.received(box) + json.dumps(self.team(box)))
        self.assertNotIn('Sidecorp side letter', json.dumps(self.net.calls) + json.dumps(self.net.blobs))

    def test_a_board_shared_by_name_takes_its_full_timeline_meetings_notes_and_intercom_only_to_them(self):
        board = self.deal_timeline()
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.rounds()
        received = self.received(self.mem)
        for text in ('walk through the data room', 'closing in June', 'test the API before closing'):
            self.assertIn(text, received)  # a meeting, its Zoom notes and an Intercom conversation: by being on the board
            self.assertNotIn(text, self.received(self.adm) + json.dumps(self.team(self.adm)))  # Ada isn't on it
        kinds = {json.loads(r['body'])['subject']: json.loads(r['body']).get('kind') for r in self.team(self.mem, 'team_mail')}
        self.assertEqual(kinds['Due diligence call'], 'meetings')
        self.assertEqual(kinds['Buyer question'], 'intercom')
        story = json.dumps(self.projects_of(self.mem)['Sale: Buyer']['timeline'])
        self.assertIn('Moved to Signed: Bo signed the letter of intent', story)
        self.assertIn('Meeting: Due diligence call', story)
        self.assertNotIn('Sidecorp board wants to wait', story)  # a move that came from another company's calendar stays
        blobs = self.only_blobs()
        self.assertEqual({tuple(b['header']['to']) for b in blobs}, {('mem3',)})  # sealed to Mo alone
        self.assertNotIn('closing in June', json.dumps(self.net.calls) + json.dumps(self.net.blobs))
        self.assertEqual(self.own.graph_unjudged(), [])  # nothing of it waits to be sorted

    def test_another_company_or_a_personal_item_on_a_shared_board_never_goes(self):
        board = self.deal_timeline()
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}, {'fleet': FLEET, 'member': 'adm2'}])
        self.rounds()
        self.assertIn('walk through the data room', self.received(self.adm))
        for box in (self.mem, self.adm):
            everything = self.received(box) + json.dumps(self.team(box))
            for text in ('Sidecorp board prep', 'Sidecorp board', 'Dinner at home', 'Dinner with Bo', 'Sidecorp pilot', 'Family weekend', 'Invoice 88'):
                self.assertNotIn(text, everything)
        subjects = [w['subject'] for w in self.own.graph_unjudged()]
        self.assertNotIn('Sidecorp board', subjects)
        self.assertNotIn('Dinner with Bo', subjects)

    def test_meetings_and_chats_of_a_team_board_go_once_judged_anything_but_sensitive_or_a_chat_among_colleagues(self):
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'cal', 'email': 'own1@acme.example', 'service': 'calendar', 'boundary': 'work:Acme'},
                                        {'id': 'li', 'service': 'linkedin', 'boundary': 'work:Acme'},
                                        {'id': 'zm', 'service': 'zoom', 'boundary': 'work:Acme'},
                                        {'id': 'homecal', 'email': 'own1@home.example', 'service': 'calendar', 'boundary': 'personal:Home'}]
        meet = lambda acct, n, title, body, who='lee@client.example': {
            'account_id': acct, 'source_id': f'{acct}-{n}', 'kind': 'calendar.event', 'occurred_at': ago(1), 'title': title, 'body': body, 'deleted': False,
            'metadata': {'organizer': {'email': 'own1@acme.example'}, 'attendees': [{'email': who}]}}
        zoom = lambda n, title, body: {'account_id': 'zm', 'source_id': f'zm-{n}', 'kind': 'zoom.summary', 'occurred_at': ago(1), 'title': title,
                                       'body': body, 'deleted': False, 'metadata': {'participants': [{'email': 'lee@client.example'}]}}
        chat = lambda n, conv, body: {'account_id': 'li', 'source_id': f'li-{n}', 'kind': 'linkedin.message', 'occurred_at': ago(1), 'title': 'LinkedIn conversation',
                                      'body': body, 'deleted': False, 'metadata': {'conversation_id': conv, 'chat_name': 'Lee Park', 'from_me': False}}
        self.add(self.own, meet('cal', 1, 'Renewal call', 'Walk Lee through the new plan.'), chat(1, 'c-lee', 'Lee: the renewal looks good.'),
                 meet('cal', 2, 'Lee check-in', 'Lee asked about the seats.'), meet('cal', 3, 'Unrelated call', 'Not on any board.'),
                 meet('cal', 4, 'Team sync', 'Only colleagues here.', 'adm2@acme.example'), chat(2, 'c-kept', 'Lee: a note to keep to me.'),
                 meet('cal', 5, 'Lee and family', 'Lee talked about his kids.'), meet('homecal', 1, 'Dinner with Lee', 'Dinner at home.'),
                 zoom(1, 'Renewal pricing', 'Lee agreed the new seat price.'), zoom(2, 'Lee health', 'Lee is off for surgery next month.'),
                 chat(3, 'c-form', 'Lee: send me the order form.'))
        self.board(self.own, 'Renewals', 'team', {'Renewal: Client': ['work-1', 'cal-1', 'li-1', 'cal-2', 'cal-4', 'li-2', 'cal-5', 'homecal-1', 'zm-1', 'zm-2',
                                                                      'li-3']})
        with self.own.store.connect() as db:
            sg.set_hand(db, self.event_id(self.own, 'li-2'), 'private')
        self.add(self.own, meet('cal', 6, 'Lee raise', 'Lee asked about a raise for his team.'))
        with self.own.store.connect() as db:
            graph.label(db, [self.event_id(self.own, 'cal-6')], 'Renewal: Client', 'review', a.now())
        self.judge(self.own, ('cal-2', 'unsure', 'Lee and seats'), ('cal-5', 'personal', 'Family talk'))
        waiting = [w['subject'] for w in self.own.graph_unjudged()]
        self.assertEqual(sorted(waiting[:3]), ['Lee raise', 'LinkedIn conversation', 'Renewal call'])  # the board's: sorted first
        self.assertNotIn('Unrelated call', waiting)  # a meeting on no board isn't sorted or shared, as before
        self.rounds()
        for box in (self.adm, self.mem):
            everything = self.received(box) + json.dumps(self.team(box))
            self.assertNotIn('Walk Lee through', everything)  # not judged yet: it waits, not even for a while
            self.assertNotIn('a raise for his team', everything)
            self.assertNotIn('new seat price', everything)  # a Zoom summary waits to be judged like mail
            self.assertIn('about the seats', everything)  # judged (unsure): on the board, so it goes
        self.judge(self.own, ('cal-1', 'other', 'Renewal call with Lee'), ('li-1', 'internal', 'Lee on the renewal'),
                   ('cal-6', 'sensitive', 'Lee and a raise'), ('zm-1', 'client', 'Lee agreed the price'), ('zm-2', 'sensitive', 'Lee and his health'),
                   ('li-3', 'unsure', 'Lee asks for the form'))
        self.assertEqual([w for w in self.own.graph_unjudged() if w['subject'] in ('Renewal call', 'Lee raise', 'LinkedIn conversation')], [])
        self.rounds()
        for box in (self.adm, self.mem):
            everything = self.received(box) + json.dumps(self.team(box))
            for text in ('Walk Lee through', 'about the seats', 'new seat price', 'the order form'):
                self.assertIn(text, everything)  # judged other or unsure: on the team's board, so it goes
            for text in ('renewal looks good', 'Not on any board', 'Only colleagues here', 'a note to keep to me', 'his kids', 'Dinner at home', 'a raise for his team', 'surgery'):
                self.assertNotIn(text, everything)  # a chat judged internal, no board, colleagues only, Keep private, personal, a personal account, sensitive
        self.assertIn('Meeting: Renewal call', json.dumps(self.projects_of(self.mem)['Renewal: Client']['timeline']))
        self.judge(self.own, ('li-3', 'internal', 'Lee asks for the form'))  # judged again: a chat among colleagues after all
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertNotIn('the order form', self.received(box))  # gone from the team's Machines again
            self.assertIn('Walk Lee through', self.received(box))

    def test_slack_among_colleagues_never_goes_whatever_the_review_said_and_slack_connect_can(self):
        """The company's own Slack (DMs, groups, channels among its members) is colleagues only: never a client thread,
        also on a team board and when the review called it client. Slack Connect, another company's member or a guest
        can be. What went before is taken back from teammates' Machines. Never a raw member id in what is shown or sent."""
        self.olive_mail()
        self.own.config['accounts'] += [{'id': 'sl', 'email': 'own1@acme.example', 'service': 'slack', 'boundary': 'work:Acme',
                                         'team_id': 'T0ACME0001', 'user_id': 'U0OLIVE001'}]
        with self.own.store.connect() as db:
            db.executemany('INSERT OR REPLACE INTO identity_names(identifier,name,email,checked_at) VALUES(?,?,?,?)',
                           [('slack:U0ADA00001', 'ada', 'adm2@acme.example', a.now()), ('slack:U0LEE00001', 'Lee Park', 'lee@client.example', a.now())])
            db.executemany('INSERT OR REPLACE INTO slack_members(user_id,outside,checked_at) VALUES(?,?,?)',
                           [('U0ADA00001', 0, a.now()), ('U0LEE00001', 1, a.now())])
        self.add(self.own, self.slack(1, 'D0ADA00001', 'DM U0ADA00001', 'U0ADA00001', 'Lee wants the renewal by Friday, can you call him?'),
                 self.slack(2, 'D0ADA00001', 'DM U0ADA00001', 'U0OLIVE001', 'Sure, I will ping <@U0LEE00001> after lunch'),
                 self.slack(3, 'C0SUPPORT1', 'support', 'U0ADA00001', 'Lee is asking about the renewal seats'),
                 self.slack(4, 'D0LEE00001', 'DM U0LEE00001', 'U0LEE00001', 'Lee here: the renewal seats look right'))
        self.board(self.own, 'Renewals', 'team', {'Renewal: Client': ['work-1', 'D0ADA00001:1.000100', 'D0ADA00001:2.000100', 'C0SUPPORT1:3.000100', 'D0LEE00001:4.000100']})
        for n in (1, 2, 3):
            self.judge(self.own, (f'D0ADA00001:{n}.000100' if n < 3 else 'C0SUPPORT1:3.000100', 'client', 'Ada and Lee on the renewal'))
        self.judge(self.own, ('D0LEE00001:4.000100', 'client', 'Lee confirmed the seats'))
        with self.own.store.connect() as db:
            scope = sg.Scope(db, ['work', 'sl'], {'acme.example'}, {'own1@acme.example'})
            views = {r['source_id']: sg.visibility(db, scope, {**dict(r), 'metadata': json.loads(r['metadata'])})
                     for r in db.execute("SELECT * FROM events WHERE kind='slack.message'")}
            shown = sg.overview(db, scope)
        self.assertEqual(views, {'D0ADA00001:1.000100': 'internal', 'D0ADA00001:2.000100': 'internal', 'C0SUPPORT1:3.000100': 'internal',
                                 'D0LEE00001:4.000100': 'team'})
        self.assertEqual(sg.why('internal'), 'Only colleagues: stays with the people on it')
        connect = self.slack(5, 'C0SHARED01', 'acme-client', 'U0ADA00001', 'In the shared channel', connect=True)['metadata']
        self.assertTrue(scope.slack_shared(connect))  # a Slack Connect channel: client checks as for mail
        self.assertFalse(scope.slack_shared({**connect, 'slack_connect': None}))
        listed = [x['title'] for x in shown['threads']]
        self.assertIn('#DM Lee Park: Lee here: the renewal seats look right', listed)
        self.assertFalse([t for t in listed if graph.SLACK_MEMBER.search(t)], listed)  # never a raw member id
        self.rounds()
        for box in (self.adm, self.mem):
            everything = self.received(box) + json.dumps(self.team(box))
            self.assertIn('the renewal seats look right', everything)  # Slack Connect, judged client: on the team's board
            self.assertIn('#DM Lee Park', everything)
            for text in ('can you call him', 'after lunch', 'asking about the renewal seats', 'U0ADA00001', 'U0LEE00001'):
                self.assertNotIn(text, everything)  # colleagues only, and no member ids
        with self.own.store.connect() as db:  # Lee turns out to be a member of the company's own Slack after all
            db.execute("UPDATE slack_members SET outside=0 WHERE user_id='U0LEE00001'")
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertNotIn('the renewal seats look right', self.received(box))  # taken back from teammates' Machines

    def test_a_project_added_to_a_shared_board_goes_and_one_moved_off_is_taken_back(self):
        board = self.deal_board()
        self.add(self.own, mail('work', 30, 'Cy Ross <cy@fund.example>', 'own1@acme.example', 'Term sheet', 'Our term sheet for the round.', 1, 't-fund'))
        self.judge(self.own, ('work-30', 'sensitive', 'Cy sent a term sheet'))
        with self.own.store.connect() as db:
            graph.label(db, [self.event_id(self.own, 'work-30')], 'Raise: Fund', 'review', a.now())
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.rounds()
        self.assertNotIn('term sheet for the round', self.received(self.mem))
        edit = {'board_id': board, 'name': 'Acquisition conversations', 'stages': ['Talks', 'Signed'], 'about': 'M&A', 'visibility': 'people'}
        with self.own.store.connect() as db:
            graph.save_board(db, {**edit, 'projects': ['Sale: Buyer', 'Raise: Fund']}, a.now())
        self.rounds()
        self.assertIn('term sheet for the round', self.received(self.mem))
        self.assertNotIn('term sheet for the round', self.received(self.adm))
        with self.own.store.connect() as db:
            graph.save_board(db, {**edit, 'projects': ['Sale: Buyer']}, a.now())
            self.assertEqual(db.execute('SELECT visibility FROM boards WHERE id=?', (board,)).fetchone()[0], 'people')
        self.rounds()
        self.assertNotIn('term sheet for the round', self.received(self.mem))  # moved off: taken back
        self.assertIn(DEAL, self.received(self.mem))

    def test_what_is_shared_by_name_is_never_passed_on_to_anyone_else(self):
        board = self.deal_board()
        self.own.graph_board_share(board, [{'fleet': FLEET, 'member': 'mem3'}])
        self.rounds()
        self.assertIn(DEAL, self.received(self.mem))
        # A Machine that passes it on anyway (an old version): the teammate's Machine refuses it
        with self.own.store.connect() as db:
            row = dict(db.execute("SELECT * FROM team_blobs WHERE kind='mail' AND header LIKE '%\"only\": true%'").fetchone())
        header = json.loads(row['header'])
        keys = self.own._public(next(g for g in self.own.directory()['fleets'] if g['id'] == FLEET), 'adm2')
        wrap = nc.seal({'dk': row['dk'], 'h': row['sha'], 'from_key': nc.public_keys(self.own._private())['sign']}, self.own._private(), keys,
                       sg.wrap_context(header, 'own1', 'adm2'))
        with self.assertRaisesRegex(ValueError, 'by name'):
            self.adm.graph_take({'header': header, 'ct': row['ct'], 'sig': row['sig'], 'wrap': wrap, 'by': 'own1'})
        # Someone new catches up on the team's Graph, never on what was shared with Mo
        self.net.people['mem4'] = ('Noor', 'member')
        noor = self.machine('mem4'); self.boxes.append(noor)
        self.rounds()
        self.ok(self.adm, 'member', 'Noor')
        self.rounds(4)
        self.assertIn(BODY, self.received(noor))
        self.assertNotIn(DEAL, self.received(noor))
        self.assertFalse([c for c in self.relays('mem4') if c[3]['blob']['header'].get('only')])
        # Mo away longer than the Network keeps: Olive's Machine passes on his own chain
        self.away(self.mem, 40)
        with self.mem.store.connect() as db:
            for table in ('team_mail', 'team_records', 'team_blobs', 'team_sources'):
                db.execute(sg.FLEET_DELETE[table], (FLEET,))
        self.mem.set_meta('graph_confirmed:' + FLEET, None)
        self.rounds(4)
        self.assertIn(DEAL, self.received(self.mem))
        self.assertIn('Sale: Buyer', self.projects_of(self.mem))

    def test_a_thread_shared_by_hand_with_chosen_teammates_never_a_personal_one(self):
        self.olive_mail()
        self.add(self.own, mail('work', 23, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Our kids', 'Family weekend plans.', 2, 't-kids'))
        self.judge(self.own, ('work-23', 'personal', 'Family'))
        self.rounds()
        self.assertNotIn(HEALTH, self.received(self.adm))
        out = self.own.graph_thread_share(self.event_id(self.own, 'work-3'), [{'fleet': FLEET, 'member': 'adm2'}])
        self.assertEqual(out['shared_with'], ['Ada'])
        self.assertEqual(out['label']['people'], ['Ada'])
        self.rounds()
        self.assertIn(HEALTH, self.received(self.adm))  # sensitive, shared by hand with Ada alone
        self.assertNotIn(HEALTH, self.received(self.mem))
        with self.assertRaisesRegex(ValueError, 'Personal'):
            self.own.graph_thread_share(self.event_id(self.own, 'work-23'), [{'fleet': FLEET, 'member': 'adm2'}])
        with self.assertRaises(ValueError):
            self.own.graph_thread_share(self.event_id(self.own, 'home-5'), [{'fleet': FLEET, 'member': 'adm2'}])
        self.own.graph_thread_share(self.event_id(self.own, 'work-3'), [])
        self.rounds()
        self.assertNotIn(HEALTH, self.received(self.adm))

    def test_only_the_share_sheet_shares_a_board_by_name(self):
        board = self.deal_board()
        with self.own.store.connect() as db:
            with self.assertRaises(ValueError):
                graph.clean_visibility('people')
            with self.assertRaises(ValueError):
                graph.save_board(db, {'board_id': board, 'name': 'Acquisition conversations', 'stages': ['Talks'], 'about': 'M&A', 'visibility': 'people'}, a.now())

    # -- whose it is: each Machine shares what its own owner took part in
    def test_a_teammates_mail_seen_through_the_crm_never_goes_from_this_machine(self):
        # Olive's mail with Lee, as Ada's Machine sees it in the shared CRM, and a meeting Olive logged there
        self.add(self.adm, self.crm('work', 1, 'Lee Park <lee@client.example>', 'Olive <own1@acme.example>', 'Rescheduling', BODY, 2, 'sf-1'),
                 self.crm('work', 2, 'Lee Park <lee@client.example>', '', 'Call with Lee', 'Notes: renewal', 1, None,
                          kind='salesflare.meeting', host='own1@acme.example'))
        self.judge(self.adm, ('crm-1', 'client', 'Olive and Lee agreed to reschedule'))
        self.rounds()
        for box in (self.own, self.mem):
            self.assertNotIn(BODY, json.dumps(self.team(box, 'team_mail')))
            self.assertNotIn('reschedule', json.dumps(self.team(box)))
            self.assertEqual([r for r in self.team(box) if r['member'] == 'adm2' and r['kind'] == 'person'], [])
        with self.adm.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM events')]
            self.assertEqual(self.adm.thread_labels(db, rows), {})  # no Team or Only you switch: not Ada's to share
            scope = next(iter(self.adm.scopes(db).values()))
            self.assertEqual(sg.unjudged(db, scope, 10), [])  # and nothing to sort for it

    def test_a_meeting_the_owner_logged_in_the_crm_is_their_own(self):
        with self.own.store.connect() as db:
            scope = next(iter(self.own.scopes(db).values()))
        own = {'host': 'own1@acme.example'}
        self.assertFalse(sg.secondhand('salesflare.meeting', own, scope.mine))
        self.assertTrue(sg.secondhand('salesflare.meeting', {'host': 'adm2@acme.example'}, scope.mine))
        self.assertTrue(sg.secondhand('salesflare.email', {'from': 'lee@client.example'}, scope.mine))
        self.assertFalse(sg.secondhand('gmail.message', {'from': 'lee@client.example'}, scope.mine))

    def test_the_owners_own_mail_never_comes_back_from_the_team(self):
        # Olive has her thread with Lee herself. A teammate's Machine from before (no CRM rule yet) sends its CRM copy.
        self.add(self.own, mail('work', 1, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Rescheduling', BODY, 2, 't-r'))
        self.add(self.adm, self.crm('work', 1, 'Lee Park <lee@client.example>', 'Olive <own1@acme.example>', 'Rescheduling', BODY, 2, 'sf-1'))
        self.judge(self.adm, ('crm-1', 'client', 'Olive and Lee agreed to reschedule'))
        with patch.object(sg, 'secondhand', return_value=False):
            self.rounds()
        self.assertIn(BODY, json.dumps(self.team(self.own, 'team_mail')))  # it reached Olive's Machine as Ada's
        with self.own.store.connect() as db:
            entry, section = self.own.team_for(db, 'email:lee@client.example')
        self.assertIsNotNone(entry)
        self.assertIsNone(section)  # but no "From the team, via Ada" with Olive's own mail, and no Ask Ada
        with self.mem.store.connect() as db:
            _, section = self.mem.team_for(db, next(e['key'] for e in self.mem.team_graph(db) if e['kind'] == 'person'))
        self.assertEqual(len(section['threads']), 1)  # Mo was not on it: he sees it

    def test_each_fact_shows_once(self):
        self.add(self.own, mail('work', 1, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Rescheduling', 'Can we move it?', 3, 't-r'),
                 mail('work', 2, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Rescheduling', 'November 25 works.', 2, 't-r'))
        self.judge(self.own, ('work-1', 'client', 'Olive and Lee agreed to reschedule'), ('work-2', 'client', 'Olive and Lee agreed to reschedule'))
        self.rounds()
        person = next(json.loads(r['body']) for r in self.team(self.mem) if r['kind'] == 'person')
        self.assertEqual([x['line'] for x in person['timeline']], ['Olive and Lee agreed to reschedule'])
        entry = {'sources': [{'fleet': FLEET, 'member': m, 'name': n, 'left': False,
                              'record': {'score': 1, 'timeline': [{'at': ago(1), 'line': 'Lee  signed.'}, {'at': ago(2), 'line': 'lee signed.'}]}}
                             for m, n in (('own1', 'Olive'), ('adm2', 'Ada'))]}
        with self.mem.store.connect() as db:
            section = self.mem.team_section(db, entry)
        self.assertEqual(len(section['timeline']), 1)  # the same fact from two teammates, once

    def test_one_email_two_teammates_had_is_one_line_in_the_viewers_language_via_both(self):
        # Lee wrote Olive and Ada in one email; each Machine wrote its own line about it, Ada's in Dutch
        same = lambda box, account, to: {**mail(account, 7, 'Lee Park <lee@client.example>', to, 'Recovery', BODY, 1, 't-' + box),
                                         'metadata': {'from': 'Lee Park <lee@client.example>', 'to': to, 'labels': ['INBOX'],
                                                      'message-id': '<recovery-7@client.example>', 'thread_id': 't-' + box}}
        self.add(self.own, same('own', 'work', 'own1@acme.example, adm2@acme.example'))
        self.add(self.adm, same('adm', 'work', 'own1@acme.example, adm2@acme.example'))
        self.judge(self.own, ('work-7', 'client', 'Olive closed Lee\'s account recovery request'))
        self.judge(self.adm, ('work-7', 'client', 'Lee kreeg antwoord'))
        with patch.object(sg.shared_graph_lines.locale_prefs, 'language', side_effect=lambda: 'nl' if self.publishing == 'adm2' else 'en'):
            for _ in range(2):
                for box in self.boxes:
                    self.publishing = box.member_id
                    box.directory(refresh=True)
                    box.shared_round()
                    box.graph_round(force=True)
        sent = {r['member']: json.loads(r['body'])['timeline'] for r in self.team(self.mem) if json.loads(r['body'])['t'] == 'person'}
        self.assertEqual({m: [x['lang'] for x in t] for m, t in sent.items()}, {'own1': ['en'], 'adm2': ['nl']})
        self.assertEqual(sent['own1'][0]['k'], sent['adm2'][0]['k'])  # one message, one Fleet-keyed hash, no message id itself
        self.assertNotIn('recovery-7', json.dumps(sent))
        with self.mem.store.connect() as db:
            entry = next(e for e in self.mem.team_graph(db) if e['kind'] == 'person')
            self.assertEqual(len(entry['sources']), 2)
            # the thread itself shows as one of each teammate's; its lines are what the Timeline has when it doesn't
            entry = {**entry, 'sources': [{**s, 'record': {**s['record'], 'threads': []}} for s in entry['sources']]}
            with patch.object(sg.shared_graph_lines.locale_prefs, 'language', return_value='en'):
                section = self.mem.team_section(db, entry)
        self.assertEqual([(x['line'], sorted(x['via'])) for x in section['timeline']], [("Olive closed Lee's account recovery request", ['Ada', 'Olive'])])

    def test_a_line_about_a_thread_the_timeline_shows_is_left_to_the_thread_which_has_its_newest_message_start(self):
        self.add(self.own, mail('work', 1, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Rescheduling', 'Can we move it?', 3, 't-r'),
                 mail('work', 2, '"Lee Park" <lee@client.example>', 'own1@acme.example', 'Re: Rescheduling', 'November 25\n\n  works.', 2, 't-r'))
        self.judge(self.own, ('work-1', 'client', 'Olive and Lee agreed to reschedule'), ('work-2', 'client', 'Olive and Lee agreed to reschedule'))
        self.rounds()
        person = next(json.loads(r['body']) for r in self.team(self.mem) if r['kind'] == 'person')
        self.assertEqual(person['timeline'][0]['tag'], person['threads'][0])  # the line says which shared thread it is about
        with self.mem.store.connect() as db:
            entry = next(e for e in self.mem.team_graph(db) if e['kind'] == 'person')
            section = self.mem.team_section(db, entry)
            self.assertEqual(section['timeline'], [])  # the thread shows; its line doesn't, too
            self.assertEqual((section['threads'][0]['from'], section['threads'][0]['preview']), ('Lee Park', 'November 25 works.'))
            # A line from a Machine from before (no thread on it) about a thread shown: its subject still tells
            old = {**entry, 'sources': [{**src, 'record': {**src['record'], 'timeline': [{'at': ago(2), 'line': 'Email: Re: Rescheduling'},
                                                                                            {'at': ago(1), 'line': 'Lee signed.'}]}} for src in entry['sources']]}
            self.assertEqual([x['line'] for x in self.mem.team_section(db, old)['timeline']], ['Lee signed'])

    # -- team learnings from team conversations (fleet_learnings.py), and asks answered from what the Team Graph shares
    def test_team_learnings_read_only_shared_client_threads_keep_only_general_ones_and_reach_teammates(self):
        self.learn_mail()
        evidence, names = self.learn_evidence(self.own)
        seen = json.dumps(evidence)
        self.assertEqual(len(evidence['threads']), 4)  # the four client threads; the personal one is never read
        for text in ('graduation', 'Springfield', 'Kai', 'pal.example', 'Lee Park', 'Ana', 'lee@client.example', 'client.example', '44710'):
            self.assertNotIn(text, seen)
        self.assertEqual(len(set(evidence['companies'].values())), 4)  # which company: only as a hash, for the check
        kept = self.learn_run(self.own, evidence, names, [
            self.REFUNDS,
            {'kind': 'product_feedback', 'text': 'Customers find the invoice screen confusing and want it simpler.', 'confidence': 0.95, 'threads': [1, 2]},
            {'kind': 'customer_specific', 'text': 'This customer always wants a refund in their own currency.', 'confidence': 0.9, 'threads': [1, 2]},
            {'kind': 'style', 'text': 'Replies thank the customer for asking before anything else.', 'confidence': 0.9, 'threads': [1]},  # one company
            {'kind': 'routing', 'text': 'Lee Park handles every refund request from the support inbox.', 'confidence': 0.9, 'threads': [1, 2]},
            {'kind': 'tool', 'text': 'Refund requests are tracked in a shared spreadsheet every week.', 'confidence': 0.5, 'threads': [1, 2]}])
        self.assertEqual([(k['kind'], k['text'], k['source']) for k in kept], [('process', self.REFUNDS['text'], 'team_conversations')])
        self.assertTrue(any(l['kind'] == 'learning' and l['outcome'] == 'shared with the team, from team conversations' for l in self.own.view()['log']))
        self.rounds()
        for box in (self.adm, self.mem):
            items = box.learnings_view(FLEET)['items']
            self.assertEqual([(i['kind'], i['text'], i['from'], i['mine']) for i in items], [('process', self.REFUNDS['text'], 'Olive', False)])
            self.assertTrue(any(l['kind'] == 'learning' and l['direction'] == 'in' for l in box.view()['log']))
        self.assertNotIn('refund template', json.dumps(self.net.calls) + json.dumps(self.net.blobs))  # sealed like the rest
        # the threads it read are read: the next pass doesn't see them again
        with self.own.connect() as db:
            db.execute("UPDATE profile_runs SET started_at=? WHERE kind='fleet_learn'", (ago(2),))
        self.assertIsNone(self.learn_evidence(self.own)[0])

    def test_a_teammate_removes_a_team_learning_for_everyone_and_it_stays_removed(self):
        self.learn_mail()
        evidence, names = self.learn_evidence(self.own)
        self.learn_run(self.own, evidence, names, [self.REFUNDS])
        self.rounds()
        fp = self.adm.learnings_view(FLEET)['items'][0]['fp']
        self.adm.remove_learning(FLEET, fp)
        self.rounds(3)
        for box in self.boxes:
            self.assertEqual(box.learnings_view(FLEET)['items'], [], box.member_id)
        self.assertTrue(any(l['outcome'] == 'removed for the team' for l in self.own.view()['log']))
        # never made again, also not worded a little differently
        again = dict(self.REFUNDS, text='Refund requests are answered from the support inbox using the refund template.')
        self.assertEqual(self.learn_run(self.own, evidence, names, [again]), [])
        with self.assertRaises(ValueError):
            self.adm.remove_learning(FLEET, 'f' * 32)

    def test_the_learnings_switch_turns_team_learnings_off_and_takes_back_what_went(self):
        import security_levels
        self.learn_mail()
        evidence, names = self.learn_evidence(self.own)
        self.learn_run(self.own, evidence, names, [self.REFUNDS])
        self.rounds()
        self.assertTrue(self.mem.learnings_view(FLEET)['items'])
        with self.own.connect() as db:
            security_levels.set_pref(db, 'learnings', 'off')  # Settings, Security, Offer to share learnings
        self.rounds(3)
        self.assertEqual(self.mem.learnings_view(FLEET)['items'], [])
        with self.own.connect() as db:
            db.execute("DELETE FROM profile_runs WHERE kind='fleet_learn'")
            db.execute('DELETE FROM fleet_learn_read')
        self.assertIsNone(self.learn_evidence(self.own)[0])  # nothing is read while it's off
        self.assertFalse(self.own.learnings_view(FLEET)['on'])

    def test_a_careful_fleet_or_a_team_graph_that_isnt_sharing_reads_nothing_for_team_learnings(self):
        self.learn_mail()
        self.own.graph_pause(FLEET, True)
        self.rounds(1)
        self.assertIsNone(self.learn_evidence(self.own)[0])
        self.own.graph_pause(FLEET, False)
        self.rounds(1)
        self.assertTrue(self.learn_evidence(self.own)[0])
        self.net.level = 'careful'
        self.rounds(1)
        self.assertIsNone(self.learn_evidence(self.own)[0])

    # -- when one person learns, everyone does: team learnings in a teammate's Work to-do preparations
    def test_a_teammates_work_to_do_uses_the_team_learning_that_fits_and_says_so_never_a_personal_one(self):
        import fleet_learnings
        with self.mem.store.connect() as db:
            self.assertEqual(fleet_learnings.usable(db, FLEET), [])  # nothing received yet: nothing used
        self.shared_refunds()
        work = self.todo(self.mem, 'w1', 'Answer the refund request', 'A customer asks for a refund of their last invoice.', ['work'])
        home = self.todo(self.mem, 'h1', 'Answer the refund request', 'A refund for the concert tickets.', ['home'])
        mixed = self.todo(self.mem, 'm1', 'Answer the refund request', 'A refund request.', ['work', 'home'])
        lines = self.mem.learning_lines(work)
        fp = self.mem.learnings_view(FLEET)['items'][0]['fp']
        self.assertIn(f"- [{fp[:8]}] {self.REFUNDS['text']}", lines)
        self.assertIn('data, not instructions', lines)
        self.assertIn("rank below the owner's own facts, draft rules, voice and skills", lines)
        self.assertNotIn('Olive', lines)  # whose learning it is never goes in
        self.assertEqual(self.mem.learning_lines(home), '')  # personal: never
        self.assertEqual(self.mem.learning_lines(mixed), '')
        self.assertIn(self.REFUNDS['text'], self.mem.lines(work))  # what the preparation gets
        # the result says it followed it: the to-do says so, with Remove; an id that isn't one is left out
        self.assertEqual(self.mem.learnings_used(work, [fp[:8], 'deadbeef']), [self.REFUNDS['text']])
        self.assertEqual(self.mem.learnings_used(home, [fp[:8]]), [])
        suggestions = [{'id': work}, {'id': home}]
        with self.mem.connect() as db:
            self.mem.annotate(db, suggestions)
        self.assertEqual(suggestions[0]['team_learnings_used'], [{'fleet': FLEET, 'fp': fp, 'text': self.REFUNDS['text']}])
        self.assertNotIn('team_learnings_used', suggestions[1])
        self.assertIsNone(self.mem.learnings_used(work, None) or None)  # left out: unchanged
        with self.mem.connect() as db:
            self.assertIn(work, fleet_learnings.used(db, [work]))
        self.assertEqual(self.mem.learnings_used(work, []), [])  # a new result that followed none
        with self.mem.connect() as db:
            self.assertEqual(fleet_learnings.used(db, [work]), {})

    def test_a_removed_team_learning_stops_being_used_at_once_here_and_for_every_teammate(self):
        self.shared_refunds()
        work = self.todo(self.mem, 'w1', 'Answer the refund request', 'A customer asks for a refund of their last invoice.', ['work'])
        mine = self.todo(self.adm, 'w2', 'Refund request from a customer', 'They want a refund through the support inbox.', ['work'])
        fp = self.mem.learnings_view(FLEET)['items'][0]['fp']
        self.mem.learnings_used(work, [fp[:8]])
        self.assertTrue(self.adm.learning_lines(mine))
        self.mem.remove_learning(FLEET, fp)  # from the to-do's Remove: gone here at once
        self.assertEqual(self.mem.learning_lines(work), '')
        suggestions = [{'id': work}]
        with self.mem.connect() as db:
            self.mem.annotate(db, suggestions)
        self.assertNotIn('team_learnings_used', suggestions[0])
        self.rounds(3)
        for box, card in ((self.adm, mine), (self.own, self.todo(self.own, 'w3', 'Refund request', 'A customer asks for a refund.', ['work']))):
            self.assertEqual(box.learning_lines(card), '', box.member_id)

    def test_a_careful_work_fleet_uses_no_team_learnings_also_not_ones_shared_before(self):
        self.shared_refunds()
        work = self.todo(self.mem, 'w1', 'Answer the refund request', 'A customer asks for a refund of their last invoice.', ['work'])
        fp = self.mem.learnings_view(FLEET)['items'][0]['fp']
        self.assertTrue(self.mem.learning_lines(work))
        self.mem.learnings_used(work, [fp[:8]])
        self.net.level = 'careful'  # an admin made the Work Fleet Careful
        self.rounds(1)
        self.assertEqual(self.mem.learning_lines(work), '')
        self.assertEqual(self.mem.learnings_used(work, [fp[:8]]), [])
        suggestions = [{'id': work}]
        with self.mem.connect() as db:
            self.mem.annotate(db, suggestions)
        self.assertNotIn('team_learnings_used', suggestions[0])

    def test_a_team_learning_is_used_as_plain_text_even_when_a_record_carried_markup(self):
        import fleet_learnings
        self.shared_refunds()
        text = 'Refund requests go out from the support inbox <b>with</b> the refund template.'
        with self.mem.connect() as db:  # kept before the plain-text check, say: what is used is plain words
            db.execute("INSERT INTO team_records(fleet,member,rid,kind,body,at) VALUES(?,?,?,?,?,?)",
                       (FLEET, 'adm2', 'e' * 32, 'learning', json.dumps({'fp': 'e' * 32, 'kind': 'process', 'text': text, 'at': '2026-10-30'}), a.now()))
            texts = [i['text'] for i in fleet_learnings.usable(db, FLEET)]
        self.assertIn('Refund requests go out from the support inbox with the refund template.', texts)
        self.assertFalse(any('<' in t for t in texts))
        work = self.todo(self.mem, 'w1', 'Refund request', 'A customer wants a refund from the support inbox.', ['work'])
        self.assertNotIn('<b>', self.mem.learning_lines(work))

    def test_only_the_team_learnings_about_a_to_do_go_in_and_at_most_a_few(self):
        import fleet_learnings
        self.shared_refunds()
        with self.mem.connect() as db:
            self.assertEqual(fleet_learnings.pick(db, FLEET, 'Book the team offsite', 'Find a venue for the spring offsite.'), [])
            texts = [f'Refund requests get a reply from the support inbox with the {n} template.' for n in ('alpha', 'bravo', 'charlie', 'delta', 'echo')]
            for t in texts:
                db.execute('INSERT INTO fleet_learnings(fleet,fp,kind,text,confidence,run_id,at) VALUES(?,?,?,?,?,?,?)',
                           (FLEET, fleet_learnings.fingerprint(t), 'process', t, 0.9, 'r', a.now()))
            self.assertEqual(len(fleet_learnings.pick(db, FLEET, 'Refund request', 'A customer wants a refund via the support inbox.')), fleet_learnings.USE_TOP)
            # by meaning when embeddings are on: closest first, none under the floor
            near = lambda text: [1.0, 0.0] if 'refund' in text.lower() and 'alpha' in text.lower() or text.startswith('title: Refund') else [0.0, 1.0]
            with patch('embeddings.embed', side_effect=lambda settings, texts, timeout=15: [near(x) for x in texts]):
                picked = fleet_learnings.pick(db, FLEET, 'Refund request', 'A refund.', {'model': 'm', 'url': 'http://x'})
            self.assertEqual([p['text'] for p in picked], [texts[0]])
            with patch('embeddings.embed', side_effect=OSError('away')):  # the server is away: shared words instead
                self.assertTrue(fleet_learnings.pick(db, FLEET, 'Refund request', 'A customer wants a refund via the support inbox.', {'model': 'm', 'url': 'http://x'}))

    def test_who_knows_someone_is_answered_by_itself_from_what_the_team_graph_shares_never_a_personal_thread(self):
        self.learn_mail()
        status, answer = self.teammate_asks(self.own, 'client.example', 'q1')
        self.assertEqual(status, 'answered')
        self.assertTrue(answer['knows'])
        status, answer = self.teammate_asks(self.own, 'pal.example', 'q2')  # the personal thread, in the same work account
        self.assertEqual(status, 'answered')
        self.assertFalse(answer['knows'])
        self.assertNotIn('Kai', self.sealed)
        self.assertTrue(any(l['outcome'].startswith('answered with what the Team Graph shares') for l in self.own.view()['log']))
        with self.own.connect() as db:  # a stored Ask me first reads as Always in a Standard Work Fleet; Never holds
            self.own.set_rule(FLEET, fleet.ALL, 'relationships', 'never')
            self.assertEqual(self.own.rule(db, FLEET, 'adm2', 'relationships')[0], 'never')
            db.execute("UPDATE fleet_rules SET rule='ask' WHERE kind='relationships'")
        with self.own.connect() as db:
            self.assertEqual(self.own.rule(db, FLEET, 'adm2', 'relationships')[0], 'always')
        self.net.level = 'careful'  # a Careful Work Fleet keeps asking
        self.rounds(1)
        self.assertEqual(self.teammate_asks(self.own, 'client.example', 'q3')[0], 'waiting')

    def test_while_the_team_graph_isnt_sharing_asks_keep_their_own_rules(self):
        self.learn_mail()
        self.own.graph_pause(FLEET, True)
        self.rounds(1)
        with self.own.connect() as db:
            self.assertEqual(self.own.rule(db, FLEET, 'adm2', 'relationships')[0], 'ask')
        self.assertEqual(self.teammate_asks(self.own, 'client.example', 'q1')[0], 'waiting')

for _name in dir(base.SharedGraph):
    if _name.startswith('test_'):
        setattr(SharedGraphMore, _name, None)  # the first half: test_shared_graph.py runs it


class SealedMore(SharedGraphMore):
    """The rules that read the messages themselves, on a store with message protection on (test_shared_graph.Sealed)."""
    PROTECT = True


for _name in dir(SharedGraphMore):
    if _name.startswith('test_') and _name not in (
            'test_someone_taken_out_gets_nothing_new_even_if_the_network_keeps_them_in',
            'test_someone_taken_out_loses_what_the_team_shared_with_them_and_only_that',
            'test_someone_taken_out_while_their_machine_is_away_loses_it_when_it_is_back', 'test_someone_taken_out_loses_it_as_soon_as_the_network_rings_their_machine'):
        setattr(SealedMore, _name, None)


if __name__ == '__main__':
    unittest.main()
