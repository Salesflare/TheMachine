"""Hand to Claude Code / Hand to Codex, the App's part: a domain mixin of App (only assistant.py composes it;
docs/code-map.md).

The hand-off actions (AGENT_ACTIONS in assistant.py, the reviewed list: the owner's own, from their dashboard only), a
job's folder, a rewritten draft, and the Settings view of where agents run. agent_card and agent_work stay in
assistant.py for now: they use helpers defined there."""
import json
from pathlib import Path
import re
import urllib.parse

import agent_jobs


class AgentsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys((
        'agent_cancel',
        'agent_draft',
        'agent_follow_up',
        'agent_outcome',
        'agent_retry',
        'agent_send',
        'set_agents',
    ), 'agents_dashboard_action')

    def agents_dashboard_action(self, name, args, owner_dashboard):
        # Hand to Claude Code / Codex: the owner's own, from the dashboard only
        if not owner_dashboard:
            raise ValueError('Hand off to Claude Code or Codex from the dashboard')
        return self.agent_action(name, args)

    def agent_action(self, name, args):
        if not self.agents:
            raise ValueError('Handing off to Claude Code or Codex is off on this Machine')
        if name == 'agent_draft':
            return self.agents.draft(args['suggestion_id'])
        if name == 'agent_send':
            return self.agents.start(args['suggestion_id'], args['tool'], args.get('brief'), args.get('note'))
        if name == 'agent_follow_up':
            return self.agents.follow_up(args['job_id'], args.get('text'))
        if name == 'agent_retry':
            return self.agents.retry(args['job_id'])
        if name == 'agent_cancel':
            return self.agents.cancel(args['job_id'])
        if name == 'agent_outcome':
            return self.agents.set_outcome(args['job_id'], args.get('outcome'))
        raise ValueError('Unknown operation')

    def agent_revise(self, suggestion_id, text, job=None):
        """A message Claude Code or Codex rewrote (its draft.md) becomes the card's draft under a new revision, when the
        card has exactly one message draft: the owner still reads it there and sends it with the card's own Send."""
        with self.store.connect() as db:
            row = db.execute('SELECT status,next_action FROM suggestions WHERE id=?', (str(suggestion_id),)).fetchone()
        if not row or row['status'] != 'prepared' or not row['next_action']:
            return False
        current = json.loads(row['next_action'])
        actions = current.get('actions') if current.get('kind') == 'menu' else [current]
        editable = [a for a in actions or [] if isinstance(a, dict) and a.get('kind') in ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'intercom', 'doc_reply') and a.get('revision')]
        if len(editable) != 1:
            return False
        return self.store.revise_draft(str(suggestion_id), editable[0]['revision'], 'agent', None, text, agent_job=job).get('status') == 'revised'

    def agents_view(self):
        """Hand to Claude Code / Codex where no local CLI of the owner's runs (agent_remote.py): the paired Claude Code
        session, the Codex cloud environment, and the claude.ai connector that brings Claude's results back."""
        own = agent_jobs.settings(self.config)
        if own is None:
            return None
        claude, codex = (own.get('claude') if isinstance(own.get('claude'), dict) else {}), (own.get('codex') if isinstance(own.get('codex'), dict) else {})
        where = self.agents.where() if getattr(self, 'agents', None) else None  # Where Codex runs, from the setup page
        on_device = (where or {}).get('codex') == 'device'
        on_machine = (where or {}).get('codex') == 'machine' and not codex.get('place')
        if not (self.config.get('manage_url') and (agent_jobs.coding_relevant(self.config) or on_device) or claude.get('place') == 'remote'
                or codex.get('place') == 'cloud'):
            return None  # hosted: shown once GitHub or Codex is connected (agent_jobs.coding_relevant)
        manage = str(self.config.get('manage_url') or '')
        origin = urllib.parse.urlsplit(manage)
        base = f'{origin.scheme}://{origin.netloc}' if origin.scheme == 'https' and origin.netloc else 'https://app.themachine.computer'
        return {'claude_session': str(claude.get('session') or ''), 'device': str(claude.get('device') or ''),
                'codex_where': 'device' if on_device else 'machine' if on_machine else None,
                'codex_device': agent_jobs.device_label(where) if on_device else '',
                'codex_setup': manage.split('#')[0] + '#codex' if manage.startswith('https://') else '',
                'codex_env': str(codex.get('env') or ''), 'codex_branch': str(codex.get('branch') or ''),
                'connector': base + '/mcp', 'on_network': bool(getattr(self, 'fleet', None)),
                'saveable': bool(getattr(self, 'config_path', None))}

    def agent_folder(self, job_id):
        """A coding agent job's own folder (its turn transcripts), or None."""
        if not re.fullmatch(r'aj_[0-9a-f]{16}', str(job_id or '')):
            return None
        agents = getattr(self, 'agents', None)
        root = agents.root if agents is not None else Path(self.config['database']).expanduser().parent / 'agent-jobs'
        return Path(root) / job_id
