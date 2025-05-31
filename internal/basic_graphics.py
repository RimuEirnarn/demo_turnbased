"""Basic graphics"""
import pygame

APP_TITLE = "Turn-based Demo"
DISPLAY = (800, 600)


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
