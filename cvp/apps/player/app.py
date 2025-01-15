# -*- coding: utf-8 -*-

import os
from io import StringIO
from typing import Optional, Tuple
from warnings import catch_warnings

import imgui
import pygame
from OpenGL import GL
from OpenGL.acceleratesupport import ACCELERATE_AVAILABLE
from OpenGL.error import Error
from pygame import NOEVENT, NUMEVENTS
from pygame.event import Event, event_name
from pygame.image import load as load_image
from pygame.key import ScancodeWrapper, get_pressed

from cvp.assets.icons import get_default_icon_path
from cvp.config.sections.proxies.graphic import ForceEglProxy, UseAccelerateProxy
from cvp.context.autofixer import AutoFixer
from cvp.context.context import Context
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.push_style_var import default_style_colors
from cvp.logging.logging import event_logger, logger, msg_logger, profile_logger
from cvp.logging.profile import ProfileLogging
from cvp.msgs.msg import Msg
from cvp.msgs.msg_type import MsgType
from cvp.popups.confirm import ConfirmPopup
from cvp.renderer.renderer import PygameRenderer
from cvp.renderer.window.mapper import WindowMapper
from cvp.renderer.world.world import World
from cvp.windows.canvas import CanvasWindow
from cvp.windows.dtype import DtypeManager
from cvp.windows.files import FilesWindow
from cvp.windows.flow import FlowWindow
from cvp.windows.font import FontManager
from cvp.windows.games.glyph_hack import GlyphHackWindow
from cvp.windows.games.tetrix import TetrixWindow
from cvp.windows.labeling import LabelingWindow
from cvp.windows.layout import LayoutManager
from cvp.windows.media import MediaManager
from cvp.windows.onvif import OnvifManager
from cvp.windows.overlay import OverlayWindow
from cvp.windows.plot import PlotWindow
from cvp.windows.preference import PreferenceManager
from cvp.windows.process import ProcessManager
from cvp.windows.stitching import StitchingWindow
from cvp.windows.terminal import TerminalWindow
from cvp.windows.text import TextWindow
from cvp.windows.toast import ToastWindow
from cvp.windows.window import WindowManager
from cvp.windows.worker import WorkerManager
from cvp.windows.wsd import WsdManager


