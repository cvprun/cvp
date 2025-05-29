# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class OpenFilePopupDemo(SimpleDemoBase):
    def __init__(self, font_name="Default", font_size=12):
        super().__init__(force_egl=True, use_accelerate=True)
        self._browser = OpenFilePopup(
            OpenFilePopup.__name__,
            target=self.on_selected,
            open_mode=OpenFilePopup.OpenMode.select_file,
        )
        self._selected = str()
        self._font_name = font_name
        self._font_size = font_size

    def on_selected(self, file: str) -> None:
        self._selected = file

    @override
    def on_init(self) -> None:
        imgui.get_io().fonts.clear()
        add_mixed_font(self._font_name, self._font_size)

    @override
    def on_frame(self) -> None:
        imgui.begin(type(self).__name__)
        imgui.text(f"Selected file: '{self._selected}'")
        if imgui.button("Browse"):
            if self._selected:
                self._browser.set_location(self._selected)
            self._browser.show()
        imgui.end()
        self._browser.on_process()


if __name__ == "__main__":
    OpenFilePopupDemo().run()
