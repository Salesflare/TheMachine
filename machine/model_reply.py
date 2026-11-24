"""A small background turn's reply that can't be read (cut off, not the JSON asked for) is no answer: never a verdict.

`read` reads the JSON in a reply and raises Unreadable when there is none. `ask` runs the turn, and once more when its
reply can't be read. `waiting` counts what stayed unreadable, so a job rests before it asks again and a broken model
never costs more than a few turns: each item is asked in TRIES passes a day at most, a job has PASSES_A_DAY such passes,
REST_SECONDS apart. Kept in memory: a restart starts the count over. Nothing here in the normal case: a reply that reads
costs one turn, as before."""
import json
import threading
import time

LAYER = 0  # a small turn's reply, read and asked once more (a leaf)
TRIES = 3
PASSES_A_DAY = 6
REST_SECONDS = 1800
DAY = 24 * 3600
AGAIN = '\n\nYour last reply to this could not be read (cut off, or not valid JSON). Answer again: only the complete JSON asked for above.'


class Unreadable(ValueError):
    """A reply that is not the answer asked for."""


def read(reply, kind=dict):
    """The JSON object (kind dict) or array (list) in a reply, in a code fence or with words around it: the first one,
    when the reply says it twice. Raises Unreadable when it has none or it is cut off."""
    text = str(reply or '')
    start = text.find('{' if kind is dict else '[')
    try:
        return json.JSONDecoder().raw_decode(text, start)[0] if start >= 0 else _none()
    except (ValueError, RecursionError):
        raise Unreadable('unreadable reply') from None


def _none():
    raise Unreadable('no reply')


def rows(reply, key):
    """The array of objects in a reply, each with `key`; an empty one is an answer too, one without any such object isn't."""
    found = read(reply, list)
    out = [x for x in found if isinstance(x, dict) and x.get(key)]
    if found and not out:
        raise Unreadable('not the rows asked for')
    return out


def ask(turn, prompt, parse):
    """parse(turn(prompt)); when parse raises Unreadable the turn runs once more, told so. A second one is raised."""
    try:
        return parse(turn(prompt))
    except Unreadable:
        return parse(turn(prompt + AGAIN))


class Waiting:
    """One job's unreadable passes of the last day, and the items on them."""

    def __init__(self):
        self.lock, self.passes, self.items = threading.Lock(), [], {}

    def missed(self, refs):
        """A pass over these items stayed unreadable."""
        at = time.time()
        with self.lock:
            self.passes = [t for t in self.passes if at - t < DAY] + [at]
            self.items = {r: kept for r, ts in self.items.items() if (kept := [t for t in ts if at - t < DAY])}
            for ref in refs:
                self.items.setdefault(ref, []).append(at)

    def tries(self, ref):
        return sum(time.time() - t < DAY for t in self.items.get(ref, ()))

    def today(self):
        return sum(time.time() - t < DAY for t in self.passes)

    def spent(self, ref):
        """Asked often enough today: left alone."""
        return self.tries(ref) >= TRIES

    def resting(self):
        """The last pass was unreadable a moment ago, or enough were today: no turn now."""
        return self.out() or bool(self.passes) and time.time() - self.passes[-1] < REST_SECONDS

    def out(self):
        """Enough unreadable passes today: no turn until tomorrow."""
        return self.today() >= PASSES_A_DAY


def waiting(app, job):
    """The app's Waiting of one job."""
    return app.__dict__.setdefault('_unreadable', {}).setdefault(job, Waiting())
