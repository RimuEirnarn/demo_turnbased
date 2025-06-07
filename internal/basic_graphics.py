"""Basic graphics"""

import pygame

from internal.types import AnchorEnum, Coords, Size

APP_TITLE = "Turn-based Demo"
RESOLUTIONS = [
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
    (1680, 1050),
    (1920, 1200),
    (1024, 768),
    (1280, 960),
    (2560, 1080),
    (3440, 1440),
    (1280, 720),
    (1600, 900),
    (1366, 768),
]
DISPLAY = RESOLUTIONS[-2]

pygame.init()  # pylint: disable=no-member
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption(APP_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

COMMON_ACTION_DEST = (440, 50)
COMMON_CRIT_DEST = (440, 75)


def log_action(value: str, dest: Coords):
    """Log actions"""
    # print(value)
    text = font.render(value, True, WHITE)
    screen.blit(text, dest=dest)


def anchored_position(
    anchor: AnchorEnum, offset_x: int = 0, offset_y: int = 0, screen_size: Size = (0, 0)
) -> Coords:
    """Anchor position relative from screen"""
    if anchor == "topleft":
        return (offset_x, offset_y)
    elif anchor == "topright":
        return (screen_size[0] - offset_x, offset_y)
    elif anchor == "bottomleft":
        return (offset_x, screen_size[1] - offset_y)
    elif anchor == "bottomright":
        return (screen_size[0] - offset_x, screen_size[1] - offset_y)
    else:  # Default to center
        return (screen_size[0] // 2 + offset_x, screen_size[1] // 2 + offset_y)
