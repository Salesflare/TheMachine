# The Machine for iOS and Android

A thin native app around the owner's own Machine. The dashboard is always loaded from the Machine itself, so a new
dashboard release reaches the app at once, with no store update. The app itself only holds:

- **The start page** (`www/`): Sign in, the offline page, and a small "Self-hosted?" link for a Machine of one's own.
- **Sign-in through the system** (`MachineShellPlugin`): the account's sign-in opens in the system's sign-in sheet
  (`ASWebAuthenticationSession` on iOS, a Custom Tab on Android), so passkeys, Face ID and saved Google or Microsoft
  sign-ins work. It comes back on `computer.themachine.app://signed-in` and the app opens the Machine.
- **Push**: native notifications through APNs and FCM. They are content-free wakeups ("New to-do"); on Android the
  app asks the Machine for the to-do's short line and shows that, and the rest is fetched when the owner opens it.
- **Share to The Machine**: text, links and up to 5 files from any app's share sheet open the dashboard's New to-do,
  filled in, for the owner to check and add. On Android, Open with The Machine on a PDF, an image or a text file does
  the same (a `VIEW` of a `content://` file). A name without its extension gets the one of its type (`ShareName`), since
  the Machine takes files by extension. The file goes from the phone to the owner's Machine only, when New to-do
  uploads it.
- **The phone's own questions**: the microphone (Talk, dictation) and notifications are asked by the phone itself when
  the owner taps the mic or Turn on. Only once the phone won't ask again does the dashboard show one line with
  Open settings, the app's page in the phone's settings (`machinePhone` in `www/inject.js`).
  While notifications are off, the home screen has one line with Turn on and an X (7 days); a first sign-in asks once.
- **The Machine's browser**: the dashboard's Browser pane, closed with its X or Back. Opened on its own (an older
  dashboard, a link straight to it) it gets a floating X back to the dashboard (`www/inject.js`).

Native code is kept small and stable on purpose: new features belong in the dashboard.

## How the app finds the Machine

| Owner | How |
|---|---|
| Hosted Machine | Sign in with the account (Google, Microsoft or passkey at themachine.computer). The account knows the Machine. |
| Self-hosted, on The Machine Network | The same sign-in: the Machine reports its Tailscale dashboard address to its owner's account only, and it is removed when they leave the Network. |
| Self-hosted, no account | "Self-hosted?" on the start page: scan the code in the dashboard's Settings, Phone app, or type its address: the `.ts.net` one, or the dashboard's own https domain (https on 443 or 8443, the default port; no other port; never an IP address). Before it is saved the app asks it for its manifest, so a typo or another site gets "That's not a Machine". Tailscale has to be on the phone when the address is on the tailnet. |

The app sign-in is bound to the app that started it: the app sends a challenge (SHA-256 of a random verifier) to
`app.themachine.computer/open?to=app&c=...`, and only that app can redeem the handoff it gets back (`&v=<verifier>`).
The cloud side is in the cloud repo's `docs/mobile-app.md`.

The WebView only opens the saved Machine (and, for a hosted Machine, other `*.app.themachine.computer` names after a
rename). Every other link opens in the system browser. Only the app's own start page can change the saved Machine.

## Push

1. The app gets a push token (APNs or FCM) and hands it to the Machine (`www/inject.js`, action `app_push_register`).
2. The Machine registers it with the account's push relay (cloud repo, `/api/fleet/app-push`). A self-hosted Machine
   only gets push when it is on The Machine Network; otherwise the app works without notifications and says so once.
3. When something needs the owner, the Machine asks the relay to wake the phone. The push carries a fixed text and a
   to-do id, never the content.
4. The app registers with `fetch`, and asks the saved Machine about the to-do (`GET api/notice?tag=`): its title
   ("Ready: <title>", at most 60 characters), next step (at most 120), buttons and their words, or `gone` for a
   to-do that no longer waits. No answer: the fixed text. The Machine's Text in notifications off gives the fixed
   text too. The lock screen with previews hidden shows the fixed text only.
5. Buttons: the notice lists them per kind (`QUICK` in `machine/delivery/push.py`; the app asks with `v=2` and the
   wakeup's kind, an older app gets Do it, Snooze and Mark done). Do it (a to-do not started yet), Snooze 2h,
   Snooze (until tomorrow) and Mark done are each the dashboard's own `decide` (`GET api/session` for the CSRF token,
   then `POST api/action` with the Machine's Origin and the sign-in), after unlocking, without opening the app; then
   the to-do's line says what happened ("Snoozed it"). Open, Open draft, Answer and Sign in open the app at the
   to-do. Nothing is sent from a notification: a draft or final step opens the app.
6. One notification per to-do (its id). When a to-do no longer waits (done, snoozed, not needed, here or anywhere),
   the Machine sends one `clear` wakeup without text (`app_clear_step`) and the app takes it away.
7. Android (`MachinePushService`, which replaces Capacitor's FCM service and still runs it): a data-only push (kind,
   ready or needs-you, the to-do id, the fixed text and a "{} to-dos need you" line), the notice with the WebView's
   cookies (over Tailscale for a Machine of their own), buttons in `NotificationActions` (Android 12+: unlock first; the opening ones open the app).
   No answer: the fixed text, or the count of that kind since the app was last opened. Words: `PushText` (tests:
   `PushTextTest`).
8. iOS: the relay's alert has `mutable-content`, and the Notification Service extension (`NotificationService/`,
   bundle `computer.themachine.app.notifications`) asks for the notice with the sign-in the app keeps in the app
   group's keychain (`Shared/MachineNotice.swift`, this device only). Buttons are a notification category per set of buttons (up to 16 kept), the
   running ones with `authenticationRequired`, the opening ones `foreground`, handled in `MachineActions` (`AppDelegate.swift`) in front of Capacitor's delegate.
   `clear` is a background push, which iOS may hold back: opening the app also takes away notifications for
   to-dos that no longer wait.

