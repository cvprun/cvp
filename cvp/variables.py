# -*- coding: utf-8 -*-

from typing import Final

from cvp.types.colors import RGBA
from cvp.types.shapes import Size

TIMEOUT_INFINITE: Final[float] = -1.0
INFINITE: Final[int] = -1
UNKNOWN_ERROR_CODE: Final[int] = -1
NOT_FOUND_INDEX: Final[int] = -1
UNKNOWN_TOTAL_SIZE: Final[int] = -1
UNKNOWN_PID: Final[int] = -1
UNKNOWN_VERSION: Final[int] = -1
UNKNOWN_THREAD_IDENT: Final[int] = -1
INFINITY_HEIGHT_IN_ITEMS: Final[int] = -1
NULL_CODEPOINT: Final[int] = 0
BACKSPACE_CODEPOINT: Final[int] = ord("\b")
NODOC: Final[str] = ""
COMMENT_PREFIX: Final[str] = "#"
HEXADECIMAL: Final[int] = 16
NEWLINE: Final[str] = "\n"
COMMA: Final[str] = ","

STDIN_FILE_HANDLE: Final[int] = 0
STDOUT_FILE_HANDLE: Final[int] = 1
STDERR_FILE_HANDLE: Final[int] = 2

STDIN_FILE_NAME: Final[str] = "stdin"
STDOUT_FILE_NAME: Final[str] = "stdout"
STDERR_FILE_NAME: Final[str] = "stderr"

CVP_TITLE: Final[str] = "CVP"
CVP_HOME_DIRNAME: Final[str] = ".cvp"
CVP_YML_FILENAME: Final[str] = "cvp.yml"
CVP_EXTENSION: Final[str] = ".cvp"
CVP_ROOT_INFO_FILENAME: Final[str] = "info.yml"
GUI_INI_FILENAME: Final[str] = "gui.ini"
LOGGING_JSON_FILENAME: Final[str] = "logging.json"

DOTENV_LOCAL_FILENAME: Final[str] = ".env.local"
DOTENV_TEST_FILENAME: Final[str] = ".env.test"

MODULE_PATH_SEPARATOR: Final[str] = "."
CONFIG_VALUE_SEPARATOR: Final[str] = ","
CHECKSUM_DELIMITER: Final[str] = ":"

UNICODE_SINGLE_BLOCK_SIZE: Final[int] = 0x100
CODEPOINT_RANGES_EXTENSION: Final[str] = ".ranges"
CODEPOINT_GLYPHS_EXTENSION: Final[str] = ".glyphs"
KEYRING_EXTENSION: Final[str] = ".cfg"

FONT_SIZE: Final[int] = 14
FONT_PREVIEW_SIZE: Final[int] = 48
FONT_SCALE: Final[float] = 1.0
FONT_NAME: Final[str] = "Default"

THREAD_POOL_PREFIX: Final[str] = "cvp.threadpool"
MAX_THREAD_WORKERS: Final[int] = 5
MAX_PROCESS_WORKERS: Final[int] = 5

PROCESS_LOGFILE_PREFIX: Final[str] = ""
PROCESS_LOGFILE_SUFFIX: Final[str] = ".log"
PROCESS_PIDFILE_SUFFIX: Final[str] = ".pid"

ASCII_RANGE: Final[int] = 127
MAX_IMGUI_KEYCODE: Final[int] = 512

MOUSE_WHEEL_OFFSET_SCALE: Final[float] = 0.5

LOGGING_STEP: Final[int] = 1000
SLOW_CALLBACK_DURATION: Final[float] = 0.05

SAFETY_FILE_SUFFIX_NEW: Final[str] = ".new.backup"
SAFETY_FILE_SUFFIX_OLD: Final[str] = ".old.backup"

LABEL_CLEAR_RECENT_ITEMS: Final[str] = "Clear recent items"
LABEL_FILTER: Final[str] = "Filter"

CHAT_SQLITE_FILENAME: Final[str] = "chat.sqlite"
CHAT_TITLE_NONAME: Final[str] = "[New chat]"
CHAT_SERVER_NONAME: Final[str] = "[New server]"
CHAT_LIMIT: Final[int] = 30
CHAT_INVALID_ID: Final[int] = -1

OLLAMA_NONAME: Final[str] = "[New Ollama]"
OLLAMA_ADDRESS: Final[str] = "http://localhost:11434/"
OLLAMA_MODEL_NAME_SEPARATOR: Final[str] = "@"

