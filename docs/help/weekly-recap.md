---
title: Weekly recap
area: weekly
summary: Once a week, how your Machine did: to-dos, promises, people and projects, and what it noticed. Off by default.
covers: weekly-recap
code: assistant.py, config.example.json
order: 1
---
## What's in it

- Your week with The Machine, and how many to-dos were worth it, compared with the week before.
- To-dos: new, done, dismissed and snoozed, and how quickly you answered.
- Promises: yours kept and open, others' that came through or are still waiting.
- Learnings to share with The Machine team, if any wait for you. See [Share learnings with the team](share-learnings.md).
- People and projects, like who has gone quiet.
- What I noticed: drafts sent as written or edited, to-dos dismissed within minutes, to-dos snoozed more than once.
- Behind the scenes: how many signals it reviewed this week, and how many still wait.
- Choices, each in its own message after the recap: a busy source without results (**Stop reviewing** or **Keep reviewing**) and a to-do snoozed more than once (**Drop**, **Do it now** or **Keep**). Nothing changes until you tap.

## When and where

Once a week, on Friday after 16:00 in your time zone by default. It comes on [Telegram](telegram.md), or as a notification titled "Your week" from the [phone app](phone-app.md).

## Turn it on

It's off by default, and the dashboard has no switch for it yet, so a hosted Machine can't turn it on today. On your own computer, set `weekly_recap` in your Machine's config.json: `enabled` true, and optionally `weekday` (1 to 7, Friday is 5) and `at` ("16:00"). See the [configuration guide](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
