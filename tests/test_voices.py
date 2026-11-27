"""How the owner writes, per channel: voices learned from their notes, edits and own messages, and what a draft gets.

Voices are a short block per channel (and All). A voice study reads the owner's own messages per channel and writes
each block; a style note on a card rewrites that channel's block; the owner edits them in Settings; a profile run's
channel lines fill empty ones. A preparation gets every voice (its card's channel
marked), the owner's own recent messages on that channel (same conversation first) and earlier edits on that channel
only. A draft the owner answered themselves instead becomes an edit to learn from. All local; nothing is sent."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

from machine.store import outcomes  # noqa: E402
import datetime as dt
import embeddings
import graph
import locale_prefs
import machine.app.preparation as machine_app_preparation
import machine.cards as machine_cards
import machine.main as machine_main
import machine.prompts.bias as machine_prompts_bias
import machine.prompts.profile as machine_prompts_profile
import machine.store.profile as machine_store_profile
import machine.store.voices as machine_store_voices
import timeutil


def mail(source_id, at, body, thread='t1', sender='Sam <sam@example.com>', to='Owner <owner@example.com>', labels=('INBOX',)):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Re: Contract',
            'body': body, 'deleted': False, 'metadata': {'from': sender, 'to': to, 'thread_id': thread, 'labels': list(labels)}}


def chat(source_id, at, body, chat_id='c1', mine=False):
    return {'account_id': 'phone', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': at, 'title': 'Kim',
            'body': body, 'deleted': False, 'metadata': {'chat_id': chat_id, 'from_me': mine, 'chat_name': 'Kim'}}


SENT = dict(sender='Owner <owner@example.com>', to='Sam <sam@example.com>', labels=('SENT',))


class Voices(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}, {'id': 'phone', 'service': 'whatsapp'}]
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts}
        self.store.commit_page('work', {}, [
            mail('in1', '2026-10-01T09:00:00+00:00', 'Can you send the contract?'),
            mail('out1', '2026-10-01T10:00:00+00:00', 'Hey Sam,\n\nHere it is.\n\nRegards,\n\nOwner', **SENT),
            mail('out2', '2026-10-02T10:00:00+00:00', 'Hi Lee,\n\nAll good, thanks!\n\nRegards,\n\nOwner', thread='t2',
                 sender='Owner <owner@example.com>', to='Lee <lee@example.org>', labels=('SENT',)),
        ])
        self.store.commit_page('phone', {}, [
            chat('w1', '2026-10-01T08:00:00+00:00', 'Are you coming tonight?'),
            chat('w2', '2026-10-01T08:05:00+00:00', 'ja tuurlijk, tot straks', mine=True),
            chat('w3', '2026-10-01T08:06:00+00:00', 'Sent a photo', mine=True),
        ])
        self.sid = self.store.suggest('contract', 'Send Sam the contract', 'Sam asked for it.', [1])['id']
        self.chat_sid = self.store.suggest('tonight', 'Answer Kim about tonight', 'Kim asks.', [4])['id']
        self.note = self.store.decide(self.chat_sid, 'other', 'no capitals on whatsapp please', 'n1', 'dashboard')

    def note_id(self):
        with self.store.connect() as db:
            return db.execute("SELECT id FROM decisions WHERE choice='other' AND feedback!=''").fetchone()['id']

    def test_a_style_note_rewrites_that_channels_voice_and_only_owner_input_teaches_it(self):
        with self.assertRaisesRegex(ValueError, 'own written notes'):  # no note: a message can't set how the owner writes
            self.app.action('remember_fact', {'kind': 'voice', 'channel': 'WhatsApp', 'text': 'Formal, full sentences.'})
        with self.assertRaisesRegex(ValueError, 'own written notes'):
            self.app.action('remember_fact', {'kind': 'voice', 'channel': 'WhatsApp', 'text': 'Formal.', 'decision_id': 'nope'})
        saved = self.app.action('remember_fact', {'kind': 'voice', 'channel': 'whatsapp', 'text': 'Short lowercase Flemish, no capitals.',
                                                  'decision_id': self.note_id()})
        self.assertEqual(saved, {'channel': 'WhatsApp', 'text': 'Short lowercase Flemish, no capitals.'})
        # The next note rewrites the whole line, it doesn't pile up beside it.
        self.app.action('remember_fact', {'kind': 'voice', 'channel': 'WhatsApp', 'text': 'Short lowercase Flemish, no capitals, no full stop at the end.',
                                          'decision_id': self.note_id()})
        self.assertEqual([(v['channel'], v['text'], v['source']) for v in self.store.voices()],
                         [('WhatsApp', 'Short lowercase Flemish, no capitals, no full stop at the end.', 'assistant')])
        with self.assertRaisesRegex(ValueError, 'short block'):
            self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': 'x' * 451, 'decision_id': self.note_id()})
        with self.assertRaisesRegex(ValueError, 'short block'):
            self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': '\n'.join(['Short.'] * 6), 'decision_id': self.note_id()})
        # Each change is marked on the quality chart, like a draft rule.
        self.assertEqual([c['kind'] for c in self.store.rule_changes('2000-01-01')], ['voice', 'voice'])

    def test_the_owner_edits_and_removes_voices_in_settings_only(self):
        with self.assertRaisesRegex(ValueError, 'Settings'):
            self.app.action('set_voice', {'channel': 'Email', 'text': 'Warm and short.'})
        out = self.app.action('set_voice', {'channel': 'All', 'text': 'Natural dates, never 2026-10-04.'}, owner_dashboard=True)
        out = self.app.action('set_voice', {'channel': 'Email', 'text': 'Warm and short. Regards, a blank line, then my name.'}, owner_dashboard=True)
        self.assertEqual([(v['channel'], v['source']) for v in out['voices']], [('All', 'owner'), ('Email', 'owner')])
        out = self.app.action('set_voice', {'channel': 'Email', 'text': ''}, owner_dashboard=True)
        self.assertEqual([v['channel'] for v in out['voices']], ['All'])

    def test_a_voice_is_a_few_lines_and_a_learned_update_keeps_the_rest_of_it(self):
        block = '- English: Hi or Hey + first name\n- Regards, a blank line, then the name\n\n• Short paragraphs, no bullets'
        out = self.app.action('set_voice', {'channel': 'Email', 'text': block}, owner_dashboard=True)
        self.assertEqual(out['voices'][0]['text'], 'English: Hi or Hey + first name\nRegards, a blank line, then the name\nShort paragraphs, no bullets')
        # A note works one thing in; it doesn't shrink the block back to that one thing.
        with self.assertRaisesRegex(ValueError, 'Keep the whole Email block'):
            self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': 'Less formal.', 'decision_id': self.note_id()})
        grown = out['voices'][0]['text'] + '\nLess formal with customers than before'
        self.assertEqual(self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': grown, 'decision_id': self.note_id()})['text'], grown)
        self.assertIn('- Email:\n  - English: Hi or Hey + first name\n  - Regards', self.store.voices_text())

    def study_messages(self):
        sent = [mail(f's{i}', f'2026-10-0{i}T10:00:00+00:00', f'Hi {n},\n\nQuick one about item {i}: {w}.\n\nRegards,\n\nOwner', thread=f'ts{i}',
                     sender='Owner <owner@example.com>', to=f'{n} <{n.lower()}@example.org>', labels=('SENT',))
                for i, (n, w) in enumerate([('Ann', 'all set'), ('Bo', 'see the doc'), ('Cy', 'call tomorrow?'), ('Di', 'thanks a lot'),
                                            ('Ed', 'invoice is in'), ('Fay', 'works for me')], 1)]
        self.store.commit_page('work', {}, sent)

    def test_a_voice_study_reads_own_messages_per_channel_and_keeps_the_owners_own_blocks(self):
        self.study_messages()
        with self.store.connect() as db:
            db.execute("INSERT INTO note_kinds VALUES(?,?,'style','assistant',?)", (self.note_id(), self.chat_sid, timeutil.now()))
        self.app.action('set_voice', {'channel': 'All', 'text': 'Natural dates.'}, owner_dashboard=True)
        self.store.commit_page('work', {}, [mail(f'ann{i}', f'2026-10-07T1{i}:00:00+00:00', f'Hi Ann,\n\nPart {i} of a long thread, all fine.\n\nOwner',
                                                 thread='tann', sender='Owner <owner@example.com>', to='Ann <ann@example.org>', labels=('SENT',)) for i in range(4)])
        sample = self.store.voice_sample()
        self.assertEqual({m['channel'] for m in sample['messages']}, {'Email'})  # one WhatsApp message says too little
        self.assertEqual(sum(m['to'] == 'Ann' for m in sample['messages']), machine_store_voices.VOICE_STUDY_PER)  # one long thread doesn't decide
        with patch.dict(machine_store_voices.VOICE_STUDY, {'gmail.message': 5}):  # evenly across what was read, newest first
            self.assertEqual([m['date'] for m in self.store.voice_sample()['messages']],
                             ['2026-10-07', '2026-10-07', '2026-10-05', '2026-10-03', '2026-10-02'])
        self.assertTrue(all(m['text'].startswith(('Hi ', 'Hey ')) for m in sample['messages']))
        self.assertEqual(sample['notes'][0]['note'], 'no capitals on whatsapp please')
        started = self.store.voice_study_start()
        session = machine_store_profile.PROFILE_SESSION_PREFIX + started['run_id']
        page = self.store.profile_evidence(1, session)
        self.assertEqual((page['counts'], page['current_voices'][0]['written_by_owner']), ({'Email': 10}, True))
        prompt = machine_prompts_profile.voices_prompt(started['run_id'], page['counts'], page['pages'])
        self.assertIn('greeting per language', prompt)
        with self.assertRaisesRegex(ValueError, 'at most 5 lines'):
            self.store.save_profile({'voices': {'Email': '\n'.join(['Short line.'] * 6)}}, session)
        email_block = 'English: Hi + first name, a blank line\nRegards, a blank line, then the name\nShort paragraphs; questions to close'
        self.store.save_profile({'voices': {'Email': email_block, 'All': 'Overwrites nothing of theirs.'}}, session)
        with self.store.connect() as db:
            db.execute("UPDATE profile_runs SET status='ok',finished_at=? WHERE run_id=?", (timeutil.now(), started['run_id']))
        self.assertEqual(self.store.apply_voice_study(started['run_id']), 1)
        self.assertEqual(self.store.apply_voice_study(started['run_id']), 0)  # once
        self.assertEqual({v['channel']: (v['text'], v['source']) for v in self.store.voices()},
                         {'All': ('Natural dates.', 'owner'), 'Email': (email_block, 'study')})
        self.assertIsNone(self.store.voice_study_due())  # read again only after a while
        with patch_everywhere(timeutil, 'now', return_value=(dt.datetime.fromisoformat(timeutil.now()) + dt.timedelta(days=31)).isoformat()):
            self.assertIn('run_id', self.store.voice_study_due())

    def test_voice_study_excludes_misattributed_style_notes(self):
        self.study_messages()
        decision = self.note_id()
        with self.store.connect() as db:
            db.execute("INSERT INTO note_kinds VALUES(?,?,'style','assistant',?)", (decision, self.chat_sid, timeutil.now()))
            db.execute("INSERT INTO decision_annotations(decision_id,status,reason) VALUES(?,'misattributed','wrong card')", (decision,))
        self.assertNotIn(decision, {n['decision_id'] for n in self.store.voice_sample()['notes']})

    def test_a_voice_study_runs_as_a_turn_and_applies_when_it_finishes(self):
        self.study_messages()
        started = self.store.voice_study_start()
        self.app.preparation_gateway = None
        sent = []
        def runner(request):
            sent.append(request)
            if request['action'] == 'start':
                self.store.save_profile({'voices': {'Email': 'Hi + first name\nRegards, a blank line, then the name'}},
                                        machine_store_profile.PROFILE_SESSION_PREFIX + started['run_id'])
                return {'status': 'admitted'}
            return {'status': 'ok'}
        self.app.profile_step(runner)
        self.assertIn('voice study', sent[0]['message'])
        self.assertEqual(self.store.voices(), [])  # not before the run is done
        self.app.profile_step(runner)
        self.assertEqual([(v['channel'], v['source']) for v in self.store.voices()], [('Email', 'study')])

    def test_a_profile_fills_empty_channels_once(self):
        draft = {'voices': {'Email': 'Short paragraphs, Regards and name.', 'WhatsApp': 'Tiny lowercase bursts.'}}
        with self.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,draft,kind) VALUES('p1','ok','2026-10-01','2026-10-01',?,'profile')", (json.dumps(draft),))
        self.app.action('set_voice', {'channel': 'Email', 'text': 'My own email line.'}, owner_dashboard=True)
        self.assertEqual(self.store.seed_voices(), 1)
        self.assertEqual({v['channel']: v['text'] for v in self.store.voices()}, {'Email': 'My own email line.', 'WhatsApp': 'Tiny lowercase bursts.'})
        self.app.action('set_voice', {'channel': 'WhatsApp', 'text': ''}, owner_dashboard=True)
        self.assertEqual(self.store.seed_voices(), 0)  # removed stays removed until a new profile
        self.assertEqual([v['channel'] for v in self.store.voices()], ['Email'])

    def test_a_draft_gets_its_channels_voice_own_messages_and_only_that_channels_edits(self):
        self.app.action('set_voice', {'channel': 'Email', 'text': 'Hey name, short, Regards then a blank line then the name.'}, owner_dashboard=True)
        self.app.action('set_voice', {'channel': 'WhatsApp', 'text': 'lowercase, no full stop.'}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES('e1',?,'a','b','whatsapp','Ah ok. See you.','ah ok, tot straks','dashboard',?)", (self.chat_sid, timeutil.now()))
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES('e2',?,'a','b','email','Dear Sam, kindly find','Hey Sam, here it is','dashboard',?)", (self.sid, timeutil.now()))
        text = self.store.style_text(self.sid)
        self.assertIn('- Email (this card):\n  - Hey name', text)
        self.assertIn('- WhatsApp:\n  - lowercase', text)  # every voice, so a draft on another channel still has one
        examples = text.split("own recent Email messages")[1]
        # Same conversation first, then others; the owner's own words without the quoted history.
        self.assertLess(examples.index('(this conversation) Hey Sam'), examples.index('(to Lee) Hi Lee'))
        self.assertIn('Hey Sam, here it is', text)
        self.assertNotIn('tot straks', text)  # a WhatsApp edit says little about email
        chat_text = self.store.style_text(self.chat_sid)
        self.assertIn('- WhatsApp (this card):\n  - lowercase', chat_text)
        self.assertIn('(this conversation) ja tuurlijk, tot straks', chat_text)
        self.assertNotIn('Sent a photo', chat_text)  # media placeholders say nothing about how they write
        self.assertNotIn('Hey Sam', chat_text)
        prompt = machine_app_preparation.preparation_prompt({'job_id': 'j' * 16, 'suggestion_id': self.sid}, '', None, '', '- Offer the booking link.', text)
        self.assertLess(prompt.index('Draft rules'), prompt.index('How the owner writes, per channel'))
        self.assertIn('kind=voice, channel=', prompt)
        # Plain drafts, a model bias correction, come before the owner's voice, which wins where they differ
        self.assertLess(prompt.index(machine_prompts_bias.PLAIN_WRITING), prompt.index('How the owner writes, per channel'))
        self.assertIn('wins where it differs', machine_prompts_bias.PLAIN_WRITING)

    def test_a_chat_draft_gets_a_length_target_from_the_owners_own_replies_there(self):
        # No history to go by yet (one own message in the chat, a photo doesn't count): the fixed fallback.
        self.assertIn(f'under {machine_store_voices.CHAT_LENGTH_FALLBACK} characters', self.store.style_text(self.chat_sid))
        # Short never drops a question they asked: both the fallback and the target say so.
        self.assertIn('answer every question and request in their message', self.store.style_text(self.chat_sid))
        self.assertNotIn('Length:', self.store.style_text(self.sid))  # an email keeps its examples, no chat target
        short = ['ok top', 'ja is goed', 'haha zeker', 'top, tot zo', 'merci!', 'ik check het even']
        self.store.commit_page('phone', {}, [chat(f'r{i}', f'2026-10-02T0{i}:00:00+00:00', text, mine=True) for i, text in enumerate(short)] +
                               [chat('r9', '2026-10-02T09:30:00+00:00', 'Sent a photo', mine=True)])
        size = self.store.reply_length(self.chat_sid)
        lengths = sorted(len(t) for t in [*short, 'ja tuurlijk, tot straks'])
        self.assertEqual((size['channel'], size['here'], size['count'], size['high']), ('WhatsApp', True, 7, lengths[-1]))
        self.assertEqual(size['median'], lengths[3])
        text = self.store.style_text(self.chat_sid)
        self.assertTrue(text.startswith('Length: '))  # first, so a long style block never cuts it
        self.assertIn(f"own WhatsApp messages in this conversation are about {lengths[3]} characters long", text)
        self.assertIn(f'aims for about {lengths[3]} characters and stays within {lengths[-1]}', text)
        self.assertIn(machine_store_voices.CHAT_LENGTH_COVERS, text)
        self.assertIn('(this conversation) ik check het even', text)  # the style samples stay beside it
        prompt = machine_app_preparation.preparation_prompt({'job_id': 'j' * 16, 'suggestion_id': self.chat_sid}, style=text)
        self.assertLess(prompt.index(machine_prompts_bias.PLAIN_WRITING), prompt.index('Length: '))  # the owner's own wins
        # Another chat with too few of its own: the channel's length, not the fallback.
        self.store.commit_page('phone', {}, [chat('o1', '2026-10-03T08:00:00+00:00', 'Can you send the address?', chat_id='c2')])
        other = self.store.suggest('address', 'Send the address', 'They ask.', [self.event_id('o1')])['id']
        self.assertIn(f'own WhatsApp messages on WhatsApp are about {lengths[3]}', self.store.style_text(other))
        with patch.object(machine_store_voices, 'CHAT_LENGTH_MIN', 20):
            self.assertIn('under 160 characters', self.store.style_text(other))
        # A message The Machine sent for the owner isn't their writing and doesn't count.
        with patch('authorship.MachineSent.wrote', lambda self, row, text=None: True):
            self.assertIsNone(self.store.reply_length(self.chat_sid)['median'])

    def event_id(self, source_id):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()['id']

    def test_plain_drafts_go_per_model_family_and_never_on_a_confirmed_last_step(self):
        bias = machine_prompts_bias
        self.assertEqual([bias.family(m) for m in ('openai/gpt-6.1-sol', 'salesflare-openai/gpt-6-astra', 'claude-cli/claude-opus-5-5',
                                                   'anthropic/claude-sonnet-5-5', 'mistral/mistral-large-latest', 'ollama-cloud/glm-5.3-flash:cloud',
                                                   'local/some-model', None)],
                         ['gpt', 'gpt', 'claude', 'claude', 'mistral', 'glm', None, None])
        job = {'job_id': 'j' * 16, 'suggestion_id': self.sid}
        for model in ('openai/gpt-6.1-sol', 'claude-cli/claude-opus-5-5', None):
            self.assertIn(bias.PLAIN_WRITING, machine_app_preparation.preparation_prompt(job, model=model))
        with patch.dict(bias.PLAIN_WRITING_FOR, {'gpt': False}):  # one family off, the others and unknown ones keep it
            self.assertNotIn(bias.PLAIN_WRITING, machine_app_preparation.preparation_prompt(job, model='openai/gpt-6.1-sol'))
            self.assertIn(bias.PLAIN_WRITING, machine_app_preparation.preparation_prompt(job, model='anthropic/claude-opus-5-5'))
        with patch.object(bias, 'DEFAULT', False):
            self.assertEqual(bias.plain_writing('local/some-model'), '')
        finish = {**job, 'finish': {'label': 'Submit form', 'instructions': 'Press Submit', 'preview': 'The form'}}
        self.assertNotIn(bias.PLAIN_WRITING, machine_app_preparation.preparation_prompt(finish))  # the text was already confirmed
        # One model's own line, besides its family's: GPT-6.2 Sol only
        self.assertEqual(bias.plain_writing('openai/gpt-6.2-sol'), bias.PLAIN_WRITING + ' ' + bias.GPT_62_SOL)
        self.assertEqual(bias.plain_writing('openai-codex/GPT-6.2-Sol'), bias.PLAIN_WRITING + ' ' + bias.GPT_62_SOL)
        self.assertEqual(bias.plain_writing('openai/gpt-6.1-sol'), bias.PLAIN_WRITING)
        self.assertEqual((bias.model_note('openai/gpt-6.1-sol'), bias.model_note('openai/gpt'), bias.model_note(None)), ('', '', ''))
        self.assertIn(bias.GPT_62_SOL, machine_app_preparation.preparation_prompt(job, model='openai/gpt-6.2-sol'))
        self.assertNotIn(bias.GPT_62_SOL, machine_app_preparation.preparation_prompt(finish, model='openai/gpt-6.2-sol'))

    def test_a_draft_answered_elsewhere_becomes_an_edit_once(self):
        draft = {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'to': ['sam@example.com'], 'subject': 'Re: Contract',
                 'body': 'Dear Sam,\n\nPlease find the contract attached.\n\nKind regards', 'revision': 'r1'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), self.sid))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,'d','j1','done',?,?)",
                       (self.sid, '2026-10-03T09:00:00+00:00', '2026-10-03T09:00:00+00:00'))
        self.store.commit_page('work', {}, [mail('out3', '2026-10-03T11:00:00+00:00', 'Hey Sam,\n\nhere you go\n\nRegards,\n\nOwner\n\n[Quoted earlier messages]\nold', **SENT),
                                            mail('out4', '2026-10-03T12:00:00+00:00', 'Other thread entirely', thread='t9', **{k: v for k, v in SENT.items()})])
        with patch_everywhere(timeutil, 'now', return_value='2026-10-03T13:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 1)
            self.assertEqual(self.store.learn_sent_elsewhere(), 0)
        with self.store.connect() as db:
            row = dict(db.execute("SELECT * FROM draft_edits WHERE source='elsewhere'").fetchone())
        self.assertEqual((row['kind'], row['old_revision']), ('email', 'r1'))
        self.assertEqual(row['after_body'], 'Hey Sam,\n\nhere you go\n\nRegards,\n\nOwner')
        with patch_everywhere(timeutil, 'now', return_value='2026-10-03T13:00:00+00:00'):
            self.assertIn('They wrote this themselves instead: Hey Sam', self.store.style_text(self.sid))
            # A review gets it once to fold a lasting habit into the channel's voice.
            lines = self.store.edits_to_learn('run1')
            self.assertIn(f"- Email, \"Send Sam the contract\" (edit_id {row['id']})", lines)
            self.assertIn('They wrote themselves instead: Hey Sam', lines)
            self.assertEqual(self.store.edits_to_learn('run2'), '')
        saved = self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': 'Hey name, plain, short.', 'edit_id': row['id']})
        self.assertEqual(saved['channel'], 'Email')

    def test_a_draft_sent_from_the_card_or_without_a_reply_teaches_nothing(self):
        draft = {'kind': 'whatsapp', 'label': 'Send reply', 'account_id': 'phone', 'chat_id': 'c1', 'body': 'Yes, see you.', 'revision': 'r1'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), self.chat_sid))
            db.execute("UPDATE preparations SET status='done',updated_at=? WHERE suggestion_id=?", ('2026-10-01T09:00:00+00:00', self.chat_sid))
        with patch_everywhere(timeutil, 'now', return_value='2026-10-01T12:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 0)  # their earlier message came before the draft
        self.store.commit_page('phone', {}, [chat('w4', '2026-10-01T10:00:00+00:00', 'ja ik kom', mine=True)])
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('j',?,'r1','{}','sent',?,?,'x','dashboard','')", (self.chat_sid, timeutil.now(), timeutil.now()))
        with patch_everywhere(timeutil, 'now', return_value='2026-10-01T12:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 0)  # sent from the card: that message is the draft itself
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='cancelled'")
        with patch_everywhere(timeutil, 'now', return_value='2026-10-01T12:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 1)  # not sent from the card: their own reply teaches

    def ready(self, sid, draft):
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), sid))

    def hint(self, sid):
        with self.store.connect() as db:
            value = db.execute('SELECT handled_hint FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
        return json.loads(value) if value else None

    def test_a_draft_answered_from_gmail_closes_the_to_do(self):
        """The owner replied in the draft's thread from Gmail itself: the to-do closes by itself (Done, with Undo), with
        their message as what shows it. Their reply from before the to-do was made (the review saw it) and one in another
        thread don't count."""
        self.ready(self.sid, {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'thread_id': 't1', 'to': ['sam@example.com'],
                              'subject': 'Re: Contract', 'body': 'Dear Sam,\n\nThe contract is attached.', 'revision': 'r1'})
        self.assertEqual(self.store.answered_elsewhere(), [])  # out1 came before the to-do: the review that made it saw it
        self.store.commit_page('work', {}, [mail('out9', '2026-10-03T12:00:00+00:00', 'Other thread entirely', thread='t9', **SENT)])
        self.assertEqual(self.store.answered_elsewhere(), [])
        self.store.commit_page('work', {}, [mail('out3', '2026-10-03T11:00:00+00:00', 'Hey Sam,\n\nhere you go\n\n[Quoted earlier messages]\nold', **SENT)])
        self.assertEqual(self.store.answered_elsewhere(), [self.sid])
        hint = self.hint(self.sid)
        self.assertEqual(hint['reason'], 'Answered in the email thread')
        with self.store.connect() as db:
            out3 = db.execute("SELECT id FROM events WHERE source_id='out3'").fetchone()[0]
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
        self.assertEqual(hint['event_ids'], [out3])  # Done shows "Done: Answered in the email thread" under the title
        self.assertEqual(machine_cards.todo_state(row), 'done')
        self.assertTrue(row['undo_until'])
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute("SELECT source,feedback FROM decisions WHERE suggestion_id=? AND choice='complete'", (self.sid,)).fetchone()),
                             ('handled', 'Answered in the email thread'))
        self.assertEqual(self.store.answered_elsewhere(), [])  # once

    def test_their_reply_on_a_to_do_with_a_done_when_waits_for_the_result(self):
        """A to-do whose point is a result (its done when) isn't done by the owner's own reply in the thread, just as a
        send from the card isn't: it waits for that result under Waiting on others, without a Looks done hint."""
        self.ready(self.sid, {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'thread_id': 't1', 'to': ['sam@example.com'],
                              'subject': 'Re: Contract', 'body': 'Dear Sam,\n\nStill looking for it.', 'revision': 'r1'})
        with self.store.connect() as db:
            outcomes.set_done_when(db, self.sid, 'Sam has the signed contract', 'run')
        self.store.commit_page('work', {}, [mail('out3', '2026-10-03T11:00:00+00:00', 'Hey Sam,\n\nwould a scan do for now?', **SENT)])
        self.assertEqual(self.store.answered_elsewhere(), [self.sid])
        self.assertIsNone(self.hint(self.sid))
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
        self.assertEqual(machine_cards.todo_state(row), 'waiting on others')
        self.assertEqual(json.loads(row['outcome'])['waiting_on'], 'Sam has the signed contract')
        self.assertIsNone(row['next_action'])
        self.assertEqual(self.store.answered_elsewhere(), [])  # once

    def test_undo_stands_until_a_newer_message_of_theirs(self):
        self.ready(self.chat_sid, {'kind': 'whatsapp', 'label': 'Send reply', 'account_id': 'phone', 'chat_id': 'c1', 'body': 'Yes, see you.', 'revision': 'r1'})
        self.store.commit_page('phone', {}, [chat('w4', '2026-10-01T10:00:00+00:00', 'Sent a photo', mine=True)])
        self.assertEqual(self.store.answered_elsewhere(), [])  # a photo says nothing
        self.store.commit_page('phone', {}, [chat('w5', '2026-10-01T10:05:00+00:00', 'ja ik kom', mine=True)])
        self.assertEqual(self.store.answered_elsewhere(), [self.chat_sid])
        self.assertEqual(self.hint(self.chat_sid)['reason'], 'Answered on WhatsApp')
        self.store.decide(self.chat_sid, 'undo', '', 'u1', 'dashboard')
        self.assertIsNone(self.hint(self.chat_sid))  # a normal to-do again, back on the list
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (self.chat_sid,)).fetchone()[0], 'prepared')
        self.assertEqual(self.store.answered_elsewhere(), [])  # they saw that message and took it back
        self.assertEqual(self.store.close_looks_done(), [])
        self.store.commit_page('phone', {}, [chat('w6', '2026-10-01T18:00:00+00:00', 'top, tot zo', mine=True)])
        self.assertEqual(self.store.answered_elsewhere(), [self.chat_sid])

    def test_slack_counts_the_to_dos_own_thread_or_a_dm_not_the_whole_channel(self):
        self.store.owner_user_ids = {'UOWNER1'}
        def slack(source_id, at, body, channel='C1', ts='100.1', user='USAM001', thread=None):
            return {'account_id': 'team', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at, 'title': '#general',
                    'body': body, 'deleted': False, 'metadata': {'channel_id': channel, 'message_ts': ts, 'thread_ts': thread or ts, 'user_id': user}}
        self.store.commit_page('team', {}, [slack('s1', '2026-10-05T09:00:00+00:00', 'Can someone check the invoice?'),
                                            slack('d1', '2026-10-05T09:00:00+00:00', 'Got a minute?', channel='D7', ts='200.1')])
        with self.store.connect() as db:
            s1, d1 = (db.execute('SELECT id FROM events WHERE source_id=?', (x,)).fetchone()[0] for x in ('s1', 'd1'))
        sid = self.store.suggest('invoice', 'Check the invoice', 'Asked in #general.', [s1])['id']
        dm = self.store.suggest('minute', 'Answer about a minute', 'Asked in a DM.', [d1])['id']
        self.ready(sid, {'kind': 'slack', 'label': 'Reply', 'account_id': 'team', 'channel_id': 'C1', 'thread_ts': '100.1', 'body': 'On it.', 'revision': 'r1'})
        self.ready(dm, {'kind': 'slack', 'label': 'Reply', 'account_id': 'team', 'channel_id': 'D7', 'body': 'Sure.', 'revision': 'r1'})
        self.store.commit_page('team', {}, [slack('s2', '2026-10-05T10:00:00+00:00', 'Lunch anyone today?', ts='300.1', user='UOWNER1'),
                                            slack('d2', '2026-10-05T10:00:00+00:00', 'sure, call me now', channel='D7', ts='400.1', user='UOWNER1')])
        self.assertEqual(self.store.answered_elsewhere(), [dm])  # another matter in the same channel isn't an answer
        self.store.commit_page('team', {}, [slack('s3', '2026-10-05T11:00:00+00:00', 'Checked it, all fine', ts='500.1', thread='100.1', user='UOWNER1')])
        self.assertEqual(self.store.answered_elsewhere(), [sid])
        self.assertEqual(self.hint(sid)['reason'], 'Answered in Slack')

    def drafted(self, key, source_id, draft, at='2026-10-05T09:30:00+00:00'):
        """A to-do about that message with this draft ready at `at`; its id."""
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]
        sid = self.store.suggest(key, 'To-do ' + key, 'Asked.', [event])['id']
        self.ready(sid, {'label': 'Reply', 'revision': 'r-' + key, **draft})
        with self.store.connect() as db:
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,'d',?,'done',?,?)", (sid, 'j-' + key, at, at))
        return sid

    def learned(self, at='2026-10-05T18:00:00+00:00'):
        """{to-do: what the owner wrote instead of its draft}, after a round of learning at that time."""
        with patch_everywhere(timeutil, 'now', return_value=at):
            self.store.learn_sent_elsewhere()
        with self.store.connect() as db:
            return {r['suggestion_id']: r['after_body'] for r in db.execute("SELECT * FROM draft_edits WHERE source='elsewhere'")}

    def slack(self, source_id, at, body, channel='C1', ts='100.1', user='USAM001', thread=None):
        self.store.owner_user_ids = {'UOWNER1'}
        self.store.commit_page('team', {}, [{'account_id': 'team', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at, 'title': '#general', 'body': body,
                                             'deleted': False, 'metadata': {'channel_id': channel, 'message_ts': ts, 'thread_ts': thread or ts, 'user_id': user}}])

    def test_another_matter_in_the_same_slack_channel_teaches_nothing_and_the_real_answer_still_does(self):
        self.slack('s1', '2026-10-05T09:00:00+00:00', 'Can someone check the invoice?')
        self.slack('d1', '2026-10-05T09:00:00+00:00', 'Got a minute?', channel='D7', ts='200.1')
        sid = self.drafted('invoice', 's1', {'kind': 'slack', 'account_id': 'team', 'user_id': 'USAM001', 'body': 'The invoice checks out, thanks.',
                                             'thread': {'channel_id': 'C1', 'ts': '100.1', 'dm': False}})
        dm = self.drafted('minute', 'd1', {'kind': 'slack', 'account_id': 'team', 'user_id': 'USAM001', 'body': 'Certainly, I do.'})
        self.slack('s2', '2026-10-05T10:00:00+00:00', 'Lunch anyone today? Pizza place at noon', ts='300.1', user='UOWNER1')
        self.slack('s4', '2026-10-05T10:10:00+00:00', 'that one is done too', ts='310.1', thread='90.1', user='UOWNER1')  # another thread
        self.slack('d2', '2026-10-05T10:00:00+00:00', 'sure, call me now', channel='D7', ts='400.1', user='UOWNER1')
        self.assertEqual(self.learned(), {dm: 'sure, call me now'})
        self.slack('s3', '2026-10-05T11:00:00+00:00', 'checked it, all fine', ts='500.1', thread='100.1', user='UOWNER1')
        self.assertEqual(self.learned(), {dm: 'sure, call me now', sid: 'checked it, all fine'})

    def test_in_a_group_chat_only_a_reply_that_quotes_the_to_dos_message_teaches(self):
        def group(source_id, at, body, kind='whatsapp.message', chat_id='1203630@g.us', mine=False, **more):
            event = chat(source_id, at, body, chat_id=chat_id, mine=mine)
            event['metadata'].update(message_id=source_id, **more)
            self.store.commit_page('phone', {}, [{**event, 'kind': kind}])
        tele = dict(kind='telegram.message', chat_id='777', chat_kind='group')
        group('g1', '2026-10-05T09:00:00+00:00', 'Who brings the tent?')
        group('11', '2026-10-05T09:00:00+00:00', 'Who drives on Friday?', **tele)
        group('21', '2026-10-05T09:00:00+00:00', 'Can you bring the keys?', kind='telegram.message', chat_id='444', chat_kind='dm')
        wa = self.drafted('tent', 'g1', {'kind': 'whatsapp', 'account_id': 'phone', 'chat_id': '1203630@g.us', 'body': 'I will bring it.'})
        tg = self.drafted('drive', '11', {'kind': 'telegram', 'account_id': 'phone', 'chat_id': '777', 'body': 'I will drive.'})
        one = self.drafted('keys', '21', {'kind': 'telegram', 'account_id': 'phone', 'chat_id': '444', 'body': 'I will bring them.'})
        group('g2', '2026-10-05T10:00:00+00:00', 'lol great photo', mine=True)
        group('12', '2026-10-05T10:00:00+00:00', 'happy birthday kim!', mine=True, **tele)
        group('13', '2026-10-05T10:01:00+00:00', 'good point, thanks', mine=True, reply_to=8, **tele)  # quotes another message
        group('22', '2026-10-05T10:00:00+00:00', 'yep, got them', kind='telegram.message', chat_id='444', chat_kind='dm', mine=True)
        self.assertEqual(self.learned(), {one: 'yep, got them'})
        group('14', '2026-10-05T11:00:00+00:00', 'me, as always', mine=True, reply_to=11, **tele)
        self.assertEqual(self.learned(), {one: 'yep, got them', tg: 'me, as always'})
        # Closing (with Undo) is not as strict: what they write in the group after the to-do mostly answers it
        self.assertEqual(sorted(self.store.answered_elsewhere()), sorted([wa, tg, one]))

    def test_in_an_email_thread_only_mail_to_who_the_draft_is_for_teaches(self):
        sid = self.drafted('price', 'in1', {'kind': 'email', 'account_id': 'work', 'thread_id': 't1', 'to': ['Sam@example.com'], 'subject': 'Re: Contract', 'body': 'Dear Sam, it is attached.'})
        def own(source_id, at, body, **people):
            self.store.commit_page('work', {}, [{**(m := mail(source_id, at, body, sender=SENT['sender'], to=people['to'], labels=('SENT',))),
                                                 'metadata': {**m['metadata'], 'cc': people.get('cc', '')}}])
        own('fw', '2026-10-05T10:00:00+00:00', 'lee, can you look at this one?', to='Lee <lee@example.org>')
        own('aside', '2026-10-05T10:30:00+00:00', 'thanks lee, sam is in copy', to='Lee <lee@example.org>', cc='Sam <sam@example.com>')
        self.assertEqual(self.learned(), {})
        own('all', '2026-10-05T11:00:00+00:00', 'hey sam, here it is', to='Sam <sam@example.com>, Lee <lee@example.org>')
        self.assertEqual(self.learned(), {sid: 'hey sam, here it is'})
        self.assertEqual(self.store.answered_elsewhere(), [sid])

    def test_a_reply_to_another_address_of_the_same_person_teaches(self):
        def draft(key):
            return {'kind': 'email', 'account_id': 'work', 'thread_id': 't-' + key, 'to': ['sam@example.com'], 'subject': 'Re: Contract', 'body': 'Dear Sam, it is attached.'}
        asked = mail('in-a', '2026-10-05T09:00:00+00:00', 'Can you send it?', thread='t-a')
        asked['metadata']['reply-to'] = 'Sam <sam@inbox.example.net>'
        self.store.commit_page('work', {}, [asked, mail('in-b', '2026-10-05T09:00:00+00:00', 'Can you send it?', thread='t-b')])
        with self.store.connect() as db:
            graph.ensure(db)
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('p1','person','Sam',1,0,?)", (json.dumps({'identifiers': ['email:sam@example.com', 'email:sam@home.example']}),))
        a, b = self.drafted('a', 'in-a', draft('a')), self.drafted('b', 'in-b', draft('b'))
        self.store.commit_page('work', {}, [
            mail('out-a', '2026-10-05T10:00:00+00:00', 'hey sam, here it is', thread='t-a', sender=SENT['sender'], to='sam@inbox.example.net', labels=('SENT',)),
            mail('out-b', '2026-10-05T10:00:00+00:00', 'sam, see below', thread='t-b', sender=SENT['sender'], to='Sam <sam@home.example>', labels=('SENT',))])
        self.assertEqual(self.learned(), {a: 'hey sam, here it is', b: 'sam, see below'})

    def test_lessons_kept_from_a_message_that_answered_something_else_go_once(self):
        self.slack('s1', '2026-10-05T09:00:00+00:00', 'Can someone check the invoice?')
        self.slack('s2', '2026-10-05T10:00:00+00:00', 'Lunch anyone today?', ts='300.1', user='UOWNER1')
        self.slack('s3', '2026-10-05T11:00:00+00:00', 'checked it, all fine', ts='500.1', thread='100.1', user='UOWNER1')
        self.slack('d1', '2026-10-05T11:00:00+00:00', 'sure, call me', channel='D7', ts='600.1', user='UOWNER1')
        self.store.commit_page('work', {}, [mail('fw', '2026-10-05T10:00:00+00:00', 'lee, can you look?', sender=SENT['sender'], to='Lee <lee@example.org>', labels=('SENT',))])
        slack = {'kind': 'slack', 'account_id': 'team', 'user_id': 'USAM001', 'body': 'The invoice checks out.'}
        sid = self.drafted('invoice', 's1', slack)
        email = self.drafted('price', 'in1', {'kind': 'email', 'account_id': 'work', 'thread_id': 't1', 'to': ['sam@example.com'], 'body': 'Dear Sam.'})
        with self.store.connect() as db:
            for source_id, kind, todo, revision in (('s2', 'slack', sid, 'r-invoice'), ('s3', 'slack', sid, 'r-invoice'), ('d1', 'slack', sid, 'r-invoice'),
                                                    ('fw', 'email', email, 'r-price'), ('out2', 'email', email, 'an older draft')):
                event = db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]
                db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                           "VALUES(?,?,?,?,?,'draft','theirs','elsewhere',?)", (source_id, todo, revision, f'elsewhere:{event}', kind, timeutil.now()))
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                       "VALUES('own','" + sid + "','a','b','slack','draft','theirs','dashboard',?)", (timeutil.now(),))
        self.assertEqual(sorted(self.store.drop_wrong_answers_once()), ['fw', 's2'])
        with self.store.connect() as db:
            self.assertEqual({r[0] for r in db.execute('SELECT id FROM draft_edits')}, {'s3', 'd1', 'out2', 'own'})
        self.assertIsNone(self.store.drop_wrong_answers_once())  # once

    def test_a_draft_sent_from_the_card_or_their_word_in_dutch(self):
        self.ready(self.chat_sid, {'kind': 'whatsapp', 'label': 'Send reply', 'account_id': 'phone', 'chat_id': 'c1', 'body': 'Yes, see you.', 'revision': 'r1'})
        self.store.commit_page('phone', {}, [chat('w4', '2026-10-01T10:00:00+00:00', 'ja ik kom', mine=True)])
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('j',?,'r1','{}','sent',?,?,'x','dashboard','')", (self.chat_sid, timeutil.now(), timeutil.now()))
        self.assertEqual(self.store.answered_elsewhere(), [])  # sent from the card: Sent closes it, not this
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='cancelled'")
        with patch.object(locale_prefs, 'language', return_value='nl'):
            self.assertEqual(self.store.answered_elsewhere(), [self.chat_sid])
        self.assertEqual(self.hint(self.chat_sid)['reason'], 'Beantwoord op WhatsApp')


