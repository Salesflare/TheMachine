import unittest
import test_ux as ux
a=ux.a

class StartedAt(unittest.TestCase):
    setUp=ux.UX.setUp
    def app(self, **config):
        app=object.__new__(a.App);app.store=self.store
        app.config={'accounts':[{'id':'work','email':'owner@example.com','boundary':'work:Acme'}],'telegram_owner':'1000001',**config}
        return app
    def test_first_own_activity_is_the_start(self):
        with self.store.connect() as db:
            first=db.execute('SELECT MIN(created_at) FROM suggestions').fetchone()[0]
        self.assertTrue(first)
        started=self.app().action('status',{'full':True})['started_at']
        self.assertTrue(started and started<=first)  # the first analysis, suggestion or sync, whichever came first
    def test_a_configured_start_wins(self):
        self.assertEqual(self.app(started_at='2026-10-01T09:00:00+00:00').action('status',{'full':True})['started_at'],'2026-10-01T09:00:00+00:00')

if __name__=='__main__':unittest.main()
