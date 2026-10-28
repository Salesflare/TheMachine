---
title: Docs: Word, OneDrive and SharePoint
area: connections
summary: Comments, mentions, tracked changes and shares on your Word files in OneDrive and SharePoint. Google Docs come later.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## What it reads

Docs reads Word files in OneDrive and SharePoint, with the Microsoft sign-in you already have for that address. That works on a hosted Machine and on your own computer paired with your account. Google Docs come later: The Machine's Google sign-in can't read docs yet. It brings in:

- Docs someone shares with you.
- Comments and replies on docs you own, and comments that mention you.
- Tracked changes in Word files you own.

The first sync looks back 30 days. Each one becomes an event, linked to the people and projects in your [Graph](graph.md). When a comment needs you, it becomes a to-do.

## What it can do

When a to-do needs a doc's text, your Machine reads that one doc, and only while it works on that to-do.

It can draft a reply to a comment. Word files have no way to post a reply from outside Word, so the reply stays a draft for you to copy into Word.

It never edits a doc, accepts a suggestion, resolves a comment or shares a file.

## What it asks for

Reading docs needs its own OK, apart from your mail sign-in: Microsoft asks to let it read your files, including the ones shared with you in OneDrive and SharePoint. Your mail and calendar access stay as they are.

If that OK is taken back later, the Docs card says **Waiting for your OK to read docs**.

## Connect it

Connect Outlook for the address first. Then:

- Hosted Machine: in the dashboard, open **Connections**, **+ Add**, pick **Docs** and press **Sign in with Microsoft**. Microsoft asks you to allow reading your files, then you come back to the dashboard.
- Your own computer, paired with your account: open **Connections**, **+ Add**, pick **Docs** and press **Sign in with Microsoft**.

It checks that the sign-in may read docs. Without that OK it isn't added.

## Work or personal

Docs follows the work or personal label of its connection, like mail. Work docs can reach your team's Graph under your [sharing rules](sharing-rules.md). Personal ones never do.

## Remove it

In the dashboard: **Connections**, open Docs, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
