"""The Machine's service: App, made of its domain mixins (machine/app/*, <domain>_app.py), and Store, the database made
of its Store mixins (machine/store/*). assistant.py is the entry point and re-exports them."""
import hashlib
import json
from pathlib import Path
import re
import threading

import agent_jobs
from agents_app import AgentsApp
from ai_app import AiApp
from calendar_app import CalendarApp
import chat_model
import check_now
from corrections_app import CorrectionsApp
import fleet
import fleet_reviews
from gbrain_app import GBrainApp
import locale_prefs
from machine.actions import FAMILY_ACTIONS
from machine.app.action_runs import ActionRunsApp
from machine.app.browser import BrowserApp
from machine.app.calendar_clashes import CalendarClashesApp
from machine.app.meeting_prep import MeetingPrepApp
from machine.app.card_actions import CardActionsApp
from machine.app.card_chat import CardChatApp
from machine.app.check_now import CheckNowApp
from machine.app.connect import ConnectApp
from machine.app.conversation import ConversationApp
from machine.app.docs import DocsApp
from machine.app.export import ExportApp
from machine.app.feedback import FeedbackApp
from machine.app.first_look import FirstLookApp
from machine.app.fleet import FleetApp
from machine.app.follow_ups import FollowUpsApp
from machine.app.graph_actions import GraphActionsApp
from machine.app.history import HistoryApp
from machine.app.knowledge_export import KnowledgeExportApp
from machine.app.mail import MailApp
from machine.app.meeting_writes import MeetingWritesApp
from machine.app.model_pacing import ModelPacingApp
from machine.app.new_cards import NewCardsApp
from machine.app.notifications import NotificationsApp
from machine.app.page_watch import PageWatchApp
from machine.app.preparation import PreparationApp
from machine.app.profile import ProfileApp
from machine.app.handled_check import HandledCheckApp
from machine.app.promise_checks import PromiseChecksApp
from machine.app.recap import RecapApp
from machine.app.recap_settings import RecapSettingsApp
from machine.app.review import ReviewApp
from machine.app.review_saves import ReviewSavesApp
from machine.app.search_ask import SearchAskApp
from machine.app.serve import ServeApp
from machine.app.settings_actions import SettingsActionsApp
from machine.app.setup_card import SetupCardApp
from machine.app.signatures import SignaturesApp
from machine.app.status import StatusApp
from machine.app.summaries import SummariesApp
from machine.app.sync import SyncApp
from machine.app.talk import TalkApp
from machine.app.voice import VoiceApp
from machine.app.workers import WorkersApp
from machine.config import LOG, WORKSPACE
from machine.sources.calendar import Calendar, calendar_event
from machine.sources.connectors import intercom_link, intercom_own_event
from machine.sources.exclusions import calendar_title_excluded, default_exclusions
from machine.sources.gmail import Gmail, message_event
from machine.sources.slack import slack_event
from machine.sources.whatsapp import WhatsApp, whatsapp_event
from machine.store.cards import CardsStore
from machine.store.core import StoreCore
from machine.store.decisions import DecisionsStore
from machine.store.done_milestones import DoneMilestonesStore
from machine.store.events import EventsStore
from machine.store.facts import FactsStore
from machine.store.faults import FaultsStore
from machine.store.first_look import FirstLookStore
from machine.store.machine_cards import MachineCardsStore
from machine.store.profile import ProfileStore
from machine.store.promises import PromisesStore
from machine.store.review import ReviewStore
from machine.store.views import ViewsStore
from machine.store.voices import VoicesStore
from machine.store.whats_new import WhatsNewStore
from meet_app import MeetApp
from mail_cleanup_app import CleanupTemplate
from reading_digest_app import DigestTemplate
from subscriptions_app import SubscriptionsTemplate
from birthdays_app import Birthdays
from birthdays_facebook_app import BirthdaysFacebook
from bring_in_app import BringInApp
from missed_work_app import MissedWorkApp
import next_actions
import notify
from recurring_app import RecurringApp
import routine_templates
from routines_app import RoutinesApp
from shared_graph_app import SharedGraphApp
import skills
from skills_app import SkillsApp
from sources import credential, owner_credential
from support_app import SupportApp
from timeutil import now, set_timezone, set_work_hours
from whatsapp_images_app import WhatsAppImagesApp


