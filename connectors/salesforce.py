"""Salesforce CRM: what changed in the owner's Salesforce, as signals, the way Salesflare's connector brings in its
CRM (machine/sources/salesflare.py).

- Opportunities: a new one, and each change of its stage or amount (salesforce.opportunity). Each goes onto a Graph
  project named after the opportunity, with its account as the organization and its contact roles as people.
- Tasks: open tasks assigned to the owner (salesforce.task), which a review can turn into to-dos, and when one is done.
- Recent activity: calls and other tasks logged as done with notes, and meetings with a description
  (salesforce.activity). Emails the owner logged are left out: their own mail already comes in from Gmail or Outlook.
- Accounts and contacts: the context on each signal (crm_account, contacts, like Salesflare's), and the job titles and
  phone numbers of the contacts on what was kept, as a record about them (enrichment.RECORD).

Writes: only with Update contact details on (the card's switch, off by default, shown as a preview first): a PATCH of a
Contact's job title, phone or LinkedIn field, planned by crm_sync.py (its rules: newer, only what changed, never a
blank, never the email or account). Nothing else is ever written: no other object, method or field.

The sign-in is the owner's own (OAuth web server flow with PKCE, scopes api and refresh_token) through The Machine's
Salesforce app at a token broker (a hosting control plane, like Zoom's); the refresh token lives on this Machine only
(mail_grants.py) and is sent along for each short-lived access token. The broker answers POST {"email",
"refresh_token"} with {"access_token", "instance_url", "expires_in"?, "refresh_token"?}:

    "salesforce_broker": {"url": "https://app.example.com/api/salesforce/token"},
    "credentials": {"salesforce-broker": "~/.local/share/personal-assistant/google-broker"}

API calls go only to the org's own instance (https://<domain>.my.salesforce.com, or another *.salesforce.com or
*.force.com host the broker names), each on the allowlist in Source.get and Source.update.
"""
import datetime as dt
import http.client
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

KINDS = {'salesforce.opportunity': 'CRM deal', 'salesforce.task': 'CRM task', 'salesforce.activity': 'CRM activity'}
SETUP = {
    'label': 'Salesforce',
    'account': {'id': 'salesforce', 'service': 'salesforce', 'transport': 'broker', 'boundary': 'work', 'poll_seconds': 900},
    'what': 'Deals, tasks and activity from Salesforce, on people and projects.',
    'group': 'customers',
    'note': 'Salesforce is connected with Connect Salesforce on your setup page, which signs in with your own Salesforce '
            'account. It needs a Salesforce sign-in broker (salesforce_broker in config.json).',
    'ask': [('email', 'Your Salesforce sign-in address')],
    'broker': True,  # signed in at the hosting control plane, not here
    'hints': {'salesforce_signin_expired': 'Salesforce asks you to connect again',
              'salesforce_broker_not_configured': 'Salesforce needs a sign-in broker',
              'salesforce_http:HTTP_403': 'Salesforce refused: your user needs API access (API Enabled)'}}
VERSION = 'v62.0'
API = f'/services/data/{VERSION}'
HOSTS = re.compile(r'[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:salesforce|force)\.com')
READS = (r'/services/oauth2/userinfo', API + r'/query', API + r'/query/[0-9A-Za-z]{15,18}-[0-9]{1,7}',
         API + r'/sobjects/Contact/describe')
CONTACT = re.compile(r'003[0-9A-Za-z]{12}(?:[0-9A-Za-z]{3})?')
ID = re.compile(r'[0-9A-Za-z]{15}(?:[0-9A-Za-z]{3})?')
WRITABLE = {'title': 'Title', 'phone': 'Phone'}  # plus the org's own LinkedIn field, when it has one (linkedin_field)
PAGE = 200            # rows of each object a run reads; more waits for the next run (more)
OVERLAP = dt.timedelta(minutes=10)
DEALS_KEEP = 3000
CONTACT_SYNC_HOURS = 6  # Update contact details looks at most this often
DESCRIBE_HOURS = 24
BODY = 20000
_tokens = {}
_lock = threading.Lock()


