---
title: Stripe
area: connections
summary: Failed payments, disputes, cancellations and big new subscriptions. It only reads.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## What it reads

Events on your Stripe account that may need you: failed payments, disputes, cancellations and big new subscriptions, with the customer they belong to. A customer's email links the event to that person and their organization in the [Graph](graph.md).

## What it can do

Nothing in Stripe. It never writes, refunds or retries a payment. The Machine's Stripe app asks Stripe for read permissions only, and Stripe shows them before you install it.

## Connect it

Sign in with Stripe, the easy way:

1. In the dashboard: **Connections**, **+ Add**, Stripe. Or on a hosted Machine's setup page at app.themachine.computer/setup: **More sources**, Stripe. On your own computer, pair it with your account first.
2. Press **Sign in with Stripe**. Stripe asks which account, and shows what The Machine may read.
3. Press **Install**. You're back where you started, and Stripe is connected.

Or paste a restricted key instead:

1. In Stripe, create a restricted key with Read on Events, Customers and Account, and None on everything else.
2. Find your account ID (acct_...) under Settings, Business details.
3. Open Stripe as above (or run `assistant connect stripe`), open **Or paste a restricted key**, paste the account ID and the key, then press **Connect**.

On your own computer, when Sign in with Stripe isn't available yet, + Add says so and opens this form straight away.

## Connect it once for your team

In a Work Fleet, an owner or admin connects Stripe once and shares it with the team:

1. Connect Stripe on your own Machine (above). The Fleet tab's **Shared connectors** box also has **Connect Stripe**.
2. On the Fleet tab, open **Share Stripe**. Everyone is ticked; untick who shouldn't get it. Press **Share**.

Teammates' Machines read it too, read only. Under Connections it says who shared it, and only the Fleet's admins can change or stop it. Your Machine renews their access every hour, so while it is off for longer, their Stripe pauses until it is back. Nobody ever gets your sign-in itself. Details: [Fleets](fleet.md).

A Stripe connection that goes through another service with one key for many connections can't be shared: that key opens more than Stripe. Connect Stripe on its own for the team instead.

## Remove it

- In the dashboard: **Connections**, open Stripe, **Details**, then **Disconnect**. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.
- Shared with a Fleet: **Stop sharing** on the Fleet tab first.

## Revoke it in Stripe

- Signed in with Stripe: in Stripe, open Settings, Installed apps, and remove The Machine.
- Restricted key: in Stripe, open Developers, API keys, and delete or roll the key.