class Store(CardsStore, DecisionsStore, DoneMilestonesStore, EventsStore, FactsStore, FaultsStore, FirstLookStore,
            ProfileStore, PromisesStore, MachineCardsStore, ReviewStore, StoreCore, ViewsStore, VoicesStore, WhatsNewStore):
    """The service's database: every table, through the Store mixins it is made of (machine/store/*)."""


# App's domain mixins (<domain>_app.py): each holds a domain's App methods and the actions it handles (its ACTIONS).
APP_MIXINS = (SupportApp, CalendarApp, SkillsApp, AgentsApp, GBrainApp, SharedGraphApp, RecurringApp, CorrectionsApp, AiApp, MeetApp, MissedWorkApp, BringInApp,
              WhatsAppImagesApp, CheckNowApp, SetupCardApp, HistoryApp, RoutinesApp)
# App's mixins in machine/app/: methods moved out of App as is (docs/code-map.md)
APP_MIXINS += (FollowUpsApp, GraphActionsApp, KnowledgeExportApp, MeetingWritesApp, ModelPacingApp, PromiseChecksApp, SignaturesApp, SummariesApp,
               VoiceApp)
APP_MIXINS += (CardChatApp, ConversationApp, ExportApp, FirstLookApp, FleetApp, PreparationApp, RecapApp, ReviewApp, TalkApp)
APP_MIXINS += (ServeApp,)
APP_MIXINS += (NewCardsApp,)
APP_MIXINS += (MailApp,)
APP_MIXINS += (SyncApp,)
APP_MIXINS += (ActionRunsApp,)
APP_MIXINS += (WorkersApp,)
APP_MIXINS += (StatusApp,)
APP_MIXINS += (DocsApp,)
APP_MIXINS += (CardActionsApp,)
APP_MIXINS += (FeedbackApp,)
APP_MIXINS += (HandledCheckApp,)
APP_MIXINS += (ProfileApp,)
APP_MIXINS += (BrowserApp,)
APP_MIXINS += (NotificationsApp, SettingsActionsApp)
APP_MIXINS += (RecapSettingsApp,)
APP_MIXINS += (SearchAskApp,)
APP_MIXINS += (ReviewSavesApp,)
APP_MIXINS += (CalendarClashesApp,)
APP_MIXINS += (MeetingPrepApp,)
APP_MIXINS += (ConnectApp,)
APP_MIXINS += (PageWatchApp,)


class BirthdaysTemplate(BirthdaysFacebook, Birthdays):
    """Birthdays (birthdays_app.py) with its one Import birthdays from Facebook to-do (birthdays_facebook_app.py): two
    modules, one template. Composed here, where *_app modules may be imported."""
    ACTIONS = {**Birthdays.ACTIONS, **BirthdaysFacebook.ACTIONS}


# Routine templates: each one's code is a routine_templates.Template, not an App mixin. The routines worker, the
# service's start and App.action load them from this list (App.template)
ROUTINE_TEMPLATES = (CleanupTemplate, DigestTemplate, BirthdaysTemplate, SubscriptionsTemplate)


