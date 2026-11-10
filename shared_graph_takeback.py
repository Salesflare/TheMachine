"""Taking back what is no longer shared while nothing new goes out (docs/shared-graph.md): this Machine's sharing is
off, or the Fleet's is paused. The other half of shared_graph's graph_publish, mixed into SharedGraph: empty blobs for
the threads, and a delta for the records that can only make them smaller."""
import collections
import hashlib
import json

import network_crypto as nc

SHRINKS = ('timeline', 'threads', 'people')  # what a record lists of the threads it came from
SOURCED = ('why', 'next', 'org')            # what a record says from one source, or about someone else


def shrunk(sent, had, current):
    """What is left of the records the team has, for a take-back (graph_take_back): (hashes {rid: hash} of what the
    team has after it, the records that changed, the ids of those that are gone). sent: {rid: record} as they went;
    current: as they would go now; had: {rid: hash} of what went. A record that would no longer go is gone. One that
    would is what went, less the lines, threads and people that are no longer on it, and without a reason, next step or
    organization that is no longer the same: never what it would be now, so nothing new is on it. sent None (this
    Machine's copies don't add up): only the records that are gone are taken back, the rest stays as it is."""
    import shared_graph as sg
    digest_of = lambda r: hashlib.sha256(sg.canon(r)).hexdigest()
    if sent is None:
        removed = sorted(rid for rid in had if rid not in current)
        return {rid: h for rid, h in had.items() if rid in current}, [], removed
    left, changed, removed = {}, [], []
    for rid, was in sent.items():
        would = current.get(rid)
        if would is None or would.get('t') != was.get('t'):
            removed.append(rid)
            continue
        after = dict(was)
        for field in SHRINKS:
            if isinstance(was.get(field), list):
                after[field] = [x for x in was[field] if x in (would.get(field) or [])]
        for field in SOURCED:
            if was.get(field) is not None and was.get(field) != would.get(field):
                after[field] = None
        if after != was:
            changed.append(after)
        left[rid] = digest_of(after)
    return left, changed, sorted(removed)


