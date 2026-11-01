# Shared Graph

A Work Fleet shares its Graph. People, organizations, projects, boards and client email that one Machine knows show up on
every teammate's Machine, sealed Machine to Machine. The Network (the control plane) carries sealed blobs it can't read.
Nothing syncs with an outside CRM: everything lives in The Machine.

Code: `shared_graph.py`, `shared_graph_app.py`, `fleet_trust.py`; on the control plane, `cloud/fleet_graph.py`. How the
Network seals and carries messages in general: [The Machine Network](network.md).

## Turning it on

The Shared Graph is **experimental** and off by default. Nothing goes until an admin turns on **Share the Graph in this
Fleet** (a signed `pause` statement; with no statement at all, sharing is off). Turning it on asks the admin to confirm
that the company may share this mail and has told its people.

A Fleet that shared before the switch existed stays on ([Migration](#migration)).

## What feeds it

**Per connection.** Each owner picks per connection (**Your connections**, `graph_connections`, kept in
`graph_conn:<fleet>`). The domain decides where each starts:

- A Work connection whose address is on one of the Fleet's domains (the members' account and work addresses,
  `fleet_domains`) starts on.
- One at another company's domain starts off and says "Other company, not shared", whatever it is named. The owner can
  turn it on.
- One without an address (a code host, a social account) starts on only when it is named for the Fleet (`work:<Fleet
  name>`).
- Personal connections never go and have no switch.

Turning a connection off takes back what it shared, like an unshare.

**Required connections.** An admin can require every member's **Work email** and **Work calendar** (a signed `policy`
statement, `{t: policy, fleet, member, key, by, require: [mail, calendar], at}`; the newest from a confirmed admin wins,
so the Network can't make one up). Only connections on the Fleet's own domains can be required, and the admin first
confirms that the company has told its people. A required connection is on whatever the owner chose before, and shows
"Required by <Fleet>". With no `pause` statement yet, a `policy` that requires something turns sharing on
(`graph_paused`); an admin's Off still wins.

**Only what the owner took part in.** Mail and meeting notes a Machine sees through a shared CRM (a teammate's mailbox,
a meeting a teammate logged) never go from it (`secondhand`). They go from their owner's Machine, under that owner's own
choices, and never come back to them as a teammate's. A teammate's thread the owner is on themselves isn't shown under
From the team, and each timeline line shows once.

Inside a connection that is on, each thread is still sorted ([Threads](#threads)), and **Keep private** on a thread or
record still wins.

## Threads

Each thread is judged on its own by the review, by what it is about anywhere in it (quoted earlier mail too), never by
word lists and never a whole company at once. Every verdict counts the same, whatever model made it. Classification is
best effort: the owner reviews the preview and corrects mistakes with Keep private. When unsure, nothing goes.

| Thread | Who reads it | What the team sees |
|---|---|---|
| **Client**: at least one person outside the company, at an organization on the Graph or with a work domain; also everyday work with a partner company, even one in the same market (an integration, a listing or link exchange, co-marketing) | The Fleet | The full email: body, from, to, date, and its attachments (up to 2.5 MB each; bigger ones show as "too large to share") |
| **Sensitive**: buying or selling a company, a merger, talks with a possible buyer, acquirer or investor (a first approach too), fundraising, board matters and investor updates, a valuation, a term sheet or LOI, a deal NDA, HR, hiring or recruiting about one person (the owner too), legal, health, own money, security (access, keys, tokens, vulnerabilities, incidents) | Only the people on it | Nothing in automatic sharing, not even that it exists. Sticky across reviews. A board or thread shared by name may include it |
| **Unsure**: probably client work, but not clear; a peer or competitor where what the two do together is unclear | The owner first | Nothing until the owner picks **Share with team** or **Share with…** in **Share these?** |
| **Internal**: colleagues only; everything in the company's own Slack, whatever the review said. Only Slack Connect (another company's member or a guest, from Slack's `is_ext_shared`, `team_id` and guest flags in `slack_members`) goes through the client checks | Only the people on it | Nothing. Never shared, also not by hand |
| **Other**: notifications, receipts, invoices, the company's own bills and support tickets with its suppliers, newsletters, cold pitches | The owner | Nothing |
| **Personal**: a personal account, or the review says it is personal | The owner | Nothing, not even that it exists. Sticky, and never by hand either |

**Labels.**

- Every thread on the dashboard has a small label, **Team** or **Only you**. One tap changes it. In chat the owner can say
  "keep the Globex thread private" and the assistant sets the same thing. A review never sets a hand choice.
- A thread no review has judged yet is **Only you** until one does. **Only you** by hand shares nothing about that thread.
- A new client thread waits an hour (`HOLD`) before it goes, so the owner can still change their mind.
- **Unshare** on a shared thread takes it back ([Unsharing](#unsharing)). The copy says honestly that someone may have
  read it already.
- Two hand choices for the same organization ask once: "Always keep threads with X private?" (a rule).

**Rules before the review.** These come before the review's call and before a hand choice:

- Only accounts with a Work boundary for this Fleet. A personal account is never read for this.
- A thread with nobody outside the company is internal.
- Automated mail is never client: a thread where nobody on the owner's side wrote and every message comes from a system
  sender (bulk, no-reply, notifications, receipts, invoices, billing, relays) or was filed by the mailbox as an update,
  promotion, social, forum or spam message is **Other** (`automated_message`, `Scope.automated`), and isn't sent to the
  review. Once someone on the owner's side replies, the review judges it.
- People of the owner's own life never go: someone only in their Family or Friends, or someone they marked Personal. No
  record of them, and a thread with them on it stays Only you.

## Records

Work records are shared by default:

| Layer | What | Shared |
|---|---|---|
| Exists | "Sam knows Lee at Globex, strong, last contact 3d" | Already, through "who knows someone" |
| Record | Name, role, company, owner, project stage, next step | Yes, for Work people, organizations and projects |
| Timeline | One short line per message or meeting, written by the review | Yes, for client threads only |
| Raw mail | The email itself and its attachments | Client threads only |

- **The record's owner** is the one picked by hand (`owner_pick`, a Work Fleet member id; `crm.py`), else whoever in the
  team is closest. It travels only with a record that is shared anyway, and so do its own fields and tags
  (`crm_fields.py`). For a record several members share, the closest one's field values win and the tags add up.
- **Keep private** on a person, organization or project shares nothing about it: no record, no timeline, none of their
  threads. It needs nobody's OK.
- **Held back:** colleagues (people at the Fleet's own domains) are never shared as records, and neither is a person
  whose reviewed threads are all sensitive.

**Only-you boards.** A board set to Only you (`boards.visibility`), and every project on it, is held back like Keep
private: no board, no record, no timeline, none of its threads, and no teammate's Team view shows it. A project can
differ from its board (`projects.visibility`; empty follows the board). Projects in an Only-you board suggestion are held
back while it waits to be saved. Switching a board or project to Only you takes back what was shared, at the next
publish. Each record passes one check before it is sealed (`Scope.shareable`). Code that shares anything asks
`graph.visible_to_team(db, node_id)` or `graph.hidden_project_ids(db)`.

**A project on a Team board** shares its record (name, board, stage, why, next step, organization, people) even before a
review has judged one of its threads, so the team pipeline shows every project on it. Its threads still go only as they
are judged.

- Its meetings, Zoom notes, Intercom conversations and chats (`Scope.team_items`) go by being on the board, whatever the
  review called them, except sensitive ones and chats judged internal (`CHAT_KINDS`). Only a board shared by name, or
  Team by hand, takes those.
- Each waits until the review has looked, and one just called client waits out `HOLD` like mail.
- Never one of a personal account or another company's, with someone of the owner's own life, called personal or
  automated, kept private, of an Only you project, or with only colleagues on it.
- A why or next step that came from a signal that never goes doesn't go either.
- Its organization (`projects.org`) goes as a name and hashed domain only when that organization could go itself: one
  with a website, outside the Fleet's domains, not personal mail and not kept private. Linking a project to an
  organization never adds people, threads or timeline lines.

## Shared by name

The owner can share a board with chosen teammates (**Share board…** on its ⋯ menu, `graph_board_share`;
`boards.visibility` `people`, the people in `share_people`), or one thread (**Share with…** on its label,
`graph_thread_share`).

**What they get** (`grants`, `Scope.granted`): the board's open projects with their full timelines. That is every thread
linked to them, sensitive ones (deals, M&A) too, and their meetings, notes, Intercom conversations and chats
(`ITEM_KINDS`, `Scope.board_items`), which count as shared by being on the board, without a review. Each project carries
its timeline (`TIMELINE_PROJECT` lines: a line per signal, its moves and its to-dos; a move or to-do only when every
signal it came from goes). A thread shared by hand goes whatever the review said.

**Never:** personal threads, people kept private or marked Personal, threads with only colleagues, or accounts the owner
hasn't selected in `graph_accounts`. Automated mail stays out when only its board is shared; an explicit thread share or
Team choice can override that.

**How it travels.** Teammates with the same grants get their own chain of records: a snapshot and deltas whose header
says `only` and carries the chain as `tag`. A thread only some get is sealed to them alone, also marked `only`.

- A Machine passes an `only` blob to nobody outside its `to` (`_graph_serve`), and refuses one passed on to it when it
  isn't in `to` (`graph_take`).
- A snapshot for the whole team goes first in each round and ends every older chain; the chains follow in the same round,
  so the newest snapshot for anyone is the one meant for them.
- Taking someone off, the board back to Only you, or a project moved off the board changes their chain: their next
  snapshot no longer lists it, and their Machine deletes it. A thread nobody gets any more gets the usual empty blob.

## The first share

There's no Start button: being in a Work Fleet where sharing is on is the choice.

- A Machine's first share goes `LOOK_OVER` (an hour) after it tells its owner once, on their phone or Telegram
  (`_start_notice`).
- In that hour every verdict not made by hand is sorted again with the current rules, and **What's shared** lists the
  client threads that would go, by organization, each with **Keep private**. **Share now** sends it at once.
- Admins see each teammate's state: sharing, not started, off, or taken out. A Machine that shared before goes on.

## History and limits

At the start a Machine shares all the Work history it has, not only recent mail, through the same labels: a history pass
(one model turn at a time, a batch of threads per turn) judges older Work threads no review saw.

- Threads go newest first, at most 1,000 blobs an hour and 18,000 a day per Machine (`PER_HOUR`, `PER_DAY`, under the
  Network's 1,200 and 20,000).
- Taking a thread or file back goes first in each round and has its own count (`GONE_HOUR`, `GONE_DAY`), so it never
  waits behind new shares.
- `share_out` keeps what went, so a backfill that stopped (a limit, the Machine off) goes on from there next round.
- Someone who joins later gets what went before by [catching up](#catching-up).

The weekly recap says, in one line: "Shared 214 threads with Acme this week, 4 held back." with a link to **What's
shared**.

## Who sees what

| | Member | Admin | Network |
|---|---|---|---|
| Records and timelines of Work | Yes | Yes | No (sealed) |
| Client threads | Yes | Yes | No (sealed) |
| Sensitive threads | No | No | No |
| Internal, Personal, Keep private, Only-you boards | No | No | No |
| Boards and threads shared by name | Only the people chosen | Only the people chosen | No (sealed) |
| Who publishes, when, how much | Yes | Yes | Yes (metadata) |
| A leaver's shared work | Yes, stays | Yes, stays | No |
| A leaver's other work mail | No | No | No |

## Dashboard

- **Mine / Team** on People, Organizations and Projects. Mine is the owner's own Graph; Team adds teammates' records.
- A quiet **via Sam** under a record a teammate shared ("via Sam and Kim", "via Sam (left)").
- **Ask Sam** on a teammate's record or tile.
- **Team / Only you** on each thread on a record's page. Tapping it shows why it went (or didn't), **Unshare** or
  **Share with the team**, **Share with…**, and a link to **What's shared**. **Keep private** on a record.
- **Share board…** on a board's ⋯ menu: the Fleet's confirmed teammates, one line on what they get ("Robin gets these 12
  projects with their full timelines, deals too. Personal and other companies never go."), and **Share** or **Stop
  sharing**. The board's header says "Shared with Robin".
- On a teammate's client thread, its attachments open from the dashboard (served as downloads, never run).

**What's shared**, a pane per Work Fleet on the Fleet tab (also in Settings):

- counts per kind;
- the first-share look, with **Keep private** and **Share now**;
- **Share these?**: the review's unsure threads in groups of one kind, named by the review with a suggested choice
  (**Share with team**, **Share with…** chosen teammates, or **Keep private**), one tap per group, opened to untick
  threads;
- every shared thread with its why-line and **Unshare**, and what is kept private;
- for admins, **Teammates** (who shares, who hasn't yet, **Take out**, **Share again**) and the switch **Share the Graph
  in this Fleet**, which everyone sees.

**The Fleet tab's Team Graph box:** for admins, "<name> joined <Fleet>. Share the team's Graph with them?" and new devices
with **Not theirs**; for everyone, their own sharing state with **Choose connections**.

## Unsharing

Nothing a teammate holds is copied anywhere else: records, threads and files stay in `team_records`, `team_mail` and
`team_files` and are read from there when shown, never into the owner's events, search index or to-dos. Deleting those
rows deletes all of it. Taking back works three ways:

- **Unshare a thread** (by hand, a rule, Keep private on a record, or a later review that makes it sensitive): the
  owner's Machine sends an empty `mail` blob for its tag and one per file, sealed and signed per recipient, plus a delta
  whose thread list no longer has it. Each receiver deletes the thread, its files and the copies it keeps to pass on. The
  records' timelines are rebuilt without its lines.
- **A Machine that was away**: the mailbox keeps blobs 30 days, and each Machine sends a snapshot of what it shares daily.
  A Machine back after longer gets the newest list and drops every thread not on it. A copy passed on late by a teammate
  is dropped when it is older than the publisher's newest list and not on it.
- **Turn off and remove shared data**: an admin's signed `pause` with `purged`. Every Machine deletes all it got from the
  Fleet, forgets what it sent and drops any older blob that still arrives. It is a trust statement, not a mailbox blob,
  so it reaches Machines that come back after any time. Once back on, each owner gets an hour to look it over again.

**Not taken back:** a member who stops sharing, or someone leaving, only stops what's new. What went stays with the
Fleet. Someone may already have read what was taken back.

## Someone leaving

- The directory drops them at once and every Machine stops sealing for them.
- An admin's Machine signs a `remove` for them, so a Network that later lists them again can't get anything sealed to
  them.
- Within a round the Fleet graph key rotates, so later blobs are sealed and hashed with a key they never had.
- What they shared stays with the Fleet, shown as "via Sam (left)". No other mail of theirs is kept for the company or
  sealed to admins.
- What they got from the Fleet is removed from their Machine once it sees it's no longer in the Fleet (`_graph_forget`,
  as `work_removal.py` does for company data). What they already read can't be unread.
- Someone taken out but still in the Fleet keeps what they got before and gets no take-backs after, since nothing is
  sealed to them any more.

## Threat model

**A compromised Network.** It can drop, delay or reorder what it carries, and see metadata: who is in the Fleet, who
publishes, when, how big, to whom, and how many threads each Machine shares. It can't:

- read: every blob is encrypted with a fresh key sealed (X25519) to each recipient Machine's pinned key;
- forge or change: every blob is signed (Ed25519) by the publishing Machine, and the seal binds the sender, the
  recipient, the kind and the blob id;
- replay an old blob as new: sequence numbers per publisher, checked by every receiver;
- add a member or a device: a Machine seals only to members confirmed by admin keys ([Trust](#trust-confirmed-members));
- bring back someone an admin took out: removal is a signed statement each Machine keeps;
- enumerate contacts: addresses inside records are keyed hashes (HMAC-SHA256 with the Fleet graph key, which the Network
  never has).

**A malicious member** can read what the Fleet shares with them: that's the point. They can't:

- write as someone else: a record carries its publisher, checked against the signature;
- overwrite others' fields: each Machine publishes only its own records; conflicts are resolved on each receiver
  ([Matching](#matching-and-conflicts));
- move a teammate's tile on that teammate's Machine: a stage move from a teammate shows as theirs on the Team board and
  never changes the receiver's own Mine board;
- get unselected Personal data, Keep private records or internal-only threads: those never go in a blob. Classification
  can be wrong, so this filter is not a cryptographic guarantee about what a message means;
- ask for more: there is no query; every Machine pushes what it shares.

**A malicious admin** can confirm a fake member. That is the trust root: admins are trusted, as in
[shared connectors](network.md#shared-connectors).

Out of scope: a compromised Machine of a member (it sees what that member sees), a compromised admin, traffic analysis.

## Trust: confirmed members

Shared connectors confirm admins by Machine keys: the owner's root, then admins vouched for by a confirmed admin. The
Shared Graph adds these statement kinds to `fleet_trust.py`, each signed by a confirmed admin's Machine:

- `member`: `{t: member, fleet, member, key, by}`, after their owner's OK ("Share the team's Graph with <name>'s
  Machine?", with their key's fingerprint). Confirmed admins are confirmed members.
- `remove`: `{t: remove, fleet, member, by, at}`, when someone leaves the directory or an admin taps **Take out**. Each
  Machine keeps the newest per member. A removed member counts again only with a `member` statement dated at or after
  the removal (**Share again**).
- `pause`: `{t: pause, fleet, member, key, by, on, at, purged?}`: the **Share the Graph in this Fleet** switch. The
  newest wins. `purged` is when an admin last picked **Turn off and remove shared data**; every later statement carries
  it, so turning sharing back on can't hide a removal from a Machine that was away.
- `policy`: required connections ([What feeds it](#what-feeds-it)).
- `optout`: `{t: optout, fleet, member, key, by, asked, at}`, an admin's OK on a member's ask to stop sharing. It counts
  only from an admin other than that member, for their current key and that very ask. Members now stop by turning their
  connections off; old asks are still honored, and admins still see them ("<name> asks to stop sharing their Work with
  the team.").

**One decision per person.** An admin OKs a person when they join ("<name> joined <Fleet>. Share the team's Graph with
them?", or **Share with all**). After that there is no OK per device: a new key of a person already admitted is vouched
for by an admin's Machine by itself after 24 hours (`REKEY_HOLD`). During that time admins see "<name> has a new
Machine" with its safety number and can tap **Not theirs**, which keeps the key out.

An OK returns as soon as its statements are signed and sent. Sealing the team's Graph for them follows in the next graph
round; until then the Team Graph box says "Sharing with <n>…" (`sending`).

**Confirmed** means: in the directory now, with a key a confirmed admin vouched for, and not removed since. Pins are kept
between rounds, so a member vouched for by an admin who later left stays confirmed. A Machine seals only to confirmed
members and opens only blobs from them.

Residual risk: a Network that hides a `remove` from the start can keep other Machines sealing to that person for as long
as it also keeps them in the directory. The removing admin's own Machine stops at once, and once any Machine has seen the
`remove` the Network can't undo it there.

## Data model

On each Machine, next to the Graph:

- `share_threads(thread, verdict, line, with_name, hand, hand_at, event_id, account_id, at)`: the review's verdict per
  thread, its one line, and the owner's hand choice (team or private).
- `share_private(node_id, at)`: Keep private.
- `team_records(fleet, member, rid, kind, body, at)`: what teammates shared, opened, one row per record.
- `team_mail(fleet, member, tag, body, at)`: client threads teammates shared, opened.
- `team_files(fleet, member, tag, name, mime, size, data, at)`: their attachments.
- `team_asks(fleet, member, off, asked, at)`: members' asks to stop sharing.
- `team_blobs`, `team_pending`, `team_wants`: blobs kept to pass on, blobs waiting for their sender's confirmation, and
  catch-up asks.
- `share_out(fleet, kind, key, hash)`: what this Machine published, to send only changes and to go on where a backfill
  stopped.
- `fleet_meta` keys: graph keys by version, sequence numbers, cursors.

With message protection on, teammates' records, mail, files and the review's lines are sealed at rest with the message
key, like the owner's own mail (`message_seal.DERIVED`).

A record (JSON, inside a blob):

```
person:  {r, t: person, name, name_hand, role, role_hand, org: {name, d}, ids: [hash], d, score, last, timeline: [{at, line}]}
org:     {r, t: org, name, role, role_hand, d, score, last}
project: {r, t: project, name, board, stages, stage, stage_hand, stage_at, why, next, org, people: [hash], score, last, timeline}
mail:    {tag, subject, messages: [{at, from, to, cc, body, attachments: [{name, size, mime, file | too_large}]}]}
file:    {name, mime, data}                                   (one attachment; `file` above is its tag)
ask:     {off, asked}                                         (a member asks to stop sharing, or not any more)
```

`r` and `tag` are HMAC(publisher secret, local id): stable per publisher, meaningless to others. `ids` and `d` are
HMAC(Fleet graph key, address or domain), under each of the newest few key versions the publisher holds, so two
teammates still match while a new key version reaches everyone. `score` is the publisher's closeness.

## Sync protocol

A **blob** has a header in the clear and an encrypted body:

```
header = {v: 1, fleet, from, id, seq, kind, at, to: [member ids], kv, tag?}
kind   = key | snapshot | delta | mail | file | ask
body   = AEAD(DK, json)                  DK: 32 fresh random bytes per blob
         HKDF-SHA256 -> encryption and MAC keys, HMAC-SHA256 counter stream, MAC over header + nonce + ciphertext
sig    = Ed25519(publisher, "tm-shared-graph/1" + header + sha256(ciphertext))
wraps  = {member: seal({dk, h}, publisher, member, {p: graph, k: kind, f: from, t: member, r: id})}
```

The seal is the Network's own (`network_crypto.seal`). `h` is the hash of header and ciphertext, so a wrap can't be moved
onto another blob.

### Kinds

- **key**: from a confirmed admin, the Fleet graph key `{kv, key}`. The first confirmed admin Machine that finds none
  makes one. Any confirmed admin seals it again for a newly confirmed member and makes a new version when someone it was
  sealed for left. Receivers keep every version and match with all of them; publishers use the newest.
- **snapshot**: all of a Machine's shared records and the tags of its shared threads. Replaces what came before from that
  Machine. Sent when the recipients or the key change, and daily.
- **delta**: changed and removed records since the last blob, with `prev` (the previous seq). A receiver that missed one
  waits for the next snapshot.
- **mail**: one client thread, by `tag`. A newer blob with the same tag replaces it; an empty one removes it. A receiver
  drops mail whose tag isn't in the publisher's latest snapshot.
- **file**: one attachment of a shared client thread, by `tag`, up to 2.5 MB. A sensitive or private thread's files are
  never even read. Removed (an empty blob) when its thread stops being shared.
- **ask**: a member's ask to stop sharing, or that they withdrew it. Only admins' Machines act on it.
- **want**: a Machine asks its teammates for what it missed ([Catching up](#catching-up)).

### Publishing and receiving

Each Machine publishes every few minutes when something changed and fetches with a cursor. The Network's inbox reports
the newest wrap cursor (`graph=`), so a Machine fetches only when there is something new for it. A receiver opens a blob
only when:

- the sender is a confirmed member and the signature checks with their pinned key;
- the wrap opens and its `h` matches;
- the seq is newer than the last one taken from them;
- the header's fleet and `to` include it (or a confirmed teammate passed it on, for a catch-up).

A blob from someone not confirmed yet waits in `team_pending` and is tried again each round for 7 days.

### The Network as a mailbox

Everything stays on the Machines; the Network only passes blobs on. A receiver acks what it took and the Network deletes
its wrap. A blob goes once every Machine it was sealed for took it; anything nobody took goes after 30 days.

There is no storage cap, only a limit per blob (4 MB) and on what a Fleet has in flight (500 MB). At that limit the
oldest of whoever has the most waiting goes first. The Network checks what it can without reading: the sender is a Work
member, `to` and the wraps name current members, `key` blobs come from an admin, sizes and rates are within limits.

### Catching up

Each Machine keeps the blobs it has as their publishers signed them (`team_blobs`: the last snapshot and the deltas
since, and the newest of each thread and file), so it can pass them on.

- A Machine that was away longer than 30 days, or one just confirmed, sends a sealed `want`: which records it has of each
  teammate and how far back it got their threads.
- Any online teammate's Machine answers from its own copies: each publisher's records first, then threads and files,
  newest first, a batch a round, going on where it stopped. A long snapshot and delta chain goes in ordered parts within
  each round's budget.
- A blob passed on is the publisher's original, still checked against their signature; only its key is sealed again, for
  the one who asked. What someone who left shared is passed on only by an admin's Machine.
- Signed empty mail and file blobs are kept as removal markers, so an older copy passed on later can't bring a removed
  one back, and an offline teammate gets the removal when catching up.
- Two teammates answering the same want is fine: the Network skips a blob already waiting for that Machine, and the
  receiver drops what it has.
- A failure listing a thread's attachments leaves the thread unfinished for a retry; files already shared aren't
  downloaded twice.

### Matching and conflicts

A receiver matches teammates' people by hashed address, organizations by hashed domain, projects by board and name. For
each field of a matched record the value set by hand wins; otherwise the value from whoever is closest (highest score).
Stages are facts with dates: the newest move by hand wins, else the newest move a message showed. The Mine view never
changes: Team is a view over Mine plus what teammates shared.

## Shared boards

Boards with the same name become one team pipeline. A tile is a project; its stage moves come from anyone's mail (the
review on each Machine moves its own copy, which it publishes). Each tile has an **owner**: the teammate closest to it.
**Ask <name>** on a tile, person or organization starts a handoff to that teammate (`fleet_requests.py`), never anything
to someone outside the Fleet.

- A tile on a teammate's Machine says what happened last: the newest line of the project's shared timeline, else why it
  moved, else its stage and date. The owner's name shows only when a column has more than one.
- **Mine / Needs me / All** filter a shared board from what reached this Machine only. Mine is a shared thread the owner
  is on, a project they own or have in their own Graph, or an open to-do of theirs for it. Needs me is that to-do, or a
  thread whose newest message is to them from someone else.
- The rest of a stage folds into "Show N more", and look-alike names (three or more with the same last or first two
  words) into one row.

Nothing more is shared for any of it (`SharedGraph.team_boards`).

## Migration

1. Machines on this version publish their root (owner) and their keys, as with shared connectors.
2. An admin's Machine asks once per person: "<name> joined <Fleet>. Share the team's Graph with them?". Until then
   nothing goes to them.
3. Every thread no hand choice covers is sorted again with the current rules (sorter v2); sensitive stays sensitive.
   Threads that went before are sorted first and stay with the team until then; after that they stay or are taken back.
   Anything a rule already says no to (another company's connection, automated mail, personal, kept private) is taken
   back at once.
4. A Fleet that shared before the switch existed stays on: a Machine that sent to it before treats it as on until an
   admin says otherwise, and the first admin Machine on this version signs the switch on once (`_was_sharing`). A
   Machine that never shared gets its hour to look it over first.
5. Past threads: all the Work history the Machine has, judged by the history pass, in batches.
6. Machines that haven't updated publish nothing and get nothing; "who knows someone" keeps working.
7. Nothing is imported from or written to another CRM.

## Decided

1. No admin escrow. When someone leaves, the Fleet keeps exactly what they shared, nothing more.
2. A member stops by turning their connections off. Keep private on a record needs nobody's OK.
3. Attachments go with a shared client thread, sealed the same way, up to 2.5 MB each. In a Careful Fleet (security
   level) they don't: the thread lists them as not shared.
4. History: as far back as the Machine has Work mail, through the same labels, in batches that resume.
5. A look first: the first share goes an hour after the owner is told, and each new client thread waits an hour.
6. One trust decision per person, when they join; no OK per device. Removal is signed.
7. Everything stays on the Machines. The Network is a mailbox: a blob goes once every Machine took it, or after 30 days.
   Machines catch each other up.
