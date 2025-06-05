# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from cvp.values.proxies.callables import CallableProxyValue


@dataclass
class GraphicConfig:
    force_egl: Optional[bool] = None
    use_accelerate: Optional[bool] = None

    @property
    def force_egl_environ(self) -> str:
        return "1" if self.force_egl else "0"

    @property
    def use_accelerate_environ(self) -> str:
        return "1" if self.use_accelerate else "0"

    def create_force_egl_proxy(self):
        def _getter() -> Optional[bool]:
            return self.force_egl

        def _setter(value: Optional[bool]) -> None:
            self.force_egl = value

        return CallableProxyValue(_getter, _setter)

    def create_use_accelerate_proxy(self):
        def _getter() -> Optional[bool]:
            return self.use_accelerate

        def _setter(value: Optional[bool]) -> None:
            self.use_accelerate = value

        return CallableProxyValue(_getter, _setter)
