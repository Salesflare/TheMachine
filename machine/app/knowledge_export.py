"""Knowledge for another AI in the service (machine/export/knowledge.py makes it): Settings, Export. The action packs
it and keeps it in memory for a few minutes; the dashboard then downloads it once from /api/knowledge-export. Nothing
of it is written to disk. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import hmac
import os
import secrets
import threading
import time
import urllib.parse
from pathlib import Path

from machine.export import knowledge
from machine.owner_error import OwnerError
import timeutil

KEEP_SECONDS = 600  # an export not downloaded by then is dropped


class KnowledgeExportApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'knowledge_export': 'knowledge_export_action'}

    def knowledge_export_action(self, name, args, owner_dashboard):
        """Pack Knowledge for another AI: {token, name, bytes}. args: messages (message text too), private (private
        and Careful content too), passphrase (optional: the file is then encrypted, as the full export is)."""
        if not owner_dashboard:
            raise OwnerError('Export it from the dashboard.')
        passphrase = args.get('passphrase') or ''
        if not isinstance(passphrase, str) or (passphrase and len(passphrase) < knowledge.MIN_PASSPHRASE):
            raise OwnerError(f'Pick a passphrase of at least {knowledge.MIN_PASSPHRASE} characters, or none.')
        options = knowledge.Options(messages=args.get('messages') is True, private=args.get('private') is True)
        workspace = Path(os.environ.get('OPENCLAW_WORKSPACE') or Path.home() / '.openclaw/workspace').expanduser()
        reader = knowledge.StoreReader(self.store, self.config, getattr(self, 'fleet', None), workspace)
        bundle = knowledge.collect(reader, options)
        data = knowledge.zipped(bundle)
        stamp = timeutil.today().isoformat()
        name = f'the-machine-knowledge-{stamp}.zip'
        if passphrase:
            data, name = knowledge.encrypt(data, passphrase), name + '.enc'
        token = secrets.token_urlsafe(24)
        with self.knowledge_lock():
            self.__dict__['knowledge_ready'] = {'token': token, 'name': name, 'data': data, 'until': time.monotonic() + KEEP_SECONDS}
        return {'token': token, 'name': name, 'bytes': len(data), 'counts': {k: len(bundle[k]) for k in ('entities', 'facts', 'todos')}}

    def knowledge_lock(self):
        return self.__dict__.setdefault('knowledge_mutex', threading.Lock())

    def knowledge_take(self, token):
        """The packed export for this token, once: (name, bytes) or None."""
        with self.knowledge_lock():
            ready = self.__dict__.get('knowledge_ready')
            if not ready or not isinstance(token, str) or not hmac.compare_digest(ready['token'].encode(), token.encode()):
                return None
            self.__dict__['knowledge_ready'] = None
        return (ready['name'], ready['data']) if ready['until'] > time.monotonic() else None

    def knowledge_download(self, handler, token):
        """GET /api/knowledge-export?token=...: the file as a download, from the owner's own dashboard only."""
        found = self.knowledge_take(token)
        if not found:
            handler.output(404, {'error': 'That export is gone. Export it again.'})
            return
        name, data = found
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/zip' if name.endswith('.zip') else 'application/octet-stream')
        handler.send_header('Content-Disposition', "attachment; filename*=UTF-8''" + urllib.parse.quote(name))
        handler.send_header('Content-Length', str(len(data)))
        handler.send_header('Cache-Control', 'no-store')
        handler.send_header('X-Content-Type-Options', 'nosniff')
        handler.send_header('Referrer-Policy', 'no-referrer')
        handler.send_header('Content-Security-Policy', "default-src 'none'; sandbox")
        handler.end_headers()
        try:
            handler.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            handler.close_connection = True
