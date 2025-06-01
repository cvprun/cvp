# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import Optional, Tuple
from uuid import uuid4

from cvp.process.mapper import ProcessMapper
from cvp.process.process import Process
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.processes import ProcessesPath
from cvp.resources.subdirs.services import ServicesPath
from cvp.service.item import ServiceItem, ServiceKey, StreamInfo
from cvp.variables import SERVICE_NONAME


class ServiceManager(ResourceManager[ServiceKey, ServiceItem]):
    _processes: ProcessMapper[ServiceKey, Process]

    def __init__(
        self,
        path: ServicesPath,
        processes_path: ProcessesPath,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=ServiceKey,
            config_type=ServiceItem,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._processes_path = processes_path
        self._processes = ProcessMapper()

    def add_service(
        self,
        name=SERVICE_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[ServiceKey, ServiceItem]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        item = ServiceItem(uuid=uuid, name=name)
        assert uuid == str(item.key)

        self.add(item.key, item)
        return item.key, item

    def has_process(self, key: ServiceKey):
        return self._processes.__contains__(key)

    def get_process(self, key: ServiceKey):
        return self._processes.get(key)

    def spawnable(self, key: ServiceKey) -> bool:
        return self._processes.spawnable(key)

    def stoppable(self, key: ServiceKey) -> bool:
        return self._processes.stoppable(key)

    def removable(self, key: ServiceKey) -> bool:
        return self._processes.removable(key)

    def status(self, key: ServiceKey):
        return self._processes.status(key)

    def send_signal(self, key: ServiceKey, signum: int) -> None:
        return self._processes.send_signal(key, signum)

    def interrupt(self, key: ServiceKey) -> None:
        return self._processes.interrupt(key)

    def removable_pop(self, key: ServiceKey):
        return self._processes.removable_pop(key)

    def shutdown(self, timeout: Optional[float] = None):
        self._processes.shutdown(timeout)

    def spawn(self, key: ServiceKey):
        if self._processes.__contains__(key):
            raise KeyError(f"A process with key '{key}' is already running")
        process = self._spawn_new_process(self.__getitem__(key))
        self._processes[key] = process

    @staticmethod
    def _spawn_new_process(item: ServiceItem):
        args = item.normalize_commands
        if not args:
            raise ValueError("No command arguments provided to spawn the process")

        executable = args[0]
        if not os.path.isfile(executable):
            raise FileNotFoundError(f"Executable not found: '{executable}'")

        if item.cwd and not os.path.isdir(item.cwd):
            raise NotADirectoryError(f"Working directory does not exist: '{item.cwd}'")

        return Process(
            args=args,
            buffer_size=item.buffer_size,
            stdin=None,
            stdout=None,
            stderr=None,
            cwd=item.cwd or None,
            env=item.env or None,
            creation_flags=item.creation_flags,
            name=item.name or None,
        )

    def generate_stream_log_path(
        self,
        key: ServiceKey,
        stream: StreamInfo,
        dt: Optional[datetime] = None,
    ):
        return self._processes_path.generate_log_path(str(key), stream.name, dt)

    def get_pid_file_path(self, key: ServiceKey):
        return self._processes_path.get_pid_path(str(key))
