# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE, PASSWORD
from cvp.imgui.input_text_value import input_text_value
from cvp.onvif.onvif import HttpAuth, OnvifConfig
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class OnvifAuthTab(TabItem[OnvifConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Auth")
        self._show_password = False

    @override
    def on_item(self, item: OnvifConfig) -> None:
        use_wsse = imgui.checkbox("Use WS-Security", item.use_wsse)
        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text("Use <wsse:UsernameToken> in <soap:Header>")
                finally:
                    imgui.end_tooltip()
        use_wsse_changed = use_wsse[0]
        use_wsse_value = use_wsse[1]
        assert isinstance(use_wsse_changed, bool)
        assert isinstance(use_wsse_value, bool)
        if use_wsse_changed:
            item.use_wsse = use_wsse_value

        if not item.use_wsse:
            return

        item.username = input_text_value("Username", item.username)

        password_flags = ENTER_RETURNS_TRUE if self._show_password else PASSWORD
        prev_password = self.context.keyring.onvif.get(item.uuid)
        next_password = input_text_value(
            "Password",
            prev_password,
            password_flags,
        )
        if prev_password != next_password:
            self.context.keyring.onvif.set(item.uuid, next_password)

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
            if imgui.begin_tooltip():
                try:
                    imgui.text('Use <wsse:Password Type="wsse:PasswordText">')
                finally:
                    imgui.end_tooltip()
        imgui.same_line()
        if imgui.radio_button("PasswordDigest", item.http_auth == HttpAuth.basic):
            item.encode_digest = True
        if imgui.is_item_hovered():
            if imgui.begin_tooltip():
                try:
                    imgui.text('Use <wsse:Password Type="wsse:PasswordDigest">')
                finally:
                    imgui.end_tooltip()

        imgui.text("HTTP Authorization header:")
        if imgui.radio_button("None", item.http_auth is None):
            item.http_auth = None
        imgui.same_line()
        if imgui.radio_button("Basic", item.http_auth == HttpAuth.basic):
            item.http_auth = HttpAuth.basic
        imgui.same_line()
        if imgui.radio_button("Digest", item.http_auth == HttpAuth.digest):
            item.http_auth = HttpAuth.digest
