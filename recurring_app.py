"""Recurring to-dos, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Repeats in New to-do (card_new with repeat, or a rhythm in the words), More > Repeat on a to-do (card_repeat), Skip
this one (card_repeat_skip), a custom rhythm read from words (repeat_read), the one-time "Make this a recurring
to-do?" (recurring_offer), and the worker that brings each series' next to-do on its date (recurring.py)."""
import datetime as dt
import json
import logging
import os
import secrets
import threading
from zoneinfo import ZoneInfo

import recurring

LOG = logging.getLogger('personal-assistant')
OFFER_EVERY = 3600  # seconds between looks for new offers


class RecurringApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'card_repeat': 'card_repeat_action',
        'card_repeat_skip': 'card_repeat_skip_action',
        'recurring_offer': 'recurring_offer_action',
        'repeat_read': 'repeat_read_action',
    }

    def recurring_tz(self):
        """The owner's timezone, as the service's own (config timezone, else ASSISTANT_TIMEZONE)."""
        try:
            return ZoneInfo(self.config.get('timezone') or os.environ.get('ASSISTANT_TIMEZONE') or 'Europe/Amsterdam')
        except Exception:
            return ZoneInfo('Europe/Amsterdam')

    def recurring_today(self):
        return dt.datetime.now(self.recurring_tz()).date()

    @staticmethod
    def recurring_stamp():
        return dt.datetime.now(dt.timezone.utc).isoformat()

    def recurring_work(self, card):
        """Whether a to-do is Work: its first account's boundary (work:<company>)."""
        ids = json.loads(card['account_ids'] or '[]')
        return any(a['id'] == (ids[0] if ids else None) and str(a.get('boundary') or '').startswith('work:') for a in self.config.get('accounts', []))

    def recurring_lock(self):
        if not hasattr(self, '_recurring_lock'):
            self._recurring_lock = threading.Lock()
        return self._recurring_lock

    # --- actions -----------------------------------------------------------------------------------------------------

    def card_new_repeating(self, args):
        """New to-do, repeating: a Repeats choice (repeat: a preset or a rule), or a rhythm in the words themselves
        ("every first Monday do payroll"; also from Talk and the voice New to-do, which make to-dos the same way).
        repeat: false keeps the words as they are."""
        rule, anchor, args = None, None, dict(args)
        today = self.recurring_today()
        due = args.get('due')
        if args.get('repeat') not in (None, False, '', 'none'):
            rule = recurring.clean_rule(args['repeat'])
            try:
                anchor = dt.date.fromisoformat(str(due)) if due else today
            except ValueError:
                raise ValueError('due is YYYY-MM-DD') from None
            if rule['unit'] == 'weekday' or rule.get('nth') is not None:
                anchor = recurring.anchor_for(rule, anchor, nth=rule.get('nth'))
        elif args.get('repeat') is None:
            got = recurring.parse(args.get('text'), today)
            if got and len(got['rest']) >= 2:
                rule, anchor = got['rule'], got['anchor']
                args['text'] = got['rest']
                if not due and anchor != today:
                    args['due'], args['due_at'] = anchor.isoformat(), None
                elif due:
                    anchor = dt.date.fromisoformat(str(due))
        saved = self.new_card(args)
        if rule:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                card = db.execute('SELECT * FROM suggestions WHERE id=?', (saved['id'],)).fetchone()
                recurring.start(db, card, rule, anchor, card['owner_words'] or card['title'], self.recurring_stamp(), self.recurring_work(card))
            saved['repeats'] = {'rule': rule, 'anchor': anchor.isoformat()}
        return saved

    def card_repeat_action(self, name, args, owner_dashboard):
        """More > Repeat on a to-do: start repeating, change the rhythm, or stop (repeat: none). words: a rhythm in the
        owner's words (the to-do's chat: "repeat this every first Monday", "stop repeating")."""
        if not owner_dashboard:
            raise ValueError('Repeats are set by the owner, on the dashboard')
        sid = str(args.get('suggestion_id') or '')
        today, stamp = self.recurring_today(), self.recurring_stamp()
        repeat = args.get('repeat')
        if args.get('words') is not None:
            words = str(args.get('words') or '')
            if recurring.STOP.search(words):
                repeat = 'none'
            else:
                got = recurring.parse(words, today)
                if not got:
                    raise ValueError('I can’t read that rhythm yet. Try every week, every first Monday or every 3 months.')
                repeat = got['rule']
        with self.recurring_lock(), self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            card = db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone()
            if not card:
                raise ValueError('Unknown to-do')
            series = recurring.series_of(db, sid)
            running = series if series and not series['stopped_at'] and series['current_id'] == sid else None
            if repeat in (None, '', 'none', False):
                if running:
                    recurring.stop(db, running['id'], stamp)
                return {'id': sid, 'repeats': None}
            rule = recurring.clean_rule(repeat)
            if running:
                recurring.change(db, running, rule, stamp, today)
            else:
                if card['status'] in recurring.CLOSED:
                    raise ValueError('Only an open to-do can repeat')
                try:
                    anchor = dt.date.fromisoformat(str(card['due'])[:10]) if card['due'] else today
                except ValueError:
                    anchor = today
                if rule['unit'] == 'weekday' or rule.get('nth') is not None:
                    anchor = recurring.anchor_for(rule, anchor, nth=rule.get('nth'))
                recurring.start(db, card, rule, anchor, card['owner_words'] or card['title'], stamp, self.recurring_work(card))
            view = {'id': sid, 'status': card['status']}
            recurring.annotate(db, [view], today)
        return {'id': sid, 'repeats': view.get('repeats')}

    def card_repeat_skip_action(self, name, args, owner_dashboard):
        """Skip this one: the open occurrence closes as not needed and the next comes on its date."""
        if not owner_dashboard:
            raise ValueError('Repeats are set by the owner, on the dashboard')
        sid = str(args.get('suggestion_id') or '')
        with self.store.connect() as db:
            series = recurring.series_of(db, sid)
        if not series or series['stopped_at'] or series['current_id'] != sid:
            raise ValueError('This to-do doesn’t repeat')
        self.store.decide(sid, 'reject', 'Skipped this one; it repeats', 'repeat-skip-' + secrets.token_hex(6), 'dashboard')
        self.recurring_step()
        with self.store.connect() as db:
            row = db.execute('SELECT next_due FROM recurring_series WHERE id=?', (series['id'],)).fetchone()
        return {'id': sid, 'next': row['next_due'] if row else None}

    def repeat_read_action(self, name, args, owner_dashboard):
        """Custom… in Repeats: the rhythm in the owner's words, read as a rule (nothing is saved)."""
        got = recurring.parse(str(args.get('text') or '')[:200], self.recurring_today())
        return {'rule': got['rule'], 'anchor': got['anchor'].isoformat()} if got else {'rule': None}

    def recurring_offer_action(self, name, args, owner_dashboard):
        """Make this a recurring to-do? Yes repeats the open to-do it is about, or adds one that repeats; No thanks
        never asks again. Either way only on the owner's tap."""
        if not owner_dashboard:
            raise ValueError('Repeats are set by the owner, on the dashboard')
        key, yes = str(args.get('key') or ''), args.get('choice') == 'yes'
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            offer = recurring.answer_offer(db, key, yes, self.recurring_stamp())
        if not yes:
            return {'key': key, 'made': None}
        rule = json.loads(offer['rule'])
        if offer['card_id']:
            try:
                return {'key': key, 'made': self.card_repeat_action('card_repeat', {'suggestion_id': offer['card_id'], 'repeat': rule}, True)['id']}
            except ValueError:
                pass  # closed since: a new one instead
        made = self.card_new_repeating({'text': offer['text'], 'repeat': rule, 'due': offer['anchor'],
                                        'scope': args.get('scope') if args.get('scope') in ('work', 'personal') else None})
        return {'key': key, 'made': made['id']}

    # --- the worker --------------------------------------------------------------------------------------------------

    def recurring_step(self):
        """Each running series' next to-do, on its date; made as an ordinary to-do in the same account and project."""
        today, stamp = self.recurring_today(), self.recurring_stamp()
        accounts = self.config.get('accounts', [])
        with self.recurring_lock():
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                due = recurring.tick(db, today, stamp)
            for s in due:
                ids = [a['id'] for a in accounts]
                account = s['account_id'] if s['account_id'] in ids else next(
                    (a['id'] for a in accounts if str(a.get('boundary') or '').startswith('work:') == bool(s['work'])), ids[0] if ids else None)
                if not account:
                    continue
                try:
                    saved = self.store.owner_card(s['text'], account, work=bool(s['work']), due=s['next_due'], project=s['project'])
                except ValueError as error:
                    LOG.warning('recurring next to-do error=%s', error)
                    continue
                with self.store.connect() as db:
                    recurring.made(db, s['id'], saved['id'], s['next_due'], stamp)
        return len(due)

    def recurring_offers_step(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            return recurring.find_offers(db, self.recurring_today(), self.recurring_stamp(), self.recurring_tz())

    def recurring_worker(self):
        last = 0.0
        while not self.stop.wait(60):
            try:
                self.recurring_step()
                if dt.datetime.now().timestamp() - last > OFFER_EVERY:
                    last = dt.datetime.now().timestamp()
                    self.recurring_offers_step()
            except Exception as error:
                LOG.error('recurring error=%s', type(error).__name__)
