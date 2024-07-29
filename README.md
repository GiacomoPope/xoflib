[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/GiacomoPope/xoflib/blob/main/LICENSE)
[![GitHub CI](https://github.com/GiacomoPope/xoflib/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/GiacomoPope/xoflib/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/xoflib/badge/?version=latest)](https://xoflib.readthedocs.io/en/latest/?badge=latest)

# xoflib

A Python package for the Shake extendable-output functions (XOFs): Shake128,
Shake256 and the turbo variants. Built using
[pyO3](https://github.com/PyO3/pyo3) bindings for the
[`sha3`](https://docs.rs/sha3/latest/sha3/) crate.

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

## Example Usage

```py
>>> from xoflib import Shaker128
>>> Shake128 = Shaker128(b"a new XOF library").finalize()
>>> Shake128.read(16).hex()
'd071c7cdd2e2108ef8515922daf7e790913c1b75a9f8afd79b38f59d03ac52fe'
>>> Shake128.read(16).hex()
'15a8957dd9ea7d3beb8ddafbf085b9658c35fe353260dd05d9e9f1e7d0004f59'
```

## Tests

There is currently partial coverage for testing the bindings in `tests/`. The `sha3` crate which we bind to is thoroughly tested.

## Documentation

https://xoflib.readthedocs.io/

## Rough Benchmark

```
10_000 calls with xoflib: 0.014042854309082031
10_000 calls with hashlib: 0.022047996520996094
10_000 calls with pycryptodome: 0.029639005661010742
--------------------------------------------------------------------------------
1_000_000 single byte reads xoflib: 0.18165993690490723
1_000_000 single byte reads pycryptodome: 1.1623139381408691
100_000 block reads xoflib: 0.5895988941192627
100_000 block reads pycryptodome: 1.635364055633545
```

For more information, see the file [`benchmarks/benchmark_xof.py`](benchmarks/benchmark_xof.py).
