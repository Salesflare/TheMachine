"""Ask from search in the service (search_ask.py has the prompts and the answer): the messages a question finds in the
area the owner is looking at, and the turns that answer it. A mixin of assistant.App (APP_MIXINS).

A question about a person reads them through the Graph: the people whose name has the words asked (every one of
them, so "Andrea" finds each Andrea and never an Andreas), and of those the one with messages in the days asked
about, else the one the owner is most in touch with; the others are named to the answer so it says which one it
means. Their messages are the ones the Graph has them directly on (from or with them), never a message that only
mentions the name. A question about a time reads only the messages of those days, in the owner's time zone. A
question about the owner's own mailbox or chat account reads only its messages, and gets what the Machine knows of it
(ask_connections.py); with a subject nothing there matches, the rest of the area in view too (search_ask_beyond).

The Graph has what came in since its last build (up to half an hour) only later, so the newest messages are also looked
at for who sent them (search_ask_recent): the person's own, or of someone else with that name, who may be the one meant.
A question about minutes ago reads all that came in since, newest first, whatever words it has."""
import datetime as dt
import json
import logging
import re
import sqlite3

import embeddings
import graph
import help_search
import locale_prefs
import timeutil
from machine.app import ask_connections, ask_memory
from machine.app.recall import recall
from machine.text import shown_body
import memory_use
from timeutil import now
from models import background_model, has_model
import search_ask
import shared_graph
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
AREAS = (None, 'work', 'personal')
FOUND = 16          # messages the search brings back before the best SOURCES go in
FOUND_IN_DAYS = 400  # keyword matches looked at for a question about a time, before only those days are kept
PEOPLE = 8          # people with the name asked about that are weighed
NEWEST = 120        # of the connections asked about, the newest looked at for what came in
RECENT = 200        # newest messages looked at for who sent them: the Graph has what came in since its last build only later
LATELY = dt.timedelta(hours=3)  # someone else with the name asked about who wrote in this time may be the one meant
LATER = 6           # messages of those
LATEST = 8          # the newest, when nothing came in since the time asked about
THERE, BEYOND = 8, 4  # messages of the place asked about and from elsewhere, when nothing there matches the subject
PERSON_ROWS = 400   # of one person's messages in the days asked about, the newest looked at
EXAMPLE_PEOPLE = 6  # people from the open to-dos a suggested question may be about
WORD_LEADS = 3      # the best keyword matches that always reach the answer's messages


def _meta(r):
    return r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')


def spread(rows, limit):
    """At most limit of these rows (newest first), spread over all of them rather than only the newest, so a busy
    week reads as a week and not as its last afternoon."""
    if len(rows) <= limit:
        return list(rows)
    step = len(rows) / limit
    return [rows[int(n * step)] for n in range(limit)]


def name_words(name):
    """The whole words of a name, without accents and case, in any alphabet."""
    words = {help_search.fold(w).casefold() for w in re.findall(r'\w+', str(name or ''))}
    return words if '@' not in str(name or '') and any(len(w) > 1 for w in words) else set()


def sender_name(meta):
    """The name on a message of who sent it."""
    return search_ask._who({k: meta.get(k) for k in ('sender_display', 'from')})


def sender_full(meta, other):
    """The same, with their address when it is the name of another too."""
    name, address = sender_name(meta), graph.addresses(meta.get('from'))[:1]
    return f'{name} ({address[0][1]})' if address and name_words(name) == name_words(other) else name


