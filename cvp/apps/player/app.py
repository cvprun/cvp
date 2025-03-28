# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from io import StringIO
from typing import Callable, Optional, Tuple
from warnings import catch_warnings

import pygame
from imgui_bundle import imgui
from OpenGL import GL
from OpenGL.acceleratesupport import ACCELERATE_AVAILABLE
from OpenGL.error import Error
from pygame import NOEVENT, NUMEVENTS
from pygame.event import Event, event_name
from pygame.image import load as load_image
from pygame.key import ScancodeWrapper, get_pressed

from cvp.apps.player.modes import create_modes
from cvp.assets.icons import get_default_icon_path
from cvp.config.sections.appearance import AppMode
from cvp.config.sections.proxies.graphic import ForceEglProxy, UseAccelerateProxy
from cvp.context.autofixer import AutoFixer
from cvp.context.context import Context
from cvp.imgui.fonts.defaults import add_mixed_font, add_ttf_file
from cvp.imgui.fonts.font import Font
from cvp.imgui.menu_item_ex import menu_item
from cvp.imgui.separator import separator
from cvp.imgui.theme import DEFAULT_THEME_NAME, apply_theme_with_name
from cvp.logging.logging import event_logger, logger, msg_logger, profile_logger
from cvp.logging.profile import ProfileLogging
from cvp.msgs.msg import Msg
from cvp.msgs.msg_type import MsgType
from cvp.popups.confirm import ConfirmPopup
from cvp.renderer.pygame.renderer import PygameRenderer
from cvp.renderer.world.world import World
from cvp.variables import DEFAULT_FONT_NAME


