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
    first_eta_minutes,
    review_step_title,
    review_steps,
)
from machine.store.faults import (
    FaultsStore,
)
from machine.app.settings_actions import (
    SettingsActionsApp,
)
from machine.app.notifications import (
    NotificationsApp,
)
from machine.app.browser import (
    BrowserApp,
)
from machine.app.profile import (
    ProfileApp,
    SKILLS_SESSION_PREFIX,
)
from machine.app.feedback import (
    FeedbackApp,
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


def hours_settings(config, changes):
    """`timezone`, `digest_at` and `work_hours` after `changes` (any of those, or the work_hours keys
    days/start/end/morning at the top level), checked; a ValueError says what is wrong."""
    current = {**WORK_HOURS_DEFAULT, **(config.get('work_hours') or {})}
    nested = changes.get('work_hours') if isinstance(changes.get('work_hours'), dict) else {}
    merged = {**current, **nested, **{k: changes[k] for k in WORK_HOURS_DEFAULT if changes.get(k) is not None}}
    zone = str(changes.get('timezone') or config.get('timezone') or getattr(local_tz(), 'key', '') or 'UTC').strip()
    try:
        ZoneInfo(zone)
    except (ValueError, KeyError, OSError):
        raise ValueError(f'Unknown time zone {zone!r}; use a name like Europe/Brussels or America/New_York') from None
    digest = '%02d:%02d' % clock(changes.get('digest_at') or config.get('digest_at') or '08:30', 'The digest time')
    return {'timezone': zone, 'digest_at': digest, 'work_hours': work_hours(merged)}


def queue_thread_snooze(db, action, job):
    if action.get('snooze_days') and action.get('thread_id'):
        db.execute("INSERT OR IGNORE INTO thread_snoozes(job_id,account_id,thread_id,until,status,created_at,updated_at) VALUES(?,?,?,?,'queued',?,?)",
                   (job['id'],action['account_id'],action['thread_id'],thread_return_time(action['snooze_days']),now(),now()))


def settle_doc_write(store, db, suggestion_id, job_id, action, url=None):
    """A doc made or changed after the owner's OK. With last:true the doc was the whole to-do: done, like a send.
    Otherwise something is left after it (a reply with its link, sharing it): the to-do stays open and carries on with
    that step (then, or what is left), drafted again for the owner's OK, never sent by itself (2026-10-30)."""
    made_now = doc_writes.made_by_itself(db.execute('SELECT approval_id FROM action_jobs WHERE id=?', (job_id,)).fetchone())
    if action.get('last') is True:
        if made_now:  # made while it was prepared (Store.make_new_docs): it stays open with the doc's link for the owner to look at
            return False
        return settle_sent(store, db, suggestion_id, job_id, next_actions.label(action), doc_writes.done(action))
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or row['status'] != 'prepared':
        return False
    finished = {r[0] for r in db.execute("SELECT revision FROM action_jobs WHERE suggestion_id=? AND status IN ('sent','done')", (suggestion_id,))}
    if any(a['kind'] in next_actions.APPROVE_KINDS + next_actions.FINISH_KINDS and a['revision'] not in finished
           for a in next_actions.visible_actions(row['next_action'])):
        return False
    note = doc_writes.done(action)
    step = (f"{note}{' (' + url + ')' if url else ''}. Now: {action.get('then') or 'what is left of this to-do after the doc'}. "
            'Draft it for the owner to approve, never send it; save outcome done only when nothing is left.')
    body = NOTHING_SENT.sub('', row['body'] or '').strip() or row['body']
    stamp = now()
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               ('sent:' + job_id, suggestion_id, 'update', note[:200], 'assistant', stamp))
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               ('after:' + job_id, suggestion_id, 'continue', step[:2000], 'assistant', stamp))
    db.execute("UPDATE suggestions SET status='accepted',body=?,outcome=NULL,early=0,undo_until=NULL WHERE id=?", (body, suggestion_id))
    store.queue_preparation(db, suggestion_id, 'after:' + job_id)
    return True


def queue_delegate_wait(db, action, job, result):
    """A task handed to someone: once the message is sent, the card waits for their answer. It
    closes when they reply (settle_awaiting) and comes back after wait_days if not."""
    if not action.get('delegate'):
        return
    row = db.execute('SELECT status FROM suggestions WHERE id=?', (job['suggestion_id'],)).fetchone()
    if not row or row['status'] != 'prepared':
        return
    if action['kind'] == 'slack':
        if not result.get('channel_id') or not result.get('user_id'):
            return
        watch = {'kind': 'slack.message', 'channel_id': result['channel_id'], 'user_id': result['user_id']}
    else:
        watch = {'kind': 'gmail.message', 'from': action['to'][0].lower(), 'thread_id': action.get('thread_id'), 'reply_to': job.get('rfc_message_id') or ''}
    watch.update(account_id=action['account_id'], since=now(), delegated=True, name=action.get('to_name') or action['to'][0])
    db.execute("UPDATE suggestions SET awaiting=?,status='snoozed',snoozed_until=?,resume_status='prepared',undo_until=NULL WHERE id=?",
               (encoded(watch), thread_return_time(action['wait_days']), job['suggestion_id']))


QUICK_RETRY_SECONDS = 15
QUICK_RETRY_MAX = 60  # a Retry-After longer than this waits in the checkpoint instead
SALESFLARE_RESTART_SPREAD = 180  # seconds: team Machines restarted together start their Salesflare rounds apart
SALESFLARE_ROUND_SPREAD = 60  # seconds: and a fresh spread each round, so two whose starts landed close drift apart again


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


VOICE_WARM_QUIET = 3   # 5-minute checks in a row that a live Machine is quiet before voice gets ready in the background


def fit_events(rows, offset=0, budget=REVIEW_PAGE_CHARS):
    """Full text where it fits; otherwise shorten bodies evenly and say how to read the rest."""
    preview = 40000
    views = [review_view(r, preview, offset) for r in rows]
    while len(encoded(views)) > budget and preview > 0:
        preview = int(preview * 0.7)
        views = [review_view(r, preview, offset) for r in rows]
    if len(encoded(views)) > budget:
        raise ValueError('Read fewer event_ids; metadata needs another page')
    return views


def event_page(rows, offset=0, row_offset=0, budget=REVIEW_PAGE_CHARS):
    """An explicit continuation, never a silently incomplete list of evidence."""
    if offset < 0 or row_offset < 0 or row_offset > len(rows):
        raise ValueError('Use a valid body_offset and row_offset')
    remaining = rows[row_offset:]
    # Metadata needs space too. Select a row page first, then give its bodies all
    # the remaining room. Continuation IDs freeze selection across new syncs.
    count = 0
    for count in range(1, len(remaining) + 1):
        skeleton = [review_view(r, 0, offset) for r in remaining[:count]]
        if len(encoded(skeleton)) > budget - 4000:
            count -= 1
            break
    selected = remaining[:count]
    result = {'events': fit_events(selected, offset, budget - 4000),
              'total': len(rows), 'row_offset': row_offset,
              'remaining_event_ids': [r['id'] for r in remaining[count:]],
              'next_row_offset': row_offset + count if count < len(remaining) else None}
    # All returned payloads, including JSON escaping and continuation, are bounded.
    if len(encoded(result)) > budget:
        raise ValueError('Request a smaller list of event_ids')
    return result


def metadata_page(row, offset):
    """Original metadata is evidence too; expose a bounded, lossless text continuation."""
    text = encoded(row['metadata'])
    if offset < 0 or offset > len(text):
        raise ValueError('Use a valid metadata_offset')
    length = min(20000, len(text) - offset)
    while True:
        result = {'id': row['id'], 'version': row['version'], 'metadata_text': text[offset:offset + length],
                  'metadata_chars': len(text), 'metadata_offset': offset,
                  'metadata_next_offset': offset + length if offset + length < len(text) else None}
        if len(encoded(result)) <= REVIEW_PAGE_CHARS:
            return result
        length = int(length * 0.7)

# The first profile on an install without the interactive installer (hosted): tries, and the wait between them.
FIRST_PROFILE_TRIES, FIRST_PROFILE_RETRY_SECONDS = 3, 6 * 3600
# A run that saved its result or blocker usually still writes its last reply: it gets this long to end by itself
# before it is stopped, so its record says how it ended (ok) instead of a stop's lost/aborted.
PREPARATION_SETTLE_SECONDS = 120


def first_cards_report(db, accounts=(), current=None):
    """How fast a new install got to its first useful card, for the hosted health report: per source when its first
    import was in, each first-look pass (start, end, status, reason, cards), when the first card was shown on the
    dashboard and when the owner first acted on one (and how). Timestamps, counts and codes only, never content. None
    on an install from before this was recorded. `db`: a plain sqlite3 connection to the events database."""
    rows = lambda sql, args=(): db.execute(sql, args).fetchall()
    if not rows("SELECT 1 FROM sqlite_master WHERE type='table' AND name='milestones'"):
        return None
    marks = {name: (at, detail) for name, at, detail in rows('SELECT name,at,detail FROM milestones')}
    since = (marks.get('tracking_since') or ('',))[0]
    current = current or dt.datetime.fromisoformat(now())
    out = {'since': since, 'sources': []}
    for account in accounts:
        if account.get('service') in SYSTEM_SERVICES:
            continue
        page, done = marks.get('first_page:' + account['id']), marks.get('first_import:' + account['id'])
        out['sources'].append({'service': str(account.get('service', 'gmail'))[:40], 'first_page_at': page and page[0], 'first_import_at': done and done[0]})
    # The first look: with reviews off, the auto previews; with reviews on, the quick first review and the regular
    # reviews up to the first that finished well (all from when this was recorded on)
    looks = rows("SELECT run_id,status,started_at,finished_at,error,window_hours,planned FROM review_runs WHERE preview=1 AND auto=1 "
                 "OR (preview=0 AND window_hours IS NOT NULL) ORDER BY started_at")
    regular = []
    for run in rows('SELECT run_id,status,started_at,finished_at,error,window_hours,planned FROM review_runs WHERE preview=0 AND window_hours IS NULL '
                    'AND started_at>=? ORDER BY started_at', (since,)):
        regular.append(run)
        if run[1] == 'ok':
            break
    runs = sorted(looks + regular, key=lambda r: r[2])
    for name, part in (('quick', [r for r in runs if r[5]]), ('full', [r for r in runs if not r[5]])):
        if not part:
            continue
        cards = sum(rows('SELECT count(*) FROM suggestions WHERE created_at>=? AND created_at<=?', (r[2], r[3] or current.isoformat()))[0][0] for r in part)
        out[name] = {'started_at': part[0][2], 'finished_at': part[-1][3], 'status': part[-1][1], 'reason': part[-1][4],
                     'tries': len(part), 'planned': part[-1][6], 'cards': cards}
    if marks.get('first_dig_done'):
        out['dig'] = marks['first_dig_done'][1]  # why the first review stopped digging: cards, covered or usage (App.first_dig)
    first = rows('SELECT min(created_at),count(*) FROM suggestions')[0]
    out['cards'] = first[1]
    out['first_card_at'] = first[0] if first[0] and first[0] >= since else None
    shown = marks.get('first_card_shown')
    out['first_card_shown_at'] = shown and shown[0]
    acted = rows("SELECT choice,created_at FROM decisions WHERE source IN ('dashboard','telegram') AND created_at>=? AND choice IN ("
                 + ','.join('?' for _ in FIRST_ACTIONS) + ') ORDER BY created_at LIMIT 1', (since, *FIRST_ACTIONS))
    out['first_action_at'], out['first_action'] = (acted[0][1], FIRST_ACTIONS[acted[0][0]]) if acted else (None, None)
    # The first approved one (Do it, Send, Mark done): a Not needed before it doesn't count as getting something done
    approved = [c for c, a in FIRST_ACTIONS.items() if a != 'dismiss']
    acted = rows("SELECT choice,created_at FROM decisions WHERE source IN ('dashboard','telegram') AND created_at>=? AND choice IN ("
                 + ','.join('?' for _ in approved) + ') ORDER BY created_at LIMIT 1', (since, *approved))
    out['first_approved_at'], out['first_approved'] = (acted[0][1], FIRST_ACTIONS[acted[0][0]]) if acted else (None, None)
    out.update(first_value(db, marks, since))
    # Where the first look is now, and about when the first cards come
    try:
        state = json.loads((marks.get('first_look_state') or (None, 'null'))[1] or 'null')
    except ValueError:
        state = None
    active = next((r for r in reversed(runs) if r[1] in ('starting', 'running', 'recovering')), None)
    eta = None
    if active:
        done = sum(len(json.loads(items)) for (items,) in rows("SELECT items FROM analyses WHERE owner_run=? AND status='complete'", (active[0],)))
        out['look'] = {'state': 'running', 'quick': bool(active[5]), 'done': done, 'planned': active[6] or 0}
        eta = first_eta_minutes({'planned': active[6] or 0, 'done': done}, None, None, current)
    elif state:
        out['look'] = {k: state.get(k) for k in ('state', 'why', 'quick', 'waiting', 'retry_at')}
        eta = first_eta_minutes(None, state, None, current)
    if eta and not out['cards']:
        out['eta_minutes'] = eta
    return out


def activity_report(db, timezone=None, current=None):
    """Per local day, the last 7 days: plain counts of what the owner did (to-dos shown and opened, Do it, Send,
    sent, Mark done, Not needed, snoozed, chat messages, visits, active hours), for the hosted health report next to
    first_cards_report. Counts only, never content (activity.py). `db`: a plain sqlite3 connection to the events database."""
    try:
        tz = ZoneInfo(timezone) if timezone else local_tz()
    except (ValueError, KeyError):
        tz = local_tz()
    return activity.report(db, tz, current or now())


VERIFIED_DECISION_SOURCES = ('telegram', 'dashboard')


# Settings the app takes from config.json while it runs (App.follow_config), so turning reviews on needs no restart:
# the hosting agent's reviews on restarted the app 44 s into a first look (2026-11-04). The hosting agent checks this
# list before it restarts the app for them.
LIVE_CONFIG = ('delivery_enabled', 'review_worker')
# Background turns beyond the first look (profile, voices, roles, organizations) start at most one per this many
# seconds, and only once the first card was shown, so the first cards come first and a new install's usage is spread
# out instead of spent in its first minutes. A draft prepared ahead is on the owner's board as Preparing, so it doesn't
# wait for this gap (2026-10-29: one waited 8 minutes behind a review's start); the usage budget still holds it.
BACKGROUND_GAP_SECONDS = 600

PROFILE_SECONDS = 900
SKILL_NOTES_MIN = 5   # notes about one kind of task before they're offered as a skill
SKILL_REGROW = 3      # after Not now, offered again only once this many more notes joined them


# Contact photos from the owner's Google contacts and Workspace directory, with the scopes the gog sign-in already has
# (a hosted sign-in through the broker has no Contacts scope, so it is never asked). Read only, once a day per account.
GOOGLE_PHOTO_LISTS = (
    ('people.connections.list', {'resourceName': 'people/me', 'pageSize': 1000, 'personFields': 'emailAddresses,phoneNumbers,photos,organizations'},
     'https://www.googleapis.com/auth/contacts', 'connections'),
    ('people.listDirectoryPeople', {'pageSize': 1000, 'readMask': 'emailAddresses,phoneNumbers,photos,organizations', 'sources': 'DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'},
     'https://www.googleapis.com/auth/directory.readonly', 'people'),
    ('otherContacts.list', {'pageSize': 1000, 'readMask': 'emailAddresses,phoneNumbers,photos'},
     'https://www.googleapis.com/auth/contacts.other.readonly', 'otherContacts'))
GOOGLE_PHOTO_PAGES = 20


def google_photo_offers(config, account, read=None, facts=None):
    """(identifiers, link, chosen) for each of the account's contacts with a real photo. A list the sign-in can't read
    is skipped. With a list as `facts`, their job title, company and phone from the same pages go there too."""
    read = read or gog_read
    offers = []
    for method, params, scope, key in GOOGLE_PHOTO_LISTS:
        token = None
        for _ in range(GOOGLE_PHOTO_PAGES):
            try:
                page = read(config, account, 'people', 'v1', method, {**params, **({'pageToken': token} if token else {})}, scope)
            except SourceError:
                break
            offers += [o for o in (enrichment.google_photo(p) for p in page.get(key) or [] if isinstance(p, dict)) if o]
            if facts is not None:
                facts += [f for p in page.get(key) or [] if isinstance(p, dict) for f in enrichment.google_facts(p)]
            token = page.get('nextPageToken')
            if not token:
                break
    return offers


def google_photo_accounts(config):
    """The owner's own Google sign-ins through gog, once per address (never one shared from a Fleet)."""
    seen = {}
    for account in config.get('accounts', []):
        if account.get('service', 'gmail') in ('gmail', 'calendar') and account.get('transport') == 'gog' and account.get('email') \
                and not account.get('shared'):
            seen.setdefault(account['email'].lower(), account)
    return list(seen.values())


class Store(CardsStore, DecisionsStore, EventsStore, FactsStore, FaultsStore, FirstLookStore, ProfileStore,
            PromisesStore, MachineCardsStore, ReviewStore, StoreCore, ViewsStore, VoicesStore):
    """The service's database: every table, through the Store mixins it is made of (machine/store/*)."""


def sync_slack(store, config, account, source=None):
    source = source or Slack(config, account)
    source.profile()
    state = store.checkpoint(account['id']) or {}
    if not state:
        state = {'mode': 'bootstrap', 'phase': 'discover', 'channels': [],
                 'after': f'{time.time() - config.get("bootstrap_days", 7) * 86400:.6f}'}
        store.commit_page(account['id'], state, [], record_sync=False)
    if state['phase'] == 'discover':
        params = {'user': account['user_id'], 'types': 'public_channel,private_channel,im,mpim',
                  'exclude_archived': 'true', 'limit': 100}
        if state.get('page_token'):
            params['cursor'] = state['page_token']
        try:
            page = source.get('users.conversations', params)
        except SourceError as error:
            if slack_error(error) == 'slack_invalid_cursor':
                state.pop('page_token', None)
                store.commit_page(account['id'], state, [], record_sync=False)
            raise
        channels = {c['id']: c for c in state['channels']}
        for c in page.get('channels', []):
            if c.get('is_archived'):
                continue
            # users.conversations is scoped to actual membership. Never join or open DMs.
            kind = 'dm' if c.get('is_im') else 'group' if c.get('is_mpim') else 'channel'
            channels.setdefault(c['id'], {'id': c['id'], 'name': c.get('name') or
                ('My notes' if c.get('user') == account['user_id'] else 'DM ' + c.get('user', c['id'])),
                'type': kind, 'threads': []})
            # Slack Connect: shared with another company. Everything else is the company's own Slack, among colleagues.
            if c.get('is_ext_shared') or c.get('is_pending_ext_shared'):
                channels[c['id']]['external'] = True
            else:
                channels[c['id']].pop('external', None)
        state['channels'] = list(channels.values())
        cursor = page.get('response_metadata', {}).get('next_cursor')
        if cursor:
            state['page_token'] = cursor
        else:
            state.pop('page_token', None)
            state['next_discovery'] = time.time() + 86400
            if state['mode'] == 'bootstrap' and 'index' not in state:
                # First import: a cheap look at every conversation first, so the read order follows activity.
                state.update(phase='triage', triage=0)
            else:
                slack_order(state['channels'])
                state.update(phase='scan', index=0)
        store.commit_page(account['id'], state, [])
        return {'mode': state['mode'], 'events': 0, 'more': True}

    if (state['mode'] == 'bootstrap' and state['phase'] == 'scan' and 'step' not in state and not state.get('scan')
            and state.get('channels') and isinstance(source, Slack)):
        # A first import begun in the old name order: the rest of it follows activity. Conversations already read
        # stay read.
        state.update(phase='triage', triage=0)
        store.commit_page(account['id'], state, [], record_sync=False)

    if state['phase'] == 'triage':
        # conversations.info isn't held to Slack's one-read-a-minute limit. A direct message shows its newest
        # message; a channel or group only when you last read it, which stands in for its activity.
        for _ in range(10):
            if state['triage'] >= len(state['channels']):
                break
            channel = state['channels'][state['triage']]
            try:
                info = source.get('conversations.info', {'channel': channel['id']}).get('channel') or {}
            except SourceError as error:
                if slack_error(error) not in ('slack_channel_not_found', 'slack_not_in_channel', 'slack_missing_scope'):
                    store.commit_page(account['id'], state, [], record_sync=False)
                    raise
                info = {}
            latest = info.get('latest') if isinstance(info.get('latest'), dict) else {}
            mark = latest.get('ts') if channel['type'] == 'dm' else info.get('last_read')
            try:
                channel['hint'] = float(mark or 0)
            except (TypeError, ValueError):
                channel['hint'] = 0.0
            state['triage'] += 1
        if state['triage'] >= len(state['channels']):
            slack_first_import_plan(config, state)
        store.commit_page(account['id'], state, [], record_sync=False)
        return {'mode': state['mode'], 'events': 0, 'more': True}

    if not state['channels']:
        state.update(mode='incremental', phase='discover')
        store.commit_page(account['id'], state, [], record_sync=False)
        return {'mode': 'incremental', 'events': 0, 'more': False}
    if state['mode'] == 'incremental' and not state.get('scan') and not slack_next_due(store, config, account, source, state):
        return {'mode': 'incremental', 'events': 0, 'more': False}
    channel = state['channels'][state['index']]
    scan = state.get('scan')
    if not scan:
        # Six-hour overlap catches recent edits; daily retained-window replay catches older
        # edits and thread metadata. No timestamp advances before every page commits.
        full = not channel.get('last_scan') or time.time() >= channel.get('next_full', 0)
        # The retained window rolls forward; state['after'] (first install) only bounds it.
        retained = max(Decimal(state['after']),
                       Decimal(f'{time.time() - config.get("bootstrap_days", 7) * 86400:.6f}'))
        oldest = str(retained) if full else str(max(retained, Decimal(channel['last_scan']) - Decimal(21600)))
        latest = f'{time.time():.6f}'
        step = state.get('step')
        if step == 'recent':
            # First import, active conversations: the last day first; the rest of the window comes after.
            oldest, full = str(max(retained, Decimal(f'{time.time() - 86400:.6f}'))), False
            deepen_to = oldest if Decimal(oldest) > retained else None
        elif step == 'deepen' and channel.get('deepen'):
            oldest, latest = str(retained), channel['deepen']
        # Known threads are polled for late replies only while reasonably recent; the
        # list otherwise grows forever and is rewritten on every page commit.
        horizon = time.time() - config.get('slack_thread_retention_days', 30) * 86400
        channel['threads'] = [ts for ts in channel.get('threads', []) if float(ts) >= horizon]
        scan = {'oldest': oldest, 'latest': latest, 'phase': 'history',
                'thread_index': 0, 'threads': list(channel.get('threads', [])), 'full': full}
        if step:
            scan['step'] = step
            if step == 'recent' and deepen_to:
                scan['deepen_to'] = deepen_to
        if channel.get('threads_waiting'):
            # Threads left for later on the first pass: read them now over the whole window.
            scan.update(thread_oldest=str(retained), thread_latest=f'{time.time():.6f}')
        elif account.get('fair_incremental') and channel.get('last_scan') and not step:
            # One old thread per channel turn, not its entire retained history.
            # Preserve all known threads and rotate durably on completed scans.
            scan['known_threads'] = list(scan['threads'])
            scan['thread_start'] = channel.get('next_thread_index',0)
            scan['threads'] = []
        state['scan'] = scan
        store.commit_page(account['id'], state, [], record_sync=False)
    params = {'channel': channel['id'], 'oldest': scan['oldest'], 'latest': scan['latest'],
              'inclusive': 'true', 'limit': 15}
    if scan['phase'] == 'threads':
        params['ts'] = scan['threads'][scan['thread_index']]
        if scan.get('thread_oldest'):
            params.update(oldest=scan['thread_oldest'],latest=scan['thread_latest'])
    if scan.get('cursor'):
        params['cursor'] = scan['cursor']
    try:
        page = source.get('conversations.history' if scan['phase'] == 'history' else 'conversations.replies', params)
    except SourceError as error:
        if (account.get('fair_incremental') and 'known_threads' in scan and
                scan['phase']=='threads' and error.category.startswith('network:')):
            # Save the failed frozen thread page, then let other conversations
            # progress. A repeated timeout cannot starve new channel messages.
            channel['deferred_thread'] = {'ts':params['ts'],'oldest':params['oldest'],'latest':params['latest'],
                                          'retry_at':time.time()+600, 'error':str(error)}
            if scan.get('cursor'):
                channel['deferred_thread']['cursor'] = scan['cursor']
            channel.update(last_scan=scan['latest'],threads=scan['known_threads'],
                           next_thread_index=scan['thread_start']+1)
            state.pop('scan',None)
            state['index']=(state['index']+1)%len(state['channels'])
            store.commit_page(account['id'],state,[],record_sync=False)
            error.retry_after = 65
        elif slack_error(error) == 'slack_invalid_cursor':
            scan.pop('cursor', None)
            store.commit_page(account['id'], state, [], record_sync=False)
        elif slack_error(error) in ('slack_thread_not_found', 'slack_channel_not_found', 'slack_not_in_channel'):
            # Keep a visible failure; don't silently mark a partial inaccessible channel complete.
            channel['error'] = slack_error(error)
            state.pop('scan', None)
            if state.get('step'):
                state['index'] += 1
                slack_first_import_next(state)
            else:
                state['index'] = (state['index'] + 1) % len(state['channels'])
            store.commit_page(account['id'], state, [], record_sync=False)
        raise
    names = slack_page_names(store, channel, page.get('messages', []))
    skipped = Skips('slack_invalid_message')  # a message it can't take is counted, never failing the channel's page
    def one(raw):
        if raw.get('subtype') == 'message_deleted':
            return store.tombstone(account['id'], channel['id'] + ':' + raw['deleted_ts'])
        e = slack_event(account, channel, raw, names)
        ts = e['metadata']['message_ts']
        channel['last_activity'] = max(float(channel.get('last_activity') or 0), float(ts))
        if e['metadata']['reply_count'] and ts not in scan['threads']:
            scan['threads'].append(ts)
            if 'known_threads' in scan and ts not in scan['known_threads']:
                scan['known_threads'].append(ts)
        return e
    events = [e for e, _ in skipped.every(page.get('messages', []), one) if e]
    cursor = page.get('response_metadata', {}).get('next_cursor')
    if cursor:
        scan['cursor'] = cursor
    elif page.get('has_more'):
        raise SourceError('slack_missing_cursor')
    else:
        scan.pop('cursor', None)
        if scan['phase'] == 'history':
            scan['phase'] = 'threads'
            if state['mode'] == 'bootstrap' and len(state['channels']) > 1 and scan['threads']:
                # First pass: every conversation's own messages before any thread replies. Slack
                # allows about one read a minute, so one busy channel's threads would otherwise
                # hold up all the others for hours. The next turn of this channel reads them.
                scan['waiting'], scan['threads'] = scan['threads'], []
            elif 'known_threads' in scan:
                known = scan['known_threads']
                selected = scan['threads'][:1]
                if not selected and known:
                    selected = [known[scan['thread_start'] % len(known)]]
                postponed = channel.get('deferred_thread')
                if postponed and time.time() < postponed['retry_at']:
                    selected = []
                if postponed and time.time() >= postponed['retry_at']:
                    scan['threads'] = [postponed['ts']]
                    scan['thread_oldest'], scan['thread_latest'] = postponed['oldest'], postponed['latest']
                    if postponed.get('cursor'):
                        scan['cursor'] = postponed['cursor']
                    selected = scan['threads']
                scan['threads'] = selected
        else:
            scan['thread_index'] += 1
            postponed = channel.get('deferred_thread')
            if postponed and params.get('ts') == postponed['ts']:
                channel.pop('deferred_thread',None)
        if scan['thread_index'] >= len(scan['threads']):
            if scan.get('step') == 'deepen' and channel.get('deepen'):
                # The older part of the window: the newest read (last_scan) stays where it was.
                channel.pop('deepen')
                channel['threads'] = list(dict.fromkeys(channel.get('threads', []) + scan['threads'] + scan.get('waiting', [])))
            else:
                channel.update(last_scan=scan['latest'], threads=scan.get('known_threads', scan['threads'] + scan.get('waiting', [])))
                if scan.get('deepen_to'):
                    channel['deepen'] = scan['deepen_to']
            if scan.get('waiting'):
                channel['threads_waiting'] = True
            else:
                channel.pop('threads_waiting', None)
            if 'known_threads' in scan:
                channel['next_thread_index'] = scan['thread_start'] + 1
            channel.pop('error', None)
            # Thread replies held back on the first pass are read on the very next round.
            channel['due'] = time.time() + (0 if scan.get('waiting') else slack_interval(config, channel))
            if scan['full']:
                channel['next_full'] = time.time() + 86400
            state.pop('scan', None)
            state['index'] += 1
            if state.get('step'):
                slack_first_import_next(state)
            elif state['index'] >= len(state['channels']):
                state.update(index=0, mode='incremental')
                if time.time() >= state.get('next_discovery', 0):
                    state['phase'] = 'discover'
    if not state.get('titles_named'):  # once: titles stored before members were named in them
        name_slack_titles(store, account['id'])
        state['titles_named'] = True
    skipped.check().note(state)
    store.commit_page(account['id'], state, events)
    if isinstance(source, Slack):
        remember_slack_names(store, source, events, state.get('channels') or ())
    more = state['mode'] != 'incremental' or state['index'] != 0 or bool(state.get('scan'))
    return {'mode': state['mode'], 'events': len(events), 'more': more, 'skipped': sum(skipped.values())}


