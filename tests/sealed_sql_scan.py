"""Finds SQL in the source that reads a sealed JSON column by a key that is not kept in the clear.

On a Machine with message protection on (the default), `events.metadata` keeps only message_seal.PLAIN_METADATA
readable to SQLite, and the columns of message_seal.DERIVED_JSON only their named keys. Every other key sits inside
the sealed member: `json_extract(metadata,'$.cc')` is NULL there and `metadata LIKE '%x%'` never matches it, while the
same row read through the store's connection opens and Python sees everything. Such a statement fails silently, on
sealed Machines only. tests/test_message_seal.py (NothingOutsideTheSealedFields) runs `reads` over the source.

What it reads: every string in every source module (an f-string's fixed parts joined, each slot as SLOT), and the
other strings of the same statement to tell which table a column belongs to. What it cannot read is in the test.
"""
import ast
import re

import message_seal

SLOT = '\x00'  # where an f-string puts a value in
JSON_CALL = re.compile(r'\bjson_(?:extract|each|tree|type|array_length)\s*\(', re.I)
DIRECT = r'^\s*(?:(?:COALESCE|IFNULL|NULLIF)\s*\(\s*)?(?:(\w+)\.|\x00\.?)?(%s)\b(?!\s*\()'  # the column itself, not a call that already read a key of it
# A Gmail label looked up in the column's text, like instr(metadata,'"SENT"'): labels are kept in the clear
LABEL = re.compile(r"""\s*,\s*'"[A-Z_]+"'\s*\)""")
WORD = r'(?:\b(\w+)\.)?\b(%s)\b(?!\s*\()'
PATH = re.compile(r"""^\s*(['"])\$(?:\.(\w+)|\.?"([^"]+)"|\[)""")


def strings(tree):
    """(line, text, context) for every string in a module: `context` is all the text of the statement it is in."""
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            text = ''.join(v.value if isinstance(v, ast.Constant) else SLOT for v in node.values)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and not isinstance(parents.get(node), ast.JoinedStr):
            text = node.value
        else:
            continue
        found.append((node, text))
    by_statement = {}
    for node, text in found:
        by_statement.setdefault(_statement(node, parents), []).append(text)
    return [(node.lineno, text, ' '.join(by_statement[_statement(node, parents)])) for node, text in found]


def _statement(node, parents):
    """The statement a string is in; for one in the header of a `for`, `with` or `if`, the header only."""
    while node in parents and not isinstance(node, ast.stmt):
        child, node = node, parents[node]
        if isinstance(node, ast.stmt) and hasattr(node, 'body') and not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            return child  # the header's expression: the body's strings belong to their own statements
    return node


def _arguments(text, start):
    """The top-level arguments of the call whose opening bracket is just before `start`."""
    depth, quote, parts, begin, i = 0, '', [], start, start
    while i < len(text):
        c = text[i]
        if quote:
            quote = '' if c == quote else quote
        elif c in '\'"':
            quote = c
        elif c == '(':
            depth += 1
        elif c == ')':
            if not depth:
                return parts + [text[begin:i]]
            depth -= 1
        elif c == ',' and not depth:
            parts.append(text[begin:i])
            begin = i + 1
        i += 1
    return parts + [text[begin:]]


def owner(prefix, column, context, sealed_table, others):
    """Whether `column` (written as prefix.column) is the sealed table's here. `others`: other tables with a column of
    that name. In doubt it is: a read that cannot be placed is checked, not passed."""
    if prefix:
        if prefix == sealed_table:
            return True
        if prefix in others:
            return False
        named = {t for t in others | {sealed_table} if re.search(rf'\b{t}\s+(?:AS\s+)?{prefix}\b', context, re.I)}
        if named:
            return sealed_table in named
    here = {t for t in others | {sealed_table} if re.search(rf'\b{t}\b', context)}
    return sealed_table in here or not here


def reads(text, context, columns, tables):
    """Reads in `text` of a sealed JSON column that SQL cannot answer on a sealed database.

    `columns`: {column name: (table, plain keys)}; `tables`: {column name: the other tables that have such a column}.
    Returns [(table.column, what)]: `what` is 'key <name>' for a key that is not plain, 'key ?' for a path only known
    at run time, 'whole' for all of the object, 'text' for a search or comparison of the column's text; and
    ('?', 'column ?') for a JSON read of a column only named at run time, which may be one of these.
    """
    if not any(c in text for c in columns) and SLOT not in text:
        return []
    names = '|'.join(columns)
    direct = re.compile(DIRECT % names, re.I)
    out = []

    def mine(prefix, column):
        return owner(prefix, column, context, columns[column][0], tables.get(column, set()))

    def key(column, path):
        found = PATH.match(path)
        if not found:
            return 'key ?'
        name = found[2] or found[3]
        if name == message_seal.SEALED_KEY:  # the sealed member itself: SQL sees that it is there (a row with hidden keys)
            return None
        return None if name in columns[column][1] else f'key {name}' if name else 'whole'

    for call in JSON_CALL.finditer(text):
        args = _arguments(text, call.end())
        first = direct.match(args[0])
        if first and mine(*first.groups()):
            out += [(first[2], key(first[2], p)) for p in args[1:]] or [(first[2], 'whole')]
        elif re.fullmatch(r'\s*(?:\w+\.|\x00\.?)?\x00\s*', args[0]):
            out.append((None, 'column ?'))
    for found in re.finditer(WORD % names + r"""\s*->>?\s*(\S+)""", text):
        prefix, column, path = found.groups()
        if mine(prefix, column):
            name = re.match(r"""['"](?:\$\.)?(\w+)""", path)
            out.append((column, 'key ?' if not name else None if name[1] in columns[column][1] else f'key {name[1]}'))
    text_reads = (r'(?:%s)\s+(?:NOT\s+)?(?:LIKE|GLOB|REGEXP|MATCH)\b' % (WORD % names),
                  r'\b(?:instr|lower|upper|substr|length|replace|trim)\s*\(\s*(?:COALESCE\s*\(\s*)?%s' % (WORD % names),
                  r'\b(?:LIKE|GLOB)\s+%s' % (WORD % names),
                  r'(?:WHERE|AND|OR|ON|WHEN)\s+\(*\s*%s\s*(?:=|!=|<>|<|>|\bIN\b|\bIS\b)' % (WORD % names))
    for pattern in text_reads:
        for found in re.finditer(pattern, text, re.I):
            prefix, column = found.group(1), found.group(2)
            if mine(prefix, column) and not re.match(r'\s*IS\s+(?:NOT\s+)?NULL', text[found.end() - 2:], re.I) and not LABEL.match(text, found.end()):
                out.append((column, 'text'))
    return [(f'{columns[c][0]}.{c}' if c else '?', what) for c, what in out if what]


def scan(paths, root, columns, tables):
    """{(file, table.column, what): [lines]} over the source files in `paths`."""
    found = {}
    for path in paths:
        source = path.read_text(encoding='utf-8')
        for line, text, context in strings(ast.parse(source)):
            for column, what in reads(text, context, columns, tables):
                found.setdefault((path.relative_to(root).as_posix(), column, what), []).append(line)
    return found
