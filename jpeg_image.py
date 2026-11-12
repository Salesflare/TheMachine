"""A small JPEG decoder for thumbnails (logo_image.py): baseline and progressive JPEG with Huffman coding, 8-bit, gray
or three colors (YCbCr, or RGB by its Adobe marker), any sampling and restart intervals. Arithmetic coding, 12-bit,
lossless, hierarchical and CMYK pictures are not read (Bad). Standard library only.

It decodes at a reduced size straight away (an 8 by 8 block becomes 1, 2 or 4 pixels when that still gives at least
`side` pixels), as libjpeg does for its scaled reads, so a thumbnail never builds the full picture. The entropy-coded
data is still read in full, so the source is capped by pixel count (MAX_PIXELS) and the callers' byte caps."""
import math
from array import array

MAX_PIXELS = 800 * 800  # bigger pictures are skipped: reading them here would take too long
ZIGZAG = (0, 1, 8, 16, 9, 2, 3, 10, 17, 24, 32, 25, 18, 11, 4, 5, 12, 19, 26, 33, 40, 48, 41, 34, 27, 20, 13, 6, 7, 14, 21,
          28, 35, 42, 49, 56, 57, 50, 43, 36, 29, 22, 15, 23, 30, 37, 44, 51, 58, 59, 52, 45, 38, 31, 39, 46, 53, 60, 61, 54,
          47, 55, 62, 63)  # the natural (row * 8 + column) place of each zigzag index
NATURAL = {n: i for i, n in enumerate(ZIGZAG)}
LOOK = 9  # Huffman codes up to this many bits are read with one table look-up


class Bad(ValueError):
    """A picture this module doesn't read."""


def _table(counts, symbols):
    """(look-up for codes up to LOOK bits, {(length, code): symbol} for longer ones) of a DHT table."""
    look, slow, code, at = [None] * (1 << LOOK), {}, 0, 0
    for length in range(1, 17):
        for _ in range(counts[length - 1]):
            if code >= 1 << length:
                raise Bad
            if length <= LOOK:
                base = code << (LOOK - length)
                for i in range(1 << (LOOK - length)):
                    look[base + i] = (length, symbols[at])
            else:
                slow[(length, code)] = symbols[at]
            code, at = code + 1, at + 1
        code <<= 1
    return look, slow


class _Bits:
    """The bits of one entropy-coded segment (stuffed bytes and markers already taken out)."""
    __slots__ = ('data', 'pos', 'acc', 'n')

    def __init__(self, data):
        self.data, self.pos, self.acc, self.n = data, 0, 0, 0

    def fill(self, k):
        while self.n < k:
            if self.pos < len(self.data):
                byte = self.data[self.pos]
            elif self.pos > len(self.data) + 1024:
                raise Bad  # far past its end: a broken picture
            else:
                byte = 0
            self.pos += 1
            self.acc = (self.acc << 8) | byte
            self.n += 8

    def bits(self, k):
        if not k:
            return 0
        self.fill(k)
        self.n -= k
        value = self.acc >> self.n
        self.acc &= (1 << self.n) - 1
        return value

    def extend(self, s):
        """A coefficient of s bits (JPEG's RECEIVE and EXTEND)."""
        value = self.bits(s)
        return value - (1 << s) + 1 if s and value < 1 << (s - 1) else value

    def symbol(self, table):
        look, slow = table
        self.fill(16)
        found = look[(self.acc >> (self.n - LOOK)) & ((1 << LOOK) - 1)]
        if found:
            self.n -= found[0]
            self.acc &= (1 << self.n) - 1
            return found[1]
        for length in range(LOOK + 1, 17):
            symbol = slow.get((length, (self.acc >> (self.n - length)) & ((1 << length) - 1)))
            if symbol is not None:
                self.n -= length
                self.acc &= (1 << self.n) - 1
                return symbol
        raise Bad


def _segments(data, at):
    """(the entropy-coded segments of a scan from `at`, split at its restart markers; where the scan ends)."""
    out, part, end = [], bytearray(), len(data)
    while at < end:
        byte = data[at]
        if byte != 0xFF:
            part.append(byte)
            at += 1
            continue
        nxt = data[at + 1] if at + 1 < end else 0xD9
        if nxt == 0:
            part.append(0xFF)
            at += 2
        elif 0xD0 <= nxt <= 0xD7:
            out.append(bytes(part))
            part = bytearray()
            at += 2
        elif nxt == 0xFF:
            at += 1  # fill bytes
        else:
            break
    out.append(bytes(part))
    return out, at


