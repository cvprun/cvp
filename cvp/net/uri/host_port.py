# -*- coding: utf-8 -*-


def has_scheme(address: str) -> bool:
    return "://" in address
