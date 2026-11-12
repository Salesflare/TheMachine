---
title: Work hours
area: settings
summary: When your Machine may message you, when snoozes land and when the morning and evening digests come.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
---
Choose when your Machine may reach you. In **Settings**, **Notifications**, under **Work hours**:

- **Work days**: work to-dos and snoozed work wait for a work day.
- **Messages from** and **Until**: nothing reaches you outside these hours: no notification, Telegram or email.
- **Snoozes land at**: when a snooze of a day or more comes back. The morning digest comes at least 5 minutes later, so they are in it.
- **Morning digest**: when the morning summary comes. Move the snooze time later and it moves along.
- **Evening digest**: when the evening summary comes. It starts at 15 minutes before **Until** and follows it until you pick a time of your own.
- **Time zone**: yours, for all of the above.

Press **Save**. The default is Monday to Friday, 08:00 to 23:00, snoozes at 08:00, the morning digest at 08:30 and the evening digest at 22:45.

What goes out within these hours, and how, is in [Notifications](notifications.md).

On your own computer, `assistant hours` shows and changes them in a terminal.
