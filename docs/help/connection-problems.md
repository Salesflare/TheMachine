---
title: A connection needs help
area: troubleshooting
summary: A source says Needs your help, or stops bringing anything in. What to try.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Check its status

Open **Connections**. Each source says how it's doing:

- **Reconnecting automatically**: a short hiccup. It retries by itself.
- **Waiting for first sync**: just connected. Give it a few minutes.
- **Reads again at** 07:00: X and LinkedIn only read during the day. Nothing to do.
- **Needs your help**: open **Details**. It says what went wrong and what to do.
- **Phone disconnected**: your Android phone isn't reaching your Machine. Open the OpenClaw app on it.

A source that brings in nothing for longer than usual says **Waiting for a fresh sync**. It clears by itself once a sync gets through.

The number on **Connections** only counts sources that need your help.

## Common fixes

- "Sign in to Google again" (or Microsoft): one **Reconnect** brings back all of that account's sources, like Gmail and Calendar.
- "needs you to sign in again": press **Reconnect** and sign in.
- Microsoft still setting up access: it tries again by itself.
- Slack: press **Reconnect**. Connected with a Maton key? Check the key and the Slack connection in Maton.
- Android: open the OpenClaw app on the phone and allow it notification access.

On your own computer, `assistant doctor` checks every source and says how to fix each problem.

Still stuck? See [Get support](get-support.md).