class Learned(unittest.TestCase):
    """A preparation gets what was learned that bears on its card, not all of it; a review condenses the list now and
    then (merging what says the same, the newer winning), and the owner sees and can undo each merge."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.store.accounts = [{'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}]
        self.app.config = {'accounts': self.store.accounts}
        self.store.commit_page('work', {}, [mail('in1', '2026-10-01T09:00:00+00:00', 'Deal on the listing swap.'),
                                            mail('in2', '2026-10-01T09:00:00+00:00', 'Quote attached.', thread='t2'),
                                            mail('in3', '2026-10-01T09:00:00+00:00', 'Quick question.', thread='t3')])
        self.sid = self.store.suggest('listing', 'Answer the listing exchange', 'They agreed to swap listings.', [1])['id']
        self.other = self.store.suggest('paint', 'Pay the painter', 'The quote excludes VAT.', [2])['id']
        self.note = self.store.decide(self.other, 'other', 'remember these', 'n1', 'dashboard')
        with self.store.connect() as db:
            self.decision = db.execute("SELECT id FROM decisions WHERE feedback!=''").fetchone()['id']

    def fact(self, text, kind='fact'):
        return self.store.remember_fact(text, self.decision, kind, quote='remember these')['id']

    def test_a_preparation_gets_the_facts_that_bear_on_its_card(self):
        few = self.fact('The office is closed on Fridays.')
        self.assertEqual(self.store.facts_for(self.sid), '- The office is closed on Fridays.')  # few: all of them
        topics = ['listing', 'paint', 'tax', 'travel', 'hiring', 'billing', 'support', 'garden', 'school', 'bank', 'car', 'dentist', 'insurance', 'lunch']
        ids = {t: self.fact(f'A long enough fact about {t}, so that all of them together are more than a preparation should carry around. ' * 1)
               for t in topics}
        own = self.store.remember_fact('This card’s own note: they write listing copy themselves.', self.decision, quote='remember these')['id']
        with self.store.connect() as db:  # a fact learned on this card
            db.execute('UPDATE facts SET suggestion_id=? WHERE id=?', (self.sid, own))
        # No embeddings: the one that shares the card's words ("listings"), then the newest, up to the limit.
        newest = self.store.facts_for(self.sid, limit=400).splitlines()
        self.assertEqual(newest[0], '- This card’s own note: they write listing copy themselves.')
        self.assertIn('listing', newest[1])
        self.assertIn('lunch', newest[2])
        # With embeddings: this card's own facts, then the closest ones above the floor.
        def embed(settings, texts, timeout=120):
            return [[1.0, 0.0] if 'listing' in t or 'Answer the listing' in t else [0.6, 0.8] if 'paint' in t or 'tax' in t else [0.0, 1.0] for t in texts]
        settings = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}
        with patch.object(embeddings, 'embed', side_effect=embed) as called:
            picked = self.store.facts_for(self.sid, settings=settings, top=2, floor=0.5).splitlines()
            self.assertEqual(len(called.call_args.args[1]), len(topics) + 3)  # every fact once, plus the card
            self.store.facts_for(self.sid, settings=settings, top=2, floor=0.5)
            self.assertEqual(len(called.call_args.args[1]), 1)  # facts' meaning is kept: only the card again
        self.assertEqual(picked[0], '- This card’s own note: they write listing copy themselves.')
        self.assertEqual([('listing' in p, 'paint' in p or 'tax' in p) for p in picked[1:]], [(True, False), (False, True)])
        self.assertFalse(any('garden' in p or 'Fridays' in p for p in picked))  # below the floor
        with patch.object(embeddings, 'embed', side_effect=embeddings.EmbeddingError('down')):
            self.assertIn('lunch', self.store.facts_for(self.sid, settings=settings, limit=400).splitlines()[2])  # down: by words, then the newest
        del few, ids

    def test_condensing_merges_keeps_the_originals_and_the_owner_can_undo_it(self):
        old = self.fact('In emails, put links behind text.')
        new = self.fact('In emails, show the URL itself, hyperlinked.')
        rule = self.fact('For listing exchanges, prepare both inclusions.', 'draft')
        with self.assertRaisesRegex(ValueError, 'not current'):
            self.app.action('remember_fact', {'text': 'Merged.', 'replaces': [old, 999]})
        out = self.app.action('remember_fact', {'text': 'In emails, show the URL itself as the link text, hyperlinked.', 'replaces': [old, new]})
        self.assertEqual(out['merged'], 2)
        self.assertEqual([f['text'] for f in self.store.facts() if f['kind'] == 'fact'], ['In emails, show the URL itself as the link text, hyperlinked.'])
        with self.store.connect() as db:  # the originals stay, behind the merged one
            self.assertEqual({r['id']: r['merged_into'] for r in db.execute('SELECT id,merged_into FROM facts WHERE merged_into IS NOT NULL')},
                             {old: f"fact:{out['id']}", new: f"fact:{out['id']}"})
        snap = self.store.snapshot([])
        self.assertEqual([(f['text'][:9], f['merged']) for f in snap['facts']], [('In emails', 2), ('For listi', 0)])  # newest first
        self.assertEqual(snap['condensed']['notes'], 2)
        # A style fact folds into its channel's voice.
        voice = self.app.action('remember_fact', {'kind': 'voice', 'channel': 'Email', 'text': 'Short, warm, URLs shown and hyperlinked.', 'replaces': [out['id']]})
        self.assertEqual(voice['merged'], 1)
        self.assertEqual([v['merged'] for v in self.store.snapshot([])['voices']], [1])
        with self.assertRaisesRegex(ValueError, 'dashboard'):
            self.app.action('unmerge_fact', {'channel': 'Email'})
        self.assertEqual(self.app.action('unmerge_fact', {'channel': 'Email'}, owner_dashboard=True), {'restored': 1})
        self.assertEqual(self.app.action('unmerge_fact', {'id': out['id']}, owner_dashboard=True), {'restored': 2})
        self.assertEqual(sorted(f['id'] for f in self.store.facts()), sorted([old, new, rule]))
        with self.assertRaisesRegex(ValueError, 'Nothing was merged'):
            self.app.action('unmerge_fact', {'id': rule}, owner_dashboard=True)
        # Owner notes stay the only source: a merge can't name facts that aren't there, and the owner's Settings line can't merge.
        self.app.action('set_voice', {'channel': 'Email', 'text': 'Mine.', 'replaces': [old]}, owner_dashboard=True)
        self.assertIn(old, [f['id'] for f in self.store.facts()])

    def test_a_review_is_offered_the_list_to_condense_now_and_then_and_unlearned_style_notes_once(self):
        for i in range(6):
            self.fact(f'Fact number {i} about something.')
        self.assertIn('id 1 (fact): Fact number 0', self.store.condense_text())
        self.assertTrue(self.store.condense_text('r1'))
        self.assertEqual(self.store.condense_text(), '')  # offered: not again until the list changes and a day passed
        self.fact('Another fact.')
        self.assertEqual(self.store.condense_text(), '')
        with patch_everywhere(timeutil, 'now', return_value='2099-01-01T00:00:00+00:00'):
            self.fact('A much later fact.')
            self.assertTrue(self.store.condense_text())
        # A style note nothing was learned from is offered once.
        with self.store.connect() as db:
            db.execute("INSERT INTO note_kinds VALUES(?,?,?,?,?)", (self.decision, self.other, 'style', 'assistant', timeutil.now()))
        self.assertEqual(self.store.style_notes_to_learn(), '')  # facts came from it already
        sid = self.store.suggest('mail', 'Answer Ann', 'Ann asks.', [3])['id']
        self.store.decide(sid, 'other', 'less formal please, always', 'n2', 'dashboard')
        with self.store.connect() as db:
            note = db.execute("SELECT id FROM decisions WHERE suggestion_id=? AND feedback!=''", (sid,)).fetchone()['id']
            db.execute("INSERT INTO note_kinds VALUES(?,?,?,?,?)", (note, sid, 'style', 'assistant', timeutil.now()))
        self.assertIn('less formal please', self.store.style_notes_to_learn('r1'))
        self.assertEqual(self.store.style_notes_to_learn(), '')


class ReviewRegressions(unittest.TestCase):
    setUp = Voices.setUp
    note_id = Voices.note_id
    def test_examples_and_elsewhere_replies_stay_on_the_cards_account(self):
        private = mail('private-out', '2026-10-03T12:00:00+00:00', 'PRIVATE PERSONAL MESSAGE', **SENT)
        private['account_id'] = 'personal'
        self.store.accounts.append({'id': 'personal', 'service': 'gmail', 'email': 'private@example.org'})
        self.store.commit_page('personal', {}, [private])
        self.assertFalse(any('PRIVATE PERSONAL' in e['text'] for e in self.store.own_examples(self.sid)))
        draft = {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'to': ['sam@example.com'],
                 'thread_id': 't1', 'subject': 'Re: Contract', 'body': 'Concrete work reply.', 'revision': 'r1'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), self.sid))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,'d','j','done',?,?)",
                       (self.sid, '2026-10-03T09:00:00+00:00', '2026-10-03T09:00:00+00:00'))
        with patch_everywhere(timeutil, 'now', return_value='2026-10-03T13:00:00+00:00'):
            self.assertEqual(self.store.learn_sent_elsewhere(), 0)
        with self.store.connect() as db:
            private_id=db.execute("SELECT id FROM events WHERE source_id='private-out' AND account_id='personal'").fetchone()[0]
        private_sid=self.store.suggest('personal-card','Private card','Private body',[private_id])['id']
        with self.store.connect() as db:
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) VALUES('private-edit',?,'a','b','email','Secret private draft.','Secret private final.','dashboard',?)",(private_sid,timeutil.now()))
        self.assertNotIn('Secret private',self.store.style_text(self.sid))
        # An inbound sender or arbitrary metadata value spelling SENT is not an outgoing label.
        incoming = mail('not-sent', '2026-10-03T14:00:00+00:00', 'NOT OWNER WRITING', thread='t1')
        incoming['metadata']['display_name'] = 'SENT'
        self.store.commit_page('work', {}, [incoming])
        self.assertFalse(any('NOT OWNER' in e['text'] for e in self.store.own_examples(self.sid)))

    def test_undo_voice_merge_restores_previous_line_but_preserves_new_owner_edit(self):
        decision = self.note_id()
        for preserve in (False, True):
            self.store.save_voice('Email', 'Original email style.', 'owner')
            fid = self.store.remember_fact('Use lowercase in email too' + (' next time.' if preserve else '.'), decision, quote='no capitals on whatsapp please')['id']
            self.store.save_voice('Email', 'Original style, lowercase.', 'assistant', replaces=[fid])
            if preserve:
                self.store.save_voice('Email', 'Newer owner style wins.', 'owner')
            self.store.unmerge_fact(channel='Email')
            self.assertEqual(next(v['text'] for v in self.store.voices() if v['channel']=='Email'),
                             'Newer owner style wins.' if preserve else 'Original email style.')
            self.store.forget_fact(fid)
        self.store.save_voice('Email', 'Before learned merge.', 'owner')
        first=self.store.remember_fact('Use original merged style.',decision, quote='no capitals on whatsapp please')['id']
        self.store.save_voice('Email','First learned merge style.','assistant',replaces=[first])
        self.store.save_voice('Email','Owner edit between merges.','owner')
        second=self.store.remember_fact('And a newer merged style.',decision, quote='no capitals on whatsapp please')['id']
        self.store.save_voice('Email','Second learned merge style.','assistant',replaces=[second])
        self.store.unmerge_fact(channel='Email')
        self.assertEqual(next(v['text'] for v in self.store.voices() if v['channel']=='Email'),'Owner edit between merges.')
        self.store.save_voice('Email', '', 'owner')
        fid = self.store.remember_fact('Another style fact to merge.', decision, quote='no capitals on whatsapp please')['id']
        self.store.save_voice('Email', 'First learned email style.', 'assistant', replaces=[fid])
        self.store.unmerge_fact(channel='Email')
        self.assertFalse(any(v['channel']=='Email' for v in self.store.voices()))

    def test_misattributed_feedback_cannot_teach_a_voice(self):
        decision = self.note_id()
        with self.store.connect() as db:
            db.execute("INSERT INTO decision_annotations(decision_id,status,reason) VALUES(?,'misattributed','wrong card')", (decision,))
        with self.assertRaisesRegex(ValueError, 'own written notes'):
            self.store.save_voice('Slack', 'Wrong style from another card.', 'assistant', decision_id=decision)

    def test_learning_offers_survive_unavailable_gateway_then_commit_after_admission(self):
        for i in range(6):
            self.store.remember_fact('Fact to condense number ' + str(i), self.note_id(), quote='no capitals on whatsapp please')
        with self.store.connect() as db:
            db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) VALUES('retry-edit',?,'a','b','email','Long stiff draft.','Hey, natural reply.','dashboard',?)", (self.sid, timeutil.now()))
            db.execute("INSERT INTO note_kinds VALUES(?,?,?,?,?)", (self.note_id(), self.chat_sid, 'style', 'assistant', timeutil.now()))
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,attempts,planned) VALUES('review-learning','starting',?,?,0,1)", (timeutil.now(), timeutil.now()))
        self.app.config.update(review_worker={'enabled': True})
        requests=[]
        def unavailable(request):
            requests.append(request)
            return {'status': 'unavailable'}
        self.app.review_step(unavailable)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM edits_offered').fetchone()[0], 0)
            db.execute("UPDATE review_runs SET retry_at=NULL,updated_at='2000-01-01T00:00:00+00:00' WHERE run_id='review-learning'")
        self.assertIn('retry-edit', requests[0]['message'])
        self.assertIn('Condense what', requests[0]['message'])
        def admitted(request):
            requests.append(request)
            return {'status': 'admitted'}
        self.app.review_step(admitted)
        self.assertIn('retry-edit', requests[-1]['message'])
        with self.store.connect() as db:
            ids={r[0] for r in db.execute('SELECT edit_id FROM edits_offered')}
        self.assertIn('retry-edit', ids)
        self.assertTrue(any(x.startswith('condense:') for x in ids))

    def test_habits_are_recorded_and_followed_exactly_and_a_saved_one_shows_on_its_card(self):
        # "No caps in chat" meant sentence starts: every prompt that writes a block asks for the exact habit, and a draft
        # follows the lines as written, on their own channel only.
        self.assertIn(machine_prompts_profile.VOICE_PRECISE, machine_prompts_profile.VOICE_TEXT)
        self.assertIn('names', machine_prompts_profile.VOICE_PRECISE)
        self.assertIn(machine_prompts_profile.VOICE_PRECISE, machine_prompts_profile.voices_prompt('r1', {'WhatsApp': 5}, 1))
        self.assertNotIn('lowercase bursts', machine_prompts_profile.profile_prompt('r1', {'WhatsApp': 5}))
        prompt = machine_app_preparation.preparation_prompt({'job_id': 'j' * 16, 'suggestion_id': self.chat_sid}, '', None, '', '', '')
        self.assertIn(machine_prompts_profile.VOICE_PRECISE, prompt)
        self.app.action('set_voice', {'channel': 'WhatsApp', 'text': 'Sentences start lowercase, names keep their capitals.'}, owner_dashboard=True)
        style = self.store.style_text(self.sid)
        self.assertIn('no broader', style)
        self.assertIn("one channel's habits stay on that channel", style)
        # Learned from a note on this card: its chat says so, with the channel, and only on that card
        text = 'Sentences start lowercase, names keep their capitals; no full stop.'
        self.app.action('remember_fact', {'kind': 'voice', 'channel': 'whatsapp', 'text': text, 'decision_id': self.note_id()})
        self.app.config['owner_name'] = 'Owner'
        with self.store.connect() as db:
            owner, _ = self.app.card_chat_service(db, self.chat_sid)
            other, _ = self.app.card_chat_service(db, self.sid)
        saved = [i for i in owner if i.get('voice')]
        self.assertEqual([(i['kind'], i['text'], i['voice']) for i in saved], [('event', 'Saved to How you write: WhatsApp', 'WhatsApp')])
        self.assertFalse(any(i.get('voice') for i in other))
        # The owner's own edit in Settings is not a card's line
        self.app.action('set_voice', {'channel': 'All', 'text': 'Natural dates.'}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertEqual(len([i for i in self.app.card_chat_service(db, self.chat_sid)[0] if i.get('voice')]), 1)


if __name__ == '__main__':
    unittest.main()
