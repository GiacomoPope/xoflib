import unittest
import os
import random
from xoflib import (
    Shake128,
    Shake256,
    shake128,
    shake256,
)

import sys

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
elif sys.version_info >= (3, 10):
    Buffer = bytes | bytearray | memoryview
else:
    from typing import ByteString as Buffer


class TestShakeKAT(unittest.TestCase):
    def shake_long_message(self, filename, shake):
        """
        Parse the data from a long message KAT and
        ensure all values match
        """
        with open(filename) as f:
            data = f.readlines()
        test_data = data[8:]

        # message length in bytes
        out_len = int(data[6].split(" = ")[-1][:-2]) // 8
        kat_number = len(test_data) // 4

        # parse out data
        for n in range(kat_number):
            msg_len = int(test_data[4 * n].split(" = ")[-1]) // 8
            msg = bytes.fromhex(test_data[4 * n + 1].split(" = ")[-1])
            out = bytes.fromhex(test_data[4 * n + 2].split(" = ")[-1])

            # Make sure messages and hashes match
            self.assertEqual(len(msg), msg_len)
            self.assertEqual(len(out), out_len)
            self.assertEqual(out, shake(msg).read(out_len))

    def test_shake128_long_message(self):
        self.shake_long_message("tests/assets/shake/SHAKE128LongMsg.rsp", shake128)

    def test_shake256_long_message(self):
        self.shake_long_message("tests/assets/shake/SHAKE256LongMsg.rsp", shake256)

    def shake_short_message(self, filename, shake):
        """
        Parse the data from a short message KAT and
        ensure all values match
        """
        with open(filename) as f:
            data = f.readlines()
        test_data = data[8:]

        # message length in bytes
        out_len = int(data[6].split(" = ")[-1][:-2]) // 8
        kat_number = len(test_data) // 4

        # parse out data
        for n in range(kat_number):
            msg_len = int(test_data[4 * n].split(" = ")[-1]) // 8
            if msg_len == 0:
                msg = b""
            else:
                msg = bytes.fromhex(test_data[4 * n + 1].split(" = ")[-1])
            out = bytes.fromhex(test_data[4 * n + 2].split(" = ")[-1])

            # Make sure messages and hashes match
            self.assertEqual(len(msg), msg_len)
            self.assertEqual(len(out), out_len)
            self.assertEqual(out, shake(msg).read(out_len))

    def test_shake128_short_message(self):
        self.shake_short_message("tests/assets/shake/SHAKE128ShortMsg.rsp", shake128)

    def test_shake256_short_message(self):
        self.shake_short_message("tests/assets/shake/SHAKE256ShortMsg.rsp", shake256)

    def shake_variable_output(self, filename, shake):
        """
        Parse the data from the variable output KAT and
        ensure all values match
        """
        with open(filename) as f:
            data = f.readlines()
        test_data = data[9:]

        # message length in bytes
        msg_len = int(data[6].split(" = ")[-1][:-2]) // 8
        kat_number = len(test_data) // 5

        # parse out data
        for n in range(kat_number):
            out_len = int(test_data[5 * n + 1].split(" = ")[-1]) // 8
            msg = bytes.fromhex(test_data[5 * n + 2].split(" = ")[-1])
            out = bytes.fromhex(test_data[5 * n + 3].split(" = ")[-1])

            # Make sure messages and hashes match
            self.assertEqual(len(msg), msg_len)
            self.assertEqual(len(out), out_len)
            self.assertEqual(out, shake(msg).read(out_len))

    def test_shake128_variable_output(self):
        self.shake_variable_output(
            "tests/assets/shake/SHAKE128VariableOut.rsp", shake128
        )

    def test_shake256_variable_output(self):
        self.shake_variable_output(
            "tests/assets/shake/SHAKE256VariableOut.rsp", shake256
        )


class TestShakeMonteCarlo(unittest.TestCase):
    """
    Ensure that Shake XOF passes the KAT Monte Carlo test
    """

    def monte_carlo(self, msg, minout_len, maxout_len, shake):
        minout_byte = minout_len // 8
        maxout_len = maxout_len // 8
        output_len = maxout_len
        range_byte = maxout_len - minout_byte + 1

        output_j = []
        for _ in range(100):
            for i in range(1000):
                msg = shake((msg + bytes(16))[:16]).read(output_len)
                output_len = (
                    int.from_bytes(msg[-2:], byteorder="big") % range_byte + minout_byte
                )
            output_j.append(msg)

        return output_j

    def monte_carlo_shake(self, filename, shake):
        with open(filename) as f:
            data = f.readlines()

        minout_len = int(data[5].split(" = ")[-1][:-2])
        maxout_len = int(data[7].split(" = ")[-1][:-2])
        msg = bytes.fromhex(data[9].split(" = ")[-1])
        test_data = data[11:]
        output_j = self.monte_carlo(msg, minout_len, maxout_len, shake)

        for j in range(100):
            out_len = int(test_data[4 * j + 1].split(" = ")[-1][:-1]) // 8
            out_kat = bytes.fromhex(test_data[4 * j + 2].split(" = ")[-1])
            out_gen = output_j[j]
            self.assertEqual(len(out_gen), out_len)
            self.assertEqual(out_gen, out_kat)

    def test_monte_carlo_shake_128(self):
        self.monte_carlo_shake("tests/assets/shake/SHAKE128Monte.rsp", shake128)

    def test_monte_carlo_shake_256(self):
        self.monte_carlo_shake("tests/assets/shake/SHAKE256Monte.rsp", shake256)


class TestShake(unittest.TestCase):
    def class_function_comparison(self, ClassHash, function_hash):
        for _ in range(50):
            # bytes to consume
            init = os.urandom(32)
            absorb = os.urandom(64)

            # create XOF from class or hash
            xof_class = ClassHash(init).absorb(absorb).finalize()
            xof_function = function_hash(init + absorb)

            # Read a bunch of bytes and make sure everything matches
            for _ in range(50):
                n = random.randint(1, 1000)
                self.assertEqual(xof_class.read(n), xof_function.read(n))

    def test_shake128(self):
        self.class_function_comparison(Shake128, shake128)

    def test_shake256(self):
        self.class_function_comparison(Shake256, shake256)

    def accept_buffer_api(self, Shake, shake, data: Buffer):
        xof1 = Shake(data).finalize()
        xof2 = shake(data)
        self.assertEqual(xof1.read(100), xof2.read(100))

    def test_all_accept_buffer_api(self):
        self.accept_buffer_api(
            Shake128, shake128, bytearray(b"bytearrays support __buffer__")
        )
        self.accept_buffer_api(
            Shake256, shake256, bytearray(b"bytearrays support __buffer__")
        )
