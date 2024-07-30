import sys
import unittest
from test_turbo_shake_data import (
    turbo_shake_128_test_vectors,
    turbo_shake_256_test_vectors,
)
from xoflib import turbo_shake128, turbo_shake256, TurboShake128, TurboShake256

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
elif sys.version_info >= (3, 10):
    Buffer = bytes | bytearray | memoryview
else:
    from typing import ByteString as Buffer


class TestTurboShakeDocumentation(unittest.TestCase):
    def parsed_data_test(self, shake, vectors):
        for test_vector in vectors:
            output = shake(test_vector["D"], test_vector["msg"]).read(
                test_vector["out_len"]
            )
            if test_vector.get("last"):
                last = test_vector.get("last")
                output = output[-last:]
            output_kat = bytes.fromhex(test_vector["output_bytes"].replace(" ", ""))
            self.assertEqual(output, output_kat)

    def test_turbo_shake_128(self):
        self.parsed_data_test(turbo_shake128, turbo_shake_128_test_vectors)

    def test_turbo_shake_256(self):
        self.parsed_data_test(turbo_shake256, turbo_shake_256_test_vectors)


class TestTurboShake(unittest.TestCase):
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
        self.accept_buffer_api(
            TurboShake128, turbo_shake128, bytearray(b"bytearrays support __buffer__")
        )
        self.accept_buffer_api(
            TurboShake256, turbo_shake256, bytearray(b"bytearrays support __buffer__")
        )
