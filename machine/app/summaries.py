"""Person summaries in the service (person_summary.py has the summaries): now and then one background turn rewrites the
lines of a few people whose evidence changed, and the owner's own change to a line. Moved out of assistant.App as is. A
mixin of assistant.App (APP_MIXINS)."""
import json
import logging
import sqlite3
import threading

import graph
import locale_prefs
from models import background_model
import person_summary
from timeutil import now

LOG = logging.getLogger('personal-assistant')


class SummariesApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    SUMMARY_SECONDS = 300

    def summary_step(self):
        """Now and then: one background turn rewrites the summaries of a few people whose evidence changed
        (person_summary.py), in a thread of its own, within the usage budget like every background turn."""
        if not (self.config.get('review_worker') or {}).get('enabled'):
            return None
        thread = getattr(self, '_summary_thread', None)
        if thread and thread.is_alive():
            return None
        if not self.background_spaced() or self.background_pause(job='person-summary'):
            return None
        with self.store.connect() as db:
            people = person_summary.due(db)
        if not people:
            return None
        self.background_started()
        self._summary_thread = threading.Thread(target=self.summary_run, args=(people,), name='person-summary', daemon=True)
        self._summary_thread.start()
        return len(people)

    def summary_run(self, people):
        """One pass: the people's evidence, one turn, their lines saved (a proposal where the owner edited theirs)."""
        import help_chat
        stand_in = getattr(self, 'summary_model', None)  # a stand-in in the sandbox and tests: (config, prompt)
        with self.store.connect() as db:
            run_id = person_summary.start_run(db, len(people), now())
        status, error, written = 'ok', None, 0
        try:
            with self.store.connect() as db:
                owner = graph.Owner({'accounts': self.config.get('accounts', [])}, db)
                owner.slack |= set(getattr(self.store, 'owner_user_ids', None) or ())
                pages = [person_summary.evidence(db, owner, p, graph.person_evidence) for p in people]
            lang = locale_prefs.language_of(self.config)
            if stand_in:
                ask = lambda text: stand_in(self.config, text)
            else:
                swap = background_model(self.config)
                ask = lambda text: help_chat.openclaw_model_run(self.config, text, '/'.join(swap) if swap else None, timeout=self.SUMMARY_SECONDS)
            found = self.summary_checked(ask, pages, lang)
            sides = {a.get('id'): graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')}
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                for p in people:  # one the turn wrote nothing for waits for newer evidence too
                    if person_summary.save(db, p['id'], found.get(p['id'], []), p['evidence_at'], sides, cleared=p['id'] in found) != 'nothing':
                        written += 1
        except help_chat.Unavailable:
            status, error = 'failed', 'model'
        except (sqlite3.Error, ValueError, KeyError, TypeError, OSError) as failure:
            status, error = 'failed', type(failure).__name__
        with self.store.connect() as db:
            person_summary.finish_run(db, run_id, status, error, written)
        if error:
            LOG.warning('person summaries not written error=%s', error)
        return written

    @staticmethod
    def summary_checked(ask, pages, lang):
        """The pass's lines, each past the check (person_summary.check_prompt): a rejected line is written again once
        with the reason and checked again; one that still fails is dropped. ask(text) runs one model turn. A first check
        that can't be read fails the pass (ValueError), so nothing unchecked is saved and the people stay due."""
        found = person_summary.parse(ask(person_summary.prompt(pages, lang)), pages)
        if not any(found.values()):
            return found
        text, index = person_summary.check_prompt(found, pages)
        kept, rejected = person_summary.judged(found, index, person_summary.verdicts(ask(text), index))
        if not rejected:
            return kept
        again = person_summary.parse(ask(person_summary.rewrite_prompt(pages, kept, rejected, lang)), pages)
        again = {node_id: lines for node_id, lines in again.items() if node_id in rejected and lines}
        if again:
            text, index = person_summary.check_prompt(again, pages)
            try:
                passed, _ = person_summary.judged(again, index, person_summary.verdicts(ask(text), index))
            except ValueError:  # the second check unreadable: the rewrites go, what passed the first time stays
                passed = {}
            for node_id, lines in passed.items():
                seen = {line['text'] for line in kept[node_id]}
                kept[node_id] += [line for line in lines if line['text'] not in seen]
        for node_id, lines in kept.items():
            lines.sort(key=lambda x: person_summary.KINDS.index(x['kind']))
            del lines[person_summary.MAX_LINES:]
        return kept

    def summary_change(self, args):
        """The owner on a person's summary: op edit (lines), use (the suggested update), keep (theirs, without it), reset."""
        op = args.get('op')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = graph.resolve(db, str(args.get('node_id') or ''))
            if not row or row['kind'] != 'person':
                raise ValueError('Unknown person')
            if op == 'edit':
                person_summary.edit(db, row['id'], args.get('lines'), json.loads(row['info'] or '{}').get('side'))
            elif op == 'use':
                person_summary.use_proposal(db, row['id'])
            elif op == 'keep':
                person_summary.dismiss_proposal(db, row['id'])
            elif op == 'reset':
                person_summary.reset(db, row['id'])
            else:
                raise ValueError('op is edit, use, keep or reset')
            return {'summary': person_summary.view(db, row['id'])}
