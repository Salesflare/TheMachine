# Using the assistant

[Documentation index](../README.md). Current reference; dated repair evidence lives in [History](history.md).

## Telegram and the dashboard

To-dos reach you on the dashboard, as phone notifications from the dashboard app, and on Telegram when you set it up. Telegram is optional.

### Without Telegram

Install the dashboard as an app and turn on its notifications. To-dos, reminders, results and the weekly recap then arrive as phone notifications.

- **Android (Chrome):** open the dashboard, tap ⋮ → **Add to Home screen** (or **Install app**). Open The Machine from your home screen, then **Settings** (the gear at the top) → **General**, and tap the bell.
- **iPhone/iPad (iOS 16.4 or newer, Safari):** open the dashboard, tap **Share** → **Add to Home Screen**. Open The Machine from your Home Screen (notifications only work there, not in a Safari tab), then **Settings** → **General**, and tap the bell.

Turn Telegram off or back on any time:

- `assistant telegram off`, or `assistant telegram on <your Telegram user ID>`.
- `off --remove-bot` also deletes the bot and its token from OpenClaw.
- Without Telegram, **Change** is typed on the dashboard to-do.

Which kinds of message go where (push, Telegram, email) is set per kind in **Settings** → **Notifications** ([help](help/notifications.md)).

### Telegram

Telegram uses OpenClaw's existing bot and message route, never a second poller.

**Sending safely**

- The outbox records intent before sending. A send with an unknown outcome is held as `uncertain` and checked against the chat. It is never resent blindly.
- After 30 minutes with no sign of it, the to-do says so and you may tap Send again yourself (`SEND_RETRY_AFTER`).
- A refused send says "Last attempt failed" with the reason, and can be retried at once.
- Only a draft's own attempts lock it. When a to-do reopens with a new draft after an earlier reply went out, you can edit and send the new one. Send sends exactly the edited text.
- While another draft of the to-do is going out (at most 90 seconds), an edit waits.

**When to-dos go out**

- To-dos and reminders go out only within your [work hours](#work-hours) (by default 08:00 to 23:00).
- Non-urgent work to-dos wait for your next work day (by default Monday after a weekend).
- Several to-dos may go out together; only the first buzzes.

**Buttons**

- **Do it**, **Change**, **Snooze** (2 hours, tomorrow, 3 days, 1 week, pick a date), **Mark done** and **Undo** (five minutes).
- **Not needed** (Dismiss) asks for a reason. When the reason holds beyond this to-do ("I do those myself"), the next review keeps it as a fact and stops suggesting that.
- Buttons edit the existing to-do instead of sending new messages. A finished Do it sends one short Ready notice.
- A step only you can do, in person or offline (go to a shop, pick something up, attend), has no Do it. **Done** leads, with **Plan it** for what the Machine can do around it: a calendar event at a sensible time, a link to the place with directions and opening hours, a message to the other side if plans change. Each still waits for your tap. Then **Snooze** and **Not needed**. The review judges which steps those are.
- A promise to-do says what was promised in its title, and only who and when in its one line.
- Each row holds up to three buttons that fit a phone's width, in order, so a Send shares its row with Mark done (`controls()` in `assistant.py` and `packRows` in the plugin follow the same rule).

**Change**

- **Change** opens Telegram's native reply box. Only a reply to that exact prompt, within ten minutes, counts as instructions.
- If the native reply box is unavailable, reply to the confirmed plain prompt. No slash command or dashboard visit is needed; the legacy slash command remains for compatibility only.
- A Change that asks for the to-do itself back later ("remind me about this next Tuesday") snoozes it, the same as **Snooze**. It leaves your list, says "Snoozed until Tue, Oct 27 at 09:00" and comes back then. A date without a time lands at your morning.
- No separate reminder is made for that. A reminder about something else, or a recurring one, still is.

### Weekly recap

The weekly recap (`weekly_recap`, off by default) arrives once a week, Fridays from 16:00 local time.

It leads with what needs you:

- promises made to you that are late (who, what, since when);
- your own promises with a date in the next two weeks, each linked to its to-do when there is one.

Then:

- **The week ahead**, Saturday to Friday: your meetings with other people that aren't routine or have a to-do on them (from a shared calendar only those you're invited to; a meeting on two calendars once), plus to-dos and promised dates due. A promise to you that is due today is still on time and isn't listed.
- **What changed:** the share of to-dos worth it, the writing rules, voices and filters adjusted, and how many drafts went out as written since.
- **New people**, by name.
- **Behind the scenes**, in one short line: signals reviewed this week and how many still wait. Never a cost, since the recap may go to anyone with a Machine.

In Telegram, each choice then comes as its own short message with its own buttons:

- A busy automated source without results (never a group chat you write in, or one with only a few people): **Stop reviewing** adds an `exclude` rule for that chat, app, channel or sender, **Undo** takes it out again, **Keep reviewing** stops asking.
- A to-do snoozed more than once: **Drop**, **Do it now**, **Keep**.

Nothing changes until you tap. A tap only changes your own filters or to-dos and never sends anything. That choice's message updates to show what was done. Without Telegram the recap arrives as a phone notification, without buttons.

## The dashboard

The dashboard shows the same to-dos grouped as **Needs your decision**, **Ready for you**, **Preparing** and **Coming back later**. It also has:

