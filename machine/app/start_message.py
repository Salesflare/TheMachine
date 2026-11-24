"""One start's message, put together so it always fits what the runner takes (preparation.PROMPT_LIMIT).

A start that is too long is refused before the Gateway sees it, and so is every retry of it. So what always goes with a
start is set aside first (the instructions and the owner's ask in front; the note that the session carries on and the
files the owner added at the end), and the rest shares the room that is left. What is least needed goes first; a short
note names what went and the call that reads it.

`REFUSED`: how a start that can never succeed is named, by the runner (preparation-run.mjs, before any Gateway call) or
here. It ends at once as what it is, never as a wait for the AI."""

REFUSED = {'prompt_too_long', 'invalid_attachments', 'invalid_request'}

# What a to-do stuck on one says. The technical side is in its details.
REFUSED_REASON = {'invalid_attachments': 'I couldn’t start this with the files that came with it. Try other or smaller files, or ask for it without them.'}
REFUSED_ELSE = 'I couldn’t start this. Tap Try again, or change the request.'
REFUSED_DETAILS = {'prompt_too_long': 'The run’s start message was longer than one run takes, so it was never sent to the AI.',
                   'invalid_attachments': 'The images of the run’s start were not ones the runner takes, so it was never sent to the AI.',
                   'invalid_request': 'The run’s start was not one the runner takes, so it was never sent to the AI.'}

# Why a call to the Gateway is `unavailable`, for the service log: fixed codes (preparation-run.mjs), never a text.
UNAVAILABLE = {'offline', 'timeout', 'refused', 'unconfirmed', 'invalid_request', 'runner_failed', 'runner_timeout', 'other'}

RESERVE = 1000  # kept free under the limit: the note of what was left out

# In the order they go when there is no room: the higher, the sooner.
HOW_TO_READ, OWNER, NEWER, BRIEF, RECORDS, SKILLS, LEARN, TEAM, RELATED, HINT = range(10)

# Blocks a run can read itself: (what it was, the assistant_signals call that reads it)
READS = {'agent': ('Claude Code or Codex work on this to-do', 'status'),
         'newer': ('the newer messages in its conversations', 'events'),
         'follow_up': ('earlier follow-ups', 'events'),
         'brief': ('what its review found', 'status and events'),
         'records': ('what is known about its people and projects', 'graph'),
         'related': ('other messages that may bear on it', 'related')}


def unavailable(reason):
    return reason if reason in UNAVAILABLE else 'other'


def too_long(message, limit):
    return len(message or '') > limit


def trimmed(build, parts, order, room):
    """build(parts) within room: the parts named in `order` are emptied one by one, first named first, until it fits.
    Returns (text, the names emptied)."""
    parts, gone, text = dict(parts), [], build(parts)
    for name in order:
        if len(text) <= room:
            break
        if parts.get(name):
            parts[name] = ''
            gone.append(name)
            text = build(parts)
    return text, gone


class StartMessage:
    """The base (always), then blocks (by rank, when they don't all fit), then the tail (always)."""

    def __init__(self, limit, tail=''):
        self.limit, self.tail, self.base, self.blocks = limit, tail, '', []

    def base_room(self):
        return self.limit - RESERVE - len(self.tail)

    def add(self, name, text, rank, left=None):
        """One block, in the message's order. left(): called when it is left out."""
        if text:
            self.blocks.append((name, text, rank, left))

    def room(self):
        """What is left for a block that fits itself to the room."""
        return max(0, self.base_room() - len(self.base) - sum(len(text) for _, text, _, _ in self.blocks))

    def text(self):
        kept, left = list(self.blocks), []
        while kept and len(self.base) + sum(len(b[1]) for b in kept) > self.base_room():
            out = max(range(len(kept)), key=lambda i: (kept[i][2], i))
            left.append(kept.pop(out))
        for _, _, _, dropped in left:
            if dropped:
                dropped()
        return self.base + ''.join(b[1] for b in kept) + left_out([b[0] for b in left]) + self.tail


def left_out(names):
    """The note for a message that had no room for these blocks: what they were and how to read them. '' for none."""
    reads = [READS[n] for n in READS if n in names]
    if not reads:
        return ''
    return ('\n\nLeft out of this message for its size: ' + '; '.join(f'{what} (read with assistant_signals {call})' for what, call in reads)
            + '. Read what matters for this before you act on it.')
