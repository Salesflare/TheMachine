---
title: Notifications
area: settings
summary: What reaches you, where and when: push, Telegram or email per kind, your work hours, and the morning digest.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Fewer notifications, or other ones? In **Settings**, **Notifications**, pick where each kind reaches you:

- **New to-dos**: a reply someone waits for, a request, anything urgent.
- **Results and questions**: a draft ready to send, a task that's stuck or needs a sign-in, a Fleet question.
- **Reminders**: snoozed to-dos, and replies you wait for, coming back.
- **Morning digest**: today's meetings, what's due, what came in overnight and the first to-dos waiting.

Each kind has a switch for **Push** (the app on your phone or computer), **Telegram** once it's set up, and **Email** on a hosted Machine or one on The Machine Network. All are on, except the digest on Telegram.

Your **Work hours** are in the same tab: work days, when notifications may go out, when snoozes land, the digest time and your time zone. See [Work hours](work-hours.md).

## When it notifies

It checks whether you're actually using the dashboard, not just whether it's open:

- Using it (in front, and you clicked, typed or scrolled in the last 10 minutes): nothing buzzes. Telegram arrives silently.
- Away (in the background, closed, or idle for 10 minutes): a push goes a minute after you left, unless you came back and saw it.
- Still unseen 15 minutes later: one email with everything that waits for you, at most one an hour. What you already handled is left out. A day spent at the dashboard may bring no email at all.
- A teammate hands you a to-do and your Machine has no phone or Telegram to reach you: one email with its title and a link, 15 minutes later if still unseen. **Email** for **Results and questions** turns it off.
- Outside your work hours: nothing. The morning digest has it.
- A new work to-do on a day off waits for your next work day's digest time. The to-do shows when it will reach you, like Notification Mon 2 Nov · 08:30.

Only what needs you notifies, not progress or edits. A burst buzzes once. The app's icon shows how many to-dos need you.

## The morning digest

It comes on work days at your **Morning digest** time, unless there's nothing to say. **Preview** shows it without sending it. By default it's a push and an email. The push names how many to-dos wait, the first two, and your first meeting's time. Tap it to open today in the **Calendar**.

## Privacy

Push goes from your Machine straight to your device, encrypted for it. Email passes through The Machine's mail server and your mail provider. When [Careful](security-levels.md) hides to-do text in notifications, emails only have counts. Turn off **Email** for a kind to keep it off email.

Turn on push for a device in **This device**, or see [Install the app](phone-app.md). The [mobile app](mobile-app.md) gets a plain line through Apple or Google, then asks your Machine for the title and next step.
