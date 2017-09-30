from helpers import *

class Game(object):
	def __init__(self, width = 400, height = 600):
		pygame.init()
		self.width = width
		self.height = height
		self.framerate = 60
		self.screen = pygame.display.set_mode((self.width, self.height))

		# User Event Declaration
		self.SPWNGRUNT = pygame.USEREVENT + 0
		self.SPWNGRUNTFORM = pygame.USEREVENT + 1
		self.SPWNBOMBER = pygame.USEREVENT + 2
		self.SPWNASTEROID = pygame.USEREVENT + 3
		self.STAGEONE = pygame.USEREVENT + 4
		self.STAGETWO = pygame.USEREVENT + 5
		self.STAGETHREE = pygame.USEREVENT + 6
		self.SPWNBATTLECRUISER = pygame.USEREVENT + 7

        def mainLoop(self):
                self.clock = pygame.time.Clock()
                self.queueStageEvents()
                self.loadSprites()
                while 1:
                        self.clock.tick(self.framerate)
                        self.getEvents()
                        self.draw()
                        self.collisionCheck()

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
				self.spawnGruntFormation(5, random.randint(0, 3))
			if event.type == self.SPWNBOMBER:
				self.spawnBomber()
			if event.type == self.SPWNASTEROID:
				self.spawnAsteroid()
			if event.type == self.SPWNBATTLECRUISER:
				self.spawnBattlecruiser()

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
		pygame.time.set_timer(self.SPWNGRUNT, 1200)
		pygame.time.set_timer(self.SPWNGRUNTFORM, 13000)
		pygame.time.set_timer(self.SPWNBOMBER, 20000)

	def stageTwo(self):
		print("STAGE 2. GO!")
		pygame.time.set_timer(self.STAGETWO, 0)
		pygame.time.set_timer(self.SPWNGRUNT, 0)
		pygame.time.set_timer(self.SPWNGRUNTFORM, 2500)

	def stageThree(self):
		print("STAGE 3. GO!")
                pygame.time.set_timer(self.STAGETHREE, 0)
                pygame.time.set_timer(self.SPWNGRUNTFORM, 3000)
                pygame.time.set_timer(self.SPWNBOMBER, 8000)

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
                weaponEquiped = True
                weaponStyle = "single"
                movementStyle = "straight"

		if direction == 0:
			xvelocity = random.randint(2, 3)
			xposition = 0
		if direction == 1:
			xvelocity = random.randint(-3, -2)
			xposition = 400
	
		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))

	def spawnBattlecruiser(self):
		graphics = ['battlecruiser.png', 'laser1.bmp']
		projectile = "lasers"
		xvelocity = 0
		yvelocity = -1
		xposition = random.randint(50, 350)
		yposition = 680
		weaponEquiped = True
		movementStyle = "straight"

		if random.randint(0, 1) == 0:
			weaponStyle = "single"
		else:
			weaponStyle = "spray"

		self.enemySprites.add(Battlecruiser(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))

	def spawnGrunt(self):
		graphics = ['grunt1.gif', 'laser1.bmp']
		projectile = "lasers"
		xvelocity = 0
		yvelocity = random.randint(2, 3)
		xposition = random.randint(50, 320)
		yposition = -50
		weaponEquiped = True
		movementStyle = "straight"

		if random.randint(0, 1) == 0:
			weaponStyle = "single"
		else:
			weaponStyle = "spray"

		self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))

		amount = random.randint(0, 2)
		if amount == 1:
			self.enemySprites.add(Grunt((xposition + 35), yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
		elif amount == 2:
			self.enemySprites.add(Grunt((xposition + 35), yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
			self.enemySprites.add(Grunt((xposition + 70), yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))

	def spawnGruntFormation(self, amount, formation):
		graphics = ['grunt2.png', 'laser1.bmp']
		projectile = "lasers"
		xvelocity = 0
		yvelocity = 3
		#formation = 7

		# Back-to-Back Formation
		if formation == 0:
			distance = -35
			xposition = random.randint(50, 300)
			yposition = distance
			weaponEquiped = False
			weaponStyle = "single"
			movementStyle = "straight"
			i = 0
			while i <= amount:
				yposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))				
				#self.enemySprites.add(Grunt((xposition + 35), yposition, (xvelocity), yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
				i += 1

		# Back-to-Back Formation
		if formation == 1:
			distance = -35
			xposition = distance
			yposition = random.randint(50, 400)
			xvelocity = 3
			yvelocity = 0
			weaponEquiped = True
			weaponStyle = "single"
			movementStyle = "straight"
			i = 0
			while i <= amount:
				xposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))				
				#self.enemySprites.add(Grunt((xposition + 35), yposition, (xvelocity), yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
				i += 1

		# Side-to-Side Formation
		if formation == 2:
			distance = 55
			xposition = 5
			yposition = -10
                        weaponEquiped = True
                        weaponStyle = "spray"
                        movementStyle = "straight"
			i = 0
			while i <= amount:
				xposition += distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
				i += 1

		# Slash Formation			
                if formation == 3:
                        distance = 50
                        xposition = 25
                        yposition = -10
                        weaponEquiped = True
                        weaponStyle = "spray"
                        movementStyle = "straight"
                        i = 0
                        while i <= amount:
                                xposition += distance
				yposition -= distance
				self.enemySprites.add(Grunt(xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquiped, weaponStyle, movementStyle))
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

