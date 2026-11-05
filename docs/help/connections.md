---
title: Connections
area: connections
summary: Your sources in one place: how each is doing, add a new one, or disconnect one.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## How they're doing

The **Connections** tab groups your sources into **Mail and calendar**, **Chat** and **Other sources**. Each one says how it's doing: Connected, Waiting for first sync, Reconnecting automatically, or Needs your help. Open **Details** for **Recent syncs**, where its sync is in plain words (like "Caught up" or "First read"), and what to do.

Its counts show what it brought in, how much came in the last 24h and what isn't reviewed yet. A calendar counts events: all it has, those in the next 7 days and the last 24h.

Under its status, each source says in one line what it brings in and, when it can act, that it does so only after you press **Send** or OK it.

## Add one

Open **+ Add** and pick a source. It shows one short form, like your setup page: what it needs (a key, an address), and **Work** with its company or **Personal**. Press **Connect**. A source that signs in, like LinkedIn or X, opens its sign-in on your Machine and goes on by itself once you're in. GitHub, WhatsApp and Codex show a code to enter, and Telegram chats a QR code to scan.

**Cancel** stops adding it. Once it is connected, your Machine restarts to start reading it, then opens the new card, which shows how its first sync goes.

On a hosted Machine, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe and Intercom sign in right here: pick **Work** or **Personal**, press **Sign in**, and you come back to this form, which shows how connecting goes, or why it didn't work. GitHub, WhatsApp, Codex, Telegram chats and your Android phone show their code right in this form. The Codex tile says whether Codex is signed in.

**Reconnect** on a source and in **Needs you** opens the same form. On your own computer, `assistant connect` does the same in a terminal.

## Work or personal

Each source counts as work (for a company you name) or personal. Change it under **Details**. It says **Guessed** only when your Machine picked it from the address; once you pick, it's yours. Work to-dos wait for your work days.

## Abilities

A source can bring in signals (what comes in becomes to-dos), do things for your to-dos (read a doc when one needs it, or send, reply or change something after your OK), or both. With both, **Details** has a switch for each: **Brings in signals** and **Can do things**. One stays on. To stop both, disconnect it. A chat's replies answer what it brings in, so a chat only has **Can do things**.

With **Brings in signals** off, it doesn't sync and its card shows no counts. With **Can do things** off, your Machine never reads on demand, drafts or changes anything with it. Sources from before have both on.

## Remove one

Open the source, **Details**, then **Disconnect**. It stops reading. What it already brought in stays. On a hosted Machine, Google, Microsoft, Microsoft OneDrive, Zoom and Stripe show **Disconnect ↗**, which opens your setup page.

**Disconnected lately** lists Google, Microsoft and Zoom sign-ins you removed. **Removed, confirmed** means Google confirmed the sign-out, or for Microsoft and Zoom that no copy is left. **Pending** says why, and your Machine keeps trying.

## Saved sign-ins

Sites your Machine's browser uses, like LinkedIn or X, can save a sign-in: tick **Save for next time** when you sign in. Then **Sign-ins** lists them. When a site logs your Machine out, it signs back in with one tap. Passwords stay encrypted on your Machine. **Forget** removes one.

## Reviews

**Reviews** shows how your Machine is reading what comes in: recent runs, and what each one found. See [Reviews paused](reviews-paused.md).

Each connection has its own article in this section, with what it reads and what it can send.
