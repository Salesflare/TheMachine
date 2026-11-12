"""The service's background workers and their steps that aren't one feature's own: retention, embeddings, enrichment,
the spacing of background work, Help topics and error reports sent to the control plane, message protection at a
start and the restart that waits for it, and stopping them all. Moved out of assistant.App as is. A mixin of
assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import threading
import time

import abilities
import chat_files
import embeddings
import enrichment
import error_feed
import fact_ties
import help_chat
import help_topics
import linkedin_connections
from machine.config import LOG
from machine.faults import restart_self
from machine.sources.calendar import calendar_owned
from machine.sources.exclusions import default_exclusions
from machine.sources.telegram import telegram_photo_asker
from machine.sources.whatsapp import whatsapp_photo_asker
from machine.store import plain_keys
from machine.store.review import bulk_kind
import message_seal
from models import background_model
import next_actions
import retention
from sources import credential, gog_read, SourceError
import team_learnings
from timeutil import local_tz, now


# Contact photos from the owner's Google contacts and Workspace directory, with the scopes the gog sign-in already has
# (a hosted sign-in through the broker has no Contacts scope, so it is never asked). Read only, once a day per account.
# The owner's contacts bring their birthdays along (the same scope), for the Birthdays template (birthdays.py).
GOOGLE_PHOTO_LISTS = (
    ('people.connections.list', {'resourceName': 'people/me', 'pageSize': 1000, 'personFields': 'emailAddresses,phoneNumbers,photos,organizations,birthdays'},
     'https://www.googleapis.com/auth/contacts', 'connections'),
    ('people.listDirectoryPeople', {'pageSize': 1000, 'readMask': 'emailAddresses,phoneNumbers,photos,organizations', 'sources': 'DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'},
     'https://www.googleapis.com/auth/directory.readonly', 'people'),
    ('otherContacts.list', {'pageSize': 1000, 'readMask': 'emailAddresses,phoneNumbers,photos'},
     'https://www.googleapis.com/auth/contacts.other.readonly', 'otherContacts'))


GOOGLE_PHOTO_PAGES = 20


# Background turns beyond the first look (profile, voices, roles, organizations) start at most one per this many
# seconds, and only once the first card was shown, so the first cards come first and a new install's usage is spread
# out instead of spent in its first minutes. A draft prepared ahead is on the owner's board as Preparing, so it doesn't
# wait for this gap (2026-10-29: one waited 8 minutes behind a review's start); the usage budget still holds it.
BACKGROUND_GAP_SECONDS = 600
# How long a sent Outlook reply may take to reach Sent Items before a thread snooze counts it as an error and backs off.
SNOOZE_SENDING_GRACE = dt.timedelta(minutes=15)


def google_photo_offers(config, account, read=None, facts=None):
    """(identifiers, link, chosen) for each of the account's contacts with a real photo. A list the sign-in can't read
    is skipped. With a list as `facts`, their job title, company and phone from the same pages go there too."""
    read = read or gog_read
    offers = []
    for method, params, scope, key in GOOGLE_PHOTO_LISTS:
        token = None
        for _ in range(GOOGLE_PHOTO_PAGES):
            try:
                page = read(config, account, 'people', 'v1', method, {**params, **({'pageToken': token} if token else {})}, scope)
            except SourceError:
                break
            offers += [o for o in (enrichment.google_photo(p) for p in page.get(key) or [] if isinstance(p, dict)) if o]
            if facts is not None:
                facts += [f for p in page.get(key) or [] if isinstance(p, dict) for f in enrichment.google_facts(p)]
            token = page.get('nextPageToken')
            if not token:
                break
    return offers


def google_photo_accounts(config):
    """The owner's own Google sign-ins through gog, once per address (never one shared from a Fleet)."""
    seen = {}
    for account in config.get('accounts', []):
        if account.get('service', 'gmail') in ('gmail', 'calendar') and account.get('transport') == 'gog' and account.get('email') \
                and not account.get('shared'):
            seen.setdefault(account['email'].lower(), account)
    return list(seen.values())


# Settings the app takes from config.json while it runs (App.follow_config), so turning reviews on needs no restart:
# the hosting agent's reviews on restarted the app 44 s into a first look (2026-11-04). The hosting agent checks this
# list before it restarts the app for them.
LIVE_CONFIG = ('delivery_enabled', 'review_worker')

