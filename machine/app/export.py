"""Settings, Export: export everything (moving.export) and import an export (moving.stage), from the dashboard. A mixin
of assistant.App (APP_MIXINS); docs/help/moving.md.

- export_start runs the export in a background thread into a private folder next to the data folder (700, never
  inside it, so the next export doesn't hold this one); export_status says how far it got and, once done, its parts,
  what is not in it and the export code (memory only, never written); /api/export-download streams the file to the
  owner; export_delete, or 24 hours, shreds it.
- /api/import-upload streams an uploaded export to disk (never whole in memory, after a free disk check);
  import_stage opens and checks it with its passphrase in a thread (moving.stage); import_discard drops it;
  import_confirm is the owner's Import now (Replace with this export): a hosted Machine's server then applies it; a
  self-hosted Machine restarts its own service and applies it at the start, before it serves (machine/export/staged.py).
  Without systemd or launchd to restart it, the status lists the commands instead.

On a hosted Machine the export itself is the account page's (Settings, Account): export_start refuses there.
Other ways out (Knowledge for any AI) are further options in the same section of the dashboard (EXPORT_OPTIONS in
dashboard/settings-export.js)."""
import datetime as dt
import json
import logging
import os
import re
import secrets
import shutil
import threading
import time
import urllib.parse
from pathlib import Path

import moving
import portable
from machine.export import staged as staged_import
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')

KEEP_HOURS = 24  # a finished export waits this long to be downloaded, then it is shredded
CHUNK = 1 << 20
UPLOAD_NAME = 'upload.tar.gz.enc'
# Staging decrypts the upload and unpacks it: room for the upload, a decrypted copy and what it unpacks to
UPLOAD_ROOM = 3
UPLOAD_SPARE = 200 * 1024 * 1024
COMMANDS = ['assistant service stop', 'assistant import --staged', 'assistant service start']


def _when(stamp):
    return dt.datetime.fromtimestamp(stamp, dt.timezone.utc).isoformat(timespec='seconds')


def human(size):
    for unit in ('bytes', 'KB', 'MB', 'GB'):
        if size < 1024 or unit == 'GB':
            return f'{size:.0f} {unit}' if unit in ('bytes', 'KB') else f'{size:.1f} {unit}'
        size /= 1024


def parts_view(parts):
    """The manifest's parts as rows for the dashboard, in the inventory's order: [{'key', 'label', 'rows', 'files', 'bytes'}]."""
    return [{'key': key, 'label': p.get('label') or key, 'rows': int(p.get('rows') or 0), 'files': int(p.get('files') or 0),
             'bytes': int(p.get('bytes') or 0)} for key, p in (parts or {}).items() if isinstance(p, dict)]


def not_view(items):
    """What could not come along, as the owner reads it: what and why (the home folder's caches are left out here)."""
    return [{'what': str(i.get('what') or ''), 'why': str(i.get('why') or '')} for i in items or []
            if isinstance(i, dict) and i.get('what') and not str(i['what']).startswith('~/')]


class ExportApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'export_start': 'export_start_action', 'export_status': 'export_status_action', 'export_delete': 'export_delete_action',
               'import_stage': 'import_stage_action', 'import_discard': 'import_discard_action', 'import_confirm': 'import_confirm_action'}
    # Where the export reads from (moving.export's workspace, openclaw_home, home): its defaults, or a test's folders
    export_paths = {}

    # --- where things are ------------------------------------------------------------------------------------------

    def _export_root(self):
        if not getattr(self, 'config_path', None):
            raise OwnerError('Export needs a Machine with its own data folder.')
        data = Path(self.config_path).expanduser().parent
        root = data.parent / f'.{data.name}.export'
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(root, 0o700)
        return root

    def _export_lock(self):
        lock = self.__dict__.get('export_lock')
        if lock is None:
            lock = self.__dict__.setdefault('export_lock', threading.Lock())
        return lock

    def _export_job(self):
        return self.__dict__.setdefault('export_job', {})

    def _import_job(self):
        return self.__dict__.setdefault('import_job', {})

    def _hosted(self):
        return bool((getattr(self, 'config', None) or {}).get('manage_url'))

    @staticmethod
    def _owner_only(owner_dashboard):
        if not owner_dashboard:
            raise OwnerError('Export and import are only in your own dashboard.')

    # --- export ----------------------------------------------------------------------------------------------------

    def _export_file(self):
        """(path, summary) of the finished export, or (None, None). One older than KEEP_HOURS is shredded here."""
        root = self._export_root() / 'out'
        try:
            summary = json.loads((root / 'export.json').read_text())
            path = root / summary['name']
            if not path.is_file():
                raise OSError
        except (OSError, ValueError, KeyError, TypeError):
            return None, None
        if time.time() - path.stat().st_mtime > KEEP_HOURS * 3600:
            self._export_shred()
            return None, None
        return path, summary

    def _export_shred(self):
        root = self._export_root() / 'out'
        portable.shred_tree(root)
        job = self._export_job()
        if job.get('state') != 'running':
            job.clear()

    def export_start_action(self, name, args, owner_dashboard):
        """Export everything: a passphrase the owner picks (or none: an export code is made), keys only with one."""
        self._owner_only(owner_dashboard)
        if self._hosted():
            raise OwnerError('On a hosted Machine, export everything from your account page.')
        passphrase = args.get('passphrase') or None
        keys = bool(args.get('keys'))
        if passphrase is not None and (not isinstance(passphrase, str) or len(passphrase) < moving.MIN_PASSPHRASE):
            raise OwnerError(f'Pick a passphrase of at least {moving.MIN_PASSPHRASE} characters.')
        if keys and not passphrase:
            raise OwnerError('Keys and tokens need a passphrase you pick.')
        with self._export_lock():
            job = self._export_job()
            if job.get('state') == 'running':
                return {'started': False, 'export': self.export_view()}
            self._export_shred()
            job.clear()
            job.update(state='running', started=time.time(), keys=keys, id=secrets.token_urlsafe(18))
            threading.Thread(target=self._export_run, args=(passphrase, keys, job), name='export', daemon=True).start()
        return {'started': True, 'export': self.export_view()}

    def _export_run(self, passphrase, keys, job):
        out = self._export_root() / 'out'
        try:
            path, manifest = moving.export(self.config_path, out, passphrase=passphrase, keys=keys,
                                           source='hosted' if self._hosted() else 'local', **self.export_paths)
            summary = {'name': path.name, 'id': job['id'], 'created_at': manifest.get('created_at'), 'bytes': path.stat().st_size,
                       'includes_keys': bool(manifest.get('includes_keys')), 'parts': manifest.get('parts') or {},
                       'not_exported': manifest.get('not_exported') or [], 'code': bool(manifest.get('code'))}
            target = out / 'export.json'
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, 'w') as handle:
                handle.write(json.dumps(summary))
            job.update(state='ready', code=manifest.get('code'), finished=time.time())
            timer = threading.Timer(KEEP_HOURS * 3600 + 60, self._export_expire, args=(job['id'],))
            timer.daemon = True
            timer.start()
            LOG.info('export ready bytes=%d', summary['bytes'])
        except moving.MoveError as error:
            job.update(state='failed', error=str(error))
        except Exception as error:  # noqa: BLE001 - a failed export says so in Settings, never stops the service
            LOG.error('export failed error=%s', type(error).__name__)
            job.update(state='failed', error='The export didn’t finish. Try again.')

    def _export_expire(self, export_id):
        _, summary = self._export_file()  # shreds one past its time
        if summary and summary.get('id') == export_id and self._export_job().get('state') != 'running':
            self._export_shred()

    def export_view(self):
        """The export's state for Settings, Export: None, running (with the bytes written so far), failed, or ready."""
        job = self._export_job()
        if job.get('state') == 'running':
            written = 0
            for folder in (self._export_root() / 'out').glob('.the-machine-export-*'):
                written += sum(f.stat().st_size for f in folder.glob('*.enc') if f.is_file())
            return {'state': 'running', 'started_at': _when(job['started']), 'bytes': written, 'size': human(written)}
        if job.get('state') == 'failed':
            return {'state': 'failed', 'error': job.get('error') or ''}
        path, summary = self._export_file()
        if not summary:
            return None
        made = path.stat().st_mtime
        view = {'state': 'ready', 'id': summary.get('id'), 'name': summary.get('name'), 'bytes': summary.get('bytes'),
                'size': human(summary.get('bytes') or 0), 'created_at': summary.get('created_at'),
                'until': _when(made + KEEP_HOURS * 3600), 'includes_keys': bool(summary.get('includes_keys')),
                'parts': parts_view(summary.get('parts')), 'not_exported': not_view(summary.get('not_exported')),
                'with_code': bool(summary.get('code'))}
        if summary.get('code') and job.get('id') == summary.get('id') and job.get('code'):
            view['code'] = job['code']  # kept in memory only; after a restart the owner has the one they wrote down
        return view

    def export_status_action(self, name, args, owner_dashboard):
        self._owner_only(owner_dashboard)
        return self.export_status()

    def export_status(self):
        hosted = self._hosted()
        view = {'hosted': hosted, 'export': None if hosted else self.export_view(), 'import': self.import_view()}
        if not hosted:
            view['restart'] = staged_import.can_restart()
            view['commands'] = self.import_commands()  # shown when it can't restart itself
        return view

    def export_delete_action(self, name, args, owner_dashboard):
        self._owner_only(owner_dashboard)
        with self._export_lock():
            if self._export_job().get('state') == 'running':
                raise OwnerError('The export is still running. Delete it once it’s done.')
            self._export_shred()
            self._export_job().clear()
        return self.export_status()

    def export_download(self, handler, query):
        """GET /api/export-download?id=...: the finished export, streamed to the owner (Handler.do_GET checked owner())."""
        path, summary = self._export_file()
        wanted = urllib.parse.parse_qs(query).get('id', [''])[0]
        if not summary or not wanted or not secrets.compare_digest(str(summary.get('id') or ''), wanted):
            handler.output(404, {'error': 'That export is gone. Export again.'})
            return
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/octet-stream')
        handler.send_header('Content-Disposition', "attachment; filename*=UTF-8''" + urllib.parse.quote(path.name))
        handler.send_header('Content-Length', str(path.stat().st_size))
        handler.send_header('Cache-Control', 'no-store')
        handler.send_header('X-Content-Type-Options', 'nosniff')
        handler.send_header('Referrer-Policy', 'no-referrer')
        handler.send_header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'; sandbox")
        handler.end_headers()
        try:
            with open(path, 'rb') as source:
                while chunk := source.read(CHUNK):
                    handler.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError, OSError):
            handler.close_connection = True

    # --- import ----------------------------------------------------------------------------------------------------

    def _upload_path(self):
        folder = self._export_root() / 'in'
        folder.mkdir(mode=0o700, exist_ok=True)
        return folder / UPLOAD_NAME

    def import_commands(self):
        """What a self-hosted owner runs to put a staged import in place: the service can't stop itself."""
        has_sources = bool((getattr(self, 'config', None) or {}).get('accounts'))
        return [COMMANDS[0], COMMANDS[1] + (' --force' if has_sources else ''), COMMANDS[2]]

    def import_upload(self, handler, dashboard):
        """POST /api/import-upload: the export file as the request body, written to a private folder in chunks."""
        if not dashboard:
            handler.output(403, {'error': 'Unauthorized'})
            return
        try:
            size = int(handler.headers.get('Content-Length') or 0)
        except ValueError:
            size = 0
        try:
            self._owner_only(dashboard)
            if size <= 0:
                raise OwnerError('Pick an export file.')
            if self._import_job().get('state') == 'checking':
                raise OwnerError('An export is being checked. Wait for it, or discard it.')
            target = self._upload_path()
            free = shutil.disk_usage(target.parent).free
            if free < size * UPLOAD_ROOM + UPLOAD_SPARE:
                raise OwnerError(f'Not enough free disk space for this export. It needs about {human(size * UPLOAD_ROOM + UPLOAD_SPARE)} free.')
        except ValueError as error:
            handler.close_connection = True  # the body is not read
            handler.output(400, {'error': str(error)})
            return
        name = re.sub(r'[^\w.\- ]', '', urllib.parse.unquote(handler.headers.get('X-File-Name') or ''))[:120] or UPLOAD_NAME
        with self._export_lock():
            moving.discard_staged(self.config_path)
            portable.shred(target)
            self._import_job().clear()
        partial = target.with_name(UPLOAD_NAME + '.part')
        portable.shred(partial)
        done = 0
        try:
            fd = os.open(partial, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'wb') as out:
                while done < size:
                    chunk = handler.rfile.read(min(CHUNK, size - done))
                    if not chunk:
                        raise OSError('short upload')
                    out.write(chunk)
                    done += len(chunk)
            os.replace(partial, target)
        except OSError:
            portable.shred(partial)
            handler.close_connection = True
            try:
                handler.output(400, {'error': 'The upload didn’t finish. Try again.'})
            except OSError:
                pass
            return
        self._import_job().update(state='uploaded', name=name, bytes=size, at=time.time())
        handler.output(200, self.export_status())

    def import_stage_action(self, name, args, owner_dashboard):
        """Open and check the uploaded export with its passphrase or export code, in a thread (moving.stage)."""
        self._owner_only(owner_dashboard)
        passphrase = args.get('passphrase')
        if not isinstance(passphrase, str) or not passphrase.strip():
            raise OwnerError('Type the passphrase or export code of this export.')
        with self._export_lock():
            job = self._import_job()
            if job.get('state') == 'checking':
                return self.export_status()
            if not self._upload_path().is_file():
                raise OwnerError('Upload the export file again.')
            job.update(state='checking', error='')
            threading.Thread(target=self._import_check, args=(passphrase.strip(), job), name='import-check', daemon=True).start()
        return self.export_status()

    def _import_check(self, passphrase, job):
        upload = self._upload_path()
        try:
            moving.stage(upload, self.config_path, passphrase)
            portable.shred(upload)
            job.update(state='staged')
        except moving.MoveError as error:
            job.update(state='uploaded', error=str(error))  # the upload stays: try the passphrase again
        except Exception as error:  # noqa: BLE001 - says so in Settings, never stops the service
            LOG.error('import check failed error=%s', type(error).__name__)
            job.update(state='uploaded', error='That file is not an export The Machine can open.')

    def import_view(self):
        """None, uploaded (waiting for its passphrase, with the last try's error), checking, staged with its summary (and
        why the last import at the start didn't go through), confirmed, or imported after the restart."""
        job = self._import_job()
        if job.get('state') == 'checking':
            return {'state': 'checking', 'name': job.get('name')}
        summary = moving.staged(self.config_path) if getattr(self, 'config_path', None) else None
        done = staged_import.result(self.config_path) if getattr(self, 'config_path', None) else None
        if done and done.get('state') == 'imported' and not summary:
            return {k: done.get(k) for k in ('state', 'at', 'created_at', 'source', 'sends', 'boards', 'reconnect')}
        if summary:
            return {'state': 'confirmed' if summary.get('confirmed') else 'staged', 'created_at': summary.get('created_at'),
                    'error': (done or {}).get('error') if (done or {}).get('state') == 'failed' and not summary.get('confirmed') else '',
                    'source': summary.get('source'), 'includes_keys': bool(summary.get('includes_keys')),
                    'parts': parts_view(summary.get('parts')), 'not_exported': not_view(summary.get('not_exported')),
                    'replaces': bool((getattr(self, 'config', None) or {}).get('accounts'))}
        upload = self._upload_path() if getattr(self, 'config_path', None) else None
        if upload and upload.is_file():
            if time.time() - upload.stat().st_mtime > moving.STAGED_HOURS * 3600:
                portable.shred(upload)
                job.clear()
                return None
            return {'state': 'uploaded', 'name': job.get('name') or UPLOAD_NAME, 'bytes': upload.stat().st_size,
                    'size': human(upload.stat().st_size), 'error': job.get('error') or ''}
        return None

    def import_discard_action(self, name, args, owner_dashboard):
        self._owner_only(owner_dashboard)
        with self._export_lock():
            if self._import_job().get('state') == 'checking':
                raise OwnerError('The export is being checked. Discard it once that’s done.')
            moving.discard_staged(self.config_path)
            staged_import.forget(self.config_path)
            portable.shred(self._upload_path())
            self._import_job().clear()
        return self.export_status()

    def import_confirm_action(self, name, args, owner_dashboard):
        """Import now. Hosted: the server applies it with the service stopped and starts it again. Self-hosted: the
        service restarts itself and applies it at its start (machine/export/staged.py); without a service manager the
        commands in the status do that."""
        self._owner_only(owner_dashboard)
        hosted = self._hosted()
        if not hosted and not staged_import.can_restart():
            raise OwnerError('Run the commands below to finish the import.')
        with self._export_lock():
            try:
                staged_import.confirm(self.config_path)
            except moving.MoveError as error:
                raise ValueError(str(error)) from None
            if not hosted and not staged_import.restart(3):
                staged_import.unconfirm(self.config_path)
                raise OwnerError('The Machine couldn’t restart itself. Run the commands below to finish the import.')
        LOG.info('import confirmed hosted=%s', hosted)
        return {**self.export_status(), 'restarting': not hosted}
