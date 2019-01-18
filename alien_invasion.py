import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
	# ~ initialize game and create a screen
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	# ~ create an instance to store our game stats and create a scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	# ~ make the play button
	play_button = Button(ai_settings, screen, "Play")

	# ~ make a ship, a group of bullets, and a group of aliens
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()

	# ~ create a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)


	while True:
		# ~ start the main loop for the game
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
		aliens, bullets)

		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship,
				aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
				bullets)

		gf.update_screen(ai_settings, screen, stats, ship, sb, aliens,
			bullets, play_button)


run_game()
