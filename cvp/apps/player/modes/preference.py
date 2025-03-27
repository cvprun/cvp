# -*- coding: utf-8 -*-

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.imgui.dockspace import dockspace_context
from cvp.msgs.msg import Msg
from cvp.types.override import override
from cvp.imgui.flags.dock_node import PASSTHRU_CENTRAL_NODE, AUTO_HIDE_TAB_BAR
from cvp.imgui.flags.child import RESIZE_X, BORDERS


class PreferenceMode(BaseMode):
    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.preference

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @override
    def do_process(self) -> None:
        # dockspace = imgui.dock_space_over_viewport(flags=PASSTHRU_CENTRAL_NODE | AUTO_HIDE_TAB_BAR)
        # imgui.set_next_window_dock_id(dockspace)

        # if (!ImGui::DockBuilderGetNode(dockspace_id)) {
        # ImGui::DockBuilderRemoveNode(dockspace_id); // reset
        # ImGui::DockBuilderAddNode(dockspace_id, ImGuiDockNodeFlags_DockSpace);
        # ImGui::DockBuilderSetNodeSize(dockspace_id, ImGui::GetMainViewport()->Size);
        #
        # ImGuiID dock_main_id = dockspace_id;
        # ImGuiID dock_left_id = ImGui::DockBuilderSplitNode(dock_main_id, ImGuiDir_Left, 0.3f, nullptr, &dock_main_id);
        # ImGuiID dock_right_id = dock_main_id;
        #
        # ImGui::DockBuilderDockWindow("Panel 1", dock_left_id);
        # ImGui::DockBuilderDockWindow("Panel 2", dock_right_id);
        # ImGui::DockBuilderFinish(dockspace_id);
        # }

        imgui.begin("Main")

        height = -imgui.get_frame_height_with_spacing()

        imgui.begin_child("Left", (150, height), child_flags=RESIZE_X | BORDERS)
        imgui.text("Content")
        imgui.end_child()

        imgui.same_line()

        imgui.begin_child("Right", (0, height))
        imgui.text("Content")
        imgui.end_child()

        imgui.end()
