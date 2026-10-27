---
title: Salesflare CRM
area: connections
summary: Accounts, contacts and deals, so it knows who matters. It reads with your API key.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## What it reads

Your accounts, contacts and deals in Salesflare, and the account feeds: colleagues' emails that don't involve you, and meetings with notes.

## What it can change

Nothing, unless you set `join_pipelines` in your Machine's settings file. Then it adds you to accounts in those pipelines by itself. It is empty by default.

## Connect it

1. In Salesflare, open [Settings, API keys](https://app.salesflare.com/#/settings/apikeys) and create a key.
2. On a hosted Machine: open your setup page at app.themachine.computer/setup, go to **More sources**, open Salesflare CRM, paste the key and press **Connect**.
3. On your own computer: run `assistant connect crm`, or **Connections**, **+ Add**, Salesflare CRM. After **Connect**, your Machine restarts and opens the Salesflare card, which first says it's finding the accounts with recent emails and meetings, then how many it has read.

## Sync details

Its card under **Connections**, **Other sources** shows how far it is: how many accounts it has read in this round, and how many it skipped because Salesflare was too slow to answer. A round that runs for hours says it may be stuck.

- **Stop**: nothing new comes in until you press **Start**. It goes on where it was.
- **Restart sync**: drops the round it is on, with its errors, and reads the last week again now. Nothing it brought in is lost.
- **API keys**: opens Salesflare's API keys page, to make a new key.

## Remove it

- In the dashboard: **Connections**, open Salesflare, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Salesflare

Delete the API key in Salesflare, under Settings, API keys.
