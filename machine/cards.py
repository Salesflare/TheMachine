"""A to-do as the dashboard shows it: card(row) with its draft (card_draft), its controls, asks and source line, its
state (todo_state, looks_done) and the snooze, hand-off and title helpers. Moved out of assistant.py as is."""
import datetime as dt
import json
import re

import i18n
import locale_prefs
from machine.sources.android import android_app_shown
from machine.sources.slack import SLACK_ID
import next_actions
from timeutil import WORK_HOURS, hour_minute, in_hours, is_work_day, local_tz, morning_label, next_work_day, now
from machine import todo_states
from machine.owner_error import OwnerError


def snooze_time(option=None, explicit=None, hours=24, work=False, start=None):
    current = dt.datetime.fromisoformat(start or now())
    if explicit:
        try:
            due = dt.datetime.fromisoformat(explicit)
        except (TypeError, ValueError):
            raise OwnerError('Choose a valid date and time') from None
        if due.tzinfo is None:
            raise OwnerError('The selected time needs a time zone')
    elif option == '2h':
        due = current + dt.timedelta(hours=2)
    elif option in ['tomorrow','1d','3d','1w']:
        local = current.astimezone(local_tz())
        # The owner's day starts at 03:00: "tomorrow" pressed at 01:30 means the morning of the
        # same calendar day, pressed from 03:00 onwards it means the next day.
        days = {'tomorrow':1,'1d':1,'3d':3,'1w':7}[option] - (1 if local.hour < 3 else 0)
        hour, minute = hour_minute(WORK_HOURS['morning'])
        due = (local + dt.timedelta(days=days)).replace(hour=hour,minute=minute,second=0,microsecond=0)
        if work:
            due = next_work_day(due)  # work comes back on a work day, not the weekend
    elif option is not None:
        raise OwnerError('Choose one of the snooze times')
    else:
        due = current + dt.timedelta(hours=min(max(int(hours),1),720))
    due = due.astimezone(dt.timezone.utc)
    if due <= current or due > current + dt.timedelta(days=366):
        raise OwnerError('Choose a future time within the next year')
    return due.isoformat()


def handoff_checkin(urgent=False, due=None, start=None):
    """When a card handed to a teammate comes back to check in if they haven't answered. Only a real deadline brings it
    back sooner than the usual 3 work days, by the card's own `urgent` and `due` fields, never words in its text:
    due today (or overdue): about 3 hours later within the owner's hours, else the next morning;
    a deadline sooner than the usual wait: the morning of the work day before it (the same day if that has passed);
    urgent without a date: its day has passed, so the next work morning, not a few hours later.
    `start` is when it was handed off (now by default)."""
    current = dt.datetime.fromisoformat(start or now())
    local = current.astimezone(local_tz())
    hour, minute = hour_minute(WORK_HOURS['morning'])

    def soon():
        later = local + dt.timedelta(hours=3)
        if later.date() == local.date() and in_hours(later):
            return later.astimezone(dt.timezone.utc).isoformat()
        morning = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if morning <= local:
            morning += dt.timedelta(days=1)
        return morning.astimezone(dt.timezone.utc).isoformat()

    try:
        deadline = dt.date.fromisoformat(str(due)[:10]) if due else None
    except ValueError:
        deadline = None
    if deadline and deadline <= local.date():
        return soon()
    usual = snooze_time('3d', work=True, start=current.isoformat())
    if urgent:
        usual = min(usual, snooze_time('tomorrow', work=True, start=current.isoformat()))
    if not deadline:
        return usual
    day = deadline - dt.timedelta(days=1)
    for _ in range(7):
        if is_work_day(day):
            break
        day -= dt.timedelta(days=1)
    before = dt.datetime.combine(day, dt.time(hour, minute), local_tz())
    if before <= local:
        return soon()
    return min(before.astimezone(dt.timezone.utc).isoformat(), usual)


def asked_snooze_time(value):
    """When the owner asked, in a Change note, for this card back later: snooze_until as the run read it.
    A date alone means that day in their morning (work_hours.morning); a time without an offset is the
    owner's own time zone, so the clock change in between is handled here, not by the model."""
    text = str(value or '').strip()
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', text):
            hour, minute = hour_minute(WORK_HOURS['morning'])
            due = dt.datetime.combine(dt.date.fromisoformat(text), dt.time(hour, minute))
        else:
            due = dt.datetime.fromisoformat(text)
    except (TypeError, ValueError):
        raise ValueError("snooze_until is the owner's local date and time, like 2026-10-27T09:00") from None
    if due.tzinfo is None:
        due = due.replace(tzinfo=local_tz())
    return snooze_time(explicit=due.isoformat())


def owner_snooze_until(value):
    """A snooze time as the dashboard or Talk sent it: with an offset it stays as it is; a local time without one, or
    a date alone, is the owner's (asked_snooze_time), never UTC."""
    text = str(value or '').strip()
    if not text:
        return None
    try:
        if dt.datetime.fromisoformat(text).tzinfo is not None:
            return text
    except ValueError:
        return text  # snooze_time says what is wrong
    return asked_snooze_time(text)


def thread_return_time(days):
    """Days from now in the morning (work_hours.morning), moved to the next work day when it lands on a day off."""
    local = dt.datetime.fromisoformat(now()).astimezone(local_tz())
    hour, minute = hour_minute(WORK_HOURS['morning'])
    due = next_work_day((local + dt.timedelta(days=days)).replace(hour=hour, minute=minute, second=0, microsecond=0))
    return due.astimezone(dt.timezone.utc).isoformat()


def thread_snooze_note(state):
    until = state.get('snooze_until')
    if state.get('snooze_status') in ('queued', 'snoozed') and until:
        moment = dt.datetime.fromisoformat(until).astimezone(local_tz())
        return ' ' + i18n.t('Thread out of your inbox until {} · {}.', locale_prefs.day_text(moment), locale_prefs.clock_text(moment))
    if state.get('snooze_status') == 'failed':
        return ' ' + (state.get('snooze_error') or i18n.t('I couldn’t snooze the thread in your mailbox.'))
    return ''


