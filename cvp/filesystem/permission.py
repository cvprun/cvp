# -*- coding: utf-8 -*-

import os
import stat

from cvp.filesystem.types import PathLike


def change_readable(path: PathLike):
    os.chmod(path, stat.S_IRUSR)


def change_writable(path: PathLike):
    os.chmod(path, stat.S_IWUSR)


def change_executable(path: PathLike):
    os.chmod(path, stat.S_IXUSR)


def is_readable_file(path: PathLike) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.R_OK):
        return False
    return True


def is_writable_file(path: PathLike) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.W_OK):
        return False
    return True


def is_executable_file(path: PathLike) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.X_OK):
        return False
    return True


def is_readable_dir(path: PathLike) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.R_OK):
        return False
    return True


def is_writable_dir(path: PathLike) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.W_OK):
        return False
    return True


def is_executable_dir(path: PathLike) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.X_OK):
        return False
    return True


def test_directory(path: PathLike) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{path!r}' does not exist")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path!r}' is not a directory")


def test_file(path: PathLike) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{path!r}' does not exist")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"'{path!r}' is not a file")


def test_readable(path: PathLike) -> None:
    if not os.access(path, os.R_OK):
        raise PermissionError(f"'{path!r}' is not readable")


def test_writable(path: PathLike) -> None:
    if not os.access(path, os.W_OK):
        raise PermissionError(f"'{path!r}' is not writable")


def test_rw(path: PathLike) -> None:
    test_readable(path)
    test_writable(path)


def test_readable_directory(path: PathLike) -> None:
    test_directory(path)
    test_readable(path)


def test_writable_directory(path: PathLike) -> None:
    test_directory(path)
    test_writable(path)


def test_rw_directory(path: PathLike) -> None:
    test_directory(path)
    test_rw(path)


def test_readable_file(path: PathLike) -> None:
    test_file(path)
    test_readable(path)


def test_writable_file(path: PathLike) -> None:
    test_file(path)
    test_writable(path)


def test_rw_file(path: PathLike) -> None:
    test_file(path)
    test_rw(path)
