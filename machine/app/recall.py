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
from machine.app import retained_facts
from machine.app import senders
from machine.app.review_facts import ReviewFacts

# A routine's run gets what was learned, said or used most lately first, in this many characters: about 300 and 150
# tokens. Everything learned is in a review; a routine is one read-only turn, often daily, so it gets the front of it.
ROUTINE_FACTS = 1200
ROUTINE_RULES = 600


def recall(app, purpose, about=None, budget=0):
    """The memory for one prompt. purpose: review, preparation, ask, routine, talk, chat or todo_chat. about: what it is for
    ({'todo': id}, {'run': id}, {'run': id, 'analysis': id} for the batch a review claimed, {'question': text}). budget: the prompt's character limit,
    for Recalled.fit. Returns a memory_use.Recalled: text(block) or fit(block, used, reserve) for the prompt,
    picked() for the items per kind, rows() for the log.

    Blocks by purpose:
    - review: history (what the owner did with the last 30 days' to-dos), facts (all learned, with ids, while they
      fit; past the cap the standing ones) and batch_facts (past the cap: the ones picked for this batch,
      review_facts.py), promises (the open ones), sender (who wrote the claimed batch: one line per sender the Graph
      knows something specific about, senders.lines; read when the batch is claimed, with the claim's reply as its
      budget), retained (set-aside facts and history that bear on the waiting signals, retained_facts.py).
    - preparation: rules and facts (for this to-do), retained (set-aside facts and history that bear on it), records (the people and projects on it), skills(rules, room),
      team (the Work Fleet's lines, team learnings among them), related (signals close in meaning).
    - ask: sources (search_ask.ask with its own arguments: the messages that fit the prompt), and what matches the
      question of promises, facts, records (a person's summary, a named project or organization) and meetings
      (machine/app/ask_memory.py, each with (what it goes on, room)).
    - routine: facts and rules (what was learned and the draft rules, said or used most lately first, up to
      ROUTINE_FACTS and ROUTINE_RULES characters), so a run and the draft it may leave follow them.
    - talk: facts(words) for its recall tool: the owner's own facts and rules that share the words
      (ask_memory.learned, plain word matching), next to OpenClaw's memory search.
    - chat: none yet; the owner's main chat reads no memory through here (docs/memory-reach.md).
    - todo_chat (a turn of a to-do's chat, {'todo': id}): retained, as for its preparation, in a smaller slice;
      the rest of what was learned is in the session from its preparation."""
    about = dict(about or {})
    memory = memory_use.Recalled(purpose, about, budget)
    store, todo = app.store, about.get('todo')
    if purpose == 'review':
        memory.add('history', lambda: store.preference_summary())
        facts = ReviewFacts(app)  # all of them while they fit; else the standing ones, and the batch's own after them
        memory.add('facts', facts.standing)
        memory.add('batch_facts', facts.for_batch)
        memory.add('promises', lambda: store.promises_text())
        memory.add('sender', lambda: senders.lines(app, about.get('analysis')))
        memory.add('retained', lambda: retained_facts.for_review(app))
    elif purpose == 'preparation':
        known = embeddings.settings(app.config)  # what was learned that this to-do needs, not all of it
        memory.add('rules', lambda: store.facts_for(todo, 'draft', known))
        memory.add('facts', lambda: store.facts_for(todo, 'fact', known, accounts=app.config.get('accounts', [])))
        memory.add('retained', lambda: retained_facts.for_todo(app, todo))
        # a fact about a record on the to-do is in the facts block (picked by record): the record's line doesn't say it again
        memory.add('records', lambda: app.graph_lines(todo, {int(i.row_id) for i in memory.blocks.get('facts', ()) if i.kind == 'fact'}))
        memory.add('skills', lambda rules, room: app.prep_skill_lines(todo, rules, room))
        memory.add('team', lambda: app.fleet.lines(todo))
        memory.add('related', lambda: app.related_lines(todo))
    elif purpose == 'todo_chat':
        memory.add('retained', lambda: retained_facts.for_todo(app, todo, retained_facts.CHAT_CHARS))
    elif purpose == 'ask':
        memory.add('sources', search_ask.ask)
        ask_memory.add(memory, app)
    elif purpose == 'routine':
        memory.add('facts', lambda: store.facts_text(ROUTINE_FACTS))
        memory.add('rules', lambda: store.facts_text(ROUTINE_RULES, 'draft'))
    elif purpose == 'talk':
        memory.add('facts', lambda words: ask_memory.learned(store, words))
    return memory
