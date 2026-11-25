# Ask from Search eval

Questions typed into Search ([Ask a question](../../docs/help/keyboard.md#ask-a-question)), answered by a real model on a
made-up Machine: two Gmails for work, a personal mailbox, a personal Outlook that can't be read since four days, and
WhatsApp. All of it is made up: every person, message and address, and every domain ends in `.example`.

| Set | Questions | What it checks |
| --- | --- | --- |
| own connections | 26 | one of the owner's own mailboxes or chat accounts, in English, Dutch and French: by address, "my personal mail", "my second Gmail", failing, not connected, in the other area, with a subject, a person or days, "check my mail" |
| ordinary | 9 | a person, a time, a subject, someone unknown, a request to send: these must stay as they were |

A question passes when a second model finds the answer right and plain (it speaks like a person, never of "these
messages"), and no message of another connection was in its prompt (`only`). Two runs each, on a lighter model at low
effort:

| | Before | With own connections |
| --- | --- | --- |
| own connections | 2/52 | 51/52 |
| ordinary | 16/18 | 18/18 |
| messages of another connection read | 22 | 0 |
| first turn, characters | 1607 | 2390 |

Both misses before in `ordinary` are the unknown person, answered with "these messages". The one miss after says up to
when the mail was read, without being asked. Someone unknown with nothing found gets no answer, as before (only the
search results). Run it with `run.py` (see its first lines for the model and the key).
