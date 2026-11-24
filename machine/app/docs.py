"""A preparation's reads and writes of the owner's docs (App.action): a doc's text, finding a doc by its words, and
writing a draft doc. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import json
import re

import abilities
import doc_writes
from machine.sources.connectors import CONNECTOR_HELPERS, doc_write_files, docs_files_offered, load_connector
from sources import SourceError
from machine.owner_error import OwnerError


MAX_FILE_SIGNINS = 3  # Google sign-ins tried for one linked Sheet or Slides file


class DocsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'doc_text': 'doc_text_action', 'doc_find': 'doc_find_action',
               'doc_write_draft': 'doc_write_draft_action'}

    def doc_text(self, args):
        """A doc's text for a run the owner started (Do it, or a card chat's run), read-only and never kept: the run reads
        it once. Through a Docs connection that can do things (abilities.py), in the to-do's area: a doc of one of the
        task's own doc events (event_id), or by file_id a doc linked in the task's messages or the owner's chat on it, or one
        doc_find gave this run. A linked Google Sheet or Slides file too, with `range` for one part of it (google_files.py)."""
        job, run, links, area = self.doc_run(args)
        plugin = load_connector('docs')
        event_id, file_id = args.get('event_id'), str(args.get('file_id') or '')
        if event_id is not None:
            if not str(event_id).isdigit():
                raise ValueError('Give the event_id of the doc event and the job_id of this preparation')
            with self.store.connect() as db:
                row = db.execute("SELECT account_id,metadata FROM events WHERE id=? AND (kind LIKE 'docs.%' OR kind LIKE 'notion.%') AND id IN "
                                 "(SELECT value FROM json_each(?))", (int(event_id), run['event_ids'])).fetchone()
            if not row:
                raise OwnerError('That doc is not one of this task’s own doc events')
            account = next((a for a in self.config['accounts'] if a['id'] == row['account_id'] and a.get('service') in abilities.DOC_SERVICES), None)
            file_id = json.loads(row['metadata']).get('file_id')
        elif re.fullmatch(r'[A-Za-z0-9_!.-]{10,300}', file_id):
            found = self.__dict__.setdefault('_docs_found', {}).get(job, {})
            linked = links.get(file_id)
            if file_id not in found and isinstance(linked, dict):
                return self.linked_file(file_id, linked, args.get('range'))
            if file_id in found:
                account = next((a for a in self.config['accounts'] if a['id'] == found[file_id]), None)
            elif linked:
                account = next((a for a in self.doc_connections(area) if a['id'] == linked), None)
                if not account:
                    raise ValueError(self.NO_DOC_CONNECTION)
            else:
                raise ValueError('Read a doc linked in this task’s messages or the owner’s chat on it, or one assistant doc-find gave this run')
        else:
            raise ValueError('Give the event_id of the doc event, or the file_id of the doc')
        if not account or not file_id or not plugin:
            raise OwnerError('That Docs connection is no longer here')
        off = abilities.refuse(self.config, account['id'])
        if off:
            raise ValueError(off)
        try:
            return plugin.read_text(self.config, account, str(file_id), CONNECTOR_HELPERS)
        except SourceError as error:
            raise self.doc_read_error(error) from None

    def doc_find(self, args):
        """Docs that match some words, for a run the owner started: through each Docs connection in the to-do's area that
        can do things (abilities.py), read-only. What it finds this run may then read (doc_text with file_id)."""
        job, _, _, area = self.doc_run(args)
        words = args.get('words')
        if not isinstance(words, str) or not words.strip() or len(words) > 200:
            raise ValueError('Give the words to look for, at most 200 characters')
        plugin = load_connector('docs')
        accounts = self.doc_connections(area)
        if not accounts:
            raise ValueError(self.NO_DOC_CONNECTION)
        found, errors = [], []
        for account in accounts:
            try:
                found += [{**d, 'account_id': account['id'], 'provider': plugin.provider(self.config, account)}
                          for d in plugin.find(self.config, account, words, CONNECTOR_HELPERS)]
            except SourceError as error:
                errors.append(str(self.doc_read_error(error)))
        kept = self.__dict__.setdefault('_docs_found', {})
        kept.setdefault(job, {}).update({d['file_id']: d['account_id'] for d in found})
        while len(kept) > 50:
            kept.pop(next(iter(kept)))
        return {'docs': found, **({'errors': errors} if errors else {})}

    def doc_write_draft(self, args):
        """Check a doc write before it goes in the preparation's result, for a run the owner started: never a write.
        Without `next_action`, an edit's doc (one of the task's own doc events) as it is now: its version and paragraphs.
        With one, the validated draft and the preview the owner will see (before and after for an edit)."""
        job = str(args.get('job_id') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        with self.store.connect() as db:
            run = db.execute("SELECT s.id,s.event_ids,s.account_ids FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                             "WHERE p.job_id=? AND p.status IN ('queued','starting','running','blocked')", (job,)).fetchone()
            if not run:
                raise ValueError('Doc drafts are checked only for a running preparation of the task the owner started')
            files = doc_write_files(db, run['event_ids'], self.config, doc_writes.area(self.config, json.loads(run['account_ids'] or '[]')),
                                    run['id'])
            file_id = None
            if args.get('event_id') is not None:
                row = db.execute("SELECT metadata FROM events WHERE id=? AND (kind LIKE 'docs.%' OR kind LIKE 'notion.%') AND id IN (SELECT value FROM json_each(?))",
                                 (int(args['event_id']) if str(args['event_id']).isdigit() else -1, run['event_ids'])).fetchone()
                file_id = row and str(json.loads(row['metadata']).get('file_id') or '')
                if not file_id:
                    raise OwnerError('That doc is not one of this task’s own doc events')
            elif args.get('file_id'):
                file_id = doc_writes.file_id_of(args['file_id'])
                if file_id not in files:
                    raise OwnerError('That doc is not one of this to-do’s docs (one made for it, its doc events, or a Google Doc '
                                     'linked in its messages)')
        plugin = load_connector('docs')
        if not plugin or not hasattr(plugin, 'Writer'):
            raise ValueError('There is no Docs connection here')
        value = args.get('next_action')
        if not isinstance(value, dict):
            if not file_id:
                raise ValueError('Give the event_id or file_id of the doc to edit, or a doc_write next_action to check')
            value = {'kind': doc_writes.KIND, 'op': 'edit', 'file_id': file_id, 'changes': []}
            context = doc_writes.context(self.config, plugin, CONNECTOR_HELPERS, files, value)
            found = (context or {}).get('snapshots', {}).get(file_id)
            if found is None:
                raise ValueError('Edits are not allowed for this Docs connection yet (Allow edits on its connection)')
            if isinstance(found, str):
                raise ValueError(found)
            return {'file_id': file_id, 'title': found['title'], 'version': found['version'], 'url': found.get('url'),
                    'paragraphs': [{'n': i + 1, 'text': p['text'], 'editable': p['editable']} for i, p in enumerate(found['paragraphs'])]}
        if file_id and value.get('op') == 'edit':
            value = {**value, 'file_id': value.get('file_id') or file_id}
        value = {**value, 'kind': doc_writes.KIND}
        action = doc_writes.validate(value, doc_writes.context(self.config, plugin, CONNECTOR_HELPERS, files, value))
        return {'preview': doc_writes.preview(action), 'next_action': {k: v for k, v in value.items()}}

    def doc_text_action(self, name, args, owner_dashboard=False):
        return self.doc_text(args)

    def doc_find_action(self, name, args, owner_dashboard=False):
        return self.doc_find(args)

    def doc_write_draft_action(self, name, args, owner_dashboard=False):
        return self.doc_write_draft(args)

    def doc_run(self, args):
        """The running preparation a doc read is for (Do it, or a to-do chat's run): its job id, its own events and its
        area (doc_writes.area). Docs are read only for a run the owner started."""
        job = str(args.get('job_id') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        with self.store.connect() as db:
            run = db.execute("SELECT s.id,s.event_ids,s.account_ids FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                             "WHERE p.job_id=? AND p.status IN ('queued','starting','running','blocked')", (job,)).fetchone()
            if not run:
                raise OwnerError('Docs are read only for a running preparation of the task the owner started')
            area = doc_writes.area(self.config, json.loads(run['account_ids'] or '[]'))
            # a doc linked in the task's messages, or in what the owner wrote in its chat -> their connection that opens it
            # here (Google Docs, or Notion); a Google Sheet or Slides file -> what it is and the sign-ins that may read it
            links, plugin = {}, load_connector('docs')
            via = {}
            for account in self.doc_connections(area) if plugin else ():
                via.setdefault(plugin.provider(self.config, account), account)
            said = [str(r['body'] or '') + ' ' + str(r['metadata'] or '') for r in db.execute(
                "SELECT e.body,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id", (run['event_ids'],))] if plugin else []
            said += [str(r[0] or '') for r in db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND choice='other' AND source IN ('telegram','dashboard') AND feedback LIKE '%://%' "
                                                         "ORDER BY created_at DESC LIMIT 50", (run['id'],))] if plugin else []
        for text in said:
            for account in (via.get('google'), via.get('notion')):
                for file_id in plugin.doc_links_of(account, text) if account else ():
                    links.setdefault(file_id, account['id'])
        for file_id, file in (plugin.file_links('\n'.join(said)) if plugin else {}).items():
            links.setdefault(file_id, {**file, 'accounts': self.file_accounts(area)})
        return job, run, links, area

    def file_accounts(self, area):
        """The owner's own Google sign-ins in this area that may read a linked Sheet or Slides file: their Google Docs
        connections, then their gog Google accounts, as far as each can do things (abilities.py)."""
        plugin = load_connector('docs')
        return self.doc_connections(area, 'google') + [
            a for a in self.config.get('accounts', []) if plugin.gog_google(a) and a.get('actions') is not False
            and doc_writes.fits(a.get('boundary'), area)]

    def linked_file(self, file_id, linked, asked=None):
        """A linked Google Sheet's cells or Slides file's text: through the first of these sign-ins that can open it. The
        owner hears the most useful reason when none can."""
        if asked is not None and (not isinstance(asked, str) or len(asked) > 200):
            raise ValueError('Give a tab and cells, or slide numbers, as the range')
        plugin = load_connector('docs')
        if not linked['accounts']:
            raise ValueError(self.NO_DOC_CONNECTION)
        errors = []
        for account in linked['accounts'][:MAX_FILE_SIGNINS]:
            try:
                return plugin.read_file(self.config, account, file_id, linked['kind'], CONNECTOR_HELPERS, linked['spots'], asked)
            except SourceError as error:
                if error.category not in ('docs_files_not_granted', 'docs_no_access', 'docs_gone', 'docs_signin_expired', 'docs_no_signin'):
                    raise self.doc_read_error(error) from None  # this sign-in opened it, or Google is the one failing
                errors.append((error, account))
        error, account = min(errors, key=lambda e: ('docs_no_access', 'docs_gone', 'docs_files_not_granted').index(e[0].category)
                             if e[0].category in ('docs_no_access', 'docs_gone', 'docs_files_not_granted') else 3)
        if error.category == 'docs_files_not_granted':
            if any(docs_files_offered(self.config, a) for _, a in errors):
                raise ValueError('The Machine can’t read Google Sheets and Slides yet: press Allow Sheets and Slides on Google Docs under '
                                 'Connections, or paste the part that matters in the chat')
            raise ValueError('The Machine can’t read Google Sheets and Slides here: open the file and paste the part that matters in the chat')
        raise self.doc_read_error(error) from None

    def doc_connections(self, area, provider=None):
        """The owner's own Docs connections in this area that can do things (abilities.py), Google or Microsoft."""
        plugin = load_connector('docs')
        return [a for a in self.config.get('accounts', []) if a.get('service') in abilities.DOC_SERVICES and plugin and abilities.actions_on(a)
                and doc_writes.fits(a.get('boundary'), area) and (provider is None or plugin.provider(self.config, a) == provider)]

    def doc_read_error(self, error):
        return ValueError({'docs_not_connected': 'Reading docs is not allowed for this account yet (Connect Google Docs or Microsoft documents)',
                           'docs_file_too_large': 'That file is too large to read here (open it in the browser instead)',
                           'docs_no_access': 'That file is private to someone else: it is not shared with the Google account connected here. Open it to ask for access, or paste the part that matters in the chat',
                           'docs_gone': 'That file was deleted, or its link is wrong',
                           'docs_file_kind': 'That file is not a Google Sheet or Slides file (an Excel or PowerPoint file in Drive). Download it and attach it in the chat',
                           'docs_range_unknown': 'That part is not in the file: give a tab and cells from the list of tabs, or slide numbers',
                           'docs_signin_expired': 'Google asks to sign in again (Reconnect under Connections)',
                           'docs_text_unsupported': 'That file has no text to read here (open it in the browser instead)'}.get(
                               error.category, f'The doc could not be read ({error.category})'))
