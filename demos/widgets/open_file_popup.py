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
            mode=OpenFilePopup.Mode.select_file | OpenFilePopup.Mode.select_directory,
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

        imgui.text("Selected file:")
        imgui.begin_disabled()
        imgui.set_next_item_width(-1 * imgui.FLT_MIN)
        imgui.input_text("##SelectedFile", self._selected)
        imgui.end_disabled()

        select_file_flag = self._browser.select_file_flag
        select_directory_flag = self._browser.select_directory_flag
        input_filename_flag = self._browser.input_filename_flag
        show_hidden_flag = self._browser.show_hidden_flag
        overwrite_popup_flag = self._browser.overwrite_popup_flag

        if imgui.checkbox("Select File", select_file_flag)[0]:
            self._browser.select_file_flag = not select_file_flag
        if imgui.checkbox("Select Directory", select_directory_flag)[0]:
            self._browser.select_directory_flag = not select_directory_flag
        if imgui.checkbox("Input Filename", input_filename_flag)[0]:
            self._browser.input_filename_flag = not input_filename_flag
        if imgui.checkbox("Show Hidden", show_hidden_flag)[0]:
            self._browser.show_hidden_flag = not show_hidden_flag
        if imgui.checkbox("Overwrite Popup", overwrite_popup_flag)[0]:
            self._browser.overwrite_popup_flag = not overwrite_popup_flag

        if imgui.button("Browse"):
            if self._selected:
                self._browser.set_location(self._selected)
            self._browser.show()

        imgui.end()

        self._browser.on_process()


if __name__ == "__main__":
    OpenFilePopupDemo().run()
