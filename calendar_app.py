"""The Calendar's actions, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

New event and edit (calendar_write), a meeting's notes (meeting_notes) and Generate notes (meeting_notes_write). The
methods they call (calendar_write, meeting_notes, meeting_write and its worker) stay in assistant.py for now: they use
the hours, model and source helpers (now, local_tz, has_model, gog_read, ...), which move out of assistant.py first."""


class CalendarApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'calendar_write': 'calendar_write_action',
        'meeting_notes': 'meeting_notes_action',
        'meeting_notes_write': 'meeting_notes_write_action',
    }

    def calendar_write_action(self, name, args, owner_dashboard):
        # the Calendar's New event and edit form: the owner's own tap, from the dashboard only
        if not owner_dashboard:
            raise ValueError('Calendar changes come from your tap in the dashboard')
        return self.calendar_write(args)

    def meeting_notes_action(self, name, args, owner_dashboard):
        return self.meeting_notes(args, owner_dashboard)

    def meeting_notes_write_action(self, name, args, owner_dashboard):
        # Generate notes on a meeting in the Calendar (meeting_writer.py)
        if not owner_dashboard:
            raise ValueError('Only the owner asks for notes to be written, in the Calendar')
        return self.meeting_write(args)
