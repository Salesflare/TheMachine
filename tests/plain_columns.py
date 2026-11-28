"""Every text column of the database that message protection leaves plain, with why (message_seal.DERIVED has the sealed
ones). test_message_seal fails when a text column is in neither, so a new one is decided on the day it is made.

Text derived from messages, or written by a model about them, is sealed. Plain are codes (a word the code chose, an id,
a time, a hash, a number, a JSON list of those) and, on purpose, the words in WORDS. Codes are checked, not trusted:
`python -m plain_columns test_x` runs a suite with a guard on every code column of every database the suite makes, and
a write of words to one fails. scripts/test.py runs the suites in PLAIN_CHECKED that way."""
import re

# By name: an id, a time, a hash, a kind, a state, … A column whose name ends so holds no words, or is in WORDS.
CODE_NAME = re.compile(
    r'[._](id|ids|at|hash|sha|status|kind|until|state|day|date|due|on|since|period|token|version|revision|lang|cursor|seq|mode|choice|'
    r'direction|stage|phase|tag|key|tool|place|by|model|role|run|session|account|thread|node|fleet|member|source)$')

# Other names, the same: what the code writes there is a code, an id, a time, a number, or JSON of those.
CODES = '''
activity_accounts.service activity_seen.ref agent_jobs.outcome ai_activity.outcome ai_activity.args
agent_key_pins.slot agent_key_pins.fingerprint ai_clients.auth_method ai_codes.challenge ai_connections.level ai_connections.area
ai_connections.events ai_event_seen.item ai_event_subs.args ai_event_subs.name
analyses.items analyses.resumed_from android_feed_health.last_checked android_feed_health.last_recorded android_inbox.payload
board_backfill_asks.fit board_backfills.ranked board_fits.fit board_suggestions.projects boards.visibility board_suggestions.visibility
bring_in_lines.line bring_in_items.file bring_in_lines.file calendar_clashes.side calendar_writes.op calendar_writes.payload
calendar_writes.result card_moves.area card_moves.accounts_before card_moves.area_before chat_files.mime chat_models.thinking
chat_stops.via checkpoints.last_success crm_fields.type data_stamps.name draft_seen.digest
email_bounce_events.via email_bounce_cc_scan.flagged event_vector_skips.reason
facts.merged_into facts.side fact_search_config.k fact_search_config.v family_invite_log.what fault_versions.fingerprint
faults.fingerprint faults.origin first_pass.verdict first_pass.what fleet_briefs.every fleet_claims.offer
fleet_learn_removed.fp fleet_learn_seen.fp fleet_learn_used.fp fleet_learn_vectors.fp fleet_learnings.fp fleet_notices.reason
fleet_out.context fleet_questions.hold fleet_splits.meeting fleet_reviews.scope fleet_reviews.decided fleet_rules.rule fleet_scopes.scope folder_overviews.basis
follow_up_basis.basis follow_up_cards.channel follow_up_cards.why follow_up_holds.why follow_up_pauses.scope follow_up_rules.scope
follow_up_rules.settings follow_up_sends.batch follow_up_sends.grp forgotten_people.digest forgotten_salt.salt
gbrain_pages.section graph_imports.counts graph_links.a graph_links.b graph_merges.a graph_merges.b graph_relations.a graph_relations.b
graph_relations.relation graph_same.a graph_same.b history_backfill.oldest learned_drafts.claim
learning_signals.ref load_speed.metric load_speed.bins mail_cleanup_items.how mail_hidden.why meet_links.pick_card meet_log.what
meet_log.outcome meet_pins.fingerprint meet_seen.msg meet_sessions.keys meet_sessions.start meet_sessions.slot
meet_sessions.video meet_sessions.rejected meet_sessions.note meet_sessions.deadline meeting_preps.verdict
memory_use.purpose memory_use.how merge_effects.operation milestones.name missed_audit_items.channel missed_audit_items.area
missed_audit_items.what missed_audit_items.label missed_audits.result ms_photo_accounts.scopes ms_photo_accounts.offered
ms_photo_asks.outcome network_outbox.method network_outbox.path network_people.relation network_pins.keys note_page_links.target
note_pages.area note_pages.starts note_pages.ends note_writeups.basis notify_app_devices.platform notify_desks.desk notify_digests.channels
opportunity_items.threads
notify_queue.batch notify_queue.channel notify_queue.delivery notify_queue.ref org_aliases.alias org_aliases.target org_apart.a org_apart.b
own_addresses.sources pacing_starts.win person_facts.field person_orgs.via person_photos.type
preparations.use_events preparations.connect preparations.update_retry preparations.move_to
project_org_checks.verdict project_splits.made project_success.proof promises.area projects.outcome projects.about_sources
projects.visibility push_subscriptions.p256dh push_subscriptions.auth push_subscriptions.computer purchases.price purchases.currency
purchases.area recap_items.week recap_items.ref recaps.week record_changes.field recurring_offers.rule recurring_offers.anchor recurring_series.rule
recurring_series.anchor recurring_series.last_done recurring_series.method recurring_series.method_prev recurring_series.method_card
retention_runs.report review_misses.origin routines.rule routines.anchor routines.origin routines.old_job routines.name_check
rule_changes.ref secondhand_searches.tab secondhand_seen.item secondhand_seen.how share_threads.verdict share_threads.hand
share_threads.suggest side_changes.before side_changes.after side_changes.why skill_hints.skill skill_clusters.relation
skills.origin skills.shared store_fixes.name subs_items.next subs_kept.amount
subs_kept.currency subs_state.name subs_state.value suggestions.deliver_after suggestions.done_report suggestions.origin suggestions.evidence_versions
suggestions.merge_offer suggestions.area suggestions.completed_from suggestions.closed_from team_asks.asked
team_records.rid team_blobs.header team_blobs.ct team_blobs.sig team_files.mime team_learning_votes.ref team_learning_votes.vote team_sources.sign
team_sources.threads team_wants.body thread_snoozes.error todo_moves.reason topic_routes.conv topic_routes.area
topic_routes.events topic_routes.left voices.channel voices.ref voice_merges.channel voice_merges.merged_ref whatsapp_photos.mime
'''

