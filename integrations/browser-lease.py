#!/usr/bin/env python3
"""One lease for all browser work: shared for the OpenClaw browser, exclusive for real Chrome.

Replaces the informal "parent/accounting release" hand-off (2026-10-11). Since
2026-10-13 the managed `openclaw` profile is shared: tested live, jobs
in separate tabs of that browser run side by side without slowing or disturbing
each other (timers, scrolling and lazy loading all keep working in background
tabs). So any number of jobs may hold the lease at once, each working only in
tabs it opened itself. Only work that needs the browser to itself takes it
exclusively: the real-Chrome fallbacks (`profile="chrome"` extension route,
`profile="user"`), desktop input, or anything that restarts the browser. An
exclusive claim waits until the shared holders are done, and new shared claims
wait behind a queued exclusive one so it is never starved.

  browser-lease.py claim   --owner NAME [--minutes N] [--exclusive] [--wait M]
                           exit 0 = yours, 3 = busy (after waiting up to M minutes)
  browser-lease.py renew   --owner NAME [--minutes N]   exit 0 = renewed, 3 = not yours
  browser-lease.py release --owner NAME                 exit 0 (also when not held)
  browser-lease.py status                               prints holders or "free"
  browser-lease.py focus                                only the window fix below

Owner names must be unique per run (e.g. x-collector, assistant-1a2b3c4d): a
claim under your own name is a renewal, never a wait. An expired holder is
dropped, so a crashed job can never block for longer than its lease.

A successful exclusive claim also makes sure Chrome's last-focused window is a
normal window: the extension opens new tabs there and groups them, and an app
window (e.g. the OpenClaw dashboard installed as an app) cannot hold tab groups,
so every new tab failed. When needed it focuses the newest normal Chrome window
for a moment and then restores whatever window was active.
"""
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import portable  # noqa: E402

STATE = Path(os.environ.get('OPENCLAW_WORKSPACE') or Path.home() / '.openclaw/workspace').expanduser() / 'data/browser-lease/lease.json'
LOCK = STATE.with_suffix('.lock')
MAX_MINUTES = 120


def now():
    import timeutil
    return timeutil.clock()


def stamp(minutes=0):
    return (now() + timedelta(minutes=minutes)).isoformat(timespec='seconds')


def live(entries):
    out = {}
    for owner, entry in (entries or {}).items():
        try:
            if datetime.fromisoformat(entry['expiresAt']) > now():
                out[owner] = entry
        except (ValueError, KeyError, TypeError):
            pass
    return out


def read():
    """{'holders': {owner: {since, expiresAt, exclusive}}, 'waiting': {owner: {expiresAt}}}"""
    try:
        state = json.loads(STATE.read_text())
    except (FileNotFoundError, ValueError):
        state = {}
    if not isinstance(state, dict):
        state = {}
    if 'owner' in state:  # single-holder format from before 2026-10-13
        state = {'holders': {state['owner']: dict(state, exclusive=True)}}
    return {'holders': live(state.get('holders')), 'waiting': live(state.get('waiting'))}


def save(state):
    state = {k: v for k, v in state.items() if v}
    if not state:
        STATE.unlink(missing_ok=True)
        return
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(state) + '\n')
    tmp.replace(STATE)


def describe(state):
    parts = [f"{o}{' (exclusive)' if e.get('exclusive') else ''} until {local(e['expiresAt'])}"
             for o, e in state['holders'].items()]
    parts += [f"{o} (waiting for exclusive)" for o in state['waiting']]
    return ', '.join(parts)


def try_claim(owner, minutes, exclusive, wait_until=None):
    """One attempt under the file lock. Returns (granted, state)."""
    with LOCK.open('a') as lock:
        portable.lock(lock)
        state = read()
        holders, waiting = state['holders'], state['waiting']
        mine = holders.get(owner)
        others = {o: e for o, e in holders.items() if o != owner}
        queued = {o for o in waiting if o != owner}
        if exclusive:
            ok = not others
        elif mine:
            ok = True  # your own lease: a renewal, never a wait
        else:
            ok = not any(e.get('exclusive') for e in others.values()) and not queued
        if ok:
            holders[owner] = {'since': mine['since'] if mine else stamp(), 'expiresAt': stamp(minutes),
                              'exclusive': bool(exclusive or (mine or {}).get('exclusive'))}
            waiting.pop(owner, None)
        elif exclusive and wait_until:
            waiting[owner] = {'expiresAt': wait_until}
        save(state)
        return ok, state


