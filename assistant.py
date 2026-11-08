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
from missed_work_app import MissedWorkApp
from gbrain_app import GBrainApp
from meet_app import MeetApp
from recurring_app import RecurringApp
from routines_app import RoutinesApp
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
    peek_tab,
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
    FACTS_GENERAL_MAX,
    FACTS_TOP,
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


# LinkedIn and X sign in in the Machine's browser while their connect waits (onboarding.wait_signed_in), up to this long
CONNECT_SIGNIN = {'linkedin': 'https://www.linkedin.com/login', 'x': 'https://x.com/i/flow/login'}
CONNECT_SIGNIN_WAIT = 600


def connect_form(source, args):
    """(answers, secrets) for onboarding.WebUI.prefill from the + Add form of one source (onboarding.web_form): only its own
    questions and key, and Work with a company or Personal, as the setup page's form sends them (agent ScriptedUI)."""
    form, answers, secrets_ = source['form'], {}, {}
    given = args.get('answers') if isinstance(args.get('answers'), dict) else {}
    for key, prompt in form['ask']:
        value = given.get(key)
        if isinstance(value, str) and value.strip():
            if len(value) > 500:
                raise ValueError('That answer is too long')
            answers[prompt] = value.strip()
    secret = args.get('secret')
    if form.get('secret') and isinstance(secret, str) and secret.strip():
        if len(secret) > 4096:
            raise ValueError('That key is too long')
        secrets_[form['secret']] = secret.strip()
    if form.get('scope'):
        scope, company = args.get('scope'), ' '.join(str(args.get('company') or '').split())[:60]
        if scope == 'personal':
            boundary = 'personal:me'
        elif scope == 'work' and company and re.fullmatch(r'[^\x00-\x1f<>:]+', company):
            boundary = 'work:' + company
        else:
            raise ValueError('Pick Work with its company, or Personal')
        answers.update({'part of your life': boundary, 'company': boundary})
    answers['You already have'] = f"add another {source['label']} account"  # a new one, when there is one; Reconnect signs one in again
    return answers, secrets_


VERIFIED_DECISION_SOURCES = ('telegram', 'dashboard')


class Store(CardsStore, DecisionsStore, EventsStore, FactsStore, FaultsStore, FirstLookStore, ProfileStore,
            PromisesStore, MachineCardsStore, ReviewStore, StoreCore, ViewsStore, VoicesStore):
    """The service's database: every table, through the Store mixins it is made of (machine/store/*)."""






SOURCE_KIND['fleet.request'] = 'Fleet'
SOURCE_KIND['fleet.email'] = 'email'  # a copy a teammate's handoff carried (fleet_requests.handoff_sources)
SOURCE_KIND['owner.card'] = 'note'  # a card the owner made themselves (New card): their own words
SOURCE_KIND['fleet.message'] = 'message'
SOURCE_KIND['fleet.intercom'] = 'Intercom'  # an Intercom conversation a handoff carried, on a Machine that doesn't read it



MAIL_SERVICES, CALENDAR_SERVICES = ('gmail', 'outlook'), ('calendar', 'outlook_calendar')




def same_signin(accounts, account, store=None):
    """The account and the others that read with its sign-in (Gmail and Calendar of one Google address, Outlook mail and
    calendar of one Microsoft address): the reconnected one always, the others only while their error is a sign-in one."""
    def family(a):
        service = a.get('service', 'gmail')
        return 'microsoft' if service in MICROSOFT_SERVICES else 'google' if service in ('gmail', 'calendar') else None
    email, kind = str(account.get('email') or '').lower(), family(account)
    ids = [account['id']]
    if not email or not kind:
        return ids
    others = [a['id'] for a in accounts if a.get('id') != account['id'] and family(a) == kind and str(a.get('email') or '').lower() == email
              and a.get('transport') == account.get('transport') and a.get('client') == account.get('client')]
    if others and store is not None:
        with store.connect() as db:
            errors = {r['account_id']: r['error'] for r in db.execute(
                'SELECT account_id,error FROM checkpoints WHERE account_id IN (%s)' % ','.join('?' * len(others)), others)}
        others = [i for i in others if re.search(SIGNIN_ERROR, errors.get(i) or '')]
    return ids + others


