"""Model bias corrections: short lines that counter a habit of today's models, kept here, apart from the prompts that
include them, so they are easy to change or drop when models change (docs/development.md, Model bias corrections).

PLAIN_WRITING: models lean toward long, elaborate, formal text (greetings, thanks, a recap of the message, bullet
lists), and a tester rewrote drafts that were "too complex" before sending them (2026-11-17). It is the default bias
correction for text the owner sends or approves; how the owner writes (their voice per channel, their own messages and
edits, USER.md) still wins where it differs. Drafts get it from preparation_prompt (Do it, prepared ahead, follow-ups,
Ask for changes, which carry on in that session) and from a routine run that leaves a draft."""
import re

PLAIN_WRITING = ("Write drafts plainly: short sentences, everyday words, only what the reader needs. No filler, pleasantries or "
                 "recap of their message, and no bullet lists or headings unless the owner writes that way. About as long as the "
                 "message it answers. How the owner writes (their voice, messages and edits below) wins where it differs.")

# Which model families get it, from a before/after eval on made-up mails (2026-11-17, in the pull request that added
# it): on where a family's drafts came out long or formal without it. A family not listed gets DEFAULT.
PLAIN_WRITING_FOR = {'gpt': True, 'claude': True}
DEFAULT = True

FAMILIES = ('gpt', 'claude', 'mistral', 'glm', 'kimi', 'deepseek', 'gemini', 'llama', 'qwen')


def family(model):
    """A model's family from its id ('openai/gpt-6.1-sol' -> 'gpt', 'claude-cli/claude-opus-5-5' -> 'claude'), or None."""
    name = str(model or '').rsplit('/', 1)[-1].lower()
    return next((f for f in FAMILIES if re.match(rf'{f}\b|{f}[-.\d]', name)), None)


def plain_writing(model=None):
    """PLAIN_WRITING when the model's family gets it (an unknown or missing model: DEFAULT), else ''."""
    return PLAIN_WRITING if PLAIN_WRITING_FOR.get(family(model), DEFAULT) else ''
