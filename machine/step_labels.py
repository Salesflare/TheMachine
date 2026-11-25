"""What a step's button label may hold, and what a label is at save (next_actions.validate). It goes out in Telegram
texts too, so it never holds what a chat app makes a mention or a tag of. Imports nothing of The Machine's."""
import re

LAYER = 0  # what a label may hold (a leaf)

WORDS = r"[^\W\d_](?:[^\W_]|[ ,’'&€$£\-/])+"  # a name's accents, an amount too
MAX = 28
TAGS = re.compile(r'[@#]|\$(?=[^\W\d_])')  # @sam, #offers, $USD
GENERIC = ('done', 'mark done', 'dismiss', 'reject', 'snooze', 'change', 'prepare', 'continue', 'do it', 'yes')


def label_text(value):
    """A label without what a chat app makes a mention or a tag of."""
    return re.sub(' {2,}', ' ', TAGS.sub('', value)).strip(' ') if TAGS.search(value) else value


def handoff_label(to_name):
    """A handoff's button: the first name of who it goes to, when that fits."""
    name = label_text(' '.join(['Hand off to', *str(to_name or '').split()[:1]]))
    return name if to_name and len(name) <= MAX and re.fullmatch(WORDS, name) else 'Hand off'


def usable(label):
    """A specific label in words, not a generic or owner-status button. Its length is checked apart (MAX)."""
    return isinstance(label, str) and bool(re.fullmatch(WORDS, label)) and label.lower() not in GENERIC
