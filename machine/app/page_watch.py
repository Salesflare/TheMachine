"""Watch a page, from the owner's own main chat (the bridge's assistant_page_watch): the watched pages, a new one, or one
taken off. Each watch is a Web page connection (connectors/web_page.py), added and removed with the same steps as
Settings, Connections, Other (ConnectApp.connect_action), so both places show the same list. A mixin of assistant.App
(APP_MIXINS)."""
import time

from connectors import web_page
from machine.owner_error import OwnerError

WAIT_SECONDS = 25  # the bridge's call gives up after 30


class PageWatchApp:
    ACTIONS = {'page_watch': 'page_watch_action'}

    def page_watch_action(self, name, args, owner_dashboard=False):
        """do: list, add (url, scope work|personal, company) or remove (id or url). Only from the owner's own main chat
        (_owner_chat, set by the bridge, never the model; an owner action, so never the local CLI), and add or remove
        only after the owner wrote there (owner_said)."""
        if args.get('_owner_chat') is not True:
            raise ValueError('Only the owner watches a page, in their own main chat')
        do = args.get('do')
        if do == 'list':
            return {'pages': self.watched_pages()}
        if do not in ('add', 'remove'):
            raise ValueError('do is list, add or remove')
        if not self.owner_said():  # read by the assistant in the chat, never shown to the owner
            raise ValueError('Add or remove a watch only when the owner asks: they wrote nothing in this chat in the last half hour.')
        try:
            url = web_page.address(args.get('url')) if args.get('url') else ''
        except ValueError:
            raise OwnerError(web_page.SETUP['hints']['web_page_address']) from None
        pages = self.watched_pages()
        if do == 'remove':
            page = next((p for p in pages if p['id'] == args.get('id') or (url and p['url'] == url)), None)
            if not page:
                return {'removed': None, 'pages': pages, 'note': 'Not watched. Ask which one, from pages.'}
            self.connect_action('connect_remove', {'account': page['id']})
            return {'removed': page['name'], 'note': 'Tell the owner "Stopped watching <name>".'}
        if not url:
            raise ValueError('url is the page to watch')
        same = next((p for p in pages if p['url'] == url), None)
        if same:
            return {'added': None, 'page': same, 'note': 'Already watched.'}
        import onboarding
        scope = args.get('scope') if args.get('scope') in ('work', 'personal') else None
        company = str(args.get('company') or '').strip() or onboarding.web_form(self.config, 'web_page')['company']
        if scope is None:
            scope = 'work' if company else 'personal'
        started = self.connect_action('connect_start', {'name': 'web_page', 'form': True, 'answers': {'url': url},
                                                        'scope': scope, 'company': company})
        view, until = started, time.monotonic() + WAIT_SECONDS
        while view.get('state') == 'running' and not view.get('question') and time.monotonic() < until:
            time.sleep(0.5)
            view = self.connect_action('connect_poll', {'session': started['session']})
        if view.get('state') == 'running':  # a question the chat cannot answer, or a slow page: Settings takes it from here
            self.connect_action('connect_cancel', {'session': started['session']})
            return {'added': None, 'note': 'Not added. The owner can add it in Settings, Connections, Other, Web page.'}
        if view.get('state') != 'done':
            return {'added': None, 'error': view.get('error'), 'fix': view.get('fix'), 'note': 'Not added: tell the owner why.'}
        return {'added': web_page.page_name(url), 'scope': scope,
                'note': 'Tell the owner "Watching <added>": a to-do comes only when something that matters changes.'}

    def watched_pages(self):
        """The Web page connections: id, url, name, the last good read and what went wrong since, if anything."""
        pages = []
        with self.store.connect() as db:
            for account in self.config.get('accounts', []):
                if account.get('service') != 'web_page':
                    continue
                row = db.execute('SELECT last_success,error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                error = str(row['error'] or '').split(':', 1)[0] if row else ''
                pages.append({'id': account['id'], 'url': account.get('url'), 'name': account.get('display_name') or web_page.page_name(account.get('url') or ''),
                              'read_at': row['last_success'] if row else None,
                              'problem': web_page.SETUP['hints'].get(error) or ('cannot read it now' if error else None)})
        return pages
