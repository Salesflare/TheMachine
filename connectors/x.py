"""X (Twitter): replies and mentions, and DMs, for one or more accounts signed in to the OpenClaw browser.

Read-only through integrations/x_inbox.py, which makes the same requests x.com does from a tab
of the signed-in OpenClaw browser (not X's developer API): no API key, no cookies leaving the
browser, and nothing marked as seen or read. Sign in to X once in that browser (`openclaw browser --browser-profile openclaw
open https://x.com/login`); add more accounts with X's own account switcher, or give an account a
browser of its own with "browser_profile": "<OpenClaw profile>" and, read directly, "browser_cdp": "<its DevTools
address>" (else X_INBOX_BROWSER_PROFILE / _CDP, else "openclaw"). One config account per X account:

    {"id": "me-x", "service": "x", "transport": "x-inbox", "boundary": "work:Acme",
     "handle": "yourhandle", "primary": "yourhandle", "poll_seconds": 3600}

`primary` is the account the browser should normally be on. To read another signed-in account
x-inbox switches to it and always switches back; since a switch changes the cookies of every
x.com tab, runs go one at a time and only switch while no other job holds the browser lease.
Optional: "active_hours": [7, 23] (local time, the default), "long_posts": true (the account has
X Premium: replies up to 25000 characters) and config "x_inbox" for the path to the reader.
Encrypted X Chat isn't read. Replies and DMs go out only as an owner-approved `x` next action
(next_actions.XTransport).
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import urllib.parse
from pathlib import Path

# Reads only from start to end hour, local time (an account's active_hours overrides it); the dashboard says when it reads again.
READ_HOURS = (7, 23)
KINDS = {'x.mention': 'X', 'x.dm': 'X message'}
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {'x.mention': 'card', 'x.dm': 'chat'}
APP = 'X'
# For `assistant connect x`: the account it adds and what it asks (see docs/adding-a-source.md).
SETUP = {'label': 'X', 'what': 'Your mentions and direct messages on X.',
         'account': {'id': 'me-x', 'service': 'x', 'transport': 'x-inbox', 'boundary': 'work', 'poll_seconds': 3600},
         # Read through the shared browser: a hosted install links to that browser on this site to sign in again.
         'browser': 'x',
         # an account's own browser (a second account of the site): its fields, read into the reader's environment
         'browser_env': {'browser_profile': 'X_INBOX_BROWSER_PROFILE', 'browser_cdp': 'X_INBOX_BROWSER_CDP'},
         'hints': {'x_signed_out': 'the browser it reads with is not signed in to X; sign in there, then connect again'},
         'note': 'Sign in to X once in the OpenClaw browser first: openclaw browser --browser-profile openclaw open https://x.com/login',
         'ask': [('handle', 'Your X handle, without @'), ('primary', 'Handle the browser is normally signed in to', '{handle}')]}
READER = Path(__file__).resolve().parent.parent / 'integrations/x_inbox.py'
# Older mentions and DMs as history (machine/app/history.py, config social_history_days, 90 days by default): read through
# the owner's own browser, not X's API, where bulk reads could get the account restricted, so very slowly. One small
# page per step (20 mentions, or 20 DMs of one conversation, or one page of the DM inbox), a random 8 to 20 minutes
# apart, at most 24 steps a day, only from 9 to 21 local time (inside active_hours), and a day off after any failed or
# odd answer.
HISTORY_PACE = {'page': 20, 'steps_per_day': 24, 'pause_minutes': (8, 20), 'hours': (9, 21)}


def browser_env(account):
    """The reader runs in this account's own browser, when it has one."""
    own = {var: account[field] for field, var in SETUP['browser_env'].items() if account.get(field)}
    return {**os.environ, **own} if own else None


