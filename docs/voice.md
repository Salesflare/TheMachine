# Voice input

The mic in the dashboard's message boxes (a to-do's chat, New to-do, Help, and changing a draft) writes what the owner
says into the box. It never sends anything: the owner reads it, edits it and sends it. The help article is
[docs/help/voice-input.md](help/voice-input.md); the code is `voice_input.py`, `voice_worker.py` and the `mic*`
functions in `dashboard.html`.

## How a clip travels

1. The browser records with `MediaRecorder` (Opus at 32 kbps where the browser has it), at most 2 minutes. Tap to start and tap the check mark to
   stop, or hold the mic and let go. The cross cancels and nothing goes anywhere.
2. The browser decodes the clip and turns it into 16 kHz mono 16-bit WAV (about 1.9 MB a minute after base64), then
   posts it as `voice_transcribe` with the `X-Upload: voice` header, which allows a larger body for that one action
   only.
3. The service checks the WAV (`voice_input.pcm`) and turns it into text with the engine the owner picked, and the
   dashboard puts the text in the box at the cursor.

The browser's own speech recognition (`SpeechRecognition`) is never used: in Chrome it sends the audio to Google, and
Firefox doesn't have it. A clip is only in memory on the Machine (for the OpenAI engine, also in a private file for
the seconds the call takes), never stored, and the log has only its length.

## Engines

- **On this Machine** (the default): [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 1.2.1 on CTranslate2,
  int8 on the CPU, in `voice_worker.py`. The service starts the worker on the first clip and stops it after 5 minutes
  without one, so its memory is free again. Clips go through it one at a time. The language is the one picked in
  Settings, or detected among the app's seven languages.
- **With OpenAI**: the owner's own OpenAI API key in OpenClaw, through `openclaw infer audio transcribe` with
  `gpt-4o-transcribe`. Offered only when `openclaw infer audio providers` says OpenAI is configured with a key. A
  ChatGPT (Codex) sign-in doesn't give access to OpenAI's audio API.

## First use, sizes and speed

Nothing is added to the install or the prebuilt images, so installs are as fast as before. The first tap on the mic
prepares the local engine in the background while the dashboard shows "Getting voice ready…" with its progress, and the
clip is written down when it's done:

| Step | Download | On disk |
|---|---|---|
| A virtualenv in `<data>/voice/env` with the packages in `voice-requirements.txt` (wheels only, every one pinned by hash) | about 100 MB (Linux arm64), 130 MB (Linux x86-64), 60 MB (macOS arm64) | about 470 MB |
| The model, from Hugging Face at a pinned revision, every file checked against its SHA-256 | small: 484 MB; base: 145 MB | the same |

That took 25 s on a desktop with a fast connection (packages 15 s, model 10 s); a small hosted server takes a few
minutes. A release that changes `voice-requirements.txt` prepares the packages again on the next use. It needs 2 GB of
free disk space to start.

Settings, Accuracy picks the model. Measured on a 4-core desktop CPU limited to 2 cores, under heavy load from other
work (load average 10 to 27), int8:

| Model | 7 sentences in 7 languages (60 s of speech) | 34 s of Dutch | Peak memory | Quality |
|---|---|---|---|---|
| small (**More accurate**, the default) | 0.5 to 1.5 × real time | 26 s (2 threads), 11 s (4 threads) | 640 MB | Good in all seven languages |
| base (**Faster**) | 0.4 × real time | 10 s | 350 MB | More words wrong, most of all in Dutch and Portuguese |

End to end through the service (worker already running, 4 threads, same load), the small model wrote a 10 s Dutch clip
in 10.6 s with the language detected, a 9 s English clip in 5.5 s, and 34 s of Dutch in 9.5 s. Each clip costs at least
one 30 s window of work, so short clips are relatively slower; detecting the language adds a little.

whisper.cpp (`pywhispercpp`, small q5_1) was tried too: slower and less steady on x86 CPUs at the same quality, so
faster-whisper it is.

## Errors

The dashboard says what to do when the microphone is blocked or missing, when the browser can't record, when the
Machine can't be reached (the clip is kept in the page and **Try again** sends it again), when preparing fails (no
`python3-venv`, no internet, not enough disk space, a download that doesn't match its hash), and when nothing was heard.
At 2 minutes recording stops by itself and the clip is written down.
