import hashlib
from random import Random


def create_rng(seed: int, name: str) -> Random:
    value = f"{seed}:{name}".encode("utf-8")

    digest = hashlib.sha256(value).digest()

    derived_seed = int.from_bytes(
        digest[:8],
        byteorder="big",
    )

    return Random(derived_seed)