"""Stripe: billing signals worth a look (failed payments, disputes, cancellations, big new subscriptions).

Read-only: GET on the account, events and customer endpoints only. Never writes, refunds or retries.

Signed in with Stripe (the easy way): the owner installs the control plane's Stripe App, which asks Stripe for read
permissions only, from the setup page or Connections, + Add. Like Zoom (connectors/zoom.py), the refresh token lives on
this Machine only, sealed in mail_grants.py, and is sent along to the broker for each access token (an hour). Stripe
rolls it on every refresh: the broker passes the new one back and it is kept here.
    {"id": "billing", "service": "stripe", "transport": "broker", "boundary": "work:Acme",
     "stripe_account": "acct_...", "poll_seconds": 900}
    "stripe_broker": {"url": "https://app.example.com/api/stripe/token"},
    "credentials": {"stripe-broker": "~/.local/share/personal-assistant/google-broker"}
A Work Fleet's admin can share it with the team (shared_connectors.py): their Machine sends fresh access tokens to
teammates' Machines, which read it as a plain "api" account and never refresh it themselves.

Or, with a restricted read-only key (Events, Customers, Account: Read) in a credential file:
    {"id": "billing", "service": "stripe", "transport": "api", "boundary": "work:Acme",
     "credential": "stripe", "stripe_account": "acct_...", "poll_seconds": 900}
or through a Maton Stripe connection:
    {"id": "billing", "service": "stripe", "transport": "maton", "boundary": "work:Acme",
     "credential": "maton", "credential_variable": "MATON_API_KEY", "connection_id": "...",
     "stripe_account": "acct_...", "poll_seconds": 900}
Optional: "large_subscription_monthly" (default 500, in the price currency): new subscriptions
at or above this monthly value become events; smaller ones are routine.
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

KINDS = {'stripe.event': 'Stripe'}
# For `assistant connect stripe`: the account it adds and what it asks (see docs/adding-a-source.md).
SETUP = {'label': 'Stripe', 'what': 'Failed payments, disputes, churn and big new subscriptions.',
         'account': {'id': 'billing', 'service': 'stripe', 'transport': 'api', 'boundary': 'work', 'credential': 'stripe',
                     'poll_seconds': 900},
         # On a hosted Machine its account page also offers Sign in with Stripe (the app The Machine), as well as pasting
         'account_page': 'source-stripe',
         'note': 'Create a restricted key in Stripe with read access to Events, Customers and Account only.',
         'ask': [('stripe_account', 'Stripe account ID (acct_…)')],
         'secret': 'Restricted Stripe key (rk_…)',
         'maton': 'Maton Stripe connection ID',
         'hints': {'stripe_signin_expired': 'Stripe asks you to sign in again',
                   'stripe:HTTP_401': 'Stripe turned the key down; sign in with Stripe again, or paste a new restricted key'}}
TYPES = ('invoice.payment_failed', 'customer.subscription.deleted', 'customer.subscription.updated',
         'customer.subscription.created', 'charge.dispute.created')
PATHS = ('v1/account', 'v1/events', 'v1/customers/')
API = 'https://api.stripe.com/'
_tokens = {}
_lock = threading.Lock()


def _key(account):
    return str(account.get('stripe_account') or '').strip().lower()


def broker_token(config, account, helpers, fresh=False, min_left=0):
    """A short-lived access token for a signed-in Stripe account: (token, seconds left). Sends the sign-in kept here to
    the broker and keeps the one Stripe rolled. min_left: a cached token with less time left is refreshed first."""
    import mail_grants
    key = _key(account)
    if not key.startswith('acct_'):
        raise helpers.SourceError('stripe_no_account')
    with _lock:
        hit = _tokens.get(key)
        if hit and not fresh and hit[1] - time.monotonic() > max(0, min_left):
            return hit[0], int(hit[1] - time.monotonic())
        url = (config.get('stripe_broker') or {}).get('url')
        if not url or not str(url).startswith('https://'):
            raise helpers.SourceError('stripe_broker_not_configured')
        try:
            secret = helpers.credential(config, 'stripe-broker')
        except Exception:
            raise helpers.SourceError('stripe_broker_credential') from None
        for attempt in (0, 1):
            try:
                kept = mail_grants.get(config, 'stripe', key)
            except mail_grants.GrantError:
                raise helpers.SourceError('stripe_signin_unreadable') from None
            if not kept:
                raise helpers.SourceError('stripe_signin_expired')
            request = urllib.request.Request(url, method='POST', data=json.dumps({'email': key, 'refresh_token': kept}).encode(),
                                             headers={'Authorization': 'Bearer ' + secret.strip(), 'Content-Type': 'application/json',
                                                      'Accept': 'application/json'})
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    answer = json.loads(response.read(200_000))
                break
            except urllib.error.HTTPError as error:
                retry = error.headers.get('Retry-After', '') if error.headers else ''
                error.close()
                if error.code in (401, 404):
                    try:
                        moved = mail_grants.get(config, 'stripe', key) not in (None, kept)
                    except mail_grants.GrantError:
                        moved = False
                    if moved and not attempt:
                        continue  # another process (a check while connecting) rolled it just now: the newer one
                    raise helpers.SourceError('stripe_signin_expired', error.code) from None
                raise helpers.SourceError('stripe_broker', error.code, retry_after=int(retry) if retry.isdigit() else None) from None
            except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException):
                raise helpers.SourceError('stripe_broker_unreachable') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        if not isinstance(access, str) or not access:
            raise helpers.SourceError('stripe_broker')
        rotated = answer.get('refresh_token')
        if isinstance(rotated, str) and rotated and rotated != kept:
            mail_grants.rotate(config, 'stripe', key, kept, rotated)  # the one sent is spent now: only the new one works
        left = max(0, int(answer.get('expires_in') or 0) - 120)
        _tokens[key] = (access, time.monotonic() + left)
        return access, left


def share_token(config, account, helpers, min_left=0):
    """What a Work Fleet admin's Machine sends its teammates for this account (shared_connectors.py): (token, seconds
    it works for, None for a pasted key that lasts). A signed-in account's access token lasts an hour, so this Machine
    sends a fresh one before the last one runs out; teammates never get the sign-in itself."""
    if account.get('transport') == 'broker':
        return broker_token(config, account, helpers, min_left=min_left)
    if account.get('transport') == 'maton':
        raise helpers.SourceError('stripe_maton_not_shared')
    return Source(config, account, helpers).secret().strip(), None


class Source:
    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        self.customers = {}
        self.verified = False

    def secret(self):
        secret = self.helpers.credential(self.config, self.account['credential'])
        variable = self.account.get('credential_variable')
        if variable:
            matches = re.findall(r'^' + re.escape(variable) + r'=(.*)$', secret, re.M)
            if len(matches) != 1:
                raise self.helpers.SourceError('stripe_credential_unavailable')
            secret = matches[0].strip().strip('"\'')
        return secret

    def get(self, path, params=None):
        """One GET to Stripe's API (or through Maton). Never any other method, and only the paths in PATHS."""
        SourceError = self.helpers.SourceError
        if not path.startswith(PATHS):
            raise SourceError('stripe_path_not_allowed')
        maton = self.account.get('transport') == 'maton'
        broker = self.account.get('transport') == 'broker'
        base = 'https://api.maton.ai/stripe/' if maton else API
        url = base + path + ('?' + urllib.parse.urlencode(params, doseq=True) if params else '')
        for attempt in (0, 1):
            token = broker_token(self.config, self.account, self.helpers, fresh=bool(attempt))[0] if broker else self.secret()
            headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
            if maton:
                headers['Maton-Connection'] = self.account['connection_id']
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method='GET'), timeout=45) as response:
                    if maton and response.headers.get('Maton-Connection') != self.account['connection_id']:
                        raise SourceError('connection_identity_mismatch')
                    return json.load(response)
            except urllib.error.HTTPError as error:
                retry = error.headers.get('Retry-After') if error.headers else None
                error.close()
                if broker and error.code == 401 and not attempt:
                    continue  # the access token ran out early: one fresh one
                raise SourceError('stripe', error.code, min(3600, max(60, int(retry))) if retry and retry.isdigit() else None) from None
            except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
                raise SourceError('network:' + type(error).__name__ + ':stripe_read') from None
            except ValueError:
                raise SourceError('stripe_invalid_json') from None
        raise SourceError('stripe', 401)

    def verify(self):
        """The key must belong to the configured Stripe account, not just any account. A signed-in one's broker checks
        that too, on every token (the account the sign-in was for); Stripe may not let an app read the account itself."""
        if not self.verified:
            try:
                found = str(self.get('v1/account').get('id') or '')
            except self.helpers.SourceError as error:
                if error.status != 403 or self.account.get('transport') == 'api' and not self.account.get('shared'):
                    raise
                found = ''  # an app's token without account access: the broker or the Fleet grant named the account
            if found and found.lower() != _key(self.account):
                raise self.helpers.SourceError('account_identity_mismatch')
            self.verified = True

    def connect(self):
        """A shared Stripe token, checked before it is kept (shared_connectors.py): it reads this account."""
        self.verify()
        return self.account

    def customer(self, customer_id):
        if not isinstance(customer_id, str) or not customer_id.startswith('cus_'):
            return {}
        if customer_id not in self.customers:
            try:
                self.customers[customer_id] = self.get('v1/customers/' + customer_id)
            except self.helpers.SourceError as error:
                if error.status != 404:
                    raise
                self.customers[customer_id] = {}
        return self.customers[customer_id]


