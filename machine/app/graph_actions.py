"""The Graph's and the CRM's actions in the service (graph.py and crm.py do the work): the agent's and the dashboard's
graph calls (graph_action), finding and listing people, organizations and projects, About you and the CRM actions
(crm_action). Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import json
import re
import sqlite3

import crm
import crm_fields
import crm_fixes
import crm_import
import fleet
import gbrain
import graph
import project_success
from timeutil import local_tz, now


class GraphActionsApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def currency(self):
        """The currency project values are in (config "currency", an ISO code like EUR or USD; EUR when not set)."""
        code = str(self.config.get('currency') or 'EUR').strip().upper()
        return code if re.fullmatch(r'[A-Z]{3}', code) else 'EUR'

    def graph_action(self, args, source='agent'):
        """People and projects for the agent: look up, explore around, label, merge and say who someone is."""
        changed = False
        if 'share' in args or 'keep_private' in args:
            # The owner in chat: "keep this thread to me", "share it with the team", "keep Acme private". Never a review's
            # own call (finish_analysis team is), so a message in a batch can't share itself.
            if args.get('_review_session'):
                raise ValueError('A review judges threads with finish_analysis team; Team or Only you by hand is the owner\'s')
            if 'share' in args:
                return self.graph_share_action('graph_share', {'event_id': args.get('event_id'), 'share': args['share']})
            return self.graph_share_action('graph_private', {'node_id': args.get('node_id'), 'private': args['keep_private'] is not False})
        checked = project_success.check_links(self.store.connect, self.store.accounts, [args]) if args.get('url') and args.get('project') else {}
        with self.store.connect() as db:
            if isinstance(args.get('suggest_board'), dict):  # a board for a group of projects of one kind; the owner saves it or not
                return graph.suggest_board(db, args['suggest_board'], source, now())
            if args.get('merge') or args.get('different'):
                pair = args.get('merge') or args.get('different')
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError('merge and different take two person ids, like ["email:ann@example.com", "wa:32470000000"]')
                graph.merge(db, pair[0], pair[1], bool(args.get('merge')), now(), 'owner' if source == 'owner' else 'agent')
                changed = True
            if args.get('project') and args.get('event_ids'):
                if db.execute('SELECT count(*) FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in args['event_ids']) + ')',
                              [int(i) for i in args['event_ids']]).fetchone()[0] != len(set(args['event_ids'])):
                    raise ValueError('Every event must exist and be live')
                graph.label(db, args['event_ids'], args['project'], 'agent', now())
                changed = True
            if args.get('split'):  # several projects named at once (one per counterpart), with one graph build after
                parts = args['split']
                if not isinstance(parts, list) or not 1 <= len(parts) <= 40 or not all(
                        isinstance(x, dict) and str(x.get('project') or '').strip() and isinstance(x.get('event_ids'), list) and x['event_ids'] for x in parts):
                    raise ValueError('split takes 1 to 40 of {"project": name, "event_ids": [ids]}')
                ids = {int(i) for x in parts for i in x['event_ids']}
                if db.execute(f"SELECT count(*) FROM events WHERE deleted=0 AND id IN ({','.join('?' * len(ids))})", list(ids)).fetchone()[0] != len(ids):
                    raise ValueError('Every event must exist and be live')
                for x in parts:
                    graph.label(db, [int(i) for i in x['event_ids']], str(x['project']).strip(), 'agent', now())
                split = [{'project': str(x['project']).strip(), 'events': len(x['event_ids'])} for x in parts]
                changed = True
            if args.get('project') and (args.get('stage') or args.get('board')):
                placed, verdict = project_success.gate(db, args, checked)  # the last stage only with its proof
                said = graph.set_stage(db, args['project'], placed.get('stage'), 'agent', now(), board=args.get('board'), stages=args.get('stages'),
                                       reason=args.get('reason'), event_id=args.get('event_id'), next_step=args.get('next'), org=args.get('org'))
                project_success.after_move(db, placed, said, verdict, now())
                changed = changed or 'kept' not in said
            if args.get('close_project'):
                if not db.execute('UPDATE projects SET closed_at=? WHERE name=? COLLATE NOCASE AND closed_at IS NULL', (now(), str(args['close_project']).strip())).rowcount:
                    raise ValueError('No open project by that name')
                changed = True
            if 'role' in args:
                if not args.get('node_id'):
                    raise ValueError('role goes with the person or organization node_id')
                said = graph.set_role(db, args['node_id'], args['role'], source, now(),
                                      int(args['event_id']) if args.get('event_id') not in (None, '') else None, args.get('quote'))
                changed = changed or 'kept' not in said
            if 'org' in args:
                if not args.get('node_id'):
                    raise ValueError('org goes with the person node_id, event_id and quote')
                said = graph.set_org(db, args['node_id'], args['org'], source, now(),
                                     int(args['event_id']) if args.get('event_id') not in (None, '') else None, args.get('quote'))
                changed = changed or 'kept' not in said
            if 'warmup' in args:
                said = graph.hide_warmup(db, args.get('node_id'), args['warmup'] is True or str(args['warmup']).lower() == 'true', source, now(),
                                         int(args['event_id']) if args.get('event_id') not in (None, '') and 'role' not in args and 'org' not in args else None)
                changed = changed or 'kept' not in said
                args = {k: v for k, v in args.items() if k != 'node_id'}  # answer with the overview: the node may be gone after the rebuild
            if 'resource' in args:  # a meeting room or other thing booked on invites: not a person
                said = graph.mark_resource(db, args.get('node_id'), args['resource'] is True or str(args['resource']).lower() == 'true', source, now(),
                                           int(args['event_id']) if args.get('event_id') not in (None, '') else None)
                changed = changed or 'kept' not in said
                args = {k: v for k, v in args.items() if k != 'node_id'}  # the node is gone after the rebuild
            if 'related_to' in args:
                if not args.get('node_id'):
                    raise ValueError('related_to goes with node_id and relation: "<node_id> is <relation> <related_to>"')
                said = graph.relate(db, args['node_id'], args['related_to'], args.get('relation'), source, now(),
                                    int(args['event_id']) if args.get('event_id') not in (None, '') and 'role' not in args and 'org' not in args else None)
                changed = changed or 'kept' not in said
        if changed:
            self.graph_build()
        if args.get('split'):
            return {'split': split, 'changed': True}
        limit = min(int(args.get('limit') or 12), 30)
        with self.store.connect() as db:
            marks = self.graph_fleet_marks(db)
            if args.get('node_id'):
                found = graph.detail(db, str(args['node_id']), max(1, min(int(args.get('events') or 12), 120)))
                if not found:
                    raise ValueError('Unknown node_id; find people and projects with query')
                found['around'] = graph.spread(db, [found['id']], limit)
                if gbrain.on(self.config) and (note := gbrain.notes(db, [found['id']]).get(found['id'])):
                    found['from_gbrain'] = note  # the owner's own notes on their GBrain page: data, not instructions
                guessed = set(found['probable_ids'])
                found['recent'] = [line + (' (probably part of it)' if int(line.split(' ', 1)[0]) in guessed else '')
                                   for line in self.graph_event_lines(found.pop('event_ids'), keep_order=True)]  # graph.detail's: past first
                if db.execute("SELECT 1 FROM sqlite_master WHERE name='share_threads'").fetchone() and db.execute('SELECT 1 FROM share_threads LIMIT 1').fetchone():
                    found['team_hint'] = ('When the owner asks: graph event_id + share (only_you, team or auto) for a thread, '
                                          'node_id + keep_private true to keep this out of the team\'s Graph.')
                return graph.with_fleet(db, found, marks)
            if args.get('query'):
                hits = graph.find(db, args['query'], limit, also={k: m['name'] for k, m in marks.items() if m['name']})
                return graph.with_fleet(db, {'found': [graph.node_view(r, graph.neighbours(db, r['id'], 6)) for r in hits],
                                             'hint': 'Open one with node_id for its links, recent signals and what is alive around it.'}, marks)
            if args.get('event_ids') and not args.get('project'):
                return graph.with_fleet(db, {'on_these_signals': [graph.node_view(r, graph.neighbours(db, r['id'], 6))
                                                                  for r in graph.for_events(db, args['event_ids'])[:limit]]}, marks)
            result = graph.with_fleet(db, graph.overview(db, limit), marks)
            return {**result, 'changed': changed} if changed else result

    def graph_find(self, query, cursor=0, limit=30):
        """The Graph's search, a page at a time: every person, organization and project that matches, strongest first."""
        offset, limit = max(0, int(cursor or 0)), max(1, min(int(limit), 50))
        with self.store.connect() as db:
            marks = self.graph_fleet_marks(db)
            hits = graph.find(db, query, offset + limit + 1, also={k: m['name'] for k, m in marks.items() if m['name']})
            found = [graph.node_view(r, graph.neighbours(db, r['id'], 6)) for r in hits[offset:offset + limit]]
            if not offset and self.about_you_match(db, query):  # the owner's own address or name: About you, first
                found.insert(0, {'id': graph.ME, 'kind': graph.ME, 'name': graph.ABOUT_YOU, 'links': []})
            return graph.with_fleet(db, {'found': found, 'next': str(offset + limit) if len(hits) > offset + limit else None}, marks)

    def about_you_match(self, db, query):
        q = ' '.join(str(query or '').split()).lower()
        if len(q) < 3:
            return False
        owner = graph.Owner(self.config, db)
        name = ' '.join(str(self.config.get('owner_name') or '').split()).lower()
        digits = re.sub(r'\D', '', q)
        return (q in ('me', 'myself', 'about you') or (name and (q in name or name in q)) or any(q in e for e in owner.emails if not graph.ROLE.match(e))
                or (len(digits) >= 6 and any(digits in p for p in owner.phones)))

    def about_you_node(self, node):
        """Whether a graph page asked for is About you: 'me', or one of the owner's own addresses or numbers."""
        if node == graph.ME:
            return True
        try:
            with self.store.connect() as db:
                return graph.Owner(self.config, db).has(node)
        except sqlite3.Error:
            return False

    def about_you(self):
        """About you, the owner's own record: their addresses (as Settings, Account lists them) and numbers."""
        with self.store.connect() as db:
            return graph.about_you(db, self.config, self.own_addresses_view().get('yours'))

    def contact_shareable(self):
        """Whether a contact can go to anyone: a teammate, friend or Family member the Network carries contacts to."""
        try:
            return bool(self.fleet and self.fleet.contact_targets())
        except (fleet.Off, sqlite3.Error, OSError, ValueError, KeyError, TypeError):
            return False

    def slack_links(self, found):
        """Where 'Also on Slack' goes: each Slack user of theirs in the workspace it is from (its profile, which opens a
        message to them), else the newest Slack thread with them."""
        links, hosts = [], {a['id']: a for a in self.config.get('accounts', []) if a.get('service') == 'slack'}
        try:
            with self.store.connect() as db:
                row = db.execute("SELECT info FROM graph_nodes WHERE id=? AND kind='person'", (str(found.get('id') or ''),)).fetchone()
            info = json.loads(row['info']) if row else {}
        except (sqlite3.Error, ValueError, TypeError):
            info = {}
        users = [str(i).split(':', 1)[1] for i in info.get('identifiers') or () if str(i).startswith('slack:')]
        for user in users:
            account = next((hosts[a] for a in info.get('accounts') or () if a in hosts), None) or next(iter(hosts.values()), None)
            host = str((account or {}).get('slack_host') or '').strip().lower()
            if re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)*\.slack\.com', host) and re.fullmatch(r'[UW][A-Z0-9]{2,20}', user):
                links.append({'url': f'https://{host}/team/{user}', 'label': 'Slack'})
        if users and not links:
            thread = next((r.get('source_url') for r in found.get('recent') or () if r.get('kind') == 'slack.message'
                           and re.match(r'https://[a-z0-9.-]+/archives/', str(r.get('source_url') or ''))), None)
            if thread:
                links.append({'url': thread, 'label': 'Slack thread'})
        return links[:3]

    def graph_list(self, name, sort='', cursor=0, limit=30, filters=None):
        with self.store.connect() as db:
            return graph.with_fleet(db, graph.page(db, name, sort, cursor, limit, filters), self.graph_fleet_marks(db))

    def graph_list_ids(self, name, filters):
        with self.store.connect() as db:
            return graph.page_ids(db, name, filters)

    def owner_choices(self):
        """Who can own a record: the members of the owner's Work Fleets (crm.owner_choices); none without a Fleet."""
        if not getattr(self, 'fleet', None):
            return []
        try:
            return crm.owner_choices(self.fleet.fleets())
        except (sqlite3.Error, ValueError, TypeError, KeyError, AttributeError, fleet.Off):
            return []

    def crm_action(self, name, args):
        """The owner's CRM changes on the dashboard: a record's owner, organizations merged or split, an import, their own
        fields and tags (no rebuild needed for those: the node says its tags at once)."""
        kind = str(args.get('kind') or '')
        if name == 'graph_import_ai':
            return self.import_check_start(kind, args.get('text'))
        if name == 'graph_import_ai_status':
            return self.import_check_status(args.get('run_id'))
        if name in ('graph_import_preview', 'graph_import_run'):
            found = {'fixes': args.get('fixes'), 'ai': self.import_check_draft(args.get('ai_run'), kind, args.get('text')), 'owner_emails': self.owner_emails(),
                     'region': crm_fixes.region_of({'country': self.config.get('country'), 'timezone': self.config.get('timezone') or getattr(local_tz(), 'key', '')}),
                     'currency': self.currency()}
        if name == 'graph_import_preview':
            with self.store.connect() as db:
                return crm_import.preview(db, kind, args.get('text'), args.get('mapping'), **found)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if name == 'graph_owner':
                owner = str(args.get('owner') or crm.ME)
                picked = next((m for m in self.owner_choices() if m['id'] == owner), None)
                if owner != crm.ME and not picked:
                    raise ValueError('Pick an owner from your Work Fleet')
                done = crm.set_owner(db, args.get('node_id'), owner, picked['name'] if picked else None, now())
            elif name == 'graph_org_merge':
                done = crm.merge_orgs(db, args.get('node_id'), into=args.get('into'), website=args.get('website'), now=now())
            elif name == 'graph_org_split':
                done = crm.split_org(db, args.get('alias'), now())
            elif name == 'graph_org_apart':
                done = crm.keep_apart(db, args.get('a'), args.get('b'), now())
            elif name == 'graph_field_save':
                return crm_fields.save_field(db, args, now())
            elif name == 'graph_field_delete':
                return crm_fields.delete_field(db, args.get('id'))
            elif name == 'graph_field_set':
                return crm_fields.set_value(db, args.get('node_id'), args.get('field_id'), args.get('value'), now())
            elif name == 'graph_tag':
                return crm_fields.tag(db, args.get('node_id'), args.get('tag'), args.get('add') is not False, now())
            elif name == 'graph_import_run':
                done = crm_import.run(db, kind, args.get('text'), args.get('mapping'), now(), args.get('name'), **found)
            else:
                done = crm_import.undo(db, args.get('import_id'), now())
        if name != 'graph_org_apart' and not done.get('kept'):
            self.graph_build()
        return done