class TakeBack:
    def graph_take_back(self, group, me, found):
        """The take-back half of graph_publish, for while this Machine's sharing is off (an admin agreed) or the Fleet's
        is paused: what went before and is no longer shared (Only you by hand, someone kept private, a board back to
        Only you) still leaves the team's Machines. A thread as an empty blob (_unshare), on the take-back budget; the
        records as a delta that can only shrink (shrunk): records that are gone, and timeline lines, threads and
        people that are, taken out of what the team already has. Nothing new ever goes this way: no thread, file or
        record, no new line on a record, to nobody who didn't have it. Nothing at all when nothing went before."""
        import shared_graph as sg
        fleet = group['id']
        to = sorted(set(found) - {me['member_id']})
        with self.connect() as db:
            sg.ensure(db)
            before = {(r['kind'], r['key']): r['hash'] for r in db.execute('SELECT kind,key,hash FROM share_out WHERE fleet=?', (fleet,))}
        keys = self.graph_keys(fleet)
        if not before or not to or not keys:
            return
        state = self.meta('graph_out:' + fleet, {}) or {}
        kept = self.meta('graph_chains:' + fleet, {}) or {}
        kv = state.get('kv') if state.get('kv') in keys else self.graph_key(fleet)[0]
        # hashed as when it went (that key first), so what is compared is the same record
        order = [keys[kv]['key'], *[k['key'] for kv_, k in sorted(keys.items(), key=lambda x: x[1]['at'], reverse=True) if kv_ != kv][:3]]
        secret = self.graph_secret()
        with self.connect() as db:
            scope = sg.Scope(db, self.graph_accounts(fleet), self.internal(fleet), self.my_emails(), self._personal_people(db))
            went = {k for (kind, k) in before if kind == 'thread'}
            held = set()
            records, threads, _, _ = sg.collect(db, scope, order, secret, held=held, kept=went)
            records.update(sg.fleet_learnings.records(db, fleet, lambda local: sg.keyed(secret, 'record|' + local)))
            by_grant = collections.defaultdict(list)
            granted = sg.grants(db, fleet)
            for m in to:
                by_grant[granted.get(m)].append(m)
            by_grant.pop(None, None)
            chains = {}
            for grant, members in by_grant.items():
                c_records, c_threads, _, _ = sg.collect(db, scope.granted(*grant), order, secret, kept=went)
                chains[sg.keyed(secret, 'chain|' + fleet + '|' + ','.join(members))] = (c_records, c_threads)
            sent = {None: self._sent_records(db, fleet, me['member_id'], None, state.get('last')),
                    **{chain: self._sent_records(db, fleet, me['member_id'], chain, st.get('last')) for chain, st in kept.items()}}
        held = {tag for tag in held if ('thread', tag) in before and tag not in threads}
        shared = set(threads) | {tag for _, c_threads in chains.values() for tag in c_threads}
        gone = self._budget(gone=True)
        try:
            for tag in [k for (kind, k) in before if kind == 'thread' and k not in shared and k not in held]:
                if gone <= 0:
                    break
                gone -= self._unshare(group, me, to, tag, before)
        except Exception as error:  # noqa: BLE001 - the Network's own limit, or away: the rest next round
            sg.LOG.info('shared graph take-backs paused fleet=%s error=%s', fleet, type(error).__name__)
            return
        if self._budget() <= 0:
            return
        if state.get('to') and state.get('last'):
            had = {k: h for (kind, k), h in before.items() if kind == 'record'}
            left, changed, removed = shrunk(sent[None], had, records)
            listed = sorted(set(state.get('threads') or []) & (set(threads) | held))
            if changed or removed or listed != sorted(state.get('threads') or []):
                header = self._put(group, me, 'delta', {'kv': kv, 'prev': state['last'], 'records': changed, 'removed': removed, 'threads': listed},
                                   [m for m in state['to'] if m in to], kv=kv)
                if not header:
                    return
                state.update(last=header['seq'], threads=listed)
                with self.connect() as db:
                    sg.went_records(db, fleet, left)
                self.set_meta('graph_out:' + fleet, state)
                sg.LOG.info('shared graph taken back while off fleet=%s records=%s removed=%s', fleet, len(changed), len(removed))
        for chain, st in kept.items():  # what was shared by name: the same, for those it went to
            if not st.get('to') or not st.get('last'):
                continue
            c_records, c_threads = chains.get(chain) or ({}, {})  # no longer shared with them by name: all of it
            left, changed, removed = shrunk(sent[chain], st.get('hashes') or {}, c_records)
            listed = sorted(set(st.get('threads') or []) & (set(c_threads) | held))
            if changed or removed or listed != sorted(st.get('threads') or []):
                header = self._put(group, me, 'delta', {'kv': kv, 'prev': st['last'], 'records': changed, 'removed': removed, 'threads': listed},
                                   [m for m in st['to'] if m in to], kv=kv, only=True, tag=chain)
                if not header:
                    continue
                kept[chain] = {**st, 'last': header['seq'], 'threads': listed, 'hashes': left}
                self.set_meta('graph_chains:' + fleet, kept)

    def graph_out(self, group, me):
        """This Machine is not a confirmed member. If an admin's signed remove says why (kept in graph_removed by
        confirmed()): what the team shared with it goes, and if it is let back in it asks again for what it missed."""
        at = (self.meta('graph_removed:' + group['id']) or {}).get(me['member_id'])
        if not at:
            return False
        self.set_meta('graph_confirmed:' + group['id'], None)
        self.set_meta('graph_want:' + group['id'], None)
        return self.graph_taken_out(group, me, at)

    def graph_nudge(self, group, me, member):
        """After an admin's remove: one empty blob for that member's Machine alone, so the Network rings it and it looks
        at the Fleet now (graph_look). It carries nothing and decides nothing: without it, their next round does it."""
        import shared_graph as sg
        try:
            self._put(group, me, 'want', None, [member], tag=sg.keyed(self.graph_secret(), 'look|' + group['id'] + '|' + member))
        except (ValueError, OSError, KeyError, TypeError) as error:
            sg.LOG.info('shared graph nudge error=%s', type(error).__name__)

    def graph_look(self, fleet):
        """An admin's Machine asked this one to look at the Fleet again: it reads the directory now and acts only on a
        signed remove it finds there (graph_out). Anything else waits for the round, as before. Whether it is out."""
        group = next((g for g in (self.directory(refresh=True).get('fleets') or []) if g.get('id') == fleet and g.get('kind') == 'work'), None)
        me = group and self._me_in(group)
        if not me or me['member_id'] in self.confirmed(group)[0]:
            return False
        self.graph_out(group, me)
        return me['member_id'] in (self.meta('graph_removed:' + fleet) or {})

    def graph_taken_out(self, group, me, at):
        """An admin took this Machine out of the team's Graph (signed, at): what teammates shared with it goes from
        here, once per removal. Their records, threads and files, by-name shares among them, and the copies kept to
        pass on. Only that: the owner's own people, organizations, projects, messages and to-dos are other tables and
        stay as they are, as does what this Machine shared itself (the team keeps that, and it goes on from there if
        an admin lets it back in). The signed remove is what brings it, so it arrives whenever this Machine is next
        on, however long it was away and whichever teammates are away then."""
        fleet, mine = group['id'], me['member_id']
        if str(at) <= str(self.meta('graph_taken_out:' + fleet) or ''):
            return False
        import shared_graph as sg
        with self.connect() as db:
            sg.ensure(db)
            had = sg.drop_received(db, fleet, mine)
            if had:
                self.log(db, 'in', fleet, None, str(group.get('name') or 'Your team')[:80], 'graph', 'What the team shared',
                         'removed from this Machine: an admin took it out of the team Graph')
        self.set_meta('graph_taken_out:' + fleet, str(at))
        sg.LOG.info('shared graph taken out fleet=%s removed=%s', fleet, had)
        return True

    @staticmethod
    def _sent_records(db, fleet, member, chain, last):
        """{rid: record} as this Machine's last snapshot and the deltas since gave them to the team (chain: those of one
        chain shared by name, None for the whole team's), from its own copies of them (keep_blob). None when they
        don't add up to the last one sent."""
        import shared_graph as sg
        out, seq = None, None
        try:
            for row in db.execute("SELECT kind,seq,dk,header,ct FROM team_blobs WHERE fleet=? AND member=? AND kind IN ('snapshot','delta') "
                                  'AND tag IS ? ORDER BY seq', (fleet, member, chain)).fetchall():
                body = sg.decrypt(nc.unb64(row['dk'], 32), json.loads(row['header']), nc.unb64(row['ct']))
                if row['kind'] == 'snapshot':
                    out = {}
                elif out is None or body.get('prev') != seq:
                    return None
                out.update((r['r'], r) for r in body.get('records') or [])
                for rid in body.get('removed') or []:
                    out.pop(rid, None)
                seq = row['seq']
        except (nc.SealError, ValueError, KeyError, TypeError):
            return None
        return out if out is not None and seq == last else None
