# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from os import PathLike
from typing import List, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.config.sections.appearance import AppearanceConfig
from cvp.config.sections.canvas import CanvasWindowConfig
from cvp.config.sections.catalog import CatalogManagerConfig
from cvp.config.sections.chat import ChatConfig
from cvp.config.sections.concurrency import ConcurrencyConfig
from cvp.config.sections.context import ContextConfig
from cvp.config.sections.developer import DeveloperConfig
from cvp.config.sections.display import DisplayConfig
from cvp.config.sections.dtype import DtypeManagerConfig
from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.config.sections.flow import FlowAuiConfig
from cvp.config.sections.font import FontConfig, FontManagerConfig
from cvp.config.sections.games.tetrix import TetrixWindowConfig
from cvp.config.sections.graphic import GraphicConfig
from cvp.config.sections.keyring import KeyringConfig
from cvp.config.sections.layout import LayoutConfig, LayoutManagerConfig
from cvp.config.sections.logging import LoggingConfig
from cvp.config.sections.media import MediaManagerConfig
from cvp.config.sections.onvif import OnvifManagerConfig
from cvp.config.sections.overlay import OverlayConfig
from cvp.config.sections.preference import PreferenceConfig
from cvp.config.sections.process import ProcessManagerConfig
from cvp.config.sections.stitching import StitchingConfig
from cvp.config.sections.supabase import SupabaseConfig
from cvp.config.sections.toast import ToastConfig
from cvp.config.sections.wsdiscovery import WsDiscoveryConfig
from cvp.inspect.member import get_public_instance_attributes
from cvp.itertools.find_index import find_index
from cvp.media.config import MediaConfig
from cvp.yaml.dumpers import DefaultDumper


@dataclass
class Config:
    appearance: AppearanceConfig = field(default_factory=AppearanceConfig)
    canvas_window: CanvasWindowConfig = field(default_factory=CanvasWindowConfig)
    catalog_manager: CatalogManagerConfig = field(default_factory=CatalogManagerConfig)
    chat: ChatConfig = field(default_factory=ChatConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    developer: DeveloperConfig = field(default_factory=DeveloperConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    dtype_manager: DtypeManagerConfig = field(default_factory=DtypeManagerConfig)
    ffmpeg: FFmpegConfig = field(default_factory=FFmpegConfig)
    flow_aui: FlowAuiConfig = field(default_factory=FlowAuiConfig)
    font: FontConfig = field(default_factory=FontConfig)
    font_manager: FontManagerConfig = field(default_factory=FontManagerConfig)
    graphic: GraphicConfig = field(default_factory=GraphicConfig)
    keyring: KeyringConfig = field(default_factory=KeyringConfig)
    layout_manager: LayoutManagerConfig = field(default_factory=LayoutManagerConfig)
    layouts: List[LayoutConfig] = field(default_factory=list)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    media_manager: MediaManagerConfig = field(default_factory=MediaManagerConfig)
    media_windows: List[MediaConfig] = field(default_factory=list)
    onvif_manager: OnvifManagerConfig = field(default_factory=OnvifManagerConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    preference: PreferenceConfig = field(default_factory=PreferenceConfig)
    process_manager: ProcessManagerConfig = field(default_factory=ProcessManagerConfig)
    server: SupabaseConfig = field(default_factory=SupabaseConfig)
    stitching: StitchingConfig = field(default_factory=StitchingConfig)
    tetrix_window: TetrixWindowConfig = field(default_factory=TetrixWindowConfig)
    toast: ToastConfig = field(default_factory=ToastConfig)
    wsdiscovery: WsDiscoveryConfig = field(default_factory=WsDiscoveryConfig)

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

    def remove_layout(self, uuid: str):
        index = find_index(self.layouts, lambda layout: layout.uuid == uuid)
        if index < 0:
            raise KeyError(f"Not found layout: '{uuid}'")
        return self.layouts.pop(index)

    def remove_media_window(self, uuid: str):
        index = find_index(self.media_windows, lambda mw: mw.uuid == uuid)
        if index < 0:
            raise KeyError(f"Not found media window: '{uuid}'")
        return self.media_windows.pop(index)

    def dumps_yaml(self, encoding="utf-8") -> bytes:
        return dump(serialize(self), Dumper=DefaultDumper).encode(encoding)

    def loads_yaml(self, data: bytes) -> None:
        result = deserialize(full_load(data), type(self))
        assert isinstance(result, type(self))
        attrs = get_public_instance_attributes(self)
        for key, _ in attrs:
            value = getattr(result, key, None)
            if value is not None:
                setattr(self, key, value)

    def write_yaml(self, file: Union[str, PathLike[str]], encoding="utf-8") -> None:
        with open(file, "wb") as f:
            f.write(self.dumps_yaml(encoding))

    def read_yaml(self, file: Union[str, PathLike[str]]) -> None:
        with open(file, "rb") as f:
            self.loads_yaml(f.read())
