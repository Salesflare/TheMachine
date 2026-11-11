# Where what the owner taught reaches

What the owner's Machine learns comes in three ways, and five kinds of work should use it. This page says, for each
pair, the path from one to the other and the test that proves it (`tests/test_memory_reach.py`, a temporary store with
made-up data, no model call), and what is still missing. How memory is picked for a prompt is in
[What a prompt reads](intelligence.md#what-a-prompt-reads).

## Ways in

- **Chat.** What the owner states in their own private chat ("remember ...") is a fact (`remember_fact` with the
  bridge's `_owner_chat`, tied to their last message there). In the web chat's main session, which has no
  `assistant_signals`, the bridge's `assistant_remember` tool does the same: `before_dispatch` notes the id of the
  owner's message there (`web_chat_said`, with the owner key, never the words) and the fact is tied to it
  (`webchat-said:<id>`). A note or correction on a to-do (Change, Not needed, a
  to-do's chat, Fixed at the source) becomes a fact, a draft rule or a voice line through the review or the to-do's
  own run.
- **Messages.** A review reads mail, Slack and the other sources. It never saves someone else's words as a fact; it
  keeps promises, the Graph (roles, organizations, projects, summaries), the owner's voice from their own sent
  messages, contact details, and ends a fact a newer message overturned.
- **OpenClaw notes.** `USER.md` is read whole by reviews, preparations, routines and the profile turn
  (`openclaw-plugin/review-recovery.ts`); `MEMORY.md` is searched by OpenClaw's memory search. Lines the owner ticks
  under Bring these in become facts and rules (`bring_in.py`, source `notes:<file>`); `notes_people.py` puts the ones
  about someone on that person's page, and a date of birth on the Birthdays routine.

## Matrix

| work | chat | messages | notes |
|---|---|---|---|
| Review | facts block, set-aside and historical facts that bear on the batch (`recall` `review`, `retained`) | promises, sender lines | facts block, `USER.md` |
| Preparation and draft | facts and rules (`facts_for`), set-aside and historical facts that bear on it (`retained`); the to-do's chat runs in that session, each turn with what changed since the session read the list (`new`) and its own smaller `retained` slice (`todo_chat`) | records, related signals, voice | facts and rules, `USER.md` |
| Ask | facts on the question's records, others by meaning, or without embeddings the owner's own by words (`ask_memory.matching`) | promises, summaries, meetings | same as chat |
| Talk | `recall` tool: learned facts by words in their plain form, then by meaning from stored vectors (`ask_memory.learned`) | search, open_record, promises | `recall`: learned facts and memory search |
| Owner's main chat | `assistant_memory` tool: their own facts and draft rules by words, then by meaning from stored vectors, then set-aside and historical ones (`recall` `chat`); facts about a person (`graph` node: `open.known`) | `graph`, `events` | `assistant_memory`, `USER.md`, `MEMORY.md` (OpenClaw) |
| Routine | facts and rules block (`recall` `routine`); a run that leaves a draft: the voice for its channel | `events` and `graph` tools; voice | facts and rules block, `USER.md`, memory search, birthdays |
| Morning digest | through the to-dos it lists | promises due today | through the to-dos it lists |

Fixed here, each with its test: a routine's run read no fact or rule (it now gets the front of what a review gets:
1,200 characters of facts and 600 of rules, logged as `routine` in `memory_use`), and Talk's `recall` only searched
OpenClaw's memory files, so a fact the owner told the chat never came back by voice (it now gets up to three of the
owner's own facts and rules that share the words, logged as `talk`). A correction said in the owner's chat ("the
office is in Brussels now") was saved next to the fact it corrects, since the chat sees no fact ids, so both values
reached preparations until the next condense pass. It now takes that fact's place at once
(`graph_actions.said_instead`): a current fact about the same records whose words it shares, with a number or name
swapped or a negation added or dropped. The old one stays behind it under Learning with Undo merge. No new model turn.
Talk's recall matched exact words only: "flying" didn't find "flights", "seat" found only "seats". Words now match in
their plain form (plurals, -ing, -ed: "booking" finds "booked"), and with embeddings on, the owner's facts and rules
whose stored vector (`fact_vectors`) is close to the words come after the word
matches, against one local embedding of the words with a 2 second timeout. No model turn, no fact embedded during the
call, still at most three (`LEARNED`). Without embeddings a word with another stem ("flying", "flights") still doesn't
match. Forgotten, ended and replaced facts stay out; a connected AI's never comes in.
Ask found a fact about no one (one about the owner themselves, or the world) only by meaning, so on a Machine without
embeddings, or while the embedding server was down, it found none. It now falls back to the owner's own facts that
share the question's words: half of what it is about, short words too ("when do I go to the gym" is about the gym;
question and common words never count, `ask_memory.QUESTION_WORDS`), or enough of the fact's own (`word_match`, as a
preparation picks without embeddings). Never a connected AI's fact by words;
forgotten, ended and replaced facts stay out, as from Ask's meaning search.

The owner's main chat (their private Telegram chat and the web chat) saved facts but couldn't read them back: only
what `graph` shows on a person's page. The bridge's `assistant_memory` tool now reads them on demand
(`recall_learned`, the `chat` recall, `ask_memory.for_chat`): the owner's own current facts and draft rules that share
at least half of the question's words in their plain form (as Talk's recall), then set-aside ones and, marked "Historical, not current", ended or replaced
ones (`retained_facts.py`). Never a connected AI's fact or one the owner removed, and a fact about a person only when
the question names them. At most 900 characters (about 225 tokens), logged as `chat` in `memory_use`. No context
block: a turn that doesn't ask costs only the tool's definition (about 120 tokens, cached with the rest). The bridge
sets the chat mark (`_owner_chat`); the service answers nothing without it.

