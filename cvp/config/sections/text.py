# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class TextConfig:
    default_encoding: str = "utf-8"
