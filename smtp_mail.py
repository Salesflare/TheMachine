"""Sending from any IMAP mailbox (Other email, imap_mail.py): the email the owner approved goes out through the
mailbox's own SMTP server, and a copy goes in its Sent folder, as any mail app does. next_actions.EmailTransport hands
an Other email send here (preflight, send); everything else about it (approval, admission, the one-send rule) is the
same as for Gmail and Outlook.

Python's own smtplib, nothing to install. Same rules as imap_mail.py: the password comes from the account's credential
file and is only ever sent to the server, over TLS (implicit TLS on 465, or STARTTLS), never plaintext; certificates
are verified except on this computer itself. Errors are fixed, content-free labels: what the server said is matched,
never kept. The greeting names no computer ([127.0.0.1]), so the owner's computer name never reaches a mail server.

What a server's answer means for the one-send rule: a refusal before the message went (sender, every recipient, or
the message itself with a 5xx code) is a definite "nothing was sent" (rejected); a temporary refusal (4xx) or no
connection before the message went is "not sent, try again shortly"; a connection lost while the message was going is
unknown, never sent again (the Sent folder is checked for it, as for Gmail)."""
import base64
import email
import email.policy
import imaplib
import re
import smtplib
import socket
import ssl
import time

import imap_mail

SECURITY = imap_mail.SECURITY
TIMEOUT = 60  # seconds per server answer; a big attachment takes a while
GREETING = '[127.0.0.1]'
FILED_WAITS = (2, 3)  # seconds to wait for a server that files sent mail itself, before filing a copy


class SmtpError(Exception):
    """A content-free label, like imap_mail.ImapError: never what the server said, and never the password."""
    def __init__(self, category, status=None):
        self.category, self.status = category, status
        super().__init__(category + (f':{status}' if status else ''))


def settings(account):
    """(host, port, security, username) of the account's SMTP server; a plaintext one is refused."""
    security = str(account.get('smtp_security') or 'starttls').lower()
    if security not in SECURITY:
        raise SmtpError('smtp_plaintext_refused')
    host = str(account.get('smtp_host') or '').strip().lower()
    if not host or not re.fullmatch(r'[a-z0-9.:\[\]-]+', host):
        raise SmtpError('smtp_not_configured')
    try:
        port = int(account.get('smtp_port') or (465 if security == 'ssl' else 587))
    except (TypeError, ValueError):
        raise SmtpError('smtp_not_configured') from None
    if not 0 < port < 65536:
        raise SmtpError('smtp_not_configured')
    return host, port, security, str(account.get('username') or account.get('email') or '')


def sends(account):
    """An Other email mailbox that sends: its SMTP server is set, and signing in to it didn't fail at setup."""
    return account.get('service') == 'imap' and bool(account.get('smtp_host')) and not account.get('smtp_refused')


def failure(error):
    """An SmtpError for what went wrong before the message went. The server's words are never kept."""
    if isinstance(error, SmtpError):
        return error
    if isinstance(error, smtplib.SMTPAuthenticationError):
        return SmtpError('smtp_auth_failed', 401)
    if isinstance(error, smtplib.SMTPNotSupportedError):
        return SmtpError('smtp_tls_failed' if 'STARTTLS' in str(error).upper() else 'smtp_no_auth')
    if isinstance(error, (socket.timeout, TimeoutError)):
        return SmtpError('timeout')
    if isinstance(error, ssl.SSLError):
        return SmtpError('smtp_tls_failed')
    if isinstance(error, smtplib.SMTPResponseException):
        return SmtpError('smtp_unavailable' if 400 <= error.smtp_code < 500 else 'smtp_refused', error.smtp_code)
    if isinstance(error, smtplib.SMTPServerDisconnected):
        return SmtpError('smtp_network')
    if isinstance(error, (socket.gaierror, ConnectionError, OSError, smtplib.SMTPException)):
        return SmtpError('smtp_unreachable')
    return SmtpError('smtp_failed')


def _plain(conn, username, password):
    """AUTH PLAIN in UTF-8: smtplib's own only takes ASCII names and passwords."""
    secret = b'\0' + username.encode() + b'\0' + password.encode()
    code, _ = conn.docmd('AUTH', 'PLAIN ' + base64.b64encode(secret).decode())
    if code != 235:
        raise smtplib.SMTPAuthenticationError(code, b'')


