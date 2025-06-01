"""Bars"""

import pygame
from ..basic_graphics import screen, GREEN, BLACK, WHITE


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
        x,
        y,
        width,
        height,
        max_value,
        current_value,
        color=GREEN,
        bg_color=BLACK,
        border_color=WHITE,
        border_width=2,
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

        # Draw the border
        pygame.draw.rect(
            surface,
            self.border_color,
            (self.x, self.y, self.width, self.height),
            self.border_width,
        )
