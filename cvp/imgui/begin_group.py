# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui


def begin_group() -> None:
    imgui.begin_group()


def end_group() -> None:
    imgui.end_group()


@contextmanager
def begin_group_context():
    begin_group()
    try:
        yield
    finally:
        end_group()
