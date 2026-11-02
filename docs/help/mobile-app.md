---
title: The mobile app
area: getting-started
summary: The Machine as an app on iPhone and Android: notifications for your to-dos, and sharing to The Machine from any app.
covers: mobile-app
code: notify.py, assistant.py, dashboard/new-todo.js, dashboard/settings-device.js
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
---
The mobile app opens your own dashboard, signed in as on the web. It works with a hosted Machine and with a self-hosted one paired with an account.

## Notifications

The app asks to allow notifications when it first opens. A notification only says that something waits, like a new to-do or a result, never what it is about: tap it to open the dashboard and read it there. No text of a to-do leaves your Machine for it: The Machine's service sends a fixed line through Apple or Google, so your to-dos stay off their servers and your lock screen.

They follow the same rules as push on the web: what you picked per kind in [Notifications](notifications.md), your [work hours](work-hours.md), and nothing while you are using a dashboard.

Each phone with the app shows in **Settings**, **Notifications** as a **Phone with the app**. **Remove** stops its notifications. A self-hosted Machine needs to be paired with an account for them.

## Share to The Machine

In any app, tap Share and pick The Machine. A **New to-do** opens with the text, link or files you shared in it. Check it, add a date if you like, and add it. Nothing is added until you do.

Plans and billing aren't shown in the app. **Open account** in **Settings** stays, to delete your account.
