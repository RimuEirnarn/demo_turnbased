"""Button"""

# pylint: disable=no-member

from typing import Callable
import pygame
from ..types import RGB


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        color: RGB = (0, 0, 0),
        hover_color: RGB = (0, 0, 0),
        text_color: RGB = (0, 0, 0),
        border_color: RGB = (0, 0, 0),
        border_width: int = 2,
        callback: Callable | None = None,
        font_size: int = 24,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.font = pygame.font.SysFont(None, font_size)
        self._clicked = False
        self._hovered = False
        self.border_color = border_color
        self.border_width = border_width
        self._active = False
        self._event_key = None
        self._disabled = False

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, matter: bool):
        self._disabled = matter

    def draw(self, surface: pygame.Surface):
        """Draw button"""
        color = self.hover_color if self._hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    @property
    def hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        self._hovered = self.rect.collidepoint(mouse_pos)
        return self._hovered

    def update(self, event_list: list[pygame.event.Event]):
        self._clicked = False
        mouse_pos = pygame.mouse.get_pos()
        self._hovered = self.rect.collidepoint(mouse_pos)

        for event in event_list:
            self.on_event(event)

    def click(self):
        self._clicked = True
        if self.callback:
            self.callback()

    def release(self):
        self._active = False

    def onclick(self):
        if self.hovered and self._active:
            self.click()
        self._active = False

    def on_event(
        self,
        event: pygame.event.Event,
        button_type: int = 1,
    ):
        if self.disabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == button_type:
            hovered = self.rect.collidepoint(event.pos)
            if hovered:
                self._active = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == button_type:
            hovered = self.rect.collidepoint(event.pos)
            if not hovered and not self._active:
                return
            self._clicked = True
            if self.callback:
                self.callback()
            self._active = False

    def on_keyevent(self,
                    event: pygame.event.Event):
        if self.disabled:
            return
        if self._event_key is None:
            raise TypeError("Cannot use keyevent when this button is not registered to a key")

        if event.type == pygame.KEYDOWN and event.key == self._event_key:
            self._active = True

        if event.type == pygame.KEYUP and event.key == self._event_key:
            if not self._active:
                return
            self._clicked = True
            if self.callback:
                self.callback()
            self._active = False

    def register_key(self, key_type: int):
        self._event_key = key_type

    @property
    def clicked(self):
        """Return True if this button is clicked"""
        if self._clicked:
            self._clicked = False
            return True
        return False
