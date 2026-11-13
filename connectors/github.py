"""GitHub: threads you take part in (review requests, mentions, assignments, replies) and failed CI runs.

Read-only through the owner's logged-in `gh` CLI: GET requests only; notifications are never
marked as read.

Config:
    {"id": "github", "service": "github", "transport": "gh", "boundary": "work:Acme",
     "login": "your-login", "poll_seconds": 600}
Optional: "repos": ["owner/repo", ...] to keep only those repositories; "ci_repos": [...] and
"ci_branch" (default "main") to report failed workflow runs on that branch; config "gh" for the
path to the CLI.
"""
import datetime as dt
import hashlib
import json
import re
import subprocess

KINDS = {'github.notification': 'GitHub', 'github.ci': 'GitHub CI'}
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {'github.notification': 'card', 'github.ci': 'card'}
APP = 'GitHub'
# For `assistant connect github`: the account it adds and what it asks (see docs/adding-a-source.md).
SETUP = {'label': 'GitHub', 'what': 'Review requests, mentions, assignments and failed CI runs.',
         'account': {'id': 'github', 'service': 'github', 'transport': 'gh', 'boundary': 'work', 'poll_seconds': 600},
         'note': 'GitHub is read through your logged-in gh CLI (gh auth login), GET requests only.',
         'ask': [('login', 'Your GitHub login')], 'detect': {'login': ['gh', 'api', 'user', '--jq', '.login']}}
REASONS = {'assign', 'author', 'comment', 'mention', 'review_requested', 'team_mention', 'security_alert', 'manual'}


