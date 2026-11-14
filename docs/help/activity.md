---
title: Activity
area: settings
summary: One list of everything The Machine did for you, newest first: messages, docs, Fleet answers, learnings, connections and more.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## What it shows

Open **Settings**, **Activity**. Each line is one thing The Machine did, newest first, by day:

- what it did, and how it ended: sent, refused, failed or undone
- when, the account or app it used, and [what allowed it](activity.md#what-allowed-it)
- a link to its to-do, when there is one
- for an AI you connected, like ChatGPT or Claude: its name with **(connected AI)**, so you can tell it from The Machine itself

It lists messages and replies, doc and calendar changes, steps on the web, fixes it merged, coding agents, Fleet questions and answers, learnings sent to The Machine team, skills, Graph imports, facts you asked your chat to forget (with **Undo**), connections added or removed, and each look by our team under [Support access](get-support.md#support-access), refused ones included.

## What allowed it

Every message, doc or calendar change, step on the web and merged fix says what let it go, as it happened:

- **Approved in the to-do** or **Approved in Telegram**: your tap on its Send, Confirm or Merge
- **Approved by voice**: your yes in Talk
- **Do it tapped**: your Do it on the to-do
- **Asked in chat**: you asked for it in words, with the start of your message in quotes. A quote only shows while those words are still in your own message.
- **Follow-up, sent by itself**, **Small fix, merged by itself**, **New private doc, made by itself** or **Prepared ahead, by itself**: a setting of yours or one of The Machine's own rules
- **No approval recorded**: nothing was recorded for it. It also goes to our [error reports](error-reports.md), so we can find the path that missed it.

Steps on the web also lists a to-do's run that clicked or typed on a page, with what allowed that run.

Older lines, from before this was recorded, keep their old words, like **After your OK**.

## Filter it

Pick a kind in the list at the top, like **Messages** or **Fleet**. **Refused or blocked** shows only what didn't go, and why. **Show more** loads older lines.

## Other places

A to-do's chat still tells its own story; Activity links to it. Fleet, **Activity** shows the same lines for your Fleets and learnings, with **Withdraw** for a learning. In Settings, **Security**, **See each look in Activity** opens the looks by our team.

Activity only shows what happened. It never changes what The Machine may do.
