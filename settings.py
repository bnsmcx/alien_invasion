class Settings():
	"""A class to store all settings for Alien Invasion""" 

	def __init__(self):
		"""Initialize the game's settings"""
		# ~ Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (72, 61, 139)

		# ~ ship settings
		self.ship_speed_factor = 1.5
		self.ship_limit = 3

		# ~ bullet settings
		self.bullet_speed_factor = 3
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = 0,0,0
		self.bullets_allowed = 3

		# ~ alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10

		# ~ how quickly the game speeds up
		self.speedup_scale = 1.1
		self.initialize_dynamic_settings()
		
		# ~ how quickly the alien point value increases
		self.score_scale = 1.5


	def initialize_dynamic_settings(self):
		"""initialize settings that change throughout the game"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1

		# ~ fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# ~ scoring
		self.alien_points = 50


	def increase_speed(self):
		"""increase speed settings and alien point values"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)


