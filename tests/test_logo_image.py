"""An organization's logo from its own site as a thumbnail of pixels only (logo_image.py, docs/shared-graph.md): what a
Machine makes of a saved site logo, and what a teammate's Machine accepts of it. No network."""
import struct
import unittest
import zlib

import logo_image as li


def chunk(kind, body):
    return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)


def png(w, h, rgba=None, extra=b'', color=6, depth=8, raw=None):
    """A PNG by hand: RGBA pixels (a gradient by default), optional chunks before IDAT."""
    rgba = rgba or bytes((x * 255 // max(1, w - 1), y * 255 // max(1, h - 1), 128, 255)[i] for y in range(h) for x in range(w) for i in range(4))
    if raw is None:
        raw = b''.join(b'\x00' + rgba[y * w * 4:(y + 1) * w * 4] for y in range(h))
    return (li.SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, depth, color, 0, 0, 0)) + extra
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def ico(*pictures):
    """An .ico file holding these pictures (PNG or BMP bytes), each with its side."""
    head, body, at = struct.pack('<HHH', 0, 1, len(pictures)), b'', 6 + 16 * len(pictures)
    for side, data in pictures:
        head += struct.pack('<BBBBHHII', side % 256, side % 256, 0, 0, 1, 32, len(data), at + len(body))
        body += data
    return head + body


def bmp(side, bits=32):
    """The BMP picture of an icon: a red square with a transparent quarter (alpha, or the mask for 24-bit)."""
    stride, mask_stride = ((side * bits + 31) // 32) * 4, ((side + 31) // 32) * 4
    rows, mask = b'', b''
    for y in range(side):  # bottom-up: the first rows are the picture's bottom
        clear = lambda x: x < side // 2 and y < side // 2
        if bits == 32:
            row = b''.join(bytes((0, 0, 255, 0 if clear(x) else 255)) for x in range(side))
        else:
            row = b''.join(bytes((0, 0, 255)) for x in range(side))
        rows += row + b'\x00' * (stride - len(row))
        bits_ = sum(1 << (7 - x % 8) << (8 * (x // 8)) for x in range(side) if clear(x) and bits != 32)
        mrow = bytes((bits_ >> (8 * i)) & 255 for i in range(side // 8 + (side % 8 > 0)))
        mask += mrow + b'\x00' * (mask_stride - len(mrow))
    return struct.pack('<IiiHHIIiiII', 40, side, side * 2, 1, bits, 0, 0, 0, 0, 0, 0) + rows + mask


class Thumbnail(unittest.TestCase):
    def test_a_big_png_becomes_a_small_new_png_of_its_pixels_only(self):
        source = png(180, 120, extra=chunk(b'tEXt', b'Comment\x00https://client.example <script>alert(1)</script>'))
        out = li.thumbnail(source, 'image/png')
        w, h, _ = li.decode_png(out, max_side=64, strict=True)
        self.assertEqual((w, h), (64, 43))  # its shape kept
        self.assertLessEqual(len(out), li.MAX_BYTES)
        self.assertNotIn(b'client.example', out)
        self.assertNotIn(b'script', out)
        self.assertNotIn(b'tEXt', out)

    def test_a_small_favicon_stays_its_size(self):
        out = li.thumbnail(png(16, 16), 'image/png')
        self.assertEqual(li.decode_png(out, strict=True)[:2], (16, 16))

    def test_an_icon_gives_its_best_picture_png_or_bmp_with_transparency(self):
        out = li.thumbnail(ico((16, png(16, 16)), (64, bmp(64)), (32, bmp(32, 24))), 'image/x-icon')
        w, h, rgba = li.decode_png(out, strict=True)
        self.assertEqual((w, h), (64, 64))
        self.assertEqual(rgba[:4], b'\xff\x00\x00\xff')  # top left: red
        self.assertEqual(rgba[(63 * 64) * 4 + 3], 0)  # bottom left: transparent
        w, h, rgba = li.decode_png(li.thumbnail(ico((32, bmp(32, 24))), 'image/x-icon'), strict=True)
        self.assertEqual(((w, h), rgba[3], rgba[(31 * 32) * 4 + 3]), ((32, 32), 255, 0))  # 24-bit: its mask says what is clear

    def test_palette_and_grey_pngs_are_read(self):
        palette = chunk(b'PLTE', b'\xff\x00\x00\x00\xff\x00') + chunk(b'tRNS', b'\xff\x00')
        source = png(8, 8, color=3, depth=1, extra=palette, raw=b''.join(b'\x00' + bytes((0b10101010,)) for _ in range(8)))
        rgba = li.decode_png(li.thumbnail(source, 'image/png'), strict=True)[2]
        self.assertEqual(rgba[:8], b'\x00\xff\x00\x00\xff\x00\x00\xff')  # index 1 (green, clear), then 0 (red)
        grey = png(4, 4, color=0, depth=8, raw=b''.join(b'\x00' + bytes((200,) * 4) for _ in range(4)))
        self.assertEqual(li.decode_png(li.thumbnail(grey, 'image/png'), strict=True)[2][:4], b'\xc8\xc8\xc8\xff')

    def test_what_it_cant_read_safely_gives_nothing(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
        for data, kind in ((svg, 'image/svg+xml'), (svg, 'image/png'), (b'\xff\xd8\xff\xe0' + b'0' * 100, 'image/jpeg'),
                           (b'RIFF\x00\x00\x00\x00WEBPVP8 ', 'image/webp'), (png(4, 4)[:30], 'image/png'), (b'\x00\x00\x01\x00\x01\x00', 'image/x-icon'),
                           (png(4, 4, rgba=bytes(64)), 'image/png'),  # fully transparent
                           (png(1024, 1024, raw=b''), 'image/png')):  # too big to decode here
            self.assertIsNone(li.thumbnail(data, kind), data[:20])


class Received(unittest.TestCase):
    """What a teammate's Machine accepts: only a PNG this module could have made, drawn again before it is kept."""
    def test_a_thumbnail_is_drawn_again_from_its_pixels(self):
        made = li.thumbnail(png(100, 100), 'image/png')
        again = li.received(made)
        self.assertEqual(li.decode_png(again, strict=True), li.decode_png(made, strict=True))

    def test_anything_else_is_refused(self):
        good = li.thumbnail(png(64, 64), 'image/png')
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(1)</script></svg>'
        bomb = li.SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', 64, 64, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b'\x00' * 5_000_000)) + chunk(b'IEND', b'')
        bad_crc = bytearray(good)
        bad_crc[-5] ^= 1
        refused = {
            'oversized': good + b'\x00' * li.MAX_BYTES,
            'too wide': png(65, 10),
            'too tall': png(10, 65),
            'svg with script': svg,
            'jpeg': b'\xff\xd8\xff\xe0\x00\x10JFIF' + b'\x00' * 200,
            'gif': b'GIF89a' + b'\x00' * 50,
            'polyglot: html after the end': good + b'<html><script>alert(1)</script></html>',
            'polyglot: zip after the end': good + b'PK\x03\x04' + b'\x00' * 30,
            'text chunk with script': png(8, 8, extra=chunk(b'tEXt', b'x\x00<script>alert(1)</script>')),
            'palette': png(8, 8, color=3, depth=8, extra=chunk(b'PLTE', b'\x00' * 3), raw=b''.join(b'\x00' + bytes(8) for _ in range(8))),
            '16-bit': png(4, 4, color=6, depth=16, raw=b''.join(b'\x00' + bytes(32) for _ in range(4))),
            'too much data (a bomb)': bomb,
            'too little data': png(8, 8, raw=b'\x00' * 10),
            'bad CRC': bytes(bad_crc),
            'not bytes': 'iVBORw0KGgo=',
            'empty': b'',
        }
        for why, data in refused.items():
            self.assertIsNone(li.received(data), why)


if __name__ == '__main__':
    unittest.main()
