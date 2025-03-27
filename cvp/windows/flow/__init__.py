# -*- coding: utf-8 -*-

from typing import Callable, Sequence, Tuple

from imgui_bundle import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.proxies.flow import SplitTreeProxy
from cvp.dtypes.dtype import Dtype
from cvp.fonts.glyphs.mdi import (
    BUG,
    DEBUG_STEP_INTO,
    DEBUG_STEP_OUT,
    DEBUG_STEP_OVER,
    PAUSE,
    PLAY,
    STOP,
)
from cvp.imgui.begin_child import begin_child, end_child
from cvp.imgui.drag_types import DRAG_FLOW_DTYPE, DRAG_FLOW_NODE, DRAG_FLOW_VARIABLE
from cvp.imgui.flags.child import BORDERS
from cvp.imgui.flags.color_var import CHILD_BG
from cvp.imgui.flags.style_var import WINDOW_PADDING
from cvp.imgui.flags.window import CANVAS_FLAGS, MENU_BAR
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.push_style_var import style_item_spacing_context
from cvp.imgui.text_centered import text_centered
from cvp.logging.logging import flow_logger as logger
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.aui import AuiWindow
from cvp.widgets.canvas.flow import FlowCanvas
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.splitter import Splitter
from cvp.windows.flow.bottom import FlowBottomTabs
from cvp.windows.flow.catalog import Catalog
from cvp.windows.flow.left import FlowLeftTabs
from cvp.windows.flow.right import FlowRightTabs


