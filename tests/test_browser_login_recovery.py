import tempfile, threading, unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
import browser_login

class Recovery(unittest.TestCase):
    def test_two_owner_requests_do_not_lose_saved_signins(self):
        with tempfile.TemporaryDirectory() as folder:
            a,b=browser_login.LoginStore(folder),browser_login.LoginStore(folder)
            a._key()
            gate=threading.Barrier(2)
            original=browser_login.LoginStore._read
            def read(obj):
                value=original(obj)
                try:gate.wait(timeout=.3)
                except threading.BrokenBarrierError:pass
                return value
            with patch.object(browser_login.LoginStore,'_read',read),ThreadPoolExecutor(2) as ex:
                futures=[ex.submit(a.save,'one.example.invalid','one','fake-one'),ex.submit(b.save,'two.example.invalid','two','fake-two')]
                for future in futures:future.result()
            self.assertEqual({x['site'] for x in a.list()},{'one.example.invalid','two.example.invalid'})

    def test_failed_observation_after_submit_is_not_reported_as_signedin(self):
        class Tab:
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def run(self,fn,*args):
                if fn=='('+browser_login.DETECT+')':return {'host':'example.invalid','secure':True,'password':True,'username':False,'code':False}
                if fn==browser_login.FOCUS:return 'ok'
                if fn==browser_login.SUBMIT:return 'clicked'
                return 'moved'
            def call(self,*a):return {}
        with patch.object(browser_login.browser_cdp,'Session',return_value=Tab()),patch.object(browser_login.browser_cdp,'evaluate',side_effect=browser_login.browser_cdp.CdpError('unreachable')),patch.object(browser_login.time,'sleep'):
            with self.assertRaisesRegex(ValueError,'confirm|verify|answer'):
                browser_login.fill({},'0:tab','example.invalid',password='fake',settle=0)