class App(*APP_MIXINS):
    # action name -> method, from the mixins' ACTIONS; App.action calls it as method(name, args, owner_dashboard). Who
    # may call an action is still the reviewed sets above (OWNER_ACTIONS, DASHBOARD_ACTIONS, SUPPORT_ACTIONS, ...).
    ACTION_HANDLERS = {name: method for mixin in APP_MIXINS for name, method in mixin.ACTIONS.items()}
    TEMPLATE_ACTIONS = routine_templates.actions(ROUTINE_TEMPLATES)  # action name -> the Template that handles it
    HISTORY_SOURCES = {'mail': (Gmail, message_event), 'calendar': (Calendar, calendar_event, calendar_title_excluded), 'whatsapp': (WhatsApp, whatsapp_event),
                       'slack': (None, slack_event)}  # Slack's client is the collector's own (SyncApp.slack_source)

    def __init__(self, config, config_path=None):
        set_timezone(config.get('timezone'))
        locale_prefs.configure(config)
        try:
            set_work_hours(config.get('work_hours'))
        except ValueError as error:
            LOG.warning('work_hours ignored, using the defaults: %s', error)
            set_work_hours(None)
        self.config = config
        self.config_path = Path(config_path) if config_path else None  # where Work hours are saved
        self.digest_follows_snoozes()  # a digest set before the morning's snoozes: saved at 5 minutes after them
        try:  # what the app starts with: changes after it are followed (follow_config)
            self.config_stamp = self.config_path.stat().st_mtime_ns if self.config_path else None
        except OSError:
            self.config_stamp = None
        self.store = Store(config['database'], protect=self.protection_now(config))
        with self.store.connect() as db:  # the first view reads these: made at start, never by a view waiting behind an import
            notify.ensure(db)
        self.store.exclusions = {a['id']: rules for a in config['accounts'] if (rules := (a.get('exclude') or []) + default_exclusions(config, a))}
        self.store.owner_user_ids = {a['user_id'] for a in config['accounts'] if a.get('service') == 'slack' and a.get('user_id')}
        self.store.accounts = config['accounts']
        self.store.config = config
        self.note_connections()
        self.token = credential(config, 'api-token')
        self.owner_token = owner_credential(config)
        self.stop = threading.Event()
        self.graph_dirty = threading.Event()
        # Check now (check_now.py): the one check, and each collector's early wake and its last finished read
        self.check, self.collector_wakes, self.collector_reads, self.collector_resting = check_now.Check(), {}, {}, set()
        self.model_usage = None
        self.chat_catalog = chat_model.Catalog()  # the models a chat can pick, from the Gateway (chat_model.py)
        # The Fleet (fleet.py): only when the control plane put this Machine in one.
        self.fleet_attach()
        # Skills (skills.py): the owner's how-tos, written to the OpenClaw workspace; shared ones come in through the Fleet.
        self.skills = skills.Skills(self.store.connect, config.get('openclaw_workspace') or WORKSPACE, self.fleet, config=config)
        self.skills.finder = self.skills_find_start
        # Hand to Claude Code / Hand to Codex on a card (agent_jobs.py): only where the tool is there to hand to.
        self.agents = agent_jobs.AgentJobs(self.store.connect, config, Path(config['database']).parent / 'agent-jobs',
                                           card=self.agent_card, revise=self.agent_revise, changed=self.store.card_message_changed,
                                           network=(lambda body: self.fleet.relay.call('POST', '/agent-results', body)) if self.fleet else None,
                                           ) if agent_jobs.settings(config) is not None else None
        if self.fleet:
            self.fleet.skills = self.skills
            self.fleet.graph_build = self.graph_later  # a shared contact the owner adds (contact_share.py): on its page at once
            self.fleet.about_you = self.about_you  # Share my contact: the owner's own addresses and numbers

    MESSAGE_CACHE = 40  # source emails kept in memory for the dashboard, newest used last
    MESSAGE_TTL = 600  # seconds

    MAILBOX_LOOKUP_MAX = 10  # messages per mailbox one search keeps

    NO_DOC_CONNECTION = 'No Docs connection in this to-do’s area can do things. Give what you need in the to-do instead.'

    def action(self, name, args, owner_dashboard=False):
        if name in self.ACTION_HANDLERS:  # an action a domain mixin handles (APP_MIXINS)
            return getattr(self, self.ACTION_HANDLERS[name])(name, args, owner_dashboard)
        if name in self.TEMPLATE_ACTIONS:  # an action on a routine template's to-do (ROUTINE_TEMPLATES)
            cls = self.TEMPLATE_ACTIONS[name]
            return getattr(self.template(cls.KEYS[0]), cls.ACTIONS[name])(name, args, owner_dashboard)
        if name.startswith('fleet_') or name in FAMILY_ACTIONS:
            return self.fleet_action(name, args, owner_dashboard)
        raise ValueError('Unknown operation')

    def template(self, key):
        """The routine template that runs this TEMPLATES key, or None. Made on first use, one of each per App."""
        found = self.__dict__.get('_templates')
        if found is None:
            found = self.__dict__.setdefault('_templates', routine_templates.load(self, ROUTINE_TEMPLATES))
        return found.get(key)

    def templates(self):
        """Every routine template, in ROUTINE_TEMPLATES' order."""
        return [self.template(cls.KEYS[0]) for cls in ROUTINE_TEMPLATES]

    def fleet_card(self, kind, ask_id, name, title, body, evidence, action=None, due=None, into=None, family=False, via=None, carried=()):
        """A card for a Fleet request the owner accepted (fleet_requests.py), made from this Machine's own data. Its
        first evidence is a Fleet event on one of the owner's work accounts, marked reviewed so no model reads it by
        itself; an intro also gets its double-opt-in draft, which goes out only with the owner's own Send. A Family's
        to-do or plan (family.py) is a personal card on any of the owner's accounts, never a work one by necessity."""
        accounts = fleet.work_accounts(self.config)
        if family:  # a personal account first
            accounts = [a['id'] for a in self.config.get('accounts', []) if a['id'] not in accounts] + accounts
        elif via and not accounts:  # a task by email can land on an install with only personal accounts
            accounts = [a['id'] for a in self.config.get('accounts', [])]
        with self.store.connect() as db:
            own = [r['account_id'] for r in db.execute(f"SELECT account_id FROM events WHERE id IN ({','.join('?' * len(evidence)) or 'NULL'})", evidence)]
        account = next((a for a in own if a in accounts), accounts[0] if accounts else None)
        if not account:
            raise ValueError('this Machine has no account' if family else 'this Machine has no work account')
        stamp, source_id = now(), 'fleet:' + str(ask_id)
        meta = {'sender_display': f"{name} ({via or ('your Family' if family else 'your Fleet')})", 'fleet_kind': kind}
        with self.store.connect() as db:
            db.execute('INSERT OR IGNORE INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                       "VALUES(?,?,'fleet.request',?,?,?,?,0,?,1,1,?)",
                       (account, source_id, stamp, title, body, json.dumps(meta), hashlib.sha256((title + body).encode()).hexdigest(), stamp))
            event_id = db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account, source_id)).fetchone()[0]
            # A handoff's sources (fleet_requests.parse_sources): copies of the emails or messages the card was built from,
            # saved here so they read like any card's sources, offline. Marked reviewed: no model reads them by itself.
            copies = []
            first = name.split()[0] if name else 'a teammate'
            for n, src in enumerate(carried):
                cid = source_id + ':' + str(n)
                where = src.get('intercom')
                own = where and intercom_own_event(db, self.config, where)
                if own:  # this Machine reads that workspace too: the card is on the conversation itself (its link, reply)
                    copies.append(own)
                    continue
                db.execute('INSERT OR IGNORE INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                           'VALUES(?,?,?,?,?,?,?,0,?,1,1,?)',
                           (account, cid, 'fleet.email' if src['kind'] == 'email' else 'fleet.intercom' if where else 'fleet.message', src['when'],
                            src['subject'] or '(no subject)', src['body'],
                            json.dumps({'sender_display': f"{src['from']}, via {first}", 'from': src['from'], 'carried_by': name,
                                        'fleet_kind': kind, **({'truncated': True} if src.get('clipped') else {}),
                                        **({'intercom': where, 'conversation_id': where['conversation_id'], 'source_url': intercom_link(where),
                                            **({'contact_email': where['contact'], 'contact_name': re.sub(r'\s*<[^>]*>', '', src['from']).strip()[:100]}
                                               if where.get('contact') else {})} if where else {})}),
                            hashlib.sha256((src['subject'] + src['body']).encode()).hexdigest(), stamp))
                copies.append(db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account, cid)).fetchone()[0])
        if into:  # a handoff on something the owner already has a card on: it joins that card, with their summary
            with self.store.connect() as db:
                row = db.execute('SELECT event_ids,body FROM suggestions WHERE id=?', (into,)).fetchone()
                ids = json.loads(row['event_ids'] or '[]')
                if event_id not in ids:
                    db.execute('UPDATE suggestions SET event_ids=?,body=? WHERE id=?',
                               (json.dumps([*ids, *[c for c in copies if c not in ids], event_id]), ((row['body'] or '') + '\n\n' + body[:700])[:2400], into))
            return into
        # A review to-do has its own key: confirm_action refuses any send from it (fleet_reviews.py)
        card = self.store.suggest(('fleet-review:' if kind == fleet_reviews.KIND else 'fleet:') + str(ask_id), title[:90], body[:700], [*copies, event_id, *[e for e in evidence if e != event_id]], when='now',
                                  work=not family and account in fleet.work_accounts(self.config), due=due)
        if action and not card.get('duplicate'):
            with self.store.connect() as db:
                row = db.execute('SELECT account_ids FROM suggestions WHERE id=?', (card['id'],)).fetchone()
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=? AND status='pending'", (card['id'],))
            draft = next_actions.validate(action, self.config, json.loads(row['account_ids']))
            self.store.prepare(card['id'], f"A double-opt-in email to {action['to'][0]}: it asks them first whether they want the "
                                           f"introduction. Read it, change it if you like, and send it yourself.", next_action=draft,
                               outcome={'state': 'needs_you', 'needs': 'read and send the intro email'})
        return card['id']

    BUG_SHOT_BYTES = 2 * 1024 * 1024
    BUG_TEXT = 4000

    HELP_TOPICS_SECONDS = 6 * 3600
