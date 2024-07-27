import random
from hashlib import shake_128
from xof_py import (
    pyo3_shake_128,
    pyo3_shake_128_one_block,
    pyo3_shake_128_n_blocks,
    Shake128_pyo3,
)
import time
import os

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    xof = Shake128_pyo3(absorb)
    b = xof.read(n)
    assert a == b

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    b = pyo3_shake_128(absorb, n)
    assert a == b

# for _ in range(100):
#     absorb = os.urandom(32)
#     n = random.randint(1, 1000)
#     a = shake_128(absorb).digest(n)
#     b = pyo3_shake_128(absorb, n)
#     assert a == b

# for _ in range(100):
#     absorb = os.urandom(32)
#     a = shake_128(absorb).digest(168)
#     b = pyo3_shake_128_one_block(absorb)
#     assert a == b

random.seed(0)
t0 = time.time()
xof = Shake128_pyo3(b"123")
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls with class pyo3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = pyo3_shake_128(b"123", n)
print(f"10_000 calls with rust sha3: {time.time() - t0 }")

print("-" * 80)