def name_slack_titles(store, account_id, ids=None):
    """Writes stored Slack titles again with people's names in place of member ids ("#DM U02AB3CD4: hi" becomes
    "#DM Sam Lee: hi"): all of them, or those of the messages with these members (a name just learned). The content
    hash stays (slack_raw_title): no message looks new or edited for it."""
    changed = 0
    with store.connect() as db:
        rows = db.execute("SELECT id,title,body,metadata FROM events WHERE kind='slack.message' AND account_id=? AND deleted=0", (account_id,)).fetchall()
        found = []
        for r in rows:
            m = json.loads(r['metadata'] or '{}')
            on = set(graph.slack_members_on(m)) | {x[0] for x in graph.SLACK_MENTION.findall(str(r['body'] or ''))}
            if ids is not None and not on & set(ids):
                continue
            if not graph.slack_title_unnamed(r['title']):
                continue
            found.append((r, m, on))
        names = graph.slack_names(db, {u for _, _, on in found for u in on})
        seal = store.sealer.seal if store.protected else (lambda value: value)
        for r, m, _ in found:
            title = graph.slack_title(m.get('channel_name'), html.unescape(str(r['body'] or '')), names)
            if title != r['title']:
                db.execute('UPDATE events SET title=? WHERE id=?', (seal(title), r['id']))
                changed += 1
    return changed


def remember_slack_names(store, source, events, channels=(), per_page=3):
    """Names and emails for the people graph: Slack messages carry only user IDs. A few lookups per
    page (new senders, people they mention, then the people behind known DMs), each once a month; the email joins the
    person to their mail. Whether each is outside the company's own Slack (another company's member through Slack
    Connect, or a guest) is kept too (slack_members): shared_graph.visibility shares on it. Titles with a member's id
    are written again with the name once it is known. Best effort."""
    users = {e['metadata'].get('user_id') for e in events} | {
        m[0] for e in events for m in graph.SLACK_MENTION.findall(str(e.get('body') or ''))} | {
        m[1] for name in [e['metadata'].get('channel_name') for e in events] + [c.get('name') for c in channels]
        for m in [re.fullmatch(r'DM ([UW][A-Z0-9]+)', name or '')] if m}
    owner = source.account.get('user_id')
    users = {u for u in users if u}
    with store.connect() as db:
        known = graph.slack_members_known(db, users)
    wanted = sorted(set(store.names_to_check(['slack:' + u for u in users - {owner}])) | {'slack:' + u for u in users - known})
    named = []
    for identifier in wanted[:per_page]:
        member = identifier.split(':', 1)[1]
        try:
            user = source.get('users.info', {'user': member}).get('user', {})
        except SourceError as error:
            if not str(error).startswith(('slack_user_not_found', 'slack_user_not_visible')):
                return  # away, or Slack's limit: the rest next page
            user = {'id': member, 'deleted': True}  # an account Slack no longer has
        profile = user.get('profile') or {}
        shown = (profile.get('real_name') or profile.get('display_name') or user.get('real_name')
                 or profile.get('real_name_normalized') or profile.get('display_name_normalized') or user.get('name'))
        person = not user.get('is_bot') and member != owner and not user.get('deleted')
        email = str(profile.get('email') or '').lower()[:320] or None
        if member != owner:  # a person's name and email for the people graph (an app: none, checked once a month)
            real = None if user.get('is_bot') else (profile.get('real_name') or profile.get('display_name') or user.get('real_name'))
            store.remember_name(identifier, real and str(real)[:200], None if user.get('is_bot') else email)
        # who is no person in the graph still has a name to show: an app by its name, the owner as themselves, someone
        # whose account is gone by the name it had, else "a former Slack user"
        label = None if person else (shown or (graph.FORMER_SLACK_USER if user.get('deleted') else None))
        team = source.account.get('team_id')
        outside = bool(user.get('is_stranger') or user.get('is_restricted') or user.get('is_ultra_restricted')
                       or (team and user.get('team_id') and user['team_id'] != team))
        with store.connect() as db:
            graph.remember_slack_member(db, member, outside, now(), label)
        if shown or label:
            named.append(member)
        if member == owner or (user.get('deleted') and not profile):
            continue  # the owner's own picture and facts aren't a contact's
        user = {**user, 'id': user.get('id') or member}
        offer, facts = enrichment.slack_photo(user), enrichment.slack_facts(user)
        if offer or facts:
            with store.connect() as db:
                enrichment.offer_photos(db, [offer], 'slack', now(), known_only=False) if offer else None
                enrichment.offer_facts(db, [facts], 'slack', now()) if facts else None
    if named and source.account.get('id'):
        name_slack_titles(store, source.account['id'], named)




SYNC_LOCKS, SYNC_LOCKS_LOCK = {}, threading.Lock()


def sync_source(store, config, account):
    service = account.get('service', 'gmail')
    if service in MAIL_SERVICES:
        return sync_gmail(store, config, account)
    if service in CALENDAR_SERVICES:
        return sync_calendar(store, config, account)
    if service == 'slack':
        return sync_slack(store, config, account)
    if service == 'whatsapp':
        return sync_whatsapp(store, config, account)
    if service == 'telegram':
        return sync_telegram(store, config, account)
    if service == 'salesflare':
        return sync_salesflare(store, config, account)
    if service == 'gateway':
        return sync_gateway(store, config, account)
    if service == 'android':
        return sync_android_preferred(store, config, account) if account['transport'] == 'openclaw-feed' else sync_android(store, config, account)
    plugin = load_connector(service)
    if plugin is None:
        raise SourceError('unsupported_service')
    return plugin.sync(store, config, account, CONNECTOR_HELPERS)


def owner_card_area(db, accounts, node_ids=(), text=''):
    """Where a to-do the owner adds without an area goes: (account id, open: the area ids to place it in later). Its
    only area when they have one; else the area its people and organizations point to (todo_areas.pointed: their side,
    the accounts they were heard on, their organization's domain), the people its words name by address among them;
    else the area its words point to (todo_areas.mentioned: a company or one of its mailboxes). Else, open, the area most
    of their recent to-dos are in (todo_areas.most_used, or their first connection's), until the review places it by
    meaning. Never the Machine's own source (the Gateway log, in no area) while an area exists. A mail account of the
    area first, the one its runs search and send from."""
    found = todo_areas.areas(accounts)
    if not found:
        return accounts[0]['id'], []
    pick = found[0]['id'] if len(found) == 1 else None
    free = lambda value: (lambda d: '' if d in graph.FREEMAIL else d)(own_addresses.email_domain(value))
    if pick is None:
        mails = todo_areas.addresses(text)
        try:
            people, rows = [], []
            select = "SELECT n.kind,n.info,o.info org_info FROM graph_nodes n LEFT JOIN graph_nodes o ON o.id=json_extract(n.info,'$.org') "
            if node_ids:
                rows += db.execute(select + f"WHERE n.id IN ({','.join('?' for _ in node_ids)}) AND n.kind IN ('person','org')", list(node_ids)).fetchall()
            if mails:
                rows += db.execute(select + f"WHERE n.kind='person' AND EXISTS (SELECT 1 FROM json_each(n.info,'$.emails') e WHERE lower(e.value) IN "
                                   f"({','.join('?' for _ in mails)}))", mails).fetchall()
            for r in rows:
                info, org = json.loads(r['info'] or '{}'), json.loads(r['org_info'] or '{}')
                people.append({'side': info.get('side'), 'accounts': info.get('accounts') or [],
                               'org_domain': info.get('domain') if r['kind'] == 'org' else org.get('domain')})
        except (sqlite3.Error, ValueError, TypeError):
            people = []
        pick = (todo_areas.pointed(people, accounts, None, free) if people else None) or todo_areas.mentioned(text, accounts, free)
    open_ = [f['id'] for f in found] if pick is None else []
    if open_:
        try:
            since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).isoformat()
            recent = db.execute('SELECT account_ids,area FROM suggestions WHERE created_at>=? ORDER BY created_at DESC LIMIT 500', (since,)).fetchall()
        except sqlite3.Error:
            recent = []
        pick = todo_areas.most_used([(r['account_ids'], r['area']) for r in recent], accounts) or next(
            x for x in (todo_areas.area_of_account(a) for a in accounts) if x in {f['id'] for f in found})
    ids = todo_areas.accounts_in(pick, accounts)
    services = {a['id']: a.get('service', 'gmail') for a in accounts}
    return next((i for i in ids if services[i] in MAIL_SERVICES), ids[0]), open_


SOURCE_KIND['fleet.request'] = 'Fleet'
SOURCE_KIND['fleet.email'] = 'email'  # a copy a teammate's handoff carried (fleet_requests.handoff_sources)
SOURCE_KIND['owner.card'] = 'note'  # a card the owner made themselves (New card): their own words
SOURCE_KIND['fleet.message'] = 'message'
SOURCE_KIND['fleet.intercom'] = 'Intercom'  # an Intercom conversation a handoff carried, on a Machine that doesn't read it



MAIL_SERVICES, CALENDAR_SERVICES = ('gmail', 'outlook'), ('calendar', 'outlook_calendar')




def active_work(db):
    """Work a restart or an update would cut off: agent jobs that run, sends under way, confirmed steps being worked on
    and preparations that started. Paused steps, blocked or queued preparations and finished work are not in it."""
    found = {}
    for name, sql, args in (
            ('agent_jobs', 'SELECT id,suggestion_id,status FROM agent_jobs WHERE status IN (%s)', agent_jobs.ACTIVE),
            ('action_jobs', 'SELECT id,suggestion_id,status FROM action_jobs WHERE status IN (%s)', ACTION_WORKING),
            ('preparations', 'SELECT job_id id,suggestion_id,status FROM preparations WHERE status IN (%s)', PREPARATION_WORKING)):
        try:
            rows = db.execute(sql % ','.join('?' for _ in args), args).fetchall()
        except sqlite3.OperationalError:  # a table this install doesn't have yet
            rows = []
        found[name] = [dict(zip(('id', 'suggestion_id', 'status'), tuple(r))) for r in rows]
    found['agent_jobs'] = agent_jobs.working(db, found['agent_jobs'])  # nor jobs whose worker is gone
    return found


def agent_messages(views):
    """The card's source messages as card/messages.md for a coding agent: who, to whom, when, and the full text, so
    it needs no mailbox of its own. The link goes last, as a reference."""
    out = []
    for v in views:
        head = [f"## {v.get('title') or v.get('kind') or 'Message'}", f"From: {v.get('from') or 'unknown'}"]
        head += [f'{k}: {v[k.lower()]}' for k in ('To', 'Cc') if v.get(k.lower())]
        head.append(f"When: {v.get('occurred_at') or ''}")
        body = str(v.get('body') or '').strip() or '(no text)'
        out.append('\n'.join(head) + '\n\n' + body + ('\n\n(Cut short here: the rest is in the original.)' if v.get('clipped') else '')
                   + (f"\n\nOriginal: {v['url']}" if v.get('url') else ''))
    return '\n\n'.join(out)


def agent_about(card, views):
    """Who and what a card is about, in plain lines: the people who wrote, the source, the due date."""
    people = list(dict.fromkeys(str(v.get('from') or '').strip() for v in views if v.get('from') and v.get('from') != 'You'))[:3]
    lines = [f"With: {', '.join(people)}" + (f" ({views[0]['kind']})" if views and views[0].get('kind') else '')] if people else []
    if card.get('source_line'):
        lines.append(str(card['source_line']).strip())
    if card.get('due'):
        lines.append(f"Due: {card['due']}")
    return lines


def agent_history(owner, results, skip='', keep=6):
    """The card's chat so far, as short background lines, newest last: what the owner asked and what came back. The
    owner's latest note is skipped (it goes in the brief word for word)."""
    turns = [(i['at'], 'I asked', i['text']) for i in owner if i.get('kind') == 'you' and i.get('via') != 'agent']
    turns += [(i['at'], f"{i.get('name') or 'The agent'} answered", i['text']) for i in owner if i.get('kind') == 'agent']
    turns += [(r['at'], 'The Machine answered', r['text']) for replies in results.values() for r in replies if r.get('kind') == 'reply']
    skip = ' '.join(str(skip or '').split())
    lines = [f'{who}: {agent_jobs.gist(text, 400)}' for at, who, text in sorted(turns, key=lambda t: t[0] or 0)
             if str(text or '').strip() and ' '.join(str(text).split()) != skip]
    return lines[-keep:]


def prompt_text(title,plain=False,kind='change'):
    t = i18n.t  # “cancel” stays the word the reply handler takes, in every language
    if kind=='dismiss':
        if plain:return t('Why isn’t this needed? Reply to this message. Send “cancel” to keep it.')
        return t('Not needed: {}', title[:90])+'\n\n'+t('Why isn’t this needed? Reply here, or send “cancel” to keep it.')
    if plain:return t('What would you like instead? Reply to this message. Send “cancel” to stop.')
    return t('Change: {}', title[:90])+'\n\n'+t('What would you like instead? Reply here, or send “cancel”.')




def weekly_recap(store, config, current=None):
    """The recap as the owner reads it on Telegram, its messages one after the other (without storing its choices)."""
    recap = weekly_recap_message(store, config, current)
    note = ['_' + i18n.t(RECAP_CHOICES_NOTE) + '_'] if recap['items'] else []
    return '\n\n'.join([recap['text'], *note, *(i['line'] for i in recap['items'])])




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
              WhatsAppImagesApp, CheckNowApp, SetupCardApp, HistoryApp)

# App's mixins in machine/app/: methods moved out of App as is (docs/code-map.md)
APP_MIXINS += (FollowUpsApp, GraphActionsApp, KnowledgeExportApp, MeetingWritesApp, ModelPacingApp, PromiseChecksApp, SignaturesApp, SummariesApp,
               VoiceApp)
