"""The Shared Graph's controls, the App's part: a domain mixin of App (only assistant.py composes it;
docs/code-map.md).

GRAPH_SHARE_ACTIONS in assistant.py stays the reviewed list of these actions (the owner's own); graph_share_action
checks where each may come from, as before (the dashboard, and Telegram's owner chat through graph share)."""
import json

import shared_graph


class SharedGraphApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys((
        'graph_ask',
        'graph_board_share',
        'graph_connection',
        'graph_optout',
        'graph_pause',
        'graph_policy',
        'graph_private',
        'graph_rekey_no',
        'graph_remove',
        'graph_rule',
        'graph_share',
        'graph_share_all',
        'graph_share_many',
        'graph_start',
        'graph_thread_share',
    ), 'graph_share_action')

    def graph_share_action(self, name, args, owner_dashboard=False):
        """The owner's Shared Graph controls, from the dashboard (and Telegram's owner chat through graph share)."""
        if name == 'graph_private' and args.get('private') is not False and self.about_you_node(str(args.get('node_id') or '')):
            raise ValueError('That’s About you: your own record is never shared, so there’s nothing to keep private')
        if not getattr(self, 'fleet', None):
            raise ValueError('Join a Work Fleet to share with your team')
        if name == 'graph_share_many' and args.get('share') == 'people':  # Share these?, Share with…: chosen teammates only
            return self.fleet.graph_threads_share(args.get('event_ids') or [], args.get('people') or [])
        with self.store.connect() as db:
            shared_graph.ensure(db)
            if name == 'graph_share':  # a thread's Team or Only you; None for the review's call again
                choice = {'team': 'team', 'only_you': 'private', 'private': 'private', 'auto': None}.get(str(args.get('share') or ''), False)
                if choice is False:
                    raise ValueError('Choose team or only_you')
                row = db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id=?', (int(args.get('event_id') or 0),)).fetchone()
                label = self.fleet.thread_labels(db, [dict(row)]).get(row['id']) if row else None
                if not label:
                    raise ValueError('Only messages in a Work account are shared with your team')
                if label['fixed'] and choice == 'team':
                    raise ValueError('Personal threads are never shared' if label.get('view') == 'personal'
                                     else 'Only colleagues are on this thread, so it stays with the people on it')
                shared_graph.set_hand(db, row['id'], choice)
                scope = next(iter(self.fleet.scopes(db).values()), None)
                suggest = shared_graph.suggest_rule(db, scope, row['id'], choice) if scope and choice else None
                return {'ok': True, 'label': self.fleet.thread_labels(db, [dict(row)]).get(row['id']), 'suggest': suggest}
            if name == 'graph_share_many':  # Share these? and the first share's look-over: several threads in one tap
                choice = {'team': 'team', 'only_you': 'private', 'private': 'private'}.get(str(args.get('share') or ''))
                ids = [int(i) for i in (args.get('event_ids') or []) if str(i).isdigit()][:500]
                if not choice or not ids:
                    raise ValueError('Choose threads, and team or only_you')
                rows = [dict(r) for r in db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id IN (SELECT value FROM json_each(?))', (json.dumps(ids),))]
                labels = self.fleet.thread_labels(db, rows)
                done = 0
                for r in rows:
                    label = labels.get(r['id'])
                    if label and not (label['fixed'] and choice == 'team'):
                        shared_graph.set_hand(db, r['id'], choice)
                        done += 1
                return {'ok': True, 'done': done}
            if name == 'graph_rule':  # "Always keep threads with X private?" (or always share), asked once after a pattern
                choice = {'team': 'team', 'only_you': 'private', 'private': 'private', 'none': None}.get(str(args.get('choice') or ''), False)
                if choice is False:
                    raise ValueError('Choose team, private or none')
                return {'ok': True, 'rule': shared_graph.set_rule(db, args.get('key'), choice, args.get('name') or '')}
            if name == 'graph_private':  # Keep private on a person, organization or project: it and its threads stay here
                return {'ok': True, 'private': shared_graph.keep_private(db, str(args.get('node_id') or ''), args.get('private') is not False)}
        if name == 'graph_board_share':  # a board for chosen teammates (none: Only you again, taken back from them)
            return self.fleet.graph_board_share(args.get('board_id'), args.get('people') or [])
        if name == 'graph_thread_share':  # one thread by hand for chosen teammates, a sensitive one too; never personal
            return self.fleet.graph_thread_share(args.get('event_id'), args.get('people') or [])
        if name == 'graph_start':  # the owner looked over their first share: it goes now
            return self.fleet.graph_start(str(args.get('fleet') or ''))
        if name == 'graph_pause':  # an admin: sharing off (on: paused; remove: also delete what went) or back on, for everyone
            return self.fleet.graph_pause(str(args.get('fleet') or ''), args.get('on') is not False, args.get('remove') is True)
        if name == 'graph_share_all':  # an admin: everyone new in the Fleet gets the team's Graph, in one OK
            return self.fleet.graph_share_all(str(args.get('fleet') or ''))
        if name == 'graph_remove':  # an admin: take someone out of the team's Graph, or let them back in (back)
            return self.fleet.graph_remove(str(args.get('fleet') or ''), str(args.get('member') or ''), args.get('back') is True)
        if name == 'graph_rekey_no':  # an admin: a teammate's new Machine isn't theirs
            return self.fleet.graph_rekey_no(str(args.get('fleet') or ''), str(args.get('member') or ''))
        if name == 'graph_policy':  # an admin: the Work connections every member shares (some of mail, calendar)
            return self.fleet.graph_set_policy(str(args.get('fleet') or ''), [str(x) for x in args.get('require') or []])
        if name == 'graph_connection':  # the owner: one connection feeds the team's Graph, or not (unless required)
            return self.fleet.graph_connection(str(args.get('fleet') or ''), str(args.get('account') or ''), args.get('on') is True)
        if name == 'graph_optout':  # off: ask an admin to stop sharing this Machine's Work; on again at once
            return self.fleet.graph_optout(str(args.get('fleet') or ''), args.get('off') is not False)
        if name == 'graph_ask':
            return self.fleet.graph_ask(str(args.get('fleet') or ''), str(args.get('member_id') or ''), str(args.get('about') or ''), str(args.get('note') or ''))
        raise ValueError('Unknown action')
