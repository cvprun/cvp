# -*- coding: utf-8 -*-

from typing import Mapping

from imgui_bundle import imgui

from cvp.config.sections.worker import WorkerConfig, WorkerManagerConfig
from cvp.imgui.button import button
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager_tabs import ManagerTabs
from cvp.windows.worker.info import WorkerInfoTab


class WorkerManager(ManagerTabs[WorkerManagerConfig, WorkerConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.worker_manager,
            title="Worker Manager",
            closable=True,
            flags=None,
        )
        self.register(WorkerInfoTab(context))

        self._new_name_popup = InputTextPopup(
            title="Create worker",
            label="Please enter a worker name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_name_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove worker?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._new_name_popup)
        self.register_popup(self._confirm_remove)

    @override
    def get_menus(self) -> Mapping[str, WorkerConfig]:
        return {worker.uuid: worker for worker in self.context.config.workers}

    @override
    def on_process_sidebar_top(self) -> None:
        if imgui.button("New"):
            self._new_name_popup.show()
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    def on_new_name_popup(self, name: str) -> None:
        config = WorkerConfig(name=name)
        self.context.config.workers.append(config)

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        uuid = selected_menu.uuid
        self.context.config.remove_worker(uuid)
