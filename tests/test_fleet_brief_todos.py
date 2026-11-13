"""The team brief's lines as to-dos (fleet_brief_todos.py): a told brief's line is a Work to-do in For you, or joins the
owner's open to-do about that company; Ask and Not needed on the to-do, and the old API (fleet_brief_hide, the Fleet's
free question), settle it; a line the next brief no longer has settles by itself; Details shows only what the Team
Graph shares. Made-up companies and people; a fake relay; nothing is sent anywhere."""
import datetime as dt
import json
import unittest

from test_fleet import NOW, TEAM, fleet, mail  # noqa: I001 - first: it puts the repository on the path
import fleet_brief
import fleet_brief_todos
import test_fleet_brief as brief_fixture

YESTERDAY = (NOW - dt.timedelta(days=1)).date().isoformat()
GLOBEX = {'org': 'Globex', 'domain': 'globex.example', 'key': 'd' * 64, 'at': YESTERDAY}  # Pat got it; the owner talks to Globex too
GONE = {'org': 'Gone', 'domain': 'gone.example', 'last': '2026-08-02', 'known': 'customer'}
PAT = {'unanswered': [GLOBEX], 'quiet': [GONE]}


class BriefTodos(unittest.TestCase):
    facts = brief_fixture.Brief.facts

    def setUp(self):  # the brief's own fixture (test_fleet_brief.py), then the app's hooks (machine/app/fleet.py)
        brief_fixture.Brief.setUp(self)
        self.fleet.brief_card = fleet_brief_todos.card_maker(self.store)
        self.fleet.done_card = lambda card, choice, why, key: self.store.decide(card, choice, why, key, 'fleet')
        with self.store.connect() as db:  # what is at stake with Globex in the owner's Graph: its renewal, on a board
            db.execute("INSERT OR IGNORE INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('org:globex.example','org','Globex',0.5,1,?)",
                       (json.dumps({'domain': 'globex.example'}),))
            db.execute("INSERT INTO boards(id,name,stages,source,created_at) VALUES(9,'Renewals','[\"Proposal\",\"Signed\"]','owner',?)", (NOW.isoformat(),))
            db.execute("INSERT INTO projects(id,name,created_at,org,board_id,stage) VALUES(90,'Globex renewal',?,'globex.example',9,'Proposal')", (NOW.isoformat(),))

    def day(self, days_ago):
        return fleet_brief._on_day((NOW - dt.timedelta(days=days_ago)).date().isoformat(), NOW.date())

    def gone_title(self):
        days = (NOW.date() - dt.date.fromisoformat(GONE['last'])).days
        return f'Gone has been quiet for {days // 7} weeks' if days < 60 else f'Gone has been quiet for {days // 30} months'

    def tell(self, pat, day=1, quiet=False):
        """A brief told for the work Fleet, from the owner's facts and Pat's answer, then its lines into To-dos."""
        view = fleet.assemble_brief(self.facts(), [('Pat', fleet.clean_brief(pat))])
        period = (NOW - dt.timedelta(days=day)).date().isoformat()
        view.update(period=period, every='day', since=period, fleet='work')
        at = (NOW - dt.timedelta(days=day)).isoformat(timespec='seconds')
        with self.store.connect() as db:
            db.execute('INSERT OR REPLACE INTO fleet_briefs(fleet,period,every,view,answers,built_at,told_at) VALUES(?,?,?,?,1,?,?)',
                       ('work', period, 'day', json.dumps(view), at, at))
        return self.fleet.brief_todos_sync('work', force=True, quiet=quiet)

    def lines(self):
        return (self.fleet.meta(fleet_brief_todos.META) or {}).get('work', {})

    def card_of(self, key):
        return self.lines()[key]['card']

    def card(self, card_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (card_id,)).fetchone())

    def brief_cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'fleet-brief:%' ORDER BY created_at")]

    def shown(self, card_id):
        rows = [self.card(card_id)]
        with self.store.connect() as db:
            self.fleet.annotate_brief(db, rows)
        return rows[0].get('fleet_brief')

    def brief_keys(self):
        return [i['key'] for i in self.fleet.briefs()['work']['items']]

    def test_a_line_is_a_work_todo_and_one_about_a_company_with_an_open_todo_joins_it(self):
        self.assertEqual(self.tell(PAT), 2)
        cards = {c['title']: c for c in self.brief_cards()}
        waiting = f'Globex has been waiting on Pat since {self.day(1)}'
        self.assertEqual(set(cards), {waiting, self.gone_title()})
        globex, gone = cards[waiting], cards[self.gone_title()]
        self.assertEqual((globex['status'], json.loads(globex['account_ids'])), ('pending', ['work']))  # Work, For you
        # who has it, what's at stake in the owner's Graph, and plainly that what they wrote is only in Pat's mail
        self.assertEqual(globex['body'], 'What they wrote isn’t shared with you. Ask Pat. At stake: renewal (Proposal). You also talk to them.')
        self.assertEqual(gone['body'], 'Last contact Aug 2. A customer.')  # why it matters: a customer, when
        self.assertNotIn('—', globex['body'] + gone['body'])
        # from the Fleet ("From your Fleet" on the dashboard), never "signal from", which reads as a Signal chat
        self.assertRegex(globex['source_line'], r'^Source: your Fleet · \w{3}, \w{3} \d{1,2}$')
        # Customer Co's waiting email already has the owner's to-do (s3, from the review): the line joins it, no second one
        lines = self.lines()
        self.assertEqual((lines['unanswered:customer.example']['card'], lines['unanswered:customer.example']['merged']), ('s3', True))
        joined = self.shown('s3')
        self.assertFalse(joined['own'])
        self.assertEqual([i['title'] for i in joined['items']], [f'Customer Co has been waiting on you since {self.day(3)}'])
        own = self.shown(globex['id'])
        self.assertTrue(own['own'])
        line = own['items'][0]
        self.assertEqual((line['kind'], line['org']['name'], line['ask']), ('waiting', 'Globex', 'Is anyone answering the email Globex sent to Pat?'))
        self.assertEqual([p['name'] for p in line['team']], ['Pat'])
        # the next round with the same brief: nothing new
        self.assertEqual(self.tell(PAT), 0)
        self.assertEqual(len(self.brief_cards()), 2)

    def deliveries(self):
        with self.store.connect() as db:
            return {r['title']: r['status'] for r in db.execute(
                "SELECT s.title,d.status FROM suggestions s JOIN deliveries d ON d.suggestion_id=s.id WHERE s.dedupe_key LIKE 'fleet-brief:%'")}

    def test_the_summary_is_the_one_ping_its_todos_come_in_silently(self):
        self.tell(PAT, quiet=True)  # the brief told with its own summary, which links to To-dos
        self.assertEqual(self.deliveries(), {f'Globex has been waiting on Pat since {self.day(1)}': 'not_sent', self.gone_title(): 'not_sent'})

    def test_without_the_summary_ping_its_todos_arrive_like_any_other(self):
        self.tell(PAT)
        self.assertEqual(set(self.deliveries().values()), {'queued'})

    def test_a_quiet_line_says_the_usual_rhythm_when_there_is_one(self):
        events = [mail('work', days, 'Lou <lou@gone.example>', 'owner@acme.example', message_id=f'<g{days}@gone.example>') for days in (101, 115, 129, 143)]
        for e in events:
            self.store.commit_page('work', {}, [e])
        self.tell({'quiet': [GONE]})
        self.assertEqual(self.card(self.card_of('quiet:gone.example'))['body'], 'Last contact Aug 2. A customer. Usually every two weeks.')
        self.assertEqual(fleet_brief_todos.rhythm_words(7), 'usually weekly')
        self.assertEqual(fleet_brief_todos.rhythm_words(1), '')

    def test_not_needed_on_the_todo_hides_the_line_and_only_something_new_brings_it_back(self):
        first = {**GLOBEX, 'at': (NOW - dt.timedelta(days=3)).date().isoformat()}
        self.tell({**PAT, 'unanswered': [first]})
        card = self.card_of('unanswered:globex.example')
        done = self.fleet.brief_todo_skip(card)
        self.assertEqual(done, {'skipped': ['unanswered:globex.example'], 'close': True})
        self.store.decide(card, 'reject', 'Not needed', 'skip-1', 'dashboard')  # as the app's fleet_brief_todo does
        self.assertNotIn('unanswered:globex.example', self.brief_keys())
        self.assertEqual(self.card(card)['status'], 'rejected')
        self.assertEqual(self.tell({**PAT, 'unanswered': [first]}), 0)  # the same brief again: it stays closed
        # Globex writes again: a new first email is a new line
        self.assertEqual(self.tell({'unanswered': [{**GLOBEX, 'key': 'f' * 64}]}, day=0), 1)
        self.assertNotEqual(self.card_of('unanswered:globex.example'), card)
        # Not needed on a to-do a line only joined: the line goes, the owner's to-do is theirs to close
        self.assertEqual(self.fleet.brief_todo_skip('s3')['close'], False)
        self.assertEqual(self.card('s3')['status'], 'pending')
        with self.assertRaises(ValueError):
            self.fleet.brief_todo_skip(card)

    def test_not_needed_on_the_old_api_closes_the_todo(self):
        self.tell(PAT)
        card = self.card_of('quiet:gone.example')
        self.fleet.hide_brief_item('work', 'quiet:gone.example')  # fleet_brief_hide
        self.assertEqual(self.card(card)['status'], 'rejected')
        self.assertTrue(self.lines()['quiet:gone.example']['closed'])
        self.assertNotIn('quiet:gone.example', self.brief_keys())

    def test_closing_the_todo_the_usual_way_settles_the_line(self):
        self.tell(PAT)
        card = self.card_of('quiet:gone.example')
        self.store.decide(card, 'reject', 'Not needed', 'reject-1', 'dashboard')
        self.fleet.brief_todo_closed(card, 'reject')  # card_actions.decide_action
        self.assertNotIn('quiet:gone.example', self.brief_keys())
        globex = self.card_of('unanswered:globex.example')
        self.store.decide(globex, 'complete', '', 'done-1', 'dashboard')
        self.fleet.brief_todo_closed(globex, 'complete')
        self.assertTrue(self.lines()['unanswered:globex.example']['closed'])
        self.assertIn('unanswered:globex.example', self.brief_keys())  # done isn't Not needed: nothing learned
        self.assertEqual(self.tell(PAT), 0)

    def test_ask_on_the_todo_and_the_same_question_on_the_old_api_show_their_answers_on_it(self):
        self.tell(PAT)
        globex = self.card_of('unanswered:globex.example')
        self.fleet.brief_todo_ask(globex, 'Who is answering Globex this week?')
        ask = self.relay.sent('/ask')[-1]
        self.assertEqual((ask['kind'], ask['question']['text']), ('anything', 'Who is answering Globex this week?'))
        asked = self.shown(globex)['asked']
        self.assertEqual((asked['question'], [a['state'] for a in asked['answers']]), ('Who is answering Globex this week?', ['waiting']))
        self.assertEqual(self.card(globex)['status'], 'pending')  # still the owner's until done or Not needed
        with self.assertRaises(ValueError):
            self.fleet.brief_todo_ask(globex, 'Hi')
        # the old API: the Fleet tab's free question with a line's own Ask text lands on that line's to-do
        gone = self.card_of('quiet:gone.example')
        self.fleet.ask_free(self.lines()['quiet:gone.example']['item']['ask'], 'work')
        self.assertIn('asked', self.shown(gone))

    def test_a_line_the_next_brief_no_longer_has_settles_by_itself(self):
        self.tell(PAT)
        globex = self.card_of('unanswered:globex.example')
        self.tell({'quiet': [GONE]}, day=0)  # Pat answered Globex, or someone took it
        row = self.card(globex)
        self.assertEqual(row['status'], 'completed')
        with self.store.connect() as db:
            why = db.execute('SELECT feedback FROM decisions WHERE suggestion_id=? ORDER BY created_at DESC', (globex,)).fetchone()[0]
        self.assertEqual(why, 'Someone on the team replied or took it on')
        self.assertEqual(self.card('s3')['status'], 'pending')  # a joined to-do stays the owner's
        self.assertEqual(self.card(self.card_of('quiet:gone.example'))['status'], 'pending')
        self.assertTrue(self.fleet.brief_todos_open('work'))  # Gone's still is: the brief is rebuilt to see it settle

    def test_details_show_only_what_the_team_graph_shares_and_the_owners_work_mail(self):
        # the owner's personal mailbox has newer mail from Globex: never on the Work to-do
        self.store.commit_page('home', {}, [mail('home', 0, 'Ada <ada@globex.example>', 'owner@gmail.com', message_id='<home@globex.example>')])
        self.store.commit_page('work', {}, [mail('work', 2, 'Ada <ada@globex.example>', 'owner@acme.example', message_id='<work@globex.example>')])
        shared = [{'subject': f'Renewal {n}', 'from': 'Ada', 'at': '2026-10-1' + str(n), 'via': 'Pat', 'preview': 'the 40k discount', 'private': False}
                  for n in range(5)]
        seen = []
        self.fleet.team_for = lambda db, node: seen.append(node) or (None, {'threads': shared, 'people': [{'name': 'Pat'}, {'name': 'Kim'}]})
        self.tell({**PAT, 'unanswered': [{**GLOBEX, 'at': (NOW - dt.timedelta(days=3)).date().isoformat()}]})
        self.store.commit_page('work', {}, [brief_fixture.reply('work', 1, 'ada@globex.example', 'tg', '<rg@acme.example>')])
        line = self.shown(self.card_of('unanswered:globex.example'))['items'][0]
        self.assertEqual(len(line['threads']), fleet_brief_todos.THREADS_SHOWN)
        self.assertEqual(set(line['threads'][0]), {'subject', 'from', 'at', 'via'})  # never a preview or anything else
        self.assertNotIn('40k', json.dumps(line))
        self.assertEqual(line['also'], ['Kim'])  # Pat is on the line already
        self.assertNotIn('home@globex', json.dumps(line))
        # what they wrote: the owner's own copy from that day on the work mailbox (not the home one), to open in the reader
        self.assertEqual(line['gist']['from'], 'Ada')
        self.assertEqual(line['gist']['at'][:10], (NOW - dt.timedelta(days=2)).date().isoformat())
        self.assertEqual(set(line['gist']), {'event', 'subject', 'from', 'at'})  # never its text
        self.assertNotIn('own', line)  # the newest from them is that same email
        self.assertEqual(line['stake'], [{'id': 'project:90', 'name': 'renewal', 'stage': 'Proposal'}])
        self.assertEqual(line['org'], {'id': 'org:globex.example', 'name': 'Globex'})
        self.assertNotIn('unshared', line)
        self.assertTrue(seen)
        # nothing shared about them: the line and the owner's own Graph alone
        self.fleet.team_for = lambda db, node: (_ for _ in ()).throw(KeyError(node))
        line = self.shown(self.card_of('unanswered:globex.example'))['items'][0]
        self.assertEqual((line['threads'], line['also'], line['gist']['from']), ([], [], 'Ada'))

    def test_vague_lines_make_no_todo_and_one_that_turns_vague_closes(self):
        recent = {**GONE, 'last': (NOW - dt.timedelta(days=5)).date().isoformat()}  # in touch five days ago: not quiet
        self.tell({'unanswered': [GLOBEX], 'quiet': [recent]})
        self.assertNotIn('quiet:gone.example', self.lines())
        globex = self.card_of('unanswered:globex.example')
        with self.store.connect() as db:  # the renewal is won and closed: nothing at stake, nothing else known
            db.execute("UPDATE projects SET closed_at=? WHERE id=90", (NOW.isoformat(),))
        self.tell({'unanswered': [GLOBEX]})
        self.assertIn('unanswered:globex.example', self.brief_keys())  # still a line of the brief
        self.assertEqual(self.card(globex)['status'], 'completed')  # but no longer a to-do: only a name and a day
        with self.store.connect() as db:
            why = db.execute('SELECT feedback FROM decisions WHERE suggestion_id=? ORDER BY created_at DESC', (globex,)).fetchone()[0]
        self.assertEqual(why, 'Nothing specific to act on, it stays in the team brief')

    def test_what_they_asked_comes_from_the_owners_own_copy_and_a_reply_from_who_it_went_to_settles_it(self):
        asked = mail('work', 1, 'Ada <ada@globex.example>', f'Pat <{TEAM}>', cc='owner@acme.example', message_id='<ask@globex.example>')
        self.store.commit_page('work', {}, [asked])
        self.tell(PAT)
        globex = self.card_of('unanswered:globex.example')
        self.assertTrue(self.card(globex)['body'].startswith('Their email: “Mail '))  # its subject, never its text
        with self.store.connect() as db:  # the review's own line about that email (client threads only)
            event = db.execute("SELECT id FROM events WHERE source_id=?", (asked['source_id'],)).fetchone()[0]
            db.execute("INSERT INTO share_lines(event_id,thread,line,at) VALUES(?,?,?,?)", (event, 'x', 'Ada asked Pat for the renewal quote', NOW.isoformat()))
        self.tell(PAT)
        row = self.card(globex)
        self.assertEqual((row['title'], row['body']), (f'Globex has been waiting on Pat since {self.day(1)}',
                                                       'Ada asked Pat for the renewal quote. At stake: renewal (Proposal). You also talk to them.'))
        # Pat's answer is in the owner's copy of the thread (cc, a shared inbox): settled, though Pat's Machine hadn't said so yet
        answer = mail('work', 0, f'Pat <{TEAM}>', 'ada@globex.example', message_id='<answer@acme.example>')
        answer['metadata'].update(thread_id=asked['metadata']['thread_id'])
        self.store.commit_page('work', {}, [answer])
        self.tell(PAT)
        self.assertEqual(self.card(globex)['status'], 'completed')
        with self.store.connect() as db:
            why = db.execute('SELECT feedback FROM decisions WHERE suggestion_id=? ORDER BY created_at DESC', (globex,)).fetchone()[0]
        self.assertEqual(why, 'Someone on the team replied or took it on')

    def test_a_quiet_company_says_what_is_at_stake_or_makes_no_todo(self):
        line = {'key': 'quiet:globex.example', 'kind': 'quiet', 'title': 'Globex went quiet', 'why': 'last contact Aug 2', 'org': 'Globex',
                'domain': 'globex.example', 'at': (NOW - dt.timedelta(days=30)).date().isoformat(), 'team': [{'label': 'Pat', 'name': 'Pat'}], 'mine': True}
        gist = {'event': 1, 'subject': 'Renewal terms', 'at': line['at'] + 'T09:00:00+00:00', 'line': 'Ada asked for the new terms'}
        stake = [{'id': 'project:90', 'name': 'Globex renewal', 'stage': 'Proposal', 'open': True}]
        made = fleet_brief_todos.specific(line, {'stake': stake, 'gist': gist}, NOW.date(), 'usually weekly')
        self.assertEqual(made['title'], 'Globex has been quiet for 4 weeks')
        self.assertEqual(made['why'], f"Last contact {fleet_brief._on_day(line['at'], NOW.date())}: Ada asked for the new terms. "
                                      'At stake: renewal (Proposal). Usually weekly. Known to you and Pat')
        self.assertIsNone(fleet_brief_todos.specific(line, {'stake': [], 'gist': gist}, NOW.date()))  # quiet, but nothing at stake
        self.assertIsNone(fleet_brief_todos.specific({**line, 'at': YESTERDAY}, {'stake': stake}, NOW.date()))  # not quiet at all


if __name__ == '__main__':
    unittest.main()
