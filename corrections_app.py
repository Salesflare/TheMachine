"""Fix it where it came from, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

A to-do's chat turn looks up where a wrong thing came from (correction_sources) and fixes it there (fix_source), from
the owner's own note on that to-do (corrections.py). The Undo is learning_undo, the owner's own, like every learned
change. A fix in the Graph rebuilds it, and wakes the GBrain sync when that is on, so The Machine's section on a
GBrain page says the right thing too (only that section: what the owner wrote there stays theirs)."""
import corrections
import learning_loop


class CorrectionsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action). Both are the
    # agent's own calls in a to-do's chat (openclaw-plugin TOOL_ACTIONS); the dashboard sends neither.
    ACTIONS = dict.fromkeys((
        'correction_sources',
        'fix_source',
    ), 'correction_action')

    def correction_action(self, name, args, owner_dashboard):
        if name == 'correction_sources':
            with self.store.connect() as db:
                return corrections.sources(db, args.get('suggestion_id'), args.get('words') or '', args.get('node_ids'))
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            done = corrections.fix(db, args.get('suggestion_id'), args.get('decision_id'), args.get('kind'), args.get('target'),
                                   args.get('value'), args.get('came_from'), learning_loop.now())
        if done.pop('graph', False):
            self.correction_refresh()
        return done

    def correction_refresh(self):
        """After a fix or its undo in the Graph: rebuild it, and let GBrain's section follow (gbrain_start wakes a running sync)."""
        self.graph_build()
        try:
            self.gbrain_start()
        except Exception:  # noqa: BLE001 - GBrain is optional; the fix stands without it
            pass
