"""Home notes (docs/notes.md, "Home"): what the owner's Machine knows about their home, in a few notes under Home,
kept the way every kind in sections is (section_notes.py: one small model call over what is new only, the owner's own
notes in a part filled in, a part only from two lines).

Each line points to where the thing lives instead of copying it. A bill's line names the payee, how often its bills
came and when the last one did, and opens that bill's to-do and mail (its amount and payment details stay on the
to-do). A subscription's line opens its Subscriptions to-do. A line from what The Machine learned is that fact: editing
it edits the fact (note_pages_app.py).

Candidates, in plain code: a payee that sent the owner two or more Personal bills within section_notes.LOOK_DAYS
(bill to-dos, Store.set_bill), a Personal subscription the owner didn't cancel (subscriptions.py), and what The
Machine learned that is about no one in the Graph (not a passing event, not on the Work side). Home is always
Personal.

Conversations too (topic_notes.py): a mail thread or chat about the home, like the landlord's, the energy supplier's
or a plumber's, is a line of the part it is about, opening its newest message. That is how a Home fills when the owner
pays by direct debit and no bill ever became a to-do."""
import section_notes

# The parts of the home a candidate can be about, each a note under Home (English: its key; titled in the owner's
# language through i18n)
SECTIONS = ('Bills and subscriptions', 'Appliances', 'Repairs and upkeep', 'The house')
PARTS = {
    'Bills and subscriptions': 'a bill, contract or subscription for the home itself: rent or mortgage, energy, water, home insurance, '
                               'internet, the municipality\'s taxes or waste collection, a home service',
    'Appliances': 'a device in the home: its make, model, warranty or manual',
    'Repairs and upkeep': 'work done on the home or who does it: a plumber, a boiler service, cleaning, the garden',
    'The house': 'the home itself: rooms, how things work there, codes, what is where',
}
MIN_BILLS = 2  # bills from one payee before it is a regular one


def candidates(db, accounts, today):
    return [*section_notes.bills(db, accounts, today, least=MIN_BILLS), *section_notes.subscriptions(db, accounts),
            *section_notes.facts(db, accounts)]


KIND = section_notes.Kind(
    'home', 'Home', SECTIONS, PARTS, 'the owner\'s own home',
    'work, a person, health, a child\'s school, a hobby, a trip, a subscription for one person\'s own use',
    candidates, section_notes.ask, section_notes.line)
