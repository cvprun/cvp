# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.begin_tab_item import begin_tab_item, end_tab_item
from cvp.imgui.flags.tab_bar import TabBarFlags
from cvp.imgui.flags.tab_item import TabItemFlags
from cvp.inspect.bind import force_bind


@dataclass
class TabItem:
    name: str
    callback: Optional[Callable] = None
    opened: Optional[bool] = None
    flags: Union[TabItemFlags, int] = 0


TabItemLike = Union[
    TabItem,
    str,
    Tuple[str],
    Tuple[str, Callable],
    Tuple[str, Callable, bool],
]


def normalize_tab_items(*items: TabItemLike) -> List[TabItem]:
    result = list()

    for item in items:
        if isinstance(item, TabItem):
            result.append(item)
        elif isinstance(item, str):
            result.append(TabItem(item))
        elif isinstance(item, (tuple, list)):
            name = str(item[0]) if 1 <= len(item) else str()
            callback = item[1] if 2 <= len(item) else None
            opened = item[2] if 3 <= len(item) else None
            result.append(TabItem(name, callback, opened))
        else:
            raise ValueError(f"Invalid tab item type: '{type(item).__name__}'")

    return result


class TabList(List[TabItem]):
    def __init__(self, *items: TabItemLike):
        super().__init__(normalize_tab_items(*items))

    @classmethod
    def from_iterable(cls, items: Iterable[TabItemLike]):
        return cls(*items)

    def do_process(
        self,
        label: str,
        *args,
        flags: Union[TabBarFlags, int] = 0,
        **kwargs,
    ) -> None:
        if isinstance(flags, TabBarFlags):
            flags = int(flags)
        assert isinstance(flags, int)

        if imgui.begin_tab_bar(label, flags):
            try:
                for tab in self:
                    item_flags = tab.flags
                    if isinstance(item_flags, TabItemFlags):
                        item_flags = int(item_flags)
                    assert isinstance(item_flags, int)

                    tab_result = begin_tab_item(tab.name, tab.opened, item_flags)
                    selected = tab_result.selected
                    opened = tab_result.opened_state

                    if (
                        opened is not None
                        and tab.opened is not None
                        and tab.opened != opened
                    ):
                        tab.opened = opened

                    if selected:
                        try:
                            if tab.callback is not None:
                                force_bind(tab.callback, *args, **kwargs)()
                        finally:
                            end_tab_item()
            finally:
                imgui.end_tab_bar()
