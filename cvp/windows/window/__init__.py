# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.window import WindowManagerConfig
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.renderer.window.mapper import WindowMapper
from cvp.types.override import override
from cvp.widgets.manager_tabs import ManagerTabs
from cvp.windows.window.info import WindowInfoTab


class WindowManager(ManagerTabs[WindowManagerConfig, WindowBase]):
    def __init__(self, context: RendererContext, windows: WindowMapper):
        super().__init__(
            context=context,
            window_config=context.config.window_manager,
            title="Window Manager",
            closable=True,
            flags=None,
        )
        self._windows = windows
        self.register(WindowInfoTab(context))

    @override
    def get_menus(self) -> Mapping[str, WindowBase]:
        return self._windows
