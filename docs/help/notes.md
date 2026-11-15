---
title: Notes
area: graph
summary: One readable page per subject, like a trip or your home, linked to the people and projects in it.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
---
A note is the overview of one subject: a trip, your home, how invoices are done. Notes sit in the Graph next to People, Organizations and Projects. They stay on your Machine and aren't shared with your team.

## Start a note

**New note** at the top of Notes. Give it a title and **Start the note**, and its page opens. **Add a line** adds what you want to keep. Each line of text becomes its own line.

## Link to people, projects and other notes

Type @ and a few letters of a name in a line. Pick a person, organization, project or note from the list, and its name goes in as a link. The page of whatever you linked shows **Linked from** with your note.

## Notes under notes

A note can sit under another, like Appliances under Home. Notes shows them as a tree: the arrow beside a note opens the ones under it. To move a note, **Edit** and pick where it goes under **Under**. **New note under this one** in the ⋯ menu starts one right there.

## Notes your Machine keeps

Your Machine also writes notes by itself, from your messages, and keeps them current. Each of its lines says where it came from, like who sent the email: tap it to open the message. A line from **What I've learned** says **From what I learned**.

Your changes always stand. Rename a note, move it, change its dates or a line, and your Machine keeps it that way when it updates the note. Delete a line or a note and it doesn't come back. Later notes on the same subject go where you put the first one.

**Back to the original** shows your Machine's own words again. Editing a line that came from what your Machine learned also changes it under **What I've learned**, so there's one version of it.

## Trips

When a flight, hotel, train, bus, ferry or rental car booking reaches your mail, your Machine adds it to a trip under **Trips**. Bookings for one journey go on one trip: the way out, the hotel and the way back. The trip has the booking code, seat and ticket for each line, in time order, and it shows its dates. In [Calendar](calendar.md) it shows as one band across those days, and opens the trip.

It reads the booking details that airlines, hotels and booking sites put in their confirmation mail. A mail without them doesn't make a trip. A changed booking updates its line, and a canceled one goes. When every booking of a trip is canceled, the trip goes too.

## Home

Under **Home**, your Machine keeps what it knows about your home: **Bills and subscriptions**, **Appliances**, **Repairs and upkeep** and **The house**. A part shows up once it has at least two lines.

- A bill that comes regularly, like energy or water, gets a line with how often it comes and the day of the last one. **Open the to-do** shows the bill itself; the amount and payment details stay there.
- A subscription you kept gets a line that opens its **Subscriptions** to-do. One you canceled isn't listed.
- What your Machine learned about your home, like the make of your dishwasher, is a line too. Editing it also changes it under **What I've learned**.
- If you keep your own note in a part, like one for your dishwasher under **Appliances**, what's about that thing goes in your note instead. Your Machine doesn't start notes like that itself.

Only Personal bills and subscriptions are used, and Home notes are always Personal. Your Machine asks its AI once about each new bill, subscription or thing it learned, to tell whether it's about your home. For a bill it sends who it's from, never the amount.

## Health

Under **Health**, your Machine keeps what it knows about your own health: **Appointments**, **Doctors and care**, **Medicines**, **Allergies and conditions** and **Bills and insurance**. A part shows up once it has at least two lines.

- An appointment in your calendar that only you go to, like the dentist, gets a line with its next date, or its last one. **From your calendar** opens it.
- A bill from a doctor, dentist or pharmacy gets a line that opens its to-do. The amount stays there.
- What your Machine learned about your health, like an allergy, is a line too. Editing it also changes it under **What I've learned**.
- Your own note in a part, like one for your physio under **Appointments**, gets what's about that thing.

Health notes are always Personal, even when a bill came in on your work address. Your Machine asks its AI once about each new appointment, bill or thing it learned, to tell whether it's about your own health. It sends an appointment's name, never its notes or who else is invited.

## Kids

Under **Kids**, your Machine keeps what it knows about your children: **School**, **Activities**, **Doctors and care** and **Bills and fees**. A part shows up once it has at least two lines.

- What your Machine learned about your child, like their class teacher or swimming day, is a line that links to their page. It counts someone as your child when their **To you** says so, like daughter or son.
- An event in your calendar that only you go to, like a parents' evening, gets a line with its next date, or its last one. **From your calendar** opens it.
- A bill for school, a club or childcare gets a line that opens its to-do. The amount stays there.
- Your own note for one child in a part, like one for Jules under **School**, gets what's about that child.

Kids notes are always Personal, even when the school writes to your work address. Your Machine asks its AI once about each new thing, to tell whether it's about your children.

## Merge, delete and undo

**Merge into…** in the ⋯ menu moves a note's lines and the notes under it into another note. Your Machine adds to that note from then on. **Delete** removes a note. Both show **Undo** for a moment, and so does removing a line.

## Not the same as meeting notes

Meeting notes and the notes on a person or organization stay where they were. Notes here are pages of their own.
