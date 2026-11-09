"""Reviewing new signals in the service (refactor PR 23b): the review step that starts a review run, checks it and
saves what it found, its queue, tick and worker, the live view while it runs and the preview on a new install, with
their timing constants and step names. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import collections
import datetime as dt
import json
import re
import sqlite3
import threading
import time
import uuid
from pathlib import Path

import embeddings
import enrichment
import error_feed
import fleet
import fleet_reviews
import graph
import i18n
from machine.app.first_look import (
    FIRST_DIG_HOURS,
    first_look_batch,
    FIRST_LOOK_NEXT_SIGNALS,
    FIRST_LOOK_SETTLE_SECONDS,
    QUICK_LOOK_HOURS,
    QUICK_LOOK_SIGNALS,
    review_max_wait,
    SYSTEM_SERVICES,
)
from machine.app.graph_actions import account_services
from machine.app.preparation import PROMPT_LIMIT
from machine.browser import STEP_NAMES, transcript_tool_calls
from machine.config import LOG, RULE_FILES
from machine.prompts.profile import VOICE_TEXT
from machine.prompts.review import FACT_KIND_HINT, review_prompt, source_notes
from machine.sources.connectors import companies_prompt
from machine.store import review_backoff, review_wait
from machine.store.cards import active_preview
from machine.store.events import RUN_SIGNAL_BUDGET, SET_ASIDE_AFTER
from machine.store.facts import suggestion_scope
from machine.store.first_look import FIRST_ACTIONS, first_value
from machine.store.review import (PREVIEW_DAYS, REVIEW_PAGE_CHARS, REVIEW_SESSION_PREFIX, REVIEW_TERMINAL, review_view,
                                  service_review_ended)
from machine.text import clamp, encoded
import next_actions
import shared_graph
from timeutil import now


# The review worker looks at its run every REVIEW_TICK_SECONDS, and every FIRST_LOOK_TICK_SECONDS while the first look
# runs or digs, starting its next batch as soon as one ended: a turn's end was noticed 8 to 39 s late and the next
# batch started 15 s after that, about a minute idle per batch while the owner watched (2026-11-04)
REVIEW_TICK_SECONDS, FIRST_LOOK_TICK_SECONDS = 15, 4


REVIEW_PROBE_SECONDS = 120  # the same for a review: old enough to be past the Gateway's queue


FIRST_LOOK_SIGNAL_SECONDS = 12  # about how long a first look takes per signal, for "first cards in about N min"


def first_eta_minutes(run=None, look=None, queue=None, current=None):
    """About how many minutes until the first to-dos, for the setup page (first_cards_report) and the empty state
    (App.review_live), so both say the same. run {planned, done}: a first review running now. look: the first look's
    state (App.first_look). queue (App.review_queue): the first regular review. None when nothing is on its way.
    A running review's time counts down from its start (run started_at): its done count only moves when a batch saves,
    so without it the quick look said "about 4 min" all through its one batch (2026-11-09)"""
    current = current or dt.datetime.fromisoformat(now())
    if run:
        left = max((run.get('planned') or 0) - (run.get('done') or 0), 1) * FIRST_LOOK_SIGNAL_SECONDS
        try:
            left -= max(0, int((current - dt.datetime.fromisoformat(run['started_at'])).total_seconds())) if run.get('started_at') else 0
        except (TypeError, ValueError):
            pass
        return max(1, -(-left // 60))
    if look:
        if not (look.get('state') == 'due' or look.get('why') in ('mail', 'settling', 'retry')):
            return None
        eta = 1 + -(-(look.get('waiting') or QUICK_LOOK_SIGNALS) * FIRST_LOOK_SIGNAL_SECONDS // 60)
        if look.get('why') == 'settling':
            eta += FIRST_LOOK_SETTLE_SECONDS // 60
        if look.get('retry_at'):
            eta += max(0, int((dt.datetime.fromisoformat(look['retry_at']) - current).total_seconds() // 60))
        return eta
    if queue and queue.get('first') and queue.get('planned'):
        try:
            wait = max(0, int((dt.datetime.fromisoformat(queue['starts_at']) - current).total_seconds())) if queue.get('starts_at') else 0
        except (TypeError, ValueError):
            wait = 0
        return max(1, -(-(wait + queue['planned'] * FIRST_LOOK_SIGNAL_SECONDS) // 60))
    return None


REVIEW_ASKED_SECONDS = 600  # the owner's Review now holds this long for the next review step


# What a review's own tool calls say it is doing, in the owner's words. Only names and card titles (what a card already
# shows) come from the call itself; never message text or search words.
REVIEW_STEPS = {'begin_analysis': 'Taking the next signals to check', 'analysis_page': 'Reading the signals',
                'events': 'Looking through earlier messages', 'finish_analysis': 'Saving what it found',
                'promise': 'Noting a promise', 'promise_close': 'Closing a promise that was kept',
                'remember_fact': 'Remembering something about you', 'status': 'Checking open to-dos',
                'preferences': 'Checking what you liked before', 'feedback': 'Checking what you liked before'}


def review_step_title(name, arguments, names=None):
    if name != 'assistant_signals':
        return STEP_NAMES.get(name, 'Working')
    action = arguments.get('action') if isinstance(arguments.get('action'), str) else ''
    args = arguments.get('args') if isinstance(arguments.get('args'), dict) else {}
    if action == 'suggest' and isinstance(args.get('title'), str) and args['title'].strip():
        return 'Suggesting: ' + clamp(' '.join(args['title'].replace('**', '').split()), 90)
    if action == 'graph':
        node = (names or {}).get(str(args.get('node_id') or ''))
        return 'Looking up ' + clamp(node, 60) if node else 'Checking who is who'
    if action == 'analysis_page' and isinstance(args.get('page'), int):
        return f"Reading the signals, part {args['page'] + 1}"
    return REVIEW_STEPS.get(action, 'Working')


def review_steps(db, run, agent_db=None, limit=8):
    """The latest steps of a running review, newest first: what it took to review (how many, from which
    accounts), its own tool calls, and how many cards it made so far."""
    steps = []
    labels = {}
    for claim in db.execute('SELECT started_at,items FROM analyses WHERE owner_run=? AND owner_session=?',
                            (run['run_id'], REVIEW_SESSION_PREFIX + run['run_id'])):
        ids = [i['id'] for i in json.loads(claim['items'])]
        kinds = collections.Counter()
        for n in range(0, len(ids), 500):
            chunk = ids[n:n + 500]
            kinds.update(r[0] for r in db.execute(f"SELECT kind FROM events WHERE id IN ({','.join('?' * len(chunk))})", chunk))
        what = ', '.join(f'{count} {KIND_WORDS.get(kind, ("signal", "signals"))[count != 1]}' for kind, count in kinds.most_common(3))
        if what:
            steps.append({'at': claim['started_at'], 'title': 'Reading ' + what})
    calls = transcript_tool_calls(REVIEW_SESSION_PREFIX + run['run_id'], agent_db, limit=limit, scan=120)
    wanted = [str((c[2].get('args') or {}).get('node_id')) for c in calls if isinstance(c[2].get('args'), dict) and (c[2]['args'].get('node_id'))]
    if wanted:
        labels = {r['id']: r['name'] for r in db.execute(f"SELECT id,name FROM graph_nodes WHERE id IN ({','.join('?' * len(wanted))})", wanted)}
    steps += [{'at': at, 'title': review_step_title(name, arguments, labels)} for at, name, arguments in calls]
    steps.sort(key=lambda x: x['at'], reverse=True)
    cards = db.execute('SELECT count(*) FROM suggestions WHERE created_at>=?', (run['started_at'],)).fetchone()[0]
    if cards:
        steps.insert(0, {'at': now(), 'title': f"{cards} suggestion{'s' if cards != 1 else ''} so far", 'count': True})
    return steps[:limit]


KIND_WORDS = {'gmail.message': ('email', 'emails'), 'calendar.event': ('meeting', 'meetings'), 'slack.message': ('Slack message', 'Slack messages'), 'teams.message': ('Teams message', 'Teams messages'),
              'whatsapp.message': ('WhatsApp message', 'WhatsApp messages'), 'telegram.message': ('Telegram message', 'Telegram messages'), 'linkedin.message': ('LinkedIn message', 'LinkedIn messages'),
              'android.notification': ('phone notification', 'phone notifications'), 'x.message': ('X message', 'X messages')}


REVIEW_FAILURES = {'runtime_error','runtime_timeout','runtime_aborted','runtime_lost',
                   'model_idle_timeout','bridge_error','rate_limited','usage_limited','connection_error','prompt_too_long'}


REVIEW_FAILURE_PHASES = {'runtime','model','bridge','connection','queue','provider','tool','gateway_draining'}


# Why a generic runtime_error happened, from a fixed list (REASONS in preparation-run.mjs): logged, never the raw text.
REVIEW_REASONS = {'mcp_runtime_limit','context_overflow','model_unavailable','auth_failed','auth_missing','unclassified'}


# A hosting layer's note while the owner signs in to an AI (a hosted Machine's ChatGPT or Claude sign-in): the dashboard
# says "Connecting ChatGPT…" instead of "Pick your AI" meanwhile. A sign-in gives up after 15 minutes; once it is
# done, the model takes a minute more to be set and reviews to turn on, so the note holds for a while after it too.
AI_CONNECTING_MINUTES = 16


AI_CONNECTED_MINUTES = 5


AI_CONNECTING_NAME = re.compile(r'[A-Za-z][A-Za-z0-9 .-]{0,29}')


def ai_connecting(config, current=None):
    """The AI the owner is signing in to right now, from the `needs_you_file` note with `ai_connecting` (no text: a
    release from before shows nothing for it): {'name', 'since'}, or None when no sign-in is going on, it stopped (the
    hosting layer takes the note away when it fails) or the note is older than a sign-in can take."""
    path = config.get('needs_you_file')
    if not path:
        return None
    try:
        notes = json.loads(Path(path).expanduser().read_text())
    except (OSError, ValueError):
        return None
    current = current or dt.datetime.now(dt.timezone.utc)
    for note in notes if isinstance(notes, list) else []:
        if not isinstance(note, dict) or not isinstance(note.get('ai_connecting'), str) or not AI_CONNECTING_NAME.fullmatch(note['ai_connecting']):
            continue
        try:
            since = dt.datetime.fromisoformat(str(note.get('since')))
            done = dt.datetime.fromisoformat(str(note['done'])) if note.get('done') else None
        except ValueError:
            continue
        if since.tzinfo is None or (done and done.tzinfo is None):
            continue
        if (done and current - done > dt.timedelta(minutes=AI_CONNECTED_MINUTES)) or current - since > dt.timedelta(minutes=AI_CONNECTING_MINUTES):
            continue
        return {'name': note['ai_connecting'], 'since': since.isoformat()}
    return None


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
        eta = first_eta_minutes({'planned': active[6] or 0, 'done': done, 'started_at': active[2]}, None, None, current)
    elif state:
        out['look'] = {k: state.get(k) for k in ('state', 'why', 'quick', 'waiting', 'retry_at')}
        eta = first_eta_minutes(None, state, None, current)
    if eta and not out['cards']:
        out['eta_minutes'] = eta
    return out


class ReviewApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {**dict.fromkeys(('events', 'related', 'begin_analysis'), 'events_action'), 'preview_review': 'preview_review_action', 'review_now': 'review_now_action',
               'review_context': 'review_context_action', 'review_failed': 'review_failed_action',
               'analysis_page': 'analysis_page_action', 'finish_analysis': 'finish_analysis_action',
               'enrich': 'enrich_action', 'looks_handled': 'looks_handled_action',
               'handoff_on_it': 'handoff_on_it_action', 'split_from_notes': 'split_from_notes_action'}

    def review_subject(self, card_id):
        """What Ask to review shows of an open to-do (fleet_reviews.py): its ready draft (to, subject, text, revision) when
        it has one, else its result or plan (the to-do's text); and whether it is Work or Personal."""
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (str(card_id),)).fetchone()
        if not row:
            raise ValueError('No such to-do')
        if row['status'] not in fleet.OPEN_CARD or str(row['dedupe_key']).startswith('fleet-review:'):
            raise ValueError(i18n.t('This to-do can’t be reviewed'))
        scope = suggestion_scope(row['account_ids'], self.config.get('accounts', []), row['area'])
        found = {'scope': scope, 'title': row['title'], 'what': 'result', 'body': fleet_reviews._text(row['body'], fleet_reviews.BODY, True)}
        try:
            value = json.loads(row['next_action'] or 'null')
        except ValueError:
            value = None
        actions = value.get('actions') if isinstance(value, dict) and value.get('kind') == 'menu' else [value]
        draft = next((a for a in actions or [] if isinstance(a, dict) and a.get('kind') in fleet_reviews.DRAFT_KINDS and a.get('revision')), None)
        if row['status'] == 'prepared' and draft:
            to = draft.get('to') if isinstance(draft.get('to'), list) else [draft.get('to_name') or draft.get('to_email') or '']
            found.update(what='draft', body=fleet_reviews._text(next_actions.draft_text(draft), fleet_reviews.BODY, True),
                         subject=' '.join(str(draft.get('subject') or '').split()), to=', '.join(str(x) for x in to if x),
                         revision=draft['revision'])
        return found

    def review_write(self, card_id, what, subject, body, revision):
        """Changes the owner accepted from a review: into their draft (revise_draft, a new revision they read before Send)
        or into the to-do's text. Nothing is sent."""
        if what == 'draft':
            return self.store.revise_draft(str(card_id), revision, 'fleet-review', subject=subject, body=body)
        return self.store.review_body(str(card_id), body)

    def review_step(self, runner=None):
        """Start one isolated review turn when a batch of reviewable signals waits, independent of the
        heartbeat and the main chat session. One run at a time, with a gap between runs."""
        settings = self.config.get('review_worker') or {}
        enabled = settings.get('enabled')
        if enabled:  # reviews just turned on: the first look's cards that want a draft get one
            self.store.prepare_first_look(int(self.config.get('prepare_ahead_per_day', 10)) if self.config.get('prepare_ahead', True) is not False else 0)
            # The reviews take over from the first look: its last state from before ("due") would stay in the health
            # report for good, with "first to-dos in about N min" that never come (first_cards_report)
            with self.store.connect() as db:
                self.store.note_first_look(db, None)
        if not enabled:
            # Reviews off: only a preview runs (and is monitored) here: the owner's, or the first look
            # The Machine starts by itself once a model and a source are there.
            with self.store.connect() as db:
                running = active_preview(db)
                look = None if running else self.first_look(db)
                due = (look or {}).get('state') == 'due'
                if not running:
                    self.store.note_first_look(db, look)
            # One usage check before every background turn (model_budget); the quick look, the first magic, may go further
            due = due and not self.background_pause(first=True, job='first_look')  # the whole first look: the first magic
            if not running and not due:
                return None
            if due:
                try:
                    self.start_preview(auto=True, quick=bool(look.get('quick')))
                except ValueError:  # nothing from the last week after all, or another review just started
                    return None
        runner = runner or self.preparation_gateway
        stamp = dt.datetime.fromisoformat(now())
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT * FROM review_runs WHERE status IN ('starting','running','recovering') ORDER BY started_at LIMIT 1").fetchone()
            if run:
                run = dict(run)
                if not enabled and not run['preview']:
                    return None
                if run['retry_at'] and run['retry_at'] > now():
                    return None
                if run['status'] == 'starting' and run['updated_at'] > (stamp - dt.timedelta(minutes=1)).isoformat() and run['attempts']:
                    return None  # wait a minute before retrying an unconfirmed admission
            elif not enabled:
                return None
            else:
                active = db.execute("SELECT * FROM analyses WHERE status IN ('running','retryable') ORDER BY started_at LIMIT 1").fetchone()
                recovery = active and service_review_ended(db, active)
                last = db.execute('SELECT status,finished_at,window_hours FROM review_runs WHERE finished_at IS NOT NULL ORDER BY finished_at DESC LIMIT 1').fetchone()
                # After failed runs, back off: 1, 2, 4… minutes up to 30, so a persistent
                # model or account failure can't start a new review every minute.
                failed = 0
                for (status,) in db.execute('SELECT status FROM review_runs WHERE finished_at IS NOT NULL ORDER BY finished_at DESC LIMIT 6'):
                    if status == 'ok':
                        break
                    failed += 1
                retry = min(settings.get('retry_seconds', 60) * 2 ** max(failed - 1, 0), settings.get('max_retry_seconds', 1800))
                # The first review digs on (first_dig): its next batch right away, after a failure within the backoff above
                dig = None if recovery else self.first_dig(db, stamp)
                dig = dig if dig and 'left' in dig else None
                # Projects the owner just put on a board are sorted within minutes, with or without new signals
                sort_due = bool(graph.unsorted_projects(db, 1)) or graph.fit_due(db, now())
                # A new board looks through the history in rounds a few minutes apart, while the model's limits have room
                backfill_due = not sort_due and self.model_room() and not self.history_paced() and graph.backfill_due(db, now())
                asked = getattr(self, 'review_asked', 0) > time.time() - REVIEW_ASKED_SECONDS  # the owner's Review now
                gap = retry if recovery or failed else settings.get('sort_gap_seconds', 60) if sort_due else \
                    settings.get('backfill_gap_seconds', 180) if backfill_due else settings.get('gap_seconds', 600)
                sort_due = sort_due or backfill_due
                if last and last['status'] == 'ok' and last['window_hours'] and not recovery:
                    gap = min(gap, 60)  # after the quick first review, the rest follows right away
                if dig and not failed:
                    gap = 0
                # ok runs that never claimed a batch back off the same way (machine/store/review_backoff.py)
                gap = review_backoff.empty_gap(review_backoff.empty_in_a_row(db), gap, settings)
                if last and (stamp - dt.datetime.fromisoformat(last['finished_at'])).total_seconds() < gap and not asked:
                    return None
                # Leave a review claimed elsewhere (a manual run) alone until it ends or expires.
                if not recovery and db.execute("SELECT 1 FROM analyses WHERE status IN ('running','retryable') AND coalesce(resumed_at,started_at)>?",
                              ((stamp - dt.timedelta(hours=1)).isoformat(),)).fetchone():
                    return None
                # Reviews just turned on and nothing reviewed yet: first a quick look at the newest mail, at once (no
                # waiting for a batch or for the rest of the import); the regular reviews take the rest after it.
                quick = 0 if recovery else self.quick_first_review(db)
                # One usage check before every background turn (model_budget). New signals are not paced per day, only
                # at the week's WEEK_CAP and the 5-hour window; the owner's Review now goes like their own chat.
                self.review_paused = self.background_pause(first=bool(quick or dig), owner=asked, job='review', db=db, signals=True)
                if self.review_paused:
                    return None
                if quick:
                    run = {'run_id': uuid.uuid4().hex, 'status': 'starting', 'started_at': now(), 'attempts': 0}
                    db.execute('INSERT INTO review_runs(run_id,status,started_at,updated_at,planned,auto,window_hours,budget) VALUES(?,?,?,?,?,1,?,?)',
                               (run['run_id'], 'starting', run['started_at'], run['started_at'], quick, QUICK_LOOK_HOURS, QUICK_LOOK_SIGNALS))
                    self.note_dig_start(db)
                else:
                    # Each run has a fixed cost (instructions, status, context), so wait for a batch: enough signals, or
                    # the oldest one from a person has waited long enough; newsletters, notifications and receipts wait
                    # longer (machine/store/review_wait.py) and join the next review
                    waiting = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<?',
                                         (SET_ASIDE_AFTER,)).fetchone()[0]
                    young = bool(waiting) and review_wait.hold(db, settings, review_max_wait(settings), settings.get('min_signals', 40)) > stamp
                    # A new mailbox: its first review starts as soon as its first import is in, as one review, not one
                    # halfway through the import and another after it (never past the usual longest wait).
                    mail = self.mail_backfill(db) if not recovery else {'filling': [], 'fresh': []}
                    # While the first review digs, its next batch goes at once: no waiting for a batch or for the rest of the import
                    nxt = bool(dig and dig['left'])
                    if mail['filling'] and young and not sort_due and not nxt:
                        return None
                    if not recovery and not mail['fresh'] and not sort_due and not nxt and (not waiting or (waiting < settings.get('min_signals', 40) and young and not asked)):
                        return None
                    if not waiting and not recovery and not sort_due:
                        return None
                    run = {'run_id': uuid.uuid4().hex, 'status': 'starting', 'started_at': now(), 'attempts': 0}
                    budget = first_look_batch(dig['left']) if nxt else RUN_SIGNAL_BUDGET
                    db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,planned,budget,promising) VALUES(?,?,?,?,?,?,?)",
                               (run['run_id'], 'starting', run['started_at'], run['started_at'], min(dig['left'] if nxt else waiting, budget), budget if nxt else None, int(nxt)))
                    self.review_asked = 0
            if run['status'] == 'starting':
                db.execute('UPDATE review_runs SET attempts=attempts+1,updated_at=? WHERE run_id=?', (now(), run['run_id']))
        expired = (stamp - dt.datetime.fromisoformat(run['started_at'])).total_seconds() > (
            settings.get('timeout_seconds', 1500) + settings.get('outage_grace_seconds', 600))
        # Stop/reconcile only this worker's exact run, never the main chat. Don't
        # release custody merely because a network request timed out.
        action = 'stop' if expired or run['status'] == 'recovering' else 'start' if run['status'] == 'starting' else 'status'
        request = {'kind': 'review', 'job_id': run['run_id'], 'action': action}
        if action == 'status' and (stamp - dt.datetime.fromisoformat(run['started_at'])).total_seconds() >= REVIEW_PROBE_SECONDS:
            # A Gateway restart ends a run without a terminal state for its id: the runner also checks the run is still
            # in its session, so a lost one ends now instead of after the timeout (a first look sat still for 35 minutes)
            request['probe'] = True
        offered_edits = []
        if request['action'] == 'start':
            self.store.note_rule_files(RULE_FILES)
            request['message'] = review_prompt(run['run_id'], [a['id'] for a in self.config['accounts']], self.store.preference_summary(), self.store.facts_text(ids=True),
                                               self.store.slipped(run['run_id']), self.store.promises_text(),
                                               self.store.unnamed_text(run['run_id']), self.store.role_text(run['run_id']), self.store.notes_to_learn(),
                                               self.waiting_handoffs_text(), self.split_notes_text(), self.store.boards_text(run['run_id']),
                                               self.store.sort_text(run['run_id']), source_notes(account_services(self.config)) + companies_prompt(self.config),
                                               self.store.fit_text(run['run_id']), self.backfill_text(run['run_id']), self.store.first_look_run(run['run_id']))
            try:  # drafts the owner rewrote, or answered themselves instead: lasting habits go into that channel's voice
                lines = self.store.edits_to_learn()
                if lines:
                    voices = self.store.voices_text()
                    block = ("\n\nDrafts the owner rewrote before sending, or answered themselves instead, shown once. Compare each draft with what they wrote. "
                             "When the difference shows how they write on that channel beyond that one message (length, tone, greeting, sign-off, language, "
                             "capitals, punctuation, emoji, formality), update that channel's voice: remember_fact kind=voice, channel, " + VOICE_TEXT + ", "
                             "edit_id. Skip differences in content or facts.\n"
                             + (f"Current voices:\n{voices}\n" if voices else '') + lines)
                    if len(request['message']) + len(block) < PROMPT_LIMIT - 2000:
                        request['message'] += block
                        offered_edits += re.findall(r'\(edit_id ([^)]+)\)', lines)
            except Exception as error:
                LOG.error('edits to learn error=%s', type(error).__name__)
            try:  # style notes no voice or rule came from yet (older ones, or ones a preparation didn't keep)
                lines = self.store.style_notes_to_learn()
                if lines:
                    voices = self.store.voices_text()
                    block = ("\n\nNotes where the owner said how a draft should have been written, not learned from yet, shown once. When one holds beyond "
                             "its card, work it into that channel's voice: remember_fact kind=voice, channel, " + VOICE_TEXT + ", "
                             "decision_id; how a kind of task is done is kind=draft. Skip notes that only fit that one message.\n"
                             + (f"Current voices:\n{voices}\n" if voices else '') + lines)
                    if len(request['message']) + len(block) < PROMPT_LIMIT - 2000:
                        request['message'] += block
                        offered_edits += ['note:' + value for value in re.findall(r'\(decision_id ([^)]+)\)', lines)]
            except Exception as error:
                LOG.error('style notes error=%s', type(error).__name__)
            try:  # condense what was learned, now and then, so it stays short and doesn't contradict itself
                lines = self.store.condense_text()
                if lines:
                    voices = self.store.voices_text()
                    block = ("\n\nCondense what you've learned, conservatively. Everything current, with ids:\n" + lines
                             + (f"\nVoices (how the owner writes per channel):\n{voices}" if voices else '') +
                             "\nOnly merge notes that say the same thing, overlap, or contradict each other: remember_fact replaces=[their ids], "
                             "text=<one sentence that keeps everything still true>, kind=draft for rules, else " + FACT_KIND_HINT + ". Where they contradict, the newer one (higher id) wins. "
                             "A note about how the owner writes on one channel goes into that channel's voice: remember_fact kind=voice, channel, "
                             + VOICE_TEXT + ", replaces=[ids]. A note a newer one made outdated merges into the newer one. "
                             "Notes marked likely the same are close in meaning: check those first, and merge them unless they really differ. "
                             "Never drop something nothing else still says, and leave a note alone when unsure. The originals stay as history and the owner can undo a merge. "
                             "A fact (not a draft rule) about one specific person, organization or project, with no about yet: tie it once with remember_fact id=<its id>, "
                             "about=[their graph node_ids], found with graph. One about the owner themselves or about the world stays without.")
                    block += self.skills_from_notes_prompt()
                    if len(request['message']) + len(block) < PROMPT_LIMIT - 2000:
                        request['message'] += block
                        offered_edits.append('condense:' + now()[:10])
            except Exception as error:
                LOG.error('condense error=%s', type(error).__name__)
            try:  # "There's a skill for this": installed skills that aren't ready here, while there is room this week
                hint = self.skills.hint_prompt() if getattr(self, 'skills', None) else ''
                if hint and len(request['message']) + len(hint) < PROMPT_LIMIT - 1500:
                    request['message'] += '\n\n' + hint
            except Exception as error:
                LOG.error('skill hint error=%s', type(error).__name__)
            if getattr(self, 'fleet', None):
                try:  # who a task can go to through The Machine (Hand it off)
                    people = sorted(set(self.fleet.handoff_people().values()))[:20]
                    if people:
                        request['message'] += ("\n\nTeammates in the owner's Work Fleet, each with their own Machine: " + ', '.join(people)
                                               + ". A task that is one of theirs is offered as a handoff to their Machine (Hand it off).")
                except Exception as error:
                    LOG.error('fleet teammates error=%s', type(error).__name__)
        # Offering learning context is not delivery: a Gateway outage must leave it eligible on retry.
        if len(request.get('message') or '') > PROMPT_LIMIT:  # the runner would refuse it on every retry: say so and end the run
            LOG.error('review prompt too long chars=%s limit=%s', len(request['message']), PROMPT_LIMIT)
            receipt = {'status': 'error', 'error': 'prompt_too_long', 'error_phase': 'runtime'}
        else:
            if request['action'] == 'start':  # what this start offers; a retry resends the first start's, with its own list
                request['_offered'] = offered_edits
            receipt = runner(request)
            offered_edits = request.get('_offered', offered_edits)
        result = receipt.get('status', 'unavailable')
        with self.store.connect() as db:
            if result == 'admitted':
                self.background_started()
                db.executemany('INSERT OR IGNORE INTO edits_offered(edit_id,run_id,offered_at) VALUES(?,?,?)',
                               [(value, run['run_id'], now()) for value in offered_edits])
                db.execute("UPDATE review_runs SET status='running',updated_at=?,error=NULL,error_phase=NULL,retry_at=NULL,unavailable_since=NULL WHERE run_id=?", (now(), run['run_id']))
            elif result in REVIEW_TERMINAL:
                getattr(self, 'model_usage_wake', threading.Event()).set()  # read the limits again after a run
                # A review that still ends with NO_REPLY (older instructions, or a model that says it anyway): on a CLI
                # runtime (Claude Code) OpenClaw fails that silent ending as an empty response, after the work: a run
                # whose batch finish_analysis saved is a finished review.
                if result == 'error' and receipt.get('silent_end') and db.execute(
                        "SELECT 1 FROM analyses WHERE owner_run=? AND owner_session=? AND status='complete' LIMIT 1",
                        (run['run_id'], REVIEW_SESSION_PREFIX + run['run_id'])).fetchone():
                    result = 'ok'
                fallback = {'error':'runtime_error','timed_out':'runtime_timeout','aborted':'runtime_aborted','lost':'runtime_lost'}
                error = (receipt.get('error') if receipt.get('error') in REVIEW_FAILURES else fallback.get(result)) if result!='ok' else None
                phase = (receipt.get('error_phase') if receipt.get('error_phase') in REVIEW_FAILURE_PHASES else 'runtime') if error else None
                # A first look's pass whose batch was saved is finished, whatever the runtime said after it (2026-10-27:
                # a 9-hour first look). Its error code still goes to the error reports and the log.
                status = 'ok' if error and self.store.first_look_run(run['run_id'], db) and self.store.review_batch_saved(db, run['run_id']) else result
                db.execute('UPDATE review_runs SET status=?,error=?,error_phase=?,last_error=coalesce(?,last_error),last_error_phase=coalesce(?,last_error_phase),error_at=CASE WHEN ? IS NOT NULL THEN ? ELSE error_at END,finished_at=?,updated_at=?,retry_at=NULL,unavailable_since=NULL WHERE run_id=?',
                           (status,None if status == 'ok' else error,None if status == 'ok' else phase,error,phase,error,now(),now(),now(),run['run_id']))
                # Terminal runtime proof makes its unfinished claim immediately
                # transferable. No event is marked reviewed by this recovery.
                db.execute("UPDATE analyses SET status='retryable',last_error=coalesce(last_error,'run_interrupted'),error_at=? WHERE owner_session=? AND owner_run=? AND status IN ('running','retryable')",
                           (now(), REVIEW_SESSION_PREFIX + run['run_id'], run['run_id']))
                if error:  # the error reports: its error code and phase, both from fixed lists (error_feed.py)
                    error_feed.record(db, 'review', error, phase or '', 'assistant.py', 'review_step', None, self.store.code_version)
                    saved = db.execute("SELECT count(*) FROM analyses WHERE owner_run=? AND owner_session=? AND status='complete'",
                                       (run['run_id'],REVIEW_SESSION_PREFIX+run['run_id'])).fetchone()[0]
                    reason = receipt.get('reason') if receipt.get('reason') in REVIEW_REASONS else None
                    LOG.warning('review runtime outcome=%s error=%s phase=%s saved_claims=%s' + (' reason=%s' if reason else '') + (' counted=ok' if status == 'ok' else ''),
                                result, error, phase, saved, *([reason] if reason else []))
                result = status
            elif result == 'unavailable':
                db.execute("UPDATE review_runs SET status=CASE WHEN ? THEN 'recovering' ELSE status END,error='openclaw_unavailable',error_phase='connection',last_error='connection_error',last_error_phase='connection',error_at=?,unavailable_since=coalesce(unavailable_since,?),retry_at=?,updated_at=? WHERE run_id=?",
                           (int(expired), now(), now(), (stamp + dt.timedelta(seconds=60)).isoformat(), now(), run['run_id']))
            else:
                db.execute("UPDATE review_runs SET status=CASE WHEN ? THEN 'recovering' ELSE status END,error=?,error_phase=NULL,retry_at=NULL,unavailable_since=NULL,updated_at=? WHERE run_id=?",
                           (int(action == 'stop'), 'completion_unconfirmed' if action == 'stop' else None, now(), run['run_id']))
        return result

    def review_queue(self, db, current=None):
        """With reviews on and none running: how many signals wait for the next review and about when it starts."""
        settings = self.config.get('review_worker') or {}
        if not settings.get('enabled') or db.execute("SELECT 1 FROM review_runs WHERE status IN ('starting','running','recovering')").fetchone():
            return None
        waiting = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<?', (SET_ASIDE_AFTER,)).fetchone()[0]
        current = current or dt.datetime.fromisoformat(now())
        mail = self.mail_backfill(db)
        first = not db.execute("SELECT 1 FROM review_runs WHERE status='ok'").fetchone()
        hold = review_wait.hold(db, settings, review_max_wait(settings), settings.get('min_signals', 40)) if waiting else None
        if mail['filling'] and (not hold or hold > current):
            # The first import of a mailbox is still coming in: the review starts when it is in (at the latest at hold)
            return {'waiting': waiting, 'planned': min(waiting, RUN_SIGNAL_BUDGET), 'starts_at': hold and hold.isoformat(),
                    'why': 'mail', 'first': first}
        if not waiting:
            return None
        last = db.execute('SELECT finished_at FROM review_runs WHERE finished_at IS NOT NULL ORDER BY finished_at DESC LIMIT 1').fetchone()
        after_gap = dt.datetime.fromisoformat(last[0]) + dt.timedelta(seconds=settings.get('gap_seconds', 600)) if last else current
        full = waiting >= settings.get('min_signals', 40) or bool(mail['fresh'])
        batch = current if full else hold
        return {'waiting': waiting, 'planned': min(waiting, RUN_SIGNAL_BUDGET), 'starts_at': max(after_gap, batch, current).isoformat(),
                'why': 'mail_in' if mail['fresh'] and after_gap <= current else 'batch' if batch >= after_gap and not full else 'gap',
                'first': first}

    def review_tick(self):
        """Seconds until the review worker looks again: FIRST_LOOK_TICK_SECONDS while a first look's batch runs or it
        digs on between batches (the owner watches it), and on a new install that has not reviewed yet while its first
        mail comes in or a new source's first page is due (first_page_due; the first look starts within seconds of the AI
        sign-in or the first page, not a tick later), else
        REVIEW_TICK_SECONDS. Never an error."""
        try:
            with self.store.connect() as db:
                current = dt.datetime.fromisoformat(now())
                live = db.execute("SELECT 1 FROM review_runs WHERE status IN ('starting','running','recovering') AND "
                                  "((preview=1 AND auto=1) OR window_hours IS NOT NULL OR promising=1) LIMIT 1").fetchone() or (
                    db.execute("SELECT 1 FROM milestones WHERE name='first_dig' AND at>?",
                               ((current - dt.timedelta(hours=FIRST_DIG_HOURS)).isoformat(),)).fetchone()
                    and not db.execute("SELECT 1 FROM milestones WHERE name='first_dig_done'").fetchone()) or (
                    (self.config.get('review_worker') or {}).get('first_look') is not False
                    and not db.execute('SELECT 1 FROM review_runs LIMIT 1').fetchone()
                    and (db.execute('SELECT 1 FROM events WHERE ingested_at>? AND history=0 LIMIT 1', ((current - dt.timedelta(hours=1)).isoformat(),)).fetchone()
                         or self.first_page_due(db, current)))
        except (sqlite3.Error, ValueError):
            return REVIEW_TICK_SECONDS
        return FIRST_LOOK_TICK_SECONDS if live else REVIEW_TICK_SECONDS

    def first_page_due(self, db, current):
        """On an install new today, a source whose first page is not in yet: it is about to land (the Machine restarts
        right after a source is connected), so the review worker already looks every few seconds. A 15 s tick set
        before the first page landed held a new owner's first look up to 15 s (agent users, 2026-11-08)."""
        since = (db.execute("SELECT at FROM milestones WHERE name='tracking_since'").fetchone() or [''])[0]
        if not since or since < (current - dt.timedelta(days=1)).isoformat():
            return False
        sources = [a['id'] for a in self.config.get('accounts', []) if a.get('id') and a.get('service') not in SYSTEM_SERVICES]
        landed = {r[0][len('first_page:'):] for r in db.execute("SELECT name FROM milestones WHERE name LIKE 'first_page:%'")}
        return any(s not in landed for s in sources)

    def review_live(self):
        """What the dashboard shows of reviews while they happen: runs in progress, the next one, the first look."""
        with self.store.connect() as db:
            runs = [self.store.review_run_view(db, dict(r)) for r in
                    db.execute("SELECT * FROM review_runs WHERE status IN ('starting','running','recovering') ORDER BY started_at DESC")]
            for run in runs:
                run['steps'] = review_steps(db, run, self.config.get('agent_db'))
            # The newest card: the dashboard shows a card as soon as a running review saves it, not after the review
            newest = db.execute('SELECT count(*),max(created_at) FROM suggestions').fetchone()
            queue, look = self.review_queue(db), self.first_look(db)
            # Before the first to-do ever: about when the first ones come (first_eta_minutes), for the empty state
            eta = None if newest[0] else first_eta_minutes(
                {'planned': runs[0].get('planned') or runs[0].get('claimed_count') or 0, 'done': runs[0].get('done_count') or 0,
                 'started_at': runs[0].get('started_at')} if runs else None, look, queue)
            return {'runs': runs, 'queue': queue, 'first_look': look, 'first_dig': self.first_dig_live(db),
                    'cards': {'count': newest[0], 'newest': newest[1]}, 'ai_connecting': ai_connecting(self.config), 'first_eta': eta}

    def start_preview(self, auto=False, quick=False):
        """`assistant preview`: one regular review run (same session, prompt and tool) over the last
        week's signals, for a new install with reviews still off. Its cards are shown on the dashboard
        only (see Store.suggest); review_step monitors the run. Config stays as it is."""
        if (self.config.get('review_worker') or {}).get('enabled'):
            raise ValueError('Checks are already on: new to-dos arrive by themselves. See assistant tasks or the dashboard.')
        accounts = [a['id'] for a in self.config['accounts']]
        hours = QUICK_LOOK_HOURS if quick else PREVIEW_DAYS * 24
        # The first look by itself: after the quick one, it digs on with the most promising FIRST_LOOK_NEXT_SIGNALS of the week
        nxt = auto and not quick
        budget = QUICK_LOOK_SIGNALS if quick else FIRST_LOOK_NEXT_SIGNALS if nxt else RUN_SIGNAL_BUDGET
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(hours=hours)).isoformat()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            run = db.execute("SELECT run_id,started_at,preview FROM review_runs WHERE status IN ('starting','running','recovering') LIMIT 1").fetchone()
            if run and run['preview']:
                return {'run_id': run['run_id'], 'started_at': run['started_at'], 'attached': True}  # follow the running preview
            if run or db.execute("SELECT 1 FROM analyses WHERE status='running' AND coalesce(resumed_at,started_at)>?",
                                 ((dt.datetime.fromisoformat(now()) - dt.timedelta(hours=1)).isoformat(),)).fetchone():
                raise ValueError('Another check is running. Try again when it has finished (assistant reviews).')
            waiting = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<? AND occurred_at>=? AND account_id IN ('
                                 + ','.join('?' for _ in accounts) + ')', (SET_ASIDE_AFTER, since, *accounts)).fetchone()[0] if accounts else 0
            if not waiting:
                raise ValueError(f'No unchecked signals from the last {PREVIEW_DAYS} days yet. Check assistant sources; the first import can take a few minutes.')
            run_id, started = uuid.uuid4().hex, now()
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,preview,auto,planned,window_hours,budget,promising) VALUES(?,'starting',?,?,1,?,?,?,?,?)",
                       (run_id, started, started, int(auto), min(waiting, budget), QUICK_LOOK_HOURS if quick else None, budget if quick or nxt else None, int(nxt)))
            if quick:
                self.note_dig_start(db)
        return {'run_id': run_id, 'started_at': started, 'waiting': waiting, 'signals': min(waiting, budget)}

    def review_worker(self):
        others = 0.0
        while not self.stop.wait(self.review_tick()):
            try:self.follow_config()
            except Exception as error:LOG.error('config follow error=%s',type(error).__name__)
            try:
                # The first look's next batch as soon as one ended, not a tick later (review_tick)
                if self.review_step() in REVIEW_TERMINAL and self.review_tick() < REVIEW_TICK_SECONDS:
                    self.review_step()
            except Exception as error:LOG.error('review worker error=%s',type(error).__name__)
            if time.monotonic() - others < REVIEW_TICK_SECONDS:
                continue  # the rest keeps its own pace while the first look is checked more often
            others = time.monotonic()
            try:self.profile_step()
            except Exception as error:LOG.error('profile worker error=%s',type(error).__name__)
            try:self.first_profile_step()
            except Exception as error:LOG.error('first profile error=%s',type(error).__name__)
            try:self.orgs_backfill_step()
            except Exception as error:LOG.error('orgs backfill error=%s',type(error).__name__)
            try:self.share_history_step()
            except Exception as error:LOG.error('share history error=%s',type(error).__name__)
            try:self.recap_step()
            except Exception as error:LOG.error('recap error=%s',type(error).__name__)
            try:self.still_needed_step()
            except Exception as error:LOG.error('still needed error=%s',type(error).__name__)

    def preview_review_action(self, name, args, owner_dashboard=False):
        return self.start_preview()

    def review_now_action(self, name, args, owner_dashboard=False):
        # the dashboard's Review now while reviews wait for the budget: the owner's own, like a preview
        if not owner_dashboard:
            raise ValueError('Only the owner can do this, on the dashboard')
        if not (self.config.get('review_worker') or {}).get('enabled'):
            return self.start_preview()
        self.review_asked, self.review_paused = time.time(), None
        LOG.info('review now asked')
        return {'asked': True}

    def review_context_action(self, name, args, owner_dashboard=False):
        return self.store.review_context(args['owner_session'], args.get('owner_run'))

    def review_failed_action(self, name, args, owner_dashboard=False):
        return self.store.review_failed(args['owner_session'], args['owner_run'], args['reason'], args.get('terminal', False))

    def analysis_page_action(self, name, args, owner_dashboard=False):
        return self.store.analysis_page(args['analysis_id'], args.get('page', 1), args.get('row_offset', 0))

    def finish_analysis_action(self, name, args, owner_dashboard=False):
        if args.get('_review_run'):  # a review that got "Boards to suggest" or "Boards to sort" answers them before it finishes
            with self.store.connect() as db:
                graph.board_check_answer(db, args['_review_run'], args.get('boards'))
                graph.sort_answer(db, args['_review_run'], args.get('sorted'))
                graph.fit_answer(db, args['_review_run'], args.get('fits'))
                graph.backfill_answer(db, args['_review_run'], args.get('fits'))
        return self.store.finish_analysis(args['analysis_id'], args.get('summary', ''), args.get('_review_session'), args.get('_review_run'), args.get('reviewed_ids'), args.get('projects'),
                                         args.get('stages'), args.get('team'), args.get('replies'), args.get('read'), args.get('no_todo'))

    def enrich_action(self, name, args, owner_dashboard=False):
        # the CLI: status, or one domain now
        if args.get('domain'):
            try:
                found = enrichment.lookup(self.store.connect, self.config, args['domain'], now())
            except enrichment.EnrichmentError as error:
                raise ValueError(str(error)) from None
            self.graph_dirty.set()
            return found
        with self.store.connect() as db:
            return {**enrichment.status(db, self.config), 'people': enrichment.people_status(db)}

    def looks_handled_action(self, name, args, owner_dashboard=False):
        if args.get('plan_changed') is True:  # a newer message overturned its plan: it closes by itself (Store.plan_changed)
            return self.store.plan_changed(args['suggestion_id'], args.get('reason'), args.get('event_ids') or [])
        return self.store.looks_handled(args['suggestion_id'], args.get('reason'), args.get('event_ids') or [])

    def handoff_on_it_action(self, name, args, owner_dashboard=False):
        # the review: a message the owner sent or a call they joined shows they took a waiting handoff on
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine is not on the Network')
        return self.fleet.handoff_on_it(str(args.get('ask_id') or ''), args.get('event_id'))

    def split_from_notes_action(self, name, args, owner_dashboard=False):
        # the review: a meeting's notes give its next steps to the people in a proposed split
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine is not on the Network')
        return self.fleet.fill_split(str(args.get('split_id') or ''), args.get('event_id'), args.get('parts') or {})

    def split_notes_text(self):
        """Proposed follow-up splits whose meeting has notes to read, for the review; nothing when off the Network."""
        try:
            return self.fleet.split_notes_text() if getattr(self, 'fleet', None) else ''
        except Exception as error:  # the review goes on without them
            LOG.warning('split notes error=%s', type(error).__name__)
            return ''

    def events_action(self, name, args, owner_dashboard=False):
        # reading signals (events, related) and starting a review (begin_analysis), on explicit accounts only
        accounts = [a['id'] for a in self.config['accounts']]
        selected = args.get('account_ids', [])
        if name in ('events', 'related') and selected in ('all', ['all']):
            selected = accounts  # search everything, asked for explicitly
        if name in ['events', 'begin_analysis', 'related'] and (not selected or not set(selected) <= set(accounts)):
            raise ValueError('Choose explicit configured account_ids (' + json.dumps(accounts) + ', or ["all"] to search every account with events '
                             'or related); cross-account reads must be intentional. A to-do\'s own accounts are its account_ids in status.')
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
