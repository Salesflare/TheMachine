"""The Machine's own changes an update set aside, back to the owner as to-dos.

When a Machine moves to a new release and its own commits (merged self-fixes) don't apply on it, the update keeps
each one under refs/machine/parked/ and moves on (scripts/release.py move_to, and the hosted Machine's agent the same
way), so a Machine never stays behind on an old version. This module lists what is parked, for the service to turn
each into a to-do once (Store.parked_fix_cards, through the first Gateway source as with the service's own errors).
Plain functions of the app folder; nothing here writes."""
import re
import subprocess

import i18n

PARKED = 'refs/machine/parked/'  # the same as scripts/release.py's
UNDO = re.compile(r'^Machine-Undo: ([0-9a-f]{40})$', re.M)  # a self-fix's undo names the fix it undid (next_actions)
STASH_SUBJECT = 'Uncommitted changes set aside by an update'


def pending(app, timeout=30):
    """[{sha, subject, changes}] of the parked commits, oldest first (as far as their times tell). A fix parked together with its own undo is
    left out (together they change nothing), and so is that undo. [] when git can't tell."""
    try:
        listed = subprocess.run(['git', '-C', str(app), 'for-each-ref', '--sort=committerdate',
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
    return [{k: item[k] for k in ('sha', 'subject', 'changes')} for item in found if item['sha'] not in cancel]


def card(item):
    """(title, body) of the to-do for one parked change."""
    short = item['sha'][:12]
    if item['changes']:
        return (i18n.t('Bring back changes the update set aside'),
                i18n.t('The update to the newest version set aside uncommitted changes in The Machine’s code, so it '
                       'could move on. They are kept as {}. Ask to redo them on the new version, or close this.', short))
    return (i18n.t('Redo a fix the update set aside'),
            i18n.t('A fix of The Machine’s own no longer fit the newest version, so the update set it aside and moved '
                   'on: “{}”. It is kept as {}. Ask to redo it on the new version, or close this.', item['subject'], short))