class FlowWindow(AuiWindow[FlowAuiConfig]):
    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.flow_aui,
            title="Flow",
            closable=True,
            flags=MENU_BAR,
            min_width=MIN_WINDOW_WIDTH,
            min_height=MIN_WINDOW_HEIGHT,
            modifiable_title=False,
        )

        self._canvases = FlowCanvasTabs(context)
        self._catalog = Catalog(context)
        self._left_tabs = FlowLeftTabs(context)
        self._right_tabs = FlowRightTabs(context)
        self._bottom_tabs = FlowBottomTabs(context)

        self._split_tree = SplitTreeProxy(context.config.flow_aui)
        self._tree_splitter = Splitter.from_horizontal(
            "##HSplitterTree",
            value_proxy=self._split_tree,
            min_value=context.config.flow_aui.min_split_tree,
            negative_delta=True,
        )

        self._drag_dtype = Dtype.any()
        self._variable_key = str()

        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layout", self.on_layout_menu),
            ("Run", self.on_run_menu),
            ("Deploy", self.on_deploy_menu),
            ("View", self.on_view_menu),
        )

        self._new_graph_popup = InputTextPopup(
            title="New graph",
            label="Please enter a graph name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_graph_popup,
        )
        self._import_graph_popup = OpenFilePopup(
            title="Import graph",
            target=self.on_import_file_popup,
        )
        self._export_graph_popup = OpenFilePopup(
            title="Export graph",
            target=self.on_export_file_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove graph?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._add_variable_popup = InputTextPopup(
            title="New variable",
            label="Please enter a variable name:",
            ok="Add",
            cancel="Cancel",
            target=self.on_add_variable,
        )

        self.register_popup(self._new_graph_popup)
        self.register_popup(self._import_graph_popup)
        self.register_popup(self._export_graph_popup)
        self.register_popup(self._confirm_remove)
        self.register_popup(self._add_variable_popup)

    @property
    def split_tree(self) -> float:
        return self.window_config.split_tree

    @split_tree.setter
    def split_tree(self, value: float) -> None:
        self.window_config.split_tree = value

    @property
    def show_layout(self) -> bool:
        return self.window_config.nodes.show_layout

    @show_layout.setter
    def show_layout(self, value: bool) -> None:
        self.window_config.nodes.show_layout = value

    @property
    def autoscroll(self) -> bool:
        return self.window_config.logs.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.window_config.logs.autoscroll = value

    def on_new_graph_popup(self, name: str) -> None:
        graph = self.context.fm.create_graph(name, append=True)
        filepath = self.context.home.flows.graph_filepath(graph.key)
        if filepath.exists():
            raise FileExistsError(f"Graph file already exists: '{str(filepath)}'")
        self.context.fm.write_graph_yaml(filepath, graph)
        self._canvases.open(graph)

    def on_import_file_popup(self, file: str) -> None:
        pass

    def on_export_file_popup(self, file: str) -> None:
        pass

    def on_confirm_remove(self, value: bool) -> None:
        pass

    def on_add_variable(self, name: str) -> None:
        if not name:
            raise ValueError("Variable name cannot be empty")

        canvas = self._canvases.canvas
        if canvas is None:
            raise ValueError("Canvas cannot be none")

        with canvas:
            canvas.graph.add_variable(name, self._drag_dtype)

    @override
    def on_process(self) -> None:
        self.on_menu()
        super().on_process()

    @staticmethod
    def _process_disabled_edit_menu() -> None:
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

    def _process_enabled_edit_menu(self, canvas: FlowCanvas) -> None:
        assert canvas.opened

        undoable = canvas.history.undoable
        redoable = canvas.history.redoable
        selected_any = bool(canvas.graph.selection)
        has_clipboard = self.context.fm.has_clipboard

        if menu_item("Undo", shortcut="Ctrl+Z", enabled=undoable):
            canvas.undo_history()
        if menu_item("Redo", shortcut="Ctrl+Y", enabled=redoable):
            canvas.redo_history()

        imgui.separator()
        if menu_item("Cut", shortcut="Ctrl+X", enabled=selected_any):
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            self.context.fm.clipboard_pivot = canvas.graph.selection.group_pos
            canvas.graph.remove_selected_items()
            canvas.save_history("Cut selected items")
        if menu_item("Copy", shortcut="Ctrl+C", enabled=selected_any):
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            px, py = canvas.graph.selection.group_pos
            px += self.window_config.paste_margin
            py += self.window_config.paste_margin
            self.context.fm.clipboard_pivot = px, py
        if menu_item("Paste", shortcut="Ctrl+V", enabled=has_clipboard):
            canvas.graph.unselect_all_items()
            canvas.graph.paste_selection(
                self.context.fm.clipboard_items,
                self.context.fm.clipboard_pivot,
                selected=True,
            )
            px, py = self.context.fm.clipboard_pivot
            px += self.window_config.paste_margin
            py += self.window_config.paste_margin
            self.context.fm.clipboard_pivot = px, py
            canvas.save_history("Paste selected items")

        imgui.separator()
        if menu_item("Delete", shortcut="Del", enabled=selected_any):
            canvas.graph.remove_selected_items()
            canvas.save_history("Remove selected items")

        imgui.separator()
        if menu_item("Reset control"):
            canvas.reset_controllers()

        imgui.separator()
        if menu_item("Select all"):
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_items()
        if menu_item("Select nodes"):
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_nodes()
        if menu_item("Select wires"):
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_wires()
        if menu_item("Select pins"):
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_pins()

    @staticmethod
    def _process_enabled_layout_menu(canvas: FlowCanvas) -> None:
        assert canvas.opened

        selected_items = canvas.graph.selection
        selected_any = bool(selected_items)
        single_item = 1 == len(selected_items)

        if menu_item("To Front", enabled=selected_any):
            canvas.graph.items_to_front(list(selected_items.values()))
            canvas.save_history("To front items")
        if menu_item("To Back", enabled=selected_any):
            canvas.graph.items_to_back(list(selected_items.values()))
            canvas.save_history("To back items")

        if menu_item("Bring Forward", enabled=single_item):
            assert 1 == len(selected_items)
            canvas.graph.item_bring_forward(selected_items.first)
            canvas.save_history("Bring forward items")
        if menu_item("Send Backward", enabled=single_item):
            assert 1 == len(selected_items)
            canvas.graph.item_send_backward(selected_items.first)
            canvas.save_history("Send backward items")

    @staticmethod
    def _process_disabled_layout_menu() -> None:
        menu_item("To Front", enabled=False)
        menu_item("To Back", enabled=False)
        menu_item("Bring Forward", enabled=False)
        menu_item("Send Backward", enabled=False)

    @staticmethod
    def _process_enabled_align_menu(canvas: FlowCanvas) -> None:
        assert canvas.opened

        nodes = canvas.graph.selection.nodes
        multiple_item = 2 <= len(nodes)

        if imgui.begin_menu("Align", enabled=multiple_item):
            pivot = nodes[-1]
            try:
                if menu_item("Left"):
                    canvas.graph.nodes_align_left(nodes, pivot)
                    canvas.save_history("Align left nodes")
                if menu_item("Center"):
                    canvas.graph.nodes_align_center(nodes, pivot)
                    canvas.save_history("Align center nodes")
                if menu_item("Right"):
                    canvas.graph.nodes_align_right(nodes, pivot)
                    canvas.save_history("Align right nodes")

                imgui.separator()
                if menu_item("Top"):
                    canvas.graph.nodes_align_top(nodes, pivot)
                    canvas.save_history("Align top nodes")
                if menu_item("Middle"):
                    canvas.graph.nodes_align_middle(nodes, pivot)
                    canvas.save_history("Align middle nodes")
                if menu_item("Bottom"):
                    canvas.graph.nodes_align_bottom(nodes, pivot)
                    canvas.save_history("Align bottom nodes")
            finally:
                imgui.end_menu()

    @staticmethod
    def _process_disabled_align_menu() -> None:
        imgui.begin_menu("Align", enabled=False)

    @staticmethod
    def _process_enabled_distribute_menu(canvas: FlowCanvas) -> None:
        assert canvas.opened

        nodes = canvas.graph.selection.nodes
        multiple_item = 2 <= len(nodes)

        if imgui.begin_menu("Distribute", enabled=multiple_item):
            assert canvas is not None
            if menu_item("Horizontal"):
                canvas.graph.nodes_distribute_horizontal(nodes)
                canvas.save_history("Distribute horizontal nodes")
            if menu_item("Vertical"):
                canvas.graph.nodes_distribute_vertical(nodes)
                canvas.save_history("Distribute vertical nodes")
            imgui.end_menu()

    @staticmethod
    def _process_disabled_distribute_menu() -> None:
        imgui.begin_menu("Distribute", enabled=False)

    def _process_enabled_run_menu(self, canvas: FlowCanvas) -> None:
        assert canvas.opened

        if imgui.begin_menu(f"{PLAY} Run"):
            try:
                begin_nodes = canvas.graph.find_begin_nodes()
                if begin_nodes:
                    for node in begin_nodes:
                        if menu_item(node.name):
                            self.context.start_flow_thread(canvas.graph, node)
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        if imgui.begin_menu(f"{BUG} Debug"):
            try:
                begin_nodes = canvas.graph.find_begin_nodes()
                if begin_nodes:
                    for node in begin_nodes:
                        if menu_item(node.name):
                            pass
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        imgui.separator()

        if menu_item(f"{PAUSE} Pause"):
            pass
        if menu_item(f"{STOP} Stop"):
            pass
        if menu_item(f"{DEBUG_STEP_OVER} Step Over"):
            pass
        if menu_item(f"{DEBUG_STEP_INTO} Step Into"):
            pass
        if menu_item(f"{DEBUG_STEP_OUT} Step Out"):
            pass

    @staticmethod
    def _process_disabled_run_menu() -> None:
        imgui.begin_menu(f"{PLAY} Run", enabled=False)
        imgui.begin_menu(f"{BUG} Debug", enabled=False)
        imgui.separator()
        menu_item(f"{PAUSE} Pause", enabled=False)
        menu_item(f"{STOP} Stop", enabled=False)
        menu_item(f"{DEBUG_STEP_OVER} Step Over", enabled=False)
        menu_item(f"{DEBUG_STEP_INTO} Step Into", enabled=False)
        menu_item(f"{DEBUG_STEP_OUT} Step Out", enabled=False)

    @staticmethod
    def _process_enabled_deploy_menu(canvas: FlowCanvas) -> None:
        assert canvas.opened

        if menu_item("Upload to ...", enabled=False):
            pass

    @staticmethod
    def _process_disabled_deploy_menu() -> None:
        menu_item("Upload to ...", enabled=False)

    def _process_add_variable_menu(self, canvas: FlowCanvas) -> None:
        menu_item(f"Add {self._variable_key} variable node", enabled=False)
        imgui.separator()

        if menu_item("Setter"):
            node = self.context.fm.add_setter_node(canvas.graph, self._variable_key)
            canvas.update_node_roi(node)
            canvas.save_history("Add setter variable node", self._variable_key)

        if menu_item("Getter"):
            node = self.context.fm.add_getter_node(canvas.graph, self._variable_key)
            canvas.update_node_roi(node)
            canvas.save_history("Add getter variable node", self._variable_key)

    def on_menu(self) -> None:
        if imgui.begin_menu_bar():
            try:
                for name, func in self._menus:
                    if imgui.begin_menu(name):
                        try:
                            func()
                        finally:
                            imgui.end_menu()
            finally:
                imgui.end_menu_bar()

    def on_file_menu(self) -> None:
        if menu_item("New graph"):
            self._new_graph_popup.show()

        if imgui.begin_menu("Open graph"):
            try:
                if self.context.fm.graphs:
                    for uuid, graph in self.context.fm.graphs.items():
                        if menu_item(graph.name):
                            self._canvases.open(graph)
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        if imgui.begin_menu("Recent graphs"):
            try:
                if self.window_config.recent:
                    for recent in self.window_config.recent:
                        if menu_item(recent):
                            pass
                else:
                    menu_item("[Empty]", enabled=False)
            finally:
                imgui.end_menu()

        imgui.separator()
        has_opened_graph = self._canvases.opened
        if menu_item("Save graph", enabled=has_opened_graph):
            self.save_current_graph()
        if menu_item("Save and close graph", enabled=has_opened_graph):
            self.save_current_graph()
            self.close_current_graph()
        if menu_item("Close graph", enabled=has_opened_graph):
            self.close_current_graph()

        imgui.separator()
        if menu_item("Import graph"):
            self._import_graph_popup.show()
        if menu_item("Export graph"):
            self._export_graph_popup.show()

        imgui.separator()
        if menu_item("Refresh graphs"):
            self.save_current_graph()
            self.refresh_graphs()

        imgui.separator()
        if menu_item("Close flow window"):
            self.close()

    def on_edit_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                if canvas.opened:
                    self._process_enabled_edit_menu(canvas)
                    return
        self._process_disabled_edit_menu()

    def on_layout_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                if canvas.opened:
                    self._process_enabled_layout_menu(canvas)
                    imgui.separator()
                    self._process_enabled_align_menu(canvas)
                    self._process_enabled_distribute_menu(canvas)
                    return

        self._process_disabled_layout_menu()
        imgui.separator()
        self._process_disabled_align_menu()
        self._process_disabled_distribute_menu()

    def on_run_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                if canvas.opened:
                    self._process_enabled_run_menu(canvas)
                    return
        self._process_disabled_run_menu()

    def on_deploy_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                if canvas.opened:
                    self._process_enabled_deploy_menu(canvas)
                    return
        self._process_disabled_deploy_menu()

    def on_view_menu(self) -> None:
        if autoscroll := menu_item("Autoscroll logs", selected=self.autoscroll):
            self.autoscroll = autoscroll.state

        imgui.separator()
        if show_layout := menu_item("Show Layout", selected=self.show_layout):
            self.show_layout = show_layout.state

    def save_current_graph(self) -> None:
        graph = self._canvases.graph
        if graph is None:
            return

        try:
            self.context.save_graph(graph)
            logger.info(f"The flow graph was successfully saved: '{graph.key}'")
        except BaseException as e:
            logger.error(f"Failed to save the flow graph: '{graph.key}' -> '{e}'")

    def close_current_graph(self):
        graph = self._canvases.graph
        if graph is None:
            return

        self._canvases.close()
        logger.info(f"Close the flow graph: '{graph.key}'")

    def refresh_graphs(self) -> None:
        graph_uuid_stash = str()

        if graph := self._canvases.graph:
            graph_uuid_stash = graph.key

        self.context.fm.graphs.clear()
        self._canvases.clear()

        try:
            self.context.fm.refresh_flow_graphs()
            logger.info("Refresh flow graphs")
        except BaseException as e:
            logger.error(e)

        if graph_uuid_stash:
            if graph := self.context.fm.graphs.get(graph_uuid_stash):
                self._canvases.open(graph)

    @override
    def on_process_sidebar_left(self):
        if begin_child("## ChildLeftTop", 0, -self.split_tree):
            try:
                self._left_tabs.do_process(self._canvases)
            finally:
                end_child()

        with style_item_spacing_context(0, -1):
            self._tree_splitter.do_process()

        if begin_child("## ChildLeftBottom"):
            try:
                with style_item_spacing_context(0, 0):
                    imgui.dummy((0, self.padding_height))
                self._catalog.on_process()
            finally:
                end_child()

    @override
    def on_process_sidebar_right(self):
        imgui.text("Canvas controller:")
        if canvas := self._canvases.canvas:
            with canvas:
                canvas.do_process_controllers(debugging=self.context.debug)
        imgui.spacing()
        self._right_tabs.do_process(self._canvases)

    @override
    def on_process_bottom(self):
        self._bottom_tabs.do_process(self._canvases)

    @override
    def on_process_main(self) -> None:
        canvas = self._canvases.canvas
        if canvas is None:
            text_centered("Please select a graph")
            return

        self.begin_child_canvas()
        try:
            with canvas:
                self.on_canvas_events(canvas)
                self.on_canvas(canvas)
        finally:
            imgui.end_child()

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(WINDOW_PADDING, (0, 0))
        imgui.push_style_color(CHILD_BG, (0.5, 0.5, 0.5, 1.0))
        try:
            begin_child(
                "##Canvas",
                child_flags=BORDERS,
                window_flags=CANVAS_FLAGS,
            )
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()
            end_child()

    def on_canvas_events(self, canvas: FlowCanvas) -> None:
        assert canvas.opened
        ctrl_down = canvas.ctrl_down
        shift_down = canvas.shift_down
        alt_down = canvas.alt_down
        only_ctrl = ctrl_down and not shift_down and not alt_down
        ctrl_shift = ctrl_down and shift_down and not alt_down

        if self.imgui_is_pressed_delete():
            canvas.graph.remove_selected_items()
            canvas.save_history("Remove selected items")
            return

        if self.imgui_is_pressed_escape():
            canvas.graph.unselect_all_items()
            return

        if canvas.history.undoable:
            if only_ctrl and self.imgui_is_pressed_z():
                canvas.undo_history()
                return

        if canvas.history.redoable:
            if only_ctrl and self.imgui_is_pressed_y():
                canvas.redo_history()
                return
            elif ctrl_shift and self.imgui_is_pressed_z():
                canvas.redo_history()
                return

        if only_ctrl and self.imgui_is_pressed_a():
            canvas.graph.select_all_nodes()
            return

        if ctrl_shift and self.imgui_is_pressed_a():
            canvas.graph.select_all_items()
            return

        if only_ctrl and self.imgui_is_pressed_x():
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            self.context.fm.clipboard_pivot = canvas.graph.selection.group_pos
            canvas.graph.remove_selected_items()
            canvas.save_history("Cut selected items")
            return

        if only_ctrl and self.imgui_is_pressed_c():
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            px, py = canvas.graph.selection.group_pos
            px += self.window_config.paste_margin
            py += self.window_config.paste_margin
            self.context.fm.clipboard_pivot = px, py
            canvas.save_history("Copy selected items")
            return

        if only_ctrl and self.imgui_is_pressed_v():
            canvas.graph.unselect_all_items()
            canvas.graph.paste_selection(
                self.context.fm.clipboard_items,
                self.context.fm.clipboard_pivot,
                selected=True,
            )
            px, py = self.context.fm.clipboard_pivot
            px += self.window_config.paste_margin
            py += self.window_config.paste_margin
            self.context.fm.clipboard_pivot = px, py
            canvas.save_history("Paste selected items")
            return

    def on_canvas(self, canvas: FlowCanvas) -> None:
        assert canvas.opened
        canvas.do_process_canvas()

        if imgui.begin_drag_drop_target():
            try:
                if payload := imgui.accept_drag_drop_payload_py_id(DRAG_FLOW_DTYPE):
                    self._drag_dtype = self.context.fm.dtypes[payload.type]
                    self._add_variable_popup.show()

                if payload := imgui.accept_drag_drop_payload_py_id(DRAG_FLOW_NODE):
                    node = self.context.fm.add_node(canvas.graph, payload.type)
                    canvas.update_node_roi(node)
                    canvas.save_history("Add a new node", payload.type)

                if payload := imgui.accept_drag_drop_payload_py_id(DRAG_FLOW_VARIABLE):
                    self._variable_key = payload.type
                    imgui.open_popup("AddVariableNodeMenus")
            finally:
                imgui.end_drag_drop_target()

        if imgui.begin_popup_context_window("AddVariableNodeMenus"):
            try:
                self._process_add_variable_menu(canvas)
            finally:
                imgui.end_popup()

        if imgui.begin_popup_context_window("CommonMenus"):
            try:
                self._process_enabled_edit_menu(canvas)
                imgui.separator()
                self._process_enabled_layout_menu(canvas)
                imgui.separator()
                self._process_enabled_align_menu(canvas)
                self._process_enabled_distribute_menu(canvas)
            finally:
                imgui.end_popup()

        canvas.draw()
