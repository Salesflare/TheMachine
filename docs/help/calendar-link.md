---
title: Proton Calendar and calendar links (ICS)
area: connections
summary: Meetings from a calendar's share link: Proton Calendar, published calendars, school or sports calendars. Read-only.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
---
## What it reads

The events in the calendar behind the link, with repeating events and time zones: the past week and the next month, then every change. They show in Calendar and in meeting prep.

A link can only be read, so it never changes a meeting. It checks the link at most every 15 minutes. Proton says changes can take a few hours to reach a link.

## Connect Proton Calendar

Proton Calendar has no other way in for apps, so it uses a share link.

1. Open Proton Calendar on the web, at calendar.proton.me. Share links can't be made in its phone apps.
2. Go to "Settings", "All settings", "Calendars", and pick the calendar.
3. Under "Share with anyone", press "Create link" and pick "Full view". Limited view only shows when you are busy.
4. Press "Copy link".
5. In the dashboard, open **Connections**, then **+ Add**, pick **Proton Calendar**, paste the link and press **Connect**.

## Connect any other calendar link

Pick **Calendar link (ICS)** and paste the link: an https or webcal address ending in .ics, like an iCloud public calendar, an Outlook published calendar or your kid's school calendar.

## Keep the link private

Anyone with the link can read the calendar. The Machine keeps it like a password: never in a log or on screen. To stop it, delete the link where you made it, then **Disconnect** here.

## When it stops

- **The calendar link stopped working**: the link was deleted or changed. Make a new one and connect it again.
- **Couldn’t reach the calendar server**: it retries by itself.
