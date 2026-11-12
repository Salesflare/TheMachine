"""The suggest action around its save (App.action 'suggest_save'): a dedupe_key the review left out is made from the
source message, arguments it got wrong are told back in words, and a save that fails keeps its messages for the next
review (machine/store/review_saves.py). A mixin of assistant.App (APP_MIXINS)."""
import json
import logging
import sqlite3

from calendar_clashes import with_others
from machine.app.preparation import activity_lines
from machine.cards import undated_card
from machine.store import review_saves
from machine.store.review import bulk_kind
from mail_senders import automated
from machine.store import outcomes
import todo_areas

LOG = logging.getLogger('personal-assistant')

# A new to-do whose evidence is automated mail alone (ReviewSavesApp.automated_only): that mail informs a to-do, and
# makes one only when it asks the owner to act itself. Told back once, like "read what came after first"; mail_asks
# (what the mail asks, in a few words) says the review judged it so. Costs a step only for these few to-dos.
AUTOMATED_ONLY = (review_saves.AUTOMATED_GUIDANCE + ' (a booking, receipt, notification or newsletter), with no message from a '
                  'person. Such mail informs a to-do; on its own it makes one only when the mail itself asks the owner to act '
                  '(an invoice to pay by hand, a card or plan that runs out). A step you work out from it, like moving the '
                  'owner\'s own plans around a booking, is no to-do: they made both and move their own. Judge what the mail '
                  'asks, never its wording. When it does ask, suggest again with mail_asks: what it asks, in a few words.')


class ReviewSavesApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'suggest': 'suggest_action', 'suggest_save': 'suggest_save_action'}

    def suggest_action(self, name, args, owner_dashboard):
        with self.store.connect() as db:
            args = review_saves.ready(db, args)
        try:
            saved = self.action('suggest_save', args, owner_dashboard)
        except ValueError as error:
            if not str(error).startswith(review_saves.STEPS):  # "read what came after first" and the like are steps, not failures
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

    def automated_only(self, event_ids):
        """Whether a new to-do's evidence is automated mail alone: at least one mail a program sent (a booking, receipt,
        notification or newsletter: what the review sees as a title line, or Precedence bulk or Auto-Submitted), and
        besides those only the owner's own calendar entries with nobody else on them. No message from a person, no
        meeting with someone, nothing the owner wrote. Read from the headers, never from words in the mail."""
        ids = [i for i in event_ids if isinstance(i, int)]
        if not ids:
            return False
        with self.store.connect() as db:
            rows = db.execute(f"SELECT kind,title,metadata FROM events WHERE id IN ({','.join('?' * len(ids))})", ids).fetchall()
        mail = False
        for row in rows:
            try:
                metadata = json.loads(row['metadata'] or '{}')
            except ValueError:
                return False
            if not isinstance(metadata, dict):
                return False
            if row['kind'] == 'calendar.event':
                if with_others({'meta': metadata}):
                    return False
            elif row['kind'] == 'gmail.message' and (bulk_kind(row['kind'], metadata, row['title']) or automated(metadata) and not (
                    metadata.get('from_me') or set(metadata.get('labels') or ()) & {'SENT', 'DRAFT'})):
                mail = True
            else:
                return False
        return mail

    def handoff_target(self, email, personal):
        """The review's handoff_to (a teammate's email from its Teammates list) as the Fleet member it is: {'fleet',
        'member_id'}, or None when there is none. One that isn't such a teammate is told back before anything is saved."""
        email = str(email or '').strip().lower()
        if not email:
            return None
        fleets = getattr(self, 'fleet', None)
        found = fleets.teammate({'to_email': email}) if fleets and not personal and email in fleets.handoff_people() else None
        if not found:
            raise ValueError('handoff_to is the email of a teammate under Teammates, each with their own Machine, on a work '
                             'to-do. Leave it out when the to-do is not one to hand to them.')
        return {'fleet': found[0], 'member_id': found[1]['member_id']}

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
        if not args.get('card_id') and not str(args.get('mail_asks') or '').strip() and self.automated_only(args['event_ids']):
            raise ValueError(AUTOMATED_ONLY)
        if not args.get('card_id'):
            # A new to-do only when nothing since shows it handled: what came after its evidence is read first
            newer = self.newer_unchecked(args['event_ids'], args.get('newer_checked'))
            if newer:
                raise ValueError('Something happened after this to-do\'s evidence. Read these with events before making it:\n' + activity_lines(newer)
                                 + '\nWhen they show it handled (the owner answered or did it, here or on another channel, someone else took '
                                 'care of it, a meeting covered it, a later message settled it) or no longer the owner\'s, make no to-do. '
                                 'Otherwise suggest again with newer_checked: [these event ids], saying in the body what is still open.')
        done_when = outcomes.clean(args.get('done_when'))  # checked before anything is saved
        # A title or summary that says "today" or "tomorrow" is wrong the day after: saved with the day itself
        (title, body), stale = undated_card(str(args['title'] or ''), str(args['body'] or ''))
        if args.get('based_on') is not None:
            with self.store.connect() as db:
                self.store.based_on_check(db, args['based_on'])
        handoff_to = self.handoff_target(args.get('handoff_to'), personal)  # checked before anything is saved
        saved = self.store.suggest(args['dedupe_key'], title, body, args['event_ids'], args.get('when') or 'digest',
                                   self.config.get('digest_at', '08:30'),work=work,urgent=args.get('urgent') is True,due=args.get('due'),
                                   ahead=args.get('prepare_ahead') is True and self.config.get('prepare_ahead', True) is not False
                                   and self.store.ahead_room(int(self.config.get('prepare_ahead_per_day', 10)), args.get('urgent') is True, args.get('due')),
                                   awaiting=args.get('awaiting_event_id'),project=args.get('project'),card_id=args.get('card_id'),
                                   separate=args.get('separate') is True,reopen=args.get('reopen') is True,match=True,
                                   owner_step=(args['owner_step'] is True) if 'owner_step' in args else None,
                                   expires_at=args.get('expires_at'), expires_what=args.get('expires_what'), company=company, personal=personal,
                                   waiting_on=args.get('waiting_on') or None,
                                   # the organization the matter is about, in the review's word; none said is none (never from who is on it)
                                   org=str(args.get('org') or ''))
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
        if isinstance(saved, dict) and saved.get('id') and not saved.get('duplicate') and not saved.get('attached'):
            with self.store.connect() as db:  # who its Hand off starts with: the teammate the review offers it to, or none
                self.store.set_handoff_to(db, saved['id'], handoff_to)
        if isinstance(saved, dict) and saved.get('id') and done_when:
            with self.store.connect() as db:  # the result that counts as done: a send alone doesn't close it (outcomes.py)
                outcomes.set_done_when(db, saved['id'], done_when, 'review')
        unknown = self.store.no_role_yet(args['event_ids'])
        if isinstance(saved, dict) and unknown:  # name them now, while the evidence is open
            saved['no_role_yet'] = unknown
            saved['hint'] = ('The people on this card have no role yet. If the evidence shows what they are to the owner, '
                             'set it with graph node_id, role, event_id and quote; otherwise leave it.')
        return saved
