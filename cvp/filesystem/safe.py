# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import NamedTuple, Optional, Union

from cvp.variables import SAFETY_FILE_SUFFIX_NEW, SAFETY_FILE_SUFFIX_OLD


class BackupPaths(NamedTuple):
    new: Path
    old: Path

    def validate_writable(self) -> None:
        if self.new.exists():
            raise FileExistsError(f"'{str(self.new)}' already exists")
        if self.old.exists():
            raise FileExistsError(f"'{str(self.old)}' already exists")

        if not os.access(self.new.parent, os.W_OK):
            raise PermissionError(f"'{str(self.new.parent)}' is not writable")
        if not os.access(self.old.parent, os.W_OK):
            raise PermissionError(f"'{str(self.old.parent)}' is not writable")

    def validate_readable(self) -> None:
        if self.new.exists():
            raise FileExistsError(f"'{str(self.new)}' already exists")
        if self.old.exists():
            raise FileExistsError(f"'{str(self.old)}' already exists")


def create_write_backup_paths(
    path: Union[str, PathLike[str]],
    *,
    suffix_new=SAFETY_FILE_SUFFIX_NEW,
    suffix_old=SAFETY_FILE_SUFFIX_OLD,
):
    new_path = Path(str(path) + suffix_new)
    old_path = Path(str(path) + suffix_old)
    return BackupPaths(new_path, old_path)


def write_text_safe(
    path: Union[str, PathLike[str]],
    data: str,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    suffix_new=SAFETY_FILE_SUFFIX_NEW,
    suffix_old=SAFETY_FILE_SUFFIX_OLD,
):
    backup_paths = create_write_backup_paths(
        path=path,
        suffix_new=suffix_new,
        suffix_old=suffix_old,
    )
    backup_paths.validate_writable()

    result = backup_paths.new.write_text(data, encoding, errors, newline)
    os.rename(path, backup_paths.old)
    os.rename(backup_paths.new, path)
    backup_paths.old.unlink()
    return result


def write_bytes_safe(
    path: Union[str, PathLike[str]],
    data: bytes,
    *,
    suffix_new=SAFETY_FILE_SUFFIX_NEW,
    suffix_old=SAFETY_FILE_SUFFIX_OLD,
):
    backup_paths = create_write_backup_paths(
        path=path,
        suffix_new=suffix_new,
        suffix_old=suffix_old,
    )
    backup_paths.validate_writable()

    result = backup_paths.new.write_bytes(data)
    os.rename(path, backup_paths.old)
    os.rename(backup_paths.new, path)
    backup_paths.old.unlink()
    return result


def read_text_safe(
    path: Union[str, PathLike[str]],
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    *,
    suffix_new=SAFETY_FILE_SUFFIX_NEW,
    suffix_old=SAFETY_FILE_SUFFIX_OLD,
):
    if not isinstance(path, Path):
        path = Path(path)
    assert isinstance(path, Path)

    backup_paths = create_write_backup_paths(
        path=path,
        suffix_new=suffix_new,
        suffix_old=suffix_old,
    )
    backup_paths.validate_readable()
    return path.read_text(encoding, errors)


def read_bytes_safe(
    path: Union[str, PathLike[str]],
    *,
    suffix_new=SAFETY_FILE_SUFFIX_NEW,
    suffix_old=SAFETY_FILE_SUFFIX_OLD,
):
    if not isinstance(path, Path):
        path = Path(path)
    assert isinstance(path, Path)

    backup_paths = create_write_backup_paths(
        path=path,
        suffix_new=suffix_new,
        suffix_old=suffix_old,
    )
    backup_paths.validate_readable()
    return path.read_bytes()
