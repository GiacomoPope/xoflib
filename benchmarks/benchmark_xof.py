import random
from hashlib import shake_128
from xoflib import Shake128, Shake256, TurboShake128, TurboShake256
import time
from Crypto.Hash.SHAKE128 import SHAKE128_XOF

random.seed(0)
t0 = time.time()
xof = Shake128(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 500)
    a = xof.read(n)
print(f"10_000 calls (read(1, 500)) with xoflib: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
for _ in range(10_000):
    n = random.randint(1, 500)
    a = shake_128(b"123").digest(n)
print(f"10_000 calls (read(1, 500)) with hashlib: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(10_000):
    n = random.randint(1, 500)
    a = xof.read(n)
print(f"10_000 calls (read(1, 500)) with pycryptodome: {time.time() - t0 }")

print("-" * 80)

t0 = time.time()
xof = Shake128(b"123").finalize()
for _ in range(1_000_000):
    a = xof.read(1)
print(f"1_000_000 single byte reads with xoflib: {time.time() - t0 }")

t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(1_000_000):
    a = xof.read(1)
print(f"1_000_000 single byte reads pycryptodome: {time.time() - t0 }")

t0 = time.time()
xof = Shake128(b"123").finalize()
for _ in range(1_000_000):
    a = xof.read(168)
print(f"100_000 block reads with xoflib: {time.time() - t0 }")

t0 = time.time()
xof = SHAKE128_XOF()
xof.update(b"123")
for _ in range(1_000_000):
    a = xof.read(168)
print(f"100_000 block reads pycryptodome: {time.time() - t0 }")

print("-" * 80)

random.seed(0)
t0 = time.time()
xof = Shake128(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls (read(1, 5000)) with xoflib Shake128: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
xof = Shake256(b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls (read(1, 5000)) with xoflib Shake256: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
xof = TurboShake128(1, b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls (read(1, 5000)) with xoflib TurboShake128: {time.time() - t0 }")

random.seed(0)
t0 = time.time()
xof = TurboShake256(1, b"123").finalize()
for _ in range(10_000):
    n = random.randint(1, 5000)
    a = xof.read(n)
print(f"10_000 calls (read(1, 5000)) with xoflib TurboShake256: {time.time() - t0 }")
