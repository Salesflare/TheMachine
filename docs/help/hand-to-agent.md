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

## Set it up

In **Settings**, **General**, under **Coding agents**:

- **Claude Code session**: the address of a Claude Code session.
- **Codex cloud environment**: its environment id.
- **Runs on**, and optionally a **Branch**.

Claude sends its result back through The Machine connector. Add it once in claude.ai, Settings, Connectors, Add custom connector, with the address shown there. For Codex on a hosted Machine, press **Connect Codex** on your setup page first, under **Add more any time**. It uses the same ChatGPT plan as your model, and OpenAI asks for one more code, for Codex.

On a hosted Machine, Coding agents shows once GitHub or Codex is connected. It also shows on setups that run jobs elsewhere. More in the [agents guide](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
