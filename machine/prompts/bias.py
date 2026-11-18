"""Model bias corrections: short lines that counter a habit of today's models, kept here, apart from the prompts that
include them, so they are easy to change or drop when models change (docs/development.md, Model bias corrections).

PLAIN_WRITING: models lean toward long, elaborate, formal text (greetings, thanks, a recap of the message, bullet
lists), and a tester rewrote drafts that were "too complex" before sending them (2026-11-17). It is the default bias
correction for text the owner sends or approves; how the owner writes (their voice per channel, their own messages and
edits, USER.md) still wins where it differs. Drafts get it from preparation_prompt (Do it, prepared ahead, follow-ups,
Ask for changes, which carry on in that session) and from a routine run that leaves a draft.

A model's own line (model_note, keyed by its name in PLAIN_WRITING_FOR) also goes into meeting briefs."""
import re

PLAIN_WRITING = ("Write drafts plainly and friendly: short sentences, everyday words, only what the reader needs; short, not blunt. "
                 "Keep a greeting and a short sign-off where the channel and their message have them (an email: yes; a chat: none "
                 "needed). No filler, recap of their message, bullet lists or headings unless the owner writes that way. About as "
                 "long as the message it answers. How the owner writes (their voice, messages and edits below) wins where it differs.")

# GPT-6.2 Sol, on top of its family's: an eval against GPT-6.1 Sol on made-up meetings and mails (2026-11-18, in the
# pull request that added it) found its meeting briefs about a quarter longer, and once it guessed a guest's gender
# from their name. Its drafts and meeting briefs get this line (model_note).
GPT_62_SOL = ("Keep it shorter than feels natural: every line well under its limit, only what helps. Never assume a "
              "person's gender from their name: use their name or they/them.")

# Which model families get it, from a before/after eval on made-up mails (2026-11-17, in the pull request that added
# it): on where a family's drafts came out long or formal without it. A family not listed gets DEFAULT. A model's own
# name (without its provider) may have a line of its own too, which its drafts and meeting briefs get besides.
PLAIN_WRITING_FOR = {'gpt': True, 'claude': True, 'gpt-6.2-sol': GPT_62_SOL}
DEFAULT = True

FAMILIES = ('gpt', 'claude', 'mistral', 'glm', 'kimi', 'deepseek', 'gemini', 'llama', 'qwen')


def family(model):
    """A model's family from its id ('openai/gpt-6.1-sol' -> 'gpt', 'claude-cli/claude-opus-5-5' -> 'claude'), or None."""
    name = str(model or '').rsplit('/', 1)[-1].lower()
    return next((f for f in FAMILIES if re.match(rf'{f}\b|{f}[-.\d]', name)), None)


def model_note(model=None):
    """The model's own line in PLAIN_WRITING_FOR (by its name, without provider), or ''."""
    note = PLAIN_WRITING_FOR.get(str(model or '').rsplit('/', 1)[-1].lower())
    return note if isinstance(note, str) else ''


def plain_writing(model=None):
    """PLAIN_WRITING when the model's family gets it (an unknown or missing model: DEFAULT), then the model's own line
    (model_note); '' when neither."""
    plain = PLAIN_WRITING if PLAIN_WRITING_FOR.get(family(model), DEFAULT) else ''
    return ' '.join(part for part in (plain, model_note(model)) if part)
