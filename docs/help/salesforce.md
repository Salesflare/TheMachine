---
title: Salesforce
area: connections
summary: Deals, tasks and activity from Salesforce on your people and projects. It can keep contact details current there, if you turn that on.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## What it reads

New deals, and deals that move to another stage or change amount. Your open tasks, calls and other tasks logged as done with notes, and meetings with a description. The last 7 days when you connect, then new ones every 15 minutes.

Each deal becomes a project in your Graph, and the contacts on it show up on their people, as a Salesforce contact at their account.

## What it can change

Nothing, until you turn on **Update contact details**. Your Salesforce sign-in stays on your Machine.

## Connect it

On a hosted Machine:

1. Open your setup page at app.themachine.computer/setup and go to **More sources**.
2. Open Salesforce and press **Connect Salesforce**.
3. Sign in to Salesforce and allow The Machine (made by Salesflare).

Or in the dashboard: **Connections**, **Customers**, pick Salesforce and press **Sign in with Salesforce**.

Your Salesforce user needs API access, which most editions include.

## Update contact details

When your Machine knows newer details for one of your Salesforce contacts, it can update the contact there: job title, phone, and the LinkedIn link if your org has a LinkedIn field on contacts.

1. In **Connections**, open Salesforce and press **Show what would change**.
2. Check the list, then press **Turn on**, or **Not now**.

What it follows:

- Only details in the person's own words, like their LinkedIn or Slack profile, or ones you set on their page. Never a guess.
- Only when the detail is newer than the contact's last change in Salesforce. An edit made there wins.
- Only fields that differ, and never a blank. It never changes the email address or the account.
- Each change is a dated line on the person's page.

Press **Turn off** to stop. A connection your Fleet shares only reads.

## Remove it

- In the dashboard: **Connections**, open Salesforce, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Revoke it in Salesforce

In Salesforce, open your personal settings, then Connected Apps OAuth Usage, or ask your admin, and revoke The Machine. It can no longer read or change anything.
