---
title: No new to-dos
area: troubleshooting
summary: Checks are off, waiting, or stopped on your model's usage limit. How to tell and what to do.
covers: 
code: dashboard.html, assistant.py
order: 3
---
To-dos come from checks: your Machine reads what came in, in small batches, within about 15 minutes.

## Just signed up

On a new hosted Machine, checks start by themselves once your AI and mail are connected. While your Machine reads your mail, To-dos says "Reading your mail, first to-dos in a few minutes." If a step is missing, **Needs you** names it, like **Connect mail**, with a link to that step.

## Checks are off

The top of To-dos says "Checks are off, so no to-dos arrive yet." On a hosted Machine, press **Turn on checks**. On your own computer, run `./install.sh --activate`.

## Your model's limit

Checks of what came in pause at about 65% of your plan's 5-hour limit and at 90% of its weekly limit, to keep room for your own chats. A board's look through your history goes slower, at about a seventh of the week a day. With a working fallback model on another plan or provider, checks don't wait. See [Model](model.md).

While checks wait, the top of the dashboard says until when, like "Checks wait until 07:15 to save your ChatGPT week." **Check now** starts one right away. When a limit is reached, the top of the dashboard says which one and when it resets. **Connections**, then **Checks**, shows it next to the run. **Settings**, **Model** shows your limits. See [Model](model.md).

Nothing is lost while it waits: what came in is checked once it can.

## A run failed

**Recent runs** under **Checks** shows each run. A failed batch is tried again by itself.
