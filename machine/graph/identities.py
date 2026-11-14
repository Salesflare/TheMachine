"""Who: the identifiers on each signal, as a Graph build (graph.build) reads them. Mailings, warm-up
traffic, meeting rooms and people the owner deleted drop out; names, organizations senders give and
where each identifier shows up are counted."""

import collections

import graph_joins
import mail_senders
from graph import (
    FLOOR, FREEMAIL, GENERIC_NAMES, HALF_LIFE, account_side, forgotten, hidden, not_resources, org_from_name,
    person_name, plain_name, relayed, resources, room_like, thread_key, touches,
)
from mail_senders import addresses, automated, list_unsubscribes, mass_mail, owner_kept, relay


def read_identities(db, signals, old, owner, current, config, past):
    unsubscribes = list_unsubscribes(db, signals + old, owner)
    kept = owner_kept(db)  # whoever the owner's word or work is on stays a person, whatever their mail looks like
    mailings = mail_senders.Hidden(current, HALF_LIFE['person'], FLOOR)  # the senders it leaves out
    listed, wrote_to = set(), set()  # listed: addresses that sent mail a mailing system sent (List-Unsubscribe, List-Id, Precedence bulk): a shared inbox's sign
    for event_id, _, kind, _, m in signals + old:
        if (kind == 'gmail.message' and ('SENT' in (m.get('labels') or ()) or any(a in owner.emails for _, a in addresses(m.get('from'))[:1]))
                and not automated(m) and event_id not in unsubscribes):
            wrote_to |= {a for _, a in addresses(m.get('to')) + addresses(m.get('cc'))}

    warmup = hidden(db)  # addresses there are a warm-up tool's traffic: nobody in the graph
    rooms = resources(db)  # meeting rooms and other things booked on invites: never people
    people_kept = not_resources(db)
    # A room by its address, or by the name kept for it (graph_names): its person leaves the graph at this build
    named_rooms = {r[0] for r in db.execute('SELECT node_id,name FROM graph_names') if str(r[0]).startswith('email:') and room_like('', r[1])}
    rooms |= {i for i in named_rooms if i not in people_kept}
    gone = forgotten(db)  # people the owner deleted permanently: never added again

    # Who: identifiers per signal, joined into people.
    seen_message_ids = set()
    per_event, names, x_names = {}, collections.defaultdict(collections.Counter), {}
    crm_names, paying_names = {}, {}
    said_orgs = collections.defaultdict(collections.Counter)  # domain -> names its senders give it ("Robin from Blue Harbor")
    appears = collections.defaultdict(set)  # identifier -> where they show up: a hint for a review, never a role
    owner_events = set()
    headlines = set()  # LinkedIn conversations whose person has a headline (read at view time: it stays sealed in the signal)
    keys = graph_joins.Keys(config, owner, plain_name, account_side, FREEMAIL)  # which identities a name may join: never a shared address
    senders = collections.defaultdict(list)  # email identifier -> [(at, event id)] of mail it wrote: its own text may carry its number
    for event_id, account_id, kind, at, m in signals + old:  # signals first: the same email as a signal and history counts as the signal
        if kind == 'gmail.message' and m.get('message-id'):
            if m['message-id'] in seen_message_ids:
                continue  # the same email in two mailboxes counts once
            seen_message_ids.add(m['message-id'])
        crm = m.get('crm_account') if isinstance(m.get('crm_account'), dict) else None
        if crm and crm.get('domain') and crm.get('name') and '@' not in str(crm['name']):  # an address is no organization's name
            crm_names[str(crm['domain']).lower()] = str(crm['name'])
        if kind in ('salesflare.email', 'salesflare.meeting', 'salesforce.opportunity', 'salesforce.task', 'salesforce.activity'):
            for c in m.get('contacts') or ():
                if isinstance(c, dict) and '@' in str(c.get('email') or ''):
                    appears['email:' + str(c['email']).lower()].add(f"a {kind.split('.')[0].title()} contact" + (' at ' + str(crm['name']) if crm and crm.get('name') else ''))
        elif kind in ('stripe.event', 'intercom.conversation'):
            billed = ' '.join(str(m.get('customer_name') or '').split()) if kind == 'stripe.event' else ''  # with "@": no name, no organization's
            for _, addr in addresses(relayed(kind, m).get('from'))[:1]:
                if addr.rsplit('@', 1)[1] in owner.domains or relay(addr):
                    continue  # a teammate answering support or sending an invoice
                appears['email:' + addr].add(('billed through Stripe' + (' as ' + billed if billed and '@' not in billed else ''))
                                             if kind == 'stripe.event' else 'wrote to support (Intercom)')
                if billed and '@' not in billed and addr.rsplit('@', 1)[1] not in FREEMAIL:
                    paying_names.setdefault(addr.rsplit('@', 1)[1], billed)
        if event_id in unsubscribes:
            continue
        if kind == 'gmail.message' and (m.get('list_unsubscribe') or m.get('list_id') or automated(m)):
            listed |= {'email:' + a for _, a in addresses(m.get('from'))[:1]}
        found = [t for t in touches(kind, m, owner, wrote_to) if not (t[0].startswith('email:') and t[0].rsplit('@', 1)[1] in warmup) and t[0] not in rooms and not gone(t[0])
                 and not (t[0].startswith('email:') and t[0] not in people_kept and room_like(t[0][6:], t[1]))]
        if kind == 'gmail.message' and found and found[0][3] in ('them', 'seen') and not {event_id, found[0][0]} & kept and (why := mass_mail(
                m, found[0][0][6:], found[0][1], org_from_name(found[0][1], found[0][0].rsplit('@', 1)[1]), wrote_to)):
            found = mailings.add(found, why, at)  # a mailing: its sender is no person, until the owner writes to them or shows them
        if not found:
            continue
        if kind == 'linkedin.message' and isinstance(m.get('headline'), str) and m['headline'].strip() and not m.get('group'):
            headlines.add('li:' + str(m['conversation_id']))
        per_event[event_id] = (kind, at, account_id, m, found)
        keys.see(event_id, account_id, kind, m, found, *thread_key(kind, m))
        if kind == 'gmail.message' and found[0][3] in ('them', 'seen') and found[0][0].startswith('email:') and event_id not in past:
            senders[found[0][0]].append((at, event_id))
        if any(role in ('owner', 'met') for _, _, _, role in found):
            owner_events.add(event_id)
        for identifier, name, _, _ in found:
            if name and str(name).strip() and '@' not in str(name) and str(name).strip().casefold() not in GENERIC_NAMES:
                names[identifier][person_name(name)] += 1
                if identifier.startswith('email:') and (org := org_from_name(name, identifier.rsplit('@', 1)[1])):
                    said_orgs[identifier.rsplit('@', 1)[1]][org] += 1
            if identifier.startswith('x:') and m.get('screen_name') and not m.get('from_me'):
                x_names[identifier] = m['screen_name']
    return (kept, mailings, listed, warmup, gone, per_event, names, x_names, crm_names, paying_names, said_orgs,
            appears, owner_events, headlines, keys, senders)
