from helpers import *

# To do:
# -Add more control over what types of enemies fire and the frequency of it
# -Manage event flow based on player score or time
# -Add collisions
# -Add animations for player, enemies and projectiles
# -Add advanced enemy movements (waving, circling)
# -Add sound
# -Add title screen
# -Add pause function
# -Add player health
# -Add player score
# -Add boss events for every certain amount of points
# -Add background graphics
# -Add ability to upload highscore to cloud
# -Look into multiplayer (local and network)
# -Look into using a controller/joystick 

class Game(object):
	def __init__(self, width = 400, height = 600):
		pygame.init()
		self.width = width
		self.height = height
		self.framerate = 60
		self.screen = pygame.display.set_mode((self.width, self.height))

		# User Event Declaration
		self.SPWNGRUNT = pygame.USEREVENT + 1
		self.SPWNGRUNTFORM = pygame.USEREVENT + 2
		self.SPWNBOMBER = pygame.USEREVENT + 3
		self.STAGEONE = pygame.USEREVENT + 4
		self.STAGETWO = pygame.USEREVENT + 5

	def loadSprites(self):
		global laserSprites
		global enemyLaserSprites
		self.player = Player(self.width, self.height)
		self.playerSprites = pygame.sprite.RenderPlain((self.player))
		self.enemySprites = pygame.sprite.RenderPlain()
		laserSprites = pygame.sprite.RenderPlain()
		enemyLaserSprites = pygame.sprite.RenderPlain()

	def getEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					self.player.fireLaser()

			# Enemy Spawn Events
			if event.type == self.SPWNGRUNT:
				self.spawnGrunt()
			if event.type == self.SPWNGRUNTFORM:
				self.spawnGruntFormation(5, random.randint(0, 1))
			if event.type == self.SPWNBOMBER:
				self.spawnBomber()

			# Stage Events
			if event.type == self.STAGEONE:
				self.stageOne()
			if event.type == self.STAGETWO:
				self.stageTwo()

		# Player Movement Events
		key = pygame.key.get_pressed()
		if key[K_UP]:
			self.player.flyUp()
		if key[K_DOWN]:
			self.player.flyDown()
		if key[K_LEFT]:
			self.player.flyLeft()
		if key[K_RIGHT]:
			self.player.flyRight()

	def draw(self):
		self.screen.fill((0, 0, 0))
		self.playerSprites.draw(self.screen)
		self.playerSprites.update()
		self.enemySprites.draw(self.screen)
		self.enemySprites.update()
		laserSprites.draw(self.screen)
		laserSprites.update()
		enemyLaserSprites.draw(self.screen)
		enemyLaserSprites.update()
		pygame.display.flip()

	# Define Stages
	def stageOne(self):
		print("STAGE 1. GO!")
		pygame.time.set_timer(self.STAGEONE, 0)
		pygame.time.set_timer(self.SPWNGRUNT, 900)
		pygame.time.set_timer(self.SPWNBOMBER, 10000)
		pygame.time.set_timer(self.SPWNGRUNTFORM, 13000)

	def stageTwo(self):
		print("STAGE 2. GO!")
		pygame.time.set_timer(self.STAGETWO, 0)
		pygame.time.set_timer(self.SPWNGRUNT, 800)

	def queueStageEvents(self):
		pygame.time.set_timer(self.STAGEONE, 1200)
		#pygame.time.set_timer(self.STAGETWO, 30000)

	def mainLoop(self):
		self.clock = pygame.time.Clock()
		self.queueStageEvents()
		self.loadSprites()
		while 1:
			self.clock.tick(self.framerate)
			self.getEvents()
			self.draw()
			self.collisionCheck()

	def spawnBomber(self):
		graphics = 'bomber1.png'
		projectile = 'bomb1.png'
		yvelocity = 0
		yposition = random.randint(50, 350)
		direction = random.randint(0, 1)
		if direction == 0:
			xvelocity = random.randint(2, 3)
			xposition = 0
		if direction == 1:
			xvelocity = random.randint(-3, -2)
			xposition = 400
		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile))

	def spawnGrunt(self):
		graphics = 'grunt1.gif'
		projectile = 'laser1.bmp'
		xvelocity = 0
		yvelocity = random.randint(3, 4)
		xposition = random.randint(50, 350)
		yposition = 0
		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile))

	def spawnGruntFormation(self, amount, formation):
		graphics = 'grunt2.png'
		projectile = 'laser1.bmp'
		xvelocity = 0
		yvelocity = random.randint(3, 4)

		# Back-to-Back Formation
		if formation == 0:
			distance = -35
			xposition = random.randint(50, 350)
			yposition = distance
			i = 0
			while i <= amount:
				yposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile))
				i += 1

		# Side-to-Side Formation
		if formation == 1:
			distance = 30
			xposition = random.randint(25, 200)
			yposition = -10
			i = 0
			while i <= amount:
				xposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile))
				i += 1			

	def collisionCheck(self):
		pygame.sprite.groupcollide(self.enemySprites, laserSprites, 1, 1)

class Player(pygame.sprite.Sprite):
	def __init__(self, screenWidth, screenHeight):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage('ship1.bmp')
		self.projectile = 'laser1.bmp'
		self.rect.centerx = 200
		self.rect.centery = 535
		self.velocity = 3
		self.laserVelocity = -18
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

	def flyUp(self):
		self.rect.centery += -self.velocity

	def flyDown(self):
		self.rect.centery += self.velocity

	def flyLeft(self):
		self.rect.centerx += -self.velocity

	def flyRight(self):
		self.rect.centerx += self.velocity

	def update(self):
		self.rect.top = max(self.rect.top, 0)
		self.rect.bottom = min(self.rect.bottom, self.screenHeight)
		self.rect.left = max(self.rect.left, 0)
		self.rect.right = min(self.rect.right, self.screenWidth)

	def fireLaser(self):
		laserSprites.add(Projectile(self.rect.center, self.laserVelocity, self.projectile))

class Projectile(pygame.sprite.Sprite):
	def __init__(self, position, velocity, graphics):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage(graphics)
		self.rect.center = position
		self.velocity = velocity

	def update(self):
		if self.rect.bottom < 0:
			self.kill()
		else:
			self.rect.move_ip(0, self.velocity)	

class Grunt(pygame.sprite.Sprite):
	def __init__(self, xposition, yposition, xvelocity, yvelocity, graphics, projectile):
		pygame.sprite.Sprite.__init__(self)
		self.graphics = graphics
		self.image, self.rect = loadImage(self.graphics)
		self.rect.centerx = xposition
		self.rect.centery = yposition
		self.xvelocity = xvelocity
		self.yvelocity = yvelocity
		self.projectile = projectile
		self.laserVelocity = (self.yvelocity + 3)
		self.laserSpeed = 50
		self.laserCharge = 0
		self.shooting = False
		self.decideIfShooting()

	def decideIfShooting(self):
		laser = random.randint(0, 10)
		if laser > 6:
			self.shooting = True

        def fireLaser(self):
                enemyLaserSprites.add(Projectile(self.rect.center, self.laserVelocity, self.projectile))

	def update(self):
		if self.rect.top > 600:
			self.kill()
		else:
			self.rect.move_ip(self.xvelocity, self.yvelocity)

		if self.shooting == True:
			self.laserCharge += 1
			
			if self.laserCharge == self.laserSpeed:
				self.fireLaser()
				self.laserCharge = 0

if __name__ == "__main__":
	game = Game()
	game.mainLoop()

