# -*- coding: utf-8 -*-

import os
import re
from importlib import import_module
from types import ModuleType


def get_module_directory(module: ModuleType) -> str:
    module_path = getattr(module, "__path__", None)
    if module_path:
        assert isinstance(module_path, list)
        return module_path[0]

    module_file = getattr(module, "__file__", None)
    if module_file:
        assert isinstance(module_file, str)
        return os.path.dirname(module_file)

    raise RuntimeError(f"The '{module.__name__}' module path is unknown")


def find_pygame_library_path(library_name: str) -> str:
    pygame = import_module("pygame")

    pygame_module_dir = get_module_directory(pygame)
    if pygame_module_dir[-1] == "/":
        pygame_module_dir = pygame_module_dir[:-1]

    suffix = "_ce" if pygame.IS_CE else ""
    pygame_lib_module_dir = pygame_module_dir + suffix + ".libs"
    if not os.path.isdir(pygame_lib_module_dir):
        raise FileNotFoundError(f"Not found module directory: {pygame_lib_module_dir}")

    regex_pattern = r"^{name}-[0-9A-Fa-f.]+\.so\.[0-9.]+$".format(name=library_name)
    matcher = re.compile(regex_pattern)

    for file in os.listdir(pygame_lib_module_dir):
        if matcher.match(file):
            return os.path.join(pygame_lib_module_dir, file)

    raise FileNotFoundError(f"Not found '{library_name}' library")


# noinspection SpellCheckingInspection
def find_libsdl2_path() -> str:
    return find_pygame_library_path("libSDL2-2")


if __name__ == "__main__":
    print(f"libSDL2 path: '{find_libsdl2_path()}'")
