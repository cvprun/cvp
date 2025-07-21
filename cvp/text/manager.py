# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Tuple, Union
from uuid import uuid4

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.texts import TextsPath
from cvp.text.item import TextItem, TextKey


class TextManager(ResourceManager[TextKey, TextItem]):
    def __init__(
        self,
        path: TextsPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=TextKey,
            config_type=TextItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        *,
        uuid: Optional[str] = None,
        path: Optional[str] = None,
        encoding="utf-8",
        errors="strict",
        opened=True,
        flags=0,
    ) -> Tuple[TextKey, TextItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        if not path:
            path = str()
        assert isinstance(path, str)

        item = TextItem(
            uuid=uuid,
            path=path,
            encoding=encoding,
            errors=errors,
            opened=opened,
            flags=flags,
        )
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

    def find_with_path(self, path: Union[str, Path]):
        if not isinstance(path, Path):
            path = Path(path)
        assert isinstance(path, Path)
        path = path.resolve()

        for item in self.values():
            if Path(item.path).resolve() == path:
                return item

        raise ValueError("No item found with the given path")
