"""A changed bridge (openclaw-plugin/) that an update could not put into OpenClaw yet, and the owner's one to-do about it.

The nightly update (scripts/release.py update --install) never swaps the bridge inside a running Gateway: that swap
waits for the plugin's work to settle and fails when it does not within a minute, and a failed swap can leave the
Gateway unable to run models. It installs the bridge with the Gateway stopped and starts it again, at night with
nothing running (installer.py staged_swap). Until that worked, NAME stays in the data folder: the fingerprint of the
bridge that waits on its first line, and on its second how many quiet nights tried and failed (attempts), since when,
and why the last one failed. A night outside the quiet hours or with work running only waits, so it counts nothing.
After TRIES failed nights the service makes one to-do (Store.bridge_wait_card), worded for an owner who never opens a
terminal: the to-do's chat can finish it. The file goes when the bridge is in (installer.write_stamp), and the to-do
closes itself then. Plain functions of the data folder; only note writes."""
import hashlib
import json
from pathlib import Path

import i18n

LAYER = 0  # a changed bridge the nightly update could not put in yet (a leaf, shared with installer.py)

ROOT = Path(__file__).resolve().parents[1] / 'openclaw-plugin'
NAME, STAMP = 'plugin-waiting', 'plugin-installed'  # in the data folder: the one that waits, next to the stamp of the one that is in
TRIES = 3  # failed quiet nights before the owner hears about it


def read(path):
    """{fingerprint, attempts, since, last, reason} of the bridge that waits, or None when none does. A file from
    before the attempts were kept (one line) counts as none tried yet."""
    try:
        lines = Path(path).read_text().splitlines()
    except (OSError, ValueError):
        return None
    try:
        state = json.loads(lines[1]) if len(lines) > 1 else {}
    except ValueError:
        state = {}
    if not isinstance(state, dict):
        state = {}
    try:
        attempts = max(0, int(state.get('attempts') or 0))
    except (TypeError, ValueError):
        attempts = 0
    return {'fingerprint': lines[0].strip() if lines else '', 'attempts': attempts, 'since': str(state.get('since') or ''),
            'last': str(state.get('last') or ''), 'reason': str(state.get('reason') or '')}


def note(path, fingerprint, failed=None, now=None):
    """The bridge with `fingerprint` waits; `failed`: a quiet night tried and could not put it in (why, for the log).
    Attempts carry over a newer bridge: the owner's question is whether the bridge goes in at all. Returns the state."""
    import timeutil  # here, not at the top: the installer imports this module before it checks the time zone
    path, stamp = Path(path), now or timeutil.stamp()
    state = read(path) or {'attempts': 0, 'since': '', 'last': '', 'reason': ''}
    state.update(fingerprint=fingerprint, since=state['since'] or stamp)
    if failed:
        state.update(attempts=state['attempts'] + 1, last=stamp, reason=str(failed)[:300])
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(fingerprint + '\n' + json.dumps({k: state[k] for k in ('attempts', 'since', 'last', 'reason')}, sort_keys=True) + '\n')
    except OSError:
        pass
    return state


def due(data):
    """The state in the data folder `data` once TRIES quiet nights failed, else None."""
    state = read(Path(data) / NAME)
    return state if state and state['attempts'] >= TRIES else None


def files(root=ROOT):
    """The bridge's own files, as a hash (installer.bridge_parts)."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob('*') if p.is_file() and 'node_modules' not in p.parts):
        digest.update(str(path.relative_to(root)).encode() + b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


def loaded(data, root=ROOT):
    """Whether the Gateway last took the very bridge that is in this folder (the stamp's parts), as far as the installer
    knows: False when it can't tell, or a changed one still waits."""
    try:
        parts = json.loads((Path(data) / STAMP).read_text().splitlines()[1])
        return not waiting(data) and parts['files'] == files(root)
    except (OSError, ValueError, LookupError, TypeError):
        return False


def waiting(data):
    """Whether a changed bridge still waits in the data folder `data`."""
    return (Path(data) / NAME).exists()


def card(state):
    """(title, body, signal) of the owner's to-do: plain words, no commands. The to-do's chat can do it."""
    return (i18n.t('Finish installing the last update'),
            i18n.t('The newest version is in, except one part that needs a short restart, which the nightly tries could '
                   'not do. Everything works as before meanwhile. Ask in this to-do’s chat and The Machine finishes it. It '
                   'also keeps trying each night.'),
            i18n.t('The nightly update could not finish one part.'))
