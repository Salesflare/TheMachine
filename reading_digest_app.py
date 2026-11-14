"""Daily digest, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The Daily digest template's own run (digest_template_run, from mail_cleanup_app.routine_template_run): plain code finds
the candidates (reading_digest.candidates); none ends the run as nothing new, without a model. Else one small model call
reads only them (digest_pass: the background model, no agent, no tools), once the usage budget allows like any
background turn, within the day's rough input cap (reading_digest.fit). Its picks become one to-do per area (a Work
to-do never lists personal mail), quiet like the cleanup to-dos: it waits in the list and the morning summary, no buzz.
A new digest replaces the area's open one. A test run only shows its picks.

On the to-do: More like this or Less like this per item (digest_feedback). On the routine's card: the interests the
owner sees and edits (digest_interest). Nothing is sent to anyone and no mail changes: the digest only reads."""
import datetime as dt
import logging

import help_chat
import i18n
import reading_digest
import routines
import todo_areas
from machine.store import outcomes
from models import background_model
from machine import todo_states
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
DIGEST_TIMEOUT = 120  # seconds the model call may take
FAVORITES = 5
WORK = 8  # open projects named as what the owner works on


class ReadingDigestApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'digest_feedback': 'digest_feedback_action',
        'digest_interest': 'digest_interest_action',
    }

    # --- the owner's taps ----------------------------------------------------------------------------------------

    def digest_feedback_action(self, name, args, owner_dashboard):
        """More like this or Less like this on a digest's item (feedback: more, less, or none to take it back)."""
        if not owner_dashboard:
            raise OwnerError('Only the owner says this, on the dashboard')
        value = args.get('feedback') or None
        try:
            n = int(args.get('item'))
        except (TypeError, ValueError):
            raise OwnerError(i18n.t('That item is gone')) from None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            reading_digest.ensure(db)
            reading_digest.feedback(db, str(args.get('suggestion_id') or ''), n, value, self.routines_stamp())
            return {'saved': True, 'interests': reading_digest.interests(db)}

    def digest_interest_action(self, name, args, owner_dashboard):
        """Add a topic to More of or Less of (kind), or take one off (remove)."""
        if not owner_dashboard:
            raise OwnerError('Only the owner changes this, on the dashboard')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            reading_digest.ensure(db)
            if args.get('remove'):
                reading_digest.drop_interest(db, args.get('topic'))
            elif not reading_digest.set_interest(db, args.get('topic'), args.get('kind') or 'more', 'owner', self.routines_stamp()):
                raise OwnerError(i18n.t('Type a topic of a few words'))
            return {'saved': True, 'interests': reading_digest.interests(db)}

    def digest_interests(self):
        """The list, for the routine's card (routines_view)."""
        with self.store.connect() as db:
            reading_digest.ensure(db)
            return reading_digest.interests(db)

    # --- a run -----------------------------------------------------------------------------------------------------

    def digest_template_run(self, run):
        """The Daily digest's run (routine_template_run): always done here, never an agent turn (True). No candidates:
        nothing new at once, no model. Else the model call in a thread of its own once the usage budget allows."""
        if run['id'] in self.__dict__.get('_routine_steps', ()):
            return True  # its pass is running
        accounts = [a['id'] for a in self.cleanup_accounts()]
        with self.store.connect() as db:
            reading_digest.ensure(db)
            since = self.cleanup_since(db, run['routine_id'])
            known = reading_digest.habits(db, accounts, dt.datetime.now(dt.timezone.utc))
            found = reading_digest.candidates(db, accounts, since, known)
        if not found:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                routines.report(db, run['id'], nothing=True, why=i18n.t('No new newsletters'), stamp=self.routines_stamp())
            return True
        now_run = str(run['period']).startswith(('now:', 'test:'))  # the owner pressed it: only the usage limit holds it
        if self.background_pause(owner=now_run, job='routine') or not (now_run or self.background_spaced()):
            return True  # a next step
        self.background_started()
        self.routine_spawn(lambda _: self.digest_pass(run, found, known), run['id'])
        return True

    def digest_context(self, db, known):
        """What the owner works on (open projects) and the newsletters they open most, for the model."""
        try:
            work = [r[0] for r in db.execute('SELECT name FROM projects WHERE closed_at IS NULL ORDER BY created_at DESC LIMIT ?', (WORK,))]
        except Exception:  # a database before projects
            work = []
        best = sorted(((reading_digest.score(h), a) for a, h in known.items() if h['n'] >= 2 and reading_digest.score(h) > 0.5), reverse=True)
        names = [a.partition('@')[2] or a for _, a in best[:FAVORITES]]
        return [' '.join(str(w).split())[:60] for w in work], names

    def digest_pass(self, run, found, known):
        """The one model call over the candidates; its picks, only from them, become the to-dos after the run is settled.
        None picked: nothing new, no to-do. A reply that isn't one: didn't work, and the next run reads the mail again."""
        day = dt.datetime.now(dt.timezone.utc).date().isoformat()
        with self.store.connect() as db:
            likes = reading_digest.interests(db)
            work, favorites = self.digest_context(db, known)
            seed = not likes['more'] and not likes['less']
            prompt, found = reading_digest.fit(db, day, found, likes, work, favorites, seed)
            if prompt:
                reading_digest.spend(db, day, reading_digest.tokens(prompt) + reading_digest.REPLY_TOKENS)
        stamp = self.routines_stamp()
        if not prompt:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                routines.report(db, run['id'], nothing=True, why=i18n.t('Today’s reading budget is used up. The next run reads them.'), stamp=stamp)
            return
        ask = getattr(self, 'digest_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                text = ask(prompt)
            else:
                model = background_model(self.config)
                text = help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=DIGEST_TIMEOUT)
        except help_chat.Unavailable:
            text = None
        answer = reading_digest.reply(text)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if answer is None:
                routines.finish(db, run['id'], 'failed', stamp, error='no_result' if text else 'runtime_error')
                return
            if seed and not routines.is_test(run):
                for topic in reading_digest.seeded(answer):
                    reading_digest.set_interest(db, topic, 'more', 'learned', stamp)
            picks = reading_digest.picked(found, answer)
            if not picks:
                routines.report(db, run['id'], nothing=True, why=i18n.t('Nothing stood out today'), stamp=stamp)
            elif routines.is_test(run):  # Try it: the picks as its result, no to-do
                routines.report(db, run['id'], text='\n'.join(f'- **{p["from"]}**: {p["title"]}. {p["why"]}' for p in picks), stamp=stamp)
            else:
                routines.report(db, run['id'], text=i18n.t('Read {} newsletters, picked {}.', len(found), len(picks)), stamp=stamp)
        if picks and not routines.is_test(run):
            missed = self.digest_todos(run, picks)
            if missed:
                with self.store.connect() as db:
                    routines.restate(db, run['id'], 'failed', i18n.t('Couldn’t make the to-do. The next run tries again.'))

    def digest_todos(self, run, picks):
        """One to-do per area with its picks; the area's open digest is done (one at a time). Returns how many picks
        are on none."""
        areas, missed = {}, 0
        for item in picks:
            account = self.cleanup_account(item['account'])
            area = todo_areas.area_of_account(account) if account else None
            if area:
                areas.setdefault(area, (account, []))[1].append(item)
            else:
                missed += 1
        companies = todo_areas.companies(self.config.get('accounts', []))
        for area, (account, mine) in areas.items():
            title = i18n.t('Daily digest: {} worth reading', len(mine))
            text = '\n'.join([i18n.t('Picked from your newsletters for what you care about.'), ''] +
                             [f'- {i["from"]}: {i["title"]}. {i["why"]}'[:200] for i in mine])[:700]
            source = f'routine-digest:{run["id"]}:{area}'
            with self.store.connect() as db:
                older = reading_digest.open_todos(db, area)
            event_id = self.store.reviewed_event(account['id'], source, reading_digest.KIND, title, text,
                                                 {'sender_display': run.get('name') or i18n.t('Daily digest'), 'routine': run['routine_id'],
                                                  'digest': True, 'items': mine})
            try:
                sid = self.store.suggest(source, title, text, [event_id], when='now', company=area if area in companies else None,
                                         work=area != todo_areas.PERSONAL)['id']
            except ValueError as error:
                LOG.warning('digest to-do not saved items=%d error=%s', len(mine), type(error).__name__)
                missed += len(mine)
                continue
            with self.store.connect() as db:
                reading_digest.ensure(db)
                reading_digest.record(db, sid, mine, self.routines_stamp())
                # the area's older digest closes by itself, not as the owner's Done: "Closed by itself: newer digest", with Undo
                reason, stamp = i18n.t('newer digest'), self.routines_stamp()
                for old in older:
                    row = db.execute(f"SELECT * FROM suggestions WHERE id=? AND status NOT IN {todo_states.sql(todo_states.CLOSED)}", (old,)).fetchone()
                    if old == sid or not row or db.execute('SELECT 1 FROM decisions WHERE id=?', ('digest-replaced:' + old,)).fetchone():
                        continue
                    outcomes.close_replaced(db, row, 'digest-replaced:' + old, reason, stamp)
        return missed
