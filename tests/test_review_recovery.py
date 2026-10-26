import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)


def event(account, number, body='Full evidence'):
    return {'account_id':account, 'source_id':str(number), 'kind':'slack.message',
            'occurred_at':f'2026-10-09T10:{number%60:02}:00+00:00', 'title':'A signal',
            'body':body, 'metadata':{}, 'deleted':False}


class ReviewRecovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name)/'events.sqlite')

    def test_same_run_retry_resumes_exact_claim_and_keeps_error(self):
        self.store.commit_page('work',{},[event('work',1)])
        first=self.store.begin_analysis(['work'],owner_session='private',owner_run='one')
        self.store.review_failed('private','one','ai_connection_reset')
        replay=self.store.begin_analysis(['work'],owner_session='private',owner_run='one')
        self.assertEqual(first['analysis_id'],replay['analysis_id'])
        self.assertTrue(replay['resumed'])
        self.store.finish_analysis(replay['analysis_id'],'Real conclusion','private','one')
        row=self.store.snapshot([])['analyses'][0]
        self.assertEqual(row['last_error'],'ai_connection_reset')
        self.assertEqual(row['attempts'],2)
        self.assertEqual(self.store.events(['work'],pending=True),[])

    def test_terminal_failure_next_run_resumes_immediately_old_run_cannot_commit(self):
        self.store.commit_page('work',{},[event('work',1)])
        first=self.store.begin_analysis(['work'],owner_session='private',owner_run='one')
        self.store.review_failed('private','one','ai_timeout')
        self.store.review_failed('private','one','run_interrupted',terminal=True)
        self.assertTrue(self.store.begin_analysis(['work'],owner_session='other',owner_run='two')['busy'])
        replay=self.store.begin_analysis(['work'],owner_session='private',owner_run='two')
        self.assertEqual(replay['last_error'],'ai_timeout')
        with self.assertRaises(ValueError):self.store.finish_analysis(first['analysis_id'],'stale','private','one')
        self.store.finish_analysis(first['analysis_id'],'Real conclusion','private','two')

    def test_resume_refreshes_changed_content_and_incomplete_ids_stay_pending(self):
        self.store.commit_page('work',{},[event('work',1),event('work',2)])
        first=self.store.begin_analysis(['work'],owner_session='private',owner_run='one')
        self.store.commit_page('work',{},[event('work',1,'New evidence')])
        replay=self.store.begin_analysis(['work'],owner_session='private',owner_run='one')
        changed=next(r for r in replay['events'] if r['source_id']=='1')
        self.assertEqual(changed['body'],'New evidence')
        self.store.finish_analysis(first['analysis_id'],'Only one assessed','private','one',[changed['id']])
        self.assertEqual([r['source_id'] for r in self.store.events(['work'],pending=True)],['2'])
        self.assertEqual(self.store.snapshot([])['analyses'][0]['checked_count'],1)

    def test_weighted_backlog_without_starving_small_account_or_old_signals(self):
        self.store.commit_page('busy',{},[event('busy',i) for i in range(100)])
        self.store.commit_page('small',{},[event('small',1)])
        batch=self.store.begin_analysis(['small','busy'],limit=40)
        self.assertEqual(len(batch['events']),40)
        self.assertEqual(sum(r['account_id']=='small' for r in batch['events']),1)
        self.assertIn('0',[r['source_id'] for r in batch['events'] if r['account_id']=='busy'])
        self.assertIn('59',[r['source_id'] for r in batch['events'] if r['account_id']=='busy'])
        self.assertEqual(len({r['id'] for r in batch['events']}),40)

    def test_abandoned_claim_remainder_gets_priority_and_recovery_count_is_real(self):
        self.store.commit_page('work',{},[event('work',i) for i in range(8)])
        first=self.store.begin_analysis(['work'],limit=2)
        old_ids={r['id'] for r in first['events']}
        with self.store.connect() as db:db.execute("UPDATE analyses SET started_at='2020-01-01' WHERE id=?",(first['analysis_id'],))
        self.store.commit_page('work',{},[event('work',99)])
        retry=self.store.begin_analysis(['work'],limit=2)
        self.assertEqual({r['id'] for r in retry['events']},old_ids)
        self.store.finish_analysis(retry['analysis_id'],'Assessed')
        historical=next(r for r in self.store.snapshot([])['analyses'] if r['id']==first['analysis_id'])
        self.assertEqual(historical['remaining_count'],0)

    def test_preview_explicit_and_exact_full_context_account_scoped(self):
        body='Evidence ' * 600
        self.store.commit_page('work',{},[event('work',1,body)])
        preview=self.store.begin_analysis(['work'])['events'][0]
        self.assertTrue(preview['body_clipped'])
        full=self.store.events(['work'],event_ids=[preview['id']])[0]
        self.assertEqual(full['body'],body)
        self.assertEqual(self.store.events(['other'],event_ids=[preview['id']]),[])

    def test_run_signal_budget_cannot_be_expanded_by_model_limit(self):
        self.store.commit_page('work',{},[event('work',i) for i in range(150)])
        batch=self.store.begin_analysis(['work'],limit=10000,owner_session='private',owner_run='one')
        self.assertEqual(len(batch['events']),120)
        self.store.finish_analysis(batch['analysis_id'],'Assessed','private','one')
        self.assertTrue(self.store.begin_analysis(['work'],owner_session='private',owner_run='one')['budget_exhausted'])
        self.assertEqual(len(self.store.events(['work'],limit=100,pending=True)),30)

    def test_smaller_claims_share_one_run_budget(self):
        self.store.commit_page('work',{},[event('work',i) for i in range(150)])
        sizes=[]
        for _ in range(3):
            batch=self.store.begin_analysis(['work'],limit=50,owner_session='private',owner_run='one')
            sizes.append(len(batch['events']))
            self.store.finish_analysis(batch['analysis_id'],'Assessed','private','one')
        self.assertEqual(sizes,[50,50,20])
        self.assertTrue(self.store.begin_analysis(['work'],owner_session='private',owner_run='one')['budget_exhausted'])

    def review(self, run, reviewed_ids, limit=10):
        batch=self.store.begin_analysis(['work'],limit=limit,owner_session='private',owner_run=run)
        self.store.finish_analysis(batch['analysis_id'],'Assessed','private',run,reviewed_ids(batch))
        return [e['id'] for e in batch['events']]

    def test_repeatedly_deferred_signal_is_set_aside_until_it_changes(self):
        self.store.commit_page('work',{},[event('work',i) for i in range(3)])
        stuck=self.store.events(['work'],limit=10)[-1]['id']
        defer_stuck=lambda batch:[e['id'] for e in batch['events'] if e['id']!=stuck]
        self.assertIn(stuck,self.review('one',defer_stuck))
        self.store.commit_page('work',{},[event('work',i) for i in range(3,6)])
        self.assertIn(stuck,self.review('two',defer_stuck))
        self.store.commit_page('work',{},[event('work',i) for i in range(6,9)])
        self.assertNotIn(stuck,self.review('three',defer_stuck))
        status=self.store.snapshot([{'id':'work','email':'w','boundary':'work:x'}])['review_health']
        self.assertEqual((status['pending'],status['set_aside']),(1,1))
        self.assertEqual(len(self.store.events(['work'],event_ids=[stuck])),1)  # still readable
        self.store.commit_page('work',{},[event('work',0,'Changed evidence')])
        self.assertIn(stuck,self.review('four',lambda b:[e['id'] for e in b['events']]))

    def test_deferred_signal_waits_behind_fresh_backlog(self):
        self.store.commit_page('work',{},[event('work',i) for i in range(4)])
        first=self.review('one',lambda b:[e['id'] for e in b['events'][1:]],limit=2)
        deferred=first[0]
        self.store.commit_page('work',{},[event('work',i) for i in range(4,8)])
        self.assertNotIn(deferred,self.review('two',lambda b:[e['id'] for e in b['events']],limit=2))

    def test_large_claim_is_paged_under_the_tool_result_limit(self):
        self.store.commit_page('work',{},[event('work',i,'Long evidence text. '*400) for i in range(120)])
        batch=self.store.begin_analysis(['work'],limit=120,owner_session='private',owner_run='one')
        self.assertEqual(batch['claimed'],120);self.assertGreater(batch['pages'],1)
        seen=[e['id'] for e in batch['events']]
        self.assertLess(len(assistant.encoded(batch)),assistant.REVIEW_PAGE_CHARS+3000)
        for page in range(1,batch['pages']):
            result=self.store.analysis_page(batch['analysis_id'],page)
            self.assertLess(len(assistant.encoded(result)),assistant.REVIEW_PAGE_CHARS+3000)
            seen+=[e['id'] for e in result['events']]
        self.assertEqual(len(set(seen)),120)
        self.assertEqual(len(seen),120)
        first=batch['events'][0]
        self.assertTrue(first['body_clipped']);self.assertEqual(first['body_chars'],len(('Long evidence text. '*400).strip()))
        self.assertNotIn('content_hash',first)

    def test_bookkeeping_metadata_is_left_out_of_reviews(self):
        e=event('work',1);e['metadata']={'from':'Ann','coverage':'long note','transport':'x','source_url':'https://x','truncated':False}
        self.store.commit_page('work',{},[e])
        view=self.store.begin_analysis(['work'])['events'][0]
        self.assertEqual(view['metadata'],{'from':'Ann'})

    def test_event_reads_fit_and_long_text_can_be_read_in_parts(self):
        body='word '*20000
        self.store.commit_page('work',{},[event('work',i,body) for i in range(5)])
        rows=self.store.events(['work'],limit=5)
        views=assistant.fit_events(rows)
        self.assertLess(len(assistant.encoded(views)),assistant.REVIEW_PAGE_CHARS)
        self.assertTrue(all(v['body_clipped'] for v in views))
        part=assistant.fit_events(rows[:1],offset=30000)[0]
        self.assertEqual(part['body_offset'],30000);self.assertTrue(part['body'].startswith('word'))
        small=assistant.fit_events(self.store.events(['work'],limit=1))
        self.assertTrue(small[0].get('body_clipped'))  # 100,000 characters never fit whole

    def test_all_120_exact_ids_are_readable_with_bounded_continuation(self):
        records=[event('work',i,'Evidence \\"\\\\ '+('long '*600)) for i in range(120)]
        for e in records:e['metadata']={f'context-{i}':'large '*100 for i in range(100)}
        self.store.commit_page('work',{},records)
        ids=list(range(1,121))
        rows=self.store.events(['work'],event_ids=ids)  # explicit IDs override default list limit
        self.assertEqual({r['id'] for r in rows},set(ids))
        self.assertEqual(self.store.events(['other'],event_ids=ids),[])
        remaining=rows;seen=[]
        while remaining:
            page=assistant.event_page(remaining)
            self.assertLessEqual(len(assistant.encoded(page)),assistant.REVIEW_PAGE_CHARS)
            self.assertTrue(page['events'])
            seen.extend(e['id'] for e in page['events'])
            self.assertTrue(all(e.get('metadata_clipped') for e in page['events']))
            remaining=[r for r in rows if r['id'] in page['remaining_event_ids']]
        self.assertEqual(len(seen),120);self.assertEqual(set(seen),set(ids))
        page=assistant.event_page(rows,row_offset=119)
        self.assertEqual([e['id'] for e in page['events']],[rows[119]['id']])
        self.assertIsNone(page['next_row_offset'])
        with self.assertRaises(ValueError):assistant.event_page(rows,row_offset=-1)

    def test_body_continuations_reconstruct_every_character_and_version(self):
        text=('A \\" quoted \\\\ string with é漢字 '*3000).strip()
        self.store.commit_page('work',{},[event('work',1,text)])
        rows=self.store.events(['work']);parts=[];offset=0
        while True:
            page=assistant.event_page(rows,offset=offset)
            self.assertLessEqual(len(assistant.encoded(page)),assistant.REVIEW_PAGE_CHARS)
            view=page['events'][0];parts.append(view['body'])
            self.assertEqual(view['version'],rows[0]['version'])
            next_offset=view.get('body_next_offset')
            if next_offset is None:break
            self.assertGreater(next_offset,offset);offset=next_offset
        self.assertEqual(''.join(parts),' '.join(text.split()))

    def test_api_pages_report_unavailable_ids_and_metadata_is_lossless(self):
        e=event('work',1);e['metadata']={'big':'Quoted \\" \\\\ '+('é漢字 '*10000)}
        self.store.commit_page('work',{},[e])
        app=object.__new__(assistant.App);app.store=self.store;app.config={'accounts':[{'id':'work'}]}
        page=app.action('events',{'account_ids':['work'],'event_ids':[1,999]})
        self.assertEqual(page['unavailable_event_ids'],[999])
        self.assertEqual(page['events'][0]['id'],1)
        chunks=[];offset=0
        while True:
            chunk=app.action('events',{'account_ids':['work'],'event_ids':[1],'metadata_offset':offset})
            self.assertLessEqual(len(assistant.encoded(chunk)),assistant.REVIEW_PAGE_CHARS)
            chunks.append(chunk['metadata_text']);offset=chunk['metadata_next_offset']
            if offset is None:break
        self.assertEqual(json.loads(''.join(chunks)),e['metadata'])

    def test_claim_page_that_grows_stays_bounded_and_keeps_all_ids(self):
        self.store.commit_page('work',{},[event('work',i,'Short') for i in range(120)])
        claim=self.store.begin_analysis(['work'],120)
        for i in range(120):
            e=event('work',i,'Now large '*1000);e['metadata']={f'field-{j}':'x'*1000 for j in range(80)}
            self.store.commit_page('work',{},[e])
        offset=0;seen=[]
        while True:
            page=self.store.analysis_page(claim['analysis_id'],0,offset)
            self.assertLessEqual(len(assistant.encoded(page)),assistant.REVIEW_PAGE_CHARS)
            seen.extend(e['id'] for e in page['events'])
            offset=page['next_row_offset']
            if offset is None:break
        self.assertEqual(len(seen),120);self.assertEqual(len(set(seen)),120)

    def test_agent_status_is_compact(self):
        self.store.commit_page('work',{},[event('work',i,'Evidence '*300) for i in range(150)])
        for run in range(30):
            batch=self.store.begin_analysis(['work'],limit=5,owner_session='s',owner_run=str(run))
            if batch.get('analysis_id'):self.store.finish_analysis(batch['analysis_id'],'Summary '*100,'s',str(run))
        full=self.store.snapshot([{'id':'work','email':'w','boundary':'work:x'}])
        full['review_health']['heartbeat']=None
        compact=assistant.compact_status(full)
        self.assertLess(len(assistant.encoded(compact)),len(assistant.encoded(full)))
        self.assertLessEqual(len(compact['recent_reviews']),8)
        self.assertNotIn('items',compact['recent_reviews'][0])

    def test_chat_signals_carry_earlier_messages_from_the_same_conversation(self):
        def msg(n,text,user,channel='D1',minute=0):
            return {'account_id':'work','source_id':f'{channel}:{n}','kind':'slack.message','occurred_at':f'2026-10-06T12:{minute:02}:00+00:00',
                    'title':'t','body':text,'metadata':{'channel_id':channel,'user_id':user},'deleted':False}
        self.store.commit_page('work',{},[msg(1,'I found the email','U_ME',minute=1),msg(2,'which one?','U_OTHER',minute=2),
                                          msg(3,'other chat','U_OTHER','D2',3),msg(4,'wait I am lost','U_OTHER',minute=4)])
        self.store.owner_user_ids={'U_ME'}
        batch=self.store.begin_analysis(['work'],limit=10)
        lost=next(e for e in batch['events'] if e['body']=='wait I am lost')
        self.assertEqual([l.split(' ',2)[2] for l in lost['earlier_in_conversation']],['you: I found the email','U_OTHER: which one?'])

    def test_redacted_error_and_resume_account_boundaries(self):
        self.store.commit_page('work',{},[event('work',1)])
        self.store.commit_page('other',{},[event('other',1)])
        self.store.begin_analysis(['work','other'],owner_session='private',owner_run='one')
        with self.assertRaises(ValueError):self.store.review_failed('private','one','private email body')
        with self.assertRaises(ValueError):self.store.begin_analysis(['work'],owner_session='private',owner_run='one')


if __name__=='__main__':unittest.main()
