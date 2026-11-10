"""What the app looks up in SQL still works with message protection on (message_seal.py).

On a sealed database SQLite sees only the keys kept in the clear (message_seal.PLAIN_METADATA for events.metadata,
DERIVED_JSON for the others): `json_extract(metadata,'$.cc')` is NULL there, silently. Each place that read such a key
in SQL now reads the rows instead, which open as they are read. These run on a sealed store, and on a plain one, and
fail on the sealed one without the fix. tests/test_message_seal.py (NothingOutsideTheSealedFields) keeps new ones out.
No real names or mail."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_ux as ux
import bounces
import enrichment
import message_seal
from machine.store import core, first_look

a = ux.a


def sealed_run(case, name):
    """Runs another file's test with every store it makes sealed; returns how many stores that were."""
    real, made = core.StoreCore.__init__, []

    def init(self, path, protect=None):
        made.append(path)
        real(self, path, protect=True)
    with patch.object(core.StoreCore, '__init__', init):
        result = unittest.TestResult()
        case(name).run(result)
    problems = result.failures + result.errors
    if problems:
        raise AssertionError(f'{case.__name__}.{name} on a sealed store:\n{problems[0][1]}')
    if result.skipped or not made:
        raise AssertionError(f'{case.__name__}.{name} did not run on a sealed store')
    return len(made)


class OnBoth(unittest.TestCase):
    """Each test's body runs on a plain store and on a sealed one."""

    def both(self, check):
        for protect in (False, True):
            with self.subTest(sealed=protect), tempfile.TemporaryDirectory() as temp:
                store = a.Store(Path(temp) / 'events.sqlite', protect=protect)
                with store.connect() as db:
                    self.assertEqual(message_seal.is_protected(db), protect)
                check(store)

    @staticmethod
    def event(account, source, kind, at, metadata, title='Note', body='Hello'):
        return {'account_id': account, 'source_id': source, 'kind': kind, 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
                'metadata': metadata}

    def test_the_keys_these_fixes_read_are_not_readable_in_sql_on_a_sealed_store(self):
        # the premise: were one of these keys made plain, its test below would no longer prove anything
        for key in ('cc', 'chat_kind', 'sender_id', 'end_at', 'status', 'location', 'admin_emails'):
            self.assertNotIn(key, message_seal.PLAIN_METADATA)
        def check(store):
            store.commit_page('work', {}, [self.event('work', 's1', 'gmail.message', '2026-10-05T09:00:00+00:00', {'to': 'pat@client.example', 'cc': 'sam@client.example'})])
            with store.connect() as db:
                seen = db.execute("SELECT json_extract(metadata,'$.cc'),json_extract(metadata,'$.to'),metadata FROM events").fetchone()
                self.assertEqual(seen[0], None if store.sealer else 'sam@client.example')
                self.assertEqual((seen[1], json.loads(seen[2])['cc']), ('pat@client.example', 'sam@client.example'))
        self.both(check)

    def test_a_flagged_address_that_was_only_copied_on_a_later_mail_clears(self):
        mail = lambda source, at, **m: self.event('work', source, 'gmail.message', at, {'thread_id': source, 'from': 'owner@example.com', **m})
        flag = "INSERT INTO email_bounces(address,kind,bounced_at,updated_at) VALUES(?,'hard',?,?)"
        def check(store):
            store.commit_page('work', {}, [
                mail('before', '2026-09-28T09:00:00+00:00', to='pat@client.example', cc='sam@client.example', labels=['SENT']),
                mail('copied', '2026-10-05T09:00:00+00:00', to='pat@client.example', cc='Sam <sam@client.example>, kim@client.example', labels=['SENT']),
                {**mail('received', '2026-10-05T10:00:00+00:00', to='owner@example.com', cc='lee@client.example', labels=['INBOX']),
                 'metadata': {'thread_id': 'received', 'from': 'pat@client.example', 'to': 'owner@example.com', 'cc': 'lee@client.example', 'labels': ['INBOX']}}])
            with store.connect() as db:
                bounces.ensure(db)
                for address in ('sam@client.example', 'lee@client.example'):
                    db.execute(flag, (address, '2026-10-01T09:00:00+00:00', '2026-10-01T09:00:00+00:00'))
                # sent to others with Sam copied, days ago and no bounce since: Sam works again. Lee was only copied
                # on a mail someone else sent: no sign of anything
                self.assertEqual(bounces.clear(db, '2026-10-09T09:00:00+00:00', {'owner@example.com'}), [('sam@client.example', 'delivered')])
                self.assertEqual(bounces.clear(db, '2026-10-09T09:05:00+00:00', {'owner@example.com'}), [])
                # an address flagged later is looked up in the mail read before too; a mail from before its bounce is no sign
                db.execute(flag, ('kim@client.example', '2026-10-02T09:00:00+00:00', '2026-10-02T09:00:00+00:00'))
                db.execute(flag, ('pat@other.example', '2026-10-02T09:00:00+00:00', '2026-10-02T09:00:00+00:00'))
                self.assertEqual(bounces.clear(db, '2026-10-09T09:10:00+00:00', {'owner@example.com'}), [('kim@client.example', 'delivered')])
            # and in mail collected after that: only the new mail is read (the pass keeps where it was)
            store.commit_page('work', {}, [mail('later', '2026-10-06T09:00:00+00:00', to='pat@client.example', cc='pat@other.example', labels=['SENT'])])
            with store.connect() as db:
                at = db.execute('SELECT last_event FROM email_bounce_cc_scan').fetchone()[0]
                self.assertEqual(at, db.execute("SELECT id FROM events WHERE source_id='copied'").fetchone()[0])
                self.assertEqual(bounces.clear(db, '2026-10-09T09:15:00+00:00', {'owner@example.com'}), [('pat@other.example', 'delivered')])
                self.assertEqual([r[0] for r in db.execute('SELECT address FROM email_bounces WHERE cleared_at IS NULL')], ['lee@client.example'])
        self.both(check)

    def test_a_telegram_picture_is_asked_for_someone_met_only_in_a_group(self):
        said = lambda source, chat, kind, sender, account='tg': self.event(account, source, 'telegram.message', '2026-10-05T09:00:00+00:00',
                                                                         {'chat_id': chat, 'chat_kind': kind, 'sender_id': sender, 'chat_name': 'Chat'})
        def check(store):
            store.commit_page('tg', {}, [said('m1', '444', 'dm', '444'), said('m2', '777', 'group', '555'), said('m3', '777', 'group', '666')])
            with store.connect() as db:
                # 444 writes one to one, 555 only in the group; the group's own id (777) is no person's chat
                found = enrichment.telegram_addresses(db, {'tg:444', 'tg:555', 'tg:777', 'tg:888'}, ['tg'])
                self.assertEqual(found, {'tg:444': ('tg', '444'), 'tg:555': ('tg', '555')})
                self.assertEqual(enrichment.telegram_addresses(db, {'tg:555'}, ['other']), {})
        self.both(check)

    def test_the_calendar_shows_what_began_before_the_days_shown_and_still_runs(self):
        day = lambda source, start, end: self.event('cal', source, 'calendar.event', start, {'end_at': end, 'status': 'confirmed'}, title=source)
        def check(store):
            store.commit_page('cal', {}, [day('trip', '2026-10-03T08:00:00+00:00', '2026-10-06T18:00:00+00:00'),
                                          day('over', '2026-10-03T09:00:00+00:00', '2026-10-03T10:00:00+00:00'),
                                          day('long ago', '2026-07-01T09:00:00+00:00', '2026-07-01T10:00:00+00:00'),
                                          day('meeting', '2026-10-05T09:00:00+00:00', '2026-10-05T10:00:00+00:00'),
                                          day('after', '2026-10-12T09:00:00+00:00', '2026-10-12T10:00:00+00:00')])
            rows = store.calendar(['cal'], '2026-10-05T00:00:00+00:00', '2026-10-12T00:00:00+00:00')
            self.assertEqual([r['title'] for r in rows], ['trip', 'meeting'])
            self.assertEqual(store.calendar(['other'], '2026-10-05T00:00:00+00:00', '2026-10-12T00:00:00+00:00'), [])
        self.both(check)

    def test_a_final_step_counts_as_the_first_verified_action_only_when_it_was_completed(self):
        job = "INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) VALUES(?,?,'r',?,'done',?,?,'a','dashboard','')"
        def check(store):
            with store.connect() as db:
                for i, state in enumerate(('failed', 'completed', 'completed')):
                    at = f'2026-10-0{i + 1}T09:00:00+00:00'
                    db.execute(job, (f'j{i}', f's{i}', json.dumps({'kind': 'finish', 'finish_result': {'state': state, 'summary': 'Booked the room'}}), at, at))
                found = first_look.first_value(db, {}, '2026-01-01T00:00:00+00:00')
                self.assertEqual((found['first_verified_action_at'], found['first_verified_action']), ('2026-10-02T09:00:00+00:00', 'finish'))
                self.assertIsNone(first_look.first_value(db, {}, '2026-10-04T00:00:00+00:00')['first_verified_action'])
        self.both(check)

