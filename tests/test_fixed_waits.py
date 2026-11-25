"""A guard on the browser tests' fixed waits (page.waitForTimeout): a test that sleeps a fixed time and then looks
fails when CI runs slower than that, and waits for nothing when it runs faster. A test waits for what it expects
instead: the call the page makes (tests/page-calls.mjs waitForAction, callAfter), what the page shows (a locator's
waitFor, page.waitForFunction, settled), or the page settling before a measurement (quiet).

The files that have fixed waits today are in WAITS, with their count, which only comes down: when a wait goes, lower
its count (`python3 tests/test_fixed_waits.py --counts` prints them). A new file has none. A wait that only steadies
a screenshot belongs in the test's shot helper, behind the variable that asks for pictures. A check that something does
not happen (no tooltip, no post, it stays) needs a time: it keeps its wait, longer than what it waits out.

And a guard on code in a trailing // comment of a .mjs test (SwallowedCode). Many lines hold several statements, and a
comment put in the middle of one takes the rest of the line with it: assertions stood in a comment and nothing said so.
Something like a statement there (an assertion, await, const, an arrow, a semicolon at its end) fails: the code goes on a
line of its own. It is here since this file already runs on every change (scripts/test_select.py ALWAYS)."""
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {'node_modules', '.git', '.venv', '__pycache__'}
FIXED_WAIT = re.compile(r'\bwaitForTimeout\s*\(')
COMMENT = re.compile(r'(?<![:\'"`/\\])//(?!/)(.*)$')  # not a URL's, nor one that opens a string
CODE = re.compile(r'assert\w*[.(]|await |;\s*$|\bconst |=>|\)\);')

