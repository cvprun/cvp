# -*- coding: utf-8 -*-

from logging import getLogger

from cvp.logging import names

logger = getLogger(names.CVP_LOGGER_NAME)

canvas_logger = getLogger(names.CVP_CANVAS_LOGGER_NAME)
chat_logger = getLogger(names.CVP_CHAT_LOGGER_NAME)
download_logger = getLogger(names.CVP_DOWNLOAD_LOGGER_NAME)
event_logger = getLogger(names.CVP_EVENT_LOGGER_NAME)
flow_logger = getLogger(names.CVP_FLOW_LOGGER_NAME)
imgui_logger = getLogger(names.CVP_IMGUI_LOGGER_NAME)
mpv_logger = getLogger(names.CVP_MPV_LOGGER_NAME)
msg_logger = getLogger(names.CVP_MSG_LOGGER_NAME)
onvif_logger = getLogger(names.CVP_ONVIF_LOGGER_NAME)
profile_logger = getLogger(names.CVP_PROFILE_LOGGER_NAME)
renderer_logger = getLogger(names.CVP_RENDERER_LOGGER_NAME)
scheduler_logger = getLogger(names.CVP_SCHEDULER_LOGGER_NAME)
service_logger = getLogger(names.CVP_SERVICE_LOGGER_NAME)
watchdog_logger = getLogger(names.CVP_WATCHDOG_LOGGER_NAME)
widgets_logger = getLogger(names.CVP_WIDGETS_LOGGER_NAME)
worker_logger = getLogger(names.CVP_WORKER_LOGGER_NAME)
ws_logger = getLogger(names.CVP_WS_LOGGER_NAME)
wsdl_logger = getLogger(names.CVP_WSDL_LOGGER_NAME)
