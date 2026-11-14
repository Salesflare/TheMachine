"""The Delivery list on Connections, Checks: every status the deliveries table takes shows a label in the owner's
language, never its raw key ("not_sent")."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDER = ROOT / 'dashboard' / 'shell-render.js'
CATALOGS = sorted(p for p in (ROOT / 'i18n').glob('*.json') if p.name != 'not-ui.json')  # each language, new ones too
# Statuses written through a variable, not a literal: store/cards.py (previewed, not_sent, queued) and
# delivery/deliver.py (sent, queued, uncertain).
WRITTEN_FROM_VARIABLES = {'previewed', 'not_sent', 'queued', 'sent', 'uncertain'}


def labels():
    source = RENDER.read_text(encoding='utf-8')
    found = re.search(r'const DELIVERY_LABEL=\{(.*?)\};', source)
    return dict(re.findall(r"(\w+):'([^']*)'", found[1]))


def written_statuses():
    """Every delivery status a literal in the app's Python writes or matches: SET status='x', VALUES(?,'x',...),
    status IN ('x','y') on a statement about the deliveries table (a to-do's own s.status is left out)."""
    statuses = set()
    for path in ROOT.rglob('*.py'):
        if {'tests', '.git', 'node_modules'} & set(path.relative_to(ROOT).parts):
            continue
        for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
            if 'deliveries' not in line:
                continue
            statuses.update(re.findall(r"(?:(?<![\w.])|\bd\.)status\s*=\s*'(\w+)'", line))
            for listed in re.findall(r"(?:(?<![\w.])|\bd\.)status\s+IN\s*\(([^)]*)\)", line):
                statuses.update(re.findall(r"'(\w+)'", listed))
            statuses.update(re.findall(r"INSERT INTO deliveries\([^)]*\)\s*VALUES\(\?,\s*'(\w+)'", line))
    return statuses


class DeliveryLabels(unittest.TestCase):
    def test_every_status_has_a_label(self):
        written = written_statuses()
        self.assertTrue({'grouped', 'cancelled', 'sending'} <= written, written)  # the scan still finds them
        missing = (written | WRITTEN_FROM_VARIABLES) - set(labels())
        self.assertFalse(missing, f'delivery statuses without a label in DELIVERY_LABEL: {sorted(missing)}')

    def test_no_raw_key_reaches_the_badge(self):
        source = RENDER.read_text(encoding='utf-8')
        self.assertIn("const deliveryStatusLabel=s=>Object.hasOwn(DELIVERY_LABEL,s)?DELIVERY_LABEL[s]:'Other';", source)
        row = re.search(r'const deliveryRow=d=>.*', source)[0]
        self.assertIn('chipNode(deliveryStatusLabel(d.status)', row)
        self.assertNotIn('||d.status', row)

    def test_labels_are_in_every_catalog(self):
        shown = set(labels().values()) | {'Other'}
        self.assertGreaterEqual(len(CATALOGS), 7)
        for path in CATALOGS:
            catalog = json.loads(path.read_text(encoding='utf-8'))
            with self.subTest(catalog=path.name):
                self.assertFalse(shown - set(catalog), f'{path.name} misses {sorted(shown - set(catalog))}')

    def test_labels_are_words_not_keys(self):
        for status, label in labels().items():
            with self.subTest(status=status):
                self.assertNotIn('_', label)
                self.assertTrue(label[:1].isupper(), label)


if __name__ == '__main__':
    unittest.main()
