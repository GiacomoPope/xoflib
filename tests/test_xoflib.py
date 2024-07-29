from hashlib import shake_128, shake_256
from xoflib import Shake128, Shake256, shake128, shake256
import unittest


class TestShakeHashlib(unittest.TestCase):
    def hashlib_test_long_calls(self, Shake, shake, shake_hashlib):
        absorb_bytes = b"testing_shake_long"
        for length in [1, 100, 1000, 2000, 5000, 1_000_000]:
            xof1 = Shake(absorb_bytes).finalize()
            xof2 = shake(absorb_bytes)
            correct = shake_hashlib(absorb_bytes).digest(length)
            self.assertEqual(xof1.read(length), correct)
            self.assertEqual(xof2.read(length), correct)

    def hashlib_test_many_calls(self, Shake, shake, shake_hashlib):
        absorb_bytes = b"testing_shake_one_byte"
        for length in [1, 100, 1000, 2000, 5000, 1_000_000]:
            xof1 = Shake(absorb_bytes).finalize()
            xof2 = shake(absorb_bytes)
            correct = shake_hashlib(absorb_bytes).digest(length)
            output1 = b"".join([xof1.read(1) for _ in range(length)])
            output2 = b"".join([xof2.read(1) for _ in range(length)])

            self.assertEqual(output1, correct)
            self.assertEqual(output2, correct)

    def test_hashlib_shake128(self):
        self.hashlib_test_long_calls(Shake128, shake128, shake_128)
        self.hashlib_test_many_calls(Shake128, shake128, shake_128)

    def test_hashlib_shake256(self):
        self.hashlib_test_long_calls(Shake256, shake256, shake_256)
        self.hashlib_test_many_calls(Shake256, shake256, shake_256)
