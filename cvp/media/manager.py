# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.media.config import MediaConfig
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.medias import MediasPath
from cvp.variables import MEDIA_NONAME


class MediaManager(ResourceManager[MediaConfig]):
    def __init__(self, path: MediasPath, *, reload=False, raise_errors=False):
        super().__init__(
            cls=MediaConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )

    def add_config(
        self,
        name=MEDIA_NONAME,
        *,
        key: Optional[str] = None,
    ) -> Tuple[str, MediaConfig]:
        key = key if key else str(uuid4())
        config = MediaConfig(uuid=key, name=name)
        self.add(key, config)
        return key, config
