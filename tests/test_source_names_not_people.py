"""A source's own name ("Slack", "GitHub", "Stripe") never shows as a person's name: a Graph person named so is one
nobody's name was known for, so the sender shows by address or as someone on Slack instead."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant as a
import graph
from machine import names
from machine.kinds import KINDS
from machine.store import message_view, views


class SourceNamesNotPeople(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def person(self, db, node, name, *identifiers):
        db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,'person',?,1,0,?)",
                   (node, name, json.dumps({'identifiers': [node, *identifiers]})))

    def test_every_source_and_service_name_is_left_out(self):
        self.assertTrue({'Slack', 'GitHub', 'Stripe', 'Trello', 'CRM email'} <= graph.SOURCE_NAMES)
        self.assertTrue({row['name'] for row in KINDS.values() if row['name']} <= graph.SOURCE_NAMES)
        self.assertTrue(set(names.SERVICES.values()) <= graph.SOURCE_NAMES)

    def test_a_node_named_after_a_source_is_no_ones_name(self):
        with self.store.connect() as db:
            self.person(db, 'email:noreply@github.example', 'GitHub', 'slack:U0GITHUB01')
            self.person(db, 'email:billing@stripe.example', 'Stripe')
            self.person(db, 'email:lee@example.com', 'Lee', 'slack:U0LEE00001')
        with self.store.connect() as db:
            self.assertEqual(views.address_names(db, {'noreply@github.example', 'billing@stripe.example', 'lee@example.com'}),
                             {'lee@example.com': 'Lee'})
            self.assertEqual(message_view.address_names(db, {'billing@stripe.example', 'lee@example.com'}), {'lee@example.com': 'Lee'})
            self.assertEqual(views.slack_people_names(db, {'U0GITHUB01', 'U0LEE00001'}), {'U0LEE00001': 'Lee'})
            self.assertEqual(graph.slack_names(db, {'U0GITHUB01', 'U0LEE00001'}), {'U0LEE00001': 'Lee'})


if __name__ == '__main__':
    unittest.main()
