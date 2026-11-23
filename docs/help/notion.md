---
title: Notion
area: connections
summary: Comments, mentions and tasks assigned to you in Notion. Replies, new pages, edits and marking tasks done wait for your OK.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
---
## What it reads

The pages your Notion connection can see. It brings in:

- Comments on your pages, replies in discussions you're in, and comments that mention you. One that needs you becomes a to-do.
- Database items assigned to you, with their due date and status. Each becomes a to-do, and its due date shows in **Calendar**. When the item is done in Notion, the to-do closes by itself. **Undo** opens it again.
- New pages someone else adds that you can see.
- A quiet heads-up when someone changes a page you asked to have changed. It never buzzes.

The first sync goes back 7 days. People link to your [Graph](graph.md) by their email address. When Notion doesn't share one, only by a full name exactly one person in your Graph has.

To use it only for doing things, turn off **Brings in signals** under **Details**.

## What it can do

When a to-do or a meeting needs a page's text, your Machine reads that one page, only while it works on it. Of a file on that page it sees only the name. It finds pages by their title, not the files on them.

Each of these waits for your OK on its to-do:

- Reply to a comment, in its discussion.
- Create a new page. It's private until you share it.
- Edit a page. Press **Review changes** to see each paragraph before and after, then **Save**. It writes only into the page as you saw it. If someone changed it in the meantime, nothing is written and the to-do says so.
- Mark a task assigned to you done. Only its status changes.

It never deletes, shares or moves a page.

## Connect it

1. In the dashboard: **Connections**, **Docs and files**, Notion. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Notion. On your own computer, pair it with your account first.
2. Press **Sign in with Notion**, pick your workspace and the pages it may see, and allow access.
3. Back in The Machine, it checks the sign-in right away and shows the workspace's name.

For another workspace, add Notion again.

## Paste a token instead

Under **Or paste an integration token**, press **Get your token**. Notion opens its integrations page: make an internal integration, allow reading and inserting content and comments, and reading user information with email addresses. Copy its token, paste it and press **Connect**.

Then share your pages with it in Notion, under **Connections** on each page. On your own computer, `assistant connect notion` asks for it too.

## Remove it

- In the dashboard: **Connections**, open Notion, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Notion

In Notion: **Settings**, **Connections**, then disconnect The Machine. A pasted token: delete the integration on the integrations page.