def current_title(card, title):
    """The title a refresh gives a card: the new one for a title The Machine wrote, so it keeps saying what needs doing
    when that changes (a new ask, a new next step); the owner's own title (title_source 'user', set when they rename a
    card) is never replaced. A card the owner made stays 'auto': the review may clean its title up, their words stay in
    owner_words. Finishing never retitles a card (title_kept): how it ended goes in its status line, so Done still shows
    what the to-do was. A done or dismissed card only takes a new title when a new signal reopens it (update_card)."""
    return card['title'] if 'title_source' in card.keys() and card['title_source'] == 'user' else title


def title_kept(outcome=None, finish_state=None, send_now=False):
    """A result that only finishes the to-do (done, done already, its final step or approved send went through) never
    retitles it: the title says what needed doing, the status line how it ended (2026-10-29)."""
    return (outcome or {}).get('state') in ('done', 'already_done') or finish_state == 'completed' or send_now


def undated_card(*texts):
    """([texts], found): a review's title and summary with relative day words ("today", "morgen") replaced by the day
    itself, in the words' own language, so the to-do still reads right on later days (locale_prefs.undated)."""
    moment, hint, out, found = dt.datetime.fromisoformat(now()).astimezone(local_tz()), locale_prefs.language(), [], []
    for text in texts:
        if text is None:
            out.append(text)
            continue
        text, words = locale_prefs.undated(text, moment, hint)
        out.append(text)
        found.extend(words)
    return out, found


def plain(text, limit=240):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text or '')
    text = re.sub(r'\s+', ' ', re.sub(r'[*_`]|\\(?=.)', '', text)).strip()
    return text if len(text) <= limit else text[:limit - 1].rstrip() + '…'


def snooze_choices(work=False):
    """The quick snooze options with labels for when each lands; work skips days off."""
    local_now = dt.datetime.fromisoformat(now()).astimezone(local_tz())
    tomorrow = (local_now - dt.timedelta(hours=3)).date() + dt.timedelta(days=1)
    choices, seen = [['2h', i18n.t('2 hours')]], set()
    for option, plain in [('tomorrow', 'Tomorrow'), ('3d', '3 days'), ('1w', '1 week')]:
        due = dt.datetime.fromisoformat(snooze_time(option, work=work)).astimezone(local_tz())
        if due in seen:
            continue
        seen.add(due)
        moved = work and due.date() != (local_now - dt.timedelta(hours=3)).date() + dt.timedelta(days={'tomorrow': 1, '3d': 3, '1w': 7}[option])
        name = i18n.t('Tomorrow') if due.date() == tomorrow else locale_prefs.weekday_name(due) if moved and (due.date() - tomorrow).days < 6 and locale_prefs.language() != 'en' else due.strftime('%A') if moved and (due.date() - tomorrow).days < 6 else locale_prefs.day_text(due) if moved else i18n.t(plain)
        choices.append([option, name + ' · ' + morning_label()])
    return choices


# The chat's Stop (Store.stop_chat): what the card says after, and a message that is only files (chat_files.py)
CHAT_STOPPED = 'Stopped. Write what to do next, or tap Try again.'


# A raw chat handle is never shown: a channel ("#DM", "#general"), a Slack or WhatsApp ID, or both together
CHAT_HANDLE = re.compile(r'(?:#[\w.-]*|[CDGUW][A-Z0-9]{8,})(?:\s+[UW][A-Z0-9]{8,})?|\d{6,}@(?:s\.whatsapp\.net|g\.us|lid)')


def chat_plain_name(name):
    """A bare lower-case first name as a handle ("andrea") reads as a name ("Andrea")."""
    name = str(name).strip()
    return name.title() if re.fullmatch(r"[a-z][a-z'-]{0,30}(?: [a-z][a-z'-]{0,30}){0,2}", name) else name


