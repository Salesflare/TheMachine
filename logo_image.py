"""Small organization logos as pixels only, for the Team Graph (docs/shared-graph.md, "Logos from an organization's
own site").

A logo a Machine took from an organization's own website (enrichment.site_logos_step) stays a file on that Machine. For
a teammate it goes as a thumbnail made here: the picture is decoded and drawn again as a new PNG of at most 64 by 64
pixels, so only pixels travel, never the file's own bytes, its metadata or anything hidden in it. The receiving Machine
decodes what came with the same strict rules (only an 8-bit RGB or RGBA PNG of at most 64 by 64 pixels, with nothing
but its image chunks, nothing after its end) and draws it again before it keeps it.

Sources it reads: PNG and .ico files (with PNG or BMP pictures inside). JPEG and WebP have no decoder in the standard
library, and SVG can hold script: those are never sent. Standard library only."""
import struct
import zlib

SIGNATURE = b'\x89PNG\r\n\x1a\n'
SIDE = 64                 # a thumbnail's longest side, in pixels
MAX_BYTES = 8192          # a thumbnail's PNG at most: a few KB, so a shared record stays small
MAX_SOURCE_PIXELS = 512 * 512  # bigger source pictures are skipped: decoding them here would take too long


class Bad(ValueError):
    pass


def _chunks(data):
    """(type, body) of each PNG chunk, CRC checked; the bytes after IEND (should be none)."""
    if data[:8] != SIGNATURE:
        raise Bad('not a PNG')
    at, out = 8, []
    while True:
        if at + 12 > len(data):
            raise Bad('cut short')
        size, kind = struct.unpack('>I4s', data[at:at + 8])
        if size > len(data) - at - 12:
            raise Bad('chunk too long')
        body = data[at + 8:at + 8 + size]
        if struct.unpack('>I', data[at + 8 + size:at + 12 + size])[0] != zlib.crc32(kind + body) & 0xffffffff:
            raise Bad('bad CRC')
        out.append((kind, body))
        at += 12 + size
        if kind == b'IEND':
            return out, data[at:]


