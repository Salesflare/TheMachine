---
title: LinkedIn
area: connections
summary: Your LinkedIn messages, read in your Machine's own signed-in browser. Replies only after you approve.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
---
## What it reads

Your LinkedIn messages. It reads them in your Machine's own browser, signed in as you, now and then during waking hours. It marks nothing as read. Replies in conversations you archived and message requests come in too; spam stays out.

## Titles and companies

It also keeps the titles and companies of your LinkedIn connections up to date on the people already in your Graph, from your Connections list. It doesn't open their profiles or add new people. When someone's title or company changes, their timeline says so, like "Now Head of Sales at Acme, was Sales Lead at Acme".

The title comes from their headline, like "Head of Sales at Acme" or "VP Sales and Strategy", never a slogan. It finds them by their profile link, or by name and company. Without a company to compare, a full name only one person in your Graph has is enough. Their page also shows since when you're connected.

It reads very slowly: one page at a time, minutes apart, a few dozen pages a day, only during the day. About 3,000 connections take some four days. If LinkedIn pushes back, it stops until the next day.

## What it can send

A reply to a message, or a new message to a profile you name, and only after you approve it on the to-do. Until then it only drafts.

LinkedIn doesn't offer an official way to do this. Reading and an occasional message you approved is very unlikely to cause trouble; mass or automated sending can get an account blocked.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup and go to **More sources**.
2. Open LinkedIn, sign in to LinkedIn in your Machine's browser when it asks, then press **Connect**.

On your own computer:

1. In the dashboard, open **Connections**, then **Chat**, and pick LinkedIn.
2. Pick **Work** (with its company) or **Personal**, then press **Connect**.
3. Press **Sign in to LinkedIn** and sign in in your Machine's browser. It connects by itself once you're in.

Or run `assistant connect linkedin`.

A second LinkedIn account gets a browser of its own. If LinkedIn signs your Machine out, see [Signed out of a site](signed-out.md).

## If LinkedIn asks for a code

LinkedIn often emails a code the first time your Machine signs in. Type it in the sign-in dialog under **Code** and press **Sign in**. The page stays put while you type.

If LinkedIn goes back to the start, or nothing happens for two minutes, wait a minute and press **Try again**. If LinkedIn shows a robot check, finish it in your Machine's browser.

## Remove it

- In the dashboard: **Connections**, open LinkedIn, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Sign it out on LinkedIn

In LinkedIn, open Settings, Sign in and security, Where you're signed in, and sign out the session of your Machine's browser.
