---
title: Zoom
area: connections
summary: The AI Companion summaries and transcripts of meetings you host. It only reads.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## What it reads

The AI Companion summary of each Zoom meeting you host, and its transcript when Zoom has one: the last 7 days when you connect, then new ones as they come in. It also reads your Zoom name and email, to know whose meetings they are.

Summaries need a paid Zoom plan, AI Companion turned on during the meeting, and no end-to-end encryption.

## What it does with them

Each summary is matched to the meeting in your calendar. It shows in that meeting's **Notes** and the transcript in its **Transcript**, marked **From Zoom**, next to anything you added. Your Machine makes to-dos from the next steps that are yours. Nothing is sent until you send it.

## What it can do

It only reads, and only your own meetings. It never creates, changes or deletes anything in Zoom. Your Zoom sign-in stays on your Machine.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup and go to **More sources**.
2. Open Zoom, pick work or personal, and press **Connect Zoom**.
3. Sign in to Zoom and allow The Machine (made by Salesflare).

Or in the dashboard: **Connections**, **Meetings**, pick Zoom and press **Sign in with Zoom**. When you're done, you're back in the dashboard.

On your own computer, once it's [paired with your account](friends.md#a-machine-on-your-own-computer): open **Connections**, then **Meetings**, pick Zoom and press **Sign in with Zoom**.

## Remove it

- In the dashboard: **Connections**, open Zoom, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on Zoom

Sign in at marketplace.zoom.us, open Manage, then Added Apps, and remove The Machine. It can no longer read anything. What it already brought in stays on your Machine until you delete it: see [Cancel and delete](cancel-and-delete.md).
