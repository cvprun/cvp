# -*- coding: utf-8 -*-

from typing import Any, Dict, Iterable, Optional, Union
from urllib.parse import quote, urlencode


def format_path(
    path: str,
    /,
    path_kwargs: Optional[Dict[str, Any]] = None,
    queries: Optional[Dict[str, Any]] = None,
    *,
    quote_safe: Union[str, Iterable[int]] = "/",
) -> str:
    try:
        formatted_path = path.format(**(path_kwargs or {}))
    except KeyError as e:
        raise ValueError(f"Missing required path parameter: {e}")

    encoded_path = quote(formatted_path, safe=quote_safe)
    filtered_queries = {k: v for k, v in (queries or {}).items() if v is not None}

    if query_string := urlencode(filtered_queries):
        return f"{encoded_path}?{query_string}"
    else:
        return encoded_path
