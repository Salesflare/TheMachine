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
    WorkersApp,
    google_photo_accounts,
    google_photo_offers,
)
from machine.app.voice import (
    VOICE_WARM_QUIET,
)


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

    def gbrain_save(self, value):
        save_hours(self.config_path, {'gbrain': value})
        self.config['gbrain'] = value

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

    def is_work(self, account_ids):
        if isinstance(account_ids, str):
            account_ids = json.loads(account_ids or '[]')
        return any(a['id'] in (account_ids or []) and a.get('boundary', '').startswith('work:') for a in self.config.get('accounts', []))

    def is_work_suggestion(self, suggestion_id):
        with self.store.connect() as db:
            row = db.execute('SELECT account_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        return bool(row) and self.is_work(row['account_ids'])

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

    @property
    def dictation_openai(self):
        """Voice input's openai engine with OpenClaw kept loaded (voice-openai-run.mjs), so a clip takes a second or two."""
        if getattr(self, '_voice_oa', None) is None:
            self._voice_oa = voice_input.OpenAIVoice(self.dictation.root / 'clips',
                                                     lambda: ([node_bin(self.config), str(Path(__file__).resolve().parent / 'voice-openai-run.mjs')], self.talk_env()))
        return self._voice_oa

    HELP_TOPICS_SECONDS = 6 * 3600

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
