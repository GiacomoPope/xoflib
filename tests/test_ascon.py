import json
import unittest
import os
import random
from xoflib import AsconXof, AsconAXof, ascon_xof, ascona_xof

def parse_kat_file(filename):
    with open(filename) as f:
        kat_data = json.load(f)
    return kat_data

class TestAsconKAT(unittest.TestCase):
    def kat_data_verify(self, filename, ascon_hash):
        kat_data = parse_kat_file(filename)
        for data in kat_data:
            msg = bytes.fromhex(data["Msg"])
            res = bytes.fromhex(data["MD"])
            self.assertEqual(ascon_hash(msg).read(32), res)

    def test_ascon_kat(self):
        self.kat_data_verify("./tests/assets/LWC_HASH_KAT_256_Ascon_Xof.json", ascon_xof)

    def test_ascona_kat(self):
        self.kat_data_verify("./tests/assets/LWC_HASH_KAT_256_AsconA_Xof.json", ascona_xof)

class TestAscon(unittest.TestCase):
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
    
    def test_ascon(self):
        self.class_function_comparison(AsconXof, ascon_xof)
    
    def test_ascona(self):
        self.class_function_comparison(AsconAXof, ascona_xof)

