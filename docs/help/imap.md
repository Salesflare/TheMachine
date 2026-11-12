---
title: Other email (IMAP)
area: connections
summary: Mail from any provider with IMAP, like iCloud, Yahoo, Fastmail, Telenet or your own domain. Reads only for now.
covers: connector:imap
code: imap_mail.py, imap_presets.py, onboarding.py
order: 13
---
## What it reads

Your inbox and your Sent folder: the last 7 days when you connect, then everything new. Mail you send counts too, so it learns how you write and what you promised. Other folders aren't read.

Nothing is changed in your mailbox. Mail isn't marked read.

## What it can do

For now it only reads: it can't send from this mailbox yet. A reply drafted for you is yours to copy into your mail app.

## Connect it

1. In the dashboard, open **Connections**, then **+ Add**, and pick **Other email**.
2. Fill in your email address and password.
3. Press **Connect**.

Many providers want an app password for mail apps, not your normal password. Make one in your provider's account settings:

- iCloud: an app-specific password at account.apple.com.
- Yahoo: Account security, Generate app password.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: your normal Telenet mail password.
- Proton Mail: run Proton Mail Bridge on the same computer and use the password Bridge shows.

The server settings are filled in for most providers. Yours not found? Open **Server settings** and type what your provider gives for mail apps: the IMAP server, port and security (SSL/TLS or STARTTLS). The Machine never connects without TLS.

Gmail or Microsoft mail, also on your own domain? Pick **Gmail** or **Outlook** instead. They sign in without a password.

## When it stops

- **The mail server refused the password**: you changed it, or the app password was removed. Connect it again with the new one.
- **Couldn’t reach the mail server**: it retries by itself. If it keeps failing, check the server name in Server settings.

## Remove it

**Connections**, open the account, **Details**, then **Disconnect**. It stops reading and what it already brought in stays. Remove the app password at your provider too.
