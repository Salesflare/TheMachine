---
title: Error reports
area: security
summary: When something breaks, your Machine tells The Machine team what failed and where in the code. Never your messages, names or addresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
---
## What it is

When something in The Machine breaks, your Machine sends our team a short, anonymous note about the error, so we can fix it before anyone reports it. It's on by default and needs [The Machine Network](/network).

## What goes

Only this, per kind of error:

- the kind of error, like `KeyError`;
- its message with anything specific taken out: numbers, ids, quoted text, email addresses, links, file paths, keys and any word that could be a name;
- where in The Machine's own code it happened, never a folder on your computer;
- the app version, how often it happened, and when first and last.

For example: `IndexError`, `list index out of range`, at `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 time.

## What never goes

What your messages, to-dos, drafts or chats say. Names, email addresses, phone numbers, links or passwords. Which account or person it was about.

## Where errors come from

- background work: checks of new messages, preparing to-dos, chat, connections and syncs;
- the dashboard, in your browser or the app, including errors it showed you;
- requests from the dashboard that fail or time out: which one, never what it sent;
- coding agent jobs that fail: the tool and the kind of failure only.

Repeats of the same error are counted, not sent again. At most one batch goes every 10 minutes. We keep them 30 days.

## Pacing

Background work waits when your AI plan's limits run low, to keep room for your own chats (see [Your AI model](model.md)).

With error reports on, your Machine also tells us once a day how often that happened: per pause, the hour, which limit, how long and how many jobs waited. Nothing about what the jobs were.

## Turn it off

In **Settings**, **Security**, turn off **Send error reports**. Nothing more is recorded or sent, and what was waiting is deleted. Errors still show on your own Machine, which can offer a fix.

See [Security and privacy](security-and-privacy.md).
