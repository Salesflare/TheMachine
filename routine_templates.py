"""Routine templates (docs/help/routines.md, "Templates"): ready-made routines the owner adds with one tap on the
Routines page. A template's routine is an ordinary one (origin 'template:<key>'): it can be paused, stopped, run now and
moved to another time, but its words are the template's own, so it has no Edit.

Its run is the template's own, not a turn on its words (routines_app.routine_template_run): Newsletter cleanup is plain
code, no model; Spam cleanup reads the day's mail by unknown senders in one short turn, only when there is any. Each
ends in at most one to-do with a choice per item (mail_cleanup.py), and nothing changes until the owner confirms there.
Birthdays is plain code too (birthdays.py, birthdays_app.py): a to-do per close contact with a birthday today, its
greeting drafted on their usual channel and sent only when the owner says so.

No table: the catalog is here, and a template is added when a live routine has its origin."""
import i18n

AT = '07:30'  # before the morning summary, so the to-do waits there
DAILY = 'daily'  # recurring.PRESETS

# key -> its name and what it does, in the owner's language at view time (scripts/i18n_extract.py SERVER_TEXT); what it
# does is also its routine's words
TEMPLATES = {
    'newsletters': {'name': 'Newsletter cleanup', 'what': 'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.'},
    'spam': {'name': 'Spam cleanup', 'what': 'Every morning, one to-do with spam that got through. Mark each one as spam or not.'},
    'birthdays': {'name': 'Birthdays', 'what': 'Every morning, a to-do with a short greeting for each close contact who has a birthday.'},
}


def key_of(origin):
    """The template a routine came from ('newsletters'), or None."""
    origin = str(origin or '')
    key = origin[9:] if origin.startswith('template:') else None
    return key if key in TEMPLATES else None


def view(db, can_mark=True):
    """The Templates section: [{key, name, what, added}], added when a live routine (on or paused) has its origin. Spam
    cleanup only when a mail account may move mail to spam (can_mark): read-only Gmail can't, so it isn't offered there."""
    live = {r[0] for r in db.execute("SELECT origin FROM routines WHERE origin LIKE 'template:%' AND state IN ('on','paused')")}
    return [{'key': key, 'name': i18n.t(t['name']), 'what': i18n.t(t['what']), 'added': 'template:' + key in live}
            for key, t in TEMPLATES.items() if key != 'spam' or can_mark]


def what(key):
    """What a template's routine does, in the owner's language: its card shows this, not the words it was made with."""
    return i18n.t(TEMPLATES[key]['what'])


def live(db, key):
    """The live routine (on or paused) of a template, or None."""
    return db.execute("SELECT * FROM routines WHERE origin=? AND state IN ('on','paused') ORDER BY created_at LIMIT 1",
                      ('template:' + key,)).fetchone()