def group_sender(who):
    """A sender as a mailing list rewrites it, the way people say it: Google Groups' "'Sam Lee' via Sales" is "Sam Lee via
    Sales", and a group named after its address ("info@acme.com readers") is that address."""
    m = re.fullmatch(r"'(.+)' via (.+)", str(who or '').strip())
    if not m:
        return who
    group = m[2].strip()
    address = re.match(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+', group)
    return f'{m[1].strip()} via {address[0] if address else group}'


# The "who" of a source line that is a raw chat handle rather than a name: a Slack DM ("#DM U02AB3CD4"), a member id,
# a WhatsApp jid or a bare Telegram number
SOURCE_DM = re.compile(r'#?DM (.+)')


SOURCE_RAW = re.compile(r'\d{6,}|\+?\d{6,}@\S+')


def source_line_shown(line, names=None):
    """A stored source line as people see it: never a raw chat handle. A Slack DM names the person ("Slack DM with Sam
    Lee"), a member id becomes their name (`names`, from slack_name_table), and one no name is known for is left out
    ("Slack · Thu 22 Oct"). Old cards stored the handle, so this runs when a card is shown, not only when it is made."""
    if not line:
        return line
    match = re.fullmatch(r'(Source: )?(.+?)(?: · ([^·]+?))?( \(\+\d+ more\))?', str(line).strip())
    if not match:
        return line
    prefix, head, when, more = match.groups()
    said = re.fullmatch(r'(.+?) (from|to) (.+)', head)
    if not said:
        return line
    kind, how, who = said.groups()
    names = names or {}
    named = lambda text: SLACK_ID.sub(lambda m: names.get(m[1], m[0]), text)
    dm = SOURCE_DM.fullmatch(who.strip())
    if dm:
        person = named(dm[1]).strip()
        head = kind if SLACK_ID.search(person) or CHAT_HANDLE.fullmatch(person) or not person else f'{kind} DM with {chat_plain_name(person)}'
    else:
        who = group_sender(named(who).strip())
        if kind == 'phone' and re.fullmatch(r'[a-z]\w*(?:\.\w+)+', who):  # an app by its package (older cards): by its name, or none
            who = android_app_shown(who)
        channel = re.fullmatch(r'#[\w.-]+', who) and not SLACK_ID.search(who)  # "#general": a channel by its name stays
        raw = not channel and (SLACK_ID.search(who) or CHAT_HANDLE.fullmatch(who) or SOURCE_RAW.fullmatch(who))
        head = kind if raw or not who else f'{kind} {how} {who if channel else chat_plain_name(who)}'
    return (prefix or '') + head + (f' · {when}' if when else '') + (more or '')


# A blocker that waits on the owner (a sign-in in the kept tab) resumes with Continue, not Try again.
HANDOFF = re.compile(r"(?i)\b(?:sign(?:ed)?[ -]?in|log(?:ged)?[ -]?in|signed out|2fa|two-factor|authenticator|passkey|tap continue)\b")


# The same buttons as the owner's dashboard names them ("tik daarna op Doorgaan"): a blocker in their language.
LOCAL_CONTINUE = re.compile(r'\b(?:' + '|'.join(sorted({re.escape(i18n.t('Continue', lang=l)) for l in locale_prefs.LANGUAGES if l != 'en'}, key=len, reverse=True)) + r')\b')


LOCAL_TRY_AGAIN = tuple({i18n.t('Try again', lang=l).lower() for l in locale_prefs.LANGUAGES})


def retry_label(reason):
    reason=reason or ''
    return 'Continue' if (HANDOFF.search(reason) or LOCAL_CONTINUE.search(reason)) and not any(w in reason.lower() for w in LOCAL_TRY_AGAIN) else 'Try again'


def merge_state(row, state):
    """Is this action state a fix to The Machine (a merge) rather than a message?"""
    if str(state.get('message_id') or '').startswith('merge:'):
        return True
    items = row.get('next_actions')
    if items is None:
        try:
            items = next_actions.actions(row.get('next_action'))
        except (ValueError, TypeError):
            items = []
    return any(a.get('kind') == 'merge' and (a.get('state') or row.get('action_status')) == state for a in items)


def expired_text(row):
    """The Done line of a to-do that closed by itself once its moment passed. A Telegram message keeps it as written, so
    it names the day; the dashboard says today or yesterday from the stored time when it shows it."""
    at = dt.datetime.fromisoformat(row['expires_at']).astimezone(local_tz())
    return i18n.t('No longer needed: {} was on {} at {}.', row.get('expires_what') or '', locale_prefs.day_text(at), locale_prefs.clock_text(at))


def card(row):
    title = row['title'].replace('*', '').replace('_', '')
    t = i18n.t  # what Telegram shows, in the owner's language
    status = {'accepted': t('On it.'), 'rejected': t('Not needed.'),
              'snoozed': t('Snoozed until {}.', locale_prefs.at_text(dt.datetime.fromisoformat(row['snoozed_until']).astimezone(local_tz()))) if row.get('snoozed_until') else t('Snoozed.'),
              'instructions': t('Got your feedback. I’ll update this.'),
              'prepared': t('Ready for you.'), 'completed': t('Done.')}.get(row['status'], '')
    # One status line: where it stands and what's left for the owner. A later sign that it's
    # handled replaces the result's own line; a result that found it already done needs no hint.
    outcome = {}
    if row['status'] == 'pending' and row.get('outcome'):  # back by itself after waiting on someone (return_waiting)
        try:
            still = json.loads(row['outcome'])
            if still.get('state') == 'still_waiting' and still.get('waiting_on'):
                status = t('Still waiting on: {}', sentence(still['waiting_on']))
        except (ValueError, TypeError, AttributeError):
            pass
    if row['status'] == 'prepared' and row.get('outcome'):
        try:
            outcome = json.loads(row['outcome'])
            status = {'your_step': t('Ready for you to check and {}.', outcome.get('step')),
                      'done': t('Finished. Mark it done if it looks right.'),
                      'answered': t('Answered. Nothing done yet.'),
                      'snoozed': t('Back, as you asked.'),
                      'already_done': t('Looks done already. Mark it done if that’s right.'),
                      'waiting': t('Waiting on: {}', sentence(outcome.get('waiting_on') or ''))}.get(outcome['state']) or t('Needs you: {}', sentence(outcome['needs']))
        except (ValueError, KeyError, TypeError, AttributeError):
            outcome = {}
    if row.get('early') and row['status'] == 'prepared' and not outcome.get('needs') and outcome.get('state') != 'already_done' and any(
            a.get('kind') != 'open' for a in row.get('next_actions') or []):
        status = t('Ready to approve. Nothing goes out until you do.')
    elif row['status'] == 'prepared' and outcome.get('state') in (None, 'done') and any(
            a.get('kind') in next_actions.WAITING_KINDS for a in row.get('next_actions') or []):
        status = t('Ready to approve. Nothing goes out until you do.')  # prepared, not done: a step still waits for them
    if row.get('handled_hint') and row['status'] not in todo_states.CLOSED and outcome.get('state') != 'already_done':
        try:
            hint = json.loads(row['handled_hint'])
            status = t('Done: {}.', hint['reason'].rstrip('.')) if hint.get('fleet') else t('Looks handled: {}. Mark it done if so.', hint['reason'].rstrip('.'))
        except (ValueError, KeyError, TypeError):
            pass
    if row.get('preparation_status')=='starting' and row.get('preparation_error')=='openclaw_unavailable':
        status=t(PREPARATION_WAITING)  # its start waits for the Gateway to come back (preparation_run_step)
    elif row.get('preparation_status') in ('starting','running'):
        status=t('Preparing… I’ve been in the browser a while; it may need you there (a sign-in or a check).') if row.get('preparation_browser') else t('Preparing…')
    elif row.get('preparation_status') == 'queued': status=t('Next up. I’ll start shortly.')
    elif row.get('preparation_status') == 'working': status=t('Working…')  # a job handed off after a stuck run (agent_jobs.WORKING)
    elif row.get('preparation_status') == 'blocked' and row.get('preparation_error') == 'stopped': status=t(CHAT_STOPPED)
    elif row.get('preparation_status') == 'blocked' and (row.get('preparation_browser') or {}).get('sign_in'):
        status=t('Waiting for you to sign in: {}. Sign in through Sign in and I carry on by myself.', row['preparation_reason'].rstrip('.'))
    elif row.get('preparation_status') == 'blocked' and row['status'] not in todo_states.CLOSED_OR_SNOOZED and not row.get('handled_hint') and ask_blocked(row):
        status=t('Needs you: {}', sentence(ask_text(row)))
    elif row.get('preparation_status') == 'blocked': status=t('I’m stuck: {}', row.get('preparation_reason') or t('Preparation did not finish. I’ll keep this in your list.'))
    action_state=row.get('action_status') or next((item.get('state') for item in row.get('next_actions',[]) if item.get('state',{}).get('status') in ('queued','sending','sent','uncertain','blocked','failed','undoing','undone')),None)
    if action_state and (row['status']=='prepared' or (row['status']=='completed' and action_state.get('status')=='sent')):
        merging=merge_state(row,action_state)
        sent=next((a for a in row.get('next_actions') or [] if a.get('state') is action_state),{})
        who=', '.join(sent.get('to') or []) if sent.get('kind')=='email' and not sent.get('to_options') else sent.get('to_name') or ''
        at=locale_prefs.clock_text(dt.datetime.fromisoformat(action_state['sent_at']).astimezone(local_tz())) if action_state.get('sent_at') else ''
        to_at=(t(' to {}', who) if who and sent.get('kind')!='intercom' else '')+(t(' at {}', at) if at else '')
        auto=merging and action_state.get('auto')
        mid=str(action_state.get('message_id') or '')
        status={'queued':t('Testing the fix. It merges by itself if every check passes.') if auto else t('Testing and merging the fix…') if merging else t('Sending your approved draft…'),'sending':t('Testing and merging the fix…') if merging else t('Sending your approved draft…'),
                'sent':((t('Merged by itself and restarted. You can undo it for 24 hours; it undoes itself if the error comes back.') if auto else t('Merged. The Machine restarts with the fix.'))
                        +(' '+action_state['error'] if action_state.get('error') else '')) if merging else
                ('✓ '+(t('LinkedIn message sent') if mid.startswith(('urn:li:','linkedin:')) else t('Slack message sent') if mid.startswith('slack:') else t('Reply posted on X') if mid.startswith('x:') else t('X message sent') if mid.startswith('xdm:') else t('WhatsApp message sent') if mid.startswith('whatsapp:') else t('Telegram message sent') if mid.startswith('telegram:') else t('Signal message sent') if mid.startswith('signal:') else t('Sent as {} in Intercom', ' '.join(str(sent.get('as_name') or t('your Intercom admin')).split())) if mid.startswith('intercom:') else t('Reply posted in the doc') if mid.startswith('doc:') else (t('Doc created') if sent.get('op')=='create' else t('Changes saved in the doc')) if mid.startswith('docwrite:') else t('Email sent'))+to_at+'.'+(' '+action_state['url'] if mid.startswith('docwrite:') and action_state.get('url') else '')+thread_snooze_note(action_state)),'uncertain':action_state.get('error'),'blocked':(action_state.get('error') or '')+(t(' Tap Merge fix to merge it anyway.') if auto else ''),'failed':action_state.get('error'),
                'undoing':t('Undoing the merge…'),'undone':action_state.get('error') or t('Merge undone.')}.get(action_state['status'],status)
    try:
        handed = json.loads(row['awaiting']) if row.get('awaiting') else {}
    except (ValueError, TypeError):
        handed = {}
    if row['status'] == 'snoozed' and checkin_line(row):  # with a teammate: when it comes back to check in, not a snooze
        status = checkin_line(row) + '.'
    elif row.get('handoff_still') and not handoff_redirect(row) and not row.get('handoff_checkin'):  # back to check in: still theirs
        status = t('Still with {}', row['handoff_still']['name'])
    if handed.get('delegated'):
        if row['status'] == 'snoozed' and row.get('snoozed_until'):
            status = t('Sent to {}. Waiting for their reply until {}; it closes when they answer.', handed['name'], locale_prefs.day_text(dt.datetime.fromisoformat(row['snoozed_until']).astimezone(local_tz())))
        elif row['status'] == 'completed' and handed.get('answered'):
            status = t('{} replied, so I closed this.', handed['name'])
        elif row['status'] == 'prepared':
            status = t('No reply from {} yet.', handed['name'])
    if row['status'] == 'completed' and row.get('expired_at') and row.get('expires_at'):
        status = expired_text(row)  # its moment passed: closed by itself (Store.expire_passed)
    elif row['status'] == 'completed' and row.get('expired_at'):
        status = t('Not needed.')  # a newer message overturned its plan: closed by itself (Store.plan_changed)
    if row['status'] not in todo_states.CLOSED_OR_SNOOZED and row.get('change_prompt',{}).get('status')=='uncertain':
        status+='\n'+t('I couldn’t confirm the message asking what to change. If it arrived, reply to it; otherwise use Ask for changes on the dashboard.')
    # A hashtag, so tapping it in Telegram lists every #work or #personal card.
    tag = '#' + row['scope'] if row.get('scope') else ''
    due = ''
    if row.get('due') and row.get('status') not in todo_states.CLOSED:
        try:
            due = t('Due {}', locale_prefs.day_text(dt.date.fromisoformat(row['due'])))
        except ValueError:
            pass
    source = ' · '.join(x for x in (due, source_line_shown(row.get('source_line')), tag) if x)
    source = ('\n\n' + source) if source else ''
    body = row.get('step_stopped') or row['body']  # a confirmed step that didn't go through: never the earlier "ready" text
    return ('**' + title + '**\n\n' + body + source + ('\n\n' + status if status else '')).strip()


CARD_DRAFT_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'signal', 'intercom', 'doc_reply')


