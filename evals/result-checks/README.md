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
