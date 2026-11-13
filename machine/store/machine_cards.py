"""The Machine's own to-dos, a Store mixin: changes an update set aside (parked_fixes.py) and problems in the
computer's own logs (machine/system_logs.py). Each goes through machine_card, which writes it. Do it on one from the
logs runs only its one safe fix (machine_fix), never an AI run. Redo it on a fix an update set aside (parked_redo)
starts the usual self-fix run from that commit, merged only through the usual Merge fix checks."""
import datetime as dt
import hashlib
import json

import ms_graph
import parked_fixes
from machine import system_logs
from timeutil import now

# A sign-in from before a newer feature (machine/app/reconnect_asks.py): its to-do's signal, one per account and ask
RECONNECT_KIND = 'machine.reconnect_ask'
RECONNECT_SOURCES = {'microsoft': 'outlook'}  # a sign-in's source under + Add, which a self-hosted Machine's Reconnect redoes


def reconnect_source(account, ask):
    return f'reconnect:{ask}:{account}'


def reconnect_lead(db, suggestion_id):
    """{provider, email, account, source} of an open reconnect to-do, which its Reconnect opens the sign-in of, else
    None. A hosted Machine's dashboard opens `provider`'s sign-in under + Add; a self-hosted one (no account page) signs
    in its `source` again, the way its Connections card's Reconnect does."""
    row = db.execute("SELECT e.metadata,e.account_id FROM suggestions s JOIN events e ON e.id=json_extract(s.event_ids,'$[0]') "
                     "WHERE s.id=? AND s.origin='machine' AND e.kind=?", (suggestion_id, RECONNECT_KIND)).fetchone()
    try:
        meta = json.loads(row['metadata'] or '{}') if row else {}
    except ValueError:
        return None
    if not isinstance(meta, dict) or not meta.get('provider'):
        return None
    return {'provider': meta['provider'], 'email': meta.get('email') or '', 'account': row['account_id'] or '',
            'source': RECONNECT_SOURCES.get(meta['provider'], meta['provider'])}


def reconnect_reword(db, suggestion_id, title, body):
    """An open reconnect to-do's words, made again to fit what reconnecting brings now (reconnect_asks.reword)."""
    db.execute("UPDATE suggestions SET title=?,body=? WHERE id=? AND status IN ('pending','snoozed')", (title[:90], body[:699], suggestion_id))


def reconnected(db, account, ask, at):
    """The account's reconnect to-do, if open, closes itself as done: its sign-in has what it asked for now."""
    for row in db.execute("SELECT s.id FROM suggestions s JOIN events e ON e.id=json_extract(s.event_ids,'$[0]') WHERE e.kind=? "
                          "AND e.source_id=? AND s.status IN ('pending','snoozed')", (RECONNECT_KIND, reconnect_source(account, ask))).fetchall():
        db.execute("UPDATE suggestions SET status='completed',completed_from='pending',snoozed_until=NULL,resume_status=NULL,early=0 WHERE id=?", (row[0],))
        db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   ('reconnected:' + row[0], row[0], 'complete', 'Reconnected: the sign-in has it now.', 'assistant', at))
        db.execute("UPDATE deliveries SET status='cancelled',reminder=0,updated_at=? WHERE suggestion_id=? AND message_id IS NULL", (at, row[0]))


def machine_fix_finding(db, suggestion_id):
    """The finding of an open to-do from the computer's logs whose safe fix Do it may run, else None."""
    row = db.execute("SELECT e.metadata FROM suggestions s JOIN events e ON e.id=json_extract(s.event_ids,'$[0]') "
                     "WHERE s.id=? AND s.origin='machine' AND e.kind='machine.system_log'", (suggestion_id,)).fetchone()
    finding = json.loads(row['metadata'] or '{}') if row else {}
    return finding if finding.get('fix') else None


