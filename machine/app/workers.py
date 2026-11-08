"""The service's background workers and their steps that aren't one feature's own: retention, embeddings, enrichment,
the spacing of background work, Help topics and error reports sent to the control plane. Moved out of assistant.App
as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import time

import chat_files
import embeddings
import enrichment
import error_feed
import help_topics
from machine.config import LOG
from machine.sources.telegram import telegram_photo_asker
from machine.sources.whatsapp import whatsapp_photo_asker
import retention
from sources import gog_read, SourceError
import team_learnings
from timeutil import local_tz, now


# Contact photos from the owner's Google contacts and Workspace directory, with the scopes the gog sign-in already has
# (a hosted sign-in through the broker has no Contacts scope, so it is never asked). Read only, once a day per account.
GOOGLE_PHOTO_LISTS = (
    ('people.connections.list', {'resourceName': 'people/me', 'pageSize': 1000, 'personFields': 'emailAddresses,phoneNumbers,photos,organizations'},
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


class WorkersApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def retention_worker(self):
        """Once a day at a quiet hour: old sync history and preparation logs go, the space goes back to the disk and
        local copies of the database rotate (retention.py). Checks every ten minutes; never stops the service."""
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
