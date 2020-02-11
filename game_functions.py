import sys
import pygame

def check_keydown_events(event, ship):
    """Respond to key press."""
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            ship.moving_left = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                ship.moving_up = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    ship.moving_down = True

def check_keyup_events(event, ship):
    """Respond to key release"""
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            ship.moving_left = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                ship.moving_up = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
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