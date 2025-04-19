# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.keyring.details import KEYRING_SAGECIPHER


@dataclass
class KeyringConfig:
    backend: str = KEYRING_SAGECIPHER
