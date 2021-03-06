import sys
from time import sleep
import pygame

from alien import Alien
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key press."""
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_w or event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key release"""
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_w or event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
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

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Update images on screen and flip to the new screen."""
    # Set the background color
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the ship and alien in its current location
    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible
    pygame.display.flip()

def fire_bullets(ai_settings, screen, ship, bullets):
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()

    # Remove bullets that are off screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens)

def check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens):
    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullets and create a new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_of_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y /(2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_of_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to being hit by alien"""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if a ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if the fleet is at an edge, update positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Look for aliens hitting the bottom
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


