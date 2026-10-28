---
title: WhatsApp
area: connections
summary: Your WhatsApp chats, read as a linked device. Replies only after you approve.
covers: connector:whatsapp
code: onboarding.py, next_actions.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## What it reads

Your WhatsApp chats, as a linked device of your phone's WhatsApp, like WhatsApp on a computer. When you connect it reads the last 7 days.

A photo, voice message or file without a caption shows as what it is, like "Sent image". WhatsApp's own notices, such as the encryption notice or someone joining a group, have no text and are left out.

## What it can send

A text into a chat that already exists, only after you approve it on the to-do.

If a to-do came in by email but you talk to that person on WhatsApp, say so in the to-do's chat. The Machine finds your existing chat with them and switches the draft to WhatsApp, for you to review and send. It never starts a new chat.

## Connect it

On a hosted Machine:

1. In the dashboard, open **Connections**, then **+ Add**, and pick WhatsApp.
2. Press **Show the QR code**.
3. On your phone, in WhatsApp, open Settings, Linked devices, Link a device, and scan the QR code.

Setting up on your phone, with no second screen to scan from? Open **On your phone? Link with a code instead**, enter your number and press **Get a code**. WhatsApp then asks for that code.

On your own computer: open **Connections**, then **+ Add**, pick WhatsApp, enter your phone number with its country code and press **Connect**. It shows a code. On your phone, in WhatsApp, open Settings, Linked devices, Link a device, then **Link with phone number instead**, and enter the code.

Or run `assistant connect whatsapp` and scan the code it shows in the terminal. Without wacli, it offers to install the pinned build from [Salesflare/wacli](https://github.com/Salesflare/wacli), checked against its checksum.

## Pictures

The Machine asks WhatsApp for the profile pictures of people in your graph who have none, at most 50 a day, through the sync that keeps WhatsApp up to date. Nothing is sent to them. Someone who hides their picture from you stays without one.

## Remove it

- On a hosted Machine: press **Remove** next to it on your setup page. Your server unlinks itself and deletes what it kept for WhatsApp.
- On your own computer: **Connections**, open WhatsApp, **Details**, then **Disconnect**. Then unlink it on your phone too.

## Unlink it in WhatsApp

On your phone, in WhatsApp, open Settings, Linked devices, tap your Machine and log out.
