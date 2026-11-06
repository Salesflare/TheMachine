"""Another AI reading Knowledge for another AI: this script knows nothing of The Machine. It gets only the export folder,
reads its README.md, records/*.jsonl, tables/*.csv and the Markdown notes with the standard library, and answers
questions the way the README tells an AI to. No model: each answer is a deterministic lookup, so the test that runs it
(tests/test_knowledge_export.py) checks that the folder alone is enough to answer.

    python3 -I tests/knowledge_export_eval.py <export folder>      prints {question: answer} as JSON

Run with -I (isolated): nothing of The Machine is importable, only this file and the folder."""
import csv
import json
import sys
from pathlib import Path


class Reader:
    def __init__(self, root):
        self.root = Path(root)
        self.readme = (self.root / 'README.md').read_text()
        self.records = {p.stem: [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
                        for p in (self.root / 'records').glob('*.jsonl')}
        self.contacts = list(csv.DictReader((self.root / 'tables/contacts.csv').open()))
        self.by_id = {e['id']: e for e in self.records['entities']}

    def find(self, name):
        """A record by name, as the README says: tables/contacts.csv or records/entities.jsonl."""
        name = name.casefold()
        hit = next((c for c in self.contacts if name in c['name'].casefold()), None)
        if hit:
            return self.by_id[hit['id']]
        return next(e for e in self.records['entities'] if name in e['name'].casefold())

    def page(self, name):
        return (self.root / self.find(name)['file']).read_text()

    def owner_prefers(self, topic):
        return [f['text'] for f in self.records['facts'] if f['sort'] == 'preference' and not f['about'] and topic in f['text'].casefold()]

    def prefers(self, name, topic):
        who = self.find(name)['id']
        return [f['text'] for f in self.records['facts'] if who in f['about'] and topic in f['text'].casefold()]

    def relation(self, a, b):
        a, b = self.find(a)['id'], self.find(b)['id']
        return [f"{self.by_id[r['from']]['name']} {r['label']} {self.by_id[r['to']]['name']}" for r in self.records['relationships']
                if {r['from'], r['to']} == {a, b}]

    def works_at(self, name):
        who = self.find(name)['id']
        return [self.by_id[r['to']]['name'] for r in self.records['relationships'] if r['from'] == who and r['kind'] == 'member']

    def promised(self, name):
        first = name.casefold()
        return [(p['what'], p['due']) for p in self.records['promises'] if p['direction'] == 'mine' and first in p['who'].casefold()]

    def todos_on(self, project):
        return [t['title'] for t in self.records['todos'] if (t.get('project') or '').casefold() == project.casefold()]

    def stage(self, project):
        e = self.find(project)
        return e.get('board'), e.get('stage')

    def writes(self, channel):
        return next(v['text'] for v in self.records['writing_style'] if v['channel'].casefold() == channel.casefold())

    def signature(self):
        return self.records['signatures'][0]['text']

    def rules(self):
        return [r['text'] for r in self.records['rules']]

    def source_of(self, words):
        fact = next(f for f in self.records['facts'] if words in f['text'].casefold())
        sources = {s['id']: s for s in self.records['sources']}
        return [{'kind': sources[s]['kind'], 'at': sources[s]['at'][:10], 'has_text': 'text' in sources[s]} for s in fact['sources']]

    def skill(self, name):
        found = next(s for s in self.records['skills'] if name.casefold() in s['name'].casefold())
        return found['body']

    def brief(self):
        return [b['text'] for b in self.records['team_briefs']]

    def summary(self, name):
        who = self.find(name)['id']
        return [s['text'] for s in self.records['summaries'] if s['about'] == who]


def answers(root):
    r = Reader(root)
    return {
        'What does the owner prefer for meetings?': r.owner_prefers('meeting'),
        'What does Avery prefer for contact?': r.prefers('Avery', 'call'),
        'Who is Bo and how do they relate to Avery?': r.relation('Bo', 'Avery'),
        'Where does Avery work?': r.works_at('Avery'),
        'What did the owner promise Avery, and by when?': r.promised('Avery'),
        'Which open to-dos are on Harbor Rollout?': r.todos_on('Harbor Rollout'),
        'Where does Harbor Rollout stand?': list(r.stage('Harbor Rollout')),
        'How does the owner write email?': r.writes('Email'),
        "What is the owner's signature?": r.signature(),
        'Which rules do drafts follow?': r.rules(),
        'Where did the fact about the pricing sheet come from?': r.source_of('pricing'),
        'How is an onboarding call done?': r.skill('Onboarding call'),
        'What does the team brief say?': r.brief(),
        'Who is Avery, in short?': r.summary('Avery'),
        "Does Avery's page say where they work?": 'Lumen Works' in r.page('Avery'),
        "Does Bo's page say how they relate to Avery?": 'assistant of' in r.page('Bo'),
        'Does the README tell an AI where to start?': 'owner/profile.md' in r.readme and 'How to use it' in r.readme,
    }


if __name__ == '__main__':
    print(json.dumps(answers(sys.argv[1]), indent=1, ensure_ascii=False))
