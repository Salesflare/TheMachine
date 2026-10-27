---
title: Error reports
area: security
summary: When something breaks, your Machine tells The Machine team what failed and where in the code. Never your messages, names or addresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html
order: 4
---
## What it is

When something in The Machine breaks, your Machine sends the team a short signature of the error, so we can fix it before anyone has to report it. It's on by default and needs [The Machine Network](/network).

## What goes

Only this, for each kind of error:

- the type of error, like `KeyError` or `TypeError`;
- its message with everything specific taken out: numbers, ids, quoted text, email addresses, links, file paths and anything that looks like a key. Any other word that could be a name is taken out too;
- where it happened in The Machine's own code: file, function and line, never a folder on your computer;
- the app version, how often it happened, and when first and last.

A real one: `IndexError`, `list index out of range`, at `assistant.py:fault_event:7899`, version `05b17ee6ac79`, 1 time.

## What never goes

What your messages, to-dos, drafts or chats say. Names, email addresses, phone numbers, links, tokens or passwords. Which account or person it was about.

## Where errors come from

- the service and its jobs: reviews, preparing to-dos, chat, connections and syncs;
- the dashboard in your browser;
- Claude Code and Codex jobs that fail: the tool and the kind of failure only.

The same error counts once, with a count. At most a batch every 10 minutes. The team keeps them 30 days.

## Pacing

Background work waits when your AI plan's limits run low, to keep room for your own chats (see [Your AI model](model.md)). With error reports on, your Machine also tells the team, once a day, how often that happened: for each time, the hour it started, which limit, how many minutes it lasted and how many jobs waited. Only counts and minutes, nothing about what the jobs were.

## Turn it off

In Settings, Security, turn off **Send error reports**. Nothing more is recorded or sent, pacing counts included, and what was waiting is deleted. Errors still show on your own Machine, which can offer a fix.

See [Security and privacy](security-and-privacy.md).
