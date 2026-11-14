"""Second-hand finds, the App's part: its routine template (routine_templates.Template), listed in machine/main.py's
ROUTINE_TEMPLATES (docs/code-map.md). The plain-code part is secondhand.py.

Added from its template card with a search page and optional filters (setup_of, setup_save): one routine per search,
every 3 hours. Its own run (run, from routines_app.routine_template_run), in a thread of its own once the usage budget
allows, like the Daily digest:
1. Under the shared browser lease (the Facebook import's), the search page in a tab of its own behind the owner's, read
   and closed; then each new listing that passes the filters code can check, LISTINGS_PER_RUN at most and PACE apart.
   The lease ends before any model call.
2. Per listing, one small model call (secondhand_check): its first photo (OpenClaw's image routing, as WhatsApp photos)
   with its text and seller lines, or the text alone. Never more than the day's DAY_CHECKS across all searches.
3. The ones it keeps, with a verdict that says something, in one to-do (secondhand_todo). None: nothing new, no to-do.

A login, captcha or bot check on the search is the owner's: one to-do says why with Open (secondhand_open: that tab,
left open, in front in The Machine's browser), and the run didn't work. A later read that works closes it by itself.

Its first run takes stock: the first few listings that pass are judged, the rest of the page is remembered as there
before (secondhand.mark 'base'), so it never brings old listings as new. A test run (Try it) reads and judges the same
but keeps nothing: no to-do, nothing remembered.

An edited one (the owner changed its words) runs as a normal routine on them, told its search page and filters
(secondhand_lines). It only reads: no message to a seller, no bid, no buy."""
import contextlib
import json
import logging
import secrets
import subprocess
import sys
import urllib.request

import browser_login
import help_chat
import i18n
import models
import routine_templates
import routines
import secondhand
import todo_areas
import timeutil
import whatsapp_images
from machine.browser import browser_lease_script, browser_link
from machine.owner_error import OwnerError
from machine.store import outcomes
from machine import todo_states

LOG = logging.getLogger('personal-assistant')
CHECK_TIMEOUT = 120  # seconds one listing's model call may take
LEASE_MINUTES = 10  # the search and LISTINGS_PER_RUN pages, PACE apart, fit well inside
# What its to-do and the run say when the site stopped the read (secondhand.WALLS)
WALL_TEXT = {
    'login': 'The site asks you to sign in. Open it in The Machine’s browser and sign in there. The next run reads it again.',
    'captcha': 'The site shows a robot check. Open it in The Machine’s browser and do it there. The next run reads it again.',
    'blocked': 'The site stopped the read. Open it in The Machine’s browser to see why. The next run tries again.',
}


