#!/usr/bin/env python3
"""Signed releases of The Machine.

A release is a git tag `release-YYYYMMDD-HHMM` on a commit of main, signed with the release key (an SSH key). Hosted
Machines and `update` below only install a release whose signature checks out against the public key in the code
that is already installed (deploy/release-signers), so a pushed commit alone never reaches a Machine.

  python3 scripts/release.py cut       sign origin/main as a new release and push the tag (needs the private key and a
                                        passed full test run on that commit; --commit SHA cuts an older one of main;
                                        --full-run waits for that run when one is going, or starts it on our CI
                                        runner when there is none, about 12 minutes, and cuts when it passes)
  python3 scripts/release.py verify    check a release tag (default: the newest) against deploy/release-signers
  python3 scripts/release.py update    self-hosted: move this checkout to the newest signed release, then ./install.sh
                                        (a first ./install.sh does this step by itself: first_install)
                                        (--install: only when nothing runs, and runs ./install.sh itself; the daily
                                        update timer that install.sh sets up calls this)

The private key is read from $THE_MACHINE_RELEASE_KEY, else ~/.config/the-machine-release/signing-key."""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    from scripts.security_gate import require_release_scan
    from scripts import ci_runs as ci
except ModuleNotFoundError:
    from security_gate import require_release_scan
    import ci_runs as ci

ROOT = Path(__file__).resolve().parent.parent
SIGNERS = ROOT / 'deploy' / 'release-signers'
TAG = re.compile(r'release-\d{8}-\d{4}')
PRINCIPAL = 'release@themachine.computer'
BEGIN = b'-----BEGIN SSH SIGNATURE-----\n'
END = b'-----END SSH SIGNATURE-----\n'


class Refused(Exception):
    pass


REPO = 'Salesflare/TheMachine'
# The runs of .github/workflows/ci.yml on main's commits: a push to main, the nightly and weekly runs and a manual one.
# A pull request's run tests its merge commit, not main's.
FULL_RUN = ('push', 'schedule', 'workflow_dispatch')


def ci_runs(query):
    """CI's runs of the tests (GitHub's API through gh), newest first."""
    out = subprocess.run(['gh', 'api', f'repos/{REPO}/actions/workflows/ci.yml/runs?{query}&per_page=30'],
                         capture_output=True, text=True, timeout=60, check=True).stdout
    return json.loads(out)['workflow_runs']


def _gh_api(path):
    return json.loads(subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=60, check=True).stdout)


def proven(run):
    """Whether a passed run proves its commit: it ran every test on it (scripts/ci_runs.py). A push to main that ran
    only the tests its changes since the last full run need is not enough for a release: a dependency the selection
    missed must never reach one."""
    return ci.tested(run, _gh_api) == 'full'


class Going(RuntimeError):
    """A full test run on the commit is still going (run: GitHub's run)."""

    def __init__(self, message, run):
        super().__init__(message)
        self.run = run


def wait_for(run, poll=30, limit=45 * 60):
    """Waits until a run of CI is done."""
    started = time.time()
    print(f'A full test run is going on {run["head_sha"][:7]} ({run["html_url"]}): waiting for it...', flush=True)
    while time.time() - started < limit:
        try:
            if _gh_api(f'repos/{REPO}/actions/runs/{run["id"]}').get('status') == 'completed':
                return
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
        time.sleep(poll)
    raise RuntimeError(f'the full test run on {run["head_sha"][:7]} did not finish in {limit // 60} minutes')


