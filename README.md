[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/GiacomoPope/xoflib/blob/main/LICENSE)
[![GitHub CI](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/xoflib/badge/?version=latest)](https://xoflib.readthedocs.io/en/latest/?badge=latest)

# xoflib

A Python package for the Ascon, BLAKE3, Shake (SHA3) and TurboShake extendable-output functions (XOFs). Built using
[pyO3](https://github.com/PyO3/pyo3) bindings for the [`ascon-hash`](https://crates.io/crates/ascon-hash), [`blake3`](https://crates.io/crates/blake3) and
[`sha3`](https://docs.rs/sha3/latest/sha3/) crates.

## Installation

This package is available as `xoflib` on
[PyPI](https://pypi.org/project/xoflib/):

```
pip install xoflib
```

## Algorithms

### Ascon

- [AsconXof()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.AsconXof)
- [AsconAXof()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.AsconAXof)

### BLAKE3

- [Blake3()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.Blake3)

### Sha3

- [Shake128()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.Shake128)
- [Shake256()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.Shake256)

### TurboShake

- [TurboShake128()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.TurboShake128)
- [TurboShake256()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.TurboShake256)

### Documentation

For more detailed documentation see the [`xoflib` package documentation](https://xoflib.readthedocs.io/en/stable/xoflib.html)

### Example Usage

For the `Shake128` and `Shake256` XOF, the intended usage is to first define a `shake` object, which is then finalized to product the XOF or Sponge:

```py
>>> from xoflib import Shake128
>>> shake128 = Shake128(b"a new XOF library")
>>> shake128.absorb(b"written using pyO3 bindings")
>>> xof = shake128.finalize()
>>> xof.read(16).hex()
'1301cd080b034973e961d585330b9e0c'
>>> xof.read(16).hex()
'1af56b984d09bce5a6c07da3f3b953bd'
```

The `TurboShake128` and `TurboShake256` XOFs additionally require a domain separation:

```py
>>> from xoflib import TurboShake256
>>> domain_sep = 123 # should be between (1, 127)
>>> turbo256 = TurboShake256(domain_sep)
>>> turbo256.absorb(b"Turbo mode")
>>> xof = turbo256.finalize()
>>> xof.read(16).hex()
'798984af20ecc1e9e593410c23f0fe67'
>>> xof.read(16).hex()
'5aa0168bc689e89a35111d43842de214'
```

Sponges can also be constructed directly:

```py
>>> from xoflib import shake128, Shake128
>>> sponge1 = Shaker128(b"a new XOF library").finalize()
>>> sponge2 = shake128(b"a new XOF library")
>>> assert sponge1.read(10) == sponge2.read(10)
```

For other XOFs, see the [documentation](https://xoflib.readthedocs.io/en/stable/xoflib.html) which includes example usage for all classes.

### Motivation

For most hashing needs, the `hashlib` module is appropriate. However, the
package maintainers have 
[decided to not support Shake as an XOF](https://github.com/python/cpython/issues/82198) 
and simply treat it as another hash with digest. This means that if a user reads
`n` bytes and then wishes for the next `m` bytes of output, they must generate
`n + m` bytes from a `digest()` call and then slice the output for the last `m`
bytes.

This can be an issue for cryptographic protocols, such as the post-quantum
protocols ML-KEM (Kyber) and ML-DSA (Dilithium), which rely on Shake128 and
Shake256 to continuously read bytes for rejection sampling.

The purpose of this package is to implement XOF for their intended use case, with `absorb()`, `finalize()` and `read()` methods, which allow for the correct instantiation of the XOF as well as efficient sampling of bytes.

## Tests

### Ascon

`AsconXOF` and `AsconAXof` are tested by comparing the output with the KAT vectors generated from [`pyascon`](https://github.com/meichlseder/pyascon). For more information, see the test file: [tests/test_ascon.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_ascon.py)

### BLAKE3

`Blake3` is tested by comparing the output with the KAT vectors downloaded from
the [BLAKE3 team implementation](https://github.com/BLAKE3-team)  [`test_vectors.json`](https://github.com/BLAKE3-team/BLAKE3/blob/master/test_vectors/test_vectors.json). For more information, see the test file: [tests/test_blake3.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_blake3.py).

### Sha3

`Shake128` and `Shake256` are tested by comparing the output with the KAT vectors downloaded from the "SHA-3 XOF Test Vectors for Byte-Oriented Output" section from [Cryptographic Algorithm Validation Program (CAVP)](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/secure-hashing). For more information, see the test file: [tests/test_shake.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_shake.py).

### TurboShake

`TurboShake128` and `TurboShake256` are tested by comparing the output with
the IRTF CRFG examples [draft-irtf-cfrg-kangarootwelve-14](https://datatracker.ietf.org/doc/draft-irtf-cfrg-kangarootwelve/) from Section 5.
For more information, see the test file:
[tests/test_turbo_shake.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_turbo_shake.py).

**Note**: the test data from the draft-irtf-cfrg isn't very nice to parse, so it was copy pasted and hand-formatted into a more sensible data structure in 
[tests/test_turbo_shake_data.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_turbo_shake_data.py).

## Benchmarking

We include rough benchmarks of the time it takes to read and absorb 100MB of
data into each XOF in chunk sizes of 32B, 1KB and 1MB. Results are displayed in
MB/s and are computed as the average throughput for running the test 100 times.

### Intel

| Algorithm      | Absorb (32B)   | Read (32B)   | Absorb (1KB)   | Read (1KB)   | Absorb (1MB)   | Read (1MB)   |
|----------------|----------------|--------------|----------------|--------------|----------------|--------------|
| AsconXof       | 84 MB/s        | 104 MB/s     | 147 MB/s       | 154 MB/s     | 160 MB/s       | 157 MB/s     |
| AsconAXof      | 100 MB/s       | 130 MB/s     | 210 MB/s       | 221 MB/s     | 222 MB/s       | 223 MB/s     |
| Blake3         | 141 MB/s       | 195 MB/s     | 793 MB/s       | 900 MB/s     | 2935 MB/s      | 1022 MB/s    |
| Shake128       | 116 MB/s       | 158 MB/s     | 320 MB/s       | 341 MB/s     | 368 MB/s       | 358 MB/s     |
| Shake256       | 106 MB/s       | 144 MB/s     | 268 MB/s       | 281 MB/s     | 287 MB/s       | 297 MB/s     |
| TurboShaker128 | 138 MB/s       | 197 MB/s     | 564 MB/s       | 615 MB/s     | 689 MB/s       | 709 MB/s     |
| TurboShaker256 | 130 MB/s       | 185 MB/s     | 470 MB/s       | 513 MB/s     | 556 MB/s       | 572 MB/s     |

All times recorded using a Intel Core i7-9750H CPU.

### ARM

| Algorithm      | Absorb (32B)   | Read (32B)   | Absorb (1KB)   | Read (1KB)   | Absorb (1MB)   | Read (1MB)   |
|----------------|----------------|--------------|----------------|--------------|----------------|--------------|
| AsconXof       | 121 MB/s       | 144 MB/s     | 163 MB/s       | 171 MB/s     | 162 MB/s       | 175 MB/s     |
| AsconAXof      | 157 MB/s       | 194 MB/s     | 235 MB/s       | 250 MB/s     | 242 MB/s       | 253 MB/s     |
| Blake3         | 211 MB/s       | 250 MB/s     | 739 MB/s       | 849 MB/s     | 1767 MB/s      | 920 MB/s     |
| Shake128       | 234 MB/s       | 341 MB/s     | 925 MB/s       | 997 MB/s     | 1041 MB/s      | 1082 MB/s    |
| Shake256       | 220 MB/s       | 315 MB/s     | 764 MB/s       | 800 MB/s     | 843 MB/s       | 833 MB/s     |
| TurboShaker128 | 277 MB/s       | 392 MB/s     | 1579 MB/s      | 1723 MB/s    | 1964 MB/s      | 2003 MB/s    |
| TurboShaker256 | 269 MB/s       | 378 MB/s     | 1354 MB/s      | 1473 MB/s    | 1669 MB/s      | 1661 MB/s    |

Times recorded using a Apple M2 CPU. Thanks are given to Bas Westerbaan for running the ARM benchmarks.

### Benchmarking against `hashlib`

We find that `xoflib` performs equally with `hashlib` and is faster than the XOFs available `pycryptodome`.

`xoflib` has the additional memory cost benefit as calling `c` bytes to be read from our XOF `n` times only needs `c` bytes of memory for each call, where as `hashlib` requires the potentially colossal amount of `n * c` bytes of memory which are then iterated over.

We include two timings for `hashlib` -- one naive where `n * c` bytes are requested and iterated over slicing over bytes and a second which uses a wrapper by David Buchanan
[from this comment](https://github.com/pyca/cryptography/issues/9185#issuecomment-1868518432) which helps with the API but has the same memory usage issues.

All times are derived by timing the computation of `c_0 ^ c_1 ^ ... c_(n-1)` for `n` chunks of `c` bytes:

```py
def benchmark_xof(shake, absorb, c, n):
    xof = shake(absorb).finalize()
    res = bytes([0] * c)
    for _ in range(n):
        chunk = xof.read(c)
        res = xor_bytes(res, chunk)
    return res
```

```
================================================================================
 Benchmarking Shake256: 
================================================================================
Requesting 1 bytes from XOF 10000 times
xoflib: 0.69s
hashlib (single call): 0.65s
hashlib (streaming): 0.82s
pycryptodome: 1.82s

Requesting 100 bytes from XOF 10000 times
xoflib: 6.65s
hashlib (single call): 6.57s
hashlib (streaming): 6.98s
pycryptodome: 7.83s

Requesting 1000 bytes from XOF 1000 times
xoflib: 6.05s
hashlib (single call): 5.90s
hashlib (streaming): 6.15s
pycryptodome: 6.15s

Requesting 10000 bytes from XOF 1000 times
xoflib: 5.82s
hashlib (single call): 5.77s
hashlib (streaming): 6.37s
pycryptodome: 5.85s

Requesting 32 bytes from XOF 100000 times
xoflib: 2.71s
hashlib (single call): 2.63s
hashlib (streaming): 2.89s
pycryptodome: 3.83s
```

For more information, see the file [`benchmarks/benchmark_xof.py`](https://github.com/GiacomoPope/xoflib/blob/main/benchmarks/benchmark_xof.py).

## Release Notes

- v0.3.1: modify the `__str__()` and `__repr__()` methods of the `Shake` and `Sponge` classes
- v0.3.0: include pyO3 bindings for BLAKE3 using the [`blake3`](https://crates.io/crates/blake3) crate
- v0.2.0: include pyO3 bindings for Ascon and AsconA using the [`ascon-hash`](https://crates.io/crates/ascon-hash) crate
- v0.1.0: include pyO3 bindings for Shake128, Shake256, TurboShake128 and  TurboShake256 using the [`sha3`](https://docs.rs/sha3/latest/sha3/) crate
