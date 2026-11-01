# Context, people, projects and learning

[Documentation index](../README.md). Current reference; dated repair evidence lives in [History](history.md).

This page covers how The Machine builds its picture of who you deal with ([People and projects](#people-and-projects)),
the optional extras that add to it ([Related signals](#related-signals-optional-local-embeddings),
[Organization data](#organization-data-optional-enrichment), [People data](#people-data)), and how it learns
([How you write](#how-you-write), [Keeps learning](#keeps-learning), [Fixed at the source](#fixed-at-the-source),
[Sharing learnings](#sharing-learnings)).

## People and projects

A living map of who you deal with and what's going on, across every account.

- `graph.py` rebuilds it from scratch every ten minutes (and soon after a label or merge), as a pure function of the
  signals, your to-do decisions, project labels and merges. So a rule change also applies to the past.
- It needs no setup, and nothing leaves the Machine (unless you turn on
  [organization data](#organization-data-optional-enrichment)).
- A rebuild over 5,000 signals with probable links and unnamed work takes under half a second.

### People

People come from identifiers only: email addresses (Gmail, Calendar, Intercom, Salesflare contacts), WhatsApp numbers,
Slack users, LinkedIn and X conversations, GitHub logins.

Left out:

- your own addresses ([below](#your-addresses)) and your own name on other channels;
- shared role addresses at your domains (info@, support@);
- newsletters (Gmail Promotions, Updates, Social and Forums, no-reply and mailing senders, unless you ever wrote to
  them), bots and mass mailings (over 20 recipients);
- system and relay addresses, even when you wrote to them: Intercom's Operator bot and its reply relays, no-reply and
  notification senders (Slack, Google Calendar, GitHub), GitHub's noreply addresses and reply+ relays (`graph.relay`).
  A support conversation the Operator bot opened counts for the customer who wrote in it.

<a id="your-addresses"></a>
### Your addresses

Who counts as you (in timelines, participant lines, "You:" labels, boards and the Graph) is every address of yours, not
only the ones in config (`own_addresses.py`). Each graph build finds them in the sources already connected:

- your own mailboxes and calendars (never one shared from a Fleet, never someone else's calendar you can see);
- Gmail send-as aliases (read once a day with the `gmail.readonly` scope mail already has) or Outlook proxy addresses
  (`User.Read`);
- the `self` attendee on your own calendar, and your Slack and Intercom profile address;
- an address at its own domain that mail from at least two people lands under in your mailbox, carrying your full name
  (a Google Workspace alias never added as a send-as address).

**Never yours:** a shared address (one a teammate in any of your Fleets uses too, one mail comes from under several
people's names like a Google Group, or one Gmail sends through someone else's account).

**Maybe yours.** When unsure it doesn't count either: a role-like address (info@, sales@, support@, team@), a send-as
address that isn't set as an alias, one only seen in mail you sent, or one that only carries your name. Those are under
**Maybe yours** in Settings, Account, with three choices and nothing picked for you:

- **Mine: I handle it**: it counts as yours.
- **The team's: others pick it up too**: it is never you. Mail that only went to it, in a thread you didn't write in,
  gets a `team_inbox` note in the review and no to-do (so no draft). The Graph treats it as neither you nor a person, so
  its threads still fill in the Graph and Fleet sharing stays as it was.
- **Not mine**: it never counts.

**Change** on the row switches it later. Your own sign-in and config addresses can't be the team's or removed. **Your
addresses** lists the rest with where each came from, and **Remove** on any found one. `owner_emails` (top level or per
account) always counts and `not_owner_emails` never does. The addresses found stay on your Machine: the Network still
only hears your work accounts' addresses.

**Sending from an alias.** A draft's From is the mailbox address, or one of your addresses (yours, not the team's) that
Gmail lists as verified send-as for that mailbox and doesn't send through another account's server
(`own_addresses.senders`).

- The review shows it as a picker. A reply to mail that came to such an alias starts from it
  (`next_actions.pick_sender`); new mail starts from the mailbox address.
- The send check reads that send-as entry from Gmail again (`sendAs.get`) and sends nothing unless it is `accepted`
  right then.
- Outlook drafts only go from the mailbox address: Graph's proxy addresses say where mail arrives, not what the mailbox
  may send as.

### Who is who

- **Slack users** are looked up once a month (`users.info`, a few per Slack page); their email joins them to their mail.
- **Names are only names.** What people or their tools add is dropped: "Kim Lee (Initech)", "Ann Bell | Acme", "Sam at
  Globex", "via LinkedIn", emoji, a degree. "Doe, Jane" becomes Jane Doe.
- **One name, one person.** The same full name on two different channels is one person, unless two people on one
  channel carry it. The agent's `graph` `merge` or `different` (two person ids) overrides either way.

### Same person?

Identities join by themselves only on strong evidence:

- the same full name on two of them in one message or conversation (someone writing from work with their own address
  in CC);
- the same LinkedIn profile found for both by a lookup;
- their WhatsApp number in mail they wrote themselves (not in quoted mail) with a matching name;
- their Slack profile's address;
- the same full name with one person carrying it per channel.

A name alone never joins two identities on one channel. Weaker evidence is only a question: the same full name that two
people on one channel carry, or a similar name ("Ann" and "Ann Lee", a nameless jane.doe@ and Jane Doe) with something
shared besides (the same company domain, people seen with both, a project, the same role).

- The person page asks it quietly ("Same person as …?"), and People lists them under **Same person?** with **Merge** and
  **Not the same**. Not the same is remembered (`graph_merges` `same=0`).
- **Merge all** merges every listed pair in one go (`graph_same_all`); one Undo splits that batch and asks again.
- A merged person keeps every identity, signal, role, note, project and photo. Their page lists why they are one
  (**Joined from N identities**), each join with **Undo**, which splits them for good. An old link to one of their
  identities opens the merged person.
- Someone deleted permanently is never merged or asked about again. The build keeps the questions in `graph_same`.

### Closeness and rhythm

**Closeness** adds per day of contact, capped at 1 a day, so a burst of chat messages is one day:

| Signal | Adds |
|---|---|
| You writing | 0.6, split over recipients |
| Them writing to you | 0.3 (0.15 by email until you've written to them) |
| A meeting | 0.5, split over attendees |
| Present in a group or CC | 0.05 to 0.15 |
| Do it, Send or Mark done on a to-do about them | +1, once per to-do |
| A Change note | +0.5 |
| Not relevant or Wrong facts | −0.5 ("Already handled" counts neither way) |

Everything fades by half every 60 days (`strength × ½^(days/60)`); below 0.01 it isn't stored. Labels: close (3+),
regular (1+), occasional (0.3+).

**Rhythm.** A contact day has contact between you and them (a message either way, a meeting), counted in your time zone
(`timezone`). Signals they're merely on, like a teammate answering a customer, don't count, and "last contact" follows
the same rule ("last seen" for someone never in direct contact).

- Each person's usual gap is the median of their last eight gaps between contact days.
- Someone you wrote to on at least two days has **gone quiet** when the silence is longer than three times their usual
  gap and at least two weeks (and under a year).
- Future meetings show as "next meeting" on people and projects. A project's "last signal" is never in the future.

### Projects

Projects are named by the review agent (`finish_analysis` `projects: {"name": [event_ids]}`, `suggest` `project`) and
with `graph` `project` + `event_ids`. `begin_analysis` returns the live names to reuse.

- A label spreads to the rest of its thread (email thread, Slack thread, Intercom conversation, GitHub issue, recurring
  meeting; chats within two days).
- Heat is 0.2 per signal plus your to-do decisions, fading by half every 21 days. The state compares now with two weeks
  ago: heating up, active, cooling, dormant.
- `close_project` ends one; naming it again reopens it.

**Probably part of a project.** A signal no label reached that reads like a labeled one (local embedding cosine ≥ 0.72)
and shares a person with it is shown as probably part of that project, at half weight (heat 0.1, a person's part 0.15).
Meaning alone isn't enough, since it groups by genre. Meetings and closed projects are left out. Review batches show the
guess as `probably_project`; a review that agrees names it in `finish_analysis` `projects`. The Graph tab marks those
signals "probably part of it". It needs [local embeddings](#related-signals-optional-local-embeddings).

**Unnamed work.** Threads from the last 45 days with no project that read alike (cosine ≥ 0.75 between thread averages)
and share a person form a group when it spans three or more threads, at least two of them not meetings, and you wrote
or met in one. Chats are left out, and a person on more than 150 threads links nothing. Up to two groups go into a
review prompt as "Possibly one piece of work nobody named", each once (again only after it has doubled); the review
names it with `graph` `project` or skips it.

**Links.** People seen together on a signal (2 to 8 people, half-life 45 days), a person's part in a project (0.3 per
signal, 45 days), organizations by non-freemail domain (named from CRM accounts when known).

### Boards

Projects of one kind in stages (partner listings, onboarding, support escalations), shown on Graph, Projects as a board.
Board is the default view and List is one click away, remembered on that device. The board only shows: it never sends
anything.

**Making a board.** Only the owner makes one: from scratch (the board's ⋯ menu, New board) or by saving a suggestion.

- **Suggestions.** When at least three open projects on no board are clearly of one kind, a review suggests a board for
  each clear group, up to three open at once, each once, with `graph` `suggest_board: {name, stages, about, projects,
  reason, visibility}`. Every open project on no board is listed for one review a day under "Boards to suggest"; that
  review answers in `finish_analysis` `boards` ("suggested" or "none: why").
- **Splitting first.** A project that holds several counterparts (one "acquisition" project with five buyers) is first
  split into one project per counterpart: `graph` `split: [{project, event_ids}]` (up to 40, one graph build after).
- **Stages** fit that work and end at the good outcome (hiring: Sourced, Screening, Interviews, Offer, Hired). A lost
  or declined ending goes in the **Stalled or declined** row, never a stage. Judged from what the projects are, not
  the words in their names.
- **Who sees it** (`visibility`): `only_you` for M&A, buyers, investors, legal, health and hiring a named person; `team`
  for customer, partner and other pipelines. An Only-you board says "Only you" with a lock. A project's page sets who
  sees that project (`project_visibility`; empty follows the board).
- Projects shows each suggestion as "Start a board for Hiring?" with its stages, Only you or Team, **Save**, **Edit**
  and **Not now**. A name dismissed with Not now is never suggested again; nothing is a board until saved
  (`board_suggestions`).
- **The editor** sets the name, stages (rename, reorder, add, remove, up to 8), the optional Stalled or declined row, a
  line on which projects belong (`about`), who sees it and the projects on it. A removed stage's projects go to the
  nearest earlier stage, and the toast says so. Deleting a board keeps its projects.

**Sorting.** A saved board's projects are sorted within minutes: a review starts for them even without a full batch of
new signals (`sort_gap_seconds`, default 60) and gets them at the top of its prompt as "Boards to sort".

- It places each one with `graph` (stage, `event_id`, `reason`), the first stage too when nothing moved it further, or
  answers `finish_analysis` `sorted: [{"project", "why"}]` when no message shows where it stands. `finish_analysis`
  refuses until each one is answered.
- The tile says "Sorting from its messages…" while that is due, then the reason and its message, or "Not sorted: why".
  When the review fails it says "Sorting failed, trying again", and after 3 reviews "Couldn't sort it in 3 reviews"
  (`sort_run`, `sort_tries`, `sort_note`).

**Moves.** A review moves a project with `finish_analysis` `stages: [{"project", "board", "stage", "reason",
"event_id", "next", "org"}]`. It judges what a message means, never its wording, and never moves a project only because
time passed.

- Each move keeps its reason and message (`project_moves`); the tile shows "Moved to In review: … · Fri, Oct 23" and
  opens that message.
- The owner drags a tile, or picks a stage from its ⋯ menu on a phone. That move stands until a newer message moves the
  project again; an older message never undoes a newer move.
- A tile shows how long the other side hasn't answered since the owner wrote ("No reply in 14 days", from 10 days) and
  links an open to-do about it.

**Which projects belong.** Open projects on no board are listed for a review as "Projects that may fit a board" (up to
40 at a time, while a board changed in the last 30 minutes or any are unchecked).

- The review places each one that fits with `graph`, or answers `finish_analysis` `fits: [{"project", "board", "fit":
  "maybe"|"no", "why"}]` (`board_fits`). Each fit names its board, and each board is judged by its own purpose.
- A maybe shows on the board as "N projects could belong here" with **Add** and **Leave out** (`board_fit`). A project
  left out is not asked about again.
- A maybe that bundles several counterparts carries `"split": true`. Its row says "Add as N", and Add makes one project
  per counterpart, puts each in the first stage and closes the emptied bundle.
- `board_fit` also takes `node_ids` (up to 200) for Add all, Leave out all or a selection. Every decision returns an
  `undo` token that `board_fit` `{undo}` takes back within a day.

**Looking through the history.** A new board also looks through the whole history once (`board_backfills`).

- Every organization, or person without one, with messages or meetings in no project yet (leaving out colleagues and
  anyone an open project is with) is a candidate. They are ranked once, by meaning with local embeddings, else by how
  many messages they have, at most 400 per board.
- Each review gets the next 30 (about 14,000 characters) as "Looking through the history for new boards". It makes each
  that clearly fits one project per organization on the board, or answers it in `finish_analysis` `fits` with its key
  (`org:<domain>` or a person id).
- Each candidate's line says how you and they talk, or "inbound only". Inbound work for you (a trial, a product
  question) can go on a board; unsolicited outreach pitching you is at most a maybe that says so. A maybe's `why` names
  who and what happened with a date ("Pitched them on Oct 12, no reply yet").
- A maybe makes no project until **Add**.
- While a look runs, reviews start every `backfill_gap_seconds` (default 180), but only while no window of the model's
  limits is past 80% used. It is done once every candidate has an answer (or after 7 days). The board header says
  "Looking through your history…", then for 3 days "N added from your history · M to review".
- Projects made for an Only-you board follow it, so nothing reaches the team that the board doesn't allow.

**By hand, like a CRM.** The owner runs projects like deals: `project_save` (name, board and stage, `org`, `value`,
`notes`, `people`), `project_outcome` (won or lost with why: won to the last stage, lost to Stalled or declined),
`project_archive`, `project_delete`, `board_default`. From the board header, a lane's + Add, a tile's ⋯, the list, a
project's, person's or organization's page and the command palette. A project the owner made stays in the graph before
it has messages (`made_by`).

**Tables:** `boards` (with `about`, `side`, `visibility`, `is_default`), `board_suggestions`, `project_moves`,
`project_people`, and on `projects`: `board_id`, `stage`, `stage_reason`, `stage_event_id`, `stage_by`, `stage_at`,
`next_step`, `org`, `value`, `notes`, `made_by`, `outcome`, `outcome_reason`. They are added on start; back up the
database before upgrading.

### Where someone works

Their work email domain, or what a source states plainly: their LinkedIn headline (kept as `headline`, shown as is), an
email signature, or them saying where they work in their own message.

- A review or the organizations pass sets `graph` with `node_id`, `org` (the name as stated, or an `org:…` node_id),
  `event_id` and `quote` (the words that say it). The service refuses a quote that isn't in that message or headline,
  and the owner's own messages.
- It is kept in `person_orgs` with where and when it was said. The person page shows "At Acme · from their LinkedIn
  headline, Oct 15" with a link to the organization.
- A stated name joins the organization with that name or domain, or stands as its own (`org:named:acme`, never looked
  up). The owner's own company marks a colleague instead.
- A work address wins over a review's statement; your own word (Edit or Add on the person page) wins over both.
- Nothing else is read from it: no seniority, no role. Reviews get up to five people with a headline and no
  organization, each once a month; one organizations pass (`profile_runs` kind `orgs`) runs once per install.

### Roles

What someone is to you: only what you say on the dashboard (Graph tab, a person, Edit) or what a review reads in a
message (`graph` with `node_id` and `role`, a few words: "accountant", "CFO at Globex"). Your word stays until you
change it.

Sources don't set one: being in the CRM, paying through Stripe or sharing a surname says too little. Instead:

- Each review gets up to five of the strongest people with no role (closeness 0.5 and up, each asked again after 30
  days) with those facts as hints, and sets a role only when the messages show it. The dashboard marks those "a review
  read it in your messages".
- Onboarding does the same up front: after the `USER.md` draft, `assistant profile` starts a roles run for the 15
  closest people with no role, three per page with their closeness, organization, projects, hints and first and latest
  direct messages. `assistant roles` runs only that step, for example after connecting more sources.
- Stripe events add their customer as a faint contact and name the organization when the CRM doesn't.

Roles show on people in the Graph tab, in preparation context, `graph` results and the recap's gone-quiet line.

**Kept honest:**

- **Evidence and Who's who.** A review gives the message it read a role in (`event_id`) and a short `quote` copied from
  it; the service refuses a quote that isn't there. The Graph tab's **Who's who** lists the review roles you haven't
  confirmed, closest first: **✓ Right** makes it your word, Edit changes it, **✓ All N are right** confirms them all
  after one check. The weekly recap counts the ones waiting.
- **Learning from corrections.** When you replace a review's role, `role_corrections` keeps the old and new one; the
  roles run and the review prompt get the latest eight as examples.
- **Just in time.** People on open to-dos with no role are asked first in reviews. `suggest` answers with `no_role_yet`
  for the people on a new to-do, and a Do it job's context names them.
- **Organizations** get a role too (`graph` `node_id` `org:…`: "accounting firm", "customer", "possible acquirer").
  People there carry it in preparation context ("at Globex (customer)"). Each review gets up to two organizations with
  no role; one is asked again as soon as one of its people gets a role.
- **Rechecks.** A review's role is offered again (at most three per review) when it was read more than 90 days ago and
  there was contact since, when new hints showed up, or when it was saved without its line. Your own roles are never
  rechecked.
- **Relations.** `graph` with `node_id`, `related_to` and `relation` ("assistant of", "sister of", "introduced by")
  links two people (`graph_relations`). Both pages show it with Remove.
- **Email warm-up traffic.** When a review reads that an organization's mail is only a warm-up tool's templated
  exchanges, it sets `graph` `warmup` (`hidden_domains`). That domain and its people leave the graph and aren't looked
  up. Organizations' **Warm up** tab lists them with Undo.

**Used.** Preparations write to each person as you would to who they are. Open to-dos sort by deadline, then by who
they're about (closeness, +2 when their organization pays through Stripe). The recap's gone-quiet line falls back to
the organization's role.

### On a person's page

- **Names.** Edit on a person's or organization's page, or Rename on a project's (owner only). A name is kept in
  `graph_names` and wins over the names in their messages; an empty one gives that back. Renaming a project to another
  project's name joins the two.
- **Fleet, Family and Friends.** Someone in one of your Fleets, your Family or your Friends gets a small marker ("Has a
  Machine · Work Fleet (Acme) · Friend"). See [In your Graph](fleet.md#in-your-graph) (`graph.fleet_marks`,
  `graph.with_fleet`).
- **Open between you.** Open promises both ways (Done and Drop) and open to-dos on their signals (for a project also
  to-dos with its name). Preparation context adds one "open:" part per person and project.
- **Summary.** A few short lines on who they are to you, where things stand and what is open both ways
  (`person_summary.py`). See [Summaries](#summaries).
- **Known about them.** Facts about them, apart from what is open, each with **Not about them** and **Forget**. A fact
  is about its subject, never about whoever sent the message (`fact_about`, set with `remember_fact` `about`). You are
  never a node, so a fact about you stays in Learning, What I've learned.
- **The page itself** keeps the dashboard's header and tabs, with a breadcrumb back (Graph › People › name). Each page
  has its own link, `#graph/<node id>`, and the browser's back button works. Its events come by day, coming up first.

### Summaries

`person_summary.py` rewrites summaries in the background, never on every signal:

- Every ten minutes the service checks for people with real activity (three or more direct signals in 90 days,
  closeness 0.3 and up) whose facts, promises or signals are newer than their summary.
- At most once an hour, up to six of them go to one turn on the background model: at most eight passes a day, each
  person at most once every 20 hours, only when the budget allows.
- Each line must cite its sources (`E` a signal, `F` a fact, `P` a promise). A line without a known source, or one that
  only repeats what the page shows above it, is dropped. A line whose source is deleted disappears.
- Your edit wins: a rewrite then shows a **Suggested update** with Use it and Keep mine. **Let The Machine write it**
  gives it back.
- Preparations add a "summary:" part with only the lines whose sources are in the to-do's area (a personal line never
  reaches a Work to-do). The Team Graph and Fleets never get it.

Tables: `person_summaries` (`lines` and `proposal` sealed), `person_summary_runs`.

### Shared with your Work Fleet

In a Work Fleet, Work records, short timelines and client threads are shared with the team (`shared_graph.py`). The
review judges each Work thread on its own (`finish_analysis` `team`), and older Work threads in a history pass
(`assistant profile_evidence` and `save_profile` with `team`). A thread you set to Team or Only you keeps your choice.
See [Shared Graph](shared-graph.md).

### Tables and uses

**Tables.** `projects`, `event_projects`, `identity_names`, `graph_merges` (with `source`), `graph_same` (recomputed),
`person_roles` (with `event_id`, `quote`, a `hints` snapshot and `checked_at`), `role_corrections`, `graph_relations`,
`graph_names`, `graph_offers` and `graph_role_asks` hold what was said, offered or asked. `graph_nodes`, `graph_links`,
`graph_events` (with a `probable` flag; readers show at most 40 recent signals), `graph_unnamed` and `graph_state` are
recomputed. `suggestions.project` keeps a to-do's project.

**Uses.**

- The agent's `graph` action: no args for an overview; `query`; `node_id` with links, recent signals and spreading
  activation two hops out; `event_ids`.
- A "People and projects" block in each Do it job message: who the people on the task are, their rhythm, projects and
  who they're often with.
- The Graph tab: `/api/graph` (`?q=` with `&cursor=`, `?node=`) and its lists, 30 at a time, from
  `/api/graph/list?list=people|quiet|new|orgs|warmup|projects|projects_done&sort=closest|last|name|stage&cursor=`
  (answers `items`, `next` and `total`; the overview's `list_counts` has each list's count).
- The weekly recap.

## Related signals (optional, local embeddings)

Off unless you set it up. Full-text search finds the same words; this finds the same *meaning*: a reply worded
differently, the same topic in another source, an answer that already came in.

- Reviews and Do it runs get a `related` action that looks up signals by meaning, only within the accounts the call
  names.
- A Do it job message ends with a short "Possibly related" list from the task's own accounts when there are close
  matches.
- **Nothing leaves your Machine:** signal text goes only to an embedding server you run on `127.0.0.1`, never to a model
  provider.

### Setup

1. Run an embedding server on loopback. Any OpenAI-compatible `/v1/embeddings` endpoint on this computer works (one that
   also lists its model in `/v1/models`). The tested one is llama.cpp's `llama-server --embedding` with an
   EmbeddingGemma GGUF, for example `embeddinggemma-300M-Q8_0.gguf` from
   [`ggml-org/embeddinggemma-300M-GGUF`](https://huggingface.co/ggml-org/embeddinggemma-300M-GGUF) (about 330 MB). If
   OpenClaw's local memory search is on, reuse its model file (`memory.search.local.modelPath` in `openclaw.json`,
   often in `~/.cache/qmd/models/`) and its bundled `llama-server` under `~/.openclaw/tools/llama.cpp/`.
2. [`deploy/embeddinggemma.service`](../deploy/embeddinggemma.service) is an example systemd user unit: bound to
   `127.0.0.1:8792`, `Nice=10`, low CPU and IO priority, `MemoryMax=2G`. Set the binary, model path and name in it (or
   in `~/.config/embeddinggemma.env`), then `systemctl --user enable --now embeddinggemma`. Check it with
   `curl -s 127.0.0.1:8792/v1/models`.
3. In `config.json`: `"embeddings": {"url": "http://127.0.0.1:8792", "model": "embeddinggemma-300m", "dims": 256}`.
   `model` must be the name the server reports (llama-server's `--alias`); the service refuses a server that serves
   another model. Optional: `floor` (cosine for signal-to-signal matches, default 0.6) and `query_floor` (for a text
   query, default 0.4). The installer adds this block with `enabled: false`: set that to `true` (or drop it), then
   restart the service.
4. Embed what you already have: `python3 assistant.py embed-backfill` (oldest first, with progress; `--batch` sets
   events per call). It's safe while the service runs; the service itself embeds new and changed signals in the
   background, newest first.

### How it works

- **Vectors.** `event_vectors` holds one normalized float32 vector per event version (Matryoshka-truncated to `dims`),
  deleted with its event. Changing `model` or `dims` re-embeds.
- **What is embedded.** The title plus the first 2,000 characters of the body, without quoted earlier messages and
  invisible format characters.
- **Fitting the server.** Each input is cut to `max_input_tokens` (2,048 by default; 8,191 for api.openai.com), counted
  as one token per UTF-8 byte, the worst case (`bytes_per_token` raises that). A request holds up to
  `max_batch_tokens` (8,192; 300,000 for OpenAI) and `max_batch_inputs` (64; 2,048). A signal the server still refuses
  is set aside (`event_vector_skips`) and tried again after a day or when it changes.
- **Queries.** `assistant_signals related` takes explicit `account_ids` and `event_ids` and/or a `query`, `limit` up to
  20 and optional `exclude_event_ids`, and returns the `events` shape plus a `similarity`. With a query, the meaning
  ranking is fused with full-text ranking; `events` with `semantic:true` uses the same. `account_ids:["all"]` searches
  every account (for `events` and `related` only).
- **Search on the dashboard.** The Cmd+K search covers all accounts by default, by meaning and words together, and
  labels each result with its account.
- **When the server is down**, the service logs `embeddings error=<class>` and retries after five minutes. Queries still
  get keyword matches, and nothing else is affected.
- **What was learned, per task.** The facts and draft rules you taught it get a vector each too (`fact_vectors`). Once
  there are more than a few, a Do it run gets the ones learned on its to-do plus up to 8 closest in meaning (cosine 0.3
  or more), not the whole list. Without embeddings it gets the newest that fit.

### Costs

- No GPU needed. On CPU the server embeds a few signals per second: a first backfill of 5,000 signals takes about 30 to
  40 minutes on a 4-core desktop CPU, and each new signal well under a second.
- The model takes about 0.3 to 0.5 GB of RAM while the server runs and no CPU when idle.
- On a small 2-core arm64 server (October 2026) it was slower and bigger: about 130 tokens a second on one core (a few
  thousand signals take a few hours once), and 370 MB idle growing to 850 MB while embedding with `--no-repack`, or
  300 MB more without it. A first `openclaw memory index` (below) took another 940 MB. Next to OpenClaw and a browser
  that is tight on 4 GB of RAM; 8 GB is comfortable. Give the unit its own `MemoryMax` and `MemorySwapMax=0`, so the
  kernel ends it alone when it grows too big and systemd restarts it.
- Vectors are about 1 KB each at 256 dimensions (5 MB for 5,000 signals). Search is brute-force cosine in plain Python,
  about 0.1 s over 5,000 vectors.

### OpenClaw's memory search on the same server

One server can serve both. Point OpenClaw at it as a provider (a model name containing `embeddinggemma` makes OpenClaw
add EmbeddingGemma's task prompts), then build its index once at low priority:

```bash
openclaw config set --batch-json '[{"path":"models.providers.machine-embeddings","value":{"api":"openai-completions","baseUrl":"http://127.0.0.1:8792/v1","apiKey":"local","models":[]}},{"path":"memory.search","value":{"enabled":true,"provider":"machine-embeddings","model":"embeddinggemma-300m","sources":["memory","sessions"]}}]'
systemctl --user restart openclaw-gateway
nice -n 19 openclaw memory index --agent main
```

An explicit provider fails closed: while the server is down, `memory_search` answers "unavailable" instead of falling
back to keywords, so keep the unit's `Restart=`.

**Off again:** remove `embeddings` (or set `enabled: false`) and restart. The `event_vectors` table can stay or be
dropped.

## Organization data (optional, enrichment)

Off unless you set it up. With a key for an enrichment service, The Machine looks up the organizations in the graph by
domain and keeps a small profile of each: industry, size, location, founded, a short description, LinkedIn, website and
logo. It describes the company, never what it is to you; that stays a role.

### Setup

Put the key in a file only you can read (`chmod 600`), then add to `config.json` and restart:

- A preset: `"enrichment": {"provider": "apollo", "key_file": "~/.local/share/personal-assistant/enrichment.key"}`.
  Presets: `apollo`, `peopledatalabs`, `hunter`.
- Any other service that answers a GET with JSON about a domain:
  `"enrichment": {"url": "https://api.example.com/companies?domain={domain}", "headers": {"Authorization": "Bearer {key}"}, "key_file": "…"}`.
  `{key}` can go in the url or the headers; `key_env` reads it from an environment variable instead. The key never goes
  in the config itself.
- Common response shapes are understood: flat, or wrapped in `organization`, `company`, `data` or `result`. If yours
  differs, `fields` adds paths of your own: `{"industry": ["category.sector"], "about": ["profile.text"]}`.

Check it with `assistant enrich globex.com` (looks one up now) and `assistant enrich` (service and counts).

### What is sent

Only organization domains from the graph: never free-mail domains, your own domains, names, addresses or messages.

- **Order:** those whose people you deal with first (you write both ways or meet, then those you wrote to, then the
  rest), within the day's budget. Never campaign sender domains (news., email., e. and the like); a paying customer
  always.
- **Budget:** five per pass every ten minutes and at most 50 a day (`per_day`); paired with the Network, hosted's budget
  of 50 per pass and 1,000 a day. Each is looked up again after 90 days. Lookups count against your plan with that
  service.
- **Errors** (rejected key, rate limit, unreachable): it waits an hour, and that domain a day. Errors never contain the
  url or the key.

### Where it shows

The Graph tab (logo and industry in the organization list; a summary, the description and links on its page), `graph`
results (`about`, `profile`), preparation context ("at Globex (customer; Manufacturing, 51-200 people, Springfield,
founded 1989)") and the roles run. Profiles are kept in `org_profiles`.

**Logos.** A lookup's logo is kept only as a plain `https` address and loads straight from the service's image host,
with no referrer, lazily and at a fixed size; the initial shows until it loads.

- When the lookup brought no logo, the Machine asks the organization's own website for the icon its home page names
  (`apple-touch-icon` or `icon`, never SVG; else `/favicon.ico`): https only, public addresses, up to 200 kB of PNG,
  JPEG, WebP or ICO, ten organizations a pass. It is saved here (`person_photos` as `logo:<domain>`), so no logo
  service learns which organizations you deal with.
- A logo from the lookup or your own picture wins. A site without one is asked again after 30 days (`org_logo_tries`).
- A lookup that found the organization without a logo is asked once more after `LOGO_RETRY_DAYS` (7), at most five a
  pass (`org_logo_retries`).

**Without a lookup.** An organization from an email domain always has that domain as its website (mail.remy.be is
https://remy.be) and, until a lookup or you name it, a readable name from the domain: Remy for remy.be, Blue Fox for
blue-fox.io, KBC for kbc.be. Many small companies aren't known to lookup services at all.

### When it's wrong

- **Edit** on an organization's page changes its name, website, LinkedIn, industry, size, location, founded and
  description. What you write is kept in `org_edits` and wins over every later lookup; an emptied field gives the
  looked-up one back. Only the fields you changed are sent and checked, and a refused field shows why under it.
- **Another company.** An answer counts as not found when its website isn't the domain's home page (a blog post, a
  form, a page on a hosting subdomain) and its name shares nothing with the domain.
- **Wrong company, clear details** drops a bad match and stops looking that domain up. **Look it up again** (or
  `assistant enrich <domain>`) undoes it.

**Off again:** remove `enrichment` (or set `"enabled": false`) and restart.

## People data

People with a company address get a job title, photo, company, LinkedIn and city and country, from the same service on
its own budget.

- On a hosted Machine it is on, through the control plane like organizations.
- Self-hosted, it needs `people_url` in `enrichment`, with `{email}`, `{name}`, `{domain}`, `{first_name}`,
  `{last_name}` and `{key}`. The `peopledatalabs` and `hunter` presets have one, and Salesflare's lead API gets
  `…/enrich/people?name={name}&domain={domain}` by itself. `people_fields` adds paths like `fields`.
- Turn it off in Settings, Security: **Look up work contacts** (also stops the Gravatar tries). Never in a Careful Work
  Fleet.

### Who is looked up

Everyone in your graph with a full name and a company address, your own colleagues too. Only technical skips: no full
name, only free mail, a shared inbox like info@ or a no-reply sender. A meeting or mail both ways goes first.

- Hosted, and self-hosted when paired with the Network: up to 3,000 a day (up to 200 per pass on a paired self-hosted
  Machine). Other self-hosted Machines: five per pass every ten minutes, at most 50 a day (`people_per_day`).
- Each is looked up again after 90 days. After an upgrade that asks for it, everyone already looked up is looked up
  again once, closest first, within the same limit (`enrich_prefs` marks it done).

### What is sent and kept

- Salesflare's lead API gets their name and company domain (an address at eu.example.com asks for example.com); services
  that look up by address get their work address. Hosted lookups send only name and company domain.
- Gravatar gets only a SHA-256 hash of their work address, for a photo.
- Only what the dashboard shows is kept, in `person_profiles`: job title, company, a photo, a LinkedIn profile address
  and city and country.
- **Misses.** An answer about someone else (a name with nothing in common, or a company at another domain) counts as not
  found. The same name at another top-level domain (example.nl for example.com) is the same company. Self-hosted, a miss
  keeps only why: `unknown`, `another person`, `another company` or `nothing to show`.

### Photos

A photo is saved once on this Machine (`person_photos`), so it never expires. Each is only a JPEG, PNG or WebP image of
at most 200 KB, checked by its own bytes, fetched over `https` from a public address.

- **From a lookup:** right after each lookup, the lookup's own photo link while it still works (not LinkedIn's stock
  silhouette), otherwise their Gravatar. One try per lookup (`person_photo_tries`). With neither, initials show; when
  the lookup's link had expired, that person is looked up again after 30 days instead of 90.
- **From your own contacts**, for anyone without a photo, personal contacts too, with the permissions the Machine
  already has: Google contacts, other contacts and the Workspace directory through a `gog` sign-in (once a day, read
  only; hosted Google sign-ins don't include Contacts), and someone's Slack profile picture. A photo the person chose
  (their own Google or Slack profile) comes before one set on a contact, and generic ones are skipped. Only links for
  people in your Graph are kept (`contact_photo_links`), each downloaded once. These photos are never sent anywhere.
- **From X and LinkedIn:** the photo on someone's X profile (from the user objects in mentions and DMs; X's default
  picture is skipped) and on their LinkedIn profile (from the participant in each one-to-one conversation).
- **Not used:** Outlook contacts (no Contacts permission), Intercom avatars and Telegram's own bot.

**WhatsApp pictures.** `wacli` keeps no pictures locally, and asking for one is a live request.

- The Machine's own WhatsApp reads stay `--read-only`. The one exception, `profile picture-info`, is passed on only to
  your always-on `wacli sync --follow`, and only when that was started with `--profile-picture-budget N` (at most N a
  day, people only). Without it, nothing is asked.
- It asks for people in your Graph with no photo whose WhatsApp address it has seen in a chat, closest first, at most 50
  a day (`whatsapp_photo_asks`). Someone without one, or who hides it, is asked again after 30 days. When the mirror
  can't answer, the Machine waits 6 hours.
- Nothing is sent to them: no message, read receipt or presence.

**Telegram pictures.** The same rules through the Telegram mirror (`telegram_mirror.py`), the process that holds the
Telegram session.

- People in your Graph without a photo whose Telegram user ID the Machine has seen in a chat it reads, closest first, at
  most 50 asks a day (`telegram_photo_asks`).
- The mirror fetches only the small profile photo (160 px), one at a time a few seconds apart, and keeps it sealed in
  its store (`photo_asks`) until the next pass saves it into `person_photos` and removes it from the store.
- Asked again after 30 days for someone without one. A Telegram flood wait pauses only the photos. When the mirror
  can't answer, the Machine waits 6 hours. Nothing is sent to them.

### Facts from your connectors

While they run, connectors keep what the pages they already fetch say about the people in them, with no extra request,
scope or sign-in:

| Source | What it keeps |
|---|---|
| Slack | their title, phone and time zone (the `users.info` lookup done for their name) |
| X | bio, location, website and handle (mentions and one-to-one DMs) |
| LinkedIn | headline and profile link (the participant in each one-to-one conversation) |
| Google | job title, company and phone of your contacts and the Workspace directory |
| Salesflare | the job title on the CRM contact |

- Each fact is kept in `person_facts` with where it came from and when, sealed like message contents, and never sent
  anywhere.
- What someone says about themselves beats a record someone keeps about them (a contact, the directory, the CRM), which
  beats a lookup's guess. Within one level the latest wins.
- Headline and bio are read when their page opens, never copied into the graph. `profile.sources` in `graph` results
  says where each field came from.
- Nothing from Outlook, Zoom, Intercom, Stripe, GitHub, WhatsApp or Telegram: what they read has no more than a name, an
  address or a number.

### Where it shows

People rows (photo or initials, and job title), their page (title, place, their local time, phone, LinkedIn, X, website,
bio), `graph` results (`profile`) and preparation context ("job title Head of Sales").

### The owner's own details

**Edit** on a person's page (`graph_person_edit`, owner only) saves their name (`graph_names`), what they are to you
(`person_roles`), where they work (`person_orgs`), and title, location, LinkedIn, phones, emails and Work or Personal in
`person_edits`.

- Those win over a lookup and later automatic updates; the build records which fields are the owner's (`edited`).
- Each field is kept on the identity whose page it was saved on, so a merged person carries it and an Undo leaves it
  with that identity.
- Phones and emails are kept as what the owner added and took off, so an address that turns up later still shows.
- Deleting someone permanently deletes their edits too.

**Work or Personal without your word** (`graph.auto_side`):

1. Someone only in your Family or Friends (`graph.circles`), or whose role says they are family or a friend
   (`graph.personal_relation`: wife, father, friend from university; a closed list, so "family lawyer" is not), is
   Personal, whatever address they write from.
2. Else Work for someone with a work address or organization.
3. Else what their threads are about (the sharing review's call: client, sensitive or colleagues only is Work, personal
   is Personal) and the projects they're on (one on a board is Work).
4. Else the accounts their conversations came from. Having no work address says nothing by itself; with thin or mixed
   evidence it stays unknown.

The Graph's Work and Personal lists, their counts and the CSV's Type all read this one stored side. A change to Family,
Friends or the Work Fleets rebuilds the graph within a minute, and the first build under a new rule records each side
it changed in `side_changes`. Sharing with a Work Fleet never includes your own life (`graph.own_life`: your Personal,
Family and Friends, a family or friend relation).

## How you write

Voice and style learn only from what the owner wrote themselves (`authorship.py`).

- A draft sent from a to-do comes back in their Sent mail or chat with their name on it. The profile, the voice study,
  the examples a draft matches and the "answered it themselves" lessons skip every message a send job (`action_jobs`)
  produced: matched by the Message-ID the send set or the id the channel returned, or else by the sent text the message
  starts with (20 characters or more, so a short reply the owner typed still counts as theirs).
- A draft the owner changed before sending teaches only through that change (`draft_edits`, what they cut and added).
- An agent's rewrite (source `agent`) teaches nothing.

## Keeps learning

Reviews fold a note into a fact, rule or voice as it comes. The learning loop (`learning_loop.py`) looks at what piles up
between them: the owner's own draft edits, dismissed and snoozed to-dos, and corrections in a to-do's chat.

- At most every 12 hours, with at least three new signals, one small background turn (kind `tune`, one page of at most
  30 signals plus the current voices, rules and facts) proposes at most three changes: a voice block reworded (keeping
  most of it), or a rule or fact added or replaced. It waits for the usage budget like every background turn.
- Each change is applied and kept in `learning_changes` with what it replaced and why. **Learning, Changes** lists them
  with **Undo**.
- A voice the owner wrote is never changed by the loop, and an undo is refused when the owner changed that voice or fact
  since.

<a id="fixed-where-it-came-from"></a>
## Fixed at the source

When the owner says in a to-do's chat that something is wrong ("she's not the CEO", "he left the company", "we don't use
that template anymore"), the chat turn first asks where it came from (`correction_sources`, `corrections.py`):

- the people, organizations and projects on the to-do, with their role, organization, title, place and stage and where
  each came from (a review and its quote, an email address, a lookup, the owner);
- the to-do's project, the facts and rules that mention it, The Machine's GBrain pages and matching skills.

When one of those holds the wrong thing it fixes it there (`fix_source`), as the owner's word:

| What | Fixed with |
|---|---|
| A role | `graph.set_role`, so a later review keeps it |
| An organization, or leaving one | `set_org` |
| A title or place | `person_edit`, which wins over enrichment |
| A project's stage | `set_stage` |
| The to-do's project | `set_card_project` |
| A fact or rule | reworded or removed |

A skill changes only through an update the owner approves. A fix comes only from the owner's own note on that to-do, at
most five per note.

- Each fix is kept in `learning_changes` (kind `source`) with what it replaced and where the wrong one came from.
- The chat shows it as **Fixed: …, from …** with **Undo**, and so does Learning, Changes. An undo puts back exactly what
  was there, and is refused when that changed since.
- A fix in the Graph rebuilds it and wakes the GBrain sync, so The Machine's section on a page follows. The owner's own
  text on a page is never changed.
- A note fixed this way is no signal for the learning loop, so no rule is added on top. When no source holds it, the
  note is learned as before.

## Sharing learnings

Now and then your Machine offers to share a few general learnings with The Machine team, so the product gets better for
everyone (`team_learnings.py`). Nothing goes without your Send, unless you chose to send automatically. For learnings
shared within a Work Fleet, see [Team learnings](fleet.md#team-learnings).

### What is written

- At most once a day (`DAYS`), when there are at least three new notes, facts or rule changes (`MIN_MATERIAL`), one
  cheap background turn reads what this Machine learned since the last run: the owner's notes on to-dos, facts, rule
  changes, voices, how drafts were edited and recent errors. The first run reads the last 30 days (`SINCE_DAYS`).
- It writes up to five general learnings, like "Drafts for people who don't know the context yet should introduce it
  first." Judged by what the notes mean, not by words. The turn's evidence is sealed like any other run's, and it waits
  for the usage budget.
- A new learning whose words overlap one already shared, removed, withdrawn or in a Never ask batch by 60% or more is
  dropped (`team_learnings.seen`, `repeats`), so the same one is never offered twice.

### What is taken out

The turn is asked for general patterns with nothing personal, and the service then strips every learning itself
(`team_learnings.strip`):

- email addresses, links, handles, phone numbers, dates, amounts and long numbers;
- every name this Machine knows: people, organizations and projects in the Graph, their first and last names, and the
  owner's own accounts. Product names like Gmail or WhatsApp stay.

Each learning says what was taken out. An error log is never written by the turn: the service adds an excerpt of the
error itself (kind, where, how often, its message with anything private taken out), never message content.

### Use cases

Each learning carries 1 to 3 use cases (`use_cases`: `given` the situation, `when` what the owner does, `then` what
should happen), retold generically in English from what actually happened. The team builds and checks a change against
them.

- They are stripped like the learning, then checked more strictly (`team_learnings.check_case`): no quoted text, and no
  capitalized word mid-sentence besides product, screen and button names.
- One that fails is left out; a learning left without a use case is dropped. An owner's edit that fails is refused.
- They travel inside the sealed learning and the vote, so nothing new leaves a Machine.

### Asking

A quiet offer under Learning, Shared and a line in the weekly recap: "Share 3 learnings with The Machine team?"

- **Review** shows exactly what would be sent, item by item, to edit or remove. An edit that adds a name back is
  refused.
- **Add the error log** is off by default, per learning.
- **Send** sends only what is on screen; **Not now** asks again in a week (`LATER_DAYS`); **Never ask** turns it off.

**Send automatically.** Opt-in: **Send automatically from now on** in the offer, or Settings, Security, **Send learnings
automatically** (off by default).

- A batch made while it is on goes as it is, through the same `final_items` check and sealing (`auto_send`), never with
  an error excerpt or the owner's email.
- A batch the check would change, or one not through within 24 hours, waits for the owner under Learning, Shared.
- It only runs while the offer is on, the owner's level isn't Careful and no Work Fleet is Careful (`auto_on`). Turning
  the offer off (also Never ask and Careful) turns it off.

### Activity and withdrawing

Settings, Activity (Learnings) and Fleet, Activity list every learning sent lately, exactly as it went
(`team_learnings.shared`). **Withdraw** posts a small envelope signed with the same learnings key, so the control plane
can tell it comes from the sender without knowing who that is. It deletes that learning for the team (its candidate,
votes and pick), and the Machine counts it as removed, so it isn't made again.

### Sending

- Over the Network to the control plane, sealed (`network_crypto`) for the team's key. Its fingerprint is pinned in the
  code (`team_learnings.TEAM_KEY_FINGERPRINT`): any other key the Network hands out sends nothing.
- Signed by a key made for learnings only (`learnings-keys.json`), not the Machine's Network identity, so the team sees
  a made-up name. **Add my email so the team can reply** adds the owner's account.
- On the control plane they land sealed in the team's Learnings inbox, where a person reads them, groups similar ones
  and decides. Nothing changes the product by itself.

Turn it off in Settings, Security: **Offer to share learnings**. It needs the Network: a Machine without it is never
asked. What the Network sees: [The Machine Network](network.md#what-the-network-sees).

### Voting

A learning one Machine shared goes, after the control plane's own scrub, to the other Machines as a candidate (text,
example and area only; never its log or who sent it).

- Once a day a Machine with voting on fetches up to 20 candidates, skips its own and any the strip would change.
- One small background turn (kind `team_votes`, at most five learnings) answers one question for each: would this have
  changed something on this Machine in the past week? It reads the owner's rules, facts and channels and the past
  week's to-dos with what the owner did.
- **Useful** needs a concrete case from that week as the vote's use case (passing `check_case`); without one the vote
  goes as `not_relevant`. Agreeing with the idea is not a vote.
- Only the vote goes back: `useful`, `not_useful` or `not_relevant`, a reason and a use case, each dropped when the
  strip or check would change it. A learning is judged once at most.
- The control plane counts the votes per account without keeping the account, and ranks the learnings for the team,
  who pick what goes into the shipped defaults (AGENTS.md, a prompt, the docs) as a change a person makes.

Settings, Security, **Vote on learnings from other Machines**: **On** (the default, it votes by itself), **Ask first**
or **Off** (`team_learnings.vote_mode`). Under Ask first, a judged vote waits in one box under Learning, Shared, never a
to-do of its own and never a notification. The owner sends or skips it (`learnings_votes_decide`); one left 14 days goes
unsent. Off skips everything waiting.

### What Help is asked

Help (`help_chat.py`) ends each answer with a TOPIC: line, a few generic words for what the question was about.
`help_topics.py` keeps it only when it passes `team_learnings.strip` with every name the Machine knows, the use-case
check and uses only words from the public help pages; else it keeps "other" for an unanswered question, or nothing.
Once a day the finished days go to the control plane as counts per topic, without the account. Settings, Security,
**Share what Help is asked** turns it off and deletes what waits.

## Error reports

Separate from learnings and on by default: when The Machine's own code fails, the Machine sends the team a signature of
the error, never what caused it (`error_feed.py`). See also [Error reports](help/error-reports.md).

**Sources:**

- the service's logged errors and dead threads (`FaultLog`);
- the dashboard's uncaught errors and unhandled rejections (posted as `client_error`, normalized again by the service);
- failed reviews and coding-agent jobs (their error codes only);
- failed syncs (the source's service and the error type). A transient one (a rate limit, the service's own 500, 502,
  503 or 504, or the network) only after 20 in a row; a 429 or such a 5xx is retried once after 15 seconds, or its
  Retry-After when that is a minute or less. A sign-in or permission error such as 401 or 403 is reported at once.

**Limits.** Each is deduplicated by type, place and normalized message (without the line number, so a release that
moves the code keeps the same signature). At most 300 kept, a batch of 50 every 10 minutes and 500 a day, kept 30 days.
Before a batch goes, every name the Machine knows is taken out once more, and each message must pass a strict shape
check (`error_feed.allowed`) or it never goes.

Settings, Security, **Send error reports** turns it off: nothing is recorded or sent, and what waited is deleted.

**Pacing.** Under the same switch, `pacing.py` counts how often background work has to pace (`model_budget.pause`): per
stretch, when it started, the window (`5h` or `week`), the threshold, how long it lasted and how many distinct jobs
waited. Once a day the finished days go over the Network (`POST /errors` with `{"action": "pacing", ...}`) for a card on
the control plane's /admin. Counts and minutes only; job ids stay on the Machine. The owner sees nothing new.

## Deleting someone

**Delete permanently…**, in the ⋯ menu on a person's page, removes them and everything The Machine knows about them:

- their graph entry, links, aliases and addresses, looked-up details and saved photo, relationship scores;
- the messages they sent or that were only between you and them;
- the notes learned about them (also the lines in the agent's memory notes that name them).

To-dos that involve them stay, as your own work, with their name and addresses taken out. Messages with other people
that they were copied on stay.

What stays is a keyed hash of their addresses and other identifiers, so they are not added, looked up or learned about
again: new messages from them, or only to them, are not kept. On a hosted Machine the control plane keeps nothing about
people to delete.