def _unfilter(raw, rows, stride, bpp):
    out, prev = bytearray(), bytearray(stride)
    for y in range(rows):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                line[i] = (line[i] + ((line[i - bpp] if i >= bpp else 0) + prev[i]) // 2) & 255
        elif f == 4:
            for i in range(stride):
                a, b, c = (line[i - bpp] if i >= bpp else 0), prev[i], (prev[i - bpp] if i >= bpp else 0)
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        elif f != 0:
            raise Bad('bad filter')
        out += line
        prev = line
    return out


def decode_png(data, max_side=None, strict=False):
    """(width, height, RGBA bytes) of a PNG. strict: only what this module makes (8-bit RGB or RGBA, not interlaced,
    only IHDR, IDAT and IEND, nothing after IEND), as a received thumbnail must be."""
    chunks, rest = _chunks(bytes(data))
    if chunks[0][0] != b'IHDR' or len(chunks[0][1]) != 13:
        raise Bad('no header')
    w, h, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', chunks[0][1])
    if not w or not h or (max_side and (w > max_side or h > max_side)) or w * h > MAX_SOURCE_PIXELS:
        raise Bad('size')
    if compression or filtering or interlace:
        raise Bad('interlaced or unknown method')
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color)
    if not channels or depth not in ({8, 16} if color in (2, 4, 6) else {1, 2, 4, 8} if color == 3 else {1, 2, 4, 8, 16}):
        raise Bad('color type')
    if strict and (color not in (2, 6) or depth != 8 or rest or any(k not in (b'IHDR', b'IDAT', b'IEND') for k, _ in chunks)):
        raise Bad('not a thumbnail')
    palette, trns = None, None
    for kind, body in chunks[1:]:
        if kind == b'PLTE':
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body) - len(body) % 3, 3)]
        elif kind == b'tRNS':
            trns = body
        elif kind[0] & 32 == 0 and kind not in (b'IDAT', b'IEND'):
            raise Bad('unknown critical chunk')
    stride = (w * channels * depth + 7) // 8
    want = h * (stride + 1)
    d = zlib.decompressobj()
    try:
        raw = d.decompress(b''.join(body for kind, body in chunks if kind == b'IDAT'), want + 1)
    except zlib.error as error:
        raise Bad('bad data') from error
    if len(raw) != want or d.unconsumed_tail:
        raise Bad('wrong amount of data')
    px = _unfilter(raw, h, stride, max(1, channels * depth // 8))
    out = bytearray(w * h * 4)
    if depth == 8 and color == 6:
        return w, h, bytes(px)
    for y in range(h):
        row = px[y * stride:(y + 1) * stride]
        if depth == 16:
            samples = row[0::2]
        elif depth == 8:
            samples = row
        else:
            per = 8 // depth
            samples = [(row[i // per] >> (8 - depth * (i % per + 1))) & ((1 << depth) - 1) for i in range(w * channels)]
        scale = 255 // ((1 << depth) - 1) if depth < 8 and color != 3 else 1
        for x in range(w):
            s = samples[x * channels:(x + 1) * channels]
            if color == 3:
                if not palette or s[0] >= len(palette):
                    raise Bad('palette')
                r, g, b = palette[s[0]]
                a = trns[s[0]] if trns and s[0] < len(trns) else 255
            elif color in (0, 4):
                r = g = b = s[0] * scale
                a = s[1] if color == 4 else 0 if trns and len(trns) == 2 and depth <= 8 and s[0] == trns[1] else 255
            else:
                r, g, b = s[0], s[1], s[2]
                a = s[3] if color == 6 else 255
            out[(y * w + x) * 4:(y * w + x) * 4 + 4] = bytes((r, g, b, a))
    return w, h, bytes(out)


def _bmp(data):
    """(width, height, RGBA) of the BMP picture inside an .ico (no file header; twice the height for its mask)."""
    if len(data) < 40 or struct.unpack('<I', data[:4])[0] != 40:
        raise Bad('not a BMP')
    w, h2, _, bits, compression = struct.unpack('<iiHHI', data[4:20])
    h = h2 // 2
    if not (0 < w <= 256 and 0 < h <= 256) or compression or bits not in (1, 4, 8, 24, 32):
        raise Bad('BMP kind')
    at = 40
    palette = []
    if bits <= 8:
        palette = [(data[at + 4 * i + 2], data[at + 4 * i + 1], data[at + 4 * i]) for i in range(1 << bits)]
        at += 4 << bits
    stride = ((w * bits + 31) // 32) * 4
    mask_stride = ((w + 31) // 32) * 4
    if len(data) < at + stride * h:
        raise Bad('BMP cut short')
    has_mask = len(data) >= at + stride * h + mask_stride * h
    out = bytearray(w * h * 4)
    alpha_seen = False
    for y in range(h):
        row = data[at + (h - 1 - y) * stride:at + (h - y) * stride]
        mask = data[at + stride * h + (h - 1 - y) * mask_stride:at + stride * h + (h - y) * mask_stride] if has_mask else b''
        for x in range(w):
            if bits == 32:
                b, g, r, a = row[x * 4:x * 4 + 4]
                alpha_seen = alpha_seen or a > 0
            elif bits == 24:
                b, g, r = row[x * 3:x * 3 + 3]
                a = 255
            else:
                i = (row[x * bits // 8] >> (8 - bits - (x * bits) % 8)) & ((1 << bits) - 1)
                r, g, b = palette[i]
                a = 255
            if mask and (bits != 32) and mask[x // 8] >> (7 - x % 8) & 1:
                a = 0
            out[(y * w + x) * 4:(y * w + x) * 4 + 4] = bytes((r, g, b, a))
    if bits == 32 and not alpha_seen:  # an old 32-bit icon without alpha: its mask says what is transparent
        for y in range(h):
            mask = data[at + stride * h + (h - 1 - y) * mask_stride:at + stride * h + (h - y) * mask_stride] if has_mask else b''
            for x in range(w):
                out[(y * w + x) * 4 + 3] = 0 if mask and mask[x // 8] >> (7 - x % 8) & 1 else 255
    return w, h, bytes(out)


def decode_ico(data):
    """The best picture of an .ico file: the smallest of 64 pixels or more, else the largest."""
    if len(data) < 6 or data[:4] != b'\x00\x00\x01\x00':
        raise Bad('not an icon')
    count = struct.unpack('<H', data[4:6])[0]
    entries = []
    for i in range(min(count, 32)):
        e = data[6 + 16 * i:22 + 16 * i]
        if len(e) < 16:
            break
        size, offset = struct.unpack('<II', e[8:16])
        entries.append(((e[0] or 256), offset, size))
    for side, offset, size in sorted(entries, key=lambda e: (0, e[0]) if e[0] >= SIDE else (1, -e[0])):
        part = data[offset:offset + size]
        if len(part) != size:
            continue
        try:
            return decode_png(part) if part[:8] == SIGNATURE else _bmp(part)
        except Bad:
            continue
    raise Bad('no picture in the icon')


def decode(data, kind):
    """(width, height, RGBA) of a saved site logo, by its type; Bad for anything this module doesn't read."""
    if kind == 'image/png':
        return decode_png(data)
    if kind == 'image/x-icon':
        return decode_ico(data)
    raise Bad('no decoder for ' + str(kind))  # JPEG, WebP: none in the standard library; SVG is never saved


def resize(w, h, rgba, side):
    """The picture fit within side x side, averaged over each new pixel's area (with its transparency weighed in);
    smaller ones stay their size."""
    scale = min(1.0, side / max(w, h))
    tw, th = max(1, round(w * scale)), max(1, round(h * scale))
    if (tw, th) == (w, h):
        return w, h, rgba
    out = bytearray(tw * th * 4)
    for ty in range(th):
        y0, y1 = ty * h // th, max(ty * h // th + 1, (ty + 1) * h // th)
        for tx in range(tw):
            x0, x1 = tx * w // tw, max(tx * w // tw + 1, (tx + 1) * w // tw)
            r = g = b = a = n = 0
            for y in range(y0, y1):
                base = y * w * 4
                for x in range(x0, x1):
                    i = base + x * 4
                    pa = rgba[i + 3]
                    r += rgba[i] * pa
                    g += rgba[i + 1] * pa
                    b += rgba[i + 2] * pa
                    a += pa
                    n += 1
            o = (ty * tw + tx) * 4
            out[o:o + 4] = bytes((r // a, g // a, b // a, a // n)) if a else bytes(4)
    return tw, th, bytes(out)


def encode_png(w, h, rgba):
    """A PNG of these pixels (RGB when it is fully opaque, else RGBA), with nothing but its image chunks."""
    opaque = all(rgba[i] == 255 for i in range(3, len(rgba), 4))
    channels = 3 if opaque else 4
    raw = bytearray()
    prev = bytes(w * channels)
    for y in range(h):
        line = rgba[y * w * 4:(y + 1) * w * 4]
        if opaque:
            line = bytes(b for i, b in enumerate(line) if i % 4 != 3)
        sub = bytes((line[i] - (line[i - channels] if i >= channels else 0)) & 255 for i in range(len(line)))
        up = bytes((line[i] - prev[i]) & 255 for i in range(len(line)))
        cost = lambda f: sum(v if v < 128 else 256 - v for v in f)
        f, data = min(((0, line), (1, sub), (2, up)), key=lambda c: cost(c[1]))
        raw += bytes((f,)) + data
        prev = line

    def chunk(kind, body):
        return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)
    return (SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6 if channels == 4 else 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


def thumbnail(data, kind):
    """A new PNG of a saved site logo, at most SIDE pixels and MAX_BYTES, or None when it can't be read or is blank."""
    try:
        w, h, rgba = decode(bytes(data), kind)
    except (Bad, IndexError, struct.error):
        return None
    if not any(rgba[i] for i in range(3, len(rgba), 4)):
        return None  # fully transparent: nothing to show
    for side in (SIDE, 48, 32):
        png = encode_png(*resize(w, h, rgba, side))
        if len(png) <= MAX_BYTES:
            return png
    return None


def received(data):
    """A teammate's thumbnail checked and drawn again here: a new PNG of the same pixels, or None. Only a PNG this
    module could have made passes: 8-bit RGB or RGBA, at most SIDE x SIDE and MAX_BYTES, nothing else in it."""
    if not isinstance(data, (bytes, bytearray)) or len(data) > MAX_BYTES:
        return None
    try:
        w, h, rgba = decode_png(data, max_side=SIDE, strict=True)
    except (Bad, IndexError, struct.error):
        return None
    png = encode_png(w, h, rgba)
    return png if len(png) <= MAX_BYTES * 2 else None
