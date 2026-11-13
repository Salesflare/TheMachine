---
title: Handoffs
area: fleet
summary: Hand a to-do to a teammate's Machine, with what they need. Check in later, or take it back.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
---
## Hand off a to-do

1. On the to-do, open **…**, then **Hand off…**, and pick **A teammate**.
2. Choose who, check what goes along (× leaves a part out), and add a note. Nothing from a Personal account or another company goes along.
3. Send it. Their Machine shows it to them as a to-do.

Their Machine pings them on their phone or in Telegram. With neither set up, it emails them once with who handed it, its title and a link. See [Notifications](notifications.md).

An Intercom conversation goes along too. If their Machine reads the same Intercom workspace, **Read message** opens it and their reply goes back in Intercom. If not, their to-do links to it.

While you wait, the to-do says what you asked and when ("Asked Pat on Tue 3 Nov: …"), only when that adds something to its title. It sits under **Coming back later**, "With Pat · waiting", with a check-in date. **Check in now** drafts a short nudge to Pat for you to send; **Change time** moves the check-in.

If Pat's Machine can't notify them, the to-do says "Pat won't get a ping. Let them know." Tell Pat yourself. The line goes once they turn on notifications.

It comes back on top only when there is something to decide: Pat answered, declined or finished it, the handoff failed, or a deadline came. The check-in follows the due date: a few hours for today, the work day before for soon, the next morning for urgent, otherwise 3 work days.

Back for a check-in, it says "Still with Pat". **Check in now** drafts a short nudge to Pat where you asked (Slack, WhatsApp, Telegram or email), on the to-do. Nothing goes until you pick **Send**; then it waits on Pat again. If nothing you connected can message Pat, the chat opens and says so. **Take it back** and **Hand off to someone else** are under **…**, then **Hand off…**.

The to-do's chat shows when it went ("Handed off to Pat's Machine · 14:02") and what came back: accepted, declined (with their note) or done. With no answer yet, it offers **Mark done**, **Snooze** and **Not needed**. To nudge them or take it back, say so in the chat.

If the handoff didn't go out, the to-do and its chat say so, with **Try again**.

## Hand it to someone else instead

While a teammate has it, the to-do says so in one line ("With Pat · waiting"), with **Take it back** and **Hand off to someone else** under **…**, then **Hand off…**. **Take it back** makes it yours again: Pat's Machine is told, and their answer no longer moves it.

**Hand off to someone else** opens the handoff form. Or say so in the to-do's chat ("this should go to Kim"): the to-do then says "Still with Pat until you send it to Kim", with **Review handoff to** Kim.

A to-do goes to each teammate once: while Pat has it, picking Pat again in the handoff form is a check-in. **Check in** drafts the same nudge, with a line of yours if you add one.

**Take it back from** Pat is on by default; turn it off to let both have it. Nothing goes out until you pick **Hand off**. Pat's Machine is told, and their copy of the to-do goes.

## When they decline

They can say why: not theirs, already done, or no time this week. Then pick **Do it myself**, **Hand off to someone else** or **Mark done**. The same goes when they don't answer in time. **Do it myself** makes it your own to-do again, under For you.

## Someone outside the Network

Pick **By email**: your Machine drafts an email for you to send. As you type, it suggests your Fleet first, then people at your company. Add a task page so they can answer in one tap: see [Task pages](task-pages.md).

Only for Work to-dos. Tick what goes in: a few lines about the to-do, its draft, links and files. Personal and Only you content stays out. **Prepare email** puts the email on the to-do: read it, then send it from your own mailbox. No tracking.

A to-do from Intercom or Slack has no mailbox of its own, so its email goes from your Work mailbox.

The to-do then tracks it as a promise until they reply that it's done, or you mark it done. The email ends with "Take this on in your own Machine": if they sign up through it, they can join your Fleet and the to-do moves to their Machine. Turn that line off in **Settings**, under Fleet.
