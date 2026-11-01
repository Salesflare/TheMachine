# The Machine

Your proactive AI assistant. It reads your email, chats, calendar and phone, turns what matters into to-dos, prepares the work, and only sends what you approve. Open source, on your own computer or hosted for you.

- **To-dos from everything that comes in:** Gmail, Outlook, Slack, WhatsApp, Telegram, LinkedIn, X, your calendar and phone notifications become one list of to-dos.
- **The work, prepared:** reply drafts, new or edited docs and the lookups behind them are ready when you open a to-do.
- **Nothing goes out unseen:** a draft is sent only after you've seen and approved it. Paying, booking or submitting waits for your yes.
- **Promises:** what you promised and what others promised you, tracked until it's kept.
- **Talk:** a live spoken conversation about a to-do or anything else (with OpenAI), and dictation into any message box.
- **People and projects:** the Graph keeps track of who you deal with and what's going on, with boards for deals, hiring and more.
- **Fleets:** your teammates' Machines answer each other's questions, sharing only what the Team Graph allows. A Family Fleet shares free times, to-dos and plans.
- **Connected AIs:** Claude, ChatGPT, Cursor and other AIs can read your to-dos and Graph over MCP, and add to-dos or Graph changes you can undo. They never send anything.

Website: [themachine.computer](https://themachine.computer). Rather not run it yourself? The same Machine is also [hosted for you](https://themachine.computer/pricing) on a private server in the EU (beta). Export and import move everything between the two.

**Early release.** One owner per installation. Runs on Linux; macOS and Windows are in beta. The core assistant needs no cloud account. Fleets and Friends connect through The Machine Network.

## Quick start

**Linux and macOS (beta):**

```bash
git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant
cd ~/.openclaw/workspace/tools/personal-assistant
./install.sh
```

**Windows (beta),** in PowerShell. It sets up WSL2 and runs the same installer inside it:

```powershell
irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex
```

- `./install.sh --dry-run` checks the prerequisites and shows what it would write, without changing anything.
- The installer sets up OpenClaw if needed, connects your sources and publishes your dashboard.
- It starts with a read-only preview. Turn on recurring reviews when the to-dos look useful.
- `assistant doctor` checks the setup without syncing your accounts.

The full walkthrough: [Getting started](docs/getting-started.md).

## Requirements

| | Linux | macOS (beta) | Windows (beta) |
|---|---|---|---|
| Runs as | systemd user service | launchd agent | systemd user service inside WSL2 (Ubuntu 24.04) |
| Install | `./install.sh` | `./install.sh` (Homebrew: `brew install python@3.12 node@24`) | `install.ps1` (above) |
| Logs | journald | `~/Library/Logs/TheMachine` | journald inside WSL |
| Not there yet | | Browser viewer, Gateway log source | Browser viewer |

- Your own user account, not root.
- **Python 3.12 or newer.** The app uses the standard library only.
- **Node.js** `>=24.22.1 <25` or `>=26.12.1` to install OpenClaw. An OpenClaw that is already set up keeps working on Node 24.16+ or 26.1+; update Node before you update OpenClaw. Node 22 and 25 are not supported.
- **[OpenClaw](https://docs.openclaw.ai) 2026.10.7 or later**, The Machine's agent runtime. The installer offers to install and set it up. A Telegram bot on it is optional: without one, to-dos reach you in the dashboard app.
- **Tailscale** to reach the dashboard (it serves only your Tailscale identity). Caddy only if you want it on your own domain (`deploy/Caddyfile`).
- Per source, only what you connect: `gog` for Gmail and Calendar, your own Microsoft Entra app for Outlook, `wacli` for WhatsApp, and so on. See [Sources](docs/sources.md) and [Getting started](docs/getting-started.md).

`assistant service status|start|stop|restart|logs` works the same on every system. `assistant support-bundle` saves versions, checks and recent logs in one file, without keys or tokens, to send when you need help. Beta means tested in CI but not yet run for long on a real computer.

## Documentation

| Topic | Guide |
|---|---|
| First install, sources, phone and preview | [Getting started](docs/getting-started.md) |
| Install flags, updates, backups, moving and recovery | [Operations](docs/operations.md) |
| Settings and defaults | [Configuration](docs/configuration.md), [example JSON](config.example.json) |
| Sources and their limits | [Sources](docs/sources.md) |
| Storage, reviews and promises | [Architecture](docs/architecture.md) |
| To-dos, Do it, snooze, work hours, sends and the CLI | [Usage](docs/usage.md) |
| Facts, people, projects, embeddings and enrichment | [Intelligence](docs/intelligence.md) |
| Model and provider setup | [Models](docs/models.md) |
| Work Fleets, Friends and The Machine Network | [Fleet](docs/fleet.md), [Network](docs/network.md), [Team Graph](docs/shared-graph.md) |
| Family Fleets: free times, to-dos and plans | [Family](docs/family.md) |
| Skills: write, approve and share them | [Skills](docs/skills.md) |
| Hand a to-do to Claude Code or Codex | [Coding agents](docs/agents.md) |
| Let other AIs read your to-dos and Graph over MCP | [Connected AIs](docs/ai-connections.md) |
| Dictation and Talk | [Voice input](docs/voice.md), [Talk](docs/talk-live.md) |
| Optional GBrain agent memory | [GBrain](docs/gbrain.md) |
| Add a connector | [Adding a source](docs/adding-a-source.md) |
| Sandbox, screenshots and layout checks | [Development](docs/development.md), [Design](docs/design.md) |
| Which module owns what | [Code map](docs/code-map.md) |
| Instructions for The Machine's agent | [AGENTS.md](AGENTS.md), [PREPARATION.md](PREPARATION.md) |
| What changed and why | [History](docs/history.md) |

Help for people using The Machine (not running it) is at [themachine.computer/help](https://themachine.computer/help), from the articles in [docs/help](docs/help).

## How it works

- Collects every source into one SQLite database on your Machine, on its own schedule.
- Reviews new messages and events in isolated turns of your main agent, with the model you picked. No second agent or model.
- Remembers your decisions, feedback, facts, people, projects and promises.
- Prepares likely useful work ahead, but never the last step that commits something.
- Does what you ask with **Do it**, and shows a **Send**, **Submit** or **Merge** button where something goes out.
- Shows the same to-dos on the dashboard, in its phone app and on Telegram.

The Machine is its own app. [OpenClaw](https://docs.openclaw.ai) is its agent runtime: OpenClaw's agent reads and thinks with your model, and its Gateway carries Telegram and the Android node. The Machine adds the dashboard, the Graph, to-dos, connections, Fleets and the Network.

### Work hours

To-dos and reminders reach you only within your work hours (by default Monday to Friday, 08:00 to 23:00). Work to-dos wait for a work day; personal ones keep their timing. Set them in **Settings**, with `assistant hours` or in `config.json`. More in [Usage](docs/usage.md#work-hours).

### Do it

**Do it** authorizes the offered task end to end. Verified written instructions authorize the exact action they ask for. Messages go out through the supported **Send** route; WhatsApp keeps a confirmation on the to-do. Full rules: [Usage](docs/usage.md#do-it) and [PREPARATION.md](PREPARATION.md).

### Prepared ahead

When a review is confident you'd say yes, the work starts before you tap anything. The to-do arrives done up to the one step that commits something: a draft with **Send**, a filled-in form with **Submit…**. That last step runs only on your confirm. Prepared work is not accepted work. More in [Usage](docs/usage.md#do-it).

### Promises

Reviews notice promises in messages: ones you made, and ones made to you. Each has its own page, closes when it's kept, and shows on the Calendar and on the people involved. More in [Architecture](docs/architecture.md#promises).

### The Machine fixes itself

The Machine records its own errors (never message content) and can fix them in a separate clone, with a test. Small proven fixes merge by themselves and can be undone for 24 hours; everything else waits for your **Merge fix**. More in [Usage](docs/usage.md#the-machine-fixes-itself).

### Optional extras

<a id="related-signals-optional-local-embeddings"></a><a id="organization-data-optional-enrichment"></a>
[Related signals with local embeddings](docs/intelligence.md#related-signals-optional-local-embeddings), [organization data from an enrichment service](docs/intelligence.md#organization-data-optional-enrichment) and [work contact details](docs/intelligence.md#people-data).

## Security model

In plain words: [themachine.computer/security](https://themachine.computer/security). The details are in [SECURITY.md](SECURITY.md). In short:

- The local API stays on loopback. The dashboard checks the owner's identity: on your own computer that's your Tailscale login, so put a passkey on that account. A hosted Machine signs in with Google or Microsoft plus an authenticator code, or a passkey.
- The CLI and the agent can't make owner decisions. The dashboard and Telegram share one store of them.
- Reviews only read. **Do it** allows broad work on the accepted task; the plugin's guards are not an OS sandbox.
- Credentials never go into the model's context.
- Private evidence goes to the model provider you chose. Local embeddings don't make model calls local.
- Message contents are encrypted in the database by default, with a key next to it (`message-content.key`). Back the key up with the database: without it the messages are lost ([configuration](docs/configuration.md#message-protection)).
- A send with an unknown outcome is checked, never blindly repeated. Cancel can't recall a send that already started.

Read [SECURITY.md](SECURITY.md) and [PREPARATION.md](PREPARATION.md) before you turn on accepted work.

## Known limitations

- Sources and model judgment are not complete or infallible.
- Phone notifications can be lost during gaps, Slack can take hours, and browser-read sources (LinkedIn, X) can break when the site changes.
- A successful sync with a limit is not a complete catch-up.
- Newer OpenClaw releases are tested weekly, not guaranteed.

More in [Operations](docs/operations.md#known-limitations).

## Tests and contributing

```bash
python3 scripts/test.py
```

The suites live in `tests/` and use synthetic data, a throwaway HOME and disposable databases and browsers. They don't prove real delivery, billing or reboot recovery. See [CONTRIBUTING.md](CONTRIBUTING.md).

Report bugs through a [GitHub issue](https://github.com/Salesflare/TheMachine/issues/new), without personal data. Report security issues privately: [SECURITY.md](SECURITY.md). Never publish real accounts, messages, customer records, credentials, raw logs or backups.

## License

Copyright (C) 2026 Salesflare. Open source under the GNU Affero General Public License v3.0 only (`AGPL-3.0-only`): [LICENSE](LICENSE).

OpenClaw and other components: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Names, branding and the hosted service have separate terms: [TRADEMARKS.md](TRADEMARKS.md).
