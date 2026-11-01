# The Machine Network

Machines talk to each other (Fleets, Family, Friends) through The Machine Network. This page says what the Network can
see, how messages stay reliable, and where it's going. What Fleets do is in [Fleets](fleet.md).

## End-to-end encryption

- **Keys.** Your Machine makes its own keys (X25519 to receive, Ed25519 to sign) and keeps the private ones in
  `network-keys.json` next to its database, readable only by you. It publishes the public keys to the Network directory.
- **Sealed.** Questions and answers are sealed for the receiving Machine and signed by the sending one, bound to who
  sends what to whom. The Network can't read them, change them or replay them elsewhere.
- **Sealed only.** The Network carries nothing else: a question or answer that isn't sealed is refused there and dropped
  by your Machine. A Machine without keys yet (from before end-to-end encryption) can't be asked until it updates.
- **Key-change warnings.** Your Machine pins a teammate's or friend's keys the first time it sees them. If they change (a
  reinstall, a new computer), the Fleet tab shows a warning with the old and new fingerprints. If their keys disappear,
  nothing is sent to them until they're back.
- **Local-first.** History stays on your Machine. The Network keeps a sealed message only until it's delivered and
  answered, and clears answers once your Machine acknowledges them.

The sealing needs nothing beyond Python: it uses the `cryptography` package when it's installed (fast), and otherwise
its own implementation of the same standard algorithms (`network_crypto.py`).

**Moving your Machine.** `assistant export --keys` carries `network-keys.json` (encrypted with your passphrase) and
`assistant import` puts it back, so your teammates and friends see the same Machine. An export without keys makes a new
Network identity on import, and your teammates and friends see a key-change notice once.

## What the Network sees

- **Routing data.** Who is in which Fleet or friends group, who asks whom, the kind of question, its status and times.
  The Network needs those to route messages.
- **Handling claims** (which of you handles an email several teammates got) are hashes of the Fleet's secret and the
  email's Message-ID, with no Message-ID, address or content in them. The Network hands out that secret, so equal
  hashes reveal matching claims, and it can test a Message-ID it got elsewhere. Claims are therefore not end-to-end
  encrypted. The secret can't open sealed questions or sign as a Machine. A secret the Network doesn't know is on the
  roadmap.
- **Finding people you know** ([Fleets](fleet.md)): on by default at the Standard security level, off at Careful, and
  either switch can be turned off any time. Contacts are looked up blinded (private set intersection), so the Network
  never sees your address book. Being findable covers your account email and your connected mail addresses, except
  shared ones (info@, sales@, a team inbox, an address a teammate also has), which stay off until you turn them on. The
  Network keeps those only blinded and learns which addresses matched people who are findable.
- **Your own addresses.** A self-hosted Machine tells the Network the mail addresses of its work accounts (so teammates'
  Machines know who knows whom), and its dashboard's https address when you set `dashboard_host`, so your Account page
  can link to it.
