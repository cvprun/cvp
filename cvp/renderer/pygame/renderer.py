# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Optional

import pygame
from imgui_bundle import imgui
from pygame.event import Event
from pygame.time import get_ticks

from cvp.ime.manager import ImeManager
from cvp.logging.logging import renderer_logger as logger
from cvp.renderer.opengl.fixed import FixedPipelineRenderer
from cvp.renderer.pygame.keycode.imgui_bundle import ImguiBundleKeycodeRemapper
from cvp.unicode.planes import BMP
from cvp.variables import BACKSPACE_CODEPOINT, MOUSE_WHEEL_OFFSET_SCALE, NULL_CODEPOINT


class PygameRenderer(FixedPipelineRenderer):
    _events: Dict[int, Callable[[Event], bool]]

    def __init__(self, *, imes: Optional[ImeManager] = None):
        super().__init__()

        display_info = pygame.display.Info()
        assert display_info.current_w == self.io.display_size.x
        assert display_info.current_h == self.io.display_size.y

        def get_clipboard_text(_imgui_context: Any) -> str:
            text = pygame.scrap.get_text()
            logger.debug(f"Pygame scrap get text: '{text}'")
            return text

        def set_clipboard_text(_imgui_context: Any, text: str) -> None:
            logger.debug(f"Pygame scrap put text: '{text}'")
            pygame.scrap.put_text(text)

        imgui.get_platform_io().platform_get_clipboard_text_fn = get_clipboard_text
        imgui.get_platform_io().platform_set_clipboard_text_fn = set_clipboard_text

        self._running_seconds = 0.0
        self._mouse_wheel_scale = MOUSE_WHEEL_OFFSET_SCALE
        self._remapper = ImguiBundleKeycodeRemapper()
        self._imes = imes if imes else ImeManager.from_default()
        self._events = {
            pygame.MOUSEMOTION: self.on_mouse_motion,
            pygame.MOUSEBUTTONDOWN: self.on_mouse_button_down,
            pygame.MOUSEBUTTONUP: self.on_mouse_button_up,
            pygame.KEYDOWN: self.on_key_down,
            pygame.KEYUP: self.on_key_up,
            pygame.WINDOWRESIZED: self.on_window_resized,
            pygame.JOYBUTTONDOWN: self.on_joy_button_down,
            pygame.JOYBUTTONUP: self.on_joy_button_up,
            pygame.TEXTEDITING: self.on_text_editing,
            pygame.TEXTINPUT: self.on_text_input,
        }

    @property
    def running_seconds(self):
        return self._running_seconds

    def on_mouse_motion(self, event: Event) -> bool:
        assert isinstance(event.pos, tuple)
        assert 2 == len(event.pos)
        self.io.mouse_pos = imgui.ImVec2(event.pos[0], event.pos[1])
        return True

    def on_mouse_button_down(self, event: Event) -> bool:
        if event.button == pygame.BUTTON_LEFT:
            self.io.add_mouse_button_event(imgui.MouseButton_.left.value, down=True)
        elif event.button == pygame.BUTTON_RIGHT:
            self.io.add_mouse_button_event(imgui.MouseButton_.right.value, down=True)
        elif event.button == pygame.BUTTON_MIDDLE:
            self.io.add_mouse_button_event(imgui.MouseButton_.middle.value, down=True)
        return True

    def on_mouse_button_up(self, event: Event) -> bool:
        if event.button == pygame.BUTTON_LEFT:
            self.io.add_mouse_button_event(imgui.MouseButton_.left.value, down=False)
        elif event.button == pygame.BUTTON_RIGHT:
            self.io.add_mouse_button_event(imgui.MouseButton_.right.value, down=False)
        elif event.button == pygame.BUTTON_MIDDLE:
            self.io.add_mouse_button_event(imgui.MouseButton_.middle.value, down=False)
        elif event.button == pygame.BUTTON_WHEELUP:
            self.io.add_mouse_wheel_event(0, +1 * self._mouse_wheel_scale)
        elif event.button == pygame.BUTTON_WHEELDOWN:
            self.io.add_mouse_wheel_event(0, -1 * self._mouse_wheel_scale)
        return True

    def update_key_state(self, pygame_keycode: int, down: bool) -> None:
        try:
            imgui_key_value = self._remapper(pygame_keycode)
        except KeyError:
            return

        imgui_keycode = imgui.Key(imgui_key_value)
        self.io.add_key_event(imgui_keycode, down=down)

        if pygame_keycode in (pygame.K_LCTRL, pygame.K_RCTRL):
            self.io.add_key_event(imgui.Key.mod_ctrl, down=down)
        elif pygame_keycode in (pygame.K_LALT, pygame.K_RALT):
            self.io.add_key_event(imgui.Key.mod_alt, down=down)
        elif pygame_keycode in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.io.add_key_event(imgui.Key.mod_shift, down=down)
        elif pygame_keycode in (pygame.K_LSUPER, pygame.K_RSUPER):
            self.io.add_key_event(imgui.Key.mod_super, down=down)

    def update_joy_state(self, pygame_joy_button: int, down: bool) -> None:
        if pygame_joy_button == pygame.CONTROLLER_BUTTON_A:
            self.io.add_key_event(imgui.Key.gamepad_face_down, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_B:
            self.io.add_key_event(imgui.Key.gamepad_face_right, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_X:
            self.io.add_key_event(imgui.Key.gamepad_face_left, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_Y:
            self.io.add_key_event(imgui.Key.gamepad_face_up, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_DPAD_UP:
            self.io.add_key_event(imgui.Key.gamepad_dpad_up, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_DPAD_DOWN:
            self.io.add_key_event(imgui.Key.gamepad_dpad_down, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
            self.io.add_key_event(imgui.Key.gamepad_dpad_left, down=down)
        elif pygame_joy_button == pygame.CONTROLLER_BUTTON_DPAD_RIGHT:
            self.io.add_key_event(imgui.Key.gamepad_dpad_right, down=down)

    @staticmethod
    def is_copy_shortcut_pressed() -> bool:
        keys = pygame.key.get_pressed()
        any_ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        any_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        any_alt = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        any_copy = keys[pygame.K_c] or keys[pygame.K_x]
        return any_ctrl and not any_shift and not any_alt and any_copy

    def on_key_down(self, event: Event) -> bool:
        if event.key == pygame.K_RALT:
            return True

        for char in event.unicode:
            codepoint = ord(char)

            if codepoint == NULL_CODEPOINT:
                continue
            if not BMP.contain(codepoint):
                continue

            if codepoint == BACKSPACE_CODEPOINT:
                if self._imes.has_composing():
                    self._imes.pop_text()
                    return True
                else:
                    self.io.add_input_character(codepoint)
            else:
                for c in self._imes.add_text(char):
                    self.io.add_input_character(ord(c))

        self.update_key_state(event.key, down=True)
        return True

    def on_key_up(self, event: Event) -> bool:
        if event.key == pygame.K_RALT:
            for c in self._imes.flush_text():
                self.io.add_input_character(ord(c))
            self._imes.change_next_mode()
            logger.debug(f"Change IME Mode: '{str(self._imes.mode)}'")
            return True

        self.update_key_state(event.key, down=False)
        return True

    def on_window_resized(self, event: Event) -> bool:
        # surface = pygame.display.get_surface()
        # NOTE: pygame does not modify existing surface upon resize,
        #       we need to do it ourselves.
        # pygame.display.set_mode((event.w, event.h), flags=surface.get_flags())

        # existing font texture is no longer valid, so we need to refresh it
        self.refresh_font_texture()

        self.io.display_size = imgui.ImVec2(event.x, event.y)
        # self.io.display_framebuffer_scale = imgui.ImVec2(1, 1)

        # delete old surface, it is no longer needed
        # del surface

        return True

    def on_joy_button_down(self, event: Event) -> bool:
        self.update_joy_state(event.button, down=True)
        return True

    def on_joy_button_up(self, event: Event) -> bool:
        self.update_joy_state(event.button, down=False)
        return True

    def on_text_editing(self, event: Event) -> bool:
        assert isinstance(event.text, str)
        assert isinstance(event.start, int)
        assert isinstance(event.length, int)
        assert self.io is not None
        # The 'TEXT_EDITING' event is no longer supported.
        return True

    def on_text_input(self, event: Event) -> bool:
        assert isinstance(event.text, str)
        assert self.io is not None
        # The 'TEXT_INPUT' event is no longer supported.
        return True

    def do_event(self, event: Event) -> bool:
        if event.type in self._events:
            return self._events[event.type](event)
        else:
            return False

    def do_tick(self):
        current_seconds = get_ticks() / 1000.0
        delta = current_seconds - self._running_seconds
        self.io.delta_time = delta if delta > 0.0 else 0.001
        self._running_seconds = current_seconds
