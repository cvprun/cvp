# -*- coding: utf-8 -*-

from typing import Mapping

from cvp.config.sections.process import ProcessManagerConfig
from cvp.process.process import Process
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager_tabs import ManagerTabs
from cvp.windows.process.info import ProcessInfoTab
from cvp.windows.process.stream import ProcessStreamTab


class ProcessManager(ManagerTabs[ProcessManagerConfig, Process]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.process_manager,
            title="Process Manager",
            closable=True,
            flags=None,
        )
        self.register(ProcessInfoTab(context))
        self.register(ProcessStreamTab.from_stdout(context))
        self.register(ProcessStreamTab.from_stderr(context))

    @override
    def get_menus(self) -> Mapping[str, Process]:
        return self._context.pm.processes
