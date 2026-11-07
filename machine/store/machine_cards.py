"""The Machine's own to-dos, a Store mixin: changes an update set aside (parked_fixes.py) and problems in the
computer's own logs (machine/system_logs.py). Each goes through Store.machine_card, which writes it."""
import datetime as dt

import parked_fixes
from machine import system_logs
from timeutil import now


class MachineCardsStore:
    def parked_fix_cards(self, account_id, items):
        """A to-do for each change an update set aside (parked_fixes.pending), once. Returns how many are new."""
        return sum(self.machine_card(account_id, 'machine.parked_fix', 'parked:' + item['sha'], *parked_fixes.card(item),
                                     {'commit': item['sha'], 'subject': item['subject'], 'changes': item['changes']}, item['sha'])
                   for item in items)

    def system_log_cards(self, account_id, findings, quiet=system_logs.QUIET, per_day=system_logs.PER_DAY):
        """A to-do for each problem in the computer's own logs (system_logs.detect), quietly: the same problem at most
        once in `quiet` and never while its to-do is still open, and at most `per_day` new ones a day. Returns how many
        are new."""
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
                                  "OR EXISTS(SELECT 1 FROM suggestions s, json_each(s.event_ids) i WHERE i.value=e.id AND s.status IN ('pending','snoozed')))",
                                  (len(key) + 1, key + ':', since)).fetchone()
            if seen:
                continue
            title, body, signal = system_logs.card(finding)
            metadata = {k: finding.get(k) for k in ('kind', 'name', 'unit', 'program', 'count', 'signal', 'piece')}
            metadata.update(transport='journald', coverage='Problems in this computer’s own logs; never log text.')
            made += self.machine_card(account_id, 'machine.system_log', f'{key}:{stamp[:10]}', title, body, signal, metadata,
                                      at=finding.get('last_at'))
        return made
