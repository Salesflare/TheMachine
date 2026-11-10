"""Where every table of The Machine's database goes in Knowledge for another AI (knowledge.py), or why it stays out.

tests/test_knowledge_export.py fails when a module creates a table that is in none of these, so new knowledge can't
be added without deciding whether the export carries it. The full export (moving.py) carries every table as is."""

# Exported: the table -> where it shows up (records/<name>.jsonl and the Markdown notes built from them)
EXPORTED = {
    'boards': 'entities (a project\'s board)',
    'crm_fields': 'entities (custom fields)',
    'crm_tags': 'entities (tags)',
    'crm_values': 'entities (custom fields)',
    'events': 'sources (id, kind, date; the text only with message text on)',
    'fact_about': 'facts (about)',
    'facts': 'facts, rules',
    'fleet_briefs': 'team_briefs',
    'graph_links': 'relationships',
    'graph_nodes': 'entities',
    'graph_relations': 'relationships (the owner\'s words)',
    'person_summaries': 'summaries',
    'projects': 'entities (a project\'s stage, next step, value)',
    'promises': 'promises',
    'skills': 'skills',
    'suggestions': 'todos (open ones)',
    'voices': 'writing_style',
}

# Read to decide what goes in or to connect it, not exported as such
READ = {
    'event_projects': 'which messages belong to an Only-you project (left out unless private is on)',
    'fleet_meta': 'which Work Fleets are Careful',
    'graph_events': 'which records a source message is about',
    'share_threads': 'threads kept private or judged sensitive (left out unless private is on)',
}

# Folded into graph_nodes by the Graph build (graph.build): exported through entities and relationships
FOLDED = {
    'contact_marks', 'graph_merges', 'graph_names', 'graph_resources', 'graph_same', 'hidden_domains', 'identity_names',
    'mail_hidden', 'mail_shown', 'manual_nodes', 'org_aliases', 'org_apart', 'org_edits', 'org_profiles', 'owner_numbers', 'person_edits', 'person_facts',
    'person_orgs', 'person_profiles', 'person_roles', 'project_org_fills', 'project_people', 'project_moves', 'record_owners',
    'role_corrections', 'side_changes', 'side_rule', 'slack_members',
}

