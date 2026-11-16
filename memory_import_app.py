"""Import memory from another assistant, the App's part: a domain mixin of App (only machine/main.py composes it;
docs/code-map.md). The owner's own dashboard only.

memory_import_prompt gives the prompt the owner copies into the other assistant. memory_import_review reads a pasted answer (memory_import.review: secrets out first, then one small turn on the
background model compares the rest with what is learned) and returns what the review screen shows; nothing is saved.
memory_import_save keeps the lines the owner picked there (memory_import.save). Between the two the review's lines
are held here in memory, at most REVIEWS of them for REVIEW_SECONDS, so an edit on the review is told from the line
as imported; the pasted answer itself is never kept."""
import logging
import secrets
import threading
import time

import help_chat
import memory_import
from models import background_model
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
REVIEWS = 4
REVIEW_SECONDS = 2 * 3600
HELD = threading.Lock()  # the reviews held between the two actions


class MemoryImportApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'memory_import_prompt': 'memory_import_action', 'memory_import_review': 'memory_import_action',
               'memory_import_save': 'memory_import_action'}

    def memory_import_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise OwnerError('Only the owner imports memory, on the dashboard')
        if name == 'memory_import_prompt':  # what the dialog's Copy prompt copies
            return {'prompt': memory_import.PROMPT, 'assistants': memory_import.ASSISTANTS}
        assistant = str(args.get('from') or '')
        if assistant not in memory_import.ASSISTANTS:
            raise OwnerError('Pick ChatGPT, Claude or Gemini')
        if name == 'memory_import_review':
            return self.memory_import_review(assistant, args.get('text'))
        return self.memory_import_save(assistant, str(args.get('token') or ''), args.get('picks'))

    def memory_import_ask(self, text):
        """One turn on the background model (no tools), or None when it can't answer."""
        ask = getattr(self, 'memory_import_model', None)  # tests and the sandbox: (prompt) -> reply
        if ask:
            return ask(text)
        model = background_model(self.config)
        try:
            return help_chat.openclaw_model_run(self.config, text, '/'.join(model) if model else None, timeout=memory_import.TIMEOUT)
        except help_chat.Unavailable:
            return None

    def memory_import_review(self, assistant, text):
        if not str(text or '').strip():
            raise OwnerError('Paste the answer first')
        known = [{'id': f['id'], 'text': f['text']} for f in self.store.facts() if f['kind'] == 'fact']
        known.reverse()  # newest first: what the turn reads when there is more than it takes
        found = memory_import.review(text, known, self.memory_import_ask)
        token = secrets.token_urlsafe(12)
        with HELD:
            held = self.__dict__.setdefault('memory_reviews', {})
            for key in [k for k, v in held.items() if v['at'] < time.monotonic() - REVIEW_SECONDS]:
                held.pop(key)
            while len(held) >= REVIEWS:  # the oldest review goes
                held.pop(min(held, key=lambda k: held[k]['at']))
            held[token] = {'at': time.monotonic(), 'from': assistant,
                           'shown': {i['n']: (i['text'], (i.get('conflict') or {}).get('id')) for i in found['items']}}
        LOG.info('memory import review from=%s shown=%s known=%s secrets=%s permissions=%s judged=%s', assistant, len(found['items']),
                 found['known'], found['secrets'], found['permissions'], found['judged'])
        return {**found, 'token': token, 'from': assistant}

    def memory_import_save(self, assistant, token, picks):
        with HELD:
            held = self.__dict__.get('memory_reviews', {}).get(token)
            if not held or held['from'] != assistant or held['at'] < time.monotonic() - REVIEW_SECONDS:
                raise OwnerError('That review expired. Paste the answer again.')
        if not isinstance(picks, list) or not picks:
            raise OwnerError('Pick at least one line')
        done = memory_import.save(self.store, assistant, token, held['shown'], picks)
        with HELD:
            self.__dict__.get('memory_reviews', {}).pop(token, None)
        LOG.info('memory import saved from=%s saved=%s replaced=%s skipped=%s', assistant, done['saved'], done['replaced'], done['skipped'])
        return done