# App's domain mixins (<domain>_app.py): each holds a domain's App methods and the actions it handles (its ACTIONS).
APP_MIXINS = (SupportApp, CalendarApp, SkillsApp, AgentsApp, GBrainApp, SharedGraphApp, RecurringApp, CorrectionsApp, AiApp, MeetApp, MissedWorkApp,
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
APP_MIXINS += (ProfileApp,)
APP_MIXINS += (BrowserApp,)
APP_MIXINS += (NotificationsApp, SettingsActionsApp)
APP_MIXINS += (RecapSettingsApp,)
APP_MIXINS += (SearchAskApp,)
APP_MIXINS += (ReviewSavesApp,)
APP_MIXINS += (CalendarClashesApp,)


class App(*APP_MIXINS):
    # action name -> method, from the mixins' ACTIONS; App.action calls it as method(name, args, owner_dashboard). Who
    # may call an action is still the reviewed sets above (OWNER_ACTIONS, DASHBOARD_ACTIONS, SUPPORT_ACTIONS, ...).
    ACTION_HANDLERS = {name: method for mixin in APP_MIXINS for name, method in mixin.ACTIONS.items()}
    HISTORY_SOURCES = {'mail': (Gmail, message_event), 'calendar': (Calendar, calendar_event, calendar_title_excluded), 'whatsapp': (WhatsApp, whatsapp_event)}

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
        try:  # what the app starts with: changes after it are followed (follow_config)
            self.config_stamp = self.config_path.stat().st_mtime_ns if self.config_path else None
        except OSError:
            self.config_stamp = None
        self.store = Store(config['database'], protect=self.protection_now(config))
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
                                           card=self.agent_card, revise=self.agent_revise,
                                           network=(lambda body: self.fleet.relay.call('POST', '/agent-results', body)) if self.fleet else None,
                                           ) if agent_jobs.settings(config) is not None else None
        if self.fleet:
            self.fleet.skills = self.skills
            self.fleet.graph_build = self.graph_build  # a shared contact the owner adds (contact_share.py)
            self.fleet.about_you = self.about_you  # Share my contact: the owner's own addresses and numbers

    MESSAGE_CACHE = 40  # source emails kept in memory for the dashboard, newest used last
    MESSAGE_TTL = 600  # seconds

    MAILBOX_LOOKUP_MAX = 10  # messages per mailbox one search keeps

    NO_DOC_CONNECTION = 'No Docs connection in this to-do’s area can do things. Give what you need in the to-do instead.'

    def action(self, name, args, owner_dashboard=False):
        accounts = [a['id'] for a in self.config['accounts']]
        selected = args.get('account_ids', [])
        if name in self.ACTION_HANDLERS:  # an action a domain mixin handles (APP_MIXINS)
            return getattr(self, self.ACTION_HANDLERS[name])(name, args, owner_dashboard)
        if name == 'bug_offer':
            return self.bug_offer(args)
        if name in ('events', 'related') and selected in ('all', ['all']):
            selected = accounts  # search everything, asked for explicitly
        if name in ['events', 'begin_analysis', 'related'] and (not selected or not set(selected) <= set(accounts)):
            raise ValueError('Choose explicit configured account_ids (or ["all"] to search every account with events or related); cross-account reads must be intentional')
        if name == 'mail_attachment':
            return self.mail_attachment({k: v for k, v in args.items() if k != '_folder'})
        if name in task_pages.ACTIONS:  # a task page for an email handoff: add, skip, stop sharing, mark done (task_pages.py)
            if not owner_dashboard:
                raise ValueError('Task pages are shared from the dashboard')
            return self.task_pages.action(name, args)
        if name.startswith('fleet_') or name in FAMILY_ACTIONS:
            return self.fleet_action(name, args, owner_dashboard)
        if name == 'related':
            if not args.get('event_ids') and not str(args.get('query') or '').strip():
                raise ValueError('Give event_ids, a query or both')
            query = str(args.get('query') or '')
            if not embeddings.settings(self.config) and not query.strip():  # no meaning search here: the given signals' own words
                query = ' '.join(r['title'] for r in self.store.events(selected, event_ids=[int(i) for i in args['event_ids']]))
            found, semantic = self.related(selected, args.get('event_ids') or (), query,
                                           min(int(args.get('limit') or 8), embeddings.MAX_LIMIT), args.get('exclude_event_ids') or ())
            score = dict(found)
            rows = sorted(self.store.events(selected, event_ids=list(score)), key=lambda r: list(score).index(r['id']))
            result = event_page(rows, int(args.get('body_offset') or 0), int(args.get('row_offset') or 0))
            for view in result['events']:
                view['similarity'] = score.get(view['id'])
            return {**result, 'semantic': semantic}
        if name == 'events' and args.get('mailbox') is True:
            # Older than what is collected: the mailboxes' own search, live and read-only; what it finds is kept to link
            ids, failed = self.mailbox_lookup(selected, args.get('query'), args.get('limit') or 5)
            rows = sorted(self.store.events(selected, event_ids=ids), key=lambda r: ids.index(r['id'])) if ids else []
            result = event_page(rows, int(args.get('body_offset') or 0), int(args.get('row_offset') or 0))
            if failed:
                result['mailbox_errors'] = failed
            if not ids:
                result['note'] = 'Nothing in those mailboxes matches. Try other words (the person\'s address, part of the subject).'
            return result
        if name == 'events' and args.get('semantic') and str(args.get('query') or '').strip() and args.get('event_ids') is None and embeddings.settings(self.config):
            # Meaning and keywords fused, best first; the plain keyword search stays the default.
            # The dashboard waits for it: a slow embedding server falls back to keywords in seconds, not minutes.
            found, _ = self.related(selected, (), str(args['query']), min(int(args.get('limit') or 40), 40), timeout=8 if args.get('full') else 30)
            order = [i for i, _ in found]
            args = {**args, 'event_ids': order, 'query': ''}
        if name == 'events':
            kinds = args.get('kinds')
            if kinds is not None and not (isinstance(kinds, list) and all(isinstance(k, str) and re.fullmatch(r'[a-z_]+\.[a-z_]+', k) for k in kinds)):
                raise ValueError('kinds is a list of event kinds')
            rows = self.store.events(selected, args.get('query', ''), args.get('limit', 40), event_ids=args.get('event_ids'), kinds=kinds)
            if args.get('semantic') and args.get('event_ids') is not None:
                rows.sort(key=lambda r: args['event_ids'].index(r['id']) if r['id'] in args['event_ids'] else 0)
            # The CLI reads whole rows; agent tool results must stay under OpenClaw's size cut.
            if args.get('full'):
                return rows
            if args.get('metadata_offset') is not None:
                if len(args.get('event_ids') or []) != 1 or len(rows) != 1:
                    raise ValueError('Read metadata with one explicit, available event_id')
                return metadata_page(rows[0], int(args['metadata_offset']))
            result = event_page(rows, int(args.get('body_offset') or 0), int(args.get('row_offset') or 0))
            if args.get('event_ids') is not None:
                result['unavailable_event_ids'] = sorted(set(args['event_ids']) - {r['id'] for r in rows})
            if len(encoded(result)) > REVIEW_PAGE_CHARS:
                raise ValueError('Request a smaller list of event_ids')
            return result
        if name == 'begin_analysis':
            result = self.store.begin_analysis(selected, args.get('limit', 40), args.get('_review_session'), args.get('_review_run'))
            if isinstance(result, dict) and result.get('analysis_id'):
                with self.store.connect() as db:
                    result['projects'] = graph.active_projects(db)  # reuse these names in finish_analysis and suggest
                    result['boards'] = graph.boards_brief(db)  # projects of one kind in stages, moved with finish_analysis stages
                team = self.team_accounts()
                if team:  # Work messages the Shared Graph needs a call on (finish_analysis team)
                    with self.store.connect() as db:
                        row = db.execute('SELECT items FROM analyses WHERE id=?', (result['analysis_id'],)).fetchone()
                        ids = [i['id'] for i in json.loads(row['items']) if not i.get('excluded')] if row else []
                        result['team'] = [r[0] for r in db.execute(f"SELECT id FROM events WHERE id IN ({','.join('?' * len(ids))}) AND account_id IN "
                                                                   f"({','.join('?' * len(team))}) ORDER BY id", (*ids, *team))] if ids else []
                        if result['team']:  # the groups unsure threads already have: reuse a name for the same kind of thread
                            shared_graph.ensure(db)
                            result['share_groups'] = shared_graph.groups(db)
            return result
        if name in CARD_ACTIONS:
            if not owner_dashboard:
                raise ValueError('Cards are added, renamed and merged by the owner, on the dashboard')
            if name == 'card_new':
                return self.card_new_repeating(args)  # recurring_app.py: Repeats, or a rhythm in the words
            if name == 'card_project':  # the to-do's project, by hand ('' for none): graph.set_card_project
                with self.store.connect() as db:
                    return {'id': str(args.get('suggestion_id') or ''), 'project': graph.set_card_project(db, args.get('suggestion_id'), args.get('project'))}
            if name == 'card_rename':
                return self.store.rename_card(args.get('suggestion_id'), args.get('title'), args.get('reset') is True, args.get('decision_id'))
            if name == 'card_move':  # More, Move to Work (todo_areas.py); undo: the move its toast's Undo takes back
                return self.store.move_card(args.get('suggestion_id'), args.get('area'), args.get('decision_id'), undo=args.get('undo'))
            if name == 'card_report_seen':  # Just done, Got it: the owner saw what their confirmed steps did
                return self.store.report_seen(args.get('ids'))
            if name == 'card_use_sources':  # "Use this email for this to-do": what its stuck run asked for (use_sources)
                return self.store.use_sources(args.get('suggestion_id'), args.get('decision_id'))
            return self.store.merge_answer(args.get('suggestion_id'), args.get('merge') is True, args.get('decision_id'))
        if name in CONNECT_ACTIONS:
            if not owner_dashboard:
                raise ValueError('Only the owner adds a source, from the dashboard')
            return self.connect_action(name, args)
        if name == 'client_error':  # the dashboard's own errors, as signatures for the error reports (error_feed.py)
            with self.store.connect() as db:
                return {'ok': True, 'counted': error_feed.record_client(db, args.get('errors'), self.store.code_version, DASHBOARD_ACTIONS)}
        if name in LEARNING_ACTIONS:
            if not owner_dashboard:
                raise ValueError('Only the owner shares learnings, from the dashboard')
            if name == 'learnings_share':
                return {**self.learnings_share(args), 'team_learnings': self.learnings_view()}
            if name == 'learnings_withdraw':
                return {**self.learnings_withdraw(args), 'team_learnings': self.learnings_view()}
            with self.store.connect() as db:
                if name == 'learnings_later':
                    team_learnings.later(db, str(args.get('id') or ''))
                elif name == 'learnings_never':
                    team_learnings.never(db, str(args.get('id') or '') or None)
                elif name == 'set_learnings_vote':  # On, Ask first or Off ({mode}); {on} from an older dashboard
                    team_learnings.set_vote(db, args['mode'] if 'mode' in args else args.get('on') is not False)
                elif name == 'learnings_votes_decide':  # Ask first: these votes may go, or never will
                    team_learnings.decide_votes(db, args.get('ids'), args.get('send') is True)
                elif name == 'set_help_topics':
                    help_topics.set_on(db, args.get('on') is not False)
                elif name == 'set_error_reports':
                    error_feed.set_on(db, args.get('on') is not False)
                elif name == 'set_learnings_auto':  # Send learnings automatically, off unless chosen
                    team_learnings.set_auto(db, args.get('on') is True)
                else:
                    team_learnings.set_offer(db, args.get('on') is not False)
            return {'team_learnings': self.learnings_view()}
        raise ValueError('Unknown operation')

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

    def connect_action(self, name, args):
        """Connections, Add: the sources this install can add, and adding one with the same steps as `assistant
        connect` (onboarding.connect), its questions answered on the dashboard (onboarding.WebUI). One at a time.
        A hosted machine's control plane signs in Google and Microsoft itself: those link to its account page."""
        import onboarding
        if onboarding._assistant is None:
            onboarding._assistant = sys.modules[__name__]  # this module, not a second copy of it
        lock = self.__dict__.setdefault('connect_lock', threading.Lock())
        sessions = self.__dict__.setdefault('connect_sessions', {})
        with lock:
            for key in [k for k, v in sessions.items() if v['state'] != 'running' and time.monotonic() - v['at'] > 1800]:
                sessions.pop(key)
        manage = str(self.config.get('manage_url') or '')
        hosted = manage.startswith('https://')
        if name == 'connect_sources':
            found = {'sources': onboarding.catalog(self.config), 'manage_url': manage if hosted else None,
                     'saveable': bool(getattr(self, 'config_path', None))}
            if hosted:
                # Google, Microsoft, Zoom, Stripe, Intercom, Docs, GitHub, WhatsApp and the phone: signed in from + Add
                # itself, by the control plane, which comes back to this form
                for source in found['sources']:
                    signin = source['service'] if source['service'] in ON_DASHBOARD else fleet.SIGNIN_OF.get(source['service'])
                    signin = 'microsoft_teams' if source['service'] == 'teams' else signin  # its own Microsoft consent
                    if signin in HOSTED_SIGNINS:
                        source['hosted_signin'] = signin
                found['sources'] = hosted_docs_sources(self.config, found['sources'])
            if not hosted:
                # Sign in with <provider> through The Machine's own app (fleet.py connect_start), once this Machine is
                # paired with an account; pasting a token stays as the fallback. One the control plane has no app for
                # (fleet.signins) is marked signin_off: the dashboard shows that other way at once.
                available = self.fleet.signins() if getattr(self, 'fleet', None) is not None else None
                for source in found['sources']:
                    if fleet.SIGNIN_OF.get(source['service']):
                        source['signin'] = fleet.SIGNIN_OF[source['service']]
                        if available is not None and source['signin'] not in available:
                            source['signin_off'] = True
                # Google Meet has no other way: shown only once the control plane says it opens Meet's sign-in for this
                # owner (for everyone, or only the owners it lists)
                found['sources'] = [x for x in found['sources'] if x['service'] != 'google_meet' or (available is not None and 'google_meet' in available)]
                found['paired'], found['pair_url'] = getattr(self, 'fleet', None) is not None, fleet.PAIR_PAGE
            if not hosted or gbrain.on(self.config):
                # GBrain (gbrain.py): one optional tile at the end, on a Machine where the owner can install it
                found['gbrain'] = {'on': gbrain.on(self.config)}
            if agent_jobs.settings(self.config) is not None:
                # Codex (codex_signin.py): its own tile, signed in with a code from OpenAI right here
                found['codex'] = {'status': codex_signin.status(self.config)}
            # Suggested for you: a few tiles this Machine has a signal for (connect_suggested), a setup that failed here first
            failed = [v['source'] for v in sessions.values() if v['state'] == 'failed']
            found['suggested'] = self.connect_suggested([x for x in found['sources'] if hosted or not x.get('broker')], failed)
            return found
        if name in ('codex_signin', 'codex_signin_state'):
            # Self-hosted: Codex's device sign-in on this computer. A hosted Machine's runs on its server, started by
            # the control plane (POST /_machine/connect), which the dashboard follows there.
            if hosted:
                raise ValueError('Your account page signs this one in')
            signin = self.__dict__.setdefault('codex_signin', codex_signin.Signin())
            return signin.start(self.config) if name == 'codex_signin' else signin.view()
        if name in ('connect_signin', 'connect_signin_state'):
            source = args.get('name') if isinstance(args.get('name'), str) else ''
            source = fleet.SIGNIN_OF.get(onboarding.SERVICES.get(source, source), source)  # Gmail and Calendar: Google
            if hosted:
                raise ValueError('Your account page signs this one in')
            if source not in fleet.SIGNIN_SOURCES:
                raise ValueError('That source signs in another way')
            if getattr(self, 'fleet', None) is None:
                raise ValueError('Pair this Machine first')
            if name == 'connect_signin_state':
                return self.fleet.signin_state(source)
            if not getattr(self, 'config_path', None):
                raise ValueError('This service cannot save its settings')
            # one already connected is signed in again (onboarding.connect_delivered), as Reconnect does
            try:
                return {'url': self.fleet.connect_start(source), 'state': 'started'}
            except fleet.SigninUnavailable:
                return {'state': 'unavailable'}  # no tab: the dashboard opens the other way
        if name == 'connect_site_signin':
            # LinkedIn or X while its connect waits for the owner to sign in there: the site's sign-in page in front
            # in the Machine's browser, for the dashboard's sign-in dialog. One already under way (the code it emailed)
            # is brought to the front as it is; `fresh` (Try again after the site stopped it) starts it over in that
            # tab. Nothing is typed here.
            site = args.get('site') if isinstance(args.get('site'), str) else ''
            if site not in CONNECT_SIGNIN:
                raise ValueError('That site signs in another way')
            try:
                base = browser_login.endpoints(self.config)[0]
                hosts = onboarding.SIGNIN_HOSTS[site]
                # a sign-in already under way there (a code it emailed) stays as it is: in front, never a fresh page
                at = lambda t: urllib.parse.urlsplit(t.get('url') or '')
                try:
                    tabs = [t for t in browser_login.browser_cdp._http(base, '/json/list', timeout=5) if t.get('type') == 'page']
                except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError):
                    tabs = []
                under_way = [t for t in tabs if any(browser_login.site(at(t).hostname) == h or browser_login.site(at(t).hostname).endswith('.' + h) for h in hosts)
                             and onboarding.SIGNIN_STEP.search(at(t).path)]
                if under_way and args.get('fresh') is True:  # Try again after the site stopped it: its sign-in page afresh
                    browser_login.browser_cdp.navigate(base, under_way[0]['id'], CONNECT_SIGNIN[site], timeout=20)
                tab = under_way[0]['id'] if under_way else browser_login.browser_cdp.open_tab(base, CONNECT_SIGNIN[site])
            except (browser_login.browser_cdp.CdpError, OSError, IndexError, TypeError, AttributeError, KeyError):
                raise ValueError('I couldn’t open the sign-in page in the browser') from None
            try:
                browser_viewer.focus(CONNECT_SIGNIN[site], base, target=tab)
            except (ValueError, OSError):
                pass
            return {'opened': True, 'view': browser_link(self.config)}
        if name in ('connect_start', 'connect_remove') and args.get('account') is not None:
            account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
            if not account:
                raise ValueError('That account is not connected here')
            if 'account_page' in reconnect_help(account, manage if hosted else None):
                raise ValueError('Your account page signs this one in and out')
            help_ = reconnect_help(account, None)
            if help_.get('shared_by'):
                raise ValueError(f"Shared by {help_['shared_by']}: only its admins can change it")
            if name == 'connect_remove' and help_.get('shared_with'):
                raise ValueError(f"Stop sharing it with {help_['shared_with']} first")
        if name == 'connect_abilities':
            # Brings in signals and Can do things, one switch each (abilities.py): the owner's own, also for one the
            # account page signs in. A restart starts or stops its sync.
            account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
            if not account:
                raise ValueError('That account is not connected here')
            if reconnect_help(account, None).get('shared_by'):
                raise ValueError('Shared by ' + reconnect_help(account, None)['shared_by'] + ': only its admins can change it')
            if not getattr(self, 'config_path', None):
                raise ValueError('This service cannot save its settings')
            with lock:
                try:
                    view = onboarding.set_abilities(self.config_path, account['id'],
                                                    {k: args.get(k) for k in abilities.ABILITIES})
                except onboarding.SetupError as error:
                    raise ValueError(error.message) from None
            LOG.info('connect abilities account=%s signals=%s actions=%s', account['id'], view['signals'], view['actions'])
            return {**view, 'restarting': restart_self(3)}
        if name == 'connect_scope':
            # Work (with its company) or Personal, for a sign-in and the accounts on the same address: the owner's
            # own marking, which a Work Fleet's removal follows (work_removal.py). Also for one the account page signs in.
            account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
            if not account:
                raise ValueError('That account is not connected here')
            if reconnect_help(account, None).get('shared_by'):
                raise ValueError('Shared by ' + reconnect_help(account, None)['shared_by'] + ': only its admins can change it')
            if not getattr(self, 'config_path', None):
                raise ValueError('This service cannot save its settings')
            if not isinstance(args.get('boundary'), str):
                raise ValueError('Pick work with a company name, or personal')
            with lock:
                try:
                    changed = onboarding.set_boundary(self.config_path, account['id'], args['boundary'])
                except onboarding.SetupError as error:
                    raise ValueError(error.message) from None
            LOG.info('connect scope accounts=%s', len(changed))
            return {'changed': changed, 'restarting': restart_self(3)}
        if name == 'connect_remove':
            if not getattr(self, 'config_path', None):
                raise ValueError('This service cannot save its settings')
            with lock:
                if any(v['state'] == 'running' for v in sessions.values()):
                    raise ValueError('A source is being set up; finish or stop that first')
                try:
                    onboarding.disconnect(self.config_path, account['id'])
                except onboarding.SetupError as error:
                    raise ValueError(error.message) from None
                if not hosted:
                    self.forget_device_grant(account)
            LOG.info('connect removed account=%s', account['id'])
            return {'removed': account['id'], 'restarting': restart_self(3)}
        if name == 'connect_start':
            # `name`, since the dashboard's requests carry their own `source` (always "dashboard")
            source = args.get('name') if isinstance(args.get('name'), str) else args.get('source')
            known = {s['name']: s for s in onboarding.catalog(self.config)}
            again = args.get('account') is not None
            if source not in known or (known[source]['broker'] and not again):
                raise ValueError('That source is not added here')
            if again and source != reconnect_help(account, None)['connect_name']:
                raise ValueError('That account is not a ' + known[source]['label'] + ' account')
            if not getattr(self, 'config_path', None):
                raise ValueError('This service cannot save its settings' if hosted else f'This service cannot save its settings; run assistant connect {source} in a terminal')
            answers, secrets_ = connect_form(known[source], args) if args.get('form') is True and not again else (None, None)
            with lock:
                for v in sessions.values():
                    # Starting the same source again replaces a setup the dashboard lost track of (a reload, another
                    # device); so does any setup left untouched for 10 minutes
                    if v['state'] == 'running' and (v['source'] == source or time.monotonic() - v['at'] > 600):
                        v['ui'].cancel()
                        v['state'] = 'cancelled'
                if any(v['state'] == 'running' for v in sessions.values()):
                    raise ValueError('Another source is being added; finish or stop that one first')
                key = secrets.token_hex(12)
                ui = onboarding.WebUI()
                ui.reconnect = again
                if answers is not None:
                    ui.prefill(answers, secrets_)
                if known[source]['form'].get('browser'):
                    # LinkedIn, X: connected before the owner signed in there, it waits, and the dashboard offers that sign-in
                    ui.wait_signin, ui.explains = CONNECT_SIGNIN_WAIT, False
                session = sessions[key] = {'ui': ui, 'state': 'running', 'source': source, 'account_id': account['id'] if again else None,
                                           'label': known[source]['label'], 'at': time.monotonic(), 'hosted': hosted}
            threading.Thread(target=self.connect_run, args=(session,), daemon=True).start()
            return {'session': key, **self.connect_view(session)}
        session = sessions.get(args.get('session')) if isinstance(args.get('session'), str) else None
        if not session:
            raise ValueError('That setup has ended; start it again')
        if name == 'connect_answer':
            value = args.get('value')
            if not isinstance(value, (str, bool, int)) or (isinstance(value, str) and len(value) > 4096):
                raise ValueError('Invalid answer')
            if not session['ui'].answer(args.get('question'), value):
                raise ValueError('That question was already answered')
            session['at'] = time.monotonic()
            time.sleep(0.3)  # most steps answer at once: show what comes next
        elif name == 'connect_cancel':
            session['ui'].cancel()
        return self.connect_view(session)

    def connect_run(self, session):
        import onboarding
        try:
            account = onboarding.connect(self.config_path, session['source'], session['ui'], account_id=session.get('account_id'), restart=False)
            if session.get('account_id'):  # signed in again and checked: its sign-in error, and its siblings', ends now
                try:
                    self.store.signed_in_again(same_signin(self.config.get('accounts', []), account, self.store))
                except Exception as error:  # noqa: BLE001 - the next sync clears it too
                    LOG.warning('sign-in error not cleared account=%s error=%s', account['id'], type(error).__name__)
            session.update(account=account['id'], restarting=restart_self(3), state='done')
        except onboarding.SetupError as error:
            session.update(state='cancelled' if session['ui'].cancelled else 'failed', error=error.message, fix=error.fix)
        except Exception as error:  # the step's own text could quote what was typed: only its kind
            LOG.error('connect source=%s error=%s', session['source'], type(error).__name__)
            session.update(state='failed', error='The setup stopped unexpectedly', fix='try again, or run assistant connect '
                           + session['source'] + ' in a terminal on this computer')
        session['at'] = time.monotonic()

    def connect_view(self, session):
        view = {**session['ui'].view(), **{k: session.get(k) for k in ('state', 'source', 'label', 'error', 'fix', 'account', 'restarting')}}
        if session.get('hosted') and re.search(r'\bterminal\b|\bassistant connect\b', view.get('fix') or ''):
            view['fix'] = 'try again, or get help from your account page'  # a hosted machine has no terminal to run it in
        elif re.fullmatch(r'rerun(?: this when you have it|: assistant connect [\w-]+)', view.get('fix') or ''):
            view['fix'] = 'check what you filled in and try again'  # Try again is right there: no command for a terminal
        view['reconnect'] = session.get('account_id')  # the account signing in again, if that is what this is
        return view

    BUG_SHOT_BYTES = 2 * 1024 * 1024
    BUG_TEXT = 4000

    HELP_TOPICS_SECONDS = 6 * 3600


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
