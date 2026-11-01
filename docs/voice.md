# Voice input

The mic in the dashboard's message boxes (a to-do's chat, New to-do, Help, and changing a draft) writes what the owner
says into the box. It never sends anything: the owner reads it, edits it and sends it. The help article is
[docs/help/voice-input.md](help/voice-input.md); the code is `voice_input.py`, `voice_worker.py` and the `mic*`
functions in `dashboard/todos-chat.js`. Spoken conversations are a different feature: [Talk live](talk-live.md).

## How a clip travels

1. The browser records with `MediaRecorder` (Opus at 32 kbps where the browser has it), at most 2 minutes. Tap to start and tap the check mark to
   stop, or hold the mic and let go. The cross cancels and nothing goes anywhere.
2. The browser decodes the clip and turns it into 16 kHz mono 16-bit WAV (about 1.9 MB a minute after base64), then
   posts it as `voice_transcribe` with the `X-Upload: voice` header, which allows a larger body for that one action
   only.
3. While the owner talks, the browser also cuts the recording at pauses (`MIC_PART`: after 6 s, at a pause of 0.7 s,
   by 25 s at the latest) and posts each part as `voice_transcribe` with `part`, so after the check mark only the last
   few seconds are left. The bar shows what was heard so far. The parts are joined in order; if one fails, the whole
   clip goes instead. Parts keep the first part's language when the owner didn't pick one.
4. The service checks the WAV (`voice_input.pcm`) and turns it into text with the engine the owner picked, and the
   dashboard puts the text in the box at the cursor.

**Never stored.** A clip is only in memory on the Machine (for the OpenAI engine, also in a private file for the seconds
the call takes), and the log has only its length.

