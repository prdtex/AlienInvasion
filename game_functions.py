import sys
import pygame

def check_keydown_events(event, ship):
    """Respond to key press."""
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        ship.moving_down = True

def check_keyup_events(event, ship):
    """Respond to key release"""
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ship):
    # Watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship):
    """Update images on screen and flip to the new screen."""
    # Set the background color
    screen.fill(ai_settings.bg_color)

    # Draw the ship in its current location
    ship.blitme()

    # Make the most recently drawn screen visible
    pygame.display.flip()