"""What an export holds from outside the data folder (inventory.HOME_AREAS), and how an import puts it back.

- OpenClaw: its conversations and memory index (agents/<agent>/agent/openclaw-agent.sqlite), the transcripts
  (agents/<agent>/sessions, without the ones deleted), its state (scheduled jobs, plugin memory), skills made in the
  workshop and the photos and files in chats (media/inbound, outbound, made images). Its databases also hold sign-ins
  (auth profiles, its secret store, device keys): an export without keys leaves those tables empty, and an import
  keeps the new install's own sign-ins in them, whatever the export had.
- Agent jobs: Claude Code's and Codex's own transcripts of each job's session, so a follow-up can resume it.
- The X and LinkedIn send logs (so nothing goes twice) and self-fixes being prepared.

Entries in an export: openclaw/<path under OpenClaw's folder>, home/<path under the home folder> and
agents-home/claude|codex/<path>."""
import os
import re
import shutil
import sqlite3
from contextlib import closing
from pathlib import Path

from machine.export import inventory

DELETED = re.compile(r'\.deleted\.|\.reset\.')  # a conversation the owner deleted or reset: OpenClaw keeps it a while
OPENCLAW_DBS = ('agents/*/agent/openclaw-agent.sqlite', 'state/openclaw.sqlite')
OPENCLAW_FOLDERS = ('agents/*/sessions', 'agents/*/agent/workshop-skills', 'media/inbound', 'media/outbound',
                    'media/tool-image-generation')
HOME_FILES = ('.local/share/x-inbox/sends.jsonl', '.local/share/linkedin-inbox/sends.jsonl')
HOME_FOLDERS = ('.cache/the-machine/fixes',)
SKIP_SUFFIXES = ('.lock', '-wal', '-shm', '-journal', '.tmp')


def _files_under(root):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not Path(base, d).is_symlink() and d not in ('node_modules', '__pycache__'))
        for name in sorted(names):
            path = Path(base) / name
            if path.is_file() and not path.is_symlink() and not name.endswith(SKIP_SUFFIXES):
                yield path


def items(openclaw_home, home=None, main_db=None, config=None, left_out=None):
    """[(kind, path, entry)]: kind 'openclaw-db' (copied, its sign-in tables emptied without keys) or 'file'."""
    openclaw_home, home = Path(openclaw_home), Path(home or Path.home())
    found = []
    for pattern in OPENCLAW_DBS:
        for path in sorted(openclaw_home.glob(pattern)):
            if path.is_file() and not path.is_symlink():
                found.append(('openclaw-db', path, f'openclaw/{path.relative_to(openclaw_home)}'))
    for pattern in OPENCLAW_FOLDERS:
        for folder in sorted(openclaw_home.glob(pattern)):
            for path in _files_under(folder) if folder.is_dir() and not folder.is_symlink() else []:
                if DELETED.search(path.name):
                    if left_out is not None:
                        left_out['deleted conversations'] = left_out.get('deleted conversations', 0) + path.stat().st_size
                    continue
                found.append(('file', path, f'openclaw/{path.relative_to(openclaw_home)}'))
    for name in HOME_FILES:
        path = home / name
        if path.is_file() and not path.is_symlink():
            found.append(('file', path, f'home/{name}'))
    for name in HOME_FOLDERS:
        for path in _files_under(home / name) if (home / name).is_dir() else []:
            found.append(('file', path, f'home/{path.relative_to(home)}'))
    found += job_transcripts(main_db, config or {}, home)
    return found


def _own_home(home):
    """Whether `home` is this account's own home folder: only then do CLAUDE_CONFIG_DIR and CODEX_HOME count."""
    return Path(home).expanduser().resolve() == Path.home().resolve()


def _claude_dir(config, home):
    found = ((config.get('agents') or {}).get('claude') or {}).get('config_dir') or (
        os.environ.get('CLAUDE_CONFIG_DIR') if _own_home(home) else None)
    return Path(os.path.expanduser(str(found))) if found else Path(home) / '.claude'


def _codex_dir(home):
    return Path(os.environ.get('CODEX_HOME') if _own_home(home) and os.environ.get('CODEX_HOME') else Path(home) / '.codex')


def job_transcripts(main_db, config, home):
    """Claude Code's and Codex's own transcripts of the sessions agent jobs ran in."""
    if not main_db or not Path(main_db).is_file():
        return []
    try:
        with closing(sqlite3.connect(f'file:{main_db}?mode=ro', uri=True, timeout=30)) as db:
            sessions = db.execute("SELECT DISTINCT tool,session_id FROM agent_jobs WHERE session_id IS NOT NULL AND session_id!=''").fetchall()
    except sqlite3.Error:
        return []
    found, claude, codex = [], _claude_dir(config, home), _codex_dir(home)
    for tool, session in sessions:
        if not re.fullmatch(r'[0-9A-Za-z-]{8,80}', str(session)):
            continue
        if tool == 'claude':
            for path in sorted((claude / 'projects').glob(f'*/{session}.jsonl')):
                found.append(('file', path, f'agents-home/claude/{path.relative_to(claude / "projects")}'))
        elif tool == 'codex':
            for path in sorted((codex / 'sessions').glob(f'**/*{session}*.jsonl')):
                found.append(('file', path, f'agents-home/codex/{path.relative_to(codex / "sessions")}'))
    return found


