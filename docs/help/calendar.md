---
title: Calendar
area: calendar
summary: The week ahead in one place: meetings, to-dos that are due, snoozed to-dos and promises.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py
order: 1
---
## What it shows

The next 7 days, with:

- meetings from the calendars you connected,
- to-dos due that day, and snoozed to-dos on the day they come back,
- check-ins on work you handed off,
- promises with a date.

A meeting on two calendars shows once. A calendar someone shared with you shows their events muted, with their first name; those never make a to-do. All-day and multi-day events show as all day, on each day they cover.

A plan made together is one promise, marked "With" and their name. A promise about a meeting that day with the same person sits on that meeting's row.

**Overdue** comes first. A meeting with an open to-do shows it: **Prep ready**, **Preparing** or **To-do**.

## Agenda or week

**Agenda** lists each day. On a computer, **Week** shows a grid. Your choice is remembered on that device.

In the grid, events at the same time sit side by side while each stays readable. The rest show as **+N**, which opens that day in the agenda.

## Open something

Click a row to open its to-do's chat, the promise, or the meeting. A meeting you can't change here, like someone else's or one with guests, shows its details: when, where and who. Someone your Graph knows, and the organizations and projects the meeting is on, are links to their page. **Open in Google Calendar** (or **Open in Outlook**) under them opens it there. Looking changes nothing.

A meeting room booked on a meeting shows under where, never as a person or in your Graph.

## Meeting notes and transcript

A meeting's details have two parts. **Notes** is the summary: decisions and action items. **Transcript** is what was said, word for word. It starts folded, with how long it runs; **Show** opens it.

Each has its own **Add notes** or **Add transcript**, **Upload file** for a Markdown or text file, **Edit** and **Remove** (tap twice). What goes in one stays there. On a meeting you can change, **Notes** under its form opens them.

With [Zoom](zoom.md) or [Google Meet](google-meet.md) connected, its notes show in Notes and its transcript in Transcript, marked **From Zoom** or **From Google Meet**. They never replace what you added: when both are there, both show.

A meeting with a transcript and no notes has **Generate notes**. The Machine writes them from the transcript: a short summary, decisions, and action items with who does them, in the meeting's language.

The Machine shows **Writing notes…** and keeps going when you close the meeting; a long one takes a few minutes. It uses your own model and waits if you reach your usage limit. The notes say **Written by The Machine**, never replace notes you added, and follow-ups come from them like from Zoom's.

The Machine can add them too. Ask on a to-do, like "add this transcript to today's board meeting". A transcript goes in Transcript, a summary in Notes. A meeting with them says **Notes** or **Transcript** in the Calendar.

The Machine reads both for the meeting's follow-ups. They are Work or Personal like the meeting, and go to your team only when the meeting does.

## Add or change an event

When a calendar can be changed from here, **New event** adds one (on a phone it's under **+** in the top bar): pick the calendar, a title and the time. Click an event without guests on that calendar to change it, or **Delete** it (tap twice).

**Where** suggests places as you type: ones you used before and your organizations first, then addresses from [OpenStreetMap](https://www.openstreetmap.org) through Photon, a free map search. Your Machine asks it, with only the words you typed. Pick one or keep your own text.

**Invite** adds people from your Graph, or any email address. It's there on your own calendar only. Who gets an invite is listed above the button, and the button says how many: **Add and invite 2**. Google sends the invitations when you tap it, not before. Without guests nobody is invited or gets an update.

A to-do can offer a change too, like a pick-up to add. It shows exactly what changes, and only your **Add**, **Save** or **Delete** makes it.

No meetings yet? Without a calendar, **Connect your calendar** opens Connections: connect [Google Calendar](google-calendar.md) or [Outlook Calendar](microsoft.md).
