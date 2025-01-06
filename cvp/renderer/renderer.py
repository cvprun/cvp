# -*- coding: utf-8 -*-

from typing import Callable, Dict

import imgui
import pygame
from imgui.integrations.opengl import FixedPipelineRenderer
from pygame.event import Event
from pygame.time import get_ticks

from cvp.logging.logging import logger
from cvp.renderer.remapper import KeycodeRemapper


class PygameRenderer(FixedPipelineRenderer):
    _events: Dict[int, Callable[[Event], bool]]

    def __init__(self):
        super().__init__()

        self._running_seconds = 0.0
        self._remapper = KeycodeRemapper()

        kmap = self.io.key_map
        kmap[imgui.KEY_TAB] = self._remapper(pygame.K_TAB)
        kmap[imgui.KEY_LEFT_ARROW] = self._remapper(pygame.K_LEFT)
        kmap[imgui.KEY_RIGHT_ARROW] = self._remapper(pygame.K_RIGHT)
        kmap[imgui.KEY_UP_ARROW] = self._remapper(pygame.K_UP)
        kmap[imgui.KEY_DOWN_ARROW] = self._remapper(pygame.K_DOWN)
        kmap[imgui.KEY_PAGE_UP] = self._remapper(pygame.K_PAGEUP)
        kmap[imgui.KEY_PAGE_DOWN] = self._remapper(pygame.K_PAGEDOWN)
        kmap[imgui.KEY_HOME] = self._remapper(pygame.K_HOME)
        kmap[imgui.KEY_END] = self._remapper(pygame.K_END)
        kmap[imgui.KEY_INSERT] = self._remapper(pygame.K_INSERT)
        kmap[imgui.KEY_DELETE] = self._remapper(pygame.K_DELETE)
        kmap[imgui.KEY_BACKSPACE] = self._remapper(pygame.K_BACKSPACE)
        kmap[imgui.KEY_SPACE] = self._remapper(pygame.K_SPACE)
        kmap[imgui.KEY_ENTER] = self._remapper(pygame.K_RETURN)
        kmap[imgui.KEY_ESCAPE] = self._remapper(pygame.K_ESCAPE)
        kmap[imgui.KEY_PAD_ENTER] = self._remapper(pygame.K_KP_ENTER)
        kmap[imgui.KEY_A] = self._remapper(pygame.K_a)
        kmap[imgui.KEY_C] = self._remapper(pygame.K_c)
        kmap[imgui.KEY_V] = self._remapper(pygame.K_v)
        kmap[imgui.KEY_X] = self._remapper(pygame.K_x)
        kmap[imgui.KEY_Y] = self._remapper(pygame.K_y)
        kmap[imgui.KEY_Z] = self._remapper(pygame.K_z)

        self._events = dict()
        self._events[pygame.MOUSEMOTION] = self.on_mouse_motion
        self._events[pygame.MOUSEBUTTONDOWN] = self.on_mouse_button_down
        self._events[pygame.MOUSEBUTTONUP] = self.on_mouse_button_up
        self._events[pygame.KEYDOWN] = self.on_key_down
        self._events[pygame.KEYUP] = self.on_key_up
        self._events[pygame.WINDOWRESIZED] = self.on_window_resized
        self._clipboard_copy = False

    @property
    def running_seconds(self):
        return self._running_seconds

    def on_mouse_motion(self, event: Event) -> bool:
        self.io.mouse_pos = event.pos
        return True

    def on_mouse_button_down(self, event: Event) -> bool:
        if event.button == pygame.BUTTON_LEFT:
            self.io.mouse_down[imgui.MOUSE_BUTTON_LEFT] = 1
        elif event.button == pygame.BUTTON_RIGHT:
            self.io.mouse_down[imgui.MOUSE_BUTTON_RIGHT] = 1
        elif event.button == pygame.BUTTON_MIDDLE:
            self.io.mouse_down[imgui.MOUSE_BUTTON_MIDDLE] = 1
        return True

    def on_mouse_button_up(self, event: Event) -> bool:
        if event.button == pygame.BUTTON_LEFT:
            self.io.mouse_down[imgui.MOUSE_BUTTON_LEFT] = 0
        elif event.button == pygame.BUTTON_RIGHT:
            self.io.mouse_down[imgui.MOUSE_BUTTON_RIGHT] = 0
        elif event.button == pygame.BUTTON_MIDDLE:
            self.io.mouse_down[imgui.MOUSE_BUTTON_MIDDLE] = 0
        elif event.button == pygame.BUTTON_WHEELUP:
            self.io.mouse_wheel = 0.5
        elif event.button == pygame.BUTTON_WHEELDOWN:
            self.io.mouse_wheel = -0.5
        return True

    def update_key_state(self, pygame_keycode: int, state: bool) -> None:
        self.io.keys_down[self._remapper(pygame_keycode)] = state

        if pygame_keycode in (pygame.K_LCTRL, pygame.K_RCTRL):
            l_ctrl = self.io.keys_down[self._remapper.l_ctrl]
            r_ctrl = self.io.keys_down[self._remapper.r_ctrl]
            self.io.key_ctrl = bool(l_ctrl or r_ctrl)
        elif pygame_keycode in (pygame.K_LALT, pygame.K_RALT):
            l_alt = self.io.keys_down[self._remapper.l_alt]
            r_alt = self.io.keys_down[self._remapper.r_alt]
            self.io.key_alt = bool(l_alt or r_alt)
        elif pygame_keycode in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            l_shift = self.io.keys_down[self._remapper.l_shift]
            r_shift = self.io.keys_down[self._remapper.r_shift]
            self.io.key_shift = bool(l_shift or r_shift)
        elif pygame_keycode in (pygame.K_LSUPER, pygame.K_RSUPER):
            l_super = self.io.keys_down[self._remapper.l_super]
            r_super = self.io.keys_down[self._remapper.r_super]
            self.io.key_super = bool(l_super or r_super)

        if self.io.key_ctrl and pygame_keycode == pygame.K_v and state:
            imgui.set_clipboard_text(pygame.scrap.get_text())

    @staticmethod
    def is_copy_shortcut_pressed() -> bool:
        keys = pygame.key.get_pressed()
        any_ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        any_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        any_alt = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        any_copy = keys[pygame.K_c] or keys[pygame.K_x]
        return any_ctrl and not any_shift and not any_alt and any_copy

    def on_key_down(self, event: Event) -> bool:
        for char in event.unicode:
            code = ord(char)
            if 0 < code < 0x10000:
                self.io.add_input_character(code)

        self.update_key_state(event.key, True)

        if self.is_copy_shortcut_pressed():
            self._clipboard_copy = True

        return True

    def on_key_up(self, event: Event) -> bool:
        self.update_key_state(event.key, False)
        return True

    def on_window_resized(self, event: Event) -> bool:
        # existing font texture is no longer valid, so we need to refresh it
        self.refresh_font_texture()
        self.io.display_size = event.x, event.y
        return True

    def do_after(self) -> None:
        if not self._clipboard_copy:
            return

        self._clipboard_copy = False
        clipboard_text = imgui.get_clipboard_text()
        logger.debug(f"Pygame scrap put text: '{clipboard_text}'")
        pygame.scrap.put_text(clipboard_text)

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