Tokens are per owner and revocable: signing out of the app, removing the phone in Settings, or leaving the Network
removes them.

## Building

```
cd mobile
npm ci
npm test
npm run sync      # the Capacitor CLI, pinned, through npx
```

**Android** (any OS): JDK 21 and the Android SDK (platform 36). `cd android && ./gradlew assembleDebug`. FCM needs
`android/app/google-services.json` from the Firebase project (not in git); without it the app works without push.

**iOS**: Xcode on a Mac: open `ios/App/App.xcodeproj`, team Salesflare, and run. The Share extension
(`ios/App/ShareExtension`) hands over through the app group `group.computer.themachine.app`.
The workflow **iOS app build** (Actions, Run workflow) checks the native code compiles on GitHub's Mac runners; it
never runs on its own, since macOS minutes cost 10x. With **upload** ticked it archives a signed build and uploads it
to TestFlight instead, signed through the App Store Connect API key in the repo secrets (`ASC_KEY_ID`,
`ASC_ISSUER_ID`, `ASC_KEY_P8`, `APPLE_TEAM_ID`); the build number is the run number.

## Store details

| | iOS | Android |
|---|---|---|
| Store name | The Machine Computer | The Machine Computer |
| Home screen name | The Machine | The Machine |
| ID | `computer.themachine.app` (Share: `computer.themachine.app.share`) | `computer.themachine.app` |
| Category | Productivity | Productivity |
| Icon | `ios/App/App/Assets.xcassets/AppIcon.appiconset` | `android/app/src/main/res/mipmap-*` |

Subtitle (iOS, 30 characters): *Your assistant for email, work*

Short description (Play, 80 characters): *Your own assistant for email and work, on your phone.*

Description:

> The Machine is your own assistant for email and work. This app opens your Machine on your phone: your to-dos,
> drafts and chat, with notifications when something needs you.
>
> Sign in with your account from themachine.computer. Running your own Machine? Connect it with its address.
>
> Share links, text and files from any app to add them as a to-do.

### Sign-in only

Accounts are created and paid for on the web. The app has no sign-up, plans, prices or buying links (App Store
3.1.3(b), multiplatform services): the start page only says "Use your account from themachine.computer" without a
link, and the dashboard hides every plan, billing and upgrade element when it runs in the app (its user agent ends in
`TheMachineApp/<n>`). Deleting the account stays reachable in the app (Settings, Account, Open account), as App Store
5.1.1(v) asks.

### Privacy labels (App Store) and Data safety (Play)

The app itself collects nothing for the developer: no analytics, no ads, no tracking. What the owner sees is their
own Machine.

| Data | Collected | Why | Linked to them | Tracking |
|---|---|---|---|---|
| Email address, name (account) | Yes | App functionality (sign-in) | Yes | No |
| Device ID (push token) | Yes | App functionality (notifications) | Yes | No |
| Emails, messages, files, contacts | Processed by the owner's own Machine; on a hosted Machine stored by The Machine for the owner | App functionality | Yes | No |

Play Data safety: data is encrypted in transit; the owner can ask for deletion (Settings, Account, Open account,
Delete account); no data shared with third parties; no data sold.

### Review notes (draft)

> The Machine is an assistant that runs on the customer's own Machine (hosted by us or self-hosted). This app is a
> companion: it signs in with an existing account and opens that account's Machine. Accounts are created and paid for
> on the web at themachine.computer; the app has no sign-up, prices or purchase links.
>
> Native features: system sign-in with passkeys (ASWebAuthenticationSession), push notifications for new to-dos,
> and a Share extension that adds shared links, text and files as a to-do.
>
> Demo account: on the sign-in page, tap App review at the bottom and sign in with the review account below. It opens
> a Machine with sample mail and to-dos.
> Account deletion: for a normal account, Settings, Account, Open account, Delete account. The review account itself is
> deleted by us after the review.

The review account is the existing reviewer account used for the AI app directory reviews, with its reviewdemo
Machine (sample mail and to-dos); its sign-in is given only in the store consoles.

### Policy risk

- Apple 4.2 (minimum functionality) and 2.5.2: a remote-loaded web app can be rejected as "a website in a wrapper";
  native push, passkey sign-in and the Share extension are what answer that, and 2.5.2 is not at risk since no code
  is downloaded into the app itself (the dashboard runs in the WebView like a web page).
- Apple 3.1.1/3.1.3(b): fine as long as nothing in the app steers to buying; the in-app mode hides it all.
- Google Play: remote web content is allowed (Webview spam policy targets apps that only show third-party sites);
  the account deletion URL and Data safety form are required.
