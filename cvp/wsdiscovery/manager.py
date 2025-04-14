# -*- coding: utf-8 -*-

from typing import Dict, List, NewType, Tuple

from type_serialize import deserialize, serialize

from cvp.logging.logging import logger
from cvp.resources.subdirs.wsdiscovery import WsDiscoveryPath
from cvp.wsdiscovery.wsd import WsDiscovery

WsDiscoveryFilename = NewType("WsDiscoveryFilename", str)


class WsDiscoveryManager(Dict[WsDiscoveryFilename, WsDiscovery]):
    def __init__(self, path: WsDiscoveryPath, *, reload=False, raise_errors=False):
        super().__init__()
        self._path = path

        if reload:
            self.reload_all_files(raise_errors=raise_errors)

    @property
    def path(self):
        return self._path

    def gen_filename_with_epr(self, epr: str) -> WsDiscoveryFilename:
        return WsDiscoveryFilename(self._path.object_path(epr).name)

    def read_serialized_object(self, filename: WsDiscoveryFilename) -> WsDiscovery:
        result = deserialize(self._path.read_object(filename), WsDiscovery)
        logger.info(f"Read from wsd config file: '{filename}'")
        return result

    def write_serialized_object(
        self,
        wsd: WsDiscovery,
        filename: WsDiscoveryFilename,
    ) -> int:
        result = self._path.write_object(serialize(wsd), filename)
        logger.info(f"Wrote to wsd config file: '{filename}'")
        return result

    def filenames(self) -> List[WsDiscoveryFilename]:
        return [WsDiscoveryFilename(x) for x in self._path.find_object_filenames()]

    def read_all_files(
        self,
        *,
        raise_errors=False,
    ) -> Dict[WsDiscoveryFilename, WsDiscovery]:
        result = dict()
        for filename in self.filenames():
            try:
                result[filename] = self.read_serialized_object(filename)
            except BaseException as e:
                if raise_errors:
                    raise
                else:
                    logger.error(f"Failed to read wsd file: '{filename}'")
                    result[filename] = WsDiscovery(error=str(e))
        return result

    def write_all_files(self) -> None:
        for filename, wsd in self.items():
            if wsd.has_error:
                logger.warning(
                    f"Skip write wsd file: '{filename}'"
                    f" because has error: {wsd.error}"
                )
                continue

            self.write_serialized_object(wsd, filename)

    def write(self, filename: WsDiscoveryFilename) -> int:
        wsd = self.__getitem__(filename)
        return self.write_serialized_object(wsd, filename)

    def read(self, filename: WsDiscoveryFilename):
        wsd = self.read_serialized_object(filename)
        self.__setattr__(filename, wsd)
        return wsd

    def remove(self, filename: WsDiscoveryFilename) -> None:
        self.__delitem__(filename)
        self._path.remove_object(filename)
        logger.info(f"Removed wsd config file: '{filename}'")

    def exists(self, filename: WsDiscoveryFilename) -> bool:
        return (self._path / filename).is_file()

    def reload_all_files(self, *, raise_errors=False) -> None:
        try:
            result = self.read_all_files(raise_errors=raise_errors)
        except:  # noqa
            raise
        else:
            self.clear()
            self.update(result)

    def add(self, wsd: WsDiscovery) -> Tuple[WsDiscoveryFilename, WsDiscovery]:
        filename = self.gen_filename_with_epr(wsd.epr)
        self.__setitem__(filename, wsd)
        return filename, wsd
