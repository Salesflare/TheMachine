---
title: To-do chat
area: cards
summary: Ask about a to-do or change its draft, in a chat that belongs to that to-do.
covers: card-chat
code: dashboard.html, assistant.py, chat_files.py, corrections.py
order: 4
---
## Open it

On a phone, tap the to-do's title. On a computer, press **See in chat ›** or the to-do's chat link. Clicking the title on a computer renames the to-do.

## Emails in the chat

Each email shows only what is new in it. The earlier messages it quotes are folded under **Earlier messages**. **Read the thread** opens the emails in full.

## What it did

Each run shows as one quiet line, like "Checked 12 things". Open it to see each kind of step once, with how many times: "Used the browser on example.com · 7". It names the site, never the address, a command or a file.

When it stopped to ask you something, the question shows as a quiet line too, like "Asked: Send it today or Monday?", and your message under it shows only your answer.

## What to ask

Before you write, the chat may offer up to three taps made from this to-do, like "Offer Tuesday 10:00 instead". Tapping one puts it in the message box, to send or change. When nothing specific fits, there are none.

- About the thread, the people or the background: "What did they ask last time?"
- To change the draft: "Make it shorter" or "Mention the new date".

A question gets an answer and leaves the draft alone. Sending stays on the to-do's buttons: the chat never sends a draft in the same reply that wrote it. A change you ask for that reaches nobody else, like a cleanup in a doc, happens right away, with no extra Confirm. Anything beyond what you asked waits for your OK. A to-do with more than one step stays open until every step is done.

On a computer, Enter or Ctrl+Enter (Cmd+Enter on a Mac) sends and Shift+Enter starts a new line. On a phone, use the send button.

## When something is wrong

Say so in the chat, like "They're not the CEO" or "They left the company". The Machine fixes it at the source: a role, a company, a title, a project's stage, the to-do's project, or a rule it learned. The chat shows what changed, like "Fixed: Sam's role is Head of Sales, from their email signature", with **Undo**. Undo puts back the old value, unless it changed since.

Your other drafts built on the wrong value are drafted again, one at a time. Their chat says **Redoing the draft after a fix**. Drafts you edited or approved, and ones going out, stay as they are. The reply says how many of each.

On a GBrain page, only The Machine's own section changes. What you wrote there stays. When it can't tell where something came from, it learns from your note instead.

## Model and thinking

Under the message box, the chat shows its model and thinking level, like "GPT-6.1 Sol" and "Low thinking". Tap either to pick another for this chat only. New chats use what you set in **Settings**, **Model** (see [Model](model.md)).

**Fast**, at the end of the model menu, makes to-do chats answer quicker, at about twice the cost (or twice as much of your plan). It covers the messages you send and Do it, in all your to-do chats, never background work. It's off by default, and grayed out for a model without it.

## Stop a reply

While a reply is being written, the send button turns into **Stop**. Stop ends it at once and keeps what it wrote so far, marked **Stopped**. Write a new message to carry on, or tap **Try again**.

## Add files

Tap the paperclip, paste a screenshot, or drop files on the chat. Each file shows above the message box, and × takes it back. A message can be only files.

- Images (PNG, JPEG, GIF, WebP) up to 5 MB go to the model as images.
- PDFs, text, spreadsheets (CSV) and Office files up to 10 MB: The Machine reads them and can attach them to a draft.
- Up to 5 files per message.

Files stay on your Machine, encrypted like your messages. Files you add but never send are removed after a day. A new to-do can carry files too, from **New to-do** (see [Make one yourself](cards.md#make-one-yourself)).