class ExistingTestsSealed(unittest.TestCase):
    """Tests that already cover a lookup, run again with their store sealed: each failed there before its fix."""

    def test_a_follow_up_whose_preparation_said_stop_without_a_draft_is_drafted_after_all(self):
        import test_follow_ups
        sealed_run(test_follow_ups.FollowUps, 'test_follow_ups_an_earlier_version_stopped_on_judgment_are_drafted_after_all')

    def test_a_calendar_does_not_count_canceled_events_as_coming_up(self):
        import test_assistant
        sealed_run(test_assistant.Invariants, 'test_a_calendar_counts_its_events_in_the_next_7_days')

    def test_the_owner_is_found_among_a_shared_intercom_accounts_admins(self):
        import test_intercom_assignee
        sealed_run(test_intercom_assignee.Store, 'test_a_shared_intercom_finds_its_owner_by_address_never_by_the_sharers_admin')

    def test_places_used_before_are_suggested(self):
        import test_calendar_writes
        sealed_run(test_calendar_writes.Suggestions, 'test_own_places_first_then_the_map_with_only_the_text')

    def test_a_failing_test_is_reported_and_one_without_a_store_does_not_count(self):
        class Fails(unittest.TestCase):
            def test_it(self):
                a.Store(Path(self.enterContext(tempfile.TemporaryDirectory())) / 'events.sqlite')
                self.fail('as expected')

            def test_no_store(self):
                pass
        with self.assertRaisesRegex(AssertionError, 'as expected'):
            sealed_run(Fails, 'test_it')
        with self.assertRaisesRegex(AssertionError, 'did not run on a sealed store'):
            sealed_run(Fails, 'test_no_store')


if __name__ == '__main__':
    unittest.main()
