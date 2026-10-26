---
title: Model
area: settings
summary: Which AI model answers for you, and how much of your plan's limits it has used.
covers: settings:model
code: dashboard.html, docs/models.md
order: 5
---
In **Settings**, **Model** shows the model in use and how you're signed in, like with ChatGPT.

## Limits

If your plan has usage limits, it shows how much of each is used and when it resets, for example the 5-hour and the weekly limit of a ChatGPT or Claude plan. Reading this never uses your plan.

## Room for your own chats

Background work (reviews, your profile, drafts prepared ahead) leaves room for your own chats. It pauses at about 65% of the 5-hour limit, and paces the weekly limit at about a seventh a day. A sign-in without usage limits, like an API key, is never paused.

Background work never runs on GPT-6 Astra. It uses GPT-6.1 Sol instead.

## When a limit is reached

The top of the dashboard says which limit was reached and when it resets. Work waits, then picks up where it left off. Nothing is lost. Some ChatGPT plans come with resets: **Use a reset** starts the limits over, after a confirm. Otherwise **See resets in ChatGPT** opens ChatGPT's own page.

## Change the model

On a hosted Machine, pick another one on your setup page, under Your model. On your own computer, change it in OpenClaw. See [ChatGPT](chatgpt.md) and the [models guide](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
