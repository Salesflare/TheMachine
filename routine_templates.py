"""Routine templates (docs/help/routines.md, "Templates"): ready-made routines the owner adds with one tap on the
Routines page. A template's routine is an ordinary one (origin 'template:<key>'): it can be paused, stopped, run now,
moved to another time, renamed and edited like any routine. Its words are the template's own (WORDS, shown in the
owner's language) until the owner changes them in Edit.

While its words are the template's own and it has no script steps (own), its run is the template's own code, not a
turn on its words (routines_app.routine_template_run): Newsletter cleanup is plain code, no model; Spam cleanup reads
the day's mail by unknown senders in one short turn, only when there is any. Each ends in at most one to-do with a
choice per item (mail_cleanup.py), and nothing changes until the owner confirms there. Birthdays is plain code too
(birthdays.py, birthdays_app.py): a to-do per close contact with a birthday today, its greeting drafted on their usual
channel and sent only when the owner says so. A rename alone keeps this cheap path.

Once the owner edits its words (or adds script steps), it runs as a normal routine on them: a read-only turn each run.
Its origin still names the template, so Templates shows it as added. An edited Newsletter or Spam cleanup still sees
the mail its template would list and may pick from it (routines_app.routine_cleanup_lines): its picks become the same
cleanup to-do, one choice per item. An edited Birthdays ends like any routine, in its result and at most one draft.
Back to the template in Edit (routine_edit back) puts the template's words back, drops script steps and runs its code
again.

No table: the catalog is here, and a template is added when a live routine has its origin."""
import i18n

AT = '07:30'  # before the morning summary, so the to-do waits there
DAILY = 'daily'  # recurring.PRESETS

# key -> its name, what it does (the Templates list) and its words (its routine's words, what Edit shows), in the
# owner's language at view time (scripts/i18n_extract.py SERVER_TEXT)
TEMPLATES = {
    'newsletters': {'name': 'Newsletter cleanup', 'what': 'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',
                    'words': 'Find the newsletters and mailing list emails that came in since the last run, one per sender. '
                             'Put them in one to-do where I pick Keep or Unsubscribe for each.'},
    'spam': {'name': 'Spam cleanup', 'what': 'Every morning, one to-do with spam that got through. Mark each one as spam or not.',
             'words': 'Find clear spam from unknown senders since the last run: cold sales pitches, scams, phishing and fake '
                      'invoices. Leave out newsletters I signed up for, receipts and real people. Put them in one to-do where '
                      'I pick Spam or Not spam for each.'},
    'birthdays': {'name': 'Birthdays', 'what': 'Every morning, a to-do with a short greeting for each close contact who has a birthday.',
                  'words': 'Find my close contacts who have a birthday today. For each one, write a short greeting in their '
                           'language, where I usually talk with them, for me to send.'},
}
CLEANUP = ('newsletters', 'spam')  # an edited one may still end in the cleanup to-do (routines_app.routine_cleanup_lines)


def key_of(origin):
    """The template a routine came from ('newsletters'), or None."""
    origin = str(origin or '')
    key = origin[9:] if origin.startswith('template:') else None
    return key if key in TEMPLATES else None


def _flat(text):
    return ' '.join(str(text or '').split())


def words(key):
    """A template's words in the owner's language: what its routine's card and Edit show while they are its own."""
    return i18n.t(TEMPLATES[key]['words'])


def is_own(key, text):
    """Are these words the template's own? Its English words as stored, the same in the owner's language (Edit saved
    as shown), or what a routine added before the template had words was made with (its 'what')."""
    if key not in TEMPLATES:
        return False
    t = TEMPLATES[key]
    return _flat(text) in {_flat(t['words']), _flat(words(key)), _flat(t['what'])}


def own(origin, text, steps=None):
    """The template whose own code runs a routine or a run with these words and steps, or None: one from a template
    with the template's words and no script steps."""
    key = key_of(origin)
    return key if key and not steps and is_own(key, text) else None


def view(db, can_mark=True):
    """The Templates section: [{key, name, what, added}], added when a live routine (on or paused) has its origin. Spam
    cleanup only when a mail account may move mail to spam (can_mark): read-only Gmail can't, so it isn't offered there."""
    live = {r[0] for r in db.execute("SELECT origin FROM routines WHERE origin LIKE 'template:%' AND state IN ('on','paused')")}
    return [{'key': key, 'name': i18n.t(t['name']), 'what': i18n.t(t['what']), 'added': 'template:' + key in live}
            for key, t in TEMPLATES.items() if key != 'spam' or can_mark]


def live(db, key):
    """The live routine (on or paused) of a template, or None."""
    return db.execute("SELECT * FROM routines WHERE origin=? AND state IN ('on','paused') ORDER BY created_at LIMIT 1",
                      ('template:' + key,)).fetchone()
