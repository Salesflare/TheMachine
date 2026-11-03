#!/usr/bin/env python3
"""Signed releases of The Machine.

A release is a git tag `release-YYYYMMDD-HHMM` on a commit of main, signed with the release key (an SSH key). Hosted
Machines and `update` below only install a release whose signature checks out against the public key in the code
that is already installed (deploy/release-signers), so a pushed commit alone never reaches a Machine.

  python3 scripts/release.py cut       sign origin/main as a new release and push the tag (needs the private key)
  python3 scripts/release.py verify    check a release tag (default: the newest) against deploy/release-signers
  python3 scripts/release.py update    self-hosted: move this checkout to the newest signed release, then ./install.sh
                                        (--install: only when nothing runs, and runs ./install.sh itself; the daily
                                        update timer that install.sh sets up calls this)

The private key is read from $THE_MACHINE_RELEASE_KEY, else ~/.config/the-machine-release/signing-key."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from scripts.security_gate import require_release_scan
except ModuleNotFoundError:
    from security_gate import require_release_scan

ROOT = Path(__file__).resolve().parent.parent
SIGNERS = ROOT / 'deploy' / 'release-signers'
TAG = re.compile(r'release-\d{8}-\d{4}')
PRINCIPAL = 'release@themachine.computer'
BEGIN = b'-----BEGIN SSH SIGNATURE-----\n'
END = b'-----END SSH SIGNATURE-----\n'


class Refused(Exception):
    pass


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


def cut(args):
    key = Path(args.key or os.environ.get('THE_MACHINE_RELEASE_KEY') or Path.home() / '.config/the-machine-release/signing-key')
    if not key.exists():
        raise SystemExit(f'No release key at {key}. Only the release key holder can cut a release.')
    git('fetch', '--quiet', '--tags', 'origin', 'main')
    sha = git('rev-parse', 'origin/main^{commit}').stdout.strip()
    for name in reversed(releases()):
        if git('rev-parse', f'{name}^{{commit}}').stdout.strip() == sha:
            print(f'origin/main ({sha[:7]}) is already released as {name}.')
            return
    tag = 'release-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M')
    if git('rev-parse', '-q', '--verify', f'refs/tags/{tag}', check=False).returncode == 0:
        raise SystemExit(f'{tag} exists already: wait a minute and try again.')
    try:
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


def move_to(sha, ref='main'):
    """Onto a verified release the way hosted Machines move: a fast-forward; else, with no commits of its own (all are
    on the branch or in a release), straight there, uncommitted changes kept; else its own commits (a merged self-fix)
    replayed on top, and left as they were when that does not apply cleanly. The git run that decided it."""
    if git('merge-base', '--is-ancestor', 'HEAD', sha, check=False).returncode == 0:
        return git('merge', '--ff-only', '--quiet', sha, check=False)
    before = git('rev-parse', '-q', '--verify', f'origin/{ref}@{{1}}', check=False).stdout.strip()  # before a rewrite
    own = git('rev-list', 'HEAD', '--not', sha, f'refs/remotes/origin/{ref}', '--tags=release-*',
              *([before] if before else []), check=False).stdout.split()
    if not own:
        return git('reset', '--keep', '-q', sha, check=False)
    result = git('-c', 'user.name=m', '-c', 'user.email=m@localhost', 'rebase', '-q', '--onto', sha, own[-1] + '^',
                 check=False)
    if result.returncode:
        git('rebase', '--abort', check=False)
    return result


def busy():
    """Work that a restart would cut off, or no way to tell: only `assistant busy` exiting 0 means idle."""
    return subprocess.run([sys.executable, str(ROOT / 'cli.py'), 'busy'], cwd=ROOT, capture_output=True,
                          text=True).returncode != 0


def update(args):
    git('fetch', '--quiet', '--tags', 'origin')
    tag, sha = verify(args.tag)
    if git('merge-base', '--is-ancestor', sha, 'HEAD', check=False).returncode == 0:
        print(f'Already on {tag} or newer.')
        return
    if args.install and busy():
        print(f'{tag} is ready, but something is running: trying again next time.')
        return
    result = move_to(sha)
    if result.returncode:
        raise SystemExit(f'{tag} is verified, but this checkout\'s own commits do not apply on it: nothing changed. '
                         + (result.stderr or result.stdout).strip()[-300:])
    print(f'Updated to {tag} ({sha[:7]}), signature verified.' + ('' if args.install else ' Now run ./install.sh'))
    if args.install:
        code = subprocess.run([str(ROOT / 'install.sh'), '--non-interactive'], cwd=ROOT).returncode
        if code:
            raise SystemExit(f'./install.sh failed (exit {code}) after the update to {tag}.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('cut', help='sign origin/main as a new release and push it')
    c.add_argument('--key', help='private key file (default: $THE_MACHINE_RELEASE_KEY or ~/.config/the-machine-release/signing-key)')
    c.add_argument('--no-push', action='store_true', help='tag and verify locally only')
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
