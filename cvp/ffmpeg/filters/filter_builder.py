# -*- coding: utf-8 -*-

from io import StringIO
from typing import Any, List, Optional


class FilterBuilder:
    """Builder for FFmpeg filter graphs."""

    def __init__(self) -> None:
        self._filters: List[str] = []

    def add(self, filter_name: str, **kwargs: Any) -> "FilterBuilder":
        """Add a filter with optional parameters."""
        if kwargs:
            params = ":".join(f"{k}={v}" for k, v in kwargs.items() if v is not None)
            self._filters.append(f"{filter_name}={params}")
        else:
            self._filters.append(filter_name)
        return self

    def add_raw(self, filter_string: str) -> "FilterBuilder":
        """Add a raw filter string."""
        self._filters.append(filter_string)
        return self

    def build(self) -> str:
        """Build the filter graph string."""
        return ",".join(self._filters)

    def clear(self) -> None:
        """Clear all filters."""
        self._filters.clear()

    def __str__(self) -> str:
        return self.build()

    def __bool__(self) -> bool:
        return len(self._filters) > 0


class ComplexFilterBuilder:
    """Builder for FFmpeg complex filter graphs."""

    def __init__(self) -> None:
        self._chains: List[str] = []

    def chain(
        self,
        inputs: Optional[List[str]] = None,
        filters: Optional[List[str]] = None,
        outputs: Optional[List[str]] = None,
    ) -> "ComplexFilterBuilder":
        """Add a filter chain with optional input/output labels."""
        buffer = StringIO()

        if inputs:
            for inp in inputs:
                buffer.write(f"[{inp}]")

        if filters:
            buffer.write(",".join(filters))

        if outputs:
            for out in outputs:
                buffer.write(f"[{out}]")

        self._chains.append(buffer.getvalue())
        return self

    def add_chain(self, chain_string: str) -> "ComplexFilterBuilder":
        """Add a raw filter chain string."""
        self._chains.append(chain_string)
        return self

    def build(self) -> str:
        """Build the complex filter graph string."""
        return ";".join(self._chains)

    def clear(self) -> None:
        """Clear all chains."""
        self._chains.clear()

    def __str__(self) -> str:
        return self.build()

    def __bool__(self) -> bool:
        return len(self._chains) > 0


def make_filter(filter_name: str, *args: Any, **kwargs: Any) -> str:
    """Create a filter string with positional and keyword arguments."""
    parts: List[str] = []

    for arg in args:
        if arg is not None:
            parts.append(str(arg))

    for key, value in kwargs.items():
        if value is not None:
            parts.append(f"{key}={value}")

    if parts:
        return f"{filter_name}={':'.join(parts)}"
    return filter_name
