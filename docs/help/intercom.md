---
title: Intercom
area: connections
summary: Customer conversations in your Intercom workspace. It replies only after you send, as you.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
---
## What it reads

Customer conversations in your Intercom workspace: the last 7 days when you connect, then new ones as they come in. It also reads which workspace and teammate the sign-in belongs to.

## What it can do

With your own **Sign in with Intercom**, it can reply in a conversation as you, only after you press **Send** on that exact text. It never assigns, closes, tags or writes notes. An Intercom shared with you through your Fleet only reads.

## To-dos from Intercom

A to-do from Intercom shows the customer, and **Read message** opens the conversation, with a link to it in Intercom. Its reply goes out in that conversation, unless you ask for an email.

Only conversations assigned to you, or to no one yet, become to-dos. When a teammate takes one in Intercom, its to-do closes by itself, with **Undo**. On an Intercom shared with you, your conversations are the ones assigned to the teammate you write as.

An Intercom to-do also closes by itself once someone on the team closes the conversation in Intercom, or answers it and the customer hasn't written since, when a reply was all the to-do asked. A note, a snooze or a bot's answer never counts.

When your Machine can't reply in Intercom (shared with you to read only, replies not turned on, or not connected), the draft goes by email instead. The to-do says why and asks **Send by email instead?** To reply in Intercom, tap **Connect your own Intercom** on the to-do and sign in. The to-do is then written again as a reply in Intercom. Nothing goes out before you send it.

Your own Intercom and one shared with you for the same workspace don't both read: the shared one rests, and its conversations move to yours, each once.

## Connect it

1. In the dashboard: **Connections**, **+ Add**, Intercom. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Intercom. On your own computer, pair it with your account first.
2. Press **Sign in with Intercom**.
3. Approve The Machine (made by Salesflare) in Intercom. You come back where you started.

Signing in to another workspace adds a second Intercom account.

Intercom always counts as work, for the company its workspace names.

## Remove it

- In the dashboard: **Connections**, open Intercom, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on Intercom

In Intercom, open Settings, Apps, Installed apps, and remove The Machine.
