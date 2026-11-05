"""The text of a file added to a new to-do (file_text.py): a PDF's text in page order (plain and compressed content,
fonts with a ToUnicode map, objects packed in object streams), plain text files, and nothing (no error) for a scanned
page, an encrypted or broken file. Bounded for files from anywhere. All files here are made up."""
import importlib.util
import random
import time
import unittest
import zlib
from pathlib import Path

spec = importlib.util.spec_from_file_location('file_text_under_test', Path(__file__).parent.parent / 'file_text.py')
file_text = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_text)


def stream(body, dictionary=b'', compress=False):
    data = zlib.compress(body) if compress else body
    return b'<<' + dictionary + (b'/Filter/FlateDecode' if compress else b'') + b'/Length %d>>stream\n' % len(data) + data + b'\nendstream'


def pdf(objects, root=1, trailer=b''):
    """A PDF of numbered objects (1, 2, ...), with a trailer naming the catalog. No xref: readers (and this one) cope."""
    out = b'%PDF-1.7\n'
    for n, body in enumerate(objects, 1):
        out += b'%d 0 obj\n' % n + body + b'\nendobj\n'
    return out + b'trailer\n<</Root %d 0 R' % root + trailer + b'>>\n%%EOF\n'


def two_pages(compress=False):
    return pdf([
        b'<</Type/Catalog/Pages 2 0 R>>',
        b'<</Type/Pages/Kids[3 0 R 4 0 R]/Count 2>>',
        b'<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 7 0 R>>>>/Contents 5 0 R>>',
        b'<</Type/Page/Parent 2 0 R/Resources<</Font<</F1 7 0 R>>>>/Contents 6 0 R>>',
        stream(b'BT /F1 18 Tf 72 720 Td (Invoice 4471) Tj 0 -24 Td (Zanzibarquill Supplies \\(made up\\)) Tj '
               b'T* [(Total due: EUR 2)-20(55.00)] TJ ET', compress=compress),
        stream(b'BT /F1 11 Tf 72 720 Td (Please pay by 20 November 2026.) Tj ET', compress=compress),
        b'<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>',
    ])


# A font whose codes are glyph numbers (as Chrome and Word write them): only its ToUnicode map says what they are
CMAP = (b'/CIDInit /ProcSet findresource begin 12 dict begin begincmap\n1 begincodespacerange <0000> <FFFF> endcodespacerange\n'
        b'2 beginbfchar\n<0003> <0020>\n<0010> <00E9>\nendbfchar\n'
        b'2 beginbfrange\n<0020> <0039> <0041>\n<0040> <0042> [<0066006C> <0031> <0032>]\nendbfrange\nendcmap end end')


def glyphs(text):
    """Codes for CMAP: A-Z are 0x20.., space 0x03, é 0x10, 'fl' 0x40, 1 and 2 are 0x41 and 0x42."""
    codes = {' ': 3, 'é': 0x10, '1': 0x41, '2': 0x42}
    out, i = b'', 0
    while i < len(text):
        if text.startswith('fl', i):
            out += (0x40).to_bytes(2, 'big')
            i += 2
            continue
        c = text[i]
        out += (codes[c] if c in codes else 0x20 + ord(c) - ord('A')).to_bytes(2, 'big')
        i += 1
    return b'<' + out.hex().upper().encode() + b'>'


def cid_pdf(packed):
    font = b'<</Type/Font/Subtype/Type0/BaseFont/ABCDEF+Made/Encoding/Identity-H/ToUnicode 5 0 R>>'
    page = b'<</Type/Page/Parent 2 0 R/Resources<</Font<</G7 4 0 R>>>>/Contents 6 0 R>>'
    content = stream(b'BT /G7 12 Tf 1 0 0 1 72 700 Tm ' + glyphs('CAFé RENT') + b' Tj 1 0 0 1 72 680 Tm [' + glyphs('flAT ') + b' -300 '
                     + glyphs('12') + b'] TJ ET', compress=True)
    if not packed:
        return pdf([b'<</Type/Catalog/Pages 2 0 R>>', b'<</Type/Pages/Kids[3 0 R]/Count 1>>', page, font, stream(CMAP, compress=True), content])
    # PDF 1.5: the catalog, pages and font packed in one compressed object stream (object 7)
    inner = [(1, b'<</Type/Catalog/Pages 2 0 R>>'), (2, b'<</Type/Pages/Kids[3 0 R]/Count 1>>'), (3, page), (4, font)]
    body, head, at = b'', b'', 0
    for n, obj in inner:
        head += b'%d %d ' % (n, at)
        body += obj + b' '
        at += len(obj) + 1
    packed_stream = stream(head + body, b'/Type/ObjStm/N 4/First %d' % len(head), compress=True)
    return pdf([b'null', b'null', b'null', b'null', stream(CMAP, compress=True), content, packed_stream])