class Source:
    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers

    def page(self, since_ms, state):
        return self.read('sync', since_ms, state)

    def history(self, since_ms, until_ms, state):
        """One small step back in time (the reader's `history`): its mentions, dms, state and done."""
        data = self.read('history', since_ms, state, ['--until', str(int(until_ms)), '--count', str(HISTORY_PACE['page'])])
        if type(data.get('done')) is not bool:
            raise self.helpers.SourceError('x_invalid_page')
        return data

    def read(self, command, since_ms, state, extra=()):
        SourceError, account = self.helpers.SourceError, self.account
        try:
            done = subprocess.run([self.config.get('x_inbox', str(READER)), command, '--handle', account['handle'],
                                   '--primary', account.get('primary', account['handle']), '--since', str(int(since_ms)),
                                   *extra, '--state', json.dumps(state)], capture_output=True, text=True, timeout=480,
                                  env=browser_env(account))
        except subprocess.TimeoutExpired:  # the reader never finished: the browser, not X (its requests end by themselves)
            raise SourceError('x_browser_stalled', retry_after=900) from None
        except OSError as error:
            raise SourceError('x_reader_missing:' + type(error).__name__) from None
        if done.returncode:
            err = done.stderr.lower()
            if 'busy' in err:
                raise SourceError('x_browser_busy', retry_after=600)
            if 'signed out' in err or 'not signed in' in err:
                raise SourceError('x_signed_out', retry_after=3600)
            if 'rate limit' in err:
                raise SourceError('x_rate_limited', retry_after=1800)
            if 'timeouterror' in err or 'signal timed out' in err:  # an X request that took longer than its own limit
                raise SourceError('x_read_timeout', retry_after=900)
            if 'in time' in err:  # the browser's tab didn't answer (or didn't load): X was never asked
                raise SourceError('x_browser_stalled', retry_after=900)
            code = self.helpers.browser_read_failure('x', done.stderr)
            if code.endswith('_browser_unreachable'):  # the browser crashed or hung: start it again, retry soon
                env = browser_env(self.account) or os.environ
                self.helpers.recover_browser(env.get('X_INBOX_BROWSER_PROFILE') or 'openclaw', own_cdp=bool(env.get('X_INBOX_BROWSER_CDP')), config=self.config)
                raise SourceError(code, retry_after=300)
            raise SourceError(code, retry_after=900)
        try:
            data = json.loads(done.stdout)
        except ValueError:
            raise SourceError('x_invalid_json') from None
        if not isinstance(data.get('mentions'), list) or not isinstance(data.get('dms'), list) or not isinstance(data.get('state'), dict):
            raise SourceError('x_invalid_page')
        return data


def person(p):
    return (str(p.get('name') or '') + ' (@' + str(p.get('screen_name') or '?') + ')').strip()


def events(account, data, helpers, skipped=None):
    """A page's mentions and DMs as events. One it can't take is counted in `skipped` (helpers.Skips), never failing
    the page; only a page of nothing but odd ones fails."""
    SourceError = helpers.SourceError
    handle = (data.get('account') or {}).get('screen_name') or account['handle']
    at = lambda ms: helpers.iso(ms / 1000)
    skipped = helpers.Skips('x_invalid_item') if skipped is None else skipped

    def mention(t):
        if not re.fullmatch(r'\d{1,25}', str(t.get('id') or '')) or type(t.get('at')) is not int:
            raise SourceError('x_invalid_mention')
        author, reply = t.get('author') or {}, t.get('reply_to') or None
        who = person(author)
        body = str(t.get('text') or '')
        if t.get('quoted'):
            body += '\n\n[Quoting: “' + str(t['quoted']) + '”]'
        if reply and reply.get('text'):
            body += '\n\n[In reply to @' + str(reply.get('screen_name') or '?') + ': “' + str(reply['text']) + '”]'
        return {'account_id': account['id'], 'source_id': hashlib.sha256(('x:' + t['id']).encode()).hexdigest(), 'kind': 'x.mention',
                'occurred_at': at(t['at']), 'title': (who + (' replied to @' if reply and reply.get('to_account') else ' mentioned @') + handle)[:1000],
                'body': body[:40000], 'deleted': False,
                'metadata': {'from': who, 'sender_display': who, 'screen_name': author.get('screen_name'), 'author_id': author.get('id'),
                             'followers': author.get('followers'), 'verified': author.get('verified') is True, 'account_handle': handle,
                             'reply': bool(reply), 'reply_to_account': bool(reply and reply.get('to_account')),
                             'in_reply_to_id': reply and reply.get('id'), 'in_reply_to': reply and reply.get('screen_name'),
                             'conversation_id': t.get('conversation_id'), 'tweet_id': t['id'], 'lang': t.get('lang'),
                             'source_url': 'https://x.com/' + urllib.parse.quote(str(author.get('screen_name') or 'i')) + '/status/' + t['id']}}

    def message(m):
        if not re.fullmatch(r'\d{1,25}', str(m.get('id') or '')) or type(m.get('at')) is not int or type(m.get('from_me')) is not bool:
            raise SourceError('x_invalid_message')
        sender = m.get('from') or {}
        who = 'You' if m['from_me'] else person(sender)
        name = str(m.get('with') or 'X conversation')
        return {'account_id': account['id'], 'source_id': hashlib.sha256(('x-dm:' + m['id']).encode()).hexdigest(), 'kind': 'x.dm',
                'occurred_at': at(m['at']), 'title': name[:1000], 'body': str(m.get('text') or '')[:40000], 'deleted': False,
                'metadata': {'chat_name': name, 'conversation_id': m.get('conversation_id'), 'message_id': m['id'], 'from_me': m['from_me'],
                             'from': who, 'sender_display': who, 'sender_id': sender.get('id'), 'screen_name': sender.get('screen_name'),
                             'group': m.get('group') is True, 'request': m.get('request') is True, 'account_handle': handle,
                             'source_url': 'https://x.com/messages/' + urllib.parse.quote(str(m.get('conversation_id') or ''))}}

    out = [e for e, _ in skipped.every(data['mentions'], mention) + skipped.every(data['dms'], message)]
    skipped.check()
    return list({e['source_id']: e for e in out}.values())


