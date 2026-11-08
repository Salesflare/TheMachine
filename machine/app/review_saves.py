"""The suggest action around its save (App.action 'suggest_save'): a dedupe_key the review left out is made from the
source message, arguments it got wrong are told back in words, and a save that fails keeps its messages for the next
review (machine/store/review_saves.py). A mixin of assistant.App (APP_MIXINS)."""
import logging
import sqlite3

from machine.app.preparation import activity_lines
from machine.cards import undated_card
from machine.store import review_saves
import todo_areas

LOG = logging.getLogger('personal-assistant')


class ReviewSavesApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'suggest': 'suggest_action', 'suggest_save': 'suggest_save_action'}

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

    def suggest_save_action(self, name, args, owner_dashboard=False):
        # suggest, with its args checked first (machine/app/review_saves.py)
        # The agent's suggestions wait for the morning digest unless it says otherwise.
        with self.store.connect() as db:
            source_accounts={r[0] for r in db.execute('SELECT account_id FROM events WHERE id IN ('+','.join('?' for _ in args['event_ids'])+')',args['event_ids'])} if args['event_ids'] else set()
        company=args.get('company') or None  # mail for another of the owner's companies: the to-do goes there (owner_companies)
        if company is not None:
            source_accounts=set(todo_areas.company_accounts(company,self.config['accounts']))
        # the owner's own life (family, friends, home), also on a work mailbox: Personal from the start (todo_areas.py)
        personal=company is None and (args.get('personal') is True or bool(args.get('family_with')))
        work=not personal and any(a['id'] in source_accounts and a.get('boundary','').startswith('work:') for a in self.config['accounts'])
        if not args.get('card_id'):
            # A new to-do only when nothing since shows it handled: what came after its evidence is read first
            newer = self.newer_unchecked(args['event_ids'], args.get('newer_checked'))
            if newer:
                raise ValueError('Something happened after this to-do\'s evidence. Read these with events before making it:\n' + activity_lines(newer)
                                 + '\nWhen they show it handled (the owner answered or did it, here or on another channel, someone else took '
                                 'care of it, a meeting covered it, a later message settled it) or no longer the owner\'s, make no to-do. '
                                 'Otherwise suggest again with newer_checked: [these event ids], saying in the body what is still open.')
        # A title or summary that says "today" or "tomorrow" is wrong the day after: saved with the day itself
        (title, body), stale = undated_card(str(args['title'] or ''), str(args['body'] or ''))
        if args.get('based_on') is not None:
            with self.store.connect() as db:
                self.store.based_on_check(db, args['based_on'])
        saved = self.store.suggest(args['dedupe_key'], title, body, args['event_ids'], args.get('when') or 'digest',
                                   self.config.get('digest_at', '08:30'),work=work,urgent=args.get('urgent') is True,due=args.get('due'),
                                   ahead=args.get('prepare_ahead') is True and self.config.get('prepare_ahead', True) is not False
                                   and self.store.ahead_room(int(self.config.get('prepare_ahead_per_day', 10))),
                                   awaiting=args.get('awaiting_event_id'),project=args.get('project'),card_id=args.get('card_id'),
                                   separate=args.get('separate') is True,reopen=args.get('reopen') is True,match=True,
                                   owner_step=(args['owner_step'] is True) if 'owner_step' in args else None,
                                   expires_at=args.get('expires_at'), expires_what=args.get('expires_what'), company=company, personal=personal)
        if isinstance(saved, dict) and stale:
            saved['dates'] = (f"Saved {', '.join(sorted({w.lower() for w in stale}))} as the day itself: a to-do is read on later days, so name "
                              'the weekday or date, never today, tomorrow or yesterday.')
        if isinstance(saved, dict) and saved.get('id') and args.get('skill_hint') and getattr(self, 'skills', None):
            saved['skill_hint'] = self.skills.hint(saved['id'], args['skill_hint'])  # "There's a skill for this", if it clearly helps
        if isinstance(saved, dict) and saved.get('id') and not saved.get('duplicate') and args.get('meet'):
            saved['meet'] = self.meet_begin(saved['id'], args['meet'], args['event_ids'])  # their Machine, if any, agrees a time (meet_app.py)
        if isinstance(saved, dict) and saved.get('id') and args.get('family_with') and getattr(self, 'fleet', None):
            # family coordination with someone the review knows is family: maybe a quiet "Invite them?" (family_invites.py)
            try:
                saved['family_invite'] = self.fleet.family_invite_offer(saved['id'], str(args['family_with']), work)
            except (sqlite3.Error, ValueError) as error:
                LOG.warning('family invite offer error=%s', type(error).__name__)
        if isinstance(saved, dict) and saved.get('id') and not saved.get('duplicate') and args.get('based_on') is not None:
            with self.store.connect() as db:  # the teammate's input the to-do follows: shown on it, with its link
                self.store.mark_based_on(db, saved['id'], args['based_on'])
        if isinstance(saved, dict) and saved.get('id') and not saved.get('duplicate') and not saved.get('attached'):
            with self.store.connect() as db:  # what the owner may want to say in its chat: each update says it again
                self.store.set_chat_asks(db, saved['id'], args.get('asks'))
        unknown = self.store.no_role_yet(args['event_ids'])
        if isinstance(saved, dict) and unknown:  # name them now, while the evidence is open
            saved['no_role_yet'] = unknown
            saved['hint'] = ('The people on this card have no role yet. If the evidence shows what they are to the owner, '
                             'set it with graph node_id, role, event_id and quote; otherwise leave it.')
        return saved
