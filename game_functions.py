import sys
import pygame
from time import sleep

from settings import Settings
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
	bullets):
	"""respond to keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
	aliens, bullets, mouse_x, mouse_y):
	"""stat a new game when the player clicks play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# ~ reset the game settings
		ai_settings.initialize_dynamic_settings()

		# ~ hide mouse cursor
		pygame.mouse.set_visible(False)

		# ~ reset the game stats
		stats.reset_stats()
		stats.game_active = True

		# ~ reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		# ~ empty the lists of aliens and bullets
		aliens.empty()
		bullets.empty()

		# ~ create a new fleet and center ship_hit
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""respond to keypresses"""
	if event.type == pygame.KEYDOWN:
		# ~ start ship movement or perform actions
		if event.key == pygame.K_RIGHT:
			ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
	"""fire new bullet if limit not reached yet"""
	# ~ create a new bullet and add it to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def check_keyup_events(event, ship):
	"""respond to keyreleases"""
	if event.type == pygame.KEYUP:
		# ~ stop ship movement
		if event.key == pygame.K_RIGHT:
			ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, sb, aliens, bullets,
	play_button):
	"""update images on the screen and flip to the new screen"""
	# ~ redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	aliens.draw(screen)

	# ~ draw the score information
	sb.show_score()

	# ~ redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	# ~ draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()

	# ~ make the most recently drawn screen visible.
	pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""update position of bullets and delete old bullets"""
	# ~ update position
	bullets.update()

	# ~ get rid of bullets that have vanished
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bulet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets)


def check_bulet_alien_collisions(ai_settings, screen, stats, sb, ship,
	aliens, bullets):
	"""respond to bullet-alien collisions"""
	# ~ remove and bullets and aliens that have collided
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	# ~ adjust score
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

	if len(aliens) == 0:
		# ~ if the entire fleet is destroyed, start a new level
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
	"""determine the number of aliens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
	"""determine the number of rows of aliens that fit on the screen"""
	available_space_y = (ai_settings.screen_height -
		(3 * alien_height ) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""create an alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""check if the fleet is at an edge and then update the positions
	of all aliens in the fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# ~ look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

	# ~ look for aliens hitting the bottom of screensize
	check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
		bullets)


def create_fleet(ai_settings, screen, ship, aliens):
	"""create a full fleet of aliens"""
	# ~ create an alien and find the number of aliens in a row
	# ~ spacing between each alien is equal to one alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)

	# ~ create the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number)


def check_fleet_edges(ai_settings, aliens):
	"""respond appropriately if any aliens have reached the edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	"""drop the entrie fleet and change its direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""respond to ship being hit by alien"""
	if stats.ships_left > 0:
		# ~ decrement ships_left
		stats.ships_left -= 1

		# ~ empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		# ~ create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# ~ pause
		sleep(.5)

		# ~ update scoreboard
		sb.prep_ships()

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
	bullets):
	"""check if any aliens have reached the bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# ~ behave as if the ship was hit
			ship_hit(ai_settings, stats, screen, sb, ship, aliens,
				bullets)
			break


def check_high_score(stats, sb):
	"""check to see if there's a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
