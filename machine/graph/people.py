"""The person nodes: name, organization by address or statement, role, Work or Personal, profile and what
Same person? compares; shared inboxes count for their organization."""

import collections
import json

import enrichment
from graph import (
    FLOOR, FREEMAIL, JOINED_WHY, auto_side, name_words, org_from_name, person_shown, personal_relation, plain_name,
    shown_id, shown_name,
)
from mail_senders import address_name, bulk, relay, shared_inbox


def person_nodes(db, owner, names, strength, union, keys, x_names, roles, last_day, current, tz, listed, kept,
                 node_events, mailings, appears, kin, thread_sides, on_projects, project_side, accounts,
                 side_of_account, headlines, live_roles, next_meeting, manual_people, history_events, live, joined):
    # Write.
    nodes, links, members = [], [], collections.defaultdict(list)
    inboxes = collections.defaultdict(list)  # domain -> [(node, strength)] of its shared inboxes: they count for the organization
    named = {r['node_id']: r['name'] for r in db.execute('SELECT node_id,name FROM graph_names')}
    role_rows = {r['identifier']: dict(r) for r in db.execute('SELECT * FROM person_roles')}
    said = {i: (r['role'] or None, 'owner' if r['source'] == 'owner' else 'review') for i, r in role_rows.items()}
    related = db.execute("SELECT a,b,relation,source FROM graph_relations ORDER BY source='owner',created_at").fetchall()
    profiles = {}
    for r in db.execute("SELECT domain,profile,status FROM org_profiles WHERE profile IS NOT NULL AND status!='wrong'").fetchall():
        found = enrichment.usable(r['domain'], json.loads(r['profile']))  # one saved before the check: dropped before (_drop_unusable_profiles)
        if found:
            profiles[r['domain']] = found
    wrong = {r[0] for r in db.execute("SELECT domain FROM org_profiles WHERE status='wrong'")}
    looked_up = {r['identifier']: r['profile'] for r in db.execute("SELECT identifier,profile FROM person_profiles WHERE status='found' AND profile IS NOT NULL")}
    photos = {r['identifier']: r['key'] for r in db.execute('SELECT identifier,key FROM person_photos')}
    site_logos = {i[5:]: k for i, k in photos.items() if i.startswith('logo:')}  # from an organization's own website (enrichment.site_logos_step)
    facts = enrichment.people_facts(db)  # what connectors read about them (job title, place, links, time zone)
    edits = {r['domain']: json.loads(r['fields']) for r in db.execute('SELECT domain,fields FROM org_edits')}
    person_edits = {r['identifier']: json.loads(r['fields']) for r in db.execute('SELECT identifier,fields FROM person_edits ORDER BY updated_at,identifier')}
    stated_rows = {r['identifier']: dict(r) for r in db.execute('SELECT * FROM person_orgs')}
    stated = {}  # person node -> the statement of where they work, when no work address says it
    named_orgs = collections.defaultdict(list)
    surnames, firsts = {n.split()[-1] for n in owner.names if len(n.split()) >= 2}, {n.split()[0].casefold() for c in names.values() for n in c if n and len(n.split()) >= 2}
    alike = {}  # person node -> what "Same person?" compares: name words, company domains, role
    for node, value in strength.items():
        if value < FLOOR:
            continue
        group = sorted(union.members.get(node, {node}))
        if any(owner.has(i) for i in group):
            continue  # the owner's own address or number: About you, never a person
        counts = collections.Counter()
        for identifier in group:
            counts.update(names.get(identifier, {}))
        name = shown_name(counts) if counts and not all(keys.several(i) for i in group) else shown_id(node, x_names)  # a list goes by its address
        if plain_name(name) in owner.names or (name == shown_id(node, x_names) and node.partition(':')[2] not in name and not any(i in named for i in group) and not roles[node]['owner'] | roles[node]['them'] | roles[node]['met']):
            continue  # the owner on another channel (a note-to-self chat, an old address); or only seen, with no name at all yet ("Slack")
        name = next((named[i] for i in group if i in named), name)  # the owner's own name for them wins
        name = (derived := node.startswith('email:') and name == node[6:] and not keys.several(node) and address_name(node[6:], firsts)) or name  # no name given: ayla@ is "Ayla"
        talk = sorted(roles[node]['owner'] | roles[node]['them'] | roles[node]['met'])
        gaps = [(b - a).days for a, b in zip(talk, talk[1:])][-8:]
        usual = sorted(gaps)[len(gaps) // 2] if len(gaps) >= 3 else None
        if talk:  # contact is with the owner: someone answering a customer or posting in a channel isn't
            last_day[node] = talk[-1]
        since = (current.astimezone(tz).date() - last_day[node]).days if node in last_day else None
        quiet = bool(usual and len(roles[node]['owner']) >= 2 and since is not None and max(14, 3 * usual) < since < 365)
        # Automated senders (a no-reply, Gemini's meeting notes) are no one's colleague: their domain makes no organization
        domains = sorted({i.split('@', 1)[1] for i in group if i.startswith('email:') and not bulk(i[6:]) and not relay(i[6:])}
                         - FREEMAIL - owner.domains)
        if domains and shared_inbox(group, name, domains[0], listed, kept, org_from_name(name, domains[0]), enrichment.registrable(domains[0])):
            inboxes[domains[0]].append((node, value)); members.setdefault(domains[0], [])
            mailings.found[node] = [name, 'shared', len(node_events[node]), last_day[node].isoformat() if node in last_day else '', value]
            continue
        said_org = max((stated_rows[i] for i in group if i in stated_rows),
                       key=lambda r: (r['source'] == 'owner', r['said_at'] or '', r['created_at'], r['identifier'] == node), default=None)
        if said_org and said_org['source'] != 'owner' and domains:
            said_org = None  # a work address says it already
        if said_org and said_org['org']:
            stated[node] = said_org
        elif domains and not said_org:
            members[domains[0]].append((node, value))
        colleague = any(i.startswith('email:') and i.rsplit('@', 1)[1] in owner.domains for i in group)
        role_id = max((i for i in group if i in role_rows), key=lambda i: (role_rows[i]['source'] == 'owner', role_rows[i].get('checked_at') or role_rows[i]['created_at'], i == node), default=None)
        role, role_by = said.get(role_id, (None, None))  # only what the owner or a review said
        full = plain_name(name)
        hints = sorted(set().union(*(appears.get(i, ()) for i in group))) + (["an address at the owner's own domain"] if colleague else []) \
            + (["in the owner's Slack"] if any(i.startswith('slack:') for i in group) else []) \
            + (["shares the owner's surname"] if full and surnames & set(full.split()[1:]) else [])
        edited = {}
        for identifier in sorted((i for i in group if i in person_edits), key=list(person_edits).index):
            edited.update(person_edits[identifier])  # the owner's word wins over the look-up, a later save over an older one
        person_profile, contacts = person_shown(group, edited, looked_up, facts, photos)
        # A person's Type (Work or Personal), the one the Work and Personal lists and sharing with a Work Fleet go by: the
        # owner's word; else someone only in their Family or Friends, or family or a friend to them ("To you": wife,
        # father), is Personal, whatever address they write from; else what The Machine knows of them (auto_side).
        side, side_why = edited.get('side'), 'owner'
        circle = set().union(*((kin or {}).get(i[6:].lower(), ()) for i in group if i.startswith('email:')))
        if not side and circle and circle <= {'family', 'friends'}:
            side, side_why = 'personal', 'network'
        elif not side and personal_relation(role):
            side, side_why = 'personal', 'relation'
        elif not side:
            called = collections.Counter(thread_sides[node].values())
            on = collections.Counter(project_side.get(pid) for pid in on_projects[node])
            side, side_why = auto_side(bool(colleague or domains or (said_org and said_org['org'])), called, on,
                                       [side_of_account.get(a) for a in accounts[node]])
        info = {'ids': sorted({shown_id(i, x_names) for i in group if not i.startswith('manual:')}), 'org': ('org:' + domains[0]) if domains and not said_org else None,
                'org_by': 'email' if domains and not said_org else None, 'has_headline': any(i in headlines for i in group),
                'wrote': len(live_roles[node]['owner']), 'heard': len(live_roles[node]['them']), 'met': len(live_roles[node]['met']),
                'accounts': sorted(accounts[node]), 'next_meeting': next_meeting[node].isoformat() if node in next_meeting else None,
                'colleague': colleague, 'role': role, 'role_by': role_by, 'role_id': role_id, 'identifiers': group, 'hints': hints, 'seen_only': not talk,
                'profile': person_profile, 'edited': sorted(edited), 'side': side, 'side_by': 'owner' if edited.get('side') else None,
                'side_why': side_why,
                'manual': any(i in manual_people for i in group), 'notes': edited.get('notes'),
                **contacts}
        if history_events.get(node):
            info.update(history=len(history_events[node]), live=round(live[node], 4))
        if len(group) > 1:
            info['joined'] = [{'a': x, 'b': y, 'a_shown': shown_id(x, x_names), 'b_shown': shown_id(y, x_names), 'why': JOINED_WHY.get(why, 'joined'),
                               'by': why} for x, y, why in joined.get(node, ()) if why]
        # What "Same person?" compares. A name that is their company's ("Seeking Alpha" at seekingalpha.com) is no
        # person's name; one read from their address (no name given) is only ever a similar one.
        no_name = bool(derived) or name == shown_id(node, x_names)
        sender_org = any(org_from_name(name, i.rsplit('@', 1)[1]) for i in group if i.startswith('email:')) and not no_name
        alike[node] = {'words': [] if sender_org or all(keys.several(i) for i in group) else name_words(name, node if no_name else None), 'derived': no_name, 'strength': value,
                       'domains': set(domains), 'role': ' '.join(str(role).casefold().split()) if role else None}
        nodes.append((node, 'person', name[:200], round(value, 4), last_day[node].isoformat() if node in last_day else None,
                      len(node_events[node]), usual, int(quiet), None, info))
    return (nodes, links, members, inboxes, named, said, related, profiles, wrong, site_logos, edits, stated,
            named_orgs, alike)
