from hashlib import shake_128
from xof_py import shake_123

import time

t0 = time.time()
for _ in range(10_000):
    a = shake_123()
print(f"10_000 calls with rust sha3: {time.time() - t0 }")

t0 = time.time()
for _ in range(10_000):
    a = shake_128(b"123").digest(10)
print(f"10_000 calls with hashlib: {time.time() - t0}")