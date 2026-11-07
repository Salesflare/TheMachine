"""The Fleet in the service (refactor PR 22; fleet.py has the Fleet itself): attaching it to this Machine, its pings and
notices, the to-dos and briefs it makes, team votes and shared learnings, shared connectors and device grants, and the
view Settings shows. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import copy
import datetime as dt
import json
import re
import secrets
import sqlite3
import threading
import time
import types
import uuid

import fleet
import fleet_learnings
import graph
import handoff_mail
import i18n
import locale_prefs
from machine.actions import CONTACT_ACTIONS
from machine.cards import card_task, plain
from machine.config import LOG
from machine.delivery.deliver import fleet_notice_push, fleet_push
from machine.delivery.push import hold_handoff, hold_mail, mail_ready, push_reach, push_send, quick_web
from machine.delivery.telegram import fleet_telegram
from machine.faults import code_version, restart_self, running_release
from machine.model_usage import telegram_on
from machine.sources.connectors import CONNECTOR_HELPERS, load_connector
from machine.store.review import own_message
import notify
import security_levels
import shared_graph
from sources import credential, SourceError
import team_learnings
from timeutil import in_hours, is_work_day, local_tz, now, WORK_HOURS
import work_removal


def fleet_served(config):
    """The tailnet address `tailscale serve` proxies to this dashboard (onboarding.dashboard_served), or None: which of
    its Tailscale names answers, for the phone app's address (fleet.app_address)."""
    import onboarding
    return onboarding.dashboard_served(config)


def own_or_joined(event, owner_slack_ids=()):
    """Whether an event is the owner's own doing: a message they sent (own_message), or a call that started, with others
    in it, that they didn't decline. A message they only received never is."""
    if str(event['kind']).endswith('calendar.event'):
        m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
        people = [a for a in m.get('attendees') or [] if isinstance(a, dict)]
        me = next((a for a in people if a.get('self')), None)
        joined = (me.get('responseStatus') != 'declined') if me else bool((m.get('organizer') or {}).get('self'))
        started = dt.datetime.fromisoformat(event['occurred_at']) <= dt.datetime.now(dt.timezone.utc)
        return joined and started and any(not a.get('self') for a in people)
    return own_message(event, owner_slack_ids)


class FleetApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def fleet_attach(self):
        """Builds self.fleet with the App's hooks: at start, and again when the Machine pairs from its dashboard
        (fleet_live). None while it isn't paired."""
        config = self.config
        self.fleet = fleet.Fleet(self.store.connect, config, lambda: credential(config, 'fleet')) if fleet.settings(config) and config.get('credentials', {}).get('fleet') else None
        if self.fleet:
            self.fleet.notify = self.fleet_notify
            self.fleet.can_ping = self.fleet_can_ping
            self.fleet.served = fleet_served  # the phone app's address: the tailnet one that answers (fleet.app_address)
            self.fleet.soon = lambda fn: threading.Thread(target=fn, name='graph-after-ok', daemon=True).start()  # Share: the heavy round after the tap
            self.fleet.retell = lambda message_id: threading.Thread(target=self.fleet_retell, args=(message_id,), daemon=True).start()
            self.fleet.notify_notice = self.fleet_notify_notice
            self.fleet.release = running_release  # said when it asks whether a bug the owner reported is fixed here
            self.fleet.language = lambda: locale_prefs.language_of(self.config)
            self.fleet.make_card, self.fleet.tell = self.fleet_card, self.fleet_tell  # Fleet requests (fleet_requests.py)
            # Ask to review (fleet_reviews.py): what a review of a to-do shows, accepted changes into the owner's own draft
            # (a new revision: Send stays theirs), and a review to-do closed once its reviewer answered
            self.fleet.review_subject, self.fleet.review_write = self.review_subject, self.review_write
            self.fleet.done_card = lambda card_id, choice, why, key: self.store.decide(card_id, choice, why, key, 'fleet')
            self.fleet.task_pages = self.email_handoff_round
            self.fleet.mail_files = self.share_files  # a shared client thread's attachments, read-only (shared_graph.py)
            # A handoff the teammate accepted is theirs now: the owner's card is done, saying to whom (Undo brings it back).
            self.fleet.close_card = lambda card_id, why, key: self.store.decide_handoff(card_id, 'complete', why, key, key.removeprefix('fleet-handoff-'))
            # Handed off and not answered yet: the card waits under Later and comes back to check in if their Machine stays
            # quiet: within hours when due today, before a near deadline, the next work morning when urgent, else in 3 work
            # days (handoff_checkin); an answer, a decline or a done brings it back at once;
            # a decline brings it back to Ready, also when the owner closed it after handing it off.
            self.fleet.wait_card = lambda card_id, why, key, expected: self.store.wait_handoff(card_id, why, key, expected)
            self.fleet.wake_card = lambda card_id, key, handed_at: self.store.handoff_back(card_id, key, key.removeprefix('fleet-handoff-back-'), handed_at)
            self.fleet.retell_notice = lambda message_id, message: threading.Thread(
                target=self.fleet_retell, args=(message_id, message), daemon=True).start()
            # Briefs and free questions keep to the owner's hours; a free question is searched with the Machine's own search.
            self.fleet.hours = {'local_now': lambda: dt.datetime.now(local_tz()), 'work_day': is_work_day, 'in_hours': in_hours,
                                'morning': lambda: WORK_HOURS['morning']}
            self.fleet.search = lambda accounts, query, limit: self.related(accounts, query=query, limit=limit)[0]
            self.fleet.card_task = card_task  # a handoff leads with what the teammate is asked to do, never a chat reply
            # A card made for a request that goes again: a silent acceptance not told, or a handoff its sender took back
            self.fleet.drop_card = lambda card_id, why=None, key=None: self.store.decide(
                card_id, 'reject', why or i18n.t('Teammate not reached'), key or 'fleet-silent-undo-' + secrets.token_hex(6), 'fleet')
            self.fleet.own_event = lambda event: own_or_joined(event, self.store.owner_user_ids)  # silent acceptance: only what the owner did
            self.fleet.notify_brief = self.fleet_notify_brief
            self.fleet.remove_work = self.fleet_remove_work
            # Shared connectors (shared_connectors.py): kept in config.json, checked with the connector's own profile read
            self.fleet.save_config = self.fleet_save_config
            self.fleet.connector_profile = self.shared_connector_profile
            self.fleet.share_token = self.shared_connector_token  # Stripe signed in: a fresh access token to send
            self.fleet.connect_delivered = self.fleet_connect_delivered  # Sign in with Intercom for this Machine (fleet.py)
            self.fleet.watch_connects = True  # and picked up a moment after consent, apart from the Fleet's loop (connects_watch)
            self.fleet.support_read = self.support_read  # Support access: the team's read, while the owner allows it (fleet.py)
            self.meet_attach(lambda: dict(WORK_HOURS), local_tz)  # scheduling with Machines outside the Fleets (meet_app.py)

    def fleet_live(self):
        """Paired just now from the dashboard (pairing.py): the Fleet starts without a restart, with everything that
        hangs on it at start (skills, agent results, bug reports)."""
        if getattr(self, 'fleet', None) is not None:
            return self.fleet
        self.fleet_attach()
        if not self.fleet:
            return None
        self.fleet.set_meta('me_sent', None)  # a new pairing hears its addresses again (fleet.directory)
        if getattr(self, 'skills', None):
            self.skills.fleet = self.fleet
            self.fleet.skills = self.skills
        self.fleet.graph_build = self.graph_build
        self.fleet.about_you = self.about_you
        if getattr(self, 'agents', None) is not None:
            self.agents._network = lambda body: self.fleet.relay.call('POST', '/agent-results', body)
        self.fleet_stop = stop = threading.Event()  # a new one: a loop from before Unpair never wakes up again
        threading.Thread(target=self.fleet.run, args=(stop,), name='fleet', daemon=True).start()
        threading.Thread(target=self.bug_queue_worker, name='bug-queue', daemon=True).start()
        self.ai_reach_start(stop)  # its own address for AIs (ai_reach.py)
        LOG.info('fleet started after pairing')
        return self.fleet

    def fleet_drop(self):
        """Unpaired from the dashboard: the Fleet's loop stops and nothing uses its token any more."""
        stop = self.__dict__.get('fleet_stop')
        if stop is not None:
            stop.set()
        self.fleet = None
        if getattr(self, 'skills', None):
            self.skills.fleet = None
        if getattr(self, 'agents', None) is not None:
            self.agents._network = None

    def fleet_can_ping(self):
        """Whether fleet_notify reaches the owner at all: a phone or computer with notifications, Telegram, or email,
        each on for results. With none, a Fleet question only waits on the dashboard (fleet.notify_round)."""
        with self.store.connect() as db:
            push = notify.allowed(db, 'result', 'push') and any(push_reach(self.store, self.config))
            mail = mail_ready(self.config) and notify.allowed(db, 'result', 'email')
        return push or mail or (telegram_on(self.config) and self.notify_on('result', 'telegram'))

    def fleet_notify(self, rows):
        """Questions waiting for the owner: a phone notification, an email if still unanswered and unseen later, and a
        Telegram message with quick buttons when Telegram is on. A teammate's handoff gets an email only when neither a
        phone nor Telegram reaches the owner, one of its own (hold_handoff). Returns the Telegram message id, which binds those
        buttons to these questions."""
        fleet_push(self.store, self.config, rows)
        pings = None
        for row in rows:
            try:
                if row['kind'] != 'handoff':
                    hold_mail(self.store, self.config, 'result', fleet.asks_line(row), 'fleet:' + row['id'], True)
                    continue
                pings = self.fleet_pings() if pings is None else pings
                if not pings:  # a teammate's handoff and nothing else reaches the owner: its own email
                    hold_handoff(self.store, self.config, row)
            except Exception as error:  # noqa: BLE001 - the notification goes on without its email
                LOG.warning('fleet mail hold error=%s', type(error).__name__)
        if not telegram_on(self.config) or not self.notify_on('result', 'telegram'):
            return None
        result = fleet_telegram(self.config, fleet.telegram_message(rows, fleet.dashboard_root(self.config)))
        message_id = str(result.get('messageId') or '')
        return message_id if re.fullmatch(r'\d+', message_id) else None

    def fleet_pings(self):
        """A Fleet question reaches the owner on their phone or in Telegram: an app to push to with push on for
        results, or Telegram on for them."""
        with self.store.connect() as db:
            push = notify.allowed(db, 'result', 'push') and any(push_reach(self.store, self.config))
        return push or (telegram_on(self.config) and self.notify_on('result', 'telegram'))

    def fleet_notify_notice(self, view, message):
        """A Fleet notice: a phone notification, and a Telegram message when Telegram is on (Confirm and Decline on a
        seat request, Open on the rest). Returns the Telegram message id, which binds those buttons to this notice."""
        fleet_notice_push(self.store, self.config, view)
        if not telegram_on(self.config) or not self.notify_on('result', 'telegram'):
            return None
        result = fleet_telegram(self.config, message)
        message_id = str(result.get('messageId') or '')
        return message_id if re.fullmatch(r'\d+', message_id) else None

    def fleet_notify_brief(self, text, url, titles=None):
        """The team brief is ready: a phone notification, and the brief itself in Telegram when Telegram is on (with
        Open only). Returns the Telegram message id. titles (its items, as the brief shows them) make the
        notification's body (notify.brief_line); with Text in notifications off, only how many."""
        subscriptions, phones = push_reach(self.store, self.config)
        if subscriptions or phones:
            # the tag names the Fleet: a tapped phone notification opens that brief (the dashboard's pushRoute)
            which = re.search(r'#fleet-brief=(fl_[0-9a-f]{16})$', url or '')
            tag = 'fleet-brief-' + which[1] if which else 'fleet-brief'
            with self.store.connect() as db:
                show = security_levels.notify_text(db, True)
            line = notify.brief_line(titles, show) if titles is not None else notify.clip(text.split('\n', 2)[-1], notify.APP_BODY) if show else ''
            push_send(self.store, self.config, subscriptions, {'title': i18n.t('What your Fleet saw'), 'body': line,
                                                               'url': url, 'tag': tag, '_body': line, 'actions': quick_web('view')},
                      'fleet-brief', kind='result', wake='fleet')
        if not telegram_on(self.config) or not self.notify_on('result', 'telegram'):
            return None
        result = fleet_telegram(self.config, {'text': text, 'buttons': [[{'text': i18n.t('Open the brief'), 'url': url}]] if url else []})
        message_id = str(result.get('messageId') or '')
        return message_id if re.fullmatch(r'\d+', message_id) else None

    def fleet_tell(self, text, anchor):
        """How the owner's own Fleet request went (an intro, a handoff, a follow-up split): a phone notification, and a
        plain Telegram line with Open when Telegram is on. No buttons to act on: it only tells."""
        root = fleet.dashboard_root(self.config)
        subscriptions, phones = push_reach(self.store, self.config)
        if subscriptions or phones:
            with self.store.connect() as db:
                show = security_levels.notify_text(db, True)
            body = text[:200] if show else ''
            push_send(self.store, self.config, subscriptions, {'title': i18n.t('Fleet update'), 'body': body, 'url': root, 'tag': 'fleet-' + anchor,
                                                               '_body': notify.clip(plain(body), notify.APP_BODY), 'actions': quick_web('view')},
                      'fleet=' + anchor, kind='result', wake='fleet')
        if telegram_on(self.config) and self.notify_on('result', 'telegram'):
            fleet_telegram(self.config, {'text': text, 'buttons': [[{'text': i18n.t('Open in To-dos'), 'url': root}]] if root else []})

    def fleet_retell(self, message_id, message=None):
        try:
            message = message or self.fleet.telegram_view(message_id)
            if message and telegram_on(self.config):
                fleet_telegram(self.config, message, message_id)
        except Exception as error:
            LOG.warning('fleet telegram edit error=%s', type(error).__name__)

    def fleet_action(self, name, args, owner_dashboard):
        """The owner's Fleet controls. From the owner's own dashboard; the one exception is a tap on the Telegram
        message sent for that very question (the plugin's owner key). Never an agent or a teammate."""
        if not owner_dashboard and not (name in ('fleet_decide', 'fleet_notice_decide') and args.get('source') == 'telegram'):
            raise ValueError('The Fleet is set from the dashboard')
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine is not in a Fleet')
        if not owner_dashboard and name == 'fleet_notice_decide':
            return self.fleet.decide_notice_from_telegram(str(args.get('id') or ''), args.get('choice'), args.get('message_id'))
        if not owner_dashboard:
            return self.fleet.decide_from_telegram(str(args.get('id') or ''), args.get('choice'), args.get('message_id'))
        if name == 'fleet_notice_decide':  # Confirm or Decline on the Fleet tab, on the terms that card showed
            return self.fleet.decide_notice(str(args.get('id') or ''), args.get('choice'), str(args.get('key') or ''), via='dashboard')
        if name == 'fleet_ask':
            kind = args.get('kind')
            question = fleet.parse_question(kind, args.get('question'))
            if not question:
                raise ValueError('Ask about a company, a domain, an email address or a name')
            return self.fleet.ask(kind, question, fleet=args.get('fleet') or 'work')
        if name == 'fleet_decide':  # text: a free question's answer as the owner edited it
            return self.fleet.decide(args.get('id'), args.get('choice'), text=args.get('text') if isinstance(args.get('text'), str) else None,
                                     note=args.get('note') if isinstance(args.get('note'), str) else None)
        if name == 'fleet_free':
            return self.fleet.ask_free(str(args.get('text') or ''), args.get('fleet') or 'work')
        if name == 'fleet_brief':
            return self.fleet.set_brief(args.get('every'), args.get('tell'))
        if name == 'fleet_share':  # share a connected Intercom with a Work Fleet: the members ticked, and every confirmed admin
            members = args.get('members') if isinstance(args.get('members'), list) else []
            return self.fleet.share(str(args.get('account') or ''), str(args.get('fleet') or ''), [str(m) for m in members][:200])
        if name == 'fleet_share_ok':
            return self.fleet.share_ok(str(args.get('id') or ''), args.get('choice'))
        if name == 'fleet_share_replace':
            return self.fleet.share_replace(str(args.get('fleet') or ''), str(args.get('service') or ''), args.get('token'))
        if name == 'fleet_share_stop':
            return self.fleet.share_stop(str(args.get('fleet') or ''), str(args.get('service') or ''))
        if name == 'fleet_brief_hide':  # Not needed on one line of the team brief
            return self.fleet.hide_brief_item(str(args.get('fleet') or ''), args.get('key'))
        if name == 'fleet_intro':  # ask one teammate who knows someone there for an intro
            return self.fleet.ask_intro(str(args.get('fleet') or ''), str(args.get('member_id') or ''), str(args.get('about') or ''),
                                        str(args.get('note') or ''))
        if name == 'fleet_handoff_draft':  # what a handoff of this card would send, to read and edit first
            return self.fleet.handoff_draft(str(args.get('suggestion_id') or ''))
        if name == 'fleet_handoff_email':  # someone not on the Network: an email draft on the card, sent by the owner
            return self.handoff_email(str(args.get('suggestion_id') or ''), str(args.get('email') or ''), str(args.get('title') or ''),
                                      str(args.get('summary') or ''), keep=args['keep'] if isinstance(args.get('keep'), list) else None,
                                      take=args.get('take') if isinstance(args.get('take'), bool) else None, name=str(args.get('name') or ''))
        if name in handoff_mail.ACTIONS:  # By email in the Hand off sheet: what can go, and the take line's setting
            return self.handoff_mail.action(name, args)
        if name == 'fleet_handoff':
            return self.fleet.hand_off(str(args.get('suggestion_id') or ''), str(args.get('fleet') or ''), str(args.get('member_id') or ''),
                                       str(args.get('title') or ''), str(args.get('summary') or ''), str(args.get('contact') or '') or None,
                                       sources=args['sources'] if isinstance(args.get('sources'), list) else args.get('sources') is not False,  # all, none or those kept
                                       replace=args.get('replace') is True)  # instead of whoever still has it
        if name == 'fleet_handoff_not_mine':  # Not mine, on a card that became the owner's by what they did: undone, the teammate told
            card = str(args.get('suggestion_id') or '')
            done = self.fleet.handoff_not_mine(card)
            if not done['joined']:  # a card made for it goes; one the owner already had stays, with its drafts and history
                self.store.decide(card, 'reject', i18n.t('Not mine'), 'fleet-not-mine-' + secrets.token_hex(6), 'dashboard')
            return done
        if name == 'fleet_handoff_mine':  # Do it myself, on a card a teammate handed back
            return self.fleet.handoff_mine(str(args.get('suggestion_id') or ''))
        if name == 'fleet_handoff_take_back':  # Take it back, while a teammate still has it: the owner's again, back from Later
            card = str(args.get('suggestion_id') or '')
            done = self.fleet.take_back(card)
            with self.store.connect() as db:
                row = db.execute('SELECT status FROM suggestions WHERE id=?', (card,)).fetchone()
            if row and row['status'] == 'snoozed':
                self.store.decide(card, 'accept', '', 'fleet-take-back-' + secrets.token_hex(6), 'dashboard')
            return done
        if name == 'fleet_review_options':  # Ask to review: who can review this to-do, and what goes
            return self.fleet.review_options(str(args.get('suggestion_id') or ''))
        if name == 'fleet_review_ask':  # one person in the matching Fleet: Work to Work, Personal to the Family
            return self.fleet.ask_review(str(args.get('suggestion_id') or ''), str(args.get('fleet') or ''), str(args.get('member_id') or ''),
                                         str(args.get('note') or ''), args['sources'] if isinstance(args.get('sources'), list) else args.get('sources') is not False)
        if name == 'fleet_review_withdraw':
            return self.fleet.withdraw_review(str(args.get('suggestion_id') or ''))
        if name == 'fleet_review_view':  # the tracked changes: who, when, the comment and each change
            return self.fleet.review_view(str(args.get('suggestion_id') or ''))
        if name == 'fleet_review_apply':  # 'all', a list of change ids, or 'ignore'; the owner's Send stays theirs
            picks = args.get('picks')
            return self.fleet.apply_review(str(args.get('suggestion_id') or ''), picks if picks in ('all', 'ignore') or isinstance(picks, list) else None)
        if name == 'fleet_review_reply':  # the reviewer: approved, changes, commented or declined; never a send
            return self.fleet.reply_review(str(args.get('suggestion_id') or ''), str(args.get('stage') or ''), str(args.get('comment') or ''),
                                           args.get('subject') if isinstance(args.get('subject'), str) else None,
                                           args.get('body') if isinstance(args.get('body'), str) else None)
        if name == 'fleet_split':  # send a follow-up split as the owner filled it in
            return self.fleet.send_split(str(args.get('id') or ''), args.get('items'))
        if name == 'fleet_split_dismiss':
            return self.fleet.set_split_aside(str(args.get('id') or ''))
        if name == 'fleet_split_adjust':  # accept a teammate's split with the owner's own part as they changed it
            return self.fleet.decide_request(str(args.get('id') or ''), 'adjust', text=str(args.get('text') or ''))
        if name == 'fleet_rule':
            return self.fleet.set_rule(args.get('fleet') or 'work', str(args.get('member_id') or ''), args.get('kind'),
                                       args.get('rule'), args.get('details'), args.get('scope'), bool(args.get('clear')))
        if name == 'fleet_learning_remove':  # a team learning, gone for the whole Fleet (fleet_learnings.py)
            return self.fleet.remove_learning(args.get('fleet') or 'work', str(args.get('fp') or ''))
        if name == 'fleet_take':
            return self.fleet.take_over(str(args.get('suggestion_id') or ''))
        if name in CONTACT_ACTIONS:  # node: a person's node id, or 'me' for the owner's own card
            source, pick, note = str(args.get('node') or ''), args.get('pick'), str(args.get('note') or '')
            if name == 'fleet_contact_options':
                return {**self.fleet.contact_options(source), 'sent': self.fleet.contact_sent(source)}
            if name == 'fleet_contact_preview':
                return self.fleet.contact_preview(source, pick, note, str(args.get('fleet') or ''), str(args.get('member_id') or ''))
            if name == 'fleet_contact_send':  # shown: the preview's digest; confirmed: the extra OK for a Personal or private contact
                return self.fleet.contact_send(source, pick, note, str(args.get('fleet') or ''), str(args.get('member_id') or ''),
                                               str(args.get('shown') or ''), args.get('confirmed') is True)
            return self.fleet.contact_decide(str(args.get('id') or ''), str(args.get('choice') or ''))
        if name == 'fleet_friend':  # add by username; withdraw, accept, decline or block a request; remove, block or unblock a friend
            return self.fleet.friend_action(str(args.get('do') or ''), str(args.get('username') or ''), str(args.get('id') or ''),
                                            str(args.get('member_id') or ''))
        if name == 'fleet_network':  # find people I know, be findable, connect, not now, never, leave the Network
            return self.fleet.network_action(str(args.get('do') or ''), str(args.get('email') or ''), str(args.get('relation') or ''))
        if name == 'fleet_availability':  # ask one friend's Machine when they are busy (busy blocks only)
            return self.fleet.ask_availability(str(args.get('member_id') or ''), str(args.get('start') or ''), args.get('days'))
        if name == 'family_free':  # ask everyone in the Family when they are busy; the common free times show here
            return self.fleet.ask_family_free(str(args.get('start') or ''), args.get('days'))
        if name == 'family_todo':  # a to-do for one member, who accepts or declines it on their Machine
            return self.fleet.propose_todo(str(args.get('member_id') or ''), str(args.get('title') or ''), str(args.get('due') or '') or None,
                                           str(args.get('note') or ''))
        if name == 'family_invite':  # Invite (the account page's form, prefilled; nothing is sent here) or Not now (family_invites.py)
            return self.fleet.family_invite(str(args.get('suggestion_id') or ''), str(args.get('do') or ''))
        if name == 'family_invite_setting':  # Settings, Fleet: Suggest inviting family
            return self.fleet.family_invite_set(args.get('on') is True)
        if name == 'family_event':  # a plan for the Family (or some of it): each says yes or no; nothing is written to a calendar
            return self.fleet.propose_event(str(args.get('title') or ''), str(args.get('start') or ''), str(args.get('end') or '') or None,
                                            str(args.get('place') or ''), str(args.get('note') or ''),
                                            [str(m) for m in args.get('to') or [] if isinstance(m, str)] or None)
        if name == 'fleet_meetings':
            self.fleet.set_meta('ask_meetings', bool(args.get('on')))
            return {'ask_meetings': self.fleet.meetings_on()}
        raise ValueError('Unknown Fleet action')

    def fleet_save_config(self, change, restart):
        """A shared connector changed (shared_connectors.py): the same change to config.json, then a restart when asked."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This service cannot save its settings')
        import onboarding
        saved = onboarding.load(self.config_path)
        change(saved)
        onboarding.save(self.config_path, saved)
        if restart:
            restart_self(5)

    def shared_connector_profile(self, service, account, token):
        """Reads a token's own profile once (Intercom: GET /me), as connecting does; ValueError when it doesn't work."""
        plugin = load_connector(service)
        if not plugin or not hasattr(plugin, 'Source'):
            raise ValueError('That connector cannot be checked here')
        helpers = types.SimpleNamespace(**{**vars(CONNECTOR_HELPERS), 'credential': lambda config, name: token})
        try:
            plugin.Source(self.config, account, helpers).connect()
        except SourceError as error:
            raise ValueError('account_identity_mismatch' in str(error) and 'That token is for another workspace'
                             or 'That token does not work: ' + str(error)) from None
        return account

    def shared_connector_token(self, service, account, min_left=0):
        """The token a Fleet admin's Machine sends for its shared account: (token, seconds it works, None: lasts). A
        signed-in Stripe account's is an access token for an hour, never the sign-in (connectors/stripe.py share_token)."""
        plugin = load_connector(service)
        if not plugin or not callable(getattr(plugin, 'share_token', None)):
            return None, None
        try:
            return plugin.share_token(self.config, account, CONNECTOR_HELPERS, min_left=min_left)
        except SourceError as error:
            LOG.info('shared connector token unavailable service=%s error=%s', service, error)
            return None, None

    def fleet_remove_work(self, item):
        """The control plane, through the Network: remove a Work Fleet's company data (work_removal.py), then restart."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This service cannot save its settings')
        result = work_removal.remove(self.config_path, item.get('domains') or [], item.get('companies') or [], store=self.store)
        LOG.info('work removal accounts=%s events=%s cards=%s', len(result['accounts']), result['events'], result['cards'])
        if result['accounts']:
            result['restarting'] = restart_self(5)
        return result

    def forget_device_grant(self, account):
        """A Google, Microsoft, Zoom, Stripe or Slack account signed in from this paired Machine's dashboard (onboarding.connect_grant),
        disconnected: once no account on that sign-in is left, its refresh token is forgotten here (Google's revoked) and
        the control plane forgets this Machine had it, so nothing refreshes it again."""
        import mail_grants
        provider = {'microsoft_docs': 'microsoft'}.get(fleet.SIGNIN_OF.get(account.get('service')), fleet.SIGNIN_OF.get(account.get('service')))
        if account.get('transport') != 'broker' or provider not in ('google', 'microsoft', 'zoom', 'stripe', 'slack', 'google_meet'):
            return
        import slack_api

        def signin_of(a):  # what the sign-in is kept under: Stripe's account id, Slack's team and user, else the address
            return slack_api.key(a) if provider == 'slack' else str(a.get('stripe_account' if provider == 'stripe' else 'email') or '').lower()
        email = signin_of(account)
        # Docs for a Microsoft address reads with the same sign-in as its Outlook mail and calendar
        services = {s for s, p in fleet.SIGNIN_OF.items() if p == provider} | ({'docs'} if provider == 'microsoft' else set())
        if any(a.get('id') != account['id'] and a.get('service') in services and signin_of(a) == email for a in self.config.get('accounts', [])):
            return
        if provider == 'slack':
            slack_api.forget_token(account)
        try:
            mail_grants.forget(self.config, provider, email)
        except (mail_grants.GrantError, OSError) as error:
            LOG.warning('sign-in not forgotten provider=%s error=%s', provider, type(error).__name__)
        if getattr(self, 'fleet', None) is not None:
            try:
                self.fleet.relay.call('POST', '/grant-forget', {'provider': provider, 'email': email}, timeout=30)
            except Exception as error:  # noqa: BLE001 - its token is gone here: the control plane can refresh nothing
                LOG.warning('grant forget not sent provider=%s error=%s', provider, type(error).__name__)

    def fleet_connect_delivered(self, body):
        """A sign-in sealed for this paired Machine (fleet.py connects_round): connected the way the dashboard's
        Connections, Add does (onboarding.connect_delivered), then a restart reads it. Only the `connect` command."""
        import onboarding
        if not isinstance(body, dict) or body.get('command') != 'connect' or not isinstance(body.get('args'), dict):
            return {'ok': False, 'error': 'Not something this Machine connects this way.'}
        if not getattr(self, 'config_path', None):
            return {'ok': False, 'error': 'This Machine cannot save its settings.'}
        lock = self.__dict__.setdefault('connect_lock', threading.Lock())
        with lock:
            if any(v['state'] == 'running' for v in self.__dict__.setdefault('connect_sessions', {}).values()):
                return {'ok': False, 'error': 'Another source is being added on this Machine. Sign in again once that is done.'}
            try:
                result = onboarding.connect_delivered(self.config_path, body['args'])
            except onboarding.SetupError as error:  # its words name the step, never what it carried
                return {'ok': False, 'error': error.message}
        LOG.info('connect delivered source=%s replies=%s', body['args'].get('source'), result.get('replies'))
        result['restarting'] = restart_self(3)
        return result

    def fleet_circles(self):
        """Which of the people in the owner's Fleets are in a Work Fleet, Family or Friends, by address (graph.circles):
        someone only in Family or Friends is a Personal contact."""
        if not getattr(self, 'fleet', None):
            return {}
        try:
            return graph.circles(self.fleet.fleets())
        except (fleet.Off, ValueError, OSError, sqlite3.Error, KeyError, TypeError, AttributeError):
            return {}

    def fleet_addresses(self):
        """The addresses of the people in the owner's Fleets (Work, Family, Friends): one they use too is never the
        owner's own (own_addresses.py)."""
        if not getattr(self, 'fleet', None):
            return set()
        try:
            return {str(e).strip().lower() for f in self.fleet.fleets().values() for m in f.get('members') or ()
                    if isinstance(m, dict) and not m.get('me') for e in m.get('emails') or ()}
        except (fleet.Off, ValueError, OSError, sqlite3.Error, KeyError, TypeError):
            return set()

    def team_accounts(self):
        """The accounts whose messages a Work Fleet's Shared Graph may carry (the connections each owner shares, graph_accounts)."""
        if not getattr(self, 'fleet', None):
            return []
        try:
            return sorted({a for ref in self.fleet.work_fleets() for a in self.fleet.graph_accounts(ref)})
        except (ValueError, KeyError, TypeError, sqlite3.Error):
            return []

    def share_groups(self):
        """The groups unsure threads already have (shared_graph.groups), for the history pass to reuse."""
        try:
            with self.store.connect() as db:
                shared_graph.ensure(db)
                return shared_graph.groups(db)
        except sqlite3.Error:
            return []

    def fleet_view(self):
        """The Fleet tab, with each member who is in the graph linked to their person there."""
        view = self.fleet.view()
        try:
            view['shared'] = self.fleet.shared_view()  # shared connectors: what this Machine shares or holds, and OKs to give
        except (ValueError, OSError, KeyError, TypeError, fleet.Off) as error:
            LOG.info('shared connectors view error=%s', type(error).__name__)
        try:
            with self.store.connect() as db:
                found = {(x['fleet'], x['member_id']): node for node, m in self.graph_fleet_marks(db).items() for x in m['in']}
        except sqlite3.Error:
            found = {}
        for f in view.get('fleets') or ():
            for p in f.get('people') or ():
                if found.get((f.get('id'), p.get('member_id'))):
                    p['graph_node'] = found[(f['id'], p['member_id'])]
        return view

    def team_votes_due(self):
        """Once a day, with voting on: fetch other Machines' learnings, send votes judged earlier, and start one small
        judging turn when some wait (team_learnings.py). The turn waits for the usage budget like every background turn."""
        try:
            call = self.fleet.relay.call
            with self.store.connect() as db:
                due = team_learnings.votes_due(db)
            if due:
                with self.store.connect() as db:
                    team_learnings.set_pref(db, 'votes_fetched_at', now())  # tried today, also when the call fails
                answer = call('POST', '/learnings', {'action': 'candidates'})
                with self.store.connect() as db:
                    team_learnings.take_candidates(db, answer)
            team_learnings.send_votes(self.store.connect, call)
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                if not team_learnings.vote_on(db) or db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone():
                    return None
                evidence = team_learnings.vote_evidence(db)
                if not evidence:
                    return None
                run_id, started = uuid.uuid4().hex, now()
                db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'team_votes',1)",
                           (run_id, started, started, json.dumps(evidence)))
            return run_id
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('learning votes error=%s', type(error).__name__)
            return None

    def fleet_learn_due(self, current=None):
        """At most once a day, in a Standard Work Fleet that shares its Team Graph: one small background turn reads a few
        threads the Team Graph already shares with the team and writes general team learnings (fleet_learnings.py).
        Nothing is asked per learning; the owner's learnings switch turns it off. It waits for the usage budget like
        every background turn. When too little is new, it looks again an hour later."""
        current = current or dt.datetime.now(dt.timezone.utc)
        if time.monotonic() - getattr(self, '_fleet_learn_tried', -3600) < 3600:
            return None
        self._fleet_learn_tried = time.monotonic()
        try:
            with self.store.connect() as db:
                fleet_learnings.ensure(db)
                if not fleet_learnings.due(db, current):
                    return None
                names = team_learnings.known_names(db, self.config)
                for ref in self.fleet.work_fleets():
                    inputs = self.fleet.learn_inputs(db, ref)
                    evidence = inputs and fleet_learnings.evidence(db, ref, inputs['gate'], inputs['accounts'], inputs['team_side'],
                                                                   inputs['company'], names, current)
                    if not evidence:
                        continue
                    db.execute('BEGIN IMMEDIATE')
                    if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone():
                        return None
                    run_id, started = uuid.uuid4().hex, now()
                    db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'fleet_learn',1)",
                               (run_id, started, started, json.dumps(evidence)))
                    return run_id
        except Exception as error:  # noqa: BLE001 - a Fleet directory or Graph not ready yet: next time
            LOG.warning('team learnings error=%s', type(error).__name__)
        return None

    def team_votes_send(self, run_id):
        with self.store.connect() as db:
            judged = team_learnings.finish_votes(db, run_id)
        if judged and getattr(self, 'fleet', None):
            try:
                team_learnings.send_votes(self.store.connect, self.fleet.relay.call)
            except Exception as error:
                LOG.warning('learning votes error=%s', type(error).__name__)

    def learnings_share(self, args):
        if not getattr(self, 'fleet', None):
            raise ValueError('Sharing needs The Machine Network. Nothing was sent.')
        if args.get('auto') is True:  # "Send automatically from now on", ticked in the offer: checked before anything goes
            with self.store.connect() as db:
                if team_learnings.careful_floor(db):
                    raise ValueError('A Careful Work Fleet keeps asking each time.')
        result = team_learnings.share(self.store.connect, self.config, str(args.get('id') or ''), args.get('items'), args.get('named') is True,
                                      self.fleet.relay.call, code_version())
        if args.get('auto') is True:
            with self.store.connect() as db:
                team_learnings.set_auto(db, True)
        return result

    def learnings_auto_send(self):
        """Send learnings automatically (team_learnings.auto_send), when the owner chose it; quiet when the Network is away."""
        if not getattr(self, 'fleet', None):
            return None
        try:
            result = team_learnings.auto_send(self.store.connect, self.config, self.fleet.relay.call, code_version())
        except Exception as error:  # noqa: BLE001 - the next step tries again
            LOG.warning('learnings auto send error=%s', type(error).__name__)
            return None
        if result:
            LOG.info('learnings sent automatically count=%s', result.get('count'))
        return result

    def learnings_withdraw(self, args):
        if not getattr(self, 'fleet', None):
            raise ValueError('Withdrawing needs The Machine Network.')
        return team_learnings.withdraw(self.store.connect, self.config, str(args.get('id') or ''), args.get('n'), self.fleet.relay.call)

    def graph_fleet_marks(self, db):
        """Who in the graph is in the owner's Fleets, Family or Friends: from the Network directory this Machine keeps,
        never by asking their Machine (graph.fleet_marks). Nothing without a Fleet."""
        if not getattr(self, 'fleet', None):
            return {}
        try:
            return copy.deepcopy(shared_graph.fleet_marks(db, self.fleet.fleets()))  # kept between requests (stamps.py)
        except (sqlite3.Error, ValueError, TypeError, KeyError, AttributeError):
            return {}
