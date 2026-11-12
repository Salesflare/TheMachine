"""Sending from any mailbox over IMAP (smtp_mail.py, next_actions.EmailTransport): the approved email goes out through
the mailbox's SMTP server and a copy lands in its Sent folder. A fake SMTP server and the fake IMAP server of
test_imap.py, both on this computer, stand in; no other server is reached and no real email is sent. The password never
shows in a log, a result or an error."""
import base64
import email
import email.policy
import re
import socketserver
import ssl
import threading
import unittest
from unittest import mock

import imap_mail
import next_actions
import smtp_mail
import sources
from test_imap import PASSWORD, USER, Base, Folder, mime, when


class FakeSmtp(socketserver.ThreadingTCPServer):
    """A small ESMTP server: EHLO, STARTTLS, AUTH PLAIN, MAIL, RCPT, DATA, RSET, NOOP, QUIT.
    mode: 'ssl', 'starttls' or 'plain' (no STARTTLS on offer). refuse: 'mail', 'rcpt', 'data451', 'data554' or 'drop'
    (the connection goes while the message is coming in). files_into: a Folder the server files sent mail in itself."""
    daemon_threads = allow_reuse_address = True

    def __init__(self, mode, cert, users):
        super().__init__(('127.0.0.1', 0), SmtpHandler)
        self.mode, self.users, self.refuse, self.files_into = mode, users, None, None
        self.received, self.greetings, self.commands = [], [], []
        self.auth, self.auths = ['PLAIN'], []  # the AUTH methods it offers; each sign-in tried, by method
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(*cert)
        threading.Thread(target=self.serve_forever, daemon=True).start()

    @property
    def port(self):
        return self.server_address[1]


class SmtpHandler(socketserver.StreamRequestHandler):
    def setup(self):
        if self.server.mode == 'ssl':
            self.request = self.server.context.wrap_socket(self.request, server_side=True)
        super().setup()
        self.tls, self.user, self.sender, self.recipients = self.server.mode == 'ssl', None, None, []

    def finish(self):
        try:
            super().finish()
        finally:
            self.request.close()

    def send(self, text):
        self.wfile.write(text.encode())
        self.wfile.flush()

    def handle(self):
        self.send('220 fake ready\r\n')
        while True:
            line = self.rfile.readline()
            if not line:
                return
            verb, _, rest = line.decode().rstrip('\r\n').partition(' ')
            verb = verb.upper()
            self.server.commands.append((verb, self.tls))
            if verb in ('EHLO', 'HELO'):
                self.server.greetings.append(rest)
                extensions = ['SMTPUTF8', '8BITMIME'] + (['STARTTLS'] if self.server.mode == 'starttls' and not self.tls else []) + (
                    ['AUTH ' + ' '.join(self.server.auth)] if self.tls else [])
                self.send(''.join(f'250-{e}\r\n' for e in ['fake'] + extensions[:-1]) + f'250 {extensions[-1]}\r\n')
            elif verb == 'STARTTLS':
                self.send('220 go ahead\r\n')
                self.request = self.server.context.wrap_socket(self.request, server_side=True)
                self.rfile, self.wfile = self.request.makefile('rb'), self.request.makefile('wb')
                self.tls = True
            elif verb == 'AUTH':
                method, _, answer = rest.partition(' ')
                self.server.auths.append(method.upper())
                if method.upper() not in self.server.auth or method.upper() == 'CRAM-MD5':  # never a working CRAM-MD5 here
                    self.send('535 5.7.8 authentication failed\r\n')
                    continue
                if method.upper() == 'LOGIN':  # the name, then the password, each asked for
                    self.send('334 VXNlcm5hbWU6\r\n')
                    user = base64.b64decode(self.rfile.readline().strip())
                    self.send('334 UGFzc3dvcmQ6\r\n')
                    password = base64.b64decode(self.rfile.readline().strip())
                else:
                    _, user, password = base64.b64decode(answer).split(b'\0')
                ok = self.tls and self.server.users.get(user.decode()) == password.decode()
                self.user = user.decode() if ok else None
                self.send('235 ok\r\n' if ok else '535 5.7.8 authentication failed\r\n')
            elif verb == 'MAIL':
                if self.server.refuse == 'mail':
                    self.send('550 5.7.1 not allowed\r\n')
                    continue
                self.sender, self.recipients = re.search(r'<([^>]*)>', rest)[1], []
                self.send('250 ok\r\n' if self.user else '530 sign in first\r\n')
            elif verb == 'RCPT':
                if self.server.refuse == 'rcpt':
                    self.send('550 5.1.1 no such user\r\n')
                    continue
                self.recipients.append(re.search(r'<([^>]*)>', rest)[1])
                self.send('250 ok\r\n')
            elif verb == 'DATA':
                self.send('354 go on\r\n')
                lines = []
                while True:
                    part = self.rfile.readline()
                    if part in (b'.\r\n', b''):
                        break
                    lines.append(part[1:] if part.startswith(b'..') else part)
                    if self.server.refuse == 'drop':
                        return
                data = b''.join(lines)
                if self.server.refuse == 'data451':
                    self.send('451 4.3.0 try again later\r\n')
                elif self.server.refuse == 'data554':
                    self.send('554 5.7.1 message refused\r\n')
                else:
                    self.server.received.append((self.sender, list(self.recipients), data))
                    if self.server.files_into is not None:
                        self.server.files_into.add(data, when(0), ['\\Seen'])
                    self.send('250 queued\r\n')
            elif verb in ('RSET', 'NOOP'):
                self.send('250 ok\r\n')
            elif verb == 'QUIT':
                self.send('221 bye\r\n')
                return
            else:
                self.send('502 unknown\r\n')


