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
>>> from xoflib import Shaker128
>>> shake128 = Shaker128(b"a new XOF library")
>>> shake128.absorb(b"written using pyO3 bindings")
>>> xof = shake128.finalize()
>>> xof.read(16).hex()
'1301cd080b034973e961d585330b9e0c'
>>> xof.read(16).hex()
'1af56b984d09bce5a6c07da3f3b953bd'
```

The `TurboShake128` and `TurboShake256` XOFs additionally require a domain separation:

```py
>>> from xoflib import TurboShaker256
>>> domain_sep = 123 # should be between (1, 127)
>>> turbo256 = TurboShaker256(domain_sep)
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

We find that `xoflib` performs equally with `hashlib` and is faster than `pycryptodome`.

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
Benchmarking Shake128: 
================================================================================
Requesting 1 bytes from XOF 10000 times
xoflib: 0.71s
hashlib (single call): 0.66s
hashlib (streaming): 0.88s
pycryptodome: 2.12s
================================================================================
Requesting 100 bytes from XOF 10000 times
xoflib: 8.67s
hashlib (single call): 7.69s
hashlib (streaming): 10.06s
pycryptodome: 11.15s
================================================================================
Requesting 1000 bytes from XOF 1000 times
xoflib: 6.77s
hashlib (single call): 6.62s
hashlib (streaming): 7.22s
pycryptodome: 6.33s
================================================================================
Requesting 10000 bytes from XOF 1000 times
xoflib: 6.32s
hashlib (single call): 6.37s
hashlib (streaming): 6.51s
pycryptodome: 6.45s
================================================================================
Requesting 32 bytes from XOF 100000 times
xoflib: 2.80s
hashlib (single call): 2.69s
hashlib (streaming): 2.95s
pycryptodome: 4.04s
================================================================================
```

For more information, see the file [`benchmarks/benchmark_xof.py`](benchmarks/benchmark_xof.py).