class PdfText(unittest.TestCase):
    def test_a_pdfs_text_in_page_order(self):
        for compress in (False, True):
            self.assertEqual(file_text.excerpt(two_pages(compress), 'application/pdf'),
                             'Invoice 4471\nZanzibarquill Supplies (made up)\nTotal due: EUR 255.00\n\nPlease pay by 20 November 2026.')

    def test_fonts_read_through_their_tounicode_map_also_in_object_streams(self):
        for packed in (False, True):
            self.assertEqual(file_text.excerpt(cid_pdf(packed), 'application/pdf'), 'CAFé RENT\nflAT 12', packed)

    def test_no_text_is_no_error(self):
        scanned = pdf([b'<</Type/Catalog/Pages 2 0 R>>', b'<</Type/Pages/Kids[3 0 R]/Count 1>>',
                       b'<</Type/Page/Parent 2 0 R/Resources<</XObject<</Im1 5 0 R>>>>/Contents 4 0 R>>',
                       stream(b'q 612 0 0 792 0 0 cm /Im1 Do Q'), stream(b'\xff\xd8\xff' + b'\0' * 64, b'/Type/XObject/Subtype/Image/Filter/DCTDecode')])
        encrypted = two_pages() .replace(b'trailer\n<</Root 1 0 R', b'trailer\n<</Root 1 0 R/Encrypt 9 0 R')
        for data in (scanned, encrypted, b'%PDF-1.4\n' + bytes(range(256)) * 40, b'not a pdf', b'', two_pages()[:300]):
            self.assertIsInstance(file_text.excerpt(data, 'application/pdf'), str)
        self.assertEqual(file_text.excerpt(scanned, 'application/pdf'), '')
        self.assertEqual(file_text.excerpt(encrypted, 'application/pdf'), '')
        self.assertEqual(file_text.excerpt(b'%PDF-1.4\n' + bytes(range(256)) * 40, 'application/pdf'), '')

    def test_a_broken_file_never_raises(self):
        rng, base = random.Random(5), [two_pages(True), cid_pdf(True), cid_pdf(False)]
        for _ in range(200):
            data = bytearray(rng.choice(base))
            for _ in range(rng.randint(1, 20)):
                at = rng.randrange(len(data))
                if rng.random() < .5:
                    data[at] = rng.randrange(256)
                else:
                    del data[at:at + rng.randint(1, 80)]
            self.assertIsInstance(file_text.excerpt(bytes(data), 'application/pdf'), str)

    def test_bounded_for_files_from_anywhere(self):
        # A small file that inflates to a lot of text: cut at the limit, quickly
        bomb = pdf([stream(b'BT (Made up line) Tj ET\n' * 2_000_000, compress=True)] * 4)
        started = time.monotonic()
        text = file_text.excerpt(bomb, 'application/pdf', limit=500)
        self.assertLess(time.monotonic() - started, 5)
        self.assertLessEqual(len(text), 500)
        self.assertTrue(text.endswith('…'))
        # Odd bytes that look almost like object headers don't make the scan slow
        odd = b'%PDF-1.4\n' + (b'1 ' * 400_000) + b'obj'
        started = time.monotonic()
        file_text.excerpt(odd, 'application/pdf')
        self.assertLess(time.monotonic() - started, 5)


class PlainText(unittest.TestCase):
    def test_text_files_and_their_limit(self):
        self.assertEqual(file_text.excerpt('Agenda\r\n\r\n\r\n- Venue   quote\x00\n- Café'.encode(), 'text/plain'), 'Agenda\n\n- Venue quote\n- Café')
        self.assertEqual(file_text.excerpt(b'{"order": 4471}', 'application/json'), '{"order": 4471}')
        long = file_text.excerpt(('word ' * 2000).encode(), 'text/markdown', limit=100)
        self.assertLessEqual(len(long), 100)
        self.assertTrue(long.endswith('word…'))

    def test_images_and_office_files_give_no_text_here(self):
        for mime in ('image/png', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            self.assertEqual(file_text.excerpt(b'\x89PNG\r\n\x1a\n', mime), '')


if __name__ == '__main__':
    unittest.main()
