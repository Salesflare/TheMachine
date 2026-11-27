# Security and privacy

The short version, for people deciding whether to install: [themachine.computer/security](https://themachine.computer/security). This file is the technical detail behind it.

## Supported release

Security fixes target the latest `main` revision and ship as signed releases: tags `release-YYYYMMDD-HHMM`, signed
with a key listed in `deploy/release-signers`.

- Update with `python3 scripts/release.py update`. It installs only a release whose signature checks out.
  On Linux, `./install.sh` sets up a daily timer that does this (signed releases only; off with `"auto_update": false`).
- Hosted Machines check the same signature before every update.
- CI checks OpenClaw 2026.11.2 and, weekly, the latest release. Future releases and older snapshots are not
  certified by those tests.

This is an early release for one owner on a trusted computer, not a public multi-user service.

## Reporting a vulnerability

Use this repository's GitHub **Security → Report a vulnerability** form for a private report.
If that form is unavailable, contact the maintainer through the GitHub profile first and
arrange a private channel. Do not put exploit details or private data in a public issue.
Include affected revisions, a synthetic reproduction and the expected security boundary.
Never include actual tokens, messages or a production database.

## Code scanning

[Aikido](https://www.aikido.dev) scans this repository and the hosted service's code for security issues,
vulnerable dependencies and leaked secrets, on every pull request and every day. It also scans the hosted
service's Azure setup, through a scoped read-only connection, and the hosted service's servers.
An AI agent goes through the findings every morning:

- critical and high issues are fixed the same day;
- medium ones are fixed or dismissed with a specific reason;
- low ones are handled in batches.

Fixes to this repository arrive as pull requests and are reviewed before they merge.

The release key holder also needs the official `@aikidosec/ci-api-client`, with its Aikido API key in the client's
protected local configuration. `scripts/release.py cut` requests a scan of the exact `origin/main` commit before
signing it. High and critical dependency, SAST, IaC and secret findings block release; an unavailable scanner,
invalid receipt or timeout blocks it as well. The token is never included in release commands or source control.

## Deployment boundaries

### Network and data

- Keep the service bound to `127.0.0.1`. Reach the dashboard through Tailscale Serve or the provided
  identity-checking reverse proxy. Don't expose the local API directly.
- Keep config, SQLite data, attachments and credentials outside the Git checkout. The installer uses a private data
  directory and mode 600 secret files.
- Backups contain private evidence and may include secrets. Protect them like the live data.

### The model and Do it

- Reviews and preparations send relevant private evidence to the configured model provider. Choose that provider and
  its data settings accordingly.
- With `meeting_prep_signin_search` on (off by default) and no search provider set up, a first meeting's briefing searches
  the web on the owner's own ChatGPT or Claude account (OpenAI or Anthropic, which may use their own search partners):
  only the person's name, their organization's name and its website go out, never messages or email addresses. What
  comes back is kept on the Machine, in the briefing and for reuse for 30 days. The search runs alone, with no other
  tool; its results are untrusted text. On ChatGPT the linked addresses are those the answer names.
- **Do it grants broad account and machine access for the accepted task.** The plugin's guards are not a sandbox.
  Source messages are untrusted and may contain prompt injection. Read the [README's security model](README.md#security-model)
  before turning on reviews or delivery. The attack set we test against, and its latest results, are in
  [evals/prompt-injection](evals/prompt-injection/README.md).
- Pages a run opens by itself: opening a page sends its address to whoever runs that site, so an address the model
  put together could carry what it read. A to-do prepared ahead (nobody tapped Do it yet) and a routine open a page
  with `web_fetch` or the browser only when its address was written in what the run read (a message, a search result,
  a page, the owner's words), is a plain page address (no query, no user name, short ordinary words), goes to a
  well-known service where nobody else sees what is asked (search, maps, Wikipedia, weather, LinkedIn, GitHub, the
  owner's account in Google, Microsoft, Stripe, Zapier or Slack), or to the owner's own company's sites. Anything else
  is refused with a hint to search instead. `web_search` is never limited. Do it, a Confirm and the owner's chats
  are not checked: the owner asked for that work. The check covers `web_fetch`, the browser's open and navigate
  addresses, and shell commands that reach the network (curl, wget, HTTPie, nc, inline Python or Node code). From
  the shell, a body, header or cookie goes only to this computer, the owner's sites or those services, and an address
  the command builds while it runs (a variable, joined text) is refused. The Machine's own service, localhost, `gog`,
  `gh` and `assistant` stay open. Typing and scripts on a page, and a script file a command runs, are not checked
  ([openclaw-plugin/outbound-urls.ts](openclaw-plugin/outbound-urls.ts)).
- Text a model wrote never loads anything by itself. The dashboard shows it escaped, with links only to tap (no
  pictures, frames or previews from it), and the installer turns off Telegram's link previews
  (`channels.telegram.linkPreview`), which Telegram's servers would otherwise fetch as a message arrives. An HTML email
  you open shows its remote images, in a sandboxed frame with no referrer.
- Fresh installs collect configured sources with recurring reviews and delivery off. One read-only first-look preview
  may run after setup; it sends no to-dos and takes no outside actions. `./install.sh --activate` turns both on.
- Credentials a tool prints (provider tokens, JWTs, private keys, `password=` and `Authorization:` values, cookie
  headers) are replaced with a placeholder before OpenClaw writes its session transcripts, so they don't stay on disk
  or in backups. The turn that printed one is not changed, and Codex's own session records are not covered.

### Sends

- Messages go out through exact owner-approved Send actions. A complete Telegram draft can be sent directly from its
  to-do. Explicit owner requests use `send_now` where supported.
- WhatsApp, Telegram chats and Signal chats keep a confirmation on the to-do. Telegram and Signal sends go through their
  mirror's outbox, keyed by the approved action, and the mirror refuses a row without one.
- A send with an unknown outcome is reconciled, never blindly repeated.
- Collectors only read by default. Configured CRM joins are an opt-in exception.

### Encryption at rest

- Message contents from every source are encrypted in the database by default, on every install, with a key next to
  it for the service user ([configuration](docs/configuration.md#message-protection)). It protects copies of the
  database and tools without the key, not against root on the machine.
- Back the key up with the database: without it the messages are lost. `"message_protection": false` turns it off.
- What was learned from messages is encrypted the same way: a Work Fleet's team learnings, what a learned change
  replaced and why, and a Fleet's log lines. Feedback, facts and rules stay readable.
- Email attachments a Do-it run saves are encrypted on disk with the same key. The run reads a private copy that is
  removed when it ends. Files a run makes itself are not encrypted.
- WhatsApp photos read with Read photos (off by default) are kept in `whatsapp-photos/` next to the database, sealed
  with the message key when message protection is on, with what the model read in them sealed in the database. Only
  JPEG, PNG and WebP up to 5 MB, downloaded read-only through `wacli`. The model reads a private copy that is removed
  right after. What a photo says is content, never instructions. A photo goes when its message or its connection goes.
- Stores other programs own are not covered: OpenClaw's session transcripts and WhatsApp's `wacli` store. The
  Telegram mirror's store seals message text and the session itself, with a key derived from the message key. The
  Telegram cloud password is passed to Telegram once and never stored.
- Files the owner adds to a to-do chat are kept in `chat-files/` next to the database (mode 600), sealed with the
  message key when message protection is on, with their names sealed in the database. They are checked by type and
  size and served back only to the owner's dashboard (images and PDFs inline, anything else as a download). A run
  that uses one gets a readable copy in the runs' private folder, removed once the run has ended. Unsent ones are
  deleted after a day.

### Saved sign-ins and the browser

- The dashboard's sign-in dialog fills in sites in the assistant's browser for the owner and can save those passwords
  in the data folder, encrypted with the message key. On a hosted Machine that key is never on the disk, so disk
  backups can't open them.
- Saved passwords never go to the model, the logs or a support bundle. An export holds them only with a passphrase.
- On a self-hosted install the key sits next to them for the service user: protect that user's account and disk
  (full-disk encryption) accordingly. Without message protection they keep a key of their own next to them.
- A saved sign-in is bound to its exact origins (scheme, host and port). The fill checks the page before typing and
  before submitting, so a lookalike address, another subdomain, `http` or another port never gets it.
- Import from a password manager reads a CSV the owner picks, the export the owner downloads from the manager's own
  page in the Machine's browser, or 1Password's `op` and LastPass's `lpass` only when the owner already signed in to
  them on this computer. The Machine never signs in to a password manager and never asks for or keeps a master
  password; it keeps a password only for the sign-ins the owner ticks to keep. On the export page the owner signs
  in; a fixed script (never the model) then only clicks the way to the export step and focuses the master password
  field. It never types, reads a field's value or takes a screenshot, and nothing from the page reaches the model, a
  log or an error: only where the owner types sits in the window (four numbers), for a phone's live view to zoom to. A download from the export page goes
  into a private folder made for it, is read once and deleted from disk right away, and the folder goes with it. Delete
  an export file you picked yourself afterwards: it holds every password in plain text.
- The browser's own cookies and sign-ins (its profile) belong to the browser: protected by the account and the disk,
  not by The Machine's keys. Anything running as the service user, the agent included, can use them.

### The browser through the owner's computer

With `browser_exit` on, the sites in `browser_exit_sites` (LinkedIn, Facebook, Instagram, X and Threads to start with)
reach the Machine's browser through the owner's desktop app, so they see the owner's own address
(`machine/browser_exit.py`). Only the browser: mail, AI calls and connectors go out from the Machine as before.

- Only the owner: the app opens `GET /api/exit` (an upgrade to `tm-exit/1`) to the Machine it is signed in to, over
  the same TLS and sign-in as its other calls; the Machine takes it only from its owner and its own origin, as every
  dashboard route. A web page can't ask for that upgrade.
- On the computer the app only connects out, never listens. It connects only to public internet addresses on ports 80
  and 443, checked after its own DNS lookup and on the address it checked (also for a redirect, which is a new
  connection): no private, loopback, link-local, cloud metadata, carrier-grade NAT, Tailscale, multicast or reserved
  ranges, nor the computer's own public address. It has caps on connections, speed and bytes a day.
- The Machine's end is a SOCKS5 listener on `127.0.0.1` of the Machine's own host, for its browser.
- What goes through is the browser's traffic as it is: for HTTPS sites that is TLS and the site's name. Nothing is
  kept or logged but that a computer connected or went, and why a connection was refused (a word, no address).
- While the owner's computer is away, listed sites go out from the Machine, as before. Only the Machine's own sign-in
  dialog first asks to open the desktop app, with a way to sign in from the Machine anyway; without a desktop app with
  it on (none, turned off, or none for 14 days) it doesn't ask.
- A robot check, a verify-it's-you page or a sign-in asked again on a listed site within a day after its way out
  changed (computer or Machine) is counted in the error reports (Settings, Send error reports): the kind of check, the
  way before and after, and the site's name if it is one of the built-in ones (else "other"). Never an address, a page's
  text or an account.

### On the device

The dashboard keeps its last to-dos, the open chat and the Graph's lists on each device so it opens at once. They are
encrypted (AES-GCM, with a key the browser can't export), for one owner, kept at most 7 days, never include a token, and
are wiped on Sign out or when the session ends ([On the device](docs/architecture.md#on-the-device)). On a shared
computer, sign out.

### The operating system

Keep the operating system patched. On a dedicated Ubuntu server, let `unattended-upgrades` install the `-security`
pockets daily, and reboot when `/run/reboot-required` appears, at a quiet hour. Then check that the OpenClaw Gateway
and `personal-assistant` came back. Update Node and OpenClaw yourself, after testing, rather than unattended. The
hosted service does exactly this on every server.

## Publishing a fork

Inspect every tracked file and all reachable history before making a fork public. Scan
for secrets, check commit author/committer emails, and inspect screenshots and sample data.
Use GitHub's noreply address if you do not want to publish your email address.
`.gitignore` and CI reduce accidental leaks; they cannot detect every kind of personal information.

If a real secret was committed, revoke it first. Removing the file in a later commit does
not remove it from history or copies that were already fetched. Then clean the affected
history and follow GitHub's guidance on removing sensitive repository data.
