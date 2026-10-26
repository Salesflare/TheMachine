---
title: Telegram
area: connections
summary: Get cards on Telegram, with the same buttons as the dashboard, through a bot of your own. Optional.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## What it does

Telegram is a way to get your cards, not something The Machine reads. Your own bot sends each card within your [work hours](work-hours.md), with the same buttons as the dashboard: **Do it**, **Snooze**, **Change**, **Mark done**, **Not needed**, and **Send** for a prepared message.

Telegram is optional. The dashboard as a phone app sends the same cards as notifications.

## What it can send

Only messages to you, from your own bot. A message to anyone else still needs your approval on the card.

## Connect it

On a hosted Machine:

1. In Telegram, message @BotFather and send /newbot. Copy the token it gives you.
2. On your setup page, under **Add more any time**, open Telegram, paste the token and press **Add my bot**.

It's not part of setup: add it whenever you like. Your dashboard suggests it once a snoozed card would only come back there.

On your own computer, the installer asks for it, or run `assistant telegram on` with your Telegram user ID.

## Remove it

- On a hosted Machine: press **Disconnect Telegram** on your setup page. Your bot and its token are removed from your server.
- On your own computer: `assistant telegram off`. Add `--remove-bot` to also forget the bot.

## Delete the bot in Telegram

Message @BotFather, send /deletebot and pick your bot.
