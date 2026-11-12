"""Shared Boards (docs/shared-graph.md): the team's pipelines from what teammates shared, mixed into SharedGraph. A tile
per project, laid out as on its owner's board: same order, days, next step, organization and unanswered mail, with
only what sharing withholds left out."""
import collections
import datetime as dt
import json

import graph


class TeamBoards:
    def _yours(self, db, e, rec, me_ids, my_mail, todos):
        """(yours, needs you) of a teammate's project here: this Machine's owner is on one of its shared threads, owns
        it, has it in their own Graph or has an open to-do about it; it needs them when that to-do is open or the newest
        message of a thread they're on came from someone else to them. From what was shared already, nothing more."""
        import shared_graph as sg
        on, waiting = bool(e['local']) or rec.get('owner') in me_ids, False
        for s in e['sources']:
            for tag in (s['record'].get('threads') or [])[:40]:
                row = db.execute('SELECT body FROM team_mail WHERE fleet=? AND member=? AND tag=?', (s['fleet'], s['member'], tag)).fetchone()
                body = json.loads(row['body']) if row else {}
                if body.get('private') or not sg.on_thread(body, my_mail):
                    continue
                on = True
                last = (body.get('messages') or [{}])[-1]
                if isinstance(last, dict):
                    sender = sg.addresses({'from': last.get('from')})
                    waiting = waiting or bool(sender and not set(sender) & my_mail and set(sg.addresses({'to': last.get('to'), 'cc': last.get('cc')})) & my_mail)
        todo = todos.get(str(rec.get('name') or '').casefold(), 0) > 0
        return on or todo, todo or waiting

    @staticmethod
    def _last_line(e):
        """What happened last on a teammate's project, with its date: the newest line of its shared timeline from every
        source, a review's line or a move before a bare title ("Chat: …"), with chat markup (<mailto:a|b>) read as text."""
        import shared_graph as sg
        lines = [x for s in e['sources'] for x in (s['record'].get('timeline') or []) if isinstance(x, dict) and x.get('line')]
        last = max(lines, key=lambda x: (not str(x['line']).startswith(sg.TITLE_WORDS), str(x.get('at') or '')), default=None)
        return {'line': sg.plain_line(last['line']), 'line_at': last.get('at')} if last else {}

    def team_boards(self, db, entries, shared):
        """Shared Boards: the team's pipelines. A tile per project, with its owner (the closest), its stage (the newest
        move by hand, else the newest a message showed), who moved it and its newest timeline line. Each tile says
        whether it is this Machine's owner's own (yours) and needs them (needs_you), for Mine and Needs me; the boards
        with most of theirs come first."""
        import shared_graph as sg
        team_ids, hidden = graph.team_board_ids(db), {'project:' + str(i) for i in graph.hidden_project_ids(db)}
        mine = {b['name'].casefold(): b for b in graph.boards(db, sg.now()) if b['id'] in team_ids}  # an Only-you board never shows here
        me_ids = {m['member_id'] for m in (self._me_in(g) for g in self._kept_groups()) if m and m.get('member_id')}
        my_mail = {x.lower() for x in self.my_emails()}
        todos = collections.Counter()
        if graph._has_column(db, 'suggestions', 'project'):
            for r in db.execute("SELECT project FROM suggestions WHERE status IN (SELECT value FROM json_each(?)) AND coalesce(project,'')<>''",
                                (json.dumps(graph.OPEN_CARD),)):
                todos[str(r['project']).casefold()] += 1
        boards = {}
        for name, b in mine.items():
            projects = [dict(p, mine=True, yours=True, needs_you=bool(p.get('todos'))) for p in b['projects'] if p['id'] in shared and p['id'] not in hidden]
            boards[name] = {'name': b['name'], 'stages': b['stages'], 'projects': projects, 'stuck': 0, 'team': True, 'yours': True,
                            'seen': b['visibility'] if b['visibility'] in ('team', 'people') else None}
        names = {(f, m): (s.get('name') or '') for (f, m), s in self.team_sources().items()}
        for e in entries:
            if e['kind'] != 'project':
                continue
            mine_tile = next((p for b in boards.values() for p in b['projects'] if p['id'] == e['local']), None)
            local_record = None
            if mine_tile:
                local_record = {'stage': mine_tile['stage'], 'stage_hand': mine_tile['by'] == 'owner', 'stage_at': mine_tile['at'], 'board': None,
                                'score': next((n['strength'] for n in [graph.node_view(r) for r in db.execute('SELECT * FROM graph_nodes WHERE id=?', (e['local'],))]), 0)}
            rec = sg.resolve(e, local_record)
            board_name = next((s['record'].get('board') for s in e['sources'] if s['record'].get('board')), None)
            if not board_name:
                continue
            board = boards.get(board_name.casefold())
            if not board:
                stages = next((s['record'].get('stages') for s in e['sources'] if s['record'].get('stages')), None) or [graph.STALLED]
                board = boards[board_name.casefold()] = {'name': board_name, 'stages': [{'name': x} for x in stages if x != graph.STALLED] + [{'name': graph.STALLED, 'side': True}],
                                                         'projects': [], 'stuck': 0, 'team': True}
            for src in e['sources']:  # whose board it is, and whether it is the whole team's or shared with chosen teammates
                if not board.get('yours') and str(src['record'].get('board') or '').casefold() == board_name.casefold():
                    if (who := sg._first_name(names.get((src['fleet'], src['member']), ''))) and who not in board.setdefault('by', []):
                        board['by'].append(who)
                    if (seen := src['record'].get('board_seen')) == 'people' or (seen == 'team' and not board.get('seen')):
                        board['seen'] = seen
            names_ok = [x['name'] for x in board['stages']]
            stage = rec.get('stage') if rec.get('stage') in names_ok else names_ok[0]
            mover = names.get(next(((s['fleet'], s['member']) for s in e['sources'] if s['member'] == rec.get('stage_by')), None), '')
            best = max(e['sources'], key=lambda s: s['record'].get('score') or 0)['record']
            src = next((s['record'] for s in e['sources'] if s['member'] == rec.get('stage_by')), best)  # whose stage it shows
            # as on the owner's board: in a stage since its move (or since it was added), sorted newest first, and how
            # long the owner's last message has gone unanswered
            since = rec.get('stage_at') or src.get('since')
            age = lambda at: max(0, (dt.datetime.now(dt.timezone.utc) - graph.parse_time(at)).days) if at else None
            days, waited = age(since) or 0, age(src.get('waiting'))
            tile = {'id': e['local'] or e['key'], 'name': rec['name'], 'stage': stage, 'reason': rec.get('why') or best.get('why'),
                    'by': 'owner' if rec.get('stage_hand') else 'review', 'mover': sg._first_name(mover) if rec.get('stage_by') else None,
                    'at': rec.get('stage_at'), 'since': since, 'event_id': None, 'next': rec.get('next'), 'first': False, 'days': days, 'closed': False,
                    'no_reply_days': waited, 'org': {'name': rec['org'].get('name'), 'logo': self._org_logo(db, rec['org'])} if rec.get('org') else None, 'card': None,
                    'owner': rec.get('owner'), 'owner_name': rec.get('owner_name'), 'fleet': e['sources'][0]['fleet'], 'via': sg.via(e['sources']),
                    'team_only': not e['local'], 'owner_hand': bool(rec.get('owner_hand')), **self._last_line(e)}
            if mine_tile:
                mine_tile.update(owner=tile['owner'], owner_name=tile['owner_name'], via=tile['via'], fleet=tile['fleet'], stage=stage if rec.get('stage_by') else mine_tile['stage'])
            else:
                tile['yours'], tile['needs_you'] = self._yours(db, e, rec, me_ids, my_mail, todos)
                board['projects'].append(tile)
        for b in boards.values():  # the owner's board's order: the newest move first (graph_boards.boards)
            b['projects'].sort(key=lambda p: str(p.get('since') or p.get('at') or ''), reverse=True)
            b['stuck'] = sum(1 for p in b['projects'] if (p.get('no_reply_days') or 0) >= graph.STUCK_DAYS and p['stage'] != graph.STALLED)
        out = [b for b in boards.values() if b['projects']]
        return sorted(out, key=lambda b: -sum(1 for p in b['projects'] if p.get('yours')))  # stable: otherwise as before

    def _org_logo(self, db, org):
        """A teammate's project's organization's logo: this Machine's own one when it knows the organization, else the
        LinkedIn one the teammate sent (team_logo), else the picture of its own site's logo a teammate sent with it."""
        import shared_graph as sg
        index = self.hash_index(db)
        local = next((index[h] for h in org.get('d') or () if str(index.get(h, '')).startswith('org:')), None)
        return (local and graph.org_card(db, local[4:])['logo']) or sg.team_logo(org.get('logo')) or sg.logos.by_domain(db, org)
