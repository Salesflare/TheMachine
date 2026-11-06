---
title: Settings
area: settings
summary: Where to find each setting, from light mode to security and your account.
covers: settings:general
code: dashboard.html
order: 1
---
Open **Settings** with the gear at the top. Its tabs:

- **Account**: **Your addresses** (the ones that count as you) and **Sign out**, at the top. On a hosted Machine also your plan, invoices, Fleet, friends, sign-in and data, with **Cancel plan** and **Delete account** at the very bottom. See [Plans and billing](plans-and-billing.md).
- **General**: language and region, this device, voice input, your Machine's browser, your Fleet, export and import, and your account.
- **Security**: Standard or Careful. See [Security levels](security-levels.md). Also **Support access**, while it's on: see [Get support](get-support.md#support-access).
- **Activity**: everything The Machine did for you, newest first. See [Activity](activity.md).
- **Notifications**: what reaches you where, and your work hours. See [Notifications](notifications.md) and [Work hours](work-hours.md).
- **Writing**: signatures and how you write. See [Writing](writing.md).
- **Skills**: how-tos your Machine follows. See [Skills](skills.md).
- **Apps**: The Machine's phone apps, then Claude, ChatGPT and other AIs you connected, and what each may do. See [The mobile app](mobile-app.md) and [Connect other AIs](ai-connections.md).
- **Model**: the AI that reads and drafts for you, and its limits. See [Model](model.md). Also **Codex and Claude Code**: see [Hand to Claude Code or Codex](hand-to-agent.md).

A tab with nothing to show is hidden.

## General

- **Language and region**: your **Region** sets how dates, times and numbers read (Oct 24 or 24 Oct). **Time format** picks 12-hour (2:05 PM) or 24-hour (14:05). To-dos, Telegram, the digest and Fleet messages follow both. A hosted Machine starts from the time zone you picked at signup.
- **Language**: English, Nederlands, Français, Deutsch, Español, Italiano or Português (Brasil). It starts from your browser's language. The dashboard, Help, notifications, Telegram, the weekly recap and the to-dos your Machine writes switch from the moment you pick it. Older text stays as it was. Teammates get Fleet and Family questions in their own language, and drafts to other people stay in the language of their conversation.
- **This device**: **Install app**, **Notifications** with **Send a test**, and **Light mode**, for this browser or phone only. See [Install the app and turn on notifications](phone-app.md).
- **Voice input**: how what you say becomes text, and the voice of Talk live. See [Voice input](voice-input.md) and [Talk live](talk-live.md).
- **Open the Machine’s browser ↗**: the browser your Machine uses for sites like LinkedIn.
- **Fleet rules**: see [Sharing rules](sharing-rules.md).
- **Export**:
  - **Everything**: everything your Machine knows in one encrypted file, to move or to keep, and **Import** to bring one in. See [Move to another computer](moving.md).
  - **Knowledge for another AI**: what your Machine learned in files any AI can read. See [Knowledge for another AI](knowledge-export.md).

## On this Machine

When your Machine runs on your own computer, a few things are done there, in a terminal:

- The settings file, `config.json`: every setting in one place. Restart the Machine after a change.
- `assistant connect`: add a source, like `assistant connect gmail` or `assistant connect outlook`.
- `assistant telegram on` or `off`: messages on Telegram. See [Telegram](telegram.md).
- `assistant doctor`: checks everything and prints a fix for each problem.

## Your addresses

Every address of yours the Machine found: your accounts, Gmail or Outlook aliases, your calendar, your Slack and Intercom profiles. Mail and meetings from any of them count as you. **Remove** one that isn't yours.

A shared address, like info@ or a Google Group, never counts by itself. One the Machine isn't sure about waits under **Maybe yours**. Choose one:

- **Mine: only I answer it**: it counts as yours. Mail to it can become your to-dos.
- **The team’s: others answer it too**: it isn't you. Mail that only went to it makes no to-dos or drafts for you. It still fills in the Graph.
- **Not mine**: it won't count as yours.

Pick by who answers it today. A team inbox like support@ is the team's. One like partnerships@ that only you answer is yours. Switch it once others answer it too.

**Change** on its row switches it later. Your own sign-in address is always yours.

### Your company's domains

The domains of your own addresses count as your company's. Using another one too, like acme.co next to acme.com? Type it under **Your company’s domains** and press **Add**.

People there are then colleagues, never clients: their threads stay out of the Team Graph, and no organization is made for it. **Remove** takes it out again. Free email domains like gmail.com can't be added.

A Gmail alias of yours can also be the **From** of a draft, when Gmail confirms you can send as it. See [Gmail](gmail.md#what-it-can-send).
