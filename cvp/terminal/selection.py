# -*- coding: utf-8 -*-

from typing import Optional

from cvp.terminal.coord import TerminalCoord


class TerminalSelection:
    def __init__(
        self,
        begin: Optional[TerminalCoord] = None,
        end: Optional[TerminalCoord] = None,
    ):
        self.begin = begin
        self.end = end

    @classmethod
    def from_raw(
        cls,
        begin_lineno: int,
        begin_column: int,
        end_lineno: int,
        end_column: int,
    ):
        begin = TerminalCoord(begin_lineno, begin_column)
        end = TerminalCoord(end_lineno, end_column)
        return cls(begin, end)

    @classmethod
    def from_lineno(cls, lineno: int):
        return cls(TerminalCoord(lineno, 1), TerminalCoord(lineno + 1, 0))

    @property
    def normalize(self):
        if self.begin is None or self.end is None:
            raise ValueError("Selection is not set")

        if self.begin <= self.end:
            return self.__class__(self.begin, self.end)
        else:
            return self.__class__(self.end, self.begin)

    @property
    def normalize_tuple(self):
        begin, end = self.normalize
        assert isinstance(begin, TerminalCoord)
        assert isinstance(end, TerminalCoord)
        return begin, end

    @property
    def exists(self) -> bool:
        return self.begin is not None and self.end is not None

    @property
    def has_area(self) -> bool:
        if not self.exists:
            return False

        begin = self.begin
        end = self.end
        assert isinstance(begin, TerminalCoord)
        assert isinstance(end, TerminalCoord)
        return begin.lineno != end.lineno or begin.column != end.column

    def __bool__(self) -> bool:
        return self.exists

    def __iter__(self):
        yield self.begin
        yield self.end

    def __eq__(self, other) -> bool:
        if not isinstance(other, TerminalSelection):
            return False

        return self.begin == other.begin and self.end == other.end

    def __repr__(self):
        return f"<{type(self).__name__} begin={self.begin}, end={self.end}>"

    def __str__(self):
        return f"{self.begin}~{self.end}"

    def clear_begin(self) -> None:
        self.begin = None

    def clear_end(self) -> None:
        self.end = None

    def clear(self) -> None:
        self.begin = None
        self.end = None

    def set_begin(self, lineno: int, column: int) -> None:
        self.begin = TerminalCoord(lineno, column)

    def set_end(self, lineno: int, column: int) -> None:
        self.end = TerminalCoord(lineno, column)

    def set_line_range(self, lineno_begin: int, lineno_end: int) -> None:
        if lineno_end <= lineno_begin:
            raise ValueError("lineno_end must be greater than lineno_begin")

        self.begin = TerminalCoord(lineno_begin, 1)
        self.end = TerminalCoord(lineno_end, 0)

    def contain_with(self, lineno: int, column: int, width=1) -> bool:
        if width == 0:
            raise ValueError("width must not be 0")

        for i in range(abs(width)):
            if 0 < width:
                offset = i  # Right direction
            else:
                offset = -1 * (i + 1)  # Left direction

            if not self.contain_with_coord(TerminalCoord(lineno, column + offset)):
                return False

        return True

    def contain_with_coord(self, coord: TerminalCoord) -> bool:
        try:
            begin, end = self.normalize
            return begin <= coord < end
        except ValueError:
            return False

    def __contains__(self, item):
        if isinstance(item, TerminalCoord):
            return self.contain_with_coord(item)
        elif isinstance(item, tuple) and len(item) == 2:
            if not isinstance(item[0], int):
                raise TypeError("The first element of the tuple must be an integer")
            if not isinstance(item[1], int):
                raise TypeError("The second element of the tuple must be an integer")
            return self.contain_with(item[0], item[1])
        elif isinstance(item, int):
            return self.contain_with_lineno(item)
        else:
            raise TypeError("The item must be an integer or a tuple")

    def contain_with_lineno(self, lineno: int) -> bool:
        try:
            begin, end = self.normalize
            return begin.lineno <= lineno < end.lineno
        except ValueError:
            return False

    def clip_lineno(self, lineno: int, *, column_end: Optional[int] = None):
        if not self.exists:
            return self.__class__()

        begin, end = self.normalize_tuple
        assert begin is not None
        assert end is not None

        if lineno < begin.lineno:
            return self.__class__()
        if end.lineno < lineno:
            return self.__class__()

        assert begin.lineno <= lineno <= end.lineno

        if begin.lineno == lineno:
            begin_lineno = lineno
            begin_column = begin.column
        else:
            assert begin.lineno < lineno
            begin_lineno = lineno
            begin_column = 1

        if end.lineno == lineno:
            end_lineno = lineno
            end_column = end.column
        else:
            assert lineno < end.lineno
            if column_end is not None:
                end_lineno = lineno
                end_column = column_end
            else:
                end_lineno = lineno + 1
                end_column = 0

        return self.__class__.from_raw(
            begin_lineno,
            begin_column,
            end_lineno,
            end_column,
        )
