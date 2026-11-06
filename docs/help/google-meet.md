---
title: Google Meet
area: connections
summary: Transcripts and Gemini notes of Meet meetings you organize. It only reads.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## What it reads

Transcripts and Gemini notes of Google Meet meetings you organized, once Meet has made them: the last 7 days when you connect, then new ones as they come in. Meet keeps them for 30 days.

Meet only makes them when transcripts or Gemini notes were turned on during the meeting.

Each one lands on its meeting in your Calendar: Gemini's notes under Notes, the transcript under Transcript, marked **From Google Meet**. What you added yourself stays.

## What it can do

Nothing in Meet, Docs or Drive. It only reads, and it never turns on transcripts itself.

## What it asks for

Its own OK, separate from your mail. Google asks to let The Machine:

- See your Google Meet meetings, their transcripts and Gemini notes.
- See your Google Docs, to read the Gemini notes doc.

It never asks for your Drive. Your Gmail and Calendar access stay as they are.

## Connect it

It doesn't need Gmail connected. To connect it:

- Hosted Machine: in the dashboard, open **Connections**, **+ Add**, pick **Google Meet** and press **Sign in with Google**. Give the OK above, and you're back in the dashboard.
- Your own computer, paired with your account: the same steps. The sign-in opens in a new tab.

Without the Meet OK it isn't added. There is nothing to paste or renew.

If the OK is taken back later, Google Meet in **Connections** asks you to sign in again.

## Remove it

In the dashboard: **Connections**, open Google Meet, **Details**, then **Disconnect**. What it already brought in stays.

## Revoke it in Google

Open myaccount.google.com/permissions and remove The Machine's access to Google Meet. Gmail and Calendar keep working.
