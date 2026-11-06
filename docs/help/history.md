---
title: History
area: connections
summary: About a year of older mail, meetings and WhatsApp chats, to search and read. Never a to-do.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## What it keeps

Your Machine brings in about a year of older email, meetings and WhatsApp chats. Search finds them, threads show them, and the [Calendar](calendar.md) shows past meetings.

Each connection in **Connections** says how far back it reaches, like **History: back to** November 2025.

## What it never does

History is only there to look things up. It never makes a to-do or a promise, and never goes to your Graph or your team. No AI model reads it.

To-dos and promises come only from new messages.

## When it runs

It starts after the first look at your messages and runs slowly in the background. It pauses while your Machine is busy or short on space, and picks up where it left off.

It uses the access each connection already has. Nothing new to approve.

## How far back

About a year. On your own computer, `history_days` in the settings file changes it (0 turns it off, up to 730). Telegram, Slack and other sources don't bring in older history.
