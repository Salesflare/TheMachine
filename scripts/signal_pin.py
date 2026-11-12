#!/usr/bin/env python3
"""Moves signal-pin.json to the newest signal-cli release (AsamK/signal-cli).

    python3 scripts/signal_pin.py check              print the pinned and the newest tag
    python3 scripts/signal_pin.py bump [--verify]    pin the newest release; --verify also downloads every archive and
                                                     checks it against its sha256

Each archive's sha256 is the one GitHub keeps for the release asset. Signal stops accepting old clients, so the monthly
signal-pin workflow runs `bump --verify` and opens a pull request when the pin moved. THIRD_PARTY_NOTICES.md names the
version too and moves with it."""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import signal_release  # noqa: E402

TAG = re.compile(r'v([0-9]+\.[0-9]+\.[0-9]+)')
NOTICES = ROOT / 'THIRD_PARTY_NOTICES.md'
NOTICE_LINE = re.compile(r'(\[signal-cli\]\(https://github\.com/AsamK/signal-cli\)) [0-9]+\.[0-9]+\.[0-9]+')


def get(url, accept='application/octet-stream'):
    headers = {'Accept': accept, 'User-Agent': 'the-machine-signal-pin'}
    if os.environ.get('GH_TOKEN') and url.startswith('https://api.github.com/'):
        headers['Authorization'] = f"Bearer {os.environ['GH_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=600) as response:
        return response.read()


def newest(repository, fetch=get):
    """(tag, {asset name: sha256}) of the latest release."""
    release = json.loads(fetch(f'https://api.github.com/repos/{repository}/releases/latest', 'application/vnd.github+json'))
    tag = release['tag_name']
    if not TAG.fullmatch(tag):
        raise SystemExit(f'unexpected release tag {tag!r}')
    sums = {}
    for asset in release.get('assets') or []:
        digest = str(asset.get('digest') or '')
        if re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
            sums[asset['name']] = digest.removeprefix('sha256:')
    return tag, sums


def updated_pin(data, tag, sums):
    """The pin for tag: each build's archive and binary renamed for its version, its sha256 from the release."""
    old, new_version = signal_release.version(data), TAG.fullmatch(tag)[1]
    new = {**data, 'tag': tag, 'builds': {}}
    for key, build in data['builds'].items():
        archive = build['archive'].replace(old, new_version)
        if archive not in sums:
            raise SystemExit(f'{tag} has no {archive} with a sha256')
        new['builds'][key] = {**build, 'archive': archive, 'binary': build['binary'].replace(old, new_version), 'sha256': sums[archive]}
    return new


def verify(data, fetch=signal_release._fetch):
    """Downloads every pinned archive and checks its sha256."""
    for key, build in data['builds'].items():
        if hashlib.sha256(fetch(signal_release.download_url(data, key))).hexdigest() != build['sha256']:
            raise SystemExit(f"{build['archive']} does not match its sha256")
        print(f"verified {build['archive']}")


def notices(text, data):
    return NOTICE_LINE.sub(lambda m: f'{m[1]} {signal_release.version(data)}', text, count=1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=['check', 'bump'])
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args(argv)
    data = signal_release.pin()
    tag, sums = newest(data['repository'])
    print(f"pinned {data['tag']}, newest {tag}")
    if args.command == 'check' or tag == data['tag']:
        return 0
    new = updated_pin(data, tag, sums)
    if args.verify:
        verify(new)
    signal_release.PIN_FILE.write_text(json.dumps(new, indent=2) + '\n')
    NOTICES.write_text(notices(NOTICES.read_text(), new))
    print(f'pinned {tag}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
