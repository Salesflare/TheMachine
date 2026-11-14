---
title: Microsoft OneDrive
area: connections
summary: Comments, mentions, tracked changes and shares on your Word files in OneDrive and SharePoint. New docs and edits wait for your OK.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## What it reads

**Microsoft OneDrive** reads your Word files in OneDrive and SharePoint, on a hosted Machine and on your own computer. Outlook doesn't need to be connected. For Google Docs, see below. It brings in:

- Docs someone shares with you.
- Comments and replies on your docs, and comments that mention you.
- Tracked changes in your Word files.

The first sync goes back 30 days. Each item links to the people and projects in your [Graph](graph.md). A comment that needs you becomes a to-do.

## What it can do

When a to-do needs a doc's text, your Machine reads that one doc, only while it works on that to-do.

It can draft a reply to a comment. Word has no way to post replies from outside, so you copy the draft into Word.

It never accepts a suggestion, resolves a comment, shares a file or changes a doc without your OK.

To use it only for doing things, turn off **Brings in signals** under **Details**. It then only finds and reads the docs your to-dos need, and makes new ones.

## Create and edit docs

Your Machine can write a new doc, or change a doc a to-do is about:

- A new doc it makes right away when the to-do or a skill asks for one. It's private, in your own OneDrive or Google Drive. The to-do shows **Open the doc**. Sharing it or sending its link waits for your OK.
- A change to an existing doc it only prepares. Press **Review changes** to see each paragraph before and after, then **Save**. A change you ask for in the to-do's chat it makes right away.
- It writes only into the doc as you saw it. If someone changed it in the meantime, nothing is written and the to-do says so. Ask for a new draft.
- In Talk, it reads the whole change aloud and waits for a clear yes.
- If Microsoft or Google refuses a new doc, the to-do says why and shows **Review and create** to try again.

It can replace text and add text, paragraphs and headings. Tables, images, tracked changes and fields stay as they are.

A Work to-do's doc goes to that company's account, never to a personal one. On your own computer, a Google account connected for Gmail with Drive access can take new Google Docs too. If no account fits, the to-do says what to connect for Work: Microsoft OneDrive, or Google Docs where your Machine can use it.

When the doc isn't the last step, like a reply with its link, the to-do stays open and drafts that step for your OK.

Editing comes with connecting. An older connection that can only read shows **Allow edits** in **Connections**. Press it once and accept.

## What it asks for

Microsoft asks you for one OK: to read and change your files, including ones shared with you. Each change still waits for your OK on its to-do. Your mail and calendar access don't change.

If that OK is taken back later, Microsoft OneDrive says **Waiting for your OK to read docs** in **Connections**.

## Connect it

On a hosted Machine, or your own computer paired with your account:

- Open **Connections**, then **Docs and files**, and pick **Microsoft OneDrive**.
- Press **Sign in with Microsoft** and allow reading and editing your files.

If Microsoft doesn't allow reading, it isn't added. If you press **Allow edits** and Microsoft doesn't allow edits, it says so.

## Google Docs

On a hosted Machine, open **Connections**, then **Docs and files**, and pick **Google Docs**. Google asks you to let it see and edit the docs you point it to, and make new ones. Gmail doesn't need to be connected, and your Gmail access doesn't change.

Then your Machine:

- Reads a Google Doc linked in a to-do's messages, only while it works on that to-do.
- Prepares changes to that doc. Each waits for your OK, as above.
- Makes new private docs in your Google Drive.

It doesn't search your Drive. It sees comments, shares and suggestions only on docs it made. More would need access to your whole Drive, which it doesn't ask for.

On your own computer, your Machine can make a new Google Doc in a Gmail account signed in there that already has Drive access. It doesn't read your other Google Docs or their comments. **Docs & files** shows it as Google Docs, on that account.

## Work or personal

It follows its connection's Work or Personal label, like mail. Work docs can reach your team's Graph under your [sharing rules](sharing-rules.md). Personal ones never do.

## Remove it

Open **Connections**, then Microsoft OneDrive or Google Docs, **Details** and **Disconnect**. It stops reading. What it already brought in stays.
