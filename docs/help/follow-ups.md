---
title: Follow-ups
area: graph
summary: Follow up by itself when someone doesn't reply, for a whole board or one project. Asks first unless you say otherwise.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
When a person on a board stops replying, your Machine drafts the follow-up for you, in your voice and in the same conversation. Off until you turn it on.

## Turn it on

**⋯** on a board, then **Follow-ups…**, and tick **Follow up when there’s no reply**. It covers every project on that board.

For one project, **Follow-ups…** in its card's **⋯** or on its page. **For this project** picks **On**, **Off**, or the board's setting. A project's own setting wins over its board's.

## Settings

- Wait 3 to 7 days without a reply. After the shortest wait a follow-up is drafted. The longest wait is the latest it goes out, even when your usage is tight.
- Follow up at least 1 and at most 3 times. It always sends the minimum. Between the two, it reads the conversation and the project and only follows up when that still makes sense. Never more than the maximum.
- **Stages**: **All open stages**, so not the board's last stage or Stalled or declined. **Customize** turns stages on or off and gives a stage its own wait.
- **Channels**: the connected ones that can send. A follow-up goes out on the same channel as the last message. **Switch channel if there’s no reply** tries the next allowed one.
- **Move to Stalled or declined after the last one**: on when the board has that row.

## Asking or sending by itself

**Ask me before sending** is the default: drafts wait in your to-dos. **Send without asking** is a standing yes for that board or project. Anything unusual still waits for you, and so does anything that fails. With Careful mode on, it always asks. A follow-up never goes out twice.

## Reviewing them

A board's follow-ups come as one to-do: "8 follow-ups ready for Alpha testers". **Review** shows them one under the other, each with **Send**, **Edit** and **Skip**. On a keyboard, j and k (or the arrows) move, Enter sends, e edits and s skips. **Send all checked** sends the ones still ticked. A single project's follow-up is a normal to-do.

## When it stops

Follow-ups stop when they reply, when the project is won, lost, archived or moved to a closed stage, and when you snooze or skip one. Before drafting, your Machine checks the conversation for anything newer, so it doesn't nag someone who already answered somewhere else.

After the last follow-up with no reply, the project shows "No reply after 3 follow-ups" and moves to Stalled or declined if that's on.

## Where you see it

The board header says "Follow-ups on, next Thu". A project's card shows its next follow-up, or that one is ready. The project's page lists what went out, including what was sent automatically.

Follow-ups wait while your Machine is busy with your to-dos or close to its usage limit, and catch up later. On a shared board, only the project owner's own Machine follows up.
