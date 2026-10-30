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

It knows the to-do you're in: its messages, its draft and its chat. It can also look up your other to-dos. Say "mark this as done", "snooze it" or "not needed" and it does that itself. Say "no, not that" right after to take it back.

It listens in your languages: the app's language and the ones your browser lists. A noise, a cough or a sound in another language gets no answer and stays out of the transcript.

The bar has **Mute** and **End**. Say goodbye, or that you're done, and it ends by itself. A conversation lasts up to 10 minutes. A minute before the end, the timer shows how much is left. Start it again to go on.

## Talk through all your to-dos

Tap **Talk** in the sidebar (in the menu on a phone) to go through everything that needs you, by voice. The Machine says how many are waiting and takes them one by one: **Ready** first, then **To decide**. It sees your other to-dos too, like the ones still **Preparing**, and tells you when one is ready.

Talk has its own page: one conversation from start to end, with the to-do it's talking about on top, its draft, and **Open the chat**. It doesn't move you from chat to chat.

Ask it to read a draft, change it, snooze it, mark it done, or move on to the next one. Sending works as in a to-do's chat: one draft per question, after a clear yes. What you say about a to-do goes into that to-do's chat. When a new to-do comes in, it mentions it at a pause. Say "add a to-do to..." and it adds a new one, without leaving the one you're on.

It reaches the rest of The Machine too. Ask about a person, an organization, a project, a meeting or a promise, and it looks it up and shows it. It can snooze, mark done, dismiss, rename or reopen a to-do, also one in **Done / dismissed**. For anything else, it adds a to-do, lets its chat handle it, and tells you the answer.

Meanwhile, other pages are fine: the bar stays at the bottom, and **Talk** in the sidebar brings you back. This conversation lasts up to 30 minutes. It keeps going in the background on computers and Android. On iPhone, it stops when the app leaves the screen.

## Ask for things, and send with a yes

When you ask for something, like "write a reply saying Thursday works" or "snooze this until Monday", The Machine hands it to the to-do's chat, as if you had typed it. The chat follows its usual rules: it can change the draft or snooze the to-do.

The chat can also look things up, like a store's opening hours on the web. It shows **Working on it…** meanwhile, and you can keep talking. When the answer is ready, The Machine tells you, and where it found it. Ask something else meanwhile and it waits its turn.

To send a draft, say so. The Machine asks first, naming who it goes to and how, like "Send this reply to Lotte by email?". It first reads the whole draft out: who it goes to, the subject and the text. So it works with your phone in your pocket, too. Answer with a clear yes, like "yes, send it", and that draft goes.

- It sends exactly the draft it read out. If the draft changes after the question, it reads it again and asks again. A question you don't answer within 3 minutes expires.
- If your answer isn't a clear yes, nothing is sent and it asks again. "No" sends nothing.
- A draft you already saw on screen, or heard in this conversation, isn't read out again: it only asks, like "Send it to Nick?".
- Say "send both" or "send all the ready ones" and it names everyone in one question. One yes sends each of them.
- Talk shows **Undo** and who it goes to, with a countdown for a few seconds before it goes, then **Sent to** that person. Tap it, or say "undo" or "wait".

Tapping **Approve** works too.

"Do it" starts The Machine on the to-do, as **Do it** does, browser work included. "Mark it done" closes it. Say "report a bug" and it sends a bug report, like **Report a bug** in Help, and asks first whether to add more.

## Pick a voice

In **Settings**, **General**, under **Voice input**, pick how The Machine sounds at **Voice**. Tap play to hear a sample. **Cedar** is the default. ChatGPT's Cove voice isn't available for Talk live.

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
- If it says it can’t make out your words, what you said didn’t come through twice in a row. Check your microphone, or type in the chat. It says this once, then waits until it hears you.
