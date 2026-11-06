---
title: ChatGPT
area: connections
summary: Sign in with ChatGPT to run your Machine on your ChatGPT plan, and import your ChatGPT skills.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## What it is for

Sign in with ChatGPT and your Machine reads and drafts with it, on your own ChatGPT plan. The Machine has no AI of its own: requests go straight to OpenAI, under your account and their terms.

## Sign in

On a hosted Machine, press **Sign in with ChatGPT** on your setup page and enter the code it shows at ChatGPT. Signed out later? Press **Reconnect ChatGPT**.

OpenAI turns the code down? Open your [ChatGPT security settings](https://chatgpt.com/settings/security), scroll to the bottom and turn on the switch "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Then enter the code again.

Don't see that switch? On a work account (Business, Enterprise or Edu), your ChatGPT admin turns it on in [Permissions & roles](https://chatgpt.com/admin/permissions), under "Codex and Work Local".

On your own computer, run `openclaw models auth login` in a terminal.

## Usage limits

A ChatGPT plan has a 5-hour and a weekly limit. **Settings**, **Model** shows how much of each is used and when it resets. Background work pauses well before a limit, to keep room for your own chats. When a limit is reached, the top of the dashboard says when it resets. See [Model](model.md).

## Import your ChatGPT skills

In **Settings**, **Skills**, press **Import**, pick **From ChatGPT** and press **Find my skills**. Only their instructions come in. See [Skills](skills.md).

## Remove it

Pick another model on your setup page (or, on your own computer, sign in to another provider the same way). To cut its access on OpenAI's side, sign out of the session in your ChatGPT security settings.
