# Help questions eval

127 questions in people's own words, in all eleven languages of the app, about every help article, each with the sections
that hold the answer (`want`) and what a right answer says (`fact`, also when that is "it can't do that"). Nothing personal:
the questions are made up.

- `dev` (67): what the search (`help_search.py`), the articles' keywords (`help_keywords.json`) and the prompt (`help_chat.py`) were tuned on.
- `held` (60): only measured, never tuned on. Keep it so: look at its totals (`--quiet`), not at its misses.

`python3 evals/help-questions/run.py --set dev` runs the search alone; with `--model` and `--judge` it asks the real prompt
and a second model grades each answer. The environment is that of `evals/family-questions/run.py`. `tests/test_help_questions.py`
keeps a floor under the search.

On gpt-6-luna, effort low, judged by gpt-6.1-sol (2026-11-24). Before: the four best whole sections, cut at 1400 characters,
and one turn.

| | dev before | dev now | held before | held now |
| --- | --- | --- | --- | --- |
| the right section, first search | 38 of 67 | 54 of 67 | 32 of 60 | 42 of 60 |
| the right section, after the second look | | 57 of 67 | | 53 of 60 |
| answered right | 33 of 67 | 55 of 67 | 30 of 60 | 48 of 60 |
| tokens in per answer | 1160 | 1232 | 1068 | 1303 |

Before, an answer was right 57 times in 70 when its section was in, and 6 times in 57 when it wasn't. The same run twice
differs by about three answers. One author wrote the questions and the Common questions article; the articles' keywords
were written from the articles alone, without the questions.
