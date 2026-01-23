# -*- coding: utf-8 -*-

from typing import Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import HUB
from cvp.context.context import Context
from cvp.hub.agent_handler import AgentSession
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class HubMode(BaseMode):
    __cvp_mode_name__ = "Hub"
    __cvp_mode_icon__ = HUB

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

        self._disconnect_candidate: Optional[str] = None
        self._confirm_disconnect = ConfirmPopup(
            title="Disconnect",
            label="Are you sure you want to disconnect this agent?",
            ok="Disconnect",
            cancel="No",
            target=self.on_confirm_disconnect,
        )
        self._confirm_disconnect_all = ConfirmPopup(
            title="Disconnect All",
            label="Are you sure you want to disconnect all agents?",
            ok="Disconnect All",
            cancel="No",
            target=self.on_confirm_disconnect_all,
        )

        self._popups = PopupList(
            self._confirm_disconnect,
            self._confirm_disconnect_all,
        )

    @property
    def hub(self):
        return self.context.hub

    @property
    def selected_session(self) -> Optional[AgentSession]:
        sessions = self.hub.sessions
        session_id = self.selected_submenu
        return sessions.get(session_id)

    def on_confirm_disconnect(self, value: bool) -> None:
        if not value:
            return
        if self._disconnect_candidate:
            self.hub.disconnect_session(self._disconnect_candidate)
            self._disconnect_candidate = None

    def on_confirm_disconnect_all(self, value: bool) -> None:
        if not value:
            return
        sessions = self.hub.sessions
        for session_id in list(sessions.keys()):
            self.hub.disconnect_session(session_id)

    def _render_server_controls(self) -> None:
        is_running = self.hub.is_running

        if is_running:
            if button("Stop"):
                self.hub.stop()
        else:
            if button("Start"):
                self.hub.start()

        imgui.same_line()
        sessions = self.hub.sessions
        session_count = len(sessions)
        has_selection = self.selected_submenu in sessions

        if button("Disconnect", disabled=not has_selection):
            self._disconnect_candidate = self.selected_submenu
            self._confirm_disconnect.show()

        imgui.same_line()
        if button("Disconnect All", disabled=session_count == 0):
            self._confirm_disconnect_all.show()

    def _render_server_status(self) -> None:
        imgui.separator()

        is_running = self.hub.is_running
        if is_running:
            self.text_success("Server: Running")
            imgui.same_line()
            imgui.text(f"({self.hub.host}:{self.hub.port})")
        else:
            self.text_warning("Server: Stopped")

        imgui.text(f"Connected Agents: {self.hub.session_count}")
        imgui.separator()

    def _render_session_list(self) -> None:
        sessions = self.hub.sessions

        if imgui.begin_list_box("##AgentList", FIT_SIZE):
            try:
                for session_id, session in sessions.items():
                    label = f"{session_id}"
                    selected = session_id == self.selected_submenu
                    if imgui.selectable(label, selected)[1]:
                        self.selected_submenu = session_id
            finally:
                imgui.end_list_box()

    def _render_session_details(self, session: AgentSession) -> None:
        imgui.text(f"Session ID: {session.session_id}")

        connected_str = session.connected_at.strftime("%Y-%m-%d %H:%M:%S")
        imgui.text(f"Connected At: {connected_str}")

        if session.last_heartbeat:
            heartbeat_str = session.last_heartbeat.strftime("%Y-%m-%d %H:%M:%S")
            imgui.text(f"Last Heartbeat: {heartbeat_str}")
        else:
            imgui.text("Last Heartbeat: N/A")

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Menu",
                size=(self._MENU_SPLIT_X, 0),
                child_flags=self._MENU_CHILD_FLAGS,
            ):
                self._render_server_controls()
                self._render_server_status()
                self._render_session_list()

            imgui.same_line()

            with begin_child_context("Main"):
                if selected_session := self.selected_session:
                    self._render_session_details(selected_session)
                else:
                    text_centered("Please select an agent")

        self._popups.do_process()
