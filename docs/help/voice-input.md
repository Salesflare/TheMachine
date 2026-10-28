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

While it listens, the box shows a timer. Tap the cross to stop without keeping anything. A recording can be up to 2 minutes; at 2 minutes it stops by itself and writes down what you said.

What you said lands in the box, where your cursor was. Nothing is sent: read it, change what you like, and send it yourself.

## The first time

The first time you tap the mic, your Machine gets voice ready. It downloads the speech model once, 150 to 500 MB, and says "Getting voice ready…" with how far it is. That takes a few minutes. Your recording waits and is written down as soon as it's ready.

## Where your voice goes

By default your recording is turned into text on your Machine itself. It never leaves it, and it is deleted as soon as the text is back. Your browser's own speech recognition isn't used, because in some browsers that sends your voice to the browser maker.

In **Settings**, **General**, under **Voice input**, you can choose:

- **Turned into text**: **On this Machine**, or **With OpenAI**. OpenAI is faster on a small server, but your recording goes to OpenAI with your own key. It needs an OpenAI API key in OpenClaw. A ChatGPT sign-in doesn't include it.
- **Accuracy**: **More accurate** works best for most languages. **Faster** is quicker but gets more words wrong. On a Standard server, which has less memory, **Faster** is the default.
- **Language**: **Detect** works for every app language. Picking yours is a little faster.

## When it doesn't work

- **The microphone is blocked**: allow the microphone for this site in your browser's settings. In the phone app, it's under the app's permissions.
- **No microphone found**: connect one and try again.
- **Can’t reach your Machine**: your recording is kept and written down when your Machine is back. To try sooner, tap **Try now**.
- **I didn’t catch anything**: talk a little closer to the mic, or longer.