def full_run(sha, poll=30, limit=45 * 60):
    """Starts the full test run on exactly this commit on our runner (ci.yml, workflow_dispatch with own_runner, from a
    short-lived branch at the commit), waits for it and raises RuntimeError unless it passed."""
    branch = f'full-run/{sha[:12]}'
    git('push', '--quiet', 'origin', f'{sha}:refs/heads/{branch}')
    started = time.time()
    try:
        subprocess.run(['gh', 'workflow', 'run', 'ci.yml', '-R', REPO, '--ref', branch, '-f', 'own_runner=true'],
                       capture_output=True, text=True, timeout=60, check=True)
        print(f'Full test run started on {sha[:7]}: waiting for it (about 12 minutes)...', flush=True)
        while time.time() - started < limit:
            time.sleep(poll)
            mine = [r for r in ci_runs(f'head_sha={sha}') if r['event'] == 'workflow_dispatch'
                    and dt.datetime.fromisoformat(r['created_at'].replace('Z', '+00:00')).timestamp() >= started - 60]
            if mine and all(r['status'] == 'completed' for r in mine):
                break
        else:
            raise RuntimeError(f'the full test run on {sha[:7]} did not finish in {limit // 60} minutes')
    except subprocess.SubprocessError as error:
        raise RuntimeError(f'the full test run on {sha[:7]} could not be started ({error})') from error
    finally:
        git('push', '--quiet', 'origin', '--delete', branch, check=False)
    require_green_tests(sha)


def require_green_tests(sha):
    """Raises RuntimeError unless every test passed on exactly this commit: a full run passed on it."""
    try:
        runs = [r for r in ci_runs(f'head_sha={sha}') if r['event'] in FULL_RUN]
        if any(r['conclusion'] == 'success' and proven(r) for r in runs):
            return
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise RuntimeError(f"CI's runs on {sha[:7]} could not be read with gh ({error})") from error
    # a run still going that tests every file: wait for it; one that tests only what changed since a full run is no
    # proof when it passes
    try:
        going = [r for r in runs if r['status'] != 'completed' and ci.testing_full(r, _gh_api)]
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise RuntimeError(f"CI's runs on {sha[:7]} could not be read with gh ({error})") from error
    if going:
        raise Going(f'the full test run on {sha[:7]} is not done yet ({going[0]["html_url"]}): cut again when it passes, '
                    'or with --full-run, which waits for it', going[0])
    failed = [r for r in runs if r['status'] == 'completed' and r['conclusion'] not in ('cancelled', 'skipped', 'success')]
    if failed:
        raise RuntimeError(f'the full test run on {sha[:7]} {failed[0]["conclusion"]} ({failed[0]["html_url"]})')
    newest = None
    try:
        newest = next((r['head_sha'] for r in ci_runs('branch=main&status=success') if r['event'] in FULL_RUN
                       and git('merge-base', '--is-ancestor', r['head_sha'], sha, check=False).returncode == 0 and proven(r)), None)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        pass
    raise RuntimeError(f'no full test run passed on {sha[:7]} (main tests only what changed; --full-run runs every test on it and cuts when it passes)'
                       + (f': wait for it, or cut the newest tested commit with --commit {newest[:7]}' if newest else ''))


def git(*args, check=True, raw=False):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=not raw)
    if check and result.returncode:
        raise SystemExit(f'git {" ".join(args)} failed: {(result.stderr or b"").strip() if raw else result.stderr.strip()}')
    return result


def signed_commit(raw: bytes, tag: str, signers: str) -> str:
    """The commit a raw tag object points to, if it is the release `tag` signed by one of `signers` (allowed-signers
    lines). Raises Refused otherwise. The same check runs on hosted Machines and on the control plane."""
    if not TAG.fullmatch(tag):
        raise Refused(f'{tag} is not a release tag')
    start = raw.rfind(b'\n' + BEGIN)
    if start < 0 or not raw.endswith(END):
        raise Refused(f'{tag} is not signed')
    payload, signature = raw[:start + 1], raw[start + 1:]
    head = payload.split(b'\n\n', 1)[0].decode('utf-8', 'replace').split('\n')
    found = re.fullmatch(r'object ([0-9a-f]{40})', head[0]) if head else None
    if not found or head[1:3] != ['type commit', f'tag {tag}']:
        raise Refused(f'{tag} does not name itself or a commit')
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / 'signers').write_text(signers)
        (Path(tmp) / 'sig').write_bytes(signature)
        result = subprocess.run(['ssh-keygen', '-Y', 'verify', '-f', str(Path(tmp) / 'signers'), '-I', PRINCIPAL, '-n', 'git',
                                 '-s', str(Path(tmp) / 'sig')], input=payload, capture_output=True)
    if result.returncode:
        raise Refused(f'{tag} is not signed with the release key')
    return found.group(1)


