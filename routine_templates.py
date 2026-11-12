"""Routine templates (docs/help/routines.md, "Templates"): ready-made routines the owner adds with one tap on the
Routines page. A template's routine is an ordinary one (origin 'template:<key>'): it can be paused, stopped, run now,
moved to another time, renamed and edited like any routine. Its words are the template's own (WORDS, shown in the
owner's language) until the owner changes them in Edit.

While its words are the template's own and it has no script steps (own), its run is the template's own code, not a
turn on its words (routines_app.routine_template_run): Newsletter cleanup is plain code, no model; Spam cleanup runs every
hour (HOURLY): plain code lists the mail by unknown senders that is new since its last run, and only when there is any
does one small model call (no tools, no agent) read just those. Each ends in at most one to-do with a
choice per item (mail_cleanup.py), and nothing changes until the owner confirms there. Birthdays is plain code too
(birthdays.py, birthdays_app.py): a to-do per close contact with a birthday today, its greeting drafted on their usual
channel and sent only when the owner says so. Daily digest (reading_digest.py, reading_digest_app.py): plain code lists
the new unread newsletters, and only when there are any does one small model call pick the few worth reading, for the
interests the owner sees and edits on its card. A rename alone keeps this cheap path.

Once the owner edits its words (or adds script steps), it runs as a normal routine on them: a read-only turn each run.
Its origin still names the template, so Templates shows it as added. An edited Newsletter or Spam cleanup still sees
the mail its template would list and may pick from it (routines_app.routine_cleanup_lines): its picks become the same
cleanup to-do, one choice per item. An edited Birthdays ends like any routine, in its result and at most one draft.
Back to the template in Edit (routine_edit back) puts the template's words back, drops script steps and runs its code
again.

No table: the catalog is here, and a template is added when a live routine has its origin."""
import i18n

AT = '07:30'  # before the morning summary, so the to-do waits there; an hourly one runs at :30
DAILY = 'daily'  # recurring.PRESETS
HOURLY = 'hourly'  # routines.HOURLY: often enough to be there before the owner marks spam by hand

# key -> its name, what it does (the Templates list) and its words (its routine's words, what Edit shows), in the
# owner's language at view time (scripts/i18n_extract.py SERVER_TEXT)
TEMPLATES = {
    'newsletters': {'name': 'Newsletter cleanup', 'what': 'Every morning, one to-do with the past day’s newsletters. Keep or unsubscribe each one.',
                    'words': 'Find the newsletters and mailing list emails that came in since the last run, one per sender. '
                             'Put them in one to-do where I pick Keep or Unsubscribe for each.'},
    'spam': {'name': 'Spam cleanup', 'what': 'Every hour, a to-do with any new spam that got through. Mark each one as spam or not.',
             'rule': HOURLY, 'was': ('Every morning, one to-do with spam that got through. Mark each one as spam or not.',),
             'words': 'Find clear spam from unknown senders since the last run: cold sales pitches, scams, phishing and fake '
                      'invoices. Leave out newsletters I signed up for, receipts and real people. Put them in one to-do where '
                      'I pick Spam or Not spam for each.'},
    'digest': {'name': 'Daily digest', 'what': 'Every morning, the few newsletter pieces worth your time, picked for what you care about.',
               'words': 'Read my newsletters since the last run and pick the few pieces most worth my time, for what I care about. '
                        'Put them in one to-do, each with one line on why it matters and a link to the original.'},
    'birthdays': {'name': 'Birthdays', 'what': 'Every morning, a to-do with a short greeting for each close contact who has a birthday.',
                  'words': 'Find my close contacts who have a birthday today. For each one, write a short greeting in their '
                           'language, where I usually talk with them, for me to send.'},
}
CLEANUP = ('newsletters', 'spam')  # an edited one may still end in the cleanup to-do (routines_app.routine_cleanup_lines)


def rule(key):
    """How often a template's routine runs: its own rhythm, else daily."""
    return TEMPLATES[key].get('rule', DAILY)


def hourly_spam(db, stamp):
    """A Spam cleanup added while it ran daily, still on the template's time (the owner never changed when): hourly
    from now on, its first hourly run right away. Changed when: left as the owner set it."""
    import routines  # routines.py owns the table
    routines.rerule(db, 'template:spam', {'unit': 'day', 'n': 1}, AT, routines.HOURLY, stamp)


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
    return _flat(text) in {_flat(t['words']), _flat(words(key)), _flat(t['what']), *map(_flat, t.get('was', ()))}


def own(origin, text, steps=None):
    """The template whose own code runs a routine or a run with these words and steps, or None: one from a template
    with the template's words and no script steps."""
    key = key_of(origin)
    return key if key and not steps and is_own(key, text) else None


def view(db, spam_needs=None):
    """The Templates section: [{key, name, what, added}], added when a live routine (on or paused) has its origin. Spam
    cleanup is always listed, so the owner knows it exists; spam_needs says why it can't be added when no mail account
    may move mail to spam ('gmail': Gmail connected read-only, the hosted broker never asks gmail.modify; 'mail': no
    mailbox it may move spam in), and the page shows that line in place of Add."""
    live = {r[0] for r in db.execute("SELECT origin FROM routines WHERE origin LIKE 'template:%' AND state IN ('on','paused')")}
    return [{'key': key, 'name': i18n.t(t['name']), 'what': i18n.t(t['what']), 'added': 'template:' + key in live,
             **({'needs': spam_needs} if key == 'spam' and spam_needs else {})}
            for key, t in TEMPLATES.items()]


def live(db, key):
    """The live routine (on or paused) of a template, or None."""
    return db.execute("SELECT * FROM routines WHERE origin=? AND state IN ('on','paused') ORDER BY created_at LIMIT 1",
                      ('template:' + key,)).fetchone()
