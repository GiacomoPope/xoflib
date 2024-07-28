import random
from hashlib import shake_128
from xof import Shaker128
import time
import os
from Crypto.Hash.SHAKE128 import SHAKE128_XOF

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    b = Shaker128(absorb).finalize().read(n)
    assert a == b

for _ in range(3):
    absorb = os.urandom(32)
    xof1 = Shaker128(absorb).finalize()
    xof2 = Shaker128(absorb).finalize()
    a = shake_128(absorb).digest(100_000)
    b = b"".join(xof1.read(1) for _ in range(100_000))
    c = xof2.read(100_000)
    assert a == b == c

random.seed(0)
t0 = time.time()
xof = Shaker128(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls with class pyo3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = shake_128(b"123").digest(n)
print(f"10_000 calls with hashlib: {time.time() - t0 }")

print("-" * 80)

t0 = time.time()
xof = Shaker128(b"123").finalize()
for _ in range(1_000_000):
    a = xof.read(1)
print(f"1_000_000 single byte reads pyo3: {time.time() - t0 }")

t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(1_000_000):
    a = xof.read(1)
print(f"1_000_000 single byte reads pycryptodome: {time.time() - t0 }")

t0 = time.time()
xof = Shaker128(b"123").finalize()
for _ in range(1_000_000):
    a = xof.read(168)
print(f"100_000 block reads pyo3: {time.time() - t0 }")

t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(1_000_000):
    a = xof.read(168)
print(f"100_000 block reads pycryptodome: {time.time() - t0 }")
