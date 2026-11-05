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

- **Ready for you**: prepared and waiting for your approval.
- **Needs your decision**: something only you can decide.
- **Preparing**: your Machine is working on it. A to-do you just said **Do it** to stays where it was while it prepares, then moves to **Ready for you**.
- **Just done**: a last step you confirmed, like submitting a form or filing an issue, went through while you were away. It shows what happened until you tap **Got it**, for a day at most, and your phone hears of it too. Then it's only in Done.
- **Coming back later**: snoozed.
- **Promises**: what you promised and what others promised you. See [Promises](promises.md).
- **Done / dismissed**: every finished to-do, by when it was finished, newest first, 30 at a time as you scroll. A to-do you just sent is at the top, and each one says when, like "Done 5 minutes ago". To-dos that seem finished already sit among them by when they started to, marked **Looks done**.

After you send, a short note says where the to-do went, like "Sent. Moved to Done." or, when it waits for a reply, "Sent. Moved to Later until Mon." **Open** takes you to it. The email thread leaving your inbox for a few days is only about your mailbox. Search finds a to-do by its title or by who it went to, also in Later and Done.

In Ready for you, Needs your decision, Preparing and Waiting on others, a to-do that's overdue or due by tomorrow comes first. The rest are newest first, by the time each to-do shows. The sidebar keeps the same order.

A to-do marked **Looks done** shows like a done one, with what shows it's done, like "PR #3451 merged". It isn't closed yet: **Reopen** puts it back on your list, and your Machine learns from it. These never show as late and don't count as waiting for you.

A to-do whose last step is still open on someone else's side, like a review, a merge or a reply, says **Waiting on:** that step and stays open. It waits in **Waiting on others**, folded above Coming back later, and doesn't count as ready for you. A new message on it brings it back.

**All clear.** means nothing needs you now. The line under it says when your Machine last looked.

**All**, **Work** and **Personal** above the list in the sidebar show all to-dos or only one kind. Your Machine keeps the choice, so your phone and computer show the same list. While Work or Personal is on, the top of the list says so, with **Show all** to go back.

A to-do on a project shows the project's name in the line under its title; it opens the project. **Project** under **Details** changes it or takes it off. See [a project's to-dos](graph.md#a-projects-to-dos).

**Area** under **Details** moves the to-do to your other area, like a personal one that has to go out from your work address. What it may read and send from follows the move; the messages it came from stay where they are. **Undo** on the note that follows moves it back.

When a to-do needs another area to go on, it asks with a **Move to Work** button. Nothing moves until you tap it; then it carries on by itself. A to-do you added without picking Work or Personal moves by itself once it finds where it belongs.

When you start a to-do, it can always read the messages it came from, also in another company's mailbox. When it needs other messages from another area, it asks with **Use this email for this to-do**; a tap adds them and it carries on. Mail for another of your companies goes to that company's to-dos from the start. A to-do about your own life, like family writing to your work address, is Personal from the start.

## The buttons

A to-do shows its next step, like **Do it** or **Review and send**, with **Snooze** beside it. See [Do it](do-it.md) and [Snooze](snooze.md).

Not prepared yet, it has **Change how** (say how to do it instead); ready, **Ask for changes** (say what to change in the draft). A full row on a phone moves **Snooze** into **…**. **Mark done** (it's handled) is there too: in sight when there is no draft, else at the top of **…**.

To have it done another way, say so in its **Chat**.

Under **…** (on a phone it opens from the bottom of the screen):

- **Hand off…**: give it to a teammate, [Claude Code or Codex](hand-to-agent.md) (the ones you set up), or [ask someone to review](ask-to-review.md).
- **Repeat…**: it [comes back on a rhythm](recurring.md).
- **Not needed**: it goes away. Pick why, optionally: **Not relevant**, **Wrong facts** or **Already handled**. Your Machine learns from it.

Tap the title, or **Name** under **Details**, to rename it. Your title stays, also when the to-do changes.

A closed to-do can come back with **Reopen**. It also comes back by itself when something new happens, like a new message from them. Your own reply doesn't bring it back.

A to-do that only mattered until a set time, like a confirmation before a meeting, closes by itself once that time has passed. It moves to **Done / dismissed** with "No longer needed" and when it was. **Undo** brings it back for a day.

On your first to-dos, a short tip under the buttons shows the key moves: **Change how** (or **Ask for changes**) and **Not needed** when a to-do isn't quite right, and on your first ready draft that nothing goes out until you press **Send**. A tip goes for good once you use its button or press ×, on all your devices.

On your first day, the top of To-dos says hi by name and who has waited longest on your reply. The Machine drafts that reply first, so it is ready when you arrive. Nothing goes out until you send it. The line goes after your first day or your first decided to-do.

Each to-do starts with its title. The line under it says who it's about, their organization, the project, Work or Personal (under **All**) and when it came in, plus where it stands when its group doesn't say so. Tap a name to open its page in the Graph.

Sometimes a quiet line under the text says what isn't known, like "Last contact 12 days ago by email; nothing since." It shows only when the last word with them is old or unanswered, and names channels they may have answered on that aren't connected, like WhatsApp. Your Machine prepares with the same facts, so it says what it doesn't know instead of guessing.

A title says what needs doing. It changes only when that does, like a new ask. A done to-do keeps its title, with how it ended under it, like what went out or "Done: Sam signed it on Tuesday".

Above the draft, one faint line names the message it came from, with that service's logo (Gmail, Slack, WhatsApp…). Tap it to read the thread. The draft starts with the logo of where it goes, so you see it's a Slack reply or an email before reading. A step with no draft, like a handoff, shows the logo on its button.

A chat (Slack, WhatsApp, Telegram, Intercom…) reads as one conversation, oldest first, each message once; the one the to-do is about has a thin line beside it.

**Details** shows its name, project and area (tap one to change it), your last note and a coding agent's result. **Chat ›** at the end of that row opens the chat. A done to-do stays short: its title, one line and what went out; the message it came from is under its **Details**.

A "Waiting on" to-do (someone promised you something) links your own last message to them, the one you're waiting on an answer to: "Email to Pat · Tue".

## Make one yourself

**New to-do** (under **Search** on a computer) adds a to-do for anything. Creating it sends nothing. Without Work or Personal picked, it goes where it belongs, by who and what it is about or the email it follows up on. The Machine looks for that email in your mailbox, also older mail it has not brought in yet.

- **Due**: type a day or a time, like "tomorrow", "next Fri", "3 Nov", "15:00", "2pm", "in 2 hours" or "tomorrow 9". It reads your language too ("over 2 uur", "morgen 9u"). The calendar icon has quick picks, like Snooze, and **Choose date**.
- **Email**: attach the email it's about. It searches your email only, by subject or sender.
- **Files**: tap the paperclip in the box, paste a screenshot, or drop files on the form. On a phone you can also take a photo. Up to 5 files, the same kinds and sizes as in the chat (see [Add files](card-chat.md#add-files)). × takes one back.

The files stay with the to-do: they show on it and in its chat, and The Machine reads them when it works on it. Files alone are enough: The Machine reads a PDF or text file's words and fills in the to-do from them.
