#!/usr/bin/env python3
"""Independent read-only ingestion, suggestions and explicitly approved email drafts."""
from __future__ import annotations

import argparse
import base64
import collections
import concurrent.futures
import contextlib
import datetime as dt
import difflib
import functools
import gzip
import hashlib
import hmac
import http.client
import importlib.util
import html
import email.utils
from html.parser import HTMLParser
import http.server
import json
import logging
import os
from pathlib import Path
from decimal import Decimal
import random
import socket
import re
import secrets
import shlex
import math
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import types
import urllib.error
import urllib.parse
import urllib.request
import uuid
from zoneinfo import ZoneInfo
from timeutil import (DAY_NAMES, WORK_HOURS, WORK_HOURS_DEFAULT, clock, in_hours, is_work_day, local_tz, morning_label,  # noqa: F401
                      next_work_day, now, set_timezone, set_work_hours, work_hours)  # the owner's time zone and hours, the clock
import abilities
import bug_queue
import check_now
import embeddings
import gbrain
import gap_note
import github_route
import graph
import knowledge
import own_addresses
import parked_fixes
import project_success
import crm
import crm_fields
import crm_fixes
import crm_import
import i18n
import locale_prefs
import notify
import clear_pace
import todo_areas
import mail_attachments
import message_seal
import enrichment
import fleet
import fleet_reviews
import shared_graph
import agent_jobs
import codex_signin
import chat_model
import activity
import activity_log
import error_feed
import mimetypes
import work_removal
import retention
import chat_files
import talk_live
import voice_input
import whatsapp_images
import security_levels
import skills
import handoff_mail
import task_invites
import task_pages
import help_topics
import team_learnings
import authorship
import corrections
import learning_loop
import bring_in
import missed_work
import person_summary
import fleet_learnings
import google_api
import ms_graph
import signatures
import next_actions
import calendar_writes
import doc_writes
import meeting_notes
import meeting_writer
import meet_link
import places
import qr
from sources import (CALENDAR_SERVICES, MAIL_SERVICES, MICROSOFT_SERVICES, SourceError, credential, gog_read,  # noqa: F401
                     gog_signed_in_since, gog_signin_command, gog_token_path, mail_account, mailbox_name, owner_credential,
                     rate_limited, transient, upstream_busy)  # reading the owner's sources: errors, credentials, Google and Microsoft
