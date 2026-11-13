"""Person photos in the Team Graph (docs/shared-graph.md, "Person photos").

A person's record goes to the team only under the Team Graph's own rules (Work, never Personal). With it may go a
thumbnail of their photo, the way an organization's logo goes (shared_graph_logos.py): pixels only, drawn again as a
new PNG of at most 64 by 64 pixels (logo_image.draw; JPEG read by jpeg_image.py), its hash in the record (photo_h),
the picture itself (photo_img) only in the blob that first brings it or after it changed, and all again weekly.

Only a photo from a work source goes: a work contact's look-up (person_profiles), or a contact photo from Slack,
LinkedIn, X, Salesflare or Microsoft (contact_photo_links.source). A photo is from there only when that row says it
was saved then (the same time as the saved photo); a photo from WhatsApp or Telegram (wa:, tg:), from the Facebook
birthdays import (kept under the person's own id), or one whose source can't be told never goes. Nor does a photo
from Google contacts, other contacts or the directory: Google's user data policy (Limited Use) doesn't allow handing
what its APIs give to other people, so it stays on the owner's own Machine. Nor does
any photo of a person the owner set a picture for or took the picture off (person_edits photo): the owner's own
choice of picture stays theirs.

The hash is keyed with the graph secret and names the saved photo (its key and when it was saved), so it is known
without reading the picture: a record never changes because a picture waits. Reading pictures has a time budget
(READ_SECONDS per WINDOW); one that waits goes in a later round.

A receiving Machine checks the picture and draws it again (shared_graph_logos.clean) and serves it from its own address
(api/person-photo). A person's own photo on this Machine comes first, and a person whose picture the owner took off
shows none; a teammate's photo fills in only otherwise. It goes with the teammate's records."""
import json
import sqlite3
import struct
import time

import jpeg_image
import logo_image
import shared_graph_logos as logos

# contact_photo_links.source of a work source (Microsoft's contact photos come as 'microsoft' or 'outlook'); never
# 'google': Google's Limited Use rules keep what its APIs give with the owner
WORK_SOURCES = frozenset({'slack', 'linkedin', 'x', 'salesflare', 'microsoft', 'outlook'})
NEVER = ('wa:', 'tg:', 'pic:', 'logo:')  # chat apps, the owner's own pictures, organization logos
# Drawing a picture is pure Python, on the Fleet's thread: after a restart, when none is drawn yet, a round's share
# holds the dashboard's requests up while it draws. A few seconds a round; the rest in the next ones.
READ_SECONDS = 4
WINDOW = 300
_THUMBS = {}  # (photo key, saved_at) -> thumbnail PNG, or None when it can't be read
_SPENT = [0.0, 0.0]  # this window's start, seconds spent reading pictures in it
WAIT = object()


def source(db, identifier, saved_at):
    """Where a saved photo came from when that is a work source: 'lookup', or its contact photo's source; else None
    (a chat app, the Facebook import, a picture the owner set, or not known)."""
    if str(identifier).startswith(NEVER):
        return None
    try:
        tried = db.execute('SELECT tried_at FROM person_photo_tries WHERE identifier=?', (identifier,)).fetchone()
        if tried and tried[0] == saved_at and db.execute('SELECT 1 FROM person_profiles WHERE identifier=?', (identifier,)).fetchone():
            return 'lookup'
        link = db.execute('SELECT source,tried_at FROM contact_photo_links WHERE identifier=?', (identifier,)).fetchone()
    except sqlite3.OperationalError:
        return None
    return link[0] if link and link[1] == saved_at and link[0] in WORK_SOURCES else None


def thumbnail(data, kind):
    """A new PNG of a saved photo (JPEG or PNG), at most logo_image.SIDE pixels, or None. WebP isn't read."""
    try:
        if kind == 'image/jpeg':
            w, h, rgba = jpeg_image.decode(data, logo_image.SIDE)
        elif kind == 'image/png':
            w, h, rgba = logo_image.decode_png(data)
        else:
            return None
    except (jpeg_image.Bad, logo_image.Bad, IndexError, struct.error):
        return None
    return logo_image.draw(w, h, rgba)


