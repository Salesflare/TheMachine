---
title: WhatsApp
area: connections
summary: Your WhatsApp chats, read as a linked device. Replies only after you approve.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## What it reads

Your WhatsApp chats, as a linked device of your phone's WhatsApp, like WhatsApp on a computer. When you connect it, WhatsApp also sends your older chats, often years of them. Your Machine keeps all of it, and only messages from the last 7 days turn into to-dos.

A photo, voice message or file without a caption shows as what it is, like "Sent image". WhatsApp's own notices, such as the encryption notice or someone joining a group, have no text and are left out.

## Read photos

Off until you turn it on. In **Connections**, open WhatsApp, then **Details**, and turn on **Read photos** and The Machine reads the photos in your work chats: a receipt, a screenshot, a photo of a letter or a form. **Also in personal chats** reads the ones in your personal chats too. A chat is work or personal the way sharing sees it, so a chat with family stays personal.

The Machine downloads each photo once and keeps it on your Machine like an email attachment: encrypted when message protection is on, and deleted when its message goes. Its own model reads what the photo shows and the text in it. That counts as part of the message, never as instructions. JPEG, PNG and WebP up to 5 MB. A one-time code in a photo is left out.

The to-do and the message show the photo. Tap it to see it large.

## What it can send

A text into a chat that already exists, only after you approve it on the to-do. A reply to the WhatsApp message a to-do came from quotes that message when more was said after it, or in a group; the draft says **As a reply**.

If a to-do came in by email but you talk to that person on WhatsApp, say so in the to-do's chat. The Machine finds your existing chat with them and switches the draft to WhatsApp, for you to review and send. It never starts a new chat.

WhatsApp doesn't offer an official way to do this. Reading and an occasional reply you approved is very unlikely to cause trouble; mass or automated sending can get an account blocked.

## Connect it

On a hosted Machine:

1. In the dashboard, open **Connections**, then **+ Add**, and pick WhatsApp.
2. Press **Show the QR code**.
3. On your phone, in WhatsApp, open Settings, Linked devices, Link a device, and scan the QR code.
4. WhatsApp shows as connected within a minute. Your chat history keeps coming in after that, and its card counts the messages while it does.
   If connecting takes too long, it says so after a few minutes. Press **Try again** to pick up where it stopped.

Setting up on your phone, with no second screen to scan from? Open **On your phone? Link with a code instead**, enter your number and press **Get a code**. WhatsApp then asks for that code.

On your own computer: open **Connections**, then **+ Add**, pick WhatsApp, enter your phone number with its country code and press **Connect**. It shows a code. On your phone, in WhatsApp, open Settings, Linked devices, Link a device, then **Link with phone number instead**, and enter the code.

Or run `assistant connect whatsapp` and scan the code it shows in the terminal. The first time, it offers to install the WhatsApp connector, a pinned build checked against its checksum ([source](https://github.com/Salesflare/wacli)).

Under Linked devices, it shows as The Machine. A Machine linked before keeps its old name there until you link it again.

## Pictures

The Machine asks WhatsApp for the profile pictures of people in your graph who have none, at most 50 a day, through the sync that keeps WhatsApp up to date. Nothing is sent to them. Someone who hides their picture from you stays without one.

## Remove it

- On a hosted Machine: press **Remove** next to it on your setup page. Your Machine unlinks itself and deletes what it kept for WhatsApp.
- On your own computer: **Connections**, open WhatsApp, **Details**, then **Disconnect**. Then unlink it on your phone too.

## Unlink it in WhatsApp

On your phone, in WhatsApp, open Settings, Linked devices, tap your Machine and log out.
