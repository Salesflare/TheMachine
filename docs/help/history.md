---
title: History
area: connections
summary: About a year of older mail, meetings and WhatsApp chats, to search, read and know your people. Never a to-do.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## What it keeps

Your Machine brings in about a year of older email, meetings and WhatsApp chats. Search finds them, also by meaning, threads show them, and the [Calendar](calendar.md) shows past meetings.

Each connection in **Connections** says how far back it reaches, like **History: back to** November 2025.

## What it adds to your Graph

Your [Graph](graph.md) counts it: how close you are to people, when you last talked, who knows whom, and the people and organizations themselves. Your Fleet's "who knows someone" answers use it from work accounts, with the same [sharing rules](sharing-rules.md) as new mail.

## What it never does

It never makes a to-do or a promise, never counts as new, never starts a check and never adds to a project. Personal history stays personal, like personal mail. Apart from Search by meaning, no AI model reads it.

## When it runs

It starts after the first look at your messages, and for each connection only once its first week is in, also for one you add later. It runs slowly in the background and pauses while a check or a sync runs, when a service asks it to slow down, or when your Machine is short on space. New messages always come first.

It uses the access each connection already has. Nothing new to approve.

## How far back

About a year. On your own computer, `history_days` in the settings file changes it (0 turns it off, up to 730). Telegram, Slack and other sources don't bring in older history.
