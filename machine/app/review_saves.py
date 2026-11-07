"""The suggest action around its save (App.action 'suggest_save'): a dedupe_key the review left out is made from the
source message, arguments it got wrong are told back in words, and a save that fails keeps its messages for the next
review (machine/store/review_saves.py). A mixin of assistant.App (APP_MIXINS)."""
import logging
import sqlite3

from machine.store import review_saves

LOG = logging.getLogger('personal-assistant')


class ReviewSavesApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'suggest': 'suggest_action'}

    def suggest_action(self, name, args, owner_dashboard):
        with self.store.connect() as db:
            args = review_saves.ready(db, args)
        try:
            saved = self.action('suggest_save', args, owner_dashboard)
        except ValueError as error:
            if not str(error).startswith(review_saves.GUIDANCE):  # "read what came after first" is a step, not a failure
                self.save_failed(args['event_ids'], error)
            raise
        except (KeyError, TypeError, sqlite3.Error) as error:
            self.save_failed(args['event_ids'], error)
            missing = f' (missing {error.args[0]})' if isinstance(error, KeyError) and error.args else ''
            raise ValueError(f'The to-do was not saved{missing}. Check the suggest args and try once more; its messages '
                             'stay unreviewed, so a later review tries them again.') from error
        with self.store.connect() as db:
            review_saves.saved(db, args['event_ids'])
        return saved

    def save_failed(self, event_ids, error):
        LOG.warning('suggest failed error=%s', type(error).__name__)
        try:
            with self.store.connect() as db:
                review_saves.failed(db, event_ids, type(error).__name__)
        except sqlite3.Error as record_error:
            LOG.warning('suggest failure record error=%s', type(record_error).__name__)
