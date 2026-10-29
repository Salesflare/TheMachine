---
title: Telegram chats
area: connections
summary: Your Telegram chats and small groups, read as a device of your own account. Replies only after you approve.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## What it reads

Your private chats and groups of up to 50 people, as a logged-in device of your own Telegram account, like Telegram Desktop. When you connect it reads the last 7 days, then what comes in.

It never reads channels, bots, Saved Messages or Telegram's own service messages. Muted and archived chats are skipped too.

It leaves your read and online status alone: nothing is marked read, and your phone still shows new messages as new.

This is separate from [Telegram](telegram.md), where your own bot sends you your to-dos.

## What it can send

A text into a chat that already exists, only after you approve it on the to-do. Sends go out one at a time, with a pause in between.

If a to-do came in by email but you talk to that person on Telegram, say so in the to-do's chat. The Machine finds your existing chat with them and switches the draft to Telegram, for you to review and send. It never starts a new chat.

## Connect it

1. In the dashboard, open **Connections**, then **+ Add**, and pick Telegram chats.
2. Choose **Scan a QR code with Telegram on another device**.
3. On your phone, in Telegram, open Settings, Devices, **Link Desktop Device**, and scan the code.
4. If your account has a cloud password, type it when asked. It goes to Telegram and is never stored.

On a phone, the form leads with **Get a code for your phone number**, since a QR code can't be scanned from the same screen. It says where Telegram sent the code: your Telegram app on another device, an SMS or your login email. No code? Press **Send the code again**.

On your own computer you also need a Telegram app ID of your own. Create one at [my.telegram.org](https://my.telegram.org), under API development tools, and fill in its api_id and api_hash in the form.

Or run `assistant connect telegram` in a terminal and scan the code it shows there.

## When it stops

- **Logged out of Telegram**: Telegram ended this device's login, or you logged it out on your phone. Press **Reconnect** on its card.
- **Telegram stopped accepting the app ID**: Telegram no longer accepts the app ID this Machine uses. Nothing is read or sent until you press **Reconnect** and add an app ID of your own.

The Machine uses Telegram's API for this. Telegram may limit or end logins from apps like it.

## Remove it

**Connections**, open Telegram chats, **Details**, then **Disconnect**. Your Machine logs itself out at Telegram and deletes what it kept for Telegram.

Or end it on your phone: in Telegram, open Settings, Devices, tap The Machine and end the session.
