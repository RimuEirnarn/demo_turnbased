"""Bars"""

import pygame

from internal.types import RGB, number
from ..basic_graphics import GREEN, BLACK, WHITE


class Bar:
    """
    Create a bar that can represent progress, health, etc.

    Parameters:
        x, y: Position of the top-left corner
        width, height: Dimensions of the bar
        max_value: Maximum value the bar can represent
        current_value: Current value the bar should show
        color: Color of the filled portion
        bg_color: Color of the background (unfilled portion)
        border_color: Color of the border
        border_width: Width of the border in pixels
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        max_value: number,
        current_value: number,
        color: RGB = GREEN,
        bg_color: RGB = BLACK,
        border_color: RGB = WHITE,
        border_width: int = 2,
    ):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.current_value = current_value
        self.color = color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)

    @property
    def x(self) -> int:
        return self.x

    @property
    def y(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.width

    @property
    def height(self) -> int:
        return self.height

    def update_value(self, new_value):
        """Update the current value of the bar (clamped between 0 and max_value)"""
        self.current_value = max(0, min(new_value, self.max_value))

    def draw(self, surface):
        """Draw the bar on the given surface"""
        # Calculate the filled width based on current value
        filled_width = (self.current_value / self.max_value) * self.width

        # Draw the background (unfilled portion)
        pygame.draw.rect(
            surface, self.bg_color, (self.x, self.y, self.width, self.height)
        )

        # Draw the filled portion
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, filled_width, self.height)
        )

        if self.border_width:
            # Draw the border
            pygame.draw.rect(
                surface,
                self.border_color,
                (self.x, self.y, self.width, self.height),
                self.border_width,
            )