class SmtpBase(Base):
    smtp_mode = 'ssl'

    def setUp(self):
        super().setUp()
        self.smtp = FakeSmtp(self.smtp_mode, self.cert, {USER: PASSWORD})
        self.addCleanup(self.smtp.server_close)
        self.addCleanup(self.smtp.shutdown)
        self.account.update(smtp_host='127.0.0.1', smtp_port=self.smtp.port, smtp_security=self.smtp_mode, sent_folder='Sent')
        waits = mock.patch.object(smtp_mail, 'FILED_WAITS', (0.05,))
        waits.start()
        self.addCleanup(waits.stop)
        self.transport = next_actions.EmailTransport(self.config, sources.credential, sources.gog_read)

    def action(self, **extra):
        return {'kind': 'email', 'account_id': self.account['id'], 'from': USER, 'to': ['sam@client.test'], 'cc': [],
                'bcc': ['ana@acme.test'], 'subject': 'Pilot recap', 'body': 'Hi Sam,\n\nThe recap is below.\n\nAlex',
                'signature': False, **extra}

    def send(self, action=None, job=None):
        action = action or self.action()
        job = job or {'rfc_message_id': '<m1.recap@acme.test>'}
        self.transport.preflight(action)
        result = self.transport.send(action, job)
        self.assert_no_password(result, self.smtp.received, self.smtp.greetings)
        return result


