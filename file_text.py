"""The text of a file the owner added to a new to-do (chat_files.py), so the review can fill the to-do in from it.

A PDF's text is read here with the standard library only: its content streams (plain or FlateDecode, also inside
object streams), the text it shows (Tj, TJ, ' and "), with each font's ToUnicode map when it has one. Scanned pages
(images only), encrypted files and other filters give no text; the file itself still reaches the to-do's runs, which
can read it with their own tools. Plain text files are read as UTF-8. Nothing leaves the Machine: this only reads
the bytes it already keeps.

Bounded on purpose, since a file comes from anywhere: at most INFLATE_BYTES inflated in all (STREAM_BYTES per
stream), MAX_OBJECTS objects, and at most `limit` characters out. A file it can't read gives ''."""
from __future__ import annotations

import re
import zlib

INFLATE_BYTES = 24 * 1024 * 1024
STREAM_BYTES = 8 * 1024 * 1024
MAX_OBJECTS = 20000
MAX_TOKENS = 3_000_000
TEXT_LIMIT = 4000
TEXT_TYPES = ('text/', 'application/json', 'message/rfc822')

_OBJ = re.compile(rb'(?<![0-9])(\d{1,10})[ \t\r\n\f\x00]{1,8}(\d{1,5})[ \t\r\n\f\x00]{1,8}obj\b')  # bounded: no slow scan of odd bytes
_REF = re.compile(rb'(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R\b')
_NAME_REF = re.compile(rb'/([^\s/<>\[\]()%{}]{1,127})\s{1,8}(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R\b')
_WS = b' \t\r\n\f\x00'
_DELIM = b'()<>[]{}/%'


def excerpt(data, mime, limit=TEXT_LIMIT):
    """Up to `limit` characters of a file's text, tidied (one space between words, at most one blank line), or ''."""
    try:
        if mime == 'application/pdf':
            text = pdf_text(data, limit * 2)
        elif any(str(mime).startswith(t) for t in TEXT_TYPES):
            text = data[:limit * 4].decode('utf-8', 'replace')
        else:
            return ''
    except Exception:  # a broken file is not an error for the to-do: it just has no text to read
        return ''
    return tidy(text, limit)


