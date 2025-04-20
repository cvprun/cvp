# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from uuid import uuid4

from cvp.media.config import MediaConfig
from cvp.process.manager import ProcessManager
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
        self._processes = ProcessManager()

    def add_config(
        self,
        name=MEDIA_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[str, MediaConfig]:
        uuid = uuid if uuid else str(uuid4())
        config = MediaConfig(uuid=uuid, name=name)
        self.add(uuid, config)
        return uuid, config

    def spawnable(self, key: str) -> bool:
        return self._processes.spawnable(key)

    def stoppable(self, key: str) -> bool:
        return self._processes.stoppable(key)

    def removable(self, key: str) -> bool:
        return self._processes.removable(key)

    def status(self, key: str):
        return self._processes.status(key)

    def interrupt(self, key: str) -> None:
        return self._processes.interrupt(key)

    def teardown_all(self, timeout: Optional[float] = None):
        self._processes.shutdown(timeout)

    def spawn_ffmpeg_with_file(self, key: str, file: str, width: int, height: int):
        if key in self._processes:
            raise KeyError(f"Key is exists: '{key}'")

        process = self._ffmpeg.spawn_with_file(key, file, width, height)
        self._processes[key] = process
        return process

    @property
    def processes(self):
        return self._processes

    def get_process(self, key: str):
        return self._processes.get(key)