APP_MIXINS += (CardChatApp, ConversationApp, ExportApp, FirstLookApp, FleetApp, PreparationApp, RecapApp, ReviewApp, TalkApp)
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

    @functools.cached_property
    def task_pages(self):
        """Pages for tasks handed off by email (task_pages.py)."""
        return task_pages.TaskPages(self)

    @functools.cached_property
    def handoff_mail(self):
        """Handoffs by email to a colleague who isn't on The Machine (handoff_mail.py)."""
        return handoff_mail.HandoffMail(self, handoff_checkin, promise_check_at)

    def handoff_mail_draft(self, card_id, body, next_action, outcome):
        """The handoff email, ready on the to-do for the owner to read and send (a pending to-do counts as accepted)."""
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=? AND status='pending'", (card_id,))
        self.store.prepare(card_id, body, next_action=next_action, outcome=outcome)

    def handoff_mail_wait(self, db, card_id, until):
        """A handoff email went out: the to-do waits under Later until its check-in, then comes back as it was."""
        db.execute("UPDATE suggestions SET status='snoozed',snoozed_until=?,resume_status='prepared',outcome=NULL,undo_until=NULL WHERE id=?",
                   (until, card_id))

    def handoff_mail_promise(self, db, card_id, event_ids, who, what, due, check_at, event):
        """Their promise to take on a to-do handed off by email, from the sent email (watch NULL: only the review closes it
        by meaning, or the to-do). The to-do then holds that email, so it is the promise's home. Returns its id."""
        stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
        cursor = db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,watch,status,created_at,updated_at) "
                            "VALUES('theirs',?,?,?,?,?,?,NULL,'open',?,?) ON CONFLICT(event_id,direction,who,what) DO NOTHING",
                            (who, what, due, check_at, event['id'], event['account_id'], stamp, stamp))
        if event['id'] not in event_ids:
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([*event_ids, event['id']]), card_id))
        return cursor.lastrowid or None

    def email_handoff_round(self):
        """In the Fleet's round: answers from task pages, then handoffs by email (take links, promises, moves)."""
        try:
            self.task_pages.round()
        finally:
            self.handoff_mail.round()

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

    def stop_all(self):
        self.stop.set()
        for wake in list(getattr(self, 'collector_wakes', {}).values()):
            wake.set()  # a collector resting till its next read stops now too
        if self.__dict__.get('fleet_stop') is not None:
            self.fleet_stop.set()

    MESSAGE_CACHE = 40  # source emails kept in memory for the dashboard, newest used last
    MESSAGE_TTL = 600  # seconds

    def gmail_message(self, account_id, message_id):
        """One source email, read live (read-only). Opening it on the dashboard reads it for its attachments, its
        HTML and each embedded image, and visible cards read it ahead, so a few recent ones stay in memory for
        MESSAGE_TTL; one read at a time per message."""
        account = next(a for a in self.config['accounts'] if a['id'] == account_id)
        cache = self.__dict__.setdefault('_messages', collections.OrderedDict())
        locks = self.__dict__.setdefault('_message_locks', collections.defaultdict(threading.Lock))
        key = (account_id, message_id)
        with locks[key]:
            hit = cache.get(key)
            if hit and time.monotonic() - hit[0] < self.MESSAGE_TTL:
                cache.move_to_end(key)
                return account, hit[1]
            message = gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.get',
                               {'userId': 'me', 'id': message_id, 'format': 'full'}, 'https://www.googleapis.com/auth/gmail.readonly')
            cache[key] = (time.monotonic(), message)
            cache.move_to_end(key)
            while len(cache) > self.MESSAGE_CACHE:
                cache.popitem(last=False)
        if len(locks) > 4 * self.MESSAGE_CACHE:
            locks.clear()  # at worst one message is read twice
        return account, message

    MAILBOX_LOOKUP_MAX = 10  # messages per mailbox one search keeps

    def mailbox_lookup(self, account_ids, query, limit=5):
        """Search the owner's own mailboxes themselves (Gmail's search, Outlook's), read-only, for mail older than what
        is collected: a mail they sent weeks ago that a to-do follows up on. What it finds is kept as collected signals
        (Store.keep_found: reviewed, so it is context, not news) for the run to read and link. Only the mail accounts
        among account_ids, never one shared from a Fleet. Returns (event ids, {account id: error category})."""
        query = ' '.join(str(query or '').split())[:200]
        if not query:
            raise ValueError('mailbox_search needs a query: Gmail search words, such as from:sam subject:pricing in:sent')
        limit = max(1, min(int(limit or 5), self.MAILBOX_LOOKUP_MAX))
        found, failed = [], {}
        for account in self.config.get('accounts', []):
            if account['id'] not in account_ids or account.get('service', 'gmail') not in MAIL_SERVICES or account.get('shared'):
                continue
            source = Gmail(self.config, account)
            try:
                source.profile()  # fail closed on account routing, as a sync does
                refs = source.get('messages', {'q': query, 'maxResults': limit}).get('messages') or []
                events = [e for e in (message_event(account, source.get('messages/' + r['id'], {'format': 'full'}), self.config)
                                      for r in refs[:limit]) if e]
            except SourceError as error:
                failed[account['id']] = error.category
                continue
            found += self.store.keep_found(account['id'], events)
        return found, failed

    def agent_card(self, suggestion_id):
        """What a Claude Code or Codex brief is made of: the card, its next step as the task, the owner's note, who it is
        about, its chat so far (background), drafts, links, result files and source messages (agent_jobs.brief_for)."""
        with self.store.connect() as db:
            row = db.execute('SELECT s.*,p.status preparation_status,p.reason preparation_reason,p.error preparation_error,'
                             'p.questions preparation_questions FROM suggestions s LEFT JOIN preparations p ON s.id=p.suggestion_id '
                             'WHERE s.id=?', (str(suggestion_id),)).fetchone()
            if not row:
                return None
            card = dict(row)
            source_lines_shown(db, [card])  # a Slack DM by the person's name, never a raw chat handle
            extra = self.store.suggestion_result(card, db)
            note = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND trim(feedback)<>'' AND source IN ('telegram','dashboard') "
                              'AND id NOT IN (SELECT decision_id FROM decision_annotations) ORDER BY created_at DESC,rowid DESC LIMIT 1',
                              (card['id'],)).fetchone()
            try:
                chat = self.card_chat_service(db, card['id'])
            except (sqlite3.Error, ValueError, TypeError, KeyError):
                chat = ([], {})
        actions = extra.get('next_actions') or []
        drafts = [a for a in actions if a.get('body') or a.get('message')]
        links = [*extra.get('original_urls', []), *[a['url'] for a in actions if a.get('kind') == 'open' and str(a.get('url') or '').startswith('https://')]]
        files = [WORKSPACE / f['path'] for f in extra.get('result_files', [])]
        try:
            views = self.store.originals(card['id'])[:5]
        except (ValueError, sqlite3.Error):
            views = []
        note = note['feedback'].strip() if note else ''
        return {'card': card, 'drafts': drafts, 'links': links, 'files': files, 'messages': agent_messages(views), 'sources': views,
                'task': card_task(card), 'note': note, 'about': agent_about(card, views), 'history': agent_history(*chat, skip=note),
                'message_kinds': [v['kind'] for v in views]}

    def newer_unchecked(self, event_ids, checked=None):
        """Before a new to-do: what happened after its evidence (activity_since) that the review hasn't said it read
        (newer_checked). [] when nothing came after, so most to-dos save at once and the check costs no extra step."""
        ids = [int(i) for i in event_ids or [] if isinstance(i, int) or str(i).isdigit()]
        with self.store.connect() as db:
            found = activity_since(db, ids, self.store.owner_user_ids, {x['email']: x['name'] for x in self.teammate_addresses()},
                                   company_domains(self.config))
        read = {int(i) for i in (checked if isinstance(checked, list) else []) if isinstance(i, int) or str(i).isdigit()}
        return [x for x in found if x['id'] not in read]

    def teammate_addresses(self):
        """The members of the owner's Work Fleets, each address with their name: who Hand off by email suggests first."""
        out = []
        try:
            for found in (self.fleet.fleets().values() if getattr(self, 'fleet', None) else ()):
                if found.get('kind') != 'work':
                    continue
                for member in found.get('members', []):
                    if member.get('me'):
                        continue
                    for email in dict.fromkeys(str(e).lower() for e in [member.get('account_email'), *(member.get('emails') or [])] if e and '@' in str(e)):
                        out.append({'name': ' '.join(str(member.get('name') or '').split())[:80], 'email': email})
        except Exception:  # noqa: BLE001 - suggestions only: the Graph and the domains still help
            return out
        return out

    def owner_emails(self):
        """The owner's addresses: each account's (its owner_emails, else its own) and the ones found as theirs
        (own_addresses.py: aliases, their calendar, their profiles; never a shared one or one they removed)."""
        found = {str(e).lower() for a in self.config.get('accounts', []) for e in a.get('owner_emails', [a.get('email')]) if e}
        try:
            with self.store.connect() as db:
                return found | own_addresses.yours(db, self.config)
        except sqlite3.Error:
            return found

    def calendar_write(self, args, transport=None):
        """The Calendar form's Add, Save or Delete: the owner filled it in and tapped it, so this one change runs now.
        request_id is the tap: the same id again is that same write (a create keeps its Google event id), never a second.
        guests: who the owner invited; the form listed them above a button that said how many (invite), so a list that
        doesn't match that count is refused, and nobody gets an invite without that tap."""
        request_id = str(args.get('request_id') or '')
        if not re.fullmatch(r'[a-f0-9-]{16,64}', request_id):
            raise ValueError('Invalid request')
        change = {k: v for k, v in args.items() if k in calendar_writes.KEYS - {'kind', 'label'}}
        if args.get('guests'):
            if not isinstance(args['guests'], list) or args.get('invite') != len(args['guests']):
                raise ValueError('Check who gets an invite and tap again. Nothing was sent.')
            change['guests'] = args['guests']
        with self.store.connect() as db:
            done = db.execute('SELECT status,result FROM calendar_writes WHERE id=?', (request_id,)).fetchone()
            if done and done['status'] == 'done':
                return {'status': 'done', 'duplicate': True}
            if done and done['status'] == 'sending':
                raise ValueError('That change is still going through.')
            events = calendar_write_events(db, [change.get('event')], self.owner_emails())
        action = calendar_writes.validate({'kind': 'calendar', **change}, self.config, events, invite=True)
        transport = transport or calendar_writes.CalendarTransport(self.config, credential, gog_read)
        transport.preflight(action)
        stamp = now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT 1 FROM calendar_writes WHERE id=? AND status IN ('sending','done')", (request_id,)).fetchone():
                raise ValueError('That change is still going through.')
            db.execute('INSERT INTO calendar_writes(id,account_id,op,payload,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?) '
                       "ON CONFLICT(id) DO UPDATE SET status='sending',payload=excluded.payload,error=NULL,updated_at=excluded.updated_at",
                       (request_id, action['account_id'], action['op'], hashlib.sha256(encoded(action).encode()).hexdigest(), 'sending', stamp, stamp))
        job = {'id': request_id}
        try:
            result = transport.send(action, job)
        except Exception:  # noqa: BLE001 - unknown outcome: read it back below
            result = {}
        if not result.get('message_id') and not result.get('rejected'):
            try:
                result = transport.reconcile(action, job) or result
            except Exception:  # noqa: BLE001
                pass
        status = 'done' if result.get('message_id') else 'failed' if result.get('rejected') else 'uncertain'
        error = {'done': None, 'failed': f"Google Calendar refused it (error {result.get('rejected')}). Nothing was changed.",
                 'uncertain': 'I couldn’t confirm the change. Check the calendar before you try again.'}[status]
        with self.store.connect() as db:
            db.execute('UPDATE calendar_writes SET status=?,result=?,error=?,updated_at=? WHERE id=?',
                       (status, result.get('message_id'), error, now(), request_id))
        if status == 'done':
            self.sync_soon(action['account_id'])
        return {'status': status, 'error': error, 'op': action['op'], 'calendar': action['calendar_name'], 'invited': len(action.get('guests') or ())}

    def connector_sync(self, args):
        """Stop, Start or Restart on a Salesflare card. Stop: nothing is read until Start, which goes on where it was.
        Restart: the round of accounts it was on is dropped, with its errors and wait, and a new one reads the last
        week again now (a round stuck on slow or failing accounts). What it brought in stays either way."""
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
        if not account or account.get('service') != 'salesflare':
            raise ValueError('Only a Salesflare connection can be stopped or restarted here')
        do = args.get('do')
        if do not in ('stop', 'start', 'restart'):
            raise ValueError('Choose stop, start or restart')
        lock = self.sync_lock(account['id'])
        if not lock.acquire(timeout=20):
            raise ValueError('It is reading a batch of accounts. Try again in a minute')
        try:
            with self.store.connect() as db:
                row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                state = json.loads(row['state'] or '{}') if row else {}
                if do == 'stop':
                    state['stopped'] = now()
                else:
                    state.pop('stopped', None)
                if do == 'restart':
                    state.pop('window', None)
                    state['next_full'] = 0
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state'
                           + ('' if do == 'stop' else ',error=NULL,retry_at=NULL,failures=0'), (account['id'], json.dumps(state)))
        finally:
            lock.release()
        LOG.info('connector_sync account=%s do=%s', account['id'], do)
        if do != 'stop':
            self.sync_soon(account['id'])
        return {'ok': True, 'do': do, 'salesflare': salesflare_progress(account, state)}

    def sync_soon(self, account_id):
        """Read this calendar again now instead of at its next poll, so a change shows in the Calendar in seconds."""
        account = next((a for a in self.config.get('accounts', []) if a.get('id') == account_id), None)
        if not account:
            return

        def read():
            try:
                with self.sync_lock(account_id):
                    sync_source(self.store, self.config, account)
            except Exception as error:  # noqa: BLE001 - the next poll reads it anyway
                LOG.warning('sync_soon account=%s error=%s', account_id, type(error).__name__)
        threading.Thread(target=read, name='sync-soon-' + account_id, daemon=True).start()

    def originals(self, suggestion_id, event_id='', event_ids=None):
        """Source messages for the dashboard, with Gmail attachments looked up live (read-only):
        a card's, one collected event opened from the Events or People tab, or a conversation's messages in order."""
        items = self.store.originals(suggestion_id) if suggestion_id else self.store.event_views(event_ids or [event_id])
        cache = self.__dict__.setdefault('_attachments', {})
        for item in items:
            body, cut = shown_body(item['body'])  # read by people: never the model's quoted-history marker
            item.update(body=body, clipped=item['clipped'] or cut)
            source = item.pop('gmail')
            item['attachments'] = []
            if not source:
                continue
            key = (source['account_id'], source['message_id'])
            if key not in cache or cache[key][0] < time.monotonic() - 600:
                try:
                    cache[key] = (time.monotonic(), message_attachments(self.gmail_message(*key)[1].get('payload')))
                except Exception:
                    continue  # Attachments are a convenience; the email itself still shows.
            item['attachments'] = cache[key][1]
        return items

    def whatsapp_source(self, account):
        """The WhatsApp source of one of the owner's connections (whatsapp_images_app fetches photos through it)."""
        return WhatsApp(self.config, account)

    def whatsapp_photo_event(self, account_id, source_id):
        """A message whose photo was kept or read, with the photo joined in (whatsapp_images.with_photo), the way its next
        sync builds it: a new version, so the review reads what the photo says."""
        with self.store.connect() as db:
            row = db.execute('SELECT kind,occurred_at,title,body,metadata,deleted FROM events WHERE account_id=? AND source_id=?',
                             (account_id, source_id)).fetchone()
            photo = db.execute('SELECT * FROM whatsapp_photos WHERE account_id=? AND source_id=?', (account_id, source_id)).fetchone()
        if not row or not photo or row['kind'] != 'whatsapp.message':
            return False
        event = {'account_id': account_id, 'source_id': source_id, 'kind': row['kind'], 'occurred_at': row['occurred_at'], 'title': row['title'],
                 'body': whatsapp_images.base_body(row['body']), 'metadata': json.loads(row['metadata']), 'deleted': bool(row['deleted'])}
        self.store.commit_page(account_id, None, [whatsapp_images.with_photo(event, dict(photo))], record_sync=False)
        return True

    def email_view(self, suggestion_id, event_id):
        """The HTML of one source email, read live (read-only), with its embedded images."""
        source = self.gmail_source(suggestion_id, event_id)
        if not source:
            raise ValueError('Email not available')
        payload = self.gmail_message(source['account_id'], source['message_id'])[1].get('payload')
        return {'html': message_html(payload), 'images': message_images(payload)}

    def gmail_source(self, suggestion_id, event_id):
        items = self.store.originals(suggestion_id) if suggestion_id else self.store.event_views([event_id])
        return next((item['gmail'] for item in items if str(item['event_id']) == str(event_id) and item['gmail']), None)

    def draft_attachment(self, suggestion_id, sha256):
        """A file attached to this card's own email draft, served from the service's store by checksum."""
        with self.store.connect() as db:
            row = db.execute('SELECT next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        record = next((r for action in next_actions.actions(row['next_action'] if row else None)
                       for r in action.get('attachments', []) if r['sha256'] == sha256), None)
        if not record:
            raise ValueError('Attachment not available')
        return next_actions.attachment_bytes(record, self.config), record['type'], record['name']

    def attachment(self, suggestion_id, event_id, part):
        source = self.gmail_source(suggestion_id, event_id)
        if not source:
            raise ValueError('Attachment not available')
        account, message = self.gmail_message(source['account_id'], source['message_id'])
        payload = message.get('payload') or {}
        # Only this message's real attachments and its embedded images are served.
        if part not in [a['part'] for a in message_attachments(payload)] + list(message_images(payload).values()):
            raise ValueError('Attachment not available')
        found = []
        def walk(node):
            if str(node.get('partId', '')) == part:
                found.append(node)
            for child in node.get('parts', []):
                walk(child)
        walk(payload)
        if not found:
            raise ValueError('Attachment not available')
        node = found[0];body = node.get('body') or {}
        data = body.get('data') or gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.attachments.get',
                                            {'userId': 'me', 'messageId': source['message_id'], 'id': body['attachmentId']},
                                            'https://www.googleapis.com/auth/gmail.readonly').get('data', '')
        return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)), node.get('mimeType', 'application/octet-stream'), node.get('filename') or 'image'

    def mail_attachment(self, args):
        """An email's attachments for a preparation, read-only (Gmail and Outlook): a list, or one saved in the job's
        attachments folder, at most 18 MB. With message protection on it is kept there sealed with the message key and
        the run reads a copy in a private folder that goes after the run (mail_attachments.py); `open` gives such a copy
        of an attachment saved earlier."""
        folder = Path(args.get('_folder') or mail_attachments.root(self.config))
        if args.get('open'):
            return mail_attachments.open_copy(self.config | {'attachment_root': str(folder)}, args['open'], args.get('job_id'))
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account_id')), None)
        message_id = str(args.get('message_id') or '')
        if args.get('event_id') is not None:
            with self.store.connect() as db:
                row = db.execute("SELECT account_id,source_id FROM events WHERE id=? AND kind IN ('gmail.message','ms_graph.message','outlook.message')",
                                 (int(args['event_id']),)).fetchone()
            if not row:
                raise ValueError('No collected email with that event_id')
            account = next((a for a in self.config['accounts'] if a['id'] == row['account_id']), None)
            message_id = row['source_id']
        if not account or not next_actions.mail_account(account):
            raise ValueError('Give the account_id of a Gmail or Outlook mailbox')
        if not message_id:
            raise ValueError('Give the message_id or event_id of the email')
        fetch = App.outlook_attachments if next_actions.outlook(account) else App.gmail_attachments
        found, data = fetch(self, account, message_id, args.get('save'))
        if not args.get('save'):
            return {'attachments': found}
        if len(data) > next_actions.MAX_ATTACHMENT_BYTES:
            raise ValueError('That attachment is larger than 18 MB')
        job = str(args.get('job_id') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        name = re.sub(r'[^\w. -]+', '_', found['name']).strip(' .') or 'attachment'
        saved = mail_attachments.save(self.config, folder / job, name, data)
        return saved | {'name': name, 'mime': found['mime'], 'size': len(data)}

    NO_DOC_CONNECTION = 'No Docs connection in this to-do’s area can do things. Give what you need in the to-do instead.'

    def doc_run(self, args):
        """The running preparation a doc read is for (Do it, or a to-do chat's run): its job id, its own events and its
        area (doc_writes.area). Docs are read only for a run the owner started."""
        job = str(args.get('job_id') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        with self.store.connect() as db:
            run = db.execute("SELECT s.event_ids,s.account_ids FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                             "WHERE p.job_id=? AND p.status IN ('queued','starting','running','blocked')", (job,)).fetchone()
            if not run:
                raise ValueError('Docs are read only for a running preparation of the task the owner started')
            links, plugin = {}, load_connector('docs')
            for r in db.execute("SELECT e.account_id,e.body,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id",
                                (run['event_ids'],)) if plugin else ():
                for file_id in plugin.doc_links(str(r['body'] or '') + ' ' + str(r['metadata'] or '')):
                    links.setdefault(file_id, r['account_id'])
        return job, run, links, doc_writes.area(self.config, json.loads(run['account_ids'] or '[]'))

    def doc_connections(self, area, provider=None):
        """The owner's own Docs connections in this area that can do things (abilities.py), Google or Microsoft."""
        plugin = load_connector('docs')
        return [a for a in self.config.get('accounts', []) if a.get('service') == 'docs' and plugin and abilities.actions_on(a)
                and doc_writes.fits(a.get('boundary'), area) and (provider is None or plugin.provider(self.config, a) == provider)]

    def doc_read_error(self, error):
        return ValueError({'docs_not_connected': 'Reading docs is not allowed for this account yet (Connect Google Docs or Microsoft documents)',
                           'docs_text_unsupported': 'That file has no text to read here (open it in the browser instead)'}.get(
                               error.category, f'The doc could not be read ({error.category})'))

    def gmail_attachments(self, account, message_id, save=None):
        """A Gmail message's real attachments, read live with gmail.readonly: the list, or (`save`: its part id or
        name) that one and its bytes."""
        try:
            message = self.gmail_message(account['id'], message_id)[1]
        except Exception as error:
            raise ValueError(f'Gmail could not give the message ({type(error).__name__})') from None
        payload = message.get('payload') or {}
        found = [{'id': a['part'], 'name': a['name'], 'mime': a['mime'], 'size': a['size'], 'inline': False, 'kind': 'file'}
                 for a in message_attachments(payload)]
        if not save:
            return found, None
        chosen = next((a for a in found if save in (a['id'], a['name'])), None)
        if not chosen:
            raise ValueError('No attachment with that id or name')
        if chosen['size'] > next_actions.MAX_ATTACHMENT_BYTES:
            raise ValueError('That attachment is larger than 18 MB')
        nodes = []
        def walk(node):
            if str(node.get('partId', '')) == chosen['id']:
                nodes.append(node)
            for child in node.get('parts', []):
                walk(child)
        walk(payload)
        body = nodes[0].get('body') or {}
        data = body.get('data') or gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.attachments.get',
                                            {'userId': 'me', 'messageId': message_id, 'id': body['attachmentId']},
                                            'https://www.googleapis.com/auth/gmail.readonly').get('data', '')
        return chosen, base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))

    def outlook_attachments(self, account, message_id, save=None):
        """An Outlook message's attachments through Microsoft Graph, read-only: the list, or that one and its bytes."""
        try:
            found = ms_graph.attachments(self.config, credential, account, message_id)
            if not save:
                return [{k: a[k] for k in ('id', 'name', 'mime', 'size', 'inline', 'kind')}
                        | ({'note': 'a link to a cloud file: open it in the browser'} if a['kind'] == 'link' else
                           {'note': 'an attached email or event: not saved; read the message itself'} if a['kind'] == 'item' else {})
                        for a in found], None
            chosen = next((a for a in found if save in (a['id'], a['name'])), None)
            if not chosen:
                raise ValueError('No attachment with that id or name')
            if chosen['kind'] != 'file':
                raise ValueError('Only file attachments can be saved; ' + ('open this cloud link in the browser' if chosen['kind'] == 'link' else 'this is an attached email or event'))
            if chosen['size'] > next_actions.MAX_ATTACHMENT_BYTES:
                raise ValueError('That attachment is larger than 18 MB')
            return chosen, ms_graph.attachment(self.config, credential, account, message_id, chosen['id'])
        except ms_graph.GraphError as error:
            raise ValueError(f'Outlook could not give the attachment ({error})') from None

    def hours(self):
        """Work hours as the dashboard shows and edits them."""
        return {**WORK_HOURS, 'timezone': getattr(local_tz(), 'key', str(local_tz())), 'digest_at': self.config.get('digest_at', '08:30'),
                'saveable': bool(getattr(self, 'config_path', None))}

    def set_hours(self, args):
        """The owner's Work hours from the dashboard: checked, saved in config.json and in use at once."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        values = hours_settings(self.config, args)
        save_hours(self.config_path, values)
        self.config.update(values)
        set_timezone(values['timezone'])
        set_work_hours(values['work_hours'])
        return self.hours()

    def locale_view(self):
        """Language and region as Settings shows them and the dashboard formats dates and times (locale_prefs)."""
        return {**locale_prefs.view(), 'saveable': bool(getattr(self, 'config_path', None))}

    def set_locale(self, args):
        """The owner's language, region, time format and To-dos filter from the dashboard: checked, saved in config.json and in use at once."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        if 'browser' in args:  # the dashboard's first load on a Machine without a region: the browser's, never over a choice
            browser = args['browser'] if isinstance(args['browser'], dict) else {}
            found = locale_prefs.guess(browser.get('zone'), browser.get('language'))
            if self.config.get('locale') or not found:
                return self.locale_view()
            args = {'locale': found}
        values = locale_prefs.settings(args)
        save_hours(self.config_path, values)
        self.config.update(values)
        locale_prefs.configure(self.config)
        return self.locale_view()

    def setup_hints_view(self):
        """setup_hints, worked out at most every 10 minutes: the dashboard asks for its state every few seconds."""
        # a source, Telegram or Codex connected just now drops its hint at once
        key = (tuple(sorted(str(a.get('service')) for a in self.config.get('accounts') or [] if isinstance(a, dict))),
               telegram_on(self.config), json.dumps(self.config.get('agents'), sort_keys=True, default=str))
        cached = getattr(self, '_setup_hints', None)
        if cached and cached[1] == key and time.monotonic() - cached[0] < 600:
            return cached[2]
        try:
            hints = setup_hints(self.store, self.config)
        except (sqlite3.Error, OSError, ValueError):
            hints = []
        self._setup_hints = (time.monotonic(), key, hints)
        return hints

    def set_agents(self, args):
        import agent_remote
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        session = str(args.get('claude_session') or '').strip()
        found = agent_remote.session_id(session) if session else ''
        if session and not found:
            raise ValueError('Paste the session link from claude.ai/code')
        env, branch = str(args.get('codex_env') or '').strip(), str(args.get('codex_branch') or '').strip()
        if env and not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', env):
            raise ValueError('That is not a Codex environment id')
        if branch and not re.fullmatch(r'[A-Za-z0-9._/-]{1,120}', branch):
            raise ValueError('That is not a branch name')
        own = dict(agent_jobs.settings(self.config) or {})
        claude = {k: v for k, v in (own.get('claude') if isinstance(own.get('claude'), dict) else {}).items() if k not in ('session', 'device')}
        codex = {k: v for k, v in (own.get('codex') if isinstance(own.get('codex'), dict) else {}).items() if k not in ('env', 'branch')}
        if found:
            claude.update(place='remote', session=found, **({'device': str(args['device']).strip()[:60]} if str(args.get('device') or '').strip() else {}))
        if env:
            codex.update(place='cloud', env=env, **({'branch': branch} if branch else {}))
        for part, key, place in ((claude, 'session', 'remote'), (codex, 'env', 'cloud')):
            if not part.get(key) and part.get('place') == place:
                part.pop('place')
        own.update(claude=claude, codex=codex)
        save_hours(self.config_path, {'agents': own})
        self.config['agents'] = own
        return self.agents_view()

    def gbrain_save(self, value):
        save_hours(self.config_path, {'gbrain': value})
        self.config['gbrain'] = value

    def gbrain_action(self, name, args):
        if name == 'gbrain_status':
            return self.gbrain_view()
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        brain = gbrain.Brain(self.config)
        if name == 'gbrain_on':
            # Nothing goes into GBrain, and reviews get none of its tools, before the owner agreed to what goes in.
            if args.get('consent') is not True:
                raise ValueError('Agree to what goes into GBrain first')
            binary = brain.binary()
            if not binary:
                raise ValueError('Install GBrain on this Machine first')
            try:
                linked = brain.link()
            except gbrain.BrainError:
                raise ValueError('The Machine could not add GBrain. Try again.') from None
            self.gbrain_save({'on': True, 'consent_at': now(), 'work': args.get('work') is True, 'linked': linked, 'bin': binary})
            self.gbrain_start()
        elif name == 'gbrain_work':
            if not gbrain.on(self.config):
                raise ValueError('Turn GBrain on first')
            self.gbrain_save({**gbrain.settings(self.config), 'work': args.get('on') is True})
            self.gbrain_start()
        elif name == 'gbrain_off':
            # The brain and the pages in it stay: only OpenClaw's link to it, when The Machine made it, and what came back.
            try:
                brain.unlink()
            except gbrain.BrainError:
                pass
            self.gbrain_save({'on': False})
            with self.store.connect() as db:
                gbrain.forget(db)
        return self.gbrain_view()

    def started_at(self):
        """When this Machine started: `started_at` in the config (a hosted machine's signup), else its first own activity."""
        given = str(self.config.get('started_at') or '')
        if given:
            return given
        if getattr(self, '_started_at', None):  # found once, it stays: the poll asked each time, two passes over big tables
            return self._started_at
        with self.store.connect() as db:
            row = db.execute("SELECT MIN(t) FROM (SELECT MIN(started_at) t FROM analyses UNION ALL SELECT MIN(created_at) FROM suggestions"
                             " UNION ALL SELECT MIN(at) FROM sync_activity UNION ALL SELECT MIN(day) FROM sync_daily)").fetchone()
        self._started_at = row[0] if row and row[0] else None
        return self._started_at

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
            if not embeddings.settings(self.config):
                raise ValueError('Related signals by meaning are not set up; search with events and a query')
            if not args.get('event_ids') and not str(args.get('query') or '').strip():
                raise ValueError('Give event_ids, a query or both')
            found, semantic = self.related(selected, args.get('event_ids') or (), str(args.get('query') or ''),
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

    def resume_wait(self, account):
        """Seconds until a slow source (polled every 10 minutes or less often: LinkedIn, X, CRM) is due
        again after a restart. A restart alone must not cost an extra read; catch-up and new accounts go now.
        Salesflare too, whatever its poll: a round starts with its account lists ordered by activity, which run close
        to Salesflare's 2-minute gateway limit on a large team. A release restarts a team's Machines together, and
        each one starting that list at the same second answered 504 (HTTP gateway timeout), so after a finished
        round it waits out its gap plus a random spread. One mid-round goes now: its list is already read."""
        delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
        crm = account.get('service') == 'salesflare'
        if delay < 600 and not crm:
            return 0
        state = self.store.checkpoint(account['id']) or {}
        with self.store.connect() as db:
            row = db.execute('SELECT last_success FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
        unfinished = state.get('page_token') or state.get('catchup') or state.get('coverage_complete') is False
        if not row or not row['last_success'] or not state or state.get('mode') != 'incremental' or (unfinished and account.get('service') != 'x') \
                or (crm and state.get('window')):
            return 0
        since = (dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(row['last_success'])).total_seconds()
        return max(0, min(delay, delay - since)) + (secrets.randbelow(SALESFLARE_RESTART_SPREAD + 1) if crm else 0)

    def wait_for_retry(self, account, row):
        """Wait until the checkpoint's retry time; True when stopping. An expired Google sign-in
        is retried as soon as the owner signs in again, instead of after the full hour."""
        expired = bool(re.search(SIGNIN_ERROR, row['error'] or ''))
        while True:
            seconds = (dt.datetime.fromisoformat(row['retry_at']) - dt.datetime.fromisoformat(now())).total_seconds()
            if seconds <= 0:
                return False
            if expired and gog_signed_in_since(self.config, account, row['error_at']):
                LOG.info('sync account=%s signed in again, retrying now', account['id'])
                with self.store.connect() as db:
                    db.execute('UPDATE checkpoints SET retry_at=NULL WHERE account_id=?', (account['id'],))
                return False
            if self.stop.wait(min(seconds, 15) if expired else seconds):
                return True

    def sync_lock(self, account_id):
        """One sync of an account at a time: its collector, and a read right after a calendar change (sync_soon)."""
        with SYNC_LOCKS_LOCK:
            return SYNC_LOCKS.setdefault(account_id, threading.Lock())

    def sync_retrying(self, account, source=None):
        """One sync of the account; when the service answers 429 or a transient 5xx, one more try shortly after (its
        Retry-After when that is short, else QUICK_RETRY_SECONDS). A second failure goes to the caller. Not for Slack's
        rate limit: its reads keep their own round (Slack.read_went), and a quick extra read would spend the next one."""
        for attempt in (0, 1):
            try:
                with self.sync_lock(account['id']):
                    return sync_slack(self.store, self.config, account, source) if source else sync_source(self.store, self.config, account)
            except SourceError as error:
                wait = error.retry_after or QUICK_RETRY_SECONDS
                if attempt or not upstream_busy(error) or (source and rate_limited(error)) or wait > QUICK_RETRY_MAX \
                        or self.stop.is_set():
                    raise
                LOG.info('sync account=%s service busy (%s), retrying in %ds', account['id'], error, wait)
                if self.stop.wait(wait):
                    raise

    def ability_checker(self, account):
        """An action-only connection (Brings in signals off): nothing is read, but what it may do (a Docs connection's
        reads and writes, from its consent) is checked now and every ABILITY_CHECK_SECONDS, for its card."""
        plugin = load_connector(account.get('service', '')) if account.get('service') not in BUILT_IN_SERVICES else None
        refresh = getattr(plugin, 'refresh', None)
        while refresh and not self.stop.is_set():
            try:
                refresh(self.store, self.config, account, CONNECTOR_HELPERS)
            except Exception as error:  # noqa: BLE001 - the card keeps what it knew
                LOG.warning('ability check account=%s error=%s', account['id'], type(error).__name__)
            if self.stop.wait(ABILITY_CHECK_SECONDS):
                break

    def collector(self, account):
        source = Slack(self.config, account, self.stop) if account.get('service') == 'slack' else None
        try:
            wait = self.resume_wait(account)
        except Exception as error:  # never keep a source from starting
            LOG.warning('resume_wait account=%s error=%s', account['id'], type(error).__name__)
            wait = 0
        if wait:
            LOG.info('sync account=%s resumes in %ds (last read before the restart)', account['id'], wait)
            if self.stop.wait(wait):
                return
        while not self.stop.is_set():
            try:
                with self.store.connect() as db:
                    row = db.execute('SELECT retry_at,error,error_at FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                local_android_feed = account.get('service') == 'android' and account.get('transport') == 'openclaw-feed'
                if row and row['retry_at'] and not local_android_feed:
                    if self.wait_for_retry(account, row):
                        break
                delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
                try:
                    result = self.sync_retrying(account, source)
                    LOG.info('sync account=%s mode=%s read=%d filtered=%d skipped=%d', account['id'], result['mode'], result['events'], result.get('filtered', 0), result.get('skipped', 0))
                    state = self.store.checkpoint(account['id'])
                    if not result.get('stopped') and (result.get('more') or state.get('mode', result['mode']) != 'incremental' or state.get('page_token')):  # a plugin's checkpoint may not keep a mode
                        delay = account.get('poll_seconds', 3600) if account.get('service') == 'x' else 30 if account.get('service') == 'linkedin' else 0 if source else 5
                    elif account.get('service') == 'salesflare':
                        # A finished round: the next one opens with the slow account lists. Rounds of teammates' Machines
                        # take about as long, so two that started close stay together for hours (both answered 504 in a
                        # regular round, 41 minutes after a shared restart). A fresh spread each round breaks that up.
                        delay += secrets.randbelow(SALESFLARE_ROUND_SPREAD + 1)
                except SourceError as error:
                    if self.stop.is_set():
                        break
                    delay = error.retry_after or delay
                    error.retry_after = delay
                    if local_android_feed:
                        # Local queue reads may resume immediately when the bridge
                        # returns. Phone fallback attempts keep their own durable cap.
                        delay = account.get('poll_seconds', 15)
                    self.store.failed(account['id'], error)
                    LOG.warning('sync account=%s error=%s', account['id'], error)
                    # Enter the checkpoint wait directly so renewed sign-ins are watched.
                    # Ordinary failures and rate limits retain their normal backoff.
                    if re.search(SIGNIN_ERROR, str(error)):
                        continue
                except sqlite3.OperationalError as error:
                    if not db_busy(error):
                        safe = SourceError(type(error).__name__, retry_after=delay)
                        self.store.failed(account['id'], safe)
                        LOG.error('sync account=%s error=%s', account['id'], safe)
                    else:  # another writer held the database past the busy timeout: transient, read again soon
                        LOG.info('sync account=%s waits: database busy', account['id'])
                        delay = DB_BUSY_RETRY
                except Exception as error:
                    safe = SourceError(type(error).__name__, retry_after=delay)
                    self.store.failed(account['id'], safe)
                    LOG.error('sync account=%s error=%s', account['id'], safe)
            except Exception as error:
                # A database error here (locked, disk full) must never end this
                # account's thread silently while /health stays green.
                LOG.error('collector account=%s internal_error=%s', account['id'], type(error).__name__)
                delay = 60
            self.__dict__.setdefault('collector_reads', {})[account['id']] = time.time()  # a read ended (Check now waits for it)
            self.collector_rest(account['id'], delay)

    # -- notifications (notify.py): Settings, Notifications and the morning digest
    def notify_on(self, kind, channel):
        with self.store.connect() as db:
            return notify.allowed(db, kind, channel)

    def notify_mail_target(self):
        """(url, token) for the digest email through the control plane, or None (not hosted or paired)."""
        return cloud_target(self.config)

    def notify_open(self, ref):
        """Whether a held notification's to-do or Fleet question still waits for the owner."""
        what, _, key = ref.partition(':')
        with self.store.connect() as db:
            if what == 'suggestion':
                row = db.execute('SELECT s.status,s.handled_hint,s.outcome,p.status prep FROM suggestions s LEFT JOIN preparations p ON p.suggestion_id=s.id '
                                 'WHERE s.id=?', (key,)).fetchone()
                return bool(row) and not looks_done(dict(row)) and not waits_on_others(dict(row)) and (row['status'] in ('pending', 'prepared', 'instructions')
                                                                  or (row['status'] == 'accepted' and row['prep'] == 'blocked'))
            if what == 'fleet':
                try:
                    return bool(db.execute("SELECT 1 FROM fleet_in WHERE id=? AND status='waiting'", (key,)).fetchone())
                except sqlite3.OperationalError:
                    return False
        return True

    def notify_step(self, current=None, push=None, mail=None):
        """Held notifications (notify.take_due): a push a minute after the owner left the dashboard, and one email for
        what is still unseen and waiting a while later. Within work hours only; a held push outside them is dropped."""
        local = (current or dt.datetime.now(dt.timezone.utc)).astimezone(local_tz())
        with self.store.connect() as db:
            notify.ensure(db)
            if not in_hours(local):
                notify.drop_pushes(db)
                return None
            pushes, lines = notify.take_due(db, self.notify_open)
            handoffs = notify.take_handoffs(db)
        subscriptions, phones = push_reach(self.store, self.config) if pushes else ([], 0)
        went = []
        if pushes and not subscriptions and not phones:
            with self.store.connect() as db:
                notify.delivered(db, pushes)  # nowhere to push to: dropped, not kept to go off later
            pushes = []
        for item in pushes:
            if push_send(self.store, self.config, subscriptions, item['payload'], 'held', push, kind=item['kind'], held=True):
                with self.store.connect() as db:
                    notify.delivered(db, [item])
                went.append('push')
        target = (lines or handoffs) and self.notify_mail_target()
        if target:
            root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/') if self.config.get('dashboard_host') else ''
            for item in handoffs:  # each its own email, once
                message = notify.handoff_mail(item, root)
                if (mail(*target, message['subject'], message['text']) if mail else notify.mail(*target, message['subject'], message['text'], delivery=item['delivery'])):
                    with self.store.connect() as db:
                        notify.delivered(db, [item])
                    went.append('email')
            message = notify.waiting_mail(lines, root) if lines else None
            if message and (mail(*target, message['subject'], message['text']) if mail else notify.mail(*target, message['subject'], message['text'], delivery=lines[0]['batch'])):
                with self.store.connect() as db:
                    notify.delivered(db, lines)
                    notify.mailed(db)
                went.append('email')
        if went:
            LOG.info('notify held channels=%s', ','.join(went))
        return went

    def app_push_action(self, name, args):
        """The mobile app's phones (app_push_register, app_push_unregister): the control plane keeps the push token and
        sends the wakeups (app_wake); this Machine keeps the phone's id, platform and name for Settings, never the token."""
        if name == 'app_push_unregister':
            device = str(args.get('id') or '')
            if not notify.APP_ID.fullmatch(device):
                raise ValueError('Invalid phone')
            target = cloud_target(self.config)
            answer = notify.app_push(*target, {'action': 'unregister', 'id': device}) if target else {'missing': True}
            if not answer:
                raise ValueError('Couldn’t remove this phone. Try again.')
            with self.store.connect() as db:
                notify.app_device_remove(db, [device])
            return {'removed': True}
        platform, token = args.get('platform'), args.get('token')
        if platform not in ('fcm', 'apns') or not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9_:.-]{16,4096}', token):
            raise ValueError('Invalid phone')
        label = ' '.join(re.sub(r'[\x00-\x1f\x7f<>]', ' ', str(args.get('label') or '')).split())[:60]
        label = label or ('iPhone' if platform == 'apns' else 'Android')
        target = cloud_target(self.config)
        if not target:  # self-hosted off The Machine Network: the relay doesn't know it. The app works without them.
            return {'registered': False, 'reason': 'network'}
        # fetch: the app shows the notification itself, with what it asks this Machine for (GET /api/notice): the Android
        # app, and the iPhone's Notification Service extension
        answer = notify.app_push(*target, {'action': 'register', 'platform': platform, 'token': token, 'label': label,
                                           'sandbox': args.get('sandbox') is True, 'fetch': args.get('fetch') is True})
        device = str((answer or {}).get('id') or '')
        if not notify.APP_ID.fullmatch(device):
            raise ValueError('Couldn’t turn on notifications for this phone. Try again.')
        with self.store.connect() as db:
            notify.app_device_add(db, device, platform, label, now())
        LOG.info('app push registered platform=%s', platform)
        return {'registered': True, 'id': device, 'platform': platform, 'label': label}

    def notify_view(self):
        with self.store.connect() as db:
            prefs = notify.prefs(db)
            devices = db.execute('SELECT count(*) FROM push_subscriptions').fetchone()[0]
            phones = notify.app_devices(db)  # the mobile app's phones count as devices too, and are listed to remove
        return {'prefs': prefs, 'telegram': telegram_on(self.config), 'email': mail_ready(self.config),
                'push_devices': devices + len(phones), 'app_devices': phones,
                'app_push_ready': bool(cloud_target(self.config)), 'phone_app': phone_app(self.config),
                'push_ready': bool(self.config.get('dashboard_host')), 'digest_at': self.config.get('digest_at', '08:30'),
                'weekly_recap': self.recap_switch_view()}

    def digest(self, current=None):
        """The morning digest as of `current` (notify.compose), or None when there is nothing to say."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        start = local.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=1)
        # Overnight: since the end of the last work day's hours (or a day back)
        hour, minute = clock(WORK_HOURS['end'])
        since = (local - dt.timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        if since > local:
            since -= dt.timedelta(days=1)
        utc = lambda t: t.astimezone(dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            meetings = recap_meetings(db, utc(start), utc(end), {})
            meetings = [m for m in meetings if m['at'] >= utc(local)] or []
            open_states = "('pending','accepted','prepared','instructions')"
            due = [dict(r) for r in db.execute(
                f"SELECT id,title FROM suggestions WHERE (status IN {open_states} AND due=? AND NOT {NOT_FOR_OWNER_SQL}) OR (status='snoozed' AND snoozed_until>=? AND snoozed_until<?) "
                "ORDER BY created_at LIMIT 20", (local.date().isoformat(), utc(local), utc(end)))]
            overnight = [dict(r) for r in db.execute(
                "SELECT id,title FROM suggestions WHERE status='pending' AND handled_hint IS NULL AND created_at>=? AND (due IS NULL OR due!=?) "
                "AND (deliver_after IS NULL OR deliver_after<=?) ORDER BY urgent DESC,created_at DESC LIMIT 20", (utc(since), local.date().isoformat(), utc(current)))]
            # What waits for the owner (waiting_count, the app's badge), in the dashboard's order (notify.open_order): the
            # ready ones (prepared, the dashboard's Ready) lead the digest; the rest is its "Waiting for you", without
            # what an earlier part already listed (notify.compose), so a pile still gets one
            later = still_needed.folded(db, utc(current), local_tz())  # a Still needed? left unanswered waits in Later
            top = notify.open_order([dict(r) for r in db.execute(
                "SELECT id,title,status,due,due_at,created_at,event_ids FROM suggestions WHERE status IN ('pending','prepared') AND NOT " + NOT_FOR_OWNER_SQL + " "
                "AND (deliver_after IS NULL OR deliver_after<=?) LIMIT 2000", (utc(current),)) if r['id'] not in later], local)
            ready = [r for r in top if r['status'] == 'prepared']
            total = waiting_count(db)
            pace = clear_pace.line(total, clear_pace.seconds(db, current))  # "4 ready · about 2 min", as To-dos says it
            show = security_levels.notify_text(db, False)
        promised = notify.promised_today(self.store.promises(), top, local.date().isoformat(), lambda p: promise_text(p)[0])
        root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/') if self.config.get('dashboard_host') else ''
        when = lambda iso: locale_prefs.clock_text(dt.datetime.fromisoformat(iso).astimezone(local_tz()))
        return notify.compose(meetings, due, overnight, root, show, when, None, total, top, ready, promised, pace)

    def digest_step(self, current=None, push=None, telegram_send=None, mail=None):
        """Send the morning digest once on a work day, at its time, on the channels the owner picked."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        day = local.date().isoformat()
        with self.store.connect() as db:
            notify.ensure(db)
            prefs = notify.prefs(db)['digest']
            if not any(prefs.values()):
                return None
            sent = notify.digest_sent(db, day)
        if not notify.digest_due(local, self.config.get('digest_at', '08:30'), WORK_HOURS['start'], WORK_HOURS['end'], is_work_day, sent):
            return None
        with self.store.connect() as db:
            if not notify.digest_claim(db, day, now()):
                return None
        digest = self.digest(current)
        went = []
        if digest:
            if prefs.get('push'):
                subscriptions, phones = push_reach(self.store, self.config)
                if subscriptions or phones:
                    payload = {**digest['push'], **({'silent': True} if notify.active() else {}),  # at the dashboard: no buzz
                               '_line': digest['push']['title'], '_body': digest['push']['body'],  # the mobile app asks for these
                               'actions': quick_web('view')}
                    if push_send(self.store, self.config, subscriptions, payload, 'digest', push, wake='digest'):
                        went.append('push')
            if prefs.get('telegram') and telegram_on(self.config):
                try:
                    (telegram_send or (lambda text: telegram_request(self.config, {'action': 'send', 'channel': 'telegram', 'accountId': telegram_account(self.config),
                                                                                  'target': self.config.get('telegram_owner'), 'message': recap_escape(text),
                                                                                  'presentation': {'blocks': [{'type': 'buttons', 'buttons': []}]}})))(digest['text'])
                    went.append('telegram')
                except (DeliveryNotSent, subprocess.TimeoutExpired, ValueError) as error:
                    LOG.warning('digest telegram error=%s', type(error).__name__)
            target = prefs.get('email') and self.notify_mail_target()
            if prefs.get('email') and not target:
                LOG.info('digest email skipped reason=not_paired')
            if target and (mail or notify.mail)(target[0], target[1], digest['subject'], digest['text']):
                went.append('email')
        with self.store.connect() as db:
            notify.digest_done(db, day, 'sent' if went else 'empty' if not digest else 'not_sent', went)
        LOG.info('digest day=%s channels=%s', day, ','.join(went) or '-')
        return went

    def waiting_handoffs_text(self):
        """Teammates' handoffs waiting for the owner, for the review (silent acceptance); nothing when off the Network."""
        try:
            return self.fleet.waiting_handoffs_text() if getattr(self, 'fleet', None) else ''
        except Exception as error:  # the review goes on without them
            LOG.warning('waiting handoffs error=%s', type(error).__name__)
            return ''

    def split_notes_text(self):
        """Proposed follow-up splits whose meeting has notes to read, for the review; nothing when off the Network."""
        try:
            return self.fleet.split_notes_text() if getattr(self, 'fleet', None) else ''
        except Exception as error:  # the review goes on without them
            LOG.warning('split notes error=%s', type(error).__name__)
            return ''

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

    def ai_card(self, who, text, area, due=None, draft=None):
        """A to-do a connected AI added (ai_app.py, docs/ai-connections.md), made like a Fleet request's (fleet_card): its
        first evidence is an event on one of the owner's accounts in that area, marked reviewed so no review or
        preparation reads it by itself, and it says which AI it is from. With a draft, an email draft from one of the
        owner's mail accounts in that area, which goes out only with the owner's own Send."""
        accounts = [a for a in self.config.get('accounts', []) if area is None or graph.account_side(a) == area]
        if draft:
            accounts = [a for a in accounts if mail_account(a)]
        elif not accounts:  # nothing placed in that area yet: a to-do sends nothing, so it goes on the Machine's own account
            accounts = self.config.get('accounts', [])[:1]
        if not accounts:
            raise ValueError('No Gmail or Outlook account here to write it from' if draft else 'No account here for this')
        account = accounts[0]['id']
        stamp, key = now(), 'ai:' + uuid.uuid4().hex[:16]
        name = ' '.join(str(who or 'AI').split())[:60]
        title = owner_title(text)
        body = text if not draft else i18n.t('{} wrote this email for you. Read it, change it if you like, and send it yourself.', name) + (
            '\n\n' + text if text != draft['subject'] else '')
        meta = {'sender_display': i18n.t('{} (connected AI)', name), 'ai_connection': name}
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                       "VALUES(?,?,'ai.request',?,?,?,?,0,?,1,1,?)",
                       (account, key, stamp, title, text, json.dumps(meta), hashlib.sha256(text.encode()).hexdigest(), stamp))
            event_id = db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account, key)).fetchone()[0]
        card = self.store.suggest(key, (i18n.t('Email to {}: {}', ', '.join(draft['to'])[:60], draft['subject']) if draft else title)[:90],
                                  body[:700], [event_id], when='now', work=(graph.account_side(accounts[0]) or area) == 'work', due=due)
        if not card.get('duplicate'):  # the owner asked for it, as with New card (owner_card): on their list now, not held for a work day
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET deliver_after=NULL WHERE id=?', (card['id'],))
        if draft and not card.get('duplicate'):
            action = next_actions.validate({'kind': 'email', 'label': 'Send', 'account_id': account, 'to': draft['to'],
                                            'subject': draft['subject'], 'body': draft['body']}, self.config, [account])
            with self.store.connect() as db:
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=? AND status='pending'", (card['id'],))
            self.store.prepare(card['id'], body[:1000], next_action=action, outcome={'state': 'needs_you', 'needs': 'read and send the email'})
        return card['id']

    def new_card(self, args):
        """New card: what the owner typed, with optional Work or Personal, a due date (YYYY-MM-DD; the dashboard reads
        "Friday" or "in 2 weeks" into one) and, when the owner gave a time ("15:00", "in 2 hours"), due_at, people, organizations or a project from the Graph, and emails to attach.
        It is a normal card (Store.owner_card); the next review fills it in."""
        accounts = self.config.get('accounts', [])
        if not accounts:
            raise ValueError('Connect a source first')
        scope = args.get('scope') or None
        if scope not in (None, 'work', 'personal'):
            raise ValueError('scope is work or personal')
        try:
            attach = list(dict.fromkeys(int(i) for i in args.get('attach') or []))
        except (TypeError, ValueError):
            raise ValueError('attach is a list of event ids') from None
        wanted = list(dict.fromkeys(str(i) for i in args.get('about') or []))
        if len(attach) > 5 or len(wanted) > 5:
            raise ValueError('Up to five people and five emails')
        known = {a['id'] for a in accounts}
        with self.store.connect() as db:
            found = {r['id']: r['account_id'] for r in db.execute(
                f"SELECT id,account_id FROM events WHERE deleted=0 AND id IN ({','.join('?' * len(attach)) or 'NULL'})", attach)}
            nodes = {r['id']: dict(r) for r in db.execute(
                f"SELECT id,kind,name FROM graph_nodes WHERE id IN ({','.join('?' * len(wanted)) or 'NULL'})", wanted)}
        if set(found) != set(attach) or not set(found.values()) <= known:
            raise ValueError('That email is no longer there')
        if set(nodes) != set(wanted):
            raise ValueError('That person is no longer in the Graph')
        about = [{'id': n['id'], 'name': n['name'][:120], 'kind': n['kind']} for n in (nodes[i] for i in wanted) if n['kind'] in ('person', 'org')]
        project = next((nodes[i]['name'] for i in wanted if nodes[i]['kind'] == 'project'), None)
        work_ids = [a['id'] for a in accounts if suggestion_scope([a['id']], accounts) == 'work']
        personal_ids = [a['id'] for a in accounts if a['id'] not in work_ids]
        if scope == 'work' and not work_ids:
            raise ValueError('No work account is connected')
        if scope == 'personal' and not personal_ids:
            raise ValueError('No personal account is connected')
        area_open = []
        if scope == 'work':
            account = work_ids[0]
        elif scope == 'personal':
            account = personal_ids[0]
        elif attach:
            account = found[attach[0]]
        else:  # no area given: where it belongs, from its people, organizations and words (owner_card_area)
            with self.store.connect() as db:
                account, area_open = owner_card_area(db, accounts, wanted, args.get('text') or '')
        work = any(a['id'] == account and str(a.get('boundary') or '').startswith('work:') for a in accounts)
        due, due_at = args.get('due') or None, args.get('due_at') or None
        try:  # a day (the owner's own calendar day), and a moment when they gave a time ("15:00", "in 2 hours")
            due = due and dt.date.fromisoformat(str(due)).isoformat()
            when = due_at and dt.datetime.fromisoformat(str(due_at))
        except ValueError:
            raise ValueError('due is YYYY-MM-DD and due_at a time with its offset') from None
        if when and when.tzinfo is None:
            raise ValueError('due_at needs its offset')
        due_at = when and when.astimezone(dt.timezone.utc).isoformat(timespec='minutes')
        if due_at and not due:
            raise ValueError('due_at goes with due, its day')
        files = args.get('files') or []
        if files and not isinstance(files, list):
            raise ValueError('files is a list of file ids')
        draft = 'new:' + str(args.get('draft') or '')
        texts = {}
        if files:  # what the PDFs and text files say, read here for the review (chat_files.texts); nothing leaves the Machine
            with self.store.connect() as db:
                texts = chat_files.texts(db, self.config, draft, files)
        saved = self.store.owner_card(args.get('text'), account, work=work, due=due, about=about, attach=attach, project=project,
                                      files=(draft, files) if files else None, due_at=due_at,
                                      area_open=area_open, file_texts=texts)
        if about and getattr(self, 'graph_dirty', None):
            self.graph_dirty.set()  # the card shows on their Graph page after the next build
        return saved

    def handoff_email(self, card_id, email, title, summary, keep=None, take=None, name=''):
        """Hand a Work card to someone who is not on The Machine: an ordinary email draft on the card, from the card's
        Gmail or Outlook account, built from what the owner ticked (handoff_mail.py), for the owner to read and send.
        Nothing about the task leaves this Machine until the owner sends it, or approves a task page for it
        (task_pages.py), which this offers on the card."""
        made = self.handoff_mail.prepare(card_id, email, name, title, summary, keep, take)
        self.task_pages.offer(made['card_id'], made['task'])
        return {'card_id': made['card_id']}

    def task_import(self, link):
        """Add a task someone sent by email (task_invites.py) as a card, and say who sent it so the owner can connect
        with them on the Network. Works without being on the Network: the link alone opens it."""
        invite_id, key = task_invites.parse_link(link)
        network = getattr(self, 'fleet', None)
        if network:  # signed in, so the Network can count it as added by this Machine
            found = network.relay.call('POST', '/task-invite', {'action': 'claim', 'id': invite_id})
        else:
            found = task_invites.claim(task_invites.network_url(self.config, fleet), invite_id)
        task = task_invites.unseal(str(found.get('sealed') or ''), key)
        who = found.get('from') or {}
        name = ' '.join(str(who.get('name') or task.get('from_name') or 'Someone').split())[:60]
        body = (task.get('summary') or task['title']) + (f"\n\nThey'd like it by {task['due']}." if task.get('due') else '')
        body += f'\n\n{name} sent this by email. Answer them there.'
        card_id = self.fleet_card('task', 'task:' + invite_id, name, task['title'], body, [], due=task.get('due'), via='by email')
        if network:
            try:
                network.relay.call('POST', '/task-invite', {'action': 'added', 'id': invite_id})
            except (ValueError, OSError):
                LOG.warning('task invite local card saved; remote addition receipt unavailable')
        username = who.get('username') if isinstance(who.get('username'), str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{1,28}[a-z0-9]', who['username']) else None
        connected = False
        if network and username:  # a friend already, or in a Work or Family Fleet together: nothing to connect
            ref = network.friends_ref()
            friends = {str(m.get('username') or '').lower() for m in network.teammates(ref)} if ref else set()
            connected = username in friends or network.in_my_fleet(network.fleet_mates(), username)
        return {'card_id': card_id, 'from': {'name': name, 'username': username}, 'can_connect': bool(network and username and not connected)}

    def skills_find_start(self, token, items, sites=None, more=False):
        """Find my skills on the service: reads the owner's own skills from claude.ai and chatgpt.com (`sites`: only
        those) in the Machine's own browser, then a turn judges which listed skills would help with this Machine's
        actual work. One at a time. `more`: looking again after the owner signed in to one."""
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone():
                return None  # another turn of this kind is on; the list still shows what is on this computer
            since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=30)).isoformat()
            cards = [r[0] for r in db.execute('SELECT title FROM suggestions WHERE created_at>? ORDER BY created_at DESC LIMIT 40', (since,))]
            run_id, started = uuid.uuid4().hex, now()
            evidence = {'token': token, 'cards': cards, 'sites': [s for s in (sites or SKILLS_SITES) if s in SKILLS_SITES], 'more': bool(more),
                        'sources': sorted({str(a.get('service') or '') for a in self.config.get('accounts', []) if a.get('service')}),
                        'skills': sorted(self.skills.mine())[:60]}
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind) VALUES(?,'starting',?,?,?,'skills')",
                       (run_id, started, started, json.dumps(evidence)))
        return run_id

    def skills_read(self, sites):
        """The owner's own skills on claude.ai and chatgpt.com, read in the Machine's browser: a tab straight on each
        site's skills page (SKILLS_PAGES), SKILLS_READ run there, the tab closed again. {'chatgpt': {'state': 'ok' |
        'signed_out' | 'unavailable', 'skills': [...], 'where': <page>, 'detail': …}}. Read-only; nothing is clicked."""
        try:
            base = browser_login.endpoints(self.config)[0]
        except (IndexError, TypeError):
            return {s: {'state': 'unavailable', 'where': SKILLS_PAGES[s], 'detail': 'the Machine’s browser isn’t running'} for s in sites}
        cdp = browser_login.browser_cdp

        def read(site):
            seen = {'where': SKILLS_PAGES[site]}
            try:
                tab = cdp.open_tab(base, SKILLS_PAGES[site])
            except (cdp.CdpError, OSError):
                return {**seen, 'state': 'unavailable', 'detail': 'the Machine’s browser didn’t open it'}
            try:
                for _ in range(25):  # up to ~25 seconds for the page to load its own origin
                    time.sleep(1)
                    try:
                        if cdp.evaluate(base, tab, "() => location.hostname + ' ' + document.readyState", timeout_ms=3000) == SKILLS_SITES[site] + ' complete':
                            break
                    except (cdp.CdpError, OSError):
                        pass
                got = cdp.evaluate(base, tab, SKILLS_READ[site], timeout_ms=120000)
            except (cdp.CdpError, OSError):
                return {**seen, 'state': 'unavailable', 'detail': 'the page didn’t answer'}
            finally:
                try:
                    cdp.close_tab(base, tab)
                except (cdp.CdpError, OSError):
                    pass
            if not isinstance(got, dict) or got.get('state') not in ('ok', 'signed_out', 'unavailable'):
                return {**seen, 'state': 'unavailable', 'detail': 'the page didn’t answer'}
            skills = [f for f in got.get('skills') or [] if isinstance(f, dict)][:60]
            out = {**seen, 'state': got['state'], 'skills': skills}
            if got['state'] == 'ok' and not skills:
                out['detail'] = (f"{got.get('failed')} couldn’t be downloaded" if got.get('failed') else 'none you made or uploaded yourself')
            elif got.get('detail'):
                out['detail'] = str(got['detail'])[:120]
            return out
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            return dict(zip(sites, pool.map(read, sites)))

    def skills_signin(self, site):
        """Sign in to ChatGPT or claude.ai for Find my skills: its sign-in page in front in the Machine's browser, for
        the dashboard's sign-in dialog. Nothing is typed here."""
        if site not in SKILLS_SIGNIN:
            raise ValueError('Which account?')
        try:
            base = browser_login.endpoints(self.config)[0]
            tab = browser_login.browser_cdp.open_tab(base, SKILLS_SIGNIN[site])
        except (browser_login.browser_cdp.CdpError, OSError, IndexError):
            raise ValueError('I couldn’t open the sign-in page in the browser') from None
        self.__dict__.setdefault('skills_signin_tabs', {})[site] = tab
        try:
            browser_viewer.focus(SKILLS_SIGNIN[site], base)
        except (ValueError, OSError):
            pass
        return {'opened': True, 'site': SKILLS_SITES[site], 'view': browser_link(self.config)}

    def skills_found(self, args):
        run_id = str(args.get('run') or '')
        with self.store.connect() as db:
            run = db.execute("SELECT evidence FROM profile_runs WHERE run_id=? AND kind='skills' AND status IN ('starting','running')", (run_id,)).fetchone()
            if not run:
                raise ValueError('This Find my skills run is no longer active')
            db.execute('UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=?', (json.dumps({'reported': True}), now(), run_id))
        token = json.loads(run['evidence'])['token']
        return self.skills.importer.report(token, args.get('found'), args.get('recommended'), args.get('browser'))

    def is_work(self, account_ids):
        if isinstance(account_ids, str):
            account_ids = json.loads(account_ids or '[]')
        return any(a['id'] in (account_ids or []) and a.get('boundary', '').startswith('work:') for a in self.config.get('accounts', []))

    def is_work_suggestion(self, suggestion_id):
        with self.store.connect() as db:
            row = db.execute('SELECT account_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        return bool(row) and self.is_work(row['account_ids'])

    def feedback_prompt_step(self, request_id=None, sender=None):
        """Durable prompt admission, receipt recovery and conservative ambiguous-send hold."""
        sender=sender or self.native_change_prompt
        stamp=now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not telegram_on(self.config):
                # No Telegram chat to ask in: the dashboard takes the change request itself.
                db.execute("UPDATE feedback_prompts SET status='cancelled' WHERE status NOT IN ('sent','cancelled')")
                return
            db.execute("UPDATE feedback_prompts SET status='cancelled' WHERE status!='sent' AND NOT EXISTS(SELECT 1 FROM suggestions s WHERE s.id=feedback_prompts.suggestion_id AND s.feedback_request_id=feedback_prompts.request_id AND s.feedback_until>? AND s.status NOT IN ('completed','rejected') AND (feedback_prompts.kind='dismiss' OR s.status!='snoozed'))",(stamp,))
            row=db.execute("SELECT * FROM feedback_prompts WHERE status NOT IN ('sent','cancelled') AND (retry_at IS NULL OR retry_at<=?)"+(' AND request_id=?' if request_id else '')+' ORDER BY created_at LIMIT 1', (stamp,request_id) if request_id else (stamp,)).fetchone()
            if not row:return
            row=dict(row)
            if row['status'] in ('native_sending','plain_sending') and row['updated_at']>(dt.datetime.fromisoformat(stamp)-dt.timedelta(seconds=75)).isoformat() and not self.prompt_receipt_file(row):return
            if row['retry_at'] and row['retry_at']>stamp:return
            if row['status'] in ('uncertain','native_sending','plain_sending'):
                # No receipt is not proof of non-delivery. Only positive evidence binds.
                message_id=self.recovered_prompt_receipt(row)
                if message_id:
                    db.execute("UPDATE feedback_prompts SET status='sent',message_id=?,error=NULL,updated_at=? WHERE request_id=?",(message_id,stamp,row['request_id']))
                    db.execute('UPDATE suggestions SET feedback_prompt_message_id=? WHERE id=? AND feedback_request_id=? AND feedback_until>?',
                        (message_id,row['suggestion_id'],row['request_id'],stamp))
                else:db.execute("UPDATE feedback_prompts SET status='uncertain',error='prompt_outcome_unknown',retry_at=? WHERE request_id=?",
                    ((dt.datetime.fromisoformat(stamp)+dt.timedelta(seconds=30)).isoformat(),row['request_id']))
                return
            if row['status']=='queued' and hasattr(self,'stop') and self.stop.is_set():return
            mode='plain' if row['status']=='plain_queued' else 'native'
            db.execute('UPDATE feedback_prompts SET status=?,updated_at=?,attempted_at=? WHERE request_id=?',
                       (mode+'_sending',stamp,stamp,row['request_id']))
        result=None
        try:
            if mode=='native':result=sender(row)
            else:result=telegram_request(self.config,{'action':'send','channel':'telegram','accountId':telegram_account(self.config),'target':self.config.get('telegram_owner'),
                'message':prompt_text(row['title'],plain=True,kind=row.get('kind') or 'change'),'replyTo':row['card_id']})
        except DeliveryNotSent:
            result={'definitely_not_sent':True}
        except (ValueError,OSError,subprocess.TimeoutExpired):
            result={}
        if result and re.fullmatch(r'\d+',str(result.get('messageId',''))):
            self.save_prompt_receipt(row,str(result['messageId']))
            self.store.bind_feedback_prompt(row['suggestion_id'],row['request_id'],result['messageId'])
            return 'sent'
        with self.store.connect() as db:
            # Plain fallback is safe only when native setup never entered send.
            status='plain_queued' if result and result.get('definitely_not_sent') else 'uncertain'
            db.execute('UPDATE feedback_prompts SET status=?,error=?,retry_at=?,updated_at=? WHERE request_id=? AND status=?',
                (status,'prompt_not_sent' if status=='plain_queued' else 'prompt_outcome_unknown',
                 (dt.datetime.fromisoformat(stamp)+dt.timedelta(seconds=10 if mode=='native' and status=='plain_queued' else 60)).isoformat(),now(),row['request_id'],mode+'_sending'))
        return status

    def feedback_prompt_safe(self,request_id=None):
        try:self.feedback_prompt_step(request_id=request_id)
        except Exception as error:LOG.error('Change prompt delivery error=%s',type(error).__name__)

    def prompt_receipt_dir(self):
        return Path(self.config.get('prompt_receipts',str(Path.home()/'.local/share/personal-assistant/prompt-receipts')))

    def save_prompt_receipt(self,row,message_id):
        folder=self.prompt_receipt_dir()
        folder.mkdir(parents=True,exist_ok=True,mode=0o700)
        dest=folder/(hashlib.sha256(row['request_id'].encode()).hexdigest()+'.json')
        temp=dest.with_suffix('.tmp')
        with temp.open('w') as stream:
            os.chmod(temp,0o600);json.dump({'messageId':message_id},stream);stream.flush();os.fsync(stream.fileno())
        temp.replace(dest)

    def prompt_receipt_file(self,row):
        folder=self.prompt_receipt_dir()
        path=folder/(hashlib.sha256(row['request_id'].encode()).hexdigest()+'.json')
        try:
            receipt=json.loads(path.read_text())
            if re.fullmatch(r'\d+',str(receipt.get('messageId',''))):return str(receipt['messageId'])
        except (OSError,ValueError):pass
        return None

    def recovered_prompt_receipt(self,row):
        message_id=self.prompt_receipt_file(row)
        if message_id:return message_id
        path=self.config.get('openclaw_state',str(Path.home()/'.openclaw/state/openclaw.sqlite'))
        try:
            with contextlib.closing(sqlite3.connect('file:'+path+'?mode=ro',uri=True,timeout=2)) as native:
                found=set()
                for value, in native.execute("SELECT value_json FROM plugin_state_entries WHERE plugin_id='telegram' AND namespace='telegram.message-cache'"):
                    msg=json.loads(value).get('sourceMessage',{})
                    if (str(msg.get('chat',{}).get('id'))!=self.config.get('telegram_owner') or not msg.get('from',{}).get('is_bot')
                        or not msg.get('message_id') or (msg.get('date') or 0)<int(dt.datetime.fromisoformat(row.get('attempted_at') or row['created_at']).timestamp())
                        or str(msg.get('reply_to_message',{}).get('message_id'))!=row['card_id']):continue
                    if msg.get('text') in (prompt_text(row['title'],kind=row.get('kind') or 'change'),prompt_text(row['title'],plain=True,kind=row.get('kind') or 'change')):found.add(str(msg['message_id']))
                if len(found)==1:return found.pop()
        except (sqlite3.Error,OSError,ValueError):pass
        return None

    def native_change_prompt(self,row):
        request={'receipt_key':hashlib.sha256(row['request_id'].encode()).hexdigest(),'card_id':row['card_id'],'text':prompt_text(row['title'],kind=row.get('kind') or 'change'),
                 'target':str(self.config.get('telegram_owner'))}
        try:
            env={**node_env(self.config),'ASSISTANT_PROMPT_RECEIPTS':os.path.abspath(self.prompt_receipt_dir())}  # where receipts go: the service's, never the request's
            result=subprocess.run([node_bin(self.config),str(ROOT/'change-prompt-run.mjs')],env=env,input=encoded(request),capture_output=True,text=True,timeout=60)
            reply=json.loads(result.stdout)
            if reply.get('definitely_not_sent'):
                # e.g. OpenClaw helpers removed or renamed by an update: visible, then the plain prompt.
                LOG.warning('native Change prompt unavailable; using plain prompt')
            return reply
        except OSError:return {'definitely_not_sent':True}
        except (ValueError,subprocess.TimeoutExpired):return {}

    def delivery_worker(self):
        while not self.stop.wait(10):
            if not self.config.get('delivery_enabled', False):
                continue
            try:
                self.feedback_prompt_step()
                deliver(self.store, self.config)
                self.notify_step()
                self.digest_step()
                app_clear_step(self.store, self.config)  # notifications on phones for what no longer waits
            except Exception as error:
                LOG.error('delivery error=%s', type(error).__name__)

    def action_step(self,transport=None):
        transport=transport or next_actions.ActionTransport(next_actions.EmailTransport(self.config,credential,gog_read),next_actions.LinkedInTransport(self.config),next_actions.SlackTransport(self.config,credential),next_actions.XTransport(self.config),next_actions.MergeTransport(self.config,restart_self),next_actions.WhatsAppTransport(self.config),intercom_transport(self.config),calendar_writes.CalendarTransport(self.config,credential,gog_read),docs_transport(self.config),next_actions.TelegramTransport(self.config),docs_write_transport(self.config))
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for candidate in db.execute("SELECT j.id,j.revision,s.status,s.next_action FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id WHERE j.status IN ('queued','blocked')").fetchall():
                if candidate['status']!='prepared' or not next_actions.selected(candidate['next_action'],candidate['revision']):
                    db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE id=?",(now(),candidate['id']))
            job=None
            for found in db.execute("SELECT * FROM action_jobs WHERE status IN ('queued','sending','uncertain') AND (retry_at IS NULL OR retry_at<=?) ORDER BY created_at",(now(),)).fetchall():
                # Automated follow-ups in a row: the next from the same account waits its gap (follow_ups.SEND_GAP); another account's goes
                # A paused board or project: Send without asking and sends queued before the pause wait (follow_ups.paused_send)
                # Only on work days: Send without asking queued for a day off waits for the next work day (follow_ups.off_day_send)
                held=(follow_ups.held_until(db,found['id'],now()) or follow_ups.paused_send(db,found['id'],now()) or follow_ups.off_day_send(db,found['id'],now(),self.follow_up_work())) if found['status']=='queued' else None
                if held:db.execute('UPDATE action_jobs SET retry_at=? WHERE id=?',(held,found['id']));continue
                job=found;break
            if not job:return
            job=dict(job);action=json.loads(job['payload'])
        if job['status'] in ('sending','uncertain'):
            # Read outside a transaction. Positive Sent-mail identity recovers an
            # interrupted send; no-match/ambiguity never permits resending.
            try:result=transport.reconcile(action,job)
            except Exception:result={}
            with self.store.connect() as db:
                if result.get('message_id'):
                    if db.execute("UPDATE action_jobs SET status='sent',message_id=?,error=NULL,updated_at=? WHERE id=? AND status IN ('sending','uncertain')",(result['message_id'],now(),job['id'])).rowcount and action['kind'] in VERIFIED_KINDS:
                        note_first(db,'first_verified_action',action['kind'])  # the provider confirmed it (first_cards_report)
                    queue_thread_snooze(db,action,job);queue_delegate_wait(db,action,job,result);self.handoff_mail.sent(db,action,job,result)
                    if action['kind']=='doc_write':settle_doc_write(self.store,db,job['suggestion_id'],job['id'],action,result.get('url'))
                    elif action['kind']!='merge':settle_sent(self.store,db,job['suggestion_id'],job['id'],next_actions.label(action),calendar_writes.done(action) if action['kind']=='calendar' else doc_writes.done(action) if action['kind']=='doc_write' else None)
                    if action['kind']=='merge' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'merge',encoded(result),'pending',now()))
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                else:
                    # Keep checking Sent mail, every five minutes for a day, then hourly.
                    wait=dt.timedelta(minutes=5 if dt.datetime.fromisoformat(job['created_at'])>dt.datetime.fromisoformat(now())-dt.timedelta(days=1) else 60)
                    db.execute("UPDATE action_jobs SET status='uncertain',error=?,retry_at=? WHERE id=? AND status IN ('sending','uncertain')",('I couldn’t confirm whether the fix was merged. I’m checking the code; I won’t merge it again.' if action['kind']=='merge' else doc_writes.UNCLEAR if action['kind']=='doc_write' else 'I couldn’t confirm the calendar change. I’m checking the calendar; I won’t make it twice.' if action['kind']=='calendar' else 'I couldn’t confirm whether this X '+('reply' if action.get('reply_to') else 'message')+' was sent. I’m checking X; I won’t send it again.' if action['kind']=='x' else 'I couldn’t confirm whether this WhatsApp message was sent. I’m checking the chat; I won’t send it again.' if action['kind']=='whatsapp' else 'I couldn’t confirm whether this Telegram message was sent. I’m checking the chat; I won’t send it again.' if action['kind']=='telegram' else 'I couldn’t confirm whether this Intercom reply was sent. I’m checking the conversation; I won’t send it again.' if action['kind']=='intercom' else 'I couldn’t confirm whether this doc reply was posted. I’m checking the comment; I won’t post it again.' if action['kind']=='doc_reply' else 'I couldn’t confirm whether this '+('LinkedIn' if action['kind']=='linkedin' else 'Slack')+' message was sent. I’m checking the conversation; I won’t send it again.' if action['kind'] in ('linkedin','slack') else 'I couldn’t confirm whether this email was sent. I’m checking Sent mail; I won’t send it again.',(dt.datetime.fromisoformat(now())+wait).isoformat(),job['id']))
            if result.get('message_id') and action['kind']=='merge':
                self.merge_effect(job,action,result,'merge',transport.pick(action) if hasattr(transport,'pick') else transport)
            return
        try:transport.preflight(action)
        except next_actions.LinkedInBusy:
            # The shared browser is in use: wait, nothing was sent and the approval stands.
            with self.store.connect() as db:
                db.execute("UPDATE action_jobs SET retry_at=?,updated_at=? WHERE id=? AND status='queued'",((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=2)).isoformat(),now(),job['id']))
            return 'waiting'
        except Exception as error:
            reason=str(error) if isinstance(error,ValueError) else 'The fix could not be checked. Nothing was merged.' if action['kind']=='merge' else 'The doc could not be checked. Nothing was changed.' if action['kind']=='doc_write' else 'The calendar could not be checked. Nothing was changed.' if action['kind']=='calendar' else ({'linkedin':'LinkedIn','slack':'Slack','x':'X','whatsapp':'WhatsApp','telegram':'Telegram','intercom':'Intercom','doc_reply':'The doc'}.get(action['kind'],mailbox_name(self.config,action))+' could not be checked. Nothing was sent.')
            with self.store.connect() as db:
                stamp=now()
                if db.execute("UPDATE action_jobs SET status='blocked',error=?,updated_at=? WHERE id=? AND status='queued'",(reason,stamp,job['id'])).rowcount:
                    activity_log.note_block(db,job['id'],reason,stamp)  # Activity keeps the block as history (activity_log.py)
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
            return 'blocked'
        # An automated follow-up: the thread read again, right before it goes; anything new since the draft holds it (follow_ups.py)
        recheck=self.follow_up_recheck(job,action)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            current=db.execute("SELECT j.status,s.status suggestion_status,s.next_action FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id WHERE j.id=?",(job['id'],)).fetchone()
            if not current or current['status']!='queued':return
            if current['suggestion_status']!='prepared' or not next_actions.selected(current['next_action'],job['revision']):
                db.execute("UPDATE action_jobs SET status='cancelled' WHERE id=?",(job['id'],));return
            if recheck and recheck[0]=='bounced':
                follow_ups.hold_bounced(db,job,current['next_action'],recheck[1],now())
                follow_ups.settle(db,now(),self.follow_up_mine())  # no working address: the draft stops ("Email bounced")
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                return 'held'
            if recheck and recheck[0]:
                follow_ups.hold(db,job['id'],job['suggestion_id'],recheck[0],recheck[1],now())
                follow_ups.settle(db,now(),self.follow_up_mine())  # a reply ends the round; the owner's own send counts as this one
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                return 'held'
            if recheck:follow_ups.unhold(db,job['id'])
            # Commit admission before the one write. Later cancellation cannot recall
            # an admitted email, and restart/repeated clicks only reconcile it.
            if action['kind'] in ('whatsapp', 'intercom'):
                action.setdefault('proof', {})[action['kind'] + '_dispatched_at'] = now()
            held=follow_ups.held_until(db,job['id'],now())
            if held:
                db.execute('UPDATE action_jobs SET retry_at=? WHERE id=?',(held,job['id']));return 'waiting'
            db.execute("UPDATE action_jobs SET status='sending',updated_at=?,retry_at=? WHERE id=?",(now(),(dt.datetime.fromisoformat(now())+dt.timedelta(seconds=90)).isoformat(),job['id']))
            follow_ups.going_out(db,job['id'],now())  # claimed with the send: the next follow-up from this account waits, also after a restart
            if action.get('proof'):db.execute('UPDATE action_jobs SET payload=? WHERE id=?',(encoded(action),job['id']))
        try:result=transport.send(action,job)
        except Exception:result={}
        if result.get('not_sent'):
            with self.store.connect() as db:
                db.execute("UPDATE action_jobs SET status='queued',retry_at=?,updated_at=? WHERE id=? AND status='sending'",((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=2)).isoformat(),now(),job['id']))
            return 'waiting'
        with self.store.connect() as db:
            status='sent' if result.get('message_id') else 'failed' if result.get('rejected') else 'uncertain'
            what,where={'linkedin':('this LinkedIn message','LinkedIn'),'slack':('this Slack message','Slack'),'x':('this X '+('reply' if action.get('reply_to') else 'message'),'X'),'whatsapp':('this WhatsApp message','WhatsApp'),'telegram':('this Telegram message','Telegram'),'intercom':('this Intercom reply','Intercom'),'doc_reply':('this doc reply','The doc')}.get(action['kind'],('this email',mailbox_name(self.config,action)))
            error={'sent':None,'failed':f"Last attempt failed: {where} refused {what} (error {result.get('rejected')}). Nothing was sent; change it or try again.",
                   'uncertain':f'I couldn’t confirm whether {what} was sent. I won’t resend it.'}[status]
            if action['kind']=='doc_write':
                error={'sent':None,'failed':doc_writes.failed(action,result.get('rejected'),result.get('reason')),'uncertain':doc_writes.UNCLEAR}[status]
            if action['kind']=='calendar':
                error={'sent':None,'failed':f"Last attempt failed: Google Calendar refused it (error {result.get('rejected')}). Nothing was changed; try again or change it.",
                       'uncertain':'I couldn’t confirm the calendar change. I’m checking the calendar; I won’t make it twice.'}[status]
            if action['kind']=='merge':
                error={'sent':' '.join(note for note in ('Pushing it failed; push it yourself.' if result.get('pushed') is False else
                                                           'Kept on this machine, not pushed upstream: push it or open a pull request if you want to share it.' if result.get('held')=='auto' else
                                                           'Not pushed: earlier changes here aren’t upstream yet, so push them together when you’re ready.' if result.get('held')=='unshared' else '',
                                                           '' if result.get('restarted') else 'Restart The Machine to use it.') if note) or None,
                       'failed':'The fix no longer applies to the running code. Nothing was merged; tap Change to redo it.',
                       'uncertain':'I couldn’t confirm whether the fix was merged. I won’t merge it again.'}[status]
            db.execute('UPDATE action_jobs SET status=?,message_id=?,error=?,updated_at=?,retry_at=?,rfc_message_id=COALESCE(?,rfc_message_id) WHERE id=?',
                (status,result.get('message_id'),error,now(),None if status=='failed' else (dt.datetime.fromisoformat(now())+dt.timedelta(minutes=5)).isoformat(),
                 result.get('rfc_message_id') if status=='sent' else None,job['id']))
            if status=='sent':
                if action['kind'] in VERIFIED_KINDS:note_first(db,'first_verified_action',action['kind'])  # the provider accepted it (first_cards_report)
                queue_thread_snooze(db,action,job);queue_delegate_wait(db,action,job,result);self.handoff_mail.sent(db,action,job,result)
                if action['kind']=='doc_write':settle_doc_write(self.store,db,job['suggestion_id'],job['id'],action,result.get('url'))
                elif action['kind']!='merge':settle_sent(self.store,db,job['suggestion_id'],job['id'],next_actions.label(action),calendar_writes.done(action) if action['kind']=='calendar' else doc_writes.done(action) if action['kind']=='doc_write' else None)
            if status=='sent' and action['kind']=='merge' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'merge',encoded(result),'pending',now()))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
        if status=='sent' and action['kind']=='merge':
            self.merge_effect(job,action,result,'merge',transport.pick(action) if hasattr(transport,'pick') else transport)
        return status

    def merge_effect(self,job,action,receipt,operation,merge):
        """Durable receipt precedes optional effects; recovery never repeats a Git mutation."""
        if not hasattr(merge,'complete'):return
        with self.store.connect() as db:
            db.execute('INSERT INTO merge_effects VALUES(?,?,?,?,?) ON CONFLICT(action_id,operation) DO NOTHING',
                       (job['id'],operation,encoded(receipt),'pending',now()))
        with self.store.connect() as db:
            saved=db.execute('SELECT receipt,status FROM merge_effects WHERE action_id=? AND operation=?',(job['id'],operation)).fetchone()
        if saved['status']=='done':return
        receipt=json.loads(saved['receipt'])
        result=merge.complete(action,receipt,operation)
        with self.store.connect() as db:
            db.execute("UPDATE merge_effects SET status='done',receipt=?,updated_at=? WHERE action_id=? AND operation=?",(encoded({**receipt,**result}),now(),job['id'],operation))
        # Both the Git outcome and push bookkeeping are durable BEFORE restart is requested.
        result['restarted']=bool(result.get('activation_ready') and merge.restart and merge.restart())
        notes=[]
        if result.get('pushed') is False:notes.append('Pushing it failed; push it yourself.')
        elif result.get('held')=='auto':notes.append('Kept on this machine, not pushed upstream: push it or open a pull request if you want to share it.')
        elif result.get('held')=='unshared':notes.append('Not pushed: earlier changes here aren’t upstream yet, so push them together when you’re ready.')
        if not result.get('restarted'):notes.append('Restart The Machine to use '+('the previous code.' if operation=='undo' else 'it.'))
        with self.store.connect() as db:
            db.execute("UPDATE merge_effects SET receipt=?,updated_at=? WHERE action_id=? AND operation=?",(encoded({**receipt,**result}),now(),job['id'],operation))
            prior=(job.get('error') or 'Merge undone.') if operation=='undo' else None
            if operation=='undo' and result.get('restarted'):prior+=' The Machine restarts on the previous code.'
            db.execute('UPDATE action_jobs SET error=? WHERE id=?',(' '.join(([prior] if prior else [])+notes) or None,job['id']))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))

    def merge_effect_step(self):
        with self.store.connect() as db:
            row=db.execute("SELECT j.*,e.operation,e.receipt FROM merge_effects e JOIN action_jobs j ON j.id=e.action_id WHERE e.status='pending' LIMIT 1").fetchone()
        if row:
            job=dict(row);self.merge_effect(job,json.loads(job['payload']),json.loads(job['receipt']),job['operation'],next_actions.MergeTransport(self.config,restart_self))

    def skills_from_notes_prompt(self):
        """The condense pass's line on turning notes into a skill: the skills here first, by name and what each is for,
        so the review judges by meaning whether one already does that job (update it) or sits next to it (related)."""
        try:
            on_hand = self.skills_on_hand()
        except Exception:
            on_hand = []
        listed = '\n'.join(f"- {s['name']}: {s['description']}" + (" (a teammate's: can be related, never updated)" if s['origin'] == 'shared' else '')
                           for s in on_hand)[:4000]
        return (f"\nWhen {SKILL_NOTES_MIN} or more notes are all about one specific kind of task or scenario (not how the owner writes in general), "
                "suggest moving them into a skill: remember_fact kind=skill, name, description=<when to use it, one sentence>, "
                "text=<SKILL.md instructions that keep everything those notes say>, replaces=[their ids]. The owner decides on a card. "
                + ("First check the skills below by what each is for, judging the meaning, not shared words. When one of the owner's own "
                   "already does the same job, add skill=<its name>: you get its instructions back, then send the whole skill rewritten as "
                   "one in text, with what the notes add merged into its own sections (no heading twice, no step said twice), and base=<what "
                   "you got>; the card offers to update that skill. When one is related but a separate job (say the other direction of the "
                   "same exchange), add related=<its name> and relation=<how they relate, one short line>: still a new skill. When none "
                   "is, add new=true.\nSkills here:\n" + listed if on_hand else "They have no skills yet."))

    def propose_skill_from_notes(self, name, description, body, replaces, into=None, related=None, relation=None, new=False, base=None):
        """Notes that are all about one kind of task become a suggestion card. It is checked against the skills here
        first (the review judges that by meaning, from their names and descriptions): when one of the owner's own already
        does the same job (into), the card offers Update <skill>: the review gets its instructions first (rewrite_needed)
        and sends the whole skill rewritten as one with the notes merged in (base names that version); when one is related but a
        separate job (related, e.g. the other direction of an exchange), the card says how in one line (relation) and
        still offers the new skill. Nothing changes until they tap Create skill (or Update, after its before and after);
        Not now isn't asked again until the same notes have grown by SKILL_REGROW."""
        if not getattr(self, 'skills', None):
            raise ValueError('Skills are not set up here')
        name, description, body = skills.validate(name, description, body)
        target, linked, relation = skills.check_against(self.skills_on_hand(), into, related, relation, new)
        if target:  # the whole skill rewritten as one, on the version the review was shown
            asked = skills.rewrite_needed(target, base)
            if asked:
                return asked
            skills.check_rewrite(target['body'], body)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            notes = self.store.replaced_facts(db, replaces)
            if not SKILL_NOTES_MIN <= len(notes) <= 20:
                raise ValueError(f'A skill takes {SKILL_NOTES_MIN} to 20 current notes (replaces=[their ids])')
            ids = {n['id'] for n in notes}
            title = sentences(f'Update {target["name"]} with {len(notes)} notes' if target else f'Turn {len(notes)} notes into a skill: {name}', 90)
            if target:
                text = (sentences(description, 250) + f"\n\nThese {len(notes)} notes fit {target['name']}. Update shows the before and after first; "
                        'only that skill changes. Not now keeps the notes as they are.')
            else:
                text = (sentences(description, 250) + (f"\n\nRelated to {linked['name']}: {relation}" if linked else '')
                        + f"\n\nI can keep these {len(notes)} notes together in a skill. Read the full instructions and notes before deciding. "
                        'Create skill makes it, on, under Skills. Not now keeps them as they are.')
            fields = {'name': name, 'description': description, 'body': body, 'target_id': target and target['id'], 'target_name': target and target['name'],
                      'base_sha': target and target['sha'],
                      'related_id': linked and linked['id'], 'related_name': linked and linked['name'], 'relation': relation if linked else None}
            for old in db.execute("SELECT c.id,c.fact_ids,c.status,c.checked,c.suggestion_id,c.base_sha,k.sha target_sha FROM skill_clusters c "
                                  "LEFT JOIN skills k ON k.id=c.target_id WHERE c.status IN ('pending','accepting','declined')").fetchall():
                before = set(json.loads(old['fact_ids']))
                if len(ids & before) * 2 >= len(before):
                    if old['status'] == 'pending' and (not old['checked'] or not old['base_sha'] and old['target_sha'] or old['base_sha'] and old['base_sha'] != old['target_sha']):
                        # Offered before skills were checked first, as an addition, or on a version of the skill changed since:
                        # the same card, brought up to date.
                        db.execute('UPDATE skill_clusters SET fact_ids=?,' + ','.join(k + '=?' for k in fields) + ',checked=1,updated_at=? WHERE id=?',
                                   (json.dumps(sorted(ids)), *fields.values(), now(), old['id']))
                        db.execute("UPDATE suggestions SET title=?,body=? WHERE id=? AND status='pending'", (title, text[:700], old['suggestion_id']))
                        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (old['suggestion_id'],))
                        return {'id': old['id'], 'suggestion_id': old['suggestion_id'], 'updated': True}
                    if old['status'] != 'declined':
                        return {'id': old['id'], 'duplicate': True}
                    if len(ids) < len(before) + SKILL_REGROW:
                        raise ValueError(f'The owner said Not now to these notes; suggest it again once {SKILL_REGROW} more have joined them')
            cards = [n['suggestion_id'] for n in notes if n['suggestion_id']]
            events = list(dict.fromkeys(i for r in db.execute('SELECT event_ids FROM suggestions WHERE id IN (' + ','.join('?' for _ in cards) + ')', cards)
                                        for i in json.loads(r['event_ids'] or '[]')))[:20] if cards else []
            if not events:
                raise ValueError('These notes have no cards behind them to show as evidence')
            cluster = 'sc_' + secrets.token_hex(6)
            card = self.store.suggest('skill-notes:' + cluster, title, text[:700], events, _db=db)
            db.execute('INSERT INTO skill_clusters(id,fact_ids,' + ','.join(fields) + ",suggestion_id,status,checked,created_at,updated_at) "
                       'VALUES(?,?,' + ','.join('?' for _ in fields) + ",?,'pending',1,?,?)",
                       (cluster, json.dumps(sorted(ids)), *fields.values(), card['id'], now(), now()))
        return {'id': cluster, 'suggestion_id': card['id']}

    def apply_skill_clusters(self):
        """The owner tapped Create skill (or Update <skill>, after its before and after): write the skill with the instructions, and move the notes into it.
        They stay in the database, shown with the skill, and leave the list every task gets."""
        if not getattr(self, 'skills', None):
            return 0
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute("SELECT * FROM skill_clusters WHERE status='accepting'")]
        for offered in rows:
            try:
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    # Dashboard and the worker can both pick the same offer; reconcile under the write lock.
                    c = db.execute("SELECT * FROM skill_clusters WHERE id=? AND status='accepting'", (offered['id'],)).fetchone()
                    if not c:
                        continue
                    if c['target_id']:
                        row = db.execute("SELECT * FROM skills WHERE id=? AND status IN ('on','off') AND origin!='shared'", (c['target_id'],)).fetchone()
                        if not row:
                            raise ValueError('That skill is gone')
                        if c['reviewed_sha'] and row['sha'] != c['reviewed_sha'] or c['base_sha'] and row['sha'] != c['base_sha']:
                            raise ValueError('That skill changed after its before and after were shown')
                        after = c['body'] if c['base_sha'] else skill_update_after(row['body'], c['body'])
                        skill_id = self.skills.save(row['id'], row['name'], row['description'], after, _db=db)
                    else:
                        skill_id = self.skills.save(None, c['name'], c['description'], c['body'], _db=db)
                    ids = json.loads(c['fact_ids'])
                    moved = db.execute('UPDATE facts SET removed_at=?,merged_into=? WHERE removed_at IS NULL AND id IN (' + ','.join('?' for _ in ids) + ')',
                                       (now(), 'skill:' + skill_id, *ids)).rowcount
                    db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'condense',?,?)",
                               (now(), f'Moved {moved} notes into the skill {c["target_name"] or c["name"]}', 'skill:' + skill_id))
                    db.execute("UPDATE skill_clusters SET status='done',skill_id=?,updated_at=? WHERE id=?", (skill_id, now(), c['id']))
            except (ValueError, OSError) as error:
                LOG.error('skill from notes error=%s', type(error).__name__)
                with self.store.connect() as db:
                    db.execute("UPDATE skill_clusters SET status='failed',updated_at=? WHERE id=? AND status='accepting'", (now(), offered['id']))
                    db.execute("UPDATE suggestions SET status='pending' WHERE id=? AND EXISTS(SELECT 1 FROM skill_clusters WHERE id=? AND status='failed')", (offered['suggestion_id'], offered['id']))
        # Files are derived from the committed skills, never a reason to replay the database operation.
        self.skills.sync()
        return len(rows)

    def style_step(self):
        """Every ten minutes: a finished profile's channel lines fill voices still empty, and a draft the owner
        answered themselves instead of sending becomes a lesson for the next drafts, and that to-do looks done."""
        seeded, learned = self.store.seed_voices(), self.store.learn_sent_elsewhere()
        self.store.answered_elsewhere()
        if (self.config.get('review_worker') or {}).get('enabled'):  # read how they write from their own messages, now and then
            self.store.voice_study_due()
            self.store.tune_due()  # keep learning from edits, dismissals, snoozes and chat corrections (learning_loop.py)
            self.missed_work_step({'owned': calendar_owned, 'bulk': bulk_kind, 'model': background_model})  # once a week: how many reviewed signals without a to-do needed one (missed_work.py)
            if self.fleet:  # learnings go to the team over the Network: without it there is nobody to offer them to
                self.store.learnings_due()
                self.team_votes_due()  # and other Machines' learnings come to be judged, when voting is on
                self.fleet_learn_due()  # and team learnings from team conversations, in a Standard Work Fleet
        if self.fleet:
            self.learnings_auto_send()  # Send learnings automatically: a batch that couldn't get through yet
            self.help_topics_send()  # what Help was asked, as topics (help_topics.py)
            self.error_reports_step()
            self.pacing_send()  # how often background work paced, counts only (pacing.py)
        self.apply_skill_clusters()  # a Create skill tapped on Telegram
        self.summary_step()  # people's summaries, when their evidence changed (person_summary.py)
        if seeded or learned:
            LOG.info('style learned voices=%s replies=%s', seeded, learned)

    def action_worker(self):
        promised = styled = followed = 0
        while not self.stop.wait(3):
            if time.monotonic() - promised >= 60:
                promised = time.monotonic()
                try:self.promise_step()
                except Exception as error:LOG.error('promise check error=%s',type(error).__name__)
            if time.monotonic() - styled >= 600:
                styled = time.monotonic()
                try:self.style_step()
                except Exception as error:LOG.error('style learning error=%s',type(error).__name__)
            if time.monotonic() - followed >= 300:
                followed = time.monotonic()
                try:self.bounce_step()  # before follow-ups: a bounced address gets none by email
                except Exception as error:LOG.error('bounce check error=%s',type(error).__name__)
                try:self.follow_up_step()
                except Exception as error:LOG.error('follow-up error=%s',type(error).__name__)
            try:self.action_step()
            except Exception as error:LOG.error('approved action error=%s',type(error).__name__)
            try:self.undo_step()
            except Exception as error:LOG.error('undo merge error=%s',type(error).__name__)
            try:self.merge_effect_step()
            except Exception as error:LOG.error('merge effects error=%s',type(error).__name__)
            try:self.thread_snooze_step()
            except Exception as error:LOG.error('thread snooze error=%s',type(error).__name__)

    def undo_step(self,merge=None):
        """Undo merged fixes: the owner's Undo, or a fix merged by itself that misbehaves."""
        for suggestion_id,reason in self.store.misbehaving_merges():
            self.store.undo_merge(suggestion_id,'auto-undo:'+uuid.uuid4().hex,'assistant',reason)
        with self.store.connect() as db:
            job=db.execute("SELECT * FROM action_jobs WHERE status='undoing' ORDER BY updated_at LIMIT 1").fetchone()
        if not job:return
        merge=merge or next_actions.MergeTransport(self.config,restart_self)
        try:
            result=merge.revert(json.loads(job['payload']))
            note=job['error'] or 'Merge undone.'
            status='undone'
        except ValueError as error:
            note,status=str(error),'sent'
        with self.store.connect() as db:
            # A failed undo leaves the fix merged and says why; the card keeps its Undo.
            db.execute('UPDATE action_jobs SET status=?,error=? WHERE id=?',(status,note,job['id']))
            if status=='undone' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'undo',encoded(result),'pending',now()))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
        if status=='undone':self.merge_effect(dict(job),json.loads(job['payload']),result,'undo',merge)
        return status

    def thread_snooze_step(self,gmail=None):
        """Archive a replied thread under a label, then return it to the inbox when due."""
        with self.store.connect() as db:
            row=db.execute("SELECT t.*,j.message_id sent_message_id FROM thread_snoozes t LEFT JOIN action_jobs j ON j.id=t.job_id WHERE (t.status='queued' OR (t.status='snoozed' AND t.until<=?)) AND (t.retry_at IS NULL OR t.retry_at<=?) ORDER BY t.created_at LIMIT 1",(now(),now())).fetchone()
            if row and row['status']=='snoozed':
                later=db.execute("SELECT max(until) FROM thread_snoozes WHERE account_id=? AND thread_id=? AND status IN ('queued','snoozed') AND until>?",(row['account_id'],row['thread_id'],now())).fetchone()[0]
                if later:
                    db.execute('UPDATE thread_snoozes SET until=? WHERE job_id=?',(later,row['job_id']))
                    return
        if not row:return
        gmail=gmail or next_actions.ThreadSnooze(self.config,credential,gog_read)
        try:
            if row['status']=='queued':
                if row['until']<=now():status='returned'  # Too late to snooze; leave the thread alone.
                else:status=gmail.snooze(row['account_id'],row['thread_id'],row['sent_message_id'])
            else:status=gmail.wake(row['account_id'],row['thread_id'])
            outlook=next((a for a in self.config.get('accounts',[]) if a['id']==row['account_id'] and a.get('service')=='outlook'),None)
            error={'no_permission':'Outlook can’t move this thread yet: connect the account again with sending on.' if outlook else 'Gmail can’t move this thread yet: the account needs the modify permission.'}.get(status)
            with self.store.connect() as db:
                db.execute('UPDATE thread_snoozes SET status=?,error=?,retry_at=NULL,updated_at=? WHERE job_id=?',
                           ('failed' if error else status,error,now(),row['job_id']))
                if status=='returned':
                    db.execute("UPDATE thread_snoozes SET status='returned',error=NULL,retry_at=NULL,updated_at=? WHERE account_id=? AND thread_id=? AND status IN ('queued','snoozed')",(now(),row['account_id'],row['thread_id']))
        except Exception as error:
            # Retry with backoff; a thread that can't come back stays labeled in Gmail.
            attempts=row['attempts']+1
            with self.store.connect() as db:
                db.execute('UPDATE thread_snoozes SET attempts=?,error=?,retry_at=?,status=?,updated_at=? WHERE job_id=?',
                           (attempts,type(error).__name__,(dt.datetime.fromisoformat(now())+dt.timedelta(minutes=min(5*2**attempts,360))).isoformat(),
                            row['status'] if attempts<12 or row['status']=='snoozed' else 'failed',now(),row['job_id']))
            LOG.error('thread snooze status=%s error=%s',row['status'],type(error).__name__)

    def stop_stale_runs(self, runner, limit=5):
        """Canceled, replaced or finished runs live on in their Gateway session until stopped. Stop and
        confirm each exact old run; only work in that same session or card waits for it. One round at a time: the
        Browser view's Stop starts one at once, beside the worker's."""
        with self.__dict__.setdefault('stale_lock', threading.Lock()):
            self._stop_stale_runs(runner, limit)

    def _stop_stale_runs(self, runner, limit):
        with self.store.connect() as db:
            stale=db.execute("""SELECT r.*,p.status prep_status,p.error prep_error,p.reason prep_reason,p.updated_at prep_updated
                FROM preparation_runs r LEFT JOIN preparations p ON p.job_id=r.job_id
                WHERE r.finished_at IS NULL AND (p.job_id IS NULL OR p.status NOT IN ('starting','running'))
                AND (r.retry_at IS NULL OR r.retry_at<=?) ORDER BY r.started_at LIMIT ?""",(now(),limit)).fetchall()
        for run in stale:
            # Its own result or blocker is saved (not replaced, canceled or timed out): the run normally ends by itself
            # seconds later. Read how it ended; stop it only when it is still going after PREPARATION_SETTLE_SECONDS.
            # Also one whose preparation was canceled after its blocker was saved (reason kept: settle_ahead before it kept
            # the blocker): that run finished by itself too, so it is never stopped and recorded as lost.
            saved=run['prep_status'] in ('done','blocked') or run['prep_status']=='cancelled' and bool((run['prep_reason'] or '').strip())
            if saved and run['prep_error'] not in ('completion_unconfirmed','stopped'):  # stopped: the chat's Stop, at once
                outcome=runner({'action':'status','job_id':run['job_id'],'session_job_id':run['session_job_id']})
                if outcome.get('status') in preparation_state.TERMINAL:
                    with self.store.connect() as db:
                        db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE job_id=? AND finished_at IS NULL',(outcome['status'],now(),run['job_id']))
                    continue
                settled=dt.datetime.fromisoformat(run['prep_updated'] or run['started_at'])
                if (dt.datetime.fromisoformat(now())-settled).total_seconds()<PREPARATION_SETTLE_SECONDS:
                    with self.store.connect() as db:
                        db.execute('UPDATE preparation_runs SET retry_at=? WHERE job_id=?',((dt.datetime.fromisoformat(now())+dt.timedelta(seconds=10)).isoformat(),run['job_id']))
                    continue
            outcome=runner({'action':'stop','job_id':run['job_id'],'session_job_id':run['session_job_id']})
            with self.store.connect() as db:
                if outcome.get('status') not in preparation_state.TERMINAL:
                    db.execute('UPDATE preparation_runs SET retry_at=? WHERE job_id=?',((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=1)).isoformat(),run['job_id']))
                    continue
                db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE job_id=?',(outcome['status'],now(),run['job_id']))
                # A run that timed out without confirmation gets its one automatic retry once it has really ended. Not on a
                # to-do waiting for the owner (a prepared-ahead one settle_ahead sent out): their Try again starts it.
                retried=db.execute("""UPDATE preparations SET job_id=?,status='queued',reason=NULL,details=NULL,retry_at=NULL,updated_at=?,
                    auto_retries=auto_retries+1,started_at=NULL WHERE job_id=? AND status='blocked' AND error='completion_unconfirmed' AND auto_retries=0
                    AND suggestion_id IN (SELECT id FROM suggestions WHERE status IN ('accepted','instructions'))""",
                    (uuid.uuid4().hex,now(),run['job_id'])).rowcount
                if retried:
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(run['suggestion_id'],))

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
                # owner (it lists them while its Google app is in Testing, where Google blocks everyone else)
                found['sources'] = [x for x in found['sources'] if x['service'] != 'google_meet' or (available is not None and 'google_meet' in available)]
                found['paired'], found['pair_url'] = getattr(self, 'fleet', None) is not None, fleet.PAIR_PAGE
            if not hosted or gbrain.on(self.config):
                # GBrain (gbrain.py): one optional tile at the end, on a Machine where the owner can install it
                found['gbrain'] = {'on': gbrain.on(self.config)}
            if agent_jobs.settings(self.config) is not None:
                # Codex (codex_signin.py): its own tile, signed in with a code from OpenAI right here
                found['codex'] = {'status': codex_signin.status(self.config)}
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

    def peek_target(self, job_id):
        """(DevTools address, target ID) of the tab a running preparation is on now (peek_tab), in the browser this
        install's DevTools address points at (loopback only); None when it uses another browser or none."""
        with self.store.connect() as db:
            tab = peek_tab(db, job_id)
        base = (browser_login.endpoints(self.config) or [None])[0]
        if not tab or not base or urllib.parse.urlsplit(base).port != tab[1]:
            return None
        return base, tab[0]

    def browser_now(self):
        """What this Machine's own browser is doing, for the note in its viewer and its Stop (in the viewer and the
        dashboard's Browser pane): the running tasks that use it (to-do ID, title and latest step), the one on the tab
        in front first, and the ones waiting there for the owner to sign in (title and site). Nothing else."""
        with self.store.connect() as db:
            rows = db.execute("SELECT p.job_id,p.session_job_id,p.suggestion_id,p.status,p.reason,s.title FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                              "WHERE p.status IN ('starting','running','blocked') ORDER BY p.updated_at DESC LIMIT 20").fetchall()
            waits = {r['job_id']: browser_wait(db, r['job_id'], r['status'], reason=r['reason']) for r in rows if r['status'] == 'blocked'}
            try:
                used = {r['job_id'] for r in rows if r['status'] != 'blocked' and db.execute(
                    "SELECT 1 FROM preparation_calls WHERE job_id=? AND tool='browser' LIMIT 1", (r['job_id'],)).fetchone()}
            except sqlite3.OperationalError:
                used = set()
            tabs = {j: run_tab(db, j) for j in used} if len(used) > 1 else {}
        front = self.front_tab(tabs) if tabs else None
        working, waiting = [], []
        for r in rows:
            title = ' '.join(str(r['title'] or '').split())[:120]
            if r['status'] == 'blocked':
                wait = waits.get(r['job_id'])
                if wait and wait['sign_in']:
                    waiting.append({'title': title, 'site': signin_name(r['reason'], wait['page'])})
            elif r['job_id'] in used:  # a run that has used the browser counts until it ends, so the note doesn't flicker
                steps = preparation_steps(r['session_job_id'] or r['job_id'], self.config.get('agent_db'), 1)
                item = {'id': r['suggestion_id'], 'title': title, 'step': steps[-1]['title'] if steps else None}
                working.insert(0, item) if front and front == tabs.get(r['job_id']) else working.append(item)
        return {'working': working[:3], 'waiting': waiting[:3]}

    def front_tab(self, tabs):
        """Which of these runs' tabs (job ID: (target ID, port)) the browser shows now: the one whose page is visible,
        read over DevTools without bringing anything to the front. None when none is, or the browser can't say."""
        base = (browser_login.endpoints(self.config) or [None])[0]
        port = urllib.parse.urlsplit(base).port if base else None
        for tab in dict.fromkeys(t for t in tabs.values() if t and t[1] == port):
            try:
                with browser_login.browser_cdp.Session(base, tab[0], timeout=2) as session:
                    if session.call('Runtime.evaluate', {'expression': 'document.visibilityState', 'returnByValue': True})['result'].get('value') == 'visible':
                        return tab
            except (browser_login.browser_cdp.CdpError, OSError, KeyError, TypeError, AttributeError, ValueError):
                continue
        return None

    def expire_step(self, every=30):
        """To-dos whose moment passed close by themselves (Store.expire_passed), about every half minute; Intercom to-dos a
        teammate took (Store.close_taken_intercom), about every five minutes."""
        if time.monotonic() - self.__dict__.get('expired_swept', -every) < every:
            return
        self.expired_swept = time.monotonic()
        self.store.expire_passed()
        if time.monotonic() - self.__dict__.get('intercom_swept', -300) >= 300:  # a teammate took it: within five minutes
            self.intercom_swept = time.monotonic()
            self.store.close_taken_intercom()

    def seal_attachments(self, every=60):
        """Email attachments that ended runs took are sealed in place and the runs' readable copies removed
        (mail_attachments.py). The first time after a start covers every earlier run; with protection off, sealed
        attachments are opened again instead."""
        last = self.__dict__.get('attachments_swept')
        if last and time.monotonic() - last[0] < every:
            return
        started, store = now(), next_actions.attachment_store(self.config)
        if not last and not self.store.protected and (opened := mail_attachments.open_all(self.config, store)):
            LOG.info('email attachments opened: %s', opened)
        if (sealed := mail_attachments.sweep(self.store.connect, self.config, since=last[1] if last else None, store=store)):
            LOG.info('email attachments sealed: %s', sealed)
        self.attachments_swept = (time.monotonic(), started)

    def flag_browser_waits(self):
        """A sent card is redrawn once when its running preparation starts waiting on the browser, so it says so and,
        with a viewer link, gets its Open the browser button. A blocked one is redrawn anyway."""
        flagged = self.__dict__.setdefault('browser_flagged', set())
        with self.store.connect() as db:
            # A blocked sign-in is redrawn once too (once per start), so a card from before gets its Sign in button.
            for job in db.execute("SELECT job_id,suggestion_id,status,reason FROM preparations WHERE status IN ('starting','running','blocked')").fetchall():
                if job['job_id'] in flagged or (job['status'] == 'blocked' and not signin_handoff(job['reason'])) or not browser_wait(db, job['job_id'], job['status'], reason=job['reason']):
                    continue
                flagged.add(job['job_id'])
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (job['suggestion_id'],))

    def signin_waits(self):
        """Blocked preparations of open tasks that wait on the owner to sign in: [(suggestion_id, job_id, page)]."""
        found = []
        with self.store.connect() as db:
            for job in db.execute("SELECT p.suggestion_id,p.job_id,p.reason FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                                  "WHERE p.status='blocked' AND s.status IN ('accepted','instructions')").fetchall():
                waiting = signin_handoff(job['reason']) and browser_wait(db, job['job_id'], 'blocked', reason=job['reason'])
                if waiting:
                    found.append((job['suggestion_id'], job['job_id'], waiting.get('page')))
        return found

    def signin_reason(self, suggestion_id):
        with self.store.connect() as db:
            row = db.execute("SELECT reason FROM preparations WHERE suggestion_id=? AND status='blocked'", (suggestion_id,)).fetchone()
        return row[0] if row else None

    def signin_tabs(self):
        """The shared browser's open pages, [{id, url}] (DevTools on loopback only)."""
        base = browser_login.endpoints(self.config)[0]
        return [{'id': t.get('id'), 'url': t.get('url') or ''} for t in browser_login.browser_cdp._http(base, '/json/list', timeout=3) if t.get('type') == 'page']

    def signin_open(self, suggestion_id):
        """The sign-in dialog for a task: its sign-in page in front in the shared browser, reopened from the address
        its own run left off at when that tab is gone. Returns what the dialog shows: {state, site, kind, view}."""
        page = self.signin_page(suggestion_id)
        view = browser_link(self.config)
        if not page:
            return {'state': 'unknown', 'site': None, 'kind': None, 'view': view}
        reason = self.signin_reason(suggestion_id)
        opened = self.__dict__.setdefault('signin_opened', {})
        try:
            tabs = self.signin_tabs()
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError):
            raise ValueError('I couldn’t reach the browser on this computer') from None
        mine = [t for t in tabs if t['id'] == opened.get(suggestion_id)] + [t for t in tabs if same_site(t['url'], page)]
        if mine:  # followed from here on, also through an identity provider on another host
            state, url, opened[suggestion_id] = 'open', mine[0]['url'], mine[0]['id']
        else:
            try:
                opened[suggestion_id] = browser_login.browser_cdp.open_tab(browser_login.endpoints(self.config)[0], page)
            except (browser_login.browser_cdp.CdpError, OSError):
                raise ValueError('I couldn’t open the sign-in page in the browser') from None
            state, url = 'opened', page
        try:
            browser_viewer.focus(url, browser_login.endpoints(self.config)[0])
        except (ValueError, OSError):
            pass
        return {'state': state, 'site': signin_name(reason, page), 'kind': signin_kind(reason, [url]), 'view': view}

    def browser_show(self, suggestion_id):
        """View in browser: the page a task's own run worked on, in front in the Machine's browser (its own tab, still as
        the run left it), else reopened there from the address the run recorded. Never the owner's own browser and
        never another task's tab. Returns {shown, opened, site, view}: `view` is the browser's viewer, when there is one."""
        with self.store.connect() as db:
            page = task_page(db, suggestion_id)
        view = browser_link(self.config)
        if not page:
            return {'shown': False, 'unknown': True, 'view': view}
        base = browser_login.endpoints(self.config)[0]
        site = browser_login.site(urllib.parse.urlsplit(page['url']).hostname)
        try:
            tabs = self.signin_tabs()
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError):
            return {'shown': False, 'site': site, 'view': view, 'error': 'I couldn’t reach the browser on this computer'}
        same_port = page['target'] and urllib.parse.urlsplit(base).port == page['port']
        tab = (next((t for t in tabs if same_port and t['id'] == page['target']), None)
               or next((t for t in tabs if t['url'] == page['url']), None))
        opened = False
        if not tab:  # the tab is gone: the same address again, in the Machine's browser
            try:
                tab = {'id': browser_login.browser_cdp.open_tab(base, page['url']), 'url': page['url']}
            except (browser_login.browser_cdp.CdpError, OSError):
                return {'shown': False, 'site': site, 'view': view, 'error': 'I couldn’t open that page in the browser'}
            opened = True
        try:
            shown = browser_viewer.focus(tab['url'], base, target=tab['id']) is not None
        except (ValueError, OSError):
            shown = False
        return {'shown': shown, 'opened': opened, 'site': site, 'view': view}

    def task_front(self, page):
        """Open the browser for a preparing card: the tab on the task's page (same site) in front in the Machine's
        browser, and when the run's tab is gone, that page opened again there, so the owner never lands on a closed or
        unrelated tab. Returns {shown, opened}."""
        base = browser_login.endpoints(self.config)[0]
        opened = None
        try:
            if not any(same_site(t['url'], page) for t in self.signin_tabs()):
                opened = browser_login.browser_cdp.open_tab(base, page)
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError, ValueError):
            pass  # can't read the tabs: bring what there is to the front, as before
        try:
            shown = browser_viewer.focus(page, base, target=opened)
        except (ValueError, OSError):
            shown = None
        return {'shown': shown is not None, 'opened': bool(opened)}

    def signin_page(self, suggestion_id):
        """The address a task's blocked sign-in waits on, from its own run steps (run_page), or None."""
        return next((page for task, job, page in self.signin_waits() if task == suggestion_id), None)

    def resume_signed_in(self, host=None, suggestion_id=None, source='signed_in'):
        """Carries on the tasks blocked on a sign-in that is now done: the one named, and those waiting on `host`'s site.
        The same as tapping Continue; nothing here signs in or touches the site. Returns the resumed task ids."""
        resumed = []
        for task, job, page in self.signin_waits():
            # Keyed on each task's own site: a sign-in elsewhere never carries a task on, named or not.
            if not (bool(page) and same_site(host, page) if host else task == suggestion_id):
                continue
            try:
                self.store.decide(task, 'retry', '', 'signed-in:' + job, source)
            except ValueError as error:
                LOG.info('sign-in resume skipped suggestion=%s error=%s', task, error)
                continue
            LOG.info('sign-in resume suggestion=%s source=%s', task, source)
            resumed.append(task)
        return resumed

    def watch_sign_ins(self, every=SIGNIN_WATCH, now=False):
        """Signing in in the browser itself carries on too. While a task waits on a sign-in, look every `every` seconds
        at the shared browser (read-only: which sign-in fields show, never what is in them, and the tabs' addresses).
        The task's site was seen at its sign-in (a form, a sign-in address, its identity provider) and now a tab of it
        is past that with no form: the owner got in, so carry on, once per blocked run. Also for sign-ins with
        nothing to type (itsme or eID, a passkey, a captcha, choosing an account). `now`: look at once (the owner just
        closed the browser). Returns the tasks it carried on."""
        state = self.__dict__.setdefault('signin_watch', {'next': 0.0, 'seen': set(), 'done': set()})
        if time.monotonic() < state['next'] and not now:
            return []
        state['next'] = time.monotonic() + every
        waits = [(task, job, page) for task, job, page in self.signin_waits() if page and job not in state['done']]
        if not waits:
            state['seen'].clear()
            return []
        try:
            shown = [p['host'] for p in browser_login.pages(self.config)]
            tabs = self.signin_tabs()
        except Exception:  # no browser right now: look again later
            return []
        resumed = []
        opened = self.__dict__.get('signin_opened', {})
        for task, job, page in waits:
            mine = [t['url'] for t in tabs if t['id'] == opened.get(task) or same_site(t['url'], page)]
            if any(same_site(host, page) for host in shown) or any(signin_address(url, page) for url in mine):
                state['seen'].add(job)
            elif job in state['seen'] and any(same_site(url, page) for url in mine):
                state['seen'].discard(job)
                state['done'].add(job)
                resumed += self.resume_signed_in(suggestion_id=task)
        return resumed

    def release_finished_browser_lease(self, lease_file=BROWSER_LEASE):
        """A Do it run holds the browser as `assistant-<first 8 of its job ID>`. Runs can end without
        releasing it (October 13: one blocked itself on its own lease), so free each such holder whose
        run is no longer starting or running. Other owners' leases are never touched. The lease is
        shared since 2026-10-13 (`holders`); the older single `owner` format is still read."""
        try:
            state=json.loads(Path(lease_file).read_text())
            owners=list(state.get('holders') or {})+([state['owner']] if state.get('owner') else [])
        except (OSError,ValueError,AttributeError,TypeError):return False
        released=False
        for owner in owners:
            match=re.fullmatch(r'assistant-([a-f0-9]{8})',str(owner))
            if not match:continue
            with self.store.connect() as db:
                known=db.execute("SELECT finished_at FROM preparation_runs WHERE substr(job_id,1,8)=?",(match[1],)).fetchall()
                if not known or any(not r['finished_at'] for r in known):
                    continue
            subprocess.run([sys.executable,str(browser_lease_script(self.config)),'release','--owner',owner],
                           capture_output=True,timeout=30)
            LOG.info('browser lease released owner=%s (run ended)',owner)
            released=True
        return released

    def short_window(self):
        """The main model's 5-hour usage window as last read (model_usage): {'used', 'reset'}, or None (an API key, a
        sign-in that reports no windows, or nothing read yet)."""
        usage = self.paced_usage()  # None while a working fallback carries work: the first review counts signals then
        found = [w for p in usage or [] for w in p.get('windows') or []
                 if model_budget.window_kind(w.get('label')) == 'short' and isinstance(w.get('used'), (int, float))]
        if not found:
            return None
        window = max(found, key=lambda w: w['used'])
        return {'used': window['used'], 'reset': window.get('reset')}

    def still_needed_step(self, current=None):
        """Still needed? (still_needed.py): asks once on each open to-do nobody touched for a week, and ends the question
        of one that closed. current: an ISO time (tests)."""
        with self.store.connect() as db:
            return Store.still_needed_ask(db, current or now(), lambda row: looks_done(row) or waits_on_others(row), local_tz())

    def profile_step(self, runner=None):
        """Start and follow the one profile turn `assistant profile` asked for (reviews may be off)."""
        runner = runner or self.preparation_gateway
        with self.store.connect() as db:
            # The one being followed first, then what the owner asked for, then The Machine's own
            run = db.execute("SELECT * FROM profile_runs WHERE status IN ('starting','running') ORDER BY status='running' DESC,coalesce(auto,0),started_at LIMIT 1").fetchone()
            ready = run and run['status'] == 'starting' and (not run['auto'] or self.store.first_magic_done(db))
        if not run:
            return None
        run, stamp = dict(run), dt.datetime.fromisoformat(now())
        if run['status'] == 'starting':
            # One usage check before every background turn (model_budget); The Machine's own turns (profile, voices, roles,
            # organizations) wait for the first card and start one per BACKGROUND_GAP_SECONDS. A usage limit holds all.
            if self.background_pause(owner=not run['auto'], job='profile:' + run['run_id']) or (run['auto'] and not (ready and self.background_spaced())):
                return None
        age = (stamp - dt.datetime.fromisoformat(run['started_at'])).total_seconds()
        if run['status'] == 'starting' and run['attempts'] and run['updated_at'] > (stamp - dt.timedelta(minutes=1)).isoformat():
            return None
        if run['status'] == 'starting' and run['attempts'] >= 5:
            with self.store.connect() as db:
                db.execute("UPDATE profile_runs SET status='error',error='openclaw_unavailable',finished_at=?,updated_at=? WHERE run_id=?", (now(), now(), run['run_id']))
            return 'error'
        action = 'stop' if age > PROFILE_SECONDS + 300 else 'start' if run['status'] == 'starting' else 'status'
        skills_run = run.get('kind') == 'skills'
        request = {'kind': 'skills' if skills_run else 'profile', 'job_id': run['run_id'], 'action': action}
        accounts = None
        if action == 'start' and skills_run:
            started = self.skills_find_begin(run)
            if started is None:
                return None  # the browser is busy with another task: try again on the next step
            if started is False:
                return 'ok'  # nothing to read: every account asked for is signed out
            accounts = started
        if action == 'start':
            first = self.store.profile_evidence(1, PROFILE_SESSION_PREFIX + run['run_id']) if not skills_run else None
            request['message'] = (skills_find_prompt(run['run_id'], {**json.loads(run['evidence']), 'items': accounts['items']}, self.config) if skills_run else
                                  roles_prompt(run['run_id'], first['pages']) if run.get('kind') == 'roles' else
                                  import_prompt(run['run_id']) if run.get('kind') == 'import' else
                                  orgs_prompt(run['run_id'], first['pages']) if run.get('kind') == 'orgs' else
                                  share_history_prompt(run['run_id'], first['pages'], self.share_groups()) if run.get('kind') == 'share' else
                                  voices_prompt(run['run_id'], first['counts'], first['pages']) if run.get('kind') == 'voices' else
                                  team_learnings.prompt(run['run_id'], json.loads(run['evidence'])) if run.get('kind') == 'learnings' else
                                  learning_loop.prompt(run['run_id']) if run.get('kind') == 'tune' else
                                  fleet_learnings.prompt(run['run_id']) if run.get('kind') == 'fleet_learn' else
                                  team_learnings.vote_prompt(run['run_id'], json.loads(run['evidence'])) if run.get('kind') == 'team_votes' else
                                  profile_prompt(run['run_id'], first['counts'], run.get('room') or PROFILE_ROOM))
            with self.store.connect() as db:
                db.execute('UPDATE profile_runs SET attempts=attempts+1,updated_at=? WHERE run_id=?', (now(), run['run_id']))
        result = runner(request).get('status', 'unavailable')
        with self.store.connect() as db:
            if result == 'admitted':
                if run['auto']:
                    self.background_started()
                db.execute("UPDATE profile_runs SET status='running',error=NULL,updated_at=? WHERE run_id=?", (now(), run['run_id']))
            elif result in REVIEW_TERMINAL or (action == 'stop' and age > PROFILE_SECONDS + 900):
                draft = db.execute('SELECT draft FROM profile_runs WHERE run_id=?', (run['run_id'],)).fetchone()[0]
                if run.get('kind') in ('roles', 'orgs'):  # done is done: a person left without one was unclear
                    draft = draft or (result == 'ok')
                status = 'ok' if draft else 'error'
                error = None if draft else ('no_draft' if result == 'ok' else result)
                db.execute('UPDATE profile_runs SET status=?,error=?,finished_at=?,updated_at=? WHERE run_id=?', (status, error, now(), now(), run['run_id']))
                if run.get('kind') == 'skills':
                    self.skills_find_done(run, status)
        if run.get('kind') == 'learnings':  # asks the owner only once the run is ok
            with self.store.connect() as db:
                batch = team_learnings.finish(db, run['run_id'])
            if batch:
                LOG.info('learnings ready')
                self.learnings_auto_send()  # sent at once when the owner chose Send automatically
        if run.get('kind') == 'tune':  # applies only once the run is ok; each change can be undone
            changed = self.store.apply_tune(run['run_id'])
            if changed:
                LOG.info('learning pass changes=%s', changed)
        if run.get('kind') == 'fleet_learn' and getattr(self, 'fleet', None):  # kept only once the run is ok, each one checked
            with self.store.connect() as db:
                kept = fleet_learnings.finish(db, run['run_id'], team_learnings.known_names(db, self.config), log=self.fleet.log)
            if kept:
                LOG.info('team learnings kept=%s', len(kept))
        if run.get('kind') == 'team_votes':  # sends only the votes, once the run is ok
            self.team_votes_send(run['run_id'])
        if run.get('kind') == 'voices':  # applies only once the run is ok
            written = self.store.apply_voice_study(run['run_id'])
            if written:
                LOG.info('voice study channels=%s', written)
        if run.get('auto') and run.get('kind') == 'profile':  # saves only once the run is ok
            self.first_profile_save(run['run_id'])
        return result

    def owner_first_names(self):
        """The owner's first name, as the config and USER.md give it ("- Name: …", "# USER.md - About …"): for
        Learning's older why lines that name them (learning_loop.to_you)."""
        names = [str(self.config.get('owner_name') or '')]
        try:
            text = self.user_md().read_text(encoding='utf-8')[:4000]
            names += re.findall(r'(?m)^- Name: *(.+)$', text) + re.findall(r'(?m)^# USER\.md - About (.+)$', text)
        except (OSError, ValueError):
            pass
        return sorted({n.split()[0] for n in names if n.split() and re.fullmatch(r"[^\W\d_][\w'’-]*", n.split()[0]) and n.split()[0].lower() not in ('me', 'the', 'you')})

    def learning_changes_shown(self, changes):
        """Learning, Changes: an older why line that names the owner reads "You corrected …" (the stored one stays)."""
        names = self.owner_first_names()
        return [{**c, 'why': learning_loop.to_you(c.get('why'), names)} for c in changes]

    def owner_role(self):
        """The Role line of USER.md ('' when there is none): only for Help's guess at how technical the owner is."""
        try:
            found = re.search(r'(?m)^- Role: *(.+)$', self.user_md().read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return ''
        return found[1].strip()[:200] if found else ''

    def user_md(self):
        import onboarding
        return onboarding.user_md_path(self.config.get('openclaw_workspace') or WORKSPACE)

    @staticmethod
    def user_md_says_how(path):
        """OpenClaw's own USER.md template has no Tone line either, yet says nothing about the owner."""
        import onboarding
        return not onboarding.user_md_is_template(path) and onboarding.says_how_you_write(path)

    def first_profile_step(self, current=None):
        """Installs set up without the interactive installer (hosted Machines) never ran `assistant profile`, so reviews
        and drafts knew neither who the owner is nor how they write. Once reviews are on and USER.md still says nothing
        about how they write, one profile turn starts by itself (and names the closest people after it). Tried a few
        times at most; `first_profile: false` in the config turns it off."""
        import onboarding
        if not (self.config.get('review_worker') or {}).get('enabled') or self.config.get('first_profile') is False:
            return None
        current = current or dt.datetime.fromisoformat(now())
        if getattr(self, '_first_profile_wait', None) and self._first_profile_wait > current:
            return None
        path = self.user_md()
        if self.user_md_says_how(path):
            return None
        with self.store.connect() as db:
            runs = db.execute("SELECT status,auto,finished_at FROM profile_runs WHERE kind='profile' ORDER BY started_at").fetchall()
        if (any(not r['auto'] or r['status'] in ('starting', 'running', 'ok') for r in runs) or len(runs) >= FIRST_PROFILE_TRIES
                or (runs and (runs[-1]['finished_at'] or '') > (current - dt.timedelta(seconds=FIRST_PROFILE_RETRY_SECONDS)).isoformat())):
            return None  # the owner ran their own, one is running or done, or tried enough
        try:
            text = path.read_text() if path.exists() else onboarding.starter_user_md(self.config)
        except OSError:
            return None
        if onboarding.user_md_is_template(path):
            text = text.rstrip() + '\n\n' + onboarding.starter_user_md(self.config)
        try:
            return self.store.profile_start(room=max(onboarding.profile_room(text), 0), auto=True)
        except ValueError:  # too few of the owner's own messages yet: look again later
            self._first_profile_wait = current + dt.timedelta(seconds=FIRST_PROFILE_RETRY_SECONDS)
            return None

    def share_files(self, event_id, part=None):
        """A Work email's attachments for the Shared Graph, read-only (Gmail and Outlook): the list, or (part) one file's
        bytes. Only files: cloud links and attached emails stay where they are."""
        with self.store.connect() as db:
            row = db.execute('SELECT account_id,source_id,kind FROM events WHERE id=?', (int(event_id),)).fetchone()
        account = row and next((a for a in self.config['accounts'] if a['id'] == row['account_id']), None)
        if not account or not next_actions.mail_account(account) or row['kind'] not in ('gmail.message', 'ms_graph.message') or not row['source_id']:
            return [] if part is None else None
        fetch = App.outlook_attachments if next_actions.outlook(account) else App.gmail_attachments
        if part is None:
            return [a for a in fetch(self, account, row['source_id'])[0] if a.get('kind', 'file') == 'file' and not a.get('inline')]
        return fetch(self, account, row['source_id'], part)[1]

    def share_history_step(self):
        """The Shared Graph's history pass, when reviews are on: Work client threads from before (as far back as the
        Machine has mail) go through the same review labels, a batch per turn, one turn at a time, until none is left.
        Stops after three turns in a row that judged nothing."""
        if not (self.config.get('review_worker') or {}).get('enabled') or not getattr(self, 'fleet', None):
            return None
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') LIMIT 1").fetchone():
                return None  # one turn at a time
            runs = db.execute("SELECT status,error,finished_at FROM profile_runs WHERE kind='share' ORDER BY started_at DESC LIMIT 3").fetchall()
        if len(runs) == 3 and all(r['status'] == 'error' for r in runs):
            return None
        if runs and runs[0]['finished_at'] and runs[0]['finished_at'] > (dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=10)).isoformat():
            return None
        threads = self.fleet.graph_unjudged(SHARE_HISTORY_BATCH)
        if not threads:
            return None
        run_id, started = uuid.uuid4().hex, now()
        with self.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'share',1)",
                       (run_id, started, started, json.dumps({'threads': threads, 'page_size': SHARE_HISTORY_PAGE})))
        return {'run_id': run_id, 'threads': len(threads)}

    def orgs_backfill_step(self):
        """Once per install, when reviews are on: one organizations turn over the people already in the graph, from
        the signals already stored. Later people get theirs from reviews. Retried when OpenClaw couldn't start it."""
        if not (self.config.get('review_worker') or {}).get('enabled'):
            return None
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') LIMIT 1").fetchone():
                return None  # one turn at a time: the owner's own profile or roles first
            runs = db.execute("SELECT status,error FROM profile_runs WHERE kind='orgs'").fetchall()
            if not db.execute("SELECT 1 FROM graph_state").fetchone():
                return None  # no graph yet
        if any(r['status'] == 'ok' or r['error'] != 'openclaw_unavailable' for r in runs) or len(runs) >= 3:
            return None
        return self.store.orgs_start(auto=True)

    def first_profile_save(self, run_id):
        """The first profile's draft goes into USER.md as its own section (marked, so the owner can edit or delete
        it), never over anything that already says how the owner writes."""
        import onboarding
        with self.store.connect() as db:
            row = db.execute("SELECT draft FROM profile_runs WHERE run_id=? AND status='ok'", (run_id,)).fetchone()
        path = self.user_md()
        if not row or not row['draft'] or self.user_md_says_how(path):
            return False
        text = path.read_text() if path.exists() else onboarding.starter_user_md(self.config)
        if onboarding.user_md_is_template(path):
            text = text.rstrip() + '\n\n' + onboarding.starter_user_md(self.config)
        merged, _ = onboarding.fit_profile(text, json.loads(row['draft']), dt.datetime.now(local_tz()).date().isoformat())
        if not merged:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        onboarding.write_private(path, merged)
        LOG.info('first profile saved to USER.md chars=%s', len(merged))
        return True

    def skills_find_begin(self, run):
        """Before the Find my skills turn: the service takes the browser lease, reads the owner's own skills from the
        accounts asked for (skills_read) and adds them to the list. Returns {'accounts': states, 'items': the list to
        judge}, None when the browser is busy, or False when there is nothing to judge (the run is then done)."""
        evidence = json.loads(run['evidence'])
        try:
            claimed = subprocess.run([sys.executable, str(browser_lease_script(self.config)), 'claim', '--owner', SKILLS_LEASE,
                                      '--minutes', '20'], capture_output=True, timeout=60).returncode
        except (OSError, subprocess.TimeoutExpired):
            claimed = 0  # no lease helper: the read goes ahead as before
        if claimed == 3:
            return None
        for site in evidence.get('sites') or ():  # the sign-in tab the dashboard opened has done its job
            tab = self.__dict__.get('skills_signin_tabs', {}).pop(site, None)
            if tab:
                try:
                    browser_login.browser_cdp.close_tab(browser_login.endpoints(self.config)[0], tab)
                except (browser_login.browser_cdp.CdpError, OSError, IndexError):
                    pass
        sites = [s for s in evidence.get('sites') or SKILLS_SITES if s in SKILLS_SITES]
        try:
            read = self.skills_read(sites) if sites else {}
        finally:  # the turn after this reads no page: the browser is free again
            self.skills_lease_release()
        accounts = {s: r.get('state', 'unavailable') for s, r in read.items()}
        found = [{**f, 'from': s} for s, r in read.items() for f in r.get('skills') or []]
        importer, token, items = self.skills.importer, evidence['token'], []
        try:
            importer.accounts(token, accounts, read)
            importer.report(token, found, [], accounts)  # every account read is done now
            scan = importer.scan(token)
            items = importer.brief(i for i in scan['items'].values() if not evidence.get('more') or i['public']['from'] in sites)
            LOG.info('skills read from accounts %s', ' '.join(f"{s}={r.get('state')}:{len(r.get('skills') or [])}" for s, r in read.items()))
        except (KeyError, AttributeError, ValueError):
            pass
        if not any(not i['blocked'] and not i['here'] for i in items):  # nothing to judge: no turn
            with self.store.connect() as db:
                db.execute("UPDATE profile_runs SET status='ok',draft=?,finished_at=?,updated_at=? WHERE run_id=?",
                           (json.dumps({'reported': False}), now(), now(), run['run_id']))
            self.skills_find_done(run, 'ok')
            return False
        return {'accounts': accounts, 'items': items[:150]}

    def skills_lease_release(self):
        try:
            subprocess.run([sys.executable, str(browser_lease_script(self.config)), 'release', '--owner', SKILLS_LEASE], capture_output=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            pass

    def follow_config(self):
        """Settings in LIVE_CONFIG that changed in config.json since the last look (the hosting agent's reviews on, while
        the first look runs) apply at once, without a restart. Best effort: an unreadable file changes nothing."""
        path = getattr(self, 'config_path', None)
        if not path:
            return False
        try:
            stamp = path.stat().st_mtime_ns
            if stamp == getattr(self, 'config_stamp', None):
                return False
            first = getattr(self, 'config_stamp', None) is None
            self.config_stamp = stamp
            if first:
                return False  # what the app started with
            saved = json.loads(path.read_text())
        except (OSError, ValueError):
            return False
        changed = False
        for key in LIVE_CONFIG:
            if isinstance(saved, dict) and key in saved and saved[key] != self.config.get(key):
                self.config[key] = saved[key]
                changed = True
        if changed:
            LOG.info('settings applied without a restart: %s', ','.join(LIVE_CONFIG))
        return changed

    def retention_worker(self):
        """Once a day at a quiet hour: old sync history and preparation logs go, the space goes back to the disk and
        local copies of the database rotate (retention.py). Checks every ten minutes; never stops the service."""
        while not self.stop.wait(600):
            try:  # sign-ins older versions kept only to revoke at Google again: dropped, never revoked (mail_grants.retry)
                import mail_grants
                mail_grants.retry(self.config, due_only=True)
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.warning('sign-out retry error=%s', type(error).__name__)
            try:
                if retention.due(self.store.connect, dt.datetime.now(dt.timezone.utc), local_tz()):
                    report = retention.run(self.store.connect, str(self.store.path), local_tz=local_tz())
                    LOG.info('retention %s', json.dumps(report, sort_keys=True))
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.error('retention error=%s', type(error).__name__)
            try:  # files added to a chat message and never sent, and those of cards that are gone (chat_files.py)
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    chat_files.sweep(db, self.config, now())
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.error('chat files sweep error=%s', type(error).__name__)

    def embedding_worker(self):
        """Small background passes (embed_pass): signals first, then history. Never blocks
        ingestion (no transaction spans the embedding call); failures wait and retry."""
        wait=10
        while not self.stop.wait(wait):
            try:wait=self.embed_pass(embeddings.settings(self.config))
            except Exception as error:
                LOG.error('embeddings error=%s',error if isinstance(error,embeddings.EmbeddingError) else type(error).__name__);wait=300

    def model_usage_worker(self):
        """Reads the AI sign-in's usage limits every five minutes, and a minute after a run ends (OpenClaw makes the
        model calls, so its usage reading is the one to ask; that reading never costs model usage). A failed read
        keeps the last one. The resets come from the Codex CLI's own sign-in when it is the same account."""
        self.model_usage_wake = getattr(self, 'model_usage_wake', None) or threading.Event()
        while not self.stop.is_set():
            self.refresh_model_usage()
            try:  # a fallback billed apart: checked while the main model's limits would hold work back (model_fallback.py)
                self.check_fallback()
            except Exception as error:  # noqa: BLE001 - never stops the worker
                LOG.error('fallback check error=%s', type(error).__name__)
            try:  # the models a chat can pick (chat_model.py): read again every ten minutes
                self.chat_models()
            except Exception as error:  # noqa: BLE001 - never stops the worker
                LOG.error('model list error=%s', type(error).__name__)
            self.model_usage_wake.clear()
            if self.stop.wait(60):
                break
            for _ in range(240):  # the rest of five minutes, or sooner when a run ended
                if self.stop.is_set() or self.model_usage_wake.is_set():
                    break
                self.stop.wait(1)

    def refresh_model_usage(self):
        reply = usage_status(self.config)
        if reply is None:
            return
        self.model_usage = model_usage(self.config, reply=reply) or getattr(self, 'model_usage', None)
        self.model_usage_reply = reply
        try:
            resets = model_resets(self.config, reply) if self.config.get('codex') is not False else None
        except (OSError, ValueError):
            resets = None
        self.model_status = model_status(self.config, reply, self.model_usage, resets)

    def enrichment_worker(self):
        """Organization and work contact data from the configured enrichment service: a few domains (and people) every ten minutes, each
        looked up again after three months. A service error waits an hour (a day for that domain)."""
        wait = 120
        while not self.stop.wait(wait):
            try:
                if enrichment.step(self.store.connect, self.config, now(), paired=bool(getattr(self, 'fleet', None))):
                    self.graph_dirty.set()  # show the new profiles
                found = enrichment.people_step(self.store.connect, self.config, now(), paired=bool(getattr(self, 'fleet', None)), stop=self.stop.is_set)
                photos = enrichment.photos_step(self.store.connect, now())  # straight after the lookups (hosted ones too, through the agent)
                photos += enrichment.site_logos_step(self.store.connect, now())  # organizations that show no logo: their own site's
                for account in google_photo_accounts(self.config):
                    with self.store.connect() as db:
                        due = enrichment.contact_run_due(db, 'google:' + account['email'].lower(), now())
                    if due and not self.stop.is_set():
                        facts = []
                        offers = google_photo_offers(self.config, account, facts=facts)
                        with self.store.connect() as db:
                            enrichment.offer_photos(db, offers, 'google', now())
                            known = enrichment.graph_people(db)  # contacts the Machine knows, like their photos
                            found += enrichment.offer_facts(db, [(ids, f, r) for ids, f, r in facts if any(i in known for i in ids)], 'google', now())
                            enrichment.contact_run_done(db, 'google:' + account['email'].lower(), now())
                photos += enrichment.contact_photos_step(self.store.connect, now())
                wa_accounts, ask = whatsapp_photo_asker(self.config)
                if wa_accounts and not self.stop.is_set():
                    photos += enrichment.whatsapp_photos_step(self.store.connect, now(), ask, wa_accounts)
                tg_accounts, ask = telegram_photo_asker(self.config)
                if tg_accounts and not self.stop.is_set():
                    photos += enrichment.telegram_photos_step(self.store.connect, now(), ask, tg_accounts)
                found += enrichment.facts_from_signals(self.store.connect, now())  # once: facts already in stored signals
                if found or photos:
                    LOG.info('enrichment people found=%s photos=%s', found, photos)
                    self.graph_dirty.set()
                wait = 600
            except enrichment.EnrichmentError as error:
                LOG.error('enrichment error=%s', error)
                wait = 3600
            except Exception as error:
                LOG.error('enrichment error=%s', type(error).__name__)
                wait = 3600

    def background_spaced(self):
        """At most one background turn beyond the first look per BACKGROUND_GAP_SECONDS."""
        return time.time() - getattr(self, 'background_at', 0) >= BACKGROUND_GAP_SECONDS

    def import_check_start(self, kind, text):
        """The owner's model looks at a file being imported (crm_import.ai_evidence: headers, a few values, unclear
        cells), when it can run now: signed in, with room in its limits and no other agent pass going. Else the
        rules' guess stands and {'ai': False, 'why'} says why."""
        if kind not in crm_import.FIELDS:
            raise ValueError('Import people, organizations or projects')
        if self.config.get('import_check') is False:
            return {'ai': False, 'why': 'off'}
        if model_ready(self.config) is False or not self.model_room():
            return {'ai': False, 'why': 'model'}
        region = crm_fixes.region_of({'country': self.config.get('country'), 'timezone': self.config.get('timezone') or getattr(local_tz(), 'key', '')})
        with self.store.connect() as db:
            evidence = crm_import.ai_evidence(db, kind, text, region, self.currency())
        run_id, started = uuid.uuid4().hex, now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute("UPDATE profile_runs SET status='error',error='replaced',finished_at=?,updated_at=? WHERE kind='import' AND status='starting'", (started, started))
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') AND kind!='import'").fetchone():
                return {'ai': False, 'why': 'busy'}  # an agent pass is going: the import doesn't wait for it
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind) VALUES(?,'starting',?,?,?,'import')",
                       (run_id, started, started, json.dumps({'kind': kind, 'digest': crm_import.digest(kind, text), 'import': evidence})))
        return {'ai': True, 'run_id': run_id, 'cells': len(evidence['cells'])}

    def import_check_status(self, run_id):
        with self.store.connect() as db:
            row = db.execute("SELECT status,error,draft FROM profile_runs WHERE run_id=? AND kind='import'", (str(run_id or ''),)).fetchone()
        if not row:
            raise ValueError('Unknown import check')
        draft = json.loads(row['draft']) if row['draft'] else {}
        return {'status': row['status'], 'columns': len(draft.get('mapping') or {}), 'fixes': len(draft.get('fixes') or ())}

    def import_check_draft(self, run_id, kind, text):
        """The model's draft for this very file (the same kind and text), else None."""
        if not run_id:
            return None
        with self.store.connect() as db:
            row = db.execute("SELECT evidence,draft FROM profile_runs WHERE run_id=? AND kind='import' AND draft IS NOT NULL", (str(run_id),)).fetchone()
        if not row or json.loads(row['evidence']).get('digest') != crm_import.digest(kind, text):
            return None
        return json.loads(row['draft'])

    BUG_SHOT_BYTES = 2 * 1024 * 1024
    BUG_TEXT = 4000

    def support_action(self, name, args):
        """Help's question (help_chat.ask, on this Machine's own model, a one-shot turn without tools) and Report a
        bug: the scrubbed support report to show (bug_preview), then that report sent to the control plane on a
        self-hosted Machine paired with the Network (bug_send). A hosted Machine's dashboard sends it to its control
        plane itself, with the owner's sign-in there."""
        import help_chat
        import onboarding
        import support
        if name == 'help_article':
            return help_chat.article(args.get('slug'))
        if name == 'help_ask':
            run = getattr(self, 'help_model', None)  # a stand-in in the sandbox and tests
            if not run and not has_model(self.config):
                raise ValueError(i18n.t('Help needs a model. Set one up in Settings, Model.'))
            swap = background_model(self.config)
            model, thinking = '/'.join(swap) if swap else None, None
            own = chat_model.clean({'model': args.get('model'), 'thinking': args.get('thinking')})
            if chat_model.chosen(self.config, own):  # a model picked for Help or for chats (chat_model.py)
                models = self.chat_models()
                picked = chat_model.resolve(self.config, models, chat_model.check(own, models, self.config) if own else {})
                model, thinking = picked['model'] or model, picked['thinking']
            try:
                found = help_chat.ask(args.get('question'), args.get('history') or [], run=run, config=self.config,
                                      model=model, thinking=thinking, role=self.owner_role())
            except help_chat.Unavailable as error:
                raise ValueError(str(error)) from None
            topic, answered = found.pop('topic', ''), found.pop('answered', False)
            try:  # the topic for The Machine team, when the owner shares it (help_topics.py); never the question
                if not getattr(self, 'fleet', None):
                    return found  # without the Network nothing goes, so nothing is kept
                with self.store.connect() as db:
                    help_topics.record(db, self.config, topic, answered)
            except (sqlite3.Error, ValueError) as error:
                LOG.info('help topic not kept error=%s', type(error).__name__)
            return found
        path = getattr(self, 'config_path', None) or os.environ.get('ASSISTANT_CONFIG') or ''
        if name == 'support_access':
            if not getattr(self, 'fleet', None):
                raise ValueError('This Machine isn’t linked to an account.')
            allow = args.get('allow')
            try:
                return self.fleet.support_access(None if allow is None else bool(allow))
            except (fleet.Off, OSError, ValueError) as error:
                LOG.info('support access not reached error=%s', type(error).__name__)
                if allow is None:
                    return {'until': self.fleet.support_until(), 'hours': self.fleet.SUPPORT_HOURS, 'accesses': [], 'error': True}
                raise ValueError('Can’t reach your account right now. Try again.') from None
        if name == 'bug_preview':
            return {**support.report(path, doctor=onboarding.doctor, budget=self.REPORT_BUDGET), 'paired': bool(getattr(self, 'fleet', None))}
        if name == 'bug_fixed':  # a bug the owner reported, fixed and running here now (fleet.Fleet.fixed); seen closes one
            if not getattr(self, 'fleet', None):
                return {'fixed': []}
            try:
                return {'fixed': self.fleet.fixed(args.get('seen') or None)}
            except (fleet.Off, fleet.Unavailable, OSError, ValueError) as error:
                LOG.info('fixed reports not read error=%s', type(error).__name__)
                return {'fixed': [], 'error': True}
        if name == 'bug_queued':  # the reports still waiting to go out (bug_queue.py)
            return {'queued': bug_queue.view(self.config)}
        if name == 'bug_offer_open':  # a report written up in chat (bug_offer), to fill Report a bug; sent marks it sent
            found = bug_queue.offered(self.config, str(args.get('id') or '') or None, args.get('sent') is True)
            return {'offer': {k: found[k] for k in ('id', 'words', 'summary', 'sent')} if found else None}
        text = str(args.get('description') or '').strip()[:self.BUG_TEXT]
        if not text:
            raise ValueError('Say what went wrong first.')
        shot = args.get('screenshot')
        if shot is not None and not (isinstance(shot, str) and re.fullmatch(r'data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+', shot)
                                     and len(shot) <= self.BUG_SHOT_BYTES * 4 // 3 + 64):
            raise ValueError('That screenshot can’t be sent. Try a smaller PNG or JPEG.')
        report = args.get('report')
        if report is not None and not isinstance(report, dict):
            raise ValueError('That report can’t be sent.')
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine isn’t linked to an account. Email support@themachine.computer instead.')
        # What the owner saw, scrubbed once more here: whatever the page sent, nothing else leaves
        body = {'description': text, 'screenshot': shot,
                'report': support.scrub_value(report) if report is not None else None}
        # Sent now, or kept here and sent by itself later when the control plane can't take it now (bug_queue.py):
        # bug_later is a hosted dashboard's report its control plane refused for now, kept the same way
        # Include a support report ticked, on a self-hosted Machine: kept here at once (it is never lost) and sent by the
        # worker right away, with the report built there; the dashboard doesn't wait for the checks and logs.
        if name == 'bug_send' and args.get('diagnostics') and report is None:
            item = bug_queue.add(self.config, {**body, 'diagnostics': True}, now=True)
            if getattr(self, 'bug_queue_wake', None):
                self.bug_queue_wake.set()
            return {'sent': True, 'id': item['id']}
        retry_after = 0
        if name == 'bug_later':
            try:
                retry_after = max(0, min(int(args.get('retry_after') or 0), 86400))
            except (TypeError, ValueError):
                retry_after = 0
        else:
            try:
                return {'sent': True, **(self.fleet.bug_report(body) or {})}
            except Exception as error:  # noqa: BLE001 - said to the owner below
                LOG.info('bug report not sent now error=%s', type(error).__name__)
                if not bug_queue.retryable(error):
                    said = str(error)  # the control plane's reason when it is one for the owner (a sentence), else ours
                    raise ValueError(said if said.endswith('.') else 'The report didn’t go out. Email support@themachine.computer.') from None
                retry_after = getattr(error, 'retry_after', 0)
        item = bug_queue.add(self.config, body, retry_after)
        if getattr(self, 'bug_queue_wake', None):
            self.bug_queue_wake.set()
        return {'sent': False, 'queued': True, 'at': item['next_at']}

    def bug_offer(self, args):
        """A problem with The Machine itself, told in chat (assistant_signals bug_offer, `assistant report-bug`): the
        report written up for Report a bug (bug_queue.offer), with the link that opens it filled in. The owner checks it
        there and taps Send; nothing goes from here. A Machine with no account to send to says where to write instead."""
        hosted = str(self.config.get('manage_url') or '').startswith('https://')
        if not hosted and not getattr(self, 'fleet', None):
            return {'linked': False, 'say': ('This Machine isn’t linked to an account, so it can’t send a report. Say they can email '
                                              'support@themachine.computer (with a file from `assistant support-bundle` if they like) '
                                              'or open an issue at https://github.com/Salesflare/TheMachine/issues. Nothing was sent or filed.')}
        item = bug_queue.offer(self.config, args.get('words'), args.get('summary'))
        host = str(self.config.get('dashboard_host') or '')
        url = 'https://' + host + self.config.get('dashboard_path', '/') + '#bug-offer=' + item['id'] if host else None
        how = f'Tap to check it and send: {url}' if url else 'Open Help, then Report a bug, in the dashboard: it is filled in there.'
        return {'linked': True, 'id': item['id'], 'url': url,
                'say': ('Offer it in one short message: you wrote it up as a bug report for The Machine team. ' + how +
                        ' Nothing is sent until they tap Send there. Never say it was sent, filed or that anyone is looking at it.')}

    def account_view(self):
        """Settings, Account on a self-hosted Machine paired with the Network: its owner's account in short, from the
        control plane (fleet.Fleet.account). A hosted Machine's dashboard asks the control plane itself, with the owner's
        sign-in on that host (/_machine/account), so this Machine never holds what opens the account's pages."""
        if not getattr(self, 'fleet', None):
            return {'on': False}
        try:
            return {'on': True, **self.fleet.account()}
        except (fleet.Off, ValueError, OSError) as error:
            LOG.info('account summary unavailable error=%s', type(error).__name__)
            return {'on': True, 'error': 'Can’t reach your account right now.'}

    def note_connections(self):
        """Activity: remember the connections there are now, so one added or removed since shows (activity_log.py).
        Never stops the service: a failed note only costs that line."""
        try:
            with self.store.connect() as db:
                activity_log.note_accounts(db, self.config.get('accounts') or [], now())
        except sqlite3.Error as error:
            LOG.warning('activity connections not noted error=%s', type(error).__name__)

    def activity_view(self, kind='', cursor=0, outcome='', actor=''):
        """Settings, Activity: one page of everything The Machine did, newest first (activity_log.page). Read-only."""
        self.note_connections()
        with self.store.connect() as db:
            return activity_log.page(db, self.config, kind, cursor, outcome=outcome, actor=actor)

    def security_view(self):
        """Settings, Security: the owner's level (Standard, Careful or Custom) and each Work Fleet's."""
        try:
            with self.store.connect() as db:
                return security_levels.view(db)
        except sqlite3.Error:
            return None

    @property
    def dictation_openai(self):
        """Voice input's openai engine with OpenClaw kept loaded (voice-openai-run.mjs), so a clip takes a second or two."""
        if getattr(self, '_voice_oa', None) is None:
            self._voice_oa = voice_input.OpenAIVoice(self.dictation.root / 'clips',
                                                     lambda: ([node_bin(self.config), str(Path(__file__).resolve().parent / 'voice-openai-run.mjs')], self.talk_env()))
        return self._voice_oa

    def voice_warm_worker(self):
        """Gets this Machine's own voice engine ready in the background, so a tap on the mic never waits on a download.
        Never during setup: only once this Machine is live (its first full review is done) and has been quiet for a while
        (VOICE_WARM_QUIET checks in a row: no review or preparation running, load under half the cores). Only when it
        will use it (no OpenAI here, or On this Machine picked) and there's room on disk. The same after an update that
        changes its packages. The install runs at a lower priority (voice_input.lowered). Until then a tap uses OpenAI or
        the browser's own speech recognition (voice_view's `use`)."""
        tried, quiet = 0.0, 0
        try:
            self.voice_openai(True, wait=True)   # known before the first tap: whether Automatic means OpenAI here
        except Exception as error:
            LOG.error('voice openai check error=%s', type(error).__name__)
        while not self.stop.wait(300):
            try:
                with self.store.connect() as db:
                    prefs = voice_input.prefs(db)
                    live = db.execute("SELECT 1 FROM review_runs WHERE status='ok' AND NOT COALESCE(window_hours,0) LIMIT 1").fetchone()
                    busy = db.execute("SELECT (SELECT count(*) FROM preparations WHERE status IN ('starting','running'))"
                                      "+(SELECT count(*) FROM review_runs WHERE status IN ('starting','running','recovering'))").fetchone()[0]
                openai = self.voice_openai(True, wait=True)   # kept 10 minutes: OpenAI connected later switches Automatic to it
                quiet = quiet + 1 if live and not busy and voice_input.idle() else 0
                status = self.dictation.status(prefs['model'])
                if quiet < VOICE_WARM_QUIET or (status['state'] == 'failed' and time.monotonic() - tried < 6 * 3600):
                    continue
                if voice_input.warm_due(prefs, openai, status, self.dictation.room()):
                    tried = time.monotonic()
                    LOG.info('voice warm start model=%s', prefs['model'])
                    self.dictation.prepare(prefs['model'])
            except Exception as error:
                LOG.error('voice warm error=%s', type(error).__name__)

    def learnings_view(self):
        """Feedback, Share learnings with The Machine team, and its Settings switch (team_learnings.py)."""
        try:
            with self.store.connect() as db:
                # and Share what Help is asked (help_topics.py) and Send error reports (error_feed.py), on the same Settings card
                return {**team_learnings.view(db, network=bool(getattr(self, 'fleet', None))), 'help_topics': help_topics.on(db), 'errors': error_feed.on(db)}
        except sqlite3.Error:
            return None

    HELP_TOPICS_SECONDS = 6 * 3600

    def help_topics_send(self):
        """Now and then: the finished days of Help topics to the control plane (help_topics.send), when sharing is on."""
        due = getattr(self, '_help_topics_at', 0)
        if time.monotonic() < due:
            return 0
        self._help_topics_at = time.monotonic() + self.HELP_TOPICS_SECONDS
        try:
            return help_topics.send(self.store.connect, self.fleet.relay.call)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('help topics error=%s', type(error).__name__)
            return 0

    def error_reports_step(self):
        """Every ten minutes, over the Network: the errors counted since the last batch, as signatures (error_feed.py).
        The names this Machine knows are taken out once more first."""
        def names():
            with self.store.connect() as db:
                return [name for name, _ in team_learnings.known_names(db, self.config)]
        try:
            return error_feed.send(self.store.connect, self.fleet.relay.call, names)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('error reports error=%s', type(error).__name__)
            return 0

    def pacing_send(self):
        """Once a day, with error reports on: the finished days' pacing counts and minutes to the control plane."""
        try:
            return pacing.send(self.store.connect, self.fleet.relay.call)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('pacing report error=%s', type(error).__name__)
            return 0

    def protection_now(self, config):
        """What the Store does with message protection at this start: on unless config.json says false. A change to an
        existing database (an upgrade that turns it on by default, say) waits while a review, preparation or profile
        turn runs, so none is cut off: the app starts as it was and restarts itself once they are done
        (`protection_waiter`). The change itself keeps a copy until it checks out (Store.message_protection)."""
        self.protection_waits = False
        want = message_seal.wanted(config)
        sealed, _ = message_seal.state(config['database'])
        if sealed is None or sealed == want:
            return want
        running = message_seal.work_running(config['database'])
        if running == 0:
            return want
        self.protection_waits = True
        LOG.info('message contents will be %s once The Machine is idle (%s running)', 'sealed' if want else 'opened',
                 running if running is not None else 'unknown')
        return None

    def protection_waiter(self, every=30):
        """Restart once nothing runs, so the next start seals (or opens) the database with nothing cut off."""
        while not self.stop.wait(every):
            if message_seal.work_running(self.config['database']) == 0:
                if restart_self():
                    LOG.info('idle: restarting to apply message protection')
                else:
                    LOG.info('idle: message protection applies at the next start')
                return

    def packed_page(self, etag, coding, page):
        """The dashboard page compressed in `coding`, made once per page (its ETag) and coding: the best compression,
        since it goes to every device opening the app. A few kept (one owner, a host or two, a coding or two)."""
        key = (etag, coding)
        with self._packed_lock:
            if key in self._packed:
                return coding, self._packed[key]
        data = compress_body(page.encode(), coding, best=True)
        with self._packed_lock:
            self._packed[key] = data
            while len(self._packed) > 6:
                self._packed.pop(next(iter(self._packed)))
        return coding, data

    def serve(self):
        app = self
        self._packed, self._packed_lock = {}, threading.Lock()
        try:  # saved sign-ins kept with a key of their own (or opened by an import) go over to the message key
            if browser_login.LoginStore(Path(self.config['database']).expanduser().parent).migrate():
                LOG.info('saved sign-ins are now encrypted with the message key')
        except Exception as error:  # they stay as they were; the next start tries again
            LOG.warning('saved sign-ins not moved to the message key: %s', type(error).__name__)

        Handler = make_handler(app)

        server = http.server.ThreadingHTTPServer(('127.0.0.1', self.config.get('port', 8787)), Handler)
        watch_faults(self.store)
        if getattr(self, 'agents', None):
            self.agents.version = self.store.code_version  # failed jobs in the error reports carry it
            try:
                self.agents.recover()  # a job that ran when the service stopped, or one still waiting for a slot
            except Exception as error:  # noqa: BLE001 - never stops the service
                LOG.error('agent jobs recover error=%s', type(error).__name__)
            if getattr(self, 'fleet', None) and not self.config.get('manage_url') and agent_jobs.find('codex'):
                # Paired with the owner's account on their own computer: Codex jobs their hosted Machine hands here
                # (Where Codex runs: On my computer) run with this computer's own Codex (agent_remote.serve)
                import agent_remote
                threading.Thread(target=agent_remote.serve, args=(self.agents, self.stop), daemon=True, name='agent-serve').start()
        if getattr(self, 'skills', None):
            self.skills.sync()  # the workspace has the skills that are on, also after edits made while this was off
        signal.signal(signal.SIGTERM, lambda *_: self.stop_all())
        signal.signal(signal.SIGINT, lambda *_: self.stop_all())
        try:  # a work removal that was going on: what a sync stored meanwhile goes too; old safety copies go
            if work_removal.settle(self.config, self.store):
                self.graph_dirty.set()
            work_removal.prune(self.config)
        except Exception as error:  # noqa: BLE001 - never stops the service
            LOG.error('work removal settle error=%s', type(error).__name__)
        for account in self.config['accounts']:
            # Brings in signals off (abilities.py): no sync; a Docs connection still checks what it may do, now and then
            threading.Thread(target=self.collector if abilities.signals_on(account) else self.ability_checker, args=(account,),
                             daemon=True).start()
        threading.Thread(target=self.delivery_worker, daemon=True).start()
        threading.Thread(target=self.preparation_worker, daemon=True).start()
        threading.Thread(target=self.whatsapp_photo_worker, name='whatsapp-photos', daemon=True).start()
        threading.Thread(target=self.voice_warm_worker, name='voice-warm', daemon=True).start()
        threading.Thread(target=self.action_worker, daemon=True).start()
        threading.Thread(target=self.review_worker, daemon=True).start()
        threading.Thread(target=self.graph_worker, daemon=True).start()
        if getattr(self, 'fleet', None):
            self.fleet_stop = threading.Event()  # set by Unpair (fleet_drop) and when the service stops
            threading.Thread(target=self.fleet.run, args=(self.fleet_stop,), daemon=True).start()
            self.ai_reach_start(self.fleet_stop)
        threading.Thread(target=self.model_usage_worker, daemon=True).start()
        if getattr(self, 'fleet', None):
            threading.Thread(target=self.bug_queue_worker, name='bug-queue', daemon=True).start()
        threading.Thread(target=self.retention_worker, daemon=True).start()
        threading.Thread(target=self.history_worker, name='history', daemon=True).start()  # older messages, as history (machine/app/history.py)
        self.meeting_write_resume()  # Generate notes that were going when the service stopped
        self.gbrain_start()  # GBrain (gbrain.py): only when the owner turned it on
        if getattr(self, 'skills', None) and self.skills.catalog:  # what OpenClaw has, for Settings > Skills and skill hints
            threading.Thread(target=self.skills.catalog.worker, args=(self.stop,), daemon=True).start()
        if embeddings.settings(self.config):
            threading.Thread(target=self.embedding_worker, daemon=True).start()
        # Always: photos and facts from the owner's own connections need no look-up service (its steps skip themselves).
        threading.Thread(target=self.enrichment_worker, daemon=True).start()
        threading.Thread(target=self.recurring_worker, name='recurring', daemon=True).start()  # recurring to-dos (recurring_app.py)
        if getattr(self, 'protection_waits', False):
            threading.Thread(target=self.protection_waiter, daemon=True).start()
        server.timeout = 1
        LOG.info('service started; loopback only; accounts=%d', len(self.config['accounts']))
        while not self.stop.is_set():
            server.handle_request()
        server.server_close()


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
