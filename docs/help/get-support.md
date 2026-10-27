---
title: Get support
area: troubleshooting
summary: Report a bug from your dashboard, write to us, or let our team look at your Machine for a day.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html
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
3. Keep **Include the support report** on, unless you'd rather not: versions, checks and recent errors, without messages, keys or addresses.
4. Tap **Review**. It shows everything that goes, exactly as it goes.
5. Tap **Send**. Nothing is sent before that.

We answer by email. A self-hosted Machine can send one when it's on the Network; otherwise write to us.

If a report can't go out right away (you're offline, or you sent many in a short time), it isn't lost. Your Machine keeps it, says when it goes out, and sends it by itself. Reports still waiting show under **Waiting to go out**.

## Support access

On a hosted Machine, our team can look at it for you, but only once you allow it. In **Settings**, **Security**, **Support access**, tap **Allow for 24 hours**.

- Read-only: logs and settings, scrubbed like the support report. Never your messages, keys or passwords.
- It ends by itself after 24 hours. **Turn off** ends it now.
- Every look is listed under it, with when.

## From your own computer

Run `assistant support-bundle`. It saves a file with versions, the checks from `assistant doctor`, recent logs and your settings, without keys, tokens, passwords or addresses. Look through it, then send it to whoever helps you.

For a bug in the open-source app, open an issue on [GitHub](https://github.com/Salesflare/TheMachine/issues), with made-up data only.
