---
title: Connections
area: connections
summary: Your sources in one place: how each is doing, add a new one, or disconnect one.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## How they're doing

The **Connections** tab groups your sources into **Mail and calendar**, **Chat** and **Other sources**. Each says how it's doing: Connected, Waiting for first sync, Reconnecting automatically, or Needs your help. **Details** shows **Recent syncs** in plain words (like "Caught up") and what to do.

Its counts show what it brought in, what came in the last 24 hours and what isn't checked yet. A calendar counts its events.

Each source also says in one line what it brings in and, if it can act, that it acts only after you press **Send** or OK it.

## Add one

Open **+ Add** and pick a source. The list is grouped (**Mail and calendar**, **Chat**, **Meetings**, **Docs and files**, **Customers**, **Projects and code**, **Other**), A to Z within each.

**Suggested for you** sits on top when your Machine sees a reason for a source, with that reason in one line: mail from Stripe, Zoom meetings on your calendar, messages that link to Google Docs, or a setup that didn't finish. It counts these on your Machine; nothing leaves it. No reason, no section. A connected source is never suggested.

Fill in what it needs (a key, an address), pick **Work** with its company or **Personal** (mail and calendars ask only when their address doesn't say), and press **Connect**. A site like LinkedIn or X opens its sign-in in your Machine's browser and goes on by itself once you're in. GitHub, WhatsApp and Codex show a code to enter, and Telegram chats a QR code to scan.

**Cancel** stops adding it. Left before it finished? Open **Connections** again, on any device, and it picks up at the same step. Once connected, your Machine restarts to start reading it, then shows how its first sync goes.

On a hosted Machine, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe and Intercom sign in right here: pick **Work** or **Personal** and press **Sign in**. You come back to this form, which shows how it went. GitHub, WhatsApp, Codex, Telegram chats and your Android phone show their code here too.

**Reconnect** on a source and in **Needs you** opens the same form. On your own computer, `assistant connect` does the same in a terminal.

## Work or personal

Each source counts as work (for a company you name) or personal. Change it under **Details**. **Guessed** means your Machine picked it from the address. Work to-dos wait for your work days. Google and Microsoft mail and calendars take it from their address when it's clear: a mail provider like Gmail or Outlook.com is Personal, your team's domain is Work. Otherwise it asks once, right after you sign in. **Change** sets it yourself. If its mail later says the other, the **Get more out of The Machine** to-do asks once whether to change it.

## Abilities

A source can bring in signals (what comes in becomes to-dos), do things for your to-dos (read a doc, or send, reply or change something after your OK), or both. With both, **Details** has a switch for each: **Brings in signals** and **Can do things**. One stays on: to stop both, disconnect it. A chat only has **Can do things**.

With **Brings in signals** off, it doesn't sync. With **Can do things** off, your Machine never reads, drafts or changes anything with it.

## Remove one

Open the source, **Details**, then **Disconnect**. It stops reading. What it already brought in stays. On a hosted Machine, Google, Microsoft, Microsoft OneDrive, Zoom and Stripe show **Disconnect ↗**, which opens your setup page.

**Disconnected lately** lists Google, Microsoft and Zoom sign-ins you removed. **Removed, confirmed** means the sign-in is gone everywhere. **Pending** says why, and your Machine keeps trying.

## Saved sign-ins

For sites like LinkedIn or X, tick **Save for next time** when you sign in. **Sign-ins** then lists them, and when a site logs your Machine out, it signs back in with one tap. Passwords stay encrypted on your Machine. **Forget** removes one.

## Checks

**Checks** shows how your Machine reads what comes in: recent checks, and what each one found. See [No new to-dos](reviews-paused.md).

Each connection has its own article in this section, with what it reads and what it can send.
