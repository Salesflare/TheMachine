---
title: Knowledge for another AI
area: settings
summary: Take what your Machine learned to any other AI, as plain files any AI can read.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Everything your Machine learns belongs to you. Give it to another AI, like ChatGPT or Claude, or keep it.

## Export it

1. In **Settings** › **General** › **Export**, press **Export** next to **Knowledge for another AI**.
2. **Message text** is off by default: only where each thing came from, and when. Turn it on to add the text.
3. Turn on **Private and Careful** only to add Only-you projects, private threads and Careful Fleets.
4. Optionally set a **Passphrase** (at least 10 characters) to encrypt the file.
5. Press **Download**. The file can be downloaded once.

It works the same on a hosted Machine and on your own computer.

## What's in it

- People, organizations and projects: one Markdown page each, with how they relate.
- Facts and preferences: what your Machine knows, about you and about them.
- Rules, how you write and signatures: what your drafts follow.
- Skills: your how-tos, on and off.
- Context: team briefs, summary lines, promises and open to-dos.
- Sources: where each thing came from, by id and date.

Contacts and to-dos also come as spreadsheets (CSV). A README at the top tells the AI how to read it all. Upload the zip to the AI as a knowledge file or project.

## What stays out

Passwords, keys and sign-ins never go in. Teammates' data, settings and photos stay out too. To move your whole Machine, see [Move to another computer](moving.md).

For developers: [the file format](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
