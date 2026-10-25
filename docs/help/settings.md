---
title: Settings
area: settings
summary: Where to find each setting, from light mode to security and your account.
covers: settings:general
code: dashboard.html
order: 1
---
Open **Settings** with the gear at the top. Its tabs:

- **Account**: **Your addresses**, the ones that count as you, with where each came from. Your plan in short, buttons to your account pages, and **Sign out**. See [Plans and billing](plans-and-billing.md).
- **General**: language and region, this device, coding agents, your Machine's browser, your Fleet and your account.
- **Security**: Standard or Careful, and the settings they set. See [Security levels](security-levels.md).
- **Work hours**: when your Machine may message you. See [Work hours](work-hours.md).
- **Writing**: signatures and how you write. See [Writing](writing.md).
- **Skills**: how-tos your Machine follows. See [Skills](skills.md).
- **Model**: what answers for you, and its limits. See [Model](model.md).

A tab with nothing to show is hidden.

## General

- **Language and region**: your **Region** sets how dates read (Oct 24 or 24 Oct) and the usual clock. **Time format** picks 12-hour (2:05 PM) or 24-hour (14:05) instead. Cards, Telegram, the digest and Fleet messages follow it. A hosted Machine starts from the country of the time zone you picked at signup. English is the only language for now.
- **This device**: the app (**Install app**), **Notifications** with **Send a test**, and **Light mode**, only for this browser or phone. See [Install the app and turn on notifications](phone-app.md).
- **Coding agents**: see [Hand to Claude Code or Codex](hand-to-agent.md).
- **Open the Machine’s browser ↗**: the browser your Machine uses for sites like LinkedIn.
- **Fleet rules**: see [Sharing rules](sharing-rules.md).
- **Account**: **Open account** and **Sign out**, on a hosted Machine.

## On this Machine

A few settings live on the computer your Machine runs on, not in the app:

- `config.json`: every setting, in one file. Restart the Machine after a change.
- `assistant connect`: add a source, like `assistant connect gmail` or `assistant connect outlook`.
- `assistant telegram on` or `off`: messages on Telegram. See [Telegram](telegram.md).
- `assistant doctor`: checks everything and prints a fix for each problem.

## Your addresses

Every address of yours the Machine found: your accounts, Gmail or Outlook aliases, your calendar, your Slack and Intercom profile. Mail and meetings from any of them show as you. **Remove** one that isn't yours.

A shared address, like info@ or a Google Group, never counts by itself. One the Machine isn't sure about is under **Maybe yours**: tap **Confirm** if only you use it, or **Not mine**.
