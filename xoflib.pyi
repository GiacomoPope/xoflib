class Shake128:
    def __init__(self, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge128:
    def read(self, n: int) -> bytes:
        ...

class Shake256:
    def __init__(self, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge256:
    def read(self, n: int) -> bytes:
        ...

class TurboShake128:
    def __init__(self, domain_sep: int, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class TurboSponge128:
    def read(self, n: int) -> bytes:
        ...

class TurboShake256:
    def __init__(self, domain_sep: int, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class TurboSponge256:
    def read(self, n: int) -> bytes:
        ...
