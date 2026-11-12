"""The small JPEG decoder (jpeg_image.py) that reads person photos for Team Graph thumbnails. The pictures are made
here by a small encoder (baseline and progressive, with restart intervals, subsampling and long Huffman codes), so
no picture file and no image library is needed: a progressive picture must read exactly as its baseline twin."""
import math
import random
import unittest

import jpeg_image

ZIGZAG = jpeg_image.ZIGZAG
COS = [[math.cos((2 * x + 1) * u * math.pi / 16) for u in range(8)] for x in range(8)]
SCALE = [math.sqrt(0.5) if u == 0 else 1.0 for u in range(8)]


def portrait(w, h):
    """A made-up avatar: a head and shoulders on a soft gradient, as RGB rows."""
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            fx, fy = x / w, y / h
            head = math.hypot(fx - 0.5, (fy - 0.4) * 1.1) < 0.2
            body = fy > 0.7 and math.hypot(fx - 0.5, (fy - 1.1) * 0.8) < 0.42
            row.append((236, 188, 150) if head else (40, 70, 120) if body else (int(90 + 120 * fx), int(160 + 60 * fy), 210))
        rows.append(row)
    return rows


def _fdct(samples):
    """8x8 level-shifted samples (row-major) to DCT coefficients (row-major), separably."""
    tmp = [sum(samples[y * 8 + x] * COS[x][u] for x in range(8)) for y in range(8) for u in range(8)]
    return [SCALE[u] * SCALE[v] / 4 * sum(tmp[y * 8 + u] * COS[y][v] for y in range(8)) for v in range(8) for u in range(8)]


def _cat(v):
    return abs(v).bit_length()


def _bits(v, s):
    return v if v >= 0 else v + (1 << s) - 1


