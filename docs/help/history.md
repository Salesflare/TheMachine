---
title: History
area: connections
summary: About a year of older mail, meetings and WhatsApp chats, to search and read. Never a to-do.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## What it keeps

Each email account, calendar and WhatsApp keeps about a year of older messages and meetings. Search finds them, a thread shows them, and the [Calendar](calendar.md) shows past meetings.

Its card says how far back it reaches: **History: back to** a month, once it's in.

## What it never does

History is only there to look things up. It never makes a to-do or a promise, never goes into a check, never counts as new, and never goes to your Graph or your team. No AI model reads it.

To-dos and promises still come only from new messages, as before.

## When it runs

It starts once the first look at your messages is done, and runs slowly in the background. It waits while a check or a sync runs, and when your Machine is short on disk space or memory. After a restart it goes on where it was.

It uses the access each connection already has. Nothing new is asked.

## How far back

About a year by default. Self-hosted Machines can set `history_days` in the config (0 turns it off, up to 730). Telegram, Slack and other sources keep what they read today.