def releases():
    names = git('tag', '--list', 'release-*').stdout.split()
    return sorted(n for n in names if TAG.fullmatch(n))


def verify(tag=None, signers=None):
    """The commit of a verified release tag (default: the newest)."""
    tag = tag or (releases() or [None])[-1]
    if not tag:
        raise Refused('there is no release yet')
    raw = git('cat-file', 'tag', f'refs/tags/{tag}', raw=True).stdout
    return tag, signed_commit(raw, tag, signers if signers is not None else SIGNERS.read_text())


WHATS_NEW = 'machine/store/whats_new.py'


def whats_new_entries(source):
    """The ENTRIES list of a whats_new.py source, read without running it; ValueError when it isn't a plain list."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ENTRIES' for t in node.targets):
            try:
                found = ast.literal_eval(node.value)
            except ValueError:
                break
            if isinstance(found, list):
                return found
    raise ValueError('ENTRIES is not a plain list')


def whats_new_problems(source, before=None):
    """What's new candidates this release adds (ids not in `before`, the last release's file) that are not valid
    (machine/store/whats_new.py problems), as 'id: problem' lines. Nothing more is checked."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from machine.store.whats_new import problems
    try:
        entries = whats_new_entries(source)
        known = {e.get('id') for e in whats_new_entries(before) if isinstance(e, dict)} if before else set()
    except (SyntaxError, ValueError) as error:
        return [str(error)]
    ids = [e.get('id') if isinstance(e, dict) else None for e in entries]
    found = [f'{i}: id used twice' for i in sorted({i for i in ids if i and ids.count(i) > 1})]
    for entry, i in zip(entries, ids):
        if i not in known:
            found += [f'{i}: {p}' for p in problems(entry)]
    return found


def cut(args):
    key = Path(args.key or os.environ.get('THE_MACHINE_RELEASE_KEY') or Path.home() / '.config/the-machine-release/signing-key')
    if not key.exists():
        raise SystemExit(f'No release key at {key}. Only the release key holder can cut a release.')
    git('fetch', '--quiet', '--tags', 'origin', 'main')
    sha = git('rev-parse', 'origin/main^{commit}').stdout.strip()
    if args.commit:
        sha = git('rev-parse', f'{args.commit}^{{commit}}').stdout.strip()
        if git('merge-base', '--is-ancestor', sha, 'origin/main', check=False).returncode:
            raise SystemExit(f'Not released: {args.commit} is not on origin/main.')
    for name in reversed(releases()):
        if git('rev-parse', f'{name}^{{commit}}').stdout.strip() == sha:
            print(f'origin/main ({sha[:7]}) is already released as {name}.')
            return
    tag = 'release-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M')
    if git('rev-parse', '-q', '--verify', f'refs/tags/{tag}', check=False).returncode == 0:
        raise SystemExit(f'{tag} exists already: wait a minute and try again.')
    last = releases()[-1] if releases() else None
    show = lambda ref: (lambda r: r.stdout if r.returncode == 0 else None)(git('show', f'{ref}:{WHATS_NEW}', check=False))
    bad = whats_new_problems(show(sha) or 'ENTRIES = []', show(last) if last else None)
    if bad:
        raise SystemExit("Not released: What's new candidates to fix first:\n  " + '\n  '.join(bad))
    try:
        try:
            require_green_tests(sha)
        except Going as going:
            if not args.full_run:
                raise
            wait_for(going.run)  # the one going already, then the same check
            require_green_tests(sha)
        except RuntimeError as missing:
            if not args.full_run or 'no full test run passed' not in str(missing):
                raise
            full_run(sha)
        require_release_scan('TheMachine', sha, cwd=ROOT)
    except RuntimeError as error:
        raise SystemExit(f'Not released: {error}') from error
    subject = git('log', '-1', '--format=%s', sha).stdout.strip()
    git('-c', 'gpg.format=ssh', '-c', f'user.signingkey={key}', '-c', f'user.name=The Machine releases', '-c', f'user.email={PRINCIPAL}',
        'tag', '-s', '-m', f'The Machine {tag}\n\nUp to: {subject}', tag, sha)
    try:
        verify(tag)
    except Refused as error:
        git('tag', '-d', tag, check=False)
        raise SystemExit(f'Not released: {error}. Is {key} the key in deploy/release-signers?')
    if not args.no_push:
        git('push', '--quiet', 'origin', f'refs/tags/{tag}')
    print(f'Released {sha[:7]} as {tag}{"" if args.no_push else " (pushed)"}. Salesflare Machines take it first; '
          'everyone else after the soak time, or sooner when promoted on /admin.')


