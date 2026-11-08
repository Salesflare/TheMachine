---
title: Routines
area: cards
summary: Work your Machine does on its own, on a rhythm, like a Monday summary of your open deals. It only reads.
covers: tab:routines
code: routines.py, routines_app.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report
---
## Make one

Open **Routines** in the sidebar and say what it should do and when, in one line: "every Monday at 9, sum up my open deals" or "every weekday morning, list the emails I still owe a reply". Then **Add**.

Without a time it runs at 8:00. The time is on your Machine's clock.

## What a routine does

At its time your Machine reads what it needs, like your messages, meetings and the Graph, and puts the result on the Routines page. Each result says **Ready**, **Nothing new** (with why) or **Didn’t work** (with why). A run that ends without a result counts as one that didn't work, never as done.

A routine only reads. It never sends, replies, posts or changes anything.

Each run knows the last result, so it can say what changed since then.

## Missed days

When your Machine was off or busy, a missed run isn't stacked: only the newest one runs, once. Each date runs once, even after a restart.

Routines run one at a time and wait when your AI plan's usage is low, like all background work. **Run now** runs it right away.

## Change or stop it

**Change when** takes a new rhythm in your own words, like "every weekday at 8". **Pause** stops the runs until **Resume**; nothing missed while paused runs afterwards. **Stop** ends a routine for good.

## Routines and recurring to-dos

A recurring to-do (recurring.md) reminds you to do something. A routine is work your Machine does by itself and shows you. Use a recurring to-do for "pay the rent on the first", and a routine for "every Friday, tell me which deals went quiet".
