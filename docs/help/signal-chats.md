---
title: Signal chats
area: connections
summary: Your Signal chats and groups, read as a linked device of your phone. Replies only after you approve.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
---
## What it reads

Your chats and groups, as a linked device of your phone, like Signal Desktop. Signal gives a new linked device no older messages, so it reads from the moment you link it.

Photos, voice messages and files show as what they are ("Sent a photo"), never their content. View-once media keeps no content at all. Edits and deletes follow what happened on your phone, and disappearing messages go from your Machine when their timer is up.

Stories, reactions, calls and Note to Self are skipped. Nothing is marked read.

## What it can send

A text into a chat that already exists, only after you approve it on the to-do. A reply quotes the message it answers when that helps. Sends go out one at a time, with a pause in between.

If a to-do came in by email but you talk to that person on Signal, say so in the to-do's chat. The Machine finds your existing chat with them and switches the draft to Signal, for you to review and send. It never starts a new chat.

## Connect it

1. In the dashboard, open **Connections**, then **+ Add**, and pick Signal chats.
2. On your phone, in Signal, open Settings, **Linked devices**, **Link new device**, and scan the code.

Scanning needs a second screen: Signal links a device only by QR code. Or run `assistant connect signal` in a terminal and scan the code it shows there.

Your Machine keeps the linked device's keys on itself. They never leave it.

## When it stops

It uses signal-cli, an unofficial Signal client. Your Machine downloads a pinned release and checks its checksum before it runs. Signal can stop accepting it at any time.

- **Signal unlinked this Machine**: you removed it on your phone, or Signal ended the link. Press **Reconnect** in **Connections** and scan a new code.
- **Update The Machine for Signal**: Signal no longer accepts this Machine's Signal client. Update The Machine.

## Remove it

**Connections**, open Signal chats, **Details**, then **Disconnect**. Your Machine deletes the keys and what it kept for Signal. Then remove it on your phone too: Signal, Settings, **Linked devices**, tap The Machine and unlink it.