- the open [promises](architecture.md#promises), each with its own page: who promised what to whom and by when, where it stands, the message it came from, who and what it's about, its to-do and a short history, with **Done**, **Change date** and **Not needed**;
- Work/Personal filters, deadlines, sources and their health;
- every done or dismissed to-do, latest first, older ones loading as you scroll (`/api/cards/done?cursor=&q=&scope=` answers a page of 30 with `next` and `total`);
- review runs, feedback and learned facts.

It is served on `127.0.0.1:<port>` and reached through Tailscale Serve or Caddy; see [Security](../SECURITY.md).

### Reading a to-do

- A to-do leads with one short status line under its title: where it stands and what's left for you ("Needs you: approve the reply", "Ready for you to check and submit", "Looks handled: …").
- It shows a few lines of its text, with the rest behind **Show more** and **Read result**. Another open to-do it names is linked by its title.
- It shows its main action and two more. The rest, such as **Hand off** to a teammate in a Fleet, sit under **More**. **Not needed** is one compact choice.

**Questions for you**

- When the status line is a question for you, or a run stopped to ask you something (not a sign-in), **Answer** leads, also on a to-do a teammate handed back.
- Answer opens a box under the question. Your answer goes back like a **Change** note, so the work carries on. On Telegram, Answer asks for a reply.
- A Change or answer after a handoff came back makes the to-do yours again.
- A run that stops for your input asks short, plain questions, with quick picks for a clear choice that fill the answer box. Small calls with an obvious default it makes itself.
- After a Try again that came back asking the same, Try again is no longer offered.

**Reviews off:** the dashboard says so, with the way to turn them on. When to-dos are already there, it says they came from the one-time first look.

### Reading the original message

Any signal, on a to-do or in message search and the Graph, opens in a built-in reader: the full email with its images and attachments (fetched read-only), or the chat, Slack or calendar text. You don't need the original app.

The to-dos on screen read their email ahead, so it opens at once. The service keeps the last 40 emails it read for 10 minutes, in memory.

### Notifications and links

- The dashboard installs as a phone app and sends a push notification for each to-do, with or without Telegram.
- A link in a notification or a Telegram message opens that to-do's own page (`#chat=<id>`), in the installed app where the phone allows it.
- At inbox zero you can poke the sleeping robot. Poke it a few times and it offers a 20-second mini game, Catch the Zzz.

### The Machine's browser

- A Preparing to-do that is working in the browser shows that tab live (see [Sources](sources.md#the-machines-browser)).
- When the Machine has a browser view, a quiet **Browser** pill beside Settings opens it.
- On a computer it opens in the main area next to the sidebar, with **Open in new tab ↗**. The session keeps running while you look at something else. `#browser` opens it too.
- On a phone it opens in a new tab.

### Settings

**Settings** (the gear at the top right) has tabs in a pill row. A tab with nothing to show is left out, and the last one you opened is kept.

- **Account**, first on a Machine linked to an account at app.themachine.computer (hosted, or self-hosted and paired with the Network): your plan and its status, the next invoice (excluding VAT), the server's size and region, the Google and Microsoft accounts connected there and your Fleets. Its buttons open that page of the account in a new tab. On a hosted Machine already signed in, that goes through a one-time link that works once, for a minute, in that browser only. Stripe's billing portal opens at Stripe. A hosted Machine also has **Sign out** here, which signs you out of the account too.
- **General:** this device's light mode and phone notifications, and a link to your Fleet rules when you are in a Fleet.
- **Security** and **Activity:** see [Activity](activity.md) for the list of everything The Machine did.
- **Notifications:** where each kind of message reaches you, and your [work hours](#work-hours).
- **Writing:** email signatures and **How you write**: a few lines per channel that drafts follow, read from your own messages and kept up to date by your notes and edits. Edit or remove any.
- **Skills**, **AIs** (other AIs connected over MCP: [help](help/ai-connections.md)) and **Model**.

Links open a tab: `#settings`, `#settings/skills` or `#settings=skills` (also `account`, `general`, `security`, `activity`, `notify`, `writing`, `ai`, `model`; `hours` opens Notifications).

### Graph and Connections

Graph and Connections have sub-tabs, like Fleet:

- **Graph:** People, Projects, Organizations and Who's who (roles to confirm, counted on the Graph tab too).
- **Connections:** your sources by kind (Mail and calendar, Chat, Other sources with Android), **+ Add**, saved **Sign-ins** and **Reviews**. A sub-tab with a source that needs you shows how many and opens first.

Links open a tab or sub-tab: `#events`, `#graph`, `#graph=roles` (`people`, `projects`, `orgs`), `#connections`, `#connections=chat` (`mail`, `other`, `add`, `signins`, `reviews`; the old `phone` opens Other sources). The older `#people` and `#health` still work.

### Adding a source

Connections, **+ Add** lists every source this Machine can add and how many of each are connected. Picking one runs the same steps as `assistant connect <source>`, inside the service:

1. Its questions show one at a time. A key goes in a password field and only to the step that asked for it.
2. A test read.
3. The service restarts to start reading it.

How each kind signs in:

- **Google:** gog's read-only sign-in in two steps: open the address it shows, then paste the address Google sends you to.
- **Outlook:** a device code.
- **WhatsApp** and other steps that need a terminal (a QR code) say which command to run.
- **Hosted Machine:** Google and Microsoft link to your account page, which signs them in. The dashboard never shows terminal commands.
- **Self-hosted Machine paired with an account:** **Sign in with Intercom**, **Sign in with Trello**, **Sign in with Google** (Gmail and Google Calendar), **Sign in with Microsoft** (Outlook) and **Sign in with Zoom**. It opens the sign-in in a new tab, and the row follows it until "Connected to <workspace or address>" ([the Fleet](fleet.md)). Not paired, it links to pairing first. Your own app stays under **Use your own app**. Intercom and Trello sign in only.

One source at a time; **Stop** ends it.

### Reconnecting and disconnecting

- A connection whose sign-in expired or was revoked shows **Reconnect** on Connections. It runs the same steps for that account, keeping its address, calendar and access.
- For a Google account gog already holds, Reconnect asks Google for exactly the scopes that sign-in has now (checked with gog's dry run), never more or less. When those can't be matched, it says which command to run instead. The terminal command stays under **Or use a terminal**.
- Each connection's **Details** also has **Reconnect** and **Disconnect**.
- Disconnect asks first, takes the account out of `config.json` (the old file stays as `config.json.bak`) and restarts the service. What it already brought in stays, and so do sign-ins and keys, which other accounts may share.
- On a hosted Machine, Google and Microsoft accounts reconnect and disconnect on your account page.

## Calendar

The **Calendar** tab is an agenda that starts today and runs on as you scroll. Later days load as you near the end, earlier ones when you scroll up at the top.

**What it shows**

- Meetings from your connected calendars, with their prep to-do when there is one.
- To-dos due or coming back that day, and handoff check-ins.
- Promises with a date, each once. A plan made together reads "With …". One about a meeting that day with the same person sits on that meeting's row.
- An event on someone else's calendar shared with you is marked with their name and muted. One on both calendars shows once, as yours.
- All-day and multi-day events show as All day with their dates.
- Overdue to-dos and promises come first.

A row opens its to-do's chat, the promise's page, or the meeting in its own calendar. Looking changes nothing.

**Adding and changing events**

- When a calendar's sign-in may write, **New event** adds one to your own calendar or a shared one marked `writable`. An event there without guests opens a small editor (Save, or Delete twice). Each change is your tap.
- On a phone, New event is a round **+** on the Today row.
- **Where** suggests your own places first, then OpenStreetMap addresses your Machine looks up with only the typed text (`place_search`).
- On your own calendar, **Invite** adds people from the Graph or any address as chips. The list of who gets an invite sits above the button, which says how many (**Add and invite 2**). Google sends the invitations on that tap. Without guests nobody is invited or gets an update.
- A to-do can offer a calendar change too ("add it to the family calendar"). It shows what changes, and only your **Add**, **Save** or **Delete** makes it, once.

**Scheduling with other Machines**

- When someone with a Machine asks to meet, your Machine asks theirs for free times over the Network and picks a slot within both your work hours (ending by 18:00), after your buffer and in your preferred times. Each of you gets one to-do, like "Meet Alex Example" with the time, length and video link below it. **Book it** on both sides adds the event to your own Google calendar and invites them; **Other time** tries the next slot (3 rounds); **Not needed** closes both to-dos.
- No Machine there, no answer within 3 minutes, or no slot: the to-do keeps its email draft with times.
- The Network pane sets **What other Machines may ask mine** (**Free/busy for scheduling**, or **Off**; Off at the Careful level), the meeting length, buffer and preferred times. A Machine answers only people you emailed both ways, free or busy only, for at most 14 days, on a 15-minute grid. Each ask is a line in Activity, under Calendar. Design: [scheduling-between-machines.md](scheduling-between-machines.md).

**Views**

**Today**, ‹ › and the dates on show stay on top, with a switch between **Agenda** (the default), **Week** and **Month**. ‹ › move by the view's span.

- **Week** on a computer is a time grid, Monday to Sunday. Each meeting is a block as long as it lasts, overlapping ones sit side by side, all-day items and dates without a time sit in a strip on top, and a line marks now.
- **Week** on a phone shows three days; swipe or use ‹ › to move three days.
- **Month** runs from the Monday on or before the 1st to the Sunday on or after the last day, with the days around it dimmed. A computer shows up to three items a day and "+N more", which opens the day in the agenda. A phone shows dots, and a tap lists the day under the grid.

The keys are t, ← → (or k j), a, w and m. The view is remembered on the device, the Calendar always opens on the current period, and the address keeps the view and date (`#calendar?view=month&date=2026-11-01`).

## Work hours

One setting for when The Machine works with you: on the dashboard under **Settings** (the gear at the top) → **Notifications** → **Work hours** (phone-friendly), with `assistant hours`, or as `work_hours` in `config.json`.

- **Work days** (default Monday to Friday): work to-dos (from `work:` sources) wait for a work day, and snoozed work and returning email threads come back on one. Personal to-dos keep their timing.
- **Messages from / until** (default 08:00 to 23:00): nothing is sent outside these hours, to Telegram or the phone; it waits until they start. Reviews keep running in the background. A range like 20:00 to 04:00 wraps past midnight.
- **Snoozes land at** (default 09:00): where Tomorrow, 3 days and 1 week land, and when a snoozed email thread comes back.
- **Morning digest** (`digest_at`, default 08:30) and **time zone** (`timezone`). The installer takes this computer's time zone, and the dashboard offers the device's when it differs.

Saved from the dashboard, it takes effect at once and is written to `config.json` (the old file stays as `config.json.bak`).

<a id="card-chat"></a>
## To-do chat

### Opening it

Tap a to-do's title (on a phone; on a computer a click on it renames the to-do), its quiet **Chat ›** link (a dot marks a to-do that already has a conversation), its **Asked** note, or **See in chat ›** after a Change. The to-do opens as a conversation (`#chat=<id>`).

- A **Change** typed on the to-do stays on the to-do; the chat never opens by itself.
- Chat opens only from a to-do, on a tap (not on the tap that stops a scroll).
- The header holds back (to the to-do), the title and a ⋯ menu with the to-do's other actions and your task list (beside the chat on a wider screen).

### The thread

The thread runs strictly by time in a calm column about 720px wide. The Machine's and a coding agent's replies are plain text, your messages are soft pills on the right, and times show on hover.

In order, it shows:

1. **What the to-do is about:** who wrote it, how, and its first lines, with **Read the thread**. An email shows only its new text, with the earlier messages it quotes folded under **Earlier messages**. For a support conversation: what the other side asked, then a teammate's internal note.
2. **The to-do itself**, as the Machine's first message: what is going on and, when it waits on a call, the question in one line ("Your call: …"), with the to-do's choices under it while it is open.
3. **Each run** as one quiet "Checked 5 things" line you can open, followed by what it said and the draft it left, inline with **Show what changed** against the draft before.
4. **Work handed to a coding agent:** your messages to it ("To Codex") and each answer, its files as chips.

The one open result (a draft waiting on you, an outcome summary or the to-do's question) is the only raised card. A draft that went out turns quiet with a muted "Sent".

The to-do's own text stays its status (where it stands, what is ready). An answer to your message shows only in the chat. What it did, or is still doing, is part of the to-do from then on: chat replies, later runs and the review build on it, so the next step never repeats finished work.

**Lines in the thread**

- A handoff to a teammate's Machine is a line with its time ("Handed off to Pat's Machine · 14:02"), then their answer when it comes ("Pat declined it. Their note: …").
- Back for a check-in with no answer, "No answer from Pat yet" sits under it, with Mark done, Snooze and Not needed instead of Do it. One that didn't go out says so, with **Try again**.
- A step without a draft (a calendar change, a merge) says when it didn't work or was canceled.
- Your own taps are small muted lines, verb first ("Chose Do it", "Snoozed it 5 times", "Sent to Sam"), lined up with the right edge of your messages. A tap you took back within a minute is left out.
- Replies are redacted like Technical details and leave out the agent's bookkeeping. A learned skill shows only as "Noted for next time", saved files as chips, and "Codex sent nothing" as a quiet note (left out when something went out after).
- A reply that left a page open in the Machine's browser offers **View in Machine browser**.
- A file a reply points to (a draft, sources) is a chip that opens it, never a bare title.

**Drafts that can't be sent from here**

A draft with no send path is the raised result itself, named for what it is ("Internal answer for Sam · Intercom note"). It shows only the draft, with its sources behind **Open**, **Copy draft** first and one line saying why. The to-do shows the same.

**Names and sources**

- Only the draft that went out says "Sent"; one canceled before it says "Not sent".
- A send names the person and the app ("Sent to Sam on Slack"), never a channel or ID.
- A small muted icon marks where a message came from (email, chat, calendar, note), on the to-do's source line too.
- That source line names the person ("Slack DM with Sam Lee"), never a channel handle or ID. When no name is known yet, it names only the app ("Slack").
- The person chip on a to-do uses their name as they write it elsewhere, not a lower-case chat handle.

### Writing in the chat

At the bottom are a status line with its one way back ("Snoozed until Fri 09:00 · Unsnooze", "Done · Reopen", "Not needed · Reopen") and a one-line message box that grows as you type. There are no canned suggestions.

- You can ask about the thread, the people or the context, as well as change the draft. A question gets an answer and leaves the draft as it is.
- A message is a **Change** on that to-do: the same path, so the to-do's status, Telegram, outcomes and learning stay in step. On a snoozed to-do it brings it back; on a done to-do it reopens it first.
- It continues the to-do's session with a short follow-up prompt instead of the full to-do context.
- Approvals stay on the to-do's buttons, and you can't add files.

**Drafts are never sent in the same reply.** A draft written or changed in a chat reply is shown first, also when your message says what to do ("email Sam now"). You read it and tap Send, or say "send it" in a later message. The service checks this itself: the Machine sends for you only a draft that was on the to-do, unchanged, before the message that approves it.

A message you send from the chat shows on its draft: **Sending…** with a bar, then who it went to, how and when ("Sent to Sam by email · 10:21", and then **Mark done** is the next step), or why it didn't go out, with **Try again**.

### Live updates

- While a run goes, the view checks about once a second and shows the reply as it grows.
- A check that fails meanwhile (the Gateway busy with the run) changes nothing on screen. A chat whose replies couldn't be loaded at all says so once the run is over, and tries again a few seconds later.
- A refresh while you type keeps your text, caret and focus. A refresh changes only what changed: you stay at the end if you were within a line of it, else where you were reading, and anything you opened stays open.
- A snooze that has ended is back in Ready at once, also before the next refresh.
- When the Machine can't be reached, the top shows "Offline · updated 10:42" with the last to-dos (or "Restarting · retrying" during an update). It tries again quietly, as soon as the service says. An open page reloads itself after an update.

### Layout

- Long titles fit on one line (two on a phone) and fade out, with the full title on hover.
- On a wider screen the list and the chat scroll on their own and the page itself stays put.
- On a phone the chat is one screen-high column, as in the ChatGPT and Claude apps. The thread scrolls in its own space and the box stays at the bottom, on the keyboard when it's open, also while the address bar moves and in the installed app. The view respects the notch and home bar.

### How it reads the session

The service reads the session through the OpenClaw Gateway's `chat.history` with the pinned official client (`@openclaw/gateway-client`, installed by `npm ci` from `package-lock.json`), as its own operator device with read access only. It takes the source messages, your notes and taps, what went out and each run's saved result from its own database. The browser never talks to the Gateway or holds its token.

<a id="new-card"></a>
## New to-do

Add a to-do yourself:

- **New to-do** under Search on a computer, or press **N**, or open the palette and type "new";
- **+** in the top bar (it also offers New person, New organization and New project);
- **New to-do** in the task list on a phone.

Type what needs doing and press Enter; nothing else is needed. Optional chips: Work or Personal, a due date ("Friday", "in 2 weeks", "24 Oct"), a person or organization from the Graph, and an email to attach.

It is a normal to-do made by the same path as the review's (`card_new`), with the same buttons, chat, snooze, Done, projects and handoffs, and "Added by you" in quiet text. Creating it sends nothing.

The next review fills it in (a cleaner title, people and threads, the next step, a draft prepared ahead), but never dismisses it or folds it into another to-do. Its title and body keep everything you said, and your words open its chat. If the review thinks it is the same as another to-do, the to-do asks "Looks like the same as … Merge?" and only your tap merges.

<a id="rename"></a>
## Rename

Give any to-do your own title:

- Rename in a to-do's More menu or the chat's ⋯ menu;
- a click on the chat's title, or on a to-do's title on a computer;
- in the sidebar: the ⋯ on hover, a double click, a right click, or a long press on a phone.

Enter saves, Esc cancels, an empty title keeps the old one, up to 200 characters.

Your title shows everywhere the to-do does: the dashboard, Telegram (which edits its message), notifications and a Fleet handoff. Reviews and preparations keep updating the summary and next step, but never the title. **Reset to suggested title** goes back to the latest generated one. The chat gets a quiet "Renamed" line.

<a id="keyboard"></a>
## Keyboard

Everything on the dashboard can be reached from the keyboard. Keys never fire while you type.

**The palette:** **⌘K** on a Mac or **Ctrl K** on Windows and Linux (or **/**). Type to find an action, a page, a to-do, a person, an organization, a project or a message, then ↑ ↓ and Enter. Its **Messages** group searches everything the Machine read, the same search as the results page, and **See all results** opens that page. Recent commands come first. With a board on Projects, the palette also switches Projects between Board and List view. On a phone it is the search icon in the top bar.

**?** shows every shortcut.

**Go to a page:** **G** then a letter.

| Key | Page | Key | Page |
|---|---|---|---|
| **T** | To-dos | **J** | Projects |
| **C** | Calendar | **W** | Who's who |
| **P** | People | **F** | Fleet |
| **O** | Organizations | **L** | Learning |
| **N** | Connections | **,** | Settings |

**E** opens the message search results, and the old **S** and **B** still work.

**In a list:** **J** and **K** move (in a chat: the next or previous to-do) and Enter opens.

**On a to-do:** **E** renames, **S** snoozes, **D** marks it done, **R** writes in its chat. **N** is a new to-do anywhere.

Nothing that sends, approves or posts runs from a key or straight from the palette. Review the email… only opens the Send dialog, and Hand to Codex… only opens the brief, where you read it and confirm.

For developers: a feature adds its own entries with `actionAdd({id, group, label, keywords, keys, run, when})` (`dashboard/shell-keys.js`), and the palette, the keys and the ? sheet all pick them up.

## Do it

**Do it** queues a preparation: an isolated turn `agent:main:assistant-review-preparation-<job>` of your main agent with `USER.md`, `PREPARATION.md`, the to-do, your latest note and the full evidence.

- Up to `preparation_concurrency` run at once and share the OpenClaw browser through a lease.
- The agent does the work and saves a short result with `prepare` (longer output goes in `memory/assistant/` in the workspace), or records a plain-language blocker.

**What comes back**

- A task it finds already done or no longer needed comes back as "Looks done already", with **Mark done** first.
- When it only answered your question, explained or made a plan, the to-do says "Answered. Nothing done yet." and **Do it** leads again.
- Emails come back as a draft with a **Send** button. Read result on the dashboard shows the draft too.
- In Telegram the to-do shows the draft itself (to, cc, subject, text), so **Send** there sends exactly that revision, and **Edit** opens it in the dashboard. A draft too long for the to-do, or one where you still pick the recipient, first shows a full preview and sends on **Send now**.

**After a send**

- Sends go through the account's Gmail. The to-do then says who it went to and when, and moves to done (Undo or Reopen bring it back).
- A handoff instead waits for the reply.
- A to-do with another send still waiting stays in Ready for you.

**When a run stops**

- A run interrupted by a crash or outage resumes with its history instead of redoing finished steps.
- A run that doesn't finish within 35 minutes is stopped and tried once more. Then the to-do says **Stuck**, with **Try again**.
- A confirmed last step whose run stopped (Stuck, a snooze) waits, paused, and carries on with **Try again** or when the snooze ends. Until then the to-do says in one line that it isn't done, why, and when it carries on, instead of the earlier result. That also holds when new work you asked for replaced that step ("not confirmed yet" when it may have gone through).

<a id="prepared-ahead"></a>
### Prepared ahead

When the review is confident you'd say yes, the work starts before you tap anything, and the to-do arrives done up to the one step that commits something:

- a reply arrives as a draft with **Send**;
- a form arrives filled in with **Submit…**, an invoice set up with **Pay…**, a booking picked with **Book…**.

That button shows what goes out (amounts, dates, names, text). **Confirm** runs only that last step, checks that it went through and reports back. Once it went through, the to-do is done. If the page shows something else by then, it stops and tells you instead.

- **A message in a web app** (a reply in a support inbox, a chat or DM): the to-do shows its exact text like an email draft. **Edit** in the Submit dialog (or Telegram) changes it. Confirm then types exactly the edited text, replacing the earlier draft on the page, and checks that it went out.
- **Files:** a file it uploads (a receipt with a reply) is listed in that dialog and opens from there. Confirm uploads exactly those files. When none are listed, it says it attaches no file.

Nothing is sent, submitted, paid or changed before your confirm. The work starts within seconds of the review that made the to-do. Only the usage budget or a usage limit holds it; the to-do then says so and roughly when it starts. Settings: `prepare_ahead` and `prepare_ahead_per_day` in [Configuration](configuration.md).

## The Machine fixes itself

The service keeps track of its own bugs and can fix them. Small fixes that prove themselves merge on their own and stay undoable for a day; everything else waits for your Merge.

### What it records

Every error raised in The Machine's own code (logged by a worker, or a thread that dies) is kept per code location and day:

- the exception type;
- its message, with quoted text, email addresses, links, long numbers and anything token-like taken out;
- the file, line and function, how often, and the code version.

Never arguments, values or message content. Trouble outside the code (a source or the network down, a full disk, a busy database) isn't recorded as a bug.

### How it reaches you

- The first `gateway` source turns them into `machine.fault` signals: the first occurrence of a day, then again at 3, 10, 30, 100…
- Each starts with a plain line: what failed, what you may notice, and whether The Machine can fix it itself. The code locations sit under Details.
- When an outside service failed (a 5xx, a timeout or a dropped connection, read from where the error came from), it says so instead: The Machine retries and nothing is needed from you. No fix is offered or merged for it.
- A review suggests a fix when an error recurs or breaks something you rely on.
- A to-do about an error nobody acted on closes by itself once newer code has gone a day without it.

### Do it and Merge fix

- **Do it** never touches the running code (the plugin blocks that). The agent clones it into `fix_dir/<job id>`, finds the cause, fixes it, adds a test, runs the whole suite and commits.
- The to-do then has a **Merge fix** button with the summary, the files and the full diff.
- **Merge now** runs the tests again in that clone (`self_test`, by default `scripts/test.py`). It checks that neither the running code nor the fix changed since you reviewed it, and that the running code has no local changes. Then it fast-forwards the running checkout to exactly that commit, pushes it when the branch has an upstream (`self_fix_push`) and restarts the service.
- Anything off means nothing is merged, with the reason on the to-do. A fix whose base moved has to be redone.
- `send_now` can't approve a merge; only the small proven-fix exception below is automatic.
- A change to the OpenClaw plugin takes effect after `openclaw plugins reload personal-assistant-bridge`.

### Merging by itself

A fix to one of its own recorded errors merges without a tap when it is small and proven:

- at most 3 Python files of the service and 50 lines besides the tests;
- a new test that fails without the fix (checked on a copy of the old code);
- no changes to the plugin, `AGENTS.md`/`PREPARATION.md`, the database layout or the config;
- one a day at most.

The to-do says it merged and has **Undo merge** for 24 hours, which reverts the commits, pushes and restarts. It undoes itself when the merged version records the same error again, or any new error within the first hour.

- `self_fix_auto: false` turns it off; anything that doesn't qualify keeps the Merge fix button.
- A fix that merged by itself stays on this machine. It isn't pushed upstream (often the public project) unless you set `self_fix_auto_push: true`, and the to-do suggests pushing it or opening a pull request.
- A later push never carries along commits that aren't upstream yet, and an undo is pushed only when its fix was.

## Command line

`assistant` (linked by the installer; code in `cli.py`) talks to the running service with the local API token. `busy`, `connect`, `doctor`, `export`, `import`, `message-key`, `service` and `support-bundle` work on this machine's files and also run while the service is down. Every command takes `--json`.

| Command | What it does |
|---|---|
| `assistant tasks` | Outstanding tasks; `--later`, `--done` or `--all` for the other tabs |
| `assistant show <id>` | One task (a unique ID prefix is enough) with decisions and evidence; `--full` keeps long evidence whole, `--no-evidence` leaves it out |
| `assistant promises` | Open promises, yours and those made to you; `--all` adds the ones closed in the last two weeks |
| `assistant search "<text>"` | Full-text search over all sources; `--account <id>` (repeatable) narrows it, `--limit` (20) |
| `assistant events --account <id> --ids 12,13` | Specific signals, or `--query` within explicit accounts |
| `assistant sources` | Connection health per source |
| `assistant reviews` | Review backlog and recent runs |
| `assistant busy` | What runs right now: agent jobs, sends, confirmed steps and preparations being worked on. Exits 3 while something runs, 0 when a restart or update cuts nothing off. A run that stopped (Stuck, Needs your help, snoozed) isn't running |
| `assistant feedback` | Recent decisions and written feedback |
| `assistant prepare <id> --file brief.md` | Save a short preparation (at most 1,000 characters) on an accepted task; `--body` instead of `--file`, `--next-action` for an exact draft |
| `assistant meeting-notes --event <id> --file notes.md` | Put notes (or with `--field transcript` a transcript) in Markdown on a calendar meeting, where the Calendar shows them and reviews use them. `--append` adds below what it has, `--remove` takes them off. `--day 2026-10-28 --query board` lists a day's meetings with their ids; `--event <id>` alone prints its notes |
| `assistant preview` | Before activation: one review of the last 7 days; prints the to-dos, sends nothing |
| `assistant roles` | Your agent reads the first and latest messages with your closest people and notes what each is to you in the Graph (also the last step of `assistant profile`; `--again` to run it again right away) |
| `assistant profile` | Your agent drafts how you write and what matters to you from your own messages, and notes what your closest people are to you in the Graph. The draft is saved to `USER.md` only after your yes, within the 4,000 characters OpenClaw loads (`--again` for a fresh draft, `--all` to keep every line, `--yes` to save without asking) |
| `assistant connect [<source>]` | Set up or redo a source (sign-in or key, IDs, a test read, first sync). Without a source, lists what still needs connecting. `--account <id>` picks or adds one of several |
| `assistant hours` | Your [work hours](#work-hours); `--days mon-fri --start 08:00 --end 23:00 --morning 09:00 --digest 08:30 --timezone Europe/Brussels` changes them and restarts the service (`--no-restart` only saves) |
| `assistant telegram status\|on <id>\|off` | Telegram is optional: turn to-do delivery there off (to-dos then reach you through the dashboard app) or back on. `off --remove-bot` also deletes the bot and its token from OpenClaw |
| `assistant doctor` | Checks the service, OpenClaw bridge, Telegram approval, every source, reviews, dashboard and `USER.md`; every problem comes with its fix. Exits 1 when something is broken |
| `assistant service status\|start\|stop\|restart\|logs` | The background service (systemd on Linux, launchd on macOS); `logs -n 200`, `-f` |
| `assistant support-bundle` | Versions, doctor and recent logs in one file to send when asking for help, with keys and tokens taken out ([Operations](operations.md#operations)) |
| `assistant message-key status\|to-keyring\|to-file` | Where the message key is kept ([Configuration](configuration.md#the-key-in-your-keyring-linux-desktop)) |
| `assistant enrich [domain]` | Organization and work contact data from your enrichment service: status, or look up one domain now |
| `assistant export` | Everything The Machine knows and how it is set up, in one encrypted archive, with an export code it shows once (`--keys` adds your keys, with a passphrase you pick instead; `--estimate` only says how big; `--out` picks the folder). See [Moving to another computer](operations.md#moving-to-another-computer) |
| `assistant import <file>` | Put an export back on a fresh install (asks its export code or passphrase) and list what to connect again; `--force` replaces a setup that already has sources, keeping a copy |
| `assistant fleet-pair <code>` | Pair this Machine with your account for a [Fleet](fleet.md), with a code from that account; `--label` names it there |
| `assistant skills` | Skills your agent follows: yours, proposed and shared ones (edit them in Settings, Skills) |
| `assistant task-import '<link>'` | Add a task someone sent you by email, from its link (opens your dashboard to confirm) |
| `assistant raw <action> '<json>'` | Any other non-owner service action |

Used by the agent during a preparation, not by hand: `attachment` (an email's attachments, read-only, or one saved for the run), `doc` and `doc-draft` (a doc's text, and a check of a doc draft; see [Doc writes](#doc-writes)), `skills-propose` and `skills-found`.

## Message actions

Each of these goes through the same approval path as email: the owner reviews and confirms, and an unclear outcome is checked, never resent.

### Slack messages and hand-offs

A Do it result can carry a Slack direct message from your own Slack account (the Maton Slack connection, as your user) to one person, named by Slack `user_id` or work email, with their name.

- `SlackTransport` in `next_actions.py` is separate from the read-only Slack source. It can only look the person up (`users.info`, `users.lookupByEmail`), open the DM, post one message and read that DM back.
- Before sending, it checks that the Slack name matches and that it's an active person, not a bot.
- An unclear outcome stays uncertain and is checked by finding exactly one message from you with that text in the DM. It's never resent.
- Sending needs a Maton Slack connection that is allowed to post as you.

**Hand-offs:** `delegate:true` (on Slack, or an email to one address) hands the task over. After the send, the to-do is snoozed for `wait_days` (default 3; a weekday at 09:00) with a watch on that person. When they reply (in that DM, or in that email thread or to that email), the to-do closes itself and their reply is reviewed as an answer to the to-do. Without a reply it comes back saying so.

For a teammate in your Work Fleet, the result is a Fleet handoff instead (`kind:handoff`, the message written to them). Its **Hand off** button opens the [Fleet handoff](fleet.md) form with that message, and nothing goes before you send it there.

### LinkedIn messages

- The `linkedin` action either replies in a conversation from the task's own LinkedIn signals (`conversation_id`), or writes to a profile slug you gave (`profile` plus `to_name`).
- Preflight resolves the recipient without sending. A profile whose name doesn't match `to_name` blocks the send.
- `LinkedInTransport` runs `linkedin_inbox.py send --yes` with the job ID as token. The reader logs its intent before the one write (fsynced, token admission locked) and never reuses a token.
- An unclear outcome stays uncertain and is checked through `linkedin_inbox.py verify` by exact message identity, not by matching text or time. Missing or damaged send evidence stays uncertain and is never resent.
- A busy browser just waits.

### X replies and DMs

These go through the same signed-in x.com session the X source reads with.

- The `x` action either replies to a post from the task's own `x.mention` signals (`reply_to`, its tweet ID), or answers in a DM conversation from its `x.dm` signals (`conversation_id`), from the account the signal came in on.
- Plain text, no media. At most 280 characters for a reply (links count 23, as on X; 25,000 with `long_posts`) and 10,000 for a DM.
- Send shows the account, the post replied to or the conversation, and the text. Preflight resolves the post or conversation without writing.
- `XTransport` then runs `x_inbox.py send --yes` with the job ID as token.
- **A reply** goes through X's own composer (`x.com/intent/post`). The tab first checks that the composer holds exactly the approved text for the approved post, then clicks Reply once, and blocks every other post request.
- **A DM** goes to the DM inbox API (`dm/new2`) with a request ID derived from the token.
- The reader logs its intent before the one write (fsynced, in `~/.local/share/x-inbox/sends.jsonl`) and never sends a token that is already in the log. It switches accounts only under its run lock and always switches back.
- An unclear outcome stays uncertain and is checked through `x_inbox.py verify` (the returned post ID, else that account's reply to the post with the same text; for a DM the request ID). Never resent.
- Encrypted X Chat conversations are refused.
- By hand, `x_inbox.py send --handle <h> --primary <p> --reply-to <id> --text '…'` only previews; `--check` also fills X's composer without posting; only `--yes` sends.

### WhatsApp messages

Only from a to-do: the owner's Send now, never `send_now`.

- The `whatsapp` action replies in a chat from the task's own `whatsapp.message` signals (`chat_id`, from the account the message came in on). Plain text, no media, at most 4,000 characters.
- When the owner says they talk to that person on WhatsApp, a to-do from another channel switches to their existing chat. The action names the owner's WhatsApp account and the `chat_id` (checked against that account's messages, else `wacli chats show`) or `to_name` (looked up with `wacli chats list --query`, which must match exactly one chat).
- Excluded chats and new numbers are refused.
- `WhatsAppTransport` checks read-only first (the linked number still matches `identity_sha256`, the chat is in the store). Then it makes the one writable wacli call, `wacli send text --to <chat> --message …`, without `--read-only`. Every other wacli call stays read-only. With the sync running, wacli hands the send to it.
- wacli has no send token, so an unclear outcome stays uncertain. It is checked by finding exactly one message from you with that text in the chat, newer than the saved pre-send message inventory and dispatch time. It's never resent.
- A busy store waits.

### Intercom replies

Only from a to-do: the owner's Send, never `send_now`.

- The `intercom` action replies in a conversation from the task's own `intercom.conversation` signals (`conversation_id`), at most 10,000 characters of plain text.
- It goes as the owner's own Intercom admin, with a reply token in a credential file of its own (`reply_credential`, with `reply_admin_id` and `reply_admin_name`).
- Only the owner's own Sign in with Intercom sets these: on a hosted Machine's setup page, or on a paired self-hosted one's dashboard (Connections, + Add). `onboarding.enable_replies` checks the token's workspace on `GET /me`.
- A pasted token only reads, and a token shared through a Fleet only reads, even if its app could write.
- The connector allows one write: `POST /conversations/<id>/reply` with `type: admin`, `message_type: comment`, the owner's own `admin_id` and the body, and no other field. Notes, assigning, closing and tags are refused before any token is read.
- `IntercomTransport` checks first, read-only: the reply token is still that admin in that workspace, and the conversation exists. It then sends once.
- Intercom has no send token, so an unclear outcome is checked by finding exactly one new comment from that admin with that text. It is never resent.
- The to-do's events say "Sent as <name> in Intercom". A customer's answer brings the to-do back.

### Doc comment replies

Only from a to-do: the owner's Post, never `send_now`.

- The `doc_reply` action answers one comment from the task's own `docs.comment` or `docs.mention` events (`comment_id`), at most 4,000 characters of plain text.
- Only Google Docs, and only when the owner granted the separate `drive` reply consent. Without it, or on Word, the reply stays a draft with an Open link.
- The connector allows one write, `drive.replies.create` on that comment.
- `DocReplyTransport` reads the comment's replies first, posts once, and settles an unclear outcome by finding exactly one new reply of the owner's with that text, never resending.
- The to-do's events say "Reply posted in the doc".

### Doc writes

Only from a to-do: the owner's Create or Save, never `send_now`. Telegram links to the dashboard's review.

- The `doc_write` action creates a doc (`op: create`: a Docs connection, a title and plain text whose `# ` to `### ` lines are headings), or edits a doc of the task's own doc events (`op: edit`, up to 20 changes: replace text within a paragraph, add paragraphs after one or at the end).
- The owner sees the new doc in full, or each changed paragraph before and after.
- Saving the draft reads the doc and pins its version. `DocWriteTransport` (`doc_writes.py`) reads it again first and refuses when it changed, writes once, and settles an unclear outcome by reading the doc back.
- Google needs the `drive` opt-in for edits and `drive.file` for a new doc. Word needs Allow edits (`Files.ReadWrite.All`).

Details per provider: [Sources, Doc writes](sources.md#doc-writes).
