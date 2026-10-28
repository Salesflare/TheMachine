---
title: Google Meet
area: connections
summary: Transcripts and Gemini notes of Meet meetings you organize. It only reads.
covers: connector:google_meet
code: connectors/google_meet.py
site: Connect, More sources, Remove
---
## What it reads

Transcripts and Gemini notes of Google Meet meetings you organized, once Meet has made them: the last 7 days when you connect, then new ones as they come in. Meet keeps them for 30 days.

Meet only makes them when transcripts or Gemini notes were turned on during the meeting.

Each one is matched to the meeting in your calendar at the same time. Gemini's notes show in that meeting's Notes and the transcript in its Transcript, marked **From Google Meet**, next to anything you added there; they never replace it.

## What it can do

Nothing in Meet or Drive. It only reads, and it never turns on transcripts itself.

## Connect it

1. In Google Cloud, turn on the Google Meet API and the Google Drive API.
2. In the OAuth Playground, get an access token with the two read-only scopes shown on the connect screen.
3. On a hosted Machine: open your setup page at app.themachine.computer/setup, go to **More sources** and open Google Meet. On your own computer: **Connections**, **+ Add**, Google Meet, or `assistant connect google_meet`.
4. Paste the token and press **Connect**.

The token expires after about an hour. When Connections says it was rejected, paste a new one.

## Remove it

- In the dashboard: **Connections**, open Google Meet, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Google

Open myaccount.google.com/permissions and remove the OAuth Playground's access.
