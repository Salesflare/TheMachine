# Stay in touch eval

Made-up friends the owner picked for the Stay in touch template, each over 41 days. `run.py` stores their chats, facts
and page summaries the way their source does, each on its own day, runs the real routine every morning with a model,
builds the Graph from them, and has a model judge each nudge against what really happened. Nothing is sent. Every person and address is made up.

| Set | Cases | What it is for |
| --- | --- | --- |
| development | 11 | written with the change |
| held-out | 19 | frozen before the first run, never tuned on |
| fresh | 8 | written after the first held-out run, frozen before the one change it led to |
| area-fresh | 14 | Work next to a friend's life (Work promises and facts, a work matter on WhatsApp, the owner writing more from the work mailbox), written by a separate agent and frozen before the first run |
| area-fresh-2 | 10 | work talk inside the WhatsApp chat next to life news, written and frozen after the first area run |

The kinds: news with a date ahead (a move, a new job, an exam, a trip, a gig), from the page's summary or a saved fact;
news put off, called off or changed (summary stale or rewritten); an active chat; a check-in the owner already sent; a
passing remark; a line from a Work account or a connected AI; a message never answered; news with a date past the 41 days.

A case can also have `promises` (on one of its messages, with the review's `area`), `work_facts` (told on a Work to-do
about a work mail) and `owner_work_mails` (the owner writing to them one to one from the work mailbox). A leak is a
nudge about a work matter (a second judge question) or one drafted on the work mailbox.

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

Work kept out of a Personal check-in (2026-11-27, same model): facts and promises go through `person_summary.sides_of`,
the draft goes in a conversation off the Work accounts when there is one, and one prompt line says a work matter is
never a reason, also in a chat. That line was the one improvement round, after the first run still had 2 leaks of 14,
both work talk inside the WhatsApp chat; area-fresh-2 was written and frozen after it.

| | Held-out, before | now | Fresh, before | now | Area-fresh, before | now | Area-fresh-2, before | now |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| useful, on time | 11 of 11 | 11 of 11 | 4 of 4 | 4 of 4 | 1 of 8 | 5 of 8 | 0 of 7 | 2 of 7 |
| early / off / missed | 0 | 0 | 0 | 0 | 5 / 2 / 0 | 2 / 1 / 0 | 5 / 2 / 0 | 1 / 2 / 2 |
| extra interruptions | 1 of 8 | 1 of 8 | 0 of 4 | 0 of 4 | 6 of 6 | 0 of 6 | 2 of 3 | 0 of 3 |
| leaks | 0 | 0 | 0 | 0 | 12 | 0 | 7 | 0 |
| wrong | 0 | 0 | 0 | 0 | 5 | 2 | 4 | 3 |
| model calls (tokens in) | 30 (12,694) | 30 (14,104) | 16 (6,710) | 16 (7,462) | 22 (9,625) | 18 (8,743) | 11 (5,026) | 15 (7,502) |

A leak is a nudge about a work matter or drafted on the work mailbox. The two missed in area-fresh-2 are life news next
to work talk that main didn't get right either (it nudged on the work matter on day 0). The off and wrong left on both
sides are a personal promise or question nudged early or read as out of time; they are Personal, not leaks. The prompt
line costs about 47 input tokens a call.
