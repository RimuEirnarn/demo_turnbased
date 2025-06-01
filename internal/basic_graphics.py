"""Basic graphics"""
import pygame

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
    (1366, 768)
]
DISPLAY = RESOLUTIONS[-2]


pygame.init() # pylint: disable=no-member
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption(APP_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)


def log_action(value: str, dest: tuple[int, int]):
    """Log actions"""
    # print(value)
    text = font.render(value, True, WHITE)
    screen.blit(text, dest=dest)
