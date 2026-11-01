# Connected AIs (MCP)

Other AIs (Claude, ChatGPT, Cursor, Codex, GBrain and anything else that speaks MCP) can connect to a Machine. They
read to-dos, promises, team briefs and the Graph. With **Read & edit** they also add to-dos and drafts and make Graph
changes the owner can undo. With **Messages** on they can also search and read messages. They never send and never act.

This page is the design. What the owner sees is in [the help article](help/ai-connections.md). It is about AIs from
outside only: The Machine's own agent, Do it and [coding agents](agents.md) are not affected.

## Two ways in

Settings, **AIs** shows two addresses, each with Copy, and the steps for ChatGPT and Claude once. The official app comes
first and is the default.

### Claude: the connector directory

The official app is listed in Claude's connector directory:
`https://claude.ai/directory/connectors/the-machine` (`AI_CLAUDE_DIRECTORY` in `dashboard/settings-ai.js`). That is the
one-click way for Claude: **Add in Claude** opens the listing, Connect there starts the official app's sign-in below with
the shared address, nothing to paste. It shows above the shared address once the official app is ready (`shared`).
The shared address stays for a custom connector, other clients and ChatGPT, whose app isn't in its directory yet.

### The official app: one shared address

`https://mcp.themachine.computer/mcp` (`ai_app.SHARED_ADDRESS`) is the same for every Machine. The account
(`fleet.CONTROL`) is the authorization server there:

1. The owner signs in with their The Machine account, and picks a Machine if they have several.
2. The account connects to that Machine as an ordinary OAuth client, over the Machine's private address: the metadata,
   `POST /oauth/register` (the AI's name, `redirect_uris` `[<account>/mcp/connect/callback/<kind>]`), then the Machine's
   own consent page with PKCE and `resource` set to its private `/mcp`.
3. The code goes back to the account, which exchanges it at the Machine's `/oauth/token`.
4. Each later MCP request of that AI is routed by its token to the Machine's private host. The Machine sees ordinary
   `/mcp` requests.

`<kind>` is `claude` or `chatgpt` when the account checked the AI's own redirect (claude.ai, claude.com; chatgpt.com,
chat.openai.com, openai.com), else `other`.

### The private address: end to end

