---
title: Team Graph
area: fleet
summary: Experimental. Share client work with your Work Fleet, like a CRM. What goes, what never does, and how to keep something private.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
In a Work Fleet, your Machine can share client work with your teammates' Machines, like a shared CRM. It's **Experimental** and starts off.

## Turn it on

An admin turns on **Share the Graph in this Fleet** on **What's shared**, and confirms the company may share this mail and has told its people. Everyone sees whether it's on.

Requiring everyone's Work email or calendar also turns it on. Each person then picks what else goes under **Your connections**. A new teammate's first share waits an hour, so they can keep things private first.

## Your connections

**Your connections** on **What's shared** lists each connection with a switch. Work ones at your Fleet's domain start on. Ones at another company's domain start off and say "Other company, not shared". Personal ones never go. Turning one off takes back what it shared.

Someone else's calendar that you read through your own sign-in shows under its own name, as personal.

Within a connection that's on, each thread is still sorted. Your company's own Slack counts as colleagues only; only a Slack Connect chat with another company can be client work. Personal, colleague-only, sensitive and automated threads stay out, unless you share one yourself.

## Required by the Fleet

An admin can require everyone's **Work email** and **Work calendar** at the Fleet's domain, under **Required by the Fleet**, after confirming the company has told its people. Work mail belongs to the company, as in any CRM. Required connections show "Required by" your Fleet and can't be turned off. Threads you keep private stay private.

## What goes to the team

- Client threads: work email with people outside your company, with attachments.
- Work people, organizations and projects, with a short timeline. On a page's **Timeline**, **Team** shows each event once, in your language where a teammate's Machine wrote it so, with everyone it came from: "via Sam, Kim, and Lee".
- A small copy of an organization's logo and of a person's work photo: from a look-up, Slack, LinkedIn, X, Salesflare or Microsoft. Never a Google contacts, WhatsApp, Telegram or Facebook picture, or a picture you changed or removed.
- On a Team board, a project's meetings, Zoom notes, Intercom conversations and chats. Sensitive ones, like deals, and colleague-only chats stay out.
- Counts and dates for a teammate's [team brief](fleet.md#brief-requests).
- Answers when a teammate asks who knows someone or wants meeting context. See [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Team learnings](fleet.md#team-learnings): how the team works, with no names or customer details.

## Kept out of automatic sharing

- Sensitive threads: buying or selling a company, investments, deal talks, HR and hiring, legal, health, money, security. Not even that they exist.
- Automated mail: receipts, invoices, alerts, newsletters and supplier bills.
- Colleague-only threads, personal mail and anything from a personal account. Personal never goes, not even when you tap Team.
- Anything you marked **Keep private**, and boards and projects set to Only you.
- Someone who is Personal to you, like your Family or Friends, and their mail. A project they're on still goes with its board, without them.

Each thread is judged on what it's about, and that can be wrong. Check what would go and use Keep private to correct it. Sharing a thread yourself, with the team or named people, overrides a sensitive label, so check who gets it.

## Share a board with chosen people

On a board's **⋯** menu, tap **Share board…** and pick teammates. Only they get its projects with full timelines: email, meetings and Zoom notes, Intercom conversations, chats, to-dos and moves. Sensitive ones, like deals, go too.

Personal and colleague-only threads stay out, and so do your Family and Friends, automated mail and connections you didn't select.

- A project added to the board later goes too. One moved off is taken back.
- Take someone off, or pick nobody, and it's taken back from their Machine.
- To share one thread with chosen people, tap its label, then **Share with…**. This can include sensitive or automated work mail, never personal or colleague-only threads.

## Not sure? It waits

When your Machine isn't sure, it doesn't share. Those threads wait under **Share these?**, grouped by kind (like "Partner and listing exchanges"), each with a suggestion:

- **Share with team**: everyone in the Fleet.
- **Share with…**: only the teammates you pick, like a board member for investor talks.
- **Keep private**: it stays with you.

One tap decides a whole group. Open a group to untick threads you want to decide one by one.

Talks about buying, selling or investing in a company, and board matters, are sensitive, so they don't wait here. Everyday work with a partner company is client work.

## Before the first share

Your first share goes by itself an hour after your Machine tells you. In that hour, open **Fleet**, then **What's shared** to see the client threads that would go, by organization. Tap **Keep private** on any of them, or **Share now** to send at once. Admins see who hasn't shared yet.

## What's shared

**Fleet** › **What's shared** shows it all: counts per kind, each shared thread and why it went, the ones under **Share these?**, and what you keep private. Tap a subject to read it. **Settings** and each thread's label link here too.

A new client thread waits an hour before it goes, so there's time to change your mind.

## Unshare

Tap the **Team** label on a thread, then **Unshare**. Every teammate's Machine deletes the thread, its attachments and its timeline lines, or does so once it's back online. Someone may have read it already.

**Keep private** on a person, organization or project unshares all of it.

Keep two threads with the same company private and your Machine asks once whether to always keep that company private.

## Who sees it

Only your teammates' Machines. It's encrypted end to end. The Machine Network passes it on but can't read it.

## Joining and new devices

An admin lets each person in once. The ask shows under **To-dos** for every admin, and the first answer counts. After that, sharing needs no more OKs.

Until then, the new person's Graph and Fleet say which admins they're waiting for. **Mine** and **Team** show a few seconds after the OK, without a reload.

A new Machine of someone already in gets the team's Graph after 24 hours. Meanwhile admins can tap **Not theirs** to keep it out.

Each of these asks keeps the Machine's safety number folded under **Their Machine's safety number**. It changes when that Machine's keys change.

## When someone leaves

They get nothing new from that moment. What they shared stays with the team. An admin can also **Take out** someone, and **Share again** later.

## Turn it off for everyone

An admin turns off **Share the Graph in this Fleet** on **What's shared**. Nothing new goes.

**Turn off** keeps what teammates already have. **Turn off and remove shared data** makes every Machine delete it. When sharing comes back on, each person looks it over again first.

## Stop sharing your own work

Turn your connections off under **Your connections**, unless the Fleet requires them. What they shared is taken back.

See also [Fleets](fleet.md) and [Security and privacy](security-and-privacy.md).
