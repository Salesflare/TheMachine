"""The team brief's lines as to-dos (2026-11-12). Mixed into fleet.Fleet, next to fleet_brief.py.

A line of "What the Fleet saw" ("Globex is waiting for a reply", "Initech went quiet") is something for the owner to
decide, so it is a to-do in For you, not a box of its own in the Fleet tab:

- Once a brief is told (all answered, or BRIEF_SETTLE passed), each of its lines gets a Work to-do: its title, the
  line's why as its context, the company as its organization. The to-do carries Ask (the Fleet's free question,
  prefilled) and Not needed (Fleet.hide_brief_item: hidden, and an overlap learned).
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
import statistics

from fleet_brief import brief_items
from i18n import t
import shared_graph_kept
import todo_org

LOG = logging.getLogger('personal-assistant')
META = 'brief_todos'
SYNCED = 'brief_todos_synced'  # {fleet: the brief's built_at and the day it was read on}: nothing new, nothing to do
KEEP_DAYS = 30  # a closed line is remembered this long: the same thing doesn't come back as a to-do
OPEN = ('pending', 'accepted', 'prepared', 'instructions', 'snoozed')
SETTLED = {'waiting': 'Someone on the team replied or took it on', 'quiet': 'Back in touch with them',
           'overlap': 'No longer in the team brief', 'meeting': 'No longer in the team brief'}  # read through t()
THREADS_SHOWN = 3


def signature(item):
    """The line and the day it hangs on: the same waiting email, meeting or last contact is the same thing."""
    return f"{item['key']}|{item.get('at') or ''}"


def snapshot(item):
    keep = ('key', 'kind', 'title', 'why', 'ask', 'open', 'org', 'domain', 'at', 'known', 'team', 'mine')
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

    # -- state
    def _brief_todos(self):
        return self.meta(META) or {}

    def _brief_todos_save(self, found):
        cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds')
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
        made, seen, stamp_now = 0, set(), dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
        for item in items:
            key, sig = item['key'], signature(item)
            seen.add(key)
            entry = mine.get(key)
            with self.connect() as db:
                if item['kind'] == 'quiet':
                    words = rhythm_words(self._brief_rhythm(db, accounts, item['domain']))
                    item = {**item, 'why': item['why'] + (', ' + words if words else '')}
                if entry and not entry.get('closed'):
                    if self._card_status(db, entry['card']) in OPEN:
                        entry.update(item=snapshot(item), sig=sig)
                        continue
                    entry.update(closed=True, at=stamp_now)  # the owner closed it: as they left it
                if entry and entry['sig'] == sig:
                    continue  # closed for this very thing: only something new brings it back
                target = self._brief_target(db, item, {e['card'] for k, e in mine.items() if not e.get('closed') and k in seen})
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
        since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)).isoformat(timespec='seconds')
        rows = db.execute(f"SELECT DISTINCT substr(occurred_at,1,10) FROM events WHERE kind='gmail.message' AND deleted=0 AND account_id IN ({','.join('?' * len(accounts))}) "
                          "AND occurred_at>? AND (instr(lower(json_extract(metadata,'$.from')),?)>0 OR instr(lower(json_extract(metadata,'$.to')),?)>0) ORDER BY 1",
                          (*accounts, since, '@' + domain.lower(), '@' + domain.lower())).fetchall()  # from and to: plain keys
        days = [dt.date.fromisoformat(r[0]) for r in rows]
        gaps = [(b - a).days for a, b in zip(days, days[1:])]
        return int(statistics.median(gaps)) if len(gaps) >= 3 else 0

    def _brief_todo_close(self, mine, key, choice, why):
        """One line done with: its own to-do closes (choice, why) unless another open line still holds it; a to-do
        the line only joined stays the owner's."""
        entry = mine[key]
        entry.update(closed=True, at=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
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
            raise ValueError('That to-do is no longer in the team brief')
        own = not all(found[f][k].get('merged') for f, k in lines)
        for fleet, key in lines:
            found[fleet][key] = {**found[fleet][key], 'closed': True, 'at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
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
            found[fleet][key] = {**found[fleet][key], 'closed': True, 'at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
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
            raise ValueError('That to-do is no longer in the team brief')
        ref, key = lines[0]
        question = fleet_module.parse_question('anything', {'text': text})
        if not question:
            raise ValueError('Ask a question of at least a few words')
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
        own = self._brief_own_mail(db, ref, item) if item.get('mine') else None
        return {'key': item['key'], 'kind': item['kind'], 'title': item['title'], 'why': item['why'], 'ask': item.get('ask') or '',
                'open': item.get('open') or '', 'at': item.get('at') or '', 'mine': bool(item.get('mine')),
                'org': {'id': org or self._brief_team_org(db, item.get('domain')) or '', 'name': item.get('org') or ''},
                'team': team, 'also': also, 'threads': threads, **({'own': own} if own else {})}

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

    def _brief_own_mail(self, db, ref, item):
        """The owner's own newest mail from that company on this Fleet's accounts: subject, sender and when."""
        accounts = self.fleet_accounts(ref)
        if not accounts or not item.get('domain'):
            return None
        row = db.execute(f"SELECT title,occurred_at,json_extract(metadata,'$.from') AS sender FROM events WHERE kind='gmail.message' AND deleted=0 "
                         f"AND account_id IN ({','.join('?' * len(accounts))}) AND instr(coalesce(json_extract(metadata,'$.labels'),''),'\"SENT\"')=0 "
                         "AND instr(lower(json_extract(metadata,'$.from')),?)>0 ORDER BY occurred_at DESC LIMIT 1",
                         (*accounts, '@' + item['domain'].lower())).fetchone()
        if not row:
            return None
        sender = ' '.join(str(row['sender'] or '').split('<')[0].replace('"', '').split()) or str(row['sender'] or '')
        return {'subject': str(row['title'] or '')[:160], 'from': sender[:80], 'at': row['occurred_at']}

    def _brief_asked(self, db, context):
        rows = db.execute('SELECT * FROM fleet_out WHERE context=? ORDER BY at', (context,)).fetchall()
        if not rows:
            return None
        import fleet as fleet_module
        late = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=fleet_module.FREE_WAIT_HOURS)).isoformat(timespec='seconds')
        answers = []
        for r in rows:
            answer = json.loads(r['answer']) if r['answer'] else None
            state = ('answered' if r['status'] == 'answered' and answer else 'no answer' if r['status'] in ('declined', 'expired') or r['at'] < late
                     else 'waiting')
            answers.append({'name': r['name'], 'state': state, 'text': (answer or {}).get('text') if state == 'answered' else None})
        return {'question': json.loads(rows[0]['question']).get('text', ''), 'at': rows[0]['at'], 'answers': answers}
