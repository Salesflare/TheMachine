"""Health notes (docs/help/notes.md, "Health"): what the owner's Machine knows about the owner's own health, in a few
notes under Health, kept the way every kind in sections is (section_notes.py: one small model call over what is new
only, the owner's own notes in a part filled in, a part only from two lines).

Each line points to where the thing lives instead of copying it: an appointment's line opens it in the calendar, a
bill's opens its to-do and mail (its amount and payment details stay there), a line from what The Machine learned is
that fact.

Candidates, in plain code: appointments (calendar events only the owner is on, section_notes.own_events), bills from
any payee, subscriptions the owner didn't cancel, and what The Machine learned that is about no one in the Graph.
Health is always Personal, whatever the account it came in on: a doctor's bill sent to a work address is still the
owner's own. The notes are never shared."""
import section_notes

# The parts of the owner's health a candidate can be about, each a note under Health (English: its key; titled in the
# owner's language through i18n)
SECTIONS = ('Appointments', 'Doctors and care', 'Medicines', 'Allergies and conditions', 'Bills and insurance')
PARTS = {
    'Appointments': 'a visit to a doctor, dentist, physiotherapist, therapist, optician, a test or a vaccination',
    'Doctors and care': 'who takes care of the owner\'s health: their doctor, dentist, practice or hospital, and how to reach them',
    'Medicines': 'a medicine or supplement the owner takes, a prescription, a pharmacy',
    'Allergies and conditions': 'an allergy, a condition, a blood type, something a doctor or nurse should know',
    'Bills and insurance': 'a bill or subscription for care: a doctor, dentist, hospital or pharmacy bill, health insurance',
}


def candidates(db, accounts, today):
    return [*section_notes.own_events(db, accounts, today), *section_notes.bills(db, accounts, today, personal=False),
            *section_notes.subscriptions(db, accounts, personal=False), *section_notes.facts(db, accounts, personal=False)]


KIND = section_notes.Kind(
    'health', 'Health', SECTIONS, PARTS, 'the owner\'s own health',
    'the home, work, a hobby or a sport, a trip, a meeting, someone else\'s health, like a child\'s or a parent\'s',
    candidates, section_notes.ask, section_notes.line)
