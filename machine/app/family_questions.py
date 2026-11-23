"""A family member's question in the service (family_questions.py has its path, family_question_sources.py what an answer
may come from): the turn on the question alone (family_question_check.py), the search in the owner's personal messages and
the turn that drafts the answer, on a thread of its own, apart from the Fleet's loop. A mixin of assistant.App (APP_MIXINS)."""
import logging
import sqlite3
import threading

import embeddings
import family_question_check as fqc
import family_question_sources as fqs
import family_questions
import help_chat
from machine.text import shown_body
import model_service
from models import has_model
import timeutil

LOG = logging.getLogger('personal-assistant')
TIMEOUT = 60
FOUND = 40  # messages the search brings back, before the ones that may not go in are left out


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
            team = {e.lower() for ref in self.fleet.work_fleets() for m in self.fleet.teammates(ref) for e in m.get('emails') or ()}
            kept = fqs.allowed(db, rows, self.config, self.fleet.own_domains(), team)
            owner = self.search_ask_owner(db)
        return fqs.sources(kept, lambda text: shown_body(text)[0], owner)

    def question_turn(self, prompt):
        """One turn without tools, with nothing of another turn's."""
        stand_in = getattr(self, 'ask_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        if stand_in:
            return stand_in(self.config, prompt)
        model, thinking = self.search_ask_model()
        return model_service.run(self.config, prompt, model, thinking, timeout=TIMEOUT)

    def question_result(self, ask):
        """{'state', 'asked', 'text', 'sources'}. A question the first turn didn't clear as an ordinary household matter, or
        that it couldn't run for, reads nothing."""
        if not getattr(self, 'ask_model', None) and not has_model(self.config, wait=False):
            return {'state': 'none'}
        if self.background_pause(job='question:' + ask['id']) is not None or not self.fleet.question_run(ask['id']):
            return {'state': 'held'}
        owner = self.question_owner(ask)
        asked = fqc.reading(self.question_turn(fqc.prompt(ask['question'], self.fleet.question_earlier(ask), ask['name'], owner)))
        if asked != family_questions.HOUSEHOLD:
            return {'state': 'none', 'asked': asked}
        found = self.question_found(ask['question'])
        if not found:
            return {'state': 'empty', 'asked': asked}
        read = fqs.reading(self.question_turn(fqs.prompt(ask['question'], found, ask['name'], owner, timeutil.today())), found)
        if read['state'] != 'ready':
            return {**read, 'asked': asked}
        kept = [{k: found[n - 1][k] for k in ('id', 'kind', 'title', 'from', 'at')} for n in read['sources']]
        return {'state': 'ready', 'asked': asked, 'text': read['text'][:family_questions.ANSWER_CHARS], 'sources': kept}

    def question_owner(self, ask):
        me = next((m for m in (self.fleet.fleets().get(ask['fleet']) or {}).get('members') or () if m.get('me')), {})
        return str(me.get('name') or '').split()[0] if str(me.get('name') or '').split() else 'the owner'