PHOTO = re.compile(r'https://pbs\.twimg\.com/profile_images/\d{1,25}/[A-Za-z0-9_-]{1,100}_normal\.(?:jpe?g|png|webp)')


def profiles(data, people):
    """What the user objects in this page say about the people in it (their own bio, place, website, handle and
    photo), for their page in the graph. Only for people in this page's mentions and one-to-one DMs."""
    out = []
    for uid, p in (data.get('profiles') or {}).items() if isinstance(data.get('profiles'), dict) else ():
        if not isinstance(p, dict) or not re.fullmatch(r'\d{1,25}', str(uid)) or 'x:' + str(uid) not in people:
            continue
        photo = str(p.get('photo') or '')
        out.append({'ids': ['x:' + str(uid)], 'rank': 2,
                    'facts': {'bio': p.get('bio') or '', 'location': p.get('location') or '', 'website': p.get('website') or '',
                              'x': p.get('screen_name') or ''},
                    'photo': photo.replace('_normal.', '_200x200.') if PHOTO.fullmatch(photo) else None})
    return out


def sync(store, config, account, helpers, source=None):
    # Browser reads: keep them to waking hours.
    current = dt.datetime.fromisoformat(helpers.now())
    start, end = account.get('active_hours', READ_HOURS)
    if not start <= current.astimezone(helpers.local_tz()).hour < end:
        return {'mode': 'incremental', 'events': 0}
    source = source or Source(config, account, helpers)
    state = store.checkpoint(account['id']) or {}
    since = state.get('since_ms') or int((current - dt.timedelta(days=int(config.get('bootstrap_days', 7)))).timestamp() * 1000)
    data = source.page(since, state.get('page') or {})
    skipped = helpers.Skips('x_invalid_item')
    found = events(account, data, helpers, skipped)
    skipped.note(state)
    more = bool(data['state'].get('mention_catchup'))
    name = ' '.join(str((data.get('account') or {}).get('name') or '').split())[:100]
    if name:
        state['account_name'] = name  # the profile's name: what its Connections card is called (machine/names.py)
    state.update(mode='incremental', since_ms=since, page=data['state'], read_items=len(found), coverage_complete=not more,
                 coverage=('Older mentions are still being collected for @' if more else 'Mentions, replies and DM inbox caught up for @') + account['handle'] + '.')
    store.commit_page(account['id'], state, found)
    people = {'x:' + str(e['metadata'].get('author_id') or e['metadata'].get('sender_id')) for e in found
              if not e['metadata'].get('group') and not e['metadata'].get('from_me')}
    people |= {'x:' + p for e in found if e['kind'] == 'x.dm' and not e['metadata'].get('group')
               for p in str(e['metadata'].get('conversation_id') or '').split('-') if p.isdigit()}
    if getattr(helpers, 'remember_profiles', None):
        helpers.remember_profiles(store, 'x', profiles(data, people))
    return {'mode': 'incremental', 'events': len(found), 'more': more, 'skipped': sum(skipped.values())}


def history_page(config, account, helpers, state, upper, target, source=None):
    """One step of older mentions and DMs, kept as history (machine/app/history.py, which paces it by HISTORY_PACE),
    newest first, from `upper` back to `target`. Returns (events, done); state['page'] holds the reader's cursors."""
    source = source or Source(config, account, helpers)
    ms = lambda text: int(dt.datetime.fromisoformat(text).timestamp() * 1000)
    data = source.history(ms(target), ms(upper), state.get('page') or {})
    found = events(account, data, helpers) if data['mentions'] or data['dms'] else []
    state['page'] = data['state']
    return [e for e in found if target <= e['occurred_at'] < upper], data['done']
