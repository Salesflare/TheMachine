"""The one way a prompt reads memory (memory_use.py has the shape and the log).

recall(app, purpose, about, budget) gives a prompt builder the memory of its purpose as named blocks. Each block is
one of the existing pickers, unchanged: the builder asks for a block's text where it used to call the picker, so the
prompt is the same text in the same order. What each picker put in is kept as items of one shape (memory_use.Item),
and Recalled.rows() is what the builder logs once its run is admitted (memory_use.record).

A new reader of memory is a block here, not another call in a builder: the builder then gets its text, its items and
its log line the same way as the rest."""
import embeddings
import memory_use
import search_ask
from machine.app import ask_memory
from machine.app import senders


def recall(app, purpose, about=None, budget=0):
    """The memory for one prompt. purpose: review, preparation, ask, talk or chat. about: what it is for
    ({'todo': id}, {'run': id}, {'run': id, 'analysis': id} for the batch a review claimed, {'question': text}). budget: the prompt's character limit,
    for Recalled.fit. Returns a memory_use.Recalled: text(block) or fit(block, used, reserve) for the prompt,
    picked() for the items per kind, rows() for the log.

    Blocks by purpose:
    - review: history (what the owner did with the last 30 days' to-dos), facts (all learned, with ids), promises
      (the open ones), sender (who wrote the claimed batch: one line per sender the Graph knows something specific
      about, senders.lines; read when the batch is claimed, with the claim's reply as its budget).
    - preparation: rules and facts (for this to-do), records (the people and projects on it), skills(rules, room),
      team (the Work Fleet's lines, team learnings among them), related (signals close in meaning).
    - ask: sources (search_ask.ask with its own arguments: the messages that fit the prompt), and what matches the
      question of promises, facts, records (a person's summary, a named project or organization) and meetings
      (machine/app/ask_memory.py, each with (what it goes on, room)).
    - talk, chat: none yet; they read no memory of their own today."""
    about = dict(about or {})
    memory = memory_use.Recalled(purpose, about, budget)
    store, todo = app.store, about.get('todo')
    if purpose == 'review':
        memory.add('history', lambda: store.preference_summary())
        memory.add('facts', lambda: store.facts_text(ids=True))
        memory.add('promises', lambda: store.promises_text())
        memory.add('sender', lambda: senders.lines(app, about.get('analysis')))
    elif purpose == 'preparation':
        known = embeddings.settings(app.config)  # what was learned that this to-do needs, not all of it
        memory.add('rules', lambda: store.facts_for(todo, 'draft', known))
        memory.add('facts', lambda: store.facts_for(todo, 'fact', known, accounts=app.config.get('accounts', [])))
        memory.add('records', lambda: app.graph_lines(todo))
        memory.add('skills', lambda rules, room: app.prep_skill_lines(todo, rules, room))
        memory.add('team', lambda: app.fleet.lines(todo))
        memory.add('related', lambda: app.related_lines(todo))
    elif purpose == 'ask':
        memory.add('sources', search_ask.ask)
        ask_memory.add(memory, app)
    return memory
