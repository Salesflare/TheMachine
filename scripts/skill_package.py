"""The skill that ships with the MCP connection (claude-plugin/skills/the-machine), packed for where it is published
(docs/ai-connections.md, The skill). desktop.yml's publish puts both on each desktop release, so the newest is always at
releases/latest/download/ (Settings, Apps links the first):

  the-machine-skill.zip    claude.ai and Claude Desktop (Customize, Skills): the folder, its SKILL.md inside
  the-machine-clawhub.zip  ClawHub: the folder's files at the top, as `clawhub publish` sends them

  python3 scripts/skill_package.py <out folder>

The same files give the same bytes (fixed dates and order), so a rebuild can be checked against a release."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / 'claude-plugin' / 'skills' / 'the-machine'
NAMES = {'claude': 'the-machine-skill.zip', 'clawhub': 'the-machine-clawhub.zip'}
WHEN = (2026, 1, 1, 0, 0, 0)


def files(folder=FOLDER):
    """The skill's files, relative to its folder, in a fixed order (no hidden ones)."""
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*')
                  if p.is_file() and not any(part.startswith('.') for part in p.relative_to(folder).parts))


def pack(out, folder=FOLDER):
    """Writes both zips into out; {kind: path}."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    made = {}
    for kind, name in NAMES.items():
        path = out / name
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as box:
            for rel in files(folder):
                info = zipfile.ZipInfo(f'{folder.name}/{rel}' if kind == 'claude' else rel, WHEN)
                info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
                box.writestr(info, (folder / rel).read_bytes())
        made[kind] = path
    return made


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    for kind, path in pack(sys.argv[1]).items():
        print(f'{kind}: {path}')
