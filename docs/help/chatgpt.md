---
title: ChatGPT
area: connections
summary: Sign in with ChatGPT to run your Machine on your ChatGPT plan, and import your ChatGPT skills.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## What it is for

ChatGPT is the model that reads and drafts for you, on your own ChatGPT plan. The Machine has no AI of its own. Your Machine's requests go from your server straight to OpenAI, under your account and their terms.

## Sign in

On a hosted Machine, on your setup page, press **Sign in with ChatGPT** and type the code it shows at ChatGPT. Signed out later? Press **Reconnect ChatGPT**.

OpenAI turns the code down? Open your [ChatGPT security settings](https://chatgpt.com/settings/security), scroll to the bottom and turn on the switch "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Then enter the code again.

Not there? On a work account (Business, Enterprise or Edu), a workspace admin turns it on in [Permissions & roles](https://chatgpt.com/admin/permissions), under "Codex and Work Local". One switch covers both codes: if your model's code worked, the Codex code works too.

On your own computer, sign OpenClaw in to ChatGPT with `openclaw models auth login`.

## Usage limits

A ChatGPT plan has a 5-hour and a weekly limit. **Settings**, then **Model**, shows how much of each is used and when it resets. Background work stops well before a limit, to keep room for your own chats. When a limit is reached, the top of the dashboard says which one and when it resets, and work picks up after. See [Model](model.md).

## Import your ChatGPT skills

In **Settings**, **Skills**, press **Import**, pick **From ChatGPT** and press **Find my skills**. It reads the skills you made, in your Machine's browser. Only instructions come in. See [Skills](skills.md).

## Remove it

Pick another model on your setup page, or sign OpenClaw in to another provider. To end its access on OpenAI's side, sign out of the session in your ChatGPT security settings.
