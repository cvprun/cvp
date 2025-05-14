# -*- coding: utf-8 -*-

from typing import Callable, Final, Sequence, Tuple

from imgui_bundle import imgui
from PIL.Image import Image
from PIL.Image import open as pillow_open
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import IMAGE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_int2 import input_int2
from cvp.imgui.input_text import input_text
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.canvas.image import ImageCanvas
from cvp.logging.logging import logger
from cvp.types.override import override


class ImageMode(BaseMode):
    __cvp_mode_name__ = "Image"
    __cvp_mode_icon__ = IMAGE

    _CANVAS_SPLIT_X: Final[int] = -300
    _CANVAS_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context):
        super().__init__(context)
        self._open_image_popup = OpenFilePopup(
            title="Load image",
            target=self.on_load_image,
        )

        self._menus = (("File", self.on_file_menu),)
        self._popups = PopupList((self._open_image_popup,))

        self._path = str()
        self._canvas = ImageCanvas()
        self._image = Image()

    def open_image_file(self, file: str) -> None:
        try:
            self._path = file
            self._image = pillow_open(file)
            self._canvas.open_with_pillow(self._image)
            self.add_recent_item(file)
            logger.info(f"Image file opened: '{file}'")
        except BaseException as e:
            logger.error(f"Failed to open image file '{file}': {e}")
            raise

    def close(self) -> None:
        self._path = str()
        self._image = Image()
        self._canvas.close()
        logger.info("Image file closed")

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        if event.type == DROPFILE:
            self.open_image_file(event.file)
            return True

        return False

    def on_load_image(self, file: str) -> None:
        self.open_image_file(file)

    def on_file_menu(self) -> None:
        if menu_item("Open image"):
            self._open_image_popup.show()
        imgui.separator()
        if imgui.begin_menu("Recent images"):
            try:
                for item in self.get_recent_items():
                    if menu_item(item.value):
                        self.open_image_file(item.value)
                        self.add_recent_item(item.value)
                imgui.separator()
                if menu_item("Clear recent items"):
                    self.clear_recent_items()
            finally:
                imgui.end_menu()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Canvas",
                size=(self._CANVAS_SPLIT_X, 0),
                child_flags=self._CANVAS_CHILD_FLAGS,
            ):
                self._canvas.do_process()

            imgui.same_line()

            with begin_child_context("Infos"):
                if self._canvas.opened:
                    self.on_image_controller()
                else:
                    text_centered("Please open the image")

        self._popups.do_process()

    def on_image_controller(self) -> None:
        input_text("File", self._path)

        width = self._image.width
        height = self._image.height
        input_int2("Size", width, height)
