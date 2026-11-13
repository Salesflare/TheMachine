---
title: Fleets
area: fleet
summary: A Work Fleet for your team, a Family Fleet for home. Machines that help each other, by your sharing rules.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV, Ask me before starting a member's Machine
order: 1
---
A Fleet lets your Machine work with the Machines of your team, family or friends, over The Machine Network. What they tell each other is encrypted end to end, and your Machine answers only by your rules.

## Kinds of Fleet

- **Work Fleet**: your team. Hand off work, ask who knows someone, get intros and a team brief.
- **Family Fleet**: up to 6 people. When everyone's free, shared to-dos and plans. Free. See [Family](family.md).
- **Friends**: anyone on The Machine, one by one. Free. See [Friends](friends.md).

## The Fleet tab

It shows once you're in a Fleet, with a pane for each Fleet, Family, Friends, Network, Sharing and Activity.

## What it costs, leaving and starting a Fleet

Under each Fleet's name, **What it costs** shows its seats, who pays for your Machine and, for the owner, the Fleet's card and invoices. **Leave this Fleet** leaves it; an owner first hands it to someone else. **Start another Fleet** starts a new one.

Each opens that step of your account, and a change in price shows the amount to confirm first. On a self-hosted Machine they open your account in a new tab, where you sign in.

## Ask your Fleet

Ask "who knows someone at Acme?" from the Fleet tab, or **Ask the Fleet** on an organization in the [Graph](graph.md). Each teammate's Machine answers by their own sharing rules, and asks them first when the rule says so.

## Answered by itself in a Work Fleet

In a Standard Work Fleet, your Machine answers three kinds of teammate questions by itself: **who knows someone**, **meeting context** ("who's this guest?") and **who handles shared emails**. It uses only what the [Team Graph](team-graph.md) already shares with your team, never private, personal or sensitive threads. Each answer shows in the Fleet tab, under **Activity**.

To stop one, set it to **Never** under **Sharing**. A rule saved as **Ask me first** works as **Always**. While Team Graph sharing is off, who knows someone and meeting context ask you first.

Careful Work Fleets, Friends and Family still ask you first. Warm intros, handoffs, shared follow-ups and free questions keep their own rules.

## Team learnings

Your Machine writes down how your team works, from client threads the Team Graph already shares, at most once a day. For example: "Refund requests are answered from the support inbox with the refund template." They show in your Work Fleet's pane under **Team learnings**, for everyone in the Fleet, and each is logged under **Activity**. Nobody is asked first.

- Only threads someone on your team wrote in. Never private, personal or sensitive ones.
- Only what holds across several customers: a process, a tool, a writing style, or who handles what. Never something about one customer, never feedback on your own product, and never names, addresses, numbers or quotes.
- Ones it isn't sure about are dropped.

Your Machine uses the learnings that fit when it prepares a Work to-do for this company. Your own facts, rules and skills come first, and personal to-dos never use them. A to-do that used one says so, like "Used a team learning: refunds go out from the support inbox." Tap **Remove** there to take it out for the whole Fleet.

Anyone in the Fleet can **Remove** a learning: it's gone for everyone and isn't made again. To stop them, turn off **Offer to share learnings** in Settings, Security. Careful Work Fleets get none.

## Team brief

Pick **Daily** or **Weekly** for **Team brief** in the Fleet tab, under **Sharing**. Your Machine then asks your teammates' Machines for counts and dates. What needs you lands in To-dos, under Work: a customer waiting on a teammate, a company quiet for two weeks or more, two of you writing the same people, or a shared meeting.

- A to-do says who it waits on, since when, what they asked and what's at stake, like an open project. With nothing specific to say, it stays a line in the brief, not a to-do.
- The company and teammates link to their pages. **Details** shows what they wrote (tap it to read it), what's at stake, who on the team is in touch and their latest threads, only what the [Team Graph](team-graph.md) shares.
- When what they wrote is only in a teammate's mail, the to-do says who to ask.
- **Ask the team** sends them a question about it, prefilled. Their answers show on the to-do.
- **Not needed** closes it, and the brief learns. It comes back only with something new.
- When someone replies or takes it on, the to-do closes by itself. One about a company you already have a to-do for joins that to-do.

## Brief requests

A teammate with the team brief on asks your Machine for counts and dates each morning. In a Work Fleet your Machine answers by itself, with only what the [Team Graph](team-graph.md) already shares, and nothing while Team Graph sharing is off. Each answer shows in the Fleet tab, under **Activity**, never as a to-do or notification.

To stop, turn off **Share my brief facts with the team** in the Fleet tab, under **Sharing**. Their brief then lists you as not answered.

In a Careful Fleet, requests wait for you in the Fleet tab under **Brief requests**: **Share once**, **Always share**, **Decline** or **Never**. Nothing is shared until you choose, and unanswered ones expire.

## Team Graph

In a Work Fleet, client work is shared with your team, after you look it over. See [Team Graph](team-graph.md).

## Shared connections

An owner or admin can connect Stripe or Intercom once and share it with the team, from **Shared connections** in the Fleet tab. Teammates can read it, not change it, and see who shared it. Only admins change or stop it. See [Stripe](stripe.md) and [Intercom](intercom.md).

## What your Machine answers

Set it per Fleet, on the Sharing pane. See [Sharing rules](sharing-rules.md). **Settings** has a shortcut: **Fleet rules**.

## Company sign-in

Let teammates join with their company account. In a hosted Work Fleet, an owner or admin signed in with Google Workspace or Microsoft 365 can turn on **Company sign-in** on the Account page.

Teammates who sign in with that company domain see **Ask to join**, and an owner or admin must **Approve** each one. Personal Gmail and Outlook.com accounts never count.

Removing someone from the Fleet signs them out everywhere.

To join a Fleet, start one, or pair a Machine on your own computer, see [Plans and billing](plans-and-billing.md) and [Friends and the Network](friends.md).

## For owners and admins

**Manage** in the Fleet tab lists each Fleet you run: its people, their roles and the invites. On a hosted Machine you invite, change roles, remove people and answer join requests right there. A change that affects the price opens your account to confirm it first. On a self-hosted Machine it shows who is in it, with a link to that Fleet's settings on your account, where you manage its people and invites.

**Fleet settings**, under each Fleet's name in its pane and in Manage, opens that Fleet's settings on your account: shared connections, security, company sign-in, which Machine answers, and these two:

- **Removed lately**: each person removed, or who left. **Removed, confirmed** means their Machine deleted the work data and they're signed out everywhere. Until then it says **Pending** and why.
- **Activity**: who did what and when: invites, joins, removals, roles, hosted Machines, billing, shared connections and approvals. Also every time our support team read a member's Machine report or its logs. Never message content. **Download CSV** exports it. Kept 12 months.

**Ask me before starting a member's Machine**, for the owner: on, a new member's Machine waits for your OK, even in a free Fleet. Off, in a free Fleet it starts at once and you're told. A Machine that costs money always waits for you to confirm its amount.

After **Stop sharing**, a shared connection shows **Removed, confirmed** once every Machine lost access to it.
