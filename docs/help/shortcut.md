---
title: Shortcut
area: connections
summary: Stories that change state, with their owners and deadlines. It only reads.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
---
## What it reads

Stories in your Shortcut workspace that change state, with their owners and deadlines.

## What it can do

Nothing in Shortcut. It only reads.

## Connect it

1. In the dashboard: **Connections**, **Projects and code**, Shortcut. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Shortcut. On your own computer, pair it with your account first.
2. Press **Sign in with Shortcut** and allow read access. It asks Shortcut for read access only.
3. Back in The Machine, it checks the sign-in right away and shows who it connected as, in which workspace.

In more than one Shortcut workspace? Switch to that one in Shortcut first. For another workspace, add Shortcut again.

## Paste a token instead

Under **Or paste an API token**, press **Get your token**. Shortcut opens its API Tokens page in a new tab: create a token, copy it, paste it and press **Connect**. On your own computer, `assistant connect shortcut` asks for it too. A token has full access to your account, but The Machine only reads with it.

## Remove it

- In the dashboard: **Connections**, open Shortcut, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Shortcut

A pasted token: delete it on the API Tokens page. Signed in: disconnecting it here stops all reading.
