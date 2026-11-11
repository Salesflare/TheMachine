---
title: Routines
area: cards
summary: Work your Machine does on its own, on a rhythm, like a Monday summary of your open deals. It only reads.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, dashboard/routines-page.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays
---
## Make one

Open **Routines** in the sidebar and say what it should do and when, in one line: "every Monday at 9, sum up my open deals" or "every weekday morning, list the emails I still owe a reply". Then **Add**.

Without a time it runs at 8:00. The time is on your Machine's clock. Its first run gives it a short name.

**Add** first does a test run, so you see what it gives before you keep it. Nothing is sent or saved. Then **Add** keeps it on its rhythm, **Change** tries other words or a new name and **Cancel** drops it.

## Templates

Under **Templates** at the bottom of Routines, **Add** turns on a ready-made routine. It runs once right away, then every morning at 7:30 (Spam cleanup every hour). Its card shows its words like any routine, and **Edit** changes them or its name.

**Newsletter cleanup** makes one to-do per area (work and personal) with the past day’s newsletters, each with **Keep** or **Unsubscribe**. Unsubscribe uses the list’s one-click link, or its unsubscribe email from your address when sending is on. Otherwise it shows **Open unsubscribe page**.

Receipts, orders and payment notices are left out. Mail that came through a group address, like a Google Group, is listed under who wrote it and never unsubscribes you from the group.

**Spam cleanup** makes one to-do per area with mail from unknown senders that looks like spam, each with **Spam** or **Not spam**. Outlook moves spam to Junk and Gmail marks it as spam. It’s only there for mail The Machine may move: Gmail connected read-only doesn’t get it. It checks every hour, so spam is usually there before you get to it.

Nothing changes until you confirm on the to-do. Senders you decided on aren’t asked again. A day without newsletters or spam makes no to-do, and these to-dos never send a notification.

**Birthdays** makes a to-do for each close contact whose birthday is today: people you write to yourself, like friends, family and regular contacts. Each comes with a short greeting drafted where you usually talk with them, like their WhatsApp chat or your email thread, in their language. It goes out only when you send it. A day without birthdays makes no to-do.

Birthdays come from your calendars (Google’s birthday events and Birthdays calendar, read each morning even when they aren’t synced, and Outlook’s Birthdays calendar), your Google contacts on a self-hosted Machine and a date field named Birthday on a person in the Graph. When none of them holds a birthday yet, its result says **No birthday info yet** and how to add some.

**Import birthdays from Facebook**: once Birthdays is on, a to-do offers to read Facebook’s birthdays page. Tap **Import** and The Machine opens it in its browser, scrolls until every month has loaded and reads each friend’s name and birthday. It shows how many it found and who matched people in your Graph by first and last name. A name that more than one person has is skipped and listed.

Only **Save** keeps them, and only the birthday, on each person’s page. A birthday you set there stays. It never reads again by itself: **Import again** on the to-do does. The browser has to be signed in to Facebook. If it isn’t, tap **Sign in to Facebook** on the to-do and sign in there; once you’re in, it reads the page by itself. The Machine never signs in for you.

Friends nobody in your Graph has are counted, with a few names. **Add … as personal contacts** adds them all at once, also after Save: each with their name and birthday, never shared with a Work Fleet. A name someone in your Graph already has, or someone you deleted permanently had, is skipped. Birthday reminders still only come for people you write to.

**Undo** on the to-do takes exactly those people away again, also after **Import again**.

While a template’s routine keeps the template’s words, it runs on its own code, without your AI plan (Spam cleanup first lists new mail from unknown senders in code, and asks your AI one short question only when there is some). A new name keeps that. Once you change its words, it runs like any routine on your words.

Newsletter cleanup and Spam cleanup still end in the same to-do with a choice per mail. An edited Birthdays gives its result and at most one draft, not a to-do per person. **Back to the template** in **Edit** puts its words back.

## What a routine does

At its time your Machine reads what it needs, like your messages, meetings and the Graph, and puts the result on the Routines page. Each result says **Ready**, **Nothing new** (with why) or **Didn’t work** (with why). A run that ends without a result counts as one that didn't work, never as done.

Routines only read: your messages, web pages, GitHub and sites like X in the browser. They don’t send, reply, post or change anything. Only a template changes mail, and only what you confirm on its to-do.

When a routine’s job ends in a post or a message, it does everything up to that step and shows the draft, like **Would post on X:**. After a real run you get it as a to-do to approve; a test run only shows it. Its name says what it is about and where it goes, its button names the step, like **Post it**, and **From your routine** under it opens the routine.

The to-do starts in the area of the account it goes out from, like Work for your company’s X account, so it never asks to be moved.

A run can follow your [skills](skills.md) that are on, picked by what the routine does: only the ones that fit are read in full. The result names them under **Used:**. A skill never makes a routine send or change anything.

