"""do_GET's routes (machine/web/handler.py): an exact path goes to its method through GET_ROUTES, the patterns (the
browser's viewer, the scripts, the i18n catalogs) stay branches of do_GET. A table answers the way the old if/elif
chain did only while no path is in it twice and no exact path is also one of the patterns."""
import ast
from pathlib import Path
import re
import sys
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import ai_access  # noqa: E402
from machine.config import BRAND_ASSETS  # noqa: E402
from machine.web.handler import make_handler  # noqa: E402
from machine.web.serving import SCRIPT_NAME  # noqa: E402

APP = SimpleNamespace(config={})  # what the class itself reads of its App
I18N = re.compile(r'/i18n/[a-z]{2}(?:-[A-Z]{2})?\.json')


def listed_paths():
    # GET_ROUTES's keys as written, so a path listed twice (the later one would win) shows
    tree = ast.parse((ROOT / 'machine' / 'web' / 'handler.py').read_text(encoding='utf-8'))
    table = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                 and any(getattr(t, 'id', '') == 'GET_ROUTES' for t in n.targets))
    paths = []
    for key in table.keys:
        if key is None:  # **dict.fromkeys(BRAND_ASSETS, ...)
            paths += list(BRAND_ASSETS)
        elif isinstance(key, ast.Constant):
            paths.append(key.value)
        else:
            spelled = ast.unparse(key)
            assert spelled == 'ai_access.AUTHORIZE', spelled
            paths.append(ai_access.AUTHORIZE)
    return paths


class GetRoutes(unittest.TestCase):
    def test_each_route_has_its_method(self):
        handler = make_handler(APP)
        for path, method in handler.GET_ROUTES.items():
            with self.subTest(path=path):
                self.assertTrue(callable(getattr(handler, method, None)), f'{path}: Handler has no {method}')

    def test_no_path_is_listed_twice(self):
        paths = listed_paths()
        self.assertEqual(sorted({p for p in paths if paths.count(p) > 1}), [])
        self.assertEqual(set(paths), set(make_handler(APP).GET_ROUTES))

    def test_no_route_is_also_a_pattern(self):
        self.assertIn(I18N.pattern, (ROOT / 'machine' / 'web' / 'handler.py').read_text(encoding='utf-8'))  # do_GET's own
        for path in make_handler(APP).GET_ROUTES:
            with self.subTest(path=path):
                self.assertFalse(path == '/browser' or path.startswith('/browser/'))
                self.assertIsNone(SCRIPT_NAME.fullmatch(path))
                self.assertIsNone(I18N.fullmatch(path))


if __name__ == '__main__':
    unittest.main()
