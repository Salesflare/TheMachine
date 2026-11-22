"""The link in a password manager's "verify export" email, for an export the Machine is running (login_import._verify).

LastPass emails a link to confirm each export started on its vault, and waits for it before it exports. While an export
the owner started on the dashboard waits there, and only for VERIFY_SECONDS after the guide's click that started it,
link() reads the owner's own connected mailboxes (the reads they already have: Gmail, Outlook or IMAP through
sources.gog_read, nothing new asked) for the newest mail since that click from the manager's own domain, with its
subject, passing the mailbox's sender checks when the mailbox records them (Authentication-Results), and answers its
https link on the manager's own hosts whose path is the manager's verify link (never judged by its words or query).
Nothing of a mail is kept, logged or answered but that one link, and login_import opens it once per export, in the
export's own browser. An export started anywhere else never gets here:
without a running export and its click there is no `since`, so no mail is read and nothing is opened.
"""
from __future__ import annotations

import base64
import email.utils
import html.parser
import re
import urllib.parse

import login_export_guide
import own_addresses
import sources

SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
LIMIT = 20  # mails since the click looked at per mailbox
VERIFY_SECONDS = 600  # LastPass's link expires after 10 minutes
EARLY = 30  # seconds a mail may be stamped before the click: LastPass mails while the click is still being sent


class _Links(html.parser.HTMLParser):
    """Each link in an HTML body with its words: [(href, words)]."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self._at = [], None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self._at = [dict(attrs).get('href') or '', []]
            self.found.append(self._at)

    def handle_data(self, data):
        if self._at is not None:
            self._at[1].append(data)

    def handle_endtag(self, tag):
        if tag == 'a':
            self._at = None


def _bodies(payload):
    """(html parts, text parts) of a message in Gmail's shape, decoded."""
    out = {'text/html': [], 'text/plain': []}

    def walk(part, depth=0):
        if not isinstance(part, dict) or depth > 8:
            return
        data = (part.get('body') or {}).get('data')
        if part.get('mimeType') in out and isinstance(data, str):
            try:
                out[part['mimeType']].append(base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)).decode('utf-8', 'replace'))
            except ValueError:
                pass
        for child in part.get('parts') or ():
            walk(child, depth + 1)

    walk(payload)
    return out['text/html'], out['text/plain']


def _authenticated(headers, verify):
    """The mailbox's own sender checks, when it records them: a DKIM or DMARC pass for the manager's domain. A mailbox
    that records none (some IMAP servers) is judged by the sender's address alone."""
    results = [v for k, v in headers if k == 'authentication-results']
    if not results:
        return True
    for value in results:
        for found in re.finditer(r'\b(dkim|dmarc)=pass\b[^;]*?\bheader\.(?:d|i|from)=@?([a-z0-9.-]+)', value, re.I):
            if re.search(verify['from'], found[2].lower()):
                return True
    return False


def pick(message, manager, since):
    """A message's verification link when it is the manager's verify email that came after `since` (seconds since
    the epoch), else None: (when it came in, ms; the link)."""
    verify = (login_export_guide.RECIPES.get(manager) or {}).get('verify')
    if not verify or not isinstance(message, dict) or not isinstance(since, (int, float)):
        return None
    try:
        came = int(message.get('internalDate'))
    except (TypeError, ValueError):
        return None
    if came < (since - EARLY) * 1000:
        return None
    payload = message.get('payload') or {}
    headers = [(str(h.get('name', '')).lower(), str(h.get('value', ''))) for h in payload.get('headers') or () if isinstance(h, dict)]
    sender = email.utils.parseaddr(next((v for k, v in headers if k == 'from'), ''))[1].lower()
    domain = sender.rpartition('@')[2]
    subject = next((v for k, v in headers if k == 'subject'), '')
    if '@' not in sender or not re.search(verify['from'], domain) or not re.search(verify['subject'], subject, re.I):
        return None
    if not _authenticated(headers, verify):
        return None
    html_parts, text_parts = _bodies(payload)
    links = []
    for part in html_parts:
        reader = _Links()
        try:
            reader.feed(part)
        except (ValueError, AssertionError):
            continue
        links += [href.strip() for href, _ in reader.found]
    for part in text_parts:
        links += re.findall(r'https://[^\s<>"\')\]]+', part)
    # only a link whose path is the manager's verify link (LastPass: /export-tokens/<token>/approve); its words and query
    # never count (the mail's logo link carries "Verifyexport" in its query). None: the owner confirms by hand.
    for href in links:
        if login_export_guide.allowed(manager, href) and re.search(verify['path'], urllib.parse.urlsplit(href).path, re.I):
            return came, href
    return None


def link(config, manager, since, seen=None):
    """The newest verification link mailed since `since` to the owner's own mailboxes, or None. `seen`: ids of mails
    already looked at in this export (each is read once)."""
    if not isinstance(since, (int, float)) or not (login_export_guide.RECIPES.get(manager) or {}).get('verify'):
        return None
    seen = set() if seen is None else seen
    found = []
    for account in own_addresses.mail_accounts(config):
        try:
            listed = sources.gog_read(config, account, 'gmail', 'v1', 'gmail.users.messages.list',
                                      {'userId': 'me', 'q': 'after:%d' % int(since - EARLY), 'maxResults': LIMIT}, SCOPE)
        except (sources.SourceError, OSError, ValueError, KeyError, TypeError):
            continue
        for item in (listed.get('messages') or [])[:LIMIT] if isinstance(listed, dict) else ():
            key = (account.get('id'), item.get('id') if isinstance(item, dict) else None)
            if key[1] is None or key in seen:
                continue
            seen.add(key)
            try:
                message = sources.gog_read(config, account, 'gmail', 'v1', 'gmail.users.messages.get',
                                           {'userId': 'me', 'id': key[1], 'format': 'full'}, SCOPE)
            except (sources.SourceError, OSError, ValueError, KeyError, TypeError):
                seen.discard(key)
                continue
            got = pick(message, manager, since)
            if got:
                found.append(got)
    return max(found)[1] if found else None
