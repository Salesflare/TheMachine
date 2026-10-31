# Connected AIs (MCP)

Other AIs (Claude, ChatGPT, Cursor, Codex, GBrain and anything else that speaks MCP) can connect to a Machine. They can
read to-dos, team briefs, people and companies in the Graph, and promises. At most they add a to-do, or a to-do with an
email draft that waits for the owner. They never send and never act. This page is the design. What the owner sees is
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
| `create_todo` | Read & draft | A new to-do with the AI's text, marked as coming from that AI |
| `create_draft` | Read & draft | A new to-do with an email draft (to, subject, text) from one of the owner's mail accounts, waiting for the owner's Send |

Nothing else: no send, no Do it, no calendar write, no change to an existing to-do, no Graph edit. A to-do an AI adds
is marked reviewed, like a Fleet request (`App.fleet_card`): no review or preparation reads it by itself, and the
owner sees "From Claude" on it. A draft goes out only when the owner taps Send on it, as any draft. At most 20 new
to-dos a day per connection.

Every tool is listed to every connection. A tool above its level is refused with what to change and where, and the
refusal is logged; the AI cannot raise its own level.

## Connections

Each AI that connects is one connection, with:

- **Access**: Off, Read, or Read & draft. Changed in Settings at any time; the next call uses it, nothing reconnects.
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

**Self-hosted.** The app serves it on the dashboard's address, `https://<dashboard host>/mcp`. AIs that run on a device
in the owner's tailnet reach it: Claude Code, Claude Desktop, Cursor, Codex, a local GBrain. Cloud AIs (claude.ai,
ChatGPT) can't reach a tailnet. For those, the owner can publish the dashboard's address themselves (Tailscale Funnel);
The Machine does not relay a self-hosted Machine's calls through the cloud, because the cloud would then see them in
the clear, which it never does for a self-hosted Machine today.

**Hosted.** The dashboard's own address, `https://<name>.app.themachine.computer/mcp`. The control plane's proxy
already carries the dashboard there (TLS to the browser, TLS with our own CA to the Machine, nothing kept). The MCP
and OAuth paths take that same proxy without the owner's browser sign-in: the control plane checks only that the
Machine exists and is running (`/_machine/ai-check`), strips cookies, the AI's `Authorization` from that check, and
marks the request (`X-Machine-Route: ai`) so the Machine's own Caddy drops the owner's identity for it. The Machine
checks the token itself. `/oauth/authorize` stays behind the owner's sign-in; signed out, the account sign-in comes
back to it afterwards. So the cloud sees these calls exactly as it sees the dashboard: in transit, never stored, never
logged (Caddy's log filter drops `Authorization` and query strings).

## Decided, and open

- One endpoint per Machine, not one shared cloud endpoint: tokens and data stay on the Machine, and the control
  plane needs no new store.
- Relaying self-hosted Machines for cloud AIs: not built (see above). Possible later as an opt-in, saying the cloud
  sees the calls in transit.
- Tools never send. A "send after the owner approves in The Machine" flow is the owner's Send on the to-do, not a tool.