class Sending(SmtpBase):
    def test_it_goes_to_every_recipient_and_a_copy_lands_in_sent(self):
        result = self.send()
        self.assertEqual(result, {'message_id': 's1700000001-1'})
        (sender, recipients, data), = self.smtp.received
        self.assertEqual((sender, recipients), (USER, ['sam@client.test', 'ana@acme.test']))
        out = email.message_from_bytes(data, policy=email.policy.default)
        self.assertNotIn('Bcc', out)  # a Bcc address gets it but shows to nobody
        self.assertEqual((out['To'], out['Message-ID']), ('sam@client.test', '<m1.recap@acme.test>'))
        filed = email.message_from_bytes(self.server.folders['Sent'].messages[1]['mime'], policy=email.policy.default)
        self.assertEqual(filed['Bcc'], 'ana@acme.test')  # the owner's own copy keeps it
        self.assertEqual([c for c, _ in self.server.commands].count('APPEND'), 1)
        self.assertEqual(set(self.smtp.greetings), {'[127.0.0.1]'})  # never this computer's name
        # It's in Sent: the one-send rule's check finds it
        self.assertEqual(self.transport.reconcile(self.action(), {'rfc_message_id': '<m1.recap@acme.test>'}),
                         {'message_id': 's1700000001-1'})

    def test_a_server_that_files_sent_mail_itself_gets_no_second_copy(self):
        self.smtp.files_into = self.server.folders['Sent']
        self.assertEqual(self.send(), {'message_id': 's1700000001-1'})
        self.assertNotIn('APPEND', [c for c, _ in self.server.commands])
        self.assertEqual(len(self.server.folders['Sent'].messages), 1)

    def test_a_reply_keeps_its_thread_headers(self):
        self.server.folders['INBOX'].add(mime('Pilot', 'Sam <sam@client.test>', USER, 'x', '<q1@client.test>', when(1)), when(1))
        self.send(self.action(in_reply_to='<q1@client.test>', references='<q1@client.test>', subject='Re: Pilot'))
        out = email.message_from_bytes(self.smtp.received[0][2], policy=email.policy.default)
        self.assertEqual((out['In-Reply-To'], out['References']), ('<q1@client.test>', '<q1@client.test>'))

    def test_refusals_say_nothing_was_sent_and_file_nothing(self):
        for refuse, result in [('mail', {'rejected': 550}), ('rcpt', {'rejected': 550}), ('data554', {'rejected': 554}),
                               ('data451', {'not_sent': True})]:
            with self.subTest(refuse=refuse):
                self.smtp.refuse = refuse
                self.assertEqual(self.send(), result)
                self.assertEqual((self.smtp.received, self.server.folders['Sent'].messages), ([], {}))

    def test_a_connection_lost_while_the_message_goes_is_unknown_never_resent(self):
        self.smtp.refuse = 'drop'
        self.assertEqual(self.send(), {})  # 'uncertain': the worker never sends it again

    def test_a_wrong_password_stops_it_before_anything_goes(self):
        self.transport = next_actions.EmailTransport(self.config, lambda config, name: 'pw-Wrong-0000', sources.gog_read)
        with self.assertRaises(ValueError) as caught:
            self.transport.preflight(self.action())
        self.assertEqual(str(caught.exception), smtp_mail.STOPPED['smtp_auth_failed'])
        self.assertEqual(self.smtp.received, [])
        # and if the password changes between the check and the send, the send is refused, not retried every minute
        self.assertEqual(self.transport.send(self.action(), {'rfc_message_id': '<m2@acme.test>'}), {'rejected': 535})

    def test_a_missing_attachment_stops_it(self):
        action = self.action(attachments=[{'name': 'deck.pdf', 'type': 'application/pdf', 'sha256': '0' * 64, 'size': 10}])
        with self.assertRaises(ValueError) as caught:
            self.transport.preflight(action)
        self.assertIn('deck.pdf', str(caught.exception))

    def test_its_sent_mail_is_read_for_the_signature_it_ends_with(self):
        signature = 'Alex Doe\nAcme Labs'
        for n in range(3):
            self.server.folders['Sent'].add(mime(f'Note {n}', USER, 'x@client.test', f'Hi,\n\nnote {n}\n\n--\n{signature}',
                                                 f'<s{n}@acme.test>', when(2)), when(2))
        bodies = smtp_mail.sent_bodies(self.config, sources.credential, self.account)
        self.assertEqual(len(bodies), 3)
        self.assertIn('Acme Labs', bodies[0])
        self.assertNotIn('<script', ''.join(bodies))

    def test_a_mailbox_that_sends_says_so_on_its_card(self):
        self.assertTrue(next_actions.mail_account(self.account))
        self.assertTrue(sources.mail_account(self.account))
        self.assertFalse(next_actions.mail_account({**self.account, 'smtp_refused': True}))
        self.assertFalse(next_actions.mail_account({k: v for k, v in self.account.items() if k != 'smtp_host'}))
        import assistant
        self.assertEqual(assistant.connector_says(self.account, 'imap').get('acts'), 'send')
        self.assertEqual(sources.mailbox_name(self.config, {'account_id': self.account['id']}), 'Your mail server')


class StartTlsSending(Sending):
    smtp_mode = 'starttls'

    def test_auth_only_after_tls(self):
        self.send()
        self.assertTrue(all(tls for verb, tls in self.smtp.commands if verb in ('AUTH', 'MAIL', 'RCPT', 'DATA')))


