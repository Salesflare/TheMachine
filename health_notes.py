"""Health notes (docs/help/notes.md, "Health"): what the owner's Machine knows about the owner's own health, in a few
notes under Health, kept the way every kind in sections is (section_notes.py: one small model call over what is new
only, the owner's own notes in a part filled in, a part only from two lines).

Each line points to where the thing lives instead of copying it: a bill's opens its to-do and mail (its amount and
payment details stay there), a line from what The Machine learned is that fact.

Candidates, in plain code: bills from any payee, subscriptions the owner didn't cancel, and what The Machine learned
that is about no one in the Graph. Never a calendar event: an appointment alone is a date, not a line of the owner's
history (section_notes.py).
Health is always Personal, whatever the account it came in on: a doctor's bill sent to a work address is still the
owner's own. The notes are never shared.

Conversations too (topic_notes.py): a mail thread or chat with a practice, a hospital, a lab or the health insurer is
a line of the part it is about, opening its newest message: the owner's medical history over time, from what their
care wrote."""
import section_notes

# The parts of the owner's health a candidate can be about, each a note under Health (English: its key; titled in the
# owner's language through i18n)
SECTIONS = ('Appointments', 'Test results', 'Doctors and care', 'Medicines', 'Allergies and conditions', 'Bills and insurance')
PARTS = {
    'Test results': 'a test, scan or lab result, a diagnosis, a doctor\'s or hospital\'s report',
    'Appointments': 'a visit to a doctor, dentist, physiotherapist, therapist, optician, a test or a vaccination',
    'Doctors and care': 'who takes care of the owner\'s health: their doctor, dentist, practice or hospital, and how to reach them',
    'Medicines': 'a medicine or supplement the owner takes, a prescription, a pharmacy',
    'Allergies and conditions': 'an allergy, a condition, a blood type, something a doctor or nurse should know',
    'Bills and insurance': 'a bill or subscription for care: a doctor, dentist, hospital or pharmacy bill, health insurance',
}


def candidates(db, accounts, today):
    return [*section_notes.bills(db, accounts, today, personal=False),
            *section_notes.subscriptions(db, accounts, personal=False), *section_notes.facts(db, accounts, personal=False)]


KIND = section_notes.Kind(
    'health', 'Health', SECTIONS, PARTS, 'the owner\'s own health',
    'the home, work, a hobby or a sport, a trip, a meeting, someone else\'s health, like a child\'s or a parent\'s',
    candidates, section_notes.ask, section_notes.line)