# A new account in config.json (a connect from the account page, the dashboard or a terminal) starts syncing in the
# running app, without a restart: the restart after a connect left a teammate's Connections page on "Can't reach your
# Machine" (2026-11-10). Only a plain addition: new accounts, and new keys (a broker's address, a credential's file)
# beside settings that stay as they were. Anything else changed, or a source with a process or store of its own, still
# restarts. The services below keep a process or store of their own that only a start sets up.
LIVE_SKIP = frozenset({'android', 'gateway', 'telegram', 'whatsapp'})


def live_additions(running, saved):
    """What config.json adds to the running config, as (new accounts, new top-level keys, new keys inside a setting),
    or None when anything else changed (an account edited or removed, a setting changed): that takes a restart."""
    if not isinstance(saved, dict) or not isinstance(saved.get('accounts'), list):
        return None
    same = lambda a, b: json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    have = {a.get('id'): a for a in running.get('accounts') or []}
    found = {a.get('id'): a for a in saved['accounts'] if isinstance(a, dict)}
    if len(found) != len(saved['accounts']) or any(i not in found or not same(a, found[i]) for i, a in have.items()):
        return None
    accounts = [a for a in saved['accounts'] if a['id'] not in have]
    if any(not isinstance(a['id'], str) or not a['id'] or a.get('service') in LIVE_SKIP for a in accounts):
        return None
    keys, inside = {}, {}
    if set(running) - set(saved) - set(LIVE_CONFIG):
        return None  # a setting removed
    for key, value in saved.items():
        if key == 'accounts' or key in LIVE_CONFIG:
            continue
        if key not in running:
            keys[key] = value
        elif isinstance(value, dict) and isinstance(running[key], dict):
            if any(k not in value or not same(v, value[k]) for k, v in running[key].items()):
                return None
            if extra := {k: v for k, v in value.items() if k not in running[key]}:
                inside[key] = extra
        elif not same(value, running[key]):
            return None
    return accounts, keys, inside


