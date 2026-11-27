# Work across threads eval

Does the weekly pass across threads ([opportunities.py](../../opportunities.py), config `opportunities`, off by default)
find work nobody asked for that the existing checks don't? For example, three customers report one bug and another
thread has the fix, or a family date clashes with a booking.

Made-up Machines: every person, message and address is made up, and every domain ends in `.example`. Each one is
replayed day by day for 60 days with the per-message review's to-dos and promises as the corpus gives them. Four weekly
passes run per Machine.
- The baseline runs the stalled-project check for real (`project_stall`: its candidates, prompt and parse).
- The other store runs the pass as it ships (`App.opportunity_run`), and later weeks see its to-dos.

One blind judge turn per Machine labels every proposal against the corpus key: planted opportunities, plus traps where
nothing should be proposed.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/opportunity-discovery/run.py --model <model> --judge <model> \
        [--set held-out] [--runs 2] [--cap 2000000] [--out results.json]

| Set | Machines | Opportunities | Traps |
| --- | --- | --- | --- |
| `development` | 2 | 10 | 12 |
| `held-out`, frozen before its first run | 5, two of them quiet | 18, 6 of them personal | 37 |
| `held-out/hx-6.json`, added and frozen before its first run | 1 | 6, 2 of them personal | 12, 3 of them a time already over or a group mail across companies |
| `held-out/hx-7.json` to `hx-9.json`, added and frozen before their first run | 3, one quiet | 12, 5 of them personal | 26, among them people who share a full name and one person on two addresses |

A separate agent wrote the held-out set without seeing the code. `FROZEN` holds its sha256 hashes, written before its
first run, and `run.py` refuses a held-out set whose files don't match.

## Bar

Set before the held-out set's first run. The pass turns on only when all of these hold:

| | Bar |
| --- | --- |
| proposals on a quiet Machine | 0 |
| trap or false proposals | 0 |
| proposals right (planted, or new and useful) | at least 85% |
| opportunities found | at least 50% |
| duplicates | at most 10% |
| proposals joining Work and Personal | 0 |
| proposals needing more than light edits | at most 1 in 10 |
| input tokens per weekly pass | at most 20k |

## Results

### Threads tied by the Graph

The pass now takes who is who from the Graph only (`--model gpt-6-luna`, low effort, `gpt-6.1-sol` judge, November
2026). The eval builds the Graph with the real code each day it replays. **It misses the bar on every set:**

| | Bar | hx-1 to hx-6, 2 runs | hx-7 to hx-9 (new, blind), 2 runs | First try's sets, 1 run |
| --- | --- | --- | --- | --- |
| proposals on a quiet Machine | 0 | **4** | 0 | **1** |
| trap or false proposals | 0 | **2** (one invoice number in two unrelated threads) | **2** (one date in two threads) | 0 |
| proposals right | at least 85% | 88% (23 of 26) | **83%** (10 of 12) | 100% (7 of 7) |
| opportunities found | at least 50% | **35%** (17 of 48) | **38%** (9 of 24) | **25%** (6 of 24) |
| proposals joining Work and Personal | 0 | 0 | 0 | 0 |
| needing more than light edits | at most 1 in 10 | 0 of 26 | 1 of 12 | 0 of 7 |
| input tokens per weekly pass | at most 20k | 14.0k at most | 13.0k at most | 12.2k at most |

Against the round before (people joined on addresses, companies and full-name mentions): hx-1 to hx-6 found 62% with
0 traps and 1 quiet-Machine proposal; the first try's sets 33%. Most opportunities join people of different
organizations, where the Graph has no tie, so they rest on what the messages say; the turn mostly links them one way
per pair (each customer to the fix), which code does not count as two signals.

### Before the Graph ties

`gpt-6-luna` at low effort for the pass, `gpt-6.1-sol` as the judge, November 2026. Held-out set with hx-6, two runs,
after the checks for a time already over and for one mail to several organizations:

| | Bar | Result |
| --- | --- | --- |
| proposals on a quiet Machine | 0 | **1, misses the bar** (hx-5, run 1: a useful check of a music order against the concert program, but on a Machine with nothing planted) |
| trap or false proposals | 0 | 0 |
| proposals right | at least 85% | 97% (31 of 32) |
| opportunities found | at least 50% | 62% (30 of 48), personal 10 of 16; hx-6 4 of 6 in each run |
| duplicates | at most 10% | 3% (1 of 32) |
| proposals joining Work and Personal | 0 | 0 |
| needing more than light edits | at most 1 in 10 | 1 in 32 |
| input tokens per weekly pass | at most 20k | 12.7k at most |

So this run does not clear the bar, on one proposal on a quiet Machine. The run before these checks (hx-1 to hx-5, two
runs) cleared every line: 0 on quiet Machines, 96% right (23 of 24), 64% found (23 of 36), 4% duplicates, 1 in 24
needing more than light edits, 12.5k tokens at most.

The two frozen sets of the first try (kept outside the repo), one run each: 8 of 8 proposals right, 0 traps, 0 on the
quiet Machines, but 8 of 24 opportunities found (33%). The first try found 30 of 48 there (62%), with a trap, a
duplicate and a proposal on a quiet Machine. Recall on those sets fell by about half: this pass trades recall for never
joining on one signal.
