"""What a draft's marks say about it, in any language: a placeholder left in, a message that ends as a sentence does, a
closing with its name (next_actions.py). Read from where the marks stand and from Unicode, never from a language's words.
A wrong refusal costs the run a turn, so a bracket with an everyday use where it stands is left alone. Imports nothing of The Machine's."""
import re
import unicodedata

LAYER = 0  # what a draft's marks say (a leaf)

# Not the draft's own words: code, a quoted line, a quotation on one line (a template in quotes, "he [Kim] said", [sic])
CODE = re.compile(r'(?ms)^[ \t]*(?P<fence>```|~~~).*?(?:^[ \t]*(?P=fence)|\Z)|(?<!`)(?P<tick>`{1,2})(?!`)[^\n]+?(?<!`)(?P=tick)(?!`)')
QUOTED_LINE = re.compile(r'(?m)^[ \t]*>.*$')
_QUOTES = '“”„«»‹›「」『』"'
QUOTATION = re.compile(f'[{_QUOTES}][^\\n{_QUOTES}]{{1,300}}[{_QUOTES}]')

BRACKET = re.compile(r'[\[［]([^\[\]［］\n]{1,80})[\]］]')
# {{field}}; TODO: as a note to oneself (never the word in a sentence, and not "todo"); XXX in front of a word or at a
# currency sign (a row of x's that closes a line is kisses)
OTHER = re.compile(r'\{\{[^}]*\}\}|(?i:<(?:name|link|date)>)|\bTODO(?=:|\()|(?<!\w)XXX(?=[ \t]+[^\W\d_]{2})|(?<=[€$£¥])[ \t]?XXX\b|\bXXX(?=[ \t]?[€$£¥])|(?i:lorem ipsum)')
REFERENCE = re.compile(r'(?m)^[ ]{0,3}\[[^\]\n]+\]:')  # [text][label] needs its [label]: line
LINE_START = re.compile(r'[ \t]*(?:(?:[-*+•–]|\d{1,3}[.)])[ \t]+)?[*_~]*')
SUBJECT_TAGS = re.compile(r'^(?:\s*[^\W\d_]{1,4}\s?[:：]|\s*[\[［][^\]］]*[\]］])+(?=\s*[^\s\[［])|(?<=\S)(?:\s*[\[［][^\]］]*[\]］])+\s*$')


def placeholder(body, subject=''):
    """The placeholder left in a draft, as it stands there, or None. A subject may start or end with tags: [list] Topic."""
    return _placeholder(SUBJECT_TAGS.sub('', subject or '')) or _placeholder(body or '')


def _placeholder(text):
    for own in (CODE, QUOTED_LINE, QUOTATION):
        text = own.sub(lambda m: re.sub(r'[^\n]', ' ', m[0]), text)
    found = [m for m in BRACKET.finditer(text) if _left_open(text, m)]
    found += OTHER.finditer(text)
    return min(found, key=lambda m: m.start())[0] if found else None


def _fill_in(words):
    """Words to be replaced: letters and what stands between them, so no number, address, path, flag or code."""
    if words.strip() in ('...', '…'):
        return True
    return (words.strip()[:1].isalpha() and not re.search(r"[^\w \t'’ʼ\-–/,.…?·]|[\d_]|\.\S", _letters(words)) and words.strip().casefold() != 'sic'
            and sum(c.isalpha() for c in words) >= 2)


def _letters(words):
    """With its combining marks (not \\w to re) as letters."""
    return ''.join('a' if unicodedata.category(c)[0] == 'M' else c for c in words)


def _left_open(text, m):
    """A bracket holding words where the draft's own words go: no link, footnote, index, checkbox or tag before a line."""
    if not _fill_in(m[1]):
        return False
    before, after = text[:m.start()], text[m.end():]
    if re.search(r'[A-Za-z0-9_)!\\^]\Z', before) or re.match(r'\(|<http', after):
        return False  # an index, an escaped bracket, a link
    if REFERENCE.search(text) and (after[:1] == '[' or before[-1:] == ']'):
        return False
    line, rest = before[before.rfind('\n') + 1:], after.split('\n', 1)[0].lstrip('*_~')
    start = LINE_START.fullmatch(line)
    if re.match(r'[:：]', rest) and (start or (rest[1:].strip() and len(m[1].split()) == 1)):
        return False  # a label, a speaker, a reference's own line
    if start and re.match(r'[ \t]+[^\W_]', rest) and (len(m[1].split()) == 1 or m[1].isupper()):
        return False  # a tag: [Optional] Bring a jacket
    if not rest.strip() and len(line.split()) >= 4 and line.rstrip()[-1:] not in (',', '，', '、', '،'):
        return False  # a note on the line: What the paper wrote about it [Dutch]
    return True


# The marks that end a sentence, in every script in everyday use (Unicode's Sentence_Terminal), and a drawn-out ～
ENDS = frozenset('.!?…‥‼‽⁇⁈⁉。｡．！？～〜؟۔।॥։՜՞።፧፨။၊៕។᠃᠉')
UNMARKED = ('THAI ', 'LAO ', 'TIBETAN ')  # written without a mark at the end of a sentence
EMOTICON = re.compile(r"[:;=][-'’]?[)(DPp3]$")
LINK_END = re.compile(r'https?://\S+$')


def ends_sentence(text):
    """A message that ends as a sentence does: its script's closing mark (maybe inside a closing quote, bracket or bold),
    an emoji, or a link."""
    text = text.rstrip()
    if LINK_END.search(text) or EMOTICON.search(text):
        return True
    while text and (text[-1] in '"*_~’\'' or unicodedata.category(text[-1]) in ('Pe', 'Pf', 'Pi', 'Cf', 'Mn', 'Me', 'Zs')):
        if text[-1] == '\u20e3':  # a keycap
            return True
        text = text[:-1]
    if not text:
        return False
    last = text[-1]
    if last in ENDS or unicodedata.category(last) in ('So', 'Sk'):
        return True
    if last == ';':  # Greek's question mark, as it is mostly typed
        return any(unicodedata.name(c, '').startswith('GREEK ') for c in text[-40:])
    return unicodedata.name(last, '').startswith(UNMARKED)


NAME_WORD = re.compile(r"[^\W\d_](?:[^\W\d_]|[.'’ʼ·-])*")


def is_name(line):
    """A signature's name: up to five words, capitalized where the script has capitals (small words between them, as in
    Jean de Wit), or a short name in a script without."""
    words = _letters(line.strip()).split()
    if not 1 <= len(words) <= 5 or not all(NAME_WORD.fullmatch(w) for w in words):
        return False
    first = line.split()
    if not all(w[0].isupper() for w in (first[0], first[-1])):
        wide = any(unicodedata.east_asian_width(c) == 'W' for c in line)  # no spaces between words there
        return not any(c.isupper() or c.islower() for c in line) and len(line.strip()) <= (6 if wide else 20) and len(words) <= 3
    middle = [w for w in first[1:-1] if not w[0].isupper()]
    return len(middle) <= 2 and all(len(w) <= 5 for w in middle)


def closing_spaced(body):
    """Owner standard: a blank line between the closing ("Regards,") and the name."""
    lines = body.rstrip().split('\n')
    if len(lines) < 2:
        return '\n'.join(lines)
    closing, name = lines[-2].strip(), lines[-1].strip()
    if (len(closing) <= 40 and closing.endswith((',', '，', '、', '،')) and is_name(name)
            # A script without capitals can't tell a name from words: the closing starts its own paragraph there
            and (name[0].isupper() or len(lines) < 3 or not lines[-3].strip())):
        lines.insert(-1, '')
    return '\n'.join(lines)