class _Component:
    __slots__ = ('id', 'h', 'v', 'tq', 'td', 'ta', 'bpl', 'bpc', 'bw', 'bh', 'coefs', 'pred')


def _decode_scan(frame, comps, segments, ss, se, ah, al, interval):
    """Reads one scan's coefficients into its components (baseline: one scan with everything; progressive: a band of
    coefficients, a first pass or a refinement)."""
    progressive = frame['progressive']
    if progressive and (ss > se or se > 63 or (ss == 0 and se) or (ss and len(comps) != 1) or al > 13):
        raise Bad
    single = len(comps) == 1
    total = comps[0].bw * comps[0].bh if single else frame['mcusx'] * frame['mcusy']
    every = interval or total
    p1, m1 = 1 << al, -1 << al
    eob = [0]

    def baseline(c, o, bits, dc, ac):
        t = bits.symbol(dc)
        c.pred += bits.extend(t) if t else 0
        co = c.coefs
        co[o] = c.pred
        k = 1
        while k < 64:
            rs = bits.symbol(ac)
            s, r = rs & 15, rs >> 4
            if not s:
                if r < 15:
                    break
                k += 16
                continue
            k += r
            if k > 63:
                raise Bad
            co[o + k] = bits.extend(s)
            k += 1

    def dc_first(c, o, bits, dc, ac):
        t = bits.symbol(dc)
        c.pred += bits.extend(t) if t else 0
        c.coefs[o] = c.pred * p1

    def dc_refine(c, o, bits, dc, ac):
        if bits.bits(1):
            c.coefs[o] |= p1

    def ac_first(c, o, bits, dc, ac):
        if eob[0]:
            eob[0] -= 1
            return
        co, k = c.coefs, ss
        while k <= se:
            rs = bits.symbol(ac)
            s, r = rs & 15, rs >> 4
            if not s:
                if r < 15:
                    eob[0] = (1 << r) - 1 + bits.bits(r)
                    break
                k += 16
                continue
            k += r
            if k > 63:
                raise Bad
            co[o + k] = bits.extend(s) * p1
            k += 1

    def ac_refine(c, o, bits, dc, ac):
        co, k = c.coefs, ss
        if not eob[0]:
            while k <= se:
                rs = bits.symbol(ac)
                s, r = rs & 15, rs >> 4
                if s:
                    s = p1 if bits.bits(1) else m1
                elif r != 15:
                    eob[0] = (1 << r) + bits.bits(r)
                    break
                while k <= se:
                    z = o + k
                    if co[z]:
                        if bits.bits(1) and not co[z] & p1:
                            co[z] += p1 if co[z] >= 0 else m1
                    else:
                        r -= 1
                        if r < 0:
                            break
                    k += 1
                if s and k <= se:
                    co[o + k] = s
                k += 1
        if eob[0]:
            while k <= se:
                z = o + k
                if co[z] and bits.bits(1) and not co[z] & p1:
                    co[z] += p1 if co[z] >= 0 else m1
                k += 1
            eob[0] -= 1

    if not progressive:
        block = baseline
    elif ss == 0:
        block = dc_first if not ah else dc_refine
    else:
        block = ac_first if not ah else ac_refine
    tables = [(frame['dc'].get(c.td), frame['ac'].get(c.ta)) for c in comps]
    for dc, ac in tables:
        if (block in (baseline, dc_first) and dc is None) or (block in (baseline, ac_first, ac_refine) and ac is None):
            raise Bad
    mcu = 0
    for segment in segments:
        if mcu >= total:
            break
        bits = _Bits(segment)
        eob[0] = 0
        for c in comps:
            c.pred = 0
        end = min(total, mcu + every)
        while mcu < end:
            if single:
                c = comps[0]
                row, col = divmod(mcu, c.bw)
                block(c, (row * c.bpl + col) * 64, bits, *tables[0])
            else:
                my, mx = divmod(mcu, frame['mcusx'])
                for (dc, ac), c in zip(tables, comps):
                    for v in range(c.v):
                        for h in range(c.h):
                            block(c, ((my * c.v + v) * c.bpl + mx * c.h + h) * 64, bits, dc, ac)
            mcu += 1


