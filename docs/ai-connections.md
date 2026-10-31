# Connected AIs (MCP)

Other AIs (Claude, ChatGPT, Cursor, Codex, GBrain and anything else that speaks MCP) can connect to a Machine. They can
read to-dos, team briefs, people and companies in the Graph, and promises. With Read & edit they also add a to-do, or
a to-do with an email draft that waits for the owner, and make Graph changes the owner can undo. They never send and
never act. This page is the design. What the owner sees is
in [the help article](help/ai-connections.md).

This is about AIs from outside only. The Machine's own agent, Do it, coding agents and their permissions are not
touched by any of it.

## What an AI can do

| tool | level | what |
|---|---|---|
| `list_todos` | Read | Open (or snoozed, or recently done) to-dos: title, text, status, due date, Work or Personal, project |
| `get_todo` | Read | One to-do, with its ready draft if it has one and where it came from (sender, subject, date; no message bodies) |
| `list_promises` | Read | Open promises: who promised what to whom, and by when |
| `search_graph` | Read | People, organizations and projects in the Graph that match a name, email or company |
| `get_graph_record` | Read | One person, organization or project: role, organization, closeness, last contact, open to-dos, promises |
| `get_team_brief` | Read | The latest team brief of each Work Fleet, as the Fleet tab shows it |
| `create_todo` | Read & edit | A new to-do with the AI's text, marked as coming from that AI |
| `create_draft` | Read & edit | A new to-do with an email draft (to, subject, text) from one of the owner's mail accounts, waiting for the owner's Send |
| `save_fact` | Read & edit | A fact about a person or organization (`id`, `text`, `kind`: fact, preference, commitment or event, optional `until`), through `Store.remember_fact`, with source "AI: <name>" |
| `update_record` | Read & edit | A person's or organization's details (`details`: title, location, linkedin_url, notes; an organization's own fields), CRM fields by name (`fields`) and tags (`add_tags`, `remove_tags`), through the dashboard's own paths (`graph.person_edit`/`org_edit`, `crm_fields.set_value`/`tag`) |
| `add_summary_line` | Read & edit | A line on a person's summary (`id`, `text`), kept like an owner's edit, so the summary writer keeps it (`person_summary.add_line`) |

Nothing else: no send, no Do it, no calendar write, no change to an existing to-do. In the Graph never a merge, a
delete, a name, an organization or role, a Work or Personal side, sharing or an owner: those tools do not exist and
`update_record` refuses those keys. A to-do an AI adds
is marked reviewed, like a Fleet request (`App.fleet_card`): no review or preparation reads it by itself, and the
owner sees "From Claude" on it. A draft goes out only when the owner taps Send on it, as any draft. At most 20 new
to-dos and 50 Graph changes a day per connection.

### Graph changes and Undo

A Graph change applies at once and is a line in Activity (kind `ai`, the AI's name as `where`) with **Undo**. Each
change keeps the state of what it touched before and after (`ai_writes.changes`, sealed at rest like the activity
detail): the fact, the record's edits (`graph.edits_state`), its CRM values and tags (`crm_fields.state`), or the
summary (`person_summary.state`). Undo (`ai_undo`, an owner dashboard action, never an MCP tool) puts the before
state back exactly, through each owner module's `restore`. When the current state differs from the stored after
state, someone changed it since, and Undo is refused with a message to change it on the page instead. A change the
area does not reach (a Personal person for a Work connection, a teammate's record, the owner) is refused and logged,
as is any write from a Read connection. A fact from an AI shows "AI: <name>" in What I've learned; a summary line
shows it too.

Every tool is listed to every connection. A tool above its level is refused with what to change and where, and the
refusal is logged; the AI cannot raise its own level.

## Connections

Each AI that connects is one connection, with:

- **Access**: Off, Read, or Read & edit (stored as `draft`, its old name). Changed in Settings at any time; the next call uses it, nothing reconnects.
- **Area**: Work, Personal or both (the choice shows only when the Machine has both). Work and Personal follow the
  accounts, as on to-dos (`suggestion_scope`): to-dos and promises by their accounts, people by their side in the
  Graph, organizations and projects only with Work, team briefs only with Work.
- **Expires**: after 1 day, 7 days, 30 days or 1 year. An expired connection is refused (and logged) until the owner
  extends it or the AI signs in again.
- **Turn off now**: Off and every token of it revoked at once.
- **Activity**: every call, refused ones included, with the tool, when, and the outcome ("3 to-dos", "Refused: this
  connection can only read"). Kept 90 days, at most 2000 lines per connection, the line's detail sealed at rest with
  the message key (`ai_activity.detail` in `message_seal.DERIVED`).
  The lines are kind `ai` of Settings, **Activity** (`activity_log.register('ai', ai_access.activity_lines)`, actor
  the connection), so they show with everything else The Machine did, under Refused or blocked when refused; a
  connection's own activity is that list filtered to it (`/api/activity?kind=ai&actor=<id>`).

Settings, **Connected AIs** lists them, with each one's activity, and **Add a key** for an AI that needs one.

**Work Fleet data.** Only what the owner sees of it already: their own to-dos (a Fleet request they took is one), and
the team brief their Fleet tab shows (counts, dates and company names, built under the Fleet's rules). Teammates'
Team Graph records and threads are never given to an outside AI, the same rule as [GBrain](gbrain.md)'s sync.

## Signing in

### OAuth 2.1 (Claude, ChatGPT, Cursor, Codex, GBrain)

The Machine is its own authorization server and resource server. Nothing about it lives on the control plane.

- `GET /.well-known/oauth-protected-resource` (also `/mcp` appended, RFC 9728): the resource (`<base>/mcp`), the
  authorization server, scopes `read` and `draft`.
- `GET /.well-known/oauth-authorization-server` (RFC 8414): endpoints; `code` only; `authorization_code` and
  `refresh_token`; PKCE `S256` only; client authentication `none`, `client_secret_post` or `client_secret_basic`.
- `POST /oauth/register` (RFC 7591, dynamic client registration): redirect URIs must be https, a loopback http
  address (any port, RFC 8252) or an app's own scheme (`cursor://...`), ASCII only. A registration grants
  nothing. Unused registrations go after a day; at most 30 new ones an hour.
- `GET /oauth/authorize`: the owner's own page (the dashboard's sign-in: Tailscale on a self-hosted Machine, the
  account's two-factor sign-in on a hosted one). It needs `code_challenge` with `S256`, an exact `redirect_uri`, and
  `resource` when given must be this Machine's `/mcp`. It shows the AI (known ones by where they send back: claude.ai,
  chatgpt.com, cursor, gbrain.io; any other as "unverified" with its address), and the owner picks the access, the
  area and the expiry, then **Connect** or **Cancel**. Posting it needs the dashboard's own origin and its CSRF token.
- `POST /oauth/token`: `authorization_code` with the `code_verifier` (checked against the challenge, constant time),
  the same `redirect_uri` and `client_id`. A code works once, for 5 minutes; a code used twice revokes what it gave.
  Access tokens last an hour, refresh tokens rotate on every use and end with the connection; a refresh token used
  twice revokes the connection's tokens (someone else has it). `refresh_token` checks the client too.
- `POST /oauth/revoke` (RFC 7009).

Codes, access tokens, refresh tokens, keys and client secrets are 32 random bytes, kept only as their SHA-256 and
compared by it. None is logged: the service logs no paths with queries or bodies, and errors name only their kind.

### A key

**Add a key** in Settings makes a connection with a key (`tm_ai_` and 43 characters), shown once, for clients that
can't do OAuth (a script, an older client). It is sent as `Authorization: Bearer <key>`. Same access, area, expiry,
Turn off now and activity as any connection.

## The endpoint

`POST /mcp` is MCP over Streamable HTTP: JSON-RPC in, JSON out, no sessions and no server-sent events (`GET` and
`DELETE` answer 405). `initialize`, `ping`, `tools/list`, `tools/call`. Without a valid token it answers 401 with
`WWW-Authenticate: Bearer resource_metadata="<base>/.well-known/oauth-protected-resource/mcp"`, which is how
Claude and ChatGPT find the sign-in. No cookies are read, no CORS headers are sent, and the owner's sign-in or the
service's own token never count on these paths. At most 120 calls a minute per connection.

Text that came from someone else (an email's subject, a to-do the review wrote from a message) is returned as data, and
the server's instructions say so: an AI should not follow instructions inside it.

## Where it runs

Every Machine has one address for AIs, `https://<name>.mcp.themachine.computer/mcp`, the same on a hosted and a
self-hosted Machine. `<name>` is the account's name (hosted: the dashboard host's first label). Settings, **AIs**
shows it with Copy and three steps each for ChatGPT and Claude. The address is a door only: nothing gets in without
the owner approving that AI on the Machine's own consent page.

**On its own host, with TLS passthrough.** `*.mcp.themachine.computer` goes to a router in the cloud that forwards
the encrypted connection by its name (SNI) and never ends TLS: the Machine holds the certificate and key for its name
and terminates TLS itself, so the cloud never sees what an AI and the Machine say (docs/network.md, The cloud
forwards, never reads). A hosted Machine does its certificate in its Caddy (Let's Encrypt only, no email address). A
self-hosted one, once paired, does it in `ai_reach.py`:

- **Dial-back.** It has no public port, so it asks: `GET /api/fleet/mcp-wait?wait=25` with its device token answers
  `{conns: [id]}`. For each it opens `GET /api/fleet/mcp-stream/<id>` (`Connection: Upgrade`,
  `Upgrade: tm-mcp-stream/1`); after `101` the AI's own TLS bytes follow, its hello first. A 401 stops the loop (the
  token is gone). Unpair stops it too.
- **TLS on the Machine.** It reads the hello's name and ALPN and answers with its own certificate for
  `<name>.mcp.themachine.computer`, or, for a certificate authority checking it (ALPN `acme-tls/1`), with the
  challenge certificate.
- **Only the public paths**: `/mcp`, `/.well-known/oauth-*`, `/oauth/token`, `/oauth/register`, `/oauth/revoke`, into
  the same handlers as the dashboard's, with no owner sign-in. Anything else is 404. On this host the issuer and the
  resource are `https://<name>.mcp.themachine.computer` (and `/mcp`); the authorization endpoint stays on the
  dashboard, behind the owner's own sign-in, and the consent page reports the issuer the AI asked (RFC 9207).
- **The certificate**: ACME (RFC 8555) with TLS-ALPN-01 (RFC 8737), from Let's Encrypt only, on an ACME account with
  no contact: no email address goes to a third party. A failed try or a rate limit waits 10 minutes, doubling up to a
  day, or the CA's `Retry-After` when that is longer. Key and certificate stay next to the database (0600) and never
  leave the Machine; renewed with 30 days left; gone on Unpair. It needs the `cryptography` package: without it
  Settings, AIs says "Install the cryptography package to use this address" and nothing starts.
- **Request bodies**: `Content-Length` or `Transfer-Encoding: chunked` (extensions ignored, trailers dropped), up to
  64 KB (413 past it, before reading more). Both headers at once is 400.

**The address goes live once the passthrough ships** in the cloud. Until then, AIs in the owner's tailnet (Claude
Code, Claude Desktop, Cursor, Codex, a local GBrain) use the dashboard's own address with `/mcp`.

**Pairing in one click** (`pairing.py`). A self-hosted Machine not paired yet shows **Get your address**:

1. `POST /api/fleet/pair-request` (no token) with the Machine's Network public keys (`network_crypto`, the keys the
   Network pins), its label and the owner's addresses, signed with its own sign key over
   `tm-device-pair/1\n` + the JSON, plus `keys_sig` (its usual signature of the keys). The answer is one page on the
   account, `/pair/<id>` (opened only when it is https on the Network's own hosts), and a short code
   (base32 of sha256 of the sign key, `XXXX-XXXX`) that the dashboard shows too.
2. On that page the signed-in owner checks the code and confirms, and picks the account's name when it has none. The
   control plane pairs the device, publishes its keys, and seals the new token for the Machine's box key, bound to the
   request (`open_box` with info `tm-device-pair/1`, context `{p: pair, r: <id>}`).
3. The Machine picks it up (`POST /api/fleet/pair-pickup`, signed again) every 2 seconds for up to 10 minutes, opens
   it, writes it 0600 to `fleet-token` next to the database and into the config as the `fleet` credential (as
   `cli.py fleet-pair` does, which keeps working), and starts the Fleet at once (`App.fleet_live`), no restart.
   `GET /api/fleet/ai-reach` then gives the name for the address.

The same button pairs from Connections, where a sign-in needs a paired Machine. **Unpair** in Settings, AIs removes the
credential and its file, stops the Fleet and the dial-back, and drops the certificate; the account keeps the device
until it is disconnected there.

## Decided, and open

- One endpoint per Machine, not one shared cloud endpoint: tokens and data stay on the Machine, and the control
  plane needs no new store.
- Self-hosted Machines reach cloud AIs through TLS passthrough on `*.mcp.themachine.computer`, never a relay that
  reads the calls: the cloud forwards encrypted bytes by name and keeps nothing.
- Tools never send. A "send after the owner approves in The Machine" flow is the owner's Send on the to-do, not a tool.
