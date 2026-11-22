---
title: Promises
area: cards
summary: What you said you'd do, and what others promised you. Kept track of by itself.
covers: promises
code: dashboard.html, assistant.py, refunds.py
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

A reply that only promises the work, like "I'll send the files by Tuesday", doesn't finish its to-do. The to-do stays open with that date, and the promise links to it. The send review says so before you send.

Already kept, like a reply you sent or a meeting that covered it? It closes by itself, with no to-do.

Given a new date later, like "next week instead"? The same promise moves, its to-do too, with no second one. Its page shows the new date and the newer message.

One without a date gets a **follow-up** day: three days after you made it, a week after they did. Still open by then? It becomes a to-do.

Promises from Slack show the person's name.

A promise by email from someone you've never written to is kept too, marked **unverified sender**: it's their word only. Its to-do starts with "Unverified: you haven't written to them before."

## Refunds

When a shop, airline, landlord or insurer promises you money back, like a refund for a canceled order or an approved claim, your Machine keeps the amount, who pays it and the day it should be in. It shows under **Promised to you**. Only when the message makes all three clear.

When the money comes back first, like a "refund processed" email, a payment service's notice or your bank app's notification on your phone, it closes by itself, with no to-do.

Not in by that day? One quiet to-do comes: "Chase the €42 refund from …", with a short email to them that names the order or case number. Nothing is sent until you send it. If the money comes in after all, the to-do closes by itself. **Undo** brings it back for a day.

The [weekly recap](weekly-recap.md) counts kept and open ones. On your own computer, `assistant promises` lists them in a terminal.
