import contextlib
with contextlib.redirect_stdout(None):
	import pygame

pygame.init()

class Display:
	window = pygame.display.set_mode((320,240))
	pq = False
	@classmethod
	def tick(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				self.pq = True
	@staticmethod
	def update():
		pygame.display.update()
	@classmethod
	def update_size(cls, size):
		cls.window = pygame.display.set_mode(size)
		cls.window.fill((0,0,0))
	@classmethod
	def pxput(self, coords, colour):
		self.window.set_at(coords, colour)
	@classmethod
	def clear(self):
		self.window.fill((0,0,0))
	@classmethod
	def pollquit(self):
		return self.pq
	@staticmethod
	def quit():
		pygame.quit()
