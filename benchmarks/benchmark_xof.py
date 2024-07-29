from hashlib import shake_128
from xoflib import Shaker128, Shaker256, TurboShaker128, TurboShaker256
from timeit import timeit
from Crypto.Hash.SHAKE128 import SHAKE128_XOF
from shake_wrapper import shake_128_hashlib

def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))


def benchmark_xoflib_stream(absorb, c, n):
    xof = Shaker128(absorb).finalize()
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res

def benchmark_hashlib_one_call(absorb, c, n):
    """
    Requires generating all c * n bytes in one go
    """
    xof = shake_128(absorb).digest(c * n)
    xof_chunks = [xof[i : i + c] for i in range(0, c * n, c)]
    assert len(xof_chunks) == n

    res = bytes([0] * c)
    for chunk in xof_chunks:
        res = xor_bytes(res, chunk)
    return res

def benchmark_hashlib_stream(absorb, c, n):
    """
    Requests only the bytes needed, but requires n calls to the digest
    """
    res = bytes([0] * c)
    xof = shake_128_hashlib(absorb)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res

def benchmark_pycryptodome_stream(absorb, c, n):
    xof = SHAKE128_XOF().update(absorb)
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res


# Ensure things work
a = benchmark_xoflib_stream(b"benchmarking...", 123, 1000)
b = benchmark_hashlib_one_call(b"benchmarking...", 123, 1000)
c = benchmark_hashlib_stream(b"benchmarking...", 123, 1000)
d = benchmark_pycryptodome_stream(b"benchmarking...", 123, 1000)

assert a == b == c == d

print("="*80)
for (c, n) in [(1, 10_000), (100, 10_000), (1000, 1000), (10_000, 1000), (32, 100_000)]:
    print(f"Requesting {c} bytes from XOF {n} times")
    xoflib_time = timeit(
        'benchmark_xoflib_stream(b"benchmarking...", c, n)',
        globals={"benchmark_xoflib_stream": benchmark_xoflib_stream, "c" : c, "n" : n},
        number = 10
    )
    print(f"xoflib: {xoflib_time:.2f}s")
    
    hashlib_single_time = timeit(
        'benchmark_hashlib_one_call(b"benchmarking...", c, n)',
        globals={"benchmark_hashlib_one_call": benchmark_hashlib_one_call, "c" : c, "n" : n},
        number = 10
    )
    print(f"hashlib (single call): {hashlib_single_time:.2f}s")

    hashlib_stream_time = timeit(
        'benchmark_hashlib_stream(b"benchmarking...", c, n)',
        globals={"benchmark_hashlib_stream": benchmark_hashlib_stream, "c" : c, "n" : n},
        number = 10
    )
    print(f"hashlib (streaming): {hashlib_stream_time:.2f}s")

    pycryptodome_time = timeit(
        'benchmark_pycryptodome_stream(b"benchmarking...", c, n)',
        globals={"benchmark_pycryptodome_stream": benchmark_pycryptodome_stream, "c" : c, "n" : n},
        number = 10
    )
    print(f"pycryptodome: {pycryptodome_time:.2f}s")
    print("="*80)


# print("-" * 80)

# random.seed(0)
# t0 = time.time()
# xof = Shaker128(b"123").finalize()
# for _ in range(10_000):
#     n = random.randint(1, 500)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 500)) with xoflib: {time.time() - t0 }")

# random.seed(0)
# t0 = time.time()
# for _ in range(10_000):
#     n = random.randint(1, 500)
#     a = shake_128(b"123").digest(n)
# print(f"10_000 calls (read(1, 500)) with hashlib: {time.time() - t0 }")

# random.seed(0)
# t0 = time.time()
# xof = SHAKE128_XOF()
# xof.update(b"123")
# for _ in range(10_000):
#     n = random.randint(1, 500)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 500)) with pycryptodome: {time.time() - t0 }")

# print("-" * 80)

# t0 = time.time()
# xof = Shaker128(b"123").finalize()
# for _ in range(1_000_000):
#     a = xof.read(1)
# print(f"1_000_000 single byte reads with xoflib: {time.time() - t0 }")

# t0 = time.time()
# xof = SHAKE128_XOF()
# xof.update(b"123")
# for _ in range(1_000_000):
#     a = xof.read(1)
# print(f"1_000_000 single byte reads pycryptodome: {time.time() - t0 }")

# t0 = time.time()
# xof = Shaker128(b"123").finalize()
# for _ in range(1_000_000):
#     a = xof.read(168)
# print(f"100_000 block reads with xoflib: {time.time() - t0 }")

# t0 = time.time()
# xof = SHAKE128_XOF()
# xof.update(b"123")
# for _ in range(1_000_000):
#     a = xof.read(168)
# print(f"100_000 block reads pycryptodome: {time.time() - t0 }")

# print("-" * 80)

# random.seed(0)
# t0 = time.time()
# xof = Shaker128(b"123").finalize()
# for _ in range(10_000):
#     n = random.randint(1, 5000)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 5000)) with xoflib Shake128: {time.time() - t0 }")

# random.seed(0)
# t0 = time.time()
# xof = Shaker256(b"123").finalize()
# for _ in range(10_000):
#     n = random.randint(1, 5000)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 5000)) with xoflib Shaker256: {time.time() - t0 }")

# random.seed(0)
# t0 = time.time()
# xof = TurboShaker128(1, b"123").finalize()
# for _ in range(10_000):
#     n = random.randint(1, 5000)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 5000)) with xoflib TurboShaker128: {time.time() - t0 }")

# random.seed(0)
# t0 = time.time()
# xof = TurboShaker256(1, b"123").finalize()
# for _ in range(10_000):
#     n = random.randint(1, 5000)
#     a = xof.read(n)
# print(f"10_000 calls (read(1, 5000)) with xoflib TurboShaker256: {time.time() - t0 }")
