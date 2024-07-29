from hashlib import shake_128, shake_256
from xoflib import Shaker128, Shaker256
import unittest


class TestShakeHashlib(unittest.TestCase):
    def hashlib_test_long_calls(self, Shake, shake_hashlib):
        absorb_bytes = b"testing_shake_long"
        for l in [1, 100, 1000, 2000, 5000, 1_000_000]:
            xof = Shake(absorb_bytes).finalize()
            self.assertEqual(shake_hashlib(absorb_bytes).digest(l), xof.read(l))

    def hashlib_test_many_calls(self, Shake, shake_hashlib):
        absorb_bytes = b"testing_shake_one_byte"
        for l in [1, 100, 1000, 2000, 5000, 1_000_000]:
            xof = Shake(absorb_bytes).finalize()
            output = b"".join([xof.read(1) for _ in range(l)])
            self.assertEqual(shake_hashlib(absorb_bytes).digest(l), output)

    def test_hashlib_shake128(self):
        self.hashlib_test_long_calls(Shaker128, shake_128)
        self.hashlib_test_many_calls(Shaker128, shake_128)

    def test_hashlib_shake256(self):
        self.hashlib_test_long_calls(Shaker256, shake_256)
        self.hashlib_test_many_calls(Shaker256, shake_256)
