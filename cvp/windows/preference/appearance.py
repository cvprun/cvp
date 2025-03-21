# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.push_style_var import DefaultStyles, style_colors
from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class AppearancePreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Appearance"):
        self._config = context.config.appearance
        self._label = label
        self._styles = [str(s.name) for s in DefaultStyles]

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    def theme(self) -> str:
        return self._config.theme

    @theme.setter
    def theme(self, value: str):
        self._config.theme = value

    @property
    def style_index(self) -> int:
        try:
            return self._styles.index(self._config.theme)
        except ValueError:
            return -1

    @override
    def on_process(self) -> None:
        style_result = imgui.combo("Style", self.style_index, self._styles)
        style_changed, style_index = style_result
        assert isinstance(style_changed, bool)
        assert isinstance(style_index, int)

        if style_changed and 0 <= style_index < len(self._styles):
            theme_value = self._styles[style_index]
            try:
                style_colors(DefaultStyles(theme_value))
            except BaseException as e:
                logger.error(f"Changed theme error: {e}")
            else:
                logger.info(f"Changed theme: '{theme_value}'")
                self.theme = theme_value

        imgui.show_font_selector("Font")
