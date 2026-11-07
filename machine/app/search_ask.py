"""Ask from search in the service (search_ask.py has the prompt and the answer): the messages a question finds in the
area the owner is looking at, and the one-shot turn that answers it. A mixin of assistant.App (APP_MIXINS)."""
import json
import logging
import sqlite3

import embeddings
import graph
import locale_prefs
from machine.text import shown_body
from models import background_model, has_model
import search_ask
import shared_graph

LOG = logging.getLogger('personal-assistant')
AREAS = (None, 'work', 'personal')
FOUND = 16  # messages the search brings back before the best SOURCES go in


class SearchAskApp:
    ACTIONS = {'search_ask': 'search_ask_action'}

    def search_ask_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Ask from search is only in your own dashboard.')
        area = args.get('area')
        area = None if area in (None, '', 'all') else area
        if area not in AREAS:
            raise ValueError('Pick All, Work or Personal.')
        return self.search_ask(args.get('query'), area)

    def search_ask_accounts(self, area):
        """The connections of the area the owner is looking at: every one for All."""
        return [a['id'] for a in self.config.get('accounts', []) if a.get('id') and (area is None or graph.account_side(a) == area)]

    def search_ask_rows(self, question, area):
        """The messages the palette's search finds for the question (by meaning and keywords where local embeddings run,
        else by keywords), best first, in the area's connections only. With Work, no thread the review judged to be
        about the owner's own life (todo_areas.py, knowledge.held)."""
        accounts = self.search_ask_accounts(area)
        if not accounts:
            return []
        if embeddings.settings(self.config):
            found, _ = self.related(accounts, (), question, FOUND, timeout=8)
            order = [i for i, _ in found]
        else:
            with self.store.connect() as db:
                order = embeddings.fts_ids(db, accounts, question, FOUND)
        if not order:
            return []
        rows = self.store.events(accounts, event_ids=order, kinds=list(graph.MESSAGE_KINDS))
        place = {e: n for n, e in enumerate(order)}
        rows.sort(key=lambda r: place.get(r['id'], len(place)))
        if area == 'work' and rows:
            try:
                with self.store.connect() as db:
                    calls = {r[0]: r[1] for r in db.execute('SELECT thread,verdict FROM share_threads')}
            except sqlite3.OperationalError:
                calls = {}  # no Shared Graph here
            meta = lambda r: r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
            rows = [r for r in rows if calls.get(shared_graph.thread_of(r['kind'], meta(r), r['id'])) != 'personal']
        return rows

    def search_ask_model(self):
        """(model, thinking) for the turn: the lighter model background work uses, at a low thinking level where the
        sign-in's model list says which levels it has; None for OpenClaw's own."""
        import chat_model
        swap = background_model(self.config)
        model = '/'.join(swap) if swap else None
        try:
            models = self.chat_models(read=False)
        except (OSError, ValueError):
            models = None
        ref = model or chat_model.resolve(self.config, models)['model']
        entry = next((m for m in models or [] if m.get('ref') == ref), None)
        return model, chat_model.nearest('low', (entry or {}).get('levels') or [])

    def search_ask(self, question, area=None):
        """{'answer', 'sources'}; {'none': True} when the words aren't a question or nothing was found; {'off': True}
        without a model; {'error': True} when the turn failed. Never sends, drafts or makes a to-do."""
        import help_chat
        stand_in = getattr(self, 'ask_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        if not stand_in and not has_model(self.config):
            return {'off': True}
        question = search_ask.clean_question(question)
        if len(question.split()) < 2:
            return {'none': True}
        try:
            rows = self.search_ask_rows(question, area)
        except (sqlite3.Error, ValueError, embeddings.EmbeddingError) as error:
            LOG.warning('search ask not searched error=%s', type(error).__name__)
            return {'error': True}
        if stand_in:
            run = lambda text: stand_in(self.config, text)
        else:
            model, thinking = self.search_ask_model()
            run = lambda text: help_chat.openclaw_model_run(self.config, text, model, thinking, timeout=search_ask.TIMEOUT)
        try:
            found = search_ask.ask(question, rows, run, locale_prefs.language_of(self.config), body=lambda b: shown_body(b)[0])
        except (search_ask.Unavailable, help_chat.Unavailable) as error:
            LOG.info('search ask not answered error=%s', type(error).__name__)
            return {'error': True}
        return found or {'none': True}
