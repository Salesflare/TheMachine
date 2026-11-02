"""qr.py, the small QR encoder for the mobile app's connect code. The expected codes come from the qrcode package
(8.2, byte mode, level M, the same mask forced); each is kept as a hash of its rows, so this test needs no package."""
import hashlib, unittest
import qr

KNOWN = [  # (text, mask, version, sha256 of the rows joined by newlines, first 24 hex)
    ('a', 0, 1, 'ad65f877bf9411d14b0b2efb'),
    ('hello world', 3, 1, '51672c7be5800174ed75f085'),
    ('computer.themachine.app://connect?u=https%3A%2F%2Fmachine.tailnet.ts.net%2Fassistant%2F', 5, 6, '1327291168ad54ab7b4a81ac'),
    ('https://x.example/' + 'y' * 150, 6, 9, '69d7f2531b5373d65ffd0dee'),  # two block groups, version information
    ('z' * 213, 7, 10, '253da557eea8cedaf26e8a04'),  # the longest it takes, 16-bit length
    ('héllo ✓', 1, 1, '3f6a0006688c30d6a7d9ec0e'),  # UTF-8 bytes
]


class QR(unittest.TestCase):
    def test_same_codes_as_the_reference(self):
        for text, mask, version, digest in KNOWN:
            rows = qr.encode(text, mask)
            self.assertEqual(len(rows), 17 + 4 * version, text[:20])
            self.assertEqual(hashlib.sha256('\n'.join(rows).encode()).hexdigest()[:24], digest, text[:20])

    def test_picks_a_mask_and_refuses_too_long(self):
        rows = qr.encode('computer.themachine.app://connect?u=x')
        self.assertTrue(all(set(r) <= {'0', '1'} and len(r) == len(rows) for r in rows))
        self.assertTrue(rows[0].startswith('1111111'))  # a finder in the corner
        self.assertIn(rows, [qr.encode('computer.themachine.app://connect?u=x', m) for m in range(8)])
        with self.assertRaises(ValueError):
            qr.encode('z' * 214)


if __name__ == '__main__':
    unittest.main()
