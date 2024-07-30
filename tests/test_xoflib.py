from hashlib import shake_128, shake_256
from xoflib import Shake128, Shake256, shake128, shake256, TurboShake128, TurboShake256, turbo_shake128, turbo_shake256
import unittest

import sys
if sys.version_info >= (3, 12):
    from collections.abc import Buffer
elif sys.version_info >= (3, 10):
    Buffer = bytes | bytearray | memoryview
else:
    from typing import ByteString as Buffer

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

    def accept_buffer_api(self, Shake, shake, shake_hashlib, data: Buffer):
        xof1 = Shake(data).finalize()
        xof2 = shake(data)
        correct = shake_hashlib(data).digest(100)
        self.assertEqual(xof1.read(100), correct)
        self.assertEqual(xof2.read(100), correct)

    def test_all_accept_buffer_api(self):
        self.accept_buffer_api(Shake128, shake128, shake_128, bytearray(b"bytearrays support __buffer__"))
        self.accept_buffer_api(Shake256, shake256, shake_256, bytearray(b"bytearrays support __buffer__"))


class TestTurboShakeHashlib(unittest.TestCase):
    def turbo_shake(self, TurboShake, turbo_shake):
        xof_1 = TurboShake(1, b"testing turbo shake").finalize()
        xof_2 = TurboShake(127, b"testing turbo shake").finalize()
        xof_3 = turbo_shake(1, b"testing turbo shake")

        a = xof_1.read(10)
        b = xof_2.read(10)
        c = xof_3.read(10)

        # Different domain sep mean bytes read don't match
        self.assertNotEqual(a, b)

        # Class or Function constructor is the same
        self.assertEqual(a, c)

    def test_turbo_domain_failure(self):
        # domain sep must be larger than 0
        self.assertRaises(ValueError, lambda: TurboShake128(0))
        self.assertRaises(ValueError, lambda: TurboShake256(0))

        # domain sep must be smaller than 128
        self.assertRaises(ValueError, lambda: TurboShake128(128))
        self.assertRaises(ValueError, lambda: TurboShake256(128))

    def test_turboshake_128(self):
        self.turbo_shake(TurboShake128, turbo_shake128)

    def test_turboshake_256(self):
        self.turbo_shake(TurboShake256, turbo_shake256)

    def accept_buffer_api(self, Shake, shake, data: Buffer):
        xof1 = Shake(1, data).finalize()
        xof2 = shake(1, data)
        self.assertEqual(xof1.read(100), xof2.read(100))

    def test_all_accept_buffer_api(self):
        self.accept_buffer_api(TurboShake128, turbo_shake128, bytearray(b"bytearrays support __buffer__"))
        self.accept_buffer_api(TurboShake256, turbo_shake256, bytearray(b"bytearrays support __buffer__"))
