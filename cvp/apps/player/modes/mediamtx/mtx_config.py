# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox_value import checkbox_value as _check
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.input_int_value import input_int_value as _int
from cvp.imgui.input_text_value import input_text_value as _text
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.begin_table_mutable_sequence import begin_table_mutable_sequence
from cvp.mediamtx.client import GlobalConf
from cvp.mediamtx.item import MediamtxItem


class MediamtxGlobalConfTab:
    def __init__(self, context: Context):
        self._context = context
        self._runner = context.create_thread_runner(self.on_update_config_main)

    @property
    def context(self):
        return self._context

    @staticmethod
    def on_update_config_main(mediamtx: MediamtxItem):
        mediamtx.update_global_config()

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def __call__(self, mediamtx: MediamtxItem) -> None:
        running = self._runner.running
        has_error = bool(self._runner.error)

        with begin_child_context("Main", size=FIT_SIZE):
            if button("Reload", disabled=running):
                self._runner(mediamtx)

            if running:
                text_centered("Requesting a global config ...")
            elif has_error:
                assert not running
                self.text_error(str(self._runner.error))
            else:
                assert not running
                assert not has_error
                if mediamtx.config is None:
                    text_centered("Empty global config ...")
                else:
                    self.do_mediamtx_config(mediamtx.config)

    @staticmethod
    def do_mediamtx_config(c: GlobalConf) -> None:
        imgui.separator_text("Logging")
        _text("logLevel", c.logLevel)
        begin_table_mutable_sequence("logDestinations", c.logDestinations or [])
        _text("logFile", c.logFile)
        _text("sysLogPrefix", c.sysLogPrefix)

        imgui.separator_text("Connection")
        _text("readTimeout", c.readTimeout)
        _text("writeTimeout", c.writeTimeout)
        _int("writeQueueSize", c.writeQueueSize)
        _int("udpMaxPayloadSize", c.udpMaxPayloadSize)
        _text("runOnConnect", c.runOnConnect)
        _check("runOnConnectRestart", c.runOnConnectRestart)
        _text("runOnDisconnect", c.runOnDisconnect)

        imgui.separator_text("Auth")
        _text("authMethod", c.authMethod)
        # authInternalUsers: typing.List["AuthInternalUser"]
        _text("authHTTPAddress", c.authHTTPAddress)
        # authHTTPExclude: typing.List["AuthInternalUserPermission"]
        _text("authJWTJWKS", c.authJWTJWKS)
        _text("authJWTClaimKey", c.authJWTClaimKey)

        imgui.separator_text("API")
        _check("api", c.api)
        _text("apiAddress", c.apiAddress)
        _check("apiEncryption", c.apiEncryption)
        _text("apiServerKey", c.apiServerKey)
        _text("apiServerCert", c.apiServerCert)
        _text("apiAllowOrigin", c.apiAllowOrigin)
        begin_table_mutable_sequence("apiTrustedProxies", c.apiTrustedProxies)

        imgui.separator_text("Metrics")
        _check("metrics", c.metrics)
        _text("metricsAddress", c.metricsAddress)
        _check("metricsEncryption", c.metricsEncryption)
        _text("metricsServerKey", c.metricsServerKey)
        _text("metricsServerCert", c.metricsServerCert)
        _text("metricsAllowOrigin", c.metricsAllowOrigin)
        begin_table_mutable_sequence("metricsTrustedProxies", c.metricsTrustedProxies)

        imgui.separator_text("Profiling")
        _check("pprof", c.pprof)
        _text("pprofAddress", c.pprofAddress)
        _check("pprof", c.pprofEncryption)
        _text("pprofServerKey", c.pprofServerKey)
        _text("pprofServerCert", c.pprofServerCert)
        _text("pprofAllowOrigin", c.pprofAllowOrigin)
        begin_table_mutable_sequence("pprofTrustedProxies", c.pprofTrustedProxies)

        imgui.separator_text("Playback")
        _check("playback", c.playback)
        _text("playbackAddress", c.playbackAddress)
        _check("playbackEncryption", c.playbackEncryption)
        _text("playbackServerKey", c.playbackServerKey)
        _text("playbackServerCert", c.playbackServerCert)
        _text("playbackAllowOrigin", c.playbackAllowOrigin)
        begin_table_mutable_sequence("playbackTrustedProxies", c.playbackTrustedProxies)

        imgui.separator_text("RTSP")
        _check("rtsp", c.rtsp)
        begin_table_mutable_sequence("rtspTransports", c.rtspTransports)
        _text("rtspEncryption", c.rtspEncryption)
        _text("rtspAddress", c.rtspAddress)
        _text("rtspsAddress", c.rtspsAddress)
        _text("rtpAddress", c.rtpAddress)
        _text("rtcpAddress", c.rtcpAddress)
        _text("multicastIPRange", c.multicastIPRange)
        _int("multicastRTPPort", c.multicastRTPPort)
        _int("multicastRTCPPort", c.multicastRTCPPort)
        _text("rtspServerKey", c.rtspServerKey)
        _text("rtspServerCert", c.rtspServerCert)
        begin_table_mutable_sequence("rtspAuthMethods", c.rtspAuthMethods)

        imgui.separator_text("RTMP")
        _check("rtmp", c.rtmp)
        _text("rtmpAddress", c.rtmpAddress)
        _text("rtmpEncryption", c.rtmpEncryption)
        _text("rtmpsAddress", c.rtmpsAddress)
        _text("rtmpServerKey", c.rtmpServerKey)
        _text("rtmpServerCert", c.rtmpServerCert)

        imgui.separator_text("HLS")
        _check("hls", c.hls)
        _text("hlsAddress", c.hlsAddress)
        _check("hlsEncryption", c.hlsEncryption)
        _text("hlsServerKey", c.hlsServerKey)
        _text("hlsServerCert", c.hlsServerCert)
        _text("hlsAllowOrigin", c.hlsAllowOrigin)
        begin_table_mutable_sequence("hlsTrustedProxies", c.hlsTrustedProxies)
        _check("hlsAlwaysRemux", c.hlsAlwaysRemux)
        _text("hlsVariant", c.hlsVariant)
        _int("hlsSegmentCount", c.hlsSegmentCount)
        _text("hlsSegmentDuration", c.hlsSegmentDuration)
        _text("hlsPartDuration", c.hlsPartDuration)
        _text("hlsSegmentMaxSize", c.hlsSegmentMaxSize)
        _text("hlsDirectory", c.hlsDirectory)
        _text("hlsMuxerCloseAfter", c.hlsMuxerCloseAfter)

        imgui.separator_text("WebRTC")
        _check("webrtc", c.webrtc)
        _text("webrtcAddress", c.webrtcAddress)
        _check("webrtcEncryption", c.webrtcEncryption)
        _text("webrtcServerKey", c.webrtcServerKey)
        _text("webrtcServerCert", c.webrtcServerCert)
        _text("webrtcAllowOrigin", c.webrtcAllowOrigin)
        begin_table_mutable_sequence("webrtcTrustedProxies", c.webrtcTrustedProxies)
        _text("webrtcLocalUDPAddress", c.webrtcLocalUDPAddress)
        _text("webrtcLocalTCPAddress", c.webrtcLocalTCPAddress)
        _check("webrtcIPsFromInterfaces", c.webrtcIPsFromInterfaces)
        begin_table_mutable_sequence(
            "webrtcIPsFromInterfacesList",
            c.webrtcIPsFromInterfacesList,
        )
        begin_table_mutable_sequence("webrtcAdditionalHosts", c.webrtcAdditionalHosts)
        begin_table_mutable_sequence("webrtcICEServers2", c.webrtcICEServers2)
        _text("webrtcHandshakeTimeout", c.webrtcHandshakeTimeout)
        _text("webrtcTrackGatherTimeout", c.webrtcTrackGatherTimeout)
        _text("webrtcSTUNGatherTimeout", c.webrtcSTUNGatherTimeout)

        imgui.separator_text("SRT")
        _check("srt", c.srt)
        _text("srtAddress", c.srtAddress)
