"""Person photos in the Team Graph (shared_graph_photos.py, docs/shared-graph.md "Person photos"): a work photo of a
shared person goes to teammates as a small re-drawn thumbnail, once, the way organization logos go; a photo from a chat
app, the Facebook import, one the owner set or took off, or one whose source can't be told never goes. The made-up
Fleet, its fake Network and the helpers are tests/test_shared_graph.py's."""
import hashlib
import json
import unittest
from unittest.mock import patch

import logo_image
import network_crypto as nc
import shared_graph as sg
import shared_graph_logos as sgl
import shared_graph_photos as photos
import test_shared_graph as base  # by module: its test classes run in its own file, not again here
from test_jpeg_image import jpeg, portrait
from test_logo_image import chunk, png
from test_shared_graph import FLEET, a, ago, graph, mail

LEE = 'email:lee@client.example'
KEYED = lambda text: hashlib.sha256(text.encode()).hexdigest()[:32]


def save_photo(db, identifier, data, at, kind='image/jpeg'):
    db.execute('INSERT INTO person_photos(identifier,key,type,data,saved_at) VALUES(?,?,?,?,?) ON CONFLICT(identifier) DO UPDATE SET '
               'type=excluded.type,data=excluded.data,saved_at=excluded.saved_at', (identifier, a.enrichment.photo_key(identifier), kind, data, at))


def looked_up(db, identifier, data, at, kind='image/jpeg'):
    """A photo the work contact look-up saved (enrichment.photos_step): its try and the photo at the same time."""
    db.execute("INSERT OR REPLACE INTO person_profiles(identifier,status,profile,fetched_at) VALUES(?,'found','{}',?)", (identifier, at))
    db.execute('INSERT OR REPLACE INTO person_photo_tries(identifier,tried_at) VALUES(?,?)', (identifier, at))
    save_photo(db, identifier, data, at, kind)


def contact_photo(db, identifier, data, at, source, tried=None):
    """A contact photo (enrichment.contact_photos_step) offered by a source and saved when it was tried."""
    a.enrichment.contact_tables(db)
    db.execute('INSERT OR REPLACE INTO contact_photo_links(identifier,url,chosen,source,seen_at,tried_at) VALUES(?,?,1,?,?,?)',
               (identifier, 'https://lh3.googleusercontent.com/a/x=s160-c', source, at, tried or at))
    save_photo(db, identifier, data, at)


