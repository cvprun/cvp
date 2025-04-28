# -*- coding: utf-8 -*-

import os
from os import PathLike
from shutil import move, unpack_archive
from ssl import SSLContext
from tempfile import TemporaryDirectory
from typing import List, Optional, Sequence, Tuple, Union
from urllib.parse import ParseResult, urlparse, urlunparse

import httpx

from cvp.hashfunc.checksum import HashFunction
from cvp.hashfunc.checksum import checksum as calc_checksum
from cvp.resources.download.links.tuples import Checksum, ExtractPair, LinkInfo


class DownloadArchive:
    _url: str
    _components: ParseResult
    _paths: List[ExtractPair]
    _checksum: Optional[Checksum]

    def __init__(
        self,
        url: Union[str, ParseResult],
        paths: Sequence[Union[Tuple[str, str], ExtractPair]],
        extract_root: Union[str, PathLike[str]],
        cache_dir: Union[str, PathLike[str]],
        temp_dir: Optional[Union[str, PathLike[str]]] = None,
        checksum: Optional[Union[str, Tuple[str, str], Checksum]] = None,
    ):
        if not paths:
            raise ValueError("No paths given")

        if isinstance(url, ParseResult):
            self._url = str(urlunparse(url))
            self._components = url
        else:
            assert isinstance(url, str)
            self._url = url
            self._components = urlparse(url)

        self._paths = list()
        for path in paths:
            if isinstance(path, ExtractPair):
                self._paths.append(path)
            else:
                assert isinstance(path, tuple)
                assert len(path) == 2
                assert isinstance(path[0], str)
                assert isinstance(path[1], str)
                self._paths.append(ExtractPair(path[0], path[1]))

        self._extract_root = extract_root
        self._cache_dir = cache_dir
        self._temp_dir = temp_dir

        if checksum:
            if isinstance(checksum, Checksum):
                self._checksum = checksum
            elif isinstance(checksum, tuple):
                assert len(checksum) == 2
                assert isinstance(checksum[0], str)
                assert isinstance(checksum[1], str)
                hash_method = HashFunction(checksum[0].lower())
                self._checksum = Checksum(hash_method, checksum[1])
            else:
                self._checksum = Checksum.parse(checksum.strip())
        else:
            self._checksum = None

    @classmethod
    def from_link(
        cls,
        link: LinkInfo,
        extract_root: Union[str, PathLike[str]],
        cache_dir: Union[str, PathLike[str]],
        temp_dir: Optional[Union[str, PathLike[str]]] = None,
    ):
        return cls(
            url=link.url,
            paths=link.paths,
            extract_root=extract_root,
            cache_dir=cache_dir,
            temp_dir=temp_dir,
            checksum=link.checksum,
        )

    def __repr__(self):
        return f"<{type(self).__name__} {self._url}>"

    @property
    def has_path(self) -> bool:
        return bool(self._paths)

    @property
    def has_checksum(self) -> bool:
        return self._checksum is not None

    @property
    def url(self) -> str:
        return self._url

    @property
    def checksum(self):
        return self._checksum

    @property
    def paths(self):
        return self._paths

    @property
    def extract_files(self) -> List[str]:
        return [os.path.join(self._extract_root, p.extract_path) for p in self._paths]

    @property
    def any_extract_files(self):
        return any((os.path.isfile(p) for p in self.extract_files))

    @property
    def root_url(self) -> str:
        return f"{self._components.scheme}://{self._components.netloc}/"

    @property
    def filename(self) -> str:
        return os.path.basename(self._components.path)

    @property
    def cache_path(self) -> str:
        return os.path.join(self._cache_dir, self.filename)

    def request_content_length(
        self,
        timeout: Optional[float] = None,
        follow_redirects=True,
        verify: Union[str, bool, SSLContext] = True,
    ) -> int:
        with httpx.Client(follow_redirects=follow_redirects, verify=verify) as client:
            response = client.head(self._url, timeout=timeout)
            return int(response.headers["Content-Length"])

    def download_streaming(
        self,
        timeout: Optional[float] = None,
        follow_redirects=True,
        verify: Union[str, bool, SSLContext] = True,
    ):
        with httpx.stream(
            "GET",
            self._url,
            timeout=timeout,
            follow_redirects=follow_redirects,
            verify=verify,
        ) as response:
            for data in response.iter_bytes():
                yield data

    def download(
        self,
        timeout: Optional[float] = None,
        follow_redirects=True,
        verify: Union[str, bool, SSLContext] = True,
    ) -> None:
        with open(self.cache_path, "wb") as f:
            for data in self.download_streaming(timeout, follow_redirects, verify):
                f.write(data)

    def verify_checksum(self) -> bool:
        if not self._checksum:
            raise ValueError("Checksum cache is empty")

        with open(self.cache_path, "rb") as f:
            method = self._checksum.hash_method
            value = self._checksum.hash_value
            return calc_checksum(method, f.read()) == value

    def extract(self) -> None:
        with TemporaryDirectory(dir=self._temp_dir) as tmpdir:
            unpack_archive(self.cache_path, tmpdir)

            for path in self._paths:
                src = os.path.join(tmpdir, path.archive_path)
                dest = os.path.join(self._extract_root, path.extract_path)
                move(src, dest)
