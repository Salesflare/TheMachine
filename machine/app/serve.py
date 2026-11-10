"""The service itself: serve() starts every worker, the collectors and the loopback web server (machine/web/handler.py)
and runs until stopped; packed_page keeps the dashboard page compressed once per page and coding. Moved out of
assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import http.server
from pathlib import Path
import signal
import threading

import abilities
import agent_jobs
import browser_login
import embeddings
import error_feed
from machine.actions import DASHBOARD_ACTIONS
from machine.browser import AGENT_DB
from machine.config import LOG
from machine.model_usage import node_bin
from machine.store import review_requeue
from machine.faults import watch_faults
from machine.web.handler import make_handler
from machine.web.serving import compress_body
import shared_connectors
import work_removal


PACKED_KEEP = 40  # compressed pages and scripts kept (packed_page): about 0.7 MB for a coding's page and scripts


class ServeApp:
    ACTIONS = {'client_error': 'client_error_action'}

    def packed_page(self, etag, coding, page):
        """The dashboard page compressed in `coding`, made once per page (its ETag) and coding: the best compression,
        since it goes to every device opening the app. Also its main script and each group of parts that loads later
        (machine/web/serving.py dashboard_files, 15 files): enough kept for all of them in a coding or two, a page or
        two, so a fresh page's files are never compressed again (with 6, they pushed each other out on every load)."""
        key = (etag, coding)
        with self._packed_lock:
            if key in self._packed:
                self._packed[key] = self._packed.pop(key)  # the least recently used goes first
                return coding, self._packed[key]
        data = compress_body(page.encode(), coding, best=True)
        with self._packed_lock:
            self._packed[key] = data
            while len(self._packed) > PACKED_KEEP:
                self._packed.pop(next(iter(self._packed)))
        return coding, data

    def serve(self):
        app = self
        self._packed, self._packed_lock = {}, threading.Lock()
        try:  # saved sign-ins kept with a key of their own (or opened by an import) go over to the message key
            if browser_login.LoginStore(Path(self.config['database']).expanduser().parent).migrate():
                LOG.info('saved sign-ins are now encrypted with the message key')
        except Exception as error:  # they stay as they were; the next start tries again
            LOG.warning('saved sign-ins not moved to the message key: %s', type(error).__name__)

        Handler = make_handler(app)

        server = http.server.ThreadingHTTPServer(('127.0.0.1', self.config.get('port', 8787)), Handler)
        watch_faults(self.store)
        if getattr(self, 'agents', None):
            self.agents.version = self.store.code_version  # failed jobs in the error reports carry it
            try:
                self.agents.recover()  # a job that ran when the service stopped, or one still waiting for a slot
            except Exception as error:  # noqa: BLE001 - never stops the service
                LOG.error('agent jobs recover error=%s', type(error).__name__)
            if getattr(self, 'fleet', None) and not self.config.get('manage_url') and agent_jobs.find('codex'):
                # Paired with the owner's account on their own computer: Codex jobs their hosted Machine hands here
                # (Where Codex runs: On my computer) run with this computer's own Codex (agent_remote.serve)
                import agent_remote
                threading.Thread(target=agent_remote.serve, args=(self.agents, self.stop), daemon=True, name='agent-serve').start()
        if getattr(self, 'skills', None):
            self.skills.sync()  # the workspace has the skills that are on, also after edits made while this was off
        signal.signal(signal.SIGTERM, lambda *_: self.stop_all())
        signal.signal(signal.SIGINT, lambda *_: self.stop_all())
        try:  # a work removal that was going on: what a sync stored meanwhile goes too; old safety copies go
            if work_removal.settle(self.config, self.store):
                self.graph_dirty.set()
            work_removal.prune(self.config)
        except Exception as error:  # noqa: BLE001 - never stops the service
            LOG.error('work removal settle error=%s', type(error).__name__)
        try:  # a Fleet-shared Intercom or Stripe the owner also connected themselves: one reader, its messages kept once
            shared_connectors.merge_covered(self.config['accounts'], self.store)
        except Exception as error:  # noqa: BLE001 - never stops the service; the next start tries again
            LOG.error('shared connector merge error=%s', type(error).__name__)
        for account in self.config['accounts']:
            if shared_connectors.covered_by(self.config['accounts'], account):
                continue  # it rests while the owner's own connection reads that workspace (its card says so)
            # Brings in signals off (abilities.py): no sync; a Docs connection still checks what it may do, now and then
            threading.Thread(target=self.collector if abilities.signals_on(account) else self.ability_checker, args=(account,),
                             daemon=True).start()
        threading.Thread(target=self.delivery_worker, daemon=True).start()
        threading.Thread(target=self.preparation_worker, daemon=True).start()
        threading.Thread(target=self.whatsapp_photo_worker, name='whatsapp-photos', daemon=True).start()
        threading.Thread(target=self.voice_warm_worker, name='voice-warm', daemon=True).start()
        threading.Thread(target=self.action_worker, daemon=True).start()
        try:  # an older Import birthdays from Facebook to-do: the friends nobody in the Graph has, read once in the background
            self.birthdays_facebook_fill_old()
        except Exception as error:  # noqa: BLE001 - never stops the service; the next start tries again
            LOG.error('facebook birthdays fill error=%s', type(error).__name__)
        try:  # once: messages whose to-do save failed before the fix of 2026-11-07 go back to the review (review_requeue.py)
            back = review_requeue.requeue(self.store, AGENT_DB, node_bin(self.config))
            if back:
                LOG.info('Sent %d message(s) whose to-do save had failed back to the review', back)
        except Exception as error:  # noqa: BLE001 - never stops the service; the next start tries again
            LOG.error('failed saves requeue error=%s', type(error).__name__)
        threading.Thread(target=self.review_worker, daemon=True).start()
        threading.Thread(target=self.graph_worker, daemon=True).start()
        if getattr(self, 'fleet', None):
            self.fleet_stop = threading.Event()  # set by Unpair (fleet_drop) and when the service stops
            threading.Thread(target=self.fleet.run, args=(self.fleet_stop,), daemon=True).start()
            self.ai_reach_start(self.fleet_stop)
        threading.Thread(target=self.model_usage_worker, daemon=True).start()
        if getattr(self, 'fleet', None):
            threading.Thread(target=self.bug_queue_worker, name='bug-queue', daemon=True).start()
        threading.Thread(target=self.retention_worker, daemon=True).start()
        threading.Thread(target=self.plain_keys_worker, name='plain-keys', daemon=True).start()  # once (machine/store/plain_keys.py)
        threading.Thread(target=self.history_worker, name='history', daemon=True).start()  # older messages, as history (machine/app/history.py)
        self.meeting_write_resume()  # Generate notes that were going when the service stopped
        self.gbrain_start()  # GBrain (gbrain.py): only when the owner turned it on
        if getattr(self, 'skills', None) and self.skills.catalog:  # what OpenClaw has, for Settings > Skills and skill hints
            threading.Thread(target=self.skills.catalog.worker, args=(self.stop,), daemon=True).start()
        if embeddings.settings(self.config):
            threading.Thread(target=self.embedding_worker, daemon=True).start()
        # Always: photos and facts from the owner's own connections need no look-up service (its steps skip themselves).
        threading.Thread(target=self.enrichment_worker, daemon=True).start()
        threading.Thread(target=self.linkedin_connections_worker, name='linkedin-connections', daemon=True).start()  # linkedin_connections.py
        threading.Thread(target=self.recurring_worker, name='recurring', daemon=True).start()  # recurring to-dos (recurring_app.py)
        threading.Thread(target=self.routines_worker, name='routines', daemon=True).start()  # routines (routines_app.py)
        if getattr(self, 'protection_waits', False):
            threading.Thread(target=self.protection_waiter, daemon=True).start()
        server.timeout = 1
        LOG.info('service started; loopback only; accounts=%d', len(self.config['accounts']))
        while not self.stop.is_set():
            server.handle_request()
        server.server_close()

    def client_error_action(self, name, args, owner_dashboard=False):
        # the dashboard's own errors, as signatures for the error reports (error_feed.py)
        with self.store.connect() as db:
            return {'ok': True, 'counted': error_feed.record_client(db, args.get('errors'), self.store.code_version, DASHBOARD_ACTIONS)}
