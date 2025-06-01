# pylint: disable=all
import pygame
import sys
import os.path

sys.path.append(os.path.abspath("./"))
from internal.basic_graphics import anchored_position
from internal.utils import EventState
from internal.gui.button import Button
from internal.gui.bars import Bar

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen_size = screen_width, screen_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Bar System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Create some example bars
health_bar = Bar(50, 50, 200, 30, 100, 100, RED)
mana_bar = Bar(50, 100, 200, 30, 100, 75, BLUE)
progress_bar = Bar(50, 150, 400, 20, 1, 0, YELLOW)  # For tasks that complete (0-1)

rect0 = pygame.Rect(0, 0, 100, 10)
rect0.bottomleft = (10, screen_height - 30)
overlay = Bar(
    rect0.x - 2,
    rect0.y - 2,
    rect0.width + 4,
    rect0.height + 4,
    max_value=100,
    current_value=0,
    color=WHITE,
    border_width=0,
)
some_bar = Bar(
    rect0.x, rect0.y, rect0.width, rect0.height, 100, 0, BLUE, border_width=0
)

button0 = Button(
    *anchored_position("bottomright", 300, 50, screen_size),
    width=200,
    height=50,
    text="Click me",
    text_color=WHITE
)
button1 = Button(
    *anchored_position("bottomright", 300, 400, screen_size),
    width=200,
    height=50,
    text="Click me (Callback)",
    text_color=WHITE,
    callback=lambda: print("Hello, World from Callback")
)

button0.register_key(pygame.K_1)
button1.register_key(pygame.K_2)
# Main game loop
clock = pygame.time.Clock()
running = EventState(True)

# For demonstration - will increment progress bar
progress = 0

hp_v = overlay_v = 0

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running.set(False)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # Decrease health by 10 when '1' is pressed
                health_bar.update_value(health_bar.current_value - 10)
            elif event.key == pygame.K_2:
                # Increase health by 10 when '2' is pressed
                health_bar.update_value(health_bar.current_value + 10)
            elif event.key == pygame.K_q:
                running.set(False)
                continue
        button0.on_keyevent(event)
        button1.on_keyevent(event)
        button0.on_event(event)
        button1.on_event(event)

    # button0.update(events)
    # button1.update(events)

    if button0.clicked:
        print("First button clicked")

    # Update progress bar for demonstration
    progress += 0.001
    if progress > 1:
        progress = 0
    progress_bar.update_value(progress)

    overlay_v += 1
    hp_v += 0.5
    if overlay_v > 100:
        overlay_v = 0
    if hp_v > 100:
        hp_v = 0
    overlay.update_value(overlay_v)
    some_bar.update_value(hp_v)

    # Fill the screen
    screen.fill((50, 50, 50))

    # Draw the bars
    health_bar.draw(screen)
    mana_bar.draw(screen)
    progress_bar.draw(screen)

    overlay.draw(screen)
    some_bar.draw(screen)

    button0.draw(screen)
    button1.draw(screen)

    # Add some labels for clarity
    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Health", True, WHITE), (50, 30))
    screen.blit(font.render("Mana", True, WHITE), (50, 80))
    screen.blit(font.render("Progress", True, WHITE), (50, 130))
    screen.blit(
        font.render("Press 1/2 to decrease/increase health", True, WHITE), (300, 50)
    )
    screen.blit(
        font.render("HP/Shield", True, WHITE),
        anchored_position("bottomleft", 20, 70, (screen_width, screen_height)),
    )

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
