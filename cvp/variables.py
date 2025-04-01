# -*- coding: utf-8 -*-

from typing import Final

from cvp.types.colors import RGBA
from cvp.types.shapes import Size

CVP_HOME_DIRNAME: Final[str] = ".cvp"
CVP_YML_FILENAME: Final[str] = "cvp.yml"
CVP_EXTENSION: Final[str] = ".cvp"
CVP_ROOT_INFO_FILENAME: Final[str] = "info.yml"
GUI_INI_FILENAME: Final[str] = "gui.ini"
LOGGING_JSON_FILENAME: Final[str] = "logging.json"

NOT_FOUND_INDEX: Final[int] = -1
FULL_WIDTH: Final[float] = -1.0
FULL_HEIGHT: Final[float] = -1.0
FULL_SIZE: Final[Size] = FULL_WIDTH, FULL_HEIGHT

DEFAULT_FONT_SIZE: Final[int] = 14
DEFAULT_FONT_SCALE: Final[float] = 1.0
DEFAULT_FONT_NAME: Final[str] = "Default"

CONFIG_VALUE_SEPARATOR: Final[str] = ","
CHECKSUM_DELIMITER: Final[str] = ":"

NODOC: Final[str] = str()

MODULE_PATH_SEPARATOR: Final[str] = "."

CODEPOINT_RANGES_EXTENSION: Final[str] = ".ranges"
CODEPOINT_GLYPHS_EXTENSION: Final[str] = ".glyphs"
KEYRING_EXTENSION: Final[str] = ".cfg"

LOCAL_DOTENV_FILENAME: Final[str] = ".env.local"

MAX_THREAD_WORKERS: Final[int] = 5
MAX_PROCESS_WORKERS: Final[int] = 5

THREAD_POOL_PREFIX: Final[str] = "cvp.threadpool"

ASCII_RANGE: Final[int] = 127
MAX_IMGUI_KEYCODE: Final[int] = 512

MOUSE_WHEEL_OFFSET_SCALE: Final[float] = 0.5

LOGGING_STEP: Final[int] = 1000
SLOW_CALLBACK_DURATION: Final[float] = 0.05

DEFAULT_MENU_LABEL: Final[str] = "Manu"
DEFAULT_MAIN_LABEL: Final[str] = "Main"
DEFAULT_MENU_WIDTH: Final[float] = 150.0

DEFAULT_OLLAMA_ADDRESS: Final[str] = "http://localhost:11434/"
DEFAULT_SUPABASE_ADDRESS: Final[str] = "http://localhost:8000/"

MIN_SIDEBAR_WIDTH: Final[float] = 160.0
MAX_SIDEBAR_WIDTH: Final[float] = 480.0

MIN_SIDEBAR_HEIGHT: Final[float] = 160.0
MAX_SIDEBAR_HEIGHT: Final[float] = 480.0

MIN_WINDOW_WIDTH: Final[int] = 400
MIN_WINDOW_HEIGHT: Final[int] = 300

API_SELECT_WIDTH: Final[float] = 180.0
MIN_API_SELECT_WIDTH: Final[float] = 100.0
MAX_API_SELECT_WIDTH: Final[float] = 300.0

MIN_POPUP_WIDTH: Final[int] = 120
MIN_POPUP_HEIGHT: Final[int] = 50
MIN_POPUP_CONFIRM_WIDTH: Final[int] = 280
MIN_POPUP_CONFIRM_HEIGHT: Final[int] = 80
MIN_POPUP_VARIABLE_WIDTH: Final[int] = 360
MIN_POPUP_VARIABLE_HEIGHT: Final[int] = 240
MIN_POPUP_TEXT_INPUT_WIDTH: Final[int] = 200
MIN_POPUP_TEXT_INPUT_HEIGHT: Final[int] = 120
MIN_POPUP_OPEN_FILE_WIDTH: Final[int] = 480
MIN_POPUP_OPEN_FILE_HEIGHT: Final[int] = 380

AUI_PADDING_WIDTH: Final[float] = 8.0
AUI_PADDING_HEIGHT: Final[float] = 8.0

PROCESS_TEARDOWN_TIMEOUT: Final[float] = 2.0

STREAM_LOGGING_MAXSIZE: Final[int] = 65536
STREAM_LOGGING_NEWLINE_SIZE: Final[int] = 88

WSD_IPV4_MULTICAST_ADDRESS: Final[str] = "239.255.255.250"
WSD_IPV6_MULTICAST_ADDRESS: Final[str] = "ff02::c"
WSD_PORT_NUMBER: Final[int] = 3702
WSD_TIMEOUT: Final[float] = 30.0
WSD_NAME_DEFAULT: Final[str] = "New Device"

ZEEP_ELEMENT_SEPARATOR: Final[str] = "."

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

CANVAS_AXIS_VISIBLE: Final[bool] = True
CANVAS_AXIS_THICKNESS: Final[float] = 1.0
CANVAS_AXIS_COLOR: Final[RGBA] = 1.0, 0.0, 0.0, 0.6

CANVAS_GRID_VISIBLE: Final[bool] = True
CANVAS_GRID_STEP: Final[float] = 50.0
CANVAS_GRID_THICKNESS: Final[float] = 1.0
CANVAS_GRID_COLOR: Final[RGBA] = 0.8, 0.8, 0.8, 0.2

CANVAS_ROI_COLOR: Final[RGBA] = 0.0, 0.0, 1.0, 0.3
CANVAS_ROI_ROUNDING: Final[float] = 0.0
CANVAS_ROI_THICKNESS: Final[float] = 2.0

FLOW_EXTENSION: Final[str] = ".flow.cvp"
FLOW_PATH_SEPARATOR: Final[str] = "."
FLOW_PATH_ENCODING: Final[str] = "utf-8"

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
FLOW_WIRE_HOVERING_TOLERANCE: Final[float] = 6.0
