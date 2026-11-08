---
title: Routines
area: cards
summary: Work your Machine does on its own, on a rhythm, like a Monday summary of your open deals. It only reads.
covers: tab:routines
code: routines.py, routines_app.py, routine_imports.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report
---
## Make one

Open **Routines** in the sidebar and say what it should do and when, in one line: "every Monday at 9, sum up my open deals" or "every weekday morning, list the emails I still owe a reply". Then **Add**.

Without a time it runs at 8:00. The time is on your Machine's clock. Its first run gives it a short name.

**Add** first does a test run, so you see what it gives before you keep it. Nothing is sent or saved. Then **Add** keeps it on its rhythm, **Change** tries other words and **Cancel** drops it.

## What a routine does

At its time your Machine reads what it needs, like your messages, meetings and the Graph, and puts the result on the Routines page. Each result says **Ready**, **Nothing new** (with why) or **Didn’t work** (with why). A run that ends without a result counts as one that didn't work, never as done.

Routines only read. They don’t send, reply, post or change anything.

A run can follow your [skills](skills.md) that are on, picked by what the routine does: only the ones that fit are read in full. The result names them under **Used:**. A skill never makes a routine send or change anything.

Your routines are under **Your routines**, below any suggestions. A long result folds to a short preview; **Show more** opens it.

Each run knows the last result, so it can say what changed since then.

## Missed days

When your Machine was off or busy, a missed run isn't stacked: only the newest one runs, once. Each date runs once, even after a restart.

Routines run one at a time and wait when your AI plan's usage is low, like all background work. **Run now** runs it right away; its result shows on the card when it is ready.

## Change or stop it

These are in the ⋯ menu on the routine. **Edit** changes what it does; when it runs and its results so far stay. **Change when** takes a new rhythm in your own words, like "every weekday at 8". Both have **Save** and **Cancel**; on a computer, Esc or a click outside cancels too.

In **Edit**, **Try it** runs the new words once and shows the result there. The routine stays as it was until **Save**.

**Pause** stops the runs until **Resume**; paused routines wait under **Paused** at the bottom, and nothing missed while paused runs afterwards. **Stop** ends a routine for good.

## Script steps

A routine can run your own commands on your Machine. In **Edit**, open **Script steps**. **Get data** runs a command first, like `python3 ~/scripts/deals.py`, in its folder (your home folder if empty) for at most its seconds. What it prints goes to the run to work with. With no words, what it prints is the result.

**Check** gets the result as input after the run. If it exits with an error, the run shows **Didn’t work** with what the check said. A Get data command that fails shows the same way.

A command is one line, run without a shell: no pipes or variables. Script steps are yours, set on your dashboard only. A test run and **Try it** run Get data too and say so; they still send and keep nothing. A routine never sends, so a script step should only read.

## From your OpenClaw jobs

If you made scheduled jobs in OpenClaw before, your Machine reads them (it never changes them) and offers the ones that fit as routines under **Suggested**. Each one ran once, so you see a real result.

It keeps your corrections to the job and leaves out what it sent or posted. A job that ran a script, or read what a script job collected, brings it along as Get data. **Add** makes it a routine, **No thanks** never asks about that job again. A job that reminded you to do something comes as a recurring to-do offer on To-dos instead.

At most three suggestions wait at a time. After a week of good runs, the routine asks **Turn off the old OpenClaw job?** It only turns off when you tap **Turn it off**, and you can turn it back on in OpenClaw.

## Routines and recurring to-dos

A recurring to-do (recurring.md) reminds you to do something. A routine is work your Machine does by itself and shows you. Use a recurring to-do for "pay the rent on the first", and a routine for "every Friday, tell me which deals went quiet".
