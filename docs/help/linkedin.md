---
title: LinkedIn
area: connections
summary: Your LinkedIn messages, read in your Machine's own signed-in browser. Replies only after you approve.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py
site: Connect, More sources, Remove
---
## What it reads

Your LinkedIn messages. It reads them in a tab of your Machine's own browser, signed in as you, now and then during waking hours. It uses no API key and marks nothing as read.

## What it can send

A reply to a message, and only after you approve it on the to-do. Until then it only drafts.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup and go to **More sources**.
2. Open LinkedIn, sign in to LinkedIn in your server's browser when it asks, then press **Connect**.

On your own computer:

1. In the dashboard, open **Connections**, then **+ Add**, and pick LinkedIn.
2. Pick **Work** with its company, or **Personal** and press **Connect**.
3. Press **Sign in to LinkedIn** and sign in in your Machine's browser. It connects by itself once you're in.

Or run `assistant connect linkedin`.

A second LinkedIn account gets a browser of its own. If LinkedIn signs your Machine out, see [Signed out of a site](signed-out.md).

## If LinkedIn asks for a code

LinkedIn often emails a code the first time your Machine signs in. Type it in the sign-in dialog under **Code** and press **Sign in**. The page stays put while you type.

If LinkedIn goes back to the start, or nothing happens for two minutes, it stopped this sign-in. Wait a minute and press **Try again**. If LinkedIn shows a robot check, finish it in your Machine's browser.

## Remove it

- In the dashboard: **Connections**, open LinkedIn, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Sign it out on LinkedIn

In LinkedIn, open Settings, Sign in and security, Where you're signed in, and sign out the session of your Machine's browser.
