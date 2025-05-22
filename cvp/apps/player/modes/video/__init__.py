# -*- coding: utf-8 -*-

from typing import Final, Optional

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import PLAY_CIRCLE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.menu_container import MenuList
from cvp.imgui.menu_item import menu_item
from cvp.imgui.menu_recent_items import menu_recent_items
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.video_player import VideoPlayer
from cvp.logging.loggers import logger
from cvp.types.override import override


class VideoPlayerMode(BaseMode):
    __cvp_mode_name__ = "Video Player"
    __cvp_mode_icon__ = PLAY_CIRCLE

    _PLAYER_SPLIT_X: Final[int] = -300
    _PLAYER_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _player: Optional[VideoPlayer]

    def __init__(self, context: Context):
        super().__init__(context)

        self._open_video_popup = OpenFilePopup(
            title="Open video",
            target=self.on_open_video,
        )
        self._open_network_popup = InputTextPopup(
            title="Open network",
            label="Please enter a network location:",
            ok="Open",
            cancel="Cancel",
            target=self.on_open_network,
        )

        self._menus = MenuList(("File", self.on_file_menu))
        self._popups = PopupList(self._open_video_popup, self._open_network_popup)

        self._path = str()
        self._region_size = 0, 0
        self._player = None

    @property
    def opened(self) -> bool:
        return self._player is not None

    def open_video_file(self, file: str) -> None:
        try:
            video_width = max(1, self._region_size[0])
            video_height = max(1, self._region_size[1])
            video_size = video_width, video_height

            self._path = file
            self._player = VideoPlayer(file, video_size)
            self.add_recent_item(file)
            logger.info(f"Video file opened: '{file}'")
        except BaseException as e:
            logger.error(f"Failed to open video file '{file}': {e}")
            raise

    def close(self) -> None:
        self._path = str()
        if self._player is not None:
            self._player.close()
            self._player = None
        logger.info("Video file closed")

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_video_file(event.file)
            return True

        return False

    def on_open_video(self, file: str) -> None:
        if not file:
            return

        self.open_video_file(file)

    def on_open_network(self, file: str) -> None:
        if not file:
            return

        self.open_video_file(file)

    def on_file_menu(self) -> None:
        if menu_item("Open video"):
            self._open_video_popup.show()

        if menu_item("Open network"):
            self._open_network_popup.show()

        if recent_item := menu_recent_items(
            label="Recent videos",
            config=self.context.config.navigation,
            cls=type(self),
            append_clear_menu=True,
            clear_menu_label="Clear recent videos",
        ):
            self.open_video_file(recent_item.value)

        imgui.separator()
        if menu_item("Close video", enabled=self.opened):
            self.close()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Player",
                size=(self._PLAYER_SPLIT_X, 0),
                child_flags=self._PLAYER_CHILD_FLAGS,
            ):
                draw_list = get_window_draw_list()
                region_size = imgui.get_content_region_avail()
                self._region_size = int(region_size.x), int(region_size.y)

                if self._player is not None:
                    self._player.do_process(draw_list)
                else:
                    text_centered("Please open the video")

            imgui.same_line()

            with begin_child_context("Infos"):
                if self._player is not None:
                    self.on_video_controller()
                else:
                    text_centered("Please open the video")

        self._popups.do_process()

    def on_video_controller(self) -> None:
        assert self._player is not None
        self._player.do_playback_slider("Playback")
        self._player.do_volume_slider("Volume")
