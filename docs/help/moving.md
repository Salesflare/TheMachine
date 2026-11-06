---
title: Move to another computer
area: getting-started
summary: Export everything your Machine knows in one encrypted file, and import it on another Machine, hosted or your own.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Everything your Machine learns belongs to you: messages, to-dos, drafts, the Graph, memories and skills. Take it all to another Machine, or keep a copy.

## Export

On your own computer:

1. In **Settings** › **General** › **Export**, press **Export** next to Everything.
2. Optionally pick a passphrase. Without one, you get an export code: write it down, the import needs it.
3. Optionally turn on **Include keys and tokens** (needs a passphrase), so you don't have to connect your sources again.
4. Press **Start export**, then **Download**. The file is deleted after 24 hours, or at once with **Delete**.

On a hosted Machine, **Export** next to Everything opens your account page. Press **Export everything**, then **Download**. Your Machine deletes the file after 24 hours, or at once with **Delete it now**.

The file is always encrypted. Settings then lists what is in it and what isn't. Google and Microsoft accounts connected through our hosted sign-in need signing in again on the other side.

## Import

1. In **Settings** › **General** › **Export**, press **Choose file** next to Import and pick the export.
2. Type its passphrase or export code and press **Open**. The Machine checks the whole file first.
3. Hosted: press **Import now**. On your own computer: press **Replace with this export**, then **Replace**. The Machine restarts with it in a few minutes, and Settings says **Imported**.

The import replaces what that Machine has now, after keeping a copy. Nothing goes out by itself: queued sends wait for you.

If Settings can't restart The Machine on your computer, it shows the commands to run instead.

On a new computer, [install The Machine](self-hosted-setup.md) first. Then cancel your hosted plan if you no longer need it: see [Cancel or delete](cancel-and-delete.md).
