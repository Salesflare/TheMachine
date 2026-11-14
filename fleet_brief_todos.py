"""The team brief's lines as to-dos (2026-11-12). Mixed into fleet.Fleet, next to fleet_brief.py.

A line of "What the Fleet saw" ("Globex is waiting for a reply", "Initech went quiet") is something for the owner to
decide, so it is a to-do in For you, not a box of its own in the Fleet tab:

- Once a brief is told (all answered, or BRIEF_SETTLE passed), each of its lines gets a Work to-do: its title, the
  line's why as its context, the company as its organization. The to-do carries Ask (the Fleet's free question,
  prefilled) and Not needed (Fleet.hide_brief_item: hidden, and an overlap learned).
- Only a specific line is a to-do (specific(), from _brief_context, no model call): who it waits on and since when,
  what they asked and what's at stake (open projects, a customer). A vague line stays in the brief; an open to-do
  that turns vague closes, one that gains a gist is retitled.
- No second to-do: when the owner already has an open to-do about that company (its organization, or mail from it on
  its evidence), the line joins it; two lines about one company share one to-do.
- It settles as the line does: once a rebuilt brief no longer has it (a reply went out, a teammate claimed it, contact
  again), the to-do is done by itself; Not needed on it, or Not needed on the old API (fleet_brief_hide), closes both.
  A line the owner closed comes back only with something new (another first email, another last contact).
- Details shows only what the Team Graph already shares with this Machine (shared_graph.team_for: teammates' client
  threads, never private, personal or sensitive ones), the owner's own mail from that company, and who of the team is
  in touch, each person linked to their page. Nothing is asked of anyone for it.

State lives in fleet_meta (META): {fleet: {line key: {'card', 'sig', 'item', 'merged', 'closed', 'asked', 'at'}}}."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import sqlite3
import statistics

from fleet_brief import brief_items
import graph
from i18n import t
import shared_graph_kept
import todo_org
from machine import todo_states
from machine.owner_error import OwnerError
import timeutil

LOG = logging.getLogger('personal-assistant')
META = 'brief_todos'
SYNCED = 'brief_todos_synced'  # {fleet: the brief's built_at and the day it was read on}: nothing new, nothing to do
KEEP_DAYS = 30  # a closed line is remembered this long: the same thing doesn't come back as a to-do
OPEN = todo_states.OPEN
SETTLED = {'waiting': 'Someone on the team replied or took it on', 'quiet': 'Back in touch with them',
           'overlap': 'No longer in the team brief', 'meeting': 'No longer in the team brief'}  # read through t()
THREADS_SHOWN = 3


STAKES_SHOWN = 2


def _sentence(text):
    text = ' '.join(str(text or '').split()).rstrip('.')
    return text[:1].upper() + text[1:]


def _stake_name(name, org):
    """A project as its to-do names it: without the company's own name in front ("Acme renewal" → "renewal")."""
    words, lead = str(name or '').split(), str(org or '').casefold().split()
    n = 0
    while n < min(len(words) - 1, len(lead)) and words[n].casefold() == lead[n]:
        n += 1
    return ' '.join(words[n:])


def stake_words(ctx, item):
    """What is at stake with the company, in a few words: its open projects (with their stage), else a customer."""
    stakes = [_stake_name(p['name'], item.get('org')) + (f" ({p['stage']})" if p.get('stage') else '') for p in ctx.get('stake') or []]
    if stakes:
        return t('At stake: {}', ', '.join(stakes))
    return t('A customer') if item.get('known') == 'customer' or ctx.get('customer') else ''