def connect(account, password):
    """A connection over TLS, signed in. Raises SmtpError."""
    host, port, security, username = settings(account)
    if not password:
        raise SmtpError('smtp_password_missing')
    context, conn = imap_mail.tls_context(host), None
    try:
        if security == 'ssl':
            conn = smtplib.SMTP_SSL(host, port, local_hostname=GREETING, timeout=TIMEOUT, context=context)
            conn.ehlo()
        else:
            conn = smtplib.SMTP(host, port, local_hostname=GREETING, timeout=TIMEOUT)
            conn.ehlo()
            if not conn.has_extn('starttls'):  # no STARTTLS on offer: refused, never sent in plaintext
                raise SmtpError('smtp_tls_failed')
            conn.starttls(context=context)
            conn.ehlo()
        if not conn.has_extn('auth'):
            raise SmtpError('smtp_no_auth')
        if username.isascii() and password.isascii():
            conn.login(username, password)
        else:
            _plain(conn, username, password)
    except Exception as error:  # noqa: BLE001 - every way it fails is mapped
        close(conn)
        raise failure(error) from None
    return conn


def close(conn):
    if conn is None:
        return
    try:
        conn.quit()
    except Exception:  # noqa: BLE001 - it is going away anyway
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass


def password_of(config, credential, account):
    try:
        return credential(config, account['credential']) if account.get('credential') else ''
    except (OSError, KeyError):
        raise SmtpError('smtp_password_missing') from None


def check(config, credential, account, password=None):
    """Sign in to the SMTP server and leave. Raises SmtpError."""
    close(connect(account, password if password is not None else password_of(config, credential, account)))


def without_bcc(data):
    """The message as it goes out: Bcc recipients get it, but nobody sees them (the Sent copy keeps them)."""
    message = email.message_from_bytes(data, policy=email.policy.SMTP)
    if 'Bcc' not in message:
        return data
    del message['Bcc']
    return message.as_bytes()


def deliver(config, credential, account, sender, recipients, data):
    """Hand the message to the server: {'accepted': True}, {'rejected': code}, {'not_sent': True} or {} (unknown)."""
    try:
        conn = connect(account, password_of(config, credential, account))
    except SmtpError as error:
        # Nothing went out. A refused password is a refusal (an hour of retries could lock the account); the rest
        # tries again shortly.
        return {'rejected': 535} if error.category == 'smtp_auth_failed' else {'not_sent': True}
    went = False
    try:
        options = ['SMTPUTF8'] if not (sender.isascii() and all(r.isascii() for r in recipients)) else []
        if options and not conn.has_extn('smtputf8'):
            return {'rejected': 553}  # an address the server can't carry
        code, _ = conn.mail(sender, options)
        if code != 250:
            return refusal(code)
        accepted, last = 0, None
        for address in recipients:
            code, _ = conn.rcpt(address)
            if code in (250, 251):
                accepted += 1
            else:
                last = code
        if not accepted:
            return refusal(last)
        went = True
        code, _ = conn.data(without_bcc(data))  # raises SMTPDataError with the server's code when it refuses
        return {'accepted': True} if code == 250 else refusal(code)
    except smtplib.SMTPResponseException as error:
        return refusal(error.smtp_code)  # the server answered: it did not take the message
    except Exception:  # noqa: BLE001 - lost while the message was going: unknown, never sent again
        return {} if went else {'not_sent': True}
    finally:
        close(conn)


def refusal(code):
    if code and 500 <= code < 600:
        return {'rejected': code}
    return {'not_sent': True}


def _find_sent(session, account, rfc_message_id):
    validity, _ = imap_mail.examine(session, account, 's')
    uids = imap_mail._uids(session.conn.uid('search', 'HEADER', 'Message-ID', imap_mail._search_words(rfc_message_id)))
    return f's{validity}-{uids[-1]}' if uids else None


