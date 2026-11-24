"""A mail the owner only passed on is no answer to who wrote it; anything unsure still is (review.answered)."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant as a
from machine.mail_quotes import sends_on
from machine.store import review

HEADER = {
    'English': '---------- Forwarded message ---------\nFrom: Ann Poe <ann@client.example>\nDate: Mon, May 3, 2027 at 10:00\nSubject: Contract\nTo: Sam <sam@acme.example>\n\n',
    'Dutch': '---------- Doorgestuurd bericht ---------\nVan: Ann Poe <ann@client.example>\nDate: ma 3 mei 2027 10:00\nSubject: Contract\nTo: Sam <sam@acme.example>\n\n',
    'German': '________________________________\nVon: Ann Poe <ann@client.example>\nGesendet: Montag, 3. Mai 2027 10:00\nAn: Sam\nBetreff: Contract\n\n',
}
ASKED = 'Can you sign this before Friday?'


class SendsOn(unittest.TestCase):
    def test_a_forward_holds_a_mail_from_someone_not_on_it(self):
        people = 'sam <sam@acme.example> kim lee <kim@acme.example>'
        for name, header in HEADER.items():
            for subject in ('Fwd: Contract', 'Rv: Contract', 'Contract'):  # whatever its prefix
                self.assertTrue(sends_on('FYI\n\n' + header + ASKED, subject, people), (name, subject))

    def test_an_answer_does_not(self):
        people = 'sam <sam@acme.example> ann poe <ann@client.example>'
        for name, header in HEADER.items():
            self.assertFalse(sends_on('Sure.\n\n' + header + ASKED, 'Re: Contract', people), name)
        self.assertFalse(sends_on('Sure.\n\nOn Mon, May 3, 2027 at 10:00 Ann Poe <ann@client.example> wrote:\n> ' + ASKED, 'Re: Contract', people))
        self.assertFalse(sends_on('Sure.', 'Re: Contract', people))
        self.assertFalse(sends_on('', '', ''))


class Answered(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'email': 'sam@acme.example', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Acme'}]
        self.n = 0

    def answered(self, *sent, sender='Ann Poe <ann@client.example>', body=ASKED, **meta):
        """Whether the message counts as answered after these sent mails: (to, subject, body, extra metadata)."""
        self.n += 1
        mail = lambda i, at, labels, frm, to, title, text, extra: {
            'account_id': 'work', 'source_id': f'{self.n}-{i}', 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': text, 'deleted': False,
            'metadata': {'from': frm, 'to': to, 'thread_id': f't{self.n}', 'labels': labels, **extra}}
        self.store.commit_page('work', {}, [mail(0, '2027-05-03T10:00:00+00:00', ['INBOX'], sender, 'Sam <sam@acme.example>', 'Contract', body, meta)] + [
            mail(i + 1, f'2027-05-0{i + 4}T10:00:00+00:00', ['SENT'], 'Sam <sam@acme.example>', to, title, text, dict(extra))
            for i, (to, title, text, *more) in enumerate(sent) for extra in [more[0] if more else {}]])
        with self.store.connect() as db:
            row = db.execute("SELECT * FROM events WHERE source_id=?", (f'{self.n}-0',)).fetchone()
            return review.answered(db, row)

    def test_only_a_forward_to_someone_else_is_no_answer(self):
        forward = lambda to, **extra: (to, 'Fwd: Contract', 'FYI\n\n' + HEADER['English'] + ASKED, extra)
        answer = ('Ann Poe <ann@client.example>', 'Re: Contract', 'Will do.')
        self.assertFalse(self.answered())
        self.assertTrue(self.answered(answer))
        self.assertFalse(self.answered(forward('Kim Lee <kim@acme.example>')))
        self.assertFalse(self.answered(forward('Kim Lee <kim@acme.example>'), forward('Lou <lou@other.example>')))
        self.assertTrue(self.answered(forward('Kim Lee <kim@acme.example>'), answer))
        self.assertFalse(self.answered(forward('Acme Support <support@acme.example>'), body='Is Acme down?'))  # its company's name is nobody's

    def test_whoever_is_theirs_on_it_or_named_is_answered(self):
        forward = lambda to, **extra: (to, 'Fwd: Contract', 'FYI\n\n' + HEADER['English'] + ASKED, extra)
        self.assertTrue(self.answered(forward('Kim Lee <kim@acme.example>', cc='ann@client.example')))
        self.assertTrue(self.answered(forward('Bo <bo@client.example>')))  # their company
        self.assertTrue(self.answered(forward('Bo <bo@mail.client.example>')))
        self.assertTrue(self.answered(forward('Kim Lee <kim@other.example>'), body='Kim takes this over, talk to Kim please.'))
        self.assertTrue(self.answered(forward('x@other.example'), body='Please contact x@other.example.'))
        self.assertTrue(self.answered(forward('Lou <lou@other.example>'), cc='lou@other.example'))
        self.assertTrue(self.answered(forward('reply+1@desk.example'), **{'reply-to': 'reply+1@desk.example'}))
        self.assertTrue(self.answered(('reply+1@desk.example', 'Re: Contract', 'Will do.')))  # no forward: where it went says nothing
        self.assertTrue(self.answered(('Lou <lou@other.example>', 'Re: Contract', 'Hello Lou.\n\n' + HEADER['German'] + ASKED)))

    def test_free_mail_is_no_company_and_their_other_address_is_theirs(self):
        forward = lambda to: (to, 'Fwd: Contract', 'FYI\n\n' + HEADER['English'].replace('client.example', 'gmail.com') + ASKED)
        self.assertFalse(self.answered(forward('Lou <lou@gmail.com>'), sender='Ann Poe <ann@gmail.com>'))
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:ann@gmail.com','person','Ann',1,1,?)",
                       (json.dumps({'identifiers': ['email:ann@gmail.com', 'email:ann@home.example']}),))
        self.assertTrue(self.answered(forward('ann@home.example'), sender='Ann Poe <ann@gmail.com>'))


if __name__ == '__main__':
    unittest.main()
