---
title: Knowledge for another AI
area: settings
summary: Take what your Machine learned to any other AI, as plain Markdown, JSONL and CSV files.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Everything your Machine learns belongs to you. Take it to another AI, or keep it, even if you stop using The Machine.

## Export it

1. In **Settings** › **General**, press **Export** next to **Knowledge for another AI**.
2. Leave **Message text** off to export only where each thing came from, and when. Turn it on to add the text.
3. **Private and Careful** stays off unless you want Only-you projects, private threads and Careful Fleets in it too.
4. Optionally set a **Passphrase** of at least 10 characters to encrypt the file.
5. Press **Download**. The file is made on your Machine and can be downloaded once.

On a hosted Machine it works the same, from your Machine's own Settings. On your own computer, `assistant export-knowledge` makes the same file.

## What's in it

- People, organizations and projects: one Markdown page each, with how they relate.
- Facts and preferences: what your Machine knows, about you and about them.
- Rules, how you write and signatures: what your drafts follow.
- Skills: your how-tos, on and off.
- Context: team briefs, summary lines, promises and open to-dos.
- Sources: where each thing came from, by id and date.

Records are JSONL, contacts and to-dos also CSV. A README.md at the top explains the layout and tells an AI how to use it. Give the folder, or the zip, to the AI as a knowledge file or project.

## What stays out

Passwords, keys and sign-ins never go in. Something that looks like a key is replaced. Teammates' and other Machines' data, settings and photos stay out too. For a full copy to move your Machine, see [Move to your own computer](moving.md).

The format is open and versioned: see [the schema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
