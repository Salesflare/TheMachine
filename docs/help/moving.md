---
title: Move to another computer
area: getting-started
summary: Export everything your Machine knows in one encrypted file, and import it on another Machine, hosted or your own.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Everything your AI learns belongs to you: messages, conversations, to-dos with their history, drafts, the Graph, memories, skills and agent jobs. You can take it all with you, also when you stop using The Machine.

## Export

On your own computer:

1. In **Settings** › **General** › **Export**, press **Export** next to Everything.
2. Optionally pick a passphrase. Without one, you get an export code: write it down, the import needs it.
3. Optionally turn on **Include keys and tokens** (needs a passphrase), so your sources don't need connecting again.
4. Press **Start export**, then **Download**. The file is deleted after 24 hours, or at once with **Delete**.

On a hosted Machine, **Export** next to Everything opens your account page. Press **Export everything**, then **Download**. Your Machine deletes the file after 24 hours, or at once with **Delete it now**.

The file is always encrypted. After an export, Settings lists what is in it, with counts, and what is not in it and why. Google and Microsoft sign-ins through the hosted service always need a new sign-in on the other side.

## Import

1. In **Settings** › **General** › **Export**, press **Choose file** next to Import and pick the export.
2. Type its passphrase or export code and press **Open**. The Machine checks the whole file first.
3. Hosted: press **Import now**. The Machine restarts with it in a few minutes. On your own computer: press **Replace with this export**, then **Replace**. The Machine restarts with it in a minute or two, and Settings says **Imported**.

The import replaces what that Machine has now and keeps a copy of it first. Nothing that was waiting goes out by itself: sends that were queued wait for you to send them again.

Advanced: on a computer that runs The Machine without a service manager, Settings shows the commands instead. You can also run them yourself: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

On a new computer, [install The Machine](self-hosted-setup.md) first. Then cancel your hosted plan if you no longer need it: see [Cancel or delete](cancel-and-delete.md).