LAYOUT_NONAME: Final[str] = "[New Layout]"

MEDIA_NONAME: Final[str] = "[New Media]"
MEDIA_FRAME_RGB24_CHANNELS: Final[int] = 3
MEDIA_FRAME_PIPE_STDOUT: Final[str] = "pipe:1"
MEDIA_FRAME_WIDTH: Final[int] = 400
MEDIA_FRAME_HEIGHT: Final[int] = 300
MEDIA_INSPECT_TIMEOUT: Final[float] = 3.0

JOB_NONAME: Final[str] = "[New Job]"
SERVICE_NONAME: Final[str] = "[New Service]"
WATCHDOG_NONAME: Final[str] = "[New Watchdog]"
MEDIAMTX_NONAME: Final[str] = "[New MediaMTX]"
TEXT_NONAME: Final[str] = "[New Text]"

SUPABASE_ADDRESS: Final[str] = "http://localhost:8000/"

HOVERED_TOOLTIP_TEXT_WRAPPED_WIDTH: Final[int] = 400

API_SELECT_WIDTH: Final[float] = 180.0
MIN_API_SELECT_WIDTH: Final[float] = 100.0
MAX_API_SELECT_WIDTH: Final[float] = 300.0

FAKER_SEED_LENGTH: Final[int] = 16
FAKER_REPEAT: Final[int] = 10
FAKER_SEPARATOR: Final[str] = "\\n"

PROCESS_TEARDOWN_TIMEOUT: Final[float] = 24.0
PROCESS_UPDATE_INTERVAL: Final[float] = 1.0
MIN_NICE = -20
MAX_NICE = 19
DEFAULT_NICE = 0

IMGUI_INPUT_DATETIME_SEPARATOR: Final[str] = "T"
IMGUI_INPUT_DATE_SEPARATOR: Final[str] = "/"
IMGUI_INPUT_TIME_SEPARATOR: Final[str] = ":"

FFMPEG_EXECUTABLE_FILENAME: Final[str] = "ffmpeg"
FFPROBE_EXECUTABLE_FILENAME: Final[str] = "ffprobe"

STREAM_LOGGING_MAXSIZE: Final[int] = 65536
STREAM_LOGGING_ENCODING: Final[str] = "utf-8"
STREAM_LOGGING_NEWLINE_SIZE: Final[int] = 88

WSD_INVALID_INSTANCE_ID: Final[int] = -1
WSD_INVALID_MESSAGE_NUMBER: Final[int] = -1
WSD_INVALID_METADATA_VERSION: Final[int] = -1
WSD_UNICAST_ADDRESS: Final[str] = "192.168.0.1"
WSD_IPV4_MULTICAST_ADDRESS: Final[str] = "239.255.255.250"
WSD_IPV6_MULTICAST_ADDRESS: Final[str] = "ff02::c"
WSD_PORT_NUMBER: Final[int] = 3702
WSD_TIMEOUT: Final[float] = 3.0
WSD_NAME_DEFAULT: Final[str] = "New Device"
WSD_ONVIF_SCOPE_PREFIX: Final[str] = "onvif://www.onvif.org/name/"
WSD_ONVIF_SCOPE_PREFIX_LEN: Final[int] = len(WSD_ONVIF_SCOPE_PREFIX)
WSD_UNICAST_UDP_REPEAT: Final[int] = 2
WSD_MULTICAST_UDP_REPEAT: Final[int] = 4
WSD_RELATES_TO: Final[bool] = True

SOCKMAP_ADDRESS_BEGIN: Final[str] = "192.168.0.1"
SOCKMAP_ADDRESS_END: Final[str] = "192.168.0.254"
SOCKMAP_PORT_RANGE: Final[str] = "80,443"
SOCKMAP_TIMEOUT: Final[float] = 3.0

ONVIF_NONAME: Final[str] = "New Device"
ONVIF_ADDRESS: Final[str] = "http://localhost/"

ZEEP_ELEMENT_SEPARATOR: Final[str] = "."

DEFAULT_MAX_TEXTURE_SIZE: Final[int] = 2048

BEZIER_CURVE_TESSELLATION_TOLERANCE: Final[float] = 1.25
"""
Tessellation tolerance when using BezierCurve without a specific number of segments.
Decrease for highly tessellated curves (higher quality, more polygons),
Increase to reduce quality.
"""

