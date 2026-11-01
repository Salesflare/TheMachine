# The Fleet

The Fleet lets your Machine and the Machines of the people you work or live with help each other. It is in beta.

- A **Work Fleet**: you and your teammates.
- A **Family Fleet**: you and the people you live with. See [Family](family.md).
- **Friends**: people whose Machines help yours one to one. See [Friends](#friends).

Machines never talk to each other directly. Questions and answers pass through The Machine Network, sealed end to end:
see [The Machine Network](network.md) for what the Network can and can't see. Hosted Machines are on it already; a
Machine you run yourself can join too ([A self-hosted Machine in a Fleet](#a-self-hosted-machine-in-a-fleet)).

## Several Fleets

You can be in several Work Fleets (ones you started and ones you joined) and one Family Fleet. Your Machine answers in
each and keeps them apart: each Fleet has its own people, rules and questions. Leaving one Fleet leaves the others as
they are.

Asking from a Fleet's section asks only that Fleet. **Ask the Fleet who knows** from the Graph tab asks each of your
Work Fleets, one at a time.

## The Fleet tab

The Fleet tab shows one view at a time, picked with pills:

- each Fleet, Work and Family, in the order you joined or made them, with **What's shared** next to a Work Fleet whose
  Graph is shared ([Shared Graph](shared-graph.md));
- **Friends**, **Network** (finding people you know, scheduling with other Machines), **Sharing** (every rule in one
  place) and **Activity** (what happened, and what your Machine asked, answered and shared).

What a Fleet needs from you (a teammate's request, a meeting's follow-ups to split, a server to confirm) shows as a
to-do under **To-dos**, tagged Fleet and Work, with the same buttons as your other to-dos. The To-dos badge counts them.
A teammate's brief ask is the exception: it comes every day, so it is never a to-do (see [The team brief](#the-team-brief)).

## Sharing skills and contacts

Any Fleet, and any friend, can share:

- **Skills**: how-tos your Machine follows. The other person reads and installs them themselves. A skill is
  instructions only and never changes your rules here. See [Skills](skills.md#sharing-with-your-fleet-or-a-friend).
- **A contact** (`contact_share.py`). From a person's page or About you, pick one teammate, friend or Family member and
  the fields that go (name, then any emails, phones, organization, role and a note). You see exactly what goes before
  you send it, sealed like every ask. A Personal or private contact needs one more confirm. The receiving Machine keeps
  it under People, **Shared with you**, until its owner adds it (new, or merged into a person they have, adding only
  what is new) or dismisses it. The Network must list `contact` in that group's asks.

## What a Work Fleet does

1. **Who knows someone at X?** Ask from the Fleet tab, or with **Ask the Fleet** on a person or organization in the
   Graph. Each teammate's Machine answers from its own graph: "knows 2 people, closest: regular, last contact 2026-09".
   What is in an answer: [Answers, not data](#answers-not-data).
2. **Meeting prep.** If you turn it on (Sharing, **Meetings and brief**), your Machine asks your Work Fleet about the
   outside people in your meetings this week: how close each teammate is, their last contact and open promises. The
   answers show on the meeting's to-do ("From your Fleet: …") and go into its preparation.
3. **No double replies.** When the same email reaches you and a teammate, the first one to take it on claims it. See
   [Shared emails](#shared-emails).
4. **Shared connectors.** An admin connects Intercom or Stripe once and shares it from the Fleet tab, **Shared
   connectors**. The Machines they say OK to get it as a work source, sealed Machine to Machine. Connections shows
   "Shared by <Fleet>". How it's kept safe: [Shared connectors](network.md#shared-connectors).
5. **Shared Graph.** Work people, organizations, projects and client threads are shared with the Fleet. Graph has
   **Mine / Team**, "via <name>" and **Ask <name>**. It all stays on the Machines; the Network only passes it on. See
   [Shared Graph](shared-graph.md).
6. **Requests**: intros, handoffs, shared follow-ups and reviews. See
   [Asking a teammate to do something](#asking-a-teammate-to-do-something).
7. **The team brief**, **team learnings** and **free questions**: see [The team brief](#the-team-brief),
   [Team learnings](#team-learnings) and [Ask the Fleet anything](#ask-the-fleet-anything).

A Family Fleet asks other things (free times, to-dos for one another, family plans) and never work questions. See
[Family](family.md).

### Shared emails

When an email reaches you and a teammate (or a shared address like info@), the first one to take it on claims it:

- The other's to-do says "<teammate> is on it", with **I'll handle it** to take it over.
- Once one of you closes theirs, the other's open to-do says "Done: <teammate> already handled this", with **Mark done**
  first. It then offers no handoff. If they reopen theirs, so does yours.
- Claims travel as a hash keyed with the Fleet's secret, never the email ([What the Network sees](network.md#what-the-network-sees)).

What your Machine tells the others depends on your rule for shared emails ([Your rules](#your-rules)).

## Asking a teammate to do something

Besides questions, a Work Fleet carries three kinds of requests: **intros**, **handoffs** and **shared follow-ups**.
Each has its own rule in the Fleet (**Ask me first** by default, **Always accept**, **Never**), and nothing happens on
your side until you accept one. **Ask to review** has no rule: each request is a to-do the reviewer answers.

### Warm intros

When "who knows someone at X?" finds a teammate who does, **Ask <teammate> for an intro** (with a line why, if you
like) asks that one teammate.

- Their To-dos, phone and Telegram show "An intro to someone at X" with **Accept** and **Decline**.
- Accepting makes a to-do on their side with a double-opt-in email to the person they know best there, from their own
  work email. It asks that person first whether they want the introduction.
- The draft is built by plain code from their own graph, signed with their name, and goes out only with their own
  **Send**.
- You follow it in your Fleet tab, on your phone and in Telegram: asked, accepted, sent or declined.

### Handoffs

**Hand off to a teammate** on a work to-do opens a small sheet:

- who, and what they are asked to do (the to-do's next step, to edit);
- what goes along, as chips: its outside contact and the to-do's sources ("Email from Stripe Alerts · Fri, Oct 23";
  × leaves one out);
- an optional note. Its title and due date go too.

**What they get.** "<you> hands you: ..." with **Accept** and **Decline**. Accepting makes a to-do on their side. Its
title is the task, it leads with your ask in your words ("<you> asks you to take this on: ..."), then the contact.

- The sources come as copies: they read them in the to-do chat and under **Read the thread** like any email, from their
  own Machine, without access to your mailbox.
- Only that to-do's own emails and messages go: up to three, about 6,000 characters each (sender, date, subject and
  text). Attachments don't travel.
- An Intercom conversation also says where it is (region, workspace, conversation id and the customer's address). When
  their Machine reads that workspace, the to-do is on that conversation itself; otherwise the copy links to it.
- The contact is the person who wrote (or the Intercom customer), by Reply-To if there is one, never a Google Group's
  own address on a "via" email.
- If they already have an open to-do on it (the same email, by a key of its Message-ID, or else the one open to-do on
  email from the same contact), your handoff joins that to-do instead of making a second one.

**While it waits.** Your to-do says "Handed off to <teammate>". It leaves Ready and sits under Later ("With <teammate> ·
waiting"), saying when it comes back if they haven't answered ("Check in with <teammate> Mon 09:00 if no answer"), with
**Check in now**, **Change time** and **Not needed**.

- It comes back after three work days. Only a real deadline brings it back sooner, by the to-do's own `due` and `urgent`
  fields: about 3 hours later (within your hours, else the next morning) when it is due today, the morning of the work
  day before a nearer deadline, and the next work morning for an urgent to-do without a date. Urgency alone never brings
  it back the same day.
- Back on top it says "Still with <teammate> · check in?", with **Check in now** (its chat), **Take it back** and
  **Hand off to someone else**. Telegram says the same.
- One open handoff per teammate: a second one to them is refused.

The Fleet tab lists your handoffs in their own **Handoffs** box, both ways: open ones first (waiting, declined, or one
waiting for you), accepted and done ones after, with **Open** to go to the to-do.

**Their answer.**

- **Accept** (or they mark it done): yours is marked done, still saying to whom. Undo brings it back.
- **Decline** asks "Why? (optional)" with quick picks (Not mine, Already done, No time this week). Your to-do is back in
  Ready, saying "<teammate> declined: <their reason>", with **Do it myself**, **Hand off to someone else** and **Mark
  done**.
- **Accept with a note** (under More) adds a short note. Only the sender sees it, sealed like the answer.
- A to-do handed to you can't be handed straight back to whoever gave it; to others it can.

**A newer choice wins.** Their answer updates your to-do only while that exact handoff still owns it. A Change, Snooze,
Done, Dismiss or Reopen you made since wins; the answer stays in the Fleet log. One exception: if you marked the to-do
done while it was with them, their decline reopens it, once.

**Handing it to someone else.** Say so in the to-do's chat. The new handoff waits on the to-do ("Still with <teammate>
until you send it to <other>", **Review handoff to <other>**), and nothing goes until your **Hand off**.
**Take it back from <teammate>** (on by default) makes the new one the only one: the chat says "Taken back from
<teammate>", their late answer no longer moves your to-do, and their Machine gets a sealed `withdraw` (only the sender
can send one): the request there says "Taken back by <you>" and the to-do it made closes as Not needed. With it off,
both have it ("With <other> and <teammate> · waiting").

**Already on it.** If you are already working on a handoff before you answer it, it can become yours without a tap.

- Your Machine's review looks only at messages you sent and calls you joined after it came, and judges by meaning
  whether you are acting on it (never a message you only received, never a word list).
- It then accepts it for you, quietly: your to-do says "Marked as yours, since you talked to Sam about it" with **Not
  mine**, which undoes it and tells your teammate.
- They see "<you> is on it · talked to Sam on Slack, Fri 10:12", and their to-do is done. Only where (email, Slack, a
  call), when, and the first name of who you talked to travel; never their address or what was said.
- Dismissing that to-do later tells your teammate you declined, so it comes back to them.
- Your own Accept or Decline always wins. An older Machine on the other side reads it as a plain accept.

**Offered by the review.** When a task is a teammate's to do, the review offers to hand it to their Machine. **Hand off
to <teammate>** then leads the to-do and opens the sheet with that teammate picked and the message to them written
already. What goes is always the message for them, never the to-do's own note of what The Machine did.

**Someone not on the Network.** Pick **Someone else, by email** and give their address. The to-do gets an ordinary email
draft from its Gmail account instead, for you to read, change and send yourself. It says what you need from them, with
no promotional line or signature.

**Task page.** The to-do then offers **Add a task page**: a page they open from your email to see the status and answer
(I'm on it, Done, Can't do this, with a short note), no account needed. See [Task pages](help/task-pages.md).

- Nothing is made until you tap it and see exactly what the page shows: the title, the details, the due date and your
  first name. **Leave out** takes a part off. The link works 7, 14 (default) or 30 days.
- **Add to email** puts one line in the draft: "Status and replies: <link>".
- Never on the page: the email or its thread, your notes, the graph or other to-dos. Details that repeat the original
  email are refused.
- The page is sealed on your Machine with a key that exists only in the link (after the #), so the Network keeps an
  unreadable copy. Opening the link (an email scanner, a preview) changes nothing, and an answer needs a check only that
  key can make.
- Answers come back on the to-do and as a notification. Can't do this brings the to-do back to Ready. Marking it done
  closes the page (within 7 days); **Stop sharing** deletes it from the Network at once.
- If they get a Machine of their own (hosted, or self-hosted with `assistant task-import '<link>'`), the task arrives
  there as a to-do with your words quoted, and their dashboard offers to connect with you.
- The Network only counts how far each link got (opened, answered, done, signed up, task added, connected), never
  what was in it.

### Shared follow-ups

After a meeting that several members of one Work Fleet attended (in the last two days), one Machine proposes who does
which follow-up: the organizer's, else that of the member who joined the Fleet first, so there is only ever one
proposal.

- It starts from that owner's own open to-dos and promises on the meeting. The owner fills in each teammate's part
  ("send the pricing", "book the demo") on a to-do with the meeting's title and day, then **Send the split** or **Not
  needed**.
- With [Zoom](sources.md) connected, the meeting's summary fills in the empty parts: the review gives each next step
  to the person it names (an unclear one stays empty). The to-do says so; nothing goes until Send the split.
- Each member's Machine shows them their part, with the meeting's title from their own calendar, to **Accept**, change
  (**Accept my change**) or **Decline**. Accepting makes their to-do. To-dos on that meeting then say who does what.
- The meeting only travels as a hash keyed with the Fleet's secret: neither its title nor its id leaves your Machine.

### Ask to review

**Ask to review** (under More on any open to-do, at any step) asks one teammate to look at it: its draft (subject,
recipients, text) or, without a draft, its text, plus a note and the to-do's sources (× leaves one out). Nothing else
goes. See also [Ask to review](help/ask-to-review.md).

- A Work to-do goes only to a Work Fleet, a Personal to-do only to the Family. The other side is refused on your
  Machine and again on theirs.
- Their Machine makes a to-do of its own, "Review: <title>", where they edit the text in place, add a comment, and pick
  **Approve**, **Send changes**, **Send comment** or **Decline**. Their Machine can help in its chat but never sends or
  acts for you (Send is refused on a review to-do).
- What comes back is a tracked change: "Waiting for Pat's review", then "Pat suggested 3 changes". **See changes**
  shows each change, word by word, to **Accept all**, **Accept selected** or **Ignore**. Accepting writes a new
  revision of your draft; it never sends.
- **Withdraw** takes the request back. One open review per to-do; a request expires after 3 days.

### Requests are data

A request's text (an intro note, a handoff summary, a follow-up part) is your teammate's own words. It is kept short,
shown quoted, and never read as an instruction: it reaches no model, tool or Do it by itself. If you later tap Do it on
the to-do it made, the preparation is told that the quoted text is data. A request goes to one Fleet's people only and
is answered in that Fleet.

## The team brief

In a Work Fleet's section, set **Team brief** to Daily or Weekly (off by default). Tick **Also send it to me** to get it
on your phone and in Telegram too.

On your work days, from your morning time, your Machine asks each Work Fleet for its brief facts and puts together
"What the Fleet saw": a few ranked lines, such as "Globex is waiting for a reply (2 emails). 5 days, sent to you and
Priya". It covers:

- email waiting on the team, and for how long, checked against everyone's replies and "is on it" claims (mail from
  today, and mail only to you younger than two days, isn't waiting yet);
- meetings with the same company on several calendars;
- companies several of you are in touch with;
- companies that went quiet, when several of you knew them or they are a customer.

**Only what involves the team.** A waiting email counts when the review made a to-do of it that is still open, and it
went to two or more of you, to a shared address of the team (sales@, info@, a group), comes from a company a teammate
is in touch with, or from a customer. Each line says which. Mail only you got, from someone only you know, stays in
To-dos. Cold sales, newsletters and notifications never count.

**On the dashboard.** Five lines show (**Show more** for the rest), each with **Ask** (a question for the Fleet), **Open**
(that company's mail, when it came to you) and **Not needed**. When nothing needs the team it says so in one line. It
is told once, within your work hours, once everyone answered or two hours passed. Teammates who haven't answered are
listed. It is put together by plain code, never a model.

**What each Machine shares** is aggregate only: company names and domains, counts, last-touch dates, hashes of emails
and meetings keyed with the Fleet's secret, which members an email went to (as hashes), the name of a shared address
("sales") and whether the company is a customer. No subjects, message text, outside people, addresses or calendar
titles.

### Brief facts follow the Team Graph

In a Work Fleet a teammate's brief ask is answered by itself, with only the events the Team Graph shares with the team
(`shared_graph.visibility` says Team: a client thread, a shared meeting).

- A private, personal or sensitive thread never counts, also in a work account.
- Nothing counts while this Machine doesn't share its Graph with that Fleet (not started, or paused by an admin).
- Each answer is logged in Fleet, Activity ("answered with what the Team Graph shares: ...").
- One switch, **Share my brief facts with the team** under Sharing, turns it off. There is no Ask me first; a stored Ask
  me first follows the Team Graph too.
- Friends and Family have no brief. In a Careful Fleet, see [Brief requests](#brief-requests).

### Brief requests

In a Careful Fleet (no Always) a teammate's brief ask waits for you. It is never a to-do and never notifies you (no
phone, Telegram or digest). It waits in that Fleet's section, in one **Brief requests** box: a line per teammate with
how much an answer would share, and **Share once**, **Always share**, **Decline** and **Never**. Only the latest ask per
teammate waits; an unanswered one expires after 3 days. Their brief lists you as not answered meanwhile.

## Answered by itself in a Work Fleet

In a Standard Work Fleet, three teammate asks follow the Team Graph (`fleet.TEAM_ASKS`): who knows someone, meeting
context and who handles shared emails.

- They take two rules, **Always** (the default) and **Never**. A stored Ask me first reads as Always.
- Who knows someone and meeting context are answered only from events the Team Graph shares (`Fleet.team_gate`, the
  same check brief facts use): closeness, last contact and open promises come only from those events, and names only of
  people seen in them.
- Names are on by default there, because only Team-shared people can be named. A stored Without names holds.
- Each answer is logged as "answered with what the Team Graph shares".
- While this Machine doesn't share its Graph with that Fleet, those two keep all three rules and Ask me first as the
  default. If the Team Graph stops between the rule and the answer, the ask waits for you.
- Who handles shared emails sends only hashes both sides already have, so it follows the Fleet's level alone.

A Careful Fleet, Friends and Family keep asking. Intros, handoffs, shared follow-ups and free questions keep their own
rules.

## Team learnings

In a Standard Work Fleet, your Machine writes a few learnings about how the team works and shares them with the Fleet
(`fleet_learnings.py`). When one person learns, everyone does.

**When.** At most once a day, and only with teammates whose Team Graph is sharing. One small background turn (kind
`fleet_learn`, waiting for the usage budget like every background turn) writes at most 3 learnings.

**What is read.**

- Only mail and Intercom threads the Team Graph shares (`team_gate`), in that Fleet's accounts, with a message from your
  side, each thread once.
- At most 12 threads, 3 messages of 600 characters each, stripped of known names, addresses, links, numbers, amounts and
  dates (`team_learnings.strip`).
- The turn sees threads by number only, never which company. It needs at least 4 threads with 2 companies.

**What is kept**, checked by code after the turn:

- a kind: process, tool, style or routing (product feedback, customer specific and personal are dropped);
- confidence of at least 0.75 (lower is dropped, never asked about);
- support from threads with at least 2 different companies;
- one sentence of 20 to 240 characters with nothing that still identifies anyone (a strip hit, a quote, an unknown
  capitalized word: dropped, not edited);
- nothing already known or removed, also worded almost the same.

**How it travels.** Each learning carries its label (kind, source `team_conversations`, this Fleet, confidence) and goes
to the Fleet as a `learning` record in this Machine's Team Graph, sealed like the rest. It is logged in Activity on both
sides.

**Removing one.** Any member can remove one. Every Machine keeps the removal, so it is never shown, shared or made
again.

**Used in preparations.** When a Machine prepares a Work to-do whose accounts are all that Fleet's, it adds the few
learnings closest to it (embeddings, cosine at least 0.3, at most 3; shared words without embeddings), from exactly what
its Fleet tab shows. Never a personal to-do, never in a Careful Work Fleet. They are marked as team learnings, data and
not instructions, below your own facts, draft rules, voice and skills. The to-do says "Used a team learning: …" with
**Remove**.

**Turning it off.** **Offer to share learnings** (Settings, Security; Careful turns it off) stops the pass and takes
this Machine's learnings back on its next round. See also [Sharing learnings](intelligence.md#sharing-learnings).

## Ask the Fleet anything

Type a question in a Work Fleet's **Ask anything** box ("has anyone dealt with Stripe disputes?").

- Each teammate's Machine searches only its owner's own work accounts in that Fleet, and shows its owner your question,
  quoted, with what it found and a draft answer built by plain code ("Yes, I have: 3 emails on this, with Acme, most
  recently in 2026-09").
- Nothing goes back until they send that draft, edited or not. Their phone and Telegram offer **Send this answer** and
  **Don't answer**. There is no Always.
- You see the answers as they arrive, and "no answer" after a day or when declined.
- A teammate can have at most 3 free questions waiting with you; more are declined by themselves.
- Free questions follow your [work hours](usage.md#work-hours): they wait outside them.
- In several Work Fleets each one hears only about the accounts of its own company (a `work:<Fleet name>` boundary, or
  an address at a teammate's domain).

## Answers, not data

A Machine never hands out an email, a message, a calendar entry or a file in an answer. It answers with a short summary
it builds itself. (The [Shared Graph](shared-graph.md) is the one place Work client threads are shared.)

| Question | Without names | With names, also |
|---|---|---|
| Who knows someone at X | knows or not, closeness, last contact month, how many people | up to 5 names with their closeness and last contact |
| Meeting context | per attendee: closeness, last contact month, how many open promises each way | the name and up to 3 open promises per side |

- **Only work contacts.** A Work Fleet only hears about people seen in your work accounts (accounts with a `work:`
  boundary; without boundaries, every account not marked personal). Neither roles, nor people with only a free-mail
  address unless asked by that exact address.
- **No content, ever:** no message text, subjects, files, calendar titles, notes or facts.

## You decide, per Fleet

### Asks and approvals

Joining a Fleet only makes your Machine reachable. The first question from a teammate (other than those
[answered by itself](#answered-by-itself-in-a-work-fleet)) waits for you as a to-do: **Share once**, **Always share**,
**Decline** or **Never share** (under More). Always and Never become your exception for that teammate and that kind, and
settle their other waiting questions of that kind.

**You hear about it.** A waiting question sends one phone notification (if turned on) and, with Telegram, one message
with **Answer once**, **Always** and **Decline**. Questions within a minute share one. They say who asks and what, never
anything of yours. With no way to reach you, it waits on the dashboard and notifies once you turn one on. A handoff's
sender then sees "<teammate> won't get a ping. Let them know."

### Your rules

Under **Sharing**, one rule per kind of question for each Fleet, for everyone in it: **Ask me first** (the default),
**Always** or **Never**.

- **How much they hear:** **Without names** (the default) or **With names** (for meeting context: **Names and
  promises**). A short example from made-up data shows what they would get. New teammates follow the Fleet's rule.
- **Exceptions:** "Different for someone? Add an exception" picks a teammate and their own choice, shown as a pill
  ("Robin: Always") that × removes. If someone is in several of your Fleets, the Fleet a question comes through decides.
- **Only about…** narrows a rule: **Only about** some companies, domains or names (anything else asks you first),
  **Never about** others (declined, and their people left out of every answer), and **Only people from your work
  accounts** (on unless you turn it off). For shared emails it goes by the other companies on the email.
- **Shared emails:** Always tells the Network you're on an email you both got, shows who is on the ones they took, and
  says when you closed one. Ask me first sends nothing by itself: the to-do says who else got it, with **Tell them
  you're on it**. Never sends nothing.

### Only from your dashboard

Rules and approvals can't be changed by Telegram, the command line, the API token or the assistant. The one exception:
the buttons on the Telegram message sent for that very question, tapped by you in your own chat. Never is only on the
dashboard. A prompt in an email can't change who gets told what. Fleet, Activity logs every question asked or answered,
both ways.

## Security level

A Work Fleet is **Standard** (the defaults above) or **Careful**, picked by its owner or an admin on the account page.
Each Machine applies Careful as a floor (`security_levels.py`):

- no Always: rules count as Ask me first, requests wait for the owner;
- Without names, and only people from work accounts;
- no attachments in the Shared Graph, no to-do text in phone notifications for work to-dos, no contact lookups.

A member's own stricter choice stays, and their looser stored choice comes back if the Fleet goes back to Standard. The
control plane also makes sign-in sessions 7 days and binds invite links to their email. Sends need the owner's own Send
at both levels. A Machine's own level (Settings, Security) is the same idea for one Machine: see
[Security levels](help/security-levels.md).

## What happens in your Fleet

If you own a Fleet, your Machine tells you what happens in it: someone asks for a server, someone joined, a member's
server started, someone left or was removed, a member's server is now paid by another Fleet. They show in Fleet,
Activity, as a phone notification and in Telegram.

**A server request** waits for you as a to-do. It says what it costs, for example "Ann wants a Standard server in Acme:
€15/month, new total €30/month." (prices exclude VAT) with **Confirm · €15/month** and **Decline**. In a Fleet that is
free for now it says "free, because this Fleet is comped" with **Start it · free**.

A tap confirms exactly what that message showed, and only counts for you as the owner, while the request is open, on
those terms. A tap on an old message, a withdrawn request, someone who left, or changed terms does nothing and says
why; with new terms, the message updates and you tap again. A decision made elsewhere updates the Telegram message.

## Safe by construction

- **Questions.** A teammate's question never reaches a model, a tool, the browser or Do it. It is parsed into a fixed
  form (an address, a domain or a name) and answered by plain database reads (`fleet.py`).
- **Free questions** are untrusted text: control and invisible characters are removed, it is cut to 300 characters,
  and only its keywords are searched. No model reads it; the draft is built by code. Only what the owner sends goes
  back, cut to 600 characters.
- **Brief facts** are counts, dates, company names and hashes, only from events the Team Graph shares with that Fleet.
  The brief is assembled by code. The same holds for the answers a Standard Work Fleet gives by itself.
- **Team learnings** come from stripped, numbered threads the Team Graph already shares, and are kept only when code
  finds no name, address, number or quote in them. A preparation gets them marked as data, ranked below the owner's own
  rules.
- **Answers** coming back are checked against the same fixed form before they are shown or added to a preparation,
  where they are marked as data from teammates' Machines.
- **Requests** (`fleet_requests.py`) are kept to a fixed form and only shown, quoted. A handoff's sources keep only
  their kind, sender, date, subject and text; on the receiving Machine they are marked reviewed, so no model reads them
  by itself. Nothing is sent, drafted or done before the owner accepts (or set Always accept). Telegram and phone
  buttons are bound to the message sent for that request; a stale tap only shows the outcome.

## Who answers

The Fleet tab lists each Fleet's members with the Machine they answer with ("Self-hosted: <its name>", "Hosted: <its
address>" or "No Machine yet") and their account email; yours is marked "you, this Machine". Two members with the same
name are told apart by their email.

Each person answers with one Machine per Fleet. If you have more than one (say a hosted one and one at home), pick which
one answers in your account. Removing someone takes effect at once, and how often a Machine can ask is limited.

## In your Graph

Members of your Fleets, your Family and your Friends are marked in the Graph tab ("Has a Machine · Work Fleet"), with
**See in Fleet** and **Ask your Fleet** on their page; the Fleet tab links each member back with a small **Profile**
link. When the messages only give part of a name ("kim"), the Graph shows the name they chose to share in the Fleet, and
**Keep** makes it yours.

It uses only what the directory already shows every member: their name, verified email addresses, and whether they
have a Machine. It matches on those addresses on your Machine when you open the Graph, never asks their Machine
anything, and nothing new leaves yours. A pending friend request or a blocked person is not marked. When someone
leaves, or you do, the marker goes and the name falls back to the one in your messages, unless you kept or renamed it.

## Leaving a Work Fleet with your Machine

When you leave a Work Fleet, or its owner or admin removes you, and you keep your Machine, your work data for that
company does not stay with you. Your Machine disconnects that company's accounts and deletes what they brought in; your
personal sources stay. The invite page says so before you join, and the confirmation before you leave.

- **Work or personal is yours to mark.** Each account is Work (with its company) or Personal: pick it in the dashboard
  (Connections, a to-do's Details, and + Add) or, on a hosted Machine, on the setup page. It is the account's `boundary`
  (`work:Acme` or `personal:me`), marked as your own choice (`boundary_by: owner`); all accounts on the same address
  follow it.
- **Which accounts.** Your marking first: what you marked Work for that company goes, whatever its address; what you
  marked Personal (or another company's) stays. Unmarked ones go when their address is at the company's email domain
  (also subdomains), or when they are in that company's work boundary and have no address elsewhere (the company Slack,
  Intercom, Salesflare or GitHub). An unmarked account with an address elsewhere (a personal Gmail) stays.
- **Their sign-ins go too** on a self-hosted Machine (`gog auth remove`, an Outlook token file). A sign-in that a staying
  account uses is never touched.
- **What goes:** their messages and events, the to-dos and drafts made only from them, their promises, graph and search
  entries and sync state, and their own secret when no other account uses it. Google and Microsoft access through a
  hosted Machine's account page is revoked.
- **First a safety copy:** config.json and the database go into `work-removal-backups/` next to the database, readable
  only by you, deleted after 7 days.
- **How it arrives:** a hosted Machine gets it from the control plane; a self-hosted one asks the Network every 10
  minutes (`GET /removals`), also when it is in no Fleet any more, and reports the counts back. An older self-hosted
  Machine can't, and the confirmation says so.
- You get an email once it is done: "Your work accounts from Acme were disconnected and their data removed."

The code is in `work_removal.py`.

## A self-hosted Machine in a Fleet

A Machine you run yourself can be your Machine in a Fleet, next to teammates on hosted Machines. It needs an account
with The Machine (no subscription) and is off until you pair it.

### Pairing

1. In your account, make a pairing code. It works once, for 15 minutes.
2. In The Machine's folder, run `python3 cli.py fleet-pair ABCD-EFGH --label "My computer"`. This stores the Machine's
   own key, readable only by you, next to its database. A wrong, expired or used code is refused: make a new one.
3. Restart the service, and pick this Machine for your Fleet in your account.

Or ask your Machine's AI to do it; your account page shows the request with your code filled in, ready to copy.

Your Machine then shares the addresses of its work accounts with your Fleet, so your teammates' Machines recognize them,
and nothing else about you. Everything above applies the same way. You can disconnect it from your account at any time;
its key then stops working.

### Sign-ins for it

Some sources sign in through The Machine's own app: Intercom, Google (Gmail and Calendar), Microsoft (Outlook mail and
calendar) and Zoom. On a paired Machine you start that on its dashboard: Connections, **+ Add**, then the source. Not
paired yet, the dashboard says to pair first; pasting a token stays as a folded fallback, also for sources the control
plane has no app for (`GET /signins`).

1. The Machine asks the control plane for a one-time start link (`POST /connect-start`), signed with the key it
   published after pairing. The control plane refuses when that key changed since. The link works once, for 10
   minutes, signed in as the Machine's owner.
2. It opens in a new tab and leads to the provider. At the callback the control plane seals what the sign-in hands back
   for this Machine's box key (`network_crypto.open_box`).
3. The Machine fetches it once (`GET /connects`). It is deleted there as it is handed out, or after 15 minutes.
4. The Machine connects it as Connections, Add would (`onboarding.connect_delivered`), checks the key first (Intercom:
   `GET /me`), and reports back (`POST /connects`). Replies turn on only for the owner's own Sign in with Intercom, never
   for a token shared through a Fleet.

Nothing it carries is logged on either side. Google, Microsoft and Zoom hand back a refresh token, kept on the Machine
only (`mail_grants.py`, as for [broker accounts](sources.md)) after a real read checks each account. Access tokens then
come from the control plane over the Machine's own device token (`POST /google-token`, `/microsoft-token`,
`/zoom-token`): the control plane uses the refresh token for that one call and keeps nothing, and a rotated one goes
back to the Machine. Disconnecting the last account on a sign-in forgets it on both sides (`POST /grant-forget`).

### What it costs

Pairing is free, and so are Friends and Family Fleets on the Network. In a Work Fleet, while a self-hosted Machine
answers for someone, the Network costs €4 a month for that member (excluding VAT), paid by the Fleet's owner and
confirmed before it starts; nothing while the Fleet is free. Each Fleet is billed on its own, apart from your own plan.

## Friends

Friends are people outside your Fleets whose Machines can help yours, one to one. Each person has a **username**: on a
hosted Machine it is your Machine's address name, which you can change on your account page. A paired self-hosted
Machine claims one too.

- **Adding someone.** In the Fleet tab under **Friends**, or on your account page, type their exact username and send a
  request. There is no directory and no search by name, and a request looks the same whether or not that name exists.
  Nothing connects until they accept. People you already know can also be found privately
  ([Finding people you know](#finding-people-you-know)).
- **A request for you** shows in the Fleet tab, on your account page, in Telegram (Accept, Decline) and as a phone
  notification. Only you can answer it.
- **Remove or block** a friend, or block a request, at any time. Blocking is silent. You can unblock later.

### What a friend's Machine can ask

Under **Sharing** there is one rule per kind for all your friends (Ask me first and Without names by default), with
"Different for someone? Add an exception" for one friend, as in a Fleet:

1. **Who knows someone at X?**, the same short answer as for a teammate.
2. **Meeting context**, only for a meeting that friend is in too.
3. **A warm intro**: you see the request with Accept and Decline; nothing is drafted before you accept, and nothing goes
   out without your Send.
4. **When are you busy?** For one to fourteen days, your Machine answers from your own calendars with busy times only:
   start and end, never what, where or with whom. All-day events, events you declined and calendars shared with you
   don't count.

Friends are kept apart from your Fleets: a friend sees nothing of your Fleets, and rules don't cross over. A friend's
questions and answers are treated as data, kept to their fixed form, and never given to your AI, its tools or Do it.
Friends are free.

Finding a meeting time with someone who has a Machine, friend or not, is
[Scheduling between Machines](scheduling-between-machines.md). Its setting, **What other Machines may ask mine**, is in
the Fleet tab under **Network**.

### Finding people you know

Two switches in the Fleet tab under **Network**. Both are on by default at the Standard security level, and off at
Careful (your own level, or a Careful Work Fleet you're in). Your choice stays until you pick a security level again. A
Machine that had them off by default before turns them on once and says so ("Now findable by people who have your
email", with **Turn off**).

- **Check which of my contacts have a Machine** looks daily for your contacts on the Network, and every 15 minutes for
  someone new. Addresses are blinded with a secret only your Machine holds before anything leaves it (a private set
  intersection), so the Network never sees your address book; your Machine learns only which contacts matched. At most
  3,000 addresses a day.
- **Let people who have my email find me** makes your account email findable that way, only by people who already have
  it, plus the addresses of your connected mail and calendar accounts. The Fleet tab lists them under **Findable by**;
  untick any. Shared addresses (info@, a mailbox shared from a Fleet, an address a teammate also has, one marked as the
  team's) start off, marked "Shared address". An address two accounts list finds neither. It needs a username.

How the matching works and what the Network learns: [What the Network sees](network.md#what-the-network-sees).

**Suggestions.** A match becomes a to-do right away when it is new: contacts already on the Network when you turn this
on, and someone who joins later, the five strongest at a time, for a week. After that, only when there is something
concrete to do together: an open to-do that involves them, or a meeting with them in the next two weeks.

- Someone at your own work domain is suggested as a colleague, anyone else as a friend or family, for you to pick.
- **Connect** sends an ordinary friend request. **Not now** hides them for 30 days unless something new comes up;
  **Never suggest** hides them for good.
- Someone in a Work or Family Fleet with you is never suggested. A friendship you have stays as it is.
- What was checked, and every switch you flip, is kept in Fleet, Activity.

**Leave the Network** turns both switches off, removes every friend and withdraws open requests. Your Fleets stay.

## Delivery and retry

Questions and answers are delivered once, with retries: see [Reliability](network.md#reliability). In short, your
Machine saves an answer before it acknowledges it, and retrying the same question returns the first result instead of
asking twice. Questions expire after at most three days, and so do unacknowledged answers.