# Words that stay plain, and why. docs/configuration.md ("What stays readable") says the same to the owner.
WORDS = {
    'learned: feedback, facts, rules, voices and skills stay readable, for support and to improve The Machine': '''
        decisions.feedback action_jobs.basis scheduled_sends.basis preparation_runs.basis learning_changes.target decision_annotations.reason facts.text facts.quote fact_search.text fact_search_idx.segid fact_search_idx.term
        fact_search_idx.pgno rule_changes.text voices.text voice_merges.previous voice_merges.merged_text profile_runs.draft
        skills.slug skills.name skills.description skills.body skills.author skills.their_slug skills.replaces skills.note
        skills.related skills.imported skills.task skill_clusters.name skill_clusters.description skill_clusters.body skill_clusters.target_name
        skill_clusters.related_name skill_task_decided.task skill_task_decided.name learning_state.value help_topics.topic digest_interests.topic
        team_learnings.items team_learnings.sent team_learning_votes.text team_learning_votes.example team_learning_votes.area
        team_learning_votes.reason team_learning_votes.use_cases team_learning_votes.use_case follow_up_pace.sender follow_up_sends.sender''',
    "a skill's public name and its own description, as its catalog has them": 'skill_hints.name skill_hints.summary',
    'a role someone has, learned or set by the owner': 'person_roles.role role_corrections.old_role role_corrections.new_role',
    'a short name for a kind of conversation, grouped in SQL': 'share_threads.grp',
    "the code's own fixed lines (a source's coverage, why an address is the owner's, how a promise was kept), or formatted for reading": '''
        checkpoints.state promise_log.detail own_addresses.reason own_address_fetched.entries network_pins.fingerprint''',
    'errors: the code\'s own line, or what a service answered': '''
        action_jobs.error activity_blocks.reason android_feed_health.error analyses.last_error calendar_writes.error checkpoints.error deliveries.error
        feedback_prompts.error faults.message faults.frames faults.location error_feed.message error_feed.location meeting_writes.error
        missed_audits.error network_outbox.error person_summary_runs.error preparations.error profile_runs.error project_stall_runs.error opportunity_runs.error recaps.error
        review_runs.error review_runs.last_error routine_runs.error sync_activity.error team_learnings.error team_learning_votes.error''',
    'who and where: people, organizations, addresses, sites and labels, which the database has to find a message by': '''
        activity_accounts.label agent_jobs.url ai_clients.name ai_clients.redirect_uris ai_codes.redirect_uri ai_connections.name
        ai_event_subs.url ai_event_verified.url
        board_backfill_asks.name contact_marks.identifier contact_marks.by_name contact_photo_links.identifier
        contact_photo_links.url contact_shares.name digest_items.address email_bounce_cc.address email_bounce_events.address email_bounces.address
        family_invite_log.person family_invite_log.name family_invite_offers.person family_invite_offers.name fleet_claims.holder_name fleet_in.name
        fleet_log.name fleet_out.name fleet_questions.asked fleet_requests.name fleet_reviews.name follow_up_changes.route follow_up_holds.news
        follow_up_threads.sends facebook_birthdays.data history_backfill.state fleet_splits.proposer gbrain_notes.slug gbrain_pages.slug graph_identifiers.identifier graph_imports.name graph_names.name
        graph_nodes.name graph_nodes.info graph_org_asks.identifier graph_resources.identifier graph_resources.name graph_same.why graph_role_asks.identifier graph_unnamed.people
        hidden_domains.domain hidden_domains.name identity_names.identifier identity_names.name identity_names.email
        mail_cleanup_items.address mail_cleanup_senders.address mail_hidden.identifier mail_hidden.name mail_shown.identifier
        manual_nodes.identifier manual_nodes.name meet_log.peer meet_log.name meet_log.args meet_pins.peer meet_sessions.peer
        meet_sessions.email meet_sessions.name meet_sessions.free meet_sessions.prefer ms_photo_accounts.email ms_photo_accounts.domains ms_photo_asks.identifier
        network_looked.email network_people.email network_people.username network_people.name network_people.hint network_people.reasons network_pins.name
        network_sealed.asker network_sealed.me notify_app_devices.label org_aliases.undo org_edits.domain org_edits.fields org_logo_retries.domain
        org_logo_tries.domain org_profiles.domain org_profiles.profile own_address_choices.address own_addresses.address own_domains.domain
        owner_numbers.number person_edits.identifier person_edits.fields person_facts.identifier person_orgs.identifier person_orgs.org
        person_photo_tries.identifier person_photos.identifier person_profiles.identifier person_profiles.profile person_roles.identifier
        project_org_checks.org project_org_fills.org projects.name projects.org promises.who push_subscriptions.endpoint notify_desks.endpoint
        reconnect_asks.ask record_owners.owner record_owners.name role_corrections.identifier role_corrections.name
        self_record_backups.identifier share_rules.name slack_members.label suggestions.org suggestions.done_elsewhere
        suggestions.handoff_to suggestions.awaiting promises.watch suggestions.project team_sources.name telegram_photo_asks.identifier
        voice_prefs.value whatsapp_photo_asks.identifier meeting_prep_web.query meeting_prep_web.results ai_folded.saved
        board_fit_undo.steps project_splits.steps recurring_series.project projects.stage projects.about_basis project_moves.stage crm_tags.tag
        facts.scope''',
    "the owner's own setup: boards, fields, searches and settings": '''
        boards.name boards.stages boards.about board_suggestions.name board_suggestions.stages crm_fields.name crm_fields.choices
        bring_in_state.value enrich_prefs.value error_feed_prefs.value fleet_meta.value gbrain_meta.value handoff_mail_prefs.value
        meet_prefs.value memory_seed_pages.page memory_seed_state.value milestones.detail notify_prefs.value pacing_prefs.value
        secondhand_searches.url secondhand_searches.filters security_prefs.value share_meta.value team_learning_prefs.value routines.why
        fleet_briefs.view fleet_notices.view merge_effects.receipt note_page_lines.item section_topics.section topic_aliases.target
        topic_routes.under topic_state.name routine_runs.used''',
    'a key SQL matches: what kind of to-do, item, subscription or search it is': '''
        suggestions.dedupe_key suggestion_keys.dedupe_key purchases.store purchases.store_name purchases.item reorder_mail.store
        reorder_todos.store reorder_todos.item subs_items.key subs_kept.key section_topics.key topic_aliases.key
        note_pages.key note_page_lines.key recurring_offers.key''',
    'sealed end to end on its way, matched in SQL until it is out': 'network_outbox.body team_pending.item',
}