class SharedGraphPhotos(base.SharedGraph):
    def setUp(self):
        super().setUp()
        photos._THUMBS.clear(); photos._SPENT[:] = [0.0, 0.0]
        budget = patch.object(photos, 'READ_SECONDS', 10 ** 6); budget.start(); self.addCleanup(budget.stop)  # a busy test host never runs out

    def lee(self, box):
        with box.store.connect() as db:
            row = db.execute("SELECT id,info FROM graph_nodes WHERE kind='person' AND id IN (SELECT n.id FROM graph_nodes n, "
                             "json_each(n.info,'$.identifiers') j WHERE j.value=?)", (LEE,)).fetchone()
            return row['id'], json.loads(row['info'])

    def spy(self, box, bodies):
        put = box._put
        return patch.object(box, '_put', side_effect=lambda group, me, kind, body, to, **kw: (bodies.append((kind, json.dumps(body))), put(group, me, kind, body, to, **kw))[1])

    def test_a_work_photo_goes_as_a_small_picture_once_shows_for_teammates_and_leaves_with_their_records(self):
        self.olive_mail()
        source = jpeg(portrait(160, 160), progressive=True)
        with self.own.store.connect() as db:
            looked_up(db, LEE, source, ago(1))
            looked_up(db, 'email:sam@friends.example', jpeg(portrait(48, 48)), ago(1))  # personal: their record never goes, nor their photo
        self.add(self.own)
        bodies = []
        with self.spy(self.own, bodies):
            self.rounds(3)
            pictures = [b for k, b in bodies if '"photo_img"' in b]
            self.assertEqual(len(pictures), 1, 'once, not each round')
            records = [r for k, b in bodies if k in ('snapshot', 'delta') for r in json.loads(b)['records']]
            lee = next(r for r in records if r.get('photo_img'))
            self.assertEqual((lee['t'], lee['name']), ('person', 'Lee Park'))
            self.assertLessEqual(len(lee['photo_img']), logo_image.MAX_BYTES * 4 // 3 + 4)
            self.assertNotIn('Sam Friend', [r['name'] for r in records])
            thumb = nc.unb64(lee['photo_img'])
            self.assertEqual(logo_image.decode_png(thumb, max_side=64, strict=True)[:2], (64, 64))  # pixels only, nothing of the file
            self.assertNotIn(source[:20], thumb)
            # the daily snapshot: the record again, its picture not
            state = self.own.meta('graph_out:' + FLEET)
            self.own.set_meta('graph_out:' + FLEET, {**state, 'snapshot_at': 0})
            went = len(bodies)
            self.rounds()
            self.assertIn('snapshot', [k for k, _ in bodies[went:]])
            self.assertEqual(len([b for k, b in bodies if '"photo_img"' in b]), 1)
            # weekly, or for new recipients: all pictures again
            state = self.own.meta('graph_out:' + FLEET)
            self.own.set_meta('graph_out:' + FLEET, {**state, 'snapshot_at': 0, 'logos_at': 0})
            self.rounds()
            self.assertEqual(len([b for k, b in bodies if '"photo_img"' in b]), 2)
        # a teammate's Team view and the person's page show it from the Machine's own address
        with self.mem.store.connect() as db:
            person = next(p for p in self.mem.team_overview(db, {})['people'] if p['name'] == 'Lee Park')
            self.assertTrue(person['team_only'])
            shown = person['profile']['photo']
            self.assertRegex(shown, r'^api/person-photo\?p=[0-9a-f]{32}$')
            self.assertEqual(self.mem.team_detail(db, person['id'])['profile']['photo'], shown)
            served, kind = sgl.photo(db, shown[-32:])
        self.assertEqual(kind, 'image/png')
        self.assertEqual(logo_image.decode_png(served, max_side=64, strict=True)[:2], (64, 64))
        # a new photo: it goes again, once
        bodies.clear()
        with self.own.store.connect() as db:
            looked_up(db, LEE, jpeg(portrait(96, 96)), ago(0))
        self.add(self.own)
        with self.spy(self.own, bodies):
            self.rounds(3)
        self.assertEqual(len([b for k, b in bodies if '"photo_img"' in b]), 1)
        with self.mem.store.connect() as db:
            person = next(p for p in self.mem.team_overview(db, {})['people'] if p['name'] == 'Lee Park')
            self.assertNotEqual(person['profile']['photo'], shown)
            shown = person['profile']['photo']
        # Mo knows Lee too: without a photo of their own, the teammate's shows; taken off by Mo, none; Mo's own first
        self.add(self.mem, mail('work', 9, 'Lee Park <lee@client.example>', 'mem3@acme.example', 'Hello', 'Hi Mo', 1, 't-mo'))
        mine = lambda: next(p for p in self.mem.team_overview(db, {})['people'] if p['name'] == 'Lee Park')
        with self.mem.store.connect() as db:
            self.assertFalse(mine().get('team_only'))
            self.assertEqual(mine()['profile']['photo'], shown)
            node = self.lee(self.mem)[0]
            graph.set_picture(db, node, None, a.now())  # Mo took the picture off
            self.assertIsNone((mine().get('profile') or {}).get('photo'))
            graph.set_picture(db, node, png(16, 16), a.now())  # Mo's own picture
        self.add(self.mem)
        with self.mem.store.connect() as db:
            self.assertNotEqual(mine()['profile']['photo'], shown)
        # Mo taken out of the team: the teammate's records go, and their pictures with them
        self.adm.graph_remove(FLEET, 'mem3')
        self.rounds(1)
        with self.mem.store.connect() as db:
            self.assertIsNone(sgl.photo(db, shown[-32:]))

    def test_nothing_from_google_contacts_goes(self):
        # Google's Limited Use rules: a contact's photo, job title, phone or birthday read from Google stays with the owner
        self.olive_mail()
        with self.own.store.connect() as db:
            contact_photo(db, LEE, jpeg(portrait(32, 32)), ago(1), 'google')
            a.enrichment.offer_facts(db, [([LEE], {'title': 'Chief Example Officer', 'company': 'Example Co', 'phone': '+15550100',
                                                   'birthday': '1990-04-02'}, a.enrichment.RECORD)], 'google', ago(1))
        self.add(self.own)
        bodies = []
        with self.spy(self.own, bodies):
            self.rounds(2)
        sent = ' '.join(b for k, b in bodies)
        self.assertIn('Lee Park', sent)  # the record went
        for word in ('photo_h', 'photo_img', 'Chief Example Officer', 'Example Co', '+15550100', '1990-04-02', '04-02'):
            self.assertNotIn(word, sent)

    def test_only_a_photo_from_a_work_source_goes(self):
        self.olive_mail()
        node, info = self.lee(self.own)
        picture = jpeg(portrait(32, 32))
        with_ids = {**info, 'identifiers': [*info.get('identifiers', []), 'wa:3255501', 'tg:77', 'slack:U1']}
        cases = {
            'the look-up': (lambda db: looked_up(db, LEE, picture, ago(1)), True),
            'Google contacts (Limited Use: it stays with the owner)': (lambda db: contact_photo(db, LEE, picture, ago(1), 'google'), False),
            'Slack': (lambda db: contact_photo(db, 'slack:U1', picture, ago(1), 'slack'), True),
            'LinkedIn': (lambda db: contact_photo(db, LEE, picture, ago(1), 'linkedin'), True),
            'Microsoft': (lambda db: contact_photo(db, LEE, picture, ago(1), 'microsoft'), True),
            'Salesflare, a PNG': (lambda db: (contact_photo(db, LEE, png(40, 40), ago(1, 1), 'salesflare'),
                                              db.execute("UPDATE person_photos SET type='image/png'")), True),
            'WhatsApp': (lambda db: save_photo(db, 'wa:3255501', picture, ago(1)), False),
            'Telegram': (lambda db: save_photo(db, 'tg:77', picture, ago(1)), False),
            'a Google contact by phone': (lambda db: contact_photo(db, 'wa:3255501', picture, ago(1), 'google'), False),
            'the Facebook import': (lambda db: a.enrichment.keep_photo(db, node, (picture, 'image/jpeg'), ago(1)), False),
            'the Facebook import after a look-up found none': (lambda db: (db.execute('INSERT INTO person_photo_tries(identifier,tried_at) VALUES(?,?)', (node, ago(3))),
                                                                          a.enrichment.keep_photo(db, node, (picture, 'image/jpeg'), ago(1))), False),
            'an unknown source': (lambda db: contact_photo(db, LEE, picture, ago(1), 'somewhere'), False),
            'no record of where it came from': (lambda db: save_photo(db, LEE, picture, ago(1)), False),
            'offered again since (another source)': (lambda db: contact_photo(db, LEE, picture, ago(2), 'linkedin', tried=ago(1)), False),
            'WebP': (lambda db: looked_up(db, LEE, b'RIFF\x00\x00\x00\x00WEBPVP8 ', ago(1), 'image/webp'), False),
            'the owner took it off': (lambda db: (looked_up(db, LEE, picture, ago(1)), graph.set_picture(db, node, None, a.now())), False),
            'the owner set a picture': (lambda db: (looked_up(db, LEE, picture, ago(1)), graph.set_picture(db, node, png(16, 16), a.now())), False),
        }
        for why, (save, goes) in cases.items():
            with self.subTest(why), self.own.store.connect() as db:
                for table in ('person_photos', 'person_photo_tries', 'person_profiles', 'contact_photo_links', 'person_edits'):
                    db.execute(f'DELETE FROM {table}')
                save(db)
                found = photos.person_photo(db, node, with_ids, KEYED)
                self.assertEqual(bool(found.get('photo_h')), goes, why)
                if goes:
                    self.assertIn(found['photo_h'], sgl._OUT)
                    self.assertEqual(logo_image.decode_png(sgl._OUT[found['photo_h']], max_side=64, strict=True)[:2], (40, 40) if 'PNG' in why else (32, 32))

    def test_a_photo_waits_when_reading_time_is_spent_without_changing_its_record(self):
        self.olive_mail()
        node, info = self.lee(self.own)
        with self.own.store.connect() as db:
            looked_up(db, LEE, jpeg(portrait(24, 24)), ago(1))
            photos._THUMBS.clear()
            with patch.object(photos, 'READ_SECONDS', 0):
                waiting = photos.person_photo(db, node, info, KEYED)
            self.assertNotIn(waiting['photo_h'], sgl._OUT)
            self.assertEqual(photos.person_photo(db, node, info, KEYED), waiting)  # the same record: no delta for a waiting picture
            self.assertIn(waiting['photo_h'], sgl._OUT)


for _name in dir(base.SharedGraph):
    if _name.startswith('test_'):
        setattr(SharedGraphPhotos, _name, None)  # test_shared_graph.py runs them


class Pictures(unittest.TestCase):
    def test_a_teammates_photo_is_checked_and_drawn_again(self):
        good = logo_image.thumbnail(png(64, 64), 'image/png')
        record = lambda img, **kw: sg._clean_record({'r': 'a' * 32, 't': 'person', 'name': 'Lee Park', 'ids': ['b' * 32], 'd': [],
                                                     'photo_h': 'c' * 32, 'photo_img': img, **kw})
        cleaned = record(nc.b64(good))
        self.assertEqual(logo_image.decode_png(nc.unb64(cleaned['photo_img']), strict=True), logo_image.decode_png(good, strict=True))
        self.assertRegex(cleaned['photo_key'], '^[0-9a-f]{32}$')
        self.assertEqual(cleaned['ids'], ['b' * 32])
        for why, img in {'oversized': nc.b64(good + b'\x00' * 9000), 'a JPEG as it was saved': nc.b64(jpeg(portrait(16, 16))),
                         'too big': nc.b64(png(200, 200)), 'text chunk': nc.b64(png(8, 8, extra=chunk(b'tEXt', b'a\x00b'))),
                         'not base64': '<img src=x onerror=alert(1)>', 'not text': 5}.items():
            cleaned = record(img)
            self.assertNotIn('photo_img', cleaned, why)
            self.assertNotIn('photo_key', cleaned, why)
        self.assertNotIn('photo_h', record(nc.b64(good), photo_h='x"><script>'))
        self.assertNotIn('logo', record(nc.b64(good), logo='https://media.licdn.com/dms/image/x'))  # a person carries no logo

    def test_a_saved_jpeg_becomes_a_small_png_and_webp_does_not_go(self):
        for data in (jpeg(portrait(160, 160)), jpeg(portrait(200, 150), progressive=True)):
            thumb = photos.thumbnail(data, 'image/jpeg')
            w, h, _ = logo_image.decode_png(thumb, max_side=64, strict=True)
            self.assertEqual(max(w, h), 64)
            self.assertLessEqual(len(thumb), logo_image.MAX_BYTES)
        self.assertIsNone(photos.thumbnail(b'RIFF\x00\x00\x00\x00WEBPVP8 ', 'image/webp'))
        self.assertIsNone(photos.thumbnail(b'\xff\xd8\xff\xe0broken', 'image/jpeg'))

    def test_pictures_in_one_blob_stay_within_its_byte_cap_and_the_rest_follow(self):
        records = {}
        for i in range(60):
            rid, h = '%032x' % i, '%032x' % (1000 + i)
            sgl._OUT[h] = bytes(8000)
            records[rid] = {'r': rid, 't': 'person', 'name': 'P', 'photo_h': h}
        out, state = sgl.snapshot_records(records, {}, ['m'], 'k')
        first = sum(len(nc.unb64(r['photo_img'])) for r in out if 'photo_img' in r)
        self.assertLessEqual(first, sgl.LOGO_BLOB_BYTES)
        self.assertGreater(first, 0)
        sent = len(state['logos'])
        out, more, state2 = sgl.delta_records(records, [], {**state, 'to': ['m'], 'kv': 'k'})
        self.assertTrue(more)
        self.assertLessEqual(sum(len(nc.unb64(r['photo_img'])) for r in out), sgl.LOGO_BLOB_BYTES)
        self.assertGreater(len(state2['logos']), sent)
        self.assertTrue(all('photo_img' in r for r in out))


if __name__ == '__main__':
    unittest.main()
