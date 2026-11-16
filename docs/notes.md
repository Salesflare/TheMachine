# Notes (off by default)

Notes are one readable wiki page per subject of your life or work, written by your Machine from your messages. The
feature is off on every Machine unless `notes_enabled` is set, and Help does not show it. This page is for a Machine
that has it on.

## Turn it on or off

Add the top-level key to `config.json` and restart the service (see [configuration](configuration.md)):

```json
"notes_enabled": true
```

Off (the default, or `false`):

- no Notes in the Graph, the sidebar, the command palette, search or a record's **Linked from**;
- no notes model calls: sorting conversations, writing pages, folder overviews and reading OpenClaw memory pages don't run;
- the notes already kept stay in the database untouched, so turning it on again brings them back;
- trips and events from booking and ticket mail still come in, show as bands in Calendar and open their page there
  ([Calendar help](help/calendar.md#trips-and-events)).

The first round with it on starts the notes from conversations over (`topic_notes.rebuild`, once): every
conversation is sorted again, and the notes made from conversations and the Home, Health and Kids notes made before go
to an **Earlier notes** folder, readable as they were (`note_pages.archive`). Nothing is deleted. A note you renamed,
moved, wrote in or keep your own notes under stays where it is. Your own notes, trips, events and the notes from your
OpenClaw memory pages stay as they are.

To roll back: set it to `false` (or remove it) and restart. The notes stay where they are, unseen. The archived notes
are kind `archived` with key `archived:<old key>` in `note_pages`.

## What a note is

A subject that keeps mattering: one child's school or class, a club, a trip, the house or a renovation, the car, a
hire, a customer or project. Not a category on its own ("bills"), small talk or marketing. One order, delivery,
receipt, booking or account is never a note of its own: it is a source of its trip, project or shop. At work a note is a
whole customer, partner or project, not one thread or deal. Titles never carry order, account or booking numbers.
A vendor or service you use (cloud, software, a subscription, a provider) is no note when all it sends is billing and
notices; a work note starts once you write with someone there. A person is never a note: their page in the Graph has
them.

Notes about the same thing become one: the same trip from a booking and from mail (same place, same dates, or without
dates the same place with mail from the same weeks), or several
threads with one customer. A note you renamed or wrote in is never merged away.

## Where it reads from

Every conversation from your mailboxes, chats and meeting notes, and the notifications that hold a subject's facts: a
school's or a club's mail, bookings, appointments, invoices and delivery notices. Spam, Gmail's Promotions, Social and
Forums tabs, automatic replies, bounces and bot chats are left out before any AI call. At most 15 mails from one
notification sender go to the AI at once, the newest.

One AI call sorts up to 40 conversations into subjects. A health subject goes only under Health and stays Personal;
someone else's health, a family conflict, money trouble or anything intimate makes no note. When unsure, no note.

## The page

The page writer reads every source of a subject in full and writes one page: a short summary of where it stands, who
is in it, the key facts and dates (term dates, trip times, what to bring, amounts), decisions, open items and a
timeline. The newest source wins, so a changed time replaces the old one. A trip gets a page too, from its bookings and
the mail about it.

The busiest subjects get their page first, the ones with the most and most recent sources. The rest wait for a new
message about them, so a first build stays cheap.

Each source is checked first. One that isn't about the subject, like a notice about another child, leaves the note and
is sorted once more, so it goes to its own subject.

Quality or nothing: every sentence cites its sources, and a page needs a summary and at least three facts, decisions
or open items. A subject without a page isn't in the Notes list until you rename it or write in it.

How it works inside: [intelligence](intelligence.md#notes-from-conversations).
