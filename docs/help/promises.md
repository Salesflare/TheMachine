---
title: Promises
area: cards
summary: What you said you'd do, and what others promised you. Kept track of by itself.
covers: promises
code: dashboard.html, assistant.py
order: 6
---
Keep track of what you promised and what others promised you. Your Machine spots promises in your messages by itself.

## Where they are

Under **Promises** on the To-dos page:

- What you said you'd do, and for whom: **You promised**.
- What others said they'd do: **Promised to you**.

Each one has a **⋯** menu:

- **Do it** on yours: it becomes a to-do now, and your Machine prepares it. **Nudge** on theirs: your Machine drafts a short follow-up where they promised it, while you stay on the list. A short note says it's on its way, with **Open to-do**, and the promise shows "a to-do now". Nothing is sent until you send it. One that is a to-do already opens that to-do.
- **Mark done**: it was kept.
- **Not happening**: it won't happen, so your Machine stops tracking it, with no to-do.

An open promise also becomes a to-do by itself around its date (yours the morning before, so there's a day to do it; theirs the morning after, if it's still open), and shows on its day in the [Calendar](calendar.md). One that is a to-do now links to it, and **Mark done** or **Not happening** closes that to-do too. When your Machine sees it done, both close, with a line saying so.

Already kept, like a reply you sent or a meeting that covered it? It closes by itself, with no to-do.

Given a new date later, like "next week instead"? The same promise moves, its to-do too, with no second one. Its page shows the new date and the newer message.

One without a date gets a **follow-up** day: three days after you made it, a week after they did. Still open by then? It becomes a to-do.

Promises from Slack show the person's name.

A promise by email from someone you've never written to is kept too, marked **unverified sender**: it's their word only. Its to-do starts with "Unverified: you haven't written to them before."

The [weekly recap](weekly-recap.md) counts kept and open ones. On your own computer, `assistant promises` lists them in a terminal.