def file_sent(config, credential, account, data, rfc_message_id):
    """Put the sent message in the Sent folder, unless the server already did (many do): its id there, or None when
    the mailbox has no Sent folder or it couldn't be filed. The only change The Machine makes in an IMAP mailbox."""
    if not rfc_message_id.isascii():
        return None
    try:
        with imap_mail._Use(config, credential, account) as session:
            folder = imap_mail.folders(session, account).get('s')
            if not folder:
                return None
            found = _find_sent(session, account, rfc_message_id)
            for wait in FILED_WAITS:
                if found:
                    return found
                time.sleep(wait)
                found = _find_sent(session, account, rfc_message_id)
            if found:
                return found
            imap_mail._ok(session.conn.append(imap_mail._quote(folder), '(\\Seen)', imaplib.Time2Internaldate(time.time()), data))
            return _find_sent(session, account, rfc_message_id)
    except Exception:  # noqa: BLE001 - it went: a missing Sent copy never makes it unsent
        return None


def sent_bodies(config, credential, account, count=10):
    """The HTML of the last sent messages (plain text as HTML), for finding the signature they end with, as
    ms_graph.sent_bodies does for Outlook."""
    import html  # noqa: PLC0415 - only here
    out = []
    try:
        with imap_mail._Use(config, credential, account) as session:
            if not imap_mail.folders(session, account).get('s'):
                return out
            _, upcoming = imap_mail.examine(session, account, 's')
            uids = imap_mail._uids(session.conn.uid('search', 'UID', f'{max(1, upcoming - 300)}:*'))[-count:]
            for uid in reversed(uids):
                row = imap_mail.parse_fetch(imap_mail._ok(session.conn.uid('fetch', str(uid), '(UID BODY.PEEK[])'))).get(uid)
                message = email.message_from_bytes(b''.join(row['bytes']) if row else b'', policy=email.policy.default)
                part = message.get_body(('html', 'plain'))
                if part is None:
                    continue
                text = part.get_content()
                out.append(text if part.get_content_subtype() == 'html' else html.escape(text).replace('\n', '<br>\n'))
    except imap_mail.ImapError:
        raise
    except Exception as error:  # noqa: BLE001
        raise imap_mail.failure(error) from None
    return out


# Why a send was stopped before anything went (EmailTransport.preflight): shown on the to-do, in the owner's language.
STOPPED = {
    'smtp_auth_failed': 'The mail server refused the password for sending. Nothing was sent; connect the mailbox again.',
    'smtp_password_missing': 'The mail server refused the password for sending. Nothing was sent; connect the mailbox again.',
    'smtp_tls_failed': 'Couldn’t make a secure connection to the mail server. Nothing was sent.',
    'smtp_no_auth': 'The mail server doesn’t let mail apps sign in to send. Nothing was sent.',
    'smtp_not_configured': 'This mailbox has no mail server for sending. Nothing was sent; connect it again.',
    'smtp_plaintext_refused': 'This mailbox has no mail server for sending. Nothing was sent; connect it again.',
}
UNREACHABLE = 'Couldn’t reach the mail server. Nothing was sent; try again in a minute.'


def preflight(transport, action, account):
    """Right before admission: the files are there, the signature is loaded and the server takes the password."""
    import i18n  # noqa: PLC0415
    import next_actions  # noqa: PLC0415 - next_actions hands sends here
    for record in action.get('attachments', []):
        try:
            next_actions.attachment_bytes(record, transport.config)
        except OSError:
            raise ValueError(f"The attachment {record['name']} is missing. Nothing was sent.") from None
    try:
        check(transport.config, transport.credential, account)
    except SmtpError as error:
        raise ValueError(i18n.t(STOPPED.get(error.category, UNREACHABLE))) from None
    if action.get('signature'):
        transport.signatures.pop(action['from'].lower(), None)  # read fresh: the owner may have changed it
        transport.signature(action, account)


def send(transport, action, job, account):
    """The one send: the message goes to every To, Cc and Bcc address, then a copy is filed in Sent."""
    import next_actions  # noqa: PLC0415
    data = next_actions.mime_bytes(action, job, transport.signature(action, account), transport.config)
    result = deliver(transport.config, transport.credential, account, action['from'],
                     [*action['to'], *action.get('cc', []), *action.get('bcc', [])], data)
    if not result.get('accepted'):
        return result
    filed = file_sent(transport.config, transport.credential, account, data, job['rfc_message_id'])
    return {'message_id': filed or 'smtp:' + job['rfc_message_id']}
