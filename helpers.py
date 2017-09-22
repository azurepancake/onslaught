import os, sys, random, pygame, math
from pygame.locals import *

def loadImage(name, colorkey=None):
	fullname = os.path.join('graphics', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message
	image = image.convert_alpha()
	if colorkey is not None:
		if colorkey == -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()
