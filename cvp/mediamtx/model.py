# -*- coding: utf-8 -*-

import os
from typing import Final

from cvp.assets.swaggers import get_swaggers_mediamtx_path
from cvp.swagger.generators.httpx_client import HttpxClientGenerator
from cvp.swagger.schemas.v3 import OpenAPIObject


def _read_mediamtx_json_text() -> str:
    with open(get_swaggers_mediamtx_path(), "rt", encoding="utf-8") as f:
        return f.read()


MEDIAMTX_SWAGGER_JSON_TEXT: Final[str] = _read_mediamtx_json_text()


def load_mediamtx_model() -> OpenAPIObject:
    return OpenAPIObject.model_validate_json(MEDIAMTX_SWAGGER_JSON_TEXT)


def generate_mediamtx_httpx_client() -> str:
    return HttpxClientGenerator(load_mediamtx_model()).generate()


def write_mediamtx_httpx_client(file: str) -> None:
    with open(file, "wt", encoding="utf-8") as f:
        f.write(generate_mediamtx_httpx_client())


def _default_write_mediamtx_httpx_client() -> None:
    package_dir = os.path.dirname(__file__)
    filename = "client.py"
    file = os.path.abspath(os.path.join(package_dir, filename))
    write_mediamtx_httpx_client(file)


if __name__ == "__main__":
    _default_write_mediamtx_httpx_client()
