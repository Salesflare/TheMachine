"""While the service waits for the message key (refactor PR 19): the page the dashboard's address answers with, and
the keeper that holds the key once it arrives. Moved out of assistant.py as is."""
import html
import http.server
import json
from pathlib import Path
import threading
import time

from machine.config import LOG
import message_seal


class KeyWaitingPage:
    """While the service waits for the message key from the keyring (message_seal.wait_for_key), the dashboard's
    address answers with why and that it starts by itself, instead of not answering at all. Nothing private: no data
    is open yet. Called with the reason while it waits, with None when it is over (the app then takes the port)."""

    def __init__(self, config):
        self.config, self.server, self.reason = config, None, ''

    def __call__(self, reason):
        if reason is None:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                self.server = None
            return
        self.reason = reason
        if self.server:
            return
        page = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                text = ('The Machine is waiting for its message key from your keyring: ' + page.reason + '. '
                        'It starts by itself once the keyring can be read. Unlock the keyring or sign in to the desktop. '
                        'Details: assistant message-key status')
                if self.path.startswith('/api/') or self.path == '/health':
                    body, kind = json.dumps({'ok': False, 'waiting': 'message-key', 'error': text}).encode(), 'application/json'
                else:
                    body = ('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width">'
                            '<meta http-equiv=refresh content=15><title>The Machine</title>'
                            '<p style="font:16px system-ui;max-width:32em;margin:3em auto;padding:0 1em">' + html.escape(text) + '</p>').encode()
                    kind = 'text/html'
                self.send_response(503)
                self.send_header('Content-Type', kind + '; charset=utf-8')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Retry-After', '15')
                self.end_headers()
                self.wfile.write(body)

            do_POST = do_GET

        try:
            self.server = http.server.ThreadingHTTPServer(('127.0.0.1', self.config.get('port', 8787)), Handler)
        except OSError:
            return  # the port is taken: the log says why it waits
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, name='key-waiting-page', daemon=True).start()


def message_key_keeper(config, every=60):
    """A key in the keyring (message_keyring.py): "message_key_store": "keyring" moves a key file there once the
    keyring checks out; while the service runs, the runtime file the Gateway's plugin reads is put back from memory
    if it goes (the keyring itself is not asked again)."""
    database = Path(config['database']).expanduser() if config.get('database') else None
    if not database:
        return
    import message_keyring
    if config.get('message_key_store') == 'keyring' and not message_seal.in_keyring(database) \
            and message_seal.key_path(database).is_file() and not message_seal.held_elsewhere(database):
        try:
            message_keyring.to_keyring(database, say=LOG.info)
        except (message_keyring.Unavailable, message_seal.SealError, OSError) as error:
            LOG.warning('message key stays in its file: %s', error)
    if message_seal.in_keyring(database):
        try:
            message_keyring.settle(database)
        except (OSError, ValueError):
            pass

        def keep():
            while True:
                time.sleep(every)
                try:
                    message_seal.load_key(database)
                except (OSError, ValueError):
                    pass
        threading.Thread(target=keep, name='message-key-keeper', daemon=True).start()
