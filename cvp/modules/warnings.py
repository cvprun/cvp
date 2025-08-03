# -*- coding: utf-8 -*-

from io import StringIO
from logging import Logger
from typing import Optional
from warnings import catch_warnings


def hide_pkg_resources_deprecated_warning(
    logger: Optional[Logger] = None,
    details=False,
) -> None:
    with catch_warnings(record=True) as wms:
        # [Warning]
        # UserWarning: pkg_resources is deprecated as an API.
        # See https://setuptools.pypa.io/en/latest/pkg_resources.html
        # The pkg_resources package is slated for removal as early as 2025-11-30.
        # Refrain from using this package or pin to Setuptools<81.
        try:
            import pkg_resources  # noqa
        except ImportError:
            pass

        for wm in wms:
            buffer = StringIO()
            if details:
                buffer.write(f"<{wm.category.__name__} ")
                buffer.write(f"message='{str(wm.message)}' ")
                buffer.write(f"file={wm.filename}:{wm.lineno}>")
            else:
                buffer.write(str(wm.message))

            if logger is not None:
                logger.warning(buffer.getvalue())