def day(timestamp):
    return dt.datetime.fromtimestamp(int(timestamp), dt.timezone.utc).date().isoformat()


def money(amount, currency):
    return f"{(amount or 0) / 100:,.2f} {str(currency or '').upper()}".replace('.00 ', ' ')


def monthly(subscription):
    """What a subscription brings in per month, from its items (yearly prices divided by 12)."""
    total, currency = 0, subscription.get('currency')
    for item in (subscription.get('items') or {}).get('data', []):
        price = item.get('price') or {}
        recurring = price.get('recurring') or {}
        months = {'day': 1 / 30, 'week': 7 / 30, 'month': 1, 'year': 12}.get(recurring.get('interval'), 1) * (recurring.get('interval_count') or 1)
        total += (price.get('unit_amount') or 0) * (item.get('quantity') or 1) / months
        currency = price.get('currency') or currency
    return round(total), currency


def large(account, subscription):
    return monthly(subscription)[0] >= 100 * float(account.get('large_subscription_monthly', 500))


def cancelling(obj, before):
    return before.get('cancel_at_period_end') is False and bool(obj.get('cancel_at_period_end'))


def overdue(obj, before):
    return 'status' in before and obj.get('status') in ('past_due', 'unpaid')


def event(account, item, source, helpers):
    """One Stripe event worth a look, or None for the routine ones (most subscription updates)."""
    kind, obj = item.get('type'), (item.get('data') or {}).get('object') or {}
    before = (item.get('data') or {}).get('previous_attributes') or {}
    if kind == 'customer.subscription.updated' and not (cancelling(obj, before) or overdue(obj, before)):
        return None
    if kind == 'customer.subscription.created' and not large(account, obj):
        return None
    if kind not in TYPES:
        return None
    customer = source.customer(obj.get('customer')) if not obj.get('customer_name') else {}
    who = obj.get('customer_name') or customer.get('name') or obj.get('customer_email') or customer.get('email') or 'A customer'
    email = obj.get('customer_email') or customer.get('email') or ''
    dashboard = 'https://dashboard.stripe.com/' + ('' if item.get('livemode', True) else 'test/')
    if kind == 'invoice.payment_failed':
        title = f"Payment failed: {who}, {money(obj.get('amount_due'), obj.get('currency'))}"
        retry = obj.get('next_payment_attempt')
        lines = [f"Attempt {obj.get('attempt_count') or 1}; " + (f"Stripe retries {day(retry)}." if retry else 'no automatic retry scheduled.'),
                 f"Reason: {obj.get('billing_reason') or 'unknown'}."]
        url = dashboard + 'invoices/' + str(obj.get('id'))
    elif kind == 'charge.dispute.created':
        due = (obj.get('evidence_details') or {}).get('due_by')
        title = f"Dispute: {who}, {money(obj.get('amount'), obj.get('currency'))}"
        lines = [f"Reason: {obj.get('reason') or 'unknown'}." + (f" Evidence due {day(due)}." if due else '')]
        url = dashboard + 'disputes/' + str(obj.get('id'))
    else:
        amount, currency = monthly(obj)
        value = f"{money(amount, currency)}/month"
        url = dashboard + 'subscriptions/' + str(obj.get('id'))
        if kind == 'customer.subscription.deleted':
            title = f"Subscription ended: {who}, {value}"
            reason = obj.get('cancellation_details') or {}
            lines = [f"Reason: {reason.get('reason') or 'not given'}." + (f" Feedback: {reason.get('feedback')}." if reason.get('feedback') else '') +
                     (f" Comment: {reason.get('comment')}" if reason.get('comment') else '')]
        elif kind == 'customer.subscription.created':
            title = f"New subscription: {who}, {value}"
            lines = [f"Status: {obj.get('status')}."]
        elif cancelling(obj, before):
            title = f"Cancellation scheduled: {who}, {value}"
            end = obj.get('cancel_at') or obj.get('current_period_end')
            lines = [f"Ends {day(end)}." if end else 'Ends at the end of the period.']
        else:
            title = f"Subscription {obj['status'].replace('_', ' ')}: {who}, {value}"
            lines = [f"Was {before['status']}."]
    body = '\n'.join(x for x in [title + '.', email and 'Email: ' + email] + lines if x)
    return {'account_id': account['id'], 'source_id': item['id'], 'kind': 'stripe.event', 'occurred_at': helpers.iso(int(item['created'])),
            'title': title[:1000], 'body': body[:40000], 'deleted': False,
            'metadata': {'type': kind, 'customer_id': obj.get('customer'), 'from': email, 'customer_name': who, 'source_url': url}}


