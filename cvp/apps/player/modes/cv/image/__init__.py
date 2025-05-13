# -*- coding: utf-8 -*-

from typing import Callable, Final, Sequence, Tuple

from imgui_bundle import imgui
from pygame import DROPFILE
from pygame.event import Event

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import IMAGE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.canvas.image import ImageCanvas
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
        self._canvas = ImageCanvas()

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
            # event.file
            return True

        return False

    def on_load_image(self, file: str) -> None:
        pass

    def on_file_menu(self) -> None:
        if menu_item("Open image"):
            self._open_image_popup.show()
        imgui.separator()
        if imgui.begin_menu("Recent images"):
            try:
                pass
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
                text_centered("Please open the image")

        self._popups.do_process()
