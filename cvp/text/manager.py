# -*- coding: utf-8 -*-

from typing import Optional, Tuple
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
    ) -> Tuple[TextKey, TextItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        if not path:
            path = str()
        assert isinstance(path, str)

        item = TextItem(uuid=uuid, path=path)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item
