# Done checks eval

Does the review write a page check (`done_check`) only when a to-do's messages give the page, and would that check close
the to-do only once the page really shows the result? `machine/store/done_checks.py` reads the page; this eval covers
the part a model writes: the page and the words.

Each case is made-up messages about one matter that waits on someone else, with the page's text before and after the
result. The prompt is the review prompt's own "Done when:" paragraph (from `--root`) plus the messages; the reply is
suggest's arguments. The real rules score it: `clean`, `in_evidence` (the address is in the messages), the baseline
read (the page before: already showing the words leaves the check inert) and `shows` (the page after). No web reads.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/done-checks/run.py --model <model> --runs 3
    ... --root <a checkout of main>     # the baseline: main's prompt, the same rules
    ... --cases cases-fresh.json        # the second held-out slice

Counted per turn: **plan** (a check written), **kept** (the app keeps it), **made-up url** (an address no message gives:
must be 0), **inert** (the baseline showed the words), **closes** (the to-do closes by itself instead of coming back:
an avoided interruption), **wrong close** (a close on a case that wants none: must be 0), **literal miss** (the page
shows the result in other words, so it comes back as before: a meaning check would catch these).

Sets: `listing` and `status` want a check; `no-url`, `not-page` (a link that isn't the result), `signin` (a page behind
a sign-in) and `homepage` (only who wrote) want none.

## Results (2026-11-27, gpt-6.1-sol, effort low, 3 runs)

`cases.json` was frozen before the first run (sha256 4b51107a…), `cases-fresh.json` before the second (8ff58dbc…).

| | turns | plan | made-up url | closes | wrong close | literal miss | input tokens |
|---|---|---|---|---|---|---|---|
| main, cases.json | 63 | 0 | 0 | 0 | 0 | 0 | 298 |
| change, first round, cases.json | 63 | 27 | 0 | 18 | 6 | 3 | 404 |
| change, final, cases-fresh.json (held out) | 24 | 12 | 0 | 9 of 9 listings | 0 | 0 | 411 |
| change, final, cases.json | 63 | 24 | 0 | 17 of 24 that want one (3 inert) | 0 | 4 | 414 |
| main, cases-fresh.json | 24 | 0 | 0 | 0 | 0 | 0 | 295 |

The first round's 6 wrong closes were pages that already showed the words (an old incident on a status page, the
owner's name on a blog's home page). The fix is in the code, not the prompt: a baseline read right after the check is
kept, and a page that shows the words then is never checked. The prompt also says no site home page. The literal misses
are a page that writes the name joined ("LumenCRM", 3) and a page that names the product but not the owner (1): those
come back as before.
