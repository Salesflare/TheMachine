---
title: GitHub
area: connections
summary: Review requests, mentions, assignments and failed CI runs. Files issues only when you confirm.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## What it reads

Your GitHub notifications: review requests, mentions, assignments, replies and failed CI runs. It never marks them as read.

## What it can do

Reading never changes anything on GitHub. When a to-do ends in a GitHub step, like filing an issue, the to-do says so and the step runs only after you tap **Confirm**, or when you asked for exactly that in its chat. Screenshots go in through your Machine's browser. Without GitHub connected, the to-do says it will use the browser and shows **Connect GitHub**.

## Connect it

On a hosted Machine:

1. Open **Connections**, then **+ Add**, and pick GitHub.
2. Pick **Work** or **Personal** and press **Sign in with GitHub**.
3. Press **Open GitHub ↗**, enter the code it shows and allow it. It connects by itself.

Your setup page at app.themachine.computer/setup has the same sign-in under **More sources**.

On your own computer:

1. Open **Connections**, then **+ Add**, and pick GitHub.
2. Pick **Work** with its company, or **Personal**, and press **Connect**.
3. If asked, press **Open GitHub ↗**, enter the code and allow it. It connects by itself.

Or run `assistant connect github` and confirm your GitHub login.

## Remove it

- Open **Connections**, then GitHub, **Details** and **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on GitHub

On GitHub, open Settings, Applications, Authorized OAuth Apps and revoke GitHub CLI. On your own computer, `gh auth logout` also signs it out.
