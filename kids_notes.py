"""Kids notes (docs/notes.md, "Kids"): what the owner's Machine knows about the owner's children and their
school, in a few notes under Kids, kept the way every kind in sections is (section_notes.py: one small model call over
what is new only, the owner's own notes in a part filled in, a part only from two lines).

Each line points to where the thing lives instead of copying it: a bill's opens its to-do and mail (its amount and
payment details stay there), a line from what The Machine learned is that fact, and links the child it is about.

Candidates, in plain code: what was learned about one of the owner's children (people in the Graph whose role to the
owner says so, section_notes.children) or about no one, bills from any payee and subscriptions the owner didn't
cancel. Never a calendar event: a lesson or a babysitter's evening alone is a date, not what the school or a club told
the owner (section_notes.py). Kids is always
Personal, whatever the account it came in on: a school's mail to a work address is still about the owner's own child.
A note the owner keeps for one child in a part (Isla under School) gets what is about that child. The notes are
never shared.

Conversations too (topic_notes.py): a mail thread or chat with the school, a club or childcare is a line of the part
it is about, opening its newest message: everything the school sends, in one place."""
import section_notes

# The parts of the children's lives a candidate can be about, each a note under Kids (English: its key; titled in the
# owner's language through i18n)
SECTIONS = ('School', 'Activities', 'Childcare', 'Doctors and care', 'Bills and fees')
PARTS = {
    'School': 'a child\'s school, class, teacher, the school\'s newsletters, school days, holidays, trips, what to bring, '
              'parents\' evenings, homework or report',
    'Activities': 'a child\'s sport, music, club, camp or lesson, its days and who runs it',
    'Childcare': 'who looks after a child: a babysitter, daycare, after-school care, a day without care at school',
    'Doctors and care': 'a child\'s health only: their doctor, dentist, allergy, medicine or a result, never a babysitter '
                        'or childcare',
    'Bills and fees': 'a bill or subscription for a child: school fees, a club or camp fee, childcare, lessons',
}


def candidates(db, accounts, today):
    return [*section_notes.child_facts(db), *section_notes.bills(db, accounts, today, personal=False), *section_notes.subscriptions(db, accounts, personal=False),
            *section_notes.facts(db, accounts, personal=False)]


KIND = section_notes.Kind(
    'kids', 'Kids', SECTIONS, PARTS, 'the owner\'s children and their school',
    'the owner\'s own health or work, the home, a trip, a meeting, someone else\'s child',
    candidates, section_notes.ask, section_notes.line)
