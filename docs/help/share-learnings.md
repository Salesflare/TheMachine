---
title: Share learnings with the team
area: security
summary: At most once a day it offers a few general learnings to The Machine team, and votes on learnings from other Machines. Nothing personal.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
---
## What it is

At most once a day, when there is something new, it turns what it learned from you since the last time into a few general learnings that could make The Machine better for everyone. For example: "Drafts for people who don't know the context yet should introduce it first." It never offers the same learning twice: not one you sent, removed or withdrawn.

Each learning comes with 1 to 3 use cases: a situation, what you do, and what should happen. For example: a first reply to a customer who hasn't heard of you; you open the draft; it says who you are before the ask. The team builds against them, so what ships stays true to what was meant.

## What goes, and what never does

- Only the general pattern, and a short made-up example if it helps.
- Names, email addresses, links, phone numbers, dates and amounts are taken out before you see it. Each learning says what was taken out.
- Use cases are checked more strictly: no quotes and no names, also ones it doesn't know. A use case that fails is left out. If you edit one, it must pass the same check before it can go.
- It is designed to share general learnings, not your messages or who you deal with. Filtering can miss details: review the exact text before **Send**.
- An error log only when you tick **Add the error log**. Review the excerpt too: filtering is best effort.

## Nothing without your OK

Under **Learning**, **Team**, a short note asks "Share 3 learnings with The Machine team?" Tap **Review** to see exactly what would be sent. Edit or remove any learning or use case (each learning keeps at least one use case), then **Send**. Or pick **Not now** or **Never ask**.

It's sealed for the team and comes from a made-up name, unless you tick **Add my email so the team can reply**.

Other Machines may vote on a learning you shared, without knowing who sent it. Your email never goes along.

## Send automatically

Tick **Send automatically from now on** next to **Send**, or turn on **Send learnings automatically** in Settings, Security. New learnings then go without asking, checked the same way. Off by default.

Every learning sent is listed in Settings, **Activity**, and in Fleet, **Activity**, exactly as it went. Tap **Withdraw** and the team no longer sees it.

Your email and error logs never go by themselves. **Careful**, a Careful Work Fleet, or turning off **Offer to share learnings** stops it. Turned back on, it asks each time again.

## Turn it off

To stop being asked, turn off **Offer to share learnings** in Settings, Security. See [Security levels](security-levels.md). It needs [The Machine Network](/network).

The same switch turns off [team learnings](fleet.md#team-learnings) for your Work Fleet, and takes back the ones your Machine shared.

## Voting

Learnings other Machines shared come to yours too. Once a day a short check asks one question: would this have changed something on your Machine in the past week? It sends back only a vote. Nothing about you goes along. Your own learnings are never sent back to you to vote on.

A useful vote needs a concrete case from your past week, told generically and checked like a use case. Without one, the vote is **Not relevant here**. The team counts only useful votes with a case.

The team sees the learnings ranked by votes and picks what goes into The Machine for everyone. Nothing changes by itself.

**Vote on learnings from other Machines** in Settings, Security has three choices:

- **On**, the default: it votes by itself.
- **Ask first**: each vote waits for you in one box under **Learning**, **Team**, with the learning and the vote as it would go. Send it or Skip it, one at a time or all at once. No to-do and no notification for it. A vote you leave goes unsent after 14 days.
- **Off**: no voting, and nothing waiting goes.

