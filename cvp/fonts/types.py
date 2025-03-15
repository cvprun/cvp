# -*- coding: utf-8 -*-

from types import MappingProxyType
from typing import NewType

IconCode = NewType("IconCode", str)
IconMappingProxy = MappingProxyType[str, IconCode]
