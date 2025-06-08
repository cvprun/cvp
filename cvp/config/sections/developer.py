# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any

from type_serialize import Serializable


@dataclass
class DeveloperConfig(Serializable):
    show_metrics: bool = False
    show_style: bool = False
    show_demo: bool = False

    _temp_debug: bool = False
    _temp_verbose: int = 0

    _persistent_debug: bool = False
    _persistent_verbose: int = 0

    def __serialize__(self) -> Any:
        return dict(
            debug=self._persistent_debug,
            verbose=self._persistent_verbose,
            show_metrics=self.show_metrics,
            show_style=self.show_style,
            show_demo=self.show_demo,
        )

    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.show_metrics = data.get("show_metrics", False)
        self.show_style = data.get("show_style", False)
        self.show_demo = data.get("show_demo", False)
        self._persistent_debug = data.get("debug", False)
        self._persistent_verbose = data.get("verbose", 0)
        self._temp_debug = self._persistent_debug
        self._temp_verbose = self._persistent_verbose

    @property
    def debug(self) -> bool:
        return self._temp_debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._temp_debug = value

    @property
    def verbose(self) -> int:
        return self._temp_verbose

    @verbose.setter
    def verbose(self, value: int) -> None:
        self._temp_verbose = value

    def rotate_verbose(self, *, max_verbose=3) -> None:
        self._temp_verbose += 1
        if max_verbose < self._temp_verbose:
            self._temp_verbose = 0

    @property
    def persistent_debug(self) -> bool:
        return self._persistent_debug

    @property
    def persistent_verbose(self) -> int:
        return self._persistent_verbose

    def set_persistent_debug(self, value: bool, *, update_temp=False) -> None:
        self._persistent_debug = value
        if update_temp:
            self._temp_debug = value

    def set_persistent_verbose(self, value: int, *, update_temp=False) -> None:
        self._persistent_verbose = value
        if update_temp:
            self._temp_verbose = value

    def flip_show_metrics(self) -> None:
        self.show_metrics = not self.show_metrics

    def flip_show_style(self) -> None:
        self.show_style = not self.show_style

    def flip_show_demo(self) -> None:
        self.show_demo = not self.show_demo