def broker_token(config, account, helpers, fresh=False):
    """(access token, instance url) through the broker, sending the sign-in kept here and keeping a rotated one."""
    import mail_grants
    email = str(account.get('email') or '').strip().lower()
    if not email:
        raise helpers.SourceError('salesforce_no_email')
    with _lock:
        hit = _tokens.get(email)
        if hit and not fresh and hit[2] > time.monotonic():
            return hit[0], hit[1]
        url = (config.get('salesforce_broker') or {}).get('url')
        if not url or not str(url).startswith('https://'):
            raise helpers.SourceError('salesforce_broker_not_configured')
        try:
            kept = mail_grants.get(config, 'salesforce', email)
        except mail_grants.GrantError:
            raise helpers.SourceError('salesforce_signin_unreadable') from None
        if not kept:
            raise helpers.SourceError('salesforce_signin_expired')
        try:
            secret = helpers.credential(config, 'salesforce-broker')
        except Exception:
            raise helpers.SourceError('salesforce_broker_credential') from None
        request = urllib.request.Request(url, method='POST', data=json.dumps({'email': email, 'refresh_token': kept}).encode(),
                                         headers={'Authorization': 'Bearer ' + secret.strip(), 'Content-Type': 'application/json',
                                                  'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                answer = json.loads(response.read(200_000))
        except urllib.error.HTTPError as error:
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            error.close()
            if error.code in (401, 404):
                raise helpers.SourceError('salesforce_signin_expired', error.code) from None
            raise helpers.SourceError('salesforce_broker', error.code, retry_after=int(retry) if retry.isdigit() else None) from None
        except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException):
            raise helpers.SourceError('salesforce_broker_unreachable') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        instance = instance_url(answer.get('instance_url') if isinstance(answer, dict) else None)
        if not isinstance(access, str) or not access or not instance:
            raise helpers.SourceError('salesforce_broker')
        rotated = answer.get('refresh_token')
        if isinstance(rotated, str) and rotated and rotated != kept:
            mail_grants.rotate(config, 'salesforce', email, kept, rotated)
        # Salesforce doesn't say how long an access token lasts (the org's session timeout, 2 hours by default)
        _tokens[email] = (access, instance, time.monotonic() + min(max(int(answer.get('expires_in') or 1800) - 120, 60), 1800))
        return access, instance


def instance_url(value):
    """The org's own https address, or None when it isn't a Salesforce host: the token never goes anywhere else."""
    parts = urllib.parse.urlsplit(str(value or ''))
    host = (parts.hostname or '').lower()
    if parts.scheme != 'https' or not HOSTS.fullmatch(host) or parts.port not in (None, 443) or parts.username:
        return None
    return 'https://' + host


def quoted(value):
    """A SOQL string literal."""
    return "'" + str(value).replace('\\', '\\\\').replace("'", "\\'") + "'"


def soql_time(stamp):
    return stamp.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value or '').replace('Z', '+00:00').replace('+0000', '+00:00'))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


class Source:
    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers

    def send(self, method, path, params=None, body=None):
        for attempt in (0, 1):
            token, instance = broker_token(self.config, self.account, self.helpers, fresh=bool(attempt))
            url = instance + path + ('?' + urllib.parse.urlencode(params) if params else '')
            request = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                             headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json',
                                                      'Content-Type': 'application/json', 'User-Agent': 'TheMachine/1'})
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read(20_000_000)
                return json.loads(raw) if raw.strip() else None
            except urllib.error.HTTPError as error:
                retry = error.headers.get('Retry-After', '') if error.headers else ''
                error.close()
                if error.code == 401 and not attempt:
                    continue  # the session ended early: one fresh token
                delay = min(3600, max(1, int(retry))) if retry.isdigit() else (900 if error.code == 403 else None)
                raise self.helpers.SourceError('salesforce_http', error.code, retry_after=delay) from None
            except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
                raise self.helpers.SourceError('salesforce_network') from None
            except (ValueError, UnicodeError):
                raise self.helpers.SourceError('salesforce_invalid_json') from None
        raise self.helpers.SourceError('salesforce_http', 401)

    def get(self, path, params=None):
        """One GET on the read allowlist (READS). Never another path."""
        if not any(re.fullmatch(route, path) for route in READS):
            raise self.helpers.SourceError('salesforce_unsupported_read')
        return self.send('GET', path, params)

    def query(self, soql, limit=PAGE):
        """The rows of one SOQL query, following its next pages up to limit."""
        found, page = [], self.get(API + '/query', {'q': soql})
        while isinstance(page, dict):
            found += [r for r in page.get('records') or [] if isinstance(r, dict)]
            following = page.get('nextRecordsUrl')
            if page.get('done', True) or not following or len(found) >= limit:
                break
            page = self.get(str(following))
        if not isinstance(page, dict):
            raise self.helpers.SourceError('salesforce_invalid_page')
        return found[:limit]

    def update(self, contact_id, fields):
        """The one write: a Contact's job title, phone or the org's LinkedIn field (linkedin), with a value each."""
        allowed = set(WRITABLE.values()) | ({self.account.get('linkedin_field')} - {None})
        if not CONTACT.fullmatch(str(contact_id)) or not fields or set(fields) - allowed \
                or any(not isinstance(v, str) or not v.strip() for v in fields.values()):
            raise self.helpers.SourceError('salesforce_unsupported_write')
        return self.send('PATCH', f'{API}/sobjects/Contact/{contact_id}', body=fields)

    def me(self):
        found = self.get('/services/oauth2/userinfo')
        if not isinstance(found, dict) or not ID.fullmatch(str(found.get('user_id') or '')):
            raise self.helpers.SourceError('salesforce_invalid_user')
        return found


