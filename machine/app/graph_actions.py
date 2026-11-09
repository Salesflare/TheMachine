"""The Graph's and the CRM's actions in the service (graph.py and crm.py do the work): the agent's and the dashboard's
graph calls (graph_action), finding and listing people, organizations and projects, About you and the CRM actions
(crm_action). Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import base64
import binascii
import contextlib
import json
import re
import sqlite3
import time

import crm
import crm_fields
import crm_fixes
import crm_import
import embeddings
import enrichment
import fleet
import gap_note
import gbrain
import graph
import mail_senders
from machine.actions import CRM_ACTIONS
from machine.config import LOG, WORKSPACE
from machine.sources.calendar import calendar_room, calendar_rooms
from machine.store.cards import source_line, source_text
from machine.store.review import own_message
from machine.text import clamp
from machine.web.handler import event_glance
import meeting_notes
import own_addresses
import project_success
from sources import gog_read, SourceError
from timeutil import local_tz, now
import work_removal


GRAPH_CHECK_SECONDS = 60  # how often the graph worker looks for new organization profiles
GRAPH_RETRY_SECONDS = 5   # a build that met edits on the way: the next try
GRAPH_LOCK_AFTER = 1800   # this long without a published build: the last try holds the write lock (graph.build lock_last)


def account_services(config, account_ids=None):
    """The services of the configured accounts, or of only these account IDs (no service is Gmail)."""
    wanted = None if account_ids is None else set(account_ids)
    return [a.get('service', 'gmail') for a in config.get('accounts', []) if wanted is None or a.get('id') in wanted]


def forget_in_notes(root, needles):
    """Takes out the lines of the agent's memory notes (Markdown and text under memory/) that name someone deleted
    permanently: their full name or an address. Returns how many lines went."""
    if not needles or not root.is_dir():
        return 0
    removed = 0
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in ('.md', '.txt') or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.splitlines(keepends=True)
        kept = [line for line in lines if not graph.mentions(line, needles)]
        if len(kept) != len(lines):
            removed += len(lines) - len(kept)
            path.write_text(''.join(kept), encoding='utf-8')
    return removed


class GraphActionsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'graph': 'graph_query_action', 'undo_merge': 'undo_merge_action',
               'remember_fact': 'remember_fact_action', 'graph_summary': 'graph_summary_action',
               'graph_fact_unlink': 'graph_fact_unlink_action', 'unmerge_fact': 'unmerge_fact_action',
               'graph_rename': 'graph_rename_action', 'graph_stage': 'graph_stage_action',
               'graph_org_edit': 'graph_org_edit_action', 'graph_org_wrong': 'graph_org_edit_action',
               'graph_new': 'graph_new_action', 'graph_org_delete': 'graph_new_action',
               'graph_picture': 'graph_picture_action', 'graph_pictures_found': 'graph_picture_action',
               'graph_person_edit': 'graph_person_edit_action', 'graph_role': 'graph_role_action',
               'graph_warmup': 'graph_warmup_action', 'graph_same': 'graph_same_action',
               'graph_same_all': 'graph_same_all_action', 'graph_show_person': 'graph_show_person_action', 'graph_person_delete': 'graph_person_delete_action',
               'graph_person_org': 'graph_person_org_action', 'graph_relation': 'graph_relation_action',
               'forget_fact': 'forget_fact_action', 'edit_fact': 'edit_fact_action', 'board_save': 'board_action',
               'board_delete': 'board_action', 'board_dismiss': 'board_action',
               'project_visibility': 'project_visibility_action', 'project_save': 'project_action',
               'project_outcome': 'project_action', 'project_archive': 'project_action',
               'project_delete': 'project_action', 'board_default': 'project_action', 'board_fit': 'project_action',
               **dict.fromkeys(CRM_ACTIONS, 'crm_actions_action')}

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
            # The owner's Merge or Not the same: the Same person? card is gone from the table already, the rebuild that
            # joins them runs in the graph worker (a whole build in the request held the database for its tens of seconds)
            (self.graph_later if source == 'owner' and (args.get('merge') or args.get('different')) else self.graph_build)()
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
                if args.get('lines', True):
                    found['recent'] = [line + (' (probably part of it)' if int(line.split(' ', 1)[0]) in guessed else '')
                                       for line in self.graph_event_lines(found.pop('event_ids'), keep_order=True)]  # graph.detail's: past first
                else:  # the dashboard's record page: its timeline shows them, only their ids are asked
                    found['recent'] = found.pop('event_ids')
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
            if name == 'hidden_senders':  # mailings the Graph left out (mail_senders.py)
                return mail_senders.hidden_page(db, cursor, limit)
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
            self.graph_later()  # the owner's edit is saved; its people and projects follow in the graph worker's rebuild
        return done

    def graph_later(self):
        """A rebuild after an owner's edit whose answer doesn't need the rebuilt Graph: the graph worker runs it at once
        (graph_dirty), so the edit answers right away instead of after a whole build (seconds, more with history). Without
        the worker (a command, a test) it builds here, as before."""
        if self.__dict__.get('graph_worker_on'):
            self.graph_dirty.set()
        else:
            self.graph_build()

    def graph_build(self, lock_last=True):
        with self.store.connect() as db:
            db.isolation_level = None  # graph.build runs its own transaction
            return graph.build(db, self.config, now(), self.fleet_addresses(), self.fleet_circles(), history=True, lock_last=lock_last)

    def graph_event_lines(self, event_ids, keep_order=False):
        """One line per signal, newest first (keep_order: in the order given): "<id> (<account>) <what, from whom, when> ·
        <title>". A signal that can't be read is logged and left out, so one odd event never fails a whole page."""
        event_ids = list(event_ids)
        rows = self.store.events([a['id'] for a in self.config['accounts']], event_ids=event_ids) if event_ids else []
        lines = []
        place = {e: i for i, e in enumerate(event_ids)}
        for r in sorted(rows, key=lambda r: place.get(r['id'], 0)) if keep_order else sorted(rows, key=lambda r: str(r['occurred_at'] or ''), reverse=True):
            try:
                lines.append(f"{r['id']} ({r['account_id']}) {source_text(r)} · {clamp(' '.join(str(r['title'] or '').split()), 100)}")
            except (ValueError, KeyError, TypeError, AttributeError) as error:
                LOG.warning('graph event line skipped event=%s error=%s', r.get('id') if isinstance(r, dict) else '?', type(error).__name__)
        return lines

    def graph_timeline(self, node, source='', cursor=0, limit=40, now=None):
        """A page of a person's, organization's or project's timeline for the owner's dashboard (graph.timeline), each
        signal as a row: who wrote it, the start of its text, its link, an Intercom conversation's state and a thread's
        Team or Only you. Never part of what the team's Graph sends."""
        accounts = self.config['accounts']
        with self.store.connect() as db:
            found = graph.timeline(db, node, source, cursor, limit, now)
        if found is None:
            raise ValueError('Not in the graph')
        both = found['items'] + found.get('upcoming', [])
        ids = [i['id'] for i in both if i['type'] == 'event']
        ids += [c for i in both for c in i.get('copies') or ()]
        rows = {r['id']: r for r in self.store.events([a['id'] for a in accounts], event_ids=ids)} if ids else {}
        # Who is on a meeting, without the owner and without the person whose page this is: they are a given here
        with self.store.connect() as db:
            got = graph.resolve(db, node)
        info = json.loads(got['info'] or '{}') if got and got['kind'] == 'person' else {}
        with self.store.connect() as db:
            graph_owner = graph.Owner(self.config, db)
        owner = self.owner_emails() | graph_owner.emails
        given = owner | {str(i)[6:].lower() for i in [got['id'] if got else '', *(info.get('identifiers') or [])] if str(i).startswith('email:')}

        # People on a meeting by the name the graph has for them, when the invite has only their address
        invited = {str(a.get('email') or '').strip().lower() for r in rows.values() if r['kind'] == 'calendar.event'
                   for a in [*(r['metadata'].get('attendees') or ()), r['metadata'].get('organizer')] if isinstance(a, dict)} - {''}
        # (one person under two addresses is one node: keyed by it, they show once) and without the rooms booked on it
        known, nodes, noted = {}, {}, {}
        rooms, kept, _ = calendar_rooms(self.store.connect) if invited else (set(), set(), {})
        if invited:
            with self.store.connect() as db:
                for start in range(0, len(invited), 400):
                    chunk = ['email:' + e for e in sorted(invited)[start:start + 400]]
                    marks = ','.join('?' * len(chunk))
                    for n in db.execute(f"SELECT id,name,id identifier FROM graph_nodes WHERE kind='person' AND id IN ({marks}) UNION ALL "
                                        f"SELECT n.id,n.name,j.value FROM graph_nodes n, json_each(n.info,'$.identifiers') j WHERE n.kind='person' AND j.value IN ({marks})",
                                        (*chunk, *chunk)):
                        address = n['identifier'][6:]
                        nodes.setdefault(address, n['id'])
                        if n['name'] and '@' not in n['name']:
                            known.setdefault(address, n['name'])
        if any(r['kind'] == 'calendar.event' for r in rows.values()):  # a meeting with notes or a transcript says so on its row
            try:
                with self.store.connect() as db:
                    noted = meeting_notes.added_for(db, [i for i, r in rows.items() if r['kind'] == 'calendar.event'])
            except sqlite3.OperationalError:
                noted = {}

        def row_for(item):
            if item['type'] != 'event':
                return item
            r = rows.get(item['id'])
            if not r:
                return None
            m = r['metadata']
            row = {'id': r['id'], 'type': 'event', 'account_id': r['account_id'], 'kind': r['kind'], 'occurred_at': r['occurred_at'], 'title': r['title'][:200],
                   'source': item['source'], 'source_url': m.get('source_url'), 'probable': item['probable'], **event_glance(r, accounts, owner)}
            if r['kind'] == 'intercom.conversation':
                row['state'] = 'open' if m.get('open') is True or m.get('state') in ('open', 'snoozed') else 'closed'
                row['thread'] = None  # one conversation is one row
                opening = next((line for line in str(r.get('body') or '').splitlines() if line.strip()), '')  # the first line, not the log of parts
                row['preview'] = ' '.join(opening.split())[:240]
                if '@' in str(row.get('from') or ''):  # who opened it by name, not by address
                    row['from'] = (str(m.get('from_name') or '') or str(m.get('contact_name') or '') or row['from'])[:80]
            if r['kind'] in meeting_notes.PREFIX and (said := re.fullmatch(r'(?:notes|transcript):(\d+)', str(r['source_id']))):
                row['meeting_id'] = int(said[1])  # a meeting's notes or transcript open with the meeting
            if r['kind'] == 'calendar.event':  # one row for its copies on several calendars, everyone on it once
                row['all_day'] = bool(m.get('all_day'))
                people, copies = {}, [r, *(rows[i] for i in item.get('copies') or () if i in rows)]
                # The owner under another address of theirs: the name they have on their own calendar's copy
                own = {' '.join(str(a.get('displayName') or '').split()).casefold() for c in copies for a in c['metadata'].get('attendees') or ()
                       if isinstance(a, dict) and a.get('self') and str(a.get('email') or '').lower() in owner} - {''}
                for c in copies:
                    cm = c['metadata']
                    for a in [*(cm.get('attendees') or ()), cm.get('organizer') or {}]:
                        if not isinstance(a, dict) or a.get('responseStatus') == 'declined':
                            continue
                        address = str(a.get('email') or '').strip().lower()
                        if address in given or graph_owner.mine(address) or not (address or a.get('displayName')):
                            continue
                        if ' '.join(str(a.get('displayName') or '').split()).casefold() in own:
                            continue
                        if a.get('resource') or 'email:' + address in rooms or calendar_room(a, rooms, kept):
                            continue  # a meeting room is where, not who
                        if nodes.get(address) and nodes[address] in {nodes.get(g) for g in given}:
                            continue  # this page's person under another address of theirs
                        shown = ' '.join(str(a.get('displayName') or '').split())
                        name = (shown if shown and '@' not in shown else '') or known.get(address) or shown or address
                        key = nodes.get(address) or address or name.casefold()
                        if key not in people or '@' in people[key] and '@' not in name:
                            people[key] = name[:80]
                where = str(m.get('location') or '').strip()
                said = [line for line in str(r.get('body') or '').splitlines() if line.strip() and not line.startswith('Participants: ') and line.strip() != where]
                names = list(people.values())
                line = ' · '.join(filter(None, ['With ' + ', '.join(names[:6]) + (f' and {len(names) - 6} more' if len(names) > 6 else '') if names else '',
                                                where, ' '.join(' '.join(said).split()) if said else '']))
                row['preview'] = line[:240] + ('…' if len(line) > 240 else '')
                for c in copies:
                    for field in ('notes', 'transcript'):
                        if field in noted.get(c['id'], {}):
                            row[field] = True
            return row
        def safe_row(item):  # one signal that can't be read is logged and left out, never the whole timeline
            try:
                return row_for(item)
            except (ValueError, KeyError, TypeError, AttributeError) as error:
                LOG.warning('graph timeline row skipped event=%s error=%s', item.get('id'), type(error).__name__)
                return None
        items = [x for x in map(safe_row, found['items']) if x]
        found['upcoming'] = [x for x in map(safe_row, found.get('upcoming', [])) if x]
        if getattr(self, 'fleet', None) and rows:  # the Shared Graph: each Work thread's Team or Only you
            try:
                with self.store.connect() as db:
                    labels = self.fleet.thread_labels(db, list(rows.values()))
                for row in items + found['upcoming']:
                    if row.get('type') == 'event' and row['id'] in labels:
                        row['share'] = labels[row['id']]
            except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
                LOG.info('shared graph timeline error=%s', type(error).__name__)
        found['items'] = items
        return found

    def graph_freshness(self):
        """What makes a rebuild worth it before the ten minutes are up: new organization or people profiles (looked up by the
        enrichment worker, or by a hosting agent writing straight into the database), who is in the owner's Family,
        Friends and Work Fleets (a Personal contact follows within a minute), and, while the graph has no organizations
        yet (the first import), new signals."""
        circles = tuple(sorted((e, tuple(sorted(k))) for e, k in self.fleet_circles().items()))
        with self.store.connect() as db:
            profiles = tuple(db.execute("SELECT count(*),max(fetched_at) FROM org_profiles WHERE status!='error'").fetchone()) \
                + tuple(db.execute("SELECT count(*),max(fetched_at) FROM person_profiles WHERE status!='error'").fetchone()) \
                + tuple(db.execute('SELECT count(*),max(saved_at) FROM person_photos').fetchone())
            empty = not db.execute("SELECT 1 FROM graph_nodes WHERE kind='org' LIMIT 1").fetchone()
            signals = tuple(db.execute('SELECT count(*),max(ingested_at) FROM events WHERE history=0').fetchone()) if empty else None
        return profiles, signals, circles

    def graph_worker(self):
        """Rebuilds the people and projects graph every ten minutes, soon after a label or merge, and within a minute
        of new organization profiles or, on a new install, of new signals: so enriched details show right away."""
        wait, built, seen, published = 30, 0.0, None, time.monotonic()
        self.graph_worker_on = True  # graph_later hands its rebuilds here
        while not self.stop.is_set():
            dirty = self.graph_dirty.wait(min(wait, GRAPH_CHECK_SECONDS))
            if self.stop.is_set():
                return
            with contextlib.suppress(Exception):
                work_removal.prune(self.config)  # a work removal's safety copy goes after its days
            try:
                fresh = self.graph_freshness()
            except Exception:
                fresh = seen
            if not dirty and time.monotonic() - built < wait and fresh == seen:
                continue
            self.graph_dirty.clear()
            built, seen = time.monotonic(), fresh  # a failing build is not retried every minute
            try:
                self.own_addresses_fetch()  # once a day per mailbox: its aliases, before the build tells the owner apart
                # A build that keeps meeting edits tries again in a few seconds instead of holding the write lock for a
                # whole build (every request that writes waited); only after half an hour without one does it hold it
                self.graph_build(lock_last=time.monotonic() - published > GRAPH_LOCK_AFTER)
                published, seen, wait = time.monotonic(), self.graph_freshness(), 600
                if self.history_graph_step():  # a slice of history taken in: the next build counts it, in a minute
                    wait = 60
            except graph.Outdated:
                self.graph_dirty.set()
                self.stop.wait(GRAPH_RETRY_SECONDS)
            except Exception as error:
                LOG.error('graph error=%s', type(error).__name__)
                wait = 1800

    def gap_lines(self, suggestion_id):
        """What isn't known about the people on a task, from synced signals only (gap_note.py), for a preparation."""
        with self.store.connect() as db:
            row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            ids = json.loads(row['event_ids'] or '[]') if row else []
            found = gap_note.for_card(db, ids, account_services(self.config), lambda e: own_message(e, self.store.owner_user_ids),
                                      now(), skip_card=suggestion_id) if ids else []
        return gap_note.prompt_lines(found)

    def graph_lines(self, suggestion_id):
        """Who the people on a task are to the owner, and the projects around them, for a preparation."""
        with self.store.connect() as db:
            row = db.execute('SELECT event_ids,project,account_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            ids = json.loads(row['event_ids'] or '[]') if row else []
            area = {a.get('id'): graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')}
            sides = {area.get(a) for a in json.loads(row['account_ids'] or '[]')} - {None} if row else set()  # a summary's lines in this area only
            text = graph.context_lines(db, ids, skip_card=suggestion_id, sides=sides) if ids else ''
            brain = self.gbrain_lines(db, ids) if text else ''
        if not text:
            return ''
        unknown = self.store.no_role_yet(ids)
        return ('\n\nPeople and projects (from all signals, closeness fades with time; look up anyone with assistant_signals graph '
                'and a query or node_id, and keep personal details out of work messages and the other way round). Write to each person '
                'as the owner would to who they are to them: a cofounder, a sister or a friend reads differently from a customer, an accountant '
                'or someone new:\n' + text
                + (('\nNo role yet for ' + ', '.join(f"{p['name']} ({p['node_id']})" for p in unknown) + ': if what you read shows what they are to '
                    'the owner, set it with assistant_signals graph node_id, role, event_id and quote.') if unknown else '') + brain)

    def related_lines(self, suggestion_id, limit=8):
        """A short "Possibly related" list for a preparation: the task's own accounts, not its evidence."""
        with self.store.connect() as db:
            row=db.execute('SELECT account_ids,event_ids FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
        accounts,ids=json.loads(row['account_ids'] or '[]'),json.loads(row['event_ids'] or '[]')
        if not accounts or not ids:return ''
        found,_=self.related(accounts,ids,'',limit,signals_only=True)  # a preparation: never history
        rows={r['id']:r for r in self.store.events(accounts,event_ids=[i for i,_ in found])} if found else {}
        # source_line skips the owner's own to-dos (owner.card: the card says "Added by you"); here each one names what it is
        where=lambda r:source_text(r) if r['kind']=='owner.card' else source_line([r])[8:]
        lines=[f"- {i} ({rows[i]['account_id']}) {where(rows[i])} · {clamp(' '.join(rows[i]['title'].split()),100)}" for i,_ in found if i in rows]
        return ('\n\nPossibly related (found by meaning in this task\'s accounts; read any that matter with events, its account and event_ids):\n'+'\n'.join(lines)) if lines else ''

    def related(self, accounts, event_ids=(), query='', limit=8, exclude=(), timeout=30, signals_only=False):
        """([(event_id, similarity)], semantic) within the given accounts. With the embedding server
        down (or slower than `timeout` seconds), or not set up, a query still gets keyword matches."""
        settings=embeddings.settings(self.config)
        try:
            if not settings:raise embeddings.EmbeddingError('not_set_up')
            return embeddings.related(self.store.connect,settings,accounts,event_ids,query,limit,exclude=exclude,timeout=timeout,
                                      signals_only=signals_only),True
        except embeddings.EmbeddingError as error:
            if settings:LOG.error('related error=%s',error)
            if not query.strip():return [],False
            skip={*map(int,event_ids),*map(int,exclude)}
            with self.store.connect() as db:
                return [(i,None) for i in embeddings.fts_ids(db,accounts,query,limit+len(skip),signals_only) if i not in skip][:limit],False

    def own_addresses_fetch(self, read=None):
        """Each of the owner's own mailboxes' send-as addresses, once a day: Gmail's sendAs list (gmail.readonly, the
        scope mail already reads with) or Outlook's proxy addresses (User.Read). A read that fails waits a day too."""
        read = read or gog_read
        for account in own_addresses.mail_accounts(self.config):
            if getattr(self, 'stop', None) and self.stop.is_set():
                return
            with self.store.connect() as db:
                if not own_addresses.fetch_due(db, account['id'], now()):
                    continue
            try:
                answer = read(self.config, account, 'gmail', 'v1', 'gmail.users.settings.sendAs.list', {'userId': 'me'},
                              'https://www.googleapis.com/auth/gmail.readonly')
                entries = own_addresses.send_as_entries(answer, account.get('email'))
            except (SourceError, OSError, ValueError, KeyError, TypeError) as error:
                LOG.info('own addresses account=%s error=%s', account['id'], type(error).__name__)
                entries = None
            with self.store.connect() as db:
                own_addresses.save_fetched(db, account['id'], entries, now())

    def own_addresses_view(self):
        """Settings, Account: the owner's addresses, where each came from, and the ones that may be theirs."""
        try:
            with self.store.connect() as db:
                return own_addresses.view(db, self.config)
        except sqlite3.Error:
            return None

    def delete_person(self, node_id, workspace=None):
        """Delete permanently (graph.delete_person), then the lines in the agent's memory notes that name them, then a
        rebuild so nothing derived from them is left."""
        with self.store.connect() as db:
            done = graph.delete_person(db, node_id, self.config, now())
        notes = forget_in_notes((workspace or WORKSPACE) / 'memory', done.pop('needles'))
        self.graph_build()
        return {**done, 'notes': notes}

    def graph_query_action(self, name, args, owner_dashboard=False):
        return self.graph_action(args)

    def undo_merge_action(self, name, args, owner_dashboard=False):
        if owner_dashboard and re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}',str(args.get('approval_id',''))):source='dashboard'
        elif not owner_dashboard and re.fullmatch(r'telegram:[A-Za-z0-9_.:-]{1,200}',str(args.get('approval_id',''))):source='telegram'
        else:raise ValueError('Undo must come from the owner’s controls')
        return self.store.undo_merge(args['suggestion_id'],args['approval_id'],source)

    def remember_fact_action(self, name, args, owner_dashboard=False):
        if args.get('kind') == 'skill':  # notes about one kind of task: offered as a skill on a card, never made by itself
            return self.propose_skill_from_notes(args.get('name'), args.get('description'), args.get('text'), args.get('replaces'), args.get('skill'),
                                                 args.get('related'), args.get('relation'), args.get('new') is True, args.get('base'))
        if args.get('kind') == 'voice':  # how the owner writes on one channel: the whole line, from their note or edit
            return self.store.save_voice(args.get('channel'), args.get('text'), 'assistant', args.get('decision_id'), args.get('edit_id'), args.get('replaces'))
        if args.get('id') is not None and args.get('ended') is True:  # a newer message says it no longer holds
            return self.store.fact_overturned(args['id'], args.get('reason'), args.get('event_ids') or [])
        if args.get('id') is not None and not args.get('text'):  # who an existing fact is about
            return self.store.fact_about(args['id'], args.get('about'))
        return self.store.remember_fact(args.get('text'), args.get('decision_id'), args.get('kind') or None, args.get('replaces'), args.get('about'),
                                        args.get('until') or args.get('valid_until'))

    def graph_summary_action(self, name, args, owner_dashboard=False):
        # a person's summary: the owner's edit, a suggested update used or kept out, or back to The Machine's
        if not owner_dashboard:
            raise ValueError('Only the owner changes a summary, on the dashboard')
        return self.summary_change(args)

    def graph_fact_unlink_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner says who a fact is not about, on the dashboard')
        return self.store.fact_unlink(args.get('fact_id'), args.get('node_id'))

    def unmerge_fact_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner undoes a condense, on the dashboard')
        return self.store.unmerge_fact(args.get('id'), args.get('channel'), args.get('skill'), args.get('expired'))

    def graph_rename_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner renames people and projects, on the dashboard')
        with self.store.connect() as db:
            renamed = graph.rename(db, args.get('node_id'), args.get('name'), now())
        self.graph_build()
        return renamed

    def graph_stage_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner moves a project by hand, on the dashboard; reviews use finish_analysis stages')
        with self.store.connect() as db:
            moved = graph.set_stage(db, str(args.get('node_id') or ''), args.get('stage'), 'owner', now())
        self.graph_build()
        return moved

    def graph_org_edit_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError("Only the owner edits an organization's details, on the dashboard")
        with self.store.connect() as db:
            if name == 'graph_org_wrong':
                done = graph.org_wrong(db, args.get('node_id'), args.get('wrong') is not False, now())
            else:
                done = graph.org_edit(db, args.get('node_id'), args.get('fields'), now())
                if 'name' in args:
                    graph.rename(db, args.get('node_id'), args.get('name'), now())
        self.graph_build()
        return done

    def graph_new_action(self, name, args, owner_dashboard=False):
        # A person or organization added by hand (New person, New organization), and deleting one added that way
        if not owner_dashboard:
            raise ValueError('Only the owner adds people and organizations by hand, on the dashboard')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            done = graph.create_record(db, args.get('kind'), args, now(), graph.Owner(self.config, db)) if name == 'graph_new' else graph.delete_org(db, args.get('node_id'))
        if done.get('created') or done.get('deleted'):
            self.graph_build()
        return done

    def graph_picture_action(self, name, args, owner_dashboard=False):
        # A person's or organization's picture: the owner's upload (made small on the dashboard), one of the pictures
        # found for them (fetched here, on this Machine), or none.
        if not owner_dashboard:
            raise ValueError("Only the owner changes a picture, on the dashboard")
        if name == 'graph_pictures_found':
            with self.store.connect() as db:
                links = graph.picture_links(db, args.get('node_id'))
            found = []
            for link in links:
                got = enrichment.download_photo(link, timeout=5)
                if got:
                    found.append('data:' + got[1] + ';base64,' + base64.b64encode(got[0]).decode())
            return {'node_id': str(args.get('node_id') or ''), 'found': found}
        data = None
        if args.get('data'):
            raw = str(args['data'])
            try:
                data = base64.b64decode(raw.split(',', 1)[1] if raw.startswith('data:') else raw, validate=True)
            except (ValueError, binascii.Error):
                raise ValueError('A picture is a JPEG, PNG or WebP image, up to 200 kB') from None
        elif not args.get('remove') and not args.get('reset'):
            raise ValueError('Upload a picture, pick one, or remove it')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            done = graph.set_picture(db, args.get('node_id'), data, now(), reset=bool(args.get('reset')))
        self.graph_build()
        return done

    def graph_person_edit_action(self, name, args, owner_dashboard=False):
        # One Save for a person's page: their name, what they are to the owner and where they work go where those
        # live (graph_names, person_roles, person_orgs, as the owner's word); the rest is person_edits.
        if not owner_dashboard:
            raise ValueError("Only the owner edits a person's details, on the dashboard")
        node_id, fields = str(args.get('node_id') or ''), args.get('fields') if isinstance(args.get('fields'), dict) else {}
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            done = graph.person_edit(db, node_id, {k: v for k, v in fields.items() if k not in ('name', 'role', 'org')}, now())
            if 'role' in fields:
                graph.set_role(db, node_id, str(fields['role'] or ''), 'owner', now())
            if 'org' in fields:
                graph.set_org(db, node_id, str(fields['org'] or ''), 'owner', now())
            if 'name' in fields:
                graph.rename(db, node_id, fields['name'], now())
        # A new role alone is on their page already (graph.set_role): the rest of the Graph follows in the worker
        (self.graph_later if set(fields) == {'role'} else self.graph_build)()
        return done

    def graph_role_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner sets a role here, on the dashboard; reviews use graph with node_id and role')
        # The same role as a review's confirms it: it becomes the owner's word. Saved and on their page at once
        # (graph.set_role); the rest of the Graph follows in the worker, and the answer is only what was saved (the
        # dashboard draws from what it shows already): ✓ Right answers in milliseconds, not after a build.
        if not args.get('node_id'):
            raise ValueError('role goes with the person or organization node_id')
        with self.store.connect() as db:
            said = graph.set_role(db, args['node_id'], args.get('role') or '', 'owner', now())
        self.graph_later()
        return {'node_id': str(args['node_id']), **said}

    def graph_warmup_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner undoes a warm-up domain here, on the dashboard; reviews use graph with warmup')
        return self.graph_action({'node_id': args.get('domain') or args.get('node_id'), 'warmup': args.get('warmup') is True}, source='owner')

    def graph_show_person_action(self, name, args, owner_dashboard=False):
        # Hidden senders: Show as a person, for good; the rebuild that adds them runs in the graph worker
        if not owner_dashboard:
            raise ValueError('Only the owner shows a hidden sender as a person, on the dashboard')
        with self.store.connect() as db:
            said = mail_senders.show(db, args.get('identifier'), now())
        self.graph_later()
        return said

    def graph_same_action(self, name, args, owner_dashboard=False):
        # Same person? Merge, or Not the same (which also undoes a merge)
        if not owner_dashboard:
            raise ValueError('Only the owner merges people here, on the dashboard; reviews use graph with merge or different')
        pair = [str(args.get('a') or ''), str(args.get('b') or '')]
        return self.graph_action({('merge' if args.get('same') is True else 'different'): pair}, source='owner')

    def graph_same_all_action(self, name, args, owner_dashboard=False):
        # Merge all the listed Same person? pairs, or undo that batch in one go
        if not owner_dashboard:
            raise ValueError('Only the owner merges people here, on the dashboard; reviews use graph with merge or different')
        with self.store.connect() as db:
            if args.get('undo'):
                said = {'split': graph.unmerge_all(db, args['undo'])}
            else:
                pairs = args.get('pairs')
                if not isinstance(pairs, list):
                    raise ValueError('pairs is the list of [a, b] person ids shown under Same person?')
                said = graph.merge_all(db, pairs[:200], now())
        if said.get('merged') or said.get('split'):
            self.graph_later()
        return said

    def graph_person_delete_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner deletes someone permanently, on their page in the dashboard')
        return self.delete_person(str(args.get('node_id') or ''))

    def graph_person_org_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner sets an organization here, on the dashboard; reviews use graph with org, event_id and quote')
        return self.graph_action({'node_id': args.get('node_id'), 'org': args.get('org') or ''}, source='owner')

    def graph_relation_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner removes a relation here, on the dashboard; reviews use graph with related_to')
        return self.graph_action({'node_id': args.get('node_id'), 'related_to': args.get('related_to'), 'relation': args.get('relation') or ''}, source='owner')

    def forget_fact_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner can remove a fact, on the dashboard')
        return self.store.forget_fact(args['id'], bool(args.get('undo')))

    def edit_fact_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner can edit what was learned, on the dashboard')
        return self.store.edit_fact(args.get('id'), args.get('text'))

    def board_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner saves, deletes or dismisses a board, on the dashboard; reviews suggest one with graph suggest_board')
        with self.store.connect() as db:
            done = graph.save_board(db, args, now()) if name == 'board_save' else graph.delete_board(db, args.get('board_id'), now()) \
                if name == 'board_delete' else graph.dismiss_board_suggestion(db, args.get('suggestion_id'), now())
        if name != 'board_dismiss':  # the board view reads boards and projects as they are now: the Graph follows in the background
            self.graph_later()  # a whole build here held a board edit some 12 s on a big Graph
        return done

    def project_visibility_action(self, name, args, owner_dashboard=False):
        # who sees one project: Only you, Team, or as its board (null)
        if not owner_dashboard:
            raise ValueError('Only the owner sets who sees a project, on the dashboard')
        with self.store.connect() as db:
            done = graph.set_project_visibility(db, args.get('node_id'), args.get('visibility'))
        self.graph_build()
        return done

    def project_action(self, name, args, owner_dashboard=False):
        # The owner's own CRM work on projects and boards: make or edit a project, won or lost, archive, delete,
        # the default board, and a project a review thought could belong on a board
        if not owner_dashboard:
            raise ValueError('Only the owner makes, edits or ends a project by hand, on the dashboard; reviews use graph and finish_analysis')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if name == 'project_save':
                done = graph.save_project(db, args, now())
            elif name == 'project_outcome':
                done = graph.set_outcome(db, args.get('node_id'), args.get('outcome') or None, args.get('reason'), now())
            elif name == 'project_archive':
                done = graph.archive_project(db, args.get('node_id'), args.get('archived') is not False, now())
            elif name == 'project_delete':
                done = graph.delete_project(db, args.get('node_id'))
            elif name == 'board_default':
                done = graph.default_board(db, args.get('board_id'))
            elif args.get('undo'):
                done = graph.undo_fit(db, args['undo'])
            else:
                many = args.get('node_ids')
                if many is not None and not (isinstance(many, list) and all(isinstance(n, str) for n in many)):
                    raise ValueError('node_ids is a list of suggestion ids')
                done = graph.decide_fit(db, args.get('board_id'), many if many is not None else args.get('node_id'), args.get('add') is not False, now())
        if name == 'board_fit':  # the board reads its projects as they are now: the Graph follows in the background
            self.graph_later()
        else:
            self.graph_build()
        return done

    def crm_actions_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner changes owners, merges organizations and imports, on the dashboard')
        return self.crm_action(name, args)