- **Your account in Settings.** A paired Machine asks for your account in short (`GET /api/fleet/account`: your email,
  your Fleets as counts, links to the account's pages), at most once a minute, for its own token's owner only. Its
  buttons are plain links: no token on your Machine opens a signed-in account page.
- **Learnings for The Machine team** ([Sharing learnings](intelligence.md#sharing-learnings)): only after the owner's
  Send on exactly what they saw. `POST /api/fleet/learnings` gets the team's public keys (checked against a fingerprint
  pinned in the code) and then the learnings sealed for them, signed by a key for learnings only. The control plane sees
  a made-up name unless the owner adds their email.
- **Error reports for The Machine team** (`error_feed.py`, [Error reports](help/error-reports.md)): on unless the owner
  turns off **Send error reports**. At most every 10 minutes, a batch of signatures: an error's type, its message
  normalized (numbers, ids, quotes, addresses, links, paths and unknown capitalized words taken out), file:function:line
  in The Machine's own code, the app version, a count and first and last seen. Never message content, names, addresses
  or tokens. Kept 30 days per Machine and signature.

## Shared connectors

A Work Fleet's admins can share a connector (Intercom or Stripe) with the Fleet, so the team's Machines read the same
customer conversations without anyone pasting a token. The token goes from Machine to Machine, sealed. The Network never
has it. Code: `shared_connectors.py` and `fleet_trust.py`.

### Who gets it

- **Only an admin's Machine sends it**, and only to the Machines an admin said OK to. The first share lists the members
  to tick; confirmed admins get it by default. Someone who joins later shows on the admin's Fleet tab: "Share Intercom
  with <name>'s Machine?". The OK is for the keys their Machine had then: when they change, nothing goes until an admin
  says OK again. Members never pass it on.
- **A signed grant goes with it**, for that Fleet, connector, workspace and recipient (member id and key fingerprint),
  and for a hash of the token (SHA-256 over the grant id and the token). The receiving Machine takes the token only
  when it came sealed, from an admin it trusts, with a grant for exactly this Machine and token that is still the Fleet's
  current one. Anything else is dropped.
- **Admins are vouched for by Machine keys**, not only by what the Network says. The owner's Machine signs its own key
  (the first one your Machine sees is pinned). An admin your Machine trusts confirms each new admin after their owner's
  OK ("Confirm <name> as an admin of <Fleet>?"). An admin only the Network made shows as "Not confirmed yet" and gets
  nothing. The owner's Machine can also name, after their OK, who takes the Fleet over if they delete their account. The
  Network can drop someone from the set, never add one.

### On each Machine

- **Where it lives.** In a credential file of its own (mode 600) next to the database: never in `config.json`, the
  Fleet's tables or a log. The account is read-only and in the Fleet's company (`work:<Fleet>`). Connections shows
  "Shared by <Fleet>. Its admins manage it." with nothing to change.
- **Stripe with Sign in with Stripe** rolls its sign-in on every refresh, so the sign-in never leaves the admin's
  Machine. That Machine sends teammates access tokens, an hour each, under the same grant, and a fresh one when theirs
  has less than 20 minutes left. Nothing lasting goes out. While the admin's Machine is off for over an hour, the team's
  Stripe pauses.

### Leaving and stopping

- **Leaving.** Leaving or being removed takes the shared account with the Fleet's other work accounts. The remaining
  admins' Machines then show "<name> left <Fleet>. Replace the Intercom token so it stops working on their Machine." with
  a field for the new one. Any admin can replace it, the new token goes to who stays, and every Machine drops the old one.
  Stripe needs no replacing: the leaver's access token runs out within the hour.
- **Stop sharing** on an admin's Fleet tab removes it for everyone.
- **Confirmed removal.** After a stop, each Machine that had the token says it deleted it (`op: dropped`, retried for a
  week). The Fleet page on the account says "Removed, confirmed" once all have.
- **Timing.** A stopped or replaced share reaches the Machines at once (their Network inbox answers as soon as the shared
  connectors change). A Machine that was away sees it at its next directory, within about 10 minutes.

**Limits.** A Machine that joins after the owner changed trusts the first root it sees. Intercom's API doesn't say what a
token may do, so use a dedicated Intercom app with read permissions only.

## Shared Graph

A Work Fleet's Graph (records, short timelines, client threads and their attachments) travels as blobs signed by the
publishing Machine and sealed to each confirmed member's Machine. The Network only passes them on and deletes each once
every Machine took it, or after 30 days; it can't read, change or add to them. The design is in
[Shared Graph](shared-graph.md). Code: `shared_graph.py`.

## Scheduling between Machines

Two owners who are not in the same Fleet can find a meeting time: their Machines trade free/busy times (never what
is on a calendar) sealed end to end, and each owner taps Book it before an invite goes out. Only Machines whose owners
emailed each other both ways can ask. The design is in [Scheduling between Machines](scheduling-between-machines.md).
Code: `meet.py`.

## Reliability

- Every question has an id: a retry never asks twice, and your Machine never acts on the same question twice.
- An answer the Network couldn't take (a restart, your connection down) waits in an outbox on your Machine and is sent
  again with backoff, for up to 3 days.
- A question the other Machine hasn't picked up yet shows as **Not delivered yet** on the Fleet tab.
- Your Machine can use more than one Network endpoint (`network_urls` in `config.json`) and switches to the next one
  when one is away.

## Failover

The Network runs on a main node and a standby node with another cloud provider (`network2.themachine.computer`), both
built in. When the main node is away your Machine uses the standby:

- The standby carries sealed questions and answers only. Pairing, keys, claims, finding people and the directory wait
  for the main node; your Machine keeps its directory from before.
- A question moves to the standby only when the main node surely didn't take it.
- An answer goes to the node that has its question, or waits in the outbox until that node is back.
- Your Machine looks into both mailboxes, and a question that came through both is taken once.
- After 5 minutes it tries the main node first again.

## Guarantees

**Keys and identity.**

- Private Network keys are written atomically on first use. Concurrent starts use one pair, and a malformed key file is
  reported instead of quietly making a new identity.
- Plain exports leave the keys out, also from a custom path; `--keys` exports carry them and the import puts them next
  to the database. If a credential there has the same file name, the keys go in `network-identity/` instead; neither
  overwrites the other.

**Replies and requests.**

- A reply is saved before it is delivered and kept after an interruption. A stale flush can't erase a newer queued
  reply.
- Family requests keep their identity after a failed response and get a new one only once the local receipt is saved.

**Which node has a question.**

- Which node a question went to is saved before it is sent and kept through restarts.
- An unclear connection failure stays on that node; only a clear refusal moves to the next one.
- Duplicate deliveries keep one choice and get the same answer on both nodes.
- These records expire after 30 days, in the local database.

**Finding people.**

- A blinded non-match is saved as checked. A match counts as checked only after its name lookup came back and was saved.
- Rate-limited, interrupted and over-cap matches are tried again on the next lookup, and the daily refresh isn't marked
  done over unfinished ones. Lookups never send a friend request again.

## The cloud forwards, never reads

AIs such as ChatGPT and Claude can reach a Machine at its private address,
`https://<name>.mcp.themachine.computer/mcp` ([Connected AIs](ai-connections.md#where-it-runs)):

- The cloud's router reads only the name in the AI's TLS hello and forwards the encrypted bytes; it never ends TLS.
- The Machine holds the certificate and its key and terminates TLS itself, so the cloud can't read or change what an AI
  and the Machine say.
- A self-hosted Machine dials out for each connection (`mcp-wait`, then `mcp-stream`) with its device token, so it needs
  no open port.
- The cloud sees which Machine an AI connects to, when, and how many bytes go each way.
- The certificate comes from Let's Encrypt on an ACME account with no email address.

The official app's shared address, `https://mcp.themachine.computer/mcp`, is different: there the cloud reads each
request's Authorization header to route it, and stores nothing of what passes
([Two ways in](ai-connections.md#two-ways-in)).

## Addresses

The Network lives at `network.themachine.computer`; the standby is `network2.themachine.computer`. The old address,
`relay.themachine.computer`, keeps working and is tried when the new one can't be reached. `fleet-pair` still accepts
`--network` and its old name `--relay`, and ignores both: the Network's address is built in.

## Roadmap

| Phase | What | State |
|---|---|---|
| 1 | Fleets and Friends through the Network, approvals, rules, an activity log on each Machine | Done |
| 2 | End-to-end encryption, key pinning and key-change warnings | Done |
| 3 | Outbox with retries, once-only handling, "Not delivered yet", endpoint failover | Done |
| 4 | A second Network node on another cloud provider, with failover drills | Done |
| 5 | Finding people you know (with permission), useful-connection suggestions, task-driven email invites | In progress |
| 6 | Other AI agents on the Network through a published protocol | Later |
