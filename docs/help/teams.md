---
title: Microsoft Teams
area: connections
summary: Teams chats, meeting chats and meeting notes for a work or school account. It only reads.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
---
## What it reads

Your 1:1, group and meeting chats in Teams: the last 7 days when you connect, then new messages every few minutes. About a year of older chats, and of channel threads with your admin's OK, comes in later as [history](history.md), a little at a time, without holding anything up.

With your admin's OK, it also reads:

- Channel threads in your teams.
- Meeting transcripts of meetings you organized.
- Copilot's meeting notes and action items, when you have a Microsoft 365 Copilot license.

Each transcript or set of notes lands on its meeting in your Calendar, marked **From Teams**. Without them, the meeting chat is still there.

Bots, apps and system messages are left out.

## What it can do

Nothing in Teams. It only reads. To reply, open the chat with **Open in Teams**.

## What it asks for

Microsoft asks to let The Machine read your chats and your profile. That needs no admin.

Channels, transcripts and Copilot notes need your organization's admin to approve them once. Until then, the Teams card says what it can't read yet and why.

It works only with a work or school Microsoft account. Personal accounts have no Teams chats to read this way.

## Connect it

On a hosted Machine:

1. In the dashboard, open **Connections**, **+ Add** and pick **Microsoft Teams**.
2. Press **Sign in with Microsoft** and give the OK. You're back in the dashboard.
3. For channels and meeting notes, send your admin the link the sign-in page shows. Once they approve, connect Teams again.

While setting up, the setup page has **Connect Microsoft Teams** too.

On your own computer, Teams isn't available yet.

## Remove it

In the dashboard: **Connections**, open Microsoft Teams, **Details**, then **Disconnect**. What it already brought in stays.

## Revoke it in Microsoft

Open myapps.microsoft.com and remove The Machine. If Outlook is connected with the same address, that disconnects it too.