ACTION_BUSY = ('queued', 'sending', 'sent', 'uncertain', 'local_preparation', 'paused', 'undoing', 'undone')


# What is really working right now, for tools and for a check before a restart or an update (`assistant busy`).
# A confirmed step whose preparation stopped (blocked, timed out, canceled by a snooze or close) is 'paused', not here.
ACTION_WORKING = ('queued', 'sending', 'undoing', 'local_preparation')


PREPARATION_WORKING = ('starting', 'running')


# A to-do whose start waits for the Gateway to come back (dashboard/todos-cards.js holdNote 'ai' says the same)
PREPARATION_WAITING = 'Waiting for the AI to come back. Then I’ll carry on.'


def action_busy(state):
    """A draft whose send is under way or done, so it has no Send button. An unconfirmed send the
    owner may retry (retry_ok) is not."""
    return state.get('status') in ACTION_BUSY and not state.get('retry_ok')


def card_draft(row):
    """The one message draft a ready card shows in Telegram, so the owner reads it there and can
    just press Send (2026-10-20). Returns {'action','text','full'}. full is False when the body
    had to be trimmed to keep the card under Telegram's limit: Send then opens the review first,
    so a one-tap send always sends exactly the text on the card. None when there is no single
    message draft, or the owner still has to pick the recipient."""
    if row.get('status') != 'prepared':
        return None
    actions = next_actions.visible_actions({'kind':'menu','actions':row['next_actions']}) if row.get('next_actions') is not None else next_actions.visible_actions(row.get('next_action'))
    ready = [a for a in actions if a['kind'] in next_actions.APPROVE_KINDS+next_actions.FINISH_KINDS+('email_demo','prepare')
             and not action_busy(a.get('state') or row.get('action_status') or {})]
    if len(ready) != 1 or ready[0]['kind'] not in CARD_DRAFT_KINDS or ready[0].get('to_options') or not ready[0].get('body'):
        return None
    a, escape = ready[0], lambda text: re.sub(r'([\\`*_{}\[\]()#+.!>|~-])', r'\\\1', str(text))
    if a['kind'] == 'email':
        head = ['To: ' + ', '.join(a.get('to') or [])] + [key.capitalize() + ': ' + ', '.join(a[key]) for key in ('cc', 'bcc') if a.get(key)]
        head.append('Subject: ' + (a.get('subject') or ''))
    elif a['kind'] == 'x':
        head = ['Reply on X to @' + a.get('to_screen_name', '') if a.get('reply_to') else 'X message to ' + a.get('to_name', '')]
    elif a['kind'] == 'intercom':
        head = ['Intercom reply to ' + a.get('to_name', '') + ', as ' + a.get('as_name', '')]
    elif a['kind'] == 'doc_reply':
        head = ['Reply to ' + a.get('to_name', '') + ' on “' + a.get('doc_title', '') + '”']
    else:
        head = [{'linkedin': 'LinkedIn', 'slack': 'Slack', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'signal': 'Signal'}[a['kind']] + ' message to ' + a.get('to_name', '')]
    tail = []
    if a.get('signature'): tail.append('+ your signature')
    if a.get('attachments'): tail.append('Attachments: ' + ', '.join(x.get('name', '') for x in a['attachments']))
    if a.get('delegate') and a.get('wait_days'):
        tail.append(f"After sending, this to-do waits {a['wait_days']} day{'s' if a['wait_days'] > 1 else ''} for {a['to_name'] + '’s' if a.get('to_name') else 'a'} reply.")
    if a.get('snooze_days'):
        tail.append(f"After sending, the thread leaves your inbox for {a['snooze_days']} day{'s' if a['snooze_days'] > 1 else ''}.")
    # Telegram takes 4096 characters; the title, summary, links and status share them.
    # Count the escaped representation conservatively in UTF-16 units too:
    # emoji and Markdown punctuation can double the old character estimate.
    units = lambda text: len(escape(text).encode('utf-16-le')) // 2
    room = max(0, min(2500, 3200 - units(row.get('title') or '') - units(row.get('body') or '')
                      - units(row.get('source_line') or '') - units((row.get('requested_feedback') or '')[:500])
                      - units('\n'.join(head + tail))))
    body = a['body'].strip()
    full = units(body) <= room
    if not full:
        used, kept = 0, []
        for char in body:
            weight = units(char)
            if used + weight > room:
                break
            kept.append(char)
            used += weight
        body = ''.join(kept).rstrip() + '…'
        tail.append('Full draft in the dashboard.')
    text = '**Draft**\n' + '\n'.join(escape(line) for line in head) + '\n\n' + escape(body) + ('\n\n' + '\n'.join(escape(line) for line in tail) if tail else '')
    return {'action': a, 'text': text, 'full': full}


