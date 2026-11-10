"""Who may call which action: the *_ACTIONS sets. OWNER_ACTIONS is what only the owner may do (the CLI refuses them),
DASHBOARD_ACTIONS what the dashboard may post to /api/action, and each domain's set is added to them here. These sets
are the security boundary and stay together in this one file, one name per line, sorted (tests/test_owner_boundary.py
checks; scripts/merge_friendly.py lays them out). Moved out of assistant.py as is; assistant.py imports every name back."""
import handoff_mail
import task_pages


# Owner decisions/feedback. Only the bridge's verified Telegram handlers and the
# authenticated dashboard may record them; never the local CLI the agent can run.
CONNECT_ACTIONS = (
    'codex_signin',
    'codex_signin_state',
    'connect_abilities',
    'connect_answer',
    'connect_cancel',
    'connect_poll',
    'connect_remove',
    'connect_running',
    'connect_scope',
    'connect_signin',
    'connect_signin_state',
    'connect_site_signin',
    'connect_sources',
    'connect_start',
)


OWNER_ACTIONS = {
    *CONNECT_ACTIONS,
    'bind_feedback_prompt',
    'board_default',
    'board_delete',
    'board_dismiss',
    'board_fit',
    'board_save',
    'browser_focus',
    'browser_login_check',
    'browser_login_choose',
    'browser_login_fill',
    'browser_login_forget',
    'browser_login_open',
    'browser_login_pages',
    'browser_logins',
    'card_chat',
    'confirm_action',
    'connector_contact_sync',
    'connector_sync',
    'decide',
    'detect_signature',
    'edit_fact',
    'feedback_reply',
    'fleet_ask',
    'fleet_brief',
    'fleet_brief_hide',
    'fleet_decide',
    'fleet_free',
    'fleet_learning_remove',
    'fleet_meetings',
    'fleet_notice_decide',
    'fleet_rule',
    'fleet_take',
    'follow_up_bring_back',
    'follow_up_change',
    'follow_up_end',
    'follow_up_pause',
    'follow_up_save',
    'follow_up_settings',
    'follow_up_stop',
    'forget_fact',
    'graph_fact_add',
    'graph_fact_unlink',
    'graph_new',
    'graph_org_delete',
    'graph_org_edit',
    'graph_org_wrong',
    'graph_person_delete',
    'graph_person_edit',
    'graph_person_org',
    'graph_picture',
    'graph_pictures_found',
    'graph_relation',
    'graph_rename',
    'graph_role',
    'graph_same',
    'graph_same_all',
    'graph_show_person',
    'graph_stage',
    'graph_summary',
    'graph_warmup',
    'knowledge_export',
    'learned_close',
    'learned_fix',
    'learning_undo',
    'meeting_notes_write',
    'model_reset',
    'model_usage_refresh',
    'own_address',
    'own_domain',
    'project_about',
    'project_archive',
    'project_delete',
    'project_outcome',
    'project_save',
    'project_visibility',
    'promise_close',
    'promise_due',
    'promise_todo',
    'recap_decide',
    'recap_set',
    'request_feedback',
    'review_now',
    'revise_draft',
    'security_level',
    'security_setting',
    'set_people_lookup',
    'set_signature',
    'set_voice',
    'set_work_hours',
    'setup_dismiss',
    'setup_restore',
    'tip_done',
    'undo_merge',
    'unmerge_fact',
    'whats_new_seen',
    'whatsapp_photos',
}
# Warm intros, handoffs and shared follow-ups (fleet_requests.py): the owner's own, from their dashboard only.
FLEET_REQUEST_ACTIONS = {
    *handoff_mail.ACTIONS,
    *task_pages.ACTIONS,
    'fleet_handoff',
    'fleet_handoff_draft',
    'fleet_handoff_email',
    'fleet_handoff_mine',
    'fleet_handoff_not_mine',
    'fleet_handoff_take_back',
    'fleet_intro',
    'fleet_review_apply',
    'fleet_review_ask',
    'fleet_review_options',
    'fleet_review_reply',
    'fleet_review_view',
    'fleet_review_withdraw',
    'fleet_split',
    'fleet_split_adjust',
    'fleet_split_dismiss',
    'task_import',
}
OWNER_ACTIONS |= FLEET_REQUEST_ACTIONS
# Friends (friends.py): adding, accepting, removing and blocking friends, and asking a friend when they are free.
# Shared connectors (shared_connectors.py): sharing, OKs, replacing and stopping, from the owner's dashboard only.
SHARE_ACTIONS = {
    'fleet_share',
    'fleet_share_ok',
    'fleet_share_replace',
    'fleet_share_stop',
}
OWNER_ACTIONS |= SHARE_ACTIONS
# The Shared Graph (shared_graph.py): a thread's Team or Only you, Keep private, asking an admin to stop sharing, and
# Ask <name>, the owner's own.
GRAPH_SHARE_ACTIONS = {
    'graph_ask',
    'graph_board_share',
    'graph_connection',
    'graph_optout',
    'graph_pause',
    'graph_policy',
    'graph_private',
    'graph_rekey_no',
    'graph_remove',
    'graph_rule',
    'graph_share',
    'graph_share_all',
    'graph_share_many',
    'graph_start',
    'graph_thread_share',
}
OWNER_ACTIONS |= GRAPH_SHARE_ACTIONS
FRIEND_ACTIONS = {
    'fleet_availability',
    'fleet_friend',
    'fleet_network',
}  # fleet_network: finding people on the Network (discovery.py)
OWNER_ACTIONS |= FRIEND_ACTIONS
# Sharing a contact (contact_share.py): what can go, the exact preview, Send, and Add or Dismiss on one shared here.
# The owner's own, from their dashboard only.
CONTACT_ACTIONS = {
    'fleet_contact_decide',
    'fleet_contact_options',
    'fleet_contact_preview',
    'fleet_contact_send',
}
OWNER_ACTIONS |= CONTACT_ACTIONS
# Family (family.py): asking when everyone is free, proposing a to-do or a plan. The owner's own, from their dashboard.
FAMILY_ACTIONS = {
    'family_event',
    'family_free',
    'family_invite',
    'family_invite_setting',
    'family_still_needed',
    'family_todo',
}
OWNER_ACTIONS |= FAMILY_ACTIONS
# Cards the owner makes, renames, moves to another area, or merges when the review asks: theirs alone, from the dashboard.
CARD_ACTIONS = {
    'card_merge',
    'card_move',
    'card_new',
    'card_project',
    'card_rename',
    'card_repeat',
    'card_repeat_skip',
    'card_report_seen',
    'card_use_sources',
    'recurring_offer',
    'repeat_read',
}
OWNER_ACTIONS |= CARD_ACTIONS
# A card chat's Stop button and the files added to a message (chat_files.py): the owner's own, from the dashboard.
# The model and thinking level for chats (chat_model.py): the default (Settings, Model) and one to-do chat's own;
# the person's Fast choice for to-do chats.
CHAT_ACTIONS = {
    'chat_fast_set',
    'chat_file_remove',
    'chat_model_default',
    'chat_model_set',
    'chat_stop',
    'chat_upload',
}
OWNER_ACTIONS |= CHAT_ACTIONS
# Ask from search (search_ask.py): a question typed into Search answered from the owner's own messages in the area
# they look at, as a one-shot turn without tools. It reads and answers; it never sends, drafts or makes a to-do.
SEARCH_ASK_ACTIONS = {
    'search_ask',
    'search_ask_examples',
}
OWNER_ACTIONS |= SEARCH_ASK_ACTIONS
# Voice input (voice_input.py): the owner's mic in the dashboard's message boxes, and its choices in Settings. The text
# lands in the box; it never sends anything.
VOICE_ACTIONS = {
    'voice_prefs',
    'voice_prepare',
    'voice_status',
    'voice_transcribe',
}
OWNER_ACTIONS |= VOICE_ACTIONS
# Talk live (talk_live.py): a spoken conversation about a to-do, from the owner's dashboard only. It reads, asks the
# to-do's chat as a typed message would, and sends one draft on screen only after a confirm question and a clear yes.
TALK_ACTIONS = {
    'draft_seen',
    'talk_ask_send',
    'talk_end',
    'talk_focus',
    'talk_line',
    'talk_offer',
    'talk_send',
    'talk_start',
    'talk_status',
    'talk_tool',
    'talk_undo',
}
OWNER_ACTIONS |= TALK_ACTIONS
# Skills (skills.py): writing, sharing and installing them is the owner's own, from the dashboard. The agent can only
# propose one (skill_propose), which waits for the owner's Approve.
# Everything else OpenClaw has (skill_installed*, skill_hub_*): shown read-only; OpenClaw's own on/off and ClawHub install, on the owner's tap.
# Importing from Claude and ChatGPT (skill_import_*): listed for the owner to tick; a skill with scripts only as OpenClaw's own, after reading.
SKILL_ACTIONS = {
    'skill_decide',
    'skill_delete',
    'skill_example',
    'skill_get',
    'skill_hint_dismiss',
    'skill_hub_get',
    'skill_hub_install',
    'skill_hub_search',
    'skill_import_find',
    'skill_import_install',
    'skill_import_paste',
    'skill_import_read',
    'skill_import_run',
    'skill_import_signin',
    'skill_import_status',
    'skill_import_upload',
    'skill_installed',
    'skill_installed_get',
    'skill_installed_toggle',
    'skill_save',
    'skill_share',
    'skill_toggle',
}
OWNER_ACTIONS |= SKILL_ACTIONS
# Bigger requests only for these (an uploaded skill export, the Find my skills turn's report), marked X-Upload: skill-import.
# Hand to Claude Code / Hand to Codex (agent_jobs.py): the owner's own, from their dashboard only.
AGENT_ACTIONS = {
    'agent_cancel',
    'agent_draft',
    'agent_follow_up',
    'agent_outcome',
    'agent_retry',
    'agent_send',
    'set_agents',
}
OWNER_ACTIONS |= AGENT_ACTIONS
# Learnings for The Machine team (team_learnings.py): sharing, Not now, Never ask and the Settings switch are the owner's
# own, from their dashboard only. Nothing is sent without their Send on exactly what they saw, or their choice to send
# automatically from now on; withdrawing a sent one is theirs too.
LEARNING_ACTIONS = {
    'bring_in_decide',
    'learnings_later',
    'learnings_never',
    'learnings_share',
    'learnings_votes_decide',
    'learnings_withdraw',
    'missed_work_label',
    'set_error_reports',
    'set_help_topics',
    'set_learnings_auto',
    'set_learnings_offer',
    'set_learnings_vote',
}
OWNER_ACTIONS |= LEARNING_ACTIONS
# The Graph as a CRM (crm.py, crm_import.py): who owns a record, one organization with several websites, and a
# spreadsheet imported; the owner's own, from their dashboard only.
CRM_ACTIONS = {
    'graph_field_delete',
    'graph_field_save',
    'graph_field_set',
    'graph_import_ai',
    'graph_import_ai_status',
    'graph_import_preview',
    'graph_import_run',
    'graph_import_undo',
    'graph_org_apart',
    'graph_org_merge',
    'graph_org_split',
    'graph_owner',
    'graph_tag',
}
OWNER_ACTIONS |= CRM_ACTIONS
# Help (help_chat.py) and Report a bug (support.report): the owner's own, from their dashboard only. help_ask answers
# and changes nothing; help_article reads one public help article in the owner's language; bug_send sends what the
# owner wrote, after their tap, with the scrubbed support report (bug_preview, the same report) only when they left
# Include a support report ticked. bug_offer_open reads a report the agent wrote up in chat (bug_offer, which sends
# nothing) to fill Report a bug, and marks it sent once the owner sent it.
# support_access: the owner's switch for Support access on a paired self-hosted Machine (fleet.Fleet.support_access).
SUPPORT_ACTIONS = {
    'bug_fixed',
    'bug_later',
    'bug_offer_open',
    'bug_preview',
    'bug_queued',
    'bug_send',
    'help_article',
    'help_ask',
    'support_access',
}
OWNER_ACTIONS |= SUPPORT_ACTIONS
# GBrain (gbrain.py, optional): turning it on (with the owner's consent), Work too, and off; the owner's own, from the
# dashboard only (Connections, + Add, GBrain).
GBRAIN_ACTIONS = {
    'gbrain_off',
    'gbrain_on',
    'gbrain_status',
    'gbrain_work',
}
OWNER_ACTIONS |= GBRAIN_ACTIONS
# Connected AIs (ai_app.py, docs/ai-connections.md): which outside AIs reach this Machine over MCP, at what access,
# for how long, Turn off now, and their activity. The owner's own, from the dashboard only; never the agent's.
AI_ACTIONS = {
    'ai_apply',
    'ai_change',
    'ai_connections',
    'ai_dismiss',
    'ai_key',
    'ai_off',
    'ai_pair_start',
    'ai_pair_state',
    'ai_remove',
    'ai_undo',
    'ai_unpair',
}
OWNER_ACTIONS |= AI_ACTIONS
# Scheduling between Machines (meet_app.py, docs/scheduling-between-machines.md): Book it, Other time or Not needed on
# a time another Machine agreed, and what other Machines may ask this one. The owner's own, from the dashboard only.
MEET_ACTIONS = {
    'meet_decide',
    'meet_setting',
}
OWNER_ACTIONS |= MEET_ACTIONS
# Settings, Export: export everything and import an export (machine/app/export.py). The owner's own, from the dashboard only.
EXPORT_ACTIONS = {
    'export_delete',
    'export_start',
    'export_status',
    'import_confirm',
    'import_discard',
    'import_stage',
}
OWNER_ACTIONS |= EXPORT_ACTIONS
# Routines (routines_app.py): make one, add a suggested one, edit it, change when, pause, resume, stop, Run now and turn an old
# OpenClaw job off; a to-do's offer to change its routine, saved or kept as is (routine_changes.py). The owner's own, from the
# dashboard only. A run's own report (routine_result) is the Gateway's, bound to its session by the plugin: never in these sets.
ROUTINE_ACTIONS = {
    'routine_accept',
    'routine_change_keep',
    'routine_change_save',
    'routine_cleanup',
    'routine_edit',
    'routine_new',
    'routine_old_job',
    'routine_run_now',
    'routine_state',
    'routine_template',
    'routine_try',
    'routine_when',
}
OWNER_ACTIONS |= ROUTINE_ACTIONS
# What the dashboard (and any client that isn't the Gateway) may call through /api/action; everything else is 403.
# test_dashboard_actions checks that every action dashboard.html posts is here.
DASHBOARD_ACTIONS = frozenset({
    *AGENT_ACTIONS,
    *AI_ACTIONS,
    *CARD_ACTIONS,
    *CHAT_ACTIONS,
    *CONNECT_ACTIONS,
    *CONTACT_ACTIONS,
    *CRM_ACTIONS,
    *EXPORT_ACTIONS,
    *FAMILY_ACTIONS,
    *FLEET_REQUEST_ACTIONS,
    *FRIEND_ACTIONS,
    *GBRAIN_ACTIONS,
    *GRAPH_SHARE_ACTIONS,
    *LEARNING_ACTIONS,
    *MEET_ACTIONS,
    *ROUTINE_ACTIONS,
    *SEARCH_ASK_ACTIONS,
    *SHARE_ACTIONS,
    *SKILL_ACTIONS,
    *SUPPORT_ACTIONS,
    *TALK_ACTIONS,
    *VOICE_ACTIONS,
    'app_push_register',
    'app_push_unregister',
    'board_default',
    'board_delete',
    'board_dismiss',
    'board_fit',
    'board_save',
    'browser_focus',
    'browser_login_check',
    'browser_login_choose',
    'browser_login_fill',
    'browser_login_forget',
    'browser_login_open',
    'browser_login_pages',
    'browser_logins',
    'browser_show',
    'calendar_write',
    'card_chat',
    'check_now',
    'client_error',
    'confirm_action',
    'connector_contact_sync',
    'connector_sync',
    'decide',
    'detect_signature',
    'edit_fact',
    'fleet_ask',
    'fleet_brief',
    'fleet_brief_hide',
    'fleet_decide',
    'fleet_free',
    'fleet_learning_remove',
    'fleet_meetings',
    'fleet_notice_decide',
    'fleet_rule',
    'fleet_take',
    'follow_up_bring_back',
    'follow_up_change',
    'follow_up_end',
    'follow_up_pause',
    'follow_up_save',
    'follow_up_settings',
    'follow_up_stop',
    'forget_fact',
    'graph_fact_add',
    'graph_fact_unlink',
    'graph_new',
    'graph_org_delete',
    'graph_org_edit',
    'graph_org_wrong',
    'graph_person_delete',
    'graph_person_edit',
    'graph_person_org',
    'graph_picture',
    'graph_pictures_found',
    'graph_relation',
    'graph_rename',
    'graph_role',
    'graph_same',
    'graph_same_all',
    'graph_show_person',
    'graph_stage',
    'graph_summary',
    'graph_warmup',
    'knowledge_export',
    'learned_close',
    'learned_fix',
    'learning_undo',
    'meeting_notes',
    'meeting_notes_write',
    'model_reset',
    'model_usage_refresh',
    'notify_active',
    'notify_preview',
    'notify_set',
    'own_address',
    'own_domain',
    'project_about',
    'project_archive',
    'project_delete',
    'project_outcome',
    'project_save',
    'project_visibility',
    'promise_close',
    'promise_due',
    'promise_todo',
    'push_subscribe',
    'push_test',
    'push_unsubscribe',
    'recap_decide',
    'recap_set',
    'review_now',
    'revise_draft',
    'security_level',
    'security_setting',
    'set_locale',
    'set_people_lookup',
    'set_signature',
    'set_voice',
    'set_work_hours',
    'setup_dismiss',
    'setup_restore',
    'tip_done',
    'undo_merge',
    'unmerge_fact',
    'whats_new_seen',
    'whatsapp_photos',
})
UPLOAD_ACTIONS = {
    'bug_fixed',  # Still not right on a fix notice: its optional screenshot
    'bug_later',
    'bug_send',
    'graph_import_ai',
    'graph_import_preview',
    'graph_import_run',
    'meeting_notes',
    'skill_import_report',
    'skill_import_upload',
    'skills_found',
}
