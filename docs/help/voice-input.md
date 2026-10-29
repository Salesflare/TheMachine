---
title: Voice input
area: cards
summary: Talk instead of typing. What you say lands in the message box for you to check, and nothing is sent.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Talk instead of typing

Tap the mic in a message box: a to-do's chat, **New to-do**, **Help**, or the box to change a draft. Talk, then tap the check mark. Or hold the mic while you talk and let go when you're done.

While it listens, the box shows a timer. Tap the cross to stop without keeping anything. A recording can be up to 2 minutes; at 2 minutes it stops by itself and writes down what you said. What it heard so far shows in the bar as you talk, so the text is there soon after you stop.

What you said lands in the box, where your cursor was. Nothing is sent: read it, change what you like, and send it yourself.

## Where your voice goes

In **Settings**, **General**, under **Voice input**, one short line says which one is in use.

- **Automatic** (the default): when OpenAI is set up in OpenClaw, your recording is turned into text by OpenAI. That's an API key, or a ChatGPT sign-in where your plan allows audio. Without OpenAI, it's turned into text on your Machine itself and never leaves it.
- **On this Machine**: always on your Machine, even when OpenAI is set up.
- **With OpenAI**: always OpenAI.

A recording is deleted as soon as the text is back.

## Getting ready

To turn speech into text itself, your Machine needs a speech model, 150 to 500 MB. It downloads it in the background, at a low priority, once it's set up, its first review is done and it has been quiet for a while. Settings says **Getting ready (in the background)** meanwhile. It never does this when OpenAI is in use.

Until it's ready, **Automatic** uses your browser's own speech recognition where your browser has one, and says so under the box. Some browsers send that to their maker. With **On this Machine** picked, your recording waits, and the box shows "Getting voice ready…" with the time left.

## Settings

- **Turned into text**: **Automatic**, **On this Machine** or **With OpenAI**.
- **Accuracy** (on your Machine only): **More accurate** works best for most languages. **Faster** is quicker but gets more words wrong. On a Standard server, which has less memory, **Faster** is the default.
- **Language**: **Detect** works for every app language. Picking yours is a little faster.

To talk with The Machine instead, out loud, see [Talk live](talk-live.md).

## When it doesn't work

- **The microphone is blocked**: allow the microphone for this site in your browser's settings. In the phone app, it's under the app's permissions.
- **No microphone found**: connect one and try again.
- **Can’t reach your Machine**: your recording is kept and written down when your Machine is back. To try sooner, tap **Try now**.
- **I didn’t catch anything**: talk a little closer to the mic, or longer.
