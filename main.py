from helpers import *

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
		self.SPWNASTEROID = pygame.USEREVENT + 4
		self.STAGEONE = pygame.USEREVENT + 5
		self.STAGETWO = pygame.USEREVENT + 6
		self.STAGETHREE = pygame.USEREVENT + 7

	def loadSprites(self):
		global laserSprites
		global enemyLaserSprites
		global bombSprites
		self.player = Player(self.width, self.height)
		self.playerSprites = pygame.sprite.RenderPlain((self.player))
		self.enemySprites = pygame.sprite.RenderPlain()
		self.debrisSprites = pygame.sprite.RenderPlain()
		laserSprites = pygame.sprite.RenderPlain()
		enemyLaserSprites = pygame.sprite.RenderPlain()
		bombSprites = pygame.sprite.RenderPlain()

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
				self.spawnGruntFormation(5, random.randint(0, 2))
			if event.type == self.SPWNBOMBER:
				self.spawnBomber()
			if event.type == self.SPWNASTEROID:
				self.spawnAsteroid()

			# Stage Events
			if event.type == self.STAGEONE:
				self.stageOne()
			if event.type == self.STAGETWO:
				self.stageTwo()
			if event.type == self.STAGETHREE:
				self.stageThree()

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
		self.enemySprites.draw(self.screen)
		self.debrisSprites.draw(self.screen)
		laserSprites.draw(self.screen)
		enemyLaserSprites.draw(self.screen)

		self.playerSprites.update()
		self.enemySprites.update()
		self.debrisSprites.update()
		laserSprites.update()
		enemyLaserSprites.update()

		pygame.display.flip()

	# Define Stages
        def queueStageEvents(self):
                pygame.time.set_timer(self.STAGEONE, 1000)
                #pygame.time.set_timer(self.STAGETWO, 30000)
                #pygame.time.set_timer(self.STAGETHREE, 60000)


	def stageOne(self):
		print("STAGE 1. GO!")
		pygame.time.set_timer(self.STAGEONE, 0)
		#pygame.time.set_timer(self.SPWNGRUNT, 1300)
		pygame.time.set_timer(self.SPWNGRUNTFORM, 3000)

	def stageTwo(self):
		print("STAGE 2. GO!")
		pygame.time.set_timer(self.STAGETWO, 0)
		pygame.time.set_timer(self.SPWNGRUNT, 300)
		pygame.time.set_timer(self.SPWNGRUNTFORM, 2000)
		pygame.time.set_timer(self.SPWNBOMBER, 2000)
		self.player.powerup = "spray"

	def stageThree(self):
                pygame.time.set_timer(self.STAGETHREE, 0)
                pygame.time.set_timer(self.SPWNGRUNT, 500)
                pygame.time.set_timer(self.SPWNASTEROID, 1200)
                pygame.time.set_timer(self.SPWNGRUNTFORM, 6000)
                pygame.time.set_timer(self.SPWNBOMBER, 3000)
                self.player.powerup = "none"

	def mainLoop(self):
		self.clock = pygame.time.Clock()
		self.queueStageEvents()
		self.loadSprites()
		while 1:
			self.clock.tick(self.framerate)
			self.getEvents()
			self.draw()
			self.collisionCheck()

	def spawnAsteroid(self):
                graphics = 'asteroid.png'
                xvelocity = random.randint(-1, 1)
                yvelocity = random.randint(2, 3)
                xposition = random.randint(50, 350)
                yposition = 0
                self.debrisSprites.add(Debris(xposition, yposition, xvelocity, yvelocity, graphics))

        def spawnLaser(self):
                graphics = 'homing-laser.png'
                xposition = 300
                yposition = 400
                enemyLaserSprites.add(HomingLaser(xposition, yposition, graphics, self.player.rect.centerx, self.player.rect.centery))

	def spawnBomber(self):
		graphics = ['bomber1.png', 'bomb1.png']
		projectile = "bombs"
		yvelocity = 0
		yposition = random.randint(50, 350)
		direction = random.randint(0, 1)
		if direction == 0:
			xvelocity = random.randint(2, 3)
			xposition = 0
		if direction == 1:
			xvelocity = random.randint(-3, -2)
			xposition = 400
		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, True, "single"))

	def spawnGrunt(self):
		graphics = ['grunt1.gif', 'laser1.bmp']
		projectile = "lasers"
		xvelocity = 0
		yvelocity = 3
		xposition = random.randint(50, 350)
		yposition = 0
		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, True, "single"))

	def spawnGruntFormation(self, amount, formation):
		graphics = ['grunt2.png', 'laser1.bmp']
		projectile = "lasers"
		xvelocity = 0
		yvelocity = 3

		# Back-to-Back Formation
		if formation == 0:
			distance = -35
			xposition = random.randint(50, 350)
			yposition = distance
			i = 0
			while i <= amount:
				yposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, False, "spray"))
				i += 1

		# Side-to-Side Formation
		if formation == 1:
			distance = 55
			xposition = 5
			yposition = -10
			i = 0
			while i <= amount:
				xposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, True, "spray"))
				i += 1

		# Slash Formation			
                if formation == 2:
                        distance = 50
                        xposition = 25
                        yposition = -10
                        i = 0
                        while i <= amount:
                                xposition += distance
				yposition -= distance
                                self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, True, "spray"))
                                i += 1

	def collisionCheck(self):
		pygame.sprite.groupcollide(self.enemySprites, laserSprites, 1, 1)
		pygame.sprite.groupcollide(self.enemySprites, self.debrisSprites, 1, 0)
		pygame.sprite.groupcollide(laserSprites, self.debrisSprites, 1, 0)
		pygame.sprite.groupcollide(enemyLaserSprites, self.debrisSprites, 1, 0)

		if pygame.sprite.groupcollide(self.enemySprites, self.playerSprites, 1, 1):
			self.player.reset()
			self.playerSprites = pygame.sprite.RenderPlain((self.player))

		if pygame.sprite.groupcollide(enemyLaserSprites, self.playerSprites, 1, 1):
			self.player.reset()
			self.playerSprites = pygame.sprite.RenderPlain((self.player))

                if pygame.sprite.groupcollide(self.debrisSprites, self.playerSprites, 1, 1):
                        self.player.reset()
                        self.playerSprites = pygame.sprite.RenderPlain((self.player))

