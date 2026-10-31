---
title: Get support
area: troubleshooting
summary: Report a bug from your dashboard, write to us, or let our team look at your Machine for a day.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Write to us

Email support@themachine.computer. A person answers.

On a hosted Machine, the dashboard's footer has "Something's wrong?", which opens your account's **Report a problem** form.

## Report a bug

Open **Help**, then **Report a bug**. An error message has a **Report a bug** button too.

1. Say what went wrong.
2. Add a screenshot if it helps: **Take a screenshot** of the dashboard, or **Attach an image**.
3. Keep **Include a support report** on, unless you'd rather not. It adds versions, checks and recent errors, without messages, keys or addresses, and lets our team read your Machine's logs and settings for 24 hours. See [Support access](get-support.md#support-access). Unticked, only what you wrote and your screenshot go.
4. Tap **Send**. The form closes at once. Your Machine adds the support report on its own; a slow check never holds your report up.

We take it from there. A self-hosted Machine can send one when it's on the Network; otherwise write to us.

Once we fix a bug you reported and your Machine runs the fix, we tell you once: a short line on your dashboard (**Got it** closes it) and a short email. A self-hosted Machine hears of it when it's on the Network.

If a report can't go out right away (you're offline, or you sent many in a short time), it isn't lost. Your Machine keeps it, says when it goes out, and sends it by itself. Reports still waiting show under **Waiting to go out**.

## Support access

Our team can look at your Machine for you, but only once you allow it. When you report a bug with **Include a support report** on, it turns on when you press **Send**. On your own computer, it needs your Machine [paired with your account](friends.md).

- Read-only: logs, settings, versions, how each connection syncs and recent errors, scrubbed like the support report. Never your messages, keys, passwords or who your contacts are.
- It ends by itself after 24 hours. While it's on, **Settings**, **Security** shows it: **Turn off** ends it now.
- Every look is listed in Settings, **Activity**, with when. See [Activity](activity.md).

## From your own computer

Run `assistant support-bundle`. It saves a file with versions, the checks from `assistant doctor`, recent logs and your settings, without keys, tokens, passwords or addresses. Look through it, then send it to whoever helps you.

For a bug in the open-source app, open an issue on [GitHub](https://github.com/Salesflare/TheMachine/issues), with made-up data only.
