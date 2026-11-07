"""The Store's first look (refactor PR 18): a new Machine's first steps. The first import and first look, the greeting,
first tips and when setup is done. A mixin of Store (assistant.py), like App's mixins. Moved out of assistant.py as
is."""
import datetime as dt
import json
import re
import secrets
import sqlite3
import time

import activity
import graph
from machine.config import LOG
from machine.store.review import REVIEW_SESSION_PREFIX
from machine.store.views import sender_first_name
from machine.text import _address, encoded
import next_actions
import still_needed
from timeutil import local_tz, now


# First-use tips on the dashboard (Store.first_tips): 'change' on a new person's first to-do (Change how and
# Not needed), 'send' on their first ready draft (nothing goes out until Send). Each goes once its button was used.
FIRST_TIPS = ('change', 'send')


TIP_USED = {'change': {'other', 'reject'}, 'send': {'send'}}


TIP_SOURCES = ('dashboard', 'telegram', 'owner-chat', 'voice')  # the owner's own decisions


GREETING_HOURS = 24  # the dashboard's hello (Store.greeting) shows this long from a new owner's first view


FIRST_TIPS_UNTIL = 10  # to-dos decided: past their first to-dos, every tip is gone


FIRST_ACTIONS = {'accept': 'approve', 'other': 'approve', 'prepare_next': 'approve', 'send': 'send', 'complete': 'done', 'reject': 'dismiss'}


FIRST_MAGIC_SETTLE_SECONDS = 900  # no card shown yet: a finished review counts as the first look after this long


# Onboarding value past the first approval (a click), for first_cards_report: the first to-do whose preparation finished
# with a result or draft (first_prepared: 'result' or 'draft'), and the first action the provider confirmed went through
# (first_verified_action: its kind). A demo send and a fix merged into The Machine itself don't count.
VERIFIED_KINDS = tuple(k for k in next_actions.APPROVE_KINDS if k not in ('email_demo', 'merge'))


def first_value(db, marks, since):
    """{first_prepared_at, first_prepared, first_prepared_backfill, first_verified_action_at, ...} for first_cards_report.
    From the marks (note_first); on an install that had them before they were marked, estimated from what it kept: when a
    draft first showed or a preparation last finished, when a confirmed send or final step was last updated. Those are
    never earlier than the real first, so they are flagged as backfill. Nothing from before tracking_since."""
    out = {}
    found = {}
    for at, kind in db.execute("SELECT min(saved_at),'draft' FROM draft_saves WHERE saved_at>=? UNION ALL "
                               "SELECT min(updated_at),'result' FROM preparations WHERE status='done' AND updated_at>=?", (since, since)).fetchall():
        if at and ('first_prepared' not in found or at < found['first_prepared'][0]):
            found['first_prepared'] = (at, kind)
    row = db.execute("SELECT updated_at,json_extract(payload,'$.kind') FROM action_jobs WHERE updated_at>=? AND (status='sent' AND message_id IS NOT NULL "
                     "AND json_extract(payload,'$.kind') IN (" + ','.join('?' for _ in VERIFIED_KINDS) + ") OR status='done' "
                     "AND json_extract(payload,'$.kind')='finish' AND json_extract(payload,'$.finish_result.state')='completed') "
                     "ORDER BY updated_at LIMIT 1", (since, *VERIFIED_KINDS)).fetchall()
    if row:
        found['first_verified_action'] = tuple(row[0])
    for name in ('first_prepared', 'first_verified_action'):
        mark = marks.get(name)
        at, kind = mark if mark else found.get(name, (None, None))
        out[name + '_at'], out[name], out[name + '_backfill'] = at, kind, bool(at and not mark)
    return out


