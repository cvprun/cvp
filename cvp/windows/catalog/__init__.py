# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.catalog import CatalogManagerConfig
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.templates.node import NodeTemplate
from cvp.types.override import override
from cvp.widgets.manager import Manager


class CatalogManager(Manager[CatalogManagerConfig, NodeTemplate]):
    def __init__(self, context: Context):
        super().__init__(
            context=context,
            window_config=context.config.catalog_manager,
            title="Catalog Manager",
            closable=True,
            flags=None,
        )

    @override
    def get_menus(self) -> Mapping[str, NodeTemplate]:
        return {key: value for key, value in self.context.fm.nodes.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: NodeTemplate) -> None:
        imgui.text("Catalog information")
        imgui.separator()

        input_text_disabled("Name", item.name)
        input_text_disabled("Path", item.path)

        # item.docs
        # item.base
        # item.icon
        # item.color
