---
title: No new to-dos
area: troubleshooting
summary: Checks are off, waiting, or stopped on your model's usage limit. How to tell and what to do.
covers: 
code: dashboard.html, assistant.py
order: 3
---
To-dos come from checks: your Machine looks at what came in within about 15 minutes.

## Just signed up

On a new hosted Machine, checks start by themselves once your AI and mail are connected. While your Machine reads your mail, To-dos says "Reading your mail, first to-dos in a few minutes." If a step is missing, **Needs you** names it, like **Connect mail**, with a link to that step.

While it reads, To-dos shows how far it got, a few of the people and organizations it came across, and your first to-do as soon as it's in. The names come from your own mail, and only you see them.

## Checks are off

The top of To-dos says "Checks are off, so no to-dos arrive yet." On a hosted Machine, press **Turn on checks**. On your own computer, run `./install.sh --activate`.

## Your model's limit

To keep room for your own chats, checks pause at about 65% of your AI plan's 5-hour limit and 90% of its weekly limit. With a backup model on another plan, checks don't wait. See [Model](model.md).

While checks wait, the top of the dashboard says until when, like "Checks wait until 07:15 to save your ChatGPT week." **Check now** starts one anyway. **Settings**, **Model** shows your limits.

Nothing is lost: what came in is checked once it can.

## A run failed

**Recent runs** under **Connections**, **Checks** shows each run. A failed one is tried again by itself.
