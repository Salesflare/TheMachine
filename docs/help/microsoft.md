---
title: Microsoft Outlook and Calendar
area: connections
summary: Outlook mail and meetings, for Microsoft 365 and Outlook.com. Sends an email only after you approve it.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## What it reads

- **Outlook**: all your mail, the last 7 days when you connect, then everything new.
- **Outlook Calendar**: your meetings, read only.

Mail in Other and newsletters get a quick look first: sender, subject and a few words, many at once. When one matters, it is read in full and can become a to-do. Nothing is skipped unseen.

## What it can send and change

- An email from a to-do, only after you approve it in the preview. It always goes out from the mailbox's own address: Microsoft doesn't confirm sending as an alias.
- When you snooze a to-do about an email, the thread's messages move to a Snoozed folder in Outlook and come back when the to-do does.

The calendar is never changed.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup.
2. Press **Connect Microsoft** and sign in.
3. If Microsoft asks for admin approval, send your Microsoft 365 admin this link: themachine.computer/m365-admin-consent. **Copy link** copies it. Once they approve, everyone in your organization can connect. If that's you, press **I'm the admin: approve now**.

Or in the dashboard: **Connections**, **+ Add**, pick Outlook and press **Sign in with Microsoft**. When you're done, you're back in the dashboard. Need your admin's approval? The same link is right under the button, with **Copy link**.

On your own computer, once it's [paired with your account](fleet.md): open **Connections**, then **+ Add**, pick Outlook and press **Sign in with Microsoft**. Mail and calendar connect together.

With your own app: open **Use your own app** there, or run `assistant connect outlook` or `assistant connect outlook_calendar`. It uses your own app registration in Microsoft Entra and a sign-in code. It asks whether to also send what you approve.

## Remove it

- On a hosted Machine: press **Disconnect** next to the account on your setup page. In the dashboard, **Disconnect ↗** on Connections takes you there. **Reconnect** there signs in again without leaving the dashboard.
- On your own computer: **Connections**, open the account, **Details**, then **Disconnect**.

## Uninstall it on Microsoft

Microsoft has no way for us to revoke a sign-in, so remove it there as well:

- Work or school account: myapps.microsoft.com
- Personal account: account.live.com/consent/Manage
