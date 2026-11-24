"""Meeting prep, the App's part: the pass that turns an upcoming meeting with people from outside into one briefing
to-do (meeting_prep.py has the rules). A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import sqlite3
import subprocess
import threading
import time

import enrichment
import graph
import i18n
import learning_loop
import locale_prefs
import meeting_prep
import person_summary
from machine import model_reply, signin_search
from machine.config import LOG
from machine.prompts import bias
from machine.sources.calendar import calendar_owned
from machine.store.review import CARD_OPEN
from machine.todo_states import OPEN_NOT_SNOOZED
from models import background_model, openclaw_model
from timeutil import local_tz, now

MEETING_PREP_SECONDS = 600  # how often the calendar is looked at
MEETING_PREP_TURN_SECONDS = 180
MEETING_PREP_SEARCH_SECONDS = 30
STALE_ONCE = 'meeting_prep_format_'  # + meeting_prep.FORMAT, in learning_state: open briefings written again once


class MeetingPrepApp:
    ACTIONS = {}

    def meeting_prep_step(self, every=MEETING_PREP_SECONDS):
        """About every ten minutes: a moved or canceled meeting's briefing follows it, and the next meeting due a
        briefing gets its one turn, in a thread of its own, within the usage budget like every background turn. With
        none due, an open briefing still in an older format is written again (once after an upgrade that changed it)."""
        if self.config.get('meeting_prep') is False or not (self.config.get('review_worker') or {}).get('enabled'):
            return None
        if time.monotonic() - self.__dict__.get('meeting_prep_at', -every) < every:
            return None
        self.meeting_prep_at = time.monotonic()
        self.meeting_prep_follow()
        thread = getattr(self, '_meeting_prep_thread', None)
        if thread and thread.is_alive():
            return None
        if not self.background_spaced() or self.background_pause(job='meeting-prep'):
            return None
        meeting, run = self.meeting_prep_next(), self.meeting_prep_run
        if not meeting:
            meeting, run = self.meeting_prep_stale_next(), self.meeting_prep_rebuild
        if not meeting:
            return None
        self.background_started()
        self._meeting_prep_thread = threading.Thread(target=run, args=(meeting,), name='meeting-prep', daemon=True)
        self._meeting_prep_thread.start()
        return meeting['id']

    def meeting_prep_owner(self, db):
        owner = graph.Owner({'accounts': self.config.get('accounts', [])}, db)
        return owner.emails, owner.domains | set(owner.team or ())

    def meeting_prep_next(self, current=None):
        """The soonest meeting due a briefing and not judged yet, with what it reads; None when there is none or the
        day's turns are used. One with no evidence is passed over (it may have some on a later pass), never asked. After a
        reply that couldn't be read none is due for a while, then the others first (model_reply.Waiting)."""
        wait = model_reply.waiting(self, 'meeting-prep')
        if wait.resting():
            return None
        current = current or dt.datetime.fromisoformat(now())
        sides = {a['id']: graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')}
        with self.store.connect() as db:
            if meeting_prep.judged_today(db, (current - dt.timedelta(days=1)).isoformat()) + wait.today() >= meeting_prep.PER_DAY:
                return None
            emails, domains = self.meeting_prep_owner(db)
            found = meeting_prep.upcoming(db, current, calendar_owned, emails, domains, local_tz())
            done = meeting_prep.judged(db, [m['key'] for m in found])
            series = lambda m: bool(m['meta'].get('recurring_event_id'))
            room = meeting_prep.recurring_today(db, (current - dt.timedelta(days=1)).isoformat()) < meeting_prep.RECURRING_PER_DAY
            research = self.config.get('meeting_prep_research') is not False and enrichment.people_on(db)
            for meeting in sorted(found, key=lambda m: (wait.tries(m['key']), series(m))):  # one-offs first
                if meeting['key'] in done or wait.spent(meeting['key']) or series(meeting) and not room:
                    continue
                if meeting_prep.taken(db, meeting['id'], CARD_OPEN):  # the review already made a to-do for it
                    meeting_prep.keep(db, meeting, 'taken', None, now())
                    continue
                side = sides.get(meeting['account_id'])
                again = meeting_prep.repeated(db, meeting, current)
                if again and not again['over']:
                    continue  # after the one before it
                evidence = meeting_prep.evidence(db, meeting, side, sides, emails, domains, current, CARD_OPEN, calendar_owned, graph.resolve,
                                                 person_summary.prep_lines, graph.excerpt)
                if again:
                    evidence['recurring'] = meeting_prep.news(db, meeting, evidence, again)
                if not meeting_prep.worth_asking(evidence) and not meeting_prep.worth_looking(meeting, side, evidence, enrichment.shared_host, research):
                    continue  # quality or nothing: no turn, no to-do
                if all(p.get('role') and graph.personal_relation(p['role']) for p in evidence['people']):
                    meeting_prep.keep(db, meeting, 'family', None, now())  # family and friends only: their own life, no turn
                    continue
                return {**meeting, 'side': side, 'evidence': evidence}
        return None

    def meeting_prep_model_turn(self, text):
        stand_in = getattr(self, 'meeting_prep_model', None)  # tests and the sandbox: (config, prompt)
        if stand_in:
            return stand_in(self.config, text)
        import help_chat
        swap = background_model(self.config)  # never the costliest model for background work
        return help_chat.openclaw_model_run(self.config, text, '/'.join(swap) if swap else None, timeout=MEETING_PREP_TURN_SECONDS)

    def meeting_prep_search(self, ask):
        """One web search through OpenClaw (`openclaw infer web search`, the provider the owner set up), else, where none is
        and the owner has it on, on their own ChatGPT or Claude sign-in (machine/signin_search.py): its results
        [{'title', 'url', 'description', 'published'}], or None when there is no search or it failed. The query is
        only a public name, organization and domain (meeting_prep.research_queries)."""
        stand_in, query = getattr(self, 'meeting_prep_web_search', None), ask['query']  # tests and the sandbox: (query)
        if stand_in:
            return stand_in(query)
        if signin_search.on(self.config) and signin_search.provider_set_up(self.config) is False:
            return signin_search.search(self.config, ask)
        args = [str(self.config.get('openclaw') or 'openclaw'), 'infer', 'web', 'search', '--json', '--limit', '5', '--query', query]
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=MEETING_PREP_SEARCH_SECONDS)
            data = json.loads(result.stdout or '{}')
        except (OSError, ValueError, subprocess.TimeoutExpired) as failure:
            LOG.info('meeting prep search error=%s', type(failure).__name__)
            return None
        outputs = [o.get('result') for o in data.get('outputs') or () if isinstance(o, dict) and isinstance(o.get('result'), dict)]
        if result.returncode != 0 or not data.get('ok') or not outputs:
            LOG.info('meeting prep search failed')
            return None
        return [r for r in outputs[0].get('results') or () if isinstance(r, dict)]

    def meeting_prep_site(self, domain):
        """The home page of an organization's own website as one result, or None when it can't be read."""
        read = getattr(self, 'meeting_prep_site_text', None) or enrichment.site_text  # tests and the sandbox: (domain)
        page = read(domain)
        return [page] if page else None

    def meeting_prep_research(self, meeting):
        """Short web research for a meeting that warrants it (meeting_prep.research_queries), when Look up work
        contacts is on: the kept results as W ids, also put on the meeting's evidence. Nothing is fetched while the
        database is held."""
        found, current = meeting['evidence'], dt.datetime.fromisoformat(now())
        if self.config.get('meeting_prep_research') is False:
            return {}
        with self.store.connect() as db:
            if not enrichment.people_on(db):
                return {}
            asks = meeting_prep.research_queries(found, enrichment.shared_host)
            raw = meeting_prep.web_raw(db, asks, current)
        ran = {}
        for ask in asks:
            if ask['query'] not in raw:
                ran[ask['query']] = self.meeting_prep_site(ask['domain']) if ask['about'] == 'site' else self.meeting_prep_search(ask)
        if any(got is not None for got in ran.values()):
            with self.store.connect() as db:
                raw.update((query, meeting_prep.web_keep(db, query, got, current)) for query, got in ran.items() if got is not None)
        web = meeting_prep.web_results(asks, raw)
        if asks:
            LOG.info('meeting prep web asks=%d searched=%d kept=%d', len(asks), len(ran), len(web))
        found['web'] = web
        found['searches'] = sum(a['about'] != 'site' and ran.get(a['query']) is not None for a in asks)
        return web

    def meeting_prep_brief(self, meeting):
        """Research when it warrants it, then the meeting's one turn: its answer checked (meeting_prep.parse), or None.
        Raises help_chat.Unavailable when there is no model now, model_reply.Unreadable when its reply couldn't be read
        (asked once more), and what the turn raised."""
        try:
            self.meeting_prep_research(meeting)
        except (sqlite3.Error, OSError, ValueError, TypeError) as error:  # a briefing without research beats none
            LOG.warning('meeting prep research error=%s', type(error).__name__)
        if not meeting_prep.worth_asking(meeting['evidence']) and not meeting_prep.looked_up(meeting['evidence']):
            return None  # nothing between them and nothing found: no turn
        meeting['evidence']['owner_organization'] = self.meeting_prep_own_organization(meeting)
        swap = background_model(self.config)  # the model meeting_prep_model_turn runs on, for its own bias correction
        note = bias.model_note('/'.join(swap) if swap else openclaw_model(self.config))
        if meeting['evidence'].get('notes'):
            meeting['evidence']['owner_name'] = self.owner_full_name()  # the notes name who does what: which of them is the owner
        text = meeting_prep.prompt(meeting, meeting['evidence'], local_tz(), i18n.prompt_rule(locale_prefs.language_of(self.config)), note)
        return model_reply.ask(self.meeting_prep_model_turn, text, lambda reply: meeting_prep.parse(reply, meeting['evidence']))

    def meeting_prep_own_organization(self, meeting):
        """What the owner's own organization does, as it was looked up (enrichment.py): the one of the meeting's calendar,
        else the only one known. None when none is."""
        address = next((str(a.get('email') or '') for a in self.config.get('accounts', []) if a.get('id') == meeting['account_id']), '')
        with self.store.connect() as db:
            owner = graph.Owner({'accounts': self.config.get('accounts', [])}, db)
            known = {d: p for d in sorted(owner.domains) if (p := enrichment.profile_of(db, d))}
        profile = known.get(address.rpartition('@')[2].lower()) or (next(iter(known.values())) if len(known) == 1 else None)
        return {k: str(profile[k])[:300] for k in ('name', 'about', 'industry') if profile.get(k)} if profile else None

    def meeting_prep_cites(self, meeting):
        """What each source of the briefing is called after a point from it: "Kickoff call, Nov 3"."""
        tz = local_tz()
        return meeting_prep.cites(meeting['evidence'], lambda at: locale_prefs.day_text(at.astimezone(tz), weekday=False))

    def meeting_prep_unreadable(self, meeting):
        """The reply couldn't be read, twice: no verdict, a later pass asks again (model_reply.Waiting)."""
        model_reply.waiting(self, 'meeting-prep').missed([meeting['key']])
        LOG.warning('meeting prep reply unreadable')

    def meeting_prep_run(self, meeting):
        """The meeting's one turn, then its to-do, or nothing when the turn found nothing useful. Returns the to-do's id."""
        import help_chat
        try:
            found = self.meeting_prep_brief(meeting)
        except help_chat.Unavailable:
            LOG.info('meeting prep: no model now')
            return None  # not judged: the next pass asks again
        except model_reply.Unreadable:
            return self.meeting_prep_unreadable(meeting)
        except (OSError, ValueError, TypeError) as failure:  # the turn may have run: never a second one for this meeting
            LOG.warning('meeting prep error=%s', type(failure).__name__)
            with self.store.connect() as db:
                meeting_prep.keep(db, meeting, 'failed', None, now())
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if meeting_prep.judged(db, [meeting['key']]):
                return None
            if not found or found['area'] == 'personal':
                meeting_prep.keep(db, meeting, 'personal' if found else 'nothing', None, now())
                LOG.info('meeting prep verdict=%s', 'personal' if found else 'nothing')
                return None
            # A to-do's title can show with its project on the Team Graph and in a handoff: not worded by a turn that read
            # notes, an earlier briefing or a message from history
            title = found['title'] if found['title'] and not any(meeting['evidence'].get(k) for k in ('notes', 'recurring', 'older')) else i18n.t('Prepare for {}', meeting['title'][:70])
            body = meeting_prep.body_text(found['fields'], i18n.t, found.get('links'), self.meeting_prep_cites(meeting))
            try:
                saved = self.store.suggest(meeting['key'], title[:90], body, [meeting['id'], *found['sources']], 'now', self.config.get('digest_at', '08:30'),
                                           work=True, _db=db, expires_at=meeting['start'].isoformat(), expires_what=title[:80])
            except ValueError as error:  # not the owner's to act on, or its moment passed
                LOG.info('meeting prep skipped reason=%s', str(error)[:80])
                meeting_prep.keep(db, meeting, 'nothing', None, now())
                return None
            made = db.execute('SELECT body FROM suggestions WHERE id=?', (saved['id'],)).fetchone()
            meeting_prep.keep(db, meeting, 'made', saved['id'], now(), made['body'] if made else body, meeting['evidence'].get('searches'))
        LOG.info('meeting prep made=1')
        return saved['id']

    def meeting_prep_stale_next(self, current=None):
        """Once after an upgrade that raised meeting_prep.FORMAT: the soonest open briefing still in an older format to
        write again (meeting_prep.stale), with what it reads; None when there is none now or the day's turns are used.
        Once none is left the pass is kept as done (learning_state) and never looks again, until the next format. One whose
        replies couldn't be read (model_reply.Waiting) stays as it is after a few."""
        wait = model_reply.waiting(self, 'meeting-prep')
        if wait.resting():
            return None
        current = current or dt.datetime.fromisoformat(now())
        sides = {a['id']: graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')}
        picked = []

        def pick(db):
            emails, domains = self.meeting_prep_owner(db)
            for meeting in meeting_prep.stale(db, OPEN_NOT_SNOOZED, current, emails, domains, i18n.t):
                side = sides.get(meeting['account_id'])
                found = meeting_prep.evidence(db, meeting, side, sides, emails, domains, current, CARD_OPEN, calendar_owned, graph.resolve,
                                              person_summary.prep_lines, graph.excerpt)
                if not meeting_prep.worth_asking(found) or wait.spent(meeting['key']) or meeting['format'] == 2 and not found['notes']:
                    meeting_prep.stamp(db, meeting['key'], db.execute('SELECT body FROM suggestions WHERE id=?', (meeting['suggestion_id'],)).fetchone()[0])
                    continue  # nothing to write it from now, or nothing that format 3 adds to it: it stays as it is
                picked.append({**meeting, 'side': side, 'evidence': found})
                return None  # one at a time: the pass is done once none is left
            return []
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                if meeting_prep.judged_today(db, (current - dt.timedelta(days=1)).isoformat()) + wait.today() >= meeting_prep.PER_DAY:
                    return None
                learning_loop.run_once(db, STALE_ONCE + str(meeting_prep.FORMAT), pick)
        except sqlite3.Error as error:  # a busy database: the next pass tries again
            LOG.warning('meeting prep stale error=%s', type(error).__name__)
            return None
        return picked[0] if picked else None

    def meeting_prep_rebuild(self, meeting):
        """A briefing in an older format written again: only its body changes; title, sources, status and time stay.
        The old one stays when the turn finds nothing useful, or when meanwhile the owner changed, snoozed or closed it
        or the meeting came too close. Returns the to-do's id when written."""
        import help_chat
        try:
            found = self.meeting_prep_brief(meeting)
        except help_chat.Unavailable:
            LOG.info('meeting prep: no model now')
            return None  # not stamped: a later pass asks again
        except model_reply.Unreadable:
            return self.meeting_prep_unreadable(meeting)
        except (OSError, ValueError, TypeError) as failure:  # the turn may have run: never a second one for it
            LOG.warning('meeting prep rebuild error=%s', type(failure).__name__)
            found = None
        sid = meeting['suggestion_id']
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT body,status,title_source,outcome FROM suggestions WHERE id=?', (sid,)).fetchone()
            if not row:
                return None
            ahead = meeting['start'] - dt.datetime.fromisoformat(now()) > meeting_prep.REBUILD_LEAD
            as_left = (row['status'] in OPEN_NOT_SNOOZED and meeting_prep.body_sha(row['body']) == meeting['was']
                       and row['title_source'] == 'auto' and not row['outcome'])
            body = meeting_prep.body_text(found['fields'], i18n.t, found.get('links'), self.meeting_prep_cites(meeting)) if found and found['area'] == 'work' else ''
            if not (body and ahead and as_left):
                meeting_prep.stamp(db, meeting['key'], row['body'], now())
                LOG.info('meeting prep rebuild kept')
                return None
            self.store.briefing_rewrite(db, sid, body)
            meeting_prep.stamp(db, meeting['key'], body, now())
        LOG.info('meeting prep rebuilt=1')
        return sid

    def meeting_prep_follow(self, current=None):
        """A briefing follows its meeting: a new time moves when it closes by itself; a canceled meeting's closes now."""
        current = current or dt.datetime.fromisoformat(now())
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                for sid, start, key in meeting_prep.moved(db, CARD_OPEN, current):
                    at = (start or current).astimezone(dt.timezone.utc).isoformat(timespec='seconds')
                    self.store.move_moment(db, sid, at)
                    meeting_prep.moved_to(db, key, start or current)
        except sqlite3.OperationalError as error:
            LOG.warning('meeting prep follow error=%s', type(error).__name__)
        self.store.expire_passed()
