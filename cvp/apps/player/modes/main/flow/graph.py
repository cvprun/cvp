# -*- coding: utf-8 -*-

from typing import Callable, Final, List, Optional, Sequence, Tuple

from imgui_bundle import imgui
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.apps.player.widgets.flows.drag_target import accept_target
from cvp.apps.player.widgets.flows.drag_types import DragTypes
from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.dtypes.dtype import Dtype
from cvp.flow.anchor import FlowAnchor
from cvp.flow.connection import FlowConnection
from cvp.flow.graph import GraphKey
from cvp.flow.mode import FlowMode
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelection
from cvp.flow.wire import FlowWire
from cvp.imgui.calc_text_size import calc_text_size
from cvp.imgui.draw_list.draw_dotted_line import draw_dotted_line
from cvp.imgui.flags.focused import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.flags.key import KeyFlags
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.popups.input_text import InputTextPopup
from cvp.imgui.push_style_var import style_window_padding_context
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.canvas.controllable import ControllableCanvas
from cvp.imgui.widgets.shortcut import Shortcut
from cvp.logging.logging import flow_logger as logger
from cvp.maths.geometry.rectangle import is_rectangle_collision
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.types.shapes import Rect


class GraphFlowWindow(ControllableCanvas, BaseWindow):
    __cvp_window_name__ = "Graph"
    __cvp_window_position__ = DockPosition.center_top

    _ADD_VARIABLE_NODE_MENU: Final[str] = "Add variable node menu"
    _MOUSE_RIGHT_BUTTON_MENU: Final[str] = "Mouse right button menu"

    _mode: FlowMode
    _connects: List[FlowNodePin]
    _roi: Optional[Rect]
    _selection_stash: Optional[FlowSelection]
    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context, graph_key: GraphKey):
        ControllableCanvas.__init__(self)
        BaseWindow.__init__(self, context)
        self._graph_key = graph_key

        graph = context.flows.graphs[graph_key]
        self._pan_x.update(graph.control.pan_x, no_emit=True)
        self._pan_y.update(graph.control.pan_y, no_emit=True)
        self._zoom.update(graph.control.zoom, no_emit=True)

        graph.clear_state()
        graph.update_wires_io()
        graph.update_wires_polyline()

        self._mode = FlowMode.normal
        self._connects = list()
        self._roi = None
        self._selection_stash = None

        self._drag_dtype = Dtype.any()
        self._variable_key = str()

        self._menus = (
            ("Edit", self.on_edit_menu),
            ("Layer", self.on_layer_menu),
            ("Run", self.on_run_menu),
            ("Deploy", self.on_deploy_menu),
            ("View", self.on_view_menu),
        )

        self._new_variable_popup = InputTextPopup(
            title="New variable",
            label="Please enter a variable name:",
            ok="Add",
            cancel="Cancel",
            target=self.on_new_variable,
        )

        self._shortcut_escape = Shortcut(
            KeyFlags.escape,
            callback=self.do_unselect_all_items,
        )
        self._shortcut_delete = Shortcut(
            KeyFlags.delete,
            callback=self.do_remove_selected_items,
        )

        self._shortcut_undo = Shortcut(
            KeyFlags.z,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_undo,
        )
        self._shortcut_redo = Shortcut(
            KeyFlags.z,
            ctrl=True,
            shift=True,
            alt=False,
            callback=self.do_redo,
        )
        self._shortcut_redo_for_windows = Shortcut(
            KeyFlags.y,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_redo,
        )

        self._shortcut_select_all_nodes = Shortcut(
            KeyFlags.a,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_select_all_nodes,
        )
        self._shortcut_select_all_items = Shortcut(
            KeyFlags.a,
            ctrl=True,
            shift=True,
            alt=False,
            callback=self.do_select_all_items,
        )

        self._shortcut_cut = Shortcut(
            KeyFlags.x,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_cut_selected_items,
        )
        self._shortcut_copy = Shortcut(
            KeyFlags.c,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_copy_selected_items,
        )
        self._shortcut_paste = Shortcut(
            KeyFlags.v,
            ctrl=True,
            shift=False,
            alt=False,
            callback=self.do_paste_selected_items,
        )

        # noinspection PyProtectedMember
        self._shortcuts = [
            self._shortcut_escape,
            self._shortcut_delete,
            self._shortcut_undo,
            self._shortcut_redo,
            self._shortcut_redo_for_windows,
            self._shortcut_select_all_nodes,
            self._shortcut_select_all_items,
            self._shortcut_cut,
            self._shortcut_copy,
            self._shortcut_paste,
        ]

    @classmethod
    def create_opened_windows(cls, context: Context):
        result = dict()
        for key, graph in context.flows.graphs.items():
            if not graph.opened:
                continue
            result[key] = cls(context, key)
        return result

    def on_new_variable(self, name: str) -> None:
        if not name:
            raise ValueError("Variable name cannot be empty")
        self.graph.add_variable(name, self._drag_dtype)

    @property
    def graph_key(self):
        return self._graph_key

    @property
    def graph(self):
        return self.context.flows.graphs[self._graph_key]

    @property
    def is_focused_in_navigation(self):
        return self.focused_key == self._graph_key

    @property
    def config(self):
        return self.context.config.flow

    @property
    def show_layout(self) -> bool:
        return self.config.nodes.show_layout

    @show_layout.setter
    def show_layout(self, value: bool) -> None:
        self.config.nodes.show_layout = value

    @property
    def autoscroll(self) -> bool:
        return self.config.logs.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.config.logs.autoscroll = value

    @property
    def is_multi_select_mode(self) -> bool:
        # Pressing the SHIFT button switches to 'Multi-node selection mode'
        return self.shift_down

    @property
    def is_pan_mode(self) -> bool:
        # Pressing the ALT button switches to 'Canvas Pan Mode'
        return self.alt_down

    @property
    def is_normal_mode(self) -> bool:
        return self._mode == FlowMode.normal

    @property
    def is_node_moving_mode(self) -> bool:
        return self._mode == FlowMode.node_moving

    @property
    def is_pin_connecting_mode(self) -> bool:
        return self._mode == FlowMode.pin_connecting

    @property
    def is_anchor_moving_mode(self) -> bool:
        return self._mode == FlowMode.anchor_moving

    @property
    def is_roi_box_mode(self) -> bool:
        return self._mode == FlowMode.roi_box

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text() + (
            f"Mode: {self._mode.name}\n"
            f"Connects: {self._connects}\n"
            f"ROI: {self._roi}\n"
            f"History: {len(self.graph.history)}\n"
            f"Cursor: {self.graph.history.cursor_index}\n"
        )

    @override
    def get_window_name(self) -> str:
        window_name = self.__cvp_window_name__
        graph = self.context.flows.graphs.get(self._graph_key)
        graph_name = graph.name if graph else window_name
        return f"{graph_name}###{window_name}/{self._graph_key}"

    @override
    def on_process(self) -> None:
        if not self.graph.opened:
            return

        with style_window_padding_context(0.0, 0.0):
            visible, opened = imgui.begin(self.get_window_name(), self.graph.opened)
            assert isinstance(opened, bool)
            self.graph.opened = opened

        if imgui.is_window_focused(ROOT_AND_CHILD_WINDOWS):
            self.focused_key = self._graph_key

        try:
            if self.graph.opened and visible:
                if self._graph_key in self.context.flows.graphs:
                    self.do_canvas_process()
                    self.do_child_process()
                else:
                    text_centered(f"Not found {self._graph_key} graph")
        except BaseException as e:
            logger.exception(e)
        finally:
            imgui.end()

        self._new_variable_popup.on_process()

    def do_child_process(self) -> None:
        if payload := accept_target():
            assert payload is not None
            assert payload.value is not None

            match payload.type:
                case DragTypes.flow_graph:
                    pass
                case DragTypes.flow_node:
                    node = self.context.flows.add_node(self.graph, payload.value)
                    self.update_node_roi(node)
                    self.graph.save_history("Add a new node", payload.value)
                case DragTypes.flow_dtype:
                    self._drag_dtype = self.context.flows.dtypes[payload.value]
                    self._new_variable_popup.show()
                case DragTypes.flow_variable:
                    self._variable_key = payload.value
                    imgui.open_popup(self._ADD_VARIABLE_NODE_MENU)
                case _:
                    assert False, "Inaccessible section"

        if imgui.begin_popup_context_window(self._ADD_VARIABLE_NODE_MENU):
            try:
                self.do_add_variable_menu()
            finally:
                imgui.end_popup()

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
    # region: Keyboard Operations
    # ==================================================================================

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        for shortcut in self._shortcuts:
            if shortcut():
                return

    def do_remove_selected_items(self) -> None:
        self.graph.remove_selected_items()
        self.graph.save_history("Remove selected items")

    def do_unselect_all_items(self) -> None:
        self.graph.unselect_all_items()

    def do_undo(self) -> None:
        if self.graph.history.undoable:
            self.graph.undo_history()

    def do_redo(self) -> None:
        if self.graph.history.redoable:
            self.graph.redo_history()

    def do_select_all_nodes(self) -> None:
        self.graph.select_all_nodes()

    def do_select_all_items(self) -> None:
        self.graph.select_all_items()

    def do_cut_selected_items(self) -> None:
        self.context.flows.clipboard_items = self.graph.selection.deepcopy()
        self.context.flows.clipboard_pivot = self.graph.selection.group_pos
        self.graph.remove_selected_items()
        self.graph.save_history("Cut selected items")

    def do_copy_selected_items(self) -> None:
        self.context.flows.clipboard_items = self.graph.selection.deepcopy()
        px, py = self.graph.selection.group_pos
        px += self.config.paste_margin
        py += self.config.paste_margin
        self.context.flows.clipboard_pivot = px, py
        self.graph.save_history("Copy selected items")

    def do_paste_selected_items(self) -> None:
        self.graph.unselect_all_items()
        self.graph.paste_selection(
            self.context.flows.clipboard_items,
            self.context.flows.clipboard_pivot,
            selected=True,
        )
        px, py = self.context.flows.clipboard_pivot
        px += self.config.paste_margin
        py += self.config.paste_margin
        self.context.flows.clipboard_pivot = px, py
        self.graph.save_history("Paste selected items")

    # ==================================================================================
    # endregion: Keyboard Operations
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

    def on_edit_menu(self) -> None:
        if self.is_focused_in_navigation:
            self.do_edit_menu()
        else:
            self.do_disabled_edit_menu()

    def on_layer_menu(self) -> None:
        if self.is_focused_in_navigation:
            self.do_layer_menu()
            imgui.separator()
            self.do_align_menu()
            self.do_distribute_menu()
        else:
            self.do_disabled_layer_menu()
            imgui.separator()
            self.do_disabled_align_menu()
            self.do_disabled_distribute_menu()

    def on_run_menu(self) -> None:
        if self.is_focused_in_navigation:
            self.do_run_menu()
        else:
            self.do_disabled_run_menu()

    def on_deploy_menu(self) -> None:
        if self.is_focused_in_navigation:
            self.do_deploy_menu()
        else:
            self.do_disabled_deploy_menu()

    def on_view_menu(self) -> None:
        if autoscroll := menu_item("Autoscroll logs", selected=self.autoscroll):
            self.autoscroll = autoscroll.state
        imgui.separator()
        if show_layout := menu_item("Show Layout", selected=self.show_layout):
            self.show_layout = show_layout.state

    def do_file_menu(self) -> None:
        if menu_item("Save graph"):
            self.context.save_flow_graph(self.graph)
        if menu_item("Save and close graph"):
            self.context.save_flow_graph(self.graph)
            self.graph.opened = False
        if menu_item("Force close graph"):
            self.graph.opened = False

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
        undoable = self.graph.history.undoable
        redoable = self.graph.history.redoable
        selected_any = bool(self.graph.selection)
        has_clipboard = self.context.flows.has_clipboard

        if menu_item("Undo", shortcut="Ctrl+Z", enabled=undoable):
            self.graph.undo_history()
        if menu_item("Redo", shortcut="Ctrl+Y", enabled=redoable):
            self.graph.redo_history()

        imgui.separator()
        if menu_item("Cut", shortcut="Ctrl+X", enabled=selected_any):
            self.context.flows.clipboard_items = self.graph.selection.deepcopy()
            self.context.flows.clipboard_pivot = self.graph.selection.group_pos
            self.graph.remove_selected_items()
            self.graph.save_history("Cut selected items")
        if menu_item("Copy", shortcut="Ctrl+C", enabled=selected_any):
            self.context.flows.clipboard_items = self.graph.selection.deepcopy()
            px, py = self.graph.selection.group_pos
            px += self.config.paste_margin
            py += self.config.paste_margin
            self.context.flows.clipboard_pivot = px, py
        if menu_item("Paste", shortcut="Ctrl+V", enabled=has_clipboard):
            self.graph.unselect_all_items()
            self.graph.paste_selection(
                self.context.flows.clipboard_items,
                self.context.flows.clipboard_pivot,
                selected=True,
            )
            px, py = self.context.flows.clipboard_pivot
            px += self.config.paste_margin
            py += self.config.paste_margin
            self.context.flows.clipboard_pivot = px, py
            self.graph.save_history("Paste selected items")

        imgui.separator()
        if menu_item("Delete", shortcut="Del", enabled=selected_any):
            self.graph.remove_selected_items()
            self.graph.save_history("Remove selected items")

        imgui.separator()
        if menu_item("Reset control"):
            self.reset_controllers()

        imgui.separator()
        if menu_item("Select all"):
            self.graph.unselect_all_items()
            self.graph.select_all_items()
        if menu_item("Select nodes"):
            self.graph.unselect_all_items()
            self.graph.select_all_nodes()
        if menu_item("Select wires"):
            self.graph.unselect_all_items()
            self.graph.select_all_wires()
        if menu_item("Select pins"):
            self.graph.unselect_all_items()
            self.graph.select_all_pins()

    @staticmethod
    def do_disabled_layer_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    def do_layer_menu(self) -> None:
        selected_items = self.graph.selection
        selected_any = bool(selected_items)
        single_item = 1 == len(selected_items)

        if menu_item("To Front", enabled=selected_any):
            self.graph.items_to_front(list(selected_items.values()))
            self.graph.save_history("To front items")
        if menu_item("To Back", enabled=selected_any):
            self.graph.items_to_back(list(selected_items.values()))
            self.graph.save_history("To back items")

        if menu_item("Bring Forward", enabled=single_item):
            assert 1 == len(selected_items)
            self.graph.item_bring_forward(selected_items.first)
            self.graph.save_history("Bring forward items")
        if menu_item("Send Backward", enabled=single_item):
            assert 1 == len(selected_items)
            self.graph.item_send_backward(selected_items.first)
            self.graph.save_history("Send backward items")

    @staticmethod
    def do_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    def do_align_menu(self) -> None:
        nodes = self.graph.selection.nodes
        multiple_item = 2 <= len(nodes)

        if imgui.begin_menu("Align", enabled=multiple_item):
            pivot = nodes[-1]
            try:
                if menu_item("Left"):
                    self.graph.nodes_align_left(nodes, pivot)
                    self.graph.save_history("Align left nodes")
                if menu_item("Center"):
                    self.graph.nodes_align_center(nodes, pivot)
                    self.graph.save_history("Align center nodes")
                if menu_item("Right"):
                    self.graph.nodes_align_right(nodes, pivot)
                    self.graph.save_history("Align right nodes")

                imgui.separator()
                if menu_item("Top"):
                    self.graph.nodes_align_top(nodes, pivot)
                    self.graph.save_history("Align top nodes")
                if menu_item("Middle"):
                    self.graph.nodes_align_middle(nodes, pivot)
                    self.graph.save_history("Align middle nodes")
                if menu_item("Bottom"):
                    self.graph.nodes_align_bottom(nodes, pivot)
                    self.graph.save_history("Align bottom nodes")
            finally:
                imgui.end_menu()

    @staticmethod
    def do_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    def do_distribute_menu(self) -> None:
        nodes = self.graph.selection.nodes
        multiple_item = 2 <= len(nodes)

        if imgui.begin_menu("Distribute", enabled=multiple_item):
            assert self is not None
            if menu_item("Horizontal"):
                self.graph.nodes_distribute_horizontal(nodes)
                self.graph.save_history("Distribute horizontal nodes")
            if menu_item("Vertical"):
                self.graph.nodes_distribute_vertical(nodes)
                self.graph.save_history("Distribute vertical nodes")
            imgui.end_menu()

    @staticmethod
    def do_disabled_run_menu() -> None:
        imgui.begin_menu(f"{mdi.PLAY} Run", enabled=False)
        imgui.begin_menu(f"{mdi.BUG} Debug", enabled=False)
        imgui.separator()
        menu_item(f"{mdi.PAUSE} Pause", enabled=False)
        menu_item(f"{mdi.STOP} Stop", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OVER} Step Over", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_INTO} Step Into", enabled=False)
        menu_item(f"{mdi.DEBUG_STEP_OUT} Step Out", enabled=False)

    def do_run_menu(self) -> None:
        if imgui.begin_menu(f"{mdi.PLAY} Run"):
            try:
                begin_nodes = self.graph.find_begin_nodes()
                if begin_nodes:
                    for node in begin_nodes:
                        if menu_item(node.name):
                            self.context.start_flow_thread(self.graph, node)
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        if imgui.begin_menu(f"{mdi.BUG} Debug"):
            try:
                begin_nodes = self.graph.find_begin_nodes()
                if begin_nodes:
                    for node in begin_nodes:
                        if menu_item(node.name):
                            pass
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        imgui.separator()

        if menu_item(f"{mdi.PAUSE} Pause"):
            pass
        if menu_item(f"{mdi.STOP} Stop"):
            pass
        if menu_item(f"{mdi.DEBUG_STEP_OVER} Step Over"):
            pass
        if menu_item(f"{mdi.DEBUG_STEP_INTO} Step Into"):
            pass
        if menu_item(f"{mdi.DEBUG_STEP_OUT} Step Out"):
            pass

    @staticmethod
    def do_disabled_deploy_menu() -> None:
        menu_item("Upload to ...", enabled=False)

    def do_deploy_menu(self) -> None:
        assert self
        menu_item("Upload to ...", enabled=False)

    def do_add_variable_menu(self) -> None:
        menu_item(f"Add {self._variable_key} variable node", enabled=False)
        imgui.separator()

        if menu_item("Setter"):
            node = self.context.flows.add_setter_node(self.graph, self._variable_key)
            self.update_node_roi(node)
            self.graph.save_history("Add setter variable node", self._variable_key)

        if menu_item("Getter"):
            node = self.context.flows.add_getter_node(self.graph, self._variable_key)
            self.update_node_roi(node)
            self.graph.save_history("Add getter variable node", self._variable_key)

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

    def save_graph(self) -> None:
        try:
            self.context.save_flow_graph(self.graph)
            logger.info(f"The flow graph was successfully saved: '{self.graph.key}'")
        except BaseException as e:
            logger.error(f"Failed to save the flow graph: '{self.graph.key}' -> '{e}'")

    def close_graph(self):
        self.graph.opened = False
        logger.info(f"Close the flow graph: '{self.graph.key}'")

    def reset_controllers(self):
        logger.info("Reset controllers")

        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self.graph.control.pan_x = 0.0
        self.graph.control.pan_y = 0.0
        self.graph.control.zoom = 1.0

    def do_process_controllers(self, debugging=False) -> None:
        if result := self.render_controllers(debugging=debugging):
            self.graph.control.pan_x = result.pan_x
            self.graph.control.pan_y = result.pan_y
            self.graph.control.zoom = result.zoom

    def do_canvas_process(self) -> None:
        if result := self.update_state():
            self.graph.control.pan_x = result.pan_x
            self.graph.control.pan_y = result.pan_y
            self.graph.control.zoom = result.zoom

        self.update_nodes_state()
        self.graph.update_wires_io()
        self.graph.update_wires_polyline()

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

            self.draw_wires()
            self.draw_nodes()

            self.draw_pin_connects()
            self.draw_roi_box()

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
    # region: Update state
    # ==================================================================================

    def update_nodes_state(self) -> None:
        self.graph.clear_state()
        self.graph.update_hovering_state(self.mouse_to_canvas_coords())

        if self.is_pan_mode:
            # Nodes cannot be selected or dragged during 'Canvas Pan Mode'.
            return

        match self._mode:
            case FlowMode.normal:
                self._update_nodes_state_for_normal()
            case FlowMode.node_moving:
                self._update_nodes_state_for_node_moving()
            case FlowMode.pin_connecting:
                self._update_nodes_state_for_pin_connecting()
            case FlowMode.anchor_moving:
                self._update_nodes_state_for_anchor_moving()
            case FlowMode.roi_box:
                self._update_nodes_state_for_selection_box()
            case _:
                assert False, "Inaccessible section"

    def _update_nodes_state_for_normal(self) -> None:
        assert not self.is_pan_mode
        assert self.is_normal_mode

        if self.changed_left_up:
            if self.is_multi_select_mode:
                self.graph.flip_selected_on_hovering_item()
            else:
                hovering_item = self.graph.find_hovering_item()
                self.graph.unselect_all_items()
                if hovering_item is not None:
                    self.graph.select_item(hovering_item)

        if self.activating and self.start_left_dragging:
            if hovering_node := self.graph.find_hovering_node():
                if hovering_pin := hovering_node.find_hovering_pin():
                    self._mode = FlowMode.pin_connecting
                    self._connects.clear()
                    self._connects.append(FlowNodePin(hovering_node, hovering_pin))
                else:
                    self._mode = FlowMode.node_moving
                    if not hovering_node.selected:
                        if not self.is_multi_select_mode:
                            self.graph.unselect_all_items()
                        self.graph.select_item(hovering_node)
            else:
                if hovering_anchor := self.graph.find_hovering_anchor():
                    hovering_anchor.selected = True
                    self._mode = FlowMode.anchor_moving
                else:
                    self._mode = FlowMode.roi_box
                    if not self.is_multi_select_mode:
                        self.graph.unselect_all_items()
                    self._roi = self.mx, self.my, self.mx, self.my
                    self._selection_stash = self.graph.selection.copy()

    def _update_nodes_state_for_node_moving(self) -> None:
        assert not self.is_pan_mode
        assert self.is_node_moving_mode

        io = imgui.get_io()
        dx = io.mouse_delta.x / self.zoom
        dy = io.mouse_delta.y / self.zoom
        self.graph.move_on_selected_nodes((dx, dy))

        if self.changed_left_up:
            self._mode = FlowMode.normal
            self.graph.save_history("The nodes has been moved")

    def _update_nodes_state_for_pin_connecting(self) -> None:
        assert not self.is_pan_mode
        assert self.is_pin_connecting_mode
        assert 1 <= len(self._connects)

        connect_pairs = list()

        if hovering_np := self.graph.find_hovering_pin():
            for conn in self._connects:
                try:
                    pair = FlowConnection.reorder_connectable_pins(conn, hovering_np)
                    connect_pairs.append(pair)
                except (ValueError, TypeError):
                    connect_pairs.clear()
                    break
            hovering_np.pin.connectable = bool(connect_pairs)

        if self.changed_left_up:
            self._mode = FlowMode.normal
            self._connects.clear()
            if connect_pairs:
                for out_conn, in_conn in connect_pairs:
                    self.graph.connect_pins(out_conn, in_conn, no_reorder=True)
                self.graph.save_history("The pins has been connected")

    def _update_nodes_state_for_anchor_moving(self) -> None:
        assert not self.is_pan_mode
        assert self.is_anchor_moving_mode

        io = imgui.get_io()
        dx = io.mouse_delta.x / self.zoom
        dy = io.mouse_delta.y / self.zoom
        self.graph.move_on_selected_anchor((dx, dy))

        if self.changed_left_up:
            self._mode = FlowMode.normal
            selected_wire = self.graph.selected_wire_only
            assert selected_wire is not None
            selected_wire.start_anchor.selected = False
            selected_wire.end_anchor.selected = False
            self.graph.save_history("The anchor has been moved")

    def _update_nodes_state_for_selection_box(self) -> None:
        assert not self.is_pan_mode
        assert self.is_roi_box_mode
        assert self._roi is not None
        assert self._selection_stash is not None

        self._roi = self._roi[0], self._roi[1], self.mx, self.my
        canvas_roi = self.screen_to_canvas_roi(self._roi)

        for node in self.graph.nodes:
            if is_rectangle_collision(canvas_roi, node.node_roi):
                node.selected = node not in self._selection_stash
            else:
                node.selected = node in self._selection_stash

        if self.changed_left_up:
            self._mode = FlowMode.normal
            self._roi = None
            self._selection_stash = None
            for node in self.graph.nodes:
                self.graph.update_selected_item(node)

    # ==================================================================================
    # endregion: Update state
    # ==================================================================================
    # region: Style properties
    # ==================================================================================

    @property
    def node_show_layout(self):
        return self.config.nodes.show_layout

    @property
    def node_item_spacing(self):
        return self.config.nodes.item_spacing

    @staticmethod
    def get_node_color_u32(node: FlowNode) -> int:
        return imgui.get_color_u32(node.color)

    def get_node_line_color(self, node: FlowNode) -> RGBA:
        if node.selected:
            return self.config.nodes.selected_color
        elif node.hovering:
            return self.config.nodes.hovering_color
        else:
            return self.config.nodes.normal_color

    def get_node_line_color_u32(self, node: FlowNode) -> int:
        return imgui.get_color_u32(self.get_node_line_color(node))

    @property
    def node_label_color_u32(self) -> int:
        return imgui.get_color_u32(self.config.nodes.label_color)

    @property
    def node_layout_color_u32(self) -> int:
        return imgui.get_color_u32(self.config.nodes.layout_color)

    @property
    def node_background_color_u32(self) -> int:
        return imgui.get_color_u32(self.config.nodes.background_color)

    def get_node_line_thickness(self, node: FlowNode) -> float:
        if node.selected:
            return self.config.nodes.selected_thickness
        elif node.hovering:
            return self.config.nodes.hovering_thickness
        else:
            return self.config.nodes.normal_thickness

    @property
    def node_rounding(self) -> float:
        return self.config.nodes.rounding

    @property
    def anchor_radius(self):
        return self.config.anchors.radius

    def get_pin_color(self, pin: FlowPin) -> RGBA:
        if self.is_pin_connecting_mode:
            if pin.hovering and pin.connectable:
                return self.config.pins.selected_color
            else:
                return self.config.pins.normal_color
        else:
            if pin.selected:
                return self.config.pins.selected_color
            elif pin.hovering:
                return self.config.pins.hovering_color
            else:
                return self.config.pins.normal_color

    def get_wire_color(self, wire: FlowWire) -> RGBA:
        if wire.selected:
            return self.config.wires.selected_color
        elif wire.hovering:
            return self.config.wires.hovering_color
        else:
            return self.config.wires.normal_color

    def get_wire_color_u32(self, wire: FlowWire) -> int:
        return imgui.get_color_u32(self.get_wire_color(wire))

    def get_wire_thickness(self, wire: FlowWire) -> float:
        if wire.selected:
            return self.config.wires.selected_thickness
        elif wire.hovering:
            return self.config.wires.hovering_thickness
        else:
            return self.config.wires.normal_thickness

    def get_anchor_color(self, anchor: FlowAnchor) -> RGBA:
        if anchor.selected:
            return self.config.anchors.selected_color
        elif anchor.hovering:
            return self.config.anchors.hovering_color
        else:
            return self.config.anchors.normal_color

    def get_anchor_color_u32(self, anchor: FlowAnchor) -> int:
        return imgui.get_color_u32(self.get_anchor_color(anchor))

    # ==================================================================================
    # endregion: Style properties
    # ==================================================================================
    # region: Node Operations
    # ==================================================================================

    def update_nodes_rois(self) -> None:
        for node in self.graph.nodes:
            self.update_node_roi(node)

    def update_node_roi(self, node: FlowNode) -> None:
        if True:  # with self.icon_font:
            node_icon_w, node_icon_h = calc_text_size(node.icon)

        if True:  # with self.title_font:
            node_name_w, node_name_h = calc_text_size(node.name)

        title_h = max(node_icon_h, node_name_h)
        icon_y_diff = title_h / 2 - node_icon_h / 2
        title_y_diff = title_h / 2 - node_name_h / 2

        if True:  # with self.pin_font:
            exec_n_w, exec_n_h = calc_text_size(self.config.pins.exec_n_icon)
            exec_y_w, exec_y_h = calc_text_size(self.config.pins.exec_y_icon)
            data_n_w, data_n_h = calc_text_size(self.config.pins.data_n_icon)
            data_y_w, data_y_h = calc_text_size(self.config.pins.data_y_icon)

        iw = max(exec_y_w, exec_n_w, data_y_w, data_n_w)
        ih = max(exec_y_h, exec_n_h, data_y_h, data_n_h)

        visible_exec_inputs = [p for p in node.exec_inputs if not p.hidden]
        visible_exec_outputs = [p for p in node.exec_outputs if not p.hidden]
        visible_data_inputs = [p for p in node.data_inputs if not p.hidden]
        visible_data_outputs = [p for p in node.data_outputs if not p.hidden]

        visible_inputs = visible_exec_inputs + visible_data_inputs
        visible_outputs = visible_exec_outputs + visible_data_outputs

        if True:  # with self.text_font:
            for pin in node.pins:
                pin.icon_size = iw, ih
                pin.name_size = calc_text_size(pin.name)
            input_name_sizes = [p.name_size for p in visible_inputs if not p.hidden]
            output_name_sizes = [p.name_size for p in visible_outputs if not p.hidden]

        inw = max(s[0] for s in input_name_sizes) if input_name_sizes else 0.0
        inh = max(s[1] for s in input_name_sizes) if input_name_sizes else 0.0
        onw = max(s[0] for s in output_name_sizes) if output_name_sizes else 0.0
        onh = max(s[1] for s in output_name_sizes) if output_name_sizes else 0.0
        pin_name_h = max(inh, onh)

        pin_h = max(ih, inh, onh)
        pin_icon_y_diff = pin_h / 2 - ih / 2
        pin_name_y_diff = pin_h / 2 - pin_name_h / 2

        isw, ish = self.node_item_spacing
        center_padding = isw * 4

        wt = isw + node_icon_w + isw + node_name_w + isw
        wf = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        wd = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        node_w = max((wt, wf, wd))

        exec_line_count = max(len(visible_exec_inputs), len(visible_exec_outputs))
        data_line_count = max(len(visible_data_inputs), len(visible_data_outputs))

        head_h = ish + title_h + ish
        exec_h = ish + (ih + ish) * exec_line_count
        data_h = ish + (ih + ish) * data_line_count
        node_h = head_h + exec_h + data_h

        node.head_height = head_h
        node.exec_height = exec_h
        node.data_height = data_h

        node_icon_x = isw
        node_icon_y = ish + icon_y_diff
        node.icon_pos = node_icon_x, node_icon_y
        node.icon_size = node_icon_w, node_icon_h

        node_name_x = node.icon_pos[0] + node.icon_size[0] + isw
        node_name_y = ish + title_y_diff
        node.name_pos = node_name_x, node_name_y
        node.name_size = node_name_w, node_name_h

        node.node_pos = self.mouse_to_canvas_coords()
        node.node_size = node_w, node_h

        for i, pin in enumerate(visible_exec_inputs):
            icon_x = isw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_data_inputs):
            icon_x = isw
            icon_y = head_h + exec_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_exec_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_data_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + exec_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

    def draw_nodes(self) -> None:
        for node in reversed(self.graph.nodes):
            self.draw_node(node)

    def draw_node(self, node: FlowNode) -> None:
        node_roi = self.canvas_to_screen_roi(node.node_roi)
        thickness = self.get_node_line_thickness(node)
        rounding = self.node_rounding
        node_color = self.get_node_color_u32(node)
        line_color = self.get_node_line_color_u32(node)
        label_color = self.node_label_color_u32
        layout_color = self.node_layout_color_u32
        background_color = self.node_background_color_u32

        nx1, ny1, nx2, ny2 = node_roi
        np1 = nx1, ny1
        np2 = nx2, ny2
        zoom = self.zoom

        header_roi = nx1, ny1, nx2, ny1 + node.head_height * zoom
        hp1 = header_roi[0], header_roi[1]
        hp2 = header_roi[2], header_roi[3]

        self._draw_list.add_rect_filled(np1, np2, background_color, rounding)
        self._draw_list.add_rect_filled(hp1, hp2, node_color, rounding)
        self._draw_list.add_rect(np1, np2, line_color, rounding, 0, thickness)

        if True:  # with self.icon_font:
            x1 = nx1 + node.icon_pos[0] * zoom
            y1 = ny1 + node.icon_pos[1] * zoom
            self._draw_list.add_text((x1, y1), label_color, node.icon)
            if self.node_show_layout:
                x2 = x1 + node.icon_size[0] * zoom
                y2 = y1 + node.icon_size[1] * zoom
                self._draw_list.add_rect((x1, y1), (x2, y2), layout_color)

        if True:  # with self.title_font:
            x1 = nx1 + node.name_pos[0] * zoom
            y1 = ny1 + node.name_pos[1] * zoom
            self._draw_list.add_text((x1, y1), label_color, node.name)
            if self.node_show_layout:
                x2 = x1 + node.name_size[0] * zoom
                y2 = y1 + node.name_size[1] * zoom
                self._draw_list.add_rect((x1, y1), (x2, y2), layout_color)

        visible_exec_inputs = [p for p in node.exec_inputs if not p.hidden]
        visible_exec_outputs = [p for p in node.exec_outputs if not p.hidden]
        visible_data_inputs = [p for p in node.data_inputs if not p.hidden]
        visible_data_outputs = [p for p in node.data_outputs if not p.hidden]

        visible_execs = visible_exec_inputs + visible_exec_outputs
        visible_datas = visible_data_inputs + visible_data_outputs

        visible_pins = visible_execs + visible_datas

        # visible_inputs = visible_exec_inputs + visible_data_inputs
        # visible_outputs = visible_exec_outputs + visible_data_outputs

        if True:  # with self.pin_font:
            exec_pin_n_icon = self.config.pins.exec_n_icon
            exec_pin_y_icon = self.config.pins.exec_y_icon

            for pin in visible_execs:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = exec_pin_y_icon if pin.connected else exec_pin_n_icon
                pin_rgba = self.get_pin_color(pin)
                pin_color = imgui.get_color_u32(pin_rgba)
                self._draw_list.add_text((x1, y1), pin_color, pin_icon)
                if self.node_show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect((x1, y1), (x2, y2), layout_color)

            data_pin_n_icon = self.config.pins.data_n_icon
            data_pin_y_icon = self.config.pins.data_y_icon

            for pin in visible_datas:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                pin_rgba = self.get_pin_color(pin)
                pin_color = imgui.get_color_u32(pin_rgba)
                self._draw_list.add_text((x1, y1), pin_color, pin_icon)
                if self.node_show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect((x1, y1), (x2, y2), layout_color)

        if True:  # with self.text_font:
            for pin in visible_pins:
                x1 = nx1 + pin.name_pos[0] * zoom
                y1 = ny1 + pin.name_pos[1] * zoom
                self._draw_list.add_text((x1, y1), label_color, pin.name)
                if self.node_show_layout:
                    x2 = x1 + pin.name_size[0] * zoom
                    y2 = y1 + pin.name_size[1] * zoom
                    self._draw_list.add_rect((x1, y1), (x2, y2), layout_color)

    # ==================================================================================
    # endregion: Node Operations
    # ==================================================================================
    # region: Arc Operations
    # ==================================================================================

    def draw_wires(self) -> None:
        for wire in self.graph.wires:
            assert wire.output is not None
            assert wire.input is not None
            self.draw_wire(wire)

        if selected_wire := self.graph.selected_wire_only:
            if selected_wire.selected and selected_wire.is_bezier_cubic_line_type:
                self.draw_bezier_cubic_anchors(selected_wire)

    def draw_wire(self, wire: FlowWire) -> None:
        color = self.get_wire_color_u32(wire)
        thickness = self.get_wire_thickness(wire)
        points = [self.canvas_to_screen_coords(p) for p in wire.polyline]
        self._draw_list.add_polyline(points, color, 0, thickness)

    def draw_bezier_cubic_anchors(self, wire: FlowWire) -> None:
        assert wire.is_bezier_cubic_line_type
        assert 2 <= len(wire.polyline)

        # The first/last index point is located at the connected pin.
        sx, sy = self.canvas_to_screen_coords(wire.polyline[0])
        ex, ey = self.canvas_to_screen_coords(wire.polyline[-1])

        radius = self.anchor_radius
        start, end = wire.get_bezier_cubic_anchors()

        start_color = self.get_anchor_color_u32(wire.start_anchor)
        sax, say = self.canvas_to_screen_coords(start)
        draw_dotted_line(self._draw_list, sx, sy, sax, say, start_color)
        self._draw_list.add_circle_filled((sax, say), radius, start_color)

        end_color = self.get_anchor_color_u32(wire.end_anchor)
        eax, eay = self.canvas_to_screen_coords(end)
        draw_dotted_line(self._draw_list, ex, ey, eax, eay, end_color)
        self._draw_list.add_circle_filled((eax, eay), radius, end_color)

    # ==================================================================================
    # endregion: Arc Operations
    # ==================================================================================
    # region: Pin Operations
    # ==================================================================================

    def draw_pin_connect(self, connect: FlowNodePin) -> None:
        node = connect.node
        pin = connect.pin

        node_roi = self.canvas_to_screen_roi(node.node_roi)
        nx = node_roi[0]
        ny = node_roi[1]
        zoom = self.zoom
        x1 = nx + pin.icon_pos[0] * zoom + pin.icon_size[0] * zoom / 2.0
        y1 = ny + pin.icon_pos[1] * zoom + pin.icon_size[1] * zoom / 2.0
        mx, my = self._mouse_pos

        color = imgui.get_color_u32(self.config.pins.connection_color)
        thickness = self.config.pins.connection_thickness
        self._draw_list.add_line((x1, y1), (mx, my), color, thickness)

    def draw_pin_connects(self) -> None:
        if not self.is_pin_connecting_mode:
            return

        for connect in self._connects:
            self.draw_pin_connect(connect)

    # ==================================================================================
    # endregion: Pin Operation
    # ==================================================================================
    # region: ROI Operations
    # ==================================================================================

    def draw_roi_box(self) -> None:
        if not self.is_roi_box_mode:
            return

        assert self._roi is not None
        x1, y1, x2, y2 = self._roi
        color = imgui.get_color_u32(self.config.roi.color)
        rounding = self.config.roi.rounding
        thickness = self.config.roi.thickness
        p1 = x1, y1
        p2 = x2, y2
        self._draw_list.add_rect_filled(p1, p2, color)
        self._draw_list.add_rect(p1, p2, color, rounding, 0, thickness)

    # ==================================================================================
    # endregion: ROI Operations
    # ==================================================================================
