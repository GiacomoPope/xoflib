import sys
if sys.version_info >= (3, 12):
    from collections.abc import Buffer
elif sys.version_info >= (3, 10):
    Buffer = bytes | bytearray | memoryview
else:
    from typing import ByteString as Buffer

class Shake128:
    def __init__(self, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "Shake128":
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge128:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

class Shake256:
    def __init__(self, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "Shake256":
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge256:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

class TurboShake128:
    def __init__(self, domain_sep: int, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "TurboShake128":
        ...

    def finalize(self) -> Sponge128:
        ...

class TurboSponge128:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

class TurboShake256:
    def __init__(self, domain_sep: int, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "TurboShake256":
        ...

    def finalize(self) -> Sponge128:
        ...

class TurboSponge256:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

def shake128(input_bytes: Buffer) -> Sponge128:
    ...

def shake256(input_bytes: Buffer) -> Sponge256:
    ...

def turbo_shake128(domain_sep: int, input_bytes: Buffer) -> TurboSponge128:
    ...

def turbo_shake256(domain_sep: int, input_bytes: Buffer) -> TurboSponge256:
    ...

class AsconXof:
    def __init__(self, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "AsconXof":
        ...

    def finalize(self) -> AsconSponge:
        ...

class AsconSponge:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

class AsconAXof:
    def __init__(self, input_bytes: Buffer | None = None):
        ...

    def absorb(self, input_bytes: Buffer) -> "AsconAXof":
        ...

    def finalize(self) -> AsconSponge:
        ...

class AsconASponge:
    def read(self, n: int) -> bytes:
        ...

    def read_into(self, buf: Buffer):
        ...

def ascon_xof(input_bytes: Buffer) -> AsconXof:
    ...

def ascona_xof(input_bytes: Buffer) -> AsconAXof:
    ...
