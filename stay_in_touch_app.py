"""Stay in touch, the App's part: its routine template (routine_templates.Template), listed in machine/main.py's
ROUTINE_TEMPLATES (docs/code-map.md).

Its run (run, from routines_app.routine_template_run): plain code shortlists the people due a nudge (stay_in_touch.py);
none ends the run as nothing to say, without a model. Else one small model call (touch_pass: the background model, no
agent, no tools) reads only them and names one specific reason per person, or none, or a day to look again when
what they shared is still ahead (stay_in_touch.later). Each reason becomes one quiet,
Personal to-do on the channel the owner usually writes to them on off their Work accounts (one of those only when
there is no other), prepared ahead: the draft is written in that
conversation, so in their language and the owner's voice, and nothing is sent until the owner sends it. It never
notifies by itself and is never shared with a Work Fleet. A nudge left alone lapses after a week. A test run only
shows its reasons.

On the routine's card: who is in it and a short list of the owner's close people to add (touch_people)."""
import datetime as dt
import json
import logging

import graph
import help_chat
import i18n
import routine_templates
import routines
import stay_in_touch
from machine.owner_error import OwnerError
from models import background_model
import timeutil

LOG = logging.getLogger('personal-assistant')
TOUCH_TIMEOUT = 90  # seconds the model call may take


class StayInTouch(routine_templates.Template):
    KEYS = ('touch',)
    ACTIONS = {'touch_people': 'touch_people_action'}  # its nudges are ordinary to-dos

    def touch_people_action(self, name, args, owner_dashboard):
        """Add someone from the suggested list (add: their node id), or take someone out (remove)."""
        if not owner_dashboard:
            raise OwnerError('Only the owner changes this, on the dashboard')
        now = timeutil.clock()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            stay_in_touch.ensure(db)
            if args.get('remove'):
                stay_in_touch.remove(db, str(args['remove']))
            else:
                node = str(args.get('add') or '')
                row = db.execute('SELECT info FROM graph_nodes WHERE id=? AND kind=?', (node, 'person')).fetchone()
                if not row or not stay_in_touch.close(json.loads(row['info'] or '{}'),
                                                      stay_in_touch.exchanges(db, node, now, self.store.owner_user_ids)):
                    raise OwnerError(i18n.t('Only people you write with often can be added'))
                stay_in_touch.add(db, node, self.routines_stamp())
            return {'saved': True, 'touch': self.touch_view(db, now)}

    def touch_view(self, db=None, now=None):
        """Who is in it and who to add, for the routine's card (routines_view)."""
        if db is None:
            with self.store.connect() as db:
                return self.touch_view(db, now)
        stay_in_touch.ensure(db)
        now = now or timeutil.clock()
        return {'people': [{'id': p['id'], 'name': p['name']} for p in stay_in_touch.people(db)],
                'suggested': stay_in_touch.suggested(db, now, self.store.owner_user_ids)}

    # --- a run -----------------------------------------------------------------------------------------------------

    def run(self, run, key):
        """A Stay in touch run (routine_template_run): always done here, never an agent turn (True). Nobody due: nothing
        to say at once, no model. Else the model call in a thread of its own once the usage budget allows."""
        if run['id'] in self.app.__dict__.get('_routine_steps', ()):
            return True  # its pass is running
        now = timeutil.clock()
        with self.store.connect() as db:
            stay_in_touch.ensure(db)
            anyone = bool(stay_in_touch.people(db))
            work = {a['id'] for a in self.config.get('accounts', []) if a.get('id') and graph.account_side(a) == 'work'}
            picked = stay_in_touch.shortlist(db, now, self.store.owner_user_ids, work=work) if anyone else []
        if not picked:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                why = i18n.t('Nothing specific to say to anyone today') if anyone else i18n.t('No one picked yet')
                routines.report(db, run['id'], nothing=True, why=why, stamp=self.routines_stamp())
            return True
        now_run = str(run['period']).startswith(('now:', 'test:'))  # the owner pressed it: only the usage limit holds it
        if self.background_pause(owner=now_run, job='routine') or not (now_run or self.background_spaced()):
            return True  # a next step
        self.background_started()
        self.routine_spawn(lambda _: self.touch_pass(run, picked), run['id'])
        return True

    def touch_pass(self, run, picked):
        """The one model call over the shortlisted people; its reasons become the nudges. None: nothing to say, no to-do.
        A reply that isn't one: didn't work, and the next run reads them again."""
        ask = getattr(self, 'touch_model', None)  # tests and the sandbox: (prompt) -> reply
        prompt = stay_in_touch.prompt(picked, i18n.language_name())
        try:
            if ask:
                text = ask(prompt)
            else:
                model = background_model(self.config)
                text = help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=TOUCH_TIMEOUT)
        except help_chat.Unavailable:
            text = None
        found = stay_in_touch.reply(text, picked)
        stamp, test = self.routines_stamp(), routines.is_test(run)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if found is None:
                routines.finish(db, run['id'], 'failed', stamp, error='no_result' if text else 'runtime_error')
                return
            if not test:  # read: the same material isn't read again for a while, or till the day the model named
                again = stay_in_touch.later(text, picked, timeutil.local_day(timeutil.clock()))
                for person in picked:
                    stay_in_touch.asked(db, person['kept'], person['key'], stamp, again.get(person['kept']))
            if not found:
                routines.report(db, run['id'], nothing=True, why=i18n.t('Nothing specific to say to anyone today'), stamp=stamp)
            elif test:  # Try it: the reasons as its result, no to-do
                routines.report(db, run['id'], text='\n'.join(f"- **{p['name']}**: {why}" for p, why in found), stamp=stamp)
        if found and not test:
            made = [p['name'] for p, why in found if self.touch_todo(p, why)]
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                if made:
                    routines.report(db, run['id'], text=i18n.t('Check in with {}.', ', '.join(made)), stamp=self.routines_stamp())
                else:
                    routines.finish(db, run['id'], 'failed', self.routines_stamp(), error='no_result')

    def touch_todo(self, person, why):
        """One person's nudge, on their usual channel, prepared ahead and quiet; its id, or None when it couldn't be made."""
        day = timeutil.clock().date()
        name = person['name']
        body = why + '\n\n' + i18n.t('Last in touch {} weeks ago.', max(1, person['days'] // 7))
        try:
            saved = self.store.suggest(f"{stay_in_touch.KEY}{person['id']}:{day.isoformat()}", i18n.t('Check in with {}', name)[:90], body,
                                       [person['event_id']], 'now', personal=True, ahead=True, quiet=True, owner_step=False,
                                       expires_at=(day + dt.timedelta(days=stay_in_touch.EXPIRES_DAYS)).isoformat(),
                                       expires_what=i18n.t('the check-in with {}', name)[:80])
        except ValueError as error:
            LOG.info('stay in touch to-do not saved error=%s', type(error).__name__)
            return None
        return saved['id']
