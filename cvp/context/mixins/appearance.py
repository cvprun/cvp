# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin


class AppearanceMixin(BaseContextMixin):
    @property
    def clear_color(self):
        return self._config.appearance.clear_color

    @property
    def success_color(self):
        return self._config.appearance.success_color

    @property
    def normal_color(self):
        return self._config.appearance.normal_color

    @property
    def warning_color(self):
        return self._config.appearance.warning_color

    @property
    def error_color(self):
        return self._config.appearance.error_color