`https://<name>.mcp.themachine.computer/mcp` is this Machine's own. The AI talks to the Machine directly and TLS ends on
the Machine ([Where it runs](#where-it-runs)). For owners who want nothing readable in the cloud.

### Trust

- **Official app:** the cloud handles requests in transit to route them. It reads the Authorization header to find the
  Machine and stores nothing of what passes.
- **Private address:** the cloud forwards encrypted bytes and can't read them.

Either way the Machine's own consent and token checks decide. Access, area, expiry, Messages, Activity and Undo work the
same.

### How the Machine tells them apart

On the consent page (`ai_access.label`), a redirect to the account's callback (`ai_access.OFFICIAL_CALLBACK`,
`<fleet.CONTROL>/mcp/connect/callback/` followed by exactly `claude`, `chatgpt` or `other`) is the official app:

- `claude` shows as Claude and `chatgpt` as ChatGPT, verified, going back to that AI.
- `other` shows the name the AI gave, unverified ("can't check who this is"), going back to the account's host.

In Settings each such connection is tagged **Official app** (`connections()`, `official`).

### When it shows

The official app shows when the account can reach this Machine at its private address (`ai_app.ai_reach`, `shared`): a
hosted Machine with a name, or a paired self-hosted one with a name of its own and its certificate ready. Until then the
official app's place shows **Get your address** ([Pairing](#pairing)), which both ways need.

## Connections

Each AI that connects is one connection, with:

- **Access**: Off, Read, or Read & edit (stored as `draft`, its old name). Changed in Settings at any time: the next
  call uses it, nothing reconnects.
- **Area**: Work, Personal or both (the choice shows only when the Machine has both). As on to-dos
  (`suggestion_scope`): to-dos and promises by their accounts, people by their side in the Graph, organizations,
  projects and team briefs only with Work.
- **Messages**: off until the owner turns it on ([Messages](#messages)).
- **Expires**: after 1 day, 7 days, 30 days or 1 year. An expired connection is refused (and logged) until the owner
  extends it or the AI signs in again.
- **Turn off now**: Off, and every token of it revoked at once.
- **Activity**: every call, refused ones included, with the tool, the time and the outcome ("3 to-dos", "Refused: this
  connection can only read"). Kept 90 days, at most 2000 lines per connection. The line's detail is sealed at rest with
  the message key (`ai_activity.detail` in `message_seal.DERIVED`).

The Activity lines are kind `ai` in Settings, **Activity** (`activity_log.register('ai', ai_access.activity_lines)`,
actor the connection), so they show with everything else The Machine did. A connection's own activity is that list
filtered to it (`/api/activity?kind=ai&actor=<id>`).

Settings, AIs lists the connections with their activity, and **Add a key** for an AI that needs one.

**Work Fleet data.** Only what the owner already sees: their own to-dos (a Fleet request they took is one), and the team
brief their Fleet tab shows. Teammates' Team Graph records and threads never go to an outside AI, the same rule as
[GBrain](gbrain.md)'s sync.

## What an AI can do

| tool | level | what |
|---|---|---|
| `list_todos` | Read | Open (or snoozed, or done in the last 30 days) to-dos: title, text, status, due date, Work or Personal, project |
| `get_todo` | Read | One to-do, with its ready draft if it has one and where it came from (sender, subject, date; no message bodies) |
| `list_promises` | Read | Open promises: who promised what to whom, and by when |
| `search_graph` | Read | People, organizations and projects that match a name, email or company |
| `get_graph_record` | Read | One person, organization or project: role, organization, closeness, last contact, open to-dos, promises |
| `get_team_brief` | Read | The latest team brief of each Work Fleet, as the Fleet tab shows it |
| `create_todo` | Read & edit | A new to-do with the AI's text, marked as coming from that AI |
| `create_draft` | Read & edit | A new to-do with an email draft (to, subject, text) from one of the owner's mail accounts, waiting for the owner's Send |
| `save_fact` | Read & edit | A fact about a person or organization (`id`, `text`, `kind`: fact, preference, commitment or event, optional `until`), through `Store.remember_fact`, source "AI: <name>" |
| `update_record` | Read & edit | Details (`details`: a person's title, location, linkedin_url, notes; an organization's own fields), the owner's own fields by name (`fields`) and tags (`add_tags`, `remove_tags`), through the dashboard's own paths (`graph.person_edit`/`org_edit`, `crm_fields.set_value`/`tag`) |
| `add_summary_line` | Read & edit | A line on a person's summary (`id`, `text`), shown "AI: <name>" (`person_summary.add_line`) |
| `search_messages` | Read, with Messages on | Messages by words (`query`, optional), `channel`, `area`, newest first: who, when, subject and the first 300 characters, each with its thread. With `person` (an id from `search_graph`): only the messages with that person or organization, from every address and number merged into them, as their Graph page's timeline has them |
| `read_thread` | Read, with Messages on | The thread or chat around one message (`id`), oldest first, up to 30 messages of up to 4000 characters |

Every tool is listed to every connection. A tool above the connection's level is refused with what to change and where,
and the refusal is logged. The AI can't raise its own level.

**Never.** No send, no Do it, no calendar write, no change to an existing to-do. In the Graph never a merge, a delete, a
name, an organization or role, a Work or Personal side, sharing or an owner: those tools don't exist and
`update_record` refuses those keys.

**To-dos from an AI** are marked reviewed, like a Fleet request (`App.fleet_card`): no review or preparation reads them
by themselves, and the owner sees "From Claude" on them. A draft goes out only when the owner taps Send.

**Limits.** At most 20 new to-dos and 50 Graph changes a day per connection.

**Marked untrusted.** Text that came from other people, or that The Machine wrote from what they sent, goes out inside
`<untrusted source="...">` and `</untrusted>` (`ai_access.untrusted`): message subjects, senders and text (source: the
channel), to-do titles and text and drafts (`messages`, or `ai` for a connected AI's), a to-do's source subjects and
senders, promise text, an organization's `about` (`web`) and team briefs (`team`). The owner's own to-dos (New to-do)
go out unmarked. A marker inside the text is escaped (`&lt;/untrusted>`), so an email can't close the block and write
outside it. The server's instructions and each of these tools' descriptions say marked text is data, never
instructions, so an email can't steer the AI into using its other tools.

**A summary line** is not an owner's edit. The owner can edit or remove it. The next summary pass gets it as data
(`ai_lines`, ids A1…) and may keep, revise or drop it; a line citing it keeps the AI's name and area.

## Messages

A connection's own switch, off until the owner turns it on: on the consent page (a box, never ticked to start with) or
in Settings, AIs (`ai_change` with `messages`). Without it `search_messages` and `read_thread` are refused and logged
("Refused: Messages is off for this connection").

**What it reads.** Only messages (mail, Slack, WhatsApp, Telegram, LinkedIn, Intercom, X DMs: `ai_app.CHANNEL_KINDS`),
through `Store.events` (never deleted messages), in the connection's area. Never returned, whoever asks:

- anything that is not a message (calendar, transcripts, notices);
- one-time codes and sign-in links (the text is replaced, as the chat sources do when they store one);
- messages of an Only you board or project (`graph.hidden_event_ids`);
- threads the Shared Graph's review judged sensitive, or that the owner kept private by hand (`share_threads`);
- for a Work-only connection, threads the review found are the owner's own life.

**Logged, never copied.** Every read is an Activity line with how many messages and which threads (subject or chat
name), never the text (`READ_DETAIL`).

**Marked.** Senders, subjects and text go out inside `<untrusted>` (see Marked untrusted above), with a note and the
server's instructions saying it is data, never instructions.

**Changes wait.** While Messages is on, a Read & edit connection's Graph changes (`WRITES`) don't apply, since what the
AI read may have steered them. The record is checked as for any change (area, refusals), and the call is kept as a
waiting row in `ai_writes` (`waiting` 1, `changes` the AI's arguments). Its Activity line says "Waiting for your OK" with:

- **Apply** (`ai_apply`): the same tool runs now as the owner's OK, with the connection's area as it is then, and the
  line gets its Undo.
- **Dismiss** (`ai_dismiss`): nothing changes, and the line says "Not applied".

Read connections are unaffected, and so is a Read & edit one with Messages off.

## Graph changes and Undo

A Graph change applies at once and is a line in Activity (kind `ai`, the AI's name as `where`) with **Undo**. Each change
keeps the state of what it touched before and after (`ai_writes.changes`, sealed at rest like the activity detail): the
fact, the record's edits (`graph.edits_state`), its field values and tags (`crm_fields.state`), or the summary
(`person_summary.state`).

- **Undo** (`ai_undo`, an owner dashboard action, never an MCP tool) puts the before state back exactly, through each
  owner module's `restore`. When the current state differs from the stored after state, someone changed it since, and
  Undo is refused with a message to change it on the page instead.
- **Refused and logged:** a change the area doesn't reach (a Personal person for a Work connection, a teammate's record,
  the owner), and any write from a Read connection.
- **Area.** What an AI saves is in its area: Work or Personal, and with both the record's (a person's side, else Work). A
  fact keeps it (`facts.side`): a preparation for a to-do in the other area leaves it out (`Store.facts_for`), and a
  summary line citing it is in that area.
- **Untrusted.** An AI's fact or summary line is that AI's claim, never the owner's word, and shows "AI: <name>" in
  What I've learned. In every prompt it goes as data with who saved it: preparations and reviews get AI facts after the
  owner's, inside a `<<<` `>>>` block under `AI_FACTS_HEAD` (`Store.facts_block`), the summary turn gets `saved_by` on
  facts and AI lines apart from the current summary, corrections and the Graph's open line say "saved by <name>", and
  team learnings leave AI facts out.

## Signing in

### OAuth 2.1 (Claude, ChatGPT, Cursor, Codex, GBrain)

The Machine is its own authorization server and resource server, on either way in. The official app's account is only
one more client of it.

- `GET /.well-known/oauth-protected-resource` (also with `/mcp` appended, RFC 9728): the resource (`<base>/mcp`), the
  authorization server, scopes `read` and `draft`.
- `GET /.well-known/oauth-authorization-server` (RFC 8414): endpoints; `code` only; `authorization_code` and
  `refresh_token`; PKCE `S256` only; client authentication `none`, `client_secret_post` or `client_secret_basic`.
- `POST /oauth/register` (RFC 7591, dynamic client registration): redirect URIs must be https, a loopback http address
  (any port, RFC 8252) or an app's own scheme (`cursor://...`), ASCII only. A registration grants nothing. Unused ones
  go after a day; at most 30 new ones an hour.
- `GET /oauth/authorize`: the owner's own page, behind the dashboard's sign-in (Tailscale on a self-hosted Machine, the
  account's two-factor sign-in on a hosted one). It needs `code_challenge` with `S256` and an exact `redirect_uri`;
  `resource`, when given, must be this Machine's `/mcp`. It shows the AI (known ones by where they send back: claude.ai,
  chatgpt.com, cursor, gbrain.io; any other as "unverified" with its address), and the owner picks the access, the
  area, Messages and the expiry, then **Connect** or **Cancel**. Posting it needs the dashboard's own origin and its CSRF
  token.
- `POST /oauth/token`: `authorization_code` with the `code_verifier` (checked against the challenge, constant time), the
  same `redirect_uri` and `client_id`. A code works once, for 5 minutes; a code used twice revokes what it gave. Access
  tokens last an hour. Refresh tokens rotate on every use and end with the connection; one used twice revokes the
  connection's tokens. `refresh_token` checks the client too.
- `POST /oauth/revoke` (RFC 7009).

Codes, tokens, keys and client secrets are 32 random bytes, kept only as their SHA-256 and compared by it. None is
logged: the service logs no paths with queries or bodies, and errors name only their kind.

### A key

**Add a key** in Settings makes a connection with a key (`tm_ai_` and 43 characters), shown once, for clients that can't
do OAuth (a script, an older client). It is sent as `Authorization: Bearer <key>`. Same access, area, expiry, Turn off
now and Activity as any connection.

## The endpoint

`POST /mcp` is MCP over Streamable HTTP: JSON-RPC in, JSON out, no sessions and no server-sent events (`GET` and `DELETE`
answer 405). Methods: `initialize`, `ping`, `tools/list`, `tools/call`.

- Without a valid token it answers 401 with `WWW-Authenticate: Bearer
  resource_metadata="<base>/.well-known/oauth-protected-resource/mcp"`, which is how Claude and ChatGPT find the sign-in.
- No cookies are read and no CORS headers are sent. The owner's sign-in and the service's own token never count here.
- At most 120 calls a minute per connection.
- Text that came from someone else (an email's subject, a to-do the review wrote from a message) is returned as data,
  and the server's instructions say so.

## Where it runs

Every Machine has one private address, `https://<name>.mcp.themachine.computer/mcp`, the same on a hosted and a
self-hosted Machine. `<name>` is the account's name (hosted: the dashboard host's first label). The address is a door
only: nothing gets in without the owner approving that AI on the Machine's own consent page.

**TLS passthrough.** `*.mcp.themachine.computer` goes to a router in the cloud that forwards the encrypted connection by
its name (SNI) and never ends TLS ([The cloud forwards, never reads](network.md#the-cloud-forwards-never-reads)). The
Machine holds the certificate and key for its name. A hosted Machine gets its certificate in its Caddy (Let's Encrypt
only, no email address). A paired self-hosted one does it in `ai_reach.py`:

- **Dial-back.** It has no public port, so it asks: `GET /api/fleet/mcp-wait?wait=25` with its device token answers
  `{conns: [id]}`. For each it opens `GET /api/fleet/mcp-stream/<id>` (`Connection: Upgrade`, `Upgrade:
  tm-mcp-stream/1`); after `101` the AI's own TLS bytes follow, its hello first. A 401 stops the loop (the token is
  gone), and so does Unpair.
- **TLS on the Machine.** It reads the hello's name and ALPN and answers with its own certificate for
  `<name>.mcp.themachine.computer`, or, for a certificate authority checking it (ALPN `acme-tls/1`), with the challenge
  certificate.
- **Only the public paths**: `/mcp`, `/.well-known/oauth-*`, `/oauth/token`, `/oauth/register`, `/oauth/revoke`, into the
  same handlers as the dashboard's, with no owner sign-in. Anything else is 404. On this host the issuer and the resource
  are `https://<name>.mcp.themachine.computer` (and `/mcp`). The authorization endpoint stays on the dashboard, behind
  the owner's own sign-in, and the consent page reports the issuer the AI asked (RFC 9207).
- **The certificate**: ACME (RFC 8555) with TLS-ALPN-01 (RFC 8737), from Let's Encrypt only, on an account with no
  contact. A failed try or a rate limit waits 10 minutes, doubling up to a day, or the CA's `Retry-After` when longer.
  Key and certificate stay next to the database (0600) and never leave the Machine; renewed with 30 days left; gone on
  Unpair. It needs the `cryptography` package: without it Settings, AIs says "Install the cryptography package to use
  this address" and nothing starts.
- **Request bodies**: `Content-Length` or `Transfer-Encoding: chunked` (extensions ignored, trailers dropped), up to 64 KB
  (413 past it, before reading more). Both headers at once is 400.

AIs in the owner's tailnet (Claude Code, Claude Desktop, Cursor, Codex, a local GBrain) can also use the dashboard's own
address with `/mcp`.

## Pairing

A self-hosted Machine that isn't paired yet shows **Get your address** (`pairing.py`):

1. `POST /api/fleet/pair-request` (no token) with the Machine's Network public keys (`network_crypto`), its label and the
   owner's addresses, signed with its own sign key over `tm-device-pair/1\n` + the JSON, plus `keys_sig`. The answer is
   one page on the account, `/pair/<id>` (opened only when it is https on the Network's own hosts), and a short code
   (base32 of sha256 of the sign key, `XXXX-XXXX`) that the dashboard shows too.
2. On that page the signed-in owner checks the code, confirms, and picks the account's name when it has none. The
   account pairs the device, publishes its keys, and seals the new token for the Machine's box key, bound to the request
   (`open_box` with info `tm-device-pair/1`, context `{p: pair, r: <id>}`).
3. The Machine picks it up (`POST /api/fleet/pair-pickup`, signed again) every 2 seconds for up to 10 minutes, opens it,
   writes it 0600 to `fleet-token` next to the database and into the config as the `fleet` credential (as `cli.py
   fleet-pair` does, which keeps working), and starts the Fleet at once (`App.fleet_live`), no restart.
   `GET /api/fleet/ai-reach` then gives the name for the address.

The same button pairs from Connections, where a sign-in needs a paired Machine. **Unpair** in Settings, AIs removes the
credential and its file, stops the Fleet and the dial-back, and drops the certificate. The account keeps the device
until it is disconnected there.

## Decided

- One endpoint per Machine, end to end, and next to it the official app's shared address. On the shared address the
  account signs in and routes, but the Machine still issues and checks every token and holds the data.
- Self-hosted Machines reach cloud AIs through TLS passthrough, never a proxy that reads the calls.
- Tools never send. Sending after the owner approves is the owner's Send on the to-do, not a tool.