def specific(item, ctx, today, rhythm=''):
    """A brief line as a to-do that says what is going on and why it matters, or None: then it stays a line of the
    brief (its summary), never a vague to-do. ctx is BriefTodos._brief_context: the company's open projects and the
    last exchange with them, from the owner's own Graph and work accounts. Waiting: who it waits on and since when,
    what they asked (the exchange's line), and what's at stake; made only when one of those says something (what
    they asked, a stake, or mail to the owner too). Quiet: how long, the last exchange and what's at stake; made only
    with a stake. Other kinds as they are."""
    from fleet_brief import QUIET_MIN_DAYS, _brief_date, _on_day, _people
    kind, org = item.get('kind'), item.get('org') or ''
    if kind not in ('waiting', 'quiet'):
        return item
    stake = stake_words(ctx, item)
    gist = ctx.get('gist') or {}
    said = gist.get('line') or (t('Their email: “{}”', gist['subject']) if gist.get('subject') else '')
    day = _on_day(item.get('at'), today)
    last = _brief_date(item.get('at'))
    names = [p.get('name') or p.get('label') for p in item.get('team') or []]
    if kind == 'waiting':
        to = list(item.get('to') or [])
        if ctx.get('answered') or not (said or stake or item.get('to_me')):
            return None
        on = _people((['You'] if item.get('to_me') else []) + to, None, True)
        parts = [said or (t('What they wrote isn’t shared with you. Ask {}', _people(to)) if to and not item.get('to_me') else ''), stake]
        also = [n for n in names if n not in to] + (['You'] if item.get('mine') and not item.get('to_me') else [])
        if also:
            parts.append(t('{} also talks to them', _people(also)) if also != ['You'] and len(also) == 1 else t('{} also talk to them', _people(also)))
        return {**item, 'title': t('{} has been waiting on {} since {}', org, on, day) if on else item['title'],
                'why': '. '.join(_sentence(p) for p in parts if p) or item['why'],
                'ask': t('Is anyone answering the email {} sent to {}?', org, _people(to, None, True)) if to else item.get('ask'),
                'gist': gist.get('event') or None}
    days = (today - last).days if last else 0
    if days < QUIET_MIN_DAYS or not stake:
        return None
    span = t('{} weeks', days // 7) if days < 60 else t('{} months', days // 30)
    then = _brief_date(gist.get('at'))
    if not then or abs((then - last).days) > 1 or not (gist.get('line') or gist.get('subject')):  # not the last contact: the day alone
        last_words = t('Last contact {}', day)
    else:
        last_words = t('Last contact {}: {}', day, gist['line']) if gist.get('line') else t('Last contact {}: “{}”', day, gist.get('subject') or '')
    parts = [last_words, stake, rhythm]
    known = (['You'] if item.get('mine') else []) + names
    if len(known) > 1:
        parts.append(t('known to {}', _people(known, None, True)))
    return {**item, 'title': t('{} has been quiet for {}', org, span), 'why': '. '.join(_sentence(p) for p in parts if p),
            'ask': t('Anyone in touch with {} since {}?', org, day), 'gist': gist.get('event') or None}


def signature(item):
    """The line and the day it hangs on: the same waiting email, meeting or last contact is the same thing."""
    return f"{item['key']}|{item.get('at') or ''}"


def snapshot(item):
    keep = ('key', 'kind', 'title', 'why', 'ask', 'open', 'org', 'domain', 'at', 'known', 'team', 'mine', 'to', 'to_me', 'gist')
    return {k: item.get(k) for k in keep}


def rhythm_words(days):
    """How often the owner was in touch, in a few words; '' when there is no clear rhythm."""
    if not days or days < 2:
        return ''
    if 6 <= days <= 8:
        return t('usually weekly')
    if 12 <= days <= 16:
        return t('usually every two weeks')
    if 26 <= days <= 35:
        return t('usually monthly')
    return t('usually every {} days', days) if days < 120 else ''


def card_maker(store):
    """The app's hook (Fleet.brief_card): a Work to-do for one brief line, with an event of its own as evidence,
    marked reviewed so no review or preparation reads it by itself."""
    def make(account, dedupe, title, body, domain, quiet=False):
        event = store.reviewed_event(account, dedupe, 'fleet.brief', title, body, {'sender_display': t('your Fleet'), 'fleet_kind': 'brief'})
        return store.suggest(dedupe, title[:90], body[:700], [event], when='now', work=True, org=domain, quiet=quiet)['id']
    return make


class BriefTodos:
    brief_card = None  # set by the app: brief_card(account, dedupe_key, title, body, domain, quiet) -> the new to-do's id
    brief_reword = None  # set by the app: brief_reword(card_id, title, body), an open brief to-do in its line's new words

    # -- state
    def _brief_todos(self):
        return self.meta(META) or {}

    def _brief_todos_save(self, found):
        cutoff = (timeutil.clock() - dt.timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds')
        found = {f: {k: e for k, e in lines.items() if not e.get('closed') or str(e.get('at') or '') >= cutoff} for f, lines in found.items()}
        self.set_meta(META, found)

    @staticmethod
    def _card_status(db, card_id):
        row = db.execute('SELECT status FROM suggestions WHERE id=?', (str(card_id),)).fetchone()
        return row['status'] if row else None

    def brief_todos_open(self, fleet):
        """Whether a to-do of this Fleet's brief is still open: the brief is rebuilt now and then to see it settle."""
        return any(not e.get('closed') for e in (self._brief_todos().get(fleet) or {}).values())

    # -- the brief's lines into To-dos
    def brief_todos_sync(self, fleet, force=False, quiet=False):
        """The newest told brief of a Fleet, line by line, as to-dos (see the module). Returns how many it made.
        quiet: the brief pings with its own summary (tell_brief), which links to To-dos: its to-dos come in silently."""
        if not self.brief_card:
            return 0
        with self.connect() as db:
            row = db.execute('SELECT * FROM fleet_briefs WHERE fleet=? AND told_at IS NOT NULL ORDER BY built_at DESC LIMIT 1', (fleet,)).fetchone()
        if not row:
            return 0
        today = self.local_now().date()
        stamp = f"{row['built_at']}|{today.isoformat()}"
        synced = self.meta(SYNCED) or {}
        if synced.get(fleet) == stamp and not force:
            return 0
        view = json.loads(row['view'])
        items = brief_items(view, today, self.brief_hidden(fleet, row['period']), self.brief_opener(), self.brief_learned(fleet), limit=None)
        found = self._brief_todos()
        mine = {k: dict(e) for k, e in (found.get(fleet) or {}).items()}
        accounts = self.fleet_accounts(fleet)
        made, seen, stamp_now = 0, set(), timeutil.clock().isoformat(timespec='seconds')
        for item in items:
            key, sig = item['key'], signature(item)
            seen.add(key)
            entry = mine.get(key)
            vague, kept, target = False, False, None
            with self.connect() as db:
                words = rhythm_words(self._brief_rhythm(db, accounts, item['domain'])) if item['kind'] == 'quiet' else ''
                ctx = self._brief_context(db, item, accounts, self._brief_repliers(fleet, item))
                line = specific(item, ctx, today, words)
                if entry and not entry.get('closed'):
                    if self._card_status(db, entry['card']) not in OPEN:
                        entry.update(closed=True, at=stamp_now)  # the owner closed it: as they left it
                    elif line is None:
                        vague = True  # nothing specific about it (any more): it stays a line of the brief
                    else:
                        kept = True
                if not kept and not vague and entry and entry['sig'] == sig:
                    continue  # closed for this very thing: only something new brings it back
                if line is not None and not kept:
                    item = line
                    target = self._brief_target(db, item, {e['card'] for k, e in mine.items() if not e.get('closed') and k in seen})
            if kept:  # still open: in the words its line has now (more specific than when it was made)
                if not entry.get('merged') and (line['title'], line['why']) != (entry['item'].get('title'), entry['item'].get('why')) and self.brief_reword:
                    self.brief_reword(entry['card'], line['title'][:90], (_sentence(line['why']) + '.')[:700])
                entry.update(item=snapshot(line), sig=sig)
                continue
            if vague:
                self._brief_todo_close(mine, key, 'complete', t(SETTLED['waiting']) if ctx.get('answered')
                                       else t('Nothing specific to act on, it stays in the team brief'))
                continue
            if line is None:
                continue
            if target:
                mine[key] = {'card': target, 'sig': sig, 'item': snapshot(item), 'merged': True, 'at': stamp_now}
                continue
            if not accounts:
                continue
            body = item['why'][:1].upper() + item['why'][1:] + '.'
            dedupe = 'fleet-brief:' + hashlib.sha256(f'{fleet}|{sig}'.encode()).hexdigest()[:24]
            try:
                card = self.brief_card(accounts[0], dedupe, item['title'], body, item['domain'], quiet)
            except ValueError as error:
                LOG.warning('fleet brief todo error=%s', type(error).__name__)
                continue
            mine[key] = {'card': card, 'sig': sig, 'item': snapshot(item), 'merged': False, 'at': stamp_now}
            made += 1
        for key, entry in mine.items():  # a line the newest brief no longer has: settled, as the brief settled it
            if key not in seen and not entry.get('closed'):
                self._brief_todo_close(mine, key, 'complete', t(SETTLED.get(entry['item'].get('kind'), SETTLED['overlap'])))
        self._brief_todos_save({**self._brief_todos(), fleet: mine})
        self.set_meta(SYNCED, {**(self.meta(SYNCED) or {}), fleet: stamp})
        return made

    def _brief_target(self, db, item, cards):
        """An open to-do of the owner's about the same company: one about that organization, or (for a waiting email)
        one with mail from it on its evidence. The brief's own to-dos of this round count too: one per company."""
        org = todo_org.card_org(db, item.get('domain')) if item.get('domain') else ''
        marks = ','.join('?' * len(OPEN))
        if org:
            row = db.execute(f'SELECT id FROM suggestions WHERE org=? AND status IN ({marks}) ORDER BY created_at DESC LIMIT 1', (org, *OPEN)).fetchone()
            if row:
                return row['id']
        for card in cards:  # one made for another line of this company (its org may be one the Graph doesn't know)
            entry = next((e for f in self._brief_todos().values() for e in f.values() if e['card'] == card), None)
            if entry and entry['item'].get('domain') == item.get('domain') and self._card_status(db, card) in OPEN:
                return card
        if item.get('kind') != 'waiting' or not item.get('mine') or not item.get('domain'):
            return None
        row = db.execute(f"SELECT s.id FROM suggestions s, json_each(s.event_ids) j JOIN events e ON e.id=j.value WHERE s.status IN ({marks}) "
                         "AND e.kind='gmail.message' AND instr(lower(json_extract(e.metadata,'$.from')),?)>0 ORDER BY s.created_at DESC LIMIT 1",
                         (*OPEN, '@' + item['domain'].lower())).fetchone()
        return row['id'] if row else None

    def _brief_rhythm(self, db, accounts, domain):
        """The usual days between the owner's contacts with a company over the last year (their own work mail), or 0."""
        if not accounts or not domain:
            return 0
        since = (timeutil.clock() - dt.timedelta(days=365)).isoformat(timespec='seconds')
        rows = db.execute(f"SELECT DISTINCT substr(occurred_at,1,10) FROM events WHERE kind='gmail.message' AND deleted=0 AND account_id IN ({','.join('?' * len(accounts))}) "
                          "AND occurred_at>? AND (instr(lower(json_extract(metadata,'$.from')),?)>0 OR instr(lower(json_extract(metadata,'$.to')),?)>0) ORDER BY 1",
                          (*accounts, since, '@' + domain.lower(), '@' + domain.lower())).fetchall()  # from and to: plain keys
        days = [dt.date.fromisoformat(r[0]) for r in rows]
        gaps = [(b - a).days for a, b in zip(days, days[1:])]
        return int(statistics.median(gaps)) if len(gaps) >= 3 else 0


    def _brief_repliers(self, ref, item):
        """The addresses of the people a waiting email went to (the teammates named on its line, and the owner when it
        went to them too): a reply from one of them in the owner's own copy of its thread answers it."""
        import fleet as fleet_module
        if item.get('kind') != 'waiting':
            return set()
        to = set(item.get('to') or ())
        labels = {p.get('label') for p in item.get('team') or [] if p.get('name') in to}
        found = {str(e).lower() for m in self.teammates(ref) if fleet_module.clean(fleet_module.label(m), 120) in labels for e in m.get('emails') or ()}
        return found | ({str(e).lower() for e in self.my_emails()} if item.get('to_me') else set())

    def _brief_context(self, db, item, accounts, repliers=()):
        """What the owner's own Machine knows that makes a brief line specific: the company's open projects in their
        Graph (`stake`), whether it is a customer, and the exchange the line hangs on (`gist`): for a waiting email, the
        message from them on its day (the review's line about it, else its subject); for a quiet company, the last one
        from them. `answered`: the owner's own copy of that email's thread (a shared CRM inbox, cc) already has a reply
        from someone it went to (`repliers`), which the brief hadn't seen. Only the owner's own work accounts and Graph: a
        teammate's Machine shares no message for a brief."""
        domain = str(item.get('domain') or '').lower()
        org = todo_org.card_org(db, domain) if domain else ''
        out = {'org': org, 'stake': [], 'customer': False, 'gist': None, 'latest': None, 'answered': False}
        if org:
            out['stake'] = [p for p in graph.org_projects(db, org) if p.get('open')][:STAKES_SHOWN]
            row = db.execute("SELECT info FROM graph_nodes WHERE id=?", (org,)).fetchone()
            out['customer'] = bool(row and json.loads(row['info'] or '{}').get('paying'))
        exchange = self._brief_exchange(db, org, domain, accounts)
        found = [m for m in exchange if m['them']]
        out['latest'] = found[0] if found else None
        if item.get('kind') == 'waiting':
            try:
                day = dt.date.fromisoformat(str(item.get('at') or '')[:10])
            except ValueError:
                day = None
            near = [m for m in found if day and abs((dt.date.fromisoformat(m['at'][:10]) - day).days) <= 1]
            out['gist'] = next((m for m in near if m.get('line')), near[0] if near else None)
            repliers = set(repliers)
            out['answered'] = any(r['thread'] == m['thread'] and r['at'] > m['at'] and r['address'] in repliers
                                  for m in near if m['thread'] for r in exchange if not r['them'])
        elif item.get('kind') == 'quiet':
            out['gist'] = next((m for m in found if m.get('line')), out['latest'])
        return out

    def _brief_exchange(self, db, org, domain, accounts, limit=40):
        """Messages with the company on the owner's work accounts, newest first: each its event, subject, sender, when,
        its mail thread, whether it came from them (`them`), and the review's one line about it (share_lines: written for
        client threads only), where there is one."""
        if not accounts or not domain:
            return []
        marks = ','.join('?' * len(accounts))
        ids, names = [], {}
        if org:  # the people of the organization: mail, chats, Intercom, a shared CRM inbox
            for name, info in db.execute("SELECT n.name,n.info FROM graph_links l JOIN graph_nodes n ON n.id=l.a WHERE l.b=? AND l.kind='member' AND n.kind='person'", (org,)):
                for i in json.loads(info or '{}').get('identifiers') or ():
                    if str(i).startswith('email:'):
                        names.setdefault(str(i)[6:].lower(), name)  # a bare address (a CRM copy) shows as the person
            ids = [r[0] for r in db.execute("SELECT g.event_id FROM graph_events g JOIN graph_links l ON l.a=g.node_id WHERE l.b=? AND l.kind='member' "
                                            "GROUP BY g.event_id ORDER BY MAX(g.at) DESC LIMIT 60", (org,))]
        ids += [r[0] for r in db.execute(f"SELECT id FROM events WHERE kind='gmail.message' AND deleted=0 AND account_id IN ({marks}) "
                                         "AND (instr(lower(json_extract(metadata,'$.from')),?)>0 OR instr(lower(json_extract(metadata,'$.to')),?)>0) "
                                         "ORDER BY occurred_at DESC LIMIT 30", (*accounts, '@' + domain, '@' + domain))]
        if not ids:
            return []
        try:
            lines = {r[0]: r[1] for r in db.execute(f"SELECT event_id,line FROM share_lines WHERE event_id IN ({','.join('?' * len(ids))})", ids)}
        except sqlite3.OperationalError:  # no Team Graph here
            lines = {}
        out = []
        for r in db.execute(f"SELECT id,title,occurred_at,metadata FROM events WHERE id IN ({','.join('?' * len(ids))}) AND deleted=0 "
                            f"AND account_id IN ({marks}) AND occurred_at<=? ORDER BY occurred_at DESC LIMIT ?",
                            (*ids, *accounts, timeutil.clock().isoformat(timespec='seconds'), limit)):
            m = json.loads(r['metadata'] or '{}')
            sender = str(m.get('from') or '')
            name = ' '.join(sender.split('<')[0].replace('"', '').split()) if '<' in sender else ''
            them = '@' + domain in sender.lower() and 'SENT' not in set(m.get('labels') or ())
            address = ((graph.addresses(sender) or [('', '')])[0][1] or '').lower()
            out.append({'event': r['id'], 'subject': str(r['title'] or '')[:160], 'from': (name or names.get(address) or sender)[:80], 'at': r['occurred_at'],
                        'them': them, 'thread': str(m.get('thread_id') or ''), 'address': address, **({'line': lines[r['id']]} if lines.get(r['id']) else {})})
        return out

    def _brief_todo_close(self, mine, key, choice, why):
        """One line done with: its own to-do closes (choice, why) unless another open line still holds it; a to-do
        the line only joined stays the owner's."""
        entry = mine[key]
        entry.update(closed=True, at=timeutil.clock().isoformat(timespec='seconds'))
        if entry.get('merged') or any(e['card'] == entry['card'] and not e.get('closed') for e in mine.values()):
            return
        with self.connect() as db:
            if self._card_status(db, entry['card']) not in OPEN:
                return
        try:
            self.done_card(entry['card'], choice, why, 'fleet-brief-' + choice + '-' + hashlib.sha256((entry['card'] + entry['sig']).encode()).hexdigest()[:16])
        except (ValueError, KeyError, TypeError) as error:
            LOG.info('fleet brief todo close error=%s', type(error).__name__)

    def _brief_lines_of(self, card_id):
        return [(f, k) for f, lines in self._brief_todos().items() for k, e in lines.items() if e['card'] == str(card_id) and not e.get('closed')]

    def brief_todo_settle(self, fleet, key, choice='reject', why=None):
        """Not needed on a brief line (the old API too): its to-do closes the same way."""
        found = self._brief_todos()
        mine = {k: dict(e) for k, e in (found.get(fleet) or {}).items()}
        if key in mine and not mine[key].get('closed'):
            self._brief_todo_close(mine, key, choice, why or t('Not needed'))
            self._brief_todos_save({**self._brief_todos(), fleet: mine})

    def brief_todo_skip(self, card_id):
        """Not needed on the to-do: every line it holds is hidden from the brief (an overlap learned, hide_brief_item).
        Returns whether the to-do is the brief's own, which the app then closes as the owner's own Not needed."""
        found = self._brief_todos()
        lines = self._brief_lines_of(card_id)
        if not lines:
            raise OwnerError('That to-do is no longer in the team brief')
        own = not all(found[f][k].get('merged') for f, k in lines)
        for fleet, key in lines:
            found[fleet][key] = {**found[fleet][key], 'closed': True, 'at': timeutil.clock().isoformat(timespec='seconds')}
        self._brief_todos_save(found)
        for fleet, key in lines:
            try:
                self.hide_brief_item(fleet, key)
            except ValueError:  # that brief is gone: the to-do still goes
                pass
        return {'skipped': [k for _, k in lines], 'close': own}

    def brief_todo_closed(self, card_id, choice):
        """The owner closed a to-do some brief line is on, the usual way: Not needed teaches the brief as its own
        Not needed does; done closes the lines quietly."""
        lines = self._brief_lines_of(card_id)
        if not lines or choice not in ('reject', 'complete'):
            return
        found = self._brief_todos()
        for fleet, key in lines:
            found[fleet][key] = {**found[fleet][key], 'closed': True, 'at': timeutil.clock().isoformat(timespec='seconds')}
        self._brief_todos_save(found)
        if choice == 'reject':
            for fleet, key in lines:
                try:
                    self.hide_brief_item(fleet, key)
                except ValueError:  # that brief is gone
                    pass

    def brief_todo_ask(self, card_id, text):
        """Ask on the to-do: the Fleet's free question, as the owner left it; its answers show on the to-do."""
        import fleet as fleet_module
        lines = self._brief_lines_of(card_id)
        if not lines:
            raise OwnerError('That to-do is no longer in the team brief')
        ref, key = lines[0]
        question = fleet_module.parse_question('anything', {'text': text})
        if not question:
            raise OwnerError('Ask a question of at least a few words')
        sent, context = self.ask_context('anything', question, 'free:', ref)
        self.brief_todo_asked(ref, question['text'], context, key)
        return {**sent, 'asked': context}

    def brief_todo_asked(self, fleet, text, context, key=None):
        """A free question about a brief line (from its to-do, or the same question asked on the old API) shows on it."""
        found = self._brief_todos()
        mine = found.get(fleet) or {}
        key = key or next((k for k, e in mine.items() if not e.get('closed') and ' '.join(str(e['item'].get('ask') or '').split()) == ' '.join(str(text).split())), None)
        if key in mine:
            mine[key] = {**mine[key], 'asked': context}
            self._brief_todos_save({**found, fleet: mine})

    # -- what the to-do shows
    def annotate_brief(self, db, suggestions):
        """`fleet_brief` on each open to-do a brief line is on: its lines (title, why, Ask's question, the company and
        the team's people linked to their pages, Details), whether the to-do is the brief's own, and an Ask's answers."""
        by_card = {}
        for ref, lines in self._brief_todos().items():
            for key, e in lines.items():
                if not e.get('closed'):
                    by_card.setdefault(e['card'], []).append((ref, key, e))
        shown = [s for s in suggestions if by_card.get(str(s.get('id'))) and s.get('status') in OPEN]
        if not shown:
            return
        try:
            marks = shared_graph_kept.fleet_marks(db, self.fleets())
        except Exception as error:  # noqa: BLE001 - no Graph yet: names without links
            LOG.info('fleet brief marks error=%s', type(error).__name__)
            marks = {}
        nodes = {(x['fleet'], x['member_id']): node for node, m in marks.items() for x in m.get('in') or []}
        for s in shown:
            entries = by_card[str(s['id'])]
            asked = next((e['asked'] for _, _, e in entries if e.get('asked')), None)
            s['fleet_brief'] = {'own': not all(e.get('merged') for _, _, e in entries),
                                'items': [self._brief_line_view(db, ref, e['item'], nodes) for ref, _, e in entries],
                                **({'asked': self._brief_asked(db, asked)} if asked else {})}

    def _brief_people(self, ref, team, nodes):
        import fleet as fleet_module
        members = {fleet_module.clean(fleet_module.label(m), 120): m['member_id'] for m in self.teammates(ref)}
        return [{'name': p.get('name') or p.get('label'), **({'node': nodes[(ref, members[p['label']])]} if (ref, members.get(p.get('label'))) in nodes else {})}
                for p in team or []]

    def _brief_line_view(self, db, ref, item, nodes):
        org = todo_org.card_org(db, item.get('domain')) if item.get('domain') else ''
        team = self._brief_people(ref, item.get('team'), nodes)
        threads, also = [], []
        try:
            _, section = self.team_for(db, org or self._brief_team_org(db, item.get('domain')))
        except Exception as error:  # noqa: BLE001 - nothing shared about them: the line alone
            LOG.info('fleet brief section error=%s', type(error).__name__)
            section = None
        if section:  # only what teammates' Machines shared with this one (team_section: never a private thread)
            threads = [{'subject': x.get('subject') or '', 'from': x.get('from') or '', 'at': x.get('at') or '', 'via': x.get('via') or ''}
                       for x in section['threads'][:THREADS_SHOWN]]
            named = {p['name'] for p in team}
            also = [p['name'] for p in section['people'] if p.get('name') and p['name'] not in named]
        ctx = self._brief_context(db, item, self.fleet_accounts(ref), self._brief_repliers(ref, item))
        shown = lambda m: {k: m[k] for k in ('event', 'subject', 'from', 'at', 'line') if m.get(k)}
        gist, own = ctx.get('gist'), ctx.get('latest')
        stake = [{'id': p['id'], 'name': _stake_name(p['name'], item.get('org')), **({'stage': p['stage']} if p.get('stage') else {})} for p in ctx['stake']]
        # what they wrote is in a teammate's mail only: say so, and who to ask
        unshared = item['kind'] == 'waiting' and not item.get('to_me') and not gist and not threads
        return {'key': item['key'], 'kind': item['kind'], 'title': item['title'], 'why': item['why'], 'ask': item.get('ask') or '',
                'open': item.get('open') or '', 'at': item.get('at') or '', 'mine': bool(item.get('mine')),
                'org': {'id': org or self._brief_team_org(db, item.get('domain')) or '', 'name': item.get('org') or ''},
                'team': team, 'also': also, 'threads': threads, 'stake': stake,
                **({'gist': shown(gist)} if gist else {}), **({'own': shown(own)} if own and (not gist or own['event'] != gist['event']) else {}),
                **({'unshared': [p['name'] for p in team if p['name'] in (item.get('to') or [])] or [p['name'] for p in team][:1]} if unshared else {})}

    def _brief_team_org(self, db, domain):
        """A company only teammates have in their Graph: its Team record's key, by the hashed domain, else ''."""
        if not domain:
            return ''
        import shared_graph
        hashes = {shared_graph.keyed(k['key'], 'domain:' + domain.lower()) for ref in self.work_fleets() for k in self.graph_keys(ref).values()}
        if not hashes:
            return ''
        try:
            for entry in self.team_graph(db):
                if entry['kind'] == 'org' and any(hashes & set(s['record']['d'] if isinstance(s['record'].get('d'), list) else [s['record'].get('d')])
                                                  for s in entry['sources']):
                    return entry['local'] or entry['key']
        except Exception as error:  # noqa: BLE001 - no Team Graph yet
            LOG.info('fleet brief team org error=%s', type(error).__name__)
        return ''

    def _brief_asked(self, db, context):
        rows = db.execute('SELECT * FROM fleet_out WHERE context=? ORDER BY at', (context,)).fetchall()
        if not rows:
            return None
        import fleet as fleet_module
        late = (timeutil.clock() - dt.timedelta(hours=fleet_module.FREE_WAIT_HOURS)).isoformat(timespec='seconds')
        answers = []
        for r in rows:
            answer = json.loads(r['answer']) if r['answer'] else None
            state = ('answered' if r['status'] == 'answered' and answer else 'no answer' if r['status'] in ('declined', 'expired') or r['at'] < late
                     else 'waiting')
            answers.append({'name': r['name'], 'state': state, 'text': (answer or {}).get('text') if state == 'answered' else None})
        return {'question': json.loads(rows[0]['question']).get('text', ''), 'at': rows[0]['at'], 'answers': answers}