class ServerQuirks(SmtpBase):
    """How the servers mail hosts run sign in (checked against them: most offer PLAIN and LOGIN, some LOGIN first,
    some CRAM-MD5 too), and a Sent folder on a cPanel-style server with no SPECIAL-USE."""
    def test_a_server_with_only_auth_login_signs_in(self):
        self.smtp.auth = ['LOGIN']
        self.assertEqual(self.send(), {'message_id': 's1700000001-1'})
        self.assertEqual(set(self.smtp.auths), {'LOGIN'})  # the check before the send, and the send

    def test_plain_is_used_when_offered_whatever_the_order(self):
        self.smtp.auth = ['CRAM-MD5', 'LOGIN', 'PLAIN']
        smtp_mail.check(self.config, sources.credential, self.account)
        self.assertEqual(self.smtp.auths, ['PLAIN'])

    def test_a_wrong_password_is_tried_once_not_once_per_method(self):
        # smtplib's own login tries every method on offer: three failed sign-ins for one wrong password, and shared
        # hosting locks the address after a few
        self.smtp.auth = ['CRAM-MD5', 'PLAIN', 'LOGIN']
        with self.assertRaises(smtp_mail.SmtpError) as caught:
            smtp_mail.check(self.config, None, self.account, 'pw-Wrong-0000')
        self.assertEqual(caught.exception.category, 'smtp_auth_failed')
        self.assertEqual(self.smtp.auths, ['PLAIN'])

    def test_a_non_ascii_password_over_auth_login(self):
        self.smtp.auth, self.smtp.users = ['LOGIN'], {USER: 'pw-Zoë-7731'}
        smtp_mail.check(self.config, None, self.account, 'pw-Zoë-7731')
        self.assertEqual(self.smtp.auths, ['LOGIN'])

    def test_the_copy_goes_in_inbox_sent_without_special_use(self):
        self.server.delimiter, self.server.special_use = '.', False
        self.server.folders = {'INBOX': self.server.folders['INBOX'], 'INBOX.Drafts': Folder(1700000005),
                               'INBOX.Sent': self.server.folders['Sent']}
        self.account.pop('sent_folder')
        self.assertEqual(self.send(), {'message_id': 's1700000001-1'})
        self.assertEqual(len(self.server.folders['INBOX.Sent'].messages), 1)
        self.assertEqual(self.server.folders['INBOX.Drafts'].messages, {})

    def test_a_pinned_certificate_on_this_computer(self):
        with open(self.cert[0], encoding='ascii') as pem:
            pin = imap_mail.fingerprint(ssl.PEM_cert_to_DER_cert(pem.read()))
        self.account.update(smtp_tls_pin=pin)
        smtp_mail.check(self.config, sources.credential, self.account)
        self.account.update(smtp_tls_pin=':'.join(['00'] * 32))  # another certificate: say Bridge was reinstalled
        with self.assertRaises(smtp_mail.SmtpError) as caught:
            smtp_mail.check(self.config, sources.credential, self.account)
        self.assertEqual(caught.exception.category, 'smtp_tls_failed')
        self.assertEqual(self.smtp.auths, ['PLAIN'])  # only the first, pinned one signed in: the password never went to the other


class PlainSmtp(SmtpBase):
    smtp_mode = 'plain'

    def setUp(self):
        super().setUp()
        self.account['smtp_security'] = 'starttls'  # asks for STARTTLS; the server has none on offer

    def test_no_tls_on_offer_sends_nothing_and_never_signs_in(self):
        with self.assertRaises(ValueError) as caught:
            self.transport.preflight(self.action())
        self.assertEqual(str(caught.exception), smtp_mail.STOPPED['smtp_tls_failed'])
        self.assertNotIn('AUTH', [verb for verb, _ in self.smtp.commands])
        self.assertEqual(self.transport.send(self.action(), {'rfc_message_id': '<m3@acme.test>'}), {'not_sent': True})
        self.assertEqual(self.smtp.received, [])


class Drafts(unittest.TestCase):
    """A draft from an Other email mailbox: its thread ids pass, and its thread is never moved (no snooze)."""
    def test_reply_draft(self):
        account = {'id': 'acme-imap', 'service': 'imap', 'transport': 'imap', 'email': USER, 'boundary': 'work:Acme',
                   'smtp_host': 'smtp.acme.test'}
        config = {'accounts': [account]}
        value = {'kind': 'email', 'account_id': 'acme-imap', 'to': ['sam@client.test'], 'subject': 'Re: Pilot',
                 'body': 'Hi Sam,\n\nYes.\n\nAlex', 'thread_id': 't' + '0' * 24, 'in_reply_to': '<q1@client.test>',
                 'snooze_days': 3}
        result = next_actions.validate(value, config, {'acme-imap'})
        self.assertEqual((result['from'], result['thread_id']), (USER, 't' + '0' * 24))
        self.assertNotIn('snooze_days', result)
        self.assertNotIn('from_options', next_actions.validate(value, config, {'acme-imap'}, senders={'acme-imap': ['me@alias.test']}))


if __name__ == '__main__':
    unittest.main()
