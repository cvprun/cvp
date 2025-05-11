# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.canvas.canvas import Canvas, CanvasKey
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.canvases import CanvasesPath


class CanvasManager(ResourceManager[CanvasKey, Canvas]):
    def __init__(self, path: CanvasesPath, *, reload=False, raise_errors=False):
        super().__init__(
            key_type=CanvasKey,
            config_type=Canvas,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_new(
        self,
        workspace: Optional[str] = None,
        name: Optional[str] = None,
        opened=False,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[CanvasKey, Canvas]:
        uuid = uuid if uuid else str(uuid4())
        workspace = workspace if workspace else str()
        name = name if name else str()
        config = Canvas(uuid=uuid, workspace=workspace, name=name, opened=opened)
        self.add(config.key, config)
        return config.key, config
