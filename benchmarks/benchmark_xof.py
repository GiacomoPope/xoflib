import random
from hashlib import shake_128
from xof import Shaker128
import time
from Crypto.Hash.SHAKE128 import SHAKE128_XOF

random.seed(0)
t0 = time.time()
xof = Shaker128(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 500)
    a = xof.read(n)
print(f"10_000 calls with xof library: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 500)
    a = shake_128(b"123").digest(n)
print(f"10_000 calls with hashlib: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(10_000):
    n = random.randint(1, 500)
    a = xof.read(n)
print(f"10_000 calls with pycryptodome: {time.time() - t0 }")

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
