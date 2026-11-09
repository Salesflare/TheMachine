---
title: Slack
area: connections
summary: The channels and direct messages you're in. Sends a direct message only after you approve it.
covers: connector:slack
code: assistant.py, next_actions.py, onboarding.py, slack_api.py
site: Connect, Remove
---
## What it reads

The conversations you're a member of: channels, private channels, direct messages and group messages, the last 7 days when you connect, then everything new. It never joins a channel or opens a conversation by itself. A quiet channel is read about once a day; when a to-do needs its newest messages, The Machine reads it right away.

About a year of older messages comes in later as [history](history.md), a little at a time.

People show by their name and apps by theirs, never by a Slack ID. Someone whose Slack account is gone shows as a former Slack user.

## What it can send

A direct message to one person, as you, and only after you approve it on the to-do. A reply to the Slack message a to-do came from goes in that message's thread, in its direct message or channel; the draft says **In thread**. It never starts a new post in a channel.

## Connect it

1. **Connections**, **+ Add**, **Slack**, then **Sign in with Slack**, and allow it in Slack. On your own computer, pair it with your account on themachine.computer first.
2. New messages and direct messages come in first. Slack lets apps read about one conversation a minute, so older messages fill in over a few hours.

Or use a Maton API key: sign in at maton.ai, connect Slack there and copy your Maton API key from Home. Then open **Or use a Maton API key** under Slack and paste it, or run `assistant connect slack` on your own computer. A Slack connected through Maton keeps working as it is.

## Remove it

- In the dashboard: **Connections**, open Slack, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on Slack

Signed in with Slack: open your workspace's Manage apps page in Slack and remove The Machine. Through Maton: remove the Slack connection in Maton and delete the Maton API key you gave. A Slack admin can also remove either app from the workspace, under Manage apps.
