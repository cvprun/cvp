# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.keyring.details import KEYRING_SAGECIPHER


@dataclass
class KeyringConfig:
    backend: str = field(default_factory=lambda: KEYRING_SAGECIPHER)
