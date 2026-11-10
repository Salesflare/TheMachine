"""Ask from search in the service (search_ask.py has the prompts and the answer): the messages a question finds in the
area the owner is looking at, and the turns that answer it. A mixin of assistant.App (APP_MIXINS).

A question about a person reads them through the Graph: the people whose name has the words asked (every one of
them, so "Andrea" finds each Andrea and never an Andreas), and of those the one with messages in the days asked
about, else the one the owner is most in touch with; the others are named to the answer so it says which one it
means. Their messages are the ones the Graph has them directly on (from or with them), never a message that only
mentions the name. A question about a time reads only the messages of those days, in the owner's time zone."""
import datetime as dt
import json
import logging
import sqlite3

import embeddings
import graph
import locale_prefs
import timeutil
from machine.app import ask_memory
from machine.app.recall import recall
from machine.text import shown_body
import memory_use
from timeutil import now
from models import background_model, has_model
import search_ask
import shared_graph

LOG = logging.getLogger('personal-assistant')
AREAS = (None, 'work', 'personal')
FOUND = 16          # messages the search brings back before the best SOURCES go in
FOUND_IN_DAYS = 400  # keyword matches looked at for a question about a time, before only those days are kept
PEOPLE = 8          # people with the name asked about that are weighed
PERSON_ROWS = 400   # of one person's messages in the days asked about, the newest looked at
EXAMPLE_PEOPLE = 6  # people from the open to-dos a suggested question may be about


def _meta(r):
    return r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')


def spread(rows, limit):
    """At most limit of these rows (newest first), spread over all of them rather than only the newest, so a busy
    week reads as a week and not as its last afternoon."""
    if len(rows) <= limit:
        return list(rows)
    step = len(rows) / limit
    return [rows[int(n * step)] for n in range(limit)]


