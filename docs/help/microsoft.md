---
title: Microsoft Outlook and Calendar
area: connections
summary: Outlook mail and meetings, for Microsoft 365 and Outlook.com. Sends an email only after you approve it.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## What it reads

- **Outlook**: all your mail, the last 7 days when you connect, then everything new.
- **Outlook Calendar**: your meetings, read only.

Mail in Other and newsletters get a quick look first: sender, subject and a few words. When one matters, it's read in full and can become a to-do.

## What it can send and change

- An email from a to-do, only after you approve it. It goes out from the mailbox's own address, not an alias.
- A reply goes into the Outlook conversation of the email it answers.
- After a reply goes out, the thread's messages move to a Snoozed folder in Outlook for a few days (3 unless the to-do says otherwise) and come back to the Inbox then, or sooner when someone answers. The review says so before you send.

The calendar is never changed.

## Photos of colleagues and contacts

Microsoft is also asked to read basic profiles in your organization (name, email and photo) and your Outlook contacts. Your Machine uses them only for photos, job titles and companies of people already in your Graph, up to 200 photos a day. Someone without a photo is checked again after 30 days.

Your organization's admin may have to approve the colleague photos. If they don't, Outlook still connects, just without these photos. An account connected before this gets one to-do: press **Reconnect**, or **Not needed** to close it for good. A personal account (Outlook.com, Hotmail) has no colleagues, so its to-do asks only for contacts’ photos.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup.
2. Press **Connect Microsoft** and sign in.
3. If Microsoft asks for admin approval, send your Microsoft 365 admin the link (**Copy link**). Once they approve, everyone in your organization can connect. If you are the admin, press **I'm the admin: approve now**.

Or in the dashboard: **Connections**, **Email**, pick Outlook and press **Sign in with Microsoft**. The admin link is right under the button.

On your own computer, once it's [paired with your account](friends.md#a-machine-on-your-own-computer): open **Connections**, then **Email**, pick Outlook and press **Sign in with Microsoft**. Mail and calendar connect together. After Microsoft, you're back in **Connections** on your dashboard.

For IT teams with their own Microsoft Entra app: open **Use your own app** there, or run `assistant connect outlook`.

## Remove it

- On a hosted Machine: press **Disconnect** next to the account on your setup page. **Disconnect ↗** on Connections takes you there.
- On your own computer: **Connections**, open the account, **Details**, then **Disconnect**.

## Uninstall it on Microsoft

Microsoft doesn't let us revoke a sign-in, so remove it there too:

- Work or school account: myapps.microsoft.com
- Personal account: account.live.com/consent/Manage
