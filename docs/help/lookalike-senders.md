---
title: Lookalike senders
area: security
summary: Mail from an address that imitates someone you deal with is flagged on its to-do, and drafts never go to it.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
---
## What it catches

Some scams come from an address that looks like one you know: `examp1e.com` for `example.com`, `example-billing.com`, or one letter off. The Machine compares each sender's domain with the ones you already deal with. When the newer one only looks like a known one, it counts as a lookalike.

The same name at another ending, like `example.nl` next to `example.com`, is the same organization, not a lookalike. Free mail like gmail.com never counts.

## On a to-do

A to-do about such a message says so plainly, like "This isn't Alex. It came from examp1e.com, not example.com." The sender shows as the bare address, without a picture or a link to the person it imitates.

## What The Machine won't do

- It never gives a lookalike sender a role in your Graph.
- It never merges them with the person they imitate, and never suggests it under **Same person?**.
- A reply it prepares goes to the address on record, not the lookalike one.

Your own choice always wins: you can still give them a role, merge them or write to any address.