def sentence(text):
    """One closing mark: a question keeps its "?" instead of getting "."."""
    text = str(text).strip()
    return text if text.endswith(('.', '?', '!', '…')) else text + '.'


def blocker_questions(value, strict=False):
    """A blocker's asks for the owner: up to 3 short questions, each answered on its own: up to 4 quick-pick options
    when it is a clear choice, else a short field, prefilled with its suggestion when the run knows a likely answer
    (last time's value). A plain string is a question without either, as runs wrote them before. [] when there are
    none. strict (a run saving them): raises on anything malformed; otherwise (stored JSON) []."""
    if not value:
        return []
    try:
        items = json.loads(value) if isinstance(value, str) else value
        if not isinstance(items, list) or len(items) > 3:
            raise ValueError
        out = []
        for item in items:
            item = {'question': item} if isinstance(item, str) else item
            question = str(item.get('question') or '').strip()
            raw = item.get('options') or []
            if not isinstance(raw, list):
                raise ValueError
            options = [str(o).strip() for o in raw if str(o).strip()]
            suggestion = ' '.join(str(item.get('suggestion') or '').split())
            if not question or len(question) > 200 or len(options) > 4 or any(len(o) > 60 for o in options) or len(suggestion) > 120:
                raise ValueError
            out.append({'question': question, **({'options': options} if options else {}),
                        **({'suggestion': suggestion} if suggestion and not options else {})})
        return out
    except (ValueError, TypeError, AttributeError):
        if not strict:
            return []
        raise ValueError('questions: at most 3 of {question (max 200 chars), options (at most 4, max 60 chars each), '
                         'suggestion (max 120 chars)}')


