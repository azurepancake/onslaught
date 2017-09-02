from helpers import *

class Game(object):
	def __init__(self, width = 400, height = 600):
		pygame.init()
		self.width = width
		self.height = height
		self.framerate = 60
		self.screen = pygame.display.set_mode((self.width, self.height))

	def loadSprites(self):
		global laserSprites
		self.player = Player(self.width, self.height)
		self.playerSprites = pygame.sprite.RenderPlain((self.player))
		laserSprites = pygame.sprite.RenderPlain()

	def getEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

	def draw(self):
		self.screen.fill((0, 0, 0))
		self.playerSprites.draw(self.screen)
		self.playerSprites.update()
		laserSprites.draw(self.screen)
		laserSprites.update()
		pygame.display.flip()

	def mainLoop(self):
		self.clock = pygame.time.Clock()
		self.loadSprites()
		while 1:
			self.clock.tick(self.framerate)
			self.getEvents()
			self.draw()

class Player(pygame.sprite.Sprite):
	def __init__(self, screenWidth, screenHeight):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage('ship1.bmp')
		self.rect.centerx = 200
		self.rect.centery = 535
		self.velocity = 3
		self.laserTimer = 9
		self.laserSpeed = 10
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

	def update(self):
		key = pygame.key.get_pressed()
		if key[K_UP]:
			self.rect.centery += -self.velocity
		if key[K_DOWN]:
			self.rect.centery += self.velocity
		if key[K_RIGHT]:
			self.rect.centerx += self.velocity
		if key[K_LEFT]:
			self.rect.centerx += -self.velocity
		if key[K_SPACE]:
			self.fireLaser()	
						
		self.rect.top = max(self.rect.top, 0)
		self.rect.bottom = min(self.rect.bottom, self.screenHeight)
		self.rect.left = max(self.rect.left, 0)
		self.rect.right = min(self.rect.right, self.screenWidth)

	def fireLaser(self):
                        self.laserTimer += 1
                        if self.laserTimer == self.laserSpeed:
				laserSprites.add(Laser(self.rect.center, self.screenHeight))
				self.laserTimer = 0


class Laser(pygame.sprite.Sprite):
	def __init__(self, position, screenHeight):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage('laser1.bmp')
		self.screenHeight = screenHeight
		self.rect.center = position

	def update(self):
		if self.rect.bottom < 0:
			self.kill()
		else:
			self.rect.move_ip(0, -18)	

if __name__ == "__main__":
	game = Game()
	game.mainLoop()

