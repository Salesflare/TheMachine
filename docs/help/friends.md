---
title: Friends and the Network
area: fleet
summary: Add friends by username, find people you know who have a Machine, and pair a Machine on your own computer.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Friends

Add someone by their exact username, in the **Fleet** tab under Friends. Friends can ask who knows someone, get meeting context and warm intros, and see when you're busy (busy times only, never what). Remove or block a friend any time.

## Find people you know

In **Fleet**, under **Network**:

- "Check which of my contacts have a Machine" suggests people you know.
- "Let people who have my email find me" lets them find you.

Both are on by default, and off at the Careful security level. Turn either off any time; your choice stays. People can find you by your sign-in email and your connected addresses, except shared ones like info@, which stay off until you turn them on.

People you know show up right away when you turn it on, and as they join later. Each one comes with Connect, Not now or **Never suggest**. **Leave the Network** takes you off it.

People it finds say **Has a Machine** in your People list. It checks the addresses in your messages and the ones you added to a person with **Edit**: if someone signed up with another address, add it to them. On the page of someone it found, **Add as friend** in the ⋯ menu sends the same request as Connect.

Phone numbers count too: the numbers in your WhatsApp chats with people you wrote to or met, and the ones you added with **Edit**. Your linked WhatsApp number and the numbers under About you make you findable, each with its own switch under **Findable by**. A number finds someone only when they looked you up too, or you are friends, so nobody can try numbers to see who has a Machine.

## Scheduling with other Machines

When someone with a Machine writes "let's meet next week", your Machine asks theirs for free times and finds one that suits you both, within your work hours. Each of you gets one to-do, like "Meet Alex Example", with the time below it. Tap **Book it**, **Other time** or **Not needed**. The invite goes out only once you both tapped Book it.

Only free or busy goes over, sealed end to end, for at most 14 days and rounded to 15 minutes. Private events count as busy. A Machine can ask only when you emailed each other both ways. Set it under **What other Machines may ask mine**: **Free/busy for scheduling** or **Off**, with your meeting length, buffer and preferred times. Each ask shows in Activity, under Calendar.

No Machine there, or no answer: the email draft gets a link where they pick one of your free times. Their pick is a to-do with **Book it**; nothing is booked before you tap it.

The link shows only free times, by the same rules, and nothing else about you. It ends once the meeting is booked, or after 14 days. The email shows it as "Pick a time". At the bottom, the page says "Your Machine found these times. Get yours." with your first name. Turn that off with **Footer on booking links**. Each link and pick shows in Activity.

## A Machine on your own computer

To join the Network from a Machine you run yourself:

1. On your account page at app.themachine.computer, press **Pair a self-hosted Machine**. The code works once, for 15 minutes.
2. On your computer, run `assistant fleet-pair` with the code, and restart.

Up to 5 Machines per account. Each one can be disconnected there.
