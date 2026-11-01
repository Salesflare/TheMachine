# Family

A **Family Fleet** links the Machines of the people you live or plan with. It is free for up to 6 people, hosted or
self-hosted. Your Machines coordinate over the Network, under rules each of you sets, and only for family things.

## What it does

- **When are we all free?** In the Fleet tab under your Family, pick a day and how many days. Every member's Machine
  answers from its owner's own calendars with **busy times only**: start and end, never what, where or with whom.
  Your Machine works out the times everyone is free (between 8:00 and 21:00, at least an hour) and shows them as they
  answer.
- **To-dos.** Ask one member to do something ("Pick up the groceries", with a due date if you like). It waits on their
  Machine as a card under To-dos with **Accept** and **Decline**. Once accepted it is their card, and on its due
  day their Machine reminds them once (phone, and Telegram when that is on). You see asked, accepted, declined, and done
  once they finish the card.
- **Plans.** Propose a plan to the whole Family ("Sunday lunch at grandma's", a time and a place). Each member says
  **I'm in** or **Can't make it** on their Machine; you see who is in, who can't and who hasn't answered yet.
  **Nothing is written to anyone's calendar.** The plan carries an **Add to my calendar** link each person opens
  themselves.

## Rules

Under **Sharing**, the Family has the same rules as a Work Fleet, one per kind for all of them, with exceptions per person
(rules set per person before were folded once, so nobody's rule changed):
**Ask me first**, **Always** or **Never**. The defaults are friendlier than at work, and still private:

| Kind | Default | What they get |
| --- | --- | --- |
| Free/busy times | Always | your busy times on those days, never what |
| To-dos | Ask me first | accepted, then done when you finish it |
| Plans | Ask me first | "is in" or "can't make it"; never your calendar |

**Always** on a to-do or plan accepts it by itself (it still only makes a card for you). **Never** answers "no".

## Kept apart from work

A Family never asks or answers work questions: who knows someone, meeting context, shared emails, intros, handoffs,
follow-up splits, the team brief or free questions. The Network refuses them in a Family, and your Machine declines
them there even if one arrives. A to-do or plan becomes a personal card, on a personal account when you have one.

## Ask to review

A Personal to-do can go to someone in your Family for a look before you send it: **Ask to review**, under More on the
to-do. They edit the draft or add a comment on a to-do of their own; their changes come back for you to accept or
ignore, and nothing goes out until you press Send. Work to-dos never go to the Family. See [The Fleet](fleet.md)
(Ask to review) and `fleet_reviews.py`.

## Safety

What a member sends is kept to a fixed shape (a title, a short note, a date or time, a place) and only ever shown,
quoted, as their words. No model, tool or Do it runs on it, and nothing happens until you accept (or set Always).
Messages travel over the Network like every Fleet question, and are end-to-end encrypted where both Machines support
it (see [Network](network.md)).

## For developers

`family.py` holds the shapes, the free-time arithmetic and the `Family` mixin of `fleet.Fleet`. To-dos and plans take
the same path as Work requests (`fleet_requests.STAGED`). Dashboard operations: `family_free`, `family_todo`,
`family_event`, from the owner's dashboard only. Tests: `test_family.py`, `test_family_dashboard.mjs`. Try it on
made-up data with `scripts/sandbox.sh family`.
