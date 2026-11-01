# Family

A **Family Fleet** links the Machines of the people you live or plan with. It is free for up to 6 people, hosted or
self-hosted. Your Machines coordinate over the Network, under rules each of you sets, and only for family things.

## What it does

- **When are we all free?** In the Fleet tab under your Family, pick a day and how many days. Every member's Machine
  answers from its owner's own calendars with **busy times only**: start and end, never what, where or with whom.
  Your Machine works out the times everyone is free (between 8:00 and 21:00, at least an hour) and shows them as they
  answer.
- **To-dos.** Ask one member to do something ("Pick up the groceries", with a due date if you like). It waits on their
  Machine as a to-do with **Accept** and **Decline**. Once accepted it is their to-do, and on its due
  day their Machine reminds them once (phone, and Telegram when that is on). You see asked, accepted, declined, and done
  once they finish it.
- **Plans.** Propose a plan to the whole Family ("Sunday lunch at grandma's", a time and a place). Each member says
  **I'm in** or **Can't make it** on their Machine; you see who is in, who can't and who hasn't answered yet.
  **Nothing is written to anyone's calendar.** The plan carries an **Add to my calendar** link each person opens
  themselves.

## Invite suggestions

Inviting someone used to be up to you. Now, when a to-do is about family plans with one person who isn't in your
Family yet ("Who picks up the kids on Wednesday?", a back-and-forth about the weekend), it can say: "Invite Sasha?
Your Machines can sort this out without you asking each other." **Invite** opens the invite form on your account page,
prefilled with their address, where you see the email before it goes; **Not now** hides it for 90 days.

- The review judges the moment by meaning and passes `family_with` (their Graph node) only when that person is family
  as their Graph role or your own words say. Never guessed from a name or the topic.
- At most once per person. Never for Work contacts (a Work to-do, the Graph's Work side, a Work Fleet member), people
  already in your Family, or someone with an open invite. Only where you can invite to a Family Fleet (its owner or an
  admin, or by starting one).
- Each suggestion and tap is a line in Activity. Turn it off in Settings, Fleet: **Suggest inviting family**.


Under **Sharing**, the Family has the same rules as a Work Fleet, one per kind for all of them, with exceptions per person
(rules set per person before were folded once, so nobody's rule changed):
**Ask me first**, **Always** or **Never**. The defaults are friendlier than at work, and still private:

| Kind | Default | What they get |
| --- | --- | --- |
| Free/busy times | Always | your busy times on those days, never what |
| To-dos | Ask me first | accepted, then done when you finish it |
| Plans | Ask me first | "is in" or "can't make it"; never your calendar |

**Always** on a to-do or plan accepts it by itself (it still only makes a to-do for you). **Never** answers "no".

## Kept apart from work

A Family never asks or answers work questions: who knows someone, meeting context, shared emails, intros, handoffs,
follow-up splits, the team brief or free questions. The Network refuses them in a Family, and your Machine declines
them there even if one arrives. A to-do or plan becomes a personal to-do, on a personal account when you have one.

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
`family_event`, `family_invite` and `family_invite_setting`, from the owner's dashboard only. `family_invites.py` decides
the invite suggestions (`test_family_invites.py`). Tests: `test_family.py`, `test_family_dashboard.mjs`. Try it on
made-up data with `scripts/sandbox.sh family`.
