import random
from hashlib import shake_128
from xof_py import pyo3_shake_128, pyo3_shake_128_one_block, pyo3_shake_128_n_blocks
import time
import os

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 1000)
    a = shake_128(absorb).digest(n)
    b = pyo3_shake_128(absorb, n)
    assert a == b

for _ in range(100):
    absorb = os.urandom(32)
    a = shake_128(absorb).digest(168)
    b = pyo3_shake_128_one_block(absorb)
    assert a == b

for _ in range(100):
    absorb = os.urandom(32)
    n = random.randint(1, 32)
    a = shake_128(absorb).digest(168 * n)
    b = pyo3_shake_128_n_blocks(absorb, n)
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

print()

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    a = pyo3_shake_128_one_block(b"123")
print(f"10_000 one block calls with rust sha3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    a = shake_128(b"123").digest(168)
print(f"10_000 one block calls with hashlib: {time.time() - t0}")

print()

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    a = pyo3_shake_128_n_blocks(b"123", 2)
print(f"10_000 2 block calls with rust sha3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    a = shake_128(b"123").digest(168 * 2)
print(f"10_000 2 block calls with hashlib: {time.time() - t0}")

print()

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 32)
    a = pyo3_shake_128_n_blocks(b"123", n)
print(f"10_000 n block calls with rust sha3: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 32)
    a = shake_128(b"123").digest(168 * n)
print(f"10_000 n block calls with hashlib: {time.time() - t0}")
