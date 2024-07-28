class Shaker128:
    def __init__(self, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge128:
    def read(self, n: int) -> bytes:
        ...

class Shaker256:
    def __init__(self, input_bytes: bytes | None = None):
        ...

    def absorb(self, input_bytes: bytes) -> None:
        ...

    def finalize(self) -> Sponge128:
        ...

class Sponge256:
    def read(self, n: int) -> bytes:
        ...