def ask_blocked(row):
    """A run that stopped to ask the owner: a blocker it wrote itself (no error of the service's own), not a sign-in,
    with the questions it asks. Those count even after a browser step. A run that named no questions (saved as an
    empty list) asks nothing: it says what stopped it (a limit, a failure), and the card says it is stuck and offers
    Try again, never Answer. A blocker from before runs named their questions (none saved at all) asks with its reason,
    unless it waits in the browser. Same rule as askBlocked() in dashboard.html."""
    reason = str(row.get('preparation_reason') or '').strip()
    if row.get('preparation_status') != 'blocked' or not reason or row.get('preparation_error') or retry_label(reason) == 'Continue':
        return False
    if blocker_questions(row.get('preparation_questions')):
        return True
    return not (row.get('preparation_questions') == '[]' or row.get('preparation_no_questions') or row.get('preparation_browser'))


def ask_text(row):
    """What a run that stopped to ask needs, for the Needs you line: its questions, else its blocker."""
    questions = blocker_questions(row.get('preparation_questions'))
    return ' '.join(q['question'] for q in questions) if questions else str(row.get('preparation_reason') or '').strip()


def card_task(row):
    """A card's next step as a task for whoever takes it on (Hand to Claude Code or Codex): its Needs you line (the
    outcome's needs, or the question its run stopped on), else the final step left, else its title. Never its latest
    chat reply: that is background."""
    try:
        outcome = json.loads(row.get('outcome') or '{}') if row.get('status') == 'prepared' else {}
    except (ValueError, TypeError):
        outcome = {}
    outcome = outcome if isinstance(outcome, dict) else {}
    needs = ' '.join(str(outcome.get('needs') or '').split()) if outcome.get('state') == 'needs_you' else ''
    if not needs and ask_blocked(row):
        needs = ' '.join(ask_text(row).split())
    if needs:
        needs = sentence(needs[0].upper() + needs[1:])
        return 'Help me answer this: ' + needs if needs.endswith('?') else needs
    if outcome.get('state') == 'your_step' and outcome.get('step'):
        return f'Check that everything is ready for me to {outcome["step"]}, and fix what isn’t.'
    title = ' '.join(str(row.get('title') or '').split())
    return sentence(title) if title else ''


def retry_pointless(row):
    """Try again already ran without new input and stopped asking again: retrying alone won't help."""
    return row.get('preparation_cause') == 'retry' and ask_blocked(row)


def ask_question(row, actions):
    """A card waiting on the owner's answer: Answer leads (the Change path) and Mark done steps back. Either a run that
    stopped to ask (ask_blocked) or a result whose needs_you is a question, with nothing to send. Same rule as
    askQuestion() in dashboard.html."""
    if row['status'] in todo_states.CLOSED_OR_SNOOZED or row.get('handled_hint'):
        return ''
    if ask_blocked(row):
        return ask_text(row)
    if row['status'] != 'prepared' or row.get('preparation_status') == 'blocked' or any(a.get('kind') != 'open' for a in actions):
        return ''
    try:
        outcome = json.loads(row.get('outcome') or '{}')
        question = str(outcome.get('needs') or '').strip()
        return question if outcome.get('state') == 'needs_you' and question.endswith('?') else ''
    except (ValueError, TypeError, AttributeError):
        return ''


def handoff_redirect(row):
    """A new handoff draft to someone other than who has the card now (the owner asked to hand it on)."""
    acts = row.get('next_actions')
    if acts is None:
        one = row.get('next_action') or {}
        one = json.loads(one) if isinstance(one, str) else one
        acts = (one.get('actions') or []) if one.get('kind') == 'menu' else [one]
    who = str((row.get('handoff_still') or {}).get('name') or '')
    return any(isinstance(a, dict) and a.get('kind') == 'handoff' and str(a.get('to_name') or '').split(' ')[0] != who for a in acts or [])


def checkin_line(row):
    """'Check in with Pat Mon 09:00 if no answer', for a card waiting on a handoff (handoff_wait)."""
    wait, until = row.get('handoff_wait') or {}, row.get('snoozed_until')
    if not wait or not until:
        return ''
    local, today = dt.datetime.fromisoformat(until).astimezone(local_tz()), dt.datetime.fromisoformat(now()).astimezone(local_tz()).date()
    days = (local.date() - today).days
    when = i18n.t('today') if days == 0 else i18n.t('tomorrow') if days == 1 else locale_prefs.weekday_name(local) if 1 < days < 7 else locale_prefs.day_text(local)
    return i18n.t('Check in with {} {} {} if no answer', wait['name'], when, locale_prefs.clock_text(local))


def answered_only(row):
    """A result that only answered, explained or planned: the task itself is still to do."""
    try:
        return row['status'] == 'prepared' and json.loads(row.get('outcome') or '{}').get('state') == 'answered'
    except (ValueError, TypeError, AttributeError):
        return False


