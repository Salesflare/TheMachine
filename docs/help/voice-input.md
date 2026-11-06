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

While it listens, the box shows a timer and what it heard so far. Tap the cross to stop without keeping anything. A recording stops by itself at 2 minutes.

The text lands in the box, where your cursor was. Nothing is sent: read it, change what you like, and send it yourself.

## Where your voice goes

Pick it in **Settings**, **General**, under **Voice input**. A short line there says which one is in use.

- **Automatic** (the default): OpenAI turns it into text when your Machine uses OpenAI (an OpenAI key, or a ChatGPT plan that allows audio). Otherwise your Machine does it itself and the recording never leaves it.
- **On this Machine**: always on your Machine, even when OpenAI is set up.
- **With OpenAI**: always OpenAI.

A recording is deleted as soon as the text is back.

## Getting ready

To turn speech into text itself, your Machine first downloads a speech model (150 to 500 MB) in the background, when it's quiet. Settings says **Getting ready (in the background)** meanwhile. It skips this when OpenAI is in use.

Until then, **Automatic** uses your browser's own speech recognition if it has one, and says so under the box. Some browsers send that to their maker. With **On this Machine** picked, your recording waits, and the box shows "Getting voice ready…" with the time left.

## Settings

- **Turned into text**: **Automatic**, **On this Machine** or **With OpenAI**.
- **Accuracy** (on your Machine only): **More accurate** works best for most languages. **Faster** is quicker but makes more mistakes, and is the default on a Standard Machine.
- **Language**: **Detect** works for every app language. Picking yours is a little faster.

To talk with The Machine instead, out loud, see [Talk live](talk-live.md).

## When it doesn't work

- **The microphone is blocked**: allow the microphone for this site in your browser's settings. In the phone app, it's under the app's permissions.
- **No microphone found**: connect one and try again.
- **Can’t reach your Machine**: your recording is kept and written down when your Machine is back. To try sooner, tap **Try now**.
- **I didn’t catch anything**: talk closer to the mic, or a little longer.
