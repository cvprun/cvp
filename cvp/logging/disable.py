# -*- coding: utf-8 -*-

import logging
from contextlib import contextmanager


@contextmanager
def disable_logging(level=logging.CRITICAL):
    previous_level = logging.root.manager.disable
    logging.disable(level)
    try:
        yield
    finally:
        logging.disable(previous_level)