def words(column):
    """SQL: whether the value reads as words (four or more, JSON's own spaces aside)."""
    return f"typeof({column})='text' AND replace(replace({column},'\": ','\":'),', ',',') LIKE '% % % %'"


def columns(db):
    """{table: [text columns]} of this database, indexes aside."""
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'event_search%' "
                                       "AND name NOT LIKE 'sqlite_%'").fetchall()]
    return {t: [r[1] for r in db.execute(f'PRAGMA table_info({t})').fetchall() if (r[2] or '').upper() in ('TEXT', '')] for t in tables}


def worded():
    return {name for names in WORDS.values() for name in names.split()}


def code_columns(db, sealed):
    """{table: its code columns}: named as one, or in CODES, and neither sealed nor words on purpose."""
    skip, named = set(sealed) | worded(), set(CODES.split())
    found = {t: [c for c in cs if f'{t}.{c}' not in skip and (CODE_NAME.search(f'{t}.{c}') or f'{t}.{c}' in named)] for t, cs in columns(db).items()}
    return {t: cs for t, cs in found.items() if cs}


def sealed_names():
    import message_seal
    return ({f'{t}.{c}' for t, cs in message_seal.DERIVED.items() for c in cs} | {f'{t}.{c}' for t, c, _ in message_seal.DERIVED_JSON}
            | {'events.title', 'events.body', 'events.metadata'})