class SearchAskApp:
    ACTIONS = {'search_ask': 'search_ask_action', 'search_ask_examples': 'search_ask_examples_action'}

    def search_ask_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Ask from search is only in your own dashboard.')
        return self.search_ask(args.get('query'), self.search_ask_area(args), args.get('plan'))

    def search_ask_examples_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Ask from search is only in your own dashboard.')
        if not getattr(self, 'ask_model', None) and has_model(self.config, wait=False):
            import model_service
            model_service.warm(self.config)  # the search is open: a question may follow, so load the model helper now
        return self.search_ask_examples(args.get('people'), self.search_ask_area(args))

    @staticmethod
    def search_ask_area(args):
        area = args.get('area')
        area = None if area in (None, '', 'all') else area
        if area not in AREAS:
            raise ValueError('Pick All, Work or Personal.')
        return area

    def search_ask_accounts(self, area):
        """The connections of the area the owner is looking at: every one for All."""
        return [a['id'] for a in self.config.get('accounts', []) if a.get('id') and (area is None or graph.account_side(a) == area)]

    def search_ask_keep(self, rows, area):
        """Rows without the threads the review judged to be about the owner's own life, with Work (todo_areas.py,
        knowledge.held)."""
        if area != 'work' or not rows:
            return rows
        try:
            with self.store.connect() as db:
                calls = {r[0]: r[1] for r in db.execute('SELECT thread,verdict FROM share_threads')}
        except sqlite3.OperationalError:
            calls = {}  # no Shared Graph here
        return [r for r in rows if calls.get(shared_graph.thread_of(r['kind'], _meta(r), r['id'])) != 'personal']

    def search_ask_rows(self, question, area, days=None, hits=None):
        """The messages the palette's search finds for the question (by meaning and keywords where local embeddings run,
        else by keywords), best first, in the area's connections only. days: (from, until) UTC bounds to keep only
        those days' messages. hits: {'ids', 'starts'} to fill with everything the search found, messages or not (the
        meeting notes and promises Ask reads from it, machine/app/ask_memory.py)."""
        accounts = self.search_ask_accounts(area)
        if not accounts:
            return []
        order, starts = [], {}
        if embeddings.settings(self.config):
            found, _ = self.related(accounts, (), question, FOUND if not days else 40, timeout=8)
            order, starts = [i for i, _ in found], embeddings.starts(found)
        if days or not order:
            with self.store.connect() as db:
                order += [i for i in embeddings.fts_ids(db, accounts, question, FOUND_IN_DAYS if days else FOUND) if i not in order]
        if not order:
            return []
        if hits is not None:
            hits.update(ids=order[:FOUND if not days else FOUND_IN_DAYS], starts=starts)
        rows = self.store.events(accounts, event_ids=order, kinds=list(graph.MESSAGE_KINDS))
        for row in rows:  # a long one that matched further on: the answer reads that part, not its start
            if row['id'] in starts and len(row['body']) > search_ask.SOURCE_CHARS:
                row['body'] = embeddings.passage_text(row['body'], starts[row['id']])
        if days:
            rows = [r for r in rows if self.search_ask_in(r, days)]
        place = {e: n for n, e in enumerate(order)}
        rows.sort(key=lambda r: place.get(r['id'], len(place)))
        return self.search_ask_keep(rows, area)[:FOUND if not days else search_ask.SCOPED_SOURCES]

    @staticmethod
    def search_ask_in(row, days):
        try:
            at = dt.datetime.fromisoformat(str(row['occurred_at']).replace('Z', '+00:00'))
        except ValueError:
            return False
        at = at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)
        start, until = (dt.datetime.fromisoformat(d) if d else None for d in days)
        return (not start or at >= start) and (not until or at < until)

    def search_ask_days_rows(self, area, days):
        """The newest messages of those days in the area: a question about a time with nothing more to look for."""
        accounts = self.search_ask_accounts(area)
        if not accounts:
            return []
        marks = ','.join('?' * len(accounts))
        kinds = ','.join('?' * len(graph.MESSAGE_KINDS))
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute(
                f'SELECT id FROM events WHERE account_id IN ({marks}) AND kind IN ({kinds}) AND deleted=0 AND occurred_at>=? AND occurred_at<? '
                'ORDER BY occurred_at DESC LIMIT ?', (*accounts, *graph.MESSAGE_KINDS, days[0], days[1], PERSON_ROWS))]
        rows = self.store.events(accounts, event_ids=ids, kinds=list(graph.MESSAGE_KINDS)) if ids else []
        return spread(self.search_ask_keep(rows, area), search_ask.SCOPED_SOURCES)

    def search_ask_owner(self, db):
        """mine(meta): whether the owner wrote a message (their address, Slack user or own number; a sent mail)."""
        owner = graph.Owner(self.config, db)

        def mine(m):
            if m.get('from_me') in (True, 'true', 'True', 1) or 'SENT' in (m.get('labels') or ()):
                return True
            if m.get('user_id') and m.get('user_id') in owner.slack:
                return True
            return any(a in owner.emails for _, a in graph.addresses(m.get('from'))[:1])
        return mine

    def search_ask_people(self, db, name):
        """[(node row, words)] for the people the name or address asked about could be: every word asked is a word of
        their name (so "Andrea" is never "Andreas"), or it is one of their addresses."""
        words = graph.name_words(name) if '@' not in name else []
        found = []
        for r in graph.find(db, name, 200, kinds=('person',)):
            info = json.loads(r['info'] or '{}')
            ids = {str(i).lower() for i in [r['id'], *(info.get('ids') or ())]}
            theirs = graph.name_words(r['name'], r['id'])
            if (words and set(words) <= set(theirs)) or name.lower() in ids or 'email:' + name.lower() in ids:
                found.append((r, theirs, ids))
        return found[:PEOPLE * 4]

    def search_ask_person_ids(self, db, node, days, accounts, limit=PERSON_ROWS):
        """Event ids of their messages (the Graph has them directly on it, not a guess), newest first, in the days."""
        marks, kinds = ','.join('?' * len(accounts)), ','.join('?' * len(graph.MESSAGE_KINDS))
        sql = (f'SELECT e.id FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id=? AND g.direct=1 AND g.probable=0 '
               f'AND e.deleted=0 AND e.account_id IN ({marks}) AND e.kind IN ({kinds})')
        args = [node, *accounts, *graph.MESSAGE_KINDS]
        if days and days[0]:
            sql += ' AND e.occurred_at>=?'
            args.append(days[0])
        if days and days[1]:
            sql += ' AND e.occurred_at<?'
            args.append(days[1])
        return [r[0] for r in db.execute(sql + ' ORDER BY e.occurred_at DESC LIMIT ?', (*args, limit))]

    def search_ask_person_rows(self, node, words, ids, days, area, said_by, mine, limit=PERSON_ROWS):
        """Their messages in the days (newest first): with said_by 'person' only the ones they wrote, with 'owner' only
        the owner's."""
        accounts = self.search_ask_accounts(area)
        if not accounts:
            return []
        with self.store.connect() as db:
            order = self.search_ask_person_ids(db, node, days, accounts, limit)
        if not order:
            return []
        rows = self.store.events(accounts, event_ids=order, kinds=list(graph.MESSAGE_KINDS))
        rows.sort(key=lambda r: r['occurred_at'], reverse=True)
        rows = self.search_ask_keep(rows, area)
        if said_by == 'person':
            rows = [r for r in rows if self.search_ask_theirs(_meta(r), words, ids, mine)]
        elif said_by == 'owner':
            rows = [r for r in rows if mine(_meta(r))]
        return rows

    @staticmethod
    def search_ask_theirs(m, words, ids, mine):
        """Whether they wrote this message: not the owner, and from one of their addresses, by their name, or in a chat
        with only the two of them."""
        if mine(m):
            return False
        sender = graph.addresses(m.get('from'))[:1]
        if sender and ('email:' + sender[0][1] in ids or sender[0][1] in ids):
            return True
        said = search_ask._who({k: m.get(k) for k in ('sender_display', 'from')})
        if said and words and graph.name_match(graph.name_words(said), words):
            return True
        one_to_one = m.get('conversation_type') in ('dm', 'im') or str(m.get('chat_id') or '').endswith('@s.whatsapp.net')
        return one_to_one and not said

    def search_ask_scoped(self, question, area, plan, mine, hits=None):
        """(rows, scope) for a question the first turn read: about a person, a time, or both. (None, None) when it is
        about neither: the search answers it as before. hits: as for search_ask_rows."""
        tz = timeutil.local_tz()
        today = self.search_ask_today()
        days = search_ask.bounds(plan['start'], plan['end'], tz) if plan.get('start') else None
        scope = {'tz': tz, 'today': today, 'start': plan.get('start'), 'end': plan.get('end'), 'said_by': plan['said_by']}
        if not plan.get('person') and not plan.get('node'):
            if not days:
                return None, None
            about = plan.get('about') or ''
            rows = self.search_ask_rows(about, area, days, hits) if about else []
            return rows or self.search_ask_days_rows(area, days), scope
        accounts = self.search_ask_accounts(area)
        with self.store.connect() as db:
            if plan.get('node'):
                row = graph.resolve(db, plan['node'])
                people = [(row, graph.name_words(row['name'], row['id']), {str(i).lower() for i in [row['id'], *(json.loads(row['info'] or '{}').get('ids') or ())]})] \
                    if row and row['kind'] == 'person' else []
            else:
                people = self.search_ask_people(db, plan['person'])
            # each one's messages in those days, then the ones with any first, the closest first
            weighed = [(len(self.search_ask_person_ids(db, r['id'], days, accounts, 50)) if accounts else 0, r['strength'] or 0, n)
                       for n, (r, _, _) in enumerate(people[:PEOPLE])]
        if not people:
            scope['unknown'] = plan['person']
            rows = self.search_ask_rows(plan.get('about') or question, area, days, hits)
            return rows, scope
        weighed.sort(key=lambda w: (w[0] > 0, w[1]), reverse=True)
        row, words, ids = people[weighed[0][2]]
        scope['name'] = row['name'] or graph.handle_shown(row['id'])
        scope['node'] = row['id']
        # Another with the name counts when they have messages in those days too, or are about as close to the owner
        top = weighed[0][1]
        scope['others'] = [people[n][0]['name'] for count, strength, n in weighed[1:]
                           if people[n][0]['name'] and people[n][0]['name'] != scope['name'] and (count or (top and strength >= top / 3))][:3]
        rows = self.search_ask_person_rows(row['id'], words, ids, days, area, plan['said_by'], mine)
        if rows and plan.get('about'):
            # what they said about something: the messages that match it first, then the rest by date
            with self.store.connect() as db:
                hits = embeddings.fts_ids(db, accounts, plan['about'], FOUND_IN_DAYS)
            place = {e: n for n, e in enumerate(hits)}
            rows.sort(key=lambda r: place.get(r['id'], len(place)))
            rows = rows[:search_ask.SCOPED_SOURCES]
        elif rows:
            rows = spread(rows, search_ask.SCOPED_SOURCES)
        elif days:
            scope['empty'] = True  # nothing in those days: their latest messages from another day
            rows = self.search_ask_person_rows(row['id'], words, ids, None, area, plan['said_by'], mine, 40)
            rows = [r for r in rows if str(r['occurred_at'])[:10] == str(rows[0]['occurred_at'])[:10]][:3] if rows else []
        return rows, scope

    @staticmethod
    def search_ask_today():
        """The owner's date now, in their time zone."""
        return dt.datetime.fromisoformat(now()).astimezone(timeutil.local_tz()).date()

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

    def search_ask(self, question, area=None, plan=None):
        """{'answer', 'sources'} (and 'messages': the other messages it read, newest first, when it read one person's or
        one time's; 'memory': the promises, facts, summaries and meeting notes it cited, ask_memory.py); {'none': True} when the words aren't a question or nothing was found; {'off': True} without a
        model; {'error': True} when the turn failed. plan: the person and days of a suggested question it offered
        (search_ask.given_plan), which skips the first turn. Never sends, drafts or makes a to-do."""
        import help_chat
        import model_service
        stand_in = getattr(self, 'ask_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        if not stand_in and not has_model(self.config, wait=False):  # never 10 s or more of `models status` first
            return {'off': True}
        question = search_ask.clean_question(question)
        if len(question.split()) < 2:
            return {'none': True}
        if stand_in:
            run = plan_run = lambda text: stand_in(self.config, text)
        else:
            model, thinking = self.search_ask_model()
            # one long-running helper, not a new OpenClaw process per turn (model_service.py)
            run = lambda text: model_service.run(self.config, text, model, thinking, timeout=search_ask.TIMEOUT)
            plan_run = lambda text: model_service.run(self.config, text, model, thinking, timeout=search_ask.PLAN_TIMEOUT)
        lang = locale_prefs.language_of(self.config)
        today = self.search_ask_today()
        read = search_ask.given_plan(plan, today)
        counted = False
        try:
            if read is None:
                read = search_ask.plan(question, plan_run, today, lang)
                counted = True
            if read is not None and not read['question']:
                return {'none': True}
        except (search_ask.Unavailable, help_chat.Unavailable) as error:
            LOG.info('search ask not planned error=%s', type(error).__name__)
            return {'error': True}
        try:
            with self.store.connect() as db:
                mine = self.search_ask_owner(db)
            hits = {}
            rows, scope = self.search_ask_scoped(question, area, read, mine, hits) if read else (None, None)
            if scope is None:
                rows = self.search_ask_rows((read or {}).get('about') or question, area, hits=hits)
        except (sqlite3.Error, ValueError, embeddings.EmbeddingError) as error:
            LOG.warning('search ask not searched error=%s', type(error).__name__)
            return {'error': True}
        try:
            memory = recall(self, 'ask', {'question': question}, search_ask.PROMPT_CHARS)
            days = search_ask.bounds(scope['start'], scope['end'], scope['tz']) if scope and scope.get('start') else None  # also when no message is of those days
            # what the Machine keeps that matches it: on the question's records, or on what the search found for it
            about = ask_memory.context(self, question, area, scope, hits.get('ids') or [r['id'] for r in rows or ()], hits.get('starts'), days,
                                       [r['id'] for r in rows or ()])
            kept, tags = ask_memory.read(memory, about, search_ask.PROMPT_CHARS)
            found = memory.read('sources', question, rows, run, lang, body=lambda b: shown_body(b)[0], scope=scope, counted=counted, mine=mine,
                                memory=kept, kept=tags)
            memory_use.record(self.store, 'ask', memory.rows())  # what its prompt held: ids only
        except (search_ask.Unavailable, help_chat.Unavailable) as error:
            LOG.info('search ask not answered error=%s', type(error).__name__)
            return {'error': True}
        if found and scope:
            cited = {s['id'] for s in found['sources']}
            rest = sorted((s for s in search_ask.sources(rows, lambda b: shown_body(b)[0], search_ask.SCOPED_SOURCES, mine) if s['id'] not in cited),
                          key=lambda s: s['at'], reverse=True)
            found['messages'] = [{k: s[k] for k in ('id', 'kind', 'title', 'from', 'at')} for s in rest[:4]]
        return found or {'none': True}

    def search_ask_examples(self, people, area=None):
        """The suggested questions Search may offer, only where the answer has something to go on: of these people (the
        open to-dos' in view), the ones who wrote the owner last week, each with its days ({'id', 'name', 'from',
        'to'}). No one: no suggestion (a general "what changed this week?" read as a week of everything, mostly noise)."""
        tz = timeutil.local_tz()
        today = self.search_ask_today()
        start, end = search_ask.last_week(today)
        days = search_ask.bounds(start, end, tz)
        out = []
        ids = [str(p)[:300] for p in (people if isinstance(people, list) else [])[:EXAMPLE_PEOPLE] if p]
        accounts = self.search_ask_accounts(area)
        if not accounts:
            return {'people': []}
        with self.store.connect() as db:
            mine = self.search_ask_owner(db)
            rows = [graph.resolve(db, i) for i in ids]
        for row in rows:
            if not row or row['kind'] != 'person' or any(o['id'] == row['id'] for o in out):
                continue
            words = graph.name_words(row['name'], row['id'])
            ids_of = {str(i).lower() for i in [row['id'], *(json.loads(row['info'] or '{}').get('ids') or ())]}
            if self.search_ask_person_rows(row['id'], words, ids_of, days, area, 'person', mine, 50):
                out.append({'id': row['id'], 'name': row['name'], 'from': start.isoformat(), 'to': end.isoformat()})
        return {'people': out[:3]}
