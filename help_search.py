"""Finds the help for a question in people's own words: the few passages of the help articles that say most about it
(help_chat.py). Words only, no model: it works on every Machine, offline, in milliseconds.

A long section is cut into passages at its paragraphs, so what its last line says is found, and goes in, as easily as its
first. A passage counts by its own words, its heading's most, and by how well its whole article fits: the title, the
summary and the keywords, which say in people's words what an article is about."""
from __future__ import annotations

import math
import re
import unicodedata

STOP = set('a an and are as at be by can do does for from has have how i if in is it its me my of on or so that the this '
           'to was what when where which who why will with you your '
           'about all into up go goes going now there am any been but cant could did didn doesn don dont each got had he her here him his im isn ive just let ll may '
           'might much must no not our please re really s she should some t than their them then there these they thing '
           'those too us ve very want wants we were won would yes'.split()
           # the same small words in the other languages of the app, so "hoe" or "comment" finds nothing on its own
           + 'de het een en van in op is ik je jij mijn hoe wat waar wie waarom met voor naar dat die dit er niet kan '
             'le la les un une des et du au aux en est je tu vous mon ma mes comment que quoi où qui pourquoi avec pour '
             'pas ne ce cette il elle der die das ein eine und von zu im ist ich du mein wie was wo wer warum mit für '
             'nicht kann el los las unos y del al es yo mi cómo qué dónde quién por con para no se lo il lo gli i una '
             'di da è io mio come cosa dove chi perché per non o os um uma e do da no na eu meu como onde quem por '
             'com não posso puedo posso kann '
             'kun kunt deze ook maar dan als wel uit om te aan zijn mij mijn hij ze heb heeft '
             'l d j m n c qu on nous sur dans mais ou puis peut plus son sa ses '
             'den dem des einen einem einer mich mir sich auch auf an bei aus oder wenn sind habe hat es '
             'me te su sus si pero más muy este esta puede hay '
             'mi ti si ci del della dei delle nel che sono ho ha può più '
             'meus minha seu sua se mas mais pode tem '
             'я мне мой мои моё как что где кто когда почему он она они это эти в на и с к по за из от до у не ли или '
             'для можно могу'.split())
WORD = re.compile(r'\w+')  # any language's words: "configuración", "Einstellungen"
IRREGULAR = {'wrote': 'write', 'written': 'write', 'writes': 'write', 'tone': 'tone', 'sent': 'send', 'got': 'get'}

# Words people use next to the ones the help uses, for the things any app has. A question finds the other words of its
# group too, for less than its own.
SAME = [line.split() for line in '''
delete remove erase wipe forget permanently
cancel end quit unsubscribe stop leave subscription
email mail message inbox
contact person people
company organization business firm account
customer client
colleague coworker teammate team boss manager employer
family wife husband partner spouse kids children home
phone mobile smartphone iphone ipad tablet
computer laptop desktop pc mac server
password login signin sign log passkey
price cost pay billing charge fee money monthly expensive
invoice receipt
notification notify alert push ping buzz
night evening weekend quiet
meeting appointment event call
picture photo image
undo revert restore reopen recover back
theme dark light color appearance
change edit modify correct fix adjust
wrong incorrect mistake
connect link add integrate
disconnect unlink remove
stopped broken fail error problem trouble
duplicate same twice merge combine
assign hand delegate give handoff
review check approve
speak talk voice dictate microphone mic
hotkey shortcut keyboard
private privacy secret confidential
old past earlier previous older history
website webpage site page
fake pretend lookalike phishing spoof impersonate
start begin setup install
move transfer migrate switch
bug crash broken report
later schedule tomorrow
task todo
search find look
import upload spreadsheet csv
export download backup
language translate
friend invite
automatically itself auto
chase remind reminder followup
'''.strip().splitlines()]

K, B = 1.2, 0.4
TITLE, HEADING, KEYWORDS, SUMMARY = 1, 2.5, 1, 1
ARTICLE = 0.6      # how much the whole article's fit adds to each of its passages
LEAD = 0.5         # what a section of the best article counts at least, next to its intro
ALSO, EARLIER = 0.75, 0.4 # what a word of the same group, or of the question before, counts next to the question's own
PASSAGE_CHARS = 600


def fold(w):
    """Without accents: people type "configuracion" too."""
    return ''.join(c for c in unicodedata.normalize('NFKD', w) if not unicodedata.combining(c)) if not w.isascii() else w


def stem(w):
    """A rough stem, so "writing", "wrote" and "write", or "personalize" and "personalized", find the same section."""
    w = IRREGULAR.get(w, w)
    if len(w) > 4 and w.endswith('s') and not w.endswith('ss'):
        w = w[:-1]
    for suffix in ('ation', 'ing', 'ed', 'ly'):
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            w = w[:-len(suffix)]
            if len(w) > 4 and w[-1] == w[-2] and w[-1] in 'bdgmnprt':
                w = w[:-1]  # stopped, shipping
            break
    if len(w) > 6 and w.endswith(('is', 'ise')):
        w = w[:w.rindex('is')] + 'iz'  # British -ise as -ize
    if len(w) > 3 and w.endswith(('e', 'y')):
        w = w[:-1] + ('i' if w[-1] == 'y' else '')
    return w[:-1] if len(w) > 4 and w.endswith('ie') else w


