import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key press."""
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_w or event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

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

def check_events(ai_settings, screen, ship, bullets):
    # Watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    """Update images on screen and flip to the new screen."""
    # Set the background color
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the ship in its current location
    ship.blitme()

    # Make the most recently drawn screen visible
    pygame.display.flip()