class SearchAskApp:
    ACTIONS = {'search_ask': 'search_ask_action', 'search_ask_examples': 'search_ask_examples_action'}

    def search_ask_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise OwnerError('Ask from search is only in your own dashboard.')
        return self.search_ask(args.get('query'), self.search_ask_area(args), args.get('plan'), args.get('before'))

    def search_ask_examples_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise OwnerError('Ask from search is only in your own dashboard.')
        if not getattr(self, 'ask_model', None) and has_model(self.config, wait=False):
            import model_service
            model_service.warm(self.config)  # the search is open: a question may follow, so load the model helper now
        return self.search_ask_examples(args.get('people'), self.search_ask_area(args))

    @staticmethod
    def search_ask_area(args):
        area = args.get('area')
        area = None if area in (None, '', 'all') else area
        if area not in AREAS:
            raise OwnerError('Pick All, Work or Personal.')
        return area

    def search_ask_accounts(self, area):
        """The connections of the area the owner is looking at: every one for All."""
        return [a['id'] for a in self.config.get('accounts', []) if a.get('id') and (area is None or graph.account_side(a) == area)]

    def search_ask_within(self, area, only=None):
        """The area's connections, or of those the ones a question is about (only: ask_connections.resolve's ids)."""
        accounts = self.search_ask_accounts(area)
        return accounts if only is None else [a for a in accounts if a in only]

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

    def search_ask_rows(self, question, area, days=None, hits=None, only=None):
        """The messages the palette's search finds for the question (by meaning and keywords where local embeddings run,
        else by keywords), best first, in the area's connections only. days: (from, until) UTC bounds to keep only
        those days' messages. hits: {'ids', 'starts'} to fill with everything the search found, messages or not (the
        meeting notes and promises Ask reads from it, machine/app/ask_memory.py). only: the connections it is about."""
        accounts = self.search_ask_within(area, only)
        if not accounts:
            return []
        order, starts = [], {}
        if embeddings.settings(self.config):
            found, semantic = self.related(accounts, (), question, FOUND if not days else 40, timeout=8)
            order, starts = [i for i, _ in found], embeddings.starts(found)
            if semantic and not days:  # the best matches by words go in too: a name or place asked is never left out
                with self.store.connect() as db:
                    order = embeddings.words_lead(order, embeddings.best_word_hits(db, accounts, question, WORD_LEADS), search_ask.SOURCES)
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

    def search_ask_days_rows(self, area, days, only=None):
        """The messages of those days in the area, spread over them: a question about a time with nothing more to look
        for. only: the connections it is about."""
        accounts = self.search_ask_within(area, only)
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

    def search_ask_recent(self, area, only, days=None, limit=RECENT):
        """The newest messages in the area (only: of the connections a question is about), newest first, in the days."""
        accounts = self.search_ask_within(area, only)
        if not accounts:
            return []
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute(
                f"SELECT id FROM events WHERE account_id IN ({','.join('?' * len(accounts))}) AND kind IN ({','.join('?' * len(graph.MESSAGE_KINDS))}) "
                'AND deleted=0 AND occurred_at>=? AND occurred_at<=? ORDER BY occurred_at DESC LIMIT ?',
                (*accounts, *graph.MESSAGE_KINDS, days[0] if days else '', min(now(), days[1] or now()) if days else now(), limit))]
        rows = self.store.events(accounts, event_ids=ids, kinds=list(graph.MESSAGE_KINDS)) if ids else []
        rows.sort(key=lambda r: r['occurred_at'], reverse=True)
        return self.search_ask_keep(rows, area)

    def search_ask_newest(self, area, only, mine, said_by, days=None):
        """The newest messages of the connections a question is about, when it asks for nothing more: what came in, or
        what the owner sent when it asks that."""
        return [r for r in self.search_ask_recent(area, only, days, NEWEST) if mine(_meta(r)) == (said_by == 'owner')][:search_ask.SCOPED_SOURCES]

    def search_ask_beyond(self, scope, rows, look, area, only, search):
        """The messages of the place a question names (rows), where nothing matches its subject, and after them what
        search(connections) finds in the rest of the area in view: the subject may be meant elsewhere, or the place was
        only mentioned. scope['beyond'] says where each of those is from. look: false for a place that can't be read now
        (what it misses says nothing), or without a subject."""
        others = [a for a in self.search_ask_accounts(area) if a not in only] if look else []
        found = search(others)[:BEYOND] if others else []
        if not found:
            return rows
        accounts = {a['id']: a for a in self.config.get('accounts', []) if a.get('id')}
        scope['beyond'] = {r['id']: ask_connections.name(accounts[r['account_id']], accounts.values()) for r in found}
        return rows[:THERE] + found

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
        words = name_words(name)
        found = []
        for r in graph.find(db, name, 200, kinds=('person',)):
            info = json.loads(r['info'] or '{}')
            ids = {str(i).lower() for i in [r['id'], *(info.get('ids') or ())]}
            theirs = graph.name_words(r['name'], r['id'])
            if (words and words <= (set(theirs) | name_words(r['name']))) or name.lower() in ids or 'email:' + name.lower() in ids:
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

    def search_ask_person_rows(self, node, words, ids, days, area, said_by, mine, limit=PERSON_ROWS, only=None, recent=()):
        """Their messages in the days (newest first): with said_by 'person' only the ones they wrote, with 'owner' only
        the owner's. only: the connections the question is about. recent: the newest messages there, of which the Graph
        may not have theirs yet (search_ask_with)."""
        accounts = self.search_ask_within(area, only)
        if not accounts:
            return []
        with self.store.connect() as db:
            order = self.search_ask_person_ids(db, node, days, accounts, limit)
        order += [r['id'] for r in recent if r['account_id'] in accounts and r['id'] not in order and self.search_ask_with(_meta(r), words, ids, mine)]
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
    def search_ask_with(m, words, ids, mine):
        """Whether a message the Graph may not have yet is surely from this person (one of their addresses or chat ids, or
        in a chat without an address their whole name), or from the owner to one of their addresses."""
        known = lambda field: any('email:' + a in ids or a in ids for _, a in graph.addresses(m.get(field)))
        if mine(m):
            return known('to') or known('cc')
        if known('from') or str(m.get('sender_id') or '').lower() in ids:
            return True
        return not graph.addresses(m.get('from')) and graph.name_match(graph.name_words(sender_name(m)), words) == 'same'

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

    def search_ask_scoped(self, question, area, plan, mine, hits=None, listed=(), lang='en', before=()):
        """(rows, scope) for a question the first turn read: about a person, a time, their own mailbox or chat account,
        or several of these. (None, None) when it is about none: the search answers it as before. hits: as for
        search_ask_rows. listed: the connections the first turn could pick from."""
        tz = timeutil.local_tz()
        today = self.search_ask_today()
        days = search_ask.bounds(plan['start'], plan['end'], tz) if plan.get('start') else None
        at = dt.datetime.fromisoformat(now())
        scope = {'tz': tz, 'today': today, 'now': at.astimezone(tz), 'start': plan.get('start'), 'end': plan.get('end'), 'said_by': plan['said_by']}
        if ago := plan.get('ago'):  # "8 minutes ago" is seldom exact: twice as far back, and what came in since
            since = at - dt.timedelta(minutes=2 * ago + 5)
            days = (since.isoformat(), '')
            scope.update(ago=ago, since=search_ask.local_at(since.isoformat(), tz))
        only = None
        with self.store.connect() as db:
            got = ask_connections.resolve(self, db, plan, listed, area, ' '.join([*before, question]))
            if got:
                told, readable = ask_connections.facts(self, db, got, area, lang, tz)
                scope['connections'] = {'names': got['names'], 'facts': told}
                only = got['ids']
        if got and not only:  # not connected, or not in view: nothing to read
            return [], scope
        about = plan.get('about') or ''
        if not plan.get('person') and not plan.get('node'):
            if not days and not got:
                return None, None
            if ago:  # all that came in since, whatever words it has
                rows = self.search_ask_newest(area, only, mine, plan['said_by'], days)
                scope.update(newest=True, late=not rows)
                rows = rows or self.search_ask_newest(area, only, mine, plan['said_by'])[:LATEST]
                scope['none'] = not rows
                return rows, scope
            rows = self.search_ask_rows(about, area, days, hits, only) if about else []
            if not rows:
                rows = self.search_ask_days_rows(area, days, only) if days else self.search_ask_newest(area, only, mine, plan['said_by'])
                scope['newest'] = not days
                scope['none'] = not rows
                if got:
                    scope['nomatch'] = about
                    rows = self.search_ask_beyond(scope, rows, about and readable, area, only, lambda others: self.search_ask_rows(about, area, days, None, others))
            return rows, scope
        accounts = self.search_ask_within(area, only)
        recent = self.search_ask_recent(area, only, days)
        with self.store.connect() as db:
            if plan.get('node'):
                row = graph.resolve(db, plan['node'])
                people = [(row, graph.name_words(row['name'], row['id']), {str(i).lower() for i in [row['id'], *(json.loads(row['info'] or '{}').get('ids') or ())]})] \
                    if row and row['kind'] == 'person' else []
            else:
                people = self.search_ask_people(db, plan['person'])
            # each one's messages in those days, then the ones with any first, the closest first
            weighed = [((len(self.search_ask_person_ids(db, r['id'], days, accounts, 50)) if accounts else 0)
                        or sum(self.search_ask_with(_meta(m), words, ids, mine) for m in recent), r['strength'] or 0, n)
                       for n, (r, words, ids) in enumerate(people[:PEOPLE])]
        if not people:
            return self.search_ask_unknown(scope, question, about, area, days, hits, only, got and readable, mine, plan, recent)
        weighed.sort(key=lambda w: (w[0] > 0, w[1]), reverse=True)
        row, words, ids = people[weighed[0][2]]
        scope['name'] = row['name'] or graph.handle_shown(row['id'])
        scope['node'] = row['id']
        # Another with the name counts when they have messages in those days too, or are about as close to the owner
        top = weighed[0][1]
        scope['others'] = [people[n][0]['name'] for count, strength, n in weighed[1:]
                           if people[n][0]['name'] and people[n][0]['name'] != scope['name'] and (count or (top and strength >= top / 3))][:3]
        theirs = lambda within: self.search_ask_person_rows(row['id'], words, ids, days, area, plan['said_by'], mine, only=within, recent=recent)

        def matching(rows, accounts):
            # what they said about something: the messages that match it first, then the rest by date
            with self.store.connect() as db:
                place = {e: n for n, e in enumerate(embeddings.fts_ids(db, accounts, about, FOUND_IN_DAYS))}
            return sorted(rows, key=lambda r: place.get(r['id'], len(place))), any(r['id'] in place for r in rows)
        rows, matched, none = theirs(only), False, False
        if about and accounts:
            rows, matched = matching(rows, accounts)
            rows = rows[:search_ask.SCOPED_SOURCES]
        if got and about and not matched:
            scope['nomatch'], there = about, rows
            rows = self.search_ask_beyond(scope, there, readable, area, only, lambda others: matching(theirs(others), others)[0])
            none = bool(rows) and not there
        later = self.search_ask_later(plan, recent, rows, words, ids, mine)
        if later and not rows:  # nothing of theirs: only of who wrote in the last hours
            scope.update(name='', node='', others=[], unknown=plan['person'], named={r['id']: sender_name(_meta(r)) for r in later}, none=False)
            return later, scope
        if rows:
            rows = rows if about else spread(rows, search_ask.SCOPED_SOURCES)
        elif days:
            scope['empty'] = True  # nothing in those days: their latest messages from another day
            rows = self.search_ask_person_rows(row['id'], words, ids, None, area, plan['said_by'], mine, 40, only, self.search_ask_recent(area, only))
            rows = [r for r in rows if str(r['occurred_at'])[:10] == str(rows[0]['occurred_at'])[:10]][:3] if rows else []
        scope['later'] = {r['id']: sender_full(_meta(r), scope['name']) for r in later}
        rows = rows[:search_ask.SCOPED_SOURCES - len(later)] + later
        scope['none'] = none or not rows
        return rows, scope

    def search_ask_later(self, plan, recent, rows, words, ids, mine):
        """The messages among recent of someone else with the name asked about, who wrote in the last hours (LATELY): they
        may be the one meant, whoever the owner is most in touch with."""
        asked = set() if plan.get('node') or plan['said_by'] == 'owner' else name_words(plan['person'])
        have, lately = {r['id'] for r in rows}, ((dt.datetime.fromisoformat(now()) - LATELY).isoformat(), '')
        return [r for r in recent if asked and r['id'] not in have and self.search_ask_in(r, lately) and not mine(_meta(r))
                and asked <= name_words(sender_name(_meta(r))) and not self.search_ask_with(_meta(r), words, ids, mine)][:LATER]

    def search_ask_unknown(self, scope, question, about, area, days, hits, only, readable, mine, plan, recent=()):
        """(rows, scope) for a question about someone who isn't in the Graph: what the search finds, first what is from
        someone with that name (scope['named']: their name on each of those). recent: the newest messages there in the
        days, looked at for that name too, as words in a message seldom say who sent it. only, readable: the connections
        it names; with a subject and nothing from them found there, the rest of the area in view too (search_ask_beyond)."""
        scope['unknown'] = plan['person'] or ''
        asked = name_words(scope['unknown'])

        def theirs(rows):
            return [r for r in rows if not mine(_meta(r)) and (asked <= name_words(sender_name(_meta(r))) if asked else
                                                               scope['unknown'].casefold() in {a for _, a in graph.addresses(_meta(r).get('from'))[:1]})]
        rows = self.search_ask_rows(about or question, area, days, hits, only)
        if only and not theirs(rows):
            latest = theirs(recent)[:search_ask.SCOPED_SOURCES]
            scope['newest'] = bool(latest and not days)
            rows = latest or rows
            scope['none'] = not rows
            if about:
                scope['nomatch'] = about
                rows = self.search_ask_beyond(scope, rows, readable, area, only, lambda others: theirs(self.search_ask_rows(about, area, days, None, others)))
        else:  # what they sent lately, also where the words asked about are not in it
            have = {r['id'] for r in rows}
            rows = [r for r in theirs(recent)[:search_ask.SOURCES] if r['id'] not in have] + rows
        scope['named'] = {r['id']: sender_name(_meta(r)) for r in theirs(rows)}
        scope.setdefault('none', not rows)
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

    def search_ask(self, question, area=None, plan=None, before=None):
        """{'answer', 'sources'} (and 'messages': the other messages it read, newest first, when it read one person's or
        one time's; 'memory': the promises, facts, summaries and meeting notes it cited, ask_memory.py); {'none': True} when the words aren't a question or nothing was found; {'off': True} without a
        model; {'error': True} when the turn failed. plan: the person and days of a suggested question it offered
        (search_ask.given_plan), which skips the first turn. before: the questions asked just before it, oldest first, which
        it may go on from (search_ask.earlier). Never sends, drafts or makes a to-do."""
        import help_chat
        import model_service
        stand_in = getattr(self, 'ask_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        if not stand_in and not has_model(self.config, wait=False):  # never 10 s or more of `models status` first
            return {'off': True}
        question = search_ask.clean_question(question)
        before = search_ask.earlier(before)
        if len(question.split()) < 2 and not (before and question):
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
        listed = ask_connections.listed(self, area) if read is None else []
        try:
            if read is None:
                read = search_ask.plan(question, plan_run, today, lang, listed, before)
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
            rows, scope = self.search_ask_scoped(question, area, read, mine, hits, listed, lang, before) if read else (None, None)
            if scope is None:
                rows = self.search_ask_rows((read or {}).get('about') or question, area, hits=hits)
        except (sqlite3.Error, ValueError, embeddings.EmbeddingError) as error:
            LOG.warning('search ask not searched error=%s', type(error).__name__)
            return {'error': True}
        try:
            memory = recall(self, 'ask', {'question': question}, search_ask.PROMPT_CHARS)
            kept, tags = '', {}
            days = search_ask.bounds(scope['start'], scope['end'], scope['tz']) if scope and scope.get('start') else None  # also when no message is of those days
            # what the Machine keeps that matches it: on the question's records, or on what the search found for it
            if not (scope and scope.get('connections')):  # one about their own mailbox is answered from its messages alone
                about = ask_memory.context(self, question, area, scope, hits.get('ids') or [r['id'] for r in rows or ()], hits.get('starts'), days,
                                           [r['id'] for r in rows or ()])
                kept, tags = ask_memory.read(memory, about, search_ask.PROMPT_CHARS)
            found = memory.read('sources', question, rows, run, lang, body=lambda b: shown_body(b)[0], scope=scope, counted=counted, mine=mine,
                                memory=kept, kept=tags, before=before)
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
