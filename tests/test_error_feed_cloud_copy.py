"""The cloud's error intake keeps its own copy of error_feed.py's word lists, types, services and patterns, and refuses
reports with anything outside them. A change here that the cloud doesn't take too gets error reports quietly refused,
so this pins a checksum of exactly what the cloud compares."""
import hashlib
import json
import unittest

import error_feed as ef

CHECKSUM = 'f77bdb5409114760971fb7f060cf803f8bd4af46ae91122a8dc838313f0a41f8'


def checksum(feed):
    parts = {'WORDS': sorted(feed.WORDS), 'TYPES': sorted(feed.TYPES), 'TYPE_NAME': feed.TYPE_NAME.pattern,
             'DOMAIN': feed.DOMAIN.pattern, 'SHAPE': feed.SHAPE.pattern, 'SAFE_WORDS': sorted(feed.SAFE_WORDS),
             'SAFE_CODES': sorted(feed.SAFE_CODES), 'SAFE_TYPES': sorted(feed.SAFE_TYPES), 'SERVICES': sorted(feed.SERVICES)}
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()


class CloudCopy(unittest.TestCase):
    def test_the_word_lists_the_cloud_copies_are_unchanged(self):
        self.assertEqual(checksum(ef), CHECKSUM, 'error_feed word lists changed: update cloud/errors.py in the cloud repo '
                         'too, then update this checksum')


if __name__ == '__main__':
    unittest.main()
