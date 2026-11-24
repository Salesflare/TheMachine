# Meeting briefings eval

Made-up meetings whose guests were in an earlier meeting with notes: what a briefing tells of them, and that it tells
nothing that is wrong or settled since. `run.py` stores the meetings, notes, mail, promises and done to-dos the way their
source does, builds the real briefing (`meeting_prep.py`, `earlier_notes.py`) with a model, and has the model check it
against the statements it should and must not hold, and for statements the case doesn't support. No to-do is made and
nothing is sent. Every person, company and address is made up. Languages: English, Dutch, French, German, Spanish,
Portuguese, Japanese.

| Set | Cases | What it is for |
| --- | --- | --- |
| development | 18 | what the prompt and limits were tuned on |
| held-out | 18 | the same kinds of case, never tuned on |

The kinds: plain notes, long notes, a point settled later (by mail, in passing, by a promise or a to-do), newer notes or
a mail that changes older ones, only an agenda, a transcript, notes the meeting app mailed, a series, another address of
the same person, a namesake, a large meeting, personal notes before a work meeting, a colleague's step, an instruction
written in the notes, and no notes at all.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/meeting-briefings/run.py --model <model> --runs 2 --set held-out
    ... --root <another checkout>    # the same cases on that code's briefings
    ... --chars 5000                 # another limit for the notes in a turn
    ... --history                    # what came before (meetings, notes, mail) is history

The environment is that of `evals/family-questions/run.py`.

On gpt-6.1-sol, effort low (2026-11-24). Before: no notes read.

| | Held-out, before | Held-out, now | Development, before | Development, now |
| --- | --- | --- | --- | --- |
| facts recalled | 14 of 94 | 83 of 94 | 7 of 48 | 46 of 48 |
| wrong or stale | 0 of 60 | 0 of 60 | 0 of 28 | 0 of 28 |
| statements not supported | 1 | 3 | 0 | 1 |
| briefings made | 17 of 36 | 34 of 36 | 6 of 18 | 17 of 18 |
| turn tokens in, average (largest) | 965 (1,081) | 1,631 (2,414) | 975 (1,075) | 1,635 (2,375) |

Held-out ran twice (36 briefings), development once. Two cases (`promise-kept`, `h-todo-done`) are made another way since, through
the store's own functions: the facts recalled in them stayed the same over two runs.

| Notes in a turn (development) | 2,500 characters | 5,000 | 10,000 | 20,000 |
| --- | --- | --- | --- | --- |
| facts recalled of 48 | 45 | 45 | 46 | 47 |
| tokens in, largest | 2,375 | 2,375 | 2,375 | 3,307 |

With `--history` (one run of each set, 2026-11-24; before: briefings read signals only):

| | Held-out, before | Held-out, now | Development, before | Development, now |
| --- | --- | --- | --- | --- |
| facts recalled | 2 of 47 | 41 of 47 | 2 of 48 | 46 of 48 |
| wrong or stale | 0 of 30 | 0 of 30 | 0 of 28 | 0 of 28 |
| statements not supported | 0 | 1 | 0 | 3 |
| briefings made | 1 of 18 | 17 of 18 | 1 of 18 | 17 of 18 |
| turn tokens in, average (largest) | 1,488 (1,488) | 1,631 (2,414) | 1,552 (1,552) | 1,638 (2,375) |

Where this is weak: the cases were written with the change, and one model wrote and checked the briefings. Only two cases
have long notes, so the limit rests on little. "Wrong or stale" counts only the statements a case names. One held-out
case gets no briefing in both runs (about a lease, probably taken for the owner's own life). Notes the model provider's
own filter refuses give no briefing.
