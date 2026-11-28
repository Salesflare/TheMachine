---
title: History
area: connections
summary: About a year of older mail, meetings and WhatsApp, Slack and Teams messages, to search, read and know your people. Never a to-do.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## What it keeps

Your Machine brings in about a year of older email, meetings and WhatsApp, Slack and Teams messages. Search finds them, also by meaning, threads show them, and the [Calendar](calendar.md) shows past meetings.

Each connection in **Connections** says how far back it reaches, like **History: back to** November 2025.

## What it adds to your Graph

Your [Graph](graph.md) counts it: how close you are to people, when you last talked, who knows whom, and the people and organizations themselves. A person's or organization's Timeline shows it too, so its last contact is always there. Your Fleet's "who knows someone" answers use it from work accounts, with the same [sharing rules](sharing-rules.md) as new mail.

## What it never does

It never makes a to-do or a promise, never counts as new, never starts a check and never adds to a project. Personal history stays personal, like personal mail.

Apart from Search by meaning, your AI model reads it in four places only:

- what a search finds, like for a question you ask or a to-do being worked on
- mail with booking details, for [trips and events](calendar.md#trips-and-events)
- a [meeting briefing](calendar.md#ready-for-your-meetings): notes of earlier meetings and a few older messages with the people you meet
- once per mailbox, the email you wrote yourself, to learn how you work (see Notes from your older email, below)

## When it runs

It starts after the first look at your messages, and for each connection only once its first week is in, also for one you add later. It runs slowly in the background and pauses while a check or a sync runs, when a service asks it to slow down, or when your Machine is short on space. New messages always come first.

Once a mailbox's history is in, your Machine reads the mail it keeps once more for booking and ticket details, so older bookings show under [trips and events](calendar.md#trips-and-events) too. It goes just as slowly and pauses for the same reasons.

It uses the access each connection already has. Nothing new to approve.

## Notes from your older email

Once a mailbox's history and its new mail are in, your Machine reads the email you wrote yourself in it, once, and keeps how you work: your rates and terms, how you like things done, what you handle. They show under **Learning**, **What I've learned**, each with the day you wrote it and your own words. **Edit** or **Remove** any of them; a removed one never comes back.

- Only your own words count. What someone else asked is not how you work.
- Something you told one client stays theirs, on their Graph page, unless what you wrote or who you told shows it is how you work for everyone. A deal for one client stays theirs also when you told a colleague.
- When a newer email of yours changes something, or what your Machine knows now says otherwise, the newer one wins.
- One rule you wrote twice, in other words or from two sides, or in parts (a goal and its target), is kept once.
- A note that would only say "him" or "her" names who, from your message, or is left out.
- Work or Personal by why it is so: an evening kept free for your choir is Personal, also when you told a client. A Personal note stays out of work.
- Never a to-do, a promise or a reply. What is over stays over.

It runs in the background after the first look, waits for your plan's limits like other background work, and uses a few small turns. `history_notes: false` in the settings file turns it off.

## How far back

About a year. On your own computer, `history_days` in the settings file changes it (0 turns it off, up to 730). Telegram and other sources don't bring in older history.

LinkedIn and X messages go back 90 days, read very slowly: a few small reads an hour, only in the daytime, and none for a day if the site pushes back, so your account stays safe (`social_history_days`, 0 turns it off).
