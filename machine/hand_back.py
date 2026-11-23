"""A step a run wrote and lost (2026-11). A save with a message or handoff was refused, or had to wait until Slack was read,
and the run's next save came without it and went through: notes with a need, or "done". The steps of a save that didn't go
through are kept (machine/app/card_actions.py), and a later save of that run without any gets them back, once: a run that
rightly finished without them goes on at its next save. From the saves' own fields, never from their words. In memory: after
a restart of the service nothing is checked. Imports nothing of The Machine's."""
import json

LAYER = 0  # whether a save lost the step an earlier one had (a leaf)

KEPT = 200    # runs whose steps are kept at most
SHOWN = 4000  # characters of the steps given back at most
ENDED = ('done', 'answered', 'needs_you')  # already_done, waiting and snoozed say why no step is left


def keep(memory, job_id, args, waiting):
    """Keep what a save that did not go through had waiting for the owner, until one does. Already given back: not again."""
    steps = args.get('next_actions') or args.get('next_action') or ()
    steps = [a for a in (steps if isinstance(steps, (list, tuple)) else [steps]) if isinstance(a, dict) and a.get('kind') in waiting]
    if not job_id or not steps or (memory.get(job_id) or {}).get('told'):
        return
    memory.pop(job_id, None)  # the newest last
    memory[job_id] = {'steps': steps}
    for old in list(memory)[:-KEPT]:
        del memory[old]


def lost(memory, job_id, outcome, kinds, waiting):
    """This save ends the run's work with no step, and an earlier one that did not go through had one: what to do."""
    kept = memory.get(job_id)
    if not kept or kept.get('told') or outcome not in ENDED or any(k in waiting for k in kinds):
        return None
    kept['told'] = True
    named = ' and '.join(dict.fromkeys(f"{a['kind']} step “{' '.join(str(a.get('label') or a['kind']).split())[:60]}”" for a in kept['steps']))
    text = json.dumps(kept['steps'], ensure_ascii=False)
    return (f"This save lost the {named} that an earlier save of this run had; that save did not go through, so the owner would never see it. "
            'Put it back' + (f' with next_actions:{text}' if len(text) <= SHOWN else '')
            + ' and save: as it was when the save only had to wait, corrected when it was refused. '
            'Only if the to-do is rightly finished without it, save this again as it is.')
