---
title: Notifications
area: settings
summary: What reaches you, where and when: only what can't wait buzzes, the rest is in one morning summary.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Fewer notifications, or other ones? In **Settings**, **Notifications**, pick where each kind reaches you:

- **New to-dos**: only what can't wait, like something due today or urgent.
- **Results and questions**: a reply ready to send, a sign-in a task needs, a Fleet question.
- **Reminders**: snoozed to-dos, and replies you wait for, coming back.
- **Morning digest**: one short summary of your day. See below.

Each kind has a switch for **Push** (the app on your phone or computer), **Telegram** once it's set up, and **Email** on a hosted Machine or one on The Machine Network. All are on, except the digest on Telegram.

Your **Work hours** are in the same tab: work days, when notifications may go out, when snoozes land, the digest time and your time zone. See [Work hours](work-hours.md).

## Only what can't wait

A push, a Telegram buzz or an email goes only for:

- a to-do due today, or marked urgent;
- a reply someone waits for, drafted and ready to send;
- a task that needs you to sign in;
- a snooze coming back at the time you picked.

Everything else lands quietly on the dashboard (and silently in Telegram) and waits for the morning summary. On a day off only what's urgent or due today buzzes. At most 8 pushes a day. After 3 days without opening the dashboard, only the morning summary comes, until you're back.

## When it notifies

It checks whether you're actually using the dashboard, not just whether it's open:

- Using it (in front, and you clicked, typed or scrolled in the last 10 minutes): nothing buzzes. Telegram arrives silently.
- Away (in the background, closed, or idle for 10 minutes): a push goes a minute after you left, unless you came back and saw it.
- Still unseen 15 minutes later, and it can't wait: one email for it, at most one an hour. What you already handled is left out. Most days the morning summary is the only email.
- A teammate hands you a to-do and your Machine has no phone or Telegram to reach you: one email with its title and a link, 15 minutes later if still unseen. **Email** for **Results and questions** turns it off.
- Outside your work hours: nothing. The morning digest has it.
- A new work to-do on a day off waits for your next work day's digest time. The to-do shows when it will reach you, like Notification Mon 2 Nov · 08:30.

Progress and edits never notify. A newer result on a to-do you haven't seen yet updates it without a new notification. A burst buzzes once. The app's icon shows how many to-dos need you.

## Buttons on notifications

Each notification has buttons for the next step. On the phone app:

- New to-do: Do it, Snooze, Mark done.
- Draft ready: Open draft, Snooze, Mark done.
- Result ready: Open, Mark done, Snooze.
- Question, stuck or a sign-in: Answer, Open or Sign in, then Snooze and Mark done.
- Reminder: Mark done, Snooze, Open.
- Morning digest: tap it to open.

A browser and Telegram show two of them. Fleet questions keep Answer once and Decline.

Nothing is sent, paid or submitted from a notification. A draft always opens first, so you see it before it goes. Open draft shows the to-do in your list with its draft in full. Do it only starts the work on a new to-do.

On the phone app, Snooze and Mark done ask you to unlock first. In a browser they open the dashboard, which does it and shows Undo. Snooze brings the to-do back in two hours, or tomorrow morning on a reminder.

Emails have Open links (and Snooze for what waits). They only open the dashboard.

## The morning digest

It comes on work days at your **Morning digest** time, unless there's nothing to say. **Preview** shows it without sending it. By default it's a push and an email, short enough to read at a glance:

- a greeting with what matters today, like "Morning Sam, 2 replies are ready to send";
- your meetings in one line;
- at most three things to do, each with an Open link: drafts ready for you and promises due today first;
- how many more can wait, and how long they take at your pace, like "12 more can wait, about 5 min to clear." To-dos that wait on your answer aren't in that time.

The push says the same without links. Tap it to open today in the **Calendar**.

## Privacy

Push goes from your Machine straight to your device, encrypted for it. Email passes through The Machine's mail server and your mail provider. When [Careful](security-levels.md) hides to-do text in notifications, emails only have counts. Turn off **Email** for a kind to keep it off email.

Turn on push for a device in **This device**, or see [Install the app](phone-app.md). The [mobile app](mobile-app.md) gets a plain line through Apple or Google, then asks your Machine for the title and next step.
