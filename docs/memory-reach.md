# Where what the owner taught reaches

What the owner's Machine learns comes in three ways, and five kinds of work should use it. This page says, for each
pair, the path from one to the other and the test that proves it (`tests/test_memory_reach.py`, a temporary store with
made-up data, no model call), and what is still missing. How memory is picked for a prompt is in
[What a prompt reads](intelligence.md#what-a-prompt-reads).

## Ways in

- **Chat.** What the owner states in their own private chat ("remember ...") is a fact (`remember_fact` with the
  bridge's `_owner_chat`, tied to their last message there). A note or correction on a to-do (Change, Not needed, a
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
| Preparation and draft | facts and rules (`facts_for`), set-aside and historical facts that bear on it (`retained`); the to-do's chat runs in that session, each turn with its own smaller `retained` slice (`todo_chat`) | records, related signals, voice | facts and rules, `USER.md` |
| Ask | facts on the question's records, others by meaning | promises, summaries, meetings | same as chat |
| Talk | `recall` tool: learned facts by words (`ask_memory.learned`) | search, open_record, promises | `recall`: learned facts and memory search |
| Owner's main chat | facts about a person (`graph` node: `open.known`) | `graph`, `events` | `USER.md`, `MEMORY.md` (OpenClaw) |
| Routine | facts and rules block (`recall` `routine`) | `events` and `graph` tools | facts and rules block, `USER.md`, memory search, birthdays |
| Morning digest | through the to-dos it lists | promises due today | through the to-dos it lists |

Fixed here, each with its test: a routine's run read no fact or rule (it now gets the front of what a review gets:
1,200 characters of facts and 600 of rules, logged as `routine` in `memory_use`), and Talk's `recall` only searched
OpenClaw's memory files, so a fact the owner told the chat never came back by voice (it now gets up to three of the
owner's own facts and rules that share the words, logged as `talk`). A correction said in the owner's chat ("the
office is in Brussels now") was saved next to the fact it corrects, since the chat sees no fact ids, so both values
reached preparations until the next condense pass. It now takes that fact's place at once
(`graph_actions.said_instead`): a current fact about the same records whose words it shares, with a number or name
swapped or a negation added or dropped. The old one stays behind it under Learning with Undo merge. No new model turn.

## Still missing

- **The owner's main chat** (Telegram, the web chat) can't read a fact about the owner or the world, nor a draft rule:
  only what the `graph` tool shows on a person's page. It saves facts there but doesn't read them back. A fix needs a
  read action in the bridge (`TOOL_ACTIONS`) or a bounded context block, both plugin changes.
- **Ask without embeddings** finds a fact about no one only by meaning, so on a Machine without embeddings it doesn't.
  `ask_memory.learned` (words) could be its fallback.
- **Routines** get no voice block, so a draft a routine leaves doesn't follow how the owner writes on that channel.
- **A to-do's chat** answers in its preparation's session: a current fact learned after that preparation started
  reaches it only on a redo (each turn does get the set-aside and historical facts that bear on the to-do).
- **Talk's recall** matches words, not meaning: "seat" finds "aisle seats", "flying" doesn't find "flights".
- **A chat correction that swaps a plain word** ("window seats" for "aisle seats") is left to the condense pass,
  which judges it by meaning; code only swaps numbers, names and negations.
- **The morning digest and weekly recap** are plain code with no model turn: what was learned reaches them only
  through the to-dos and promises they list. By design.
