# -*- coding: utf-8 -*-

from pygame import key as pg_key
from pygame.typing import RectLike


class Keyboardable:
    @staticmethod
    def key_get_focused():
        return pg_key.get_focused()

    @staticmethod
    def key_get_pressed():
        return pg_key.get_pressed()

    @staticmethod
    def key_get_just_pressed():
        return pg_key.get_just_pressed()

    @staticmethod
    def key_get_just_released():
        return pg_key.get_just_released()

    @staticmethod
    def key_get_mods():
        return pg_key.get_mods()

    @staticmethod
    def key_set_mods(mods: int):
        return pg_key.set_mods(mods)

    @staticmethod
    def key_set_repeat(delay=0, interval=0):
        return pg_key.set_repeat(delay, interval)

    @staticmethod
    def key_get_repeat():
        return pg_key.get_repeat()

    @staticmethod
    def key_name(key: int, use_compat=True):
        return pg_key.name(key, use_compat)

    @staticmethod
    def key_key_code(name: str):
        return pg_key.key_code(name)

    @staticmethod
    def key_start_text_input():
        return pg_key.start_text_input()

    @staticmethod
    def key_stop_text_input():
        return pg_key.stop_text_input()

    @staticmethod
    def key_set_text_input_rect(rect: RectLike):
        return pg_key.set_text_input_rect(rect)
