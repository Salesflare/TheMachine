---
title: A connection needs help
area: troubleshooting
summary: A source says Needs your help, or stops bringing anything in. What to try.
covers: 
code: onboarding.py, dashboard.html
order: 1
---
## Check its status

Open **Connections**. Each source says how it's doing:

- **Reconnecting automatically**: a short hiccup. It retries by itself.
- **Waiting for first sync**: just connected. Give it a few minutes.
- **Reads again at** 07:00: X and LinkedIn only read during the day. Nothing to do.
- **Needs your help**: open **Details**. It says what went wrong and what to do.

The number on **Connections** only counts sources that need your help.

## Common fixes

- "needs you to sign in again": press **Reconnect** and sign in. On a hosted Machine, you sign in right there and come back to the dashboard.
- Microsoft still setting up access: it tries again by itself.
- Slack: check your Maton API key and the Slack connection in Maton.
- Android: open the OpenClaw app on the phone, and allow it notification access.

On your own computer, `assistant doctor` checks every source and prints the fix for each problem.

Still stuck? See [Get support](get-support.md).