# Where an update sets aside the Machine's own commits that don't apply on a release (and uncommitted changes that
# are in its way): one ref per commit, so nothing is lost and the service brings each back to the owner as a to-do
# (parked_fixes.py, which names the same folder).
PARKED = 'refs/machine/parked/'
STASH_NOTE = 'Uncommitted changes set aside by an update'
NAMED = ('-c', 'user.name=m', '-c', 'user.email=m@localhost')  # for git runs that make a commit
SHA = re.compile(r'[0-9a-f]{40}')


def undo_cut_off():
    """A run cut off halfway (a restart, a crash) can leave a rebase or a cherry-pick going, with HEAD detached on the
    release: undo it, so HEAD is the Machine's own branch again and none of its own commits is left only in the reflog.
    Before anything looks at HEAD."""
    where = lambda name: ROOT / git('rev-parse', '--git-path', name, check=False).stdout.strip()
    if where('rebase-merge').exists() or where('rebase-apply').exists():
        git('rebase', '--abort', check=False)
    if where('CHERRY_PICK_HEAD').exists():
        git('cherry-pick', '--abort', check=False)


# Where an update notes each file the owner added that it moved aside (keep_local_files): one tab-separated line per
# file (when, release commit, path, where it is now), in the checkout's git folder.
KEPT = 'machine-kept-local'


def keep_local_files(sha):
    """Files the owner added here (untracked, ignored ones too) at a path where the release brings a file of its own:
    git refuses to move over one (the Machine would stay on an old version) and overwrites an ignored one without a
    word. Each is moved aside next to itself as <name>.local-<date> and noted in KEPT, before anything moves.
    [(path, backup)], or OSError when one can't be moved (the ones already moved are put back)."""
    tracked = set(git('ls-files', '-z').stdout.split('\0'))
    taken = set(git('ls-tree', '-r', '-z', '--name-only', sha).stdout.split('\0')) - {''}
    incoming, in_way = sorted(taken - tracked), set()
    for path in incoming:
        parts = path.split('/')
        for depth in range(1, len(parts) + 1):
            here = '/'.join(parts[:depth])
            if here in tracked or not os.path.lexists(ROOT / here):
                continue
            last, is_dir = depth == len(parts), (ROOT / here).is_dir() and not (ROOT / here).is_symlink()
            if (not last and not is_dir) or (last and not (is_dir and git('ls-files', '-z', '--', here).stdout)):
                in_way.add(here)  # a file where the release has a folder, or anything where it has a file
                break
    in_way = sorted(p for p in in_way if not any(p.startswith(q + '/') for q in in_way))
    day, kept = dt.date.today().strftime('%Y%m%d'), []
    log = ROOT / git('rev-parse', '--git-path', KEPT).stdout.strip()
    try:
        for path in in_way:
            backup, n = f'{path}.local-{day}', 1
            while os.path.lexists(ROOT / backup) or backup in taken:
                n += 1
                backup = f'{path}.local-{day}-{n}'
            os.rename(ROOT / path, ROOT / backup)
            kept.append((path, backup))
            with open(log, 'a', encoding='utf-8') as out:
                out.write(f'{dt.datetime.now().isoformat(timespec="seconds")}\t{sha}\t{path}\t{backup}\n')
    except OSError:
        put_back(kept)
        raise
    return kept


