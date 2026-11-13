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

On a new hosted Machine, checks start by themselves once your AI and mail are connected. While your Machine reads your mail, To-dos says "Reading your mail, first to-dos in a few minutes." Once it knows how much there is, it says roughly how long: "First to-dos in about 10 min." If a step is missing, **Needs you** names it, like **Connect mail**, with a link to that step.

While it reads, To-dos shows how far it got ("Read 20 of 132 messages. Reading the next 40…"), a few of the people and organizations it came across, and your first to-do as soon as it's in. The number counts messages it has finished reading; the bar keeps moving while it reads the next ones. The names come from your own mail, and only you see them.

When the first look finds nothing for you, it says what it read and offers next steps, like connecting a service that mails you often or asking what changed this week.

## Checks are off

The top of To-dos says "Checks are off, so no to-dos arrive yet." On a hosted Machine, press **Turn on checks**. On your own computer, run `./install.sh --activate`.

## Your model's limit

To keep room for your own chats, checks pause at about 65% of your AI plan's 5-hour limit and 90% of its weekly limit. With a backup model on another plan, checks don't wait. See [Model](model.md).

While checks wait, the top of the dashboard says until when, like "Checks wait until 07:15 to save your ChatGPT week." **Check now** starts one anyway. **Settings**, **Model** shows your limits.

Nothing is lost: what came in is checked once it can.

## A run failed

**Recent runs** under **Connections**, **Checks** shows each run. A failed one is tried again by itself.

## Set aside

When a check puts a message off twice, it is set aside. **Connections**, **Checks** shows how many, and **Set aside** lists them. One from a person writing to you, someone you know or a customer gets one more look about 3 days after it came in. That look makes a to-do or closes it. What you dismissed or snoozed stays that way.
