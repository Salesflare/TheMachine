"""A merge shows at once (graph.merge): the two people's records become one right away, so People, its search and their
pages show one person. Before, Merge only saved the decision and both records stayed until the graph worker's rebuild
(seconds to minutes on a big Graph), while the dashboard already said Merged. The rebuild still computes the joined
record from all their signals, and every later one keeps them joined (graph_merges), whatever a sync brings in."""
import json

import graph
import graph_show


def fold(db, a, b, source='agent', prefer=None):
    """Fold the record of b into the one of a (or the other way): the record an address names stays, as the rebuild
    names it, unless prefer names one of the two. The other's identifiers, links and signals move to it, so its old
    links open the one that stays. The id that stays, or None when one of them is not in the Graph yet (the rebuild
    joins them)."""
    one, other = graph.resolve(db, a), graph.resolve(db, b)
    if not one or not other or one['kind'] != 'person' or other['kind'] != 'person':
        return None
    if one['id'] == other['id']:
        return one['id']
    stays, goes = sorted((one, other), key=lambda r: (r['id'] != prefer, not r['id'].startswith('email:'), -(r['strength'] or 0), r['id']))
    kept, went = json.loads(stays['info'] or '{}'), json.loads(goes['info'] or '{}')
    info = dict(kept)
    for field in ('identifiers', 'ids', 'accounts', 'hints'):
        info[field] = sorted(set(kept.get(field) or ([stays['id']] if field == 'identifiers' else [])) |
                             set(went.get(field) or ([goes['id']] if field == 'identifiers' else [])))
    for field in ('org', 'role', 'notes'):  # what only the other one had, with its source
        if not kept.get(field) and went.get(field):
            info.update({k: v for k, v in went.items() if k == field or k.startswith(field + '_')})
    for field in ('wrote', 'heard', 'met'):
        info[field] = (kept.get(field) or 0) + (went.get(field) or 0)
    meetings = [m for m in (kept.get('next_meeting'), went.get('next_meeting')) if m]
    info['next_meeting'] = min(meetings) if meetings else None
    info['has_headline'] = bool(kept.get('has_headline') or went.get('has_headline'))
    info['seen_only'] = bool(kept.get('seen_only', True) and went.get('seen_only', True))
    info['manual'] = bool(kept.get('manual') or went.get('manual'))
    info['same'] = [s for s in (kept.get('same') or []) + (went.get('same') or []) if isinstance(s, dict) and s.get('id') not in (stays['id'], goes['id'])]
    info['joined'] = (kept.get('joined') or []) + (went.get('joined') or []) + [
        {'a': a, 'b': b, 'a_shown': graph.shown_id(a, {}), 'b_shown': graph.shown_id(b, {}), 'why': graph.JOINED_WHY.get(source, 'joined'), 'by': source}]
    last = max((d for d in (stays['last_at'], goes['last_at']) if d), default=None)
    graph.fold_write(db, stays['id'], goes['id'], max(stays['strength'] or 0, goes['strength'] or 0), last,
                     (stays['signals'] or 0) + (goes['signals'] or 0), info)
    # Their emails, phones, photo and details from both, as a build shows them (the owner's edits first)
    graph_show.show_person_edit(db, stays['id'], ())
    return stays['id']
