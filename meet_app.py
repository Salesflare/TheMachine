"""Scheduling between Machines, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The protocol is meet.py (on the Fleet); this wires it to the app: a meeting request the review marks on a to-do
(suggest with `meet`) asks the other person's Machine, the other side's to-do (meet_card), Book it as the owner's own
calendar write with the invite (meet_book), and the owner's taps and setting from the dashboard (meet_decide,
meet_setting). Design: docs/scheduling-between-machines.md."""
import hashlib
import json
import logging
import re
import threading

import calendar_writes
import graph
import i18n
import meet
import meet_link
import next_actions

LOG = logging.getLogger('personal-assistant')
EMAIL = re.compile(r'[^@\s<>(),;:"\[\]]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+')


class MeetApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'meet_decide': 'meet_decide_action',
        'meet_setting': 'meet_setting_action',
    }

    def meet_attach(self, hours, tz):
        """The Fleet's hooks for meet.py: on once this Machine is on the Network (fleet_attach)."""
        box = self.fleet
        box.meet_card, box.meet_book, box.meet_close = self.meet_card, self.meet_book, self.meet_close
        box.meet_link_draft = self.meet_link_draft
        box.meet_hours, box.meet_tz = hours, tz
        box.meet_on = True

    # -- the dashboard
    def meet_decide_action(self, name, args, owner_dashboard):
        """Book it, Other time or Not needed on a scheduling to-do: the owner's own tap, from the dashboard only."""
        if not owner_dashboard:
            raise ValueError('Book it, Other time and Not needed are your own taps, in the dashboard')
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine is not on The Machine Network')
        return self.fleet.meet_decide(str(args.get('suggestion_id') or ''), str(args.get('choice') or ''))

    def meet_setting_action(self, name, args, owner_dashboard):
        """What other Machines may ask this one, and the meeting preferences. Read with no args; set from the dashboard."""
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine is not on The Machine Network')
        change = {k: args[k] for k in ('allow', 'minutes', 'buffer', 'prefer', 'brand') if args.get(k) is not None}
        if change and not owner_dashboard:
            raise ValueError('This setting is changed in the dashboard')
        return self.fleet.meet_set(**change) if change else self.fleet.meet_setting()

    # -- the review's meeting request (suggest with `meet`)
    def meet_begin(self, card_id, request, event_ids):
        """A to-do the review marked as a meeting request: ask the other person's Machine, in the background. Only an
        address from the to-do's own evidence (its sender or recipients), so a review can't make this Machine look
        anyone else up. Without a calendar to book on, or without a Machine there, the to-do stays as it is."""
        fleet = getattr(self, 'fleet', None)
        if not fleet or not fleet.meet_on or not isinstance(request, dict):
            return None
        email = str(request.get('with') or '').strip().lower()
        if not EMAIL.fullmatch(email) or email in {e.lower() for e in self.owner_emails()} or email not in self.meet_evidence_addresses(event_ids):
            return None
        if not self.meet_calendar():
            return None
        minutes = request.get('minutes') if request.get('minutes') in meet.LENGTHS else None
        days = request.get('days') if isinstance(request.get('days'), int) and not isinstance(request.get('days'), bool) else None
        start = str(request.get('start') or '')[:10] or None
        name = ' '.join(str(request.get('name') or '').split())[:80]

        def run():
            try:
                fleet.meet_start(card_id, email, name, minutes=minutes, start=start, days=days)
            except Exception as error:  # noqa: BLE001 - the to-do keeps its email draft
                LOG.warning('meet start error=%s', type(error).__name__)
        threading.Thread(target=run, name='meet-start', daemon=True).start()
        return 'asking'

    def meet_evidence_addresses(self, event_ids):
        """The addresses on these events: senders and recipients."""
        if not event_ids:
            return set()
        with self.store.connect() as db:
            rows = db.execute(f"SELECT metadata FROM events WHERE id IN ({','.join('?' * len(event_ids))})", list(event_ids)).fetchall()
        found = set()
        for (meta,) in rows:
            try:
                meta = json.loads(meta or '{}')
            except ValueError:
                continue
            for key in ('from', 'to', 'cc', 'reply-to'):
                found |= {m.group(0).lower() for m in EMAIL.finditer(str(meta.get(key) or ''))}
        return found

    def meet_calendar(self):
        """The owner's own Google calendar that sends invites, or None (then the email draft does it)."""
        return next((c for c in calendar_writes.calendars(self.config) if c['invite']), None)

    # -- the Fleet's hooks
    def meet_card(self, session):
        """The other side's to-do for a time another Machine proposed: Book it, Other time, Not needed. Its evidence
        is an event on one of the owner's accounts, marked reviewed so no review or preparation reads it by itself."""
        accounts = self.config.get('accounts', [])
        account = next((a for a in accounts if a.get('service') == 'calendar'), accounts[0] if accounts else None)
        if not account:
            raise ValueError('No account here for this')
        name = session.get('name') or session.get('email') or i18n.t('someone')
        key = 'meet:' + str(session['id'])
        body = session.get('body') or i18n.t('{}’s Machine found a time that suits you both. The invite goes out once you both tap Book it.', name)
        meta = {'sender_display': i18n.t('{} (The Machine Network)', name), 'meet_session': session['id']}
        event_id = self.store.reviewed_event(account['id'], key, 'meet.request', session['title'], body, meta)
        card = self.store.suggest(key, session['title'][:90], body[:700], [event_id], when='now', work=graph.account_side(account) == 'work')
        return card['id']

    def meet_book(self, session):
        """Both owners tapped Book it: the event on the owner's own calendar, with an invite to the other person
        (Google sends it). The same session books once (its request id)."""
        calendar = self.meet_calendar()
        if not calendar:
            return {'status': 'failed', 'error': 'no calendar'}
        start, end = json.loads(session['slot'])
        name = session.get('name') or session['email']
        video = meet.VIDEO.get(session.get('video'))
        args = {'request_id': hashlib.sha256(('meet:' + session['id'] + ':' + start).encode()).hexdigest()[:32], 'op': 'create',
                'calendar': calendar['id'], 'title': i18n.t('Meeting with {}', name), 'start': meet.parse_slot(start).isoformat(),
                'end': meet.parse_slot(end).isoformat(), 'guests': [session['email']], 'invite': 1}
        if video:
            args['notes'] = i18n.t('Video: {}', video)
        return self.calendar_write(args)

    def meet_link_draft(self, card_id, email, lines):
        """A booking link into the to-do's email draft to that address, while it is still a draft (meet_link.py): the
        owner sees it before Send. False when there is no such draft (yet)."""
        with self.store.connect() as db:
            row = db.execute('SELECT status,next_action FROM suggestions WHERE id=?', (str(card_id),)).fetchone()
        if not row or row['status'] != 'prepared' or not row['next_action']:
            return False
        current = json.loads(row['next_action'])
        drafts = [a for a in (current.get('actions') if current.get('kind') == 'menu' else [current]) if a.get('kind') == 'email'
                  and email in {f.group(0).lower() for x in a.get('to') or [] for f in EMAIL.finditer(str(x))}]
        if not drafts:
            return False
        body = next_actions.draft_text(drafts[0]) or ''
        revised = meet_link.with_lines(body, lines)
        if revised != body:
            self.store.revise_draft(str(card_id), drafts[0].get('revision'), 'agent', None, revised)
        return True

    def meet_close(self, card_id, why):
        try:
            self.store.decide(card_id, 'complete', why, 'meet-close-' + hashlib.sha256((card_id + why).encode()).hexdigest()[:12], 'assistant')
        except (ValueError, KeyError) as error:
            LOG.info('meet close error=%s', type(error).__name__)
