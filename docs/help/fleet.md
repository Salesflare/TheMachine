---
title: Fleets
area: fleet
summary: A Work Fleet for your team, a Family Fleet for home. Machines that help each other, by your sharing rules.
covers: tab:fleet, network
code: fleet.py, network.py, dashboard.html
site: Company sign-in, Ask to join, Approve, Removed lately, Activity, Download CSV
order: 1
---
The Machine Network connects Machines. What they tell each other is encrypted end to end, and each Machine answers only by your rules.

## Kinds of Fleet

- **Work Fleet**: your team. Hand off work, ask who knows someone, get intros and a team brief.
- **Family Fleet**: up to 6 people. When everyone's free, shared to-dos and plans. Free. See [Family](family.md).
- **Friends**: anyone on The Machine, one by one. Free. See [Friends](friends.md).

## The Fleet tab

It shows once you're in a Fleet, with a pane for each Fleet, Family, Friends, Network, Sharing and Activity.

## Ask your Fleet

Ask "who knows someone at Acme?" from the Fleet tab, or **Ask the Fleet** on an organization in the [Graph](graph.md). Each teammate's Machine answers by their own sharing rules, and asks them first when the rule says so.

## Answered by itself in a Work Fleet

In a Standard Work Fleet, your Machine answers a teammate's **who knows someone**, **meeting context** ("who's this guest?") and **who handles shared emails** by itself. It uses only what the [Team Graph](team-graph.md) already shares with your team. Private, personal and sensitive threads never count, and names come only of people the Team Graph already shares. Each answer shows in the Fleet tab, under **Activity**.

To stop one, set it to **Never** under **Sharing**. A rule saved as **Ask me first** now works as **Always**. While your Fleet's Team Graph sharing is off, who knows someone and meeting context keep asking you first.

Careful Work Fleets, Friends and Family still ask you first. Warm intros, handoffs, shared follow-ups and free questions keep their own rules.

## Team learnings

Once a day at most, your Machine reads a few client threads the Team Graph already shares with your team, and writes down how the team works. For example: "Refund requests are answered from the support inbox with the refund template." They show in your Work Fleet's pane under **Team learnings**, for everyone in the Fleet, and each one is logged under **Activity**. Nobody is asked first.

- Only threads someone on your team wrote in. Never private, personal or sensitive ones.
- Only what holds across several customers: a process, a tool, a writing style, or who handles what. Never something about one customer, never feedback on your own product, and never names, addresses, numbers or quotes.
- Each one has a label: what kind it is, that it came from team conversations, and that it's for this Fleet. Ones it isn't sure about are dropped.

Anyone in the Fleet can **Remove** a learning. It's gone for everyone and isn't made again. To stop, turn off **Offer to share learnings** in Settings, Security. Careful Work Fleets get none.

## Brief requests

A teammate with the team brief on asks your Machine for counts and dates each morning. In a Work Fleet your Machine answers by itself, with only what the [Team Graph](team-graph.md) already shares with your team. Private and personal threads never count, and nothing goes while your Fleet's Team Graph sharing is off. Each answer shows in the Fleet tab, under **Activity**. It never becomes a to-do or a notification.

To stop, turn off **Share my brief facts with the team** in the Fleet tab, under **Sharing**. Their brief then lists you as not answered.

In a Careful Fleet, asks wait for you in the Fleet tab under **Brief requests**: **Share once**, **Always share**, **Decline** or **Never**. Only the latest ask per teammate waits, and unanswered ones expire. Nothing is shared until you choose.

## Team Graph

In a Work Fleet, client work is shared with your team, after you look it over. See [Team Graph](team-graph.md).

## What your Machine answers

Set it per Fleet, on the Sharing pane. See [Sharing rules](sharing-rules.md). **Settings** has a shortcut: **Fleet rules**.

## Company sign-in

For a hosted Work Fleet. An owner or admin signed in with a company Google Workspace or Microsoft 365 account can turn on **Company sign-in** on the Account page. It uses that account's domain.

Teammates who sign in with an account on that domain then see **Ask to join**. An owner or admin must **Approve** each request. Personal Gmail and Outlook.com accounts never count.

Removing someone from the Fleet signs them out everywhere.

To join a Fleet, start one, or pair a Machine on your own computer, see [Plans and billing](plans-and-billing.md) and [Friends and the Network](friends.md).

## For owners and admins

The Fleet part of your account page shows two more things:

- **Removed lately**: each person removed, or who left. It says **Removed, confirmed** once their Machine removed the work data, Google confirmed the sign-out and any shared token they had was replaced. Until then it says **Pending** and why.
- **Activity**: who did what and when. Invites, joins, removals, roles, servers and billing, shared connectors and approvals. It also lists every time our team opened a member's server or its logs. Never message content. **Download CSV** exports it. Kept 12 months.

After **Stop sharing**, a shared connector shows **Removed, confirmed** once every Machine deleted the token.
