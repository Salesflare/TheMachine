---
title: iCloud and other calendars (CalDAV)
area: connections
summary: Meetings from iCloud Calendar or any CalDAV calendar, like Fastmail, Nextcloud or Zoho. Read-only.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## What it reads

Your meetings, with their guests, rooms and notes: the past week and the next month when you connect, then every change. They show in Calendar and in meeting prep, like Google or Outlook meetings. Every calendar of the account is read, or only the one you name.

It is read-only: it never adds, moves or removes a meeting.

## Connect iCloud Calendar

1. Make an app-specific password at [appleid.apple.com](https://appleid.apple.com), under **Sign-In and Security**. The one you made for iCloud Mail works too.
2. In the dashboard, open **Connections**, then **Calendar**, and pick **iCloud Calendar**.
3. Fill in your Apple ID and the app-specific password, then press **Connect**.

## Connect another calendar

1. Open **Connections**, then **Calendar**, and pick **Other calendar**.
2. Fill in your email address and password. Many providers want an app password here, made in your account settings.
3. Press **Connect**.

The server is found for Fastmail, Yahoo, Zoho and servers that announce it. Yours not found? Open **Server settings** and type its CalDAV address, like `nextcloud.example.com/remote.php/dav`. **Only this calendar** reads one calendar by its name.

Google or Microsoft calendars? Pick **Google Calendar** or **Outlook Calendar** instead.

## When it stops

- **The calendar server refused the password**: you changed it, or the app password was removed. Connect it again with a new one.
- **Couldn’t reach the calendar server**: it retries by itself. If it keeps failing, check the address in Server settings.

## Remove it

**Connections**, open the calendar, **Details**, then **Disconnect**. What it already brought in stays. Remove the app password at your provider too.
