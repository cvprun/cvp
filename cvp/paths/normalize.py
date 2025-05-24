# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import AnyStr, Union


def normalize_path(path: Union[AnyStr, PathLike[AnyStr]]) -> AnyStr:
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    return os.path.abspath(path)