import browser_login
import browser_viewer
import preparation_state
import model_budget
import model_fallback
# which model OpenClaw runs and whether it can (models.py)
from models import background_model, claude_plan_route, has_model, main_model, model_ready, openclaw_model  # noqa: F401
import follow_ups
import bounces
import recurring
import still_needed
import pacing
import portable
import service
import dashboard_parts
import ai_access
from agents_app import AgentsApp
from ai_app import AiApp
from calendar_app import CALENDAR_BACK_DAYS, CalendarApp
from corrections_app import CorrectionsApp
from bring_in_app import BringInApp
from missed_work_app import MissedWorkApp
from gbrain_app import GBrainApp
from meet_app import MeetApp
from recurring_app import RecurringApp
from routines_app import RoutinesApp
from mail_cleanup_app import MailCleanupApp  # noqa: F401  (composed in machine/main.py)
from reading_digest_app import ReadingDigestApp  # noqa: F401  (composed in machine/main.py)
from subscriptions_app import SubscriptionsApp  # noqa: F401  (composed in machine/main.py)
from birthdays_app import BirthdaysApp  # noqa: F401  (composed in machine/main.py)
from birthdays_facebook_app import BirthdaysFacebookApp  # noqa: F401  (composed in machine/main.py)
from shared_graph_app import SharedGraphApp
from skills_app import SkillsApp
from whatsapp_images_app import WhatsAppImagesApp
from support_app import SupportApp
from machine import names as display_names
from machine.sources.rows import SKIPPED, Skips
from machine.app.check_now import CheckNowApp
from machine.app.conversation import ConversationApp
from machine.app.export import ExportApp
from machine.export import staged as staged_import
from machine.app.history import HistoryApp
from machine.store import history as history_store
from machine.store import review_backoff
from machine.store.machine_cards import MachineCardsStore
from machine.store.core import StoreCore
from machine.app.setup_card import (
    PHONE_APP_STORE,
    SetupCardApp,
    phone_app_nudge,
    phone_qr,
    setup_card,
    setup_dismiss,
    setup_restore,
)
from machine.sources.slack import (
    SLACK_FIRST_STEPS,
    SLACK_ID,
    SLACK_KEPT_KEY,
    Slack,
    slack_activity,
    slack_error,
    slack_event,
    slack_first_import_next,
    slack_first_import_plan,
    slack_first_import_progress,
    slack_first_import_wanted,
    slack_ids_named,
    slack_interval,
    slack_name_table,
    slack_named,
    slack_named_out,
    slack_next_due,
    slack_order,
    slack_page_names,
    slack_raw_title,
    slack_rest,
)
from machine.app.knowledge_export import KnowledgeExportApp
from machine.app.meeting_writes import MeetingWritesApp
from machine.app.model_pacing import ModelPacingApp
from machine.app.recap_settings import RecapSettingsApp
from machine.app.review_saves import ReviewSavesApp
from machine.app.calendar_clashes import CalendarClashesApp
from machine.app.search_ask import SearchAskApp
from machine.app.signatures import SignaturesApp
from machine.app.summaries import SummariesApp
from machine.app.voice import VoiceApp
from machine.config import (
    BRAND_ASSETS,
    BROWSER_LEASE,
    DEFAULT_CONFIG,
    LOG,
    ROOT,
    RULE_FILES,
    SIGNIN_ERROR,
    SOURCE_NOTES,
    SOURCE_NOTE_ALIASES,
    WORKSPACE,
)
from machine.timing import (
    SLOW_REQUEST_SECONDS,
    _REQUEST_TIMING,
)
from machine.text import (
    ATTACHMENT_INLINE,
    COPY_CHUNK,
    COPY_MAGIC,
    FORWARD_SUBJECT,
    INVISIBLE,
    PLAIN_PLACEHOLDER,
    PlainHTML,
    QUOTED_HISTORY_KEPT,
    QUOTED_MARK,
    REPLY_HEADER,
    _address,
    _copy_keys,
    _copy_tag,
    _xor,
    clamp,
    email_body,
    encoded,
    first_sentence,
    message_attachments,
    message_html,
    message_images,
    open_copy,
    plain_html,
    seal_copy,
    shown_body,
    split_quoted_history,
    trim_quoted_history,
    visible_text,
)
from machine.prompts.review import (
    FACTS_YOU,
    FACT_KIND_HINT,
    FIRST_LOOK_READ_RULE,
    OWNER_YOU,
    REVIEW_DONE,
    review_prompt,
    source_notes,
)
from machine.prompts.profile import (
    ORG_STEP,
    PROFILE_ROOM,
    SHARE_VERDICTS,
    SKILLS_LEASE,
    SKILLS_PAGES,
    SKILLS_READ,
    SKILLS_SIGNIN,
    SKILLS_SITES,
    SKILLS_ZIP_JS,
    VOICE_CHARS,
    VOICE_LINES,
    VOICE_PRECISE,
    VOICE_TEXT,
    import_prompt,
    orgs_prompt,
    profile_prompt,
    roles_prompt,
    share_history_prompt,
    skills_find_prompt,
    voices_prompt,
)
from machine.cards import (
    ACTION_BUSY,
    ACTION_WORKING,
    CARD_DRAFT_KINDS,
    CHAT_HANDLE,
    CHAT_STOPPED,
    HANDOFF,
    LOCAL_CONTINUE,
    LOCAL_TRY_AGAIN,
    LOOKS_DONE_SQL,
    NOT_FOR_OWNER_SQL,
    PREPARATION_WAITING,
    PREPARATION_WORKING,
    SOURCE_DM,
    SOURCE_RAW,
    action_busy,
    answered_only,
    ask_blocked,
    ask_question,
    ask_text,
    asked_snooze_time,
    blocker_questions,
    card,
    card_draft,
    card_recipients,
    card_task,
    chat_plain_name,
    checkin_line,
    controls,
    current_title,
    expired_text,
    group_sender,
    handoff_checkin,
    handoff_redirect,
    looks_done,
    looks_done_at,
    merge_state,
    outcome_state,
    owner_snooze_until,
    plain,
    retry_label,
    retry_pointless,
    sentence,
    snooze_choices,
    snooze_time,
    source_line_shown,
    thread_return_time,
    thread_snooze_note,
    title_kept,
    todo_state,
    undated_card,
    waits_on_others,
)
from machine.browser import (
    AGENT_DB,
    BROWSER_DOWN,
    BROWSER_RECOVERED,
    BROWSER_WAIT,
    BROWSER_WORK,
    FINAL_STEPS,
    PANE_QUERY,
    PEEK_EVERY,
    PEEK_WIDTH,
    SECRET_PARAM,
    SIGNIN_ADDRESS,
    SIGNIN_KINDS,
    SIGNIN_WATCH,
    STEP_NAMES,
    TAB_LOOK,
    browser_lease_script,
    browser_link,
    browser_read_failure,
    browser_result,
    browser_view_link,
    browser_wait,
    own_tab,
    preparation_steps,
    recover_browser,
    run_page,
    run_tab,
    safe_link,
    same_site,
    signin_address,
    signin_handoff,
    signin_kind,
    signin_link,
    signin_name,
    task_page,
    transcript_tool_calls,
)
from machine.chat import (
    AGENT_WORK_NOTE,
    CHAT_AGENTS,
    CHAT_FILES_ONLY,
    CHAT_HISTORY_LIMIT,
    CHAT_IDS,
    CHAT_LEARNED,
    CHAT_MARKER,
    CHAT_NOTES,
    CHAT_NOT_SENT,
    CHAT_ON,
    CHAT_OWNER_WORDS,
    CHAT_PART,
    CHAT_PATHS,
    CHAT_RESULT_LINK,
    CHAT_ROLES,
    CHAT_SAVED,
    CHAT_SECRETS,
    CHAT_SENT,
    CHAT_STEP_FAILED,
    CHAT_STEP_HOW,
    CHAT_UNDONE,
    card_chat_handoffs,
    chat_agent_text,
    chat_cli_replies,
    chat_conversation,
    chat_draft,
    chat_excerpt,
    chat_items,
    chat_ms,
    chat_name,
    chat_person,
    chat_reply,
    chat_result_files,
    chat_run_keys,
    chat_text,
    chat_text_phase,
    handoff_machine,
    owner_time_line,
    unseen_draft,
)
from machine.faults import (
    DB_BUSY_RETRY,
    EXTERNAL_ERRORS,
    FAULT_AREAS,
    FAULT_QUOTED,
    FAULT_STEPS,
    FAULT_WHERE,
    FaultLog,
    OUTSIDE_SERVICES,
    RELEASE_TAG,
    SOURCE_REPO,
    _SOURCE_URL,
    code_version,
    db_busy,
    fault_event,
    fault_frames,
    fault_message,
    fault_origin,
    fault_plain,
    fault_where,
    outside_service,
    restart_self,
    running_release,
    source_url,
    watch_faults,
)
from machine.sources.exclusions import (
    ANDROID_STATUS_NOTICES,
    DEFAULT_EXCLUDED_EMAIL_SUBJECTS,
    ROUTINE_CALENDAR,
    calendar_title_excluded,
    default_exclusions,
    email_subject_excluded,
    excluded_by_rules,
    routine_recurring_instance,
    routine_rules,
)
from machine.sources.salesflare import (
    SALESFLARE_APP,
    SALESFLARE_STUCK,
    Salesflare,
    salesflare_context,
    salesflare_email_event,
    salesflare_feed,
    salesflare_in_pipelines,
    salesflare_link,
    salesflare_meeting_event,
    salesflare_progress,
    salesflare_recent_accounts,
    salesflare_time,
    salesflare_time_or_none,
    sync_salesflare,
)
from machine.sources.telegram import (
    TELEGRAM_CHAT,
    Telegram,
    owner_telegram_chats,
    sync_telegram,
    telegram_event,
    telegram_photo_asker,
)
from machine.sources.signal_chats import (
    Signal,
    owner_signal_chats,
    signal_event,
    sync_signal,
)
from machine.sources.gmail import (
    Gmail,
    list_headers,
    message_event,
    sync_gmail,
)
from machine.sources.calendar import (
    Calendar,
    all_day_span,
    calendar_account_owner,
    calendar_edit_times,
    calendar_event,
    calendar_guests,
    calendar_keys,
    calendar_owned,
    calendar_owner_name,
    calendar_room,
    calendar_rooms,
    calendar_time,
    calendar_write_events,
    calendar_write_ids,
    company_domains,
    event_start,
    expiry_moment,
    invite_people,
    room_name,
    sync_calendar,
    team_people,
)
from machine.model_usage import (
    CHATGPT_USAGE_PAGE,
    CodexAppServer,
    codex_same_account,
    model_resets,
    model_status,
    model_usage,
    node_bin,
    node_env,
    telegram_account,
    telegram_on,
    usage_status,
    use_model_reset,
)
from machine.sources.android import (
    ANDROID_APP_NAMES,
    Android,
    android_app_name,
    android_event,
    sync_android,
    sync_android_feed,
    sync_android_preferred,
)
from machine.sources.gateway import (
    GATEWAY_BUCKET,
    GATEWAY_SIGNALS,
    GatewayJournal,
    gateway_classify,
    gateway_event,
    gateway_line,
    sync_gateway,
)
from machine.sources.connectors import (
    ABILITY_CHECK_SECONDS,
    BUILT_IN_SERVICES,
    CONNECTORS,
    CONNECTOR_HELPERS,
    HOSTED_SIGNINS,
    ON_DASHBOARD,
    SIGNIN_ONLY,
    reconnect_help,
    hosted_docs_sources,
    REPLY_SERVICES,
    SILENT_HOURS,
    SILENT_MIN_FAILURES,
    SILENT_MIN_WEEKLY,
    UNNAMED,
    WHATSAPP_HISTORY_GREW,
    WHATSAPP_HISTORY_HOURS,
    _connectors,
    _whatsapp_history,
    calendar_prompt,
    companies_prompt,
    connector_says,
    connector_services,
    doc_comments,
    doc_write_files,
    doc_write_prompt,
    docs_health,
    docs_offered,
    docs_provider,
    docs_transport,
    docs_unset,
    docs_write_offered,
    docs_write_transport,
    intercom_link,
    intercom_own_event,
    intercom_transport,
    load_connector,
    meeting_notes_prompt,
    read_window,
    remember_profiles,
    silent_failure,
    whatsapp_history,
    writable_calendars,
)
from machine.sources.whatsapp import (
    WHATSAPP_JID,
    WhatsApp,
    owner_whatsapp_chats,
    reply_spots,
    sync_whatsapp,
    whatsapp_event,
    whatsapp_photo_asker,
)
from machine.delivery.push import (
    APP_BODY,
    APP_BUTTONS,
    APP_EMPTY,
    APP_GONE,
    APP_SCHEME,
    DANGLING_POINTER,
    HINT_MAILS,
    HINT_SOURCES,
    HOSTED_REVIEWS_AUTO_SINCE,
    NOTICE_DECISION,
    NUDGE_KINDS,
    QUICK,
    QUICK_LABELS,
    QUICK_OPENS,
    QUICK_RUNS,
    REPORT_HOURS,
    TALK_KINDS,
    app_clear_step,
    app_draft_lead,
    app_next_step,
    app_notice,
    app_wake,
    cloud_target,
    hold_handoff,
    hold_mail,
    notice_decision_refused,
    mail_ready,
    nudge_wait,
    person_line,
    phone_app,
    push_key,
    push_node,
    push_notify,
    push_reach,
    push_send,
    quick_kind,
    quick_web,
    reminder_channels,
    reminder_line,
    report_done,
    reported,
    result_lead,
    reviews_start_by_themselves,
    setup_hints,
    strip_result_links,
    talk_about,
    waiting_count,
)
from machine.delivery.telegram import (
    DeliveryNotSent,
    fleet_telegram,
    telegram,
    telegram_request,
)
from machine.delivery.deliver import (
    EDIT_ROWS,
    FEEDBACK_COLUMN,
    cached_card_ids,
    deliver,
    deliver_one,
    delivery_time,
    fleet_notice_push,
    fleet_push,
    reconcile_uncertain,
)
from machine.actions import (
    AGENT_ACTIONS,
    AI_ACTIONS,
    CARD_ACTIONS,
    CHAT_ACTIONS,
    COMPOSE_ACTIONS,
    CONNECT_ACTIONS,
    CONTACT_ACTIONS,
    CRM_ACTIONS,
    DASHBOARD_ACTIONS,
    EXPORT_ACTIONS,
    FAMILY_ACTIONS,
    FLEET_REQUEST_ACTIONS,
    FRIEND_ACTIONS,
    GBRAIN_ACTIONS,
    GRAPH_SHARE_ACTIONS,
    LEARNING_ACTIONS,
    MEET_ACTIONS,
    OWNER_ACTIONS,
    SEARCH_ASK_ACTIONS,
    SHARE_ACTIONS,
    SKILL_ACTIONS,
    SUPPORT_ACTIONS,
    TALK_ACTIONS,
    UPLOAD_ACTIONS,
    VOICE_ACTIONS,
)
from machine.store.events import (
    EventsStore,
    RUN_SIGNAL_BUDGET,
    SET_ASIDE_AFTER,
    TRANSIENT_REPORT_AFTER,
)
from machine.store.review import (
    AUTOMATED_LABELS,
    BRIEF_SNIPPET_CHARS,
    BRIEF_WEIGHT,
    BULK_PRECEDENCE,
    CARD_OPEN,
    FIRST_LOOK_NOTE,
    FIRST_LOOK_READ,
    INTERCOM_ASSIGNED,
    INTERCOM_TAKEN_RULE,
    OWNER_AREA_RULE,
    OWNER_CARD_RULE,
    OWNER_FILES_RULE,
    PREVIEW_DAYS,
    REPLY_KINDS,
    REVIEW_METADATA_SKIP,
    REVIEW_PAGE_CHARS,
    REVIEW_PREVIEW_CHARS,
    REVIEW_SESSION_PREFIX,
    REVIEW_TERMINAL,
    ROBOT_SENDER,
    ReviewStore,
    TEAM_INBOX_RULE,
    board_replies_waiting,
    bulk_kind,
    claim_weight,
    compact_metadata,
    intercom_assignment,
    intercom_taken,
    own_message,
    review_pages,
    review_view,
    service_review_ended,
    signal_weight,
    team_only,
    title_view,
)
from machine.store.cards import (
    CardsStore,
    KEEP_OWNER_TITLE,
    OWNER_WORDS_MAX,
    SOURCE_KIND,
    TITLE_OWNER_MAX,
    USE_MAIL_KINDS,
    active_preview,
    awaiting_key,
    awaiting_match,
    first_look_running,
    own_life_evidence,
    owner_card_alike,
    owner_card_of,
    owner_title,
    promise_closed_at,
    same_matter_cards,
    same_thread_card,
    source_kind,
    source_line,
    source_text,
    thread_keys,
    use_line,
    use_view,
)
from machine.store.decisions import (
    ALREADY_HANDLED,
    AUTO_UNDO_NEW,
    DecisionsStore,
    MESSAGE_KINDS,
    NEGATED_COMPLETION,
    NOTHING_SENT,
    NOT_TAKEN,
    SEND_RETRY_AFTER,
    UNDO_MERGE,
    draft_saved,
    handoff_wait,
    note_first,
    owner_area_open,
    owner_reports_handled,
    pause_idle_steps,
    reply_lead,
    send_lock,
    send_retry_ok,
    settle_sent,
    skill_update_after,
    skill_update_view,
)
from machine.store.voices import (
    DRAFT_EVENT_KINDS,
    ELSEWHERE_DAYS,
    EVENT_CHANNELS,
    NOTE_KINDS,
    OWN_KINDS,
    PROFILE_SKIP,
    VOICE_CHANNELS,
    VOICE_EXAMPLES,
    VOICE_KEEP,
    VOICE_MAX,
    VOICE_STUDY,
    VOICE_STUDY_DAYS,
    VOICE_STUDY_EACH,
    VOICE_STUDY_MIN,
    VOICE_STUDY_PER,
    VOICE_STUDY_SCAN,
    VoicesStore,
    conversation_of,
    own_predicate,
    own_text,
    sentences,
    similar,
    voice_block,
    voice_channel,
    voice_lines,
)
from machine.store.facts import (
    AI_FACTS_HEAD,
    EVENT_DAYS,
    FACTS_ALL_UNDER,
    FACTS_FLOOR,
    FACTS_GENERAL_HARD,
    FACTS_GENERAL_MAX,
    FACTS_GENERAL_ROOM,
    FACTS_TOP,
    FACTS_UNUSED_DAYS,
    FACT_HALF_LIFE,
    FACT_KINDS,
    FACT_SORTS,
    FactsStore,
    ai_fact_by,
    fact_expired,
    fact_until,
    fact_weight,
    suggestion_scope,
)
from machine.store.promises import (
    PROMISE_CHECK_DAYS,
    PROMISE_TITLE_MAX,
    PROMISE_WHAT_MAX,
    PromisesStore,
    TITLE_CLAUSE,
    TITLE_DANGLING,
    fit_title,
    promise_check_at,
    promise_logged,
    promise_state,
    promise_text,
    promise_title,
    promise_who_named,
)
from machine.store.views import (
    CHAT_KINDS,
    INTERCOM_PART,
    ViewsStore,
    area_hint,
    based_on_views,
    chat_view,
    sender_first_name,
    skill_labels,
    slack_people_names,
    source_leads,
    source_lines_shown,
    stopped_step,
)
from machine.store.profile import (
    EVIDENCE_PAGE_CHARS,
    ORGS_PEOPLE,
    PROFILE_LISTS,
    PROFILE_MESSAGES,
    PROFILE_MIN,
    PROFILE_SESSION_PREFIX,
    PROFILE_TEMPLATE_COPIES,
    PROFILE_TEXT,
    PROFILE_VOICES,
    PROFILE_WEIGHTS,
    ProfileStore,
    ROLES_PEOPLE,
    SHARE_HISTORY_BATCH,
    SHARE_HISTORY_PAGE,
    TODO_SOURCE,
    TODO_SOURCE_OTHER,
    evidence_pages,
    recap_day,
    todo_source,
)
from machine.store.first_look import (
    FIRST_ACTIONS,
    FIRST_LOOK_NAMES,
    FIRST_MAGIC_SETTLE_SECONDS,
    FIRST_TIPS,
    FIRST_TIPS_UNTIL,
    FirstLookStore,
    GREETING_HOURS,
    TIP_SOURCES,
    TIP_USED,
    VERIFIED_KINDS,
    first_value,
)
from machine.web.serving import (
    COMPRESSIBLE,
    COMPRESS_MIN,
    _DASHBOARD_VERSION,
    _WHOIS,
    _brotli,
    _zstd,
    compress_body,
    content_codings,
    dashboard_base,
    dashboard_cache_scope,
    dashboard_csrf,
    dashboard_hosts,
    dashboard_page,
    dashboard_status,
    dashboard_version,
    etag_base,
    etag_matches,
    tailnet_login,
)
from machine.web.waiting import (
    KeyWaitingPage,
    message_key_keeper,
)
from machine.web.handler import (
    ACTION_FAILED,
    EMAIL_KINDS,
    MAIL_HEAD,
    SLACK_LINK,
    UPLOAD_REQUEST_BYTES,
    approval_document,
    browser_embed,
    event_glance,
    make_handler,
)
from machine.app.talk import (
    TalkApp,
)
from machine.app.fleet import (
    FleetApp,
    fleet_served,
    own_or_joined,
)
from machine.app.follow_ups import (
    FollowUpsApp,
    NEWER_KINDS,
    activity_who,
    newer_activity,
)
from machine.app.promise_checks import (
    ELSEWHERE_KINDS,
    PROMISE_CARDS_PER_DAY,
    PromiseChecksApp,
    activity_since,
    owner_last_word,
    promise_home,
)
from machine.app.graph_actions import (
    GRAPH_CHECK_SECONDS,
    GraphActionsApp,
    account_services,
    forget_in_notes,
)
from machine.app.card_chat import (
    CardChatApp,
    save_hours,
)
from machine.app.recap import (
    RECAP_CHOICES,
    RECAP_CHOICES_NOTE,
    RECAP_CIRCLE,
    RECAP_DONE,
    RECAP_DONE_NUMBERED,
    RecapApp,
    recap_buttons,
    recap_choice_view,
    recap_clip,
    recap_escape,
    recap_graph_lines,
    recap_meetings,
    recap_named,
    recap_noise,
    recap_presentation,
    recap_share_lines,
    recap_view,
    weekly_recap,
    weekly_recap_message,
)
from machine.app.first_look import (
    FIRST_DIG_CARDS,
    FIRST_DIG_HOURS,
    FIRST_DIG_PACE_SECONDS,
    FIRST_DIG_SIGNALS,
    FIRST_DIG_USAGE,
    FIRST_LOOK_DONE_HOURS,
    FIRST_LOOK_NEXT_SIGNALS,
    FIRST_LOOK_RETRY_MIN_SECONDS,
    FIRST_LOOK_RETRY_SECONDS,
    FIRST_LOOK_SETTLE_SECONDS,
    FIRST_LOOK_TAIL_SIGNALS,
    FIRST_LOOK_TRIES,
    FirstLookApp,
    QUICK_LOOK_HOURS,
    QUICK_LOOK_SIGNALS,
    REVIEW_MAX_WAIT_MINUTES,
    SYSTEM_SERVICES,
    first_look_batch,
    first_look_retry_at,
    first_look_spent,
    review_max_wait,
    signal_family,
)
from machine.app.preparation import (
    BROWSER_UPLOADS,
    OWNER_STEP_PREPARATION,
    PREPARATION_DEADLINE_SECONDS,
    PREPARATION_INTERRUPTED_TRIES,
    PREPARATION_PROBE_SECONDS,
    PROMPT_LIMIT,
    PreparationApp,
    activity_lines,
    area_prompt,
    card_sources,
    chat_prompt,
    finish_files,
    finish_text,
    newer_activity_lines,
    owner_details,
    preparation_overdue,
    preparation_prompt,
    stage_finish_files,
)
from machine.app.review import (
    AI_CONNECTED_MINUTES,
    AI_CONNECTING_MINUTES,
    AI_CONNECTING_NAME,
    FIRST_LOOK_SIGNAL_SECONDS,
    FIRST_LOOK_TICK_SECONDS,
    KIND_WORDS,
    REVIEW_ASKED_SECONDS,
    REVIEW_FAILURES,
    REVIEW_FAILURE_PHASES,
    REVIEW_PROBE_SECONDS,
    REVIEW_REASONS,
    REVIEW_STEPS,
    REVIEW_TICK_SECONDS,
    ReviewApp,
    ai_connecting,
    event_page,
    first_cards_report,
    first_eta_minutes,
    fit_events,
    metadata_page,
    review_step_title,
    review_steps,
)
from machine.store.faults import (
    FaultsStore,
)
from machine.app.settings_actions import (
    SettingsActionsApp,
    activity_report,
    hours_settings,
)
from machine.app.notifications import (
    NotificationsApp,
)
from machine.app.browser import (
    BrowserApp,
)
from machine.app.profile import (
    FIRST_PROFILE_RETRY_SECONDS,
    FIRST_PROFILE_TRIES,
    PROFILE_SECONDS,
    ProfileApp,
    SKILLS_SESSION_PREFIX,
)
from machine.app.feedback import (
    FeedbackApp,
    prompt_text,
)
from machine.app.card_actions import (
    CardActionsApp,
    NOT_A_PERSON,
    SENDING_FINISH,
    ask_do_now,
    doable_now,
    owner_turn,
    replied_to,
    reply_to_newest,
    thread_recipients,
)
from machine.app.docs import (
    DocsApp,
)
from machine.app.status import (
    StatusApp,
    agent_work_status,
    compact_status,
    needs_you,
    sign_in_help,
)
from skills_app import (
    SKILL_NOTES_MIN,
    SKILL_REGROW,
)
from machine.app.workers import (
    BACKGROUND_GAP_SECONDS,
    GOOGLE_PHOTO_LISTS,
    GOOGLE_PHOTO_PAGES,
    LIVE_CONFIG,
    WorkersApp,
    google_photo_accounts,
    google_photo_offers,
)
from machine.app.voice import (
    VOICE_WARM_QUIET,
)
from machine.app.action_runs import (
    ActionRunsApp,
    PREPARATION_SETTLE_SECONDS,
    active_work,
    queue_delegate_wait,
    queue_thread_snooze,
    settle_doc_write,
)
from machine.app.sync import (
    QUICK_RETRY_MAX,
    QUICK_RETRY_SECONDS,
    SALESFLARE_RESTART_SPREAD,
    SALESFLARE_ROUND_SPREAD,
    SYNC_LOCKS,
    SYNC_LOCKS_LOCK,
    SyncApp,
    remember_slack_names,
    sync_slack,
    sync_source,
)
from machine.app.mail import (
    MailApp,
)
from machine.app.new_cards import (
    NewCardsApp,
    agent_about,
    agent_history,
    agent_messages,
    owner_card_area,
)
from machine.app.serve import (
    ServeApp,
)
from machine.app.connect import (
    ConnectApp,
    CONNECT_SIGNIN,
    CONNECT_SIGNIN_WAIT,
    connect_form,
    same_signin,
)

