# -*- coding: utf-8 -*-

from io import StringIO
from urllib.parse import urlparse


def replace_netloc(src_url: str, host_url: str) -> str:
    src = urlparse(src_url)
    new = urlparse(host_url)

    buffer = StringIO()
    buffer.write(src.scheme)
    buffer.write("://")

    if new.hostname:
        buffer.write(new.hostname)
    if new.port:
        buffer.write(f":{new.port}")

    if src.path:
        assert src.path.startswith("/")
        buffer.write(src.path)

    if src.query:
        assert not src.query.startswith("?")
        buffer.write(f"?{src.query}")

    if src.fragment:
        assert not src.query.startswith("#")
        buffer.write(f"#{src.fragment}")

    return buffer.getvalue()


def is_file_scheme(address: str):
    try:
        # https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
        return urlparse(address).scheme in ("file", "filesystem")
    except:  # noqa
        return False
