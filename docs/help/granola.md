---
title: Granola
area: connections
summary: Notes and transcripts of the meetings you had in Granola. It only reads.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
---
## What it reads

Granola's notes and transcripts of meetings you were in: the last 7 days when you connect, then new ones as they come in. Notes still being written come in once Granola has finished them.

Each one lands on its meeting in your Calendar, the one Granola names, else the meeting at the same time. Granola's notes go under Notes, the transcript under Transcript, marked **From Granola**. What you added yourself stays.

After the meeting, The Machine reads them for what was promised, decided or still owed, like "I'll send the deck", and makes to-dos only for clear next steps. People in the meeting link to your [Graph](graph.md) by their email address.

## What it can do

Nothing in Granola. It only reads, and never changes, shares or deletes a note.

## What it asks for

A personal API key from Granola. Granola has API keys on its Business and Enterprise plans. The key reads your own notes and the ones shared with you, as you see them in Granola.

## Connect it

1. In Granola's desktop app: **Settings**, **Connectors**, **API keys**. Create a key with **Personal notes** and copy it.
2. In the dashboard: **Connections**, **Meetings**, Granola. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Granola. On your own computer, `assistant connect granola` asks for it too.
3. Paste the key, pick **Work** or **Personal** and press **Connect**.

It checks the key right away. If Granola later refuses it, Granola in **Connections** asks for a new key.

## Remove it

- In the dashboard: **Connections**, open Granola, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Granola

In Granola's desktop app: **Settings**, **Connectors**, **API keys**, then delete the key.