Your routines are under **Your routines**, below any suggestions. A long result folds to a short preview; **Show more**, or a tap on it, opens it.

Each run knows the last result, so it can say what changed since then.

After a good run, your Machine may write itself a recipe for the reading that is the same each time, like which mails or GitHub changes to look at. The next runs read those first, in plain code, and the AI only picks what matters and writes it, with fewer tokens. A recipe only reads; when it stops working, the run reads by itself and fixes it. It shows under **Advanced: script steps** in the ⋯ menu.

## Missed days

When your Machine was off or busy, a missed run isn't stacked: only the newest one runs, once. Each date runs once, even after a restart.

Routines run one at a time and wait when your AI plan's usage is low, like all background work. **Run now** runs it right away; its result shows on the card when it is ready.

## Change or stop it

These are in the ⋯ menu on the routine. **Edit** changes its name and what it does; when it runs and its results so far stay. **Change when** takes a new rhythm in your own words, like "every weekday at 8". Both have **Save** and **Cancel**; on a computer, Esc or a click outside cancels too.

In **Edit**, **Try it** runs the new words once and shows the result there. The routine stays as it was until **Save**.

**Pause** stops the runs until **Resume**; paused routines wait under **Paused** at the bottom, and nothing missed while paused runs afterwards. **Stop** ends a routine for good.

When you use **Ask for changes** on a routine’s to-do, or write in its chat, and your note is meant for every run, like "never use emoji", the to-do offers **Also change the routine**, on the to-do and in its chat under the reply. It shows what changes in the routine’s words, and the routine only changes when you tap **Change it**. **Keep it as is** leaves it. A fix to just that draft offers nothing.

## Advanced: script steps

No script needed: say what a routine should do in your own words, and your Machine works out the rest.

For power users, a routine can also run your own commands on your Machine: in the ⋯ menu, pick **Advanced: script steps**. **Edit** shows them only once a routine has some. **Get data** runs a command first, in its folder (your home folder if empty) for at most its seconds. What it prints goes to the run to work with. With no words, what it prints is the result.

**Check** gets the result as input after the run. If it exits with an error, the run shows **Didn’t work** with what the check said. A Get data command that fails shows the same way.

A command is one line, run without a shell: no pipes or variables. Script steps are yours, set on your dashboard only. A test run and **Try it** run Get data too and say so; they still send and keep nothing. A routine never sends, so a script step should only read.

## From your OpenClaw jobs

If you made scheduled jobs in OpenClaw before, your Machine reads them (it never changes them) and offers the ones that fit as routines under **Suggested**. Each one ran once, so you see a real result.

It keeps your corrections to the job and leaves out what it sent or posted. A job that ran a script, or read what a script job collected, brings it along as Get data. **Add** makes it a routine, **No thanks** never asks about that job again. A job that reminded you to do something comes as a recurring to-do offer on To-dos instead.

Before you add a suggestion, **Edit** and **Change when** in its ⋯ menu change it like any routine. **Run again** runs it now with its current words, to see newer results, say after a quiet weekend. It only reads, runs once per tap, and its new result replaces the old one.

At most three suggestions wait at a time. After a week of good runs, the routine asks **Turn off the old OpenClaw job?** It only turns off when you tap **Turn it off**, and you can turn it back on in OpenClaw.

## From what you do

Your Machine also notices work you do on a rhythm and offers it as a routine under **Suggested**, also without OpenClaw. It looks for:

- the same ask, three times or more in a row, like "sum up the open support tickets" every Monday;
- a mail you send on a rhythm, like a weekly report to your team;
- newsletters and update mails that keep coming every week;
- a busy Slack channel that others write in every week;
- mail you forward one by one to the same person, like school and club mails to your partner: a weekly digest for them saves the forwarding;
- the same request you answer on a rhythm, like a monthly approval for the same person.

Each suggestion says what it saw, like "Asked 4 times in a row" or "Forwarded 6 mails to Sam in 3 weeks", and ran once so you see a real result. Think of a team recap, a brief before a weekly call, a support or dev summary, a pulse on your numbers, or a digest of the newsletters you get.

It only suggests what is specific to you and clearly useful: a news digest only over your own newsletters, never a generic one. When nothing fits, there is no suggestion.

It looks at most once a day and brings at most one new suggestion a week, without a notification. **No thanks** never brings that one back. Forwards and replies stay with the account they were sent from, so Work and Personal don’t mix. All of it stays on your Machine. A to-do you close on a rhythm comes as a recurring to-do offer instead.

## Routines and recurring to-dos

A recurring to-do (recurring.md) reminds you to do something. A routine is work your Machine does by itself and shows you. Use a recurring to-do for "pay the rent on the first", and a routine for "every Friday, tell me which deals went quiet".
