---
title: Hand to Claude Code or Codex
area: cards
summary: Send a coding to-do to Claude Code or Codex. The result comes back on the to-do.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Hand off a to-do

1. On the to-do, open **More** and pick **Hand to Codex** or **Hand to Claude Code**. It shows when that tool is set up.
2. Check the summary and what it gets, add a note if you like, and press **Hand off**. **See the full job** shows the whole brief.

The to-do then shows that it's working, and the result when it's done, with **Show changes**. **Change** asks it for changes; **Hand off again** starts over.

A job never sends anything for you.

## In the Codex app

- **Open in Codex** opens the job's thread in the Codex app. While Codex works on it here, the app can't open it yet. It opens once it's done.
- **Change** on a thread that's open in the Codex app goes on in that same conversation there, and the to-do follows it.
- A job only stops when Codex does nothing for 30 minutes, or after 6 hours in all. A restart of The Machine doesn't stop it.

## Set it up

In **Settings**, **General**, under **Coding agents**:

- **Claude Code session**: the address of a Claude Code session.
- **Codex cloud environment**: its environment id, for Codex cloud.
- **Runs on**, and optionally a **Branch**.

Claude sends its result back through The Machine connector. Add it once in claude.ai, Settings, Connectors, Add custom connector, with the address shown there.

## Where Codex runs

On a hosted Machine, pick it on your setup page, under **Add more any time**, **Codex**:

- **On my computer** (the default): the job runs on your own computer, with the Codex signed in there. Nothing of Codex is on your server, and the job is encrypted for that computer only: the Network passes it on but can't read it. Install The Machine on that computer, pair it on your Account page, and run `codex login` there. Keep The Machine running on it. The job shows as a thread in the Codex app on that computer, and the result comes back on the to-do. When the computer is off, jobs wait until it's back.
- **Codex cloud**: the job runs in OpenAI's cloud. Press **Connect Codex**. It uses the same ChatGPT plan as your model, and OpenAI asks for one more code, for Codex. Then enter the Codex cloud environment in Settings.

On a hosted Machine, Coding agents shows once GitHub or Codex is connected. It also shows on setups that run jobs elsewhere. More in the [agents guide](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
