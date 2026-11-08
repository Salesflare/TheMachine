"""Work or Personal, checked against the mail once it is in. When + Add had to ask (an address on its own domain, which
people use for personal mail too) or a sign-in from the account page had to guess Personal in doubt, the account is
marked scope_check (onboarding.connect, connect_grant). Once its mail is read, the people the owner writes to say
which it is: mostly at mail providers is personal mail, at several companies and none at a mail provider is work mail,
writing to Work Fleet teammates is work mail. When that clearly says the other, the setup to-do gets one row, "<address>
looks like work mail. Change it?" (setup_hints_view): Change sets it (connect_scope, which restarts to apply it) and
closes the row, its × closes it; either way it never comes back (milestone setup:hint-scope-<key>). Never a switch by
itself: sharing follows Work. From the senders and recipients the Machine keeps in the clear (message_seal.PLAIN_METADATA),
no message text and no model call."""
from __future__ import annotations

import email.utils
import hashlib

import i18n

SENT_LOOKED_AT = 40   # the owner's newest sent messages in this mailbox looked at
ROWS_LOOKED_AT = 600  # the newest messages read to find them
ENOUGH = 5            # people written to (outside the address's own domain) before the mail says anything
PERSONAL_SHARE = 0.7  # this share of them at a mail provider: personal mail
WORK_SHARE = 0.1      # at most this share at a mail provider, and WORK_DOMAINS companies or more: work mail
WORK_DOMAINS = 3
MAIL_SERVICES = ('gmail', 'outlook')


def hint_id(account):
    """The setup to-do row's id for this account: short and of the letters a row id may have, whatever the account id."""
    return 'scope-' + hashlib.sha256(str(account.get('id')).encode()).hexdigest()[:10]


def _domain(address):
    return address.rpartition('@')[2].lower().rstrip('.')


def people_written_to(db, account):
    """The addresses the owner wrote to from this mailbox, in their newest SENT_LOOKED_AT messages there."""
    own = str(account.get('email') or '').strip().lower()
    rows = db.execute("SELECT json_extract(metadata,'$.from'),json_extract(metadata,'$.to') FROM events WHERE account_id=? "
                      "AND kind='gmail.message' AND deleted=0 ORDER BY occurred_at DESC LIMIT ?", (account.get('id'), ROWS_LOOKED_AT))
    found, sent = set(), 0
    for sender, to in rows:
        if email.utils.parseaddr(str(sender or ''))[1].lower() != own:
            continue
        found |= {a.lower() for _, a in email.utils.getaddresses([str(to or '')]) if '@' in a}
        sent += 1
        if sent >= SENT_LOOKED_AT:
            break
    return found - {own}


def mailbox_says(account, people, team_domains=()):
    """'work', 'personal' or None (not clear) from the people written to: the address's own domain left out (colleagues
    there, or family on a family domain, say nothing either way)."""
    from work_or_personal import company_of
    home = _domain(str(account.get('email') or ''))
    outside = {p for p in people if _domain(p) != home}
    if len(outside) < ENOUGH:
        return None
    providers = [p for p in outside if not company_of(p)]
    share = len(providers) / len(outside)
    teams = {str(d).lower() for d in team_domains}
    if share >= PERSONAL_SHARE:
        return 'personal'
    companies = {_domain(p) for p in outside} - {_domain(p) for p in providers}
    if share <= WORK_SHARE and (len(companies) >= WORK_DOMAINS or companies & teams):
        return 'work'
    return None


def scope_hints(store, config, team_domains=()):
    """[{id, title, text, button, scope: {account, boundary}}]: a setup to-do row for each mailbox marked scope_check whose
    mail clearly says the other of what it is set to, and whose row wasn't closed."""
    from work_or_personal import company_of
    hints = []
    accounts = [a for a in config.get('accounts') or [] if isinstance(a, dict) and a.get('scope_check') and not a.get('shared')
                and a.get('service') in MAIL_SERVICES and str(a.get('boundary') or '').startswith(('work:', 'personal:'))]
    if not accounts:
        return hints
    with store.connect() as db:
        closed = {r[0][len('setup:hint-'):] for r in db.execute("SELECT name FROM milestones WHERE name LIKE 'setup:hint-scope-%'")}
        for account in accounts:
            if hint_id(account) in closed:
                continue
            says = mailbox_says(account, people_written_to(db, account), team_domains)
            work = str(account['boundary']).startswith('work:')
            if says == 'work' and not work:
                target = 'work:' + (company_of(account['email']) or 'Main')
                title = i18n.t('{} looks like work mail. Change it to Work?', account['email'])
            elif says == 'personal' and work:
                target, title = 'personal:me', i18n.t('{} looks like personal mail. Change it to Personal?', account['email'])
            else:
                continue
            hints.append({'id': hint_id(account), 'title': title, 'text': '', 'button': i18n.t('Change'),
                          'scope': {'account': account['id'], 'boundary': target}})
    return hints
