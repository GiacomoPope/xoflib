[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/GiacomoPope/xof-py/blob/main/LICENSE)
[![GitHub CI](https://github.com/GiacomoPope/xof-py/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/GiacomoPope/xof-py/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/xof-py/badge/?version=latest)](https://xof-py.readthedocs.io/en/latest/?badge=latest)

# xof-py

## Example

```py
>>> from xof import Shaker128
>>> Shake128 = Shaker128(b"a new XOF library").finalize()
>>> Shake128.read(16).hex()
'd071c7cdd2e2108ef8515922daf7e790913c1b75a9f8afd79b38f59d03ac52fe'
>>> Shake128.read(16).hex()
'15a8957dd9ea7d3beb8ddafbf085b9658c35fe353260dd05d9e9f1e7d0004f59'
```

## Tests

Could be expanded, currently just check random tests against hashlib

## Documentation

https://xof-py.readthedocs.io/

## Benchmark

```
10_000 calls with xof library: 0.014042854309082031
10_000 calls with hashlib: 0.022047996520996094
10_000 calls with pycryptodome: 0.029639005661010742
--------------------------------------------------------------------------------
1_000_000 single byte reads xof library: 0.18165993690490723
1_000_000 single byte reads pycryptodome: 1.1623139381408691
100_000 block reads xof library: 0.5895988941192627
100_000 block reads pycryptodome: 1.635364055633545
```