def put_back(kept):
    """Back where they were, when the checkout didn't move after all."""
    for path, backup in reversed(kept):
        try:
            if not os.path.lexists(ROOT / path):
                os.rename(ROOT / backup, ROOT / path)
        except OSError:
            pass  # it stays at its backup name, noted in KEPT


def move_to(sha, ref='main'):
    """Onto a verified release (moved_to below), with files the owner added in its way kept aside first
    (keep_local_files): its result, with .kept: [(path, backup)]. When the checkout doesn't move, they are put back."""
    undo_cut_off()
    try:
        kept = keep_local_files(sha)
    except OSError as error:
        result = subprocess.CompletedProcess([], 1, '', f'a file added here is in the way and could not be moved aside: {error}')
        result.parked, result.kept = [], []
        return result
    result = moved_to(sha, ref)
    if result.returncode:
        put_back(kept)
        kept = []
    result.kept = kept
    return result


def moved_to(sha, ref='main'):
    """Onto a verified release the way hosted Machines move: a fast-forward; else, with no commits of its own (all are
    on the branch or in a release), straight there; else its own commits (merged self-fixes) replayed on top, one at a
    time. Uncommitted changes are kept. Each own commit that doesn't apply, and changes that don't fit back on top, are
    set aside under PARKED and the checkout moves to the release anyway: a Machine never stays behind on an old version.
    The git run that decided it, with .parked: what was set aside (own commits oldest first, then the changes)."""
    run = lambda *args: git(*args, check=False)
    if run('merge-base', '--is-ancestor', 'HEAD', sha).returncode == 0:
        result, own = run('merge', '--ff-only', '--quiet', sha), []
    else:
        before = run('rev-parse', '-q', '--verify', f'origin/{ref}@{{1}}').stdout.strip()  # the branch before a rewrite
        own = run('rev-list', '--reverse', 'HEAD', '--not', sha, f'refs/remotes/origin/{ref}', '--tags=release-*',
                  *([before] if before else [])).stdout.split()
        result = None if own else run('reset', '--keep', '-q', sha)
    if result is not None and result.returncode == 0:
        result.parked = []
        return result
    # Each own commit is kept under PARKED before anything moves, so a run cut off from here on loses none of them;
    # the ones that replay drop their ref again. Uncommitted changes go aside the same way, only once their ref holds.
    for commit in own:
        run('update-ref', PARKED + commit, commit)
    changes = run(*NAMED, 'stash', 'create', STASH_NOTE).stdout.strip()
    if not SHA.fullmatch(changes) or run('update-ref', PARKED + changes, changes).returncode:
        changes = ''  # nothing to set aside, or it can't be kept: the checkout is left as it is
    if changes:
        run('reset', '--hard', '-q', 'HEAD')
    in_release = {line[2:] for line in run('cherry', sha, 'HEAD').stdout.splitlines() if line.startswith('- ')}
    result, parked = run('reset', '--keep', '-q', sha), []
    for commit in own:
        if result.returncode or commit in in_release:  # it didn't move (it stays on the old checkout), or it's in the release
            run('update-ref', '-d', PARKED + commit)
        elif run(*NAMED, 'cherry-pick', commit).returncode:
            run('cherry-pick', '--abort')
            parked.append(commit)
        else:
            run('update-ref', '-d', PARKED + commit)
    if changes and run('stash', 'apply', '-q', changes).returncode:
        run('reset', '--hard', '-q', 'HEAD')  # they don't fit on the release: they stay under PARKED
        parked.append(changes)
    elif changes:
        run('update-ref', '-d', PARKED + changes)
    result.parked = parked
    return result


def moved(tag, result):
    """What the update did with the Machine's own commits, for its log line; SystemExit when it didn't move."""
    if result.returncode:
        raise SystemExit(f'{tag} is verified, but the checkout could not move to it: nothing changed. '
                         + (result.stderr or result.stdout).strip()[-300:])
    note = ''
    if getattr(result, 'kept', None):
        note += (f' {len(result.kept)} file(s) added on this Machine were where the release has files of its own, so '
                 'they were kept under a new name: ' + ', '.join(f'{p} is now {b}' for p, b in result.kept) + '.')
    if result.parked:
        note += (f' {len(result.parked)} of this Machine\'s own changes did not apply on it, so they were set aside '
                 f'({PARKED}); each comes back to the owner as a to-do.')
    return note


