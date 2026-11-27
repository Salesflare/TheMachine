# Learning scope eval

Where does a rule or fact a learning pass writes hold? The turn is the app's own (`learning_loop.prompt`, with the page
as `profile_evidence` gives it); each change it answers is placed the way `apply` places it (`learning_loop.scope_of`).
`--main` places the same answers with another `learning_loop.py` too, so two gates are judged on one set of turns.

    OPENAI_BASE_URL=... OPENAI_API_KEY=... python3 evals/learning-scope/run.py --model <model> --runs 3 --main old_learning_loop.py
    ... --cases cases-fresh.json

Sets: `cases.json` (20), `cases-fresh.json` (24) and `cases-fresh2.json` (20), each written apart and frozen before its
first run. A case is one batch with the scopes a rule from it may rightly take (`none`: nothing to learn).

Counted per change: right, wrongly global, too broad (an area or channel where the case wants one person or
organization), too narrow, off, lost (not kept although there is something to learn), unwanted (kept on a case with
nothing to learn).

## Results (2026-11-27, effort low, 3 runs, 64 cases, 576 turns)

`cases.json` sha256 fec8c513…, `cases-fresh.json` 52f802ef… (one note's word respelled in US English after the runs), `cases-fresh2.json` cd0651f6….

| model | gate | right | wrongly global | too broad | too narrow | lost |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | main | 162 | 0 | 0 | 6 | 0 |
| gpt-6.1-sol | change | 162 | 0 | 0 | 6 | 0 |
| gpt-6-luna | main | 133 | 0 | 6 | 5 | 17 |
| gpt-6-luna | change | 133 | 0 | 6 | 5 | 17 |
| gpt-5.6-luna | main | 122 | 0 | 6 | 5 | 13 |
| gpt-5.6-luna | change | 124 | 0 | 4 | 5 | 13 |

Every global the models gave was one the case wanted (2 more on a case with nothing to learn, kept by both gates as
unwanted). The change differs from main on 2 changes, both wins: three signals all with one person, said `area:work`,
now kept for that person. A first round that also required every signal of a batch without `from` and narrowed to a
shared organization lost 8 right placements (a team's work habit narrowed to the owner's own company, a missing `from`
dropping an area rule) and was dropped. The remaining too broad changes all came without a scope field (the model wrote
it into the text), so the whole batch's shared area or channel was used.
