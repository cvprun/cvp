# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin
from cvp.service.item import ServiceKey


class ServiceMixin(BaseContextMixin):
    def do_process_exited(self, key: ServiceKey) -> None:
        self._services.handle_exited_process(key)