# Chinese and Japanese write without spaces, Korean glues particles to its words: those runs count by each pair of
# characters ("设置语言" is 设置, 置语, 语言), so a question finds the section with the same words in it.
CJK = re.compile(r'[぀-ヿ㐀-鿿가-힯]+')


def words(text, lang='en'):
    """The words of a text that mean something, as stems. In another language than English a long word also counts by
    how it starts ("Benachrichtigung" and "Benachrichtigungen")."""
    out = []
    for w in WORD.findall(str(text).lower()):
        if w in STOP:
            continue
        for part in re.split(f'({CJK.pattern})', w) if CJK.search(w) else [w]:
            if CJK.fullmatch(part):
                out += [part] if len(part) == 1 else [part[i:i + 2] for i in range(len(part) - 1)]
            elif part:
                out.append(stem(fold(part)))
                if lang != 'en' and len(part) > 5:
                    out.append(fold(part)[:5] + '~')
    return out


def _same():
    out = {}
    for group in SAME:
        stems = {stem(w) for w in group}
        for w in stems:
            out.setdefault(w, set()).update(stems - {w})
    return out


SAME_STEMS = _same()


def passages(text, limit=PASSAGE_CHARS):
    """A section's text in pieces of about limit characters, cut between its paragraphs and list items."""
    out = []
    for block in re.split(r'\n\s*\n|\n(?=- |\d+\. )', text.strip()):
        if out and len(out[-1]) + len(block) < limit:
            out[-1] += ('\n' if re.match(r'- |\d+\. ', block) else '\n\n') + block
        elif block.strip():
            out.append(block)
    return out or ['']


def bm25(tf, length, df, n):
    """What a word found tf times counts in a text of a length (1: the average), when df of n texts have it."""
    return math.log(1 + (n - df + 0.5) / (df + 0.5)) * tf * (K + 1) / (tf + K * (1 - B + B * length))


def tally(*fields):
    out = {}
    for weight, terms in fields:
        for w in terms:
            out[w] = out.get(w, 0) + weight
    return out


def df(tallies):
    out = {}
    for t in tallies:
        for w in t:
            out[w] = out.get(w, 0) + 1
    return out


class Help:
    """The help sections (help_chat.help_sections), searchable by passage."""

    def __init__(self, sections, lang='en'):
        self.docs, self.lang = sections, lang
        self.passages = []  # (section, its nth passage's text)
        self.articles = {}
        tallies = []
        of = lambda text: words(text, lang)
        for s in sections:
            art = self.articles.setdefault(s['slug'], [])
            art.append((TITLE if not s['anchor'] else 0, of(s['title'] + ' ' + s.get('en_title', ''))))
            art.append((KEYWORDS, of(s.get('keywords', ''))))
            art.append((HEADING / 2, of(s['heading'] + ' ' + s.get('en_heading', ''))))
            if not s['anchor']:
                art.append((SUMMARY, of(s['text'])))
            english = passages(s.get('english', '')) if s.get('english') else []
            pieces = passages(s['text'])
            for i, piece in enumerate(pieces):
                # a translated section's English passage sits where its translation does
                also = ' '.join(english[len(english) * i // len(pieces):max(len(english) * (i + 1) // len(pieces), len(english) * i // len(pieces) + 1)])
                body = of(piece) + of(also)
                self.passages.append((s, i, piece, len(body) + 1))
                tallies.append(tally((1, body), (HEADING, set(of(s['heading'] + ' ' + s.get('en_heading', '')))),
                                     (TITLE, set(of(s['title'] + ' ' + s.get('en_title', '')))),
                                     (KEYWORDS, set(of(s.get('keywords', ''))))))
        self.tallies = tallies
        self.terms = [list(t) for t in tallies]
        self.df = df(tallies)
        self.average = sum(p[3] for p in self.passages) / max(1, len(self.passages))
        self.article_tallies = {slug: tally(*fields) for slug, fields in self.articles.items()}
        self.article_df = df(self.article_tallies.values())

    def query(self, question, earlier=''):
        """For each word asked for, the words that answer to it: [[(word, what it counts), ...], ...], its own first."""
        out = {w: 1.0 for w in words(question, self.lang)}
        for w in words(earlier, self.lang):
            out.setdefault(w, EARLIER)
        return [[(w, weight), *((same, weight * ALSO) for same in sorted(SAME_STEMS.get(w, ())))] for w, weight in out.items()]

    def search(self, question, earlier=''):
        """[(score, section, n, passage)], best first."""
        asked = self.query(question, earlier)

        def fit(t, length, df, n):  # each word asked for counts once, by its best match
            return sum(max((weight * bm25(t[w], length, df[w], n) for w, weight in same if w in t), default=0) for same in asked)
        whole = {slug: fit(t, 1, self.article_df, len(self.article_tallies)) for slug, t in self.article_tallies.items()}
        out = []
        for (section, i, piece, length), t in zip(self.passages, self.tallies):
            score = fit(t, length / self.average, self.df, len(self.passages)) + ARTICLE * whole[section['slug']]
            if score:
                out.append((score, section, i, piece))
        out.sort(key=lambda x: -x[0])
        if out and not out[0][1]['anchor']:  # an article that matches as a whole brings its sections: its intro only says what it is about
            best, lead = out[0][0], out[0][1]['slug']
            out = [(max(score, best * LEAD), section, i, piece) if section['slug'] == lead else (score, section, i, piece) for score, section, i, piece in out]
            out.sort(key=lambda x: -x[0])
        return out