def jpeg(rows, progressive=False, sampling=(2, 2), gray=False, restart=0, long_codes=False, quant=(3, 5)):
    """A JPEG of these RGB rows: baseline or progressive (spectral selection and successive approximation, with EOB
    runs), 4:2:0 or other sampling for luma, optional restart intervals and Huffman codes longer than the decoder's
    one-step look-up."""
    h, w = len(rows), len(rows[0])
    planes = [[[0.299 * r + 0.587 * g + 0.114 * b for r, g, b in row] for row in rows]]
    if not gray:
        planes.append([[128 - 0.168736 * r - 0.331264 * g + 0.5 * b for r, g, b in row] for row in rows])
        planes.append([[128 + 0.5 * r - 0.418688 * g - 0.081312 * b for r, g, b in row] for row in rows])
    factors = [sampling] + [(1, 1)] * (len(planes) - 1)
    hmax, vmax = max(f[0] for f in factors), max(f[1] for f in factors)
    mcusx, mcusy = -(-w // (8 * hmax)), -(-h // (8 * vmax))
    comps = []
    for i, (plane, (ch, cv)) in enumerate(zip(planes, factors)):
        bpl, bpc = mcusx * ch, mcusy * cv
        sx, sy = hmax // ch, vmax // cv
        q = quant[min(i, 1)]

        def sample(x, y, plane=plane, sx=sx, sy=sy):
            vals = [plane[min(h - 1, y * sy + j)][min(w - 1, x * sx + i)] for j in range(sy) for i in range(sx)]
            return sum(vals) / len(vals)
        blocks = {}
        for row in range(bpc):
            for col in range(bpl):
                coefs = _fdct([sample(col * 8 + x, row * 8 + y) - 128 for y in range(8) for x in range(8)])
                blocks[(row, col)] = [int(round(coefs[ZIGZAG[k]] / q)) for k in range(64)]
        comps.append({'id': i + 1, 'h': ch, 'v': cv, 'q': q, 'blocks': blocks, 'table': min(i, 1), 'bpl': bpl,
                      'bw': -(-(-(-w * ch // hmax)) // 8), 'bh': -(-(-(-h * cv // vmax)) // 8)})

    scans = []  # (component indexes, ss, se, ah, al, ops)

    def blocks_of(sel):
        if len(sel) == 1:
            c = comps[sel[0]]
            return [[(c, (r, k))] for r in range(c['bh']) for k in range(c['bw'])]
        return [[(comps[i], (my * comps[i]['v'] + v, mx * comps[i]['h'] + hh)) for i in sel
                 for v in range(comps[i]['v']) for hh in range(comps[i]['h'])] for my in range(mcusy) for mx in range(mcusx)]

    def scan(sel, ss, se, ah, al, encode):
        ops, units = [], blocks_of(sel)
        state = {'pred': {}, 'eobrun': 0}
        for n, unit in enumerate(units):
            if restart and n and n % restart == 0:
                flush(ops, state, unit[0][0])
                ops.append(('r',))
                state['pred'] = {}
            for c, at in unit:
                encode(ops, state, c, c['blocks'][at], ss, se, ah, al)
        flush(ops, state, units[-1][-1][0])
        scans.append((sel, ss, se, ah, al, ops))

    def flush(ops, state, c):
        run = state['eobrun']
        if run:
            r = run.bit_length() - 1
            ops += [('s', 'ac', c['table'], r << 4), ('b', run - (1 << r), r)]
            state['eobrun'] = 0

    def dc(ops, state, c, q, ss, se, ah, al):
        value = q[0] >> al
        diff = value - state['pred'].get(c['id'], 0)
        state['pred'][c['id']] = value
        ops += [('s', 'dc', c['table'], _cat(diff)), ('b', _bits(diff, _cat(diff)), _cat(diff))]

    def baseline(ops, state, c, q, ss, se, ah, al):
        dc(ops, state, c, q, ss, se, ah, al)
        run = 0
        for k in range(1, 64):
            if not q[k]:
                run += 1
                continue
            while run > 15:
                ops.append(('s', 'ac', c['table'], 0xF0))
                run -= 16
            ops += [('s', 'ac', c['table'], (run << 4) | _cat(q[k])), ('b', _bits(q[k], _cat(q[k])), _cat(q[k]))]
            run = 0
        if run:
            ops.append(('s', 'ac', c['table'], 0))

    def dc_refine(ops, state, c, q, ss, se, ah, al):
        ops.append(('b', (q[0] >> al) & 1, 1))

    def ac_first(ops, state, c, q, ss, se, ah, al):
        band = [(1 if q[k] > 0 else -1) * (abs(q[k]) >> al) for k in range(ss, se + 1)]
        if not any(band):
            state['eobrun'] += 1
            if state['eobrun'] == 0x7FFF:
                flush(ops, state, c)
            return
        flush(ops, state, c)
        run = 0
        for v in band:
            if not v:
                run += 1
                continue
            while run > 15:
                ops.append(('s', 'ac', c['table'], 0xF0))
                run -= 16
            ops += [('s', 'ac', c['table'], (run << 4) | _cat(v)), ('b', _bits(v, _cat(v)), _cat(v))]
            run = 0
        if run:
            state['eobrun'] += 1

    def ac_refine(ops, state, c, q, ss, se, ah, al):
        hist = {k: abs(q[k]) >> (al + 1) for k in range(ss, se + 1)}
        new = [k for k in range(ss, se + 1) if not hist[k] and (abs(q[k]) >> al) & 1]
        corrections = lambda a, b: [('b', (abs(q[k]) >> al) & 1, 1) for k in range(a, b) if hist[k]]
        cur = ss
        for p in new:
            zeros = [k for k in range(cur, p) if not hist[k]]
            while len(zeros) >= 16:
                ops.append(('s', 'ac', c['table'], 0xF0))
                ops += corrections(cur, zeros[15])
                cur, zeros = zeros[15] + 1, zeros[16:]
            ops += [('s', 'ac', c['table'], (len(zeros) << 4) | 1), ('b', 1 if q[p] > 0 else 0, 1)]
            ops += corrections(cur, p)
            cur = p + 1
        if cur <= se:
            ops.append(('s', 'ac', c['table'], 0))
            ops += corrections(cur, se + 1)

    every = list(range(len(comps)))
    if not progressive:
        scan(every, 0, 63, 0, 0, baseline)
    else:
        scan(every, 0, 0, 0, 1, dc)
        scan([0], 1, 5, 0, 1, ac_first)
        for i in every[1:]:
            scan([i], 1, 63, 0, 1, ac_first)
        scan([0], 6, 63, 0, 1, ac_first)
        for i in every:
            scan([i], 1, 63, 1, 0, ac_refine)
        scan(every, 0, 0, 1, 0, dc_refine)

    # Huffman tables: a flat code per table (all its symbols one length), longer than needed when asked
    used = {}
    for *_, ops in scans:
        for op in ops:
            if op[0] == 's':
                used.setdefault((op[1], op[2]), set()).add(op[3])
    codes, dht = {}, b''
    for (kind, table), symbols in sorted(used.items()):
        symbols = sorted(symbols)
        length = max(1, len(symbols).bit_length(), 12 if long_codes and kind == 'ac' else 0)
        counts = [0] * 16
        counts[length - 1] = len(symbols)
        codes[(kind, table)] = {s: (i, length) for i, s in enumerate(symbols)}
        dht += bytes(((1 if kind == 'ac' else 0) << 4 | table,)) + bytes(counts) + bytes(symbols)

    def segment(marker, body):
        return b'\xff' + bytes((marker,)) + (len(body) + 2).to_bytes(2, 'big') + body
    out = b'\xff\xd8'
    out += segment(0xDB, b''.join(bytes((t,)) + bytes((quant[t],)) * 64 for t in sorted({c['table'] for c in comps})))
    out += segment(0xC2 if progressive else 0xC0, bytes((8,)) + h.to_bytes(2, 'big') + w.to_bytes(2, 'big') + bytes((len(comps),))
                   + b''.join(bytes((c['id'], c['h'] << 4 | c['v'], c['table'])) for c in comps))
    out += segment(0xC4, dht)
    if restart:
        out += segment(0xDD, restart.to_bytes(2, 'big'))
    for sel, ss, se, ah, al, ops in scans:
        out += segment(0xDA, bytes((len(sel),)) + b''.join(bytes((comps[i]['id'], comps[i]['table'] << 4 | comps[i]['table'])) for i in sel)
                       + bytes((ss, se, ah << 4 | al)))
        data, acc, n, marker = bytearray(), 0, 0, 0

        def put(value, size):
            nonlocal acc, n
            acc, n = (acc << size) | value, n + size
            while n >= 8:
                byte = (acc >> (n - 8)) & 255
                data.append(byte)
                if byte == 0xFF:
                    data.append(0)
                n -= 8
                acc &= (1 << n) - 1
        for op in ops:
            if op[0] == 's':
                put(*codes[(op[1], op[2])][op[3]])
            elif op[0] == 'b':
                if op[2]:
                    put(op[1], op[2])
            else:
                if n:
                    put((1 << (8 - n)) - 1, 8 - n)
                data += bytes((0xFF, 0xD0 + marker % 8))
                marker += 1
        if n:
            put((1 << (8 - n)) - 1, 8 - n)
        out += bytes(data)
    return out + b'\xff\xd9'


def difference(rgba, rows):
    w = len(rows[0])
    return sum(abs(rgba[(y * w + x) * 4 + c] - rows[y][x][c]) for y in range(len(rows)) for x in range(w) for c in range(3)) / (len(rows) * w * 3)


class JpegImage(unittest.TestCase):
    rows = portrait(40, 36)

    def test_a_baseline_picture_reads_close_to_its_pixels_with_any_sampling(self):
        for sampling in ((2, 2), (1, 1), (2, 1)):
            w, h, rgba = jpeg_image.decode(jpeg(self.rows, sampling=sampling))
            self.assertEqual((w, h, len(rgba)), (40, 36, 40 * 36 * 4))
            self.assertLess(difference(rgba, self.rows), 8, sampling)
            self.assertEqual(set(rgba[3::4]), {255})

    def test_a_progressive_picture_reads_exactly_as_its_baseline_twin(self):
        for sampling in ((2, 2), (1, 1)):
            self.assertEqual(jpeg_image.decode(jpeg(self.rows, progressive=True, sampling=sampling)), jpeg_image.decode(jpeg(self.rows, sampling=sampling)))

    def test_restart_intervals_long_codes_and_gray(self):
        plain = jpeg_image.decode(jpeg(self.rows))
        self.assertEqual(jpeg_image.decode(jpeg(self.rows, restart=2)), plain)
        self.assertEqual(jpeg_image.decode(jpeg(self.rows, progressive=True, restart=3)), plain)
        self.assertEqual(jpeg_image.decode(jpeg(self.rows, long_codes=True)), plain)
        self.assertEqual(jpeg_image.decode(jpeg(self.rows, progressive=True, long_codes=True)), plain)
        w, h, rgba = jpeg_image.decode(jpeg(self.rows, gray=True, sampling=(1, 1)))
        self.assertEqual((w, h), (40, 36))
        self.assertTrue(all(rgba[i] == rgba[i + 1] == rgba[i + 2] for i in range(0, len(rgba), 4)))

    def test_a_big_picture_is_read_at_a_reduced_size_close_to_its_averages(self):
        rows = portrait(128, 96)
        w, h, rgba = jpeg_image.decode(jpeg(rows), side=32)  # 128 at 1/4 is 32: no full picture is built
        self.assertEqual((w, h), (32, 24))
        small = [[tuple(sum(rows[y * 4 + j][x * 4 + i][c] for j in range(4) for i in range(4)) / 16 for c in range(3))
                  for x in range(32)] for y in range(24)]
        self.assertLess(difference(rgba, small), 12)
        self.assertEqual(jpeg_image.decode(jpeg(rows), side=16)[:2], (16, 12))
        self.assertEqual(jpeg_image.decode(jpeg(rows, progressive=True), side=16)[:2], (16, 12))

    def test_what_it_does_not_read_is_bad_and_nothing_else(self):
        good = jpeg(self.rows)
        sof = good.index(b'\xff\xc0')
        for why, data in {'not a jpeg': b'\x89PNG\r\n\x1a\n', 'empty': b'', 'only the start': b'\xff\xd8',
                          'arithmetic coding': good[:sof] + b'\xff\xc9' + good[sof + 2:],
                          'lossless': good[:sof] + b'\xff\xc3' + good[sof + 2:],
                          '12-bit': good[:sof + 4] + b'\x0c' + good[sof + 5:],
                          'too many pixels': good[:sof + 5] + b'\x0f\xff\x0f\xff' + good[sof + 9:],
                          'no scan': good[:good.index(b'\xff\xda')] + b'\xff\xd9'}.items():
            with self.assertRaises(jpeg_image.Bad, msg=why):
                jpeg_image.decode(data)
        rng = random.Random(7)
        for data in [good[:n] for n in range(0, len(good), 37)] + [bytes(b ^ (rng.randrange(256) if rng.random() < 0.02 else 0) for b in good) for _ in range(40)]:
            try:
                w, h, rgba = jpeg_image.decode(data)
            except jpeg_image.Bad:
                continue
            self.assertEqual(len(rgba), w * h * 4)


if __name__ == '__main__':
    unittest.main()