def tidy(text, limit=TEXT_LIMIT):
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f�]', '', str(text or ''))
    lines = [' '.join(line.split()) for line in text.replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()
    if len(text) > limit:
        cut = text[:limit - 1]
        text = (cut.rsplit(' ', 1)[0] if ' ' in cut[-40:] else cut).rstrip() + '…'
    return text


# --- PDF ---------------------------------------------------------------------------------------------------------

class _Budget:
    """What reading one file may still take: inflated bytes, content tokens."""
    def __init__(self):
        self.left = INFLATE_BYTES
        self.tokens = MAX_TOKENS


class _Out(list):
    """The text so far, with its length."""
    chars = 0

    def append(self, text):
        self.chars += len(text)
        super().append(text)


def _inflate(raw, budget):
    take = min(STREAM_BYTES, budget.left)
    if take <= 0:
        return None
    d = zlib.decompressobj()
    try:
        out = d.decompress(raw, take)
    except zlib.error:
        # Some writers end a stream early or with junk: keep what inflated
        return None
    budget.left -= len(out)
    return out


def _stream(dictionary, raw, budget):
    """A stream's decoded bytes, or None for a filter this doesn't read (images, LZW, encryption...)."""
    found = re.search(rb'/Filter\s*(\[[^\]]*\]|/[A-Za-z0-9]+)', dictionary)
    filters = re.findall(rb'/([A-Za-z0-9]+)', found[1]) if found else []
    if not filters:
        return raw
    if filters in ([b'FlateDecode'], [b'Fl']) and not re.search(rb'/Predictor\s+(?:[2-9]|1\d)', dictionary):
        return _inflate(raw, budget)
    return None


def _objects(data, budget):
    """{object number: (dictionary bytes, decoded stream or None)}; objects in object streams too."""
    objects, packed = {}, []
    for count, m in enumerate(_OBJ.finditer(data)):
        if count >= MAX_OBJECTS:
            break
        start = m.end()
        end = data.find(b'endobj', start)
        if end < 0:
            end = len(data)
        body = data[start:end]
        s = re.search(rb'\bstream(?:\r\n|\n|\r)', body)
        number = int(m[1])
        if s:
            dictionary = body[:s.start()]
            raw = body[s.end():]
            e = raw.rfind(b'endstream')
            raw = raw[:e] if e >= 0 else raw
            stream = _stream(dictionary, raw, budget)
            objects[number] = (dictionary, stream)
            if stream and re.search(rb'/Type\s*/ObjStm\b', dictionary):
                packed.append((dictionary, stream))
        else:
            objects.setdefault(number, (body, None))
    for dictionary, stream in packed:  # PDF 1.5: small objects (fonts, pages) packed in a compressed stream
        n, first = re.search(rb'/N\s+(\d+)', dictionary), re.search(rb'/First\s+(\d+)', dictionary)
        if not n or not first:
            continue
        head = stream[:int(first[1])].split()
        pairs = [(int(head[i]), int(head[i + 1])) for i in range(0, min(len(head) - 1, 2 * int(n[1])), 2) if head[i].isdigit() and head[i + 1].isdigit()]
        for i, (number, offset) in enumerate(pairs):
            start = int(first[1]) + offset
            end = int(first[1]) + pairs[i + 1][1] if i + 1 < len(pairs) else len(stream)
            if number not in objects or objects[number][0].strip() in (b'', b'null'):
                objects[number] = (stream[start:end], None)
        if len(objects) > MAX_OBJECTS:
            break
    return objects


def _hex(s):
    s = re.sub(rb'[^0-9A-Fa-f]', b'', s)
    if len(s) % 2:
        s += b'0'
    return bytes.fromhex(s.decode())


def _cmap(stream):
    """A ToUnicode CMap: ({code bytes: text}, code lengths)."""
    out = {}
    for block in re.findall(rb'beginbfchar(.*?)endbfchar', stream, re.S):
        for src, dst in re.findall(rb'<([0-9A-Fa-f\s]+)>\s*<([0-9A-Fa-f\s]*)>', block):
            out[_hex(src)] = _hex(dst).decode('utf-16-be', 'ignore')
    for block in re.findall(rb'beginbfrange(.*?)endbfrange', stream, re.S):
        for lo, hi, rest in re.findall(rb'<([0-9A-Fa-f\s]+)>\s*<([0-9A-Fa-f\s]+)>\s*(<[0-9A-Fa-f\s]*>|\[[^\]]*\])', block):
            lo, hi = _hex(lo), _hex(hi)
            a, b, size = int.from_bytes(lo, 'big'), int.from_bytes(hi, 'big'), len(lo)
            if b < a or b - a > 65535:
                continue
            if rest.startswith(b'['):
                for i, dst in enumerate(re.findall(rb'<([0-9A-Fa-f\s]*)>', rest)):
                    if a + i <= b:
                        out[(a + i).to_bytes(size, 'big')] = _hex(dst).decode('utf-16-be', 'ignore')
            else:
                start = _hex(rest[1:-1])
                if not start:
                    continue
                base = int.from_bytes(start, 'big')
                for i in range(b - a + 1):
                    try:
                        out[(a + i).to_bytes(size, 'big')] = (base + i).to_bytes(len(start), 'big').decode('utf-16-be', 'ignore')
                    except OverflowError:
                        break
    return out, sorted({len(k) for k in out}, reverse=True) or [1]


def _fonts(objects):
    """{font resource name: cmap} from every /Font resource dictionary: names are per page, so when two pages use one
    name for different fonts the first one wins, which is right for most files."""
    cmaps = {}
    for number, (dictionary, _) in objects.items():
        m = re.search(rb'/ToUnicode\s+(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R', dictionary)
        if m and int(m[1]) in objects and objects[int(m[1])][1]:
            cmaps[number] = _cmap(objects[int(m[1])][1])
    names = {}
    for dictionary, _ in objects.values():
        for m in re.finditer(rb'/Font\s*(<<.*?>>|\d{1,10}\s{1,8}\d{1,5}\s{1,8}R)', dictionary, re.S):
            body = m[1]
            ref = re.fullmatch(rb'(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R', body)
            if ref:
                body = objects.get(int(ref[1]), (b'', None))[0]
            for name, number in _NAME_REF.findall(body):
                if int(number) in cmaps:
                    names.setdefault(name, cmaps[int(number)])
    return names


def _pages(objects, data):
    """The content streams in page order (the page tree from the catalog), else every stream that shows text."""
    root = re.search(rb'/Root\s+(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R', data[-4096:]) or re.search(rb'/Root\s+(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R', data)
    order, seen = [], set()

    def walk(number, depth=0):
        if number in seen or number not in objects or depth > 32 or len(order) > 2000:
            return
        seen.add(number)
        dictionary = objects[number][0]
        kids = re.search(rb'/Kids\s*\[([^\]]*)\]', dictionary)
        if kids and re.search(rb'/Type\s*/Pages\b', dictionary):
            for k in _REF.findall(kids[1]):
                walk(int(k), depth + 1)
            return
        contents = re.search(rb'/Contents\s*(\[[^\]]*\]|\d{1,10}\s{1,8}\d{1,5}\s{1,8}R)', dictionary)
        if contents:
            for c in _REF.findall(contents[1]):
                c = int(c)
                if c in objects and objects[c][1] is None:  # an array of streams kept in another object
                    order.extend(int(x) for x in _REF.findall(objects[c][0]))
                else:
                    order.append(c)

    if root and int(root[1]) in objects:
        pages = re.search(rb'/Pages\s+(\d{1,10})\s{1,8}\d{1,5}\s{1,8}R', objects[int(root[1])][0])
        if pages:
            walk(int(pages[1]))
    streams = [objects[n][1] for n in order if n in objects and objects[n][1]]
    if not streams:
        streams = [s for d, s in objects.values() if s and b'BT' in s and (b'Tj' in s or b'TJ' in s)]
    return streams


def _literal(s, i):
    """A (literal string) from s[i] == '(': (bytes, index after it)."""
    out, depth, i = bytearray(), 1, i + 1
    escapes = {ord('n'): 10, ord('r'): 13, ord('t'): 9, ord('b'): 8, ord('f'): 12}
    while i < len(s):
        c = s[i]
        if c == 0x5c:  # backslash
            i += 1
            if i >= len(s):
                break
            c = s[i]
            if c in escapes:
                out.append(escapes[c])
            elif 0x30 <= c <= 0x37:
                j = i
                while j < len(s) and j < i + 3 and 0x30 <= s[j] <= 0x37:
                    j += 1
                out.append(int(s[i:j], 8) & 0xff)
                i = j
                continue
            elif c in (10, 13):  # a line continuation
                if c == 13 and i + 1 < len(s) and s[i + 1] == 10:
                    i += 1
            else:
                out.append(c)
        elif c == 0x28:
            depth += 1
            out.append(c)
        elif c == 0x29:
            depth -= 1
            if depth == 0:
                return bytes(out), i + 1
            out.append(c)
        else:
            out.append(c)
        i += 1
    return bytes(out), i


def _tokens(s):
    """A content stream's operands and operators: ('s', bytes) strings, ('n', float), ('/', name), ('[',) and (']',), ('op', name)."""
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in _WS:
            i += 1
        elif c == 0x25:  # % comment
            while i < n and s[i] not in b'\r\n':
                i += 1
        elif c == 0x28:
            value, i = _literal(s, i)
            yield ('s', value)
        elif c == 0x3c:
            if s[i + 1:i + 2] == b'<':
                yield ('<<',)
                i += 2
            else:
                j = s.find(b'>', i)
                j = n if j < 0 else j
                yield ('s', _hex(s[i + 1:j]))
                i = j + 1
        elif c == 0x3e:
            i += 2 if s[i + 1:i + 2] == b'>' else 1
        elif c == 0x5b:
            yield ('[',)
            i += 1
        elif c == 0x5d:
            yield (']',)
            i += 1
        elif c == 0x2f:
            j = i + 1
            while j < n and s[j] not in _WS and s[j] not in _DELIM:
                j += 1
            yield ('/', s[i + 1:j])
            i = j
        else:
            j = i
            while j < n and s[j] not in _WS and s[j] not in _DELIM:
                j += 1
            word = s[i:j] or s[i:i + 1]
            i = j if j > i else i + 1
            try:
                yield ('n', float(word))
            except ValueError:
                yield ('op', word)


def _decode(raw, cmap):
    if not cmap:
        return raw.decode('latin-1')
    table, sizes = cmap
    out, i = [], 0
    while i < len(raw):
        for size in sizes:
            code = raw[i:i + size]
            if code in table:
                out.append(table[code])
                i += size
                break
        else:
            i += sizes[-1]  # a code without text (a ligature's other half, a symbol)
    return ''.join(out)


def _show(content, fonts, out, limit, budget):
    """Append the text a content stream shows to out; False once out holds `limit` characters or the work budget is spent."""
    cmap, operands, array, y = None, [], None, None
    font_size, shown = 10.0, 0  # shown: characters of the last string, to tell a word gap from kerning
    for tok in _tokens(content):
        budget.tokens -= 1
        if budget.tokens <= 0:
            return False
        kind = tok[0]
        if kind == '[':
            array = []
        elif kind == ']':
            operands.append(('a', array or []))
            array = None
        elif array is not None:
            array.append(tok)
        elif kind != 'op':
            operands.append(tok)
        else:
            op = tok[1]
            if op == b'Tf' and len(operands) >= 2 and operands[-2][0] == '/':
                cmap = fonts.get(operands[-2][1])
                if operands[-1][0] == 'n' and operands[-1][1] > 0:
                    font_size = operands[-1][1]
            elif op in (b'Tj', b"'", b'"') and operands and operands[-1][0] == 's':
                if op != b'Tj':
                    out.append('\n')
                text = _decode(operands[-1][1], cmap)
                out.append(text)
                shown = len(text)
            elif op == b'TJ' and operands and operands[-1][0] == 'a':
                shown = 0
                for part in operands[-1][1]:
                    if part[0] == 's':
                        text = _decode(part[1], cmap)
                        out.append(text)
                        shown += len(text)
                    elif part[0] == 'n' and part[1] < -180:  # a gap wider than a space: a space
                        out.append(' ')
                        shown = 0
            elif op in (b'Td', b'TD') and len(operands) >= 2 and operands[-1][0] == 'n' and operands[-2][0] == 'n':
                if abs(operands[-1][1]) > 0.01:
                    out.append('\n')
                elif operands[-2][1] > font_size * (0.5 * shown + 0.15):  # further than the last text's width: a gap
                    out.append(' ')
                shown = 0
            elif op == b'T*':
                out.append('\n')
            elif op == b'Tm' and len(operands) >= 6 and operands[-1][0] == 'n':
                out.append('\n' if y is not None and abs(operands[-1][1] - y) > 0.01 else ' ')
                y = operands[-1][1]
            elif op == b'ET':
                out.append(' ')
            operands = []
            if out.chars > limit:
                return False
    return True


def pdf_text(data, limit=TEXT_LIMIT * 2):
    """The text a PDF shows, in page order, or '' (see the module's note)."""
    if not data.startswith(b'%PDF-'):
        return ''
    tail = data[-4096:]
    if b'/Encrypt' in tail or re.search(rb'trailer\s*<<[^>]*/Encrypt', data):
        return ''
    budget = _Budget()
    objects = _objects(data, budget)
    if any(re.search(rb'/Type\s*/XRef\b', d) and b'/Encrypt' in d for d, _ in objects.values()):
        return ''
    fonts = _fonts(objects)
    out = _Out()
    for content in _pages(objects, data):
        going = _show(content, fonts, out, limit, budget)
        out.append('\n\n')
        if not going:
            break
    return ''.join(out)
