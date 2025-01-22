# -*- coding: utf-8 -*-

import os
from concurrent.futures import Executor
from copy import deepcopy
from enum import IntEnum, auto, unique
from ssl import SSLContext
from threading import Lock
from time import time
from typing import NamedTuple, Optional, Union

from cvp.logging.logging import download_logger as logger
from cvp.resources.download.archive import DownloadArchive


@unique
class DownloadStep(IntEnum):
    prepare = auto()
    request_content_length = auto()
    download_streaming = auto()
    checksum = auto()
    extract = auto()
    done = auto()


class DownloadState(NamedTuple):
    step: DownloadStep
    content_length: int
    download_bytes: int

    def __str__(self):
        return f"step={self.step},content={self.download_bytes}/{self.content_length}"


class DownloadRunner:
    _exception: Optional[BaseException]

    def __init__(
        self,
        executor: Executor,
        downloader: DownloadArchive,
        download_timeout: Optional[float] = None,
        verify_checksum=True,
        follow_redirects=True,
        verify: Union[str, bool, SSLContext] = True,
    ):
        self._downloader = downloader
        self._download_timeout = download_timeout
        self._verify_checksum = verify_checksum
        self._follow_redirects = follow_redirects
        self._verify = verify

        self._lock = Lock()
        self._step = DownloadStep.prepare
        self._content_length = 0
        self._download_bytes = 0
        self._exception = None

        self._future = executor.submit(self._runner)

    @property
    def future(self):
        return self._future

    @property
    def state(self):
        with self._lock:
            return DownloadState(
                DownloadStep(self._step),
                int(self._content_length),
                int(self._download_bytes),
            )

    @property
    def exception(self) -> Optional[BaseException]:
        with self._lock:
            return deepcopy(self._exception)

    def _runner(self) -> None:
        logger.info(f"{type(self).__name__} start")
        try:
            self._streaming_main()
        except BaseException as e:
            logger.error(e)
            with self._lock:
                self._exception = e
        finally:
            with self._lock:
                self._step = DownloadStep.done
            logger.info(f"{type(self).__name__} done")

    def _streaming_main(self) -> None:
        logger.debug(f"{type(self).__name__} any_extract_files check ...")

        if self._downloader.any_extract_files:
            raise FileExistsError("The result file exists")

        if not os.path.exists(self._downloader.cache_path):
            with self._lock:
                self._step = DownloadStep.request_content_length

            download_timeout = self._download_timeout
            if download_timeout is not None:
                timeout_text = f"{download_timeout:.03f}s"
            else:
                timeout_text = "None"

            logger.debug(
                f"{type(self).__name__} request_content_length ("
                f"timeout={timeout_text},"
                f"follow_redirects={self._follow_redirects},"
                f"verify={self._verify}"
                ") ..."
            )

            begin = time()
            content_length = self._downloader.request_content_length(
                timeout=download_timeout,
                follow_redirects=self._follow_redirects,
                verify=self._verify,
            )
            with self._lock:
                self._content_length = content_length

            logger.debug(f"{type(self).__name__} content_length: {content_length}byes")

            if download_timeout is not None:
                download_timeout -= time() - begin

            with self._lock:
                self._step = DownloadStep.download_streaming

            if download_timeout is not None:
                timeout_text = f"{download_timeout:.03f}s"
            else:
                timeout_text = "None"

            logger.debug(
                f"{type(self).__name__} download_streaming ("
                f"timeout={timeout_text},"
                f"follow_redirects={self._follow_redirects},"
                f"verify={self._verify}"
                ") ..."
            )

            with open(self._downloader.cache_path, "wb") as f:
                for data in self._downloader.download_streaming(
                    timeout=download_timeout,
                    follow_redirects=self._follow_redirects,
                    verify=self._verify,
                ):
                    f.write(data)
                    size = len(data)
                    with self._lock:
                        self._download_bytes += size

        logger.debug(f"{type(self).__name__} cache_path check ...")

        if not os.path.isfile(self._downloader.cache_path):
            raise FileNotFoundError("Not found cache file")

        with self._lock:
            self._step = DownloadStep.checksum

        logger.debug(f"{type(self).__name__} checksum ...")

        if self._verify_checksum and not self._downloader.verify_checksum():
            raise ValueError("Invalid checksum")

        with self._lock:
            self._step = DownloadStep.extract

        logger.debug(f"{type(self).__name__} extract ...")

        self._downloader.extract()

        logger.debug(f"{type(self).__name__} extract_files check ...")

        for path in self._downloader.extract_files:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"'{path}' is not a file")
