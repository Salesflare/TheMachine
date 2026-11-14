"""To-do kinds: to-dos a routine template or a feature makes that behave unlike an ordinary to-do (the owner picks per
item on the to-do, it is only for reading, it never buzzes). The core paths ask here instead of naming each kind's
module: delivery (quiet), the to-do's card and its choices (close_only), the owner's decision (refused), the view
(view, reads) and the area digest (reading).

A kind's own module holds its code and table; KINDS names it by module, imported on first use (a kind's module may
import machine.cards, which asks here). Each trait keeps what its path did before the registry, one kind at a time:
where two kinds differ, the trait says so."""
import importlib
import sqlite3

import i18n


class TodoKind:
    """One kind of to-do.
    key: its part of the to-do's view (suggestion_result's extra[key]) and of card_reads' read-ahead.
    module: the module that owns it; test, view: its functions there. test(db, suggestion_id) -> is it one; view(db,
      suggestion_id, metas[, read]) -> what the to-do shows of it, or None. metas: no when its view takes no evidence.
    table: its items, one or more rows per to-do (suggestion_id).
    quiet: never buzzes: no ping, push or waiting email; it waits in the list and the morning summary (deliver.py).
    reading: something to read or sort, not to do: an area's digest leaves it out (notifications.to_read).
    close_only: its Telegram card offers only Mark done, Snooze and Not needed: its picks are on the to-do (cards.py).
    refused: the line shown for Do it, Answer or Try again, which it has none of (card_actions.py), or None.
    reads: SQL reading its items for a list of to-dos at once (json_each of their ids), and read_as: the keyword its
      view takes them by; read_dict: each row as a dict (else the row)."""

    def __init__(self, key, module, *, test=None, view='view', metas=True, table=None, quiet=False, reading=False,
                 close_only=False, refused=None, reads=None, read_as=None, read_dict=False):
        self.key, self.module, self.test_name, self.view_name, self.metas = key, module, test, view, metas
        self.table, self.quiet, self.reading, self.close_only, self.refused = table, quiet, reading, close_only, refused
        self.reads, self.read_as, self.read_dict = reads, read_as, read_dict

    def code(self):
        return importlib.import_module(self.module)

    def test(self, db, suggestion_id):
        return bool(self.test_name) and getattr(self.code(), self.test_name)(db, suggestion_id)

    def view(self, db, suggestion_id, metas, pre=None):
        """What the to-do shows of this kind, or None. pre: card_reads' read-ahead for a list of to-dos."""
        read = pre.get(self.key) if pre and self.read_as else None
        args = (db, suggestion_id, metas) if self.metas else (db, suggestion_id)
        return getattr(self.code(), self.view_name)(*args, **({self.read_as: read.get(suggestion_id, {})} if read is not None else {}))


# In the order the core paths asked before: the owner's decision checked cleanup, then Subscriptions, then the digest.
KINDS = (
    # A routine template's cleanup (mail_cleanup.py: newsletters, spam): Keep or Unsubscribe, Spam or Not spam, per item
    TodoKind('cleanup', 'mail_cleanup', test='is_cleanup', table='mail_cleanup_items', quiet=True, reading=True, close_only=True,
             refused=lambda: i18n.t('Pick for each one on the to-do, then confirm.'),
             reads='SELECT * FROM mail_cleanup_items WHERE suggestion_id IN (SELECT value FROM json_each(?))', read_as='have', read_dict=True),
    # Subscriptions and trials (subscriptions.py): Keep or Cancel per subscription. Cancel only drafts; the owner sends it.
    # Keep and Cancel live on the dashboard's rows, so its Telegram card has only Mark done, Snooze and Not needed. Unlike
    # the other two, an area's digest keeps it (reading no): a trial about to charge needs the owner.
    TodoKind('subs', 'subscriptions', test='is_subs', table='subs_items', quiet=True, close_only=True,
             refused=lambda: i18n.t('Pick Keep or Cancel it for each one on the to-do.')),
    # The Daily digest (reading_digest.py): why each one matters, More or Less like this. Reading, never urgent.
    TodoKind('digest', 'reading_digest', test='is_digest', table='digest_items', quiet=True, reading=True, close_only=True,
             refused=lambda: i18n.t('A digest is only for reading.'),
             reads='SELECT suggestion_id,item,feedback FROM digest_items WHERE suggestion_id IN (SELECT value FROM json_each(?))', read_as='rows'),
    # Birthdays' import from Facebook (birthdays_facebook.py): Import, the preview, Save. Only its view is its own.
    TodoKind('facebook_birthdays', 'birthdays_facebook', metas=False, table='facebook_birthdays'),
)


def quiet(db, suggestion_id):
    """Is it a to-do of a kind that never buzzes?"""
    return any(k.test(db, suggestion_id) for k in KINDS if k.quiet)


def refused(db, suggestion_id):
    """The line for Do it, Answer or Try again on a to-do of a kind that has none, or None."""
    for k in KINDS:
        if k.refused and k.test(db, suggestion_id):
            return k.refused()
    return None


def close_only(view):
    """Does this to-do's view (suggestion_result) hold a kind whose picks are on the to-do?"""
    return any(view.get(k.key) for k in KINDS if k.close_only)


def views(db, suggestion_id, metas, pre=None):
    """{key: what the to-do shows} of the kinds it is, for suggestion_result's extra."""
    out = {}
    for k in KINDS:
        shown = k.view(db, suggestion_id, metas, pre)
        if shown:
            out[k.key] = shown
    return out


def reads(db, ids):
    """card_reads' read-ahead: {key: {suggestion_id: {item: row}}} for the kinds that read their items for a list of
    to-dos (ids: their JSON list). A kind whose table isn't there yet is left out: each to-do looks as before."""
    pre = {}
    for k in KINDS:
        if not k.reads:
            continue
        try:
            found = {}
            for r in db.execute(k.reads, (ids,)):
                found.setdefault(r['suggestion_id'], {})[r['item']] = dict(r) if k.read_dict else r
            pre[k.key] = found
        except sqlite3.OperationalError:
            pass
    return pre


def reading_ids(db):
    """The ids of the to-dos of a kind that is something to read or sort, not to do."""
    ids = set()
    for k in KINDS:
        if k.reading:
            try:
                ids |= {r[0] for r in db.execute(f'SELECT DISTINCT suggestion_id FROM {k.table}')}
            except sqlite3.OperationalError:  # a database before that table
                pass
    return ids
