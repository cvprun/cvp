# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import NamedTuple

from cvp.keyring import details


@unique
class KeyringBackendName(StrEnum):
    chainer = details.KEYRING_CHAINER
    encrypted = details.KEYRING_ENCRYPTED
    fail = details.KEYRING_FAIL
    kwallet = details.KEYRING_KWALLET
    macos = details.KEYRING_MACOS
    null = details.KEYRING_NULL
    plain_text = details.KEYRING_PLAIN_TEXT
    sagecipher = details.KEYRING_SAGECIPHER
    secret_service = details.KEYRING_SECRET_SERVICE
    windows = details.KEYRING_WINDOWS


class ServiceKey(NamedTuple):
    service: str
    key: str


@unique
class ServiceName(StrEnum):
    supabase = auto()
    onvif = auto()


@unique
class SupabaseKey(StrEnum):
    supabase_key = auto()
    password = auto()
