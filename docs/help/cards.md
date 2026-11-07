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

- **Ready for you**: prepared and waiting for your OK.
- **Needs your decision**: something only you can decide.
- **Preparing**: your Machine is working on it. After **Do it**, a to-do stays in place while it prepares, then moves to **Ready for you**.
- **Just done**: a last step you confirmed, like a form or an issue, went through while you were away. It stays until you tap **Got it**, for a day at most, and your phone hears of it too.
- **Coming back later**: snoozed to-dos, and ones with no answer to **Still needed?** (below).
- **Promises**: what you promised and what others promised you. See [Promises](promises.md).
- **Done / dismissed**: every finished to-do, newest first, with when it finished, like "Done 5 minutes ago". To-dos that seem finished already are marked **Looks done**.

After you send, a short note says where the to-do went, like "Sent. Moved to Done." or "Sent. Moved to Later until Mon." **Open** takes you to it. Search finds a to-do by its title or by who it went to, also in Later and Done.

In the open groups, to-dos that are overdue or due by tomorrow come first. The rest are newest first. The sidebar keeps the same order.

**Looks done** means your Machine sees it's done, like "PR #3451 merged", but it isn't closed yet. **Reopen** puts it back on your list, and your Machine learns from it. These never show as late. A to-do with a reply draft also looks done when you answered that conversation yourself, like in Gmail or Slack.

A to-do still waiting on someone else, like a review or a reply, says **Waiting on:** that step. It sits in **Waiting on others**, folded above Coming back later, until a new message brings it back.

A to-do nobody touched for a week asks once: **Still needed?** **Drop** closes it like **Not needed**, with **Undo**. **Keep** keeps it, and it never asks again. With no answer for another week, it folds into Coming back later. Opening it, a chat message, an edit, a snooze or a new message brings it back.

When nothing needs you, your Machine naps on an empty list. While it checks, it wakes up and says so. If a check failed or is late, its line says that, with **Check now** under it.

**All**, **Work** and **Personal** at the top of the sidebar list show all to-dos or only one kind. Your phone and computer show the same choice. While Work or Personal is on, **Show all** goes back.

A to-do on a project shows the project's name under its title. Tap it to open the project. **Project** under **Details** changes it or takes it off. See [a project's to-dos](projects.md#a-projects-to-dos).

**Area** under **Details** moves a to-do to your other area, like a personal one that has to go out from your work address. What it may read and send from moves with it. **Undo** on the note moves it back.

When a to-do needs your other area to go on and the messages it came from are all there, it moves there by itself and goes on. Otherwise it shows **Move to Work**, and nothing moves until you tap it. A to-do you added without picking Work or Personal moves by itself once it finds where it belongs.

A to-do can always read the messages it came from. When it needs other messages from your other area, it asks with **Use this email for this to-do**. Mail for another of your companies goes to that company's to-dos, and a to-do about your own life, like family writing to your work address, is Personal from the start.

## Check now

Your Machine reads each source every few minutes, day and night. It checks what came in once 40 messages wait or the oldest has waited 15 minutes.

**Check now** reads every source right away. With nothing open, tap your Machine's line to see it, with **Details**, which opens Checks under Connections. With to-dos open, it's at the top on a computer. A short line there shows only while a check runs, or when one failed or is late. You can also ask in chat.

LinkedIn, X and Salesflare keep their own pace.

## The buttons

A to-do shows its next step, like **Do it** or **Review and send**, with **Snooze** beside it. See [Do it](do-it.md) and [Snooze](snooze.md).

Before it's prepared, **Change how** says how to do it instead. Once a draft is ready, **Ask for changes** says what to change. **Mark done** means it's handled: in sight when there is no draft, otherwise at the top of **…**. It leaves the list at once, with **Undo** in the message.

To have it done another way, say so in its **Chat**.

Under **…**:

- **Hand off…**: give it to a teammate, [Claude Code or Codex](hand-to-agent.md), or [ask someone to review](ask-to-review.md).
- **Repeat…**: it [comes back on a rhythm](recurring.md).
- **Not needed**: it goes away. Optionally pick why: **Not relevant**, **Wrong facts** or **Already handled**. Your Machine learns from it.

Tap the title, or **Name** under **Details**, to rename it. Your title stays.

**Reopen** brings a closed to-do back. It also comes back by itself when something new happens, like a new message from them, but not for your own reply.

A to-do that only mattered until a set time, like a confirmation before a meeting, closes by itself after that time. It moves to **Done / dismissed** as "No longer needed". **Undo** brings it back for a day.

On your first to-dos, a short tip shows the key moves: **Change how** (or **Ask for changes**) and **Not needed**, and that nothing goes out until you press **Send**. A tip goes for good once you use its button or press ×.

On your first day, the top of To-dos greets you and names who has waited longest on your reply. That reply is drafted first, so it's ready when you arrive.

Each to-do starts with its title. The line under it says who it's about, their organization, the project, Work or Personal and when it came in. Tap a name to open their page in the Graph.

Sometimes a quiet line says what isn't known, like "Last contact 12 days ago by email; nothing since." It shows when the last word with them is old or unanswered, and names channels that aren't connected, like WhatsApp. Your Machine says what it doesn't know instead of guessing.

A title says what needs doing, and changes only when that does. A done to-do keeps its title, with how it ended under it, like "Done: Sam signed it on Tuesday".

Above the draft, one faint line names the message it came from, with that service's logo. Tap it to read the thread. The draft shows the logo of where it goes, so you see at once if it's a Slack reply or an email.

When the draft follows someone's input elsewhere, like a teammate's suggestion in Slack, a line says so, like "Based on Sam in #ops". Tap it to read that message.

A chat (Slack, WhatsApp, Telegram, Intercom…) reads as one conversation, oldest first: the messages before the one the to-do is about and the replies after it. That message has a thin line beside it and opens in view. **Show earlier** adds older messages. An email shows the rest of its thread folded above and below it.

**Details** shows its name, project and area (tap one to change it), your last note and a coding agent's result. **Chat ›** opens the chat. A done to-do stays short; the message it came from is under **Details**.

A "Waiting on" to-do links your last message to them, the one you're waiting on: "Email to Pat · Tue".

## Make one yourself

**New to-do** (under **Search** on a computer) adds a to-do for anything. Creating it sends nothing. Without Work or Personal picked, it goes where it belongs, by who and what it's about. It also finds the email it follows up on, even older mail.

- **Due**: type a day or time, like "tomorrow", "next Fri", "3 Nov", "2pm" or "in 2 hours", in your own language too. The calendar icon has quick picks and **Choose date**.
- **Email**: attach the email it's about. Search by subject or sender.
- **Files**: tap the paperclip, paste a screenshot or drop files on the form. On a phone you can take a photo. Up to 5 files, like in the chat (see [Add files](card-chat.md#add-files)). × takes one back.

The files stay with the to-do, and The Machine reads them when it works on it. Files alone are enough: it fills in the to-do from a PDF or text file.
