# -*- coding: utf-8 -*-

from typing import List, Optional
from weakref import ReferenceType, ref

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.flow.anchor import FlowAnchor
from cvp.flow.arc import FlowArc
from cvp.flow.connection import FlowConnection
from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelection
from cvp.imgui.draw_list.draw_dotted_line import draw_dotted_line
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.logging.logging import flow_logger as logger
from cvp.maths.geometry.rectangle import is_rectangle_collision
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.types.shapes import Rect
from cvp.widgets.canvas.controller import CanvasController
from cvp.widgets.canvas.graph.history import History
from cvp.widgets.canvas.graph.mode import ControlMode


class CanvasGraph(CanvasController):
    _graph_ref: ReferenceType[FlowGraph]
    _fonts_ref: ReferenceType[FontMapper]
    _config_ref: ReferenceType[FlowAuiConfig]

    _graph: Optional[FlowGraph]
    _fonts: Optional[FontMapper]
    _config: Optional[FlowAuiConfig]

    _mode: ControlMode
    _connects: List[FlowNodePin]
    _roi: Optional[Rect]
    _selection_stash: Optional[FlowSelection]

    def __init__(self, graph: FlowGraph, fonts: FontMapper, config: FlowAuiConfig):
        super().__init__()

        self._pan_x.update(graph.control.pan_x, no_emit=True)
        self._pan_y.update(graph.control.pan_y, no_emit=True)
        self._zoom.update(graph.control.zoom, no_emit=True)

        self._graph_ref = ref(graph)
        self._fonts_ref = ref(fonts)
        self._config_ref = ref(config)

        self._graph = None
        self._fonts = None
        self._config = None

        graph.clear_state()
        graph.update_arcs_io()
        graph.update_arcs_polyline()

        self._history = History(max_history=config.max_history)
        self._history.save_history("Initialize graph", graph)

        self._mode = ControlMode.normal
        self._connects = list()
        self._roi = None
        self._selection_stash = None

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
        return self._mode == ControlMode.normal

    @property
    def is_node_moving_mode(self) -> bool:
        return self._mode == ControlMode.node_moving

    @property
    def is_pin_connecting_mode(self) -> bool:
        return self._mode == ControlMode.pin_connecting

    @property
    def is_anchor_moving_mode(self) -> bool:
        return self._mode == ControlMode.anchor_moving

    @property
    def is_roi_box_mode(self) -> bool:
        return self._mode == ControlMode.roi_box

    @override
    def as_unformatted_text(self) -> str:
        return super().as_unformatted_text() + (
            f"Mode: {self._mode.name}\n"
            f"Connects: {self._connects}\n"
            f"ROI: {self._roi}\n"
            f"History: {len(self._history)}\n"
            f"Cursor: {self._history.cursor_index}\n"
        )

    # ==================================================================================
    # Graph/Fonts Context Operations
    # ==================================================================================

    @property
    def graph(self) -> FlowGraph:
        if self._graph is None:
            raise ReferenceError("The graph instance has expired")
        return self._graph

    @property
    def fonts(self) -> FontMapper:
        if self._fonts is None:
            raise ReferenceError("The fonts instance has expired")
        return self._fonts

    @property
    def config(self) -> FlowAuiConfig:
        if self._config is None:
            raise ReferenceError("The fonts instance has expired")
        return self._config

    @property
    def opened(self) -> bool:
        if self._graph is not None:
            assert self._fonts is not None
            assert self._config is not None
            return True
        else:
            assert self._fonts is None
            assert self._config is None
            return False

    def _clear_refs(self) -> None:
        self._graph = None
        self._fonts = None
        self._config = None

    def open(self) -> None:
        if self._graph is not None:
            raise ValueError("Graph already open")
        if self._fonts is not None:
            raise ValueError("Fonts already open")
        if self._config is not None:
            raise ValueError("Config already open")

        assert self._graph is None
        assert self._fonts is None
        assert self._config is None
        self._graph = self._graph_ref()
        self._fonts = self._fonts_ref()
        self._config = self._config_ref()

        if self._graph is None:
            self._clear_refs()
            raise ReferenceError("The graph instance has expired")

        if self._fonts is None:
            self._clear_refs()
            raise ReferenceError("The fonts instance has expired")

        if self._config is None:
            self._clear_refs()
            raise ReferenceError("The config instance has expired")

        assert self._graph is not None
        assert self._fonts is not None
        assert self._config is not None

    def close(self) -> None:
        if self._graph is None:
            raise ValueError("Graph instance has expired")
        if self._fonts is None:
            raise ValueError("Fonts instance has expired")
        if self._config is None:
            raise ValueError("Config instance has expired")

        self._clear_refs()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ==================================================================================
    # History Operations
    # ==================================================================================

    @property
    def history(self):
        return self._history

    def clear_history(self) -> None:
        logger.info("Clear history")
        self._history.clear_history()

    def save_history(
        self,
        title: str,
        details: Optional[str] = None,
        *,
        no_logging=False,
    ) -> None:
        if not no_logging:
            logger.info(title)
            if details:
                logger.debug(details)

        self._history.save_history(
            title=title,
            graph=self.graph,
            details=details,
            max_history=self.config.max_history,
        )

    def load_history(self, index: int, *, no_logging=False) -> None:
        if not no_logging:
            logger.info(f"Load history: {index}")
        self.graph.restore(self._history.load_history(index))

    def undo_history(self, *, no_logging=False) -> None:
        if not self._history.undoable:
            raise ValueError("History is not undoable")
        if not no_logging:
            logger.info("Undo history")
        self.load_history(self._history.cursor_index - 1, no_logging=True)

    def redo_history(self, *, no_logging=False) -> None:
        if not self._history.redoable:
            raise ValueError("History is not redoable")
        if not no_logging:
            logger.info("Redo history")
        self.load_history(self._history.cursor_index + 1, no_logging=True)

    # ==================================================================================
    # Public Operations
    # ==================================================================================

    def reset_controllers(self):
        assert self._graph is not None
        assert self._fonts is not None
        assert self._config is not None

        logger.info("Reset controllers")

        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0

        self.graph.control.pan_x = 0.0
        self.graph.control.pan_y = 0.0
        self.graph.control.zoom = 1.0

    def do_process_controllers(self, debugging=False) -> None:
        assert self._graph is not None
        assert self._fonts is not None
        assert self._config is not None

        if result := self.render_controllers(debugging=debugging):
            self.graph.control.pan_x = result.pan_x
            self.graph.control.pan_y = result.pan_y
            self.graph.control.zoom = result.zoom

    def do_process_canvas(self) -> None:
        assert self._graph is not None
        assert self._fonts is not None
        assert self._config is not None

        if result := self.update_state():
            self.graph.control.pan_x = result.pan_x
            self.graph.control.pan_y = result.pan_y
            self.graph.control.zoom = result.zoom

        self.update_nodes_state()
        self.graph.update_arcs_io()
        self.graph.update_arcs_polyline()

    # ==================================================================================
    # Draw Operations
    # ==================================================================================

    def draw(self) -> None:
        with window_font_scale(self.zoom):
            self.fill()
            self.draw_grid_x()
            self.draw_grid_y()
            self.draw_axis_x()
            self.draw_axis_y()

            self.draw_arcs()
            self.draw_nodes()

            self.draw_pin_connects()
            self.draw_roi_box()

    def fill(self) -> None:
        color = imgui.get_color_u32_rgba(*self.config.background_color)
        self._draw_list.add_rect_filled(*self.canvas_roi, color)

    def draw_grid_x(self) -> None:
        grid_x = self.config.grid_x
        if not grid_x.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_x.color)
        for line in self.vertical_grid_lines(grid_x.step):
            self._draw_list.add_line(*line, color, grid_x.thickness)

    def draw_grid_y(self) -> None:
        grid_y = self.config.grid_y
        if not grid_y.visible:
            return

        color = imgui.get_color_u32_rgba(*grid_y.color)
        for line in self.horizontal_grid_lines(grid_y.step):
            self._draw_list.add_line(*line, color, grid_y.thickness)

    def draw_axis_x(self) -> None:
        axis_x = self.config.axis_x
        if not axis_x.visible:
            return

        origin_y = self.local_origin_to_screen_coords()[1]
        color = imgui.get_color_u32_rgba(*axis_x.color)

        x1 = self.cx
        y1 = origin_y
        x2 = self.cx + self.cw
        y2 = origin_y
        self._draw_list.add_line(x1, y1, x2, y2, color, axis_x.thickness)

    def draw_axis_y(self) -> None:
        axis_y = self.config.axis_y
        if not axis_y.visible:
            return

        origin_x = self.local_origin_to_screen_coords()[0]
        color = imgui.get_color_u32_rgba(*axis_y.color)

        x1 = origin_x
        y1 = self.cy
        x2 = origin_x
        y2 = self.cy + self.ch
        self._draw_list.add_line(x1, y1, x2, y2, color, axis_y.thickness)

    # ==================================================================================
    # Update state
    # ==================================================================================

    def update_nodes_state(self) -> None:
        self.graph.clear_state()
        self.graph.update_hovering_state(self.mouse_to_canvas_coords())

        if self.is_pan_mode:
            # Nodes cannot be selected or dragged during 'Canvas Pan Mode'.
            return

        match self._mode:
            case ControlMode.normal:
                self._update_nodes_state_for_normal()
            case ControlMode.node_moving:
                self._update_nodes_state_for_node_moving()
            case ControlMode.pin_connecting:
                self._update_nodes_state_for_pin_connecting()
            case ControlMode.anchor_moving:
                self._update_nodes_state_for_anchor_moving()
            case ControlMode.roi_box:
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
                    self._mode = ControlMode.pin_connecting
                    self._connects.clear()
                    self._connects.append(FlowNodePin(hovering_node, hovering_pin))
                else:
                    self._mode = ControlMode.node_moving
                    if not hovering_node.selected:
                        if not self.is_multi_select_mode:
                            self.graph.unselect_all_items()
                        self.graph.select_item(hovering_node)
            else:
                if hovering_anchor := self.graph.find_hovering_anchor():
                    hovering_anchor.selected = True
                    self._mode = ControlMode.anchor_moving
                else:
                    self._mode = ControlMode.roi_box
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
            self._mode = ControlMode.normal
            self.save_history("The nodes has been moved")

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
            self._mode = ControlMode.normal
            self._connects.clear()
            if connect_pairs:
                for out_conn, in_conn in connect_pairs:
                    self.graph.connect_pins(out_conn, in_conn, no_reorder=True)
                self.save_history("The pins has been connected")

    def _update_nodes_state_for_anchor_moving(self) -> None:
        assert not self.is_pan_mode
        assert self.is_anchor_moving_mode

        io = imgui.get_io()
        dx = io.mouse_delta.x / self.zoom
        dy = io.mouse_delta.y / self.zoom
        self.graph.move_on_selected_anchor((dx, dy))

        if self.changed_left_up:
            self._mode = ControlMode.normal
            selected_arc = self.graph.selected_arc_only
            assert selected_arc is not None
            selected_arc.start_anchor.selected = False
            selected_arc.end_anchor.selected = False
            self.save_history("The anchor has been moved")

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
            self._mode = ControlMode.normal
            self._roi = None
            self._selection_stash = None
            for node in self.graph.nodes:
                self.graph.update_selected_item(node)

    # ==================================================================================
    # Style properties
    # ==================================================================================

    @property
    def node_show_layout(self):
        return self.config.nodes.show_layout

    @property
    def node_item_spacing(self):
        return self.config.nodes.item_spacing

    @staticmethod
    def get_node_color_u32(node: FlowNode) -> int:
        return imgui.get_color_u32_rgba(*node.color)

    def get_node_line_color(self, node: FlowNode) -> RGBA:
        if node.selected:
            return self.config.nodes.selected_color
        elif node.hovering:
            return self.config.nodes.hovering_color
        else:
            return self.config.nodes.normal_color

    def get_node_line_color_u32(self, node: FlowNode) -> int:
        return imgui.get_color_u32_rgba(*self.get_node_line_color(node))

    @property
    def node_label_color_u32(self) -> int:
        return imgui.get_color_u32_rgba(*self.config.nodes.label_color)

    @property
    def node_layout_color_u32(self) -> int:
        return imgui.get_color_u32_rgba(*self.config.nodes.layout_color)

    @property
    def node_background_color_u32(self) -> int:
        return imgui.get_color_u32_rgba(*self.config.nodes.background_color)

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

    @property
    def title_font(self):
        return self.fonts.get_scaled_text(self.config.nodes.title_size)

    @property
    def text_font(self):
        return self.fonts.get_scaled_text(self.config.nodes.text_size)

    @property
    def icon_font(self):
        return self.fonts.get_scaled_icon(self.config.nodes.icon_size)

    @property
    def pin_font(self):
        return self.fonts.get_scaled_icon(self.config.pins.icon_size)

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

    def get_arc_color(self, arc: FlowArc) -> RGBA:
        if arc.selected:
            return self.config.arcs.selected_color
        elif arc.hovering:
            return self.config.arcs.hovering_color
        else:
            return self.config.arcs.normal_color

    def get_arc_color_u32(self, arc: FlowArc) -> int:
        return imgui.get_color_u32_rgba(*self.get_arc_color(arc))

    def get_arc_thickness(self, arc: FlowArc) -> float:
        if arc.selected:
            return self.config.arcs.selected_thickness
        elif arc.hovering:
            return self.config.arcs.hovering_thickness
        else:
            return self.config.arcs.normal_thickness

    def get_anchor_color(self, anchor: FlowAnchor) -> RGBA:
        if anchor.selected:
            return self.config.anchors.selected_color
        elif anchor.hovering:
            return self.config.anchors.hovering_color
        else:
            return self.config.anchors.normal_color

    def get_anchor_color_u32(self, anchor: FlowAnchor) -> int:
        return imgui.get_color_u32_rgba(*self.get_anchor_color(anchor))

    # ==================================================================================
    # Node Operations
    # ==================================================================================

    def update_nodes_rois(self) -> None:
        for node in self.graph.nodes:
            self.update_node_roi(node)

    def update_node_roi(self, node: FlowNode) -> None:
        with self.icon_font:
            node_icon_w, node_icon_h = imgui.calc_text_size(node.icon)

        with self.title_font:
            node_name_w, node_name_h = imgui.calc_text_size(node.name)

        title_h = max(node_icon_h, node_name_h)
        icon_y_diff = title_h / 2 - node_icon_h / 2
        title_y_diff = title_h / 2 - node_name_h / 2

        with self.pin_font:
            flow_n_w, flow_n_h = imgui.calc_text_size(self.config.pins.flow_n_icon)
            flow_y_w, flow_y_h = imgui.calc_text_size(self.config.pins.flow_y_icon)
            data_n_w, data_n_h = imgui.calc_text_size(self.config.pins.data_n_icon)
            data_y_w, data_y_h = imgui.calc_text_size(self.config.pins.data_y_icon)

        iw = max(flow_y_w, flow_n_w, data_y_w, data_n_w)
        ih = max(flow_y_h, flow_n_h, data_y_h, data_n_h)

        visible_flow_inputs = [p for p in node.flow_inputs if not p.hidden]
        visible_flow_outputs = [p for p in node.flow_outputs if not p.hidden]
        visible_data_inputs = [p for p in node.data_inputs if not p.hidden]
        visible_data_outputs = [p for p in node.data_outputs if not p.hidden]

        visible_inputs = visible_flow_inputs + visible_data_inputs
        visible_outputs = visible_flow_outputs + visible_data_outputs

        with self.text_font:
            for pin in node.pins:
                pin.icon_size = iw, ih
                pin.name_size = imgui.calc_text_size(pin.name)
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

        flow_line_count = max(len(visible_flow_inputs), len(visible_flow_outputs))
        data_line_count = max(len(visible_data_inputs), len(visible_data_outputs))

        head_h = ish + title_h + ish
        flow_h = ish + (ih + ish) * flow_line_count
        data_h = ish + (ih + ish) * data_line_count
        node_h = head_h + flow_h + data_h

        node.head_height = head_h
        node.flow_height = flow_h
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

        for i, pin in enumerate(visible_flow_inputs):
            icon_x = isw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_data_inputs):
            icon_x = isw
            icon_y = head_h + flow_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_flow_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(visible_data_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + flow_h + ish + (ih + ish) * i
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
        zoom = self.zoom
        header_roi = nx1, ny1, nx2, ny1 + node.head_height * zoom

        self._draw_list.add_rect_filled(*node_roi, background_color, rounding)
        self._draw_list.add_rect_filled(*header_roi, node_color, rounding)
        self._draw_list.add_rect(*node_roi, line_color, rounding, 0, thickness)

        with self.icon_font:
            x1 = nx1 + node.icon_pos[0] * zoom
            y1 = ny1 + node.icon_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.icon)
            if self.node_show_layout:
                x2 = x1 + node.icon_size[0] * zoom
                y2 = y1 + node.icon_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with self.title_font:
            x1 = nx1 + node.name_pos[0] * zoom
            y1 = ny1 + node.name_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.name)
            if self.node_show_layout:
                x2 = x1 + node.name_size[0] * zoom
                y2 = y1 + node.name_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        visible_flow_inputs = [p for p in node.flow_inputs if not p.hidden]
        visible_flow_outputs = [p for p in node.flow_outputs if not p.hidden]
        visible_data_inputs = [p for p in node.data_inputs if not p.hidden]
        visible_data_outputs = [p for p in node.data_outputs if not p.hidden]

        visible_flows = visible_flow_inputs + visible_flow_outputs
        visible_datas = visible_data_inputs + visible_data_outputs

        visible_pins = visible_flows + visible_datas

        # visible_inputs = visible_flow_inputs + visible_data_inputs
        # visible_outputs = visible_flow_outputs + visible_data_outputs

        with self.pin_font:
            flow_pin_n_icon = self.config.pins.flow_n_icon
            flow_pin_y_icon = self.config.pins.flow_y_icon

            for pin in visible_flows:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                pin_rgba = self.get_pin_color(pin)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if self.node_show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

            data_pin_n_icon = self.config.pins.data_n_icon
            data_pin_y_icon = self.config.pins.data_y_icon

            for pin in visible_datas:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                pin_rgba = self.get_pin_color(pin)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if self.node_show_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with self.text_font:
            for pin in visible_pins:
                x1 = nx1 + pin.name_pos[0] * zoom
                y1 = ny1 + pin.name_pos[1] * zoom
                self._draw_list.add_text(x1, y1, label_color, pin.name)
                if self.node_show_layout:
                    x2 = x1 + pin.name_size[0] * zoom
                    y2 = y1 + pin.name_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

    # ==================================================================================
    # Arc Operations
    # ==================================================================================

    def draw_arcs(self) -> None:
        for arc in self.graph.arcs:
            assert arc.output is not None
            assert arc.input is not None
            self.draw_arc(arc)

        if selected_arc := self.graph.selected_arc_only:
            if selected_arc.selected and selected_arc.is_bezier_cubic_line_type:
                self.draw_bezier_cubic_anchors(selected_arc)

    def draw_arc(self, arc: FlowArc) -> None:
        color = self.get_arc_color_u32(arc)
        thickness = self.get_arc_thickness(arc)
        polyline = [self.canvas_to_screen_coords(p) for p in arc.polyline]
        self._draw_list.add_polyline(polyline, color, 0, thickness)

    def draw_bezier_cubic_anchors(self, arc: FlowArc) -> None:
        assert arc.is_bezier_cubic_line_type
        assert 2 <= len(arc.polyline)

        # The first/last index point is located at the connected pin.
        sx, sy = self.canvas_to_screen_coords(arc.polyline[0])
        ex, ey = self.canvas_to_screen_coords(arc.polyline[-1])

        radius = self.anchor_radius
        start, end = arc.get_bezier_cubic_anchors()

        start_color = self.get_anchor_color_u32(arc.start_anchor)
        sax, say = self.canvas_to_screen_coords(start)
        draw_dotted_line(self._draw_list, sx, sy, sax, say, start_color)
        self._draw_list.add_circle_filled(sax, say, radius, start_color)

        end_color = self.get_anchor_color_u32(arc.end_anchor)
        eax, eay = self.canvas_to_screen_coords(end)
        draw_dotted_line(self._draw_list, ex, ey, eax, eay, end_color)
        self._draw_list.add_circle_filled(eax, eay, radius, end_color)

    # ==================================================================================
    # Pin Operations
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

        color = imgui.get_color_u32_rgba(*self.config.pins.connection_color)
        thickness = self.config.pins.connection_thickness
        self._draw_list.add_line(x1, y1, mx, my, color, thickness)

    def draw_pin_connects(self) -> None:
        if not self.is_pin_connecting_mode:
            return

        for connect in self._connects:
            self.draw_pin_connect(connect)

    # ==================================================================================
    # ROI Operations
    # ==================================================================================

    def draw_roi_box(self) -> None:
        if not self.is_roi_box_mode:
            return

        assert self._roi is not None
        x1, y1, x2, y2 = self._roi
        color = imgui.get_color_u32_rgba(*self.config.roi.color)
        rounding = self.config.roi.rounding
        thickness = self.config.roi.thickness
        self._draw_list.add_rect_filled(x1, y1, x2, y2, color)
        self._draw_list.add_rect(x1, y1, x2, y2, color, rounding, 0, thickness)
