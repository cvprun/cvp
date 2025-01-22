# -*- coding: utf-8 -*-

from typing import Callable, Final, Optional, Sequence, Tuple

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.proxies.flow import SplitTreeProxy
from cvp.context.context import Context
from cvp.fonts.glyphs.mdi import (
    BUG,
    DEBUG_STEP_INTO,
    DEBUG_STEP_OUT,
    DEBUG_STEP_OVER,
    PAUSE,
    PLAY,
    STOP,
)
from cvp.imgui.begin_child import begin_child
from cvp.imgui.drag_types import DRAG_FLOW_NODE
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.push_style_var import style_item_spacing
from cvp.imgui.text_centered import text_centered
from cvp.logging.logging import flow_logger as logger
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.aui import AuiWindow
from cvp.widgets.canvas.graph import CanvasGraph
from cvp.widgets.splitter import Splitter
from cvp.windows.flow.bottom import FlowBottomTabs
from cvp.windows.flow.canvases import Canvases
from cvp.windows.flow.catalog import Catalog
from cvp.windows.flow.left import FlowLeftTabs
from cvp.windows.flow.right import FlowRightTabs

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE
_CANVAS_FLAGS: Final[int] = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE


class FlowWindow(AuiWindow[FlowAuiConfig]):
    _menus: Sequence[Tuple[str, Callable[[], None]]]

    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            window_config=context.config.flow_aui,
            title="Flow",
            closable=True,
            flags=imgui.WINDOW_MENU_BAR,
            min_width=MIN_WINDOW_WIDTH,
            min_height=MIN_WINDOW_HEIGHT,
            modifiable_title=False,
        )

        self._fonts = fonts
        self._canvases = Canvases(fonts, context.config.flow_aui)
        self._catalog = Catalog(context, fonts)
        self._left_tabs = FlowLeftTabs(context, fonts)
        self._right_tabs = FlowRightTabs(context, fonts)
        self._bottom_tabs = FlowBottomTabs(context, fonts)

        self._split_tree = SplitTreeProxy(context.config.flow_aui)
        self._tree_splitter = Splitter.from_horizontal(
            "##HSplitterTree",
            value_proxy=self._split_tree,
            min_value=context.config.flow_aui.min_split_tree,
            negative_delta=True,
        )

        self._menus = (
            ("File", self.on_file_menu),
            ("Edit", self.on_edit_menu),
            ("Layout", self.on_layout_menu),
            ("Run", self.on_run_menu),
            ("View", self.on_view_menu),
        )

        self._new_graph_popup = InputTextPopup(
            title="New graph",
            label="Please enter a graph name:",
            ok="Create",
            cancel="Cancel",
            target=self.on_new_graph_popup,
        )
        self._open_graph_popup = OpenFilePopup(
            title="Open graph file",
            target=self.on_open_file_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove graph?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._new_graph_popup)
        self.register_popup(self._open_graph_popup)
        self.register_popup(self._confirm_remove)

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
        filepath = self.context.home.flows.graph_filepath(graph.uuid)
        if filepath.exists():
            raise FileExistsError(f"Graph file already exists: '{str(filepath)}'")
        self.context.fm.write_graph_yaml(filepath, graph)
        self._canvases.open(graph)

    def on_open_file_popup(self, file: str) -> None:
        pass

    def on_confirm_remove(self, value: bool) -> None:
        pass

    @override
    def on_process(self) -> None:
        self.on_menu()
        super().on_process()

    def _process_edit_menu(
        self,
        canvas: Optional[CanvasGraph] = None,
    ) -> None:
        if canvas is not None and canvas.opened:
            opened = True
            undoable = canvas.history.undoable
            redoable = canvas.history.redoable
            selected_any = bool(canvas.graph.selection)
            has_clipboard = self.context.fm.has_clipboard
        else:
            opened = False
            undoable = False
            redoable = False
            selected_any = False
            has_clipboard = False

        if menu_item("Undo", shortcut="Ctrl+Z", enabled=undoable):
            assert canvas is not None
            canvas.undo_history()
        if menu_item("Redo", shortcut="Ctrl+Y", enabled=redoable):
            assert canvas is not None
            canvas.redo_history()

        imgui.separator()
        if menu_item("Cut", shortcut="Ctrl+X", enabled=selected_any):
            assert canvas is not None
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            self.context.fm.clipboard_pivot = canvas.graph.selection.group_pos
            canvas.graph.remove_selected_items()
            canvas.save_history("Cut selected items")
        if menu_item("Copy", shortcut="Ctrl+C", enabled=selected_any):
            assert canvas is not None
            self.context.fm.clipboard_items = canvas.graph.selection.deepcopy()
            px, py = canvas.graph.selection.group_pos
            px += self.window_config.paste_margin
            py += self.window_config.paste_margin
            self.context.fm.clipboard_pivot = px, py
        if menu_item("Paste", shortcut="Ctrl+V", enabled=has_clipboard):
            assert canvas is not None
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
            assert canvas is not None
            canvas.graph.remove_selected_items()
            canvas.save_history("Remove selected items")

        imgui.separator()
        if menu_item("Reset control", enabled=opened):
            assert canvas is not None
            canvas.reset_controllers()

        imgui.separator()
        if menu_item("Select all", enabled=opened):
            assert canvas is not None
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_items()
        if menu_item("Select nodes", enabled=opened):
            assert canvas is not None
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_nodes()
        if menu_item("Select arcs", enabled=opened):
            assert canvas is not None
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_arcs()
        if menu_item("Select pins", enabled=opened):
            assert canvas is not None
            canvas.graph.unselect_all_items()
            canvas.graph.select_all_pins()

    @staticmethod
    def _process_layout_menu(canvas: Optional[CanvasGraph] = None) -> None:
        if canvas is not None and canvas.opened:
            selected_items = canvas.graph.selection
            selected_any = bool(selected_items)
            single_item = 1 == len(selected_items)
        else:
            selected_items = list()
            selected_any = False
            single_item = False

        if menu_item("To Front", enabled=selected_any):
            assert canvas is not None
            canvas.graph.items_to_front(list(selected_items.values()))
            canvas.save_history("To front items")
        if menu_item("To Back", enabled=selected_any):
            assert canvas is not None
            canvas.graph.items_to_back(list(selected_items.values()))
            canvas.save_history("To back items")

        if menu_item("Bring Forward", enabled=single_item):
            assert canvas is not None
            assert 1 == len(selected_items)
            canvas.graph.item_bring_forward(selected_items.first)
            canvas.save_history("Bring forward items")
        if menu_item("Send Backward", enabled=single_item):
            assert canvas is not None
            assert 1 == len(selected_items)
            canvas.graph.item_send_backward(selected_items.first)
            canvas.save_history("Send backward items")

    @staticmethod
    def _process_align_menu(canvas: Optional[CanvasGraph] = None) -> None:
        if canvas is not None and canvas.opened:
            nodes = canvas.graph.selection.nodes
            multiple_item = 2 <= len(nodes)
        else:
            nodes = list()
            multiple_item = False

        if imgui.begin_menu("Align", enabled=multiple_item).opened:
            assert canvas is not None
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
    def _process_distribute_menu(canvas: Optional[CanvasGraph] = None) -> None:
        if canvas is not None and canvas.opened:
            nodes = canvas.graph.selection.nodes
            multiple_item = 2 <= len(nodes)
        else:
            nodes = list()
            multiple_item = False

        if imgui.begin_menu("Distribute", enabled=multiple_item).opened:
            assert canvas is not None
            if menu_item("Horizontal"):
                canvas.graph.nodes_distribute_horizontal(nodes)
                canvas.save_history("Distribute horizontal nodes")
            if menu_item("Vertical"):
                canvas.graph.nodes_distribute_vertical(nodes)
                canvas.save_history("Distribute vertical nodes")
            imgui.end_menu()

    @staticmethod
    def _process_run_menu(
        fonts: FontMapper,
        canvas: Optional[CanvasGraph] = None,
    ) -> None:
        if canvas is not None and canvas.opened:
            opened = True
        else:
            opened = False

        if fonts.normal_icon:
            if menu_item(f"{PLAY} Run", enabled=opened):
                pass
            if menu_item(f"{BUG} Debug", enabled=opened):
                pass
            if menu_item(f"{PAUSE} Pause", enabled=opened):
                pass
            if menu_item(f"{STOP} Stop", enabled=opened):
                pass
            if menu_item(f"{DEBUG_STEP_OVER} Step Over", enabled=opened):
                pass
            if menu_item(f"{DEBUG_STEP_INTO} Step Into", enabled=opened):
                pass
            if menu_item(f"{DEBUG_STEP_OUT} Step Out", enabled=opened):
                pass

    def on_menu(self) -> None:
        with imgui.begin_menu_bar() as menu_bar:
            if not menu_bar.opened:
                return

            for name, func in self._menus:
                with imgui.begin_menu(name) as menu:
                    if menu.opened:
                        func()

    def on_file_menu(self) -> None:
        if menu_item("New graph"):
            self.show_new_graph_popup()

        imgui.separator()
        has_opened_graph = self._canvases.opened
        if menu_item("Save graph", enabled=has_opened_graph):
            self.save_current_graph()
        if menu_item("Save and close graph", enabled=has_opened_graph):
            self.save_current_graph()
            self.close_current_graph()
        if menu_item("Close graph", enabled=has_opened_graph):
            self.close_current_graph()

        # imgui.separator()
        # if menu_item("Import graph"):
        #     self._open_graph_popup.show()
        # if menu_item("Export graph"):
        #     self._open_graph_popup.show()

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
                self._process_edit_menu(canvas)
        else:
            self._process_edit_menu()

    def on_layout_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                self._process_layout_menu(canvas)
                imgui.separator()
                self._process_align_menu(canvas)
                self._process_distribute_menu(canvas)
        else:
            self._process_layout_menu()
            imgui.separator()
            self._process_align_menu()
            self._process_distribute_menu()

    def on_run_menu(self) -> None:
        if canvas := self._canvases.canvas:
            with canvas:
                self._process_run_menu(self._fonts, canvas)
        else:
            self._process_run_menu(self._fonts)

    def on_view_menu(self) -> None:
        if autoscroll := menu_item("Autoscroll logs", selected=self.autoscroll):
            self.autoscroll = autoscroll.state

        imgui.separator()
        if show_layout := menu_item("Show Layout", selected=self.show_layout):
            self.show_layout = show_layout.state

    def show_new_graph_popup(self) -> None:
        self._new_graph_popup.show()

    def save_current_graph(self) -> None:
        graph = self._canvases.graph
        if graph is None:
            return

        try:
            self.context.save_graph(graph)
            logger.info(f"The flow graph was successfully saved: '{graph.uuid}'")
        except BaseException as e:
            logger.error(f"Failed to save the flow graph: '{graph.uuid}' -> '{e}'")

    def close_current_graph(self):
        graph = self._canvases.graph
        if graph is None:
            return

        self._canvases.close()
        logger.info(f"Close the flow graph: '{graph.uuid}'")

    def refresh_graphs(self) -> None:
        graph_uuid_stash = str()

        if graph := self._canvases.graph:
            graph_uuid_stash = graph.uuid

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
        with begin_child("## ChildLeftTop", 0, -self.split_tree):
            self._left_tabs.do_process(self._canvases)

        with style_item_spacing(0, -1):
            self._tree_splitter.do_process()

        with begin_child("## ChildLeftBottom"):
            with style_item_spacing(0, 0):
                imgui.dummy(0, self.padding_height)
            self._catalog.on_process()

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
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        try:
            return begin_child("##Canvas", border=True, flags=_CANVAS_FLAGS)
        finally:
            imgui.pop_style_color()
            imgui.pop_style_var()

    def on_canvas_events(self, canvas: CanvasGraph) -> None:
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

    def on_canvas(self, canvas: CanvasGraph) -> None:
        assert canvas.opened
        canvas.do_process_canvas()

        with imgui.begin_drag_drop_target() as target:
            if target.hovered:
                if payload := imgui.accept_drag_drop_payload(DRAG_FLOW_NODE):
                    node_path = str(payload, encoding="utf-8")
                    node = self.context.fm.add_node(canvas.graph, node_path)
                    canvas.update_node_roi(node)
                    canvas.save_history("Add a new node", node_path)

        if imgui.begin_popup_context_window().opened:
            try:
                self._process_edit_menu(canvas)
                imgui.separator()
                self._process_layout_menu(canvas)
                imgui.separator()
                self._process_align_menu(canvas)
                self._process_distribute_menu(canvas)
            finally:
                imgui.end_popup()

        canvas.draw()
