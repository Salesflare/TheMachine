---
title: Microsoft OneDrive
area: connections
summary: Comments, mentions and tracked changes on your Word files in OneDrive. New docs and edits wait for your OK.
covers: connector:docs
code: connectors/docs.py, google_files.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## What it reads

**Microsoft OneDrive** reads your Word files in OneDrive, on a hosted Machine and on your own computer. Outlook doesn't need to be connected. For Google Docs, see below. It brings in:

- Comments and replies on your Word files, and comments there that mention you.
- Tracked changes in your Word files.

The first sync goes back 7 days. Each item links to the people and projects in your [Graph](graph.md). A comment that needs you becomes a to-do.

## Files others share with you

Microsoft stops listing these in November 2026. Shares, and mentions in someone else's file, then reach your Machine only as Microsoft's own emails. Connect [Outlook](microsoft.md) too, and keep those emails on. A to-do from one opens the email, and its button opens the file. A share or mention without an email isn't seen.

## What it can do

When a to-do needs a doc's text, your Machine reads that one doc, only while it works on that to-do. It can read Word, PDF and text files.

It also looks for files of any kind in your own OneDrive, and gives you the link. It doesn't search SharePoint sites or files shared with you. It can't read a scanned PDF's text.

It can draft a reply to a comment. Word has no way to post replies from outside, so you copy the draft into Word.

It never accepts a suggestion, resolves a comment, shares a file or changes a doc without your OK.

To use it only for doing things, turn off **Brings in signals** under **Details**. It then only finds and reads the files your to-dos need, and makes new ones.

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

- Reads a Google Doc linked in a to-do's messages, or pasted in its chat, only while it works on that to-do.
- Prepares changes to that doc. Each waits for your OK, as above.
- Makes new private docs in your Google Drive.

It doesn't search your Drive. It sees comments, shares and suggestions only on docs it made. More would need access to your whole Drive, which it doesn't ask for.

## Google Sheets and Slides

If Google Docs under **Connections** shows **Allow Sheets and Slides**, press it and allow both. Google asks to let your Machine see your Sheets and Slides files. It can't change them.

Then your Machine also reads a Google Sheet or Slides file linked in a to-do's messages, or pasted in its chat, only while it works on that to-do. It keeps no copy:

- From a sheet, the linked tab or cells first, then the other tabs, up to 2,000 cells. A formula shows as its value. Hidden tabs are read only when linked or asked for.
- From slides, the text and speaker notes, in order. Images and charts aren't read.

For a large file, ask in the chat for the tab, cells or slides you mean. If a file is private to someone else, deleted or an Excel or PowerPoint file, the to-do says so.

## Google Docs on your own computer

On your own computer, your Machine can make a new Google Doc in a Gmail account signed in there that already has Drive access. It doesn't read your other Google Docs or their comments. **Docs and files** shows it as Google Docs, on that account. It can also change a doc it made there for a to-do.

It also reads a Google Sheet or Slides file linked in a to-do, or pasted in its chat, if that Google sign-in already has access to Drive, Sheets or Slides. It never asks Google for more. If Google says no, turn on the Google Sheets or Slides API in that sign-in's own Google project.

## Work or personal

It follows its connection's Work or Personal label, like mail. Work docs can reach your team's Graph under your [sharing rules](sharing-rules.md). Personal ones never do.

## Remove it

Open **Connections**, then Microsoft OneDrive or Google Docs, **Details** and **Disconnect**. It stops reading. What it already brought in stays. On a hosted Machine, **Disconnect ↗** opens your setup page, which holds the sign-in.