def secret_tables(db):
    return [name for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")
            if inventory.OPENCLAW_SECRET.search(name) and not name.startswith('sqlite_')]


def copy_db(path, copy, keys):
    """A consistent copy of an OpenClaw database at `copy`; without keys, its sign-in tables emptied. Returns the
    tables emptied."""
    with closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=30)) as source, closing(sqlite3.connect(copy)) as target:
        source.backup(target)
    emptied = []
    if not keys:
        with closing(sqlite3.connect(copy)) as db:
            for table in secret_tables(db):
                try:
                    db.execute(f'DELETE FROM "{table}"')
                    emptied.append(table)
                except sqlite3.Error:  # a virtual table whose module isn't here: its rows are in its own tables
                    pass
            db.commit()
            db.execute('VACUUM')
    return emptied


def _busy(path):
    return any(Path(str(path) + suffix).exists() for suffix in ('-wal', '-shm', '-journal'))


def restore_db(source, target, notes, stamp):
    """Put an exported OpenClaw database in place. The new install's own sign-ins stay: each sign-in table that has
    rows here keeps them. A database that is open (OpenClaw runs) is left for `assistant import --finish`.
    Returns where it went."""
    target = Path(target)
    if _busy(target):
        pending = target.parent / f'{target.name}.from-export'
        shutil.copyfile(source, pending)
        os.chmod(pending, 0o600)
        notes.append(f'OpenClaw is running, so its conversations wait in {pending}. Stop the OpenClaw Gateway, then run: '
                     'assistant import --finish')
        return pending
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    work = target.parent / f'.{target.name}.import'
    shutil.copyfile(source, work)
    try:
        if target.exists():
            keep = target.with_name(f'{target.name}.before-import-{stamp}')
            shutil.copyfile(target, keep)
            _keep_signins(work, target)
        os.chmod(work, 0o600)
        os.replace(work, target)
    finally:
        Path(work).unlink(missing_ok=True)
    return target


def _keep_signins(work, current):
    with closing(sqlite3.connect(work)) as db:
        db.execute('ATTACH DATABASE ? AS here', (str(current),))
        here = {name for (name,) in db.execute("SELECT name FROM here.sqlite_master WHERE type='table'")}
        for table in secret_tables(db):
            if table not in here or not db.execute(f'SELECT 1 FROM here."{table}" LIMIT 1').fetchone():
                continue
            try:
                db.execute('SAVEPOINT keep')
                db.execute(f'DELETE FROM main."{table}"')
                db.execute(f'INSERT INTO main."{table}" SELECT * FROM here."{table}"')
                db.execute('RELEASE keep')
            except sqlite3.Error:  # its columns changed between versions: the new install's own table wins whole
                db.execute('ROLLBACK TO keep')
                db.execute('RELEASE keep')
        db.commit()
        db.execute('DETACH DATABASE here')


def finish(openclaw_home, notes, stamp):
    """`assistant import --finish`: the OpenClaw databases an import left waiting while OpenClaw ran."""
    done = []
    for pattern in OPENCLAW_DBS:
        for target in sorted(Path(openclaw_home).glob(pattern)):
            pending = target.parent / f'{target.name}.from-export'
            if pending.is_file():
                if _busy(target):
                    notes.append(f'OpenClaw still runs: stop the OpenClaw Gateway first ({target})')
                    continue
                done.append(str(restore_db(pending, target, notes, stamp)))
                pending.unlink()
    return done


def target_for(entry, openclaw_home, home, data, config):
    """Where an exported entry from outside the data folder goes on this computer, or None."""
    parts = Path(entry).parts
    if parts[0] == 'openclaw':
        return Path(openclaw_home).joinpath(*parts[1:])
    if parts[0] == 'home':
        return Path(home).joinpath(*parts[1:])
    if parts[0] == 'agents-home' and len(parts) > 2 and parts[1] == 'claude':
        # Claude Code names a project's folder after its path: the job's folder is under this data folder now
        folder = parts[2]
        moved = re.sub(r'^.*?(-agent-jobs-)', lambda m: re.sub(r'[^A-Za-z0-9]', '-', str(data)) + m.group(1), folder)
        return _claude_dir(config, Path(home)) / 'projects' / moved / Path(*parts[3:])
    if parts[0] == 'agents-home' and len(parts) > 2 and parts[1] == 'codex':
        return _codex_dir(Path(home)) / 'sessions' / Path(*parts[2:])
    return None