def _ceil(a, b):
    return -(-a // b)


def _idct_table(n):
    """T[x][u]: the 8-point inverse DCT's basis at the centers of n equal parts of a block, for its first n
    frequencies (a block read at 1/8, 1/4 or 1/2 of its size)."""
    return [[(math.sqrt(0.5) if u == 0 else 1.0) / 2 * math.cos((2 * x + 1) * u * math.pi / (2 * n)) for u in range(n)] for x in range(n)]


def _plane(c, quant, n):
    """A component's samples at n/8 of its size, as one row-major plane (bpl * n wide)."""
    t = _idct_table(n)
    width = c.bpl * n
    out = bytearray(width * c.bpc * n)
    places = [NATURAL[v * 8 + u] for v in range(n) for u in range(n)]
    pairs = list(zip(places, [quant[p] for p in places]))
    dc_scale, co, span = t[0][0] * t[0][0], c.coefs, range(n)
    for row in range(c.bpc):
        for col in range(c.bpl):
            o = (row * c.bpl + col) * 64
            f = [co[o + p] * q for p, q in pairs]
            top = row * n * width + col * n
            if not any(f[1:]):  # a flat block (common in a small picture): one value
                value = _CLAMP[int(f[0] * dc_scale + 128.5) + 512]
                for y in span:
                    out[top + y * width:top + y * width + n] = bytes((value,)) * n
                continue
            tmp = [0.0] * (n * n)
            for y in span:
                ty = t[y]
                for u in span:
                    s = 0.0
                    for v in span:
                        s += ty[v] * f[v * n + u]
                    tmp[y * n + u] = s
            for y in span:
                line = top + y * width
                for x in span:
                    tx, s = t[x], 0.0
                    for u in span:
                        s += tx[u] * tmp[y * n + u]
                    out[line + x] = _CLAMP[int(s + 128.5) + 512]
    return width, out


def decode(data, side=None):
    """(width, height, RGBA) of a JPEG; with side, at the smallest of its sizes 1/8, 1/4, 1/2 or full that is still
    at least side pixels on its longest side. Bad for anything this module doesn't read."""
    try:
        return _decode(bytes(data), side)
    except (IndexError, OverflowError, ValueError) as error:
        raise Bad from error


def _decode(data, side):
    if data[:2] != b'\xff\xd8':
        raise Bad
    at, frame, quant, adobe = 2, None, {}, None
    dc, ac, interval, scans = {}, {}, 0, 0
    while at + 4 <= len(data):
        if data[at] != 0xFF:
            raise Bad
        marker = data[at + 1]
        if marker == 0xFF:
            at += 1
            continue
        if marker == 0xD9:
            break
        size = int.from_bytes(data[at + 2:at + 4], 'big')
        body = data[at + 4:at + 2 + size]
        if size < 2 or len(body) != size - 2:
            raise Bad
        at += 2 + size
        if marker == 0xDB:
            i = 0
            while i < len(body):
                wide, tq = body[i] >> 4, body[i] & 15
                n = 128 if wide else 64
                values = body[i + 1:i + 1 + n]
                if len(values) != n or tq > 3:
                    raise Bad
                quant[tq] = [int.from_bytes(values[j:j + 2], 'big') for j in range(0, 128, 2)] if wide else list(values)
                i += 1 + n
        elif marker == 0xC4:
            i = 0
            while i < len(body):
                kind, th = body[i] >> 4, body[i] & 15
                counts = body[i + 1:i + 17]
                total = sum(counts)
                symbols = body[i + 17:i + 17 + total]
                if len(counts) != 16 or len(symbols) != total or kind > 1 or th > 3 or total > 256:
                    raise Bad
                (ac if kind else dc)[th] = _table(counts, symbols)
                i += 17 + total
        elif marker == 0xDD:
            if len(body) != 2:
                raise Bad
            interval = int.from_bytes(body, 'big')
        elif marker == 0xEE and body[:5] == b'Adobe' and len(body) >= 12:
            adobe = body[11]
        elif marker in (0xC0, 0xC1, 0xC2):
            if frame or len(body) < 6:
                raise Bad
            precision, height, width, count = body[0], int.from_bytes(body[1:3], 'big'), int.from_bytes(body[3:5], 'big'), body[5]
            if precision != 8 or not height or not width or width * height > MAX_PIXELS or count not in (1, 3) or len(body) != 6 + 3 * count:
                raise Bad
            comps = []
            for i in range(count):
                c = _Component()
                c.id, c.h, c.v, c.tq = body[6 + 3 * i], body[7 + 3 * i] >> 4, body[7 + 3 * i] & 15, body[8 + 3 * i]
                if not (1 <= c.h <= 4 and 1 <= c.v <= 4) or c.tq > 3:
                    raise Bad
                comps.append(c)
            hmax, vmax = max(c.h for c in comps), max(c.v for c in comps)
            mcusx, mcusy = _ceil(width, 8 * hmax), _ceil(height, 8 * vmax)
            for c in comps:
                c.bw, c.bh = _ceil(_ceil(width * c.h, hmax), 8), _ceil(_ceil(height * c.v, vmax), 8)
                c.bpl, c.bpc = mcusx * c.h, mcusy * c.v
                c.coefs = array('i', bytes(4 * 64 * c.bpl * c.bpc))
                c.pred = 0
            frame = {'width': width, 'height': height, 'comps': comps, 'hmax': hmax, 'vmax': vmax, 'mcusx': mcusx, 'mcusy': mcusy,
                     'progressive': marker == 0xC2, 'dc': dc, 'ac': ac}
        elif 0xC3 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            raise Bad  # lossless, hierarchical or arithmetic coding
        elif marker == 0xDA:
            if not frame or not body or len(body) != 4 + 2 * body[0]:
                raise Bad
            by_id = {c.id: c for c in frame['comps']}
            chosen = []
            for i in range(body[0]):
                c = by_id.get(body[1 + 2 * i])
                if c is None or c in chosen:
                    raise Bad
                c.td, c.ta = body[2 + 2 * i] >> 4, body[2 + 2 * i] & 15
                chosen.append(c)
            ss, se, ah, al = body[-3], body[-2], body[-1] >> 4, body[-1] & 15
            if not frame['progressive'] and (ss or se != 63 or ah or al):
                raise Bad
            segments, at = _segments(data, at)
            _decode_scan(frame, chosen, segments, ss, se, ah, al, interval)
            scans += 1
            if scans > 64:
                raise Bad
    if not frame or not scans:
        raise Bad
    return _pixels(frame, quant, adobe, side)


def _pixels(frame, quant, adobe, side):
    width, height, comps = frame['width'], frame['height'], frame['comps']
    n = next((n for n in (1, 2, 4) if side and max(width, height) * n / 8 >= side), 8)
    planes = []
    for c in comps:
        if c.tq not in quant:
            raise Bad
        planes.append(_plane(c, quant[c.tq], n))
    w, h = -(-width * n // 8), -(-height * n // 8)
    out = bytearray(w * h * 4)
    out[3::4] = b'\xff' * (w * h)
    rgb = len(comps) == 3 and (adobe == 0 or [c.id for c in comps] == [ord('R'), ord('G'), ord('B')])
    hmax, vmax = frame['hmax'], frame['vmax']
    columns = [[x * c.h // hmax for x in range(w)] for c in comps]
    for y in range(h):
        s = [[plane[row + x] for x in xs] for (pw, plane), xs, row in
             zip(planes, columns, [(y * c.v // vmax) * pw for c, (pw, _) in zip(comps, planes)])]
        if len(s) == 1:
            r = g = b = bytes(s[0])
        elif rgb:
            r, g, b = bytes(s[0]), bytes(s[1]), bytes(s[2])
        else:
            lum, cb, cr = s
            r = bytes([_CLAMP[a + _CR_R[d] + 512] for a, d in zip(lum, cr)])
            g = bytes([_CLAMP[a + ((_CB_G[e] + _CR_G[d]) >> 16) + 512] for a, e, d in zip(lum, cb, cr)])
            b = bytes([_CLAMP[a + _CB_B[e] + 512] for a, e in zip(lum, cb)])
        line = y * w * 4
        out[line:line + w * 4:4], out[line + 1:line + w * 4:4], out[line + 2:line + w * 4:4] = r, g, b
    return w, h, bytes(out)


# YCbCr to RGB in whole numbers (as libjpeg does): R = Y + 1.402 Cr, G = Y - 0.34414 Cb - 0.71414 Cr, B = Y + 1.772 Cb
_CLAMP = bytes([0] * 512 + list(range(256)) + [255] * 768)  # a value + 512, clamped to 0..255
_CR_R = [int(1.402 * (i - 128) + 0.5 * (1 if i >= 128 else -1)) for i in range(256)]
_CB_B = [int(1.772 * (i - 128) + 0.5 * (1 if i >= 128 else -1)) for i in range(256)]
_CB_G = [-int(0.34414 * 65536 + 0.5) * (i - 128) for i in range(256)]
_CR_G = [-int(0.71414 * 65536 + 0.5) * (i - 128) + 32768 for i in range(256)]
