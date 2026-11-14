"""An error whose message is for the owner: it says what happened or what to do, in plain words, and the dashboard
shows it as it is (translated through the catalog, i18n/). A leaf: it imports nothing, so any module can raise it.

Any other ValueError that reaches the dashboard is a bug or a request the page shouldn't have sent: its text (such as
a JSON decode error) isn't for the owner. machine/web/handler.py logs those and counts them for the error reports
(error_feed.py). scripts/i18n_extract.py reads every OwnerError message for the catalog.

It is a ValueError, so every `except ValueError` still catches it."""


class OwnerError(ValueError):
    """A message for the owner, such as "Handing off to Claude Code or Codex is off on this Machine"."""