def sync(store, config, account, helpers, source=None):
    source = source or Source(config, account, helpers)
    source.verify()
    state = store.checkpoint(account['id']) or {}
    since = int(state.get('since') or time.time() - 86400 * int(config.get('bootstrap_days', 7)))
    window = state.get('catchup') or {'after': max(0, since - 1), 'before': int(time.time()), 'newest': since}
    params = {'limit': 100, 'types[]': list(TYPES), 'created[gte]': window['after'], 'created[lte]': window['before']}
    if window.get('cursor'):
        params['starting_after'] = window['cursor']
    read, count, more = 0, 0, False
    for _ in range(10):  # newest first; a quiet account needs one page
        page = source.get('v1/events', params)
        items = page.get('data', [])
        if page.get('has_more') and not items:
            raise helpers.SourceError('stripe_invalid_page')
        events = [e for e in (event(account, item, source, helpers) for item in reversed(items)) if e]
        read += len(items)
        count += len(events)
        window['newest'] = max([window['newest']] + [int(item.get('created') or 0) for item in items])
        more = bool(page.get('has_more'))
        if more:
            cursor = items[-1]['id']
            if cursor == window.get('cursor'):
                raise helpers.SourceError('stripe_invalid_cursor')
            window['cursor'] = cursor
            state.update(mode='incremental', since=since, catchup=window)
            params['starting_after'] = cursor
        else:
            state.update(mode='incremental', since=window['newest'])
            state.pop('catchup', None)
        state.update(coverage_complete=not more, coverage='Older Stripe events are still being collected.' if more else 'Stripe event pages caught up.')
        store.commit_page(account['id'], state, events)
        if not more:
            break
    return {'mode': 'incremental', 'events': count, 'read': read, 'more': more}
