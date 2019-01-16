import pygame

class Ship():
	"""Initialize the ship and set it's starting position""" 

	def __init__(self, ai_settings, screen):
		self.screen = screen
		self.ai_settings = ai_settings

		# ~ load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# ~ start each new ship at the bottom center of screensize
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# ~ store a decimal value for the ship's center
		self.center = float(self.rect.centerx)

		# ~ movement flag
		self.moving_right = False
		self.moving_left = False


	def update(self):
		"""update the ship's position based on movement flags"""
		# ~ update the ship's ceenter value, not the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		# ~ update rect object from self.center
		self.rect.centerx = self.center


	def center_ship(self):
		"""center the ship on the bottom of the screen"""
		self.center = self.screen_rect.centerx


	def blitme(self):
		"""draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)
