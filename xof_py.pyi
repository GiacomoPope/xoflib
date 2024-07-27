class Sponge128:
    def read(n: int) -> bytes:
        ...

class Shake128:
    def absorb(input_bytes: bytes) -> None:
        ...

    def finalize() -> Sponge128:
        ...

class Sponge256:
    def read(n: int) -> bytes:
        ...

class Shake256:
    def absorb(input_bytes: bytes) -> None:
        ...

    def finalize() -> Sponge256:
        ...
