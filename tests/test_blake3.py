import json
import unittest
from xoflib import Blake3, blake3_xof
from utilities import create_pattern
import os
import random

# Data parsed for KAT vectors downloaded from
# https://github.com/BLAKE3-team/BLAKE3/blob/master/test_vectors/test_vectors.json
class TestBlake3KAT(unittest.TestCase):
    def test_blake3_kat(self):
        with open("tests/assets/blake3/test_vectors.json") as f:
            kat_data = json.load(f)

        for data in kat_data["cases"]:
            kat_hash = bytes.fromhex(data["hash"])
            input_bytes = create_pattern(250, int(data["input_len"]))
            self.assertEqual(kat_hash, blake3_xof(input_bytes).read(131))

class TestBlake(unittest.TestCase):
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

    def test_blake3(self):
        self.class_function_comparison(Blake3, blake3_xof)

    def test_accept_buffer_api(self):
        data = bytearray(b"bytearrays support __buffer__")
        xof1 = Blake3(data).finalize()
        xof2 = blake3_xof(data)
        self.assertEqual(xof1.read(100), xof2.read(100))
