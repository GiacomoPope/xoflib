# xof-py

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
maturin develop
```

You should now be able to use the package:

```
(.env) Jack: xof-py % python3
Python 3.12.4 (main, Jun  6 2024, 18:26:44) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from xof_py import sum_as_string
>>> sum_as_string(1, 2)
'3'
```
