# Result checks eval

When a waiting to-do's result seems to have come (its page shows the words, a message shows it), does the check close
it only when it is what was agreed? `machine/store/result_checks.py` keeps the verdict; this eval runs the same turn
(`machine/prompts/result_check.py`) on made-up cases and keeps it the same way: a close only on "matches" with nothing
owed in return, the case's open promises first.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/result-checks/run.py --model <model> --runs 3 --old
    ... --main     # main's rule: the words found close it, no turn

Sets in `cases.json`: `matching`, `mismatch-price`, `mismatch-description`, `mismatch-link`, `mismatch-name`, `early`
(published before the owner's OK), `partial`, `unrelated` (the words on a page about something else), and exchanges:
`reciprocal-theirs-first` (the owner's half still owed), `reciprocal-both-done`, `reciprocal-owner-first`,
`reciprocal-one-way`. `--old` adds the done-checks eval's listing and status cases, live, as matching cases.

`cases-fresh.json` and `cases-fresh2.json` (held out, written apart from the code) carry each message's date, sender and
whether the owner wrote it, as `result_checks.thread` gives them: `approval-by-other` and `skipped-approval` (an OK only
from the other side, or none), `author-swap` (the owner changed the value the other side proposed), `misleading` (it
says "as agreed" but isn't), `partial`, `injection` (text aimed at the checker, fake answers, `<<<`/`>>>` to leave its
quotes), `owed` and `matching`. `cases.json`'s lines are read the same way ("The owner sent: ", "From X: ").

    ... --cases cases.json cases-fresh.json cases-fresh2.json

Counted: **matching closed** (of the cases that want a close, must be 80% or more), **wrong closes** (a close on any
other case, must be 0), **closes while owed** (must be 0), **differs** and how many name a real difference (the case's
tokens in it, must be all), tokens per check.

## Results (2026-11-27, gpt-6.1-sol, effort low, 3 runs)

`cases.json` was frozen before the first run (sha256 3e35a692…).

| | turns | matching closed | wrong closes | closes while owed | differs (real) | tokens in / out |
|---|---|---|---|---|---|---|
| main (words close it) | 52 | 26 of 26 | 26 | 4 | 0 | 0 |
| change, first round | 156 | 63 of 78 (81%) | 0 | 0 | 36 (36) | 590 / 52 |
| change, final | 156 | 63 of 78 (81%) | 0 | 0 | 36 (36) | 621 / 46 |

The improvement round changed only how the lines read: the first round's "checked" clauses were whole sentences
("Toolbench lists Quillnote with…") and some differences said "the owner sent". The final prompt asks for at most 8
words starting with "with" and "you". Misses come back for a look, never closed: a guest post page that shows the title
and byline but not the text (2 cases), status pages whose thread doesn't say which incident is the owner's (2), and a
thread that never names the owner's product (1).

## Results: who wrote what, and quotes checked (2026-11-27, gpt-6.1-sol, effort low, 3 runs)

Main's thread had no sender or date on collected messages, only "The owner sent: " on what the Machine sent; main below
gets that (generously: every own message as one the Machine sent). The change labels each message with its date and
"the owner" or the sender's name, and a match must quote what came and the thread (`shows`, `agreed`), each sentence
found by `machine.text.quoted_in`. `cases-fresh.json` sha256 2053b0ad…, `cases-fresh2.json` 3e4354bf…, both frozen
before their first run.

| | set | turns | matching closed | wrong closes | tokens in / out |
|---|---|---|---|---|---|
| main | cases.json + old (as labeled lines) | 156 | 63 of 78 (81%) | 0 | 621 / 47 |
| change, first round | cases.json + old | 156 | 51 of 78 (65%) | 0 | 785 / 97 |
| change, final | cases.json + old | 156 | 60 of 78 (77%) | 0 | 785 / 98 |
| main | cases-fresh.json | 180 | 42 of 45 | 16 | 697 / 51 |
| change, final | cases-fresh.json | 180 | 42 of 45 | 0 | 890 / 99 |
| main | cases-fresh2.json | 90 | 39 of 51 | 3 | 682 / 44 |
| change, final | cases-fresh2.json | 90 | 39 of 51 | 0 | 875 / 92 |

Main's wrong closes: an OK that came only from the other side (15), and text on the page or in the message that claimed the owner's OK (4). The
first round's quote had to be one stretch of one message; a model often joins a sentence from two ("…as discussed.
Signed and attached."), so the final round checks each sentence on its own. The remaining loss on `cases.json` is one
case (a link back the page text can't show, 3 runs), now unsure.
