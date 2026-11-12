---
title: To-dos
area: cards
summary: One to-do per thing that needs you, ready for your yes. What the parts of a to-do mean.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Your Machine reads everything new and makes a to-do only when something needs you. One to-do per matter, however many messages it spans.

## Where to-dos sit

The **To-dos** page groups them:

- **For you**: everything waiting on you, most urgent first. Each says **Prepared** (the work is done, and **Do it** or **Send** carries it out) **Needs you** (it needs your decision or an answer first) or **Preparing…** (your Machine is working on it).
- **Just done**: a last step you confirmed, like a form or an issue, went through while you were away. It stays until you tap **Got it**, for a day at most, and your phone hears of it too.
- **Coming back later**: snoozed to-dos, and ones with no answer to **Still needed?** (below).
- **Promises**: what you promised and what others promised you. See [Promises](promises.md).
- **Done / dismissed**: every finished to-do, newest first, with when it finished, like "Done 5 minutes ago". To-dos that seem finished already are marked **Looks done**.

After you send, a short note says where the to-do went, like "Sent. Moved to Done." or "Sent. Moved to Later until Mon." **Open** takes you to it. Search finds a to-do by its title or by who it went to, also in Later and Done.

**For you** puts first what's overdue or due by tomorrow, then questions from your Fleet, then the rest. Within each, newest first. A to-do keeps its place while your Machine prepares it and when it's done: only its mark changes. The other open groups put overdue or due by tomorrow first, the rest newest first. The sidebar keeps the same order.

**Looks done** means your Machine sees it's done, like "PR #3451 merged", but it isn't closed yet. **Reopen** puts it back on your list, and your Machine learns from it. These never show as late. After a day, it closes by itself, with **Undo**. A to-do you already handled yourself, like with a reply in Gmail or Slack, closes by itself too.

A to-do still waiting on someone else, like a review or a reply, says **Waiting on:** that step. It sits in **Waiting on others**, folded above Coming back later, until a new message brings it back. The same goes after you asked a question back: it returns the morning before its deadline, at the deadline when that is later today, or the next morning once it has passed, and says whom it is still waiting on.

When a to-do is for a result someone else delivers, like a signed contract, **Details** shows it as **Done when**. Sending your part doesn't close it: it waits in **Waiting on others** until a message shows the result, then closes by itself, with **Undo**. If nothing comes by the time to chase them, it comes back with **Write a short nudge** in its chat. Tell it in the chat what counts as done to change it.

A to-do nobody touched for a week asks once: **Still needed?** **Not needed** closes it, with **Undo**. **Keep** keeps it, and it never asks again. With no answer for another week, it folds into Coming back later, and the number on the app icon and the morning digest stop counting it. Opening it, a chat message, an edit, a snooze or a new message brings it back.

When nothing needs you, your Machine naps on an empty list. While it checks, it wakes up and says so. If a check failed or is late, its line says that, with **Check now** under it.

**All**, **Work** and **Personal** at the top of the sidebar list show all to-dos or only one kind. Your phone and computer show the same choice. While Work or Personal is on, **Show all** goes back. An alert about your Machine itself, like a part that keeps restarting, is neither Work nor Personal and shows under All only.

