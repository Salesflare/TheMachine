"""Organization logos from their own website in the Team Graph (docs/shared-graph.md, "Logos from an organization's own
site").

A logo a Machine took from an organization's own website (enrichment.site_logos_step) is a file on that Machine, not an
address. It goes with the organization's record, which follows the sharing rules as before, as a thumbnail of pixels
only (logo_image.py): its hash in the record (logo_h), the picture itself (logo_img) only in the blob that first brings
it to the recipients, or after it changed. The record's own hash leaves the picture out, so a picture never makes a delta
by itself; the record never says the site's address or domain (only the hashed domain, as before). All pictures go
again when the recipients or the key change, and weekly, so a teammate who caught up from a later snapshot gets them.
At most LOGO_BLOB_BYTES of pictures go in one blob; the rest wait for the next rounds.

A receiving Machine checks a picture and draws it again (logo_image.received) before it keeps it in the teammate's
record (team_records, sealed at rest and removed with it), and serves it from its own address (api/person-photo).
Its own logo for an organization it knows comes first, then a teammate's LinkedIn logo, then this picture."""
import hashlib
import json
import re
import sqlite3
import time

import graph
import logo_image
from machine import stamps
import network_crypto as nc
import shared_graph_kept

LOGOS_EVERY = 7 * 86400
LOGO_BLOB_BYTES = 200_000
HEX = re.compile(r'[a-f0-9]{32}')
_THUMBS = {}  # (photo key, saved_at) -> thumbnail PNG or None: made once per saved logo, not each round
_OUT = {}  # logo_h -> thumbnail PNG, for the blobs of this round


# -- sending
def site_logo_thumb(db, logo):
    """(logo_h, PNG) of the thumbnail of a logo saved from an organization's own website, or None: only that kind of
    saved logo (never a picture the owner set, never an address)."""
    if not isinstance(logo, str) or not graph.PICTURE.fullmatch(logo):
        return None
    try:
        row = db.execute("SELECT data,type,saved_at FROM person_photos WHERE key=? AND identifier LIKE 'logo:%'", (logo[-32:],)).fetchone()
    except sqlite3.OperationalError:
        return None
    if not row:
        return None
    at = (logo[-32:], row['saved_at'])
    if at not in _THUMBS:
        if len(_THUMBS) > 5000:
            _THUMBS.clear()
        _THUMBS[at] = logo_image.thumbnail(bytes(row['data']), row['type'])
    png = _THUMBS[at]
    if not png:
        return None
    h = hashlib.sha256(png).hexdigest()[:32]
    _OUT[h] = png
    return h, png


def _attach(records, sent, budget):
    """records with the picture of each logo `sent` doesn't have yet, within budget (bytes): (records, {rid: logo_h}
    attached, bytes left)."""
    out, attached = [], {}
    for rec in records:
        h = rec.get('logo_h')
        png = _OUT.get(h) if h and sent.get(rec['r']) != h else None
        if png and len(png) <= budget:
            rec = {**rec, 'logo_img': nc.b64(png)}
            attached[rec['r']] = h
            budget -= len(png)
        out.append(rec)
    return out, attached, budget


def _kept(records, sent, attached):
    """What the recipients have of each record's logo picture after a blob: only for records that still carry it."""
    return {rid: h for rid, h in {**sent, **attached}.items() if (records.get(rid) or {}).get('logo_h') == h}


def snapshot_records(records, st, to, kv):
    """(the records of a snapshot, with the pictures that go in it; its logo state for st): all of them again when the
    recipients or the key changed, or weekly, else only those not sent yet."""
    reset = st.get('to') != to or st.get('kv') != kv or time.time() - st.get('logos_at', 0) > LOGOS_EVERY
    sent = {} if reset else dict(st.get('logos') or {})
    out, attached, _ = _attach(list(records.values()), sent, LOGO_BLOB_BYTES)
    return out, {'logos': _kept(records, sent, attached), 'logos_at': time.time() if reset else st.get('logos_at', 0)}


def delta_records(records, changed, st):
    """(the records of a delta: the changed ones, then unchanged ones whose picture waited for room; whether such a
    picture goes; its logo state for st)."""
    sent = dict(st.get('logos') or {})
    out, attached, left = _attach([records[r] for r in changed], sent, LOGO_BLOB_BYTES)
    waiting = [records[r] for r, rec in records.items() if r not in changed and rec.get('logo_h') in _OUT and sent.get(r) != rec['logo_h']]
    waiting, more, _ = _attach(waiting, sent, left)
    attached.update(more)
    return out + [r for r in waiting if r['r'] in more], bool(more), {'logos': _kept(records, sent, attached)}


# -- receiving
def clean(r, out):
    """A teammate's organization record's logo picture, checked and drawn again here, into its cleaned record."""
    if not HEX.fullmatch(str(r.get('logo_h'))):
        return
    out['logo_h'] = r['logo_h']
    text = r.get('logo_img')
    if not isinstance(text, str) or len(text) > logo_image.MAX_BYTES * 4 // 3 + 4:
        return
    try:
        png = logo_image.received(nc.unb64(text))
    except ValueError:
        return
    if png:
        out.update(logo_img=nc.b64(png), logo_key=hashlib.sha256(png).hexdigest()[:32])


def had(db, fleet, member):
    """{logo_h: (picture, key)} of a teammate's organization logo pictures this Machine keeps."""
    out = {}
    for row in db.execute("SELECT body FROM team_records WHERE fleet=? AND member=? AND kind='org'", (fleet, member)):
        body = json.loads(row['body'])
        if body.get('logo_h') and body.get('logo_img'):
            out[body['logo_h']] = (body['logo_img'], body.get('logo_key'))
    return out


def carry(record, kept):
    """A record that came again without its picture (it went before) keeps the one this Machine has of it."""
    if record.get('logo_h') and 'logo_img' not in record and record['logo_h'] in (kept or {}):
        record['logo_img'], record['logo_key'] = kept[record['logo_h']]
    return record


def pictures(db):
    """{'png': {key: PNG}, 'by_d': {domain hash: key}} of teammates' organization logo pictures, kept until
    team_records changes."""
    def build():
        out = {'png': {}, 'by_d': {}}
        try:
            rows = db.execute("SELECT body FROM team_records WHERE kind='org'").fetchall()
        except sqlite3.OperationalError:
            return out
        for row in rows:
            body = json.loads(row['body'])
            key, img = body.get('logo_key'), body.get('logo_img')
            if HEX.fullmatch(str(key)) and isinstance(img, str):
                out['png'][key] = nc.unb64(img)
                for h in body.get('d') or ():
                    out['by_d'].setdefault(h, key)
        return out
    return shared_graph_kept.KEPT.get(('team logos',), stamps.stamp(db, ('team_records',)), build)


def url(key):
    return 'api/person-photo?p=' + key


def photo(db, key):
    """(PNG, type) of a teammate's organization logo picture by its key, for the dashboard (api/person-photo), or None."""
    png = pictures(db)['png'].get(key) if HEX.fullmatch(str(key or '')) else None
    return (png, 'image/png') if png else None
