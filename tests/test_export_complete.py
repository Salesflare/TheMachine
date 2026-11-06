"""An export stays complete over time (machine/export/inventory.py): every table the code creates, every folder under
the home folder it writes to, and every file a full install keeps has a part in the export or a reason why not.

A new table, data folder or home path fails here until it is added to the inventory (TABLES, DATA_FILES, HOME_AREAS)
or listed with its reason (NOT_EXPORTED_HOME, HOME_OTHER)."""
import fnmatch
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from machine.export import inventory  # noqa: E402

CREATE = re.compile(r'\bCREATE\s+(?:VIRTUAL\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`\[]?([A-Za-z_]\w*)["`\]]?\s*\(')
VIRTUAL = re.compile(r'\bCREATE\s+VIRTUAL\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_]\w*)\s+USING')
HOME = re.compile(r"Path\.home\(\)\s*/\s*['\"]([^'\"]+)['\"](?:\s*/\s*['\"]([^'\"]+)['\"])?")
SKIP = {'tests', 'node_modules', '.git', 'sandbox', 'scripts'}


def sources():
    for path in sorted(ROOT.rglob('*.py')):
        if not SKIP & set(path.relative_to(ROOT).parts):
            yield path, path.read_text(encoding='utf-8', errors='replace')


def created_tables():
    found = {}
    for path, text in sources():
        for pattern in (CREATE, VIRTUAL):
            for match in pattern.finditer(text):
                found.setdefault(match.group(1), set()).add(str(path.relative_to(ROOT)))
    return found


def home_paths():
    found = {}
    for path, text in sources():
        for match in HOME.finditer(text):
            found.setdefault('/'.join(p for p in match.groups() if p), set()).add(str(path.relative_to(ROOT)))
    return found


def covered(path):
    """Whether a path under the home folder is exported (HOME_AREAS, and what is in them) or has a reason
    (NOT_EXPORTED_HOME, and what is in them; HOME_OTHER, only by its own name)."""
    if path in inventory.HOME_OTHER or path == inventory.DATA_HOME or path.startswith(inventory.DATA_HOME + '/'):
        return True  # HOME_OTHER by its own name only, never what sits under it
    patterns = [p for p, _, _ in inventory.HOME_AREAS] + [p for p, _ in inventory.NOT_EXPORTED_HOME]
    return any(path == p or fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path, p + '/*') for p in patterns)


class ExportComplete(unittest.TestCase):
    def test_every_table_the_code_creates_has_a_part(self):
        missing = {name: where for name, where in created_tables().items() if name not in inventory.TABLES}
        self.assertEqual({}, missing, 'add these tables to machine/export/inventory.py (_BY_PART), so an export lists them')

    def test_every_part_names_tables_that_exist(self):
        made = created_tables()
        stale = sorted(name for name in inventory.TABLES if name not in made)
        self.assertEqual([], stale, 'these tables are in the inventory but no code creates them any more')

    def test_parts_have_labels(self):
        self.assertEqual(set(), set(inventory.TABLES.values()) - set(inventory.PARTS))
        self.assertEqual(set(), {part for _, part, _ in inventory.HOME_AREAS} - set(inventory.PARTS))
        self.assertEqual(set(), set(inventory.DATA_FILES.values()) - set(inventory.PARTS))

    def test_every_home_path_is_exported_or_has_a_reason(self):
        missing = {path: where for path, where in home_paths().items() if not covered(path)}
        self.assertEqual({}, missing, 'add these to inventory.HOME_AREAS (exported) or HOME_OTHER / NOT_EXPORTED_HOME (with why)')

    def test_what_cannot_move_says_why(self):
        for item in inventory.NOT_EXPORTED:
            self.assertTrue(item['what'] and item['why'], item)
        for path, why in inventory.NOT_EXPORTED_HOME:
            self.assertTrue(why, path)

    def test_the_check_itself_notices_a_new_table_and_path(self):
        self.assertEqual(['brand_new_things'], [m.group(1) for m in CREATE.finditer('CREATE TABLE IF NOT EXISTS brand_new_things(id INTEGER)')])
        self.assertFalse(covered('.local/share/brand-new-store'))
        self.assertTrue(covered('.openclaw/agents/main/sessions'))


if __name__ == '__main__':
    unittest.main()
