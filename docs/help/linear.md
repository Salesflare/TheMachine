---
title: Linear
area: connections
summary: Your Linear issues, mentions, comments, reviews and due dates. Comments, status and assignee changes and new issues wait for your OK.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
---
## What it reads

Your own Linear inbox and the issues assigned to you. It brings in:

- Issues assigned to you: new ones, and ones whose status, due date or title changed. When an issue is done or canceled in Linear, its to-do closes by itself. **Undo** opens it again.
- Mentions of you, and comments and replies on issues you follow.
- Review requests and issues added to triage.
- Due date reminders.

Each becomes a to-do only when it needs you, judged by what it says. Your own changes never come in. The first sync goes back 7 days. People link to your [Graph](graph.md) by the email address Linear shows for them.

To use it only for doing things, turn off **Brings in signals** under **Details**.

## What it can do

Each of these waits for your OK on its to-do:

- Comment on an issue the to-do is about, or reply in a comment's thread. It posts as you.
- Change that issue's status, to one of its team's statuses.
- Assign it to someone on its team, or to you.
- Create a new issue in one of your teams.

It never deletes, archives or moves an issue to another team.

## Connect it

1. In the dashboard: **Connections**, **+ Add**, Linear. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Linear. On your own computer, pair it with your account first.
2. Press **Sign in with Linear**, pick your workspace and allow access.
3. Back in The Machine, it checks the sign-in right away and shows the workspace's name.

For another workspace, add Linear again. Choose **Work** or **Personal** like any connection.

## Paste an API key instead

Under **Or paste an API key**, press **Get your token**. Linear opens **Settings**, **Security & access**: make a personal API key, copy it, paste it and press **Connect**. On your own computer, `assistant connect linear` asks for it too.

## Remove it

- In the dashboard: **Connections**, open Linear, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Linear

In Linear: **Settings**, **Security & access**, then revoke The Machine under authorized applications. A pasted key: revoke the key on the same page.
