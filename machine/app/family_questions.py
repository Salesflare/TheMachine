"""A family member's question in the service (family_questions.py has its path, family_question_sources.py what an answer
may come from): the turn on the question alone, the search in the owner's personal messages, the turn that drafts the
answer and, for a member on Always, the layers that let it go by itself after a hold (family_question_always.py). On a
thread of its own, apart from the Fleet's loop. A mixin of assistant.App (APP_MIXINS)."""
import logging
import sqlite3
import threading
from pathlib import Path

import embeddings
import family_question_always as always
import family_question_check as fqc
import family_question_facts as fqf
import family_question_hold
import family_question_links as links
import family_question_sources as fqs
import family_questions
import fleet
import help_chat
from i18n import t
from machine import bridge_wait
from machine.dashboard_link import dashboard_link
from machine.delivery.push import push_reach, push_send
from machine.delivery.telegram import fleet_telegram
from machine.model_usage import telegram_on
from machine.text import shown_body
import model_service
from models import has_model
import notify
import own_addresses
import security_levels
import timeutil

LOG = logging.getLogger('personal-assistant')
TIMEOUT = 60
HITS, NEWEST = 3, 4  # of what it reads: the best hits, then the newest on the same matter as those
FOUND = 40  # messages the search brings back, before the ones that may not go in are left out
SECRET = 'a surprise, a present or a secret plan for {}; {} does not know and should not find out'


def said_body(text):
    return shown_body(text)[0]