def controls(row, root=''):
    t = i18n.t  # button labels in the owner's language; the choices stay as they are
    if row['status'] in todo_states.CLOSED:
        choices = [('Undo','undo')] if row.get('undo_until') and row['undo_until']>now() else []
    elif row['status'] == 'snoozed':
        choices = [('Check in now' if row.get('handoff_wait') else 'Unsnooze','accept'),('Change time','snooze'),('Not needed','reject')]
    elif row['status'] in todo_states.TAKEN_ON:
        choices = [('Mark done','complete'),('Snooze','snooze'),('Ask for changes','other'),('Not needed','reject')]
        if row.get('preparation_status')=='blocked':choices.insert(0,(retry_label(row.get('preparation_reason')),'retry'))
        elif answered_only(row):choices=[('Do it','accept'),('Snooze','snooze'),('Ask for changes','other'),('Mark done','complete'),('Not needed','reject')]
    else:
        choices = [('Do it','accept'),('Mark done','complete'),('Snooze','snooze'),('Ask for changes','other'),('Not needed','reject')]
        if row.get('preparation_status') == 'blocked':  # its prepared-ahead run got stuck (settle_ahead): Try again leads
            choices[0] = (retry_label(row.get('preparation_reason')), 'retry')
    if row.get('owner_step') and row['status'] not in todo_states.CLOSED_OR_SNOOZED:
        # Only the owner can do this step (a visit, a pickup): Mark done leads; Plan it is what The Machine can do around it.
        # An update's note: Done, Snooze; a problem in the computer's logs also Not needed (machine_log: it never comes
        # back), and with a safe fix Do it (machine_fix). A fix an update set aside (parked_redo) has Redo it while nothing
        # runs on it, which starts the usual self-fix run, and Try again when that run got stuck. A sign-in from before a
        # newer feature (reconnect: the dashboard's Reconnect leads) has Not needed too, for good.
        redo = row.get('origin') == 'machine' and row.get('parked_redo')
        fix = row.get('origin') == 'machine' and row.get('machine_fix')
        lead = [('Do it','accept')] if fix else [('Redo it','accept')] if redo and (row['status'] == 'pending' or answered_only(row)) \
            and row.get('preparation_status') != 'blocked' else []
        choices = lead + [('Mark done','complete')] + [
            ('Plan it' if choice == 'accept' else label, choice) for label, choice in choices if choice != 'complete'
            and (row.get('origin') != 'machine' or choice == 'snooze' or (choice == 'reject' and (row.get('machine_log') or row.get('reconnect')))
                 or (choice == 'retry' and redo))]
    actions=next_actions.visible_actions({'kind':'menu','actions':row['next_actions']}) if row.get('next_actions') is not None else next_actions.visible_actions(row.get('next_action'))
    if ask_question(row,actions):choices=[('Answer','other'),*([(retry_label(row.get('preparation_reason')),'retry')] if row.get('preparation_status')=='blocked' and not retry_pointless(row) else []),('Mark done','complete'),('Snooze','snooze'),('Not needed','reject')]
    if (row.get('cleanup') or row.get('digest')) and row['status'] not in todo_states.CLOSED:
        # A routine template's cleanup (mail_cleanup.py): its picks and their confirm are on the to-do; nothing to Do
        choices = [(label, choice) for label, choice in choices if choice in ('complete','snooze','reject')]
    choices = [(t(label), choice) for label, choice in choices]
    if row['status'] == 'pending' and row.get('labels'):
        choices = [(row['labels'].get(choice, label), choice) for label, choice in choices]
    buttons=[]
    link=(row.get('preparation_browser') or {}).get('link') or ''
    signin=(row.get('preparation_browser') or {}).get('signin_url') or ''
    if signin.startswith('https://') and row['status'] in todo_states.PREPARING:
        buttons.append({'label':t('Sign in'),'action':{'type':'url','url':signin}})  # the dashboard's sign-in, which also opens the browser
    elif link.startswith('https://') and row['status'] in todo_states.PREPARING:
        buttons.append({'label':t('Open the browser'),'action':{'type':'url','url':link}})
    if row['status']=='prepared':
        shown=card_draft(row)
        for action in actions:
            state=action.get('state') or row.get('action_status',{})
            if action['kind']=='finish' and state.get('status')=='done':continue
            if action['kind'] in ('email','email_demo','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply','merge','prepare','finish') and not action_busy(state):
                if shown and shown['full'] and shown['action']['revision']==action['revision']:
                    # The card shows this draft in full: Send confirms it, Edit opens it in the dashboard editor.
                    buttons.append({'label':next_actions.label(action),'action':{'type':'callback','value':f"assistant:{row['id']}:confirm_{action['revision']}"}})
                    if root:buttons.append({'label':t('Edit'),'action':{'type':'url','url':f"{root}#send={row['id']}&revision={action['revision']}&edit=1"}})
                    continue
                choice=('next_' if action['kind']=='prepare' else 'send_')+action['revision']
                buttons.append({'label':next_actions.label(action),'action':{'type':'callback','value':f"assistant:{row['id']}:{choice}"}})
            elif action['kind']=='open' and str(action.get('url') or '').startswith(('https://','http://')):buttons.append({'label':action['label'],'action':{'type':'url','url':action['url']}})
            elif action['kind'] in ('calendar','doc_write') and root and not action_busy(state):buttons.append({'label':next_actions.label(action),'action':{'type':'url','url':f"{root}#send={row['id']}&revision={action['revision']}"}})  # shown in the dashboard first, then tapped there
            elif action['kind']=='handoff' and root and not row.get('handled_hint'):buttons.append({'label':next_actions.label(action),'action':{'type':'url','url':f"{root}#task-{row['id']}"}})  # the Fleet handoff form is on the dashboard
    if row['status'] in (todo_states.PREPARED, todo_states.COMPLETED) and any(a['kind']=='merge' and (a.get('state') or row.get('action_status') or {}).get('undo_until','')>now() for a in actions):
        buttons.append({'label':t('Undo merge'),'action':{'type':'callback','value':f"assistant:{row['id']}:unmerge"}})  # a merged fix stays reversible for a day
    if row.get('skill_proposal') and row['skill_proposal'].get('update') and row['status']=='pending':
        # Update changes one of the owner's skills: its before and after are on the dashboard, and the tap is there.
        choices=[c for c in choices if c[1]!='accept']
        if root:buttons.append({'label':t('Review update'),'action':{'type':'url','url':f"{root}#chat={row['id']}"}})
    elif row.get('skill_proposal') and root:
        buttons.append({'label':t('Read instructions'),'action':{'type':'url','url':f"{root}#chat={row['id']}"}})
    buttons+=[{'label':label,'action':{'type':'callback','value':f"assistant:{row['id']}:{choice}"}} for label,choice in choices]
    # Fewer rows: up to three buttons per row that fit a phone's width, in order, so a Send
    # shares its row with Mark done. Same rule as packRows in the plugin.
    blocks,width=[],0
    for button in buttons:
        size=len(button['label'])+2
        if blocks and len(blocks[-1]['buttons'])<3 and width+size<=32:
            blocks[-1]['buttons'].append(button);width+=size
        else:
            blocks.append({'type':'buttons','buttons':[button]});width=size
    if not blocks:blocks=[{'type':'buttons','buttons':[]}]
    return {'blocks':blocks}


