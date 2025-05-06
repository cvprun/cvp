# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.canvas.canvas import CanvasKey
from cvp.context.context import Context
from cvp.imgui.flags.focused import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.push_style_var import style_window_padding_context
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas
from cvp.logging.logging import canvas_logger as logger
from cvp.types.override import override


class CanvasWindow(ControllableCanvas):
    def __init__(self, context: Context, canvas_key: CanvasKey):
        super().__init__()

        self._context = context
        self._canvas_key = canvas_key

        canvas = context.canvases[canvas_key]
        self._pan_x.update(canvas.control.pan_x, no_emit=True)
        self._pan_y.update(canvas.control.pan_y, no_emit=True)
        self._zoom.update(canvas.control.zoom, no_emit=True)

    @classmethod
    def create_opened_windows(cls, context: Context):
        result = dict()
        for key, canvas in context.canvases.items():
            if not canvas.opened:
                continue
            result[key] = cls(context, key)
        return result

    @property
    def context(self):
        return self._context

    @property
    def canvas_key(self):
        return self._canvas_key

    @property
    def canvas(self):
        return self.context.canvases[self._canvas_key]

    @property
    def focused_key(self):
        return CanvasKey(self.context.config.navigation.focused_key)

    @focused_key.setter
    def focused_key(self, value: CanvasKey) -> None:
        self.context.config.navigation.focused_key = str(value)

    @property
    def config(self):
        return self.context.config.canvas

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text()

    def get_window_name(self) -> str:
        class_name = type(self).__name__
        canvas = self.context.canvases.get(self._canvas_key)
        canvas_name = canvas.name if canvas else class_name
        return f"{canvas_name}###{class_name}/{self._canvas_key}"

    def do_process(self) -> None:
        if not self.canvas.opened:
            return

        with style_window_padding_context(0.0, 0.0):
            visible, opened = imgui.begin(self.get_window_name(), self.canvas.opened)
            assert isinstance(opened, bool)
            self.canvas.opened = opened

        if imgui.is_window_focused(ROOT_AND_CHILD_WINDOWS):
            self.focused_key = self._canvas_key

        try:
            if visible:
                if self._canvas_key in self.context.flows.canvass:
                    self.do_canvas_process()
                    self.do_child_process()
                else:
                    text_centered(f"Not found {self._canvas_key} canvas")
        except BaseException as e:
            logger.exception(e)
        finally:
            imgui.end()

    def do_child_process(self) -> None:
        pass

    def do_process_controllers(self, debugging=False) -> None:
        if result := self.render_controllers(debugging=debugging):
            self.canvas.control.pan_x = result.pan_x
            self.canvas.control.pan_y = result.pan_y
            self.canvas.control.zoom = result.zoom

    def do_canvas_process(self) -> None:
        if result := self.update_state():
            self.canvas.control.pan_x = result.pan_x
            self.canvas.control.pan_y = result.pan_y
            self.canvas.control.zoom = result.zoom

    def do_file_menu(self) -> None:
        if menu_item("Save canvas"):
            pass
        if menu_item("Save and close graph"):
            self.canvas.opened = False
        if menu_item("Force close graph"):
            self.canvas.opened = False

    def do_edit_menu(self) -> None:
        imgui.separator()
        if menu_item("Reset control"):
            self.reset_controllers()

    def do_layer_menu(self) -> None:
        pass

    def do_align_menu(self) -> None:
        pass

    def do_distribute_menu(self) -> None:
        pass

    def reset_controllers(self) -> None:
        logger.info("Reset controllers")

        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self.canvas.control.pan_x = 0.0
        self.canvas.control.pan_y = 0.0
        self.canvas.control.zoom = 1.0
