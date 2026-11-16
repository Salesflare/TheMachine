"""Run the app's real web server (App.serve) in a test, and stop it completely before the test's folder goes.

`port = serve(self)` starts `App.serve` on `self.app` in a thread and returns the port it listens on. serve()
also starts the account readers and every background worker; tests over the request handler need none of them, and
they would write into the test's temporary folder, also while it is removed after the test ("Directory not empty").
So they are stubbed, the error log serve() hangs on the shared logger comes off again, and on cleanup serve() and every
thread it started (the server's request threads too) are joined, with a check that each stopped and the server closed.

Register the temporary folder's cleanup before calling this: cleanups run last in, first out, so this one runs first."""
import signal
import threading
from unittest.mock import patch

from machine.config import LOG
import machine.main as machine_main
import machine.web.loopback as machine_web_loopback

# What serve() starts besides the web server (machine/app/serve.py)
BACKGROUND = ('collector', 'ability_checker', 'delivery_worker', 'preparation_worker', 'whatsapp_photo_worker',
              'voice_warm_worker', 'action_worker', 'review_worker', 'graph_worker', 'model_usage_worker', 'retention_worker',
              'plain_keys_worker', 'history_worker', 'embedding_worker', 'enrichment_worker', 'linkedin_connections_worker',
              'recurring_worker', 'routines_worker', 'protection_waiter', 'routine_templates_start', 'meeting_write_resume',
              'gbrain_start')


def serve(test, a=None, patches=()):
    """Start `test.app` serving, with `patches` (more patchers) on for the whole test; the port it listens on. `a`, an
    assistant module some tests still pass, is not read: App, LOG and signal are the same objects in it."""
    import machine.app.serve as serve_module
    servers, started = [], threading.Event()
    real_server, real_watch = machine_web_loopback.Server, serve_module.watch_faults

    def capture(*args, **kwargs):
        servers.append(real_server(*args, **kwargs))
        started.set()
        return servers[-1]

    def watch(store, *args):  # its error log hangs on the shared logger and writes into this test's database: it comes off
        hook = threading.excepthook
        log = real_watch(store, *args)

        def unwatch():
            LOG.removeHandler(log)
            threading.excepthook = hook
        test.addCleanup(unwatch)
        return log
    for patcher in (patch.object(serve_module, 'watch_faults', side_effect=watch),
                    patch.object(machine_web_loopback, 'Server', side_effect=capture), patch.object(signal, 'signal'),
                    patch('machine.store.review_requeue.requeue', return_value=0),
                    *(patch.object(machine_main.App, name) for name in BACKGROUND), *patches):
        patcher.start()
        test.addCleanup(patcher.stop)
    before = set(threading.enumerate())
    thread = threading.Thread(target=test.app.serve, daemon=True)
    thread.start()
    test.assertTrue(started.wait(10), 'serve() did not start its server')

    def stop():  # serve() ends within its server's 1 s timeout and closes it (server_close); then what it started
        test.app.stop.set()
        thread.join(10)
        test.assertFalse(thread.is_alive(), 'serve() still running after the test')
        for other in set(threading.enumerate()) - before:
            other.join(10)
            test.assertFalse(other.is_alive(), f'{other.name} still running after the test')
        test.assertEqual(servers[0].socket.fileno(), -1, 'serve() did not close its server')
    test.addCleanup(stop)
    return servers[0].server_address[1]