class Player(pygame.sprite.Sprite):
	def __init__(self, screenWidth, screenHeight):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage('ship1.bmp')
		self.projectile = 'laser1.bmp'
		self.rect.centerx = 200
		self.rect.centery = 535
		self.velocity = 3
		self.yLaserVelocity = -18
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.powerup = None

	def flyUp(self):
		self.rect.centery += -self.velocity

	def flyDown(self):
		self.rect.centery += self.velocity

	def flyLeft(self):
		self.rect.centerx += -self.velocity

	def flyRight(self):
		self.rect.centerx += self.velocity

	def checkRestrictions(self):	
                self.rect.top = max(self.rect.top, 0)
                self.rect.bottom = min(self.rect.bottom, self.screenHeight)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, self.screenWidth)

	def update(self):
		self.checkRestrictions()

	def fireLaser(self):
		if self.powerup == None:
			laserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.projectile))
		elif self.powerup == "spray":
			laserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.projectile))
			laserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, -3, self.projectile))
			laserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 3, self.projectile))

	def reset(self):
                self.rect.centerx = 200
                self.rect.centery = 535

class Projectile(pygame.sprite.Sprite):
	def __init__(self, position, yvelocity, xvelocity, graphics):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = loadImage(graphics)
		self.rect.center = position
		self.yvelocity = yvelocity
		self.xvelocity = xvelocity

	def update(self):
		if self.rect.bottom < 0:
			self.kill()
		else:
			self.rect.move_ip(self.xvelocity, self.yvelocity)	
	
class Debris(pygame.sprite.Sprite):
	def __init__(self, xposition, yposition, xvelocity, yvelocity, graphics):
		pygame.sprite.Sprite.__init__(self)
		self.graphics = graphics
		self.image, self.rect = loadImage(self.graphics)
		self.rect.centerx = xposition
		self.rect.centery = yposition
		self.xvelocity = xvelocity
		self.yvelocity = yvelocity

	def float(self):
                if self.rect.top > 600:
                        self.kill()
                else:
                        self.rect.move_ip(self.xvelocity, self.yvelocity)

	def update(self):
		self.float()

class Grunt(pygame.sprite.Sprite):
	def __init__(self, xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquipped, fireType):
		pygame.sprite.Sprite.__init__(self)
		self.graphics = graphics
		self.image, self.rect = loadImage(self.graphics[0])
		self.rect.centerx = xposition
		self.rect.centery = yposition
		self.xvelocity = xvelocity
		self.yvelocity = yvelocity
		self.projectile = projectile
		self.shooting = False
		self.yLaserVelocity = (self.yvelocity + 1)
		self.weaponSpeed = 80
		self.weaponCharge = 0
		self.weaponEquipped = weaponEquipped
		self.fireType = fireType

		if self.weaponEquipped:
			if self.projectile == "lasers":
				self.decideIfShooting()
			if self.projectile == "bombs":
				self.weaponSpeed = random.randint(25, 30)
				self.shooting = True

	def decideIfShooting(self):
		i = random.randint(0, 10)
		if i > 6:
			self.shooting = True

	def prepareWeapon(self):
                if self.shooting == True:
                        self.weaponCharge += 1

                        if self.weaponCharge == self.weaponSpeed:
				if self.fireType == "single":
					self.yLaserVelocity += 2
                                	self.fireSingle()
				elif self.fireType == "spray":
					self.yLaserVelocity += 1
					self.fireSpray()

                                self.weaponCharge = 0
				self.yLaserVelocity = self.yvelocity

        def fireSingle(self):
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.graphics[1]))

	def fireSpray(self):
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.graphics[1]))
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 2, self.graphics[1]))
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, -2, self.graphics[1]))
	
	def fly(self):
                if self.rect.top > 600 or self.rect.right < -20 or self.rect.left > 420:
                        self.kill()
                else:
                        self.rect.move_ip(self.xvelocity, self.yvelocity)

	def update(self):
		self.fly()
		self.prepareWeapon()

if __name__ == "__main__":
	game = Game()
	game.mainLoop()

