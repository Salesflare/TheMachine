---
title: Share learnings with the team
area: security
summary: At most once a day it offers a few general learnings to The Machine team, and votes on learnings from other Machines. Nothing personal.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
---
## What it is

At most once a day, when there's something new, your Machine turns what it learned from you into a few general learnings that could make The Machine better for everyone. For example: "Drafts for people who don't know the context yet should introduce it first." It never offers the same learning twice.

Each learning comes with 1 to 3 use cases: a situation, what you do, and what should happen. For example: a first reply to a customer who hasn't heard of you; you open the draft; it says who you are before the ask. The team builds against them.

## What goes, and what never does

- Only the general pattern, with a short made-up example if it helps.
- Names, email addresses, links, phone numbers, dates and amounts are taken out before you see it. Each learning says what was taken out.
- Use cases are checked more strictly: no quotes and no names. One that fails is left out, also after you edit it.
- Filtering can miss details, so read the exact text before **Send**.
- An error log goes only when you tick **Add the error log**. Read that excerpt too.

## Nothing without your OK

Under **Learning**, **Shared**, a note asks "Share 3 learnings with The Machine team?" Tap **Review** to see exactly what would go. Edit or remove any learning or use case (each learning keeps at least one), then **Send**. Or pick **Not now** or **Never ask**.

It's sealed for the team and sent under a made-up name, unless you tick **Add my email so the team can reply**.

Other Machines may vote on a learning you shared, without knowing who sent it.

## Send automatically

Tick **Send automatically from now on** next to **Send**, or turn on **Send learnings automatically** in Settings, Security. New learnings then go without asking, checked the same way. It's off by default.

Every learning sent is listed, exactly as it went, in Settings, **Activity** and in Fleet, **Activity**. Tap **Withdraw** and the team no longer sees it.

Your email and error logs never go automatically. **Careful**, a Careful Work Fleet, or turning off **Offer to share learnings** stops automatic sending. Turned back on, it asks each time again.

## Turn it off

Turn off **Offer to share learnings** in Settings, Security. See [Security levels](security-levels.md). Sharing needs [The Machine Network](/network).

The same switch turns off [team learnings](fleet.md#team-learnings) for your Work Fleet and takes back the ones your Machine shared.

## Voting

Learnings from other Machines come to yours too. Once a day a short check asks: would this have changed something on your Machine in the past week? Only the vote goes back. Your own learnings never come back to you.

A useful vote needs a concrete case from your past week, told in general terms and checked like a use case. Without one, the vote is **Not relevant here**.

The team ranks learnings by useful votes and picks what goes into The Machine for everyone. Nothing changes by itself.

**Vote on learnings from other Machines** in Settings, Security has three choices:

- **On**, the default: it votes by itself.
- **Ask first**: votes wait for you under **Learning**, **Shared**, each with the learning and the vote. Send or skip them one by one or all at once. No to-do or notification. Votes you leave expire after 14 days.
- **Off**: no voting, and nothing waiting goes.
