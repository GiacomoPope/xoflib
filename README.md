[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/GiacomoPope/xoflib/blob/main/LICENSE)
[![GitHub CI](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/xoflib/badge/?version=latest)](https://xoflib.readthedocs.io/en/latest/?badge=latest)

# xoflib

A Python package for the Shake extendable-output functions (XOFs): Shake128,
Shake256 and the turbo variants. Built using
[pyO3](https://github.com/PyO3/pyo3) bindings for the
[`sha3`](https://docs.rs/sha3/latest/sha3/) crate.

## Algorithms

We currently have pyO3 bindings for the four XOF available in the `sha3` crate:

- `Shake128`
- `Shake256`
- `TurboShake128`
- `TurboShake256`

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

There is currently partial coverage for testing the bindings in `tests/`. The `sha3` crate which we bind to is thoroughly tested.

## Documentation

https://xoflib.readthedocs.io/

## Rough Benchmark

```
10_000 calls (read(1, 500)) with xoflib: 0.014404773712158203
10_000 calls (read(1, 500)) with hashlib: 0.02388787269592285
10_000 calls (read(1, 500)) with pycryptodome: 0.028993844985961914
--------------------------------------------------------------------------------
1_000_000 single byte reads with xoflib: 0.16383790969848633
1_000_000 single byte reads pycryptodome: 1.172316312789917
100_000 block reads with xoflib: 0.6025588512420654
100_000 block reads pycryptodome: 1.6401760578155518
--------------------------------------------------------------------------------
10_000 calls (read(1, 5000)) with xoflib Shake128: 0.07348895072937012
10_000 calls (read(1, 5000)) with xoflib Shake256: 0.08775138854980469
10_000 calls (read(1, 5000)) with xoflib TurboShake128: 0.04633498191833496
10_000 calls (read(1, 5000)) with xoflib TurboShake256: 0.056485891342163086
```

For more information, see the file [`benchmarks/benchmark_xof.py`](benchmarks/benchmark_xof.py).
