"""Organizations people are in: the ones the owner added by hand, and stated organizations joined to
the one with that name or domain, or standing on their own."""

import enrichment
from graph import folded_words


def place_in_organizations(manual, named_orgs, owner, warmup, members, crm_names, edits, named, paying_names, profiles,
                           said_orgs, inboxes, mailings, nodes, stated, strength):
    # Organizations the owner added by hand stand even with nobody in them yet.
    for r in manual:
        if r['kind'] == 'org' and r['identifier'].startswith('org:named:'):
            named_orgs.setdefault(r['identifier'], [])
        elif r['kind'] == 'org' and r['identifier'][4:] not in owner.domains | warmup:
            members.setdefault(r['identifier'][4:], [])

    # Stated organizations join the one with that name or domain, or stand as their own (no domain, never looked up).
    def org_name(domain):
        # A CRM or Stripe name that is only the domain says nothing; a looked-up or readable one reads better.
        said = [n for n in (crm_names.get(domain), paying_names.get(domain)) if n and str(n).strip().lower().removeprefix('www.') != domain]
        return (named.get('org:' + domain) or (said[0] if said else None)
                or ({**(profiles.get(domain) or {}), **edits.get(domain, {})}).get('name')
                or (said_orgs[domain].most_common(1)[0][0] if said_orgs.get(domain) else None) or enrichment.readable_name(domain))
    by_org_name = {}
    for domain in sorted(members):
        by_org_name.setdefault(folded_words(org_name(domain)), domain)
        for node, _ in inboxes.get(domain, ()): mailings.found[node][0] = org_name(domain)  # a shared inbox goes by its organization
    for domain in sorted(members):  # "Acme" is acme.com when no organization is called that
        by_org_name.setdefault(folded_words(domain.split('.')[0]), domain)
    infos = {n[0]: n[9] for n in nodes}
    own = {folded_words(d.split('.')[0]) for d in owner.domains}
    for node, said_org in stated.items():
        value = strength[node]
        if folded_words(said_org['org']) in own:
            infos[node]['colleague'] = True  # the owner's own company, as with an address at the owner's domain
            continue
        given = str(said_org['org_id'] or '')
        domain = given[4:] if given.startswith('org:') and given[4:] in members else by_org_name.get(folded_words(said_org['org']))
        if domain:
            members[domain].append((node, value))
            org_id = 'org:' + domain
        else:
            org_id = 'org:named:' + '-'.join(folded_words(said_org['org']).split())[:80]
            named_orgs[org_id].append((node, value, said_org['org']))
        infos[node].update(org=org_id, org_by=said_org['source'] if said_org['source'] == 'owner' else 'review', org_name=said_org['org'],
                           org_via=said_org['via'], org_event_id=said_org['event_id'], org_at=said_org['said_at'])  # the quote stays sealed
    return (org_name, infos)
