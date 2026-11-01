---
title: Follow-ups
area: graph
summary: Follow up by itself when someone doesn't reply, for a whole board or one project. Asks first unless you say otherwise.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
When a person on a board stops replying, your Machine drafts the follow-up for you, in your voice and in the same conversation. Off until you turn it on. When one of your skills fits the board, the drafts follow it, including what comes first in the email.

## Turn it on

**⋯** on a board, then **Follow-ups…**, and tick **Follow up when there’s no reply**. It covers every project on that board. Or tap **Follow-ups off** under the board's name, or **Follow them up** in a stage with projects that got no reply in 10+ days.

For one project, **Follow-ups…** in its card's **⋯** or on its page. **For this project** picks **On**, **Off**, or the board's setting. A project's own setting wins over its board's.

## Settings

- Wait 3 to 7 days without a reply. After the shortest wait a follow-up is drafted. The longest wait is the latest it goes out, even when your usage is tight.
- **Only on workdays**: nothing is drafted or sent on your days off (from **Settings > Work hours**). What comes due then waits for your next work morning. On for Work, off for Personal.
- Follow up at least 1 and at most 3 times. It always sends the minimum. Between the two, it still drafts each one. When it thinks you'd better stop, the draft says why ("The Machine would stop here: 9 unanswered emails since August") and isn't ticked: send it, skip it, or pick **Stop follow-ups here**. Ask for one anyway in a follow-up's chat and it writes one. Never more than the maximum.
- **Stages**: **All open stages**, so not the board's last stage or Stalled or declined. **Customize** turns stages on or off and gives a stage its own wait.
- **Channels**: the connected ones that can send. A follow-up goes out on the same channel as the last message. **Switch channel if there’s no reply** tries the next allowed one.
- **Move to Stalled or declined after the last one**: on when the board has that row.

## Asking or sending by itself

**Ask me before sending** is the default: drafts wait in your to-dos. **Send without asking** is a standing yes for that board or project. Anything unusual still waits for you, and so does anything that fails. With Careful mode on, it always asks. A follow-up never goes out twice.

Right before one goes, the thread is checked again, and if anyone wrote since the draft it isn’t sent: "Not sent: new message in the thread".

## Reviewing them

A board's follow-ups come as one to-do, never one per email. While they're drafted it says "Writing 3 follow-ups…", then "8 follow-ups ready for Alpha testers".

**Review** shows them one under the other, each in full, so one scroll reads them all. **Send**, **Edit** and **Skip** show on the current one. On a keyboard, j and k (or the arrows) move, Enter sends, e edits, s skips and c changes. **Send all checked** sends the ones still ticked.

**Skip** unticks a draft and moves it to the bottom, marked Skipped with an **Undo**; it's skipped for good when you close the review. A skipped one comes back with **Bring back** in the project's follow-ups or on its to-do in Done, as long as no newer follow-up came. A single project's follow-up is a normal to-do.

**Change…** rewrites all checked drafts, or only the current one, the way you say; nothing is sent, and **Undo change** brings back the old text. While the Change box is open or a rewrite runs, nothing can be sent, and a draft that changed is shown again before it can go.

When several go out in a row, also with Send without asking, each mailbox sends one every 30 to 45 seconds, and the to-do shows how far it got: "Sending 3 of 8…". **Stop sending** stops the rest: one already on its way still goes, and the others are back in the review as drafts, to send later ("Stopped. 1 sent, 11 kept as drafts.").

## Emails sent before your Machine

Emails you sent from another app, before your Machine read that mailbox, count too. It reads the conversation itself (or, when it can't, the earlier emails quoted in your last one), so three emails with no reply count as three, and "No reply for" counts from the first. If you already reached the maximum, it doesn't draft another one.

## When it stops

Follow-ups stop when they reply, when the project is won, lost, archived or moved to a closed stage, and when you snooze or skip one. Before drafting, your Machine checks the conversation for anything newer, so it doesn't nag someone who already answered somewhere else.

**Pause** in **Follow-ups…** holds a board or project without turning follow-ups off: nothing is drafted or sent, no round ends, and open follow-up to-dos stay open. Pick a day to resume on, or tap **Resume** when ready. The wait picks up where it was, and what was due comes one by one. It shows **Paused** meanwhile.

After the last follow-up with no reply, the project shows "No reply after 3 follow-ups" and moves to Stalled or declined if that's on. Stopped before any went out, it says "Follow-ups stopped" and stays in its stage.

If their email bounced and they have another address, the follow-up goes there instead ("Bounced, now to <address>"). A draft whose address bounces before it goes is held: "Not sent: <address> bounced", and moves to their other address to wait for your Send.

With no other address, follow-ups move to LinkedIn or WhatsApp when that's allowed and you talk there. Otherwise they stop with "Email bounced". When the project matters, you get a to-do to find a new address.

## Where you see it

The board header says "Follow-ups on, next Thu". A project's card shows its next follow-up, or that one is ready. The project's page lists what went out, including what was sent automatically.

Follow-ups wait while your Machine is busy with your to-dos or close to its usage limit, and catch up later. On a shared board, only the project owner's own Machine follows up.
