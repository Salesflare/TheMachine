---
title: Talk live
area: cards
summary: A spoken conversation with The Machine about a to-do, with OpenAI's voice. It works in the to-do's chat, and sends a draft only after you say yes to it.
covers: talk-live
code: talk_live.py, talk-live-run.mjs, dashboard.html
order: 8
keywords: talk live, voice, conversation, speak, call, realtime, openai, chatgpt, gpt live
---
## Start a conversation

In a to-do's chat, tap the wave next to the mic. Allow the microphone if your browser asks. When the bar says **Live**, talk as you would on a call. The Machine answers out loud, and you can talk over it to interrupt.

It knows the to-do you're in: its messages, its draft and its chat. It can also look up your other to-dos.

The bar has **Mute** and **End**. A conversation lasts up to 10 minutes. A minute before the end, the timer shows how much is left. Start it again to go on.

## Ask for things, and send with a yes

When you ask for something, like "write a reply saying Thursday works" or "snooze this until Monday", The Machine hands it to the to-do's chat, as if you had typed it. The chat follows its usual rules: it can change the draft or snooze the to-do.

To send a draft, say so. The Machine asks first, naming who it goes to and how, like "Send this reply to Lotte by email?". On a phone, it reads the whole draft out before it asks. Answer with a clear yes, in any language, and that one draft goes.

- It only asks about the draft shown in the chat. If the draft changes after the question, it asks again.
- If your answer isn't a clear yes, nothing is sent and it asks again. "No" sends nothing.
- A yes always sends one draft. To send several, use the follow-up review.
- The chat shows **Approved by voice** with **Undo** for a few seconds before it goes.

Tapping **Approve** works too.

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
