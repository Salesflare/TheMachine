# Stay in touch eval

Made-up friends the owner picked for the Stay in touch template, each over 41 days. `run.py` stores their chats, facts
and page summaries the way their source does, each on its own day, runs the real routine every morning with a model,
builds the Graph from them, and has a model judge each nudge against what really happened. Nothing is sent. Every person and address is made up.

| Set | Cases | What it is for |
| --- | --- | --- |
| development | 11 | written with the change |
| held-out | 19 | frozen before the first run, never tuned on |
| fresh | 8 | written after the first held-out run, frozen before the one change it led to |

The kinds: news with a date ahead (a move, a new job, an exam, a trip, a gig), from the page's summary or a saved fact;
news put off, called off or changed (summary stale or rewritten); an active chat; a check-in the owner already sent; a
passing remark; a line from a Work account or a connected AI; a message never answered; news with a date past the 41 days.

A `nudge` case is right when its first nudge comes from the day before to 10 days after the date (`window`) and is about
it; earlier is early, later is late, none is missed. Any nudge in a `quiet` case is an extra interruption.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/stay-in-touch/run.py --model <model> --set held-out
    ... --root <another checkout>    # the same cases on that code

The environment is that of `evals/family-questions/run.py`.

On gpt-6.1-sol, effort low, one run (2026-11-27). Before: the summary not read, the same material not read again for
30 days whatever its date, and a message to a Work account read as unanswered.

| | Held-out, before | Held-out, now | Fresh, before | Fresh, now | Development, before | Development, now |
| --- | --- | --- | --- | --- | --- | --- |
| useful, on time | 2 of 11 | 11 of 11 | 0 of 4 | 4 of 4 | 1 of 4 | 4 of 4 |
| late | 2 | 0 | 1 | 0 | 1 | 0 |
| missed | 7 | 0 | 3 | 0 | 2 | 0 |
| extra interruptions | 2 of 8 | 1 of 8 | 0 of 4 | 0 of 4 | 2 of 7 | 1 of 7 |
| wrong or stale | 0 | 0 | 0 | 0 | 1 | 0 |
| model calls | 9 | 30 | 2 | 16 | 6 | 17 |
| tokens in (out) | 2,873 (517) | 12,694 (919) | 610 (86) | 6,710 (445) | 1,921 (312) | 7,206 (520) |

The first held-out run had one more extra interruption (a follow-up on a purchase that fell through) and two guessed
genders; one line of the instructions changed after it (called off or gone wrong is no reason, no guessed gender). The
extra interruption left on both sides: after the owner's own check-in, the friend's short reply was never answered,
and that counts as something to say. The one gone: a work mail read as a Personal unanswered message.

Where this is weak: one run each, the cases were written with the change, and one model wrote and judged the nudges.
Summaries are stored as given, not written by the summary pass. A Not needed back-off and the weekly cap aren't in it.
