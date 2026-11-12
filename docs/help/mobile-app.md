---
title: The mobile app
area: getting-started
summary: The Machine as an app on iPhone and Android: notifications for your to-dos, and sharing to The Machine from any app.
covers: mobile-app
code: notify.py, assistant.py, file_text.py, dashboard/new-todo.js, dashboard/settings-device.js, dashboard/setup-card.js, dashboard/settings-apps.js, sw.js, manifest.webmanifest
order: 3
keywords: ios, android, app store, play store, share sheet, share, phone, mobile, push
---
The mobile app opens your own dashboard, signed in as on the web. Get it on the [App Store](https://apps.apple.com/app/id6829875215) for iPhone and iPad, or on [Google Play](https://play.google.com/store/apps/details?id=computer.themachine.app) for Android.

The **Get more out of The Machine** to-do at the top of To-dos suggests it. In a phone's browser, **Get it** opens the store. On a phone set to show desktop sites, it shows both store links. On a computer it shows a QR code to scan with your phone, and links to both stores.

On any phone, [themachine.computer/app](https://themachine.computer/app) opens the right store. **Settings**, **Apps** has both stores at the top, or just your phone's store on a phone. On a computer, **Computer** installs the dashboard as an app: see [Install the app](phone-app.md).

## Connect it

On a hosted Machine the app signs in with your account. On a self-hosted one, open **Settings**, **Apps** on a computer: under the stores, **Not on the Network?** shows a code. Install the app, then scan it with the phone's camera, or type the address shown under it into the app. The app asks before it connects, and your Machine's own sign-in still applies.

## Notifications

The app asks to allow notifications when it first opens. Tap one to open what it is about: a to-do opens its chat, the morning opens today in the **Calendar**, the team brief opens To-dos, and a Fleet question opens its to-do. No text of a to-do passes through Apple, Google or The Machine's service: they only carry a fixed line, like "A to-do needs you".

The app then asks your own Machine for the to-do's title and next step, like "Reply to Sam" with "Send to Sam: Tuesday 10:00 works". The morning gets what waits and your first meeting's time, the team brief its first items, a Fleet update what happened. When it can't reach your Machine, the fixed line stays. On Android it says how many wait, like "2 to-dos need you".

A notification has **Snooze** (until tomorrow) and **Mark done**, and **Do it** for a to-do not started yet. They work after you unlock the phone, without opening the app. Sending and final steps always open the app. One notification per to-do: "Preparing" turns into "Ready", and it goes away once the to-do is done or snoozed, here or anywhere.

When a step you confirmed goes through, its notification says **Done** and what happened, until you tap **Got it** on To-dos. On iPhone that can wait until you next open the app.

With **Text in notifications** off in **Settings**, **Security**, it keeps the fixed line. So does a lock screen that hides notification content. When there's nothing it may show, it says "Tap to open." If your phone can't reach your Machine when one comes in, it shows the details once it's back online.

They follow the same rules as push on the web: what you picked per kind in [Notifications](notifications.md), your [work hours](work-hours.md), and nothing while you are using a dashboard.

Each phone with the app shows in **Settings**, **Notifications** as a **Phone with the app**. **Remove** stops its notifications. A self-hosted Machine needs The Machine Network for them; the app works without them.

## Share to The Machine

In any app, tap Share and pick The Machine. A **New to-do** opens with the text, link or files you shared in it. Check it, add a date if you like, and add it. Nothing is added until you do.

A file alone is enough, like an invoice or a letter. Your Machine reads a PDF's text and fills in the to-do: what it is, the next step and its date. The file goes straight to your Machine and stays there.

The dashboard installed as an app on Android takes shares too: pick it in the share sheet the same way.

Plans and billing aren't shown in the app. **Open account** in **Settings** stays, to delete your account.
