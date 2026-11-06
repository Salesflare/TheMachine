---
title: Model
area: settings
summary: Which AI model answers for you, how hard it thinks, and how much of your plan's limits it has used.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
**Settings**, **Model** shows which AI model does your **Background work** and how you're signed in, like with ChatGPT.

## Model and thinking for chats

Under **Chats**, pick the model and thinking level for your to-do chats and Help. You only see the models and levels your sign-in offers.

More thinking answers hard questions better, but is slower and uses more of your plan. **Ultra thinking** brings in helpers for the hardest questions, and uses the most. A new Machine starts at **Low thinking**: good results for much less of your plan. A change applies from the next message.

To change it for one chat only, tap the model or thinking level under its message box. Pick the Settings choice again to follow Settings.

Checks, your profile and drafts prepared ahead keep their own model.

## Limits

If your plan has usage limits, like a ChatGPT or Claude plan's 5-hour and weekly limits, it shows how much is used and when each resets. Looking never uses your plan.

## Room for your own chats

Background work leaves room for your own chats. It pauses at about 65% of the 5-hour limit. Checks of new messages go on until about 90% of the weekly limit; other work takes about a seventh of the week a day. A sign-in without limits, like an API key, never pauses.

Background work never runs on GPT-6 Astra. It uses GPT-6.1 Sol instead.

## When a limit is reached

The top of the dashboard says which limit was reached and when it resets. Work waits, then picks up where it left off. Nothing is lost. If your ChatGPT plan has resets, **Use a reset** starts the limits over. Otherwise **See resets in ChatGPT** opens ChatGPT's page.

## With a fallback

If your Machine has a fallback model on another plan or provider, it takes over when a limit is reached, and nothing waits. The top of the dashboard says "ChatGPT limit reached, using your fallback." If the fallback stops working, the pauses come back.

## Change the main model

The main model is what the rest of The Machine uses. On a hosted Machine, change it on your setup page, under Your AI. On your own computer, see [ChatGPT](chatgpt.md) and the [models guide](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