# Left out, by why
LEFT_OUT = {
    'OpenClaw\'s own scheduled jobs (only the sandbox makes a stand-in; an install\'s are in OpenClaw)': {'cron_jobs'},
    'credentials and sign-ins (never exported)': {
        'agent_key_pins', 'ai_clients', 'ai_codes', 'ai_connections', 'ai_folded', 'ai_tokens', 'network_pins', 'network_sealed',
        'push_subscriptions', 'notify_app_devices',
    },
    'message contents and their search index (only references go in)': {
        'chat_files', 'chats', 'event_passages', 'event_search', 'event_vector_skips', 'event_vectors', 'events_monotonic', 'messages', 'outbox',
        'talk_lines', 'team_mail', 'android_inbox',
    },
    'teammates\' and other Machines\' data, not this Machine\'s learning': {
        'fleet_claims', 'fleet_handled', 'fleet_in', 'fleet_learn_read', 'fleet_learn_removed', 'fleet_learn_seen', 'fleet_learn_used',
        'fleet_learn_vectors', 'fleet_learnings', 'fleet_log', 'fleet_notices', 'fleet_out', 'fleet_requests', 'fleet_reviews', 'fleet_rules',
        'fleet_scopes', 'fleet_splits', 'network_aliases', 'network_looked', 'network_outbox', 'network_people', 'network_replies',
        'network_request_nodes', 'network_taken', 'network_twins', 'share_lines', 'share_meta', 'share_out', 'share_people', 'share_private',
        'share_rules', 'team_asks', 'team_blobs', 'team_files', 'team_pending', 'team_records', 'team_sources', 'team_wants',
        'contact_shares', 'family_invite_log', 'family_invite_offers',
    },
    'settings, kept by the full export': {
        'enrich_prefs', 'error_feed_prefs', 'follow_up_rules', 'handoff_mail_prefs', 'meet_prefs', 'notify_prefs', 'pacing_prefs',
        'security_prefs', 'team_learning_prefs', 'voice_prefs', 'whatsapp_photo_prefs', 'own_address_choices', 'own_addresses',
        'own_domains', 'own_address_fetched', 'chat_models',
    },
    'photos and logos (images, not knowledge)': {
        'contact_photo_links', 'contact_photo_runs', 'org_logo_retries', 'org_logo_tries', 'person_photo_tries', 'person_photos',
        'photo_asks', 'telegram_photo_asks', 'whatsapp_photo_asks', 'whatsapp_photos',
    },
    'derived from the Graph and rebuilt from it on import': {'graph_identifiers'},
    'in the owner\'s own GBrain already': {'gbrain_meta', 'gbrain_notes', 'gbrain_pages'},
    'proposals the owner has not taken on': {
        'board_suggestions', 'skill_clusters', 'skill_hints', 'team_learning_votes', 'team_learnings', 'board_fits', 'tool_approval_proposals',
    },
    'how The Machine runs: queues, runs, logs, caches and checks': {
        'action_jobs', 'activity_accounts', 'activity_blocks', 'activity_seen', 'agent_jobs', 'agent_relayed', 'agent_result_receipts',
        'ai_activity', 'ai_writes', 'analyses', 'android_feed_health', 'android_receipts', 'board_backfill_asks', 'board_backfills',
        'board_backfills_queued', 'board_fit_undo', 'board_offers', 'calendar_clashes', 'calendar_writes', 'card_moves', 'card_uses', 'data_stamps', 'chat_fast_sessions',
        'chat_stops', 'checkpoints', 'decision_annotations', 'decisions', 'deliveries', 'draft_edits', 'draft_saves', 'draft_seen',
        'edits_offered', 'email_bounce_cc', 'email_bounce_cc_scan', 'email_bounce_events', 'email_bounce_scan', 'email_bounces', 'error_feed', 'fact_vectors', 'fault_versions',
        'faults', 'feedback_prompts', 'first_look_ahead', 'gateway_starts', 'follow_up_advice', 'follow_up_basis', 'follow_up_cards', 'follow_up_changes',
        'follow_up_ends', 'follow_up_holds', 'follow_up_pace', 'follow_up_pauses', 'follow_up_sends', 'follow_up_threads',
        'forgotten_people', 'forgotten_salt', 'graph_edits', 'graph_history', 'graph_history_events', 'graph_imports', 'graph_offers', 'graph_org_asks', 'graph_role_asks',
        'graph_state', 'graph_unnamed', 'handoff_mails', 'help_topics', 'history_backfill', 'learned_fixes', 'learning_changes', 'learning_signals',
        'learning_state', 'meet_links', 'meet_log', 'meet_pins', 'meet_seen', 'meet_sessions', 'meeting_moves', 'meeting_writes', 'memory_use',
        'merge_effects', 'milestones', 'missed_audit_calibration', 'missed_audit_items', 'missed_audits', 'moved_in', 'note_kinds', 'notify_app_lines',
        'notify_digests', 'notify_queue', 'pacing_starts', 'person_summary_runs', 'preparation_calls', 'preparation_runs', 'preparations',
        'profile_runs', 'project_org_backfill', 'project_success', 'promise_log', 'promises_next', 'recap_items', 'recaps', 'record_changes',
        'recurring_cards', 'recurring_offers', 'recurring_series', 'mail_cleanup_items', 'mail_cleanup_senders', 'retention_runs', 'routine_changes', 'routine_runs', 'routines', 'review_runs', 'review_save_failures', 'rule_changes', 'self_record_backups',
        'skill_task_decided', 'slipped', 'state', 'store_fixes', 'plain_key_pass', 'suggestion_keys', 'sync_activity', 'sync_daily', 'task_pages',
        'thread_snoozes', 'voice_merges',
    },
}


def classified():
    """{table: where} for every table this file knows."""
    out = {**EXPORTED, **READ, **{t: 'folded into graph_nodes' for t in FOLDED}}
    for why, tables in LEFT_OUT.items():
        out.update({t: 'left out: ' + why for t in tables})
    return out
