"""A small QR code encoder (byte mode, error correction M, versions 1 to 10: up to 213 bytes), standard library only.
It draws the mobile app's connect code in Settings (assistant.App.phone_app_view) without a dependency: the qrcode
package is only in the optional Telegram libraries. encode(text) returns the rows as strings of 0 and 1, as the
dashboard's qrSvg draws them (telegram_mirror.qr_matrix gives the same shape). tests/test_qr.py checks it against
known codes."""
from __future__ import annotations

# version: (EC codewords per block, [(blocks, data codewords per block), ...]) for level M
BLOCKS = {1: (10, [(1, 16)]), 2: (16, [(1, 28)]), 3: (26, [(1, 44)]), 4: (18, [(2, 32)]), 5: (24, [(2, 43)]),
          6: (16, [(4, 27)]), 7: (18, [(4, 31)]), 8: (22, [(2, 38), (2, 39)]), 9: (22, [(3, 36), (2, 37)]),
          10: (26, [(4, 43), (1, 44)])}
ALIGN = {2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46],
         10: [6, 28, 50]}
MASKS = [lambda r, c: (r + c) % 2 == 0, lambda r, c: r % 2 == 0, lambda r, c: c % 3 == 0, lambda r, c: (r + c) % 3 == 0,
         lambda r, c: (r // 2 + c // 3) % 2 == 0, lambda r, c: r * c % 2 + r * c % 3 == 0,
         lambda r, c: (r * c % 2 + r * c % 3) % 2 == 0, lambda r, c: ((r + c) % 2 + r * c % 3) % 2 == 0]

# GF(256) with the QR polynomial 0x11d
EXP, LOG = [0] * 512, [0] * 256
_x = 1
for _i in range(255):
    EXP[_i], LOG[_x] = _x, _i
    _x = (_x << 1) ^ (0x11d if _x & 0x80 else 0)
for _i in range(255, 512):
    EXP[_i] = EXP[_i - 255]


def ec_codewords(data, n):
    """Reed-Solomon: the n error correction codewords for a block."""
    gen = [1]
    for i in range(n):
        gen = [a ^ (EXP[LOG[b] + i] if b else 0) for a, b in zip(gen + [0], [0] + gen)]
    rest = list(data) + [0] * n
    for i in range(len(data)):
        factor = rest[i]
        if factor:
            for j, g in enumerate(gen):
                if g:
                    rest[i + j] ^= EXP[LOG[g] + LOG[factor]]
    return rest[len(data):]


def bch(value, poly, bits):
    """value followed by its BCH remainder (format and version information)."""
    rem = value << (poly.bit_length() - 1)
    while rem.bit_length() >= poly.bit_length():
        rem ^= poly << (rem.bit_length() - poly.bit_length())
    return (value << (poly.bit_length() - 1)) | rem


def codewords(data, version):
    ec, groups = BLOCKS[version]
    capacity = sum(n * size for n, size in groups)
    bits = '0100' + format(len(data), '08b' if version < 10 else '016b') + ''.join(format(b, '08b') for b in data)
    bits += '0' * min(4, capacity * 8 - len(bits))
    bits += '0' * (-len(bits) % 8)
    stream = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    stream += [(0xec, 0x11)[i % 2] for i in range(capacity - len(stream))]
    blocks, at = [], 0
    for n, size in groups:
        for _ in range(n):
            blocks.append(stream[at:at + size])
            at += size
    out = [b[i] for i in range(max(map(len, blocks))) for b in blocks if i < len(b)]
    ecs = [ec_codewords(b, ec) for b in blocks]
    return out + [e[i] for i in range(ec) for e in ecs]


def encode(text, mask=None):
    """The QR code of `text` as rows of '0' and '1' (no quiet zone). ValueError when it is too long. `mask` forces
    one of the 8 masks (tests); else the one with the lowest penalty."""
    data = text.encode('utf-8')
    version = next((v for v, (_, groups) in BLOCKS.items()
                    if len(data) + (3 if v >= 10 else 2) <= sum(n * size for n, size in groups)), None)
    if version is None:
        raise ValueError('Too long for a QR code')
    size = 17 + 4 * version
    grid = [[None] * size for _ in range(size)]

    def finder(r0, c0):
        for r in range(-1, 8):
            for c in range(-1, 8):
                if 0 <= r0 + r < size and 0 <= c0 + c < size:
                    grid[r0 + r][c0 + c] = 0 <= r <= 6 and 0 <= c <= 6 and (
                        r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4))
    finder(0, 0), finder(0, size - 7), finder(size - 7, 0)
    for i in range(8, size - 8):
        grid[6][i] = grid[i][6] = i % 2 == 0
    centers = ALIGN.get(version, [])
    for r in centers:
        for c in centers:
            if (r, c) not in ((6, 6), (6, size - 7), (size - 7, 6)):  # not on a finder; over the timing lines is right
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        grid[r + dr][c + dc] = max(abs(dr), abs(dc)) != 1
    grid[size - 8][8] = True  # the dark module
    reserved = [row[:] for row in grid]
    for i in range(9):  # format information areas
        for r, c in ((8, i), (i, 8)):
            if reserved[r][c] is None:
                reserved[r][c] = False
    for i in range(8):
        reserved[8][size - 1 - i] = False
    for i in range(7):  # above them the dark module
        reserved[size - 1 - i][8] = False
    if version >= 7:
        for i in range(6):
            for j in range(3):
                reserved[i][size - 11 + j] = reserved[size - 11 + j][i] = False
    bits = ''.join(format(b, '08b') for b in codewords(data, version))
    bits += '0' * (7 if 2 <= version <= 6 else 0)
    data_cells, at, upward = [], 0, True
    col = size - 1
    while col > 0:
        if col == 6:
            col -= 1
        for k in range(size):
            r = size - 1 - k if upward else k
            for c in (col, col - 1):
                if reserved[r][c] is None:
                    data_cells.append((r, c))
        upward = not upward
        col -= 2

    def build(mask):
        m = [row[:] for row in reserved]
        for i, (r, c) in enumerate(data_cells):
            m[r][c] = (bits[i] == '1' if i < len(bits) else False) != MASKS[mask](r, c)
        fmt = bch((0b00 << 3) | mask, 0b10100110111, 5) ^ 0b101010000010010  # level M is 00
        f = [(fmt >> i) & 1 == 1 for i in range(15)]
        for i in range(6):
            m[i][8] = f[i]
        m[7][8], m[8][8], m[8][7] = f[6], f[7], f[8]
        for i in range(9, 15):
            m[8][14 - i] = f[i]
        for i in range(8):
            m[8][size - 1 - i] = f[i]
        for i in range(8, 15):
            m[size - 15 + i][8] = f[i]
        if version >= 7:
            v = bch(version, 0b1111100100101, 6)
            for i in range(18):
                bit = (v >> i) & 1 == 1
                m[i // 3][size - 11 + i % 3] = m[size - 11 + i % 3][i // 3] = bit
        return m

    best = build(mask) if mask is not None else min((build(k) for k in range(8)), key=penalty)
    return [''.join('1' if cell else '0' for cell in row) for row in best]


def penalty(m):
    """The standard's score for a masked code; the lowest wins."""
    n, score = len(m), 0
    for lines in (m, [list(col) for col in zip(*m)]):
        for line in lines:
            run = 1
            for i in range(1, n + 1):
                if i < n and line[i] == line[i - 1]:
                    run += 1
                else:
                    score += run - 2 if run >= 5 else 0
                    run = 1
            text = ''.join('1' if x else '0' for x in line)
            score += 40 * sum(text.startswith(p, i) for p in ('10111010000', '00001011101') for i in range(n - 10))
    score += 3 * sum(m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1] for r in range(n - 1) for c in range(n - 1))
    dark = sum(map(sum, m)) * 100 // (n * n)
    return score + 10 * (abs(dark - 50) // 5)
