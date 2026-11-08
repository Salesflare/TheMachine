"""Which services mail the owner: the senders' own domains in the mail on this Machine. For the setup hints
(machine/delivery/push.py setup_hints) and Connections, + Add, Suggested for you (suggest.py)."""
from __future__ import annotations

import email.utils

# The sources a setup hint may suggest when their mail keeps coming in: (service, label, sender domains)
HINT_SOURCES = (('github', 'GitHub', ('github.com',)), ('slack', 'Slack', ('slack.com',)),
                ('stripe', 'Stripe', ('stripe.com',)), ('intercom', 'Intercom', ('intercom.io', 'intercom-mail.com', 'intercom.com')),
                ('zoom', 'Zoom', ('zoom.us',)))
HINT_MAILS = 3  # this many mails in 30 days from a service before it is worth suggesting


def sender_domain_in(sender, domains):
    """Whether a From ("Name <a@mail.slack.com>" or the bare address) is at one of these domains or a subdomain of one:
    the address's own domain, so notslack.com, slack.com.example and a name that mentions slack.com never count."""
    address = email.utils.parseaddr(str(sender or ''))[1].lower()
    host = address.rpartition('@')[2].rstrip('.') if '@' in address else ''
    return bool(host) and any(host == d or host.endswith('.' + d) for d in domains)


def mails_from(db, domains, since, enough):
    """How many mails since `since` came from one of these domains (sender_domain_in), counting up to `enough`."""
    like = ' OR '.join("lower(json_extract(metadata,'$.from')) LIKE ?" for _ in domains)
    rows = db.execute(f"SELECT json_extract(metadata,'$.from') FROM events WHERE kind IN ('gmail.message','ms_graph.message') AND history=0 "
                      f"AND occurred_at>=? AND ({like})", (since, *[f'%@%{d}%' for d in domains]))
    found = 0
    for (sender,) in rows:  # the LIKE only narrows: the sender's own domain must be the service's (not x.com in fedex.com)
        found += sender_domain_in(sender, domains)
        if found >= enough:
            break
    return found
