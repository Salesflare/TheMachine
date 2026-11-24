# Help questions eval

399 questions in people's own words about every help article, each with the sections that hold the answer (`want`) and what
a right answer says (`fact`, also when that is "it can't do that"). Nothing personal: the questions are made up.

- `dev` (207): what the search (`help_search.py`), the articles' keywords (`help_keywords.json`), the everyday words of other
  languages (`help_words.json`) and the prompt (`help_chat.py`) were tuned on.
- `held` (192): only measured, never tuned on. Keep it so: look at its totals (`--quiet`), not at its misses.

127 are in one of the eleven languages of the app (`d` and `h`). The other 272 (`p` and `q`) are 68 questions, each in English,
Dutch, German and French, written by a model that saw only the section with the answer. `--lang nl` asks one language's.

`python3 evals/help-questions/run.py --set dev` runs the search alone; with `--model` and `--judge` it asks the real prompt
and a second model grades each answer. The environment is that of `evals/family-questions/run.py`. `tests/test_help_questions.py`
keeps a floor under the search.

On gpt-6-luna, effort low, judged by gpt-6.1-sol (2026-11-24). Before: the same articles without the sections on sharing one
to-do, backups and one newsletter, and a search that knew no words of other languages.

| | dev before | dev now | held before | held now |
| --- | --- | --- | --- | --- |
| the right section, first search | 126 of 207 | 169 of 207 | 123 of 192 | 149 of 192 |
| the right section, after the second look | 142 of 207 | 177 of 207 | 144 of 192 | 165 of 192 |
| answered right | 135 of 207 | 168 of 207 | 139 of 192 | 155 of 192 |
| tokens in per answer | 1205 | 1161 | 1271 | 1169 |

The same run twice differs by about three answers per set of 60. On the 127 questions that were here before, the answers stayed
about as they were: 102, 102, 106 and 110 right before, 100, 102, 106 and 106
now, in four runs each. A new heading makes an article fall back to English in the other languages until the daily
translation, and the questions are asked in that state.
