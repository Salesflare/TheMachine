---
title: Exchange Server
area: connections
summary: Meetings from an Exchange Server your company runs (2013 to 2019 or Subscription Edition). Read-only.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## What it reads

Your meetings, with their guests, rooms and notes: the past week and the next month when you connect, then every change. They show in Calendar and in meeting prep.

It is read-only: it never adds, moves or removes a meeting. Mail from Exchange Server isn't read yet.

## Microsoft 365 or Exchange Server?

Exchange Server runs at your company. Microsoft 365 (Exchange Online) is Microsoft's cloud: pick **Outlook Calendar** for it instead. When your address turns out to be on Microsoft 365, the form says so.

## Connect it

1. In the dashboard, open **Connections**, then **+ Add**, and pick **Exchange Server**.
2. Fill in your work email address and your Windows password.
3. Press **Connect**.

The server is found from your address (Autodiscover). Not found? Open **Server settings** and type the server your IT team gives for Outlook, like `mail.example.com`. Signs in with a different name than your address? Type it as `DOMAIN\name` under **Username**.

It signs in with NTLM or Basic, over https only.

## When it stops

- **The calendar server refused the password**: your Windows password changed. Connect it again.
- **A Microsoft 365 mailbox**: your mailbox moved to Microsoft 365. Disconnect this one and connect **Outlook Calendar**.
- **Couldn’t reach the calendar server**: it retries by itself. Some servers are only reachable inside the company network or VPN.

## Remove it

**Connections**, open the calendar, **Details**, then **Disconnect**. What it already brought in stays.
