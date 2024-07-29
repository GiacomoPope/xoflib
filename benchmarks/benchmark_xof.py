from timeit import timeit
from hashlib import shake_128, shake_256
from xoflib import Shake128, Shake256, TurboShake128, TurboShake256
from Crypto.Hash.SHAKE128 import SHAKE128_XOF
from Crypto.Hash.SHAKE256 import SHAKE256_XOF
from shake_wrapper import shake_128_hashlib, shake_256_hashlib


def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))


def benchmark_xoflib_stream(shake, absorb, c, n):
    xof = shake(absorb).finalize()
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res


def benchmark_xoflib_turbo_stream(turboshake, absorb, c, n):
    xof = turboshake(1, absorb).finalize()
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res


def benchmark_hashlib_one_call(shake, absorb, c, n):
    """
    Requires generating all c * n bytes in one go
    """
    xof = shake(absorb).digest(c * n)
    xof_chunks = [xof[i : i + c] for i in range(0, c * n, c)]
    assert len(xof_chunks) == n

    res = bytes([0] * c)
    for chunk in xof_chunks:
        res = xor_bytes(res, chunk)
    return res


def benchmark_hashlib_stream(shake, absorb, c, n):
    """
    Requests only the bytes needed, but requires n calls to the digest
    """
    res = bytes([0] * c)
    xof = shake(absorb)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res


def benchmark_pycryptodome_stream(shake, absorb, c, n):
    shake.__init__()
    xof = shake.update(absorb)
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res


# Ensure things work
a = benchmark_xoflib_stream(Shake128, b"benchmarking...", 123, 1000)
b = benchmark_hashlib_one_call(shake_128, b"benchmarking...", 123, 1000)
c = benchmark_hashlib_stream(shake_128_hashlib, b"benchmarking...", 123, 1000)
d = benchmark_pycryptodome_stream(SHAKE128_XOF(), b"benchmarking...", 123, 1000)
assert a == b == c == d

benchmark_data = [
    (1, 10_000, 100),
    (100, 10_000, 100),
    (1000, 1000, 100),
    (10_000, 1000, 10),
    (32, 100_000, 10),
]

for name, shakes in [
    ("Shake128: ", (Shake128, shake_128, shake_128_hashlib, SHAKE128_XOF())),
    ("Shake256: ", (Shake256, shake_256, shake_256_hashlib, SHAKE256_XOF())),
]:
    print("=" * 80)
    print(f"Benchmarking {name}")
    print("=" * 80)
    for c, n, number in benchmark_data:
        print(f"Requesting {c} bytes from XOF {n} times")
        xoflib_time = timeit(
            'benchmark_xoflib_stream(shake, b"benchmarking...", c, n)',
            globals={
                "shake": shakes[0],
                "benchmark_xoflib_stream": benchmark_xoflib_stream,
                "c": c,
                "n": n,
            },
            number=number,
        )
        print(f"xoflib: {xoflib_time:.2f}s")

        hashlib_single_time = timeit(
            'benchmark_hashlib_one_call(shake, b"benchmarking...", c, n)',
            globals={
                "shake": shakes[1],
                "benchmark_hashlib_one_call": benchmark_hashlib_one_call,
                "c": c,
                "n": n,
            },
            number=number,
        )
        print(f"hashlib (single call): {hashlib_single_time:.2f}s")

        hashlib_stream_time = timeit(
            'benchmark_hashlib_stream(shake, b"benchmarking...", c, n)',
            globals={
                "shake": shakes[2],
                "benchmark_hashlib_stream": benchmark_hashlib_stream,
                "c": c,
                "n": n,
            },
            number=number,
        )
        print(f"hashlib (streaming): {hashlib_stream_time:.2f}s")

        pycryptodome_time = timeit(
            'benchmark_pycryptodome_stream(shake, b"benchmarking...", c, n)',
            globals={
                "shake": shakes[3],
                "benchmark_pycryptodome_stream": benchmark_pycryptodome_stream,
                "c": c,
                "n": n,
            },
            number=number,
        )
        print(f"pycryptodome: {pycryptodome_time:.2f}s")
        print()

for name, shake in [("TurboShake128", TurboShake128), ("TurboShake256", TurboShake256)]:
    print("=" * 80)
    print(f"Benchmarking {name}")
    print("=" * 80)
    for c, n, number in benchmark_data:
        print(f"Requesting {c} bytes from XOF {n} times")
        xoflib_time = timeit(
            'benchmark_xoflib_stream(shake, b"benchmarking...", c, n)',
            globals={
                "shake": shakes[0],
                "benchmark_xoflib_stream": benchmark_xoflib_stream,
                "c": c,
                "n": n,
            },
            number=number,
        )
        print(f"xoflib: {xoflib_time:.2f}s")
        print()
