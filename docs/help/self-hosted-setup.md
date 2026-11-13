---
title: Run it on your own computer
area: getting-started
summary: Install the open-source app on Linux, macOS or Windows. Free, with your own model and your own data.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
Run The Machine on your own computer for free. It's open source (AGPL), and your data stays with you. Installing it takes a terminal. Connecting your accounts doesn't.

## What it needs

- OpenClaw 2026.11.2 or newer, the open-source agent The Machine runs on. The installer offers to install it.
- Python 3.12 or newer, and Node.js 24 (24.22.1 or newer) or 26.12.1 or newer, not 25.
- Tailscale, to reach your dashboard from your phone.
- A normal user account, not root.

## Install it

On Linux or macOS (macOS is in beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

On Windows (beta), it runs inside WSL2. In PowerShell, run `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. It sets up WSL2 with Ubuntu and everything the app needs, then runs `./install.sh`.

The installer finds your accounts, connects them one by one, and shows a preview of last week before anything turns on.

## After installing

- Connect your mail: at the top of **To-dos**, press **Gmail** (or **Outlook**), then **Pair this Machine** to pair it with your account. Without an account, **Use your own app** is right below it.
- Then press **Sign in with Google** (or **Sign in with Microsoft** for Outlook). Mail and calendar connect together.
- Other sources: **Connections**, then the source's kind. Your own Google client or Entra app: `assistant connect` in a terminal.
- Check everything with `assistant doctor`. It prints a fix for each problem.
- It installs the newest signed release, and updates come as signed releases too.
- Pair it with your account, and the phone app opens it after you sign in. Unpairing removes that link.

The full guide is in the repository: [Getting started](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
