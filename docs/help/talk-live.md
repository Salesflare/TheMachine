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

In a to-do's chat, tap the wave next to the mic and allow the microphone if asked. When the bar says **Live**, talk as on a call. The Machine answers out loud. Talk over it to interrupt.

It knows this to-do: its messages, draft and chat, and it can look up your other to-dos. Say "mark this as done", "snooze it until tomorrow at 9" or "not needed" and it does it. Say "no, not that" right after to take it back. Times follow your [Work hours](work-hours.md) time zone.

It listens in the app's language and the languages your browser lists. Coughs, noise and other languages get no answer and stay out of the transcript.

The bar has **Mute** and **End**. Say goodbye and it ends by itself. A conversation lasts up to 10 minutes, with a countdown in the last minute. Start again to go on.

## Talk through all your to-dos

Tap **Talk** in the sidebar (in the menu on a phone). The Machine says how many to-dos wait and takes them one by one: **Ready** first, then **To decide**. It tells you when one still **Preparing** is ready.

Talk has its own page: the to-do it's on sits on top, with its draft and **Open the chat**.

Ask it to read a draft, change it, snooze it, mark it done or go to the next one. What you say about a to-do goes into its chat. It mentions new to-dos at a pause. Say "add a to-do to..." to add one without losing your place.

Ask about a person, organization, project, meeting or promise, and it looks it up and shows it. It can also dismiss, rename or reopen to-dos, also ones in **Done / dismissed**. For anything else, it hands the question to a new to-do's chat and tells you the answer.

It remembers your earlier talks with it. Ask "what did I decide about the offsite?" and it tells you, and when you said it. Only Talk in the sidebar does this.

Other pages are fine meanwhile: the bar stays at the bottom, and **Talk** brings you back. This conversation lasts up to 30 minutes. It keeps going in the background on computers and Android. On iPhone, it stops when the app leaves the screen.

## Ask for things, and send with a yes

Ask for something, like "write a reply saying Thursday works", and The Machine passes it to the to-do's chat as if you typed it. The chat follows its usual rules.

The chat can also look things up, like a store's opening hours. It shows **Working on it…** and you can keep talking. When the answer is ready, The Machine tells you, and where it found it.

To send a draft, say so. The Machine reads it out (who it goes to, the subject and the text) and asks, like "Send this reply to Sam by email?". It works with your phone in your pocket. Say a clear yes, like "yes, send it", and that draft goes.

- It sends exactly the draft it read. If the draft changes, it reads and asks again. A question you don't answer within 3 minutes expires.
- Anything but a clear yes sends nothing.
- A draft you already saw or heard isn't read again. It only asks, like "Send it to Pat?".
- Say "send all the ready ones" and it names everyone in one question. One yes sends them all.
- After a yes, Talk shows **Undo** with a countdown. Tap it, or say "undo" or "wait".
- Once sent, Talk says "Sent." and the to-do shows **Sent to** that person with the time. If it failed, Talk says why. Ask "is it sent?" any time: it checks, never guesses.

Tapping **Approve** works too.

Say "do it" to start The Machine on the to-do, like **Do it**. Say "report a bug" to send a bug report, like **Report a bug** in Help.

## Pick a voice

In **Settings**, **General**, under **Voice input**, pick a **Voice** and tap play to hear it. **Cedar** is the default. ChatGPT's Cove voice isn't available.

## A record in the chat

Everything said goes into the to-do's chat, under a **Talked live** line, to read back later.

## What you need

Talk live uses OpenAI's voice, so your Machine needs one of these:

- A ChatGPT sign-in: included in plans that offer it.
- An OpenAI API key: OpenAI charges it per minute, and the bar says so. With both, your Machine uses the key.

**Settings**, **General**, **Voice input** shows whether Talk live is ready. Without OpenAI, the wave doesn't show. Your audio goes from your browser straight to OpenAI.

## When it doesn't work

- **The microphone is blocked**: allow the microphone for this site in your browser's settings.
- **Talk live couldn’t start**: check your ChatGPT sign-in or OpenAI key and try again.
- **Talk live lost its connection**: start again. What was said stays in the chat.
- It says it can't make out your words: check your microphone, or type in the chat.
