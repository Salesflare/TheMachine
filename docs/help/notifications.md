---
title: Notifications
area: settings
summary: What reaches you, where: push, Telegram or email, per kind. Plus the morning digest.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 3
---
In **Settings**, **Notifications**, pick per kind where it reaches you:

- **New to-dos**: a reply someone waits for, a request, anything urgent.
- **Results and questions**: a draft ready to approve or send, a task that's stuck or needs a sign-in, a Fleet question.
- **Reminders**: snoozes and waits coming back.
- **Morning digest**: today's meetings, what's due and what came in overnight.

Each has a switch for **Push** (the app on your phone or computer), **Telegram** when it's set up, and for the digest **Email**.

## Smart by default

- Only what needs you notifies. Progress and edits don't.
- A burst buzzes once. The rest arrive silently.
- Nothing goes out outside your [work hours](work-hours.md).
- While the dashboard is open in front of you, no push goes to any device and Telegram arrives without a sound.
- The app's icon shows how many to-dos need you.

## The morning digest

It comes on work days at your **Morning digest** time in [Work hours](work-hours.md), and is skipped when there's nothing to say. **Preview** shows it on the page without sending it. By default it's a push only.

## Privacy

Push goes from your Machine straight to your device, encrypted for that device. The control plane never sees it. Email is sent by The Machine's mail server to your account's address, so the text passes through it and the mail provider. That's why email is off until you turn it on, and why it only has counts when [Careful](security-levels.md) hides to-do text in notifications.

Turn on push for a device in **This device**, or see [Install the app](phone-app.md).
