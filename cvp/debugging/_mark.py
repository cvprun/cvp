# -*- coding: utf-8 -*-

from typing import Optional


class Mark:
    """
    This is a list of symbol pivots for navigating to code locations responsible for
    specific functionality.
    """

    __slots__ = ("assertion", "message")

    def __init__(self, message: Optional[str] = None, *, assertion=True):
        self.assertion = assertion
        self.message = message if message else str()

    @classmethod
    def from_mark(cls, mark: "Mark"):
        return cls(mark.message, assertion=mark.assertion)

    def __bool__(self):
        """
        Should be confirmed when added with an `assert`
        """
        return self.assertion

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.message}'>"


class MarkTodo(Mark):
    pass


class MarkBeginRegion(Mark):
    pass


class MarkEndRegion(Mark):
    pass


class MarkBeginEndPair(Mark):
    pass
