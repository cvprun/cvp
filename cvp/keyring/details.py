# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from os import PathLike
from typing import Final, Optional, TypeGuard, Union

import keyring
from keyring import core
from keyring.backend import KeyringBackend, get_all_keyring
from keyring.credentials import Credential
from keyrings.alt.file_base import FileBacked

from cvp.logging.logging import logger

KEYRING_CHAINER: Final[str] = "keyring.backends.chainer.ChainerBackend"
KEYRING_ENCRYPTED: Final[str] = "keyrings.alt.file.EncryptedKeyring"
KEYRING_FAIL: Final[str] = "keyring.backends.fail.Keyring"
KEYRING_KWALLET: Final[str] = "keyring.backends.kwallet.DBusKeyring"
KEYRING_MACOS: Final[str] = "keyring.backends.macOS.Keyring"
KEYRING_NULL: Final[str] = "keyring.backends.null.Keyring"
KEYRING_PLAIN_TEXT: Final[str] = "keyrings.alt.file.PlaintextKeyring"
KEYRING_SAGECIPHER: Final[str] = "sagecipher.keyring.Keyring"
KEYRING_SECRET_SERVICE: Final[str] = "keyring.backends.SecretService.Keyring"
KEYRING_WINDOWS: Final[str] = "keyring.backends.Windows.WinVaultKeyring"


def is_valid_sagecipher() -> bool:
    from paramiko import Agent

    return bool(Agent().get_keys())


def get_keyring_name(backend: KeyringBackend) -> str:
    return f"{type(backend).__module__}.{type(backend).__name__}"


def set_keyring(backend: KeyringBackend) -> None:
    keyring.set_keyring(backend)


def get_keyring() -> KeyringBackend:
    return keyring.get_keyring()


def load_keyring(name: str):
    return core.load_keyring(name)


@contextmanager
def keyring_context(backend: Optional[Union[str, KeyringBackend]] = None):
    origin_backend = get_keyring()
    try:
        if backend is not None:
            if isinstance(backend, KeyringBackend):
                set_keyring(backend)
            elif isinstance(backend, str):
                set_keyring(load_keyring(backend))
            else:
                raise TypeError(f"Invalid backend type: {type(backend).__name__}")
        yield get_keyring()
    finally:
        set_keyring(origin_backend)


def list_keyring():
    return get_all_keyring()


def list_keyring_names():
    return [get_keyring_name(k) for k in get_all_keyring()]


def list_keyring_map():
    return {get_keyring_name(k): k for k in get_all_keyring()}


def set_password(service: str, username: str, password: str) -> None:
    keyring.set_password(service, username, password)


def get_password(service: str, username: str) -> Optional[str]:
    password = keyring.get_password(service, username)
    if password is None:
        return None
    if isinstance(password, str):
        return password
    elif isinstance(password, bytes):
        return str(password, encoding="utf-8")
    else:
        raise TypeError(f"Unsupported password type: {type(password).__name__}")


def get_credential(service: str, username: str) -> Optional[Credential]:
    return keyring.get_credential(service, username)


def delete_password(service: str, username: str) -> None:
    keyring.delete_password(service, username)
    logger.info(f"Delete password: {service}.{username}")


def is_file_backed(backend: KeyringBackend) -> TypeGuard[FileBacked]:
    return isinstance(backend, FileBacked)


def set_file_path(backend: KeyringBackend, path: Union[str, PathLike[str]]) -> None:
    if not isinstance(backend, FileBacked):
        raise TypeError(f"Invalid backend type: {type(backend).__name__}")

    type(backend).file_path = path


def set_all_filepath(data_dir: Union[str, PathLike[str]], extension=".cfg") -> None:
    for backend in get_all_keyring():
        if not is_file_backed(backend):
            continue

        filename = get_keyring_name(backend) + extension
        filepath = os.path.join(data_dir, filename)
        set_file_path(backend, filepath)