def claim(owner, minutes, exclusive=False, wait_minutes=0, sleep=time.sleep, poll=5):
    deadline = now() + timedelta(minutes=wait_minutes)
    # A queued exclusive claim reserves its place for one poll beyond the next try.
    reserve = lambda: (now() + timedelta(seconds=poll * 3)).isoformat(timespec='seconds')
    while True:
        ok, state = try_claim(owner, minutes, exclusive, reserve() if wait_minutes else None)
        if ok or now() >= deadline:
            break
        sleep(poll)
    if not ok and exclusive:
        with LOCK.open('a') as lock:
            portable.lock(lock)
            current = read()
            current['waiting'].pop(owner, None)
            save(current)
    return ok, state


def local(stamp):
    return datetime.fromisoformat(stamp).astimezone().strftime('%H:%M')


def hyprctl(*args):
    return subprocess.run(['hyprctl', *args], capture_output=True, text=True, timeout=10).stdout


def focus_window(address):
    hyprctl('dispatch', f'hl.dsp.focus({{ window = "address:{address}" }})')


def ensure_normal_chrome_window(run=hyprctl, focus=focus_window, pause=1.5):
    """Return a short note when focus was changed or impossible, else ''."""
    try:
        clients = json.loads(run('clients', '-j') or '[]')
        active = json.loads(run('activewindow', '-j') or '{}')
    except (OSError, ValueError, subprocess.SubprocessError):
        return ''  # no Hyprland session: nothing to fix
    chrome = sorted((c for c in clients if c.get('mapped', True)
                     and (c.get('class') == 'google-chrome' or c.get('class', '').startswith('chrome-'))),
                    key=lambda c: c.get('focusHistoryID', 1 << 30))
    if not chrome or chrome[0].get('class') == 'google-chrome':
        return ''
    normal = [c for c in chrome if c.get('class') == 'google-chrome']
    if not normal:
        return 'note: no normal Chrome window; new tabs may fail until one is opened'
    focus(normal[0]['address'])
    time.sleep(pause)
    previous = active.get('address')
    if previous and previous != normal[0]['address']:
        focus(previous)
    return 'focused a normal Chrome window for new tabs'


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('action', choices=['claim', 'renew', 'release', 'status', 'focus'])
    p.add_argument('--owner')
    p.add_argument('--minutes', type=int, default=20)
    p.add_argument('--exclusive', action='store_true', help='the browser to yourself (real Chrome, desktop input)')
    p.add_argument('--wait', type=float, default=0, metavar='M', help='wait up to M minutes while busy')
    a = p.parse_args()
    if a.action == 'focus':
        print(ensure_normal_chrome_window() or 'ok')
        return 0
    if a.action != 'status' and not (a.owner or '').strip():
        p.error('--owner is required')
    minutes = max(1, min(a.minutes, MAX_MINUTES))
    STATE.parent.mkdir(parents=True, exist_ok=True)
    if a.action == 'claim':
        ok, state = claim(a.owner, minutes, a.exclusive, max(0, min(a.wait, MAX_MINUTES)))
        if not ok:
            print('busy: held by ' + describe(state))
            return 3
        entry = state['holders'][a.owner]
        shared = [o for o in state['holders'] if o != a.owner]
        print(f"claimed{' exclusively' if entry['exclusive'] else ''} until {local(entry['expiresAt'])}"
              + (f" (shared with {', '.join(shared)})" if shared else ''))
        # Outside the file lock so the window fix never delays other callers.
        note = ensure_normal_chrome_window() if entry['exclusive'] else ''
        if note:
            print(note)
        return 0
    with LOCK.open('a') as lock:
        portable.lock(lock)
        state = read()
        if a.action == 'status':
            print(describe(state) or 'free')
            return 0
        mine = state['holders'].get(a.owner)
        if a.action == 'renew':
            if not mine:
                print('not yours: lease expired or released; claim again')
                return 3
            mine['expiresAt'] = stamp(minutes)
            save(state)
            print(f"renewed until {local(mine['expiresAt'])}")
            return 0
        if mine:
            del state['holders'][a.owner]
            save(state)
            print('released')
        else:
            print('not held by you; nothing to release')
        return 0


if __name__ == '__main__':
    sys.exit(main())
