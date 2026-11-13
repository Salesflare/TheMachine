---
title: Calendar
area: calendar
summary: The week ahead in one place: meetings, to-dos that are due, snoozed to-dos and promises.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
---
## What it shows

Your days from today on, with:

- meetings from the calendars you connected,
- to-dos due that day, and snoozed to-dos on the day they come back,
- check-ins on work you handed off,
- promises with a date.

A meeting on two calendars shows once. A calendar someone shared with you shows their events muted, with their first name; those never make a to-do. All-day and multi-day events show as all day, on each day they cover.

A plan made together is one promise, marked "With" and their name. A promise about a meeting that day with the same person sits on that meeting's row.

**Overdue** comes first. A meeting with an open to-do shows it: **Prep ready**, **Preparing** or **To-do**. A to-do that looks done (you already answered, or its run found it done) is not shown as **Due**.

## Agenda, week or month

- **Agenda** lists each day. Scroll down for later days, or up (or **Show earlier days**) for earlier ones. It goes back to a week before you connected your calendar, and a line at the top says from which day. Once its [history](history.md) is in, it goes back about a year.
- **Week** shows a grid, Monday to Sunday. On a phone it shows three days.
- **Month** shows the whole month. A computer shows up to three items a day; a phone shows dots, and a tap lists that day.

**Today**, ‹ and › at the top move through the weeks or months. The view you pick is remembered on that device.

In the week grid, events at the same time sit side by side while each stays readable. The rest show as **+N**, which opens that day in the agenda.

## Open something

Click a row to open its to-do's chat, the promise, or the meeting. A meeting you can't change here, like someone else's or one with guests, shows its details: when, where and who. Someone your Graph knows, and the organizations and projects the meeting is on, are links to their page. **Open in Google Calendar** (or **Open in Outlook**) under them opens it there. Looking changes nothing.

A meeting room booked on a meeting shows under where, never as a person or in your Graph.

A meeting link shows as its service, like Zoom, Google Meet or Teams, or as **Video call**. Open the meeting to join.

## Meeting notes and transcript

A meeting's details have two parts. **Notes** is the summary: decisions and action items. **Transcript** is what was said, word for word. It starts folded, with how long it runs; **Show** opens it.

If they don't load, it tries again by itself for about half a minute. After that, tap **Try again**.

Each has its own **Add notes** or **Add transcript**, **Upload file** for a Markdown or text file, **Edit** and **Remove** (tap twice). What goes in one stays there. On a meeting you can change, **Notes** under its form opens them.

With [Zoom](zoom.md) or [Google Meet](google-meet.md) connected, its notes show in Notes and its transcript in Transcript, marked **From Zoom** or **From Google Meet**. They never replace what you added: when both are there, both show.

Notes can also come in the meeting's own calendar event, added after it started, or by mail from Zoom or Gemini. After the meeting ends, The Machine makes to-dos from them only for clear next steps. The same notes coming two ways make one to-do, with the meeting as its source: **Notes from** the meeting.

A meeting with a transcript and no notes has **Generate notes**. The Machine writes them from the transcript: a short summary, decisions, and action items with who does them, in the meeting's language.

It shows **Writing notes…** and keeps going when you close the meeting. A long one takes a few minutes, using your own model. The notes say **Written by The Machine** and never replace notes you added.

The Machine can add them too. Ask on a to-do, like "add this transcript to today's board meeting". A transcript goes in Transcript, a summary in Notes. A meeting with them says **Notes** or **Transcript** in the Calendar.

The Machine reads both for the meeting's follow-ups. They are Work or Personal like the meeting, and go to your team only when the meeting does.

A meeting opens with these details wherever you find it: on a timeline, in a message search or as a to-do's source. **Original invite** at the bottom shows the invite as it came in.

## Add or change an event

When a calendar can be changed from here, **New event** adds one (on a phone it's under **+** in the top bar): pick the calendar, a title and the time. Click an event without guests on that calendar to change it, or **Delete** it (tap twice).

**Where** suggests places as you type: ones you used before and your organizations first, then addresses from [OpenStreetMap](https://www.openstreetmap.org), a free map. Only the words you type are sent to look them up. Pick one or keep your own text.

**Invite** adds people from your Graph, or any email address. It's there on your own calendar only. Who gets an invite is listed above the button, and the button says how many: **Add and invite 2**. Google sends the invitations when you tap it, not before. Without guests nobody is invited or gets an update.

A to-do can offer a change too, like a pick-up to add. It shows exactly what changes, and only your **Add**, **Save** or **Delete** makes it.

No meetings yet? Without a calendar, **Connect your calendar** opens Connections: connect [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) or [another calendar](other-calendars.md).

## Clashes with your other calendar

When a work meeting overlaps something in your personal calendar, or the other way around, The Machine makes one to-do about the newer of the two. It can draft a short note to move it, or offer to decline. Nothing goes out until you approve it.

All-day, free and tentative events never count, and each clash comes up once. A Work to-do only says there is a conflict, so your team never sees the personal event. Only you see what it clashes with.

## Ready for your meetings

Before a meeting with people from outside your company, The Machine makes one to-do: **Prepare for** the meeting. It's a short briefing:

- **Who:** who they are, from your Graph.
- **Last contact:** your last exchange with them. That message is the to-do's source, after the meeting.
- **Open promises:** what you or they still owe.
- **Open questions:** what is still unanswered.
- **Decide or bring:** what to settle or bring along.

It comes on the morning of a work day: the meeting's own day when it's in the afternoon, else the work day before. It only uses what is already on your Machine. It is only for reading: **Done** when you have read it. A promise or question in it that needs doing has its own to-do.

No useful history means no to-do. Recurring, internal, personal and declined meetings get none. A meeting that moves keeps its one to-do, at the new time. A dismissed one doesn't come back, and a canceled meeting's closes by itself.

The meeting's details show its to-do under **To-do**, one tap from its chat.
