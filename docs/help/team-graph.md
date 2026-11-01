---
title: Team Graph
area: fleet
summary: Experimental. Share client work with your Work Fleet, like a CRM. What goes, what never does, and how to keep something private.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
In a Work Fleet, your Machine can share your client work with your teammates' Machines, like a shared CRM. It's **Experimental**: new and still changing, so it starts off.

## Turn it on

An admin turns on **Share the Graph in this Fleet** on **What's shared**, and confirms the company may share this mail and has told its people. Everyone sees whether it's on. A Fleet that already shared before stays on.

Requiring everyone's Work email or calendar turns it on too. Then nobody has to start anything: what the Fleet requires goes, and each person picks what else goes under **Your connections**. A new teammate's first share goes within the hour, so they can keep anything private first.

## Your connections

**Your connections** on **What's shared** lists each one with a switch. Work ones at your Fleet's own domain start on. One at another company's domain starts off, even when it's a Work account: it says "Other company, not shared". You can turn it on. Personal ones never go. Turning one off takes back what it shared.

Someone else's calendar that you read through your own sign-in shows under its own name, as a personal connection.

Inside a connection that's on, each thread is still sorted. Your company's own Slack counts as colleagues only, also direct messages: only a Slack Connect conversation with another company can be a client thread. Personal and colleague-only threads stay out. Sensitive and automated mail stays out of automatic sharing; your explicit sharing choices can override those classifications.

## Required by the Fleet

An admin can require everyone's **Work email** and **Work calendar** at the Fleet's own domain, under **Required by the Fleet**, after confirming the company has told its people. Work mail belongs to the company, like in any CRM. Those then show "Required by" your Fleet and can't be turned off. Threads you keep private stay private. When sharing is still off, requiring something turns it on: no second switch.

## What goes to the team

- Client threads: email with people outside your company about work, with their attachments.
- Work people, organizations and projects, with a short timeline.
- On a Team board, a project's meetings, Zoom notes, Intercom conversations and chats too, by being on the board. Sensitive ones, such as deals, stay out, and so do chats only among colleagues.
- Your counts and dates for a teammate's [team brief](fleet.md#brief-requests), from these only.
- Answers to a teammate's who knows someone and meeting context, from these only. See [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Team learnings](fleet.md#team-learnings): how the team works, written from these threads, with no names or customer details.

## Kept out of automatic sharing

- Sensitive threads: buying or selling a company, investments, valuations, deal talks, HR, hiring and recruiters, legal, health, money, security. Not even that they exist.
- Automated mail: receipts, invoices, alerts, newsletters, and your company's own bills with its suppliers.
- Internal threads (only colleagues on them), personal mail and anything from a personal account. Personal never goes, not even when you tap Team.
- Anything you marked **Keep private**, and boards and projects set to Only you.

Each thread is judged on its own, by what it is about. Classification can be wrong; review what would go and use Keep private to correct it. Your explicit Team choice or a share with named teammates can override a sensitive classification; check the recipients before sharing.

## Share a board with chosen people

On a board's **⋯** menu, tap **Share board…** and pick teammates. Only they get its projects with their full timelines: email threads, meetings and their Zoom notes, Intercom conversations, chats, to-dos and moves. Sensitive ones go too, such as deals.

Personal and colleague-only threads stay out, and so do people in your Family or Friends and automated mail when only its board is shared. Connections you have not selected stay out too.

- A project added to the board later goes too. One moved off the board is taken back.
- Take someone off, or pick nobody, and it is taken back from their Machine.
- One thread can go to chosen people too: tap its label, then **Share with…**. This explicit choice can include sensitive or automated work mail. Personal and colleague-only threads cannot be shared.

## Not sure? It waits

When your Machine isn't sure, it doesn't share. Those threads wait under **Share these?**, grouped by what they are (like "Partner and listing exchanges"), each group with a suggested choice:

- **Share with team** goes to everyone in the Fleet.
- **Share with…** goes only to the teammates you pick, for example a board member for investor talks. The rest of the team doesn't get it.
- **Keep private** keeps it with you.

One tap decides a whole group. Open a group to see its threads and untick any you want to decide separately.

Talks about buying, selling or investing in a company, and board matters, count as sensitive, so they don't wait here. Listings, integrations and other everyday work with a partner company are client work.

## Before the first share

Your first share goes by itself within the hour, with nothing to confirm. Your Machine tells you once when that hour starts. In that hour, open **Fleet**, then **What's shared**: it lists the client threads that would go, by organization. Tap **Keep private** on any of them. **Share now** sends it without waiting. Admins see who hasn't shared yet.

## What's shared

**Fleet** › **What's shared** shows everything in one place: counts per kind, every shared thread with why it went, the ones waiting under **Share these?**, and what you keep private. Tap a thread's subject to read it. **Settings** has a shortcut, and so does the label on each thread.

A new client thread waits an hour before it goes, so there's time to change your mind.

## Unshare

Tap the **Team** label on a thread, then **Unshare**. Your Machine tells every teammate's Machine, and each deletes the thread, its attachments and its lines in the timeline. A Machine that was off does it when it's back. Someone may have read it already.

**Keep private** on a person, organization or project unshares all of it the same way.

Keep two threads with the same company private and your Machine asks once: always keep that company's threads private?

## Who sees it

Only your teammates' Machines. Everything is encrypted end to end, sealed for each teammate's Machine. The Machine Network only passes it on and can't read it.

## Joining and new devices

An admin lets each person into the Fleet once. After that, sharing with them needs no more OKs. The ask shows under **To-dos** for each admin, and the first answer counts for the whole team. Members never get it.

A new Machine of someone already in gets the team's Graph after 24 hours. Admins see it in the meantime and can tap **Not theirs** to keep it out.

## When someone leaves

They get nothing new from that moment. What they shared stays with the team. An admin can also **Take out** someone, and **Share again** later.

## Turn it off for everyone

An admin can turn **Share the Graph in this Fleet** off on **What's shared**. Everyone sees whether it's on. When it's off, nothing new goes.

**Turn off** keeps what went on teammates' Machines. **Turn off and remove shared data** makes every Machine delete what it got. When sharing is back on, each person looks it over again first.

## Stop sharing your own work

Turn your connections off under **Your connections**, unless the Fleet requires them. What they shared is taken back.

See also [Fleets](fleet.md) and [Security and privacy](security-and-privacy.md).
