---
title: Connect other AIs
area: connections
summary: Let Claude, ChatGPT, Cursor, Codex or GBrain read your to-dos and Graph over MCP, each with its own access and expiry.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## What another AI can do

Other AIs can connect to your Machine over MCP: Claude, ChatGPT, Cursor, Codex, GBrain and others. They can read your to-dos, promises, team briefs and the people and companies in your Graph.

At most they add a to-do, or a to-do with an email draft. A draft waits in your Machine until you read it and press Send yourself. A connected AI never sends anything and never acts for you. Your Machine's own Do it and agents are not part of this.

## Connect one

In the other AI, add a custom connector or MCP server with your Machine's address followed by `/mcp`. On a hosted Machine that is `https://<your name>.app.themachine.computer/mcp`. On a Machine on your own computer it is your dashboard's address, which only devices in your tailnet reach.

The AI sends you to your Machine to sign in. Your Machine shows which AI it is. An AI it can't recognize shows the address it came from: connect only if you just started this yourself.

Pick what it can do, **Read** or **Read & draft**. With both Work and Personal accounts, pick what it can see. Then pick for how long: **1 day**, **7 days**, **30 days** or **1 year**. Press **Connect**, or **Cancel** to send it back with nothing.

## What it sees

A connection sees only its area. Work covers your work accounts' to-dos and promises, work people, companies, projects and your Work Fleet's team brief. Personal covers the rest. Message text stays on your Machine: an AI sees a to-do's sources by sender, subject and date only.

Teammates' Team Graph records never go to an outside AI.

## In Settings

Open **Settings**, **AIs** to see each AI that connected, with when it was last used and how many calls it made. Change its access, its area or how long it lasts there. The next call uses it. **Turn off now** ends every sign-in it has at once. **Activity** lists every call, refused ones too. **Remove** takes it away.

An AI that can't sign in by itself can use a key. Under **Add a key**, name it, pick the access and how long, and press **Make key**. Copy the key right away: it shows only once. The AI sends it as `Authorization: Bearer <key>`.

## Keep it safe

Every call is logged, refused ones too. A connection that expired or is off is refused until you change it. Signing in uses OAuth with PKCE. Your Machine keeps only a fingerprint of each token, so a copy of its data opens nothing.
