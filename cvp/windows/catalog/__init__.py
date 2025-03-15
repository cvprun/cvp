# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.catalog import CatalogManagerConfig
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.nodes.node import Node
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager import Manager


class CatalogManager(Manager[CatalogManagerConfig, Node]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.catalog_manager,
            title="Catalog Manager",
            closable=True,
            flags=None,
        )

    @override
    def get_menus(self) -> Mapping[str, Node]:
        return {key: value for key, value in self.context.fm.nodes.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: Node) -> None:
        imgui.text("Catalog information")
        imgui.separator()

        input_text_disabled("Name", item.name)
        input_text_disabled("Path", item.path)

        # item.docs
        # item.base
        # item.icon
        # item.color
