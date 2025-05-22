# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin


class DownloadMixin(BaseContextMixin):
    # def make_downloader(self, link: LinkInfo):
    #     return DownloadArchive.from_link(
    #         link=link,
    #         extract_root=self._home,
    #         cache_dir=self._home.cache,
    #         temp_dir=self._home.temp,
    #     )

    # def start_download_thread(
    #     self,
    #     downloader: DownloadArchive,
    #     download_timeout: Optional[float] = None,
    #     verify_checksum=True,
    # ):
    #     return DownloadRunner(
    #         executor=self._thread_pool,
    #         downloader=downloader,
    #         download_timeout=download_timeout,
    #         verify_checksum=verify_checksum,
    #     )

    pass
