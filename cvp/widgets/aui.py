# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypeVar

from imgui_bundle import imgui

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.config.sections.proxies.aui import AuiBottomProxy, AuiLeftProxy, AuiRightProxy
from cvp.imgui.begin_child import begin_child
from cvp.imgui.cursor import cursor_pos_y
from cvp.imgui.push_style_var import style_item_spacing, style_window_padding
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from cvp.widgets.splitter import Splitter

AuiSectionT = TypeVar("AuiSectionT", bound=AuiWindowConfig)


class AuiInterface(ABC):
    @abstractmethod
    def on_process_sidebar_left(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_sidebar_right(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_main(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_bottom(self) -> None:
        raise NotImplementedError


class AuiWindow(WindowBase[AuiSectionT], AuiInterface):
    def __init__(
        self,
        context: RendererContext,
        window_config: AuiSectionT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
    ):
        super().__init__(
            context=context,
            window_config=window_config,
            title=title,
            closable=closable,
            flags=flags,
            min_width=min_width,
            min_height=min_height,
            modifiable_title=modifiable_title,
        )

        self._split_left = AuiLeftProxy(window_config)
        self._split_right = AuiRightProxy(window_config)
        self._split_bottom = AuiBottomProxy(window_config)

        self._left_child_id = "ChildLeft"
        self._right_child_id = "ChildRight"
        self._center_child_id = "ChildCenter"
        self._main_child_id = "ChildMain"
        self._bottom_child_id = "ChildBottom"

        self._left_splitter = Splitter.from_vertical(
            "## VSplitterLeft",
            value_proxy=self._split_left,
            min_value=window_config.min_sidebar_left,
            max_value=window_config.max_sidebar_right,
        )
        self._right_splitter = Splitter.from_vertical(
            "## VSplitterRight",
            value_proxy=self._split_right,
            min_value=window_config.min_sidebar_right,
            max_value=window_config.max_sidebar_right,
            negative_delta=True,
        )
        self._bottom_splitter = Splitter.from_horizontal(
            "## HSplitterBottom",
            value_proxy=self._split_bottom,
            min_value=window_config.min_sidebar_bottom,
            max_value=window_config.max_sidebar_bottom,
            negative_delta=True,
        )

    @property
    def split_left(self) -> float:
        value = self.window_config.split_left
        return self._left_splitter.normalize_value(value)

    @split_left.setter
    def split_left(self, value: float) -> None:
        value = self._left_splitter.normalize_value(value)
        self.window_config.split_left = value

    @property
    def split_right(self) -> float:
        value = self.window_config.split_right
        return self._right_splitter.normalize_value(value)

    @split_right.setter
    def split_right(self, value: float) -> None:
        value = self._right_splitter.normalize_value(value)
        self.window_config.split_right = value

    @property
    def split_bottom(self) -> float:
        value = self.window_config.split_bottom
        return self._bottom_splitter.normalize_value(value)

    @split_bottom.setter
    def split_bottom(self, value: float) -> None:
        value = self._bottom_splitter.normalize_value(value)
        self.window_config.split_bottom = value

    @property
    def padding_width(self) -> float:
        return self.window_config.padding_width

    @property
    def padding_height(self) -> float:
        return self.window_config.padding_height

    @property
    def padding(self) -> Tuple[float, float]:
        return self.padding_width, self.padding_height

    @override
    def begin(self) -> Tuple[bool, bool]:
        with style_window_padding(0, 0):
            return super().begin()

    @override
    def on_process(self) -> None:
        pw = self.padding_width
        ph = self.padding_height
        top = imgui.get_cursor_pos_y()

        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + pw)
        with begin_child(f"##{self._left_child_id}", self.split_left):
            with style_item_spacing(0, 0):
                imgui.dummy(0, ph)
            self.on_process_sidebar_left()

        with style_item_spacing(pw, 0):
            imgui.same_line()

        with cursor_pos_y(top):
            self._left_splitter.do_process()

        with style_item_spacing(-1, 0):
            imgui.same_line()

        main_x: float
        main_y: float
        main_w: float
        main_h: float

        with begin_child(f"##{self._center_child_id}", -self.split_right - pw):
            with style_item_spacing(0, -1):
                with begin_child(f"##{self._main_child_id}", 0.0, -self.split_bottom):
                    main_x, main_y = imgui.get_window_position()
                    main_w, main_h = imgui.get_window_size()
                    # [IMPORTANT]
                    # When the font scale is changed, it affects other children.
                    # Therefore, the 'main_child' must be rendered last.

            with style_item_spacing(0, -1):
                self._bottom_splitter.do_process()

            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + pw)
            with begin_child(f"##{self._bottom_child_id}", -pw):
                with style_item_spacing(0, 0):
                    imgui.dummy(0, ph)
                self.on_process_bottom()

        with style_item_spacing(-1, 0):
            imgui.same_line()

        with cursor_pos_y(top):
            self._right_splitter.do_process()

        with style_item_spacing(pw, 0):
            imgui.same_line()

        with begin_child(f"##{self._right_child_id}", -pw):
            with style_item_spacing(0, 0):
                imgui.dummy(0, ph)
            self.on_process_sidebar_right()

        imgui.set_next_window_position(main_x, main_y)
        with begin_child(f"##{self._main_child_id}", main_w, main_h):
            # This is where the actual rendering of main_child occurs.
            self.on_process_main()

    @override
    def on_process_sidebar_left(self) -> None:
        pass

    @override
    def on_process_sidebar_right(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass

    @override
    def on_process_bottom(self) -> None:
        pass
