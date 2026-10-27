---
title: Google Docs and Word
area: connections
summary: Comments, mentions, suggested edits and shares on your Google Docs or Word files. It reads, and posts a comment reply only after you press Post.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
---
## What it reads

Docs uses the Google or Microsoft sign-in you already have for that address. It brings in:

- Docs someone shares with you.
- Comments and replies on docs you own, and comments that mention you.
- Suggested edits on Google Docs you own, and tracked changes in Word files you own.

The first sync looks back 30 days. Each one becomes an event, linked to the people and projects in your [Graph](graph.md). When a comment needs you, it becomes a to-do.

## What it can do

When a to-do needs a doc's text, your Machine reads that one doc, and only while it works on that to-do.

It can draft a reply to a comment. On Google Docs, the reply waits on the to-do: press **Review and post**, check it, then **Post now**. Nothing is posted until you do. Word files have no way to post a reply from outside Word, so those replies stay drafts for you to copy into Word.

It never edits a doc, accepts a suggestion, resolves a comment or shares a file.

## What it asks for

Reading docs needs its own OK, apart from your mail sign-in. Your Gmail and calendar access stay as they are.

- Google: read-only access to your Drive files and comments. Posting replies needs one more OK, which you can skip.
- Microsoft: read access to your files, including the ones shared with you in OneDrive and SharePoint.

Until you give it, the Docs card says **Waiting for your OK to read docs**, with a button to give it.

## Connect it

1. Connect Gmail or Outlook for the address first.
2. Open **Connections**, then **+ Add**, pick Docs and enter that address. Or run `assistant connect docs`.
3. Press **Connect Google Docs** or **Connect Microsoft documents** on its card, and approve.

## Work or personal

Docs follows the work or personal label of its connection, like mail. Work docs can reach your team's Graph under your [sharing rules](sharing-rules.md). Personal ones never do.

## Remove it

In the dashboard: **Connections**, open Docs, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
