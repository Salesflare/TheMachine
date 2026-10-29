---
title: Model
area: settings
summary: Which AI model answers for you, how hard it thinks, and how much of your plan's limits it has used.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
In **Settings**, **Model** shows the model background work uses (marked **Background work**) and how you're signed in, like with ChatGPT.

## Model and thinking for chats

Under **Chats**, pick the model and the thinking level your to-do chats and Help use. The list has only the models your sign-in offers, like ChatGPT's when you signed in with ChatGPT, and each model only the levels it has.

More thinking answers harder questions better, but is slower and uses more of your plan. **Ultra thinking** brings in helpers for the hardest questions: the slowest, and it uses the most. A change applies from the next message. A new Machine starts at **Low thinking** when its model has it: good results for much less of your plan.

One chat can use something else: under its message box, tap the model or the thinking level. That choice is for that chat only. Pick the same as in Settings again to follow Settings.

Reviews, your profile and drafts prepared ahead keep their own model.

## Limits

If your plan has usage limits, it shows how much of each is used and when it resets, for example the 5-hour and the weekly limit of a ChatGPT or Claude plan. Reading this never uses your plan.

## Room for your own chats

Background work (reviews, your profile, drafts prepared ahead) leaves room for your own chats. It pauses at about 65% of the 5-hour limit. Reviews of what came in go on until about 90% of the weekly limit; the rest paces it at about a seventh a day. A sign-in without usage limits, like an API key, is never paused.

Background work never runs on GPT-6 Astra. It uses GPT-6.1 Sol instead.

## When a limit is reached

The top of the dashboard says which limit was reached and when it resets. Work waits, then picks up where it left off. Nothing is lost. Some ChatGPT plans come with resets: **Use a reset** starts the limits over, after a confirm. Otherwise **See resets in ChatGPT** opens ChatGPT's own page.

## Change the main model

The main model is what the rest of The Machine uses. On a hosted Machine, pick another one on your setup page, under Your AI. On your own computer, change it in OpenClaw. See [ChatGPT](chatgpt.md) and the [models guide](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
