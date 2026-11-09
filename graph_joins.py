"""Which identities a name may join in a graph build (graph._build_in; docs/intelligence.md, Same person?).

A name joins two identities only when each of them is one person's own:

- A shared address is never a join key, for the message, conversation and name rules alike: a role or team inbox
  (info@, sales@, team@: own_addresses.role_like), an automated sender (mail_senders.bulk), a mailing list (the
  address its List-Id names), or any identifier seen under two or more people's names (own_addresses.people: a Google
  Group's "Ann via Founders" and "Bo via Founders", a mailbox two colleagues answer). The people who wrote through it
  stay themselves. Such an address, or a list, goes by its address and has no person's name to ask about (several()).
- A name alone never joins a work contact with a personal chat. An identity's side is the side of the accounts it was
  seen in (graph.account_side); for an account that was never placed, a company address, Slack and the CRM are work,
  WhatsApp and Telegram personal, and anything else says nothing. When a name is on a work identity and on a personal
  one, they are one person as before when something else agrees (Keys.agree): the work side is a colleague (an
  address at the owner's own domain), the chat's number is known for the work side (a connector's profile, the
  owner's own edit), both are on one project, both are at one organization, or one signal has both. When the name is
  all there is, each side joins within itself only, and the pair is left for "Same person?" (graph.likely_same) to ask.

Nothing is stored: it is worked out again each build, from the signals. The owner's and the agent's own merges
(graph_merges) are joined before any of this and are never undone by it. So a person an older build made of several
people comes apart by the next build, and nothing is deleted: what the owner kept on them (a note, a role, a project)
stays with the identity it was kept on, the one the person was named for. Keep private goes with every part
(private_parts, keep_private), so nobody the owner kept private is shared for having been told apart."""
from __future__ import annotations

import collections
import contextlib
import json
import re

import own_addresses
from mail_senders import bulk

PERSONAL_SPACES = frozenset({'wa', 'tg'})
WORK_SPACES = frozenset({'slack'})
CRM_KINDS = ('salesflare.', 'salesforce.')
LIST_ID = re.compile(r'<([^<>\s]+)>\s*$')
email_first = lambda identifier: (not identifier.startswith('email:'), identifier)


