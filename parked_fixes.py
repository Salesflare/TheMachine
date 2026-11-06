"""The Machine's own changes an update set aside, back to the owner as to-dos.

When a Machine moves to a new release and its own commits (merged self-fixes) don't apply on it, the update keeps
each one under refs/machine/parked/ and moves on (scripts/release.py move_to, and the hosted Machine's agent the same
way), so a Machine never stays behind on an old version. This module lists what is parked, for the service to turn
each into a to-do once (Store.parked_fix_cards, through the first Gateway source as with the service's own errors),
and the same for files the owner added that an update renamed rather than overwrite them (KEPT): one to-do per update.
Plain functions of the app folder; nothing here writes."""
import re
import subprocess
from pathlib import Path

import i18n

PARKED = 'refs/machine/parked/'  # the same as scripts/release.py's
UNDO = re.compile(r'^Machine-Undo: ([0-9a-f]{40})$', re.M)  # a self-fix's undo names the fix it undid (next_actions)
STASH_SUBJECT = 'Uncommitted changes set aside by an update'
# Files the owner added that an update renamed instead of overwriting them (scripts/release.py keep_local_files): one
# tab-separated line per file (when, release commit, path, new name), in the checkout's git folder.
KEPT = 'machine-kept-local'  # the same as scripts/release.py's


def pending(app, timeout=30):
    """[{sha, subject, changes}] of the parked commits, oldest first (as far as their times tell). One still on the
    checkout is left out (the update didn't move past it), and so is a fix parked together with its own undo (together
    they change nothing) and that undo. [] when git can't tell."""
    try:
        listed = subprocess.run(['git', '-C', str(app), 'for-each-ref', '--sort=committerdate', '--no-merged=HEAD',
                                 '--format=%(objectname)%00%(contents:subject)%00%(contents:body)%00%(parent)%01', PARKED],
                                capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if listed.returncode:
        return []
    found = []
    for record in listed.stdout.split('\x01'):  # one per ref: a body has lines of its own
        parts = record.strip('\n').split('\0')
        if len(parts) != 4 or not re.fullmatch(r'[0-9a-f]{40}', parts[0]):
            continue
        sha, subject, body, parents = parts
        found.append({'sha': sha, 'subject': ' '.join(subject.split())[:200], 'body': body,
                      'changes': subject.endswith(STASH_SUBJECT) and len(parents.split()) > 1})
    undone = {m for item in found for m in UNDO.findall(item['body'])}
    shas = {item['sha'] for item in found}
    cancel = {item['sha'] for item in found if set(UNDO.findall(item['body'])) & shas} | (undone & shas)
    return [{k: item[k] for k in ('sha', 'subject', 'changes')} for item in found if item['sha'] not in cancel] + kept_files(app, timeout)


def kept_files(app, timeout=30):
    """[{sha, subject, changes, kept: [(path, new name)]}], one per update that renamed files the owner added (its
    sha: 'kept-' and the release commit, so each update brings one to-do). [] when there are none or git can't tell."""
    try:
        where = subprocess.run(['git', '-C', str(app), 'rev-parse', '--git-path', KEPT], capture_output=True, text=True,
                               timeout=timeout)
        lines = (Path(app) / where.stdout.strip()).read_text(encoding='utf-8').splitlines() if not where.returncode else []
    except (OSError, UnicodeDecodeError, subprocess.TimeoutExpired):
        return []
    updates = {}
    for line in lines:
        parts = line.split('\t')
        if len(parts) == 4 and re.fullmatch(r'[0-9a-f]{40}', parts[1]) and parts[2] and parts[3]:
            updates.setdefault(parts[1], []).append((parts[2], parts[3]))
    return [{'sha': 'kept-' + sha, 'subject': 'Files kept by an update', 'changes': False, 'kept': kept}
            for sha, kept in updates.items()]


def card(item):
    """(title, body, signal) of the to-do for one parked change: what to do, and what was kept (its signal), once each."""
    if item.get('kept'):
        return (i18n.t('Your update kept {} of your own files', len(item['kept'])),
                i18n.t('The new version has files with the same names, so the update renamed yours:\n{}\nClose this once '
                       'you’ve checked them.', '\n'.join(f'{path} → {name}' for path, name in item['kept'])),
                i18n.t('An update kept your own files.'))
    short = item['sha'][:12]
    if item['changes']:
        return (i18n.t('Bring back changes the update set aside'),
                i18n.t('They no longer fit the newest version, so the update set them aside and moved on. Ask to redo them '
                       'on the new version, or close this.'),
                i18n.t('Uncommitted changes in The Machine’s code, kept as {}.', short))
    return (i18n.t('Redo a fix the update set aside'),
            i18n.t('It no longer fit the newest version, so the update set it aside and moved on. Ask to redo it on the '
                   'new version, or close this.'),
            i18n.t('A fix of The Machine’s own: “{}”, kept as {}.', item['subject'], short))
