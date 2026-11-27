# Catch-all projects eval

Does the guard in `project_spread.py` keep a review from piling separate people into one project, and leave genuine
projects whole? Each case is made-up mail about one project, replayed a day at a time into a fresh database: each day's
messages are labeled onto the project the way a review would, before the change (`graph.label`) and after it
(`project_spread.label`). Plain code, no model, so no tokens and no runs to average.

    python3 evals/project-catchalls/run.py

Cases (`cases.json`, frozen before the first run, sha1 32a12eb4…): `catch-all` outreach to many separate
organizations (tester invites, buyer pitches, candidates), a few of whom answer; `genuine` projects with several
companies (a deal with a partner and a customer, a party, kitchen quotes, a conference); `small` (an office lease).

Counted: **catch-alls formed** (6 or more separate groups on one project), **separate counterparts absorbed** (groups
on a catch-all case), **genuine projects wrongly split** (a genuine project with an answered thread kept off, or flagged
for a split: must be 0), **genuine conversations kept off** (must be 0), **genuine unanswered messages kept off**.

## Results (2026-11-27)

| | catch-alls formed | counterparts absorbed | flagged for a split | genuine wrongly split | genuine conversations off | unanswered off | time |
|---|---|---|---|---|---|---|---|
| before | 3 | 57 | 3 | 0 | 0 | 0 | 6 ms |
| after | 2 | 20 | 0 | 0 | 0 | 2 | 44 ms |

Counterparts absorbed drop by 65%. The two catch-alls left hold only people who answered: same-kind outreach that got
replies is told apart by meaning, which the review prompt now asks for, not by this guard. The two unanswered messages
kept off are party invites nobody answered; a reply brings their thread back.

One improvement round: the first rule flagged a project half one-way; a genuine project (a party, most guests never
replying) was flagged, so a catch-all now needs two thirds one-way, or 25 groups.