def parked_redo(db, suggestion_id):
    """The set-aside fix ({commit, subject}) a to-do of an update's is about, which Redo it makes again, else None."""
    row = db.execute("SELECT e.metadata FROM suggestions s JOIN events e ON e.id=json_extract(s.event_ids,'$[0]') "
                     "WHERE s.id=? AND s.origin='machine' AND e.kind='machine.parked_fix'", (suggestion_id,)).fetchone()
    try:
        return parked_fixes.redoable(json.loads(row['metadata'] or '{}')) if row else None
    except (ValueError, TypeError, AttributeError):
        return None


class MachineCardsStore:
    def machine_card(self, account_id, kind, source_id, title, body, signal, metadata, digest=None, at=None, quiet=False):
        """A to-do of The Machine's own (an update's note, a problem in the computer's logs) with its signal, once per
        source_id: the signal is already read, so no review makes a second one. `quiet`: on the dashboard only, never
        pushed or in a digest. Whether it is new."""
        stamp = now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            cursor = db.execute('INSERT OR IGNORE INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,'
                                'version,analyzed_version,ingested_at) VALUES(?,?,?,?,?,?,?,0,?,1,1,?)',
                                (account_id, source_id, kind, at or stamp, title, signal, json.dumps(metadata),
                                 hashlib.sha256((digest or source_id).encode()).hexdigest(), stamp))
            if not cursor.rowcount:
                return False
            card = self.suggest(source_id, title[:90], body[:699], [cursor.lastrowid], when='now', owner_step=True, _db=db)
            db.execute("UPDATE suggestions SET origin='machine' WHERE id=?", (card['id'],))  # no thread to read, nothing to plan
            if quiet:
                db.execute("UPDATE deliveries SET status='cancelled',reminder=0,updated_at=? WHERE suggestion_id=? AND message_id IS NULL",
                           (stamp, card['id']))
        return True

    def parked_fix_cards(self, account_id, items):
        """A to-do for each change an update set aside (parked_fixes.pending), once. Returns how many are new."""
        return sum(self.machine_card(account_id, 'machine.parked_fix', 'parked:' + item['sha'], *parked_fixes.card(item),
                                     {'commit': item['sha'], 'subject': item['subject'], 'changes': item['changes']}, item['sha'])
                   for item in items)

    def system_log_cards(self, account_id, findings, quiet=system_logs.QUIET, per_day=system_logs.PER_DAY):
        """A to-do for each problem in the computer's own logs (system_logs.detect), quietly: the same problem at most
        once in `quiet`, never while its to-do is still open and never again once the owner said Not needed, and at
        most `per_day` new ones a day. Returns how many are new."""
        made = 0
        stamp = now()
        since = (dt.datetime.fromisoformat(stamp) - quiet).isoformat()
        day = (dt.datetime.fromisoformat(stamp) - dt.timedelta(days=1)).isoformat()
        with self.connect() as db:
            today = db.execute("SELECT count(*) FROM events WHERE kind='machine.system_log' AND ingested_at>=?", (day,)).fetchone()[0]
        for finding in findings:
            if today + made >= per_day:
                break
            key = 'syslog:' + finding['key']
            with self.connect() as db:
                seen = db.execute("SELECT 1 FROM events e WHERE e.kind='machine.system_log' AND substr(e.source_id,1,?)=? AND (e.ingested_at>=? "
                                  "OR EXISTS(SELECT 1 FROM suggestions s, json_each(s.event_ids) i WHERE i.value=e.id AND s.status IN ('pending','snoozed','rejected')))",
                                  (len(key) + 1, key + ':', since)).fetchone()
            if seen:
                continue
            title, body, signal = system_logs.card(finding)
            metadata = {k: finding.get(k) for k in ('kind', 'name', 'unit', 'program', 'count', 'signal', 'piece', 'pid')}
            metadata.update(transport='journald', coverage='Problems in this computer’s own logs; never log text.')
            if not system_logs.fix_command(finding):
                metadata.pop('fix', None)  # no safe fix here (its command is missing): no Do it
            else:
                metadata['fix'] = finding['fix']
            made += self.machine_card(account_id, 'machine.system_log', f'{key}:{stamp[:10]}', title, body, signal, metadata,
                                      at=finding.get('last_at'))
        return made

    def machine_fix_finding(self, db, suggestion_id):
        return machine_fix_finding(db, suggestion_id)

    def machine_fix_views(self, db, cards):
        """machine_log on each to-do from the computer's logs, so it keeps Not needed (cards.controls, the dashboard),
        machine_fix on each such open one with a safe fix: the command Do it runs, so it offers Do it, and parked_redo on
        each open one about a fix an update set aside, so it offers Redo it."""
        ids = [c['id'] for c in cards if c.get('origin') == 'machine']
        for n in range(0, len(ids), 500):
            chunk = ids[n:n + 500]
            logs = {r[0] for r in db.execute("SELECT s.id FROM suggestions s JOIN events e ON e.id=json_extract(s.event_ids,'$[0]') "
                                             f"WHERE e.kind='machine.system_log' AND s.id IN ({','.join('?' * len(chunk))})", chunk)}
            for card in cards:
                if card['id'] in logs:
                    card['machine_log'] = True
        for card in cards:
            if card.get('origin') == 'machine' and card.get('status') in ('pending', 'prepared'):
                finding = self.machine_fix_finding(db, card['id'])
                argv = system_logs.fix_command(finding) if finding else None
                if argv and (card['status'] == 'pending' or json.loads(card.get('outcome') or '{}').get('state') == 'answered'):
                    card['machine_fix'] = ' '.join(argv)
            # a fix an update set aside, still open: Redo it starts the usual self-fix run (cards.controls says when).
            # 'redo' while nothing runs on it (pending, or a result that only answered): the dashboard offers Redo it then
            if card.get('origin') == 'machine' and card.get('status') in ('pending', 'accepted', 'instructions', 'prepared') \
                    and not card.get('machine_log') and parked_redo(db, card['id']):
                card['parked_redo'] = 'redo' if card['status'] == 'pending' or json.loads(card.get('outcome') or '{}').get('state') == 'answered' else True
            # a sign-in from before a newer feature, still open: Reconnect leads (reconnect_asks.py), Not needed closes it for good
            if card.get('origin') == 'machine' and card.get('status') in ('pending', 'snoozed'):
                lead = reconnect_lead(db, card['id'])
                if lead:
                    # personal: an Outlook.com account, which has no admin: its sign-in step shows no admin's approval link
                    accounts = getattr(self, 'accounts', None) or (getattr(self, 'config', None) or {}).get('accounts') or []
                    account = next((a for a in accounts if isinstance(a, dict) and a.get('id') == lead['account']), None)
                    card['reconnect'] = {**lead, 'personal': bool(account and lead['provider'] == 'microsoft' and ms_graph.personal(account))}

    def machine_fix(self, job):
        """Do it on a to-do from the computer's logs (its preparation starting from the owner's Do it): runs its one
        safe fix (system_logs.run_fix) and saves how it went as the to-do's result, in its chat. A run that didn't work
        leaves Do it there to try again. False for every other preparation, a chat message on it among them."""
        with self.connect() as db:
            finding = self.machine_fix_finding(db, job['suggestion_id'])
            asked = db.execute('SELECT choice FROM decisions WHERE id=?', (job.get('decision_id'),)).fetchone()
        if not finding or not asked or asked['choice'] != 'accept':
            return False
        ok, text = system_logs.run_fix(finding)
        with self.connect() as db:
            db.execute("UPDATE preparation_runs SET status='machine_fix',finished_at=? WHERE job_id=?", (now(), job['job_id']))  # no AI run
            row = db.execute('SELECT body,outcome FROM suggestions WHERE id=?', (job['suggestion_id'],)).fetchone()
        try:  # the to-do keeps its text; how each run went is its reply in the chat (card_chat_service)
            ran = (json.loads(row['outcome'] or '{}') or {}).get('fix_results', [])[-4:] + [{'job_id': job['job_id'], 'text': text}]
            self.prepare(job['suggestion_id'], row['body'], job_id=job['job_id'],
                         outcome={'state': 'done' if ok else 'answered', 'fix_results': ran})
        except ValueError:  # closed or snoozed meanwhile: its result has no place, and the fix never runs a second time
            with self.connect() as db:
                db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE job_id=?", (now(), job['job_id']))
        return True
