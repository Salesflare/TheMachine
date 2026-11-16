"""A Notion heads-up (connectors/notion.py notion.edit): someone changed a page the owner asked to have changed. Its
to-do is quiet (machine/todo_kinds.py): it never buzzes, it waits in the list and the morning summary."""
import sqlite3


def is_heads_up(db, suggestion_id):
    """Whether a to-do comes only from Notion page changes the owner asked for."""
    try:
        kinds = {r[0] for r in db.execute('SELECT e.kind FROM suggestions s JOIN json_each(s.event_ids) j JOIN events e ON e.id=j.value '
                                          'WHERE s.id=?', (suggestion_id,))}
    except sqlite3.OperationalError:
        return False
    return kinds == {'notion.edit'}


def view(db, suggestion_id, metas):
    """Nothing of its own to show: it reads like any to-do."""
    return None
