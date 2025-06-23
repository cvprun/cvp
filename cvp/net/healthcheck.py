# -*- coding: utf-8 -*-

from typing import Union

import requests


def is_connect_to_server(url: Union[str, bytes], timeout: float) -> bool:
    try:
        requests.get(url, timeout=timeout)
        return True
    except:  # noqa
        return False
