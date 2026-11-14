"""How long each part of a Graph build took (graph._build_in): its summary's passes_ms, and the Graph worker's log
line for a slow build (machine/app/graph_actions.py slow_build_line)."""

import time


class Laps:
    """Milliseconds per part of a build, in the order they ran: each call ends the part since the one before and
    passes on what it is given, so `found = lap('joins', join_identities(...))` times that pass. A clock read per part,
    nothing written."""

    def __init__(self):
        self.ms, self.at = {}, time.perf_counter()

    def __call__(self, name, result=None):
        at = time.perf_counter()
        self.ms[name] = round((at - self.at) * 1000, 1)
        self.at = at
        return result
