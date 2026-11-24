---
title: Send later
area: cards
summary: Approve a message now and pick when it goes. If they write first, it waits for you again.
covers: send-later
code: machine/store/send_later.py, machine/app/send_later.py, dashboard/todos-send-later.js
order: 13
keywords: schedule, scheduled, send at a time, delay, tomorrow morning, unsend, take back
---
## Schedule a message

In the window where you check a message, press **Send later** next to **Send now**. Pick **In 2 hours**, **Tomorrow**, **Monday**, or **Choose date** and **Save time**. It goes out exactly as you saw it, at that time in your own time zone.

It works for email, Slack, WhatsApp, Telegram, Signal, Teams and Intercom. Not for LinkedIn and X, where your Machine can't check for a new message right before it sends, and not for a reply in a doc.

In **New email** it's there too. Several messages you check together all go at the time you pick.

## While it waits

The to-do sits under **Coming back later** and on its day in the [Calendar](calendar.md), with the message and when it goes: "Sends Thu, Nov 26, 09:30". **Send now** sends it right away, **Change time** picks another time, **Cancel** makes it a draft again. Its chat shows the same.

Edit the draft, finish the to-do, dismiss it or bring it back, and it doesn't go: it needs your yes again.

## If they write first

When the person writes before it goes, your Machine doesn't send it. The to-do comes back with their message, like "Not sent: Sam Lee wrote first.", and you get the notice a snoozed to-do gives. For an email that counts from any address your Machine knows for them, in any mailbox you connected. Someone else who answers in the conversation counts too.

An automatic reply, like an out of office, doesn't stop it. Neither does a message of your own.

Right before it sends, your Machine reads the conversation again. If it can't, the to-do says "Couldn’t check for a new message yet." and it tries again for an hour. Then it asks you instead of sending.

On WhatsApp it checks the messages your own linked WhatsApp has received so far.

## If The Machine is off

If your Machine is off, asleep or signed out at that time, the message goes when it's back, up to an hour late. After that the to-do comes back with "Not sent: it was more than an hour late." and you decide.

When you move to another computer, scheduled messages ask again there. See [Moving](moving.md).

## Who can schedule

Only you, in the dashboard or the app. Your Machine, its chat, an AI you connected and other Machines can't schedule a message. [Activity](activity.md) shows when one was scheduled, changed, canceled, sent or not sent.
