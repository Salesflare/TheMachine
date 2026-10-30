---
title: Gmail
area: connections
summary: Reads your mail and drafts replies in your voice. Sends an email only after you approve it.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## What it reads

All your mail: the last 7 days when you connect, then everything new, in and out. Mail you send counts too, so it learns how you write and what you promised.

Promotions, newsletters, Updates and Forums mail get a quick look first: sender, subject and a few words, many at once. When one matters, it is read in full and can become a to-do. Nothing is skipped unseen.

## What it can send

An email from a to-do, and only after you approve it. **Do it** prepares a draft; **Review and send** opens it ready to edit, and nothing goes out until you press **Send now**. **Sign in with Google** asks Google for sending too. With your own app on your own computer, the sign-in is read-only until you add sending yourself.

**From** in the review is a small picker when Gmail lets this mailbox send as an alias of yours (one marked **Mine** in Settings, [Your addresses](settings.md#your-addresses)). A reply to mail that came to that alias starts from it; new mail starts from your mailbox address. Right before sending, Gmail is asked again: if it doesn't confirm the address, nothing is sent.

A reply goes into the thread of the email it answers. When it goes from another of your mailboxes than the one that email came in on, the to-do says so before you send. It still lands in their thread.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup.
2. Under **Mail and Calendar**, press **Connect Google** and sign in. Google's screen names Salesflare, who makes The Machine.
3. Gmail and Google Calendar connect together.

Or in the dashboard: **Connections**, **+ Add**, pick Gmail and press **Sign in with Google**. When you're done, you're back in the dashboard.

On your own computer, once it's [paired with your account](fleet.md):

1. In the dashboard, open **Connections**, then **+ Add**, and pick Gmail.
2. Press **Sign in with Google** and sign in in the tab that opens. Gmail and Google Calendar connect together.

Not paired, or with your own Google OAuth client: open **Use your own app** there, or run `assistant connect gmail`. It uses gog. Open the address it shows and sign in.

A Google Workspace admin may have to allow the app first, in the Admin console.

## Remove it

- On a hosted Machine: press **Disconnect** next to the address on your setup page. That removes Gmail and Calendar for that address and revokes the sign-in at Google. In the dashboard, **Disconnect ↗** on Connections takes you there. **Reconnect** there signs in again without leaving the dashboard.
- On your own computer: **Connections**, open Gmail, **Details**, then **Disconnect**. It stops reading. What it already brought in stays. When nothing else uses that Google sign-in, it is revoked at Google.

## Uninstall it on Google

In your Google Account, open Security, then Your connections to third-party apps and services, and remove Salesflare (Sign in with Google, or hosted) or your own app.
