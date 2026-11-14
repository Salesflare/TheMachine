---
title: Weekly recap
area: weekly
summary: Once a week, how your Machine did: to-dos, promises, people and projects, and what it noticed. On by default.
covers: weekly-recap
code: assistant.py, machine/app/recap_settings.py, config.example.json
order: 1
---
## What's in it

- Needs you: late promises made to you, and your own promises that are late or due in the next two weeks.
- Next week: your meetings (with a link when the prep is ready), to-dos that are due and promises others made for then.
- What changed: how many to-dos were worth it, compared with the week before, how often **Do it** was right the first time, what it adjusted in how you write and in its filters, and how many drafts went out as written.
- For The Machine team: learnings to share, if any wait for you. See [Share learnings with the team](share-learnings.md).
- People and projects: projects heating up or cooling down, who is new and who has gone quiet.
- Behind the scenes: how many signals it checked this week, and how many still wait.
- On [Telegram](telegram.md), choices follow, each in its own message: a busy source without results (**Stop checking** or **Keep checking**) and a to-do snoozed more than once (**Not needed**, **Do it** or **Keep**). Nothing changes until you tap.

## When and where

Once a week, on Friday after 16:00 in your time zone by default. It comes on [Telegram](telegram.md), or as a notification titled "Your week" from the [phone app](phone-app.md) and the dashboard app. It also comes by email when email is on for **Morning digest** in Settings › Notifications. With [Careful](security-levels.md), or with **Text in notifications** off, it doesn't come by email.

## Turn it off

It's on by default. Turn it off in Settings › Notifications with the **Weekly recap** switch. If you turned it off, it stays off. On your own computer you can also set `weekly_recap` in config.json: `enabled` false with `chosen` true, and optionally `weekday` (1 to 7, Friday is 5) and `at` ("16:00"). See the [configuration guide](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).