# A to-do that looks done already: a later signal suggests it's handled (looks_handled), or its run found it done
# (outcome already_done). It shows at the top of Done / dismissed, still open for a day (Reopen there puts it back on the
# list), then closes by itself (Store.close_looks_done); it never counts as waiting for them (badge, reminders, nudges)
# and is never late. Same rule as looksDone() in dashboard.html. A to-do without an outcome (most ready drafts) has no state: ifnull
# keeps NOT (...) true for it, where a bare NULL left every such ready to-do out of the badge and the digest.
LOOKS_DONE_SQL = "(handled_hint IS NOT NULL OR (status='prepared' AND ifnull(json_extract(outcome,'$.state'),'')='already_done'))"


# Waiting on others: its run found a step still open on someone else's side (outcome waiting: a review, merge, deploy,
# a reply), or the review saw the owner do their part and the next step go to someone else (store.cards.wait_on_others,
# which also brings it back when chasing is due). Nothing for the owner until that step moves; a new message on it
# (update_card) brings it back as open.
# Neither kind counts as needing the owner. Same rule as waitsOnOthers() in dashboard.html.
NOT_FOR_OWNER_SQL = "(" + LOOKS_DONE_SQL + " OR (status='prepared' AND ifnull(json_extract(outcome,'$.state'),'')='waiting'))"


def card_recipients(next_action):
    """Who a to-do's messages go to, names and addresses in one line, so a search finds it by recipient (done ones too)."""
    try:
        found = next_actions.actions(next_action)
    except (TypeError, ValueError, AttributeError):
        return ''
    out = []
    for a in found:
        if not isinstance(a, dict):
            continue
        out += [str(a.get(k) or '') for k in ('to_name', 'to_email')]
        for k in ('to', 'cc'):
            out += [str(x) for x in a[k]] if isinstance(a.get(k), list) else [str(a.get(k) or '')]
    return ' '.join(x for x in out if x)


def outcome_state(row):
    try:
        return (json.loads(row['outcome'] or 'null') or {}).get('state')
    except (TypeError, ValueError, AttributeError, KeyError, IndexError):
        return None


def looks_done(row):
    return row['status'] not in todo_states.CLOSED_OR_SNOOZED and bool(
        row.get('handled_hint') or (row['status'] == 'prepared' and outcome_state(row) == 'already_done'))


def waits_on_others(row):
    return row['status'] == 'prepared' and not row.get('handled_hint') and outcome_state(row) == 'waiting'


def todo_state(row):
    """An open to-do's state in plain words (talk_live.STATES, or LOOKS_DONE), as the dashboard's lists place it: looksDone,
    waitsOnOthers and placeOf in dashboard.html. A closed one is 'done' or 'dismissed' (Done / dismissed)."""
    if row['status'] in todo_states.CLOSED:
        return 'done' if row['status'] == 'completed' else 'dismissed'
    if looks_done(row):
        return 'looks done'
    if row['status'] == 'snoozed':
        return 'snoozed'
    if waits_on_others(row):
        return 'waiting on others'
    if row['status'] == 'pending' or row.get('preparation_status') == 'blocked':
        return 'needs you'
    return 'prepared' if row['status'] == 'prepared' else 'preparing'


def delivery_time(when, digest_at='08:30', current=None, work=False, urgent=False):
    """When a new suggestion's card goes out: now, the next morning digest, or a given day."""
    current = current or dt.datetime.fromisoformat(now())
    local = current.astimezone(local_tz())
    hour, minute = (int(x) for x in digest_at.split(':'))
    def weekend(target):
        # Work waits for a work day (work_hours.days), at the digest.
        local_target=target.astimezone(local_tz())
        if work and not urgent and not is_work_day(local_target):
            return next_work_day(local_target).replace(hour=hour,minute=minute,second=0,microsecond=0).astimezone(dt.timezone.utc).isoformat()
        return None if target<=current else target.astimezone(dt.timezone.utc).isoformat()
    if when == 'now':
        return weekend(current)
    if when and when != 'digest':
        try:
            target = dt.datetime.fromisoformat(str(when))
        except ValueError:
            raise ValueError('when is "now", "digest" or a date/time like 2026-10-12 or 2026-10-12T09:00') from None
        if target.tzinfo is None:
            target = target.replace(tzinfo=local_tz())
            if len(str(when)) <= 10:
                target = target.replace(hour=hour, minute=minute)
        return weekend(max(target,current))
    digest = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if digest <= local:
        digest += dt.timedelta(days=1)
    return weekend(digest)


def looks_done_at(db, row):
    """When a to-do started to look done: the later sign that it's handled, else when its run found it done already."""
    try:
        at = (json.loads(row.get('handled_hint') or 'null') or {}).get('at')
    except (TypeError, ValueError, AttributeError):
        at = None
    if not at:
        found = db.execute('SELECT updated_at FROM preparations WHERE suggestion_id=?', (row['id'],)).fetchone()
        at = found[0] if found else None
    return at or row.get('created_at')
