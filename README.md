# xof-py


## Documentation

https://xof-py.readthedocs.io/en/latest/generated/xof.html


## Building with Maturin

- https://pyo3.rs/v0.22.2/
- https://github.com/PyO3/maturin

First set up a virtual environment:

```
python3 -m venv .env
source .env/bin/activate
```

Then install maturin

```
pip install maturin
```

Then to build the package run

```
maturin develop --release
```

You should now be able to use the package:

```py
>>> from xof import pyo3_shake_128
>>> pyo3_shake_128(b"cryptohack", 100).hex()
'8d043455562ebedd1b3fcf5b0e0a058091752d161e7eef40364a565aacb3b5d3bbefa804de6087e77c4c211ef57ab83869e3e18627f8421540ae9a8b61da847d0da513c56c5feba397ab2b4a1a2ef67c6f17162c8dfdb41901ad70bca8195fd35bcea259'
```

### Speed Test

```
(.env) Jack: xof-py % python3 speed_test.py               
10_000 calls with rust sha3: 0.08595705032348633
10_000 calls with hashlib: 0.06728601455688477

10_000 one block calls with rust sha3: 0.01061105728149414
10_000 one block calls with hashlib: 0.012787818908691406

10_000 2 block calls with rust sha3: 0.016810894012451172
10_000 2 block calls with hashlib: 0.01606297492980957

10_000 n block calls with rust sha3: 0.08771300315856934
10_000 n block calls with hashlib: 0.07766127586364746
```