The chat's tool matched by words only, so "flights" or "plane trip" didn't find "You only fly KLM". With embeddings
on it now also finds by meaning, as Talk: one local embedding of the question (2 second timeout, only when some fact
has a stored vector), against the stored vectors (`fact_vectors`) of the current facts and draft rules (at least
`FACT_FLOOR`) and of the set-aside, ended and replaced ones (`retained_facts.near`, within `MEANING_WORK`
comparisons). Word matches still come first; no fact is embedded during the call and no model turn runs. Without
embeddings, or when the embedding server fails, the words alone, as before. The same rules hold: never a forgotten
fact (its vector may still be stored, it is never read), ended and replaced ones only as history, never a connected
AI's, a person's fact only when named, and the same 900 characters. On a store with 5,000 facts the meaning scan adds
about 60 ms to a call, plus the one embedding request.

A to-do's chat answers in its preparation's session, so a fact learned after that preparation started reached it only
on a redo. Each chat turn now gets what changed since the session read the list (`retained_facts.since_session`, the
`new` block of `todo_chat`): a fact or rule learned, edited or brought back since, that bears on the to-do (all of
them while the list is short, as a preparation gets all of it then), and a line for one the session had that the
owner removed ("no longer use it") or that ended (as history). At most 3 lines and 400 characters, never one the
session was already given in that state (the session's runs in `memory_use`), never one learned on this to-do or a
connected AI's. Logged as `todo_chat`.

A correction that swapped a plain word ("window seats" for "aisle seats") was left to the condense pass. It now takes
the fact's place too (`graph_actions.swaps_word`): one content word swapped and every other word the same, in the same
order ("now" or "instead" aside), about the same records. Guarded so another matter in the same frame stays apart: not
the subject ("Lunch is at noon" and "Dinner is at noon"), not a word after a scope word ("on flights", "on trains") or
in a list ("apples and pears"), not another form of the same word, and at least three other content words shared
("You like tea" and "You like coffee" stay apart). The old one stays as history with Undo merge, and reaches a to-do it
bears on as "Historical, not current". No model call.

A routine's run got no voice block, so a draft it left didn't follow how the owner writes on that channel. A run that
leaves a draft now gets the owner's voice for its channel (the `voice` block of the `routine` recall): All and the block
of the account the draft goes out from, whole blocks only, up to 800 characters. Never judged from the run's words: a
routine that left a draft before gets it in its turn's message (`routines_app.routine_draft_channels`); a run that
hands in its first draft gets it back once, nothing saved, to follow it (`routine_draft_voice`). A service its words
or the draft's title name (Slack, LinkedIn) only goes first. A run that hands in no draft gets nothing. Logged as
`voice` (by channel) under `routine` in `memory_use`.

## One fact end to end

`tests/test_memory_e2e.py` follows one fact through every surface, on a database file with made-up data, and checks
each step again after a restart (a new Store and App on the same file). The owner says it in passing in the web chat
and in their private chat (no "remember"), it is found by the main chat (`assistant_memory`), Ask, a to-do's
preparation and chat, and Talk; a plain-word correction ("actually it's Antwerp") replaces it, the old one only as
history; once the owner removes it under Learning it is gone from all of them and from the knowledge export. A fact
about a Personal person stays out of a Work to-do, Ask in Work and the team's learnings; a connected AI's fact is never
read back as the owner's; each surface stays in its budget.

Fixed with it: Ask in Work found a fact about a Personal person by its words or meaning (a preparation already left
it out). It now leaves out a fact about people all on the other side, as `Store.facts_for` does
(`fact_links.on_side`). And a removed fact kept its stored vector, as did the facts it had replaced: removing one
now deletes those vectors (`Store.forget_fact`); one brought back is embedded again by the next background pass.

A fact got its stored vector only once a preparation or Ask ranked it, so one said in passing ("I only fly KLM") was
found by words only until then, by the main chat, Talk and the retained facts alike. The embedding worker now embeds
it within a minute (`Store.embed_new_facts`): each pass reads the owner's current facts and draft rules that have no
vector of the model in use, newest first, and embeds at most `FACT_VECTOR_BATCH` (8) in one local request, stored as
a preparation stores them (only while the fact still says what was embedded). A pass with none waiting is one read.
Never a removed or forgotten fact, nor a connected AI's (a preparation given one still embeds it, as before). Without
embeddings nothing runs; an embedding error leaves them for the next pass, logged once per kind.

What stays by design: the owner's own facts have no area of their own (`side` is a connected AI's only); one about no
person holds in Work and Personal. A removed fact's row stays behind as a tombstone (it keeps a review from saving it
again, lets a to-do's chat tell its session to stop using it, and Undo merge), so its words stay in the keyword
index (`fact_search`); every reader of the index leaves removed facts out. The main chat has no tool to remove a fact:
the owner removes it under Learning.

## Still missing

- **Without embeddings**, the owner's main chat, Talk and Ask match what was learned by words in their plain form
  only: a word that changes its stem ("flights" for "fly") or another word for the same thing ("plane") finds it
  only by meaning. With embeddings on, a fact learned in the last minute (before the background pass embeds it) is
  found by words only.
- **The morning digest and weekly recap** are plain code with no model turn: what was learned reaches them only
  through the to-dos and promises they list. By design.
