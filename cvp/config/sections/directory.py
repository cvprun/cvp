# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

import platformdirs


@dataclass
class DirectoryConfig:
    user_documents: str = field(default_factory=platformdirs.user_documents_dir)
    user_downloads: str = field(default_factory=platformdirs.user_downloads_dir)
    user_pictures: str = field(default_factory=platformdirs.user_pictures_dir)
    user_videos: str = field(default_factory=platformdirs.user_videos_dir)
    user_music: str = field(default_factory=platformdirs.user_music_dir)
    user_desktop: str = field(default_factory=platformdirs.user_desktop_dir)

    # user_runtime: str = field(default_factory=lambda: platformdirs.user_runtime_dir)
    # user_data: str = field(default_factory=lambda: platformdirs.user_data_dir)
    # user_config: str = field(default_factory=lambda: platformdirs.user_config_dir)
    # user_cache: str = field(default_factory=lambda: platformdirs.user_cache_dir)
    # site_data: str = field(default_factory=lambda: platformdirs.site_data_dir)
    # site_config: str = field(default_factory=lambda: platformdirs.site_config_dir)
    # user_log: str = field(default_factory=lambda: platformdirs.user_log_dir)
