# Scheduling between Machines

Two people who each have a Machine, and who are not in the same Fleet, find a meeting time over The Machine Network.
Their Machines trade free/busy times, never what is on a calendar, and each owner taps **Book it** before anything is
booked. Code: `meet.py` (protocol, the to-do's states) and `cloud/meet.py` in the cloud repo (finding and routing).

## The flow

1. Someone writes "let's meet next week". The review marks the to-do as a meeting request (`meet` on `suggest`) and,
   as today, prepares an email draft that proposes times.
2. The owner's Machine looks up the other person's address on the Network. No Machine there: the to-do stays as it
   is, with the email draft. That is the fallback for every step below.
3. Their Machine is found: the owner's Machine asks it for free times in a window (the days the review saw, at most
   14). It waits up to 3 minutes. No answer, or a refusal: the email draft stays.
4. The answer is free times only, within the other owner's work hours, after their buffer, rounded to 15 minutes.
5. The owner's Machine (the proposer) picks the first slot that fits both: its own free times, work hours, meeting
   length and buffer, both sides' preferred part of the day. It sends the slot to the other Machine.
6. Each owner gets one to-do: "Meet Alex Tue 14:00, 30 min, Zoom?" with **Book it**, **Other time** and **Not needed**.
   The proposer's to-do is the one the email made; the other side gets a new one.
7. **Book it** on both sides: the proposer's Machine adds the event to its owner's calendar and invites the other
   person (Google sends the invite). It tells the other Machine, which closes its to-do.
8. **Other time** on either side: the proposer picks the next slot that fits and both to-dos show it, with both taps
   needed again. After 3 rounds the proposer's to-do falls back to the email draft.
9. **Not needed** on either side closes both to-dos.

## Rules

- **Taps.** No invite, email or calendar change goes out without the owner's own tap. The invite needs both taps.
- **Careful.** At the Careful level the setting below starts Off, and the proposer sends a slot only after its own
  owner tapped Book it, so not even a free slot leaves before a tap.
- **End to end.** Every message is sealed for the other Machine with the Network keys Fleets use (`network_crypto`),
  bound to who sends what to whom. The cloud routes sealed envelopes and can't read them. Keys are pinned the first
  time; a Machine whose keys change is refused until it starts over.
- **The setting.** Fleet, Network: **What other Machines may ask mine**: **Free/busy for scheduling** (the default) or
  **Off**. Off answers nobody and takes the owner out of the lookup.
- **Who can ask.** Only a Machine the cloud verified (an active account, its keys published, the account's current
  Machine). The cloud passes on the asker's verified addresses (their account email and mail they connected with
  OAuth). The answering Machine answers only when its own mail shows an exchange with one of those addresses both ways
  (the owner wrote to them and they wrote to the owner). Strangers can't probe a calendar.
- **Limits.** The cloud limits lookups (20 an hour, 60 a day) and messages per person and per pair. Each Machine also
  answers at most 6 asks a day from one person and 40 a day in all.
- **The answer.** Only the asked window, at most 14 days, starting within 60 days. Free times inside work hours only,
  busy times widened to the 15-minute grid. Private and personal events count as busy, without any detail.
- **Activity.** Each exchange is a line under Activity, Calendar: who asked, which window, which slot, how it ended.
  Never an event's title or details.

## Finding a Machine

There was no lookup by email address (Discovery matches a whole address book privately, for friend suggestions). The
cloud adds a small one for scheduling:

- A Machine says what its owner allows (`op: allow`), and gets its scheduling id (`mt_...`), apart from Fleet and
  friend ids.
- `op: find` takes `sha256("tm-meet/1\n" + address)` and returns the id, public keys and first name of the one active
  account with that verified address whose setting is on. Nothing for anyone else, the same answer for "no such
  person" and "Off". An address that more than one account lists finds nobody.
- `op: send`, `op: inbox` and `op: ack` carry sealed envelopes between those ids. The cloud deletes them once
  acknowledged, or after 3 days. The Fleet inbox says `meet: <count>` so a Machine fetches them at once.

## Messages

All sealed, all with a session id (32 hex):

| Type | From | Body |
|---|---|---|
| `ask` | proposer | window `start` (a date) and `days`, `minutes` |
| `free` | other | free times `[[start, end]]` UTC on the 15-minute grid, preferred ones, `book` (can show the to-do) |
| `no` | other | nothing else (the reason stays in its own Activity) |
| `propose` | proposer | `start`, `end`, `video`, `round` |
| `ok` | other | the `start` its owner tapped Book it on |
| `other` | other | asks for another time |
| `cancel` | either | Not needed, or the proposer gave up |
| `booked` | proposer | `start`, `end`: the invite went out |

## Preferences

Length (default 30 minutes), buffer around meetings (10), preferred part of the day (any, mornings, afternoons), from
the same setting. Meetings stay within Work hours (Settings, Notifications) and end by 18:00. The video habit is read
from the owner's own recent meetings (Zoom, Google Meet or Teams links); the to-do names it as a question.

## Not yet

- Outlook calendars: the proposer needs a Google calendar it can write to, else it falls back to the email draft.
- A video link is not created: the invite names the habit, and the owner adds the link.
- Group meetings (more than two Machines).
