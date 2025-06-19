# -*- coding: utf-8 -*-

from typing import Final

from cvp.assets.swaggers import get_swaggers_mediamtx_path
from cvp.swagger.schemas.v3 import OpenAPIObject


def _read_mediamtx_json_text() -> str:
    with open(get_swaggers_mediamtx_path(), "rt", encoding="utf-8") as f:
        return f.read()


MEDIAMTX_SWAGGER_JSON_TEXT: Final[str] = _read_mediamtx_json_text()


def load_mediamtx_model() -> OpenAPIObject:
    return OpenAPIObject.model_validate_json(MEDIAMTX_SWAGGER_JSON_TEXT)
