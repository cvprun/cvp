# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from os import PathLike
from typing import Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.config.sections.appearance import AppearanceConfig
from cvp.config.sections.canvas import CanvasConfig
from cvp.config.sections.chat import ChatConfig
from cvp.config.sections.concurrency import ConcurrencyConfig
from cvp.config.sections.context import ContextConfig
from cvp.config.sections.developer import DeveloperConfig
from cvp.config.sections.directory import DirectoryConfig
from cvp.config.sections.display import DisplayConfig
from cvp.config.sections.downloader import DownloaderConfig
from cvp.config.sections.faker import FakerConfig
from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.config.sections.flow import FlowConfig
from cvp.config.sections.font import FontConfig
from cvp.config.sections.games.tetrix import TetrixConfig
from cvp.config.sections.graphic import GraphicConfig
from cvp.config.sections.keyring import KeyringConfig
from cvp.config.sections.logging import LoggingConfig
from cvp.config.sections.mediamtx import MediamtxConfig
from cvp.config.sections.navigation import NavigationConfig
from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.overlay import OverlayConfig
from cvp.config.sections.process import ProcessConfig
from cvp.config.sections.scheduler import SchedulerConfig
from cvp.config.sections.sockmap import SockmapConfig
from cvp.config.sections.stitching import StitchingConfig
from cvp.config.sections.supabase import SupabaseConfig
from cvp.config.sections.terminal import TerminalConfig
from cvp.config.sections.toast import ToastConfig
from cvp.config.sections.watchdog import WatchdogConfig
from cvp.config.sections.wsdiscovery import WsDiscoveryConfig
from cvp.inspect.member import get_public_instance_attributes
from cvp.yaml.dumpers import DefaultDumper


@dataclass
class Config:
    appearance: AppearanceConfig = field(default_factory=AppearanceConfig)
    canvas: CanvasConfig = field(default_factory=CanvasConfig)
    chat: ChatConfig = field(default_factory=ChatConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    developer: DeveloperConfig = field(default_factory=DeveloperConfig)
    directory: DirectoryConfig = field(default_factory=DirectoryConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    downloader: DownloaderConfig = field(default_factory=DownloaderConfig)
    faker: FakerConfig = field(default_factory=FakerConfig)
    ffmpeg: FFmpegConfig = field(default_factory=FFmpegConfig)
    flow: FlowConfig = field(default_factory=FlowConfig)
    font: FontConfig = field(default_factory=FontConfig)
    graphic: GraphicConfig = field(default_factory=GraphicConfig)
    keyring: KeyringConfig = field(default_factory=KeyringConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    mediamtx: MediamtxConfig = field(default_factory=MediamtxConfig)
    navigation: NavigationConfig = field(default_factory=NavigationConfig)
    onvif: OnvifConfig = field(default_factory=OnvifConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    process: ProcessConfig = field(default_factory=ProcessConfig)
    sockmap: SockmapConfig = field(default_factory=SockmapConfig)
    server: SupabaseConfig = field(default_factory=SupabaseConfig)
    terminal: TerminalConfig = field(default_factory=TerminalConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    stitching: StitchingConfig = field(default_factory=StitchingConfig)
    tetrix: TetrixConfig = field(default_factory=TetrixConfig)
    toast: ToastConfig = field(default_factory=ToastConfig)
    watchdog: WatchdogConfig = field(default_factory=WatchdogConfig)
    wsdiscovery: WsDiscoveryConfig = field(default_factory=WsDiscoveryConfig)

    @property
    def debug(self):
        return self.developer.debug

    @property
    def verbose(self):
        return self.developer.verbose

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