from machine.main import (  # noqa: F401 - the service and its mixins (machine/main.py), re-exported
    APP_MIXINS,
    App,
    Store,
)


VERIFIED_DECISION_SOURCES = ('telegram', 'dashboard')


SOURCE_KIND['fleet.request'] = 'Fleet'
SOURCE_KIND['fleet.email'] = 'email'  # a copy a teammate's handoff carried (fleet_requests.handoff_sources)
SOURCE_KIND['owner.card'] = 'note'  # a card the owner made themselves (New card): their own words
SOURCE_KIND['fleet.message'] = 'message'
SOURCE_KIND['fleet.intercom'] = 'Intercom'  # an Intercom conversation a handoff carried, on a Machine that doesn't read it


MAIL_SERVICES, CALENDAR_SERVICES = ('gmail', 'outlook', 'imap'), ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('command', choices=['serve', 'status', 'call', 'sync-once', 'embed-backfill'])
    parser.add_argument('--input', type=Path, help='JSON action request file; use - for stdin')
    parser.add_argument('--batch', type=int, default=16, help='embed-backfill: events per embedding call')
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.command == 'embed-backfill':
        # Safe next to the running service (it embeds newest first, this oldest first).
        if not embeddings.settings(config):
            raise SystemExit('Set "embeddings" in the config first (see README, Related signals).')
        embeddings.backfill(Store(config['database']).connect, embeddings.settings(config), max(1, args.batch), out=lambda line: print(line, flush=True))
        return
    if args.command == 'call':
        import sys
        request = sys.stdin.read() if str(args.input) == '-' else args.input.read_text()
        if json.loads(request).get('action') in OWNER_ACTIONS:
            sys.exit('Owner decisions and feedback come from Telegram or the dashboard, not the local CLI.')
        token = credential(config, 'api-token')
        http_request = urllib.request.Request(f"http://127.0.0.1:{config['port']}/api/action", data=request.encode(),
                                             headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                                                      'X-Assistant-Client': 'local-cli'})
        with urllib.request.urlopen(http_request, timeout=45) as response:
            print(response.read().decode())
        return
    if args.command == 'serve':
        if staged_import.apply_confirmed(args.config, config):  # Settings, Export: Replace with this export, before serving
            config = json.loads(args.config.read_text())
        lock = Path(config['database']).parent / 'service.lock'
        service.trim_log()
        with lock.open('w') as handle:
            portable.lock(handle, blocking=False)
            # a hosted key comes after a restart, a key in the keyring once it can be read: meanwhile the dashboard says so
            message_seal.wait_for_key(config['database'], say=LOG.warning, protect=message_seal.wanted(config),
                                      waiting=KeyWaitingPage(config))
            message_key_keeper(config)
            App(config, args.config).serve()
    elif args.command == 'status':
        app = App(config)
        print(json.dumps(app.store.snapshot(config['accounts']), indent=2))
    else:
        app = App(config)
        for account in config['accounts']:
            print(account['id'], sync_source(app.store, config, account))


if __name__ == '__main__':
    os.umask(0o077)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    main()