class Battlecruiser(pygame.sprite.Sprite):
	def __init__(self, xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquipped, fireType, movementStyle):
		pygame.sprite.Sprite.__init__(self)
		self.graphics = graphics
		self.image, self.rect = loadImage(self.graphics[0])
		self.rect.centerx = xposition
		self.rect.centery = yposition
		self.xposition = xposition
		self.yposition = yposition
		self.xvelocity = xvelocity
		self.yvelocity = yvelocity
		self.projectile = projectile
		self.shooting = False
		self.yLaserVelocity = (self.yvelocity)
		self.weaponSpeed = 150
		self.weaponCharge = 0
		self.weaponEquipped = weaponEquipped
		self.fireType = fireType
		self.movementStyle = movementStyle
		self.step = 0
		self.amplitude = 50

	def fly(self):
                #if self.rect.top > 600 or self.rect.right < -20 or self.rect.left > 420:
                #        self.kill()

                if self.movementStyle == "straight":
                        self.rect.move_ip(self.xvelocity, self.yvelocity)

	def fire(self):
		self.weaponCharge += 1

		if self.weaponCharge == self.weaponSpeed:
			#self.yLaserVelocity -= 2

			enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity - 3), 0, self.graphics[1]))
			enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity - 2), -2, self.graphics[1]))
                        enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity - 2), 2, self.graphics[1]))
			enemyLaserSprites.add(Projectile(self.rect.center, 0, 2, self.graphics[1]))
			enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity + 4), 0, self.graphics[1]))
                        enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity + 2), -2, self.graphics[1]))
                        enemyLaserSprites.add(Projectile(self.rect.center, (self.yLaserVelocity + 2), 2, self.graphics[1]))
			enemyLaserSprites.add(Projectile(self.rect.center, 0, -2, self.graphics[1]))

			self.weaponCharge = 0
			self.yLaserVelocity = self.yvelocity

	def update(self):
		self.fly()
		self.fire()


class Grunt(pygame.sprite.Sprite):
	def __init__(self, xposition, yposition, xvelocity, yvelocity, graphics, projectile, weaponEquipped, fireType, movementStyle):
		pygame.sprite.Sprite.__init__(self)
		self.graphics = graphics
		self.image, self.rect = loadImage(self.graphics[0])
		self.rect.centerx = xposition
		self.rect.centery = yposition
		self.xposition = xposition
		self.yposition = yposition
		self.xvelocity = xvelocity
		self.yvelocity = yvelocity
		self.projectile = projectile
		self.shooting = False
		#self.yLaserVelocity = (self.yvelocity + 1)
		self.yLaserVelocity = 3
		self.weaponSpeed = 80
		self.weaponCharge = 0
		self.weaponEquipped = weaponEquipped
		self.fireType = fireType
		self.movementStyle = movementStyle
		self.step = 0
		self.amplitude = 50
		self.backup = random.randint(0, 1)

		if self.weaponEquipped:
			if self.projectile == "lasers":
				self.decideIfShooting()
			if self.projectile == "bombs":
				self.yLaserVelocity = 3
				self.weaponSpeed = 30
				self.shooting = True

	def decideIfShooting(self):
		if self.backup > 0:
			self.shooting = False
			return

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
		self.yLaserVelocity = 4
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.graphics[1]))

	def fireSpray(self):
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 0, self.graphics[1]))
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, 2, self.graphics[1]))
                enemyLaserSprites.add(Projectile(self.rect.center, self.yLaserVelocity, -2, self.graphics[1]))
	
	def fly(self):
                if self.rect.top > 600 or self.rect.right < -300 or self.rect.left > 420:
                        self.kill()

                elif self.movementStyle == "straight":
                        self.rect.move_ip(self.xvelocity, self.yvelocity)

		elif self.movementStyle == "sine":
			print("Y Position: %d" % self.rect.centery)
			print("X Position: %d" % self.rect.centerx)
			xposition = 1 * math.sin(self.step) * self.amplitude
			self.yposition += 3
			self.rect.center = (int(xposition) + 200 + 20, int(self.yposition))
			#self.rect.move_ip(self.xvelocity, self.yvelocity)
			#self.step += 0.008
			self.step += 0.09
			self.step %= 2 * math.pi

                elif self.movementStyle == "inAndOut":
                        print("Y Position: %d" % self.rect.centery)
                        print("X Position: %d" % self.rect.centerx)
			self.amplitude = 200
                        xposition = 1 * math.sin(self.step) * self.amplitude
                        #self.yposition += 3
                        self.rect.center = (int(xposition), int(self.yposition) + 200 + 20)
                        #self.rect.move_ip(self.xvelocity, self.yvelocity)
                        #self.step += 0.008
                        self.step += 0.03
                        self.step %= 2 * math.pi

	def update(self):
		self.fly()
		self.prepareWeapon()
		
		if self.backup > 0 and self.rect.centery > 400:
			self.xvelocity = random.randint(-2, 2)
			self.yvelocity = -2
			self.yLaserVelocity = 3
			self.shooting = True
			self.weaponSpeed = 43
			self.fireType = "single"			

if __name__ == "__main__":
	game = Game()
	game.mainLoop()

