import random
from hashlib import shake_128
from xof_py import pyo3_shake_128
import time
import os

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    b = pyo3_shake_128(absorb, n)
    assert a == b

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = pyo3_shake_128(b"123", n)
print(f"10_000 calls with rust sha3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = shake_128(b"123").digest(n)
print(f"10_000 calls with hashlib: {time.time() - t0}")