A to-do on a project shows the project's name under its title. Tap it to open the project. **Project** under **Details** changes it or takes it off. See [a project's to-dos](projects.md#a-projects-to-dos).

**Area** under **Details** moves a to-do to your other area. What it may read and send from moves with it. **Undo** on the note moves it back.

When a to-do needs your other area to go on and the messages it came from are all there, it moves there by itself and goes on. Otherwise it shows **Move to Work**, and nothing moves until you tap it. A to-do you added without picking Work or Personal moves by itself once it finds where it belongs.

A to-do can always read the messages it came from. When it needs other messages from your other area, it asks with **Use this email for this to-do**. A work mailbox you labeled Personal counts as Personal. Mail for another of your companies goes to that company's to-dos, and a to-do about your own life, like family writing to your work address, is Personal from the start. Work that reaches you on a personal account, like a client on WhatsApp or an order in your personal mailbox, is Work from the start. A to-do you moved or placed yourself always stays where you put it.

Such a Personal to-do still replies from the work address its email came in on, and it never shows up in a Work Fleet or the Team Graph.

With two or more waiting, **Go through** in the header of For you steps through them one at a time, in the list's order, each draft in full, with **Send** or **Do it**, **Ask for changes**, **Snooze** and **Skip**. On a computer, Enter sends what's on screen, `S` snoozes, `→` skips and Esc stops. Under the title, the header also says how long they take at your own pace, like "about 2 min".

A to-do that asks you something is left out of both: it takes your answer, not a tap.

## Check now

Your Machine reads each source every few minutes, day and night. It checks what came in once 40 messages wait or the oldest message from a person has waited 15 minutes. Newsletters, notifications and receipts join the next check, within the hour.

**Check now** reads every source right away. With nothing open, tap your Machine's line to see it, with **Details**, which opens Checks under Connections. With to-dos open, it's at the top on a computer. A short line there shows only while a check runs, or when one failed or is late. You can also ask in chat.

LinkedIn, X and Salesflare keep their own pace.

## Last check

After a check that read new messages, a line above your to-dos says what it found, from every source it read, like "Checked 13 messages at 16:11 · nothing needs you" or "· 2 new to-dos". When a new to-do waits for a better moment, like your morning summary, it says until when: "1 to-do held until tomorrow 08:30".

Tap the line to see each email thread, chat and notification, with its source's icon: who wrote, the subject or first words, and its new to-do or why it needed nothing, like "Only cc'd, a teammate is answering" or "Meeting already set for Thursday". A thread shows no reason when the check gave only a vague one. Tap one to read it.

The first 10 show, and a tap below them shows the rest. A number after a name, like (3), is how many new messages that chat has. A phone notification about a message that's already listed shows only once. The line shows for 12 hours after the check.

It counts only mail to you. Your own replies are read for context and promises, but aren't new mail. The Machine's own emails to you, like your morning summary or a fix notice, are never read or listed. Mail about billing, your trial or an invite is read as usual.

## The buttons

A to-do shows its next step, like **Do it** or **Review and send**, with **Snooze** beside it. See [Do it](do-it.md) and [Snooze](snooze.md).

**Ask for changes** says what to change: how to do it, or, once a draft is ready, what to change in it. **Mark done** means it's handled: in sight on a ready one without a draft, otherwise at the top of **…**, also on one that needs your decision. It leaves the list at once, with **Undo** in the message. Swipe the message away, or drag it off with the mouse, to close it sooner. The change stays.

To have it done another way, say so in its **Chat**.

Under **…**:

- **Hand off…**: give it to a teammate, [Claude Code or Codex](hand-to-agent.md), or [ask someone to review](ask-to-review.md).
- **Repeat…**: it [comes back on a rhythm](recurring.md).
- **Not needed**: it goes away. Optionally pick why: **Not relevant**, **Wrong facts** or **Already handled**. Your Machine learns from it.

Tap the title, or **Name** under **Details**, to rename it. Your title stays.

**Reopen** brings a closed to-do back. It also comes back by itself when something new happens, like a new message from them, but not for your own reply.

A bill you still have to pay yourself, from any country, becomes a to-do with the amount, the due date and the payment details the bill gives. Bills paid automatically, like a direct debit or a card on file, don't. When a later email shows it paid, like the sender confirming your payment came in, the to-do closes by itself. **Undo** brings it back for a day.

A to-do that only mattered until a set time, like a confirmation before a meeting, closes by itself after that time. It moves to **Done / dismissed** as "No longer needed". **Undo** brings it back for a day.

Before a message or handoff for someone shows as ready, your Machine checks your recent chats with the people in it, group chats too, and waits for Slack to read them. When a later message shows it is done already, like they were asked and said yes, the to-do closes by itself. **Undo** brings it back for a day.

When a newer message changes the plan, like a party moved to another venue or a booking dropped, The Machine updates its to-dos itself. One that still matters follows the new plan. One with nothing left to do moves to **Done / dismissed** as "Not needed", its chat says "Updated:" and why, and **Undo** brings it back for a day.

On your first to-dos, a short tip shows the key moves: **Ask for changes** and **Not needed**, and that nothing goes out until you press **Send**. A tip goes for good once you use its button or press ×.

On your first day, the top of To-dos greets you and names who has waited longest on your reply. That reply is drafted first, so it's ready when you arrive.

Each to-do starts with its title. The line under it says who it's about, the organization when it's about one (never just because someone works there), the project, Work or Personal and when it came in. Tap a name to open their page in the Graph. A name and an organization show their photo or logo when the Graph has one.

Sometimes a quiet line says what isn't known, like "Last contact 12 days ago by email; nothing since." It shows when the last word with them is old or unanswered, and names channels that aren't connected, like WhatsApp. Your Machine says what it doesn't know instead of guessing.

When it names a channel that isn't connected, Connect next to it opens that connection.

A title says what needs doing, and changes only when that does. A done to-do keeps its title, with how it ended under it, like "Done: Sam signed it on Tuesday".

Above the draft, one faint line names the message it came from, with that service's logo. Tap it to read the thread. The draft shows the logo of where it goes, so you see at once if it's a Slack reply or an email.

When the draft follows someone's input elsewhere, like a teammate's suggestion in Slack, a line says so, like "Based on Sam in #ops". Tap it to read that message.

A chat (Slack, WhatsApp, Telegram, Intercom…) reads as one conversation, oldest first: the messages before the one the to-do is about and the replies after it. That message has a thin line beside it and opens in view. **Show earlier** adds older messages. An email shows the rest of its thread folded above and below it.

**Details** shows its name, project and area (tap one to change it), your last note and a coding agent's result. **Chat ›** opens the chat. A done to-do stays short; the message it came from is under **Details**.

A "Waiting on" to-do links your last message to them, the one you're waiting on: "Email to Pat · Tue".

## Make one yourself

**New to-do** (under **Search** on a computer) adds a to-do for anything. Creating it sends nothing. Without Work or Personal picked, it goes where it belongs, by who and what it's about. It also finds the email it follows up on, even older mail.

- **Due**: type a day or time, like "tomorrow", "next Fri", "3 Nov", "2pm" or "in 2 hours", in your own language too. The calendar icon has quick picks and **Choose date**.
- **Message**: attach the message it's about: an email, Slack, Teams, WhatsApp, Telegram or any other message The Machine has. Search by text or sender. Each result shows where it's from, who sent it and when.
- **Files**: tap the paperclip, paste a screenshot or drop files on the form. On a phone you can take a photo. Up to 5 files, like in the chat (see [Add files](card-chat.md#add-files)). × takes one back.

The files stay with the to-do, and The Machine reads them when it works on it. Files alone are enough: it fills in the to-do from a PDF or text file.