CANVAS_ANCHOR_SELECTED_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.9
CANVAS_ANCHOR_HOVERING_COLOR: Final[RGBA] = 1.0, 0.49, 0.05, 0.9
CANVAS_ANCHOR_NORMAL_COLOR: Final[RGBA] = 0.0, 0.0, 1.0, 0.8
CANVAS_ANCHOR_DRAWING_RADIUS: Final[float] = 4.0
CANVAS_ANCHOR_HOVERING_TOLERANCE: Final[float] = 6.0
CANVAS_LINE_HOVERING_TOLERANCE: Final[float] = 6.0
CANVAS_MAX_HISTORY: Final[int] = 20

CANVAS_ZOOM_FACTOR: Final[float] = 1.125
CANVAS_ZOOM_MIN_SCALE: Final[float] = 0.001
CANVAS_ZOOM_MAX_SCALE: Final[float] = 256.0

CANVAS_AXIS_VISIBLE: Final[bool] = True
CANVAS_AXIS_THICKNESS: Final[float] = 1.0
CANVAS_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6

CANVAS_GRID_VISIBLE: Final[bool] = True
CANVAS_GRID_STEP: Final[float] = 50.0
CANVAS_GRID_THICKNESS: Final[float] = 1.0
CANVAS_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2

CANVAS_PIXEL_VISIBLE: Final[bool] = True
CANVAS_PIXEL_THICKNESS: Final[float] = 1.0
CANVAS_PIXEL_COLOR: Final[RGBA] = 0.5, 0.5, 0.5, 0.5
CANVAS_PIXEL_ZOOM_THRESHOLD: Final[float] = 64

CANVAS_ROI_COLOR: Final[RGBA] = 0.0, 0.0, 1.0, 0.3
CANVAS_ROI_ROUNDING: Final[float] = 0.0
CANVAS_ROI_THICKNESS: Final[float] = 2.0

FLOW_PATH_SEPARATOR: Final[str] = "."
FLOW_PATH_ENCODING: Final[str] = "utf-8"
FLOW_GRAPHS_DIRNAME: Final[str] = "graphs"

FLOW_BACKGROUND_COLOR: Final[RGBA] = 0.5, 0.5, 0.5, 1.0
FLOW_MAX_HISTORY: Final[int] = 20
FLOW_PASTE_MARGIN: Final[float] = 20.0

FLOW_NODE_SHOW_LAYOUT: Final[bool] = False
FLOW_NODE_ITEM_SPACING: Final[Size] = 2.0, 2.0
FLOW_NODE_BACKGROUND_COLOR: Final[RGBA] = 1.0, 1.0, 1.0, 0.6
FLOW_NODE_LAYOUT_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.8
FLOW_NODE_LABEL_COLOR: Final[RGBA] = 0.0, 0.0, 0.0, 0.8

FLOW_NODE_SELECTED_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.9
FLOW_NODE_HOVERING_COLOR: Final[RGBA] = 1.0, 0.49, 0.05, 0.9
FLOW_NODE_NORMAL_COLOR: Final[RGBA] = 1.0, 1.0, 1.0, 0.8
FLOW_NODE_SELECTED_THICKNESS: Final[float] = 2.0
FLOW_NODE_HOVERING_THICKNESS: Final[float] = 1.5
FLOW_NODE_NORMAL_THICKNESS: Final[float] = 1.0
FLOW_NODE_ROUNDING: Final[float] = 1.0

FLOW_PIN_SELECTED_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.9
FLOW_PIN_HOVERING_COLOR: Final[RGBA] = 1.0, 0.49, 0.05, 0.9
FLOW_PIN_NORMAL_COLOR: Final[RGBA] = 0.0, 0.0, 0.0, 0.8
FLOW_PIN_CONNECTION_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.8
FLOW_PIN_CONNECTION_THICKNESS: Final[float] = 2.0

FLOW_WIRE_SELECTED_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.9
FLOW_WIRE_HOVERING_COLOR: Final[RGBA] = 1.0, 0.49, 0.05, 0.9
FLOW_WIRE_NORMAL_COLOR: Final[RGBA] = 0.75, 0.75, 0.75, 0.8
FLOW_WIRE_SELECTED_THICKNESS: Final[float] = 2.0
FLOW_WIRE_HOVERING_THICKNESS: Final[float] = 2.0
FLOW_WIRE_NORMAL_THICKNESS: Final[float] = 2.0
