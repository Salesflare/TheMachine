"""The night pause lets go only for the owner (machine/night_pause.py, notify.mark_active): requests a page or the
browser makes by itself (a status poll, the push subscription a page renews on load, the service worker's fetches), a
page in the background and a headless browser never wake the night's reviews; a page the owner really uses does,
through the real web server."""
import datetime as dt
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import assistant as a
from machine import timing
from machine.web.serving import dashboard_csrf
import notify
from seams import patch_everywhere
import served
import timeutil

SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}
CHROME = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
HEADLESS = CHROME.replace('Chrome/', 'HeadlessChrome/')


class NightPresence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop('ASSISTANT_QUIET_HOURS', None)
        timeutil.set_work_hours({})
        self.addCleanup(timeutil.set_work_hours, {})
        notify.reset_active()
        self.addCleanup(notify.reset_active)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 'events.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443',
                           'port': 0, 'http_timeout': 1, 'digest_at': '08:30', 'review_worker': {'enabled': True}}
        # 03:00 on a night long after setup, with a review done before: the pause holds
        self.night = dt.datetime(2026, 11, 18, 3, tzinfo=timeutil.local_tz())
        old = (self.night - dt.timedelta(days=8)).astimezone(dt.timezone.utc).isoformat()
        with self.app.store.connect() as db:
            db.execute("UPDATE milestones SET at=? WHERE name='tracking_since'", (old,))
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at) VALUES(?, 'ok', ?, ?, ?)", ('0' * 32, old, old, old))
        clock = patch.object(notify, 'time', wraps=notify.time)  # the pages' heartbeats land at 03:00
        clock.start().time.return_value = self.night.timestamp()
        self.addCleanup(clock.stop)
        inline = patch_everywhere(timing, 'aside', new=lambda write, what, once=True: write())  # no side thread to outlive the test
        inline.start()
        self.addCleanup(inline.stop)
        self.port = served.serve(self, a)
        self.owner = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com', 'User-Agent': CHROME}

    def request(self, method, path, body=None, headers=None):
        headers = {**self.owner, **(headers or {})}
        if method == 'POST':
            headers.update({'Content-Type': 'application/json', 'Origin': 'https://machine.example:8443',
                            'X-CSRF-Token': dashboard_csrf('test-token', 'owner@example.com')})
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        conn.request(method, path, json.dumps(body) if body is not None else None, headers)
        response = conn.getresponse()
        response.read()
        conn.close()
        return response.status

    def action(self, name, args, **headers):
        self.assertEqual(self.request('POST', '/api/action', {'action': name, 'args': args}, headers), 200)

    def held(self):
        """The night pause still holds the reviews of new signals five minutes later."""
        with self.app.store.connect() as db:
            return self.app.night_hold(db, (self.night + dt.timedelta(minutes=5)).astimezone(dt.timezone.utc)) is not None

    def test_a_status_poll_does_not_wake_the_reviews(self):
        self.assertEqual(self.request('GET', '/api/session'), 200)
        self.assertEqual(self.request('GET', '/api/status'), 200)
        self.assertTrue(self.held())

    def test_the_push_subscription_a_page_renews_on_load_does_not_wake_the_reviews(self):
        self.action('push_subscribe', SUB)
        self.assertTrue(self.held())

    def test_the_service_worker_s_fetches_do_not_wake_the_reviews(self):
        for path in ('/', '/sw.js', '/manifest.webmanifest'):
            self.assertEqual(self.request('GET', path, headers={'Service-Worker': 'script'} if path == '/sw.js' else None), 200, path)
        self.assertTrue(self.held())

    def test_a_page_in_the_background_does_not_wake_the_reviews(self):
        self.action('notify_active', {'client': 'hidden1', 'active': False, 'idle': 86400})
        self.assertTrue(self.held())

    def test_a_headless_browser_does_not_wake_the_reviews(self):
        self.action('notify_active', {'client': 'robot1', 'active': True}, **{'User-Agent': HEADLESS})
        self.assertFalse(notify.active())
        self.assertTrue(self.held())

    def test_the_owner_using_a_page_at_night_wakes_the_reviews(self):
        self.action('notify_active', {'client': 'desk1', 'active': True})
        self.assertTrue(notify.active())
        self.assertFalse(self.held())  # their to-dos come right away, as by day


if __name__ == '__main__':
    unittest.main()