class FirstLookStore:
    """Store methods for a new Machine's first steps."""

    def note_first_import(self, db, account, state):
        """Milestones of a source's first import: its first page in, and the whole import in (its checkpoint leaves
        bootstrap). Only a source that starts here is timed: one already past its first import keeps no milestone."""
        row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account,)).fetchone()
        try:
            before = json.loads(row['state'] or '{}') if row else {}
        except (TypeError, ValueError):
            return
        if before.get('mode') not in ('bootstrap', None) or (before and 'mode' not in before):
            return  # past its first import (or a plugin's own cursor): not timed
        db.execute('INSERT OR IGNORE INTO milestones(name,at) VALUES(?,?)', ('first_page:' + account, now()))
        if (state or {}).get('mode', 'incremental') not in ('bootstrap', 'resync') and not (state or {}).get('page_token'):
            db.execute('INSERT OR IGNORE INTO milestones(name,at) VALUES(?,?)', ('first_import:' + account, now()))

    def first_look_run(self, run_id, db=None):
        """Whether a review run is part of the first look: a preview it started by itself, the quick first review, or
        its digging on after (first_dig), before the first look stopped digging. `db`: a caller's open connection."""
        if db is None:
            with self.connect() as db:
                return self.first_look_run(run_id, db)
        if db.execute("SELECT 1 FROM milestones WHERE name='first_dig_done'").fetchone():
            return False
        row = db.execute('SELECT preview,auto,window_hours,promising FROM review_runs WHERE run_id=?', (run_id,)).fetchone()
        return bool(row and ((row['preview'] and row['auto']) or row['window_hours'] or row['promising']))

    @staticmethod
    def reviews_failing(db):
        """How many reviews in a row ended without going well, the newest back to the last one that did (at most a dozen
        counted). For the dashboard's first look (App.first_look, App.first_dig_live): from the third on, it says the
        tries keep failing instead of "Reading on"."""
        failed = 0
        for (status,) in db.execute('SELECT status FROM review_runs WHERE finished_at IS NOT NULL ORDER BY finished_at DESC LIMIT 12'):
            if status == 'ok':
                break
            failed += 1
        return failed

    @staticmethod
    def review_batch_saved(db, run_id):
        """The run's reviewer saved its batch (finish_analysis) and left no batch of its own unfinished: a first look's
        pass that did its work, also when its runtime reported a failure after it (App.review_step)."""
        session = REVIEW_SESSION_PREFIX + run_id
        return bool(db.execute("SELECT 1 FROM analyses WHERE owner_run=? AND owner_session=? AND status='complete' LIMIT 1", (run_id, session)).fetchone()
                    and not db.execute("SELECT 1 FROM analyses WHERE owner_run=? AND status IN ('running','retryable') LIMIT 1", (run_id,)).fetchone())

    def note_first_look(self, db, look):
        """The first look's last state, for the health report (first_cards_report): kept only when it changed."""
        detail = encoded({k: look.get(k) for k in ('state', 'why', 'quick', 'waiting', 'retry_at') if look.get(k) is not None}) if look else None
        row = db.execute("SELECT detail FROM milestones WHERE name='first_look_state'").fetchone()
        if not row or row['detail'] != detail:
            db.execute("INSERT OR REPLACE INTO milestones(name,at,detail) VALUES('first_look_state',?,?)", (now(), detail))

    def first_magic_done(self, db):
        """The first look has done its job, so the rest of onboarding (profile, voices, roles, organizations, drafts
        beyond the first) may start: the first card was shown, or a review finished a while ago (one that found no card,
        an install from before this was recorded)."""
        if db.execute("SELECT 1 FROM milestones WHERE name='first_card_shown'").fetchone():
            return True
        settled = (dt.datetime.fromisoformat(now()) - dt.timedelta(seconds=FIRST_MAGIC_SETTLE_SECONDS)).isoformat()
        return bool(db.execute("SELECT 1 FROM review_runs WHERE status='ok' AND finished_at<=? LIMIT 1", (settled,)).fetchone())

    def note_card_shown(self):
        """The first card the dashboard showed on a new install (one with cards from before this was recorded keeps none)."""
        if getattr(self, '_card_shown', False):
            return
        with self.connect() as db:
            if db.execute("SELECT 1 FROM milestones WHERE name='first_card_shown'").fetchone():
                self._card_shown = True
                return
            since = (db.execute("SELECT at FROM milestones WHERE name='tracking_since'").fetchone() or [''])[0]
            if db.execute('SELECT 1 FROM suggestions WHERE created_at<?', (since,)).fetchone():
                self._card_shown = True  # cards from before: not a new install's first
                return
            shown = db.execute("SELECT count(*) FROM suggestions WHERE status IN ('pending','accepted','instructions','prepared')").fetchone()[0]
            if shown:
                db.execute("INSERT OR IGNORE INTO milestones(name,at,detail) VALUES('first_card_shown',?,?)", (now(), str(shown)))
                self._card_shown = True

    def note_activity(self, kind, ref=None):
        """Count one dashboard moment for the daily activity counts (activity.py): 'dashboard' (its list was asked for),
        'visit' (a page load) or 'opened' (a to-do, ref its id). Never raises: a count never costs the owner a page.
        The list's poll writes at most once a minute."""
        if kind == 'dashboard':
            if time.time() - getattr(self, '_activity_at', 0) < 60:
                return
            self._activity_at = time.time()
        try:
            with self.connect() as db:
                activity.ensure(db)
                if kind == 'dashboard':
                    activity.note_dashboard(db, now(), local_tz())
                elif kind == 'visit':
                    activity.note_visit(db, now(), local_tz())
                elif kind == 'opened' and isinstance(ref, str) and re.fullmatch(r'[a-f0-9]{16}', ref):
                    activity.note_opened(db, ref, now(), local_tz())
        except (sqlite3.Error, ValueError) as error:
            LOG.warning('activity not noted kind=%s error=%s', kind, type(error).__name__)

    def first_tips(self):
        """The first-use tips still to show on the dashboard (FIRST_TIPS), kept on the Machine so every device agrees.
        Only a new person gets them: the first time this is asked, someone who has already decided a to-do is past them
        for good ('tips' milestone off). A tip goes when its button was used (TIP_USED, from any device or Telegram),
        when it was closed with × (tip_done), and all of them once FIRST_TIPS_UNTIL to-dos were decided."""
        with self.connect() as db:
            decided = db.execute('SELECT count(*) FROM (SELECT 1 FROM decisions WHERE source IN (' + ','.join('?' * len(TIP_SOURCES))
                                 + ') LIMIT ?)', (*TIP_SOURCES, FIRST_TIPS_UNTIL)).fetchone()[0]
            row = db.execute("SELECT detail FROM milestones WHERE name='tips'").fetchone()
            if not row:
                db.execute("INSERT OR IGNORE INTO milestones(name,at,detail) VALUES('tips',?,?)", (now(), 'off' if decided else 'on'))
                row = db.execute("SELECT detail FROM milestones WHERE name='tips'").fetchone()
            if row['detail'] != 'on' or decided >= FIRST_TIPS_UNTIL:
                return []
            done = {r['name'][4:] for r in db.execute("SELECT name FROM milestones WHERE name LIKE 'tip:%'")}
            used = {r['choice'] for r in db.execute('SELECT DISTINCT choice FROM decisions WHERE source IN (' + ','.join('?' * len(TIP_SOURCES)) + ')', TIP_SOURCES)}
        return [tip for tip in FIRST_TIPS if tip not in done and not used & TIP_USED[tip]]

    def greeting(self, owner_name=''):
        """The dashboard's hello on a new owner's first views (GREETING_HOURS from their first, until they first decide a
        to-do): {'name': their first name, 'line': {'person', 'since', 'card'}} with the open to-do someone has waited
        on them for longest (greeting_wait; a ready one first), named from their own Machine; just the name when
        nothing is ready yet. The line names who wrote the to-do's own message (its first evidence, as its source line),
        never another message it carries, so it always names what it links to; a to-do whose sender has no proper name
        (greeting_name) gives no line. The dashboard leads with that to-do (line.card) and keeps the rest of the page quiet.
        None once past it, or for someone who had decided to-dos before this existed. For the owner's own dashboard only:
        nothing of it goes into a report or leaves the Machine."""
        first = (str(owner_name or '').split() or [''])[0]
        first = first if re.fullmatch(r"[^\W\d_][\w'’-]*", first) else ''
        with self.connect() as db:
            decided = lambda since='': db.execute(
                'SELECT 1 FROM decisions WHERE source IN (' + ','.join('?' * len(TIP_SOURCES)) + ') AND choice IN ('
                + ','.join('?' * len(FIRST_ACTIONS)) + ') AND created_at>=? LIMIT 1', (*TIP_SOURCES, *FIRST_ACTIONS, since)).fetchone()
            row = db.execute("SELECT at,detail FROM milestones WHERE name='greeting'").fetchone()
            if not row:
                db.execute("INSERT OR IGNORE INTO milestones(name,at,detail) VALUES('greeting',?,?)", (now(), 'off' if decided() else 'on'))
                row = db.execute("SELECT at,detail FROM milestones WHERE name='greeting'").fetchone()
            ends = (dt.datetime.fromisoformat(row['at']) + dt.timedelta(hours=GREETING_HOURS)).isoformat()
            if row['detail'] != 'on' or decided(row['at']) or now() >= ends:
                return None
            # A ready to-do (its draft prepared) before one still to decide or preparing; within each, the longest wait
            best = None
            for card in db.execute('SELECT id,status,event_ids FROM suggestions WHERE ' + activity.SHOWN, (now(),)).fetchall():
                found = self.greeting_wait(db, card)
                person = found and self.greeting_name(db, found[1])
                key = found and (card['status'] != 'prepared', found[0])
                if person and (not best or key < best[0]):
                    best = (key, {'person': person, 'since': found[0], 'card': card['id']})
        line = best and best[1]
        return {'name': first, **({'line': line} if line else {})} if first or line else None

    def greeting_wait(self, db, card):
        """(since, row) for the hello: the earliest unanswered message someone waits on the owner for in the to-do's own
        conversation (its first evidence, and the rest of that thread among its evidence), or None. Another message the
        to-do also carries (its "+1 more", from someone else) never names it."""
        ids = json.loads(card['event_ids'] or '[]')
        rows = {r['id']: dict(r) for r in db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE deleted=0 AND id IN ('
                                                     + ','.join('?' * len(ids)) + ')', ids)} if ids else {}
        rows = [rows[i] for i in ids if i in rows and rows[i]['kind'] != 'owner.card']
        if not rows:
            return None
        meta = lambda r: r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        lead, thread = rows[0], meta(rows[0]).get('thread_id')
        same = [r for r in rows if r is lead or (thread and r['kind'] == lead['kind'] and r['account_id'] == lead['account_id']
                                                 and meta(r).get('thread_id') == thread)]
        return self.waiting_since(db, same)

    @staticmethod
    def greeting_name(db, row):
        """Who to name in the hello for this message: the sender's first name as the message gives it, else the name the
        Graph knows them by, else their organization ("Acme Town Hall"). '' when only a mailbox name ("billing",
        "frontdesk") or an address is known: no line then, never a name made up from an address."""
        m = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
        person = sender_first_name(m)
        if person:
            return person
        address = _address(m.get('from'))
        for r in db.execute("SELECT n.name,o.name org FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id LEFT JOIN graph_nodes o "
                            "ON o.id=json_extract(n.info,'$.org') AND o.kind='org' WHERE g.direct=1 AND n.kind='person' AND g.event_id=? "
                            "ORDER BY n.strength DESC", (row['id'],)):
            name = sender_first_name({'from': graph.person_name(r['name'] or '') + (f' <{address}>' if address else '')})
            if name:
                return name
            org = ' '.join(str(r['org'] or '').split())
            if org and '@' not in org and re.search(r'[^\W\d_]{2}', org):
                return org
        return ''

    @staticmethod
    def still_needed_ask(db, stamp, skip=lambda row: False, tz=dt.timezone.utc):
        """Still needed? (still_needed.py) in the weekly recap's choices table: ends the question of a to-do that closed
        (dropped when it was rejected), then asks once on each to-do still_needed.due names. Returns the ids asked now."""
        db.execute("UPDATE recap_items SET status=CASE WHEN (SELECT status FROM suggestions WHERE id=recap_items.ref)='rejected' THEN 'dropped' "
                   "ELSE 'closed' END,decided_at=? WHERE kind=? AND status='open' AND COALESCE((SELECT status FROM suggestions WHERE id=recap_items.ref),"
                   "'rejected') IN ('completed','rejected')", (stamp, still_needed.KIND))
        rows = still_needed.due(db, stamp, skip, tz)
        for r in rows:
            db.execute("INSERT INTO recap_items(id,week,n,kind,ref,line,data,status) VALUES(?,'',0,?,?,?,?,'open')",
                       ('sn_' + secrets.token_hex(6), still_needed.KIND, r['id'], r['title'], json.dumps({'asked_at': stamp})))
        return [r['id'] for r in rows]

    @staticmethod
    def greeting_on(db, at):
        """The hello's first view is now (`at`), whatever was decided before: for the sandbox, whose sample history is
        older than its owner's first look (the site demo shows the first view)."""
        db.execute("INSERT OR REPLACE INTO milestones(name,at,detail) VALUES('greeting',?,'on')", (at,))

    def setup_closed(self, step, closed=True):
        """The setup to-do's row (or card) closed with its ×, or back (closed=False; step 'all': every one), on every device
        (milestones 'setup:<step>'; machine/app/setup_card.py checks the step)."""
        with self.connect() as db:
            if closed:
                db.execute('INSERT OR IGNORE INTO milestones(name,at) VALUES(?,?)', ('setup:' + step, now()))
            elif step == 'all':
                db.execute("DELETE FROM milestones WHERE name LIKE 'setup:%'")
            else:
                db.execute('DELETE FROM milestones WHERE name=?', ('setup:' + step,))

    def tip_done(self, tip):
        """A first-use tip closed (×) or its button used on the dashboard: it never comes back, on any device."""
        if tip not in FIRST_TIPS:
            raise ValueError('Unknown tip')
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO milestones(name,at) VALUES(?,?)', ('tip:' + tip, now()))
        return {'first_tips': self.first_tips()}