class FamilyQuestionsApp:
    ACTIONS = {}

    def question_soon(self, ask_id):
        threading.Thread(target=self.question_draft_run, args=(ask_id,), name='family-question', daemon=True).start()

    def question_draft_run(self, ask_id):
        """Drafts one question's answer, once. Whatever goes wrong, the question then waits for the owner without one."""
        ask = self.fleet.question_claim(ask_id)
        if not ask:
            return None
        result = {'state': 'failed'}
        try:
            result = self.question_result(ask)
        except (sqlite3.Error, ValueError, OSError, embeddings.EmbeddingError, help_chat.Unavailable) as error:
            LOG.warning('family question not drafted error=%s', type(error).__name__)
        finally:
            self.fleet.question_drafted(ask_id, result)
        return result['state']

    def question_company(self):
        """(the owner's company's domains, their teammates' addresses): never family."""
        return self.fleet.own_domains(), {e.lower() for ref in self.fleet.work_fleets() for m in self.fleet.teammates(ref) for e in m.get('emails') or ()}

    def question_found(self, question):
        """The owner's messages an answer may come from, best first, as the model would read them."""
        mine = fqs.accounts(self.config)
        if not mine:
            return []
        order = []
        if embeddings.settings(self.config):
            found, semantic = self.related(mine, (), question, FOUND, timeout=8)
            order = [i for i, _ in found]
            if semantic:
                with self.store.connect() as db:
                    order = embeddings.words_lead(order, embeddings.best_word_hits(db, mine, question, 3), fqs.SOURCES)
        with self.store.connect() as db:
            order += [i for i in embeddings.fts_ids(db, mine, question, FOUND) if i not in order]
        rows = self.store.events(mine, event_ids=order, kinds=list(fqs.KINDS)) if order else []
        place = {e: n for n, e in enumerate(order)}
        rows.sort(key=lambda r: place.get(r['id'], len(place)))
        with self.store.connect() as db:
            kept = fqs.allowed(db, rows, self.config, *self.question_company())
            more = self.question_newest(db, kept[:HITS], question)
            owner = self.search_ask_owner(db)
        return fqs.sources([*kept[:HITS], *more, *[r for r in kept[HITS:] if r['id'] not in {m['id'] for m in more}]], said_body, owner)

    def question_newest(self, db, hits, question):
        """The newest messages on the same matter as the best hits, which the search's words or meaning may have missed."""
        accounts = fqs.accounts(self.config)
        found = links.linked(db, hits, links.mailed(db, self.store, accounts, timeutil.clock()), question)
        ids = [e for e in found if e not in {r['id'] for r in hits}]
        rows = self.store.events(accounts, event_ids=ids, kinds=list(fqs.KINDS)) if ids else []
        rows = fqs.allowed(db, list(rows), self.config, *self.question_company())
        rows.sort(key=lambda r: (found[r['id']] == 'sender', -links.moment(r['occurred_at']).timestamp()))
        return rows[:NEWEST]

    def question_turn(self, prompt):
        """One turn without tools, with nothing of another turn's."""
        stand_in = getattr(self, 'ask_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        if stand_in:
            return stand_in(self.config, prompt)
        model, thinking = self.search_ask_model()
        return model_service.run(self.config, prompt, model, thinking, timeout=TIMEOUT)

    def question_result(self, ask):
        """{'state', 'asked', 'text', 'sources', 'mark'}. A question the first turn didn't clear as an ordinary
        household matter, or that it couldn't run for, reads nothing."""
        if not getattr(self, 'ask_model', None) and not has_model(self.config, wait=False):
            return {'state': 'none'}
        if self.background_pause(job='question:' + ask['id']) is not None or not self.fleet.question_run(ask['id']):
            return {'state': 'held'}
        owner = self.question_owner(ask)
        asked = {'asked': fqc.reading(self.question_turn(fqc.prompt(ask['question'], self.fleet.question_earlier(ask), ask['name'], owner)))}
        if asked['asked'] != fqc.HOUSEHOLD:
            return {'state': 'none', **asked}
        found = self.question_found(ask['question'])
        if not found:
            return {'state': 'empty', **asked}
        read = fqs.reading(self.question_turn(fqs.prompt(ask['question'], found, ask['name'], owner, timeutil.today())), found)
        if read['state'] != 'ready':
            return {**read, **asked}
        kept = [{k: found[n - 1][k] for k in ('id', 'kind', 'title', 'from', 'at')} for n in read['sources']]
        draft = {'state': 'ready', 'text': read['text'][:family_questions.ANSWER_CHARS], 'sources': kept, **asked}
        with self.store.connect() as db:
            may = self.fleet.question_always(db, ask['fleet'], ask['member_id']) and self.fleet.question_may(db, ask['fleet'], ask['member_id'])
        if not may:
            return draft
        try:
            return {**draft, 'mark': self.question_mark(ask, draft)}
        except (sqlite3.Error, ValueError, OSError, embeddings.EmbeddingError, help_chat.Unavailable) as error:
            LOG.warning('family question not checked error=%s', type(error).__name__)
            return draft

    # -- by itself: the layers, and the hold's hooks
    def question_mark(self, ask, draft):
        """What is on the matter now, when every layer lets this answer go by itself; else None."""
        seen = {}
        for layer, good in self.question_layers(ask, draft, seen):
            if not good:
                LOG.info('family question asks first layer=%s', layer)
                return None
        return seen['mark']

    def question_layers(self, ask, draft, seen, today=None):
        """(layer, whether it lets the answer go), cheapest first: family_question_always.py says what each looks at."""
        today = today or timeutil.today()
        rows, asker = self.question_rows(draft), self.question_asker(ask)
        with self.store.connect() as db:
            mine = {e.lower() for e in own_addresses.yours(db, self.config)}
            every = links.mailed(db, self.store, fqs.accounts(self.config), timeutil.clock())
            gift = always.season(today) or always.near_birthday(db, asker['emails'], today)
        yield 'answer', len(rows) == len(draft['sources']) and always.first(ask['question'], draft['text'], rows, lambda r: links.believed(r, every, mine, asker))
        yield 'season', not (gift and always.bought(rows))
        found = self.question_matter(ask, draft, rows, asker, near=True)
        seen['why'] = found['why']
        yield 'matter', found['why'] is None
        words = links.tokens(ask['question'])
        with self.store.connect() as db:
            seen['mark'] = always.mark(db, found['watch'])
            titles = always.todos(db, self.config, words)
            read = always.items(found['rows'], said_body, self.search_ask_owner(db), asker, words)
        owner = self.question_owner(ask)
        second = always.reading(self.question_turn(always.prompt(ask['question'], draft['text'], read, titles, ask['name'], owner, today, self.fleet.question_earlier(ask))))
        yield 'second', second['safe']
        facts = fqf.reading(self.question_turn(fqf.prompt(ask['question'], read, ask['name'], owner, today)))
        seen['stops'] = fqf.stops(facts, found['rows'][:len(read)], {r['id'] for r in rows}, second, draft['text'], timeutil.clock(timeutil.local_tz()), every)
        yield 'facts', seen['stops'] is None
        yield 'bought', not gift or not always.bought(rows, second, facts)

    def question_rows(self, draft):
        return list(self.store.events(fqs.accounts(self.config), event_ids=[s['id'] for s in draft['sources']], kinds=list(fqs.KINDS)))

    def question_asker(self, ask):
        who = self.fleet.member(ask['fleet'], ask['member_id']) or {}
        return {'name': ask['name'], 'emails': [e.lower() for e in who.get('emails') or ()], 'first': (str(who.get('name') or '').split() or [''])[0]}

    def question_matter(self, ask, draft, rows, asker, near=False):
        ids = []
        if near and embeddings.settings(self.config):
            for seeds, words in (((), SECRET.format(asker['first'], asker['first'])), ([r['id'] for r in rows], ask['question'])):
                ids += [i for i, _ in self.related(fqs.accounts(self.config), seeds, words, always.NEAR, timeout=8)[0]]
        with self.store.connect() as db:
            return always.matter(db, self.store, self.config, rows, ask['question'], draft['text'], asker, *self.question_company(), near=ids)

    def question_moved(self, ask_id, mark):
        """Whether something on a held answer's matter is new or changed since it was checked."""
        with self.store.connect() as db:
            row = db.execute('SELECT id,fleet,member_id,name,question FROM fleet_in WHERE id=?', (str(ask_id),)).fetchone()
            draft = self.fleet.question_draft(db, ask_id)
        if not row or draft.get('state') != 'ready':
            return True
        ask = {**dict(row), 'question': (family_questions._load(row['question']) or {}).get('text') or ''}
        rows = self.question_rows(draft)
        if len(rows) != len(draft['sources']):
            return True
        found = self.question_matter(ask, draft, rows, self.question_asker(ask))
        with self.store.connect() as db:
            return found['why'] is not None or always.moved(mark, always.mark(db, found['watch']), found['watch'])

    def question_notify_hold(self, row, hold):
        """The notice of an answer that goes by itself, at once: True, or the Telegram message's id, when it reached the
        owner's phone or Telegram; None when it reached neither. A held notification, an email or a Machine nobody looks at
        doesn't count: the question then waits for them."""
        reached = None
        subscriptions, phones = push_reach(self.store, self.config)
        with self.store.connect() as db:
            push = (subscriptions or phones) and notify.allowed(db, 'result', 'push')
            shows = security_levels.notify_text(db)
        if push:
            line, text = family_question_hold.hold_line(row, hold), family_question_hold.hold_text(row)
            sent = push_send(self.store, self.config, subscriptions, {
                'title': line, 'body': text if shows else '', 'url': dashboard_link(self.config) + '#fleet=' + row['id'], 'tag': 'fleet-' + row['id'],
                'actions': [{'action': 'stop', 'title': t('Stop')}, {'action': 'open', 'title': t('Open')}]}, 'fleet=' + row['id'], kind='result', held=True, wake='fleet')
            reached = True if any(200 <= int(r.get('status') or 0) < 300 and r.get('app', 1) for r in sent) else None
        # Only with the bridge of this release in the Gateway: an older one drops a tap on Stop, and the answer would go
        if telegram_on(self.config) and self.notify_on('result', 'telegram') and bridge_wait.loaded(Path(self.config['database']).expanduser().parent):
            message = str(fleet_telegram(self.config, fleet.telegram_message([row], dashboard_link(self.config))).get('messageId') or '')
            reached = message if message.isdigit() else reached
        return reached

    def question_owner(self, ask):
        me = next((m for m in (self.fleet.fleets().get(ask['fleet']) or {}).get('members') or () if m.get('me')), {})
        return str(me.get('name') or '').split()[0] if str(me.get('name') or '').split() else 'the owner'