def first_install():
    """A fresh install from a clone (./install.sh with no config yet) starts from the newest signed release, not from
    whatever main is: (tag, sha) when the checkout moved there, None when it is already on it; Refused or SystemExit
    when no release verifies or the checkout can't move (nothing changed then)."""
    git('fetch', '--quiet', '--tags', 'origin')
    tag, sha = verify()
    undo_cut_off()
    if git('rev-parse', 'HEAD').stdout.strip() == sha:
        return None
    note = moved(tag, move_to(sha))
    if note:
        print(note.strip())
    return tag, sha


def busy():
    """Work that a restart would cut off, or no way to tell: only `assistant busy` exiting 0 means idle."""
    return subprocess.run([sys.executable, str(ROOT / 'cli.py'), 'busy'], cwd=ROOT, capture_output=True,
                          text=True).returncode != 0


# The installer as the nightly update runs it: a changed bridge never goes in as a swap inside the running Gateway,
# only on a quiet night with the Gateway restarted around it; until then it waits and the install still ends well
# (installer.py staged_swap). A bridge that keeps failing becomes one owner to-do, never a failed update unit.
UNATTENDED = ('--non-interactive', '--unattended')


def update(args):
    git('fetch', '--quiet', '--tags', 'origin')
    tag, sha = verify(args.tag)
    undo_cut_off()
    if git('merge-base', '--is-ancestor', sha, 'HEAD', check=False).returncode == 0:
        print(f'Already on {tag} or newer.')
        if args.install and not busy():
            # A changed bridge that could not go into OpenClaw last time (its memory index was running, or the night
            # was not quiet) is tried again; with none waiting the installer does nothing.
            code = subprocess.run([str(ROOT / 'install.sh'), *UNATTENDED, '--if-bridge-waits'], cwd=ROOT).returncode
            if code:
                raise SystemExit(f'./install.sh failed (exit {code}): the bridge that was waiting is still not in OpenClaw.')
        return
    if args.install and busy():
        print(f'{tag} is ready, but something is running: trying again next time.')
        return
    note = moved(tag, move_to(sha))
    print(f'Updated to {tag} ({sha[:7]}), signature verified.' + note + ('' if args.install else ' Now run ./install.sh'))
    if args.install:
        code = subprocess.run([str(ROOT / 'install.sh'), *UNATTENDED], cwd=ROOT).returncode
        if code:
            raise SystemExit(f'./install.sh failed (exit {code}) after the update to {tag}.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('cut', help='sign origin/main as a new release and push it')
    c.add_argument('--key', help='private key file (default: $THE_MACHINE_RELEASE_KEY or ~/.config/the-machine-release/signing-key)')
    c.add_argument('--no-push', action='store_true', help='tag and verify locally only')
    c.add_argument('--commit', help='a commit of main to sign instead of its newest (one whose full test run passed)')
    c.add_argument('--full-run', action='store_true', help='no full test run passed on it: start one on our runner, wait, cut when it passes')
    v = sub.add_parser('verify', help='check a release tag against deploy/release-signers')
    v.add_argument('tag', nargs='?')
    u = sub.add_parser('update', help='move this checkout to the newest signed release')
    u.add_argument('--tag', help='a specific release instead of the newest')
    u.add_argument('--install', action='store_true', help='only when nothing runs; then run ./install.sh --non-interactive')
    args = parser.parse_args(argv)
    try:
        if args.command == 'cut':
            cut(args)
        elif args.command == 'verify':
            tag, sha = verify(args.tag)
            print(f'{tag}: signed with the release key, commit {sha}')
        else:
            update(args)
    except Refused as error:
        raise SystemExit(f'Unsigned update refused: {error}')


if __name__ == '__main__':
    main()
