import base64,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('assistant_bodies',Path(__file__).parent.parent.joinpath('assistant.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
ACCOUNT={'id':'work','email':'me@example.com'}
def raw(plain='',markup=''):
    parts=[{'mimeType':m,'body':{'data':base64.urlsafe_b64encode(v.encode()).decode()}} for m,v in [('text/plain',plain),('text/html',markup)] if v]
    return {'id':'m1','internalDate':'1791540000000','snippet':'snippet','payload':{'headers':[{'name':'Subject','value':'Hi'}],'parts':parts}}
HISTORY='\r\n'.join('> earlier line %d with some words'%i for i in range(400))

class Scope(unittest.TestCase):
    def test_work_when_any_account_is_work(self):
        accounts=[{'id':'w','boundary':'work:Acme'},{'id':'p','boundary':'personal:phone'},{'id':'g','boundary':'owner:system'}]
        self.assertEqual(a.suggestion_scope('["w","p"]',accounts),'work')
        self.assertEqual(a.suggestion_scope(['p'],accounts),'personal')
        self.assertEqual(a.suggestion_scope('["g"]',accounts),'personal')

    def test_account_scope_overrides_boundary(self):
        accounts=[{'id':'d','boundary':'work:Beta','scope':'personal'},{'id':'w','boundary':'work:Acme'}]
        self.assertEqual(a.suggestion_scope(['d'],accounts),'personal')
        self.assertEqual(a.suggestion_scope(['d','w'],accounts),'work')

    def test_telegram_card_carries_hashtag(self):
        row={'title':'T','body':'B','status':'pending','source_line':'Source: email from Ann','scope':'work'}
        self.assertTrue(a.card(row).endswith('Source: email from Ann · #work'))
        self.assertTrue(a.card({**row,'source_line':None,'scope':'personal'}).endswith('\n\n#personal'))
        self.assertNotIn('#',a.card({**row,'scope':None}))

class ResultLinks(unittest.TestCase):
    def test_link_only_lines_leave_no_gap(self):
        body='Hi\n\n[Plan](memory/assistant/x.md)\n\nNext\nDraft: memory/assistant/y.md\n[A](memory/assistant/a.md) · [B](memory/assistant/b.md)\n\nEnd'
        self.assertEqual(a.strip_result_links(body),'Hi\n\nNext\n\nEnd')

class GroupSender(unittest.TestCase):
    def test_reply_to_is_kept_only_when_present(self):
        message=raw(plain='Hi');message['payload']['headers']+=[
            {'name':'From','value':'"\'Will\' via info@example.com readers" <info@example.com>'},
            {'name':'Reply-To','value':'Will <will@vendor.example>'}]
        self.assertEqual(a.message_event(ACCOUNT,message)['metadata']['reply-to'],'Will <will@vendor.example>')
        self.assertNotIn('reply-to',a.message_event(ACCOUNT,raw(plain='Hi'))['metadata'])

class QuotedHistory(unittest.TestCase):
    def test_reply_headers_in_several_shapes(self):
        for header in ['On Thu, Oct 8, 2026 at 11:28 AM Ann Lee <ann@example.com> wrote:',
                       'On Thu, Oct 8, 2026 at 11:28 AM Ann Lee <\r\nann@example.com> wrote:',
                       'On Mon, Oct 5, 2026 at 11:04 AM Ann Lee <ann@example.com>\r\nwrote:',
                       'Le jeu. 8 oct. 2026 à 11:57, Ann Lee <ann@example.com> a\r\nécrit :',
                       'Op do 8 okt 2026 om 10:00 schreef Ann Lee <ann@example.com>:',
                       'Am Do., 8. Okt. 2026 um 10:00 Uhr schrieb Ann Lee <\r\nann@example.com>:',
                       '-----Original Message-----',
                       'From: Ann Lee <ann@example.com>\r\nSent: Thursday, October 8, 2026 2:44 PM']:
            new,quoted=a.split_quoted_history('Thanks, done.\r\n\r\n'+header+'\r\n'+HISTORY)
            self.assertEqual(new,'Thanks, done.',header);self.assertTrue(quoted.startswith(header[:10]),header)

    def test_nested_headers_and_forwards_are_not_split(self):
        nested='New text\r\n\r\n> On Thu, Ann <ann@example.com> wrote:\r\n> old'
        self.assertEqual(a.split_quoted_history(nested),(nested,''))
        forward='FYI\r\n\r\n---------- Forwarded message ---------\r\nFrom: Ann <ann@example.com>\r\nDate: Thu\r\n\r\nThe content'
        self.assertEqual(a.split_quoted_history(forward),(forward,''))  # Gmail forward: From:/Date:, not a reply
        outlook_forward='FYI\r\n\r\nFrom: Ann <ann@example.com>\r\nSent: Thursday\r\n\r\nThe content'
        self.assertEqual(a.split_quoted_history(outlook_forward,'FW: Contract'),(outlook_forward,''))
        self.assertNotEqual(a.split_quoted_history(outlook_forward,'RE: Contract')[1],'')
        self.assertEqual(a.split_quoted_history('On Thu, Ann <a@b.c> wrote:\r\n> only quote')[1],'')  # nothing new above

    def test_gmail_keeps_new_text_and_start_of_history(self):
        body='Looks good!\r\n\r\nOn Thu, Oct 8, 2026 Ann <ann@example.com> wrote:\r\n'+HISTORY*3
        event=a.message_event(ACCOUNT,raw(plain=body))
        self.assertTrue(event['body'].startswith('Looks good!\n\n[Quoted earlier messages: first 3,000 of'))
        self.assertLess(len(event['body']),3300)
        self.assertFalse(event['metadata']['truncated']);self.assertTrue(event['metadata']['quoted_history_shortened'])
        plain=a.message_event(ACCOUNT,raw(plain='Just a note'))
        self.assertEqual((plain['body'],plain['metadata']['quoted_history_chars']),('Just a note',0))

class HtmlFallback(unittest.TestCase):
    def test_placeholder_text_part_uses_html(self):
        event=a.message_event(ACCOUNT,raw(plain='Plain text version not available',markup='<p>Stress leaves <b>traces</b></p><script>x()</script>'))
        self.assertIn('Stress leaves traces',event['body']);self.assertNotIn('x()',event['body'])
        self.assertIn('the real text',a.message_event(ACCOUNT,raw(markup='<div>the real text</div>'))['body'])

    def test_real_text_part_is_kept(self):
        event=a.message_event(ACCOUNT,raw(plain='Real plain message',markup='<p>Different html</p>'))
        self.assertEqual(event['body'],'Real plain message')


if __name__=='__main__':unittest.main()

class StoredCleanup(unittest.TestCase):
    def test_trims_stored_email_without_changing_review_state(self):
        import tempfile
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        store=a.Store(Path(tmp.name)/'e.sqlite')
        old=a.message_event(ACCOUNT,raw(plain='x'))
        old.update(source_id='m2',body='Agreed.\r\n\r\nOn Thu, Ann <ann@example.com> wrote:\r\n'+HISTORY*4,metadata={'truncated':True})
        store.commit_page('work',{},[old])
        with store.connect() as db:db.execute('UPDATE events SET analyzed_version=1,deferrals=2')
        self.assertEqual(store.trim_stored_quoted_history(),{'trimmed':1,'emails':1})
        with store.connect() as db:row=dict(db.execute('SELECT * FROM events').fetchone())
        self.assertTrue(row['body'].startswith('Agreed.\n\n[Quoted earlier messages'))
        self.assertEqual((row['version'],row['analyzed_version'],row['deferrals']),(1,1,0))
        self.assertFalse(a.json.loads(row['metadata'])['truncated'])
        self.assertEqual(store.trim_stored_quoted_history()['trimmed'],0)  # idempotent
