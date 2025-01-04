# -*- coding: utf-8 -*-

from typing import List, Optional
from weakref import ReferenceType, ref

import imgui

from cvp.config.sections.flow import FlowAuiConfig
from cvp.flow.datas.anchor import Anchor
from cvp.flow.datas.arc import Arc
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.node import Node
from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.selected_items import SelectedItems
from cvp.flow.datas.stroke import Stroke
from cvp.flow.datas.style import Style
from cvp.imgui.draw_list.draw_dotted_line import draw_dotted_line
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.set_window_font_scale import window_font_scale
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.types.shapes import Rect
from cvp.widgets.canvas.controller import CanvasController
from cvp.widgets.canvas.graph.mode import ControlMode


class CanvasGraph(CanvasController):
    _graph_ref: ReferenceType[Graph]
    _fonts_ref: ReferenceType[FontMapper]
    _config_ref: ReferenceType[FlowAuiConfig]

    _graph: Optional[Graph]
    _fonts: Optional[FontMapper]
    _config: Optional[FlowAuiConfig]

    _mode: ControlMode
    _connects: List[NodePin]
    _roi: Optional[Rect]
    _selected_stash: Optional[SelectedItems]

    def __init__(self, graph: Graph, fonts: FontMapper, config: FlowAuiConfig):
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

        self._mode = ControlMode.normal
        self._connects = list()
        self._roi = None
        self._selected_stash = None

    @property
    def is_multi_select_mode(self) -> bool:
        # Pressing the CTRL button switches to 'Multi-node selection mode'
        return self.ctrl_down

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
        )

    # ==================================================================================
    # Graph/Fonts Context Operations
    # ==================================================================================

    @property
    def graph(self) -> Graph:
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
    # Properties
    # ==================================================================================

    @property
    def show_node_layout(self):
        return self.config.nodes.show_layout

    @property
    def item_spacing(self):
        return self.config.nodes.item_spacing

    @property
    def icon_font(self):
        return self.fonts.get_scaled_icon(self.graph.style.icon_scale)

    @property
    def pin_font(self):
        assert self._graph is not None
        assert self._fonts is not None
        return self.fonts.get_scaled_icon(self.graph.style.pin_scale)

    @property
    def title_font(self):
        assert self._graph is not None
        assert self._fonts is not None
        return self.fonts.get_scaled_text(self.graph.style.title_scale)

    @property
    def text_font(self):
        assert self._graph is not None
        assert self._fonts is not None
        return self.fonts.get_scaled_text(self.graph.style.text_scale)

    # ==================================================================================
    # Public Operations
    # ==================================================================================

    def reset_controllers(self):
        assert self._graph is not None
        assert self._fonts is not None
        assert self._config is not None

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
        color = imgui.get_color_u32_rgba(*self.graph.color)
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
        self.graph.update_hovering_state(
            self.mouse_to_canvas_coords(),
            self.config.arcs.hovering_tolerance,
        )

        if imgui.is_key_pressed(imgui.get_key_index(imgui.KEY_DELETE)):
            self.graph.remove_selected_items()

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
                    self._connects.append(NodePin(hovering_node, hovering_pin))
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
                    self._selected_stash = self.graph.selected_items.copy()

    def _update_nodes_state_for_node_moving(self) -> None:
        assert not self.is_pan_mode
        assert self.is_node_moving_mode

        io = imgui.get_io()
        dx = io.mouse_delta.x / self.zoom
        dy = io.mouse_delta.y / self.zoom
        self.graph.move_on_selected_nodes((dx, dy))

        if self.changed_left_up:
            self._mode = ControlMode.normal

    def _update_nodes_state_for_pin_connecting(self) -> None:
        assert not self.is_pan_mode
        assert self.is_pin_connecting_mode
        assert 1 <= len(self._connects)

        connect_pairs = list()

        if hovering_np := self.graph.find_hovering_pin():
            for conn in self._connects:
                try:
                    pair = self.graph.reorder_connectable_pins(conn, hovering_np)
                    connect_pairs.append(pair)
                except ValueError:
                    connect_pairs.clear()
                    break
            hovering_np.pin.connectable = bool(connect_pairs)

        if self.changed_left_up:
            self._mode = ControlMode.normal
            self._connects.clear()
            if connect_pairs:
                for out_conn, in_conn in connect_pairs:
                    self.graph.connect_pins(out_conn, in_conn, no_reorder=True)

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

    def _update_nodes_state_for_selection_box(self) -> None:
        assert not self.is_pan_mode
        assert self.is_roi_box_mode
        assert self._roi is not None
        assert self._selected_stash is not None

        x1 = self._roi[0]
        y1 = self._roi[1]
        x2 = self.mx
        y2 = self.my
        self._roi = x1, y1, x2, y2

        x1, y1, x2, y2 = self.screen_to_canvas_roi(self._roi)
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        for node in self.graph.nodes:
            nx1, ny1, nx2, ny2 = node.node_roi
            x_in = left <= nx1 <= right or left <= nx2 <= right
            y_in = top <= ny1 <= bottom or top <= ny2 <= bottom
            if x_in and y_in:
                node.selected = node not in self._selected_stash
            else:
                node.selected = node in self._selected_stash

        if self.changed_left_up:
            self._mode = ControlMode.normal
            self._roi = None
            self._selected_stash = None
            for node in self.graph.nodes:
                self.graph.update_selected_item(node)

    # ==================================================================================
    # Color Picker
    # ==================================================================================

    def get_pin_color(self, pin: Pin, style: Style) -> RGBA:
        if self.is_pin_connecting_mode:
            if pin.hovering and pin.connectable:
                return style.select_color
            else:
                return style.normal_color
        else:
            if pin.selected:
                return style.select_color
            elif pin.hovering:
                return style.hovering_color
            else:
                return style.normal_color

    @staticmethod
    def get_arc_color(arc: Arc, style: Style) -> RGBA:
        if arc.selected:
            return style.select_color
        elif arc.hovering:
            return style.hovering_color
        else:
            return style.arc_color

    @staticmethod
    def get_anchor_color(arc: Anchor, style: Style) -> RGBA:
        if arc.selected:
            return style.select_color
        elif arc.hovering:
            return style.hovering_color
        else:
            return style.anchor_color

    @staticmethod
    def get_node_stroke(node: Node, style: Style) -> Stroke:
        if node.selected:
            return style.selected_node
        elif node.hovering:
            return style.hovering_node
        else:
            return style.normal_node

    # ==================================================================================
    # Node Operations
    # ==================================================================================

    def update_nodes_rois(self) -> None:
        for node in self.graph.nodes:
            self.update_node_roi(node)

    def update_node_roi(self, node: Node) -> None:
        with self.icon_font:
            node_emblem_w, node_emblem_h = imgui.calc_text_size(node.emblem)

        with self.title_font:
            node_name_w, node_name_h = imgui.calc_text_size(node.name)

        title_h = max(node_emblem_h, node_name_h)
        emblem_y_diff = title_h / 2 - node_emblem_h / 2
        title_y_diff = title_h / 2 - node_name_h / 2

        with self.pin_font:
            flow_n_w, flow_n_h = imgui.calc_text_size(self.config.pins.flow_n_icon)
            flow_y_w, flow_y_h = imgui.calc_text_size(self.config.pins.flow_y_icon)
            data_n_w, data_n_h = imgui.calc_text_size(self.config.pins.data_n_icon)
            data_y_w, data_y_h = imgui.calc_text_size(self.config.pins.data_y_icon)

        iw = max(flow_y_w, flow_n_w, data_y_w, data_n_w)
        ih = max(flow_y_h, flow_n_h, data_y_h, data_n_h)

        with self.text_font:
            for pin in node.pins:
                pin.icon_size = iw, ih
                pin.name_size = imgui.calc_text_size(pin.name)
            input_name_sizes = [p.name_size for p in node.input_pins]
            output_name_sizes = [p.name_size for p in node.output_pins]

        inw = max(s[0] for s in input_name_sizes)
        inh = max(s[1] for s in input_name_sizes)
        onw = max(s[0] for s in output_name_sizes)
        onh = max(s[1] for s in output_name_sizes)
        pin_name_h = max(inh, onh)

        pin_h = max(ih, inh, onh)
        pin_icon_y_diff = pin_h / 2 - ih / 2
        pin_name_y_diff = pin_h / 2 - pin_name_h / 2

        isw, ish = self.item_spacing
        center_padding = isw * 4

        wt = isw + node_emblem_w + isw + node_name_w + isw
        wf = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        wd = isw + iw + isw + inw + center_padding + onw + isw + iw + isw
        node_w = max((wt, wf, wd))

        head_h = ish + title_h + ish
        flow_h = ish + (ih + ish) * node.flow_lines
        data_h = ish + (ih + ish) * node.data_lines
        node_h = head_h + flow_h + data_h

        node.head_height = head_h
        node.flow_height = flow_h
        node.data_height = data_h

        node_emblem_x = isw
        node_emblem_y = ish + emblem_y_diff
        node.emblem_pos = node_emblem_x, node_emblem_y
        node.emblem_size = node_emblem_w, node_emblem_h

        node_name_x = node.emblem_pos[0] + node.emblem_size[0] + isw
        node_name_y = ish + title_y_diff
        node.name_pos = node_name_x, node_name_y
        node.name_size = node_name_w, node_name_h

        node.node_pos = 0.0, 0.0
        node.node_size = node_w, node_h

        for i, pin in enumerate(node.flow_inputs):
            icon_x = isw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.data_inputs):
            icon_x = isw
            icon_y = head_h + flow_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x + pin.icon_size[0] + isw
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.flow_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

        for i, pin in enumerate(node.data_outputs):
            icon_x = node_w - isw - iw
            icon_y = head_h + flow_h + ish + (ih + ish) * i
            pin.icon_pos = icon_x, icon_y + pin_icon_y_diff

            name_x = icon_x - isw - pin.name_size[0]
            name_y = icon_y + pin_name_y_diff
            pin.name_pos = name_x, name_y

    def draw_nodes(self) -> None:
        for node in reversed(self.graph.nodes):
            self.draw_node(node)

    def draw_node(self, node: Node) -> None:
        node_roi = self.canvas_to_screen_roi(node.node_roi)
        style = self.graph.style
        stroke = self.get_node_stroke(node, style)

        node_color = imgui.get_color_u32_rgba(*node.color)
        stroke_color = imgui.get_color_u32_rgba(*stroke.color)
        label_color = imgui.get_color_u32_rgba(*style.normal_color)
        layout_color = imgui.get_color_u32_rgba(*style.layout_color)
        node_bg_color = imgui.get_color_u32_rgba(*style.node_bg_color)

        thickness = stroke.thickness
        rounding = stroke.rounding
        flags = stroke.flags

        nx1, ny1, nx2, ny2 = node_roi
        zoom = self.zoom
        header_roi = nx1, ny1, nx2, ny1 + node.head_height * zoom

        self._draw_list.add_rect_filled(*node_roi, node_bg_color, rounding, flags)
        self._draw_list.add_rect_filled(*header_roi, node_color, rounding, flags)
        self._draw_list.add_rect(*node_roi, stroke_color, rounding, flags, thickness)

        with self.icon_font:
            x1 = nx1 + node.emblem_pos[0] * zoom
            y1 = ny1 + node.emblem_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.emblem)
            if self.show_node_layout:
                x2 = x1 + node.emblem_size[0] * zoom
                y2 = y1 + node.emblem_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with self.title_font:
            x1 = nx1 + node.name_pos[0] * zoom
            y1 = ny1 + node.name_pos[1] * zoom
            self._draw_list.add_text(x1, y1, label_color, node.name)
            if self.show_node_layout:
                x2 = x1 + node.name_size[0] * zoom
                y2 = y1 + node.name_size[1] * zoom
                self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with self.pin_font:
            flow_pin_n_icon = self.config.pins.flow_n_icon
            flow_pin_y_icon = self.config.pins.flow_y_icon

            for pin in node.flow_pins:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                pin_rgba = self.get_pin_color(pin, self.graph.style)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if self.show_node_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

            data_pin_n_icon = self.config.pins.data_n_icon
            data_pin_y_icon = self.config.pins.data_y_icon

            for pin in node.data_pins:
                x1 = nx1 + pin.icon_pos[0] * zoom
                y1 = ny1 + pin.icon_pos[1] * zoom
                pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                pin_rgba = self.get_pin_color(pin, self.graph.style)
                pin_color = imgui.get_color_u32_rgba(*pin_rgba)
                self._draw_list.add_text(x1, y1, pin_color, pin_icon)
                if self.show_node_layout:
                    x2 = x1 + pin.icon_size[0] * zoom
                    y2 = y1 + pin.icon_size[1] * zoom
                    self._draw_list.add_rect(x1, y1, x2, y2, layout_color)

        with self.text_font:
            for pin in node.pins:
                x1 = nx1 + pin.name_pos[0] * zoom
                y1 = ny1 + pin.name_pos[1] * zoom
                self._draw_list.add_text(x1, y1, label_color, pin.name)
                if self.show_node_layout:
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

    def draw_arc(self, arc: Arc) -> None:
        color = imgui.get_color_u32_rgba(*self.get_arc_color(arc, self.graph.style))
        thickness = self.graph.style.arc_thickness
        polyline = [self.canvas_to_screen_coords(p) for p in arc.polyline]
        self._draw_list.add_polyline(polyline, color, 0, thickness)

    def draw_bezier_cubic_anchors(self, arc: Arc) -> None:
        assert arc.is_bezier_cubic_line_type
        assert 2 <= len(arc.polyline)

        # The first/last index point is located at the connected pin.
        sx, sy = self.canvas_to_screen_coords(arc.polyline[0])
        ex, ey = self.canvas_to_screen_coords(arc.polyline[-1])

        radius = self.graph.style.anchor_radius
        start, end = arc.get_bezier_cubic_anchors()

        start_rgba = self.get_anchor_color(arc.start_anchor, self.graph.style)
        start_color = imgui.get_color_u32_rgba(*start_rgba)
        sax, say = self.canvas_to_screen_coords(start)
        draw_dotted_line(self._draw_list, sx, sy, sax, say, start_color)
        self._draw_list.add_circle_filled(sax, say, radius, start_color)

        end_rgba = self.get_anchor_color(arc.end_anchor, self.graph.style)
        end_color = imgui.get_color_u32_rgba(*end_rgba)
        eax, eay = self.canvas_to_screen_coords(end)
        draw_dotted_line(self._draw_list, ex, ey, eax, eay, end_color)
        self._draw_list.add_circle_filled(eax, eay, radius, end_color)

    # ==================================================================================
    # Pin Operations
    # ==================================================================================

    def draw_pin_connect(self, connect: NodePin) -> None:
        node = connect.node
        pin = connect.pin

        node_roi = self.canvas_to_screen_roi(node.node_roi)
        nx = node_roi[0]
        ny = node_roi[1]
        zoom = self.zoom
        x1 = nx + pin.icon_pos[0] * zoom + pin.icon_size[0] * zoom / 2.0
        y1 = ny + pin.icon_pos[1] * zoom + pin.icon_size[1] * zoom / 2.0
        mx, my = self._mouse_pos

        color = imgui.get_color_u32_rgba(*self.graph.style.pin_connection_color)
        thickness = self.graph.style.pin_connection_thickness
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
        color = imgui.get_color_u32_rgba(*self.graph.style.selection_box_color)
        thickness = self.graph.style.selection_box_thickness
        self._draw_list.add_rect_filled(x1, y1, x2, y2, color)
        self._draw_list.add_rect(x1, y1, x2, y2, color, 0.0, 0, thickness)
