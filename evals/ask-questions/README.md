# Ask from Search eval

Questions typed into Search ([Ask a question](../../docs/help/keyboard.md#ask-a-question)), answered by a real model on a
made-up Machine: one of three (`cases.json`, `cases-2.json`, `cases-3.json`), the first two each with work and personal mailboxes, one that can't be read
since days, and chat accounts. All of it is made up: every person, message and address, and every domain ends in
`.example`.

| Set | Questions | What it checks |
| --- | --- | --- |
| own connections | 42 | one of the owner's own mailboxes or chat accounts, in English, Dutch and French: by address, "my personal mail", "my second Gmail", failing, not connected, in the other area, with a subject (there, only elsewhere, or nowhere), a person or days, "check my mail" |
| just came in (`cases-3.json`) | 15 | messages that came in after the Graph was built and are not reviewed (`after`, in minutes): a new sender by name with and without accents and hyphens, one with the name of someone the owner is more in touch with, "8 minutes ago", "just came in", and questions that go on from an earlier one (`before`) |
| ordinary | 14 | a person, a time, a subject, someone unknown, a request to send, a service or address the messages are only about ("leaving Gmail"): these must stay as they were |

A question passes when a second model finds the answer right and plain (it speaks like a person, never of "these
messages"), no message of another connection was in its prompt (`only`; not with `beyond`, where a subject nothing
there matches may be looked for in the rest of the area), the messages it `needs` were, and an ordinary one was not
narrowed to a connection (`whole`). Two runs each, on a lighter model at low effort:

| | Before | With own connections | With the place told from the subject |
| --- | --- | --- | --- |
| own connections | 4/84 | 79/84 | 81/84 |
| ordinary | 24/26 | 21/26 | 26/26 |
| ordinary, narrowed to a connection | 0 | 4 | 0 |
| messages of another connection read | 37 | 0 | 0 |
| first turn, characters | 1611 | 2423 | 2516 |

Of the three misses left, one tells up to when the mail was read without being asked, one names a mail by its subject
only, one writes a citation out. Someone unknown with nothing found gets no answer, as before (only the search results).
Just came in, two runs: before 16/30, now 30/30 (its questions were in view while this was made). Two sets written and
frozen before their first run: 17/32 before and 29/32 now on the first, after which a name two people have was put
plainly to the answer; 16/32 and 29/32 on the second, with nothing changed after it. Of the last three misses, all tell
the right message and leave out one thing it asks. The other sets stay as they were: 82/84 and 25/26 to 26/26, the
first turn 2511 characters.

There are no local embeddings here, so a subject is found by its words only. Run it with `run.py` (see its first lines
for the model and the key).
