---
title: The mobile app
area: getting-started
summary: The Machine as an app on iPhone and Android: notifications for your to-dos, and sharing to The Machine from any app.
covers: mobile-app
code: notify.py, assistant.py, dashboard/new-todo.js, dashboard/settings-device.js
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
---
The mobile app opens your own dashboard, signed in as on the web.

## Connect it

On a hosted Machine the app signs in with your account. On a self-hosted one, open **Settings**, **General** on a computer: **Phone app** shows a code. Install the app, then scan it with the phone's camera, or type the address shown under it into the app. The app asks before it connects, and your Machine's own sign-in still applies.

## Notifications

The app asks to allow notifications when it first opens. Tap one to open its to-do. No text of a to-do passes through Apple, Google or The Machine's service: they only carry a fixed line, like "A to-do needs you".

On Android the app then asks your own Machine for the to-do's title and shows it, like "Ready: Reply about the listing". When it can't reach your Machine, it says how many wait, like "2 to-dos need you".

With **Text in notifications** off in **Settings**, **Security**, it keeps the fixed line. When your phone hides sensitive notification content on the lock screen, only the fixed line shows there. On iPhone the fixed line stays.

They follow the same rules as push on the web: what you picked per kind in [Notifications](notifications.md), your [work hours](work-hours.md), and nothing while you are using a dashboard.

Each phone with the app shows in **Settings**, **Notifications** as a **Phone with the app**. **Remove** stops its notifications. A self-hosted Machine needs The Machine Network for them; the app works without them.

## Share to The Machine

In any app, tap Share and pick The Machine. A **New to-do** opens with the text, link or files you shared in it. Check it, add a date if you like, and add it. Nothing is added until you do.

Plans and billing aren't shown in the app. **Open account** in **Settings** stays, to delete your account.
