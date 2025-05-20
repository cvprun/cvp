# -*- coding: utf-8 -*-

from typing import Callable, Final, Sequence, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.canvas.canvas import CanvasKey
from cvp.context.context import Context
from cvp.imgui.flags.focused import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.menu_item import menu_item
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.push_style_var import style_window_padding_context
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas
from cvp.logging.loggers import canvas_logger as logger
from cvp.types.override import override


class CanvasWindow(ControllableCanvas, BaseWindow):
    __cvp_window_name__ = "Canvas"
    __cvp_window_position__ = DockPosition.center_top

    _MOUSE_RIGHT_BUTTON_MENU: Final[str] = "Mouse right button menu"

    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context, canvas_key: CanvasKey):
        ControllableCanvas.__init__(self)
        BaseWindow.__init__(self, context)
        self._canvas_key = canvas_key

        canvas = context.canvases[canvas_key]
        self._pan_x.update(canvas.control.pan_x, no_emit=True)
        self._pan_y.update(canvas.control.pan_y, no_emit=True)
        self._zoom.update(canvas.control.zoom, no_emit=True)

        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
            ("View", self.on_view_menu),
        )

        self._new_canvas_popup = InputTextPopup(
            title="New canvas",
            label="Please enter a canvas name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_canvas,
        )
        self._import_canvas_popup = OpenFilePopup(
            title="Import canvas",
            target=self.on_import_canvas,
        )
        self._export_canvas_popup = OpenFilePopup(
            title="Export canvas",
            target=self.on_export_canvas,
            open_mode=OpenFilePopup.OpenMode.input_filename,
        )
        self._confirm_remove_canvas_popup = ConfirmPopup(
            title="Remove canvas",
            label="Are you sure you want to remove canvas?",
            ok="Remove",
            cancel="Cancel",
            target=self.on_confirm_remove_canvas,
        )
        self._popups = (
            self._new_canvas_popup,
            self._import_canvas_popup,
            self._export_canvas_popup,
            self._confirm_remove_canvas_popup,
        )

    @classmethod
    def create_opened_windows(cls, context: Context):
        result = dict()
        for key, canvas in context.canvases.items():
            if not canvas.opened:
                continue
            result[key] = cls(context, key)
        return result

    def on_new_canvas(self, name: str) -> None:
        pass

    def on_import_canvas(self, file: str) -> None:
        pass

    def on_export_canvas(self, file: str) -> None:
        pass

    def on_confirm_remove_canvas(self, value: bool) -> None:
        pass

    @property
    def canvas_key(self):
        return self._canvas_key

    @property
    def canvas(self):
        return self.context.canvases[self._canvas_key]

    @property
    def is_selected_canvas(self):
        return self.context.selected_canvas_key == self._canvas_key

    @property
    def config(self):
        return self.context.config.canvas

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text()

    @override
    def get_window_name(self) -> str:
        window_name = self.__cvp_window_name__
        canvas = self.context.flows.canvass.get(self._canvas_key)
        canvas_name = canvas.name if canvas else window_name
        return f"{canvas_name}###{window_name}/{self._canvas_key}"

    @override
    def on_process(self) -> None:
        if not self.canvas.opened:
            return

        with style_window_padding_context(0.0, 0.0):
            visible, opened = imgui.begin(self.get_window_name(), self.canvas.opened)
            assert isinstance(opened, bool)
            self.canvas.opened = opened

        if imgui.is_window_focused(ROOT_AND_CHILD_WINDOWS):
            self.context.selected_canvas_key = self._canvas_key

        try:
            if self.canvas.opened and visible:
                if self._canvas_key in self.context.canvases:
                    self.do_canvas_process()
                    self.do_child_process()
                else:
                    text_centered(f"Not found {self._canvas_key} canvas")
        except BaseException as e:
            logger.exception(e)
        finally:
            imgui.end()

        for popup in self._popups:
            popup.on_process()

    def do_child_process(self) -> None:
        if imgui.begin_popup_context_window(self._MOUSE_RIGHT_BUTTON_MENU):
            try:
                self.do_file_menu()
                imgui.separator()
                self.do_edit_menu()
                imgui.separator()
                self.do_layer_menu()
                imgui.separator()
                self.do_align_menu()
                self.do_distribute_menu()
            finally:
                imgui.end_popup()

        self.draw()

    # ==================================================================================
    # region: Context Menu Operations
    # ==================================================================================

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

    def on_file_menu(self) -> None:
        if menu_item("New canvas"):
            pass

        imgui.separator()
        if self.is_selected_canvas:
            self.do_file_menu()
        else:
            self.do_disabled_file_menu()

        imgui.separator()
        if menu_item("Import canvas"):
            pass
        if menu_item("Export canvas", enabled=self.is_selected_canvas):
            pass

    def on_edit_menu(self) -> None:
        if self.is_selected_canvas:
            self.do_edit_menu()
        else:
            self.do_disabled_edit_menu()

    def on_layer_menu(self) -> None:
        if self.is_selected_canvas:
            self.do_layer_menu()
            imgui.separator()
            self.do_align_menu()
            self.do_distribute_menu()
        else:
            self.do_disabled_layer_menu()
            imgui.separator()
            self.do_disabled_align_menu()
            self.do_disabled_distribute_menu()

    def on_view_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_file_menu() -> None:
        menu_item("Save canvas", enabled=False)
        menu_item("Save and close canvas", enabled=False)
        menu_item("Force close canvas", enabled=False)

    def do_file_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_edit_menu() -> None:
        menu_item("Undo", shortcut="Ctrl+Z", enabled=False)
        menu_item("Redo", shortcut="Ctrl+Y", enabled=False)
        imgui.separator()
        menu_item("Cut", shortcut="Ctrl+X", enabled=False)
        menu_item("Copy", shortcut="Ctrl+C", enabled=False)
        menu_item("Paste", shortcut="Ctrl+V", enabled=False)
        imgui.separator()
        menu_item("Delete", shortcut="Del", enabled=False)
        imgui.separator()
        menu_item("Reset control", enabled=False)
        imgui.separator()
        menu_item("Select all", enabled=False)
        menu_item("Select nodes", enabled=False)
        menu_item("Select wires", enabled=False)
        menu_item("Select pins", enabled=False)

    def do_edit_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_layer_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    def do_layer_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    def do_align_menu(self) -> None:
        pass

    @staticmethod
    def do_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    def do_distribute_menu(self) -> None:
        pass

    # ==================================================================================
    # endregion: Context Menu Operations
    # ==================================================================================
    # region: Status Bar Operations
    # ==================================================================================

    @override
    def on_status_menu(self) -> None:
        imgui.text(f"Pan:{int(self.pan_x)}x{int(self.pan_y)} Zoom:{self.zoom:.02f}")

    # ==================================================================================
    # endregion: Status Bar Operations
    # ==================================================================================
    # region: Public Operations
    # ==================================================================================

    def save_canvas(self) -> None:
        pass

    def close_canvas(self):
        self.canvas.opened = False
        logger.info(f"Close the canvas: '{self.canvas.key}'")

    def reset_controllers(self):
        logger.info("Reset controllers")

        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self.canvas.control.pan_x = 0.0
        self.canvas.control.pan_y = 0.0
        self.canvas.control.zoom = 1.0

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

    # ==================================================================================
    # endregion: Public Operations
    # ==================================================================================
    # region: Draw Operations
    # ==================================================================================

    def draw(self) -> None:
        with window_font_scale(self.zoom):
            self.fill()
            self.draw_grid_x()
            self.draw_grid_y()
            self.draw_axis_x()
            self.draw_axis_y()

    def fill(self) -> None:
        color = imgui.get_color_u32(self.config.background_color)
        x1, y1, x2, y2 = self.canvas_roi
        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_rect_filled(p1, p2, color)

    def draw_grid_x(self) -> None:
        grid_x = self.config.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32(grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_x.thickness)

    def draw_grid_y(self) -> None:
        grid_y = self.config.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32(grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            p1 = line[0], line[1]
            p2 = line[2], line[3]
            self._draw_list.add_line(p1, p2, color, grid_y.thickness)

    def draw_axis_x(self) -> None:
        axis_x = self.config.axis_x
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        color = imgui.get_color_u32(axis_x.color)

        x1 = self.cx
        y1 = origin_y
        x2 = self.cx + self.cw
        y2 = origin_y

        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_line(p1, p2, color, axis_x.thickness)

    def draw_axis_y(self) -> None:
        axis_y = self.config.axis_y
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        color = imgui.get_color_u32(axis_y.color)

        x1 = origin_x
        y1 = self.cy
        x2 = origin_x
        y2 = self.cy + self.ch

        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_line(p1, p2, color, axis_y.thickness)

    # ==================================================================================
    # endregion: Draw Operations
    # ==================================================================================
