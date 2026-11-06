---
title: Salesflare CRM
area: connections
summary: Accounts, contacts and deals, so it knows who matters. It reads with your API key.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## What it reads

Your accounts, contacts and deals in Salesflare, and each account's feed: colleagues' emails you weren't on, and meetings with notes.

## What it can change

Nothing. (On your own computer, the `join_pipelines` setting can make it add you to accounts in chosen pipelines. It's off by default.)

## Connect it

1. In Salesflare, open [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) and create a key.
2. On a hosted Machine: open your setup page at app.themachine.computer/setup, go to **More sources**, open Salesflare CRM, paste the key and press **Connect**.
3. In the dashboard: **Connections**, **+ Add**, Salesflare CRM, paste the key and press **Connect**. It then shows how many accounts it has read.

## Sync details

Under **Connections**, **Other sources**, Salesflare shows how far it is: accounts read this round, and any skipped because Salesflare was too slow. A round that runs for hours says it may be stuck.

- **Stop**: nothing new comes in until you press **Start**. It goes on where it was.
- **Restart sync**: starts over and reads the last week again. Nothing it brought in is lost.
- **API keys**: opens Salesflare's API keys page, to make a new key.

## Remove it

- In the dashboard: **Connections**, open Salesflare, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Salesflare

Delete the API key in Salesflare, under Settings, API keys.
