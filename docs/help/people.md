---
title: People
area: graph
summary: Everyone you're in touch with: their page, summary and timeline, and how to add, edit, merge or delete someone.
code: graph.py, crm.py, bounces.py, enrichment.py, dashboard.html
order: 2
---
Everyone you're in touch with, closest first, from your messages and meetings. Newsletters, receipts and other mailings don't add anyone until you write back. They are under Hidden senders, below the list: Show as a person brings one in. Filters, fields, tags and import work the same on all three lists: see [The Graph](graph.md).

## Someone's page

It starts with their photo, name, title, organization and place, and one line on how you're in touch ("Talk daily · last Fri, Oct 23 · next meeting Tue, Oct 27"). Below that:

- **Contact**: their phones and emails. Tap one to call or write, or **Copy** it.
- **With you**: what they are to you, Work or Personal contact, and your Family or Fleet, with **See in Fleet**.
- **Also on**: the other places you talk with them. **Slack** opens them in Slack, or your newest Slack thread with them.
- **People** and **Projects** they're part of, **Open between you** (promises both ways, with **Mark done** and **Drop**), and their **Timeline**.

Someone's addresses and chats are joined by themselves when it's clear they're one person, like a work email with their own address in CC.

If a page says **Couldn’t load this page.**, tap **Try again**. If it keeps saying so, use **Something's wrong?** at the bottom of the page.

## Summary

A few short lines at the top of a person's page: what was decided, asked, planned or promised, with everyone named. The Machine rewrites it when there's something new, only for people you're really in touch with, and checks each line first.

A vague line is left out; with nothing specific to say, there's no summary. Each line links to where it came from: messages from one day share one date with their count, and open together.

**Edit** it to say it your way. When there's news, The Machine shows a **Suggested update** with **Use it** and **Keep mine**. **Let The Machine write it** gives it back.

Meeting preps use it, only the lines from that to-do's side (Work or Personal). It stays on your Machine; your team never sees it.

## Timeline

Every person and organization page has one, newest first: email, meetings and their Zoom summaries, Intercom conversations (with **Open in Intercom**), WhatsApp, Telegram, Slack, LinkedIn and X chats, to-dos, promises and project moves. The chips on top show one source at a time. **Show more** loads older ones.

Meetings still to come sit on top under **Coming up**, soonest first; **Show all upcoming** shows the rest. A meeting shows who was on it, each person once. One with notes or a transcript says **Notes** or **Transcript**; click it to read them.

Your timelines are yours: the team's Graph shows only what your sharing rules allow.

## Work and Personal

The **Work** and **Personal** tabs list people by their Type, the one on their page. Your own pick (**Edit**) wins. Otherwise your Family and Friends, and family or friends to you (a wife, a father), are Personal, whatever address they write from. Your team never gets Personal contacts.

## Add someone

**New person** at the top of People, or **+** in the top bar on a phone. Give a name, and an email and organization if you have them. When someone like it is already in your Graph, the form shows them first, so you can open that one instead. **Add** opens the new page.

Someone you add stays, also with no messages yet. Their first message joins them.

## Edit someone

**Edit**, at the top of their page, changes their name, title, organization, location, LinkedIn, phones and emails, what they are to you, and Work or Personal. Its **Notes** field is for anything you want to remember; notes stay through merges. **Save** keeps it, **Cancel** leaves it as it was.

Your edits stay, also when their details are looked up again, and through **Merge** and **Undo**. Empty a field to use the looked-up value again. An empty name brings back the one from their messages.

To change their picture, click it: **Upload a picture**, pick one found for them, or **Remove picture**. It stays on your Machine.

## Merge two people

When two people might be one, their page asks if they are the same person, and People lists them under **Same person?**. **Merge** joins them, with all their messages, notes, roles and projects. **Not the same** keeps them apart for good. Your answer shows on the pair until you open People again, so you can tap through the list quickly.

**Merge all** merges every pair in the list at once, except the ones you marked **Not the same**. **Undo** right after splits them all again.

To join two people yourself, open one of them, then **⋯**, **Same person as…** and pick the other. A joined person's page lists why under **Joined from**, with **Undo** to split them again.

## Delete someone permanently

On their page, open the ⋯ menu and pick **Delete permanently…**, then **Delete**. It removes them and what your Machine knows about them: their entry, addresses, looked-up details, the messages only between the two of you, and notes about them.

To-dos that involve them stay, with their name taken out. They won't be added again. It can't be undone.

## Bounced

When an email to someone bounces, their address shows **Bounced** with the date, and another address of theirs comes first. New drafts never go to it when another address is known. If it's their only one, the send sheet warns you, and you can still send.

A bounce counts when the mail server says the address doesn't exist, or after 3 temporary failures over a week. It clears when they write from that address again, or when an email to it goes through.

## Job title and photo

People with a company address get a job title, photo, LinkedIn and city, looked up like [organization details](organization-data.md). Only their name and company domain are sent on a hosted Machine. Turn it off in **Settings**, under Security: **Look up work contacts**.

Your connections fill in more with what they already read: a title, phone and time zone from Slack, a bio and place from X, a headline and photo from LinkedIn, job titles from Google contacts and Salesflare. Hover over the line under their name to see where it came from.

WhatsApp and Telegram pictures come through your WhatsApp sync and your Telegram chats connection: up to 50 a day each, only for people already in your Graph. Nothing is sent to them. It all stays on your Machine.

## About you

Your own addresses and numbers, aliases too, are always you, never someone in your Graph. Searching for yourself, or adding a person with one of your addresses, opens **About you**, and an import skips your own row.

About you lists your addresses with where each came from; change them in **Settings**, under Account. To send your own contact to a teammate or friend, pick **Share my contact**. See [Share a contact](share-contact.md).

## Who's who

Roles your Machine read in your messages, waiting for your word. **✓ Right** confirms one; **Edit** opens their page in Edit. It learns from your edits. This shows only when roles are waiting.

## What it knows about someone

Under Known about, each fact has a menu:

- **Forget** deletes it everywhere.
- Not about them only takes it off that page.

## A to-do about someone

**New to-do** in the **⋯** menu of a person, organization or project starts a to-do about them.
