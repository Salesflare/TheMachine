# Coding agents

A card can go to Claude Code or Codex. **Hand to Claude Code** and **Hand to Codex** sit with the card's other
actions when that tool is there. A small sheet opens (in the card chat, in the message box's place): **Hand to** with a
switch between the tools, one line of what it will do, chips for what it gets (the emails, the draft, `messages.md`,
links counted, never shown raw) and an optional note for the agent. **See the full job** shows the whole brief to read
or edit. It opens with the task, the card's next step (its Needs you line), then your note on the card word for word,
who it's about, what happened so far as background, the card's drafts and files, what done looks like and the limits.
Nothing goes without your **Hand off**.

The job runs in its own folder under the Machine's data folder (`agent-jobs/<job>/work`), with the card's messages in
`card/messages.md`, full text included, so it needs no mailbox of its own. A job that runs away from this computer
(Claude Code on your paired computer, Codex cloud) doesn't get that folder, so the messages are in the brief itself,
newest first, shortened to fit with a note where something is cut. The card shows its progress, then a short result with up to three of the files it made: the ones its answer names, never logs or `.pid` files. The full list and the rest stay folded under Details. The chat shows the same block. **Ask for
changes** sends a follow-up to the same job. Cancel stops it.

A job never sends anything for you. If it rewrites a message (`draft.md`), that text becomes the card's draft, and you
still send it with the card's own Send.

The CLIs keep their own sign-ins. The Machine never reads, copies or stores a Claude or ChatGPT credential.

## On your own computer

- **Claude Code** runs as a background session (`claude --bg`, named after the card) with Remote Control on. It is in
  `claude agents`, at claude.ai/code and in the Claude apps, where you can read it and keep talking to it. **Open in
  Claude** goes there. Claude Code asks once whether to trust the jobs folder: run `claude` in it and accept. Until
  then, jobs run as `claude -p` and only show on the card.
- **Codex** runs through the Codex app's own app server, so the job is a thread in the Codex app (named after the
  card), also from your phone through the app's remote access. **Open in Codex** opens it. Without the Codex app it
  uses `codex exec`, and the job only shows on the card. Nothing is approved for you: a command that needs approval is
  declined. If the job's thread is open in the Codex app, a follow-up from the card is queued there (`codex queue`),
  so the app runs it in the same conversation and the card follows that turn (`thread/turns/list`). An older Codex
  without `codex queue` goes on in a copy of the thread (`thread/fork`); if even that is refused, the card says to
  carry on in Codex. While The Machine runs a turn itself, the app can't open the thread yet, so **Open in Codex**
  says it opens when the turn is done.
- **On your other devices**: with remote connections on in the Codex app on this computer, **Open in Codex** from
  another device opens the thread on this computer through that connection (`codex://threads/<id>?hostId=...`). The
  job keeps running here. A plain thread link would look for it on the device you clicked it on.
- **Restarts**: on Linux, Codex's app server runs in a systemd user unit of its own. It keeps The Machine's own
  hardening (NoNewPrivileges, PrivateTmp, UMask) and environment, and it listens on loopback behind a token that only
  the job folder holds. An update that restarts The Machine doesn't stop the job: The Machine picks it up again when
  it is back, also for a follow-up the Codex app is running. Claude Code background sessions run on by themselves too.
- **Limits**: `timeout_minutes` is how long a Codex turn may go without any activity before it is stopped. A turn
  that keeps working runs on, up to 6 hours in all, counted from when the job started, across restarts.
- **Try again** carries on in the job's own thread or session, where it left off. It starts again from the brief only
  when that thread is gone. The card says in plain words why a job stopped.

## On a hosted Machine

A hosted Machine has no Claude Code or Codex of yours, so it hands the job on. Set it up in **Settings > Model >
Codex and Claude Code**.

- **Claude Code**: paste the link of a Claude Code session from claude.ai/code. The job goes to that session as a
  message (`claude -p <message> --cloud <session>`). That session can't reach your Machine, so it sends its result
  back through The Machine connector. Add it once in claude.ai: Settings, Connectors, Add custom connector,
  `https://app.themachine.computer/mcp`. It has one tool, `report_result`. Each job gets its own ticket, and the
  Network keeps only the ticket's hash and the sealed result until your Machine picks it up. A result that hasn't come
  back after two days shows as stopped.
- **Codex**: pick where it runs on the setup page (step **Codex**, **Where Codex runs**).
- **Codex, On my computer** (the default): the job runs on your own computer, which needs The Machine installed and
  paired with your account (Account page, Fleet, pair a Machine) and `codex login` done there. Your hosted Machine
  hands the brief to the Network with only a ticket's sha256 (`dispatch`). The brief is end to end: your hosted
  Machine seals it for that one computer's Network keys and signs it with its own (`network_crypto.seal`, bound to
  both Machines and the ticket), so the Network only relays an envelope it can't read, and deletes it once your
  computer takes it. Your computer asks for work every 30 seconds with its own device token, opens the brief with its
  private key (`network-keys.json`, which never leaves it), checks it was signed by your hosted Machine, and runs
  it as an ordinary local Codex job (a thread in the Codex app there), and reports its progress and result into
  that ticket. Your hosted Machine fetches it like a Claude result. Only your own paired computer can take the job, and
  no sign-in or token moves between the two. Both pin each other's keys the first time; if either one's keys change,
  nothing is sealed or opened until you pair the computer again. A computer that isn't signed in to Codex takes no jobs; set
  `"codex": {"serve": false}` in its config.json to never take any. A job that waits for a computer that is off
  stops after two days.
- **Codex cloud**: sign in to Codex first, on the setup page (step **Codex**): your server runs `codex login --device-auth`
  and the page shows a code to enter on OpenAI's page, on your own phone or computer. The Codex CLI keeps its sign-in
  on your server, as it always does. Then enter a Codex cloud environment id (and a branch, if not the default). The job runs as a Codex cloud task
  (`codex cloud exec`). The card shows its status and then its changes, and **Open in Codex cloud** goes to the task.

## Settings

`agents` in config.json, all optional:

```json
{"agents": {"claude": {"command": "claude", "config_dir": "~/.claude-other", "background": true},
            "codex": {"command": "codex", "app_server": true, "detach": true},
            "max_parallel": 2, "timeout_minutes": 30}}
```

`config_dir` points the jobs' Claude Code at another config folder, such as another account, and only for jobs.
`"detach": false` keeps Codex's app server a child of The Machine, so a restart stops the job.
`"claude": false` or `"codex": false` hides that action. `"agents": false` turns both off.

## Result recovery

Remote results carry a numbered receipt. The app commits the result and receipt before acknowledging that exact version; a failed acknowledgment is retried after restart without applying the draft twice. A newer report is not erased by an older acknowledgment. The Network keeps encrypted-at-rest results for at most seven days (not end-to-end encryption); control-plane recovery backups expire within 30 days.

A coding job may replace the draft only while that same turn is still active and the draft still has the revision handed to it. Cancellation, a newer turn or the owner's edit wins. Otherwise the result remains available without replacing the owner's draft. Normal Send and execution permissions are unchanged.
