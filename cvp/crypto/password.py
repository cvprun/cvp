# -*- coding: utf-8 -*-

from hashlib import pbkdf2_hmac
from typing import Final

DEFAULT_PBKDF2_HMAC_HASH_NAME: Final[str] = "sha256"
DEFAULT_PBKDF2_HMAC_ITERATIONS: Final[int] = 100000


def encrypt_password(password: str, salt: bytes) -> bytes:
    return pbkdf2_hmac(
        DEFAULT_PBKDF2_HMAC_HASH_NAME,
        bytes.fromhex(password),
        salt,
        DEFAULT_PBKDF2_HMAC_ITERATIONS,
    )
