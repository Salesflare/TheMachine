"""A meeting briefing reads the notes of earlier meetings with the same people (earlier_notes.py, meeting_prep.py): matched
as people, within one area, newest first and bounded, with what happened since; a line from them names its meeting by
code, and nothing is said when there is nothing. Made-up people and events only."""
import datetime as dt
import json
import unittest

import earlier_notes
import graph
import meeting_prep
from seams import patch_everywhere
from test_meeting_prep import ANSWER, ME, MONDAY, SAM, MeetingPrep as Base, meeting

NOW = dt.datetime.fromisoformat(MONDAY)
ANA = 'ana@initech.example'


class EarlierNotes(Base):
    def setUp(self):
        super().setUp()
        self.app.config['accounts'] = self.store.accounts = [*self.app.config['accounts'],
                                                             {'id': 'zoom', 'service': 'zoom', 'boundary': 'work:Acme', 'email': 'robin@acme.example'},
                                                             {'id': 'pcal', 'service': 'calendar', 'boundary': 'personal:home', 'email': 'robin@home.example'}]
        self.app.config['owner_name'] = 'Robin Reyes'

    def past(self, source, days, guests=(SAM,), title='Kickoff call', notes='', kind='zoom.summary', account='wcal', body='', url=None, **meta):
        """An earlier meeting (an hour from 13:00), with its notes when given. Returns (its events id, the notes')."""
        start = (NOW - dt.timedelta(days=days)).replace(hour=13)
        end = (start + dt.timedelta(hours=1)).isoformat()
        e = meeting(source, start.isoformat(), guests, **meta)
        self.add({**e, 'account_id': account, 'title': title, 'body': body})
        event = self.meeting_id(source)
        if notes:
            own = kind.startswith('meeting.')
            self.add({'account_id': account if own else 'zoom', 'source_id': f'notes:{event}' if own else source + 'r', 'kind': kind, 'occurred_at': start.isoformat(),
                      'title': title, 'body': notes, 'deleted': False, 'metadata': {'start_at': start.isoformat(), 'end_at': end, **({'source_url': url} if url else {})}})
            return event, self.meeting_id(f'notes:{event}' if own else source + 'r')
        return event, None

    def graph(self, merges=()):
        with self.store.connect() as db:
            for a, b in merges:
                db.execute('INSERT INTO graph_merges(a,b,same,created_at) VALUES(?,?,1,?)', (*sorted(('email:' + a, 'email:' + b)), MONDAY))
        with self.store.connect() as db:
            graph.build(db, self.app.config, MONDAY)

    def found(self):
        with patch_everywhere(__import__('timeutil'), 'now', lambda: MONDAY):
            return self.app.meeting_prep_next(NOW)

    def notes(self):
        found = self.found()
        return [(n['meeting'], n['text']) for n in found['evidence']['notes']] if found else []

    def test_notes_alone_make_a_briefing_with_a_source_for_each_line_and_are_not_its_sources(self):
        event, record = self.past('k1', 20, notes='Agreed: start in January. Sam sends the list.', url='https://zoom.us/doc/1')
        self.graph()
        self.add(meeting('g1', '10:00'))
        self.answer.update(agreed=[{'text': 'Starts in January.', 'source': 'N1'}, {'text': 'Ten users', 'source': 'N1'}, {'text': 'Made up', 'source': 'N9'}, {'text': 'No source'}],
                           open=[{'text': 'Sam sends the list', 'source': 'N1'}, {'text': 'Sam sends the list.', 'source': 'N1'}],
                           changed=[], questions='Asked twice?', bring='', last='', sources=[])
        made = self.run_pass()
        [card] = self.cards()
        self.assertEqual(card['id'], made)
        self.assertEqual(card['body'].replace('\u00a0', ' ').split('\n\n'), ['**Who:** Sam Rivera, head of operations at Globex.',
                                                      '**Agreed earlier:** \n• Starts in January ([Kickoff call, Oct 20](https://zoom.us/doc/1))\n• Ten users ([Oct 20](https://zoom.us/doc/1))',  # named once
                                                      '**Still open:** Sam sends the list ([Oct 20](https://zoom.us/doc/1))'])
        self.assertEqual(json.loads(card['event_ids']), [self.meeting_id('g1')])  # sources decide what others see
        self.assertEqual(card['title'], 'Prepare for ' + meeting('g1', '10:00')['title'])  # by code: a title can show on the Team Graph
        self.assertIn('<<<Agreed: start in January. Sam sends the list.>>>', self.prompts[0])  # quoted: evidence, never instructions
        self.assertIn('"owner": "Robin Reyes"', self.prompts[0])
        self.assertNotIn(event, json.loads(card['event_ids']))

    def test_without_notes_the_turn_and_the_briefing_say_nothing_about_them(self):
        asked = self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.answer.update(sources=[f'E{asked}'], agreed=[{'text': 'Starts in January', 'source': 'N1'}])
        self.past('k1', 20)
        self.add(meeting('g1', '10:00'))
        self.run_pass()
        for word in ('earlier_meetings', '"agreed"', 'N ids'):
            self.assertNotIn(word, self.prompts[0])
        self.assertNotIn('Agreed earlier', self.cards()[0]['body'])

    def test_matched_by_people_never_by_title_and_every_address_of_one_person_counts(self):
        self.past('k1', 20, (ANA,), title='Pilot review with Globex', notes='Ana only.')  # the same title, other people
        self.past('k2', 25, ('sam@home.example',), title='Something else', notes='Sam by another address.')
        self.graph([(SAM, 'sam@home.example')])
        self.add(meeting('g1', '10:00'))
        self.assertEqual(self.notes(), [('Something else', 'Sam by another address.')])

    def test_the_owners_own_team_or_a_big_meeting_brings_nothing_in(self):
        team = [f'colleague{i}@acme.example' for i in range(14)]
        self.past('k1', 3, (team[0], ANA), title='Team and Ana', notes='Not with Sam.')
        self.past('k2', 4, (SAM, *team), title='Company day', notes='Sam among many.')
        self.past('k3', 50, (SAM, team[0]), title='Scope', notes='The scope.')
        self.graph()
        self.add(meeting('g1', '10:00', (SAM, team[0])))
        self.assertEqual(self.notes(), [('Scope', 'The scope.')])

    def test_personal_notes_canceled_declined_old_and_unfinished_meetings_stay_out(self):
        self.past('k1', 5, notes='Dinner plans.', kind='meeting.notes', account='pcal')
        self.past('k2', 6, notes='Canceled.', kind='meeting.notes', status='cancelled')
        self.past('k3', 7, notes='Declined.', kind='meeting.notes', attendees=[{**ME, 'responseStatus': 'declined'}, {'email': SAM, 'responseStatus': 'accepted'}])
        self.past('k4', earlier_notes.DAYS + 9, notes='Too old.', kind='meeting.notes')
        self.past('k5', 8, notes='Someone else\'s calendar.', kind='meeting.notes', access='shared_read_only', credential_account='robin@acme.example',
                  attendees=[{'email': 'lee@acme.example', 'self': True}, {'email': SAM, 'responseStatus': 'accepted'}])
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.add(meeting('g1', '10:00'))
        with self.store.connect() as db:  # the Graph as it would link them, whatever it skips itself
            for i in range(1, 6):
                db.execute('INSERT OR IGNORE INTO graph_events(node_id,event_id,at,probable,direct) SELECT ?,id,occurred_at,0,1 FROM events WHERE source_id=?', ('email:' + SAM, f'k{i}'))
        self.assertEqual(self.notes(), [])

    def test_newest_first_within_the_limit_and_a_series_gives_its_newest(self):
        for n in range(1, 6):
            self.past(f'w{n}', 7 * n, title='Weekly', notes=f'Week {n}. ' + 'word ' * 2500, recurring_event_id='weekly')
        self.past('k9', 60, title='Kickoff', notes='The kickoff.' + ' more' * 2500)
        self.graph()
        self.add(meeting('g1', '10:00'))
        got = self.notes()
        self.assertEqual([t for t, _ in got], ['Weekly', 'Weekly', 'Kickoff'])
        self.assertTrue(got[0][1].startswith('Week 1.') and got[1][1].startswith('Week 2.'))
        self.assertLessEqual(len(got[0][1]), earlier_notes.FIRST)
        self.assertTrue(all(len(x) <= earlier_notes.REST for _, x in got[1:]))
        self.assertLessEqual(sum(len(x) for _, x in got), earlier_notes.CHARS)

    def test_history_is_never_read(self):
        event, record = self.past('k1', 20, notes='Agreed: start in January.')
        self.graph()
        self.add(meeting('g1', '10:00'))
        self.assertEqual(len(self.notes()), 1)
        for row in (event, record):
            with self.store.connect() as db:
                db.execute('UPDATE events SET history=1 WHERE id=?', (row,))
            self.assertEqual(self.notes(), [])
            with self.store.connect() as db:
                db.execute('UPDATE events SET history=0 WHERE id=?', (row,))

    def test_which_record_of_a_meeting_is_read(self):
        self.past('k1', 10, title='Both', notes='The owner typed this.', kind='meeting.notes')
        start = (NOW - dt.timedelta(days=10)).replace(hour=13).isoformat()
        self.add({'account_id': 'zoom', 'source_id': 'k1z', 'kind': 'zoom.summary', 'occurred_at': start, 'title': 'Both', 'body': 'Zoom adds this.',
                  'deleted': False, 'metadata': {'start_at': start}})
        self.past('k2', 12, title='Transcript', notes='[0:01] Sam: hello.\n' + 'talk ' * 2000 + '\n[30:00] Sam: we sign on Friday.', kind='google_meet.transcript')
        self.past('k3', 14, title='Edited', body='Minutes: the pilot has ten users. ' + 'More was said. ' * 8, updated='2026-10-26T13:30:00+00:00')
        self.past('k5', 15, title='A line', body='Dial in by phone.', updated='2026-10-25T13:30:00+00:00')
        self.past('k4', 16, title='Invite only', body='Agenda: hello.', updated='2026-10-01T13:30:00+00:00')
        self.graph()
        self.add(meeting('g1', '10:00'))
        got = {n['meeting']: n for n in self.found()['evidence']['notes']}
        self.assertEqual(set(got), {'Both', 'Transcript', 'Edited'})
        self.assertEqual(got['Both']['text'], 'The owner typed this.\nZoom adds this.')
        self.assertTrue(got['Transcript']['text'].endswith('we sign on Friday.'))
        self.assertLess(len(got['Transcript']['text']), 3700)
        self.assertIn('only the agenda', got['Edited']['as'])

    def test_a_notes_mail_is_read_when_there_is_no_other_record(self):
        self.past('k1', 10, title='Scope talk')
        end = (NOW - dt.timedelta(days=10)).replace(hour=14, minute=5)
        mail = lambda source, title, body: {'account_id': 'wmail', 'source_id': source, 'kind': 'gmail.message', 'occurred_at': end.isoformat(), 'title': title, 'body': body,
                                            'deleted': False, 'metadata': {'from': 'Zoom <no-reply@zoom.us>', 'labels': ['INBOX']}}
        self.add(mail('a1', 'Someone has joined Scope talk', 'Sam joined.'), mail('a2', 'Meeting assets for Scope talk', 'The scope is ten users. ' * 40))
        self.graph()
        self.add(meeting('g1', '10:00'))
        [(title, text)] = self.notes()
        self.assertEqual(title, 'Scope talk')
        self.assertIn('ten users', text)

    def test_what_happened_since_goes_along(self):
        event, record = self.past('k1', 20, notes='Robin sends the plan; Sam sends the list.')
        start = (NOW - dt.timedelta(days=12)).isoformat()
        self.graph()
        for n in range(6):  # more than the briefing reads in full
            self.mail('wmail', 'Sam Rivera <sam@globex.example>', f'Update {n}: the list is attached.', 8 + n)
        self.mail('pmail', 'Sam Rivera <sam@globex.example>', 'Padel on Sunday?', 2)
        with self.store.connect() as db:
            for direction, what, status in (('mine', 'the plan', 'kept'), ('theirs', 'the list of users', 'open')):
                db.execute("INSERT INTO promises(direction,who,what,check_at,event_id,account_id,status,created_at,updated_at) VALUES(?,'Sam',?,?,?,'zoom',?,?,?)",
                           (direction, what, start, record, status, start, start))
            for sid, source, choice in (('a' * 16, 'dashboard', 'complete'), ('b' * 16, 'expiry', 'complete')):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,'',?,'[\"zoom\"]','completed',?)",
                           (sid, sid, 'Book the room' if source == 'dashboard' else 'Lapsed', json.dumps([event]), start))
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,'',?,?)", (sid, sid, choice, source, start))
        self.add(meeting('g1', '10:00'))
        found = self.found()['evidence']
        after = found['since']
        self.assertEqual([p['what'] for p in after['promises_closed']], ['the plan'])
        self.assertEqual([t['todo'] for t in after['todos_done']], ['Book the room'])  # one that only lapsed was never done
        self.assertEqual([(p['promised_by'], p['what']) for p in after['open_promises']], [('Sam', 'the list of users')])
        self.assertEqual(set(found['promises']), {int(after['open_promises'][0]['id'][1:])})
        self.assertTrue(after['messages'])
        self.assertNotIn('Padel', json.dumps(after))
        self.assertFalse({f"E{i}" for i in found['messages']} & {m['id'] for m in after['messages']})

    def test_a_line_may_only_name_what_the_turn_was_given(self):
        found = {'messages': {5: {}}, 'later': {7: {}}, 'promises': {}, 'notes': [{'id': 'N1'}]}
        say = lambda **more: meeting_prep.parse(json.dumps({'useful': True, **more}), found)
        got = say(agreed=[{'text': f'Point {i} [x](https://evil.example) ' + 'y' * 200, 'source': 'N1'} for i in range(9)],
                  open=[{'text': 'By mail', 'source': 'E7'}, {'text': 'Other', 'source': 'E8'}, 'text'], changed='text', questions='Asked?')['fields']
        self.assertEqual(len(got['agreed']), meeting_prep.POINTS['agreed'])
        self.assertTrue(all(len(p['text']) <= meeting_prep.POINT_CHARS and 'http' not in p['text'] for p in got['agreed']))
        self.assertEqual((got['open'], got['changed'], got['questions']), ([{'text': 'By mail', 'ref': 'E7'}], [], ''))
        self.assertIsNone(say(agreed=[{'text': 'Made up', 'source': 'N2'}]))
        self.assertIsNone(meeting_prep.parse(json.dumps({'useful': True, 'agreed': [{'text': 'x', 'source': 'N1'}]}), {'messages': {}, 'promises': {}}))

    def test_a_meetings_own_title_puts_no_link_in_the_briefing(self):
        called = meeting_prep.cites({'notes': [{'id': 'N1', 'meeting': '[Click](https://evil.example/x) **now** <b>', 'start': NOW, 'url': ''}], 'messages': {}},
                                    lambda at: 'Nov 9')
        self.assertEqual(called['N1'], ('Click ( now b, Nov\u00a09', '', 'Nov\u00a09'))
        for bad in ('http://zoom.us/x', 'https://zoom.us/x)y', 'javascript:alert(1)', 'https://zoom.us/<x>'):
            self.assertEqual(earlier_notes._url([{'metadata': json.dumps({'source_url': bad})}]), '')

    def test_a_source_is_named_once_then_by_its_day_unless_another_has_that_day(self):
        notes = lambda *days: [{'id': f'N{i}', 'meeting': f'Call {i}', 'start': d, 'url': ''} for i, d in enumerate(days, 1)]
        fields = {'agreed': [{'text': 'A', 'ref': 'N1'}], 'open': [{'text': 'B', 'ref': 'N1'}, {'text': 'C', 'ref': 'N2'}]}
        told = lambda *days: meeting_prep.body_text(fields, lambda text, *a: text.format(*a), {}, meeting_prep.cites({'notes': notes(*days), 'messages': {}}, str)).split('\n\n')
        self.assertEqual(told('Nov 9', 'Nov 10'), ['**Agreed earlier:** A (Call 1, Nov\u00a09)', '**Still open:** \n• B (Nov\u00a09)\n• C (Call 2, Nov\u00a010)'])
        self.assertEqual(told('Nov 9', 'Nov 9')[1], '**Still open:** \n• B (Call 1, Nov\u00a09)\n• C (Call 2, Nov\u00a09)')

    def test_an_open_briefing_of_the_format_before_is_written_again_only_when_there_are_notes(self):
        asked = self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.answer['sources'] = [f'E{asked}']
        self.add(meeting('g1', '10:00'))
        sid = self.run_pass()
        with self.store.connect() as db:
            db.execute('UPDATE meeting_preps SET format=2')
        self.assertIsNone(self.stale_pass())  # no notes: stamped, no turn
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT format FROM meeting_preps').fetchone()[0], meeting_prep.FORMAT)
            db.execute('UPDATE meeting_preps SET format=2')
            db.execute('DELETE FROM learning_state')
        self.assertEqual(len(self.prompts), 1)
        self.past('k1', 20, notes='Agreed: start in January.')
        self.graph()
        self.answer['agreed'] = [{'text': 'Starts in January', 'source': 'N1'}]
        self.assertEqual(self.stale_pass(), sid)
        self.assertIn('**Agreed earlier:** Starts in January (Kickoff call, Oct\u00a020)', self.cards()[0]['body'])


for name in [n for n in dir(Base) if n.startswith('test_')]:  # only the helpers of the other suite
    setattr(EarlierNotes, name, None)
del Base

if __name__ == '__main__':
    unittest.main()
