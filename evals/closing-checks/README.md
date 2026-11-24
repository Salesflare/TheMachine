# Closing checks eval

Made-up cases for the two checks that close something by themselves: an open to-do (`handled_check_text`) and a due
promise (`promise_check_text`). `run.py` stores the messages the way their source does, builds the real pages and asks
a model. Nothing is closed or sent. Every person, company and address is made up.

| Set | Cases | What it tests |
| --- | --- | --- |
| late-open | 12 | the part that leaves it open comes after the first 400 characters, for some after a start that sounds done |
| late-done | 4 | the part that does it comes after the first 400 characters |
| partial | 5 | a reply that delivers only part |
| no-file | 6 | it says something is attached, and no file came with it |
| file-only | 5 | the file delivers it, the message says next to nothing |
| cut | 3 | longer than what is shown: settled by its end, or by nothing shown |
| files-unknown | 5 | a source that doesn't record files: the words decide |
| plain-done, plain-open | 11 | short messages, as before |

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/closing-checks/run.py --model <model> --runs 4
    ... --root <another checkout>    # the same cases on that code's pages

The environment is that of `evals/family-questions/run.py`. A wrong close ("closed wrongly") is worse than one left
open: the owner never sees it again.

On gpt-6.1-sol, effort low, four runs of all 51 cases (2026-11-24). Before: the first 400 characters of title and body,
no files.

| Set | Before | Now |
| --- | --- | --- |
| late-open | 36 of 48 | 48 of 48 |
| late-done | 4 of 16 | 16 of 16 |
| partial | 20 of 20 | 20 of 20 |
| no-file | 4 of 24 | 24 of 24 |
| file-only | 4 of 20 | 20 of 20 |
| cut | 8 of 12 | 12 of 12 |
| files-unknown | 16 of 20 | 16 of 20 |
| plain | 44 of 44 | 44 of 44 |
| closed wrongly | 32 | 0 |
| left open though done | 36 | 4 |

The cases were written with this change, so they say what it fixes, not how often it happens. The one case still wrong
is `uf1`: "Here's the roadmap file, as promised" on Slack, which doesn't record files, is left open.
