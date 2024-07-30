[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/GiacomoPope/xoflib/blob/main/LICENSE)
[![GitHub CI](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/xoflib/badge/?version=latest)](https://xoflib.readthedocs.io/en/latest/?badge=latest)

# xoflib

A Python package for the Shake and Ascon extendable-output functions (XOFs). Built using
[pyO3](https://github.com/PyO3/pyo3) bindings for the
[`sha3`](https://docs.rs/sha3/latest/sha3/) and [`ascon-hash`](https://crates.io/crates/ascon-hash) crates.

## Installation

This package is available as `xoflib` on
[PyPI](https://pypi.org/project/xoflib/):

```
pip install xoflib
```

## Algorithms

We currently have pyO3 bindings for the four Shake XOF available in the [`sha3`](https://crates.io/crates/sha3) crate as well as the Ascon XOFs from the [`ascon-hash`](https://crates.io/crates/ascon-hash) crate.

### Sha3

- [Shake128()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.Shake128)
- [Shake256()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.Shake256)
- [TurboShake128()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.TurboShake128)
- [TurboShake256()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.TurboShake256)

### Ascon

- [AsconXof()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.AsconXof)
- [AsconAXof()](https://xoflib.readthedocs.io/en/stable/xoflib.html#xoflib.AsconAXof)

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

### Sha3

We rely on the testing of the `sha3` crate for correctness of the Shake implementations. For API testing and consistency with `hashlib` we include some unittests for the XOFs exposed in our module: [tests/test_shake.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_shake.py)

### Ascon

`AsconXOF` and `AsconAXof` are both tested by comparing the output with the KAT vectors generated from [`pyascon`](https://github.com/meichlseder/pyascon). For more information, see the test file: [tests/test_ascon.py](https://github.com/GiacomoPope/xoflib/blob/main/tests/test_ascon.py)


## Rough Benchmarking

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
