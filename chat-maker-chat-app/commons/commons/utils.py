from hashlib import sha256
from typing import Set


def hash_set(s: Set) -> str:
    return sha256(str(s).encode()).hexdigest()
