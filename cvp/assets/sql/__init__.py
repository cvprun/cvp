# -*- coding: utf-8 -*-

import os
from functools import lru_cache

from cvp.assets import get_assets_dir


@lru_cache
def get_sql_dir() -> str:
    return os.path.join(get_assets_dir(), "sql")


@lru_cache
def get_sql_chat_postgres_path() -> str:
    return os.path.join(get_sql_dir(), "chat.postgres.sql")


@lru_cache
def get_sql_chat_sqlite_path() -> str:
    return os.path.join(get_sql_dir(), "chat.sqlite.sql")
