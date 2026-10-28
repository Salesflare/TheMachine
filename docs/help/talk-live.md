---
title: Talk live
area: cards
summary: A spoken conversation with The Machine about a to-do, with OpenAI's voice. It can look things up and suggest, but it never sends anything.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Start a conversation

In a to-do's chat, tap the wave next to the mic. Allow the microphone if your browser asks. When the bar says **Live**, talk as you would on a call. The Machine answers out loud.

It knows the to-do you're in: its messages and its draft. It can also look up your other to-dos.

The bar has **Mute** and **End**. A conversation lasts up to 10 minutes. A minute before the end, the timer shows how much is left. Start it again to go on.

## Nothing is sent from a conversation

The Machine can't send, change or approve anything while you talk. When you ask for something, like "write a reply saying Thursday works", it shows the request above the bar. Tap **Send to chat** to hand it to the chat. What the chat drafts then waits for your **Approve**, as always.

Saying "yes" or "send it" does nothing. Only your taps count.

## A record in the chat

What you both say is written into the to-do's chat, under a **Talked live** line. You can read it back later.

## What you need

Talk live uses OpenAI's realtime voice, so OpenAI has to be set up in OpenClaw:

- A ChatGPT sign-in: included in your plan, where your plan has access.
- An OpenAI API key: OpenAI charges your key per minute of talk, and the bar says so. When both are set up, OpenClaw uses the key.

**Settings**, **General**, **Voice input** shows whether Talk live is ready. Without OpenAI, the wave doesn't show. Your audio goes from your browser straight to OpenAI. Your key never reaches the browser.

## When it doesn't work

- **The microphone is blocked**: allow the microphone for this site in your browser's settings.
- **Talk live couldn’t start**: check OpenAI in OpenClaw, then try again.
- **Talk live lost its connection**: start it again. What was said so far stays in the chat.
