from hashlib import sha256
from typing import List


def hash_list(s: List) -> str:
    return sha256(str(s).encode()).hexdigest()