class PlayerApplication:
    _renderer: PygameRenderer

    def __init__(self, context: Context):
        self._context = context
        self._windows = WindowMapper()
        self._fonts = FontMapper()
        self._profiler = ProfileLogging(profile_logger)
        self._world = World(self._context)

        self._canvas = CanvasWindow(self._context, self._fonts)
        self._dtype_manager = DtypeManager(self._context)
        self._files = FilesWindow(self._context, self._fonts)
        self._flow = FlowWindow(self._context, self._fonts)
        self._font_manager = FontManager(self._context, self._fonts)
        self._glyph_hack = GlyphHackWindow(self._context)
        self._labeling_manager = LabelingWindow(self._context)
        self._layout_manager = LayoutManager(self._context, self._windows)
        self._media_manager = MediaManager(self._context, self._windows)
        self._onvif_manager = OnvifManager(self._context)
        self._overlay = OverlayWindow(self._context)
        self._plot = PlotWindow(self._context)
        self._pref_manager = PreferenceManager(self._context)
        self._process_manager = ProcessManager(self._context)
        self._stitching = StitchingWindow(self._context)
        self._terminal = TerminalWindow(self._context)
        self._tetrix = TetrixWindow(self._context)
        self._text = TextWindow(self._context)
        self._toast = ToastWindow(self._context)
        self._window_manager = WindowManager(self._context, self._windows)
        self._worker_manager = WorkerManager(self._context)
        self._wsd_manager = WsdManager(self._context)

        self._confirm_quit = ConfirmPopup(
            title="Exit",
            label="Are you sure you want to exit?",
            ok="Exit",
            cancel="No",
        )

    @property
    def home(self):
        return self._context.home

    @property
    def config(self):
        return self._context.config

    @property
    def debug(self):
        return self._context.debug

    @property
    def verbose(self):
        return self._context.verbose

    @property
    def pygame_display_size(self) -> Tuple[int, int]:
        assert pygame.display.get_init(), "pygame must be initialized"

        w = self.config.display.width
        h = self.config.display.height
        if w >= 1 and h >= 1:
            return w, h
        else:
            info = pygame.display.Info()
            return info.current_w, info.current_h

    @property
    def pygame_display_flags(self) -> int:
        common_flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self.config.display.fullscreen:
            return common_flags | pygame.FULLSCREEN
        else:
            return common_flags | pygame.RESIZABLE

    def _raise_force_egl_error(self, error: Error) -> None:
        fixer = AutoFixer[Optional[bool], Error](
            context=self._context,
            config_proxy=ForceEglProxy(self.config.graphic),
            config_section_path="graphic.force_egl",
            not_exists_value=None,
            update_value=True,
        )
        fixer.run(error)

    def _validate_accelerate_available(self) -> None:
        if self.config.graphic.use_accelerate is None:
            return

        use_accelerate = self.config.graphic.use_accelerate
        if use_accelerate != ACCELERATE_AVAILABLE:
            raise ValueError(
                f"The set 'use_accelerate' value ({use_accelerate}) "
                f"and 'accelerate_available' value ({ACCELERATE_AVAILABLE}) "
                "must be the same.\n"
                "Calling configuration and environment variables should take "
                "precedence over importing PyOpenGL."
            )

    def _raise_use_accelerate_error(self, error: ValueError) -> None:
        # 'numpy.dtype size changed, may indicate binary incompatibility.
        # Expected 96 from C header, got 88 from PyObject', 1,
        # <OpenGL.platform.baseplatform.glGenTextures object at 0x7b0a5ec96800>
        fixer = AutoFixer[Optional[bool], ValueError](
            context=self._context,
            config_proxy=UseAccelerateProxy(self.config.graphic),
            config_section_path="graphic.use_accelerate",
            not_exists_value=None,
            update_value=False,
        )
        fixer.run(error)

    def start(self) -> None:
        self.on_init()
        try:
            self.on_process()
        except Error as e:
            if str(e) == "Attempt to retrieve context when no valid context":
                self._raise_force_egl_error(e)
            else:
                raise
        finally:
            self.on_exit()

    def on_init(self) -> None:
        if self.debug:
            self._validate_accelerate_available()

        pygame.init()

        icon_path = get_default_icon_path()
        if os.path.isfile(icon_path):
            icon_image = load_image(icon_path)
            pygame.display.set_icon(icon_image)

        try:
            GL.glDeleteTextures(1, GL.glGenTextures(1))
        except ValueError as e:
            self._raise_use_accelerate_error(e)

        size = self.pygame_display_size
        flags = self.pygame_display_flags

        with catch_warnings(record=True) as wms:
            # [Warning]
            # PyGame seems to be running through X11 on top of wayland,
            # instead of wayland directly `pygame.display.set_mode(size, flags)`
            pygame.display.set_mode(size, flags)

            for wm in wms:
                buffer = StringIO()
                if self.verbose >= 1:
                    buffer.write(f"<{wm.category.__name__} ")
                    buffer.write(f"message='{str(wm.message)}' ")
                    buffer.write(f"file={wm.filename}:{wm.lineno}>")
                else:
                    buffer.write(str(wm.message))
                logger.warning(buffer.getvalue())

        imgui.create_context()

        # When the clipboard is empty,
        # calling get_clipboard_text can cause a 'Segmentation Fault'.
        imgui.set_clipboard_text(str())

        io = imgui.get_io()
        io.display_size = size
        io.ini_file_name = None
        io.log_file_name = None
        imgui.load_ini_settings_from_disk(str(self.home.gui_ini))

        self._renderer = PygameRenderer()

        io.fonts.clear()
        normal_text_size_pixels = self.config.font.normal_text_size_pixels
        medium_text_size_pixels = self.config.font.medium_text_size_pixels
        large_text_size_pixels = self.config.font.large_text_size_pixels

        user_font = self.config.font.user_font
        if os.path.isfile(user_font):
            self._fonts.add_normal_ttf(user_font, normal_text_size_pixels)
            self._fonts.add_medium_ttf(user_font, medium_text_size_pixels)
            self._fonts.add_large_ttf(user_font, large_text_size_pixels)
        else:
            self._fonts.add_mixed_normal_text_font(normal_text_size_pixels)
            self._fonts.add_mixed_medium_text_font(medium_text_size_pixels)
            self._fonts.add_mixed_large_text_font(large_text_size_pixels)

        normal_icon_size_pixels = self.config.font.normal_icon_size_pixels
        medium_icon_size_pixels = self.config.font.medium_icon_size_pixels
        large_icon_size_pixels = self.config.font.large_icon_size_pixels
        self._fonts.add_mdi_normal_icon_font(normal_icon_size_pixels)
        self._fonts.add_mdi_medium_icon_font(medium_icon_size_pixels)
        self._fonts.add_mdi_large_icon_font(large_icon_size_pixels)

        io.font_global_scale = self.config.font.scale
        self._renderer.refresh_font_texture()

        theme = self.config.appearance.theme
        default_style_colors(theme)

        GL.glClearColor(0, 0, 0, 1)

        self._world.on_create()
        self._world.on_window_resized(size[0], size[1])

        begin_order = self._context.config.window_manager.begin_order
        self._windows.add_windows(
            self._canvas,
            self._dtype_manager,
            self._files,
            self._flow,
            self._font_manager,
            self._glyph_hack,
            self._labeling_manager,
            self._layout_manager,
            self._media_manager,
            self._onvif_manager,
            self._overlay,
            self._plot,
            self._pref_manager,
            self._process_manager,
            self._stitching,
            self._terminal,
            self._tetrix,
            self._text,
            self._toast,
            self._window_manager,
            self._worker_manager,
            self._wsd_manager,
            begin_order=begin_order,
        )

    def on_exit(self) -> None:
        self._context.teardown_process_manager()
        self._windows.do_destroy()
        self._world.on_destroy()
        self._fonts.close()

        self.config.display.fullscreen = pygame.display.is_fullscreen()
        self.config.display.size = pygame.display.get_window_size()

        self._context.save_config()
        imgui.save_ini_settings_to_disk(str(self.home.gui_ini))

        self._context.save_graphs()

        del self._renderer
        pygame.quit()

    def on_process(self) -> None:
        while not self._context.is_done():
            with self._profiler:
                try:
                    for event in pygame.event.get():
                        self.on_event(event)

                    for msg in self._context.mq.get():
                        self.on_msg(msg)

                    self.on_keyboard_shortcut(get_pressed())
                    self.on_tick()
                    self.on_frame()

                    self.on_next()
                finally:
                    self.on_after()

    def on_after(self) -> None:
        self._renderer.do_after()

    def on_event(self, event: Event) -> None:
        assert NOEVENT < event.type < NUMEVENTS
        event_logger.debug(f"Event {event_name(event.type)}: {event.dict}")

        consumed_event = self._windows.do_event(event)
        if not consumed_event:
            self.on_event_fallback(event)

    def on_event_fallback(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self._confirm_quit.show()
        elif event.type == pygame.DROPBEGIN:
            logger.debug("Drop BEGIN")
        elif event.type == pygame.DROPCOMPLETE:
            logger.debug("Drop COMPLETE")
        elif event.type == pygame.DROPFILE:
            logger.debug(f"Drop FILE: {event.file}")
        elif event.type == pygame.DROPTEXT:
            logger.debug(f"Drop TEXT: {event.text}")
        elif event.type == pygame.WINDOWRESIZED:
            self._world.on_window_resized(event.x, event.y)

        self._renderer.do_event(event)

    def on_msg(self, msg: Msg) -> None:
        name = msg.get_type_name()
        uuid = msg.uuid
        args = msg.as_args()
        msg_logger.debug(f"<Msg {name} {uuid}> {args}")

        consumed_msg = self._windows.do_msg(msg)
        if not consumed_msg:
            self.on_msg_fallback(msg)

    def on_msg_fallback(self, msg: Msg) -> None:
        if msg.mtype == MsgType.toast:
            self._toast.show_simple(msg.message)

    def on_keyboard_shortcut(self, keys: ScancodeWrapper) -> None:
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            self._confirm_quit.show()
        if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_s]:
            self._pref_manager.opened = True

    def on_tick(self) -> None:
        self._renderer.do_tick()

    def on_frame(self) -> None:
        imgui.new_frame()
        try:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.on_main_menu()
            self.on_popups()
            self._windows.do_process()

            if self.debug:
                self.on_metrics_window()
                self.on_style_editor_window()
                self.on_demo_window()

            self._world.on_process(imgui.get_io().delta_time)
        finally:
            # Cannot use `screen.fill((1, 1, 1))` because pygame's screen does not
            # support fill() on OpenGL surfaces
            imgui.render()
            self._renderer.render(imgui.get_draw_data())
            pygame.display.flip()

    def on_next(self) -> None:
        self._windows.do_next()

    def on_file_menu(self) -> None:
        # imgui.separator()
        if imgui.menu_item("Quit", "Ctrl+Q")[0]:
            self._confirm_quit.show()

    def on_tools_menu(self) -> None:
        imgui.menu_item("Computer Vision", None, False, False)
        if imgui.menu_item("Flow", None, self._flow.opened)[0]:
            self._flow.flip_opened()
        if imgui.menu_item("Dtype", None, self._dtype_manager.opened)[0]:
            self._dtype_manager.flip_opened()
        if imgui.menu_item("Stitching", None, self._stitching.opened)[0]:
            self._stitching.flip_opened()
        if imgui.menu_item("Labeling", None, self._labeling_manager.opened)[0]:
            self._labeling_manager.flip_opened()

        imgui.separator()
        imgui.menu_item("Editors", None, False, False)
        if imgui.menu_item("Text", None, self._text.opened)[0]:
            self._text.flip_opened()
        if imgui.menu_item("Canvas", None, self._canvas.opened)[0]:
            self._canvas.flip_opened()

        imgui.separator()
        imgui.menu_item("Network Device", None, False, False)
        if imgui.menu_item("Media", None, self._media_manager.opened)[0]:
            self._media_manager.flip_opened()
        if imgui.menu_item("ONVIF", None, self._onvif_manager.opened)[0]:
            self._onvif_manager.flip_opened()
        if imgui.menu_item("WsDiscovery", None, self._wsd_manager.opened)[0]:
            self._wsd_manager.flip_opened()

        imgui.separator()
        imgui.menu_item("Information", None, False, False)
        if imgui.menu_item("Overlay", None, self._overlay.opened)[0]:
            self._overlay.flip_opened()

        imgui.separator()
        imgui.menu_item("Management", None, False, False)
        if imgui.menu_item("Layout", None, self._layout_manager.opened)[0]:
            self._layout_manager.flip_opened()
        if imgui.menu_item("Process", None, self._process_manager.opened)[0]:
            self._process_manager.flip_opened()
        if imgui.menu_item("Window", None, self._window_manager.opened)[0]:
            self._window_manager.flip_opened()
        if imgui.menu_item("Worker", None, self._worker_manager.opened)[0]:
            self._worker_manager.flip_opened()
        if imgui.menu_item("Files", None, self._files.opened)[0]:
            self._files.flip_opened()

        imgui.separator()
        imgui.menu_item("Development", None, False, False)
        if imgui.menu_item("Terminal", None, self._terminal.opened)[0]:
            self._terminal.flip_opened()

        imgui.separator()
        imgui.menu_item("Game", None, False, False)
        if imgui.menu_item("TetriX", None, self._tetrix.opened)[0]:
            self._tetrix.flip_opened()
        if imgui.menu_item("GlyphWorld", None, self._glyph_hack.opened)[0]:
            self._glyph_hack.flip_opened()

        imgui.separator()
        if imgui.menu_item("Font", None, self._font_manager.opened)[0]:
            self._font_manager.flip_opened()
        if imgui.menu_item("Preference", "Ctrl+Alt+S", self._pref_manager.opened)[0]:
            self._pref_manager.opened = not self._pref_manager.opened

    def on_windows_menu(self) -> None:
        for key, win in self._windows.items():
            if imgui.menu_item(key, None, win.opened)[0]:
                win.opened = not win.opened

        if self.debug:
            imgui.separator()
            if imgui.menu_item("Metrics", None, self.config.developer.show_metrics)[0]:
                self.config.developer.flip_show_metrics()
            if imgui.menu_item("Style", None, self.config.developer.show_style)[0]:
                self.config.developer.flip_show_style()
            if imgui.menu_item("Demo", None, self.config.developer.show_demo)[0]:
                self.config.developer.flip_show_demo()

    def on_main_menu(self) -> None:
        with imgui.begin_main_menu_bar() as main_menu_bar:
            if not main_menu_bar.opened:
                return

            menus = (
                ("File", self.on_file_menu),
                ("Tools", self.on_tools_menu),
                ("Windows", self.on_windows_menu),
            )

            for name, func in menus:
                with imgui.begin_menu(name) as menu:
                    if menu.opened:
                        func()

    def on_popups(self) -> None:
        if self._confirm_quit.do_process():
            self._context.quit()

    def on_metrics_window(self) -> None:
        if not self.config.developer.show_metrics:
            return
        if not imgui.show_metrics_window(True):
            self.config.developer.show_metrics = False

    def on_style_editor_window(self) -> None:
        if not self.config.developer.show_style:
            return
        expanded, opened = imgui.begin("Style editor", True)
        try:
            if not opened:
                self.config.developer.show_style = False
                return
            if not expanded:
                return
            imgui.show_style_editor()
        finally:
            imgui.end()

    def on_demo_window(self) -> None:
        if not self.config.developer.show_demo:
            return
        if not imgui.show_demo_window(True):
            self.config.developer.show_demo = False