class WorkersApp:
    ACTIONS = {'accounts_follow': 'accounts_follow_action'}  # its other actions are still App.action's own branches

    def accounts_follow_action(self, name, args, owner_dashboard=False):
        """Setup (onboarding.restart_and_sync) asks the running app to take what it just saved: the accounts it reads
        now, and whether it has all of config.json (taken). Both mean no restart. Only the local API token reaches it."""
        self.follow_config()
        try:
            left = live_additions(self.config, json.loads(self.config_path.read_text()))
        except (OSError, ValueError, AttributeError, TypeError):
            left = None
        # taken: nothing in the file the running app doesn't have (an edited account, a changed setting: a restart)
        return {'accounts': [a['id'] for a in self.config.get('accounts') or []], 'taken': left is not None and not any(left)}

    def adopt_accounts(self, accounts, keys, inside):
        """New accounts start syncing now, as at a start (serve): their settings first, then a collector each."""
        for key, value in keys.items():
            self.config[key] = value
        for key, extra in inside.items():
            self.config[key].update(extra)
        for account in accounts:
            rules = (account.get('exclude') or []) + default_exclusions(self.config, account)
            if rules:
                self.store.exclusions[account['id']] = rules
            if account.get('service') == 'slack' and account.get('user_id'):
                self.store.owner_user_ids.add(account['user_id'])
            self.config['accounts'].append(account)  # the store reads the same list (App.__init__)
        self.note_connections()
        if getattr(self, 'stop', None) is None:
            return
        for account in accounts:
            threading.Thread(target=self.collector if abilities.signals_on(account) else self.ability_checker, args=(account,),
                             daemon=True).start()
        LOG.info('accounts added without a restart: %d', len(accounts))

    def plain_keys_worker(self):
        """Once after the update: the messages kept before get their routing keys in the clear (machine/store/plain_keys.py),
        in batches beside the service's own work. Waits for the message key when it is not there yet; an error is tried
        again in ten minutes. Never stops the service. It begins half a minute after the start: the start's own work
        and the first requests go first."""
        wait = 30
        while not self.stop.wait(wait):
            wait = 600
            try:
                report = plain_keys.run(self.store, self.stop)
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.error('plain keys pass error=%s', type(error).__name__)
                continue
            if report is None or report['state'] != 'waiting':
                if report and report['state'] == 'done':
                    LOG.info('Routing keys of %d kept message(s) are readable in SQL now; %d did not open and were left as they are',
                             report['changed'], report['unread'])
                return
            wait = 60

    def whats_new_team(self):
        """Whether this Machine is in a Work Fleet, so What's new may pick what only a team can use."""
        fleet = getattr(self, 'fleet', None)
        return bool(fleet and fleet.work_fleets())

    def retention_worker(self):
        """Once a day at a quiet hour: old sync history and preparation logs go, the space goes back to the disk and
        local copies of the database rotate (retention.py). Also the morning's What's new pick. Checks every ten
        minutes; never stops the service."""
        while not self.stop.wait(600):
            try:  # sign-ins older versions kept only to revoke at Google again: dropped, never revoked (mail_grants.retry)
                import mail_grants
                mail_grants.retry(self.config, due_only=True)
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.warning('sign-out retry error=%s', type(error).__name__)
            try:
                if retention.due(self.store.connect, dt.datetime.now(dt.timezone.utc), local_tz()):
                    report = retention.run(self.store.connect, str(self.store.path), local_tz=local_tz())
                    LOG.info('retention %s', json.dumps(report, sort_keys=True))
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.error('retention error=%s', type(error).__name__)
            try:  # What's new: the morning's pick from the pool, once a day (machine/store/whats_new.py)
                self.store.whats_new_pick(team=self.whats_new_team())
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.warning('whats new pick error=%s', type(error).__name__)
            try:  # files added to a chat message and never sent, and those of cards that are gone (chat_files.py)
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    chat_files.sweep(db, self.config, now())
            except Exception as error:  # noqa: BLE001 - tried again in ten minutes
                LOG.error('chat files sweep error=%s', type(error).__name__)

    def embedding_worker(self):
        """Small background passes (embed_pass): signals first, then history. Never blocks
        ingestion (no transaction spans the embedding call); failures wait and retry."""
        wait=10
        while not self.stop.wait(wait):
            try:wait=self.embed_pass(embeddings.settings(self.config))
            except Exception as error:
                LOG.error('embeddings error=%s',error if isinstance(error,embeddings.EmbeddingError) else type(error).__name__);wait=300

    def enrichment_worker(self):
        """Organization and work contact data from the configured enrichment service: a few domains (and people) every ten minutes, each
        looked up again after three months. A service error waits an hour (a day for that domain)."""
        wait = 120
        while not self.stop.wait(wait):
            try:
                if enrichment.step(self.store.connect, self.config, now(), paired=bool(getattr(self, 'fleet', None))):
                    self.graph_dirty.set()  # show the new profiles
                found = enrichment.people_step(self.store.connect, self.config, now(), paired=bool(getattr(self, 'fleet', None)), stop=self.stop.is_set)
                photos = enrichment.photos_step(self.store.connect, now())  # straight after the lookups (hosted ones too, through the agent)
                photos += enrichment.site_logos_step(self.store.connect, now())  # organizations that show no logo: their own site's
                for account in google_photo_accounts(self.config):
                    with self.store.connect() as db:
                        due = enrichment.contact_run_due(db, 'google:' + account['email'].lower(), now())
                    if due and not self.stop.is_set():
                        facts = []
                        offers = google_photo_offers(self.config, account, facts=facts)
                        with self.store.connect() as db:
                            enrichment.offer_photos(db, offers, 'google', now())
                            known = enrichment.graph_people(db)  # contacts the Machine knows, like their photos
                            found += enrichment.offer_facts(db, [(ids, f, r) for ids, f, r in facts if any(i in known for i in ids)], 'google', now())
                            enrichment.contact_run_done(db, 'google:' + account['email'].lower(), now())
                photos += enrichment.contact_photos_step(self.store.connect, now())
                wa_accounts, ask = whatsapp_photo_asker(self.config)
                if wa_accounts and not self.stop.is_set():
                    photos += enrichment.whatsapp_photos_step(self.store.connect, now(), ask, wa_accounts)
                tg_accounts, ask = telegram_photo_asker(self.config)
                if tg_accounts and not self.stop.is_set():
                    photos += enrichment.telegram_photos_step(self.store.connect, now(), ask, tg_accounts)
                found += enrichment.facts_from_signals(self.store.connect, now())  # once: facts already in stored signals
                if found or photos:
                    LOG.info('enrichment people found=%s photos=%s', found, photos)
                    self.graph_dirty.set()
                wait = 600
            except enrichment.EnrichmentError as error:
                LOG.error('enrichment error=%s', error)
                wait = 3600
            except Exception as error:
                LOG.error('enrichment error=%s', type(error).__name__)
                wait = 3600

    def linkedin_connections_worker(self):
        """LinkedIn connections' titles and companies onto the Graph's people (linkedin_connections.py): checks every
        five minutes; each account's own slow pace decides whether a page is read."""
        while not self.stop.wait(300):
            for account in linkedin_connections.accounts(self.config):
                if self.stop.is_set():
                    break
                try:
                    found = linkedin_connections.step(self.store.connect, self.config, account)
                except Exception as error:  # noqa: BLE001 - its pace waits; never stops the service
                    LOG.error('linkedin connections error=%s', type(error).__name__)
                    continue
                if found.get('error') or found.get('seen') is not None:
                    LOG.info('linkedin connections account=%s %s', account['id'], json.dumps(found, sort_keys=True))
                if found.get('changed') or found.get('noted'):
                    self.graph_dirty.set()

    def background_spaced(self):
        """At most one background turn beyond the first look per BACKGROUND_GAP_SECONDS."""
        return time.time() - getattr(self, 'background_at', 0) >= BACKGROUND_GAP_SECONDS

    def help_topics_send(self):
        """Now and then: the finished days of Help topics to the control plane (help_topics.send), when sharing is on."""
        due = getattr(self, '_help_topics_at', 0)
        if time.monotonic() < due:
            return 0
        self._help_topics_at = time.monotonic() + self.HELP_TOPICS_SECONDS
        try:
            return help_topics.send(self.store.connect, self.fleet.relay.call)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('help topics error=%s', type(error).__name__)
            return 0

    def error_reports_step(self):
        """Every ten minutes, over the Network: the errors counted since the last batch, as signatures (error_feed.py).
        The names this Machine knows are taken out once more first."""
        def names():
            with self.store.connect() as db:
                return [name for name, _ in team_learnings.known_names(db, self.config)]
        try:
            return error_feed.send(self.store.connect, self.fleet.relay.call, names)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('error reports error=%s', type(error).__name__)
            return 0

    def fact_ties_step(self):
        """Start the one-time pass that ties loose facts to who they are about, when it is due and the budget allows; it
        runs in its own thread. True when started."""
        running = getattr(self, 'fact_ties_thread', None)
        if running and running.is_alive():
            return False
        with self.store.connect() as db:
            if not fact_ties.due(db):
                return False
        if self.background_pause(job='fact-ties') or not self.background_spaced():
            return False
        self.background_started()
        self.fact_ties_thread = threading.Thread(target=self.fact_ties_run, daemon=True, name='fact-ties')
        self.fact_ties_thread.start()
        return True

    def fact_ties_run(self, ask=None):
        """The pass: what to ask in one short read, one small turn per batch outside any connection, then written together."""
        ask = ask or getattr(self, 'fact_ties_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            with self.store.connect() as db:
                state = fact_ties.prepare(db, self.store.own_config())
            model = None if ask else background_model(self.config)
            replies = []
            for batch in state['batches']:
                try:
                    replies.append(ask(batch['prompt']) if ask else help_chat.openclaw_model_run(
                        self.config, batch['prompt'], '/'.join(model) if model else None, timeout=fact_ties.TIMEOUT))
                except help_chat.Unavailable:
                    replies.append(None)
                if replies[-1] is None:
                    break
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                found = fact_ties.conclude(db, state, replies)
        except Exception as error:  # noqa: BLE001 - a pass that fails is tried again later; nothing depends on it
            LOG.info('fact ties error=%s', type(error).__name__)
            return {'error': type(error).__name__}
        LOG.info('fact ties status=%s asked=%s linked=%s', found.get('error') or 'ok', state['asked'], found.get('linked', 0))
        return found

    def style_step(self):
        """Every ten minutes: a finished profile's channel lines fill voices still empty, and a draft the owner
        answered themselves instead of sending becomes a lesson for the next drafts, and that to-do closes by itself."""
        seeded, learned = self.store.seed_voices(), self.store.learn_sent_elsewhere()
        self.store.answered_elsewhere()
        self.store.name_links_once()  # one time: facts already learned are tied to the record they name (fact_links.py)
        if self.store.contacts_once():  # one time: contact details saved as facts go on the person's record (contact_facts.py)
            self.graph_later()
        if (self.config.get('review_worker') or {}).get('enabled'):  # read how they write from their own messages, now and then
            self.store.voice_study_due()
            self.store.tune_due()  # keep learning from edits, dismissals, snoozes and chat corrections (learning_loop.py)
            self.fact_ties_step()  # one time, after the name pass: loose facts tied to who they are about (fact_ties.py)
            self.bring_in_step({'model': background_model})  # once a day at most: new lines in the owner's OpenClaw notes worth keeping (bring_in.py)
            self.notes_people_step({'model': background_model})  # facts kept from those notes: on who they are about, in the owner's words (notes_people.py)
            self.missed_work_step({'owned': calendar_owned, 'bulk': bulk_kind, 'model': background_model})  # once a week: how many reviewed signals without a to-do needed one (missed_work.py)
            if self.fleet:  # learnings go to the team over the Network: without it there is nobody to offer them to
                self.store.learnings_due()
                self.team_votes_due()  # and other Machines' learnings come to be judged, when voting is on
                self.fleet_learn_due()  # and team learnings from team conversations, in a Standard Work Fleet
        if self.fleet:
            self.learnings_auto_send()  # Send learnings automatically: a batch that couldn't get through yet
            self.help_topics_send()  # what Help was asked, as topics (help_topics.py)
            self.error_reports_step()
            self.pacing_send()  # how often background work paced, counts only (pacing.py)
        self.apply_skill_clusters()  # a Create skill tapped on Telegram
        self.summary_step()  # people's summaries, when their evidence changed (person_summary.py)
        self.about_step()  # project descriptions, when their evidence changed (project_about.py)
        if seeded or learned:
            LOG.info('style learned voices=%s replies=%s', seeded, learned)

    def expire_step(self, every=30):
        """To-dos whose moment passed close by themselves (Store.expire_passed), about every half minute; Intercom to-dos a
        teammate took (Store.close_taken_intercom) and ones that have looked done for a day (Store.close_looks_done),
        about every five minutes, the first time right after a start."""
        if time.monotonic() - self.__dict__.get('expired_swept', -every) < every:
            return
        self.expired_swept = time.monotonic()
        self.store.expire_passed()
        if time.monotonic() - self.__dict__.get('intercom_swept', -300) >= 300:  # a teammate took it: within five minutes
            self.intercom_swept = time.monotonic()
            self.store.close_taken_intercom()
            self.store.close_looks_done()

    def thread_snooze_step(self,gmail=None):
        """Archive a replied thread under a label, then return it to the inbox when due."""
        with self.store.connect() as db:
            row=db.execute("SELECT t.*,j.message_id sent_message_id FROM thread_snoozes t LEFT JOIN action_jobs j ON j.id=t.job_id WHERE (t.status='queued' OR (t.status='snoozed' AND t.until<=?)) AND (t.retry_at IS NULL OR t.retry_at<=?) ORDER BY t.created_at LIMIT 1",(now(),now())).fetchone()
            if row and row['status']=='snoozed':
                later=db.execute("SELECT max(until) FROM thread_snoozes WHERE account_id=? AND thread_id=? AND status IN ('queued','snoozed') AND until>?",(row['account_id'],row['thread_id'],now())).fetchone()[0]
                if later:
                    db.execute('UPDATE thread_snoozes SET until=? WHERE job_id=?',(later,row['job_id']))
                    return
        if not row:return
        gmail=gmail or next_actions.ThreadSnooze(self.config,credential,gog_read)
        try:
            if row['status']=='queued':
                if row['until']<=now():status='returned'  # Too late to snooze; leave the thread alone.
                else:status=gmail.snooze(row['account_id'],row['thread_id'],row['sent_message_id'])
            else:status=gmail.wake(row['account_id'],row['thread_id'])
            if status=='sending':  # Outlook hasn't put the sent reply in Sent Items yet: ask again in a minute
                if dt.datetime.fromisoformat(now())-dt.datetime.fromisoformat(row['created_at'])>=SNOOZE_SENDING_GRACE:
                    raise RuntimeError('sent_message_not_confirmed')
                with self.store.connect() as db:
                    db.execute('UPDATE thread_snoozes SET retry_at=?,updated_at=? WHERE job_id=?',
                               ((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=1)).isoformat(),now(),row['job_id']))
                return
            outlook=next((a for a in self.config.get('accounts',[]) if a['id']==row['account_id'] and a.get('service')=='outlook'),None)
            error={'no_permission':'Outlook can’t move this thread yet: connect the account again with sending on.' if outlook else 'Gmail can’t move this thread yet: the account needs the modify permission.'}.get(status)
            with self.store.connect() as db:
                db.execute('UPDATE thread_snoozes SET status=?,error=?,retry_at=NULL,updated_at=? WHERE job_id=?',
                           ('failed' if error else status,error,now(),row['job_id']))
                if status=='returned':
                    db.execute("UPDATE thread_snoozes SET status='returned',error=NULL,retry_at=NULL,updated_at=? WHERE account_id=? AND thread_id=? AND status IN ('queued','snoozed')",(now(),row['account_id'],row['thread_id']))
        except Exception as error:
            # Retry with backoff; a thread that can't come back stays labeled in Gmail.
            attempts=row['attempts']+1
            with self.store.connect() as db:
                db.execute('UPDATE thread_snoozes SET attempts=?,error=?,retry_at=?,status=?,updated_at=? WHERE job_id=?',
                           (attempts,type(error).__name__,(dt.datetime.fromisoformat(now())+dt.timedelta(minutes=min(5*2**attempts,360))).isoformat(),
                            row['status'] if attempts<12 or row['status']=='snoozed' else 'failed',now(),row['job_id']))
            LOG.error('thread snooze status=%s error=%s',row['status'],type(error).__name__)

    def follow_config(self):
        """Settings in LIVE_CONFIG that changed in config.json since the last look (the hosting agent's reviews on, while
        the first look runs) apply at once, without a restart. Best effort: an unreadable file changes nothing."""
        path = getattr(self, 'config_path', None)
        if not path:
            return False
        with self.__dict__.setdefault('config_following', threading.Lock()):  # the review worker and setup's ask
            try:
                stamp = path.stat().st_mtime_ns
                if stamp == getattr(self, 'config_stamp', None):
                    return False
                if getattr(self, 'config_stamp', None) is None:
                    self.config_stamp = stamp
                    return False  # what the app started with
                saved = json.loads(path.read_text())
            except (OSError, ValueError):
                return False  # a file being written: the next look reads it again
            self.config_stamp = stamp
            changed = False
            for key in LIVE_CONFIG:
                if isinstance(saved, dict) and key in saved and saved[key] != self.config.get(key):
                    self.config[key] = saved[key]
                    changed = True
            if changed:
                LOG.info('settings applied without a restart: %s', ','.join(LIVE_CONFIG))
            added = live_additions(self.config, saved)
            if added and added[0]:
                self.adopt_accounts(*added)
                changed = True
            return changed

    def stop_all(self):
        self.stop.set()
        for wake in list(getattr(self, 'collector_wakes', {}).values()):
            wake.set()  # a collector resting till its next read stops now too
        if self.__dict__.get('fleet_stop') is not None:
            self.fleet_stop.set()

    def protection_now(self, config):
        """What the Store does with message protection at this start: on unless config.json says false. A change to an
        existing database (an upgrade that turns it on by default, say) waits while a review, preparation or profile
        turn runs, so none is cut off: the app starts as it was and restarts itself once they are done
        (`protection_waiter`). The change itself keeps a copy until it checks out (Store.message_protection)."""
        self.protection_waits = False
        want = message_seal.wanted(config)
        sealed, _ = message_seal.state(config['database'])
        if sealed is None or sealed == want:
            return want
        running = message_seal.work_running(config['database'])
        if running == 0:
            return want
        self.protection_waits = True
        LOG.info('message contents will be %s once The Machine is idle (%s running)', 'sealed' if want else 'opened',
                 running if running is not None else 'unknown')
        return None

    def protection_waiter(self, every=30):
        """Restart once nothing runs, so the next start seals (or opens) the database with nothing cut off."""
        while not self.stop.wait(every):
            if message_seal.work_running(self.config['database']) == 0:
                if restart_self():
                    LOG.info('idle: restarting to apply message protection')
                else:
                    LOG.info('idle: message protection applies at the next start')
                return