# The fixed waits each test file has today: these only come down.
WAITS = {
    'tests/click-speed.mjs': 4,
    'tests/test_account_dashboard.mjs': 1,
    'tests/test_agent_jobs_dashboard.mjs': 1,
    'tests/test_alias_send_dashboard.mjs': 1,
    'tests/test_app_link_launch_dashboard.mjs': 5,
    'tests/test_area_digest_dashboard.mjs': 1,
    'tests/test_ask_questions_dashboard.mjs': 1,
    'tests/test_back_closes_dialogs_dashboard.mjs': 2,
    'tests/test_bring_in_dashboard.mjs': 1,
    'tests/test_browser_guard.mjs': 1,
    'tests/test_browser_pane_fit_dashboard.mjs': 8,
    'tests/test_browser_stop_dashboard.mjs': 3,
    'tests/test_calendar_dashboard.mjs': 4,
    'tests/test_calendar_grid_dashboard.mjs': 2,
    'tests/test_calendar_notes_dashboard.mjs': 1,
    'tests/test_calendar_scroll_dashboard.mjs': 5,
    'tests/test_calendar_starts_dashboard.mjs': 2,
    'tests/test_calendar_write_dashboard.mjs': 5,
    'tests/test_card_button_labels_dashboard.mjs': 1,
    'tests/test_card_buttons_dashboard.mjs': 1,
    'tests/test_card_chat_dashboard.mjs': 9,
    'tests/test_card_row_phone_dashboard.mjs': 1,
    'tests/test_card_short_dashboard.mjs': 1,
    'tests/test_change_how_dashboard.mjs': 2,
    'tests/test_chat_composer_dashboard.mjs': 8,
    'tests/test_chat_fast_dashboard.mjs': 2,
    'tests/test_chat_finish_dashboard.mjs': 2,
    'tests/test_chat_fixed_notice_dashboard.mjs': 1,
    'tests/test_chat_keys_dashboard.mjs': 4,
    'tests/test_chat_menu_states_dashboard.mjs': 1,
    'tests/test_chat_peek_dashboard.mjs': 1,
    'tests/test_chat_read_backoff_dashboard.mjs': 1,
    'tests/test_chat_send_at_once_dashboard.mjs': 4,
    'tests/test_chat_stays_open_dashboard.mjs': 2,
    'tests/test_chat_stop_files_dashboard.mjs': 1,
    'tests/test_chat_thread_dashboard.mjs': 1,
    'tests/test_clamp_fit_dashboard.mjs': 7,
    'tests/test_clamp_tap_dashboard.mjs': 3,
    'tests/test_clear_ready_dashboard.mjs': 2,
    'tests/test_client_errors_dashboard.mjs': 1,
    'tests/test_compose_email_dashboard.mjs': 3,
    'tests/test_connect_add_scroll_dashboard.mjs': 3,
    'tests/test_connect_hosted_return_dashboard.mjs': 1,
    'tests/test_connect_restart_window_dashboard.mjs': 2,
    'tests/test_connect_whatsapp_linking_dashboard.mjs': 1,
    'tests/test_connection_kinds_dashboard.mjs': 1,
    'tests/test_connections_history_dashboard.mjs': 1,
    'tests/test_connections_machine_health_dashboard.mjs': 1,
    'tests/test_connections_row_calendar_dashboard.mjs': 1,
    'tests/test_decide_toast_dashboard.mjs': 1,
    'tests/test_desktop_layout_dashboard.mjs': 1,
    'tests/test_digest_card_link_dashboard.mjs': 1,
    'tests/test_disconnected_dashboard.mjs': 1,
    'tests/test_doc_reply_dashboard.mjs': 3,
    'tests/test_doc_write_dashboard.mjs': 1,
    'tests/test_docs_signin_dashboard.mjs': 2,
    'tests/test_drawer_scroll_dashboard.mjs': 2,
    'tests/test_email_frame_layout_dashboard.mjs': 1,
    'tests/test_email_links_dashboard.mjs': 2,
    'tests/test_error_reports_dashboard.mjs': 3,
    'tests/test_family_invites_dashboard.mjs': 5,
    'tests/test_finish_merge_dashboard.mjs': 1,
    'tests/test_first_card_stream_dashboard.mjs': 2,
    'tests/test_first_look_live_dashboard.mjs': 1,
    'tests/test_first_look_no_flip_dashboard.mjs': 3,
    'tests/test_first_look_reading_dashboard.mjs': 2,
    'tests/test_first_look_steady_dashboard.mjs': 2,
    'tests/test_first_look_stops_dashboard.mjs': 1,
    'tests/test_first_paint_reads_dashboard.mjs': 1,
    'tests/test_fleet_ask_dashboard.mjs': 2,
    'tests/test_fleet_brief_dashboard.mjs': 2,
    'tests/test_fleet_calm_dashboard.mjs': 3,
    'tests/test_fleet_card_todo_dashboard.mjs': 2,
    'tests/test_fleet_handoff_dashboard.mjs': 1,
    'tests/test_fleet_handoff_decline_dashboard.mjs': 2,
    'tests/test_fleet_learnings_dashboard.mjs': 1,
    'tests/test_fleet_refresh_dashboard.mjs': 4,
    'tests/test_fleet_requests_dashboard.mjs': 1,
    'tests/test_fleet_review_dashboard.mjs': 3,
    'tests/test_fleet_stamp_dashboard.mjs': 2,
    'tests/test_follow_ups_dashboard.mjs': 2,
    'tests/test_friends_dashboard.mjs': 4,
    'tests/test_github_step_dashboard.mjs': 1,
    'tests/test_graph_counts_status_dashboard.mjs': 2,
    'tests/test_graph_dashboard.mjs': 3,
    'tests/test_graph_detail_dashboard.mjs': 1,
    'tests/test_graph_fleet_dashboard.mjs': 8,
    'tests/test_graph_load_error_dashboard.mjs': 2,
    'tests/test_graph_parts_dashboard.mjs': 1,
    'tests/test_graph_phone_overflow_dashboard.mjs': 1,
    'tests/test_greeting_dashboard.mjs': 1,
    'tests/test_handoff_chat_dashboard.mjs': 1,
    'tests/test_handoff_mail_dashboard.mjs': 1,
    'tests/test_handoff_sheet_fit_dashboard.mjs': 1,
    'tests/test_handoff_silent_dashboard.mjs': 1,
    'tests/test_help_dashboard.mjs': 1,
    'tests/test_i18n_dashboard.mjs': 1,
    'tests/test_inline_edit_dashboard.mjs': 1,
    'tests/test_instant_decide_dashboard.mjs': 2,
    'tests/test_instant_graph_dashboard.mjs': 6,
    'tests/test_intercom_reply_dashboard.mjs': 1,
    'tests/test_keyboard_walk_dashboard.mjs': 1,
    'tests/test_learned_chat_dashboard.mjs': 1,
    'tests/test_learned_dashboard.mjs': 1,
    'tests/test_long_lists_dashboard.mjs': 4,
    'tests/test_machine_clipboard.mjs': 4,
    'tests/test_machine_view.mjs': 4,
    'tests/test_machine_view_resize.mjs': 2,
    'tests/test_mail_cleanup_dashboard.mjs': 2,
    'tests/test_meeting_fields_dashboard.mjs': 5,
    'tests/test_meeting_open_dashboard.mjs': 2,
    'tests/test_meeting_prep_dashboard.mjs': 1,
    'tests/test_message_context_dashboard.mjs': 3,
    'tests/test_message_view_dashboard.mjs': 1,
    'tests/test_milestone_dashboard.mjs': 2,
    'tests/test_needs_you_place_dashboard.mjs': 5,
    'tests/test_new_card_dashboard.mjs': 2,
    'tests/test_new_card_files_dashboard.mjs': 1,
    'tests/test_notify_dashboard.mjs': 1,
    'tests/test_offline_dashboard.mjs': 3,
    'tests/test_offline_resume_dashboard.mjs': 2,
    'tests/test_omarchy_dashboard.mjs': 6,
    'tests/test_open_between_link_dashboard.mjs': 3,
    'tests/test_org_page_dashboard.mjs': 3,
    'tests/test_outcomes_dashboard.mjs': 1,
    'tests/test_peek_connect_dashboard.mjs': 2,
    'tests/test_peek_steady_dashboard.mjs': 2,
    'tests/test_person_page_dashboard.mjs': 1,
    'tests/test_person_wrap_dashboard.mjs': 2,
    'tests/test_phone_dialogs_dashboard.mjs': 4,
    'tests/test_place_hold_dashboard.mjs': 7,
    'tests/test_preparing_in_place_dashboard.mjs': 1,
    'tests/test_project_picker_fit_dashboard.mjs': 1,
    'tests/test_promise_page_dashboard.mjs': 2,
    'tests/test_push_links_dashboard.mjs': 1,
    'tests/test_quality_wait_dashboard.mjs': 1,
    'tests/test_quick_buttons_dashboard.mjs': 1,
    'tests/test_reading_digest_dashboard.mjs': 1,
    'tests/test_reconnect_todo_dashboard.mjs': 1,
    'tests/test_review_live_dashboard.mjs': 2,
    'tests/test_roles_dashboard.mjs': 10,
    'tests/test_routines_dashboard.mjs': 4,
    'tests/test_routines_earlier_open_dashboard.mjs': 6,
    'tests/test_routines_poll_dashboard.mjs': 3,
    'tests/test_routines_scroll.mjs': 1,
    'tests/test_salesflare_card_dashboard.mjs': 1,
    'tests/test_search_ask_dashboard.mjs': 2,
    'tests/test_send_all_dashboard.mjs': 4,
    'tests/test_settings_fleet_polish_dashboard.mjs': 2,
    'tests/test_settings_upkeep.mjs': 3,
    'tests/test_settings_views_dashboard.mjs': 4,
    'tests/test_setup_card_dashboard.mjs': 4,
    'tests/test_setup_mail_first_dashboard.mjs': 3,
    'tests/test_setup_quiet_dashboard.mjs': 1,
    'tests/test_setup_restart_dashboard.mjs': 2,
    'tests/test_share_all_dashboard.mjs': 1,
    'tests/test_share_new_todo_dashboard.mjs': 4,
    'tests/test_shared_connectors_dashboard.mjs': 1,
    'tests/test_shared_stripe_dashboard.mjs': 1,
    'tests/test_shell_details_dashboard.mjs': 1,
    'tests/test_sidebar_pages_dashboard.mjs': 5,
    'tests/test_sidebar_row_menu.mjs': 4,
    'tests/test_signature_paste_live_dashboard.mjs': 3,
    'tests/test_signature_paste_save_dashboard.mjs': 7,
    'tests/test_signatures_dashboard.mjs': 2,
    'tests/test_signin_approve_dashboard.mjs': 1,
    'tests/test_signin_resume_dashboard.mjs': 1,
    'tests/test_skills_catalog_dashboard.mjs': 1,
    'tests/test_slow_not_offline_dashboard.mjs': 1,
    'tests/test_snooze_reminder_dashboard.mjs': 1,
    'tests/test_source_line_marks_dashboard.mjs': 1,
    'tests/test_stale_note_dashboard.mjs': 1,
    'tests/test_startup_cache_dashboard.mjs': 3,
    'tests/test_tab_links_dashboard.mjs': 1,
    'tests/test_talk_actions_dashboard.mjs': 6,
    'tests/test_talk_hearing_dashboard.mjs': 7,
    'tests/test_talk_live_dashboard.mjs': 17,
    'tests/test_talk_main_dashboard.mjs': 28,
    'tests/test_telegram_links_dashboard.mjs': 1,
    'tests/test_toast_lift_dashboard.mjs': 3,
    'tests/test_toast_swipe_dashboard.mjs': 7,
    'tests/test_todo_connect_dashboard.mjs': 2,
    'tests/test_todo_move_area_dashboard.mjs': 1,
    'tests/test_todo_stuck_details_dashboard.mjs': 1,
    'tests/test_todo_use_sources_dashboard.mjs': 1,
    'tests/test_touch_hover_dashboard.mjs': 3,
    'tests/test_ux_dashboard.mjs': 6,
    'tests/test_voice_input_dashboard.mjs': 20,
    'tests/test_voice_saved_dashboard.mjs': 1,
    'tests/test_whats_new_dashboard.mjs': 4,
    'tests/test_work_label_dashboard.mjs': 1,
}


