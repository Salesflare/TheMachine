import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)
import agent_jobs  # noqa: E402
import agent_remote  # noqa: E402
import retention  # noqa: E402
from machine.upkeep import agent_workspaces  # noqa: E402

NOW = dt.datetime(2026, 11, 6, 3, 30, tzinfo=dt.timezone.utc)


def ago(days):
    return (NOW - dt.timedelta(days=days)).isoformat()


class Workspaces(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.store = assistant.Store(self.dir / 'events.sqlite', protect=True)
        self.root = self.dir / 'agent-jobs'
        self.jobs = agent_jobs.AgentJobs(self.store.connect, {'database': str(self.dir / 'events.sqlite'), 'accounts': [], 'agents': {}}, self.root)
        self.n = 0

    def job(self, status='result', card='completed', ended=10, outcome=None, files=(), suggestion=None):
        self.n += 1
        job_id, sid = f'aj_{self.n:016x}', suggestion or f's{self.n}'
        with self.store.connect() as db:
            if card and not suggestion:
                db.execute("INSERT INTO suggestions(id,dedupe_key,account_ids,event_ids,title,body,status,created_at) VALUES(?,?,'[]','[]',?,?,?,?)",
                           (sid, 'k-' + sid, 'Title', 'Body', card, ago(30)))
            db.execute('INSERT INTO agent_jobs(id,suggestion_id,tool,place,status,brief,asks,turns,outcome,session_id,files,created_at,updated_at,finished_at) '
                       'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (job_id, sid, 'codex', 'local', status, 'The brief', '[]', 1, outcome, 'thread-1',
                        json.dumps([{'path': f, 'size': 1} for f in files]), ago(ended + 1), ago(ended), ago(ended)))
        work = self.root / job_id / 'work'
        for rel in ('BRIEF.md', '.claude/settings.json', 'card/messages.md', 'site/node_modules/big.bin', 'site/index.html',
                    'publish.sh', 'out/report.pdf', '.npm-cache/x'):
            (work / rel).parent.mkdir(parents=True, exist_ok=True)
            (work / rel).write_text('x' * 1000)
        (self.root / job_id / 'git' / 'objects').mkdir(parents=True)
        (self.root / job_id / 'git' / 'objects' / 'pack').write_text('x' * 5000)
        (self.root / job_id / 'turn-1.jsonl').write_text('{}\n')
        return job_id

    def left(self, job_id):
        work = self.root / job_id / 'work'
        return sorted(p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file())

    def test_a_finished_job_is_cleared_after_the_grace_and_what_its_to_do_links_to_stays(self):
        job_id = self.job(files=['publish.sh', 'out/report.pdf'], ended=agent_workspaces.GRACE_DAYS + 1)
        report = agent_workspaces.prune(self.store.connect, self.root, NOW)
        self.assertEqual(report['cleared'], [job_id])
        self.assertGreater(report['freed_bytes'], 5000)
        self.assertEqual(self.left(job_id), ['.claude/settings.json', 'BRIEF.md', 'out/report.pdf', 'publish.sh'])
        self.assertFalse((self.root / job_id / 'git').exists())
        self.assertTrue((self.root / job_id / 'turn-1.jsonl').exists())  # its answers still show
        self.assertEqual(self.jobs.file(job_id, 'publish.sh').read_text(), 'x' * 1000)  # the to-do's link still opens
        marker = json.loads((self.root / job_id / agent_workspaces.MARKER).read_text())
        self.assertEqual(marker['kept'], ['out/report.pdf', 'publish.sh'])
        self.assertEqual(agent_workspaces.prune(self.store.connect, self.root, NOW)['cleared'], [])  # once

    def test_a_job_that_can_still_go_on_keeps_its_folder(self):
        old = agent_workspaces.GRACE_DAYS + 20
        kept = {
            self.job(status='failed', card='pending', ended=old): 'to-do open',  # Try again
            self.job(status='cancelled', card='snoozed', ended=old): 'to-do open',
            self.job(status='result', card='prepared', ended=old): 'to-do open',  # Ask for changes
            self.job(status='running', ended=old): 'running',
            self.job(status='sent', ended=old): 'running',
        }
        relayed = self.job(status='result', card=None, suggestion=agent_jobs.RELAYED + 'ab12', ended=old)
        with self.store.connect() as db:
            db.execute(agent_remote.RELAY_SCHEMA)
            db.execute('INSERT INTO agent_relayed(ticket_hash,job_id,reported,created_at) VALUES(?,?,0,?)', ('h' * 64, relayed, ago(old)))
        kept[relayed] = 'not reported back'  # the hosted Machine hasn't heard its result yet
        before = {job_id: self.left(job_id) for job_id in kept}
        report = agent_workspaces.prune(self.store.connect, self.root, NOW)
        self.assertEqual(report['cleared'], [])
        self.assertEqual(report['kept'], kept)
        self.assertEqual({job_id: self.left(job_id) for job_id in kept}, before)
        with self.store.connect() as db:
            db.execute('UPDATE agent_relayed SET reported=1')
            db.execute("UPDATE suggestions SET status='completed' WHERE id IN (SELECT suggestion_id FROM agent_jobs WHERE status='failed')")
        cleared = agent_workspaces.prune(self.store.connect, self.root, NOW)['cleared']
        self.assertEqual(sorted(cleared), sorted([relayed] + [j for j, why in kept.items() if why == 'to-do open'][:1]))

    def test_at_most_a_few_finished_folders_stay_within_the_grace(self):
        recent = [self.job(ended=n / 10, card='rejected' if n % 2 else 'completed') for n in range(5)]  # newest first
        old = self.job(ended=agent_workspaces.GRACE_DAYS + 1)
        report = agent_workspaces.prune(self.store.connect, self.root, NOW)
        self.assertEqual(sorted(report['cleared']), sorted(recent[agent_workspaces.KEEP_FINISHED:] + [old]))
        self.assertEqual({j: report['kept'][j] for j in recent[:agent_workspaces.KEEP_FINISHED]}, dict.fromkeys(recent[:3], 'recent'))
        self.assertIn('site/index.html', self.left(recent[0]))

    def test_a_job_picked_up_again_counts_afresh_and_unknown_folders_stay(self):
        job_id = self.job(ended=agent_workspaces.GRACE_DAYS + 1, files=['publish.sh'])
        stray = self.root / 'aj_ffffffffffffffff' / 'work'
        stray.mkdir(parents=True)
        (stray / 'big.bin').write_text('x')
        agent_workspaces.prune(self.store.connect, self.root, NOW)
        (self.root / job_id / 'work' / 'again.bin').write_text('x')  # it ran again after Try again on a reopened to-do
        with self.store.connect() as db:
            db.execute('UPDATE agent_jobs SET updated_at=? WHERE id=?', (ago(1), job_id))
        self.assertEqual(agent_workspaces.prune(self.store.connect, self.root, NOW)['kept'][job_id], 'recent')
        self.assertEqual(agent_workspaces.prune(self.store.connect, self.root, NOW + dt.timedelta(days=10))['cleared'], [job_id])
        self.assertEqual(self.left(job_id), ['.claude/settings.json', 'BRIEF.md', 'publish.sh'])
        self.assertTrue((stray / 'big.bin').exists())

    def test_a_link_in_the_folder_is_removed_never_followed(self):
        outside = self.dir / 'outside'
        outside.mkdir()
        (outside / 'keep.txt').write_text('mine')
        job_id = self.job(ended=agent_workspaces.GRACE_DAYS + 1, files=['linked'])
        (self.root / job_id / 'work' / 'linked').symlink_to(outside, target_is_directory=True)
        (self.root / job_id / 'work' / 'file-link').symlink_to(outside / 'keep.txt')
        agent_workspaces.prune(self.store.connect, self.root, NOW)
        self.assertFalse((self.root / job_id / 'work' / 'linked').is_symlink())
        self.assertFalse((self.root / job_id / 'work' / 'file-link').is_symlink())
        self.assertEqual((outside / 'keep.txt').read_text(), 'mine')

    def test_the_nightly_run_clears_them(self):
        job_id = self.job(ended=agent_workspaces.GRACE_DAYS + 1)
        report = retention.run(self.store.connect, str(self.dir / 'events.sqlite'), now=NOW, busy=0)
        self.assertEqual(report['agent_workspaces']['cleared'], 1)
        self.assertEqual(self.left(job_id), ['.claude/settings.json', 'BRIEF.md'])


if __name__ == '__main__':
    unittest.main()
