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

`gpt-6-luna` at low effort for the pass, `gpt-6.1-sol` as the judge, November 2026. Held-out set, two runs:

| | Bar | Result |
| --- | --- | --- |
| proposals on a quiet Machine | 0 | 0 |
| trap or false proposals | 0 | 0 |
| proposals right | at least 85% | 96% (23 of 24) |
| opportunities found | at least 50% | 64% (23 of 36), personal 6 of 12 |
| duplicates | at most 10% | 4% (1 of 24) |
| proposals joining Work and Personal | 0 | 0 |
| needing more than light edits | at most 1 in 10 | 1 in 24 |
| input tokens per weekly pass | at most 20k | 12.5k at most |

The two frozen sets of the first try (kept outside the repo), one run each: 8 of 8 proposals right, 0 traps, 0 on the
quiet Machines, but 8 of 24 opportunities found (33%). The first try found more there (30 of 48) with a trap, a
duplicate and a proposal on a quiet Machine: this pass trades recall for never joining on one signal.
