import random
from hashlib import shake_128
from xof_py import Shaker128
import time
import os

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    b = Shaker128(absorb).finalize().read(n)
    assert a == b

random.seed(0)
t0 = time.time()
xof = Shaker128(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls with class pyo3: {time.time() - t0 }")

print("-" * 80)
