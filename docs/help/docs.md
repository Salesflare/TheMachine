---
title: Microsoft OneDrive: Word files in OneDrive and SharePoint
area: connections
summary: Comments, mentions, tracked changes and shares on Word files in OneDrive and SharePoint, plus private new docs and edits you approve. Google Docs come later.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## What it reads

The **Microsoft OneDrive** connection reads Word files in OneDrive and SharePoint. You sign in with Microsoft for it, with or without Outlook connected. That works on a hosted Machine and on your own computer paired with your account. Google Docs come later: The Machine's Google sign-in can't read docs yet. It brings in:

- Docs someone shares with you.
- Comments and replies on docs you own, and comments that mention you.
- Tracked changes in Word files you own.

The first sync looks back 30 days. Each one becomes an event, linked to the people and projects in your [Graph](graph.md). When a comment needs you, it becomes a to-do.

## What it can do

When a to-do needs a doc's text, your Machine reads that one doc, and only while it works on that to-do.

It can draft a reply to a comment. Word files have no way to post a reply from outside Word, so the reply stays a draft for you to copy into Word.

It never accepts a suggestion, resolves a comment, shares a file or changes a doc without your OK.

A docs connection can be action-only: turn **Brings in signals** off under **Details**, and it only finds and reads the docs your to-dos need, and makes new ones. A Google one without access to all of Drive reads docs by their link, and the ones your Machine made.

## Create and edit docs

Your Machine can write a new doc, or change a doc one of your to-dos is about:

- A new doc it makes right away, when the to-do or a skill says to make one: a private doc in your own Google Drive or OneDrive, shared with nobody. The to-do shows it with **Open the doc**. Sharing it, or sending its link to someone, waits for your OK.
- A change to an existing doc it only prepares, each paragraph before and after. Press **Review changes**, read it, then **Save**. A change you ask for in the to-do chat it makes right away.
- It writes a change once, and only into the doc as you saw it. If someone changed the doc in the meantime, nothing is written and the to-do says so. Ask for a new draft.
- In Talk, it reads the whole change aloud and waits for a clear yes.
- If Google or Microsoft refuses a new doc, the to-do says what was refused and shows **Review and create** to try again.

It replaces text, adds text and adds paragraphs and headings. It leaves tables, images, tracked changes and fields alone. A new doc lands in your Google Drive or OneDrive and stays private until you share it.

A new doc goes to an account in the to-do's own area: a Work to-do's doc to that company's account, the one the conversation is in when it can, never to a personal one. On your own computer, a Google account signed in for Gmail that already has Drive access can take a new Google Doc too. If no account fits, the to-do says **Connect Google Docs or Microsoft OneDrive for Work**.

When the doc isn't the end of the to-do, like a reply with its link, the to-do stays open and drafts that next step for your OK.

Connecting Microsoft OneDrive already allows this: there is no separate step. A Microsoft OneDrive connection from before that only reads shows **Allow edits** on its card in **Connections**. Press it once and accept.

## What it asks for

Microsoft OneDrive asks Microsoft for one OK, apart from your mail sign-in: to read and change your files, including the ones shared with you in OneDrive and SharePoint. Each change still waits for your OK on its to-do. Your mail and calendar access stay as they are. Without Outlook, the sign-in only covers your files, never your mail or calendar.

If that OK is taken back later, the Microsoft OneDrive card says **Waiting for your OK to read docs**.

## Connect it

Outlook doesn't need to be connected for it.

- Hosted Machine: in the dashboard, open **Connections**, **+ Add**, pick **Microsoft OneDrive** and press **Sign in with Microsoft**. Microsoft asks you to allow reading and editing your files, then you come back to the dashboard.
- Your own computer, paired with your account: open **Connections**, **+ Add**, pick **Microsoft OneDrive** and press **Sign in with Microsoft**.

It checks that the sign-in may read docs. Without that OK it isn't added. If you press **Allow edits** and Microsoft doesn't allow edits, it says so instead of Connected.

## Work or personal

Microsoft OneDrive follows the work or personal label of its connection, like mail. Work docs can reach your team's Graph under your [sharing rules](sharing-rules.md). Personal ones never do.

## Remove it

In the dashboard: **Connections**, open Microsoft OneDrive, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