class SecondhandTemplate(routine_templates.Template):
    KEYS = ('secondhand',)
    KIND = 'secondhand'
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'secondhand_search': 'secondhand_search_action', 'secondhand_open': 'secondhand_open_action'}
    PACE = secondhand.PACE  # tests: None (no wait between pages)

    # --- the owner's setup ----------------------------------------------------------------------------------------

    def setup_of(self, args):
        """The template card's setup, checked: {url, filters, name}. OwnerError says what is wrong."""
        url = secondhand.address(args.get('url'))
        filters = ' '.join(str(args.get('filters') or '').split())[:secondhand.FILTERS_MAX]
        return {'url': url, 'filters': filters, 'name': self.secondhand_name(url)}

    def setup_save(self, db, routine_id, made, stamp):
        secondhand.set_search(db, routine_id, made['url'], made['filters'], stamp)

    @staticmethod
    def secondhand_name(url):
        return i18n.t('Second-hand: {}', secondhand.search_name(url))[:routines.NAME_MAX]

    def secondhand_search_action(self, name, args, owner_dashboard):
        """Change search on its routine's card: a new search page or filters (id, url, filters). A name it made from the
        old address follows the new one; one the owner gave stays."""
        if not owner_dashboard:
            raise OwnerError('Only the owner changes a search, on the dashboard')
        made = self.setup_of(args)
        stamp = self.routines_stamp()
        with self.routines_lock(), self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = routines.get(db, args.get('id'), routines.LIVE)
            if routine_templates.key_of(row['origin']) != 'secondhand':
                raise OwnerError('That routine isn’t a second-hand search')
            old = secondhand.search(db, row['id'])
            secondhand.set_search(db, row['id'], made['url'], made['filters'], stamp)
            if old and row['name'] == self.secondhand_name(old['url']) and row['name_check'] != routines.OWNER_NAMED:
                routines.retitle(db, row['id'], made['name'], stamp)
        return self.routines_view(row['id'])

    def secondhand_view(self, routine_id):
        """The search on its routine's card: {url, name, site, filters}."""
        with self.store.connect() as db:
            found = secondhand.search(db, routine_id)
        return {k: found[k] for k in ('url', 'name', 'site', 'filters')} if found else None

    def secondhand_lines(self, run):
        """For an edited one's turn: the search page and filters its words are about. '' for any other routine."""
        with self.store.connect() as db:
            origin = db.execute('SELECT origin FROM routines WHERE id=?', (run['routine_id'],)).fetchone()
            found = origin and routine_templates.key_of(origin[0]) == 'secondhand' and secondhand.search(db, run['routine_id'])
        if not found:
            return ''
        return (f'The owner\'s second-hand search page: {found["url"]}. Their filters: {found["filters"] or "none"}. Open it in the '
                'browser and read it; a login, captcha or robot check there is the owner\'s: say so, never solve it. Never contact '
                'a seller, bid, buy or message.')

    # --- Open on a to-do whose search was stopped -----------------------------------------------------------------

    def secondhand_open_action(self, name, args, owner_dashboard):
        """Open: the search page in front in The Machine's browser (the tab the read left open on the wall, else the
        address again), for the owner to sign in or pass the check there themselves. {shown, view}."""
        if not owner_dashboard:
            raise OwnerError('Only the owner opens the browser, from the dashboard')
        with self.store.connect() as db:
            secondhand.ensure(db)
            row = db.execute('SELECT routine_id FROM secondhand_todos WHERE suggestion_id=?', (str(args.get('suggestion_id') or ''),)).fetchone()
            found = row and secondhand.search(db, row[0])
        if not found:
            raise OwnerError('That search is gone')
        view, base = browser_link(self.config), self.secondhand_base()
        if not base:
            return {'shown': False, 'view': view, 'error': i18n.t('The Machine’s browser isn’t available right now.')}
        cdp = secondhand.browser_cdp
        try:
            tabs = {t.get('id'): t for t in cdp._http(base, '/json/list', timeout=10) if t.get('type') == 'page'}
            target = found['tab'] if found['tab'] in tabs else cdp.open_tab(base, found['url'])
            cdp._http(base, '/json/activate/' + target, timeout=10)
        except (cdp.CdpError, OSError, TypeError, AttributeError):
            return {'shown': False, 'view': view, 'error': i18n.t('The Machine’s browser isn’t available right now.')}
        with self.store.connect() as db:
            secondhand.set_tab(db, row[0], target)
        try:
            import browser_viewer
            browser_viewer.raise_window(base)
        except Exception:  # noqa: BLE001 - a window that can't be raised is still in front in the viewer
            pass
        return {'shown': True, 'view': view}

    # --- a run -----------------------------------------------------------------------------------------------------

    def run(self, run, key):
        """A run (routine_template_run): always done here, never an agent turn (True). The read and the checks in a
        thread of their own, once the usage budget allows like any background turn."""
        if run['id'] in self.app.__dict__.get('_routine_steps', ()):
            return True  # its pass is running
        now_run = str(run['period']).startswith(('now:', 'test:'))  # the owner pressed it: only the usage limit holds it
        if self.background_pause(owner=now_run, job='routine') or not (now_run or self.background_spaced()):
            return True  # a next step
        self.background_started()
        self.routine_spawn(lambda _: self.secondhand_pass(run), run['id'])
        return True

    def secondhand_base(self):
        """The shared browser's DevTools address when it answers, else None."""
        base = (browser_login.endpoints(self.config) or [None])[0]
        if not base:
            return None
        try:
            urllib.request.urlopen(base + '/json/version', timeout=5).close()
        except (OSError, ValueError):
            return None
        return base

    @contextlib.contextmanager
    def secondhand_lease(self):
        """The shared browser lease (integrations/browser-lease.py) for one run's reads: True while held, False when
        another reader has the browser."""
        owner = 'secondhand-' + secrets.token_hex(6)
        lease = [sys.executable, str(browser_lease_script(self.config))]
        claim = subprocess.run([*lease, 'claim', '--owner', owner, '--minutes', str(LEASE_MINUTES), '--wait', '1'],
                               capture_output=True, text=True, timeout=90)
        try:
            yield claim.returncode == 0
        finally:
            if claim.returncode == 0:
                try:
                    subprocess.run([*lease, 'release', '--owner', owner], capture_output=True, text=True, timeout=30)
                except (OSError, subprocess.SubprocessError):
                    pass  # the lease runs out by itself

    def secondhand_end(self, run, state, why=None, text=None, error=None):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if state == 'failed':
                routines.finish(db, run['id'], 'failed', self.routines_stamp(), why=why, error=error)
            else:
                routines.report(db, run['id'], text=text, nothing=state == 'nothing', why=why, stamp=self.routines_stamp())

    def secondhand_pass(self, run):
        """One run: read, filter, open, check, then at most one to-do. Whatever goes wrong, the run says so."""
        try:
            self.secondhand_read(run)
        except Exception as error:  # noqa: BLE001 - the run says it didn't work; the next one tries again
            LOG.info('second-hand run failed error=%s', type(error).__name__)
            self.secondhand_end(run, 'failed', error='runtime_error')

    def secondhand_read(self, run):
        rid, test = run['routine_id'], routines.is_test(run)
        stamp, day = self.routines_stamp(), timeutil.clock().date().isoformat()
        with self.store.connect() as db:
            found = secondhand.search(db, rid)
            known = secondhand.seen(db, rid) if found else {}
            left = secondhand.checks_left(db, day)
        if not found:
            return self.secondhand_end(run, 'failed', error='secondhand_setup')
        f = secondhand.filters(found['filters'])
        base = self.secondhand_base()
        if not base:
            return self.secondhand_end(run, 'failed', error='secondhand_browser')
        pages, broken = [], []
        with self.secondhand_lease() as held:
            if not held:
                return self.secondhand_end(run, 'failed', error='secondhand_busy')
            if found['tab']:  # a tab a wall left open last time: the owner had their look
                try:
                    secondhand.browser_cdp.close_tab(base, found['tab'])
                except secondhand.browser_cdp.CdpError:
                    pass
            got = secondhand.read_search(base, found['url'])
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                secondhand.set_tab(db, rid, got.get('tab'))
                if not got['wall']:
                    secondhand.read_done(db, rid, stamp)
            if got['wall']:
                if not test:
                    self.secondhand_blocked(run, found, got['wall'])
                return self.secondhand_end(run, 'failed', error='secondhand_' + got['wall'])
            listings = got['listings']
            if not listings:
                return self.secondhand_end(run, 'nothing', why=i18n.t('No listings on the search page'))
            fresh = [x for x in listings if x['url'] not in known]
            dropped = [x['url'] for x in fresh if secondhand.cheap(x, f)]
            passing = [x for x in fresh if x['url'] not in dropped]
            take = passing[:min(secondhand.LISTINGS_PER_RUN, left)]
            waiting = len(passing) - len(take)
            # The first run takes stock: what the page has beyond the few it judges was there before
            stock = [x['url'] for x in passing[len(take):]] if not known else []
            for n, item in enumerate(take):
                secondhand.pause(self.PACE)  # after the search page too: a person's pace, never a burst
                try:
                    page = secondhand.read_listing(base, item['url'])
                except secondhand.browser_cdp.CdpError:
                    broken.append(item['url'])
                    continue
                if page['wall']:  # the site stopped in between: the rest waits for the next run
                    waiting += len(take) - n
                    break
                merged = {**item, **{k: v for k, v in page.items() if v not in (None, '', [])}, 'image': item.get('image')}
                if secondhand.cheap(merged, f):
                    dropped.append(item['url'])
                else:
                    pages.append(merged)
        self.secondhand_after(run, found, f, listings, fresh, dropped, pages, broken, stock, waiting, left, day)

    def secondhand_after(self, run, found, f, listings, fresh, dropped, pages, broken, stock, waiting, left, day):
        """The checks, after the browser is free again; then what is remembered, the to-do and the run's result."""
        rid, test, stamp = run['routine_id'], routines.is_test(run), self.routines_stamp()
        finds, judged, unanswered = [], [], 0
        for item in pages:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                secondhand.spend(db, day)
            said = self.secondhand_check(item, f)
            if said is None:
                unanswered += 1  # not remembered: the next run asks again
                continue
            keep, verdict = said
            judged.append(item['url'])
            if keep and verdict:
                finds.append({'title': item.get('title') or '', 'price': item.get('price'), 'price_text': secondhand.price_text(item),
                              'verdict': verdict, 'photo': (item.get('photos') or [item.get('image')])[0] or item.get('image') or None,
                              'url': item['url']})
        if not test:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                secondhand.mark(db, rid, dropped, 'filter', stamp)
                secondhand.mark(db, rid, broken, 'checked', stamp)
                secondhand.mark(db, rid, [u for u in judged if u not in {x['url'] for x in finds}], 'checked', stamp)
                secondhand.mark(db, rid, [x['url'] for x in finds], 'shown', stamp)
                secondhand.mark(db, rid, stock, 'base', stamp)
            self.secondhand_unblocked(rid)
        if pages and unanswered == len(pages):
            return self.secondhand_end(run, 'failed', error='no_result')
        if not finds:
            why = (i18n.t('Today’s check limit is reached. The rest waits for tomorrow.') if waiting and not left
                   else i18n.t('No new listings') if not fresh else i18n.t('Nothing new passed the filters and checks'))
            return self.secondhand_end(run, 'nothing', why=why)
        finds = finds[:secondhand.SHOWN_MAX]
        lines = [f'- **{x["title"]}**' + (f' · {x["price_text"]}' if x['price_text'] else '') + f': {x["verdict"]}' for x in finds]
        text = '\n'.join([i18n.t('Read {} listings: {} new, {} worth a look.', len(listings), len(fresh), len(finds))] + ([] if not test else lines))
        if not test:
            if not self.secondhand_todo(run, found, finds):
                return self.secondhand_end(run, 'failed', why=i18n.t('Couldn’t make the to-do. The next run tries again.'))
        self.secondhand_end(run, 'ready', text=text)

    def secondhand_check(self, item, f):
        """One listing's check, one small model call: (keep, verdict), or None when the model didn't answer. Its first
        photo goes with it when there is one this can read (OpenClaw's image routing first, then the background model,
        as WhatsApp photos); else the text alone."""
        ask = getattr(self, 'secondhand_model', None)  # tests and the sandbox: (prompt, photo bytes or None) -> reply
        pic = None
        for url in [*(item.get('photos') or []), item.get('image')][:2]:
            if url:
                pic = (getattr(self, 'secondhand_photo', None) or secondhand.photo)(url)
                if pic:
                    break
        prompt = secondhand.check_prompt(item, f['text'], bool(pic))
        try:
            if ask:
                text = ask(prompt, pic[0] if pic else None)
            elif pic:
                text = self.secondhand_photo_ask(prompt, *pic)
            else:
                model = models.background_model(self.config)
                text = help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=CHECK_TIMEOUT)
        except help_chat.Unavailable:
            text = None
        return secondhand.check_reply(text) if text else None

    def secondhand_photo_ask(self, prompt, data, ext):
        """The prompt with one photo (`openclaw infer image describe`): the reply's text, or None. The photo's copy lives
        in a private folder only while the model reads it."""
        folder = whatsapp_images.private_dir(self.config)
        try:
            path = folder / ('listing.' + ext)
            path.write_bytes(data)
            path.chmod(0o600)
            swap = models.background_model(self.config)
            fallback = '/'.join(swap) if swap else models.openclaw_model(self.config)
            for model in (None, fallback) if fallback else (None,):
                command = [str(self.config.get('openclaw') or 'openclaw'), 'infer', 'image', 'describe', '--file', str(path),
                           '--prompt', prompt, '--timeout-ms', str(CHECK_TIMEOUT * 1000), '--json', *(['--model', model] if model else [])]
                try:
                    done = subprocess.run(command, capture_output=True, text=True, timeout=CHECK_TIMEOUT + 30)
                    answer = json.loads(done.stdout)
                except (OSError, ValueError, subprocess.TimeoutExpired):
                    continue
                outputs = answer.get('outputs') if isinstance(answer, dict) and answer.get('ok') else None
                said = '\n'.join(str(o.get('text') or '').strip() for o in outputs or [] if isinstance(o, dict)).strip()
                if said:
                    return said
            return None
        finally:
            whatsapp_images.drop(folder)

    # --- its to-dos ------------------------------------------------------------------------------------------------

    def secondhand_account(self, rid):
        """The account its to-dos go on: a personal one unless the routine is Work (routines.work)."""
        with self.store.connect() as db:
            row = db.execute('SELECT work FROM routines WHERE id=?', (rid,)).fetchone()
        work = bool(row and row['work'])
        accounts = self.config.get('accounts', [])
        want = (lambda a: todo_areas.area_of_account(a) not in (None, todo_areas.PERSONAL)) if work else \
            (lambda a: todo_areas.area_of_account(a) == todo_areas.PERSONAL)
        return next((a for a in accounts if want(a)), None) or next((a for a in accounts if todo_areas.area_of_account(a)), None), work

    def secondhand_todo(self, run, found, finds):
        """One to-do with this run's finds. Returns its id, or None."""
        account, work = self.secondhand_account(run['routine_id'])
        if not account:
            return None
        title = i18n.t('{} finds for {}', len(finds), found['name'])  # en.json: one and other
        text = '\n'.join(f'- {x["title"]}' + (f' ({x["price_text"]})' if x['price_text'] else '') + f': {x["verdict"]} {x["url"]}' for x in finds)[:3000]
        source = f'routine-secondhand:{run["id"]}'
        event_id = self.store.reviewed_event(account['id'], source, secondhand.KIND, title, text,
                                             {'sender_display': run.get('name') or i18n.t('Second-hand finds'), 'routine': run['routine_id'],
                                              'secondhand': True, 'search': found['name'], 'site': found['site'], 'url': found['url'], 'items': finds})
        try:
            sid = self.store.suggest(source, title, text, [event_id], when='now', work=work, personal=not work)['id']
        except ValueError as error:
            LOG.warning('second-hand to-do not saved items=%d error=%s', len(finds), type(error).__name__)
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            secondhand.record(db, sid, run['routine_id'], 'finds', self.routines_stamp())
        return sid

    def secondhand_blocked(self, run, found, wall):
        """The to-do that says the site stopped the read, once while it stays open."""
        with self.store.connect() as db:
            if secondhand.open_blocked(db, run['routine_id']):
                return None
        account, work = self.secondhand_account(run['routine_id'])
        if not account:
            return None
        title = i18n.t('{} stopped the search for {}', found['site'], found['name'])
        text = i18n.t(WALL_TEXT[wall])
        source = f'routine-secondhand-blocked:{run["id"]}'
        event_id = self.store.reviewed_event(account['id'], source, secondhand.KIND, title, text,
                                             {'sender_display': run.get('name') or i18n.t('Second-hand finds'), 'routine': run['routine_id'],
                                              'secondhand': True, 'blocked': wall, 'search': found['name'], 'site': found['site'], 'url': found['url']})
        try:
            sid = self.store.suggest(source, title, text, [event_id], when='now', work=work, personal=not work, owner_step=True)['id']
        except ValueError as error:
            LOG.info('second-hand blocked to-do not saved error=%s', type(error).__name__)
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            secondhand.record(db, sid, run['routine_id'], 'blocked', self.routines_stamp())
        return sid

    def secondhand_unblocked(self, rid):
        """A read that worked: its open blocked to-do closes by itself ("Closed by itself: it reads again"), with Undo."""
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = secondhand.open_blocked(db, rid)
            if row and row['status'] not in todo_states.CLOSED:
                outcomes.close_replaced(db, row, 'secondhand-unblocked:' + row['id'], i18n.t('the search reads again'), self.routines_stamp())
