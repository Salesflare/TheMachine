---
title: Android notifications
area: connections
summary: The notifications on your Android phone, through the OpenClaw app. It only reads.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
---
## What it reads

The notifications on your Android phone, through the OpenClaw app. One-time codes stay out, and so do WhatsApp, Telegram, Signal and Discord notifications.

## What it can do

Nothing on your phone. It only reads notifications.

## Connect it

On a hosted Machine:

1. Install OpenClaw from Google Play on your phone.
2. In the dashboard, open **Connections**, then **+ Add**, pick Android phone and press **Show a setup code**.
3. In the OpenClaw app, add a Gateway and scan the code. Back in the dashboard, press **Approve**.
4. Allow notification access when the app asks. Then turn on Forward Notification Events in the app's settings, so notifications come in as they arrive, not only at the check every 10 minutes.

On your own computer, pair the phone in the OpenClaw app, then run `assistant connect android`.

## Remove it

- In the dashboard: **Connections**, open Android, **Details**, then **Disconnect**.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Remove it on the phone

Turn off notification access for the OpenClaw app in Android's settings, or unpair the phone in the OpenClaw app.