def guard(db):
    """A write of words to a code column fails from here on, whatever code writes it."""
    for table, names in code_columns(db, sealed_names()).items():
        for when, of in (('INSERT', ''), ('UPDATE', ' OF ' + ','.join(f'"{c}"' for c in names))):
            name = f'plain_{table}_{when.lower()}'
            if db.execute('SELECT 1 FROM sqlite_master WHERE name=?', (name,)).fetchone():
                continue
            said = ' '.join(f"WHEN {words(f'new.{chr(34)}{c}{chr(34)}')} THEN '{table}.{c}'" for c in names)
            db.execute(f"CREATE TRIGGER {name} BEFORE {when}{of} ON {table} WHEN CASE {said} END IS NOT NULL BEGIN "
                       f"SELECT RAISE(ABORT,'a plain column of {table} holds words: seal it (message_seal.DERIVED) or say why not (plain_columns)'); END")


def install():
    """Every database a Store opens in this process is guarded, tables made later too (as the sealed guards are)."""
    import contextlib
    from machine.store import core
    plain, seen = core.StoreCore._connect, {}

    @contextlib.contextmanager
    def connect(self, *args, **kwargs):
        with plain(self, *args, **kwargs) as db:
            version = db.execute('PRAGMA schema_version').fetchone()[0]
            if seen.get(str(self.path)) != version and not db.in_transaction:
                guard(db)
                seen[str(self.path)] = db.execute('PRAGMA schema_version').fetchone()[0]
            yield db
    core.StoreCore._connect = connect


if __name__ == '__main__':
    import unittest
    install()
    unittest.main(module=None)