class PlayerApplication:
    _renderer: Optional[PygameRenderer]
    _font_normal: Optional[Font]

    _prefix_menus: OrderedDict[str, Callable[[], None]]
    _suffix_menus: OrderedDict[str, Callable[[], None]]

    def __init__(self, context: Context):
        self._context = context
        self._profiler = ProfileLogging(profile_logger)
        self._world = World(self._context)

        self._renderer = None
        self._font_normal = None

        self._confirm_quit = ConfirmPopup(
            title="Exit",
            label="Are you sure you want to exit?",
            ok="Exit",
            cancel="No",
        )

        prefix_menus = {"File": self.on_file_menu, "Mode": self.on_mode_menu}
        self._prefix_menus = OrderedDict(prefix_menus)

        suffix_menus = {"Tools": self.on_tools_menu, "Windows": self.on_windows_menu}
        self._suffix_menus = OrderedDict(suffix_menus)

        self._modes = create_modes(self._context)
        self._default_mode = self._modes[AppMode.dashboard]

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
    def mode(self):
        return self._modes.get(self._context.config.appearance.mode, self._default_mode)

    @property
    def renderer(self) -> PygameRenderer:
        assert self._renderer is not None
        return self._renderer

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
        """
        The first entry point that should be called immediately after object creation.
        """

        self.on_init()
        try:
            self.on_main()
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
        logger.info("Initialized all pygame modules.")

        icon_path = get_default_icon_path()
        if os.path.isfile(icon_path):
            icon_image = load_image(icon_path)
            pygame.display.set_icon(icon_image)
            logger.info(f"The program icon has been set: '{icon_path}'")

        try:
            logger.debug("Testing Texture API...")
            GL.glDeleteTextures(1, GL.glGenTextures(1))
        except ValueError as e:
            self._raise_use_accelerate_error(e)

        size = self.pygame_display_size
        flags = self.pygame_display_flags
        depth = 0
        display = 0
        vsync = 0
        logger.info(f"Display size: {size[0]}x{size[1]}")
        logger.info(f"Display flags: {flags}")

        with catch_warnings(record=True) as wms:
            # [Warning]
            # PyGame seems to be running through X11 on top of wayland,
            # instead of wayland directly `pygame.display.set_mode(size, flags)`
            pygame.display.set_mode(size, flags, depth, display, vsync)

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
        logger.info("Created an imgui context.")

        io = imgui.get_io()
        io.config_flags |= imgui.ConfigFlags_.docking_enable.value
        io.display_size = imgui.ImVec2(size[0], size[1])
        io.set_ini_filename(str())
        io.set_log_filename(str())

        # When the clipboard is empty,
        # calling get_clipboard_text can cause a 'Segmentation Fault'.
        imgui.set_clipboard_text(str())

        gui_ini_path = str(self.home.gui_ini)
        imgui.load_ini_settings_from_disk(gui_ini_path)
        logger.info(f"Loaded imgui configuration information: '{gui_ini_path}'")

        self._renderer = PygameRenderer()
        logger.info("Created a Pygame renderer object.")

        io.fonts.clear()
        default_font_pixels = self.config.font.size_pixels
        user_font = self.config.font.user_font
        if os.path.isfile(user_font):
            self._font_normal = add_ttf_file(user_font, default_font_pixels)
            logger.info(f"Create user font: '{user_font}', {default_font_pixels}pixels")
        else:
            self._font_normal = add_mixed_font(DEFAULT_FONT_NAME, default_font_pixels)
            logger.info(f"Create default font: {default_font_pixels}pixels")

        io.font_global_scale = self.config.font.scale
        logger.info(f"Global font scale: {io.font_global_scale}")

        self._renderer.refresh_font_texture()
        logger.info("Refresh font textures.")

        theme_name = self.config.appearance.theme
        apply_theme_with_name(theme_name, default=DEFAULT_THEME_NAME)
        logger.info(f"Apply theme: '{theme_name}'")

        clear_color = self.config.appearance.clear_color
        GL.glClearColor(*clear_color)
        logger.info(f"Apply clear color: {clear_color}")

        self._world.on_create()
        self._world.on_window_resized(size[0], size[1])
        logger.info("Initialized world object.")

    def on_exit(self) -> None:
        self._context.stop_all_flow_runners()
        self._context.teardown_process_manager()
        self._world.on_destroy()

        assert self._font_normal is not None
        self._font_normal.close()

        self.config.display.fullscreen = pygame.display.is_fullscreen()
        self.config.display.size = pygame.display.get_window_size()

        self._context.save_config()
        imgui.save_ini_settings_to_disk(str(self.home.gui_ini))

        self._context.save_graphs()

        assert self._renderer is not None
        del self._renderer

        imgui.destroy_context()
        pygame.quit()

    def on_main(self) -> None:
        while not self._context.is_done():
            with self._profiler:
                for event in pygame.event.get():
                    self.on_event(event)
                for msg in self._context.mq.get():
                    self.on_msg(msg)

                self.on_keyboard(get_pressed())
                self.renderer.do_tick()
                self.on_frame()

    def on_event(self, event: Event) -> None:
        assert NOEVENT < event.type < NUMEVENTS
        event_logger.debug(f"<Event {event_name(event.type)}> {event.dict}")

        consumed_event = self.mode.do_event(event)
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
        self.renderer.do_event(event)

    def on_msg(self, msg: Msg) -> None:
        name = msg.get_type_name()
        uuid = msg.uuid
        args = msg.as_args()
        msg_logger.debug(f"<Msg {name} {uuid}> {args}")

        consumed_msg = self.mode.do_msg(msg)
        if not consumed_msg:
            self.on_msg_fallback(msg)

    def on_msg_fallback(self, msg: Msg) -> None:
        assert self
        if msg.mtype == MsgType.toast:
            pass

    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        """This is where keyboard shortcuts are processed."""

        l_ctrl = keys[pygame.K_LCTRL]
        r_ctrl = keys[pygame.K_RCTRL]
        l_shift = keys[pygame.K_LSHIFT]
        r_shift = keys[pygame.K_RSHIFT]
        l_alt = keys[pygame.K_LALT]
        r_alt = keys[pygame.K_RALT]

        m_ctrl = l_ctrl or r_ctrl
        m_shift = l_shift or r_shift
        m_alt = l_alt or r_alt

        only_ctrl = m_ctrl and not m_shift and not m_alt
        only_shift = not m_ctrl and m_shift and not m_alt  # noqa: F841
        only_alt = not m_ctrl and not m_shift and m_alt

        if only_ctrl and keys[pygame.K_q]:
            self._confirm_quit.show()
            return

        # TODO: You will need to restore it later.
        # if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and keys[pygame.K_s]:
        #     self._pref_manager.opened = True

        if only_alt:
            mode_index: Optional[int] = None
            if keys[pygame.K_1]:
                mode_index = 1
            elif keys[pygame.K_2]:
                mode_index = 2
            elif keys[pygame.K_3]:
                mode_index = 3
            elif keys[pygame.K_4]:
                mode_index = 4
            elif keys[pygame.K_5]:
                mode_index = 5
            elif keys[pygame.K_6]:
                mode_index = 6
            elif keys[pygame.K_7]:
                mode_index = 7
            elif keys[pygame.K_8]:
                mode_index = 8
            elif keys[pygame.K_9]:
                mode_index = 9
            elif keys[pygame.K_0]:
                mode_index = 0

            if mode_index is not None:
                if mode_index < len(self._modes):
                    self.config.appearance.mode = list(self._modes.keys())[mode_index]

        self.mode.on_keyboard(keys)

    def on_frame(self) -> None:
        imgui.new_frame()
        try:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.on_main_menu()
            self.on_popups_process()
            self.mode.do_process()

            if self.debug:
                self.on_metrics_window()
                self.on_style_editor_window()
                self.on_demo_window()

            self._world.on_process(imgui.get_io().delta_time)
        finally:
            # Cannot use `screen.fill((1, 1, 1))` because pygame's screen does not
            # support fill() on OpenGL surfaces
            imgui.render()
            self.renderer.render(imgui.get_draw_data())
            pygame.display.flip()

    def on_file_menu(self) -> None:
        if menu_item("Quit", shortcut="Ctrl+Q"):
            self._confirm_quit.show()

    def on_mode_menu(self) -> None:
        for index, mode in enumerate(self._modes.keys()):
            title = str(mode).capitalize()
            selected = mode == self.config.appearance.mode
            shortcut = f"Alt+{index}" if index <= 9 else str()
            enabled = not selected
            if menu_item(title, selected=selected, shortcut=shortcut, enabled=enabled):
                self.config.appearance.mode = mode

    def on_tools_menu(self) -> None:
        # TODO: You will need to restore it later.
        # menu_item("Computer Vision", enabled=False)
        # if menu_item("Flow", self._flow.opened):
        #     self._flow.flip_opened()
        # if menu_item("Dtype", self._dtype_manager.opened):
        #     self._dtype_manager.flip_opened()
        # if menu_item("Catalog", self._catalog_manager.opened):
        #     self._catalog_manager.flip_opened()
        #
        # if self.debug:
        #     if menu_item("Stitching", self._stitching.opened):
        #         self._stitching.flip_opened()
        #     if menu_item("Labeling", self._labeling_manager.opened):
        #         self._labeling_manager.flip_opened()
        #
        # if self.debug:
        #     separator()
        #     menu_item("Editors", enabled=False)
        #     if menu_item("Text", self._text.opened):
        #         self._text.flip_opened()
        #     if menu_item("Canvas", self._canvas.opened):
        #         self._canvas.flip_opened()
        #
        # separator()
        # menu_item("Network Device", enabled=False)
        # if menu_item("Media", self._media_manager.opened):
        #     self._media_manager.flip_opened()
        # if menu_item("ONVIF", self._onvif_manager.opened):
        #     self._onvif_manager.flip_opened()
        # if menu_item("WsDiscovery", self._wsd_manager.opened):
        #     self._wsd_manager.flip_opened()
        #
        # separator()
        # menu_item("Information", enabled=False)
        # if menu_item("Overlay", self._overlay.opened):
        #     self._overlay.flip_opened()
        #
        # separator()
        # menu_item("Management", enabled=False)
        # if menu_item("Layout", self._layout_manager.opened):
        #     self._layout_manager.flip_opened()
        # if menu_item("Process", self._process_manager.opened):
        #     self._process_manager.flip_opened()
        # if menu_item("Window", self._window_manager.opened):
        #     self._window_manager.flip_opened()
        #
        # if self.debug:
        #     if menu_item("Worker", self._worker_manager.opened):
        #         self._worker_manager.flip_opened()
        #     if menu_item("Files", self._files.opened):
        #         self._files.flip_opened()
        #
        # if self.debug:
        #     separator()
        #     menu_item("Development", enabled=False)
        #     if menu_item("Terminal", self._terminal.opened):
        #         self._terminal.flip_opened()
        #
        # separator()
        # menu_item("Game", enabled=False)
        # if menu_item("TetriX", self._tetrix.opened):
        #     self._tetrix.flip_opened()
        #
        # if self.debug:
        #     if menu_item("GlyphWorld", self._glyph_hack.opened):
        #         self._glyph_hack.flip_opened()
        #
        # separator()
        # if menu_item("Font", self._font_manager.opened):
        #     self._font_manager.flip_opened()
        # if menu_item("Preference", self._pref_manager.opened, shortcut="Ctrl+Alt+S"):
        #     self._pref_manager.opened = not self._pref_manager.opened
        pass

    def on_windows_menu(self) -> None:
        if self.debug:
            separator()
            if menu_item("Metrics", self.config.developer.show_metrics):
                self.config.developer.flip_show_metrics()
            if menu_item("Style", self.config.developer.show_style):
                self.config.developer.flip_show_style()
            if menu_item("Demo", self.config.developer.show_demo):
                self.config.developer.flip_show_demo()

    def on_main_menu(self) -> None:
        if imgui.begin_main_menu_bar():
            try:
                for name, func in self._prefix_menus.items():
                    if imgui.begin_menu(name):
                        try:
                            func()
                        finally:
                            imgui.end_menu()

                self.mode.on_main_menu()

                for name, func in self._suffix_menus.items():
                    if imgui.begin_menu(name):
                        try:
                            func()
                        finally:
                            imgui.end_menu()
            finally:
                imgui.end_main_menu_bar()

    def on_popups_process(self) -> None:
        """Where to render the popup object."""

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
