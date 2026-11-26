"""The desktop app's version for a release of The Machine, written where each build reads it (desktop.yml, a release).

  python3 tools/version.py release-20261126-1430     # prints 2026.1126.1430 and writes it into the files below

A release tag (scripts/release.py) becomes year.monthday.hourminute: each later release is a higher version, as the
updater wants, and each part fits Windows' installer (at most 65535). The Arch package downloads that release's .deb.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
TAG = re.compile(r'release-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})')


def version(tag):
    found = TAG.fullmatch(tag)
    if not found:
        raise SystemExit(f'{tag} is not a release tag')
    year, month, day, hour, minute = found.groups()
    return f'{int(year)}.{int(month + day)}.{int(hour + minute)}'


def write(tag, root=HERE):
    v = version(tag)
    conf = root / 'tauri.conf.json'
    data = json.loads(conf.read_text())
    data['version'] = v
    conf.write_text(json.dumps(data, indent=2) + '\n')
    pkgbuild = root / 'linux' / 'PKGBUILD'
    text = pkgbuild.read_text()
    text, versions = re.subn(r'(?m)^pkgver=.*$', f'pkgver={v}', text)
    text, tags = re.subn(r'(?m)^_tag=.*$', f'_tag={tag}', text)
    if (versions, tags) != (1, 1):
        raise SystemExit('linux/PKGBUILD has no pkgver= or _tag= line')
    pkgbuild.write_text(text)
    plist = root / 'mac' / 'Info.plist'
    text, n = re.subn(r'(<key>CFBundle(?:ShortVersionString|Version)</key><string>)[^<]*(</string>)', rf'\g<1>{v}\g<2>', plist.read_text())
    if n != 2:
        raise SystemExit('mac/Info.plist has no CFBundleShortVersionString and CFBundleVersion')
    plist.write_text(text)
    return v


if __name__ == '__main__':
    print(write(sys.argv[1]))
