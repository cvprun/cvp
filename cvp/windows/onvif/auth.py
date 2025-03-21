# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.config.sections.onvif import HttpAuth, OnvifConfig
from cvp.imgui.input_text_value import input_text_value
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
INPUT_PASSWORD: Final[int] = imgui.INPUT_TEXT_PASSWORD
INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifAuthTab(TabItem[OnvifConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Auth")
        self._show_password = False

    @property
    def keyrings(self):
        return self.context.home.keyrings

    @override
    def on_item(self, item: OnvifConfig) -> None:
        use_wsse = imgui.checkbox("Use WS-Security", item.use_wsse)
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text("Use <wsse:UsernameToken> in <soap:Header>")
        use_wsse_changed = use_wsse[0]
        use_wsse_value = use_wsse[1]
        assert isinstance(use_wsse_changed, bool)
        assert isinstance(use_wsse_value, bool)
        if use_wsse_changed:
            item.use_wsse = use_wsse_value

        if not item.use_wsse:
            return

        item.username = input_text_value(
            "Username",
            item.username,
            INPUT_BUFFER_SIZE,
        )

        password_flags = ENTER_RETURN if self._show_password else INPUT_PASSWORD
        prev_password = self.keyrings.get_onvif_password(item.uuid, str())
        next_password = input_text_value(
            "Password",
            prev_password,
            INPUT_BUFFER_SIZE,
            password_flags,
        )
        if prev_password != next_password:
            self.keyrings.set_onvif_password(item.uuid, next_password)

        show_password = imgui.checkbox("Show Password", self._show_password)
        show_password_changed = show_password[0]
        show_password_value = show_password[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_password = show_password_value

        imgui.text("Password Type:")
        if imgui.radio_button("PasswordText", item.http_auth is None):
            item.encode_digest = False
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text('Use <wsse:Password Type="wsse:PasswordText">')
        imgui.same_line()
        if imgui.radio_button("PasswordDigest", item.http_auth == HttpAuth.basic):
            item.encode_digest = True
        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text('Use <wsse:Password Type="wsse:PasswordDigest">')

        imgui.text("HTTP Authorization header:")
        if imgui.radio_button("None", item.http_auth is None):
            item.http_auth = None
        imgui.same_line()
        if imgui.radio_button("Basic", item.http_auth == HttpAuth.basic):
            item.http_auth = HttpAuth.basic
        imgui.same_line()
        if imgui.radio_button("Digest", item.http_auth == HttpAuth.digest):
            item.http_auth = HttpAuth.digest
