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
| `held-out/hz-1.json` to `hz-3.json`, the same | 3, one quiet | 12, 4 of them personal | 26 |
| `held-out/hy-1.json` to `hy-3.json`, the same | 3, one quiet | 12, 4 of them personal | 26 |
| `held-out/hw-1.json` to `hw-3.json`, the same, for the ledger's final run | 3, one quiet | 12, 4 of them personal | 26 |

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

### The ledger (November 2026)

The pass as it ships now: a ledger of a few checked facts per thread, candidate groups found in code, two judging
turns per area that must agree, the date and "Not needed" checks and the quiet gate (`--model gpt-6-luna`, low effort,
`gpt-6.1-sol` judge). It was tuned on hx, hz and hy only; hw was written blind by a separate agent and hashed before
its one measured run. **It clears every line on hw:**

| | Bar | hw-1 to hw-3 (new, blind), 2 runs |
| --- | --- | --- |
| proposals on a quiet Machine | 0 | 0 |
| trap or false proposals | 0 | 0 |
| proposals right | at least 85% | 100% (17 of 17) |
| opportunities found | at least 50% | 70% (17 of 24) |
| duplicates | at most 10% | 0% |
| proposals joining Work and Personal | 0 | 0 |
| needing more than light edits | at most 1 in 10 | 0 of 17 |
| input tokens per weekly pass | at most 20k | 11.7k at most (the first pass reads every thread; later ones about 5k to 11k) |

On the way there, each change measured on the tuning sets:

| | hy-1 to hy-3, 2 runs (blind then) | hy-1 and hy-3 after the checks, 1 run |
| --- | --- | --- |
| one judging turn, value-ranked, at most four a week | 94% right, 62% found, but **1 trap** (a boat show already over) and **1 proposal on the quiet Machine**, each in one run of two | |
| plus two samples that must agree, the "Not needed" and past-date checks, the quiet gate | | 100% right (5 of 5), 4 of 6 found, 0 traps, 0 on the quiet Machine |

The quiet gate counts the threads in a week's candidate groups: under 12 on every quiet Machine in these sets (2 to 10),
10 to 50 on the others. A busy Machine's first weeks can fall under it too; then only value-3 work the Graph ties gets
through.

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