def _thumb(db, key, saved_at, kind):
    """The thumbnail of a saved photo, made once; WAIT when this window's reading time is spent."""
    at = (key, saved_at)
    if at in _THUMBS:
        return _THUMBS[at]
    start = time.monotonic()
    if start - _SPENT[0] > WINDOW:
        _SPENT[:] = [start, 0.0]
    if _SPENT[1] >= READ_SECONDS:
        return WAIT
    row = db.execute('SELECT data FROM person_photos WHERE key=? AND saved_at=?', (key, saved_at)).fetchone()
    png = thumbnail(bytes(row[0]), kind) if row else None
    _SPENT[1] += time.monotonic() - start
    if len(_THUMBS) > 5000:
        _THUMBS.clear()
    _THUMBS[at] = png
    return png


def person_photo(db, node_id, info, keyed):
    """What a shared person's record says of their photo: {'photo_h': hash} of a work source's photo (the one their
    page shows first), else {}. keyed(text) is the graph's keyed hash."""
    group = sorted(set(info.get('identifiers') or ()) | {node_id})
    every = json.dumps(group)
    try:
        if db.execute("SELECT 1 FROM person_edits WHERE identifier IN (SELECT value FROM json_each(?)) "
                      "AND json_extract(fields,'$.photo') IS NOT NULL", (every,)).fetchone():
            return {}  # the owner set a picture or took it off
        rows = db.execute("SELECT identifier,key,type,saved_at FROM person_photos WHERE identifier IN (SELECT value FROM json_each(?)) "
                          "AND type IN ('image/jpeg','image/png')", (every,)).fetchall()
    except sqlite3.OperationalError:
        return {}
    shown = str((info.get('profile') or {}).get('photo') or '')[-32:]
    for identifier, key, kind, saved_at in sorted(rows, key=lambda r: (r[1] != shown, r[0])):
        if not source(db, identifier, saved_at):
            continue
        png = _thumb(db, key, saved_at, kind)
        if png is None:
            continue
        h = keyed('photo|' + key + '|' + saved_at)
        if png is not WAIT:
            logos._OUT[h] = png
        return {'photo_h': h}
    return {}


# -- receiving
def closest(sources, pics):
    """A person's photo from teammates' records: the closest teammate's that this Machine keeps, or None."""
    ranked = sorted(sources, key=lambda s: -(s['record'].get('score') or 0))
    return next((logos.url(s['record']['photo_key']) for s in ranked if s['record'].get('photo_key') in pics['png']), None)


def took_off(db, node_id):
    """Whether the owner took this person's picture off (person_edits photo 'none' on any of their identities)."""
    row = db.execute("SELECT info FROM graph_nodes WHERE id=? AND kind='person'", (node_id,)).fetchone()
    group = sorted(set(json.loads(row['info'] or '{}').get('identifiers') or ()) | {node_id}) if row else [node_id]
    try:
        return bool(db.execute("SELECT 1 FROM person_edits WHERE identifier IN (SELECT value FROM json_each(?)) "
                               "AND json_extract(fields,'$.photo')='none'", (json.dumps(group),)).fetchone())
    except sqlite3.OperationalError:
        return False


def fill(db, item, view, entry, pics):
    """A Team view row's picture: its own logo or photo here first, else the closest teammate's (none for a person
    whose picture the owner took off)."""
    name = {'org': 'logo', 'person': 'photo'}.get(entry['kind'])
    if not name or (view.get('profile') or {}).get(name) or (name == 'photo' and view and took_off(db, view['id'])):
        return
    found = logos.closest(entry['sources'], pics) if name == 'logo' else closest(entry['sources'], pics)
    if found:
        item['profile'] = {**(item.get('profile') or {}), name: found}


def profile(db, entry):
    """A team-only person's page: {'profile': {'photo': address}} of the closest teammate's photo, else {}."""
    found = closest(entry['sources'], logos.pictures(db)) if entry['kind'] == 'person' else None
    return {'profile': {'photo': found}} if found else {}