**The browser's own recognition** (`SpeechRecognition`) is used in one case only: on **Automatic**, without OpenAI,
while the Machine's own engine isn't ready yet (`voice_status`'s `use` is `browser`). The box then says "Your browser
writes this one down.". In Chrome it sends the audio to Google, so it's never used with **On this Machine** picked.
Where a browser doesn't have it (Firefox) the clip waits for the Machine instead.

## Engines

Settings, Voice input, **Turned into text** (`voice_input.ENGINES`), with one short line saying which one is in use
(`voice_status`'s `in_use`):

- **Automatic** (the default): OpenAI when the Machine has OpenAI access that can transcribe, else this Machine.
  `voice_input.engine_for` decides. OpenAI access is checked at start and every 5 minutes (kept 10 minutes), so OpenAI
  connected later switches to it by itself, and a Machine with OpenAI never downloads the local model. When OpenAI
  refuses a clip (a ChatGPT plan without audio), the service stops offering it for an hour and uses this Machine.
- **On this Machine**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 1.2.1 on CTranslate2,
  int8 on the CPU, in `voice_worker.py`. The service starts the worker on the first clip and stops it after 5 minutes
  without one, so its memory is free again. The package install runs at a lower priority (`nice -n 10`,
  below-normal priority on Windows); the worker runs at the normal priority, since the owner is waiting on it. Clips go through it one at a
  time. The language is the one picked in Settings, or detected among the app's seven languages.
- **With OpenAI**: `gpt-4o-transcribe` through OpenClaw's own transcription, in `voice-openai-run.mjs`: a Node worker
  that loads OpenClaw once and stays up for 5 minutes, so a clip takes 1 to 3 s instead of the 8 s the
  `openclaw infer audio transcribe` CLI needs to start (still the fallback). A tap on the mic warms it up. Offered when
  `openclaw infer audio providers` says OpenAI is configured. That's an OpenAI API key, or the ChatGPT (Codex) sign-in:
  OpenClaw's docs say its batch transcription can use the ChatGPT OAuth profile "when the account permits it". OpenAI's
  own Sign in with ChatGPT docs only describe the Responses API, so a plan without audio gets a clear error and
  **Automatic** falls back to this Machine.

## Getting ready ahead of time

Nothing is added to the install, setup or the prebuilt images, so a new Machine sets up as fast as before. The local
engine is prepared ahead of time by `voice_warm_worker`, never during setup:

- only when the Machine will use it: **On this Machine** picked, or **Automatic** without OpenAI access;
- only once the Machine is live: its first full review finished;
- only when it has been quiet for 15 minutes (3 checks, 5 minutes apart, with no review or preparation running and a
  load average under half the cores), on a Standard server as on a desktop;
- only when the disk check passes (2 GB free); after a failure it waits 6 hours before trying again;
- at a lower priority (`nice -n 10`). A release that changes `voice-requirements.txt` prepares the packages again the
  same way.

Settings shows "Getting ready (in the background)" while it runs. A tap on the mic never waits on it when there's
another way: OpenAI when available, else on **Automatic** the browser's own speech recognition where it has one. Only
with **On this Machine** picked (or a browser without speech recognition) does the clip wait, with "Getting voice
ready…" and the time left, estimated from the download's pace.

## Sizes and speed

What the local engine downloads, once:

| Step | Download | On disk |
|---|---|---|
| A virtualenv in `<data>/voice/env` with the packages in `voice-requirements.txt` (wheels only, every one pinned by hash) | about 100 MB (Linux arm64), 130 MB (Linux x86-64), 60 MB (macOS arm64) | about 470 MB |
| The model, from Hugging Face at a pinned revision, every file checked against its SHA-256 | small: 484 MB; base: 145 MB | the same |

That took 25 s on a desktop with a fast connection (packages 15 s, model 10 s); a small hosted server takes a few
minutes. The 2 GB disk check runs before anything downloads, and the dashboard says so if there isn't enough.

Settings, Accuracy picks the model. The default is **small** on Machines with 6 GB of memory or more (desktops,
Bigger servers) and **base** below that (Standard servers have 4 GB and 2 cores; see [On a Standard server](#on-a-standard-server)).

Measured on a 4-core desktop CPU limited to 2 cores, under heavy load from other work (load average 10 to 27), int8:

| Model | 7 sentences in 7 languages (60 s of speech) | 34 s of Dutch | Peak memory | Quality |
|---|---|---|---|---|
| small (**More accurate**) | 0.5 to 1.5 × real time | 26 s (2 threads), 11 s (4 threads) | 640 MB | Good in all seven languages |
| base (**Faster**) | 0.4 × real time | 10 s | 350 MB | More words wrong, most of all in Dutch and Portuguese |

End to end through the service (worker already running, 4 threads, same load), the small model wrote a 10 s Dutch clip
in 10.6 s with the language detected, a 9 s English clip in 5.5 s, and 34 s of Dutch in 9.5 s. Each clip costs at least
one 30 s window of work, so short clips are relatively slower; detecting the language adds a little.

### Time from the check mark to the text

Measured on a desktop Machine (OpenAI through a ChatGPT sign-in, busy with other work), clip length to the
time the service took:

| | 9 s English | 10 s Dutch | 34 s Dutch |
|---|---|---|---|
| OpenAI before: the `openclaw infer` CLI, about 8 s of it starting up | 7.3 s | 7.4 s | 12.3 s |
| OpenAI now: the worker, warm | 2.5 s | 1.4 s | 2.5 s |
| On this Machine (small), worker loaded on the clip | 10.0 s | 6.1 s | 13.9 s |
| On this Machine (small), worker warm | 9.8 s | 7.7 s | 17.3 s |

With parts, only the tail is left after the check mark: 1.7 s for 6 s with OpenAI, about 7 s on this Machine (each
clip costs one 30 s window, so short tails don't get faster locally). The worker's first start, 3 to 7 s, happens
while the owner talks.

### On a Standard server

A Standard server (Hetzner CAX11 or CX23: 2 vCPU, 4 GB, 2 GB swap) was matched with a systemd scope limited to 2 CPUs
(`CPUQuota=200%`), 4 GB of memory and 2 GB of swap, on an x86 desktop that was busy with other work at the same time
(load average 10 to 17). Inside it ran an OpenClaw 2026.10.5 Gateway, a headless Chromium with one page and a stand-in
for the service's own 320 MB, about 1.5 GB of anonymous memory before any voice:

| | base | small |
|---|---|---|
| 10 s of Dutch | 4.2 s | 9.1 to 17.2 s |
| 9 s of English | 2.4 s | 6.1 to 9.5 s |
| 34 s of Dutch | 6.4 to 7.4 s | 17.1 to 26.2 s |
| 2 minutes, mixed languages | 57 to 96 s | 109 to 154 s |
| Worker's peak memory (short clip / 2 minutes) | 320 / 480 MB | 610 MB / 1.1 GB |
| Scope's peak memory | 2.4 GB | 2.4 to 3.3 GB |

There was no OOM kill with either model, but with small the 2-minute clip took longer than the recording and its 1.1
GB peak leaves little room next to a running review on a 4 GB server, so base is the default there. Its words are
right in English and mostly right in Dutch; an owner who wants small on a Standard server can still pick it.

With `nice -n 10`, a busy review thread sharing one core with a transcription kept about 80% of that core (81% and
80% in two runs); without it, about 40% (37% and 40%).

whisper.cpp (`pywhispercpp`, small q5_1) was tried too: slower and less steady on x86 CPUs at the same quality, so
faster-whisper it is.

## Errors

The dashboard says what to do when:

- the microphone is blocked or missing, or the browser can't record;
- the Machine can't be reached: the clip is kept in the page, the offline bar shows, and the clip is sent when the
  Machine is back or on the bar's **Try now**;
- preparing fails: no `python3-venv`, no internet, not enough disk space, or a download that doesn't match its hash;
- nothing was heard.

At 2 minutes recording stops by itself and the clip is written down.
