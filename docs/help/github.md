---
title: GitHub
area: connections
summary: Review requests, mentions, assignments and failed CI runs. Files issues only when you confirm.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## What it reads

Your GitHub notifications: review requests, mentions, assignments, replies and failed CI runs. It never marks a notification as read.

## What it can do

Reading never changes anything on GitHub. When a to-do ends in a GitHub step, like filing an issue, that step runs with the same gh sign-in once you tap **Confirm**, and the to-do says so first. Screenshots still go in through your Machine's browser, since GitHub's own tool can't add images. Without GitHub connected, the to-do says it will use the browser, with **Connect GitHub**.

## Connect it

On a hosted Machine:

1. In the dashboard, open **Connections**, then **+ Add**, and pick GitHub.
2. Pick **Work** or **Personal** and press **Sign in with GitHub**.
3. It shows a code. Press **Open GitHub ↗**, enter the code and allow it. It goes on by itself.

Your setup page at app.themachine.computer/setup has the same sign-in under **More sources**.

On your own computer:

1. In the dashboard, open **Connections**, then **+ Add**, and pick GitHub.
2. Pick **Work** with its company, or **Personal**, and press **Connect**.
3. If your Machine isn't signed in to GitHub yet, it shows a code. Press **Open GitHub ↗**, enter the code and allow it. It goes on by itself.

Or run `assistant connect github` and confirm your GitHub login. The Machine checks it matches on every sync.

## Remove it

- In the dashboard: **Connections**, open GitHub, **Details**, then **Disconnect**. It stops reading. What it already brought in stays.
- On a hosted Machine you can also press **Remove** next to it on your setup page.

## Uninstall it on GitHub

Revoke the GitHub CLI's access in GitHub, under Settings, Applications, Authorized OAuth Apps. On your own computer, `gh auth logout` also signs the CLI out.