def domain_of(website):
    host = urllib.parse.urlsplit(website if '//' in str(website or '') else '//' + str(website or '')).hostname or ''
    host = host.lower().removeprefix('www.')
    return host if re.fullmatch(r'(?:[a-z0-9-]+\.)+[a-z]{2,24}', host) else ''


def crm_account(row):
    account = row.get('Account') if isinstance(row.get('Account'), dict) else None
    if not account or not row.get('AccountId'):
        return None
    return {'id': str(row['AccountId']), 'name': str(account.get('Name') or ''), 'domain': domain_of(account.get('Website'))}


def person(found, role=None):
    if not isinstance(found, dict) or '@' not in str(found.get('Email') or ''):
        return None
    return {'id': str(found.get('Id') or ''), 'name': str(found.get('Name') or ''), 'email': str(found['Email']).lower(),
            'role': str(found.get('Title') or '') or None, **({'crm_role': role} if role else {})}


def link(instance, record_id):
    return f'{instance}/lightning/r/{record_id}/view' if instance and ID.fullmatch(str(record_id or '')) else None


def money(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    return f'{value:,.0f}' if float(value).is_integer() else f'{value:,.2f}'


def opportunity_event(account, instance, row, before):
    """A new opportunity, or one whose stage or amount changed since `before` ({stage, amount}); None when neither."""
    stage, amount = str(row.get('StageName') or ''), row.get('Amount')
    if before and before.get('stage') == stage and before.get('amount') == amount:
        return None
    lines = [f"Stage: {stage}" + (f" (was {before['stage']})" if before and before.get('stage') != stage and before.get('stage') else '')]
    if amount is not None or (before and before.get('amount') is not None):
        lines.append(f"Amount: {money(amount) or 'none'}" + (f" (was {money(before.get('amount')) or 'none'})"
                                                              if before and before.get('amount') != amount else ''))
    if row.get('CloseDate'):
        lines.append(f"Close date: {row['CloseDate']}")
    org = crm_account(row)
    if org and org['name']:
        lines.append(f"Account: {org['name']}")
    owner = row.get('Owner') if isinstance(row.get('Owner'), dict) else {}
    if owner.get('Name'):
        lines.append(f"Owner: {owner['Name']}")
    roles = (row.get('OpportunityContactRoles') or {}).get('records') or [] if isinstance(row.get('OpportunityContactRoles'), dict) else []
    contacts = [p for p in (person(r.get('Contact'), r.get('Role')) for r in roles if isinstance(r, dict)) if p][:10]
    if contacts:
        lines.append('Contacts: ' + ', '.join(f"{c['name'] or c['email']}" + (f" ({c['crm_role']})" if c.get('crm_role') else '') for c in contacts))
    description = str(row.get('Description') or '').strip()
    body = '\n'.join(lines) + (f"\n\n{description}" if description else '')
    name = ' '.join(str(row.get('Name') or 'Opportunity').split())
    what = 'New deal' if not before else 'Deal moved' if before.get('stage') != stage else 'Deal amount changed'
    at = stamp(row.get('LastModifiedDate')) or stamp(row.get('SystemModstamp'))
    if not at or not ID.fullmatch(str(row.get('Id') or '')):
        raise ValueError('salesforce_invalid_opportunity')
    return {'account_id': account['id'], 'source_id': f"opportunity:{row['Id']}:{stage}:{amount}", 'kind': 'salesforce.opportunity',
            'occurred_at': at.isoformat(), 'title': f'{what}: {name}'[:1000], 'body': body[:BODY],
            'metadata': {'crm_account': org, 'contacts': contacts, 'opportunity_id': row['Id'], 'opportunity': name[:200],
                         'stage': stage, 'amount': amount, 'previous': before or None, 'close_date': row.get('CloseDate'),
                         'closed': bool(row.get('IsClosed')), 'won': bool(row.get('IsWon')),
                         'owner_email': str(owner.get('Email') or '').lower(), 'truncated': len(body) > BODY,
                         **({'source_url': link(instance, row['Id'])} if link(instance, row['Id']) else {})},
            'deleted': False}


def task_event(account, instance, row, me):
    """An open task of the owner's (salesforce.task, and once done, that it is), or a task done with notes
    (salesforce.activity). None for the rest, and for emails the owner logged (their own mail comes in already)."""
    mine = str(row.get('OwnerId') or '')[:15] == str(me or '')[:15]
    notes = str(row.get('Description') or '').strip()
    if row.get('TaskSubtype') == 'Email' and mine:
        return None
    if not mine and not (row.get('IsClosed') and notes):
        return None
    if mine and row.get('IsClosed') and not notes and not row.get('_was_open'):
        return None
    who = person(row.get('Who')) if isinstance(row.get('Who'), dict) and row['Who'].get('Type') in (None, 'Contact', 'Lead') else None
    kind = 'salesforce.task' if mine and (not row.get('IsClosed') or row.get('_was_open')) else 'salesforce.activity'
    at = stamp(row.get('CompletedDateTime')) if row.get('IsClosed') else None
    at = at or stamp(row.get('LastModifiedDate'))
    if not at or not ID.fullmatch(str(row.get('Id') or '')):
        raise ValueError('salesforce_invalid_task')
    what = row.get('What') if isinstance(row.get('What'), dict) else {}
    lines = [f"Status: {row.get('Status') or ''}"]
    if row.get('ActivityDate'):
        lines.append(f"Due: {row['ActivityDate']}")
    if who:
        lines.append(f"With: {who['name'] or who['email']}")
    if what.get('Name'):
        lines.append(f"About: {what['Name']}")
    owner = row.get('Owner') if isinstance(row.get('Owner'), dict) else {}
    if not mine and owner.get('Name'):
        lines.append(f"Logged by: {owner['Name']}")
    body = '\n'.join(lines) + (f"\n\n{notes}" if notes else '')
    return {'account_id': account['id'], 'source_id': 'task:' + row['Id'], 'kind': kind, 'occurred_at': at.isoformat(),
            'title': ' '.join(str(row.get('Subject') or 'Task').split())[:1000], 'body': body[:BODY],
            'metadata': {'crm_account': crm_account(row), 'contacts': [who] if who else [], 'task_id': row['Id'],
                         'status': row.get('Status'), 'due': row.get('ActivityDate'), 'closed': bool(row.get('IsClosed')),
                         'mine': mine, 'subtype': row.get('TaskSubtype'), 'about': what.get('Name'),
                         'opportunity_id': row.get('WhatId') if str(row.get('WhatId') or '').startswith('006') else None,
                         'truncated': len(body) > BODY, **({'source_url': link(instance, row['Id'])} if link(instance, row['Id']) else {})},
            'deleted': False}


def meeting_event(account, instance, row, me):
    """A meeting with a description (its notes), like Salesflare's meetings with notes."""
    notes = str(row.get('Description') or '').strip()
    if not notes:
        return None
    at = stamp(row.get('StartDateTime')) or stamp(row.get('ActivityDateTime'))
    if not at or not ID.fullmatch(str(row.get('Id') or '')):
        raise ValueError('salesforce_invalid_event')
    who = person(row.get('Who')) if isinstance(row.get('Who'), dict) else None
    owner = row.get('Owner') if isinstance(row.get('Owner'), dict) else {}
    body = (f"With: {who['name'] or who['email']}\n\n" if who else '') + 'Notes:\n' + notes
    return {'account_id': account['id'], 'source_id': 'event:' + row['Id'], 'kind': 'salesforce.activity', 'occurred_at': at.isoformat(),
            'title': ' '.join(str(row.get('Subject') or 'Meeting').split())[:1000], 'body': body[:BODY],
            'metadata': {'crm_account': crm_account(row), 'contacts': [who] if who else [], 'meeting': True,
                         'host': str(owner.get('Email') or '').lower(), 'mine': str(row.get('OwnerId') or '')[:15] == str(me or '')[:15],
                         'truncated': len(body) > BODY, **({'source_url': link(instance, row['Id'])} if link(instance, row['Id']) else {})},
            'deleted': False}


OPPORTUNITIES = ('SELECT Id, Name, StageName, Amount, CloseDate, IsClosed, IsWon, Description, LastModifiedDate, SystemModstamp, '
                 'CreatedDate, AccountId, Account.Name, Account.Website, Owner.Name, Owner.Email, '
                 '(SELECT Role, Contact.Id, Contact.Name, Contact.Email, Contact.Title FROM OpportunityContactRoles LIMIT 10) '
                 'FROM Opportunity WHERE SystemModstamp >= {since} ORDER BY SystemModstamp LIMIT {limit}')
TASKS = ('SELECT Id, Subject, Description, Status, ActivityDate, IsClosed, TaskSubtype, CompletedDateTime, OwnerId, Owner.Name, '
         'WhoId, Who.Type, Who.Name, Who.Email, Who.Title, WhatId, What.Name, AccountId, Account.Name, Account.Website, '
         'LastModifiedDate, SystemModstamp FROM Task WHERE SystemModstamp >= {since} ORDER BY SystemModstamp LIMIT {limit}')
MEETINGS = ('SELECT Id, Subject, Description, StartDateTime, ActivityDateTime, OwnerId, Owner.Email, Who.Type, Who.Name, Who.Email, '
            'Who.Title, AccountId, Account.Name, Account.Website, SystemModstamp FROM Event WHERE SystemModstamp >= {since} '
            'ORDER BY SystemModstamp LIMIT {limit}')
CUSTOM_FIELD = re.compile(r'[A-Za-z][A-Za-z0-9_]{0,79}__c')  # an org's own field, as the API names it: nothing else goes in a query
CONTACTS = ('SELECT Id, Name, Email, Title, Phone, LastModifiedDate{extra} FROM Contact WHERE Email IN ({emails}) '
            'ORDER BY LastModifiedDate DESC LIMIT {limit}')


def read(source, soql, since, limit=PAGE):
    """Rows changed since `since`, oldest first, and the stamp of the last one when the page is full (more to read)."""
    rows = source.query(soql.format(since=soql_time(since), limit=limit), limit)
    last = stamp(rows[-1].get('SystemModstamp')) if len(rows) >= limit else None
    return rows, last


def linkedin_field(source, state, now):
    """The org's own LinkedIn field on Contact, when it has one the owner's user can edit (a URL or text field with
    LinkedIn in its name or label): Salesforce has none of its own. Looked up once a day."""
    checked = stamp(state.get('linkedin_checked'))
    if checked and now - checked < dt.timedelta(hours=DESCRIBE_HOURS):
        return state.get('linkedin_field')
    found = None
    described = source.get(API + '/sobjects/Contact/describe')
    for field in (described or {}).get('fields') or []:
        if not isinstance(field, dict) or not field.get('updateable') or field.get('type') not in ('url', 'string'):
            continue
        if ('linkedin' in (str(field.get('name') or '') + ' ' + str(field.get('label') or '')).lower() and field.get('custom')
                and CUSTOM_FIELD.fullmatch(str(field.get('name') or ''))):
            found = str(field['name'])
            break
    state.update(linkedin_field=found, linkedin_checked=now.isoformat())
    return found


def contacts_for(source, emails, extra=None):
    """The Salesforce Contacts with these addresses, as crm_sync.plan takes them. SOQL over REST has no bound
    parameters: each address is checked against a strict pattern and quoted, and the field name must be a custom field's."""
    out = []
    if extra is not None and not CUSTOM_FIELD.fullmatch(str(extra)):
        raise ValueError(repr(extra))  # not a custom field's name
    for start in range(0, len(emails), 100):
        chunk = [e for e in emails[start:start + 100] if re.fullmatch(r'[^@\s\'\\]{1,100}@[A-Za-z0-9.-]{1,200}', e)]
        if not chunk:
            continue
        rows = source.query(CONTACTS.format(extra=', ' + extra if extra else '', emails=', '.join(quoted(e) for e in chunk), limit=200), 200)
        for row in rows:
            if '@' in str(row.get('Email') or '') and CONTACT.fullmatch(str(row.get('Id') or '')):
                out.append({'id': row['Id'], 'email': str(row['Email']).lower(), 'name': row.get('Name') or '',
                            'modified': row.get('LastModifiedDate'), 'title': row.get('Title'), 'phone': row.get('Phone'),
                            **({'linkedin_url': row.get(extra)} if extra else {})})
    return out


def plan_contacts(store, source, state, now):
    """What Update contact details would change now ([crm_sync.plan items]) and the LinkedIn field it would use."""
    import crm_sync
    field = linkedin_field(source, state, now)
    with store.connect() as db:
        emails = crm_sync.emails_worth_checking(db)
    if not emails:
        return [], field
    contacts = contacts_for(source, emails, field)
    with store.connect() as db:
        items = crm_sync.plan(db, contacts, 'Salesforce', state.get('contact_written'),
                              fields=('title', 'phone') + (('linkedin_url',) if field else ()))
    return items, field


# Why Salesforce refused one contact's update, by its answer: shown with that contact on the card
REFUSED = {400: 'A rule in Salesforce refused it', 403: 'Your user may not edit this contact', 404: 'The contact is gone from Salesforce'}


def apply_contacts(store, source, account, state, now, helpers):
    """Update contact details: the planned changes, each a PATCH of one Contact and a dated line on the person."""
    import crm_sync
    items, field = plan_contacts(store, source, state, now)
    names = {**WRITABLE, **({'linkedin_url': field} if field else {})}
    done, failed = [], []
    source.account = {**account, 'linkedin_field': field}
    for item in items:
        try:
            source.update(item['contact_id'], {names[c['field']]: c['new'] for c in item['changes']})
        except helpers.SourceError as error:
            if error.status in (400, 403, 404):  # a validation rule, a locked or deleted contact: this one stays as it is
                failed.append({'name': item['name'], 'why': REFUSED[error.status]})
                continue
            raise
        item['done_at'] = now.isoformat()
        written = crm_sync.remember(dict(state.get('contact_written') or {}), item)
        state['contact_written'] = written
        with store.connect() as db:
            crm_sync.logged(db, item, now.isoformat())
        done.append(item)
    state['contact_updates'] = (crm_sync.shown(done) + list(state.get('contact_updates') or []))[:50]
    state['contact_sync_at'] = now.isoformat()
    if failed:
        state['contact_failed'], state['contact_refused'] = len(failed), failed[:10]
    else:
        state.pop('contact_failed', None)
        state.pop('contact_refused', None)
    return len(done)


def label_projects(store, account, events, helpers):
    """Each opportunity's signals go onto the Graph project named after it."""
    import graph
    deals = [(e['source_id'], e['metadata']['opportunity'][:60]) for e in events if e['kind'] == 'salesforce.opportunity'
             and str(e['metadata'].get('opportunity') or '').strip()]
    if not deals:
        return
    with store.connect() as db:
        for source_id, name in deals:
            row = db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account['id'], source_id)).fetchone()
            if row:
                graph.label(db, [row[0]], name, 'salesforce', helpers.now())


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    state = dict(store.checkpoint(account['id']) or {})
    if state.get('stopped'):
        return {'mode': state.get('mode') or 'incremental', 'events': 0, 'stopped': True}
    me = source.me()
    email = str(me.get('email') or '').lower()
    if email and account.get('email') and email != str(account['email']).lower():
        raise helpers.SourceError('account_identity_mismatch')
    if state.get('org_id') and me.get('organization_id') and state['org_id'] != me['organization_id']:
        raise helpers.SourceError('account_identity_mismatch')
    state.update(user_id=me['user_id'], org_id=me.get('organization_id'))
    now = stamp(helpers.now())
    _, instance = broker_token(config, account, helpers)
    first = not state.get('since')
    # A run that stopped at a full page goes on from its last row; a caught-up one rereads a little overlap
    since = (stamp(state.get('since')) - (OVERLAP if state.get('coverage_complete', True) else dt.timedelta(0))) if not first \
        else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    skipped = helpers.Skips('salesforce_invalid_row')
    events, more, upto = [], False, now
    deals = dict(state.get('deals') or {})
    rows, last = read(source, OPPORTUNITIES, since)
    for row in rows:
        before = deals.get(str(row.get('Id')))
        created = stamp(row.get('CreatedDate'))
        if before is None and not (created and created >= since):
            event = None  # first seen, not new: its stage and amount are where later changes start from
        else:
            event = skipped.take(opportunity_event, account, instance, row, before)
            event = None if event is skipped.SKIPPED else event
        if event:
            events.append(event)
        if ID.fullmatch(str(row.get('Id') or '')):
            deals[row['Id']] = {'stage': str(row.get('StageName') or ''), 'amount': row.get('Amount')}
    upto, more = (min(upto, last), True) if last else (upto, more)
    open_tasks = set(state.get('open_tasks') or [])
    rows, last = read(source, TASKS, since)
    for row in rows:
        row['_was_open'] = str(row.get('Id')) in open_tasks
        event = skipped.take(task_event, account, instance, row, state['user_id'])
        if event and event is not skipped.SKIPPED:
            events.append(event)
        if str(row.get('OwnerId') or '')[:15] == str(state['user_id'])[:15] and not row.get('IsClosed'):
            open_tasks.add(str(row.get('Id')))
        else:
            open_tasks.discard(str(row.get('Id')))
    upto, more = (min(upto, last), True) if last else (upto, more)
    rows, last = read(source, MEETINGS, since)
    for row in rows:
        event = skipped.take(meeting_event, account, instance, row, state['user_id'])
        if event and event is not skipped.SKIPPED:
            events.append(event)
    upto, more = (min(upto, last), True) if last else (upto, more)
    skipped.check().note(state)
    if len(deals) > DEALS_KEEP:
        deals = dict(list(deals.items())[-DEALS_KEEP:])
    state.update(deals=deals, open_tasks=sorted(open_tasks)[-1000:], since=upto.isoformat(), mode='incremental',
                 instance=instance, coverage_complete=not more)
    store.commit_page(account['id'], state, events)
    label_projects(store, account, events, helpers)
    # What Salesforce keeps about the contacts on what was kept: their job title, as a record about them
    offers = [(['email:' + c['email']], {'title': c['role']}, 1) for e in events for c in e['metadata'].get('contacts') or () if c.get('role')]
    if offers:
        helpers.remember_profiles(store, 'salesforce', [{'ids': ids, 'facts': facts, 'rank': rank} for ids, facts, rank in offers])
    updated = 0
    synced = stamp(state.get('contact_sync_at'))
    if state.get('contact_sync') and not account.get('shared') and (not synced or now - synced >= dt.timedelta(hours=CONTACT_SYNC_HOURS)):
        updated = apply_contacts(store, source, account, state, now, helpers)
        store.commit_page(account['id'], state, [])
    return {'mode': 'incremental', 'events': len(events), 'more': more, 'skipped': sum(skipped.values()), 'contacts_updated': updated}


def preview(store, config, account, helpers):
    """What Update contact details would change now, for the card before it is turned on: nothing is written."""
    import crm_sync
    source = Source(config, account, helpers)
    state = dict(store.checkpoint(account['id']) or {})
    items, _ = plan_contacts(store, source, state, stamp(helpers.now()))
    return crm_sync.shown(items), state


def card(account, state):
    """The card's sync details: whether it updates contact details, and the last few it updated."""
    return {'contact_sync': bool(state.get('contact_sync')) and not account.get('shared'), 'contact_updates': list(state.get('contact_updates') or [])[:5],
            'contact_failed': int(state.get('contact_failed') or 0), 'contact_refused': list(state.get('contact_refused') or [])[:10], 'linkedin_field': bool(state.get('linkedin_field')),
            'can_write': not account.get('shared'), 'stopped': state.get('stopped') or None}


def check(config, account, helpers):
    """A real read without storing anything: who is signed in, and that their opportunities can be queried."""
    source = Source(config, account, helpers)
    me = source.me()
    email = str(me.get('email') or '').lower()
    if email and account.get('email') and email != str(account['email']).lower():
        raise helpers.SourceError('account_identity_mismatch')
    source.query('SELECT Id FROM Opportunity LIMIT 1', 1)
    return None
