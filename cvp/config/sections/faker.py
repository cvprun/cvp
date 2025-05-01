# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from functools import lru_cache
from locale import getlocale
from secrets import choice
from string import ascii_letters, digits

from cvp.variables import FAKER_REPEAT, FAKER_SEED_LENGTH, FAKER_SEPARATOR


@lru_cache
def _default_locale() -> str:
    locale = getlocale()[0]
    return locale if locale else str()


def _random_seed(size=FAKER_SEED_LENGTH):
    return str().join(choice(ascii_letters + digits) for _ in range(size))


@dataclass
class FakerConfig:
    seed: str = field(default_factory=lambda: _random_seed())
    repeat: int = FAKER_REPEAT
    separator: str = FAKER_SEPARATOR
    locale: str = field(default_factory=_default_locale)

    @property
    def escaped_separator(self) -> str:
        return self.separator.encode("utf-8").decode("unicode_escape")

    def update_random_seed(self):
        self.seed = _random_seed()
