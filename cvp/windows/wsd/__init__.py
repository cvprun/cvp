# -*- coding: utf-8 -*-

from typing import Final, Mapping

from imgui_bundle import imgui
from wsdiscovery import WSDiscovery

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsd import WsdConfig, WsdManagerConfig
from cvp.imgui.button import button
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_item_width import item_width
from cvp.logging.logging import logger
from cvp.popups.confirm import ConfirmPopup
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import WSD_NAME_DEFAULT
from cvp.widgets.manager import Manager

NAME_BUFFER_SIZE: Final[int] = 2048
ENTER_RETURNS: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE

WSD_NAME_SCOPE_PREFIX: Final[str] = "onvif://www.onvif.org/name/"
WSD_NAME_SCOPE_PREFIX_LEN: Final[int] = len(WSD_NAME_SCOPE_PREFIX)


class WsdManager(Manager[WsdManagerConfig, WsdConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.wsd_manager,
            title="WsDiscovery",
            closable=True,
            flags=None,
        )

        self._wsd_running = False
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove device?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._confirm_remove)

    def run_discovery(self) -> None:
        if self._wsd_running:
            raise ValueError("WsDiscovery is already running")

        self._wsd_running = True
        self.context.pm.submit_thread(self._discovery_main)

    def _discovery_main(self) -> None:
        try:
            wsd = WSDiscovery()
            wsd.start()
            try:
                for service in wsd.searchServices():
                    config = WsdConfig()
                    config.epr = service.getEPR()
                    config.instance_id = service.getInstanceId()
                    config.message_number = service.getMessageNumber()
                    config.metadata_version = service.getMetadataVersion()
                    config.scopes = [s.getValue() for s in service.getScopes()]
                    config.types = [t.getFullname() for t in service.getTypes()]
                    config.xaddrs = [a for a in service.getXAddrs()]

                    for scope in config.scopes:
                        assert isinstance(scope, str)
                        if scope.startswith(WSD_NAME_SCOPE_PREFIX):
                            config.name = scope[WSD_NAME_SCOPE_PREFIX_LEN:]

                    if not config.name:
                        config.name = config.epr
                    if not config.name:
                        config.name = WSD_NAME_DEFAULT

                    logger.info(f"Device discovered: {config}")
                    try:
                        self.context.config.remove_wsd(config.epr)
                    except KeyError:
                        pass
                    self.context.config.wsds.append(config)
            finally:
                wsd.stop()
        finally:
            self._wsd_running = False

    @override
    def get_menus(self) -> Mapping[str, WsdConfig]:
        return {wsd.epr: wsd for wsd in self.context.config.wsds}

    @override
    def on_process_sidebar_top(self) -> None:
        if button("Discovery", disabled=self._wsd_running):
            self.run_discovery()
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    @override
    def on_menu(self, key: str, item: WsdConfig) -> None:
        imgui.text("Web Services Dynamic Discovery")
        imgui.separator()

        imgui.text("Name:")
        with item_width(-1):
            changed_name, value_name = imgui.input_text(
                "## Name",
                item.name,
                NAME_BUFFER_SIZE,
                ENTER_RETURNS,
            )
            assert isinstance(changed_name, bool)
            assert isinstance(value_name, str)
            if changed_name:
                item.name = value_name

        imgui.text("EPR:")
        input_text_disabled("## EPR", item.epr)

        imgui.text("Instance ID:")
        input_text_disabled("## InstanceID", str(item.instance_id))

        imgui.text("Message Number:")
        input_text_disabled("## MessageNumber", str(item.message_number))

        imgui.text("Metadata Version:")
        input_text_disabled("## MetadataVersion", str(item.metadata_version))

        imgui.text("Types:")
        if item.types:
            for i, type_ in enumerate(item.types):
                imgui.bullet()
                imgui.same_line()
                input_text_disabled(f"## Type[{i}]", type_)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty types")

        imgui.text("Scopes:")
        if item.scopes:
            for i, scope in enumerate(item.scopes):
                imgui.bullet()
                imgui.same_line()
                input_text_disabled(f"## Scope[{i}]", scope)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty scopes")

        imgui.text("XAddr:")
        if item.xaddrs:
            has_onvif_scope = item.has_onvif_scope()
            for i, xaddr in enumerate(item.xaddrs):
                imgui.bullet()

                if has_onvif_scope:
                    imgui.same_line()
                    if imgui.button(f"Use ONVIF## Use ONVIF[{i}]"):
                        config = OnvifConfig(address=xaddr, name=item.name)
                        self.context.config.onvifs.append(config)

                imgui.same_line()
                input_text_disabled(f"## XAddr[{i}]", xaddr)
        else:
            imgui.bullet()
            imgui.same_line()
            imgui.text("Empty xaddrs")

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        epr = selected_menu.epr
        self.context.config.remove_wsd(epr)
