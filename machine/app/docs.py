"""A preparation's reads and writes of the owner's docs (App.action): a doc's text, finding a doc by its words, and
writing a draft doc. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import json
import re

import abilities
import doc_writes
from machine.sources.connectors import CONNECTOR_HELPERS, doc_write_files, load_connector
from sources import SourceError


class DocsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'doc_text': 'doc_text_action', 'doc_find': 'doc_find_action',
               'doc_write_draft': 'doc_write_draft_action'}

    def doc_text(self, args):
        """A doc's text for a run the owner started (Do it, or a card chat's run), read-only and never kept: the run reads
        it once. Through a Docs connection that can do things (abilities.py), in the to-do's area: a doc of one of the
        task's own doc events (event_id), or by file_id a doc linked in the task's messages or one doc_find gave this run."""
        job, run, links, area = self.doc_run(args)
        plugin = load_connector('docs')
        event_id, file_id = args.get('event_id'), str(args.get('file_id') or '')
        if event_id is not None:
            if not str(event_id).isdigit():
                raise ValueError('Give the event_id of the doc event and the job_id of this preparation')
            with self.store.connect() as db:
                row = db.execute("SELECT account_id,metadata FROM events WHERE id=? AND kind LIKE 'docs.%' AND id IN "
                                 "(SELECT value FROM json_each(?))", (int(event_id), run['event_ids'])).fetchone()
            if not row:
                raise ValueError('That doc is not one of this task’s own doc events')
            account = next((a for a in self.config['accounts'] if a['id'] == row['account_id'] and a.get('service') == 'docs'), None)
            file_id = json.loads(row['metadata']).get('file_id')
        elif re.fullmatch(r'[A-Za-z0-9_!.-]{10,300}', file_id):
            found = self.__dict__.setdefault('_docs_found', {}).get(job, {})
            if file_id in found:
                account = next((a for a in self.config['accounts'] if a['id'] == found[file_id]), None)
            elif file_id in links:
                account = next(iter(self.doc_connections(area, 'google')), None)
                if not account:
                    raise ValueError(self.NO_DOC_CONNECTION)
            else:
                raise ValueError('Read a doc linked in this task’s messages, or one assistant doc-find gave this run')
        else:
            raise ValueError('Give the event_id of the doc event, or the file_id of the doc')
        if not account or not file_id or not plugin:
            raise ValueError('That Docs connection is no longer here')
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
            run = db.execute("SELECT s.event_ids,s.account_ids FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                             "WHERE p.job_id=? AND p.status IN ('queued','starting','running','blocked')", (job,)).fetchone()
            if not run:
                raise ValueError('Doc drafts are checked only for a running preparation of the task the owner started')
            files = doc_write_files(db, run['event_ids'], self.config, doc_writes.area(self.config, json.loads(run['account_ids'] or '[]')))
            file_id = None
            if args.get('event_id') is not None:
                row = db.execute("SELECT metadata FROM events WHERE id=? AND kind LIKE 'docs.%' AND id IN (SELECT value FROM json_each(?))",
                                 (int(args['event_id']) if str(args['event_id']).isdigit() else -1, run['event_ids'])).fetchone()
                file_id = row and str(json.loads(row['metadata']).get('file_id') or '')
                if not file_id:
                    raise ValueError('That doc is not one of this task’s own doc events')
        plugin = load_connector('docs')
        if not plugin or not hasattr(plugin, 'Writer'):
            raise ValueError('There is no Docs connection here')
        value = args.get('next_action')
        if not isinstance(value, dict):
            if not file_id:
                raise ValueError('Give the event_id of the doc to edit, or a doc_write next_action to check')
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
