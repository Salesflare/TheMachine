"""The standing eval (tests/knowledge_eval.py): every surface answers "who is X", "latest messages with X", "what is
open with X", "when did I last talk to X", "what did we say about Y" and "what did I decide about Z before" with the same records,
under the same rules.

GAPS lists the answers a surface still gets wrong until it moves onto knowledge.py; each move removes its lines. A gap
that starts passing fails here too, so the list only ever shrinks."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT))
import knowledge_eval  # noqa: E402

GAPS = {
    ('who: by phone number "0470 00 01 02"', 'chat'),
    ('who: by phone number "0470 00 01 02"', 'mcp'), ('who: by phone number "0470 00 01 02"', 'page'),
    ('who: by phone number "0470 00 01 02"', 'search'),
    ('who: by phone number "0032470000102"', 'chat'),
    ('who: by phone number "0032470000102"', 'mcp'), ('who: by phone number "0032470000102"', 'page'),
    ('who: by phone number "0032470000102"', 'search'),
    ("open: an organization has its people's promises", 'chat'),
    ("open: an organization has its people's promises", 'mcp'), ("open: an organization has its people's promises", 'page'),
}


class Eval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        config, ids = knowledge_eval.sandbox(cls.temp.name)
        import assistant
        cls.results = knowledge_eval.run(knowledge_eval.with_memory(knowledge_eval.app_for(config, assistant)), assistant, ids)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_every_surface_gives_the_same_answers(self):
        failed = {(name, surface): detail for name, surface, ok, detail in self.results if not ok}
        self.assertEqual({k: v for k, v in failed.items() if k not in GAPS}, {}, 'answers a surface got wrong')
        self.assertEqual(GAPS - set(failed), set(), 'these pass now: take them out of GAPS')

    def test_the_layer_and_every_surface_are_asked(self):
        asked = {surface for _, surface, _, _ in self.results}
        self.assertEqual(asked, set(knowledge_eval.SURFACES))
        self.assertTrue(all(ok for _, surface, ok, _ in self.results if surface == 'layer'))


if __name__ == '__main__':
    unittest.main()