def fixed_waits():
    """{file: count} for every browser test script (tests/**/*.mjs, *.js) with a fixed wait."""
    out = {}
    for path in sorted((ROOT / 'tests').rglob('*')):
        if path.suffix not in ('.mjs', '.js') or SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        found = len(FIXED_WAIT.findall(path.read_text(encoding='utf-8', errors='replace')))
        if found:
            out[path.relative_to(ROOT).as_posix()] = found
    return out


def swallowed(text):
    """[(line number, the comment)] for each line with code before a // comment and something like code in it."""
    out = []
    for n, line in enumerate(text.split('\n'), 1):
        m = COMMENT.search(line)
        if m and line[:m.start()].strip() and CODE.search(m[1]):
            out.append((n, m[0]))
    return out


class FixedWaits(unittest.TestCase):
    def test_fixed_waits_only_come_down(self):
        found = fixed_waits()
        for name in sorted(set(found) | set(WAITS)):
            with self.subTest(name):
                have, allowed = found.get(name, 0), WAITS.get(name, 0)
                self.assertLessEqual(have, allowed, f'{name} has {have} fixed waits ({allowed} allowed): wait for the '
                                     'call (waitForAction) or what the page shows (waitFor, waitForFunction) instead')
                self.assertGreaterEqual(have, allowed, f'{name} has {have} fixed waits now: lower its count in WAITS '
                                        'to that')

    def test_the_guard_counts_fixed_waits(self):
        self.assertEqual(len(FIXED_WAIT.findall("await page.waitForTimeout(100);await p.waitForTimeout (5);")), 2)
        self.assertEqual(FIXED_WAIT.findall("page.waitForFunction(()=>ok);page.waitForTimeoutish"), [])