class Source:
    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        self.verified, self.name = False, ''

    def get(self, path):
        SourceError = self.helpers.SourceError
        if not re.fullmatch(r'[A-Za-z0-9_./?=&%:+,-]+', path) or path.startswith(('/', 'graphql')):
            raise SourceError('github_path_not_allowed')
        try:
            done = subprocess.run([self.config.get('gh', 'gh'), 'api', '--method', 'GET', path], capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise SourceError('network:' + type(error).__name__ + ':github_read') from None
        if done.returncode:
            code = re.search(r'HTTP (\d{3})', done.stderr or '')
            raise SourceError('github', int(code.group(1)) if code else None)
        try:
            return json.loads(done.stdout or 'null')
        except ValueError:
            raise SourceError('github_invalid_json') from None

    def verify(self):
        """gh must be logged in as the configured login, not whoever ran `gh auth login` last."""
        if not self.verified:
            user = self.get('user') or {}
            if user.get('login', '').lower() != self.account['login'].lower():
                raise self.helpers.SourceError('account_identity_mismatch')
            self.verified, self.name = True, ' '.join(str(user.get('name') or '').split())[:100]


def html(url):
    """API URL of an issue, PR or commit -> the page in the browser."""
    m = re.fullmatch(r'https://api\.github\.com/repos/([^/]+/[^/]+)/(issues|pulls|commits)/([^/]+)', url or '')
    if not m:
        return ''
    return f"https://github.com/{m.group(1)}/{ {'pulls': 'pull', 'commits': 'commit'}.get(m.group(2), 'issues')}/{m.group(3)}"


def utc(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(dt.timezone.utc).isoformat()


def api_path(url):
    return url.split('api.github.com/', 1)[1] if (url or '').startswith('https://api.github.com/') else None


def sync(store, config, account, helpers, source=None):
    source = source or Source(config, account, helpers)
    source.verify()
    state = store.checkpoint(account['id']) or {}
    if getattr(source, 'name', ''):
        state['account_name'] = source.name  # the profile's name: what its Connections card is called (machine/names.py)
    since = state.get('since') or (dt.datetime.fromisoformat(helpers.now()) - dt.timedelta(days=int(config.get('bootstrap_days', 7)))).strftime('%Y-%m-%dT%H:%M:%SZ')
    repos = {r.lower() for r in account.get('repos', [])}
    me = account['login'].lower()
    window = state.get('catchup') or {'since': since, 'before': dt.datetime.fromisoformat(helpers.now()).strftime('%Y-%m-%dT%H:%M:%SZ'), 'page': 1, 'newest': since}
    def page_items(page):
        return source.get(f"notifications?all=true&participating=true&per_page=50&page={page}&since={window['since']}&before={window['before']}") or []
    def fingerprint(items):
        return hashlib.sha256(json.dumps([(n.get('id'), n.get('updated_at')) for n in items]).encode()).hexdigest()
    # An old numeric continuation has no shift proof; safely replay its window once.
    if window['page'] > 1 and not window.get('anchor'):
        window['page'] = 1
    count, read, more = 0, 0, False
    for _ in range(5):
        anchor = window.get('anchor')
        if anchor and fingerprint(page_items(anchor['page'])) != anchor['fingerprint']:
            window['page'] = 1
            window.pop('anchor', None)
            anchor = None
        page = window['page']
        items = page_items(page)
        events = []
        for n in items:
            window['newest'] = max(window['newest'], n.get('updated_at') or window['newest'])
            repo = (n.get('repository') or {}).get('full_name', '')
            if n.get('reason') not in REASONS or (repos and repo.lower() not in repos):
                continue
            subject = n.get('subject') or {}
            detail = source.get(api_path(subject.get('url'))) or {} if api_path(subject.get('url')) else {}
            latest = {}
            comment = subject.get('latest_comment_url') or ''
            if comment != subject.get('url') and api_path(comment):
                try:
                    latest = source.get(api_path(comment)) or {}
                except helpers.SourceError as error:
                    if error.status != 404:
                        raise
            author = (latest.get('user') or detail.get('user') or {}).get('login') or ''
            url = latest.get('html_url') or detail.get('html_url') or html(subject.get('url')) or f'https://github.com/{repo}'
            status = ('merged' if detail.get('merged_at') else detail.get('state') or '') if detail else ''
            body = '\n\n'.join(x for x in [
                f"{subject.get('type', 'Thread')} in {repo}" + (f" ({status})" if status else '') + f"; why you got it: {n.get('reason', '').replace('_', ' ')}.",
                (detail.get('body') or '')[:6000],
                f"Latest comment by {author}:\n{(latest.get('body') or '')[:6000]}" if latest else ''] if x)
            events.append({'account_id': account['id'], 'source_id': 'n:' + str(n['id']), 'kind': 'github.notification',
                           'occurred_at': utc(n['updated_at']), 'title': f"[{repo.split('/')[-1]}] {subject.get('title', '')}"[:1000],
                           'body': body[:40000], 'deleted': False,
                           'metadata': {'repo': repo, 'reason': n.get('reason'), 'type': subject.get('type'), 'number': detail.get('number'),
                                        'author': (detail.get('user') or {}).get('login') or '',  # who opened it, not who commented
                                        'state': status, 'from': author, 'from_me': author.lower() == me, 'source_url': url}})
        read += len(items)
        count += len(events)
        # Check again after this read: a notification can leave the frozen window
        # between the first anchor check and fetching the next numbered page.
        shifted = anchor and fingerprint(page_items(anchor['page'])) != anchor['fingerprint']
        more = len(items) == 50 or bool(shifted)
        if more:
            window['page'] = 1 if shifted else page + 1
            if shifted:
                window.pop('anchor', None)
            else:
                window['anchor'] = {'page': page, 'fingerprint': fingerprint(items)}
            state.update(mode='incremental', since=since, catchup=window)
        else:
            state.update(mode='incremental', since=window['newest'])
            state.pop('catchup', None)
        state.update(coverage_complete=not more, coverage='Older GitHub notifications are still being collected.' if more else 'GitHub notification pages caught up.')
        store.commit_page(account['id'], state, events)
        if not more:
            break
    events = []
    for repo in account.get('ci_repos', []):
        branch = account.get('ci_branch', 'main')
        runs = (source.get(f"repos/{repo}/actions/runs?branch={branch}&status=failure&per_page=20&created=%3E{since[:10]}") or {}).get('workflow_runs', [])
        for run in runs:
            actor = (run.get('actor') or {}).get('login', '')
            events.append({'account_id': account['id'], 'source_id': 'ci:' + str(run['id']), 'kind': 'github.ci',
                           'occurred_at': utc(run['updated_at']), 'title': f"[{repo.split('/')[-1]}] {run.get('name', 'CI')} failed on {branch}"[:1000],
                           'body': f"Commit: {((run.get('head_commit') or {}).get('message') or '')[:2000]}\nBy: {actor}",
                           'deleted': False, 'metadata': {'repo': repo, 'from': actor, 'from_me': actor.lower() == me, 'source_url': run.get('html_url', '')}})
    if events:
        store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': count + len(events), 'read': read, 'more': more}
