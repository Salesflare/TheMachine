# Meeting briefings eval

Made-up meetings whose guests were in an earlier meeting with notes, first meetings and meetings that repeat: what a
briefing tells of them, and that it tells nothing that is wrong or settled since. `run.py` stores the meetings, notes, mail, promises and done to-dos the way their
source does, builds the real briefing (`meeting_prep.py`, `earlier_notes.py`) with a model, and has the model check it
against the statements it should and must not hold, and for statements the case doesn't support. No to-do is made and
nothing is sent. Every person, company and address is made up. Languages: English, Dutch, French, German, Spanish,
Portuguese, Japanese.

| Set | Cases | What it is for |
| --- | --- | --- |
| development | 29 | what the prompt and limits were tuned on |
| held-out | 32 | the same kinds of case, never tuned on |

The kinds: plain notes, long notes, a point settled later (by mail, in passing, by a promise or a to-do), newer notes or
a mail that changes older ones, only an agenda, a transcript, notes the meeting app mailed, a series, another address of
the same person, a namesake, a large meeting, personal notes before a work meeting, a colleague's step, an instruction
written in the notes, and no notes at all.

First meetings (`f-`): only the booking mail or nothing yet, and what the web has (`web`: the organization's home page and
the results of a search on the person). Meetings that repeat (`r-`): what came since the one before, and the series' last
briefing (`before`). In a `quiet` case there is nothing to say, so no briefing is right. A case that isn't quiet needs one.

Chats (`c-chat`, `h-chat`): what was said in many short messages, alone or next to mail.

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

First meetings and meetings that repeat (two runs of each set, 2026-11-24; before: no briefing for a meeting that
repeats, no page of their own site read, no search on a first name):

| | Held-out, before | Held-out, now | Development, before | Development, now |
| --- | --- | --- | --- | --- |
| facts recalled | 4 of 36 | 30 of 36 | 0 of 26 | 25 of 26 |
| wrong or stale | 0 of 10 | 0 of 10 | 0 of 14 | 0 of 14 |
| statements not supported | 0 | 0 | 0 | 0 |
| briefings with nothing to say | 0 of 8 | 0 of 8 | 0 of 8 | 0 of 8 |
| briefings made | 2 of 24 | 16 of 24 | 0 of 18 | 10 of 18 |
| turn tokens in, average (largest) | 982 (1,077) | 1,367 (1,679) | 964 (967) | 1,357 (1,707) |

Three lines of the instructions were changed once after a first run of all of them (held-out 31 of 36 then): no word on what isn't
known, no forced link to the owner's organization, and what was agreed last time is kept. The other 36 cases stayed as they were (recalled 87 of 95, one run).
What a first meeting means for the owner is still sometimes a stretch.

Chats (the 4 cases, two runs each, 2026-11-24; before: each chat message counted as one. The other cases' turns are the same text):

| | Held-out, before | Held-out, now | Development, before | Development, now |
| --- | --- | --- | --- | --- |
| facts recalled | 0 of 16 | 16 of 16 | 0 of 16 | 16 of 16 |
| wrong or stale | 0 of 6 | 0 of 6 | 2 of 4 | 0 of 4 |
| statements not supported | 5 | 0 | 4 | 0 |
| briefings made | 2 of 4 | 4 of 4 | 2 of 4 | 4 of 4 |
| turn tokens in, average (largest) | 1,083 (1,089) | 1,191 (1,254) | 1,081 (1,088) | 1,152 (1,200) |

Where this is weak: the cases were written with the change, and one model wrote and checked the briefings. Only two cases
have long notes, so the limit rests on little. "Wrong or stale" counts only the statements a case names. One held-out
case gets no briefing in both runs (about a lease, probably taken for the owner's own life). Notes the model provider's
own filter refuses give no briefing.
