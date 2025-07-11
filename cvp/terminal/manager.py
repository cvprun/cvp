# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.terminals import TerminalsPath
from cvp.terminal.item import TerminalItem, TerminalKey


class TerminalManager(ResourceManager[TerminalKey, TerminalItem]):
    def __init__(
        self,
        path: TerminalsPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=TerminalKey,
            config_type=TerminalItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[TerminalKey, TerminalItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = TerminalItem(uuid=uuid)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item
