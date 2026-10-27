---
title: Notifications
area: settings
summary: What reaches you, where and when: push, Telegram or email per kind, your work hours, and the morning digest.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
In **Settings**, **Notifications**, pick per kind where it reaches you:

- **New to-dos**: a reply someone waits for, a request, anything urgent.
- **Results and questions**: a draft ready to approve or send, a task that's stuck or needs a sign-in, a Fleet question.
- **Reminders**: snoozes and waits coming back.
- **Morning digest**: today's meetings, what's due and what came in overnight.

Each has a switch for **Push** (the app on your phone or computer), **Telegram** when it's set up, and **Email** on a hosted Machine or one on The Machine Network. All are on, except the digest on Telegram.

**Work hours** sit in the same tab: your work days, the hours notifications may go out, when snoozes land, the digest time and your time zone. See [Work hours](work-hours.md).

## When it notifies

Like Slack, it looks at whether you're using the dashboard, not just whether it's open:

- In use: the dashboard is in front of you, in focus, and you clicked, typed, scrolled or touched it in the last 10 minutes. Nothing buzzes. Telegram arrives without a sound.
- Away: the dashboard is in the background, minimized, closed, or idle for 10 minutes. A push goes a minute after you left, unless you came back and saw it first.
- Still unseen 15 minutes later: one email with everything that still waits for you. At most one an hour. Anything you handled in the meantime, on Telegram or elsewhere, is left out.
- A teammate hands you a to-do and your Machine has no phone or Telegram to ping you on: one email for it, 15 minutes later if you still haven't seen it. Just its title and a link. **Email** for **Results and questions** turns it off.
- Outside your work hours: nothing. The morning digest has what came in.

Only what needs you notifies. Progress and edits don't. A burst buzzes once. The app's icon shows how many to-dos need you.

## The morning digest

It comes on work days at your **Morning digest** time, and is skipped when there's nothing to say. **Preview**, in its row, shows it on the page without sending it. By default it's a push and an email.

## Privacy

Push goes from your Machine straight to your device, encrypted for that device. The control plane never sees it. Email is sent by The Machine's mail server to your account's address, so the text passes through it and the mail provider. When [Careful](security-levels.md) hides to-do text in notifications, emails only have counts. Turn off **Email** for a kind to keep it off email entirely.

Turn on push for a device in **This device**, or see [Install the app](phone-app.md).
