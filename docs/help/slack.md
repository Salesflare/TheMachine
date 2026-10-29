---
title: Slack
area: connections
summary: The channels and direct messages you're in. Sends a direct message only after you approve it.
covers: connector:slack
code: assistant.py, slack_api.py, next_actions.py, onboarding.py
site: Sign in with Slack, Connect, More sources, Remove
---
## What it reads

The conversations you're a member of: channels, private channels, direct messages and group messages, the last 7 days when you connect, then everything new. It never joins a channel or opens a conversation by itself.

## What it can send

A direct message to one person, as you, and only after you approve it on the to-do. It never posts in a channel.

## Connect it

Sign in with Slack, the easy way:

1. In the dashboard: **Connections**, **+ Add**, Slack. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Slack. On your own computer, pair it with your account first.
2. Press **Sign in with Slack**. Slack asks which workspace, and shows what The Machine may read and send.
3. Press **Allow**. You're back where you started, and Slack is connected.

Some workspaces let only admins approve new apps. Slack then asks an admin first; once they approve, sign in again.

Or use Maton instead:

1. Sign in at maton.ai, connect Slack there, and copy your Maton API key from Home.
2. Open Slack as above (or run `assistant connect slack`), open **Or use a Maton API key**, paste the key and press **Connect**.

Connected Slack through Maton before? It keeps working. Connections shows **Reconnect Slack**: press it and sign in with Slack to stop using Maton. What Slack already brought in stays.

## Remove it

- In the dashboard: **Connections**, open Slack, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on Slack

- Signed in with Slack: in Slack, open your workspace's Manage apps page (or Settings, Apps), find The Machine and remove it. A Slack admin can also remove it for the whole workspace.
- Through Maton: remove the Slack connection in Maton, and delete the Maton API key you gave.