class Keys:
    """One build's join keys. owner: graph.Owner (its names are never a person's); plain_name, account_side and
    freemail come from graph.py, which imports this module."""
    def __init__(self, config, owner, plain_name, account_side, freemail):
        self.owner, self.plain_name, self.freemail = owner, plain_name, freemail
        self.side_of_account = {a.get('id'): account_side(a) for a in config.get('accounts', []) if isinstance(a, dict) and a.get('id')}
        self.named_on = collections.defaultdict(lambda: collections.defaultdict(set))  # (message or conversation) -> full name -> identifiers
        self.carried = collections.defaultdict(set)  # identifier -> the full names it was seen under
        self.seen_in = collections.defaultdict(set)  # identifier -> the sides of the accounts it was seen in
        self.lists = set()
        self.signals = collections.defaultdict(set)  # identifier -> the signals it is on
        self.threads = collections.defaultdict(set)  # identifier -> its conversations; conversation -> its signals
        self._shared, self._known = {}, None

    def see(self, event_id, account_id, kind, m, found, key, exact):
        """One signal's identities (graph.touches) and its conversation (graph.thread_key)."""
        listed = str(m.get('list_id') or '').strip().lower()
        listed = (LIST_ID.search(listed).group(1) if LIST_ID.search(listed) else listed).strip('.')
        side = 'work' if kind.startswith(CRM_KINDS) else self.side_of_account.get(account_id)
        for identifier, name, _, _ in found:
            self.signals[identifier].add(event_id)
            if key:
                self.threads[identifier].add((account_id, key))
                self.threads[(account_id, key)].add(event_id)
            if side:
                self.seen_in[identifier].add(side)
            if listed and identifier.startswith('email:') and identifier[6:].replace('@', '.') == listed:
                self.lists.add(identifier)
            full = self.plain_name(name) if name and '@' not in str(name) else None
            if full and full not in self.owner.names:
                self.carried[identifier].add(full)
                self.named_on[('message', event_id)][full].add(identifier)
                if key and exact:
                    self.named_on[('thread', account_id, key)][full].add(identifier)

    def people(self, identifier):
        return own_addresses.people(self.carried.get(identifier, ()))

    def several(self, identifier):
        """A mailing list, or an address read under two or more people's names: it goes by its address, and there is
        no person's name on it to ask about."""
        return identifier in self.lists or identifier.startswith('email:') and self.people(identifier) >= 2

    def shared(self, identifier):
        """More than one person writes through it, or may: never a join key."""
        if identifier not in self._shared:
            address = identifier[6:] if identifier.startswith('email:') else ''
            self._shared[identifier] = bool(address and (own_addresses.role_like(address) or bulk(address))) or identifier in self.lists or self.people(identifier) >= 2
        return self._shared[identifier]

    def together(self):
        """(a, b, 'message' or 'thread'): the same full name on two identities in one message, then in one conversation."""
        for where, by_full in sorted(self.named_on.items(), key=lambda item: item[0][0] != 'message'):
            for _, group in sorted(by_full.items()):
                group = sorted((i for i in group if not self.shared(i)), key=email_first)
                for other in group[1:]:
                    yield group[0], other, where[0]

    def side(self, members):
        """'work' or 'personal' when everything known of these identifiers points one way, else None."""
        sides = set()
        for identifier in members:
            space, _, value = identifier.partition(':')
            sides |= self.seen_in.get(identifier) or (
                {'personal'} if space in PERSONAL_SPACES else
                {'work'} if space in WORK_SPACES or space == 'email' and value.rsplit('@', 1)[-1] not in self.freemail else set())
        return sides.pop() if len(sides) == 1 else None

    def known(self, db):
        """What the Machine knows besides names, read once: {'phones' | 'orgs' | 'projects': identifier -> set}, and
        'events': signal -> its projects."""
        if self._known is None:
            import enrichment
            from graph import folded_words
            self.fold = folded_words
            out = self._known = {k: collections.defaultdict(set) for k in ('phones', 'orgs', 'projects', 'events')}
            digits = lambda value: re.sub(r'\D', '', str(value or ''))[-9:]
            for identifier, facts in enrichment.people_facts(db, fields={'phone'}).items():  # a connector's profile (Slack, the CRM)
                out['phones'][identifier].add(digits(facts['phone'][0]))
            for r in db.execute("SELECT identifier,json_extract(profile,'$.phone') FROM person_profiles WHERE status='found' AND profile IS NOT NULL"):
                out['phones'][r[0]].add(digits(r[1]))
            for r in db.execute("SELECT identifier,fields FROM person_edits"):  # the owner's own edit
                with contextlib.suppress(ValueError, AttributeError, TypeError):
                    out['phones'][r[0]] |= {digits(v) for v in (json.loads(r[1]).get('phones') or {}).get('added') or ()}
            for r in db.execute('SELECT identifier,org,org_id FROM person_orgs'):  # where they said they work
                out['orgs'][r[0]] |= {folded_words(r[1])} | ({r[2][4:]} if str(r[2] or '').startswith('org:') else set())
            for r in db.execute('SELECT event_id,project_id FROM event_projects'):
                out['events'][r[0]].add(r[1])
            for r in db.execute('SELECT project_id,node_id FROM project_people'):  # put on a project by the owner
                out['projects'][r[1]].add(r[0])
        return self._known

    def agree(self, db, work, chat):
        """Whether something besides the name says these work identities and these personal ones are one person."""
        known = self.known(db)
        address = lambda i: i[6:] if i.startswith('email:') else ''
        own = {self.fold(d.split('.')[0]) for d in self.owner.domains}
        if any(address(i).rsplit('@', 1)[-1] in self.owner.domains or known['orgs'].get(i, set()) & own for i in work):
            return True  # a colleague: the owner knows who that is
        if set().union(*(self.signals[i] for i in work)) & set().union(*(self.signals[i] for i in chat)):
            return True
        numbers = {i[3:][-9:] for i in chat if i.startswith('wa:') and i[3:].isdigit() and len(i) > 10}  # the chat's own number
        if numbers & set().union(*(known['phones'].get(i, ()) for i in work)):
            return True

        def projects(side):  # a project its own signals are on, or one a conversation of theirs is on
            events = set().union(*(self.signals[i] for i in side), *(self.threads[t] for i in side for t in self.threads[i]))
            return set().union(*(known['events'].get(e, ()) for e in events), *(known['projects'].get(i, ()) for i in side))

        def orgs(side):
            domains = {address(i).rsplit('@', 1)[-1] for i in side if address(i)} - self.freemail
            return domains | {self.fold(d.split('.')[0]) for d in domains} | set().union(*(known['orgs'].get(i, ()) for i in side))
        return bool(projects(work) & projects(chat) or orgs(work) & orgs(chat))

    def join_names(self, db, union, known, best):
        """The same full name on different channels is one person, unless two people carry it on one channel (two
        addresses or two chats not shown to be one), someone said they differ, or it is all a work contact and a
        personal chat have in common (agree): then it is only a question. best: identifier -> the name it mostly goes by."""
        by_name = collections.defaultdict(set)
        for identifier in known:
            full = self.plain_name(best(identifier))
            if full and full not in self.owner.names and not self.shared(identifier):  # the owner writes from other channels too
                by_name[full].add(identifier)
        for _, group in sorted(by_name.items()):
            spaces = collections.defaultdict(set)
            for i in group:
                spaces[i.split(':', 1)[0]].add(union.find(i))
            if len(spaces) < 2 or any(len(roots) > 1 for roots in spaces.values()):
                continue
            group = sorted(group, key=email_first)
            sides = {i: self.side(union.members[union.find(i)]) for i in group}
            ids = lambda side: set().union(*(union.members[union.find(i)] for i in group if sides[i] == side))
            both = {'work', 'personal'} <= set(sides.values()) and not self.agree(db, ids('work'), ids('personal'))
            for other in group[1:]:
                first = next((i for i in group if sides[i] and sides[i] == sides[other]), None) if both else group[0]
                if first and first != other:
                    union.join(first, other, 'name')


def private_parts(db, union, nodes):
    """Before a build's publish: the people this build makes of someone kept private (shared_graph.py, share_private)
    who don't carry that yet. A person split in two, or merged under another identity's id, stays private in every part."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='share_private'").fetchone():
        return set()
    private = {r[0] for r in db.execute('SELECT node_id FROM share_private')}
    parts = set()
    for r in db.execute("SELECT n.info FROM share_private p JOIN graph_nodes n ON n.id=p.node_id WHERE n.kind='person'"):
        with contextlib.suppress(ValueError, AttributeError, TypeError):
            parts |= {union.find(i) for i in json.loads(r[0] or '{}').get('identifiers') or () if i in union.parent}
    return (parts & set(nodes)) - private


def keep_private(db, parts):
    """After the publish: the owner's Keep private, on each part (private_parts)."""
    if parts:
        import shared_graph  # it imports graph, which imports this module
        for node in sorted(parts):
            with contextlib.suppress(ValueError):
                shared_graph.keep_private(db, node)