class SwallowedCode(unittest.TestCase):
    def test_no_code_in_a_trailing_comment(self):
        checked = [p for p in sorted((ROOT / 'tests').rglob('*.mjs')) if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]
        self.assertGreater(len(checked), 200, 'the .mjs files in tests/')
        found = [f'{p.relative_to(ROOT).as_posix()}:{n}: {comment}' for p in checked
                 for n, comment in swallowed(p.read_text(encoding='utf-8'))]
        self.assertEqual(found, [], 'code in a trailing // comment never runs: put it on a line of its own')

    def test_the_guard_finds_the_lines_it_is_for(self):
        for line in (  # the three it found, as they were
            "  await page.locator('body').press('c');await page.waitForTimeout(200);  // a check that nothing opensassert.ok(!(await dialog.isVisible()),'C is not New to-do any more');",
            "  assert.match(await page.locator('.proj-facts').textContent(),/Value €12,000/);assert.equal(await page.locator('.proj-org').textContent(),'paperkite.example');  // the logo's initial isn't part of the textassert.match(await page.locator('.proj-facts').textContent(),/Wants SSO/);",
            "  const more=async c=>(await c.locator('.more-menu button:not([data-mm-back])').evaluateAll(n=>n.map(x=>x.dataset.full||x.textContent)))  // Hand off…'s sheet names a teammate's choice A teammate; its whole name is data-full.map(x=>x.trim());",
        ):
            self.assertEqual(len(swallowed(line)), 1, line)
        for line in ("assert.equal(a,1);  // the one kept", "// assert.equal(a,1);", "await page.goto('http://127.0.0.1:80/');await ready(page);",
                     "const url='//cdn.example/x.js';"):
            self.assertEqual(swallowed(line), [], line)


if __name__ == '__main__':
    if '--counts' in sys.argv:
        for name, count in fixed_waits().items():
            print(f'    {name!r}: {count},')
    else:
        unittest.main()
